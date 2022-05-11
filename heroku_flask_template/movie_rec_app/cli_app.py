# example input of web application
from recommender import recommend_most_popular, recommend_random
from utils import movies, ratings, print_movie_titles


user_rating = {
    'the lion king': 5,
    'terminator': 5,
    'star wars': 2
}
# Please make sure that you output the ids and 
# then modify the lookupmovieId to give the user the titles
### Terminal recommender:

print('>>>> Here are some movie recommendations for you:')
print('')
print('Random movies')
movie_ids = recommend_random(movies, user_rating)
print(movie_ids)
    #movie_titles = [lookup_movieId(movies, id) for id in movie_ids]
    #print_movie_titles(movie_titles)
print('')   

print("recommend most popular")
print_movie_titles(recommend_most_popular(user_rating, movies, ratings=None, k=3))
