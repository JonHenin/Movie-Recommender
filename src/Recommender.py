#%%
import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from pathlib import Path


# File Variables
base_path = Path('data/')
file_movies = base_path / 'movies.csv'
file_ratings = base_path / 'ratings.csv'

movies = pd.read_csv(file_movies)
users = pd.read_csv(file_ratings)
df = users.join(movies.set_index('movieId'), on=['movieId'])

# Pivot database to get a list of users and their movie ratings.
ratings = pd.pivot_table(df, values='rating', index=['userId'],
                       columns=['title'], fill_value=0).reset_index(drop=True)

#%%
#test_ratings = [
#    ('GoldenEye (1995)', 5),
#    ('Broken Arrow (1996)', 2),
#    ('Muppet Treasure Island (1996)', 3),
#    ('Crimson Tide (1995)', 4),
#    ('Waterworld (1995)', 4)
#]

def vector_ratings(list_of_ratings):
    """Take a list of ratings and turn it into a sparse array

    Args:
        list_of_ratings (list): The list of movies and scores entered by user

    Returns:
        [sparse array]: A sparse array of ratings
    """
    my_vector = [0 for x in range(len(ratings.columns))]
    for movie in list_of_ratings:
        inp = ratings.columns.get_loc(movie[0])
        my_vector[inp] = movie[1]

    return csr_matrix(np.array(my_vector))

def compare_vectors(user_ratings):
    """Compare the overall list of user ratings against the user ratings and return
    a list of users who match the closest to ratings.

    Args:
        user_ratings (list): The list of movies and scores entered by user

    Returns:
        [series]: A series of users and their rankings in descending order
    """
    similarities = cosine_similarity(ratings.values, vector_ratings(user_ratings))
    ratings_matrix = pd.DataFrame(similarities)

    return ratings_matrix.sort_values(0, ascending=False)

def recommend_movies(user_ratings):
    """Takes the list of users and search through their movies to get recommendations
    for user.

    Args:
        user_ratings (list): The list of movies and scores entered by user
    """
    list_of_movies = [movie[0] for movie in user_ratings]
    movie_recommendations = []

    # Get a list of users in order of most like
    like_users = list(compare_vectors(user_ratings).index.values)

    # Create a new ratings dataset without the movies already ranked.
    ratings_remove = ratings[ratings.columns.difference(list_of_movies)]

    # Add number of movie recommendations equal to original number of movies rated.
    for user in like_users:
        user_movie_list = ratings_remove.loc[user].sort_values(ascending=False)
        for title, rating in user_movie_list.items():
            # Only return movies that are >= a rating of 4
            if rating >= 4:
                movie_recommendations.append(title)
                if len(movie_recommendations) == len(list_of_movies):
                    print("Your recommended movies:")
                    print("\n".join([str(x) for x in movie_recommendations]))
                    break
