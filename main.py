from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

# Get the env data
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Returns a token to give the access to the API
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes  =auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization":"Basic " + auth_base64,
        "Content-Type":"application/x-www-form-urlencoded"
    }
    data = {"grant_type":"client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# Returns a authorization header
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# Get artist data from Spotify API
def serch_for_artists(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    # 'type' is what a type of data you're searching for, limit set the amount of results
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist found")
        return None
    
    return json_result

def get_songs_by_artist(token, artist_id):
    url=f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


token = get_token()

# Collect artist data
artist_name = ""
result = serch_for_artists(token, artist_name)
artist_id = result[0]["id"]

# Returns the artist top tracks
songs = get_songs_by_artist(token, artist_id)
for item, song in enumerate(songs):
    print(f"{item+1}. {song['name']}")