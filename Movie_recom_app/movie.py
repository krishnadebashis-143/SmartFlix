import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import webbrowser

# Set Streamlit page configuration
st.set_page_config(page_title="SmartFlix – Your Ultimate Movie Companion")

# Sidebar for Navigation
st.sidebar.title("Movie Explorer")
section = st.sidebar.radio("Select Section", ["Home", "Upload Dataset", "Movie Search", "Top Movies", "Analysis", "Watch Trailers"])

# Initialize session state for dataset
if "movies" not in st.session_state:
    st.session_state.movies = None

# Landing Page
if section == "Home":
    st.title("SmartFlix – Your Ultimate Movie Companion")
    st.write("Discover Movies You’ll Love! Upload, Search, and Explore.")

# Upload CSV File
elif section == "Upload Dataset":
    st.header("Upload a Movie Dataset")
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    
    @st.cache_data
    def load_data(file):
        try:
            df = pd.read_csv(file)
            df.rename(columns={"Title": "title", "Genre": "genres"}, inplace=True)
            required_columns = ["title", "overview", "genres", "popularity", "director", "rating", "reviews"]
            for col in required_columns:
                if col not in df.columns:
                    df[col] = "Unknown" if col not in ["popularity", "rating", "reviews"] else np.random.randint(1, 100, len(df))
            return df
        except Exception as e:
            st.error(f"Error loading dataset: {e}")
            return None
    
    if uploaded_file:
        st.session_state.movies = load_data(uploaded_file)
        st.success("Dataset Uploaded Successfully!")
    
    if st.session_state.movies is not None:
        st.dataframe(st.session_state.movies.head())

# Movie Search
elif section == "Movie Search":
    st.header("Search for a Movie")
    if st.session_state.movies is not None:
        search_query = st.text_input("Enter movie name:")
        if search_query:
            results = st.session_state.movies[st.session_state.movies["title"].str.contains(search_query, case=False, na=False)]
            st.dataframe(results)
    else:
        st.warning("Please upload a dataset first.")

# Top Movies Section
elif section == "Top Movies":
    st.header("Top 10 Rated Movies")
    if st.session_state.movies is not None:
        top_movies = st.session_state.movies.sort_values(by="rating", ascending=False).head(10)
        fig_bar = px.bar(top_movies, x="title", y="rating", color="rating", text="rating")
        st.plotly_chart(fig_bar)
    else:
        st.warning("Please upload a dataset first.")

# Analysis Section
elif section == "Analysis":
    st.header("Popularity vs Rating Analysis")
    if st.session_state.movies is not None:
        fig = px.scatter(st.session_state.movies, x="popularity", y="rating", size="reviews", color="genres", hover_name="title")
        st.plotly_chart(fig)
    else:
        st.warning("Please upload a dataset first.")

# Watch Trailers Section
elif section == "Watch Trailers":
    st.header("Watch Movie Trailers")
    if st.session_state.movies is not None:
        movie_choice = st.selectbox("Select a movie to watch its trailer:", st.session_state.movies["title"].unique())
        search_url = f"https://www.youtube.com/results?search_query={movie_choice}+trailer"
        if st.button("Watch Trailer"):
            webbrowser.open(search_url)
    else:
        st.warning("Please upload a dataset first.")
