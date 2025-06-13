from flask import Flask, request, Response, jsonify
import redis
import uuid
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# r = redis.Redis(host="localhost", port=6379)  # Replace with Redis IP if needed
r = redis.Redis(host="10.95.149.115", port=6379)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("message")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    task_id = str(uuid.uuid4())
    r.rpush("ollama_jobs", json.dumps({"task_id": task_id, "prompt": prompt}))
    pubsub = r.pubsub()
    pubsub.subscribe(f"stream:{task_id}")

    def generate():
        for message in pubsub.listen():
            if message["type"] == "message":
                content = message["data"].decode()
                if content == "[END]":
                    break
                yield content

    return Response(generate(), mimetype="text/plain")

@app.route("/test-redis", methods=["GET"])
def test_redis():
    try:
        r.set("ping", "pong")
        value = r.get("ping").decode()
        return jsonify({"status": "✅ Connected to Redis", "value": value})
    except Exception as e:
        return jsonify({"status": "❌ Failed to connect", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
