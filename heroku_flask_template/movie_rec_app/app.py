from flask import Flask, render_template, request
from movie_rec_app.recommender import recommend_random, recommend_most_popular, recommend_with_NMF, recommend_with_user_similarity
from movie_rec_app.utils import movies, ratings, lookup_movieId, print_movie_titles, user_item_matrix

# construct our flask instance, pass name of module
app = Flask(__name__)

# example input of web application
user_rating = {
    'the lion king': 5,
    'terminator': 5,
    'star wars': 2
}

# route decorator for mapping urls to functions
@app.route('/')
def hello_world():
    # jinja is the templating engine
    return render_template('index.html', name='Beatiful people', movies=movies['title'].tolist(),
    methods=['Random', 'Popular Movies', 'NMF', 'Similar'])
    
# Random model: 
@app.route('/recommendations')
def recommendations():
    # read user input from url
    print(request.args)

    titles = request.args.getlist("title")
    rating = request.args.getlist("rating")
    method = request.args["method"]
    print(titles, rating, method)

    user_rating = dict(zip(titles, ratings))

    print(user_rating)

    #methods=['Random', 'Popular movies', 'NMF', 'Similar']
    if method=='Random':
        recs = recommend_random(user_rating, movies, k=5)
        return render_template('recommendations.html', recs=recs)
    elif method=='Popular Movies':
        recs = recommend_most_popular(user_rating, movies, ratings, k=5)
        return render_template('recommendations.html', recs=recs)
    elif method=='NMF':
        recs =recommend_with_NMF(movies, user_rating, k=5)
        return render_template('recommendations.html', recs=recs)
    elif method=='Similar':
        recs =recommend_with_user_similarity(movies, user_rating, k=5)
        return render_template('recommendations.html', recs=recs)


# only run the app if we are in the main module
if (__name__ == '__main__'):
    app.run(debug=True, port=5004)







