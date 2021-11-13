from flask import Flask, g, jsonify, request, make_response
from threading import Thread
from background import background
import sqlite3
from pprint import pprint


def create_app():
	app = Flask(__name__)
	# Storing database connection in app context
	with app.app_context():
		get_db()
	# Creating background thread
	# Thread(target=background).start()
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
	db = g.pop('sqlite_db', None)

	if db is not None:
		db.close()


@app.route("/videos", methods=["GET"])
def index():
	page = request.args.get("page")

	if page is None:
		page = 0
	cur = get_db().cursor()
	out = cur.execute("SELECT * FROM videos ORDER BY published_at DESC LIMIT ?, 5", (int(page) * 5,))
	res = jsonify({"videos": [dict(i) for i in out.fetchall()]})
	cur.close()
	return res

@app.route("/search", methods=["GET"])
def search():
	query = request.args.get("query")
	if query is None or query == "":
		return make_response(jsonify({"error": "No query provided"}), 400)
	cur = get_db().cursor()
	out = cur.execute("SELECT * FROM videos WHERE (title LIKE ? OR description LIKE ?)", ("%" + query + "%", "%" + query + "%"))
	res = jsonify({"videos": [dict(i) for i in out.fetchall()]})
	cur.close()
	return res
