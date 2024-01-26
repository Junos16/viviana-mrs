import requests
import streamlit as st
import pandas as pd
import json

st.title('Viviana - Movie Recommendation System')
st.markdown('### By [Hriddhit Datta](https://www.linkedin.com/in/hriddhit-datta-035608223/)')

movies = pd.read_pickle('movies.pkl')
#userData = pickle.load(open('userData.pkl','rb'))
userTable = pd.read_pickle('userTable.pkl')
#tagData = pickle.load(open('tagData.pkl','rb'))
tagTable = pd.read_pickle('tagTable.pkl')

def fetch_poster(movie_id):
    with open('config.json') as config_file:
        config = json.load(config_file)

    api_key = config.get('api_key')
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url)
    data = data.json()
    try:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        #print(url)
        #print(full_path)
        return full_path
    except KeyError:
        full_path = "https://wellesleysocietyofartists.org/wp-content/uploads/2015/11/image-not-found.jpg"
        return full_path

def contentBasedFiltering(inputMovie, recCount):
    similar = tagTable.corrwith(tagTable[inputMovie]).sort_values(ascending = False) # Finding movie similar to the movie input by the user
    if recCount == 0: # If movie input is input via recommendation (hybrid filtering)
        return similar # Return similar series
    else: # If movie is input via contentBasedFiltering
        print(similar[:recCount]) # Display certain number of movies similar to the input movie

def collaborativeFiltering(inputMovie, recCount):
    similar = userTable.corrwith(userTable[inputMovie]).sort_values(ascending = False) # Finding movie similar to the movie input by the user
    if recCount == 0: # If movie input is input via recommendation (hybrid filtering)
        return similar # Return similar series
    else: # If movie is input via collaborativeFiltering
        print(similar[:recCount]) # Display certain number of similar movies to the input movie

def recommendation(inputMovie, recCount):
    serA = contentBasedFiltering(inputMovie, 0).sort_index(ascending = True) # Output given by contentBasedFiltering function
    serB = collaborativeFiltering(inputMovie, 0).sort_index(ascending = True) # Output given by collaborativeFiltering function
    similar = serA.mul(0.4).add(serB.mul(0.6)).sort_values(ascending = False) # Weighted mean of the two outputs 
    similar = similar.to_frame().reset_index()
    #print(similar[:recCount]) # Display certain number of similar movies to the input movie
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in range(1, recCount):
        rec = similar.loc[i, 'title']
        recommended_movie_names.append(rec)        
        movie_id = movies.loc[movies['title'] == rec]['tmdbId']
        movie_id = movie_id.values[0]
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names,recommended_movie_posters

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommendation(selected_movie, 6)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

