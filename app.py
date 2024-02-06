# from flask import Flask, render_template, request, redirect, url_for
# from ytmusicapi import YTMusic
# import sqlite3
# import requests

# app = Flask(__name__)

# # Initialize YTMusic API
# yt = YTMusic('oauth.json')

# # Connect to SQLite database (create if not exists)
# conn = sqlite3.connect('playlist.db')
# cursor = conn.cursor()

# # Create table to store songs
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS songs (
#         id INTEGER PRIMARY KEY,
#         title TEXT,
#         video_id TEXT
#     )
# ''')
# cursor.execute("PRAGMA table_info(songs)")
# columns = cursor.fetchall()
# column_names = [col[1] for col in columns]
# # cursor.execute("DELETE FROM songs")

# if 'mp3_link' not in column_names:
#     # Add new column to the songs table
#     cursor.execute("ALTER TABLE songs ADD COLUMN mp3_link TEXT")
#     print("Column 'mp3_link' added successfully.")
# else:
#     print("Column 'mp3_link' already exists.")


# # Commit changes and close connection
# conn.commit()
# conn.close()

# @app.route('/' , methods=['GET'])
# def index():
#     return render_template('index.html')

# @app.route('/search', methods=['POST'])
# def search():
#     query = request.form['query']
#     search_results = yt.search(query)
#     top_5_results = search_results[:5]  # Slice to get only the top 5 results
#     return render_template('results.html', results=top_5_results)


# @app.route('/add_to_playlist', methods=['POST'])
# def add_to_playlist():
#     video_id = request.form['video_id']
#     title = request.form['title']
    
    
#     # Fetch MP3 link from Gaana API
#     gaana_url = request.form['gaana_url']  # Assuming you pass Gaana URL from the form
#     response = requests.get(f'http://127.0.0.1:5001/result/?url={gaana_url}')
#     if response.status_code == 200:
#         song_data = response.json()
#         mp3_link = song_data.get('link')
#     else:
#         mp3_link = None
    
#     # Insert song into SQLite database
#     conn = sqlite3.connect('playlist.db')
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO songs (title, video_id, mp3_link) VALUES (?, ?, ?)", (title, video_id, mp3_link))
#     conn.commit()
#     conn.close()
    
#     # return 'Song added to playlist successfully'
#     return redirect(url_for('index'))


# @app.route('/saved_songs')
# def saved_songs():
#     conn = sqlite3.connect('playlist.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM songs")
#     songs = cursor.fetchall()
#     conn.close()
    
#     return render_template('saved_songs.html', songs=songs)

# if __name__ == '__main__':
#     app.run(debug=True,port=5001)





from flask import Flask, jsonify, render_template, request, redirect, url_for
from ytmusicapi import YTMusic
import sqlite3
import requests

app = Flask(__name__)

# Initialize YTMusic API
yt = YTMusic('oauth.json')

# Connect to SQLite database (create if not exists)
conn = sqlite3.connect('playlist.db')
cursor = conn.cursor()

# Create table to store songs
cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY,
        title TEXT,
        video_id TEXT
    )
''')
cursor.execute("PRAGMA table_info(songs)")
columns = cursor.fetchall()
column_names = [col[1] for col in columns]

if 'mp3_link' not in column_names:
    # Add new column to the songs table
    cursor.execute("ALTER TABLE songs ADD COLUMN mp3_link TEXT")
    print("Column 'mp3_link' added successfully.")
else:
    print("Column 'mp3_link' already exists.")

# Commit changes and close connection
conn.commit()
conn.close()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    search_results = yt.search(query)
    top_5_results = search_results[:5]  # Slice to get only the top 5 results
    return render_template('results.html', results=top_5_results)

@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    video_id = request.form['video_id']
    title = request.form['title']
    gaana_url = request.form['gaana_url']
    
    # Fetch MP3 link from Gaana API
    response = requests.get(f'http://127.0.0.1:5001/result/?url={gaana_url}')
    if response.status_code == 200:
        song_data = response.json()
        mp3_link = song_data.get('link')
    else:
        mp3_link = None
    
    # Insert song into SQLite database
    conn = sqlite3.connect('playlist.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO songs (title, video_id, mp3_link) VALUES (?, ?, ?)", (title, video_id, mp3_link))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/saved_songs')
def saved_songs():
    conn = sqlite3.connect('playlist.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()
    conn.close()
    
    return render_template('saved_songs.html', songs=songs)

@app.route('/remove_from_playlist/<int:song_id>', methods=['POST'])
def remove_from_playlist(song_id):
    # Remove song from SQLite database
    conn = sqlite3.connect('playlist.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM songs WHERE id = ?", (song_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('saved_songs'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)