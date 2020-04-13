import pandas as pd
from pathlib import Path
from .Recommender import recommend_movies
from fuzzywuzzy import fuzz, process

base_path = Path('data/')
file_movies = base_path / 'movies.csv'

movies = pd.read_csv(file_movies)
my_movies = []

def list_of_movies():
    """Take an input string from a user and return a list of movies
    that are similar using fuzzy logic.

    Returns:
        [list]: list of movies
    """
    input_movie = input("Find a movie to rate: ")
    movie_choices = process.extract(input_movie, movies['title'], limit=100, scorer=fuzz.partial_ratio)
    return [movie for movie in movie_choices if movie[1] > 85]

def add_movies():
    """This is the main function called from main.  It keeps asking the user
    to add movies and rankings until 5 movies are scored.  Once 5 movies are
    scored you can either keep adding as many movies as you like or you can get
    a list of recommended movies.
    """
    while True:
        # Take a user input string and return a list of movies.
        listmovies = list_of_movies()

        # If No Movies returned search again.
        if len(listmovies) == 0:
            print("No movies returned. Try another search.")
            continue

        # If a movie is found:
        else:

            # Add a value to return back to search.
            listmovies.append(("I don't see what I'm looking for.", 0, 0))

            # Display list of Movies
            for i in range(len(listmovies)):
                print(f"{i+1}. {listmovies[i][0]}")

            # Get movie input from user
            addmovie = int(input("Type number of movie to add from list: ")) - 1

            # Do the following if they chose a movie, otherwise, ask again for a movie selection
            if addmovie + 1 != len(listmovies):
                # Get User to provide a score for the movie, add it to list and then print movies so far.
                input_rank = int(input(f"How much did you enjoy {listmovies[addmovie][0]} on a scale of 0 to 5? \n(0 - hated it, 5 - loved it): "))
                my_movies.append((listmovies[addmovie][0], input_rank))
                print("My List:")
                for i in range(len(my_movies)):
                    print(f"{i+1}. {my_movies[i]}")

                # If the list of movies is 5 or more, ask if they want to start recommendations.
                if len(my_movies) >= 5:
                    input_recommendation = input("Start Recommendation (Y) \n Add Another Movie (N)\n")

                    # Output recommendations
                    if input_recommendation.lower() == 'y':
                        recommend_movies(my_movies)
                        break

                    # Add more movies
                    else:
                        continue

            else:
                continue