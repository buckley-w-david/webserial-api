import os
import time
import toml  # type: ignore
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth  # type: ignore
from werkzeug.security import check_password_hash
from threading import Thread
from webserial_api.tasks import submit_story, delete_story

import os

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("application.cfg")
auth = HTTPBasicAuth()

users = app.config.get("USERS", {})

@auth.verify_password
def verify_password(username, password):
    expected = users.get(username)

    if expected and check_password_hash(expected, password):
        return username


@app.route("/follow/", methods=["POST"])
@auth.login_required
def submit():
    url = request.data.decode("utf-8")
    user = app.config.get("CALIBRE_USERNAME", "")
    password = app.config.get("CALIBRE_PASSWORD", "")
    library = app.config.get("CALIBRE_LIBRARY", "")

    thread = Thread(target=submit_story, args=(url, user, password, library))
    thread.daemon = True
    thread.start()
    return jsonify({"thread_name": str(thread.name), "started": True})


@app.route("/follow/<int:id>", methods=["DELETE"])
@auth.login_required
def delete(id):
    user = app.config.get("CALIBRE_USERNAME", "")
    password = app.config.get("CALIBRE_PASSWORD", "")
    library = app.config.get("CALIBRE_LIBRARY", "")

    thread = Thread(target=delete_story, args=(id, user, password, library))
    thread.daemon = True
    thread.start()
    return jsonify({"thread_name": str(thread.name), "started": True})
