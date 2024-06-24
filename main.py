from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, FloatField, IntegerField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

dotenv = load_dotenv(
    dotenv_path=".env",
    verbose=True)


TMDB_HEADERS = {
        "accept": "application/json",
        "Authorization": os.getenv("TMDB_AUTH")
    }


class EditForm(FlaskForm):
    rating = FloatField('New Rating', validators=[DataRequired()])
    review = StringField('New Review', validators=[DataRequired()])
    submit = SubmitField(label="Done")

class FindMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top10-movies-collection.db"

# initialize the app with the extension
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Movie {self.title}>'



def search_movie(search_title):
    params = {'query': search_title, 'include_adult': 'False', 'language': 'en-US', 'page': 1}
    response = requests.get(url="https://api.themoviedb.org/3/search/movie", headers=TMDB_HEADERS, params=params)
    search_list = response.json()['results']
    return search_list



@app.route("/")
def home():
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html", list=all_movies)


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    form = EditForm()
    movie_id = request.args.get('id')
    if form.validate_on_submit():
    # if request.method == "POST":
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
        movie_to_update.rating = form.rating.data
        movie_to_update.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    else:
        movie = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
        m_title = movie.title
        m_description = movie.description
        m_rating = movie.rating
        return render_template('edit.html', form=form, num=movie_id, title=m_title, rating=m_rating, desc=m_description)


@app.route("/delete", methods=['GET'])
def delete():
    if request.method == "GET":
        movie_id = request.args.get('id')
        movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect(url_for('home'))


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = FindMovieForm()
    movie_to_search = form.title.data
    # this is the action when the movie title is being search. It will populate select.html with a serch list.
    if form.validate_on_submit():
        list = search_movie(movie_to_search)
        return render_template('select.html', list=list)
    else:
        return render_template('add.html', form=form)


@app.route("/find")
def get_movie_details():
    movie_id = request.args.get('id')
    if movie_id:
    ## Initiate API request to get the movie details
        response = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}", headers=TMDB_HEADERS)
        movie = response.json()
        new_movie = Movie(title=movie['original_title'],
                          year=movie['release_date'].split("-")[0],
                          description=movie['overview'],
                          rating=None,
                          ranking=None,
                          review="",
                          img_url=f"https://image.tmdb.org/t/p/original{movie['poster_path']}"
                          )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('edit', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
