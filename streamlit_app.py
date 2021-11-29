import streamlit as st
import pandas as pd
import altair as alt

# Set page config
st.set_page_config(
    page_title="Simple Recommender",
    page_icon="🎥",
    layout="wide")

# import data sources


@st.cache()
def load_data():
    column_names = ['user_id', 'item_id', 'rating', 'timestamp']
    data = pd.read_csv('u.data', sep='\t', names=column_names)
    movie_titles = pd.read_csv('Movie_Id_Titles')
    data = pd.merge(data, movie_titles, on='item_id')
    return data


def create_matrix(data):
    mat = data.pivot_table(index='user_id', columns='title', values='rating')
    return mat


def create_ratings(data):
    ratings = pd.DataFrame(data.groupby('title')['rating'].mean())
    ratings['num of ratings'] = pd.DataFrame(
        data.groupby('title')['rating'].count())
    return ratings


def get_recs(data, title, nr):
    # create recommendation matrix
    mat = create_matrix(data)
    # create the ratings table
    # we need this to apply filtering to the final results
    ratings = create_ratings(data)
    # get the ratings from each user of the selected title
    ur_df = mat[title]
    # get correlations between the selected title and all other titles
    sim_df = mat.corrwith(ur_df)
    # turn into a dataframe and dropna
    corr_df = pd.DataFrame(sim_df, columns=['Correlation'])
    corr_df.dropna(inplace=True)
    # add the number of ratings to the df so we can filter the results
    corr_df = corr_df.join(ratings['num of ratings'])
    # get the top 11 most correllated titles and put into a yet another df
    results = corr_df[corr_df['num of ratings'] > nr].sort_values(
        'Correlation', ascending=False).head(11)
    # drop the first row of the results. it's always the selected title because correlation = 1.
    results = results.iloc[1:, :]
    return results


data = load_data()
ratings = create_ratings(data)

row1_1, row1_2 = st.columns((2, 3))

with row1_1:
    st.title("Simple Movie Recommender")
    selected_title = st.selectbox(
        'Select a title',
        ratings[ratings['num of ratings'] > 200].reset_index(),
        index=0
    )

# 'Hunchback of Notre Dame, The (1996)', 'Mask, The (1994)',	'Tomorrow Never Dies (1997)'

with row1_2:
    st.write(
        """
        ##
        A very simple (and not very accurate) movie recommender using item similarity from the MovieLens dataset.

        Select a title using the dropdown on the left. Adjust the slider to set the minimum number of ratings for a movie to appear as a recommendation.
        """
    )
    min_ratings = st.slider(
        'Select minimum number of ratings',
        0,
        500,
        value=100,
        step=50
    )

results = get_recs(data, selected_title, min_ratings)


row2_1, row2_2, row2_3 = st.columns((2, 1, 1))
with row2_1:
    st.header(selected_title)


with row2_2:
    st.metric('Number of ratings',
              int(ratings.loc[selected_title]['num of ratings']))


with row2_3:
    st.metric('Average rating', round(
        ratings.loc[selected_title]['rating'], 2))

st.subheader('Recommendations')
st.write(results)

st.write(
    """
    [View Source Code](https://github.com)
    """
)
