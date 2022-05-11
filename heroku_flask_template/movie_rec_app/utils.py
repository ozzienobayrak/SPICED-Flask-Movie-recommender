"""
UTILS 
- Helper functions to use for your recommender funcions, etc
- Data: import files/models here e.g.
    - movies: list of movie titles and assigned cluster
    - ratings
    - user_item_matrix
    - item-item matrix 
- Models:
    - nmf_model: trained sklearn NMF model
"""
import pandas as pd
import numpy as np
from fuzzywuzzy import process
from scipy.sparse import csr_matrix
from sklearn.decomposition import NMF
import pickle
import sklearn
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import pairwise
import os


movies=pd.read_csv('movie_rec_app/data/movies.csv', sep=",", index_col='movieId')
ratings=pd.read_csv('movie_rec_app/data/ratings.csv', sep=",", index_col='movieId')

#DATA PROCESSING for ratings: Filtering the movies seen by less than 20 users
usercount=ratings.groupby('movieId')['userId'].count()
popular=usercount.loc[usercount>20]
ratings =ratings.loc[popular.index]
ratings=ratings.reset_index()

def user_item_matrix ():
    user_item_matrix = csr_matrix((ratings['rating'], (ratings['userId'], ratings['movieId'])))
    return user_item_matrix

def match_movie_title(input_title, movie_titles):
    """
    Matches inputed movie title to existing one in the list with fuzzywuzzy
    """
    matched_title = process.extractOne(input_title, movie_titles)[0]

    return matched_title

def print_movie_titles(movie_titles):
    """
    Prints list of movie titles in cli app
    """    
    for movie_title in movie_titles:
        print(f'> {movie_title}')
    pass


def create_user_vector(user_rating, movies):
    """
    Convert dict of user_ratings to a user_vector
    """       
    # generate the user vector
    data = list(user_rating.values())   # the ratings of the new user
    row_ind = [0]*len(data)       # use just a single row 0 for this user 
    col_ind = list(user_rating.keys())  # the columns (=movieId) of the ratings
    data, row_ind, col_ind
    user_vec = csr_matrix((data, (row_ind, col_ind)), shape=(1, R.shape[1]))
    return user_vector


def lookup_movieId(movies, movieId):
    """
    Convert output of recommendation to movie title
    """
    # match movieId to title
    movies = movies.reset_index()
    boolean = movies["movieid"] == movieId
    movie_title = list(movies[boolean]["title"])[0]
    return movie_title

    return movie_title

if __name__ == "__main__":
    user_rating = {
        "four rooms": 5,
        "sudden death": 3,
        "othello": 4,
        "nixon": 3,
        "Golden eye": 1,
        "total eclipse": 5,
        "nadja": 3
    }
    print(create_user_vector(user_rating, movies))