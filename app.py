from flask import Flask, g, jsonify, request, make_response
from threading import Thread
from background import background
import sqlite3


def create_app():
	"""Create new flask app that will start background thread automatically"""
	app = Flask(__name__)
	# Creating background thread
	Thread(target=background).start()
	return app


def connect_db():
	"""Connects to the cricket database."""
	con = sqlite3.connect("cricket.db")
	con.row_factory = sqlite3.Row
	return con


def get_db():
	"""Opens a new database connection if there is none yet for the
    current application context.
    """
	if not hasattr(g, "sqlite_db"):
		g.sqlite_db = connect_db()
	return g.sqlite_db


app = create_app()


@app.teardown_appcontext
def teardown_db(exception):
	"""Closes the database again at the end of the server."""
	db = g.pop('sqlite_db', None)

	if db is not None:
		db.close()


@app.route("/videos", methods=["GET"])
def videos():
	"""Get videos in reverse chronological order with each page containing 5 videos"""
	page = request.args.get("page")

	# Invalidate request if page not present
	if page is None:
		return make_response(jsonify({"error": "page number not provided"}),
		                     400)

	cur = get_db().cursor()
	# Paginate and sort videos with given page number
	out = cur.execute(
	    "SELECT * FROM videos ORDER BY published_at DESC LIMIT ?, 5", [
	        int(page) * 5,
	    ])
	res = jsonify({"videos": [dict(i) for i in out.fetchall()]})
	cur.close()
	return res


@app.route("/search", methods=["GET"])
def search():
	"""Search videos by title and description"""
	query = request.args.get("query")

	# Invalidate request if query not present
	if query is None or query == "":
		return make_response(jsonify({"error": "No query provided"}), 400)
	cur = get_db().cursor()

	# Use inbuilt [MATCH] function to search for videos with given query
	out = cur.execute(
	    "SELECT * FROM videos WHERE (title LIKE ? OR description LIKE ?)",
	    ("%" + query + "%", "%" + query + "%"))
	res = jsonify({"videos": [dict(i) for i in out.fetchall()]})
	cur.close()
	return res
