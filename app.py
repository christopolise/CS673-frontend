from flask import Flask, render_template, request, redirect, url_for, Response
import os
import random
import json
from flask_socketio import SocketIO
from threading import Thread
import time

prompts = [
    "Pop dance track with catchy melodies, tropical percussion, and upbeat rhythms, perfect for the beach",
    "A grand orchestral arrangement with thunderous percussion, epic brass fanfares, and soaring strings, creating a cinematic atmosphere fit for a heroic battle.",
    "classic reggae track with an electronic guitar solo",
    "earthy tones, environmentally conscious, ukulele-infused, harmonic, breezy, easygoing, organic instrumentation, gentle grooves",
    "lofi slow bpm electro chill with organic samples",
    "drum and bass beat with intense percussions",
    "A dynamic blend of hip-hop and orchestral elements, with sweeping strings and brass, evoking the vibrant energy of the city.",
    "violins and synths that inspire awe at the finiteness of life and the universe",
    "80s electronic track with melodic synthesizers, catchy beat and groovy bass",
    "reggaeton track, with a booming 808 kick, synth melodies layered with Latin percussion elements, uplifting and energizing",
    "a piano and cello duet playing a sad chambers music",
    "smooth jazz, with a saxophone solo, piano chords, and snare full drums",
    "a light and cheerly EDM track, with syncopated drums, aery pads, and strong emotions",
    "a punchy double-bass and a distorted guitar riff",
    "acoustic folk song to play during roadtrips: guitar flute choirs",
    "rock with saturated guitars, a heavy bass line and crazy drum break and fills.",
]

app = Flask(__name__)
socketio = SocketIO(app)

def poll_for_completion():
    while True:
        if os.path.exists("static/sc_audio/output.mp3"):
            socketio.emit("gen_complete", {"sid": request.json["sid"]})
            break
        time.sleep(1)

@app.route("/random_pc", methods=["GET"])
def pre_random():
    # Return a random song from audio
    songs = [file for file in os.listdir("static/precomputed") if file.endswith(".mp3")]
    song = random.choice(songs)
    return Response(song, mimetype="text/plain")

@app.route("/gen", methods=["POST"])
def gen(sid):
    # Assign the session id to the request
    request.json["sid"] = sid

    with open("static/sc_audio/prompt.json", "w") as f:
        f.write(json.dumps(request.json))
    # Response text
    msg = "Generating song with the following prompts: \n"
    for field, prompt in request.json.items():
        msg += f"{field}: {prompt}\n"
    return Response(msg, mimetype="text/plain")

@app.route("/")
def index():
    return render_template(
        "index.html",
        songs=[file for file in os.listdir("static/audio") if file.endswith(".mp3")],
    )

if __name__ == "__main__":
    socketio.run(app, debug=True)