from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Third post", "content": "This post will be deleted."}
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    title = data.get("title")
    content = data.get("content")

    missing_fields = []
    if not title or title.strip() == "":
        missing_fields.append("title")
    if not content or content.strip() == "":
        missing_fields.append("content")

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing_fields,
            "message": "Please provide non-empty 'title' and/or 'content'."}), 400

    new_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1
    new_post = {"id": new_id, "title": title.strip(), "content": content.strip()}
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = next((post for post in POSTS if post["id"] == id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    POSTS.remove(post)
    return jsonify({"message": f"Post with id {id} has been deleted."}), 200


# Update post by id
@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    # Find post by id
    post = next((post for post in POSTS if post["id"] == id), None)

    # If post not found → 404
    if not post:
        return jsonify({"error": "Post not found"}), 404

    # Get JSON data from request
    data = request.get_json() or {}

    # Update title and content
    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])

    return jsonify(post), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)