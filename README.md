# Simple Movie Recommender

I created this simple recommendation system using the MovieLens 100k dataset. All recommendations are based on item similarity.

The method is

1. Create matrix indexed on the user. Each movie title gets a column and the user rating is filled in where available.
2. For the selected movie, find the correlation coefficient for all other available titles.
3. Display a list of titles with the highest correlation to the selected title. This list is filtered to movies with more than 100 ratings by default to reduce the number of false positives.

[View the live app](https://share.streamlit.io/peterarbaugh/simple-movie-recommender/main)
