from flask import Flask, render_template, request, redirect, url_for, Response
import os
import random

app = Flask(__name__)

@app.route("/random", methods=["GET"])
def random():
    # Return a random song from audio
    songs = [file for file in os.listdir("static/audio") if file.endswith(".mp3")]
    song = random.choice(songs)
    return Response(song, mimetype="text/plain")

@app.route("/")
def index():
    return render_template(
        "index.html",
        songs=[
            file for file in os.listdir("static/audio") if file.endswith(".mp3")
        ],
    )
