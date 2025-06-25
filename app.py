import streamlit as st
import pandas as pd
import pickle
import requests
movies_dict=pickle.load(open('movies_dict.pkl', 'rb'))
similarity=pickle.load(open('similarity.pkl', 'rb'))

movies=pd.DataFrame(movies_dict)


def fetch_posters(movie_id):
    response=requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7680ecd686538266e1965f6a3ed8d05c&language=en-US")
    data=response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)), reverse=True , key=lambda x:x[1])[1:6]

    recommended_movies=[]
    movies_posters=[]
    for n in movies_list:
        movie_id=movies.iloc[n[0]].id
        recommended_movies.append(movies.iloc[n[0]].title)
        movies_posters.append(fetch_posters(movie_id))
    return recommended_movies, movies_posters


st.title("Movies Recommendation System")
selected_movie_name=st.selectbox(
    "Which movie do you want to recommend?",
    movies['title'].values
)

if st.button("Recommend Movie"):
    names, posters =recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])