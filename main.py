import streamlit as st
import pickle as pkl
import pandas as pd
import requests

# Function to fetch poster using TMDb API
def get_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzNWI4ZWI3OWJmNWE3N2I5MmViY2I0MjU4YmMxNjJkMCIsIm5iZiI6MTc1NDQ3NzYzOC41MjcsInN1YiI6IjY4OTMzNDQ2ODYzNDU1YWE5NmRiZmQwOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._N-seWjsD9JpPb-TDQiCltlWPFw_ZlLbvtnA0OlgzS0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return ""  # Return empty string if poster not found

# Recommendation function
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(get_poster(movie_id))

    return recommended_movies, recommended_posters

# Load movie data
movies_dict = pkl.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pkl.load(open("similarity.pkl", "rb"))

# Streamlit UI
st.title("Movie Recommender System")
selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)  # Updated from beta_columns
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
