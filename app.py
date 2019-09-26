from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient()
db = client.Playlister
playlists = db.playlists

app = Flask(__name__)

# OUR MOCK ARRAY OF PROJECTS
# playlists = [
#     { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
#     { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' }
# ]

@app.route('/')
def playlists_index():
    """Show all playlists."""
    return render_template('playlists_index.html', playlists=playlists.find())

# @app.route('/playlists/new', methods=['GET'])
# @app.route('/playlists', methods=['POST'])
# @app.route('/playlists/:id', methods=['GET'])
# @app.route('/playlists/:id/edit', methods=['GET'])
# @app.route('/playlists/:id', methods=['PUT'])
# @app.route('/playlists/:id', methods=['DELETE'])


if __name__ == '__main__':
    app.run(debug=True)
