import webbrowser
import urllib.parse
import requests 
from bs4 import BeautifulSoup
import os

PORT = os.environ("PORT")
APPID = os.environ("APPID")
SECRET = os.environ("SECRET")

if __name__ == "__main__":
    webbrowser.open('https://connect.deezer.com/oauth/auth.php?' + urllib.parse.urlencode({
        'app_id': APPID,
        'redirect_uri': 'http://localhost:8000/authfinish'.format(PORT),
        'perms': 'basic_access,manage_library'
    }))

    code = input("Enter the code: ")
    f = requests.get(f"https://connect.deezer.com/oauth/access_token.php?app_id={APPID}&secret={SECRET}&code={code}")
    access_code = str(f.content).split("=")[1].split("&")[0]

    tracklist_url = input("Enter tracklist url: ")
    playlist_name = tracklist_url.split("/")[-1].split(".")[0]

    res = requests.get(
        tracklist_url,
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        )
    soup = BeautifulSoup(res.content, "html.parser")
    tracks = soup.select(".tlpItem")
    exported_tracks = []
    for track in tracks:
        track_elem = track.select("meta")[0]
        exported_tracks.append(track_elem["content"])
    
    song_ids = []
    for track in exported_tracks:
        search = requests.get(f"https://api.deezer.com/search?access_token={access_code}&q={track}")
        results = search.json()["data"]
        if results:
            song_ids.append(results[0]["id"])

    playlist = requests.post(f"https://api.deezer.com/user/me/playlists?access_token={access_code}", data={"title": playlist_name})
    playlist_id = playlist.json()["id"]

    songs = ",".join(str(sid) for sid in song_ids)

    update = requests.post(f"https://api.deezer.com/playlist/{playlist_id}/tracks?access_token={access_code}", data={"songs": songs})
    if update.status_code == 200:
        playlist = requests.get(f"https://api.deezer.com/playlist/{playlist_id}?access_token={access_code}")
        link = playlist.json()["link"]
        print(f"Here's your playlist link: {link}")



