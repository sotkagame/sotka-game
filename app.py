from flask import Flask, request, jsonify, send_file
import random
import time

app = Flask(__name__)

rooms = {}

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/join", methods=["POST"])
def join():
    user_id = request.json.get("user_id")

    # ищем свободную комнату
    for room_id, room in rooms.items():
        if len(room["players"]) < 2:
            room["players"].append(user_id)
            return jsonify({
                "room_id": room_id,
                "player": len(room["players"]),
                "status": "matched"
            })

    # создаём новую комнату
    room_id = f"room_{int(time.time())}"
    rooms[room_id] = {
        "players": [user_id],
        "numbers": {}
    }

    return jsonify({
        "room_id": room_id,
        "player": 1,
        "status": "waiting"
    })

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    room_id = data["room_id"]
    user_id = data["user_id"]
    number = data["number"]

    rooms[room_id]["numbers"][user_id] = number

    if len(rooms[room_id]["numbers"]) == 2:
        bot_number = random.randint(1, 100)
        return jsonify({
            "status": "start",
            "bot_number": bot_number
        })

    return jsonify({"status": "waiting"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
