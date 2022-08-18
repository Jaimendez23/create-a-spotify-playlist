from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# 2019-06-03
CLIENT_ID = "0"
CLIENT_SECRET = "0"
top_song_date = input("Which Year do you want to travel to? "
                      "Type the date in this format YYYY-MM-DD: \n")

url = f"https://www.billboard.com/charts/hot-100/{top_song_date}"

response = requests.get(url)
bb_webpage = response.text

soup = BeautifulSoup(bb_webpage, 'html.parser')
# song_names_h3 = soup.find_all(name="h3", id="title-of-a-story", class_="c-title")
song_names_h3 = soup.select(selector="li h3")
song_names = [song_names_h3[song].getText() for song in range(0, 100)]
song_names = [song.replace("\n", "") for song in song_names]
song_names = [song.replace("\t", "") for song in song_names]
# print(song_names)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    redirect_uri="http://example.com",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    show_dialog=True,
    cache_path="token.txt"
))
user_id = sp.current_user()["id"]

song_uri = []

year = top_song_date.split("-")[0]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{top_song_date} Billboard 100", public=False)
playlist_id = playlist["id"]
# print(playlist_id)
sp.playlist_add_items(playlist_id=playlist_id, items=song_uri)

print(f"your playlist link is: https://open.spotify.com/playlist/{playlist_id}")

