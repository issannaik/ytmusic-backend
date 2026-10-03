from flask import Flask, request, jsonify
from ytmusicapi import YTMusic

app = Flask(__name__)

yt = YTMusic()


@app.route("/")
def home():
    return "YTMusic Backend is running!"


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "error": "Search query is required"
        }), 400

    try:
        results = yt.search(query, filter="songs")

        songs = []

        for item in results[:20]:
            songs.append({
                "videoId": item.get("videoId"),
                "title": item.get("title"),
                "artist": (
                    item.get("artists", [{}])[0].get("name")
                    if item.get("artists")
                    else ""
                ),
                "album": (
                    item.get("album", {}).get("name")
                    if item.get("album")
                    else ""
                ),
                "duration": item.get("duration"),
                "thumbnail": (
                    item.get("thumbnails", [{}])[-1].get("url")
                    if item.get("thumbnails")
                    else ""
                )
            })

        return jsonify(songs)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
