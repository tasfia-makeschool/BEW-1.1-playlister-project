from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

# heroku deployment
host = os.environ.get('MONGODB_URI', 'mongodb://<tanner>:<makeschool2021>@ds157223.mlab.com:57223/heroku_56km70rf')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
playlists = db.playlists
comments = db.comments

# local deployment
# client = MongoClient()
# db = client.Playlister
# playlists = db.playlists
# comments = db.comments

app = Flask(__name__)

# index page
@app.route('/')
def playlists_index():
    """Show all playlists."""
    return render_template('playlists_index.html', playlists=playlists.find())

# create a new playlist
@app.route('/playlists/new', methods=['GET'])
def playlists_new():
    """Create a new playlist."""
    return render_template('playlists_new.html', playlist={}, title='New Playlist')

# return to home page updated w/ new playlist
@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
    videos = request.form.get('videos').split()
    videos_embed = []
    for video in videos: 
        youtube = 'https://www.youtube.com/embed/'
        if '=' in video:
            videos_embed.append(youtube + video.split("=")[1])
        else:
            videos_embed.append(video)

    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos_embed,
        'created_at': datetime.now()
    }

    playlist_id = playlists.insert_one(playlist).inserted_id
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

# show playlist and its videos
@app.route('/playlists/<playlist_id>', methods=['GET'])
def playlists_show(playlist_id):
    # return f'My ID is {playlist_id}'
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    playlist_comments = comments.find({'playlist_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist, comments=playlist_comments)

# edit playlist
@app.route('/playlists/<playlist_id>/edit', methods=['GET'])
def playlists_edit(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')

# return to playlist page w/ edited changes
@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """Submit an edited playlist."""
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

# delete playlist and return to home page
@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    """Delete one playlist."""
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))

# add comment
@app.route('/playlists/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'playlist_id': ObjectId(request.form.get('playlist_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('playlists_show', playlist_id=request.form.get('playlist_id')))

# delete comment
@app.route('/playlists/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('playlists_show', playlist_id=comment.get('playlist_id')))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
