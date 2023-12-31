import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, inspect, func, MetaData, Table, Column, Integer, String, Float
from flask import Flask, render_template
import json
 
from flask import Flask, render_template, request, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///spotify_songs.sqlite")

Base = declarative_base()

class SpotifySongs(Base):
    __tablename__ = 'spotify_songs'
    track_id = Column(Integer, primary_key=True)
    track_name = Column(String(225))
    artist = Column(String(225))
    popularity = Column(Integer)
    album_id = Column(String(225))
    album_name = Column(String(225))
    album_release_date = Column(String(225))
    playlist_name = Column(String(225))
    playlist_id = Column(String(225))
    playlist_genre = Column(String(225))
    playlist_subgenre = Column(String(225))
    danceability = Column(Float)
    energy = Column(Float)
    key = Column(Integer)
    loudness = Column(Float)
    mode = Column(Integer)
    speechiness = Column(Float)
    acousticness = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)
    duration_ms = Column(Integer)
    duration_seconds = Column(Integer)
    duration_minutes_seconds = Column(Float)  
    

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Welcome page
@app.route("/")
def welcome():

    return render_template("index.html")

# Playlist Genre Analysis Page
@app.route("/pie")
def pie():
    return render_template("pie.html")

# Playlist Attributes Correlation Page
@app.route("/attribute_analysis")
def attribute_analysis():
    return render_template("attribute_analysis.html")

# Playlist Attribute Analysis Page
@app.route("/bar")
def bar():
    return render_template("bar_chart.html")

# Top 100 Songs page
@app.route("/top_100")
def top_100():
    return render_template("top_100.html")

# Song Length over the Years page
@app.route("/song_length")
def song_length():
    return render_template("song_length.html")

# Song JSON
@app.route("/songs_extract") # remove as route maybe?
def extract():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    results = session.query(SpotifySongs).all()

    session.close()

    all_songs = [{"track_name": track[0]} for track in results]

    all_songs = []
    for song in results:
        spotify_dict = {
        "track_id": song.track_id,
        "track_name": song.track_name,
        "artist": song.artist,
        "popularity": song.popularity,
        "album_id": song.album_id,
        "album_release_date": song.album_release_date,
        "playlist_name": song.playlist_name,
        "playlist_id": song.playlist_id,
        "playlist_genre": song.playlist_genre,
        "playlist_subgenre": song.playlist_subgenre,
        "danceability": song.danceability,
        "energy": song.energy,
        "key": song.key,
        "loudness": song.loudness,
        "mode": song.mode,
        "speechiness": song.speechiness,
        "acousticness": song.acousticness,
        "instrumentalness": song.instrumentalness,
        "liveness": song.liveness,
        "valence": song.valence,
        "tempo": song.tempo,
        "duration_ms": song.duration_ms,
        "duration_seconds": song.duration_seconds,
        "duration_minutes_seconds": song.duration_minutes_seconds,
        }
        all_songs.append(spotify_dict)

    with open('static/spotify_songs.json', 'w') as file2:
        json.dump(all_songs, file2)

    return render_template('songs_extract.html')

# Tracks JSON
@app.route("/songs")
def songs():

    session = Session(engine)
    
    results = session.query(SpotifySongs).limit(3000).all()

    session.close()

    all_songs = [{"TRACK": song.track_name, "ARTIST": song.artist, "LENGTH": song.duration_minutes_seconds}
    for song in results]

    return jsonify(all_songs)

# Search Function
@app.route('/search', methods=['GET'])
def search_form():
    return render_template('search_form.html')

# Extended Search Function
@app.route('/search', methods=['POST'])
def search():
    session = Session(engine)

    search_query = request.form.get('search_query', '')
    page = int(request.form.get('page', 1))

    # Assuming SpotifySongs is your SQLAlchemy model
    query = session.query(SpotifySongs).filter(
        (SpotifySongs.track_name.ilike(f'%{search_query}%')) |
        (SpotifySongs.artist.ilike(f'%{search_query}%'))
    )

    total_results = query.count()
    paginated_results = get_paginated_results(query, page)

    session.close()

    if paginated_results:
        # Return a list of matching songs as JSON
        result_list = [{
            "track_name": song.track_name,
            "artist": song.artist,
            "popularity": song.popularity,
            "danceability": song.danceability
            # Include additional details as needed
        } for song in paginated_results]

        return jsonify({
            "total_results": total_results,
            "per_page": 25,
            "current_page": page,
            "results": result_list,
        })

    # Return a JSON indicating that no matching songs were found
    return jsonify({"error": "No matching songs found"})

# Function to get paginated results in search function
def get_paginated_results(query, page=1, per_page=25):
    offset = (page - 1) * per_page
    return query.offset(offset).limit(per_page).all()

if __name__ == '__main__':
    app.run(debug=True)