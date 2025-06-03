import streamlit as st
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Define file paths properly
path = r"C:\Users\abhir\Downloads\for all.py\sololearn.py\Machine Learning\Songs_list"
spath = r"C:\Users\abhir\Downloads\for all.py\sololearn.py\Machine Learning\Similarity.pkl"

# Load the data
music = pickle.load(open(path, "rb"))
similarity = pickle.load(open(spath, "rb"))

# Streamlit header
st.header("Spotify Mini Songs Recommendation System")

# Spotify API credentials
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"


# Select song from dropdown
select_value = st.selectbox("Enter Your Favourite Song", music["song"])


def recommend(song):
    index = music[music["song"] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])

    recommended_songs = []
    recommended_posters = []  # New list for posters

    for i in distances[:5]:  # Correct slicing
        song_name = music.iloc[i[0]]['song']
        artist_name = music.iloc[i[0]]['artist']

        album_cover_url = get_song_album_cover_url(song_name, artist_name)

        recommended_songs.append(song_name)
        recommended_posters.append(album_cover_url)  # Append poster URLs

    return recommended_songs, recommended_posters


# Show recommendations
if st.button("Show Recommendation"):
    recommended_songs, recommended_posters = recommend(select_value)  # Properly unpack return values

    cols = st.columns(5)  # Create five columns dynamically

    for i in range(len(recommended_songs)):  # Loop through recommendations
        with cols[i]:
            st.text(recommended_songs[i])  # Display song name
            st.image(recommended_posters[i])  # Display album cover poster