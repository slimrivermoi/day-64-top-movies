import requests

###### SEARCH MOVIE ##########

#
# url = "https://api.themoviedb.org/3/movie/624860?language=en-US"
#
# headers = {
#     "accept": "application/json",
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1YTBiNTdmYzcwOTcxMTAwMjM3NWMxZTRjYTNkMzM2ZSIsInN1YiI6IjY2NzQ3NjhkODM1MTVkN2UxMmZjNjAyNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.x3TlruPr7Jn2q71ekZsYTQ3G4GyQDGgxzx2yvkWYWak"
# }
#
# response = requests.get(url, headers=headers)
#
# print(response.text)

### REVISED FOR SEARCH MOVIE ###
# url_2 = "https://api.themoviedb.org/3/search/movie"
# params = {
#     'query': 'The Matrix',
#     'include_adult':'False',
#     'language':'en-US',
#     'page':1
#           }
#
# headers = {
#     "accept": "application/json",
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1YTBiNTdmYzcwOTcxMTAwMjM3NWMxZTRjYTNkMzM2ZSIsInN1YiI6IjY2NzQ3NjhkODM1MTVkN2UxMmZjNjAyNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.x3TlruPr7Jn2q71ekZsYTQ3G4GyQDGgxzx2yvkWYWak"
# }
#
# response2 = requests.get(url_2, headers=headers, params=params)
#
# list = response2.json()['results']


############### get movie detail #########

url = "https://api.themoviedb.org/3/movie/"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1YTBiNTdmYzcwOTcxMTAwMjM3NWMxZTRjYTNkMzM2ZSIsInN1YiI6IjY2NzQ3NjhkODM1MTVkN2UxMmZjNjAyNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.x3TlruPr7Jn2q71ekZsYTQ3G4GyQDGgxzx2yvkWYWak"
}

movie_id = 624860

params = {'language':'en-US'}

response = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}", headers=headers, params=params)
movie = response.json()
print(movie['original_title'])    #title
print(movie['release_date'].split("-")[0])  #year
print(movie['overview']) #description
print(movie['poster_path'])  #img_url

