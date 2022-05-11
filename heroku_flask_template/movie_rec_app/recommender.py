"""
Contains various recommondation implementations
all algorithms return a list of movieids
"""

import pandas as pd
import random
from movie_rec_app.utils import match_movie_title


def recommend_random(user_rating, movies, k=5):
    """
    return k random unseen movies for user 
    (note: the version below also considers seen movies)
    """
    all_movies = list(movies['title'])
    random_movies = random.choices(all_movies,k=5)
    return random_movies


def recommend_most_popular(user_rating, movies, ratings, k=5):
    """
    return k movies from list of 50 best rated movies unseen for user
    """
    # filter for movies with more than 20 ratings and extract the index
    # popular_movies = movies
    popular_movies = movies.loc[~movies['title'].isin(user_rating.keys())]
    popular_movies = popular_movies.reset_index()
    popular_movies = ratings.groupby('movieId')['rating'].sum().sort_values(ascending = False)
    popular_movies = popular_movies.head(k).index
    popular_movies = movies.loc[popular_movies]['title'] 

    return popular_movies



def recommend_with_NMF(user_item_matrix, user_rating, k=5):
    """
    NMF Recommender
    INPUT
    - user_vector with shape (1, #number of movies)
    - user_item_matrix
    - trained NMF model

    OUTPUT
    - a list of movieIds
    """
    from sklearn.decomposition import NMF
    import numpy as np
    # initialization - impute missing values    
    # 55 hidden features (hyperparameter that you can play with-take 10 efor instance)
    model = NMF(n_components=55, init='nndsvd', max_iter=10000, tol=0.01, verbose=2) 

    # fit it to the user-item rating matrix
    model.fit(user_item_matrix)
    # transform user vector into hidden feature space
    P=model.transform(user_item_matrix)
    Q=model.components_
    # R -> encoding -> P -> decoding -> Rhat
    # inverse transformation
    R_hat=model.inverse_transform(model.transform(user_item_matrix))
    np.sqrt(np.sum(np.square(R-R_hat)))
    #save the model
    with open('./nmf_recommender.pkl', 'wb') as file:
            pickle.dump(model, file)
   #read the model 
    with open('./nmf_recommender.pkl', 'rb') as file:
            model = pickle.load(file)
    # build a dataframe
    
    # discard seen movies and sort the prediction
    scores = model.inverse_transform(model.transform(user_vec))
    scores=pd.Series(scores[0])
    scores[query.keys()] = 0
    scores = scores.sort_values(ascending=False)
    # return a list of movie ids
    recommendations = scores.head(10).index
    movies.set_index('movieId').loc[recommendations]
    movies.set_index('movieId').loc[query.keys()]
    return recommendations

    pass

def recommend_with_user_similarity(user_item_matrix, user_rating, k=5):

    # which metrics can we use for sparse matrics?
    sorted(sklearn.neighbors.VALID_METRICS_SPARSE['brute'])
    # initialize the unsupervised model
    model = NearestNeighbors(metric='cosine')
    # fit it to the user-item rating matrix
    model.fit(user_item_matrix)
    #save the model2
    with open('./distance_recommender.pkl', 'wb') as file:
        pickle.dump(model, file)
    #Read the model saved
    with open('./distance_recommender.pkl', 'rb') as file:
        model = pickle.load(file)
    # calculates the distances to all other users in the data!
    distances, userIds = model.kneighbors([user_vec], n_neighbors=10, return_distance=True)
    # sklearn returns a list of predictions - extract the first and only value of the list
    distances = distances[0]
    userIds = userIds[0]
    # only look at ratings for users that are similar!
    neighborhood = ratings.set_index('userId').loc[userIds]
    # averaging introduces bias for movies only seen by few users in the neighboorhood
    scores = neighborhood.groupby('movieId')['rating'].sum()
    allready_seen = scores.index.isin(query.keys())
    scores.loc[allready_seen] = 0
    scores = scores.sort_values(ascending=False)
    # get the movieIds of the top 10 entries
    recommendations = scores.head(10).index
    movies.set_index('movieId').loc[recommendations]
    return recommendations

    pass

