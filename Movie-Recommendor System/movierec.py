import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=24ef4bbf598de4626ed255d167b77e64&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie,a):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:a+1]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters 

similarity = pickle.load(open('similarity.pkl','rb'))
movies_list = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_list)
st.title('Movies Recommender System')

option = st.selectbox(
    "Please Enter Movie name?",
    movies['title'].values,
)

o = st.number_input('Enter number of movies you want to show',min_value=0, step=1, format="%d")


if st.button('Give Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(option, o)
    if o>=1:
        num_columns = []
        for x in range(o):
            num_columns.append(2)
        
        columns = st.columns(num_columns)

    # Use the columns to display the recommendations
        for i in range(o):
            with columns[i % len(num_columns)]:  # Handle multiple columns if needed
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
    else:
       st.error('Please enter a number greater or equal to 1!')              


    # col1, col2, col3, col4, col5 = st.columns(5)
    # with col1:
    #     st.text(recommended_movie_names[0])
    #     st.image(recommended_movie_posters[0])
    # with col2:
    #     st.text(recommended_movie_names[1])
    #     st.image(recommended_movie_posters[1])

    # with col3:
    #     st.text(recommended_movie_names[2])
    #     st.image(recommended_movie_posters[2])
    # with col4:
    #     st.text(recommended_movie_names[3])
    #     st.image(recommended_movie_posters[3])
    # with col5:
    #     st.text(recommended_movie_names[4])
    #     st.image(recommended_movie_posters[4])
