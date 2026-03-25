from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Third post", "content": "This post will be deleted."}
]


# Get all posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


# Add new post
@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()  # Get JSON data

    # Check if data exists
    if not data:
        return jsonify({"error": "No data provided"}), 400

    title = data.get("title")
    content = data.get("content")

    # Check required fields
    missing_fields = []
    if not title:
        missing_fields.append("title")
    if not content:
        missing_fields.append("content")

    # Return error if fields missing
    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing_fields
        }), 400

    # Generate new ID
    new_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1

    # Create new post
    new_post = {
        "id": new_id,
        "title": title,
        "content": content
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # Find post by id
    post = next((post for post in POSTS if post["id"] == id), None)

    # If post not found
    if not post:
        return jsonify({
            "error": "Post not found"
        }), 404

    POSTS.remove(post)

    return jsonify({
        "message": f"Post with id {id} has been deleted."
    }), 200


# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "The requested resource was not found"}), 404

@app.errorhandler(405)
def not_allowed(e):
    return jsonify({"error": "Method Not Allowed"}), 405

@app.errorhandler(429)
def rate_limit(e):
    return jsonify({"error": "Too many requests"}), 429


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
