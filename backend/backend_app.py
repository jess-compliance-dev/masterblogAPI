from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Third post", "content": "This post will be deleted."},
    {"id": 4, "title": "ABC", "content": "This is the alphabet"},
    {"id": 5, "title": "South America", "content": "Lima"},
    {"id": 6, "title": "South America", "content": "Machu Picchu"},
]


# GET all posts, sorting is optional
@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Return all posts. Optionally sort by 'title' or 'content' if direction is 'asc' or 'desc'."""
    sort_field = request.args.get("sort", None)
    direction = request.args.get("direction", None)  # None = unsortiert

    # Copy posts to avoid changing original list
    result_posts = []
    for post in POSTS:
        result_posts.append(post)

    # Only sort if both field and direction are valid
    if sort_field in ["title", "content"] and direction in ["asc", "desc"]:
        reverse = True if direction == "desc" else False
        result_posts.sort(key=lambda post: post[sort_field].lower(), reverse=reverse)

    return jsonify(result_posts)


# Add a new post
@app.route('/api/posts', methods=['POST'])
def add_post():
    """Add a new post. Requires 'title' and 'content' in JSON body."""
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
            "message": "Please provide non-empty 'title' and/or 'content'."
        }), 400

    max_id = 0
    for post in POSTS:
        if post["id"] > max_id:
            max_id = post["id"]
    new_id = max_id + 1 if POSTS else 1

    new_post = {"id": new_id, "title": title.strip(), "content": content.strip()}
    POSTS.append(new_post)
    return jsonify(new_post), 201


# Delete post by id
@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """Delete a post by its ID. Returns 404 if post not found."""
    post = None
    for p in POSTS:
        if p["id"] == id:
            post = p
            break

    if not post:
        return jsonify({"error": "Post not found"}), 404

    POSTS.remove(post)
    return jsonify({"message": f"Post with id {id} has been deleted."}), 200


# Update post by id
@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """Update title and/or content of a post by its ID. Returns 404 if post not found."""
    post = None
    for p in POSTS:
        if p["id"] == id:
            post = p
            break

    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json() or {}

    if "title" in data and data["title"].strip() != "":
        post["title"] = data["title"].strip()
    if "content" in data and data["content"].strip() != "":
        post["content"] = data["content"].strip()

    return jsonify(post), 200


# Search posts by title/content
@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search posts by title and/or content. Returns matching posts."""
    title_query = request.args.get("title", "").lower()
    content_query = request.args.get("content", "").lower()

    results = []

    for post in POSTS:
        match = False
        if title_query and title_query in post["title"].lower():
            match = True
        if content_query and content_query in post["content"].lower():
            match = True
        if match:
            results.append(post)

    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)