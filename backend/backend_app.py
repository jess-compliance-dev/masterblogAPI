from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["60 per hour"])
limiter.init_app(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Third post", "content": "This post will be deleted."},
    {"id": 4, "title": "ABC", "content": "This is the alphabet"},
    {"id": 5, "title": "South America", "content": "Lima"},
    {"id": 6, "title": "South America", "content": "Machu Picchu"},
]


@app.route('/api/posts', methods=['GET'])
@limiter.limit("100/hour")
def get_posts():
    sort_field = request.args.get("sort", None)
    direction = request.args.get("direction", None)
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    result_posts = POSTS.copy()

    if sort_field in ["title", "content"] and direction in ["asc", "desc"]:
        reverse = direction == "desc"
        result_posts.sort(key=lambda post: post[sort_field].lower(), reverse=reverse)

    start = (page - 1) * per_page
    end = start + per_page
    paginated = result_posts[start:end]

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": len(result_posts),
        "posts": paginated})


@app.route('/api/posts', methods=['POST'])
@limiter.limit("50/hour")
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
            "message": "Please provide non-empty 'title' and 'content'."}), 400

    new_id = max([post["id"] for post in POSTS] or [0]) + 1
    new_post = {"id": new_id, "title": title.strip(), "content": content.strip()}
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
@limiter.limit("50/hour")
def delete_post(id):
    post = next((p for p in POSTS if p["id"] == id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    POSTS.remove(post)
    return jsonify({"message": f"Post with id {id} has been deleted."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
@limiter.limit("50/hour")
def update_post(id):
    post = next((p for p in POSTS if p["id"] == id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json() or {}
    title = data.get("title")
    content = data.get("content")

    if (title is not None and title.strip() == "") or (content is not None and content.strip() == ""):
        return jsonify({
            "error": "Fields cannot be empty",
            "message": "Title or content cannot be empty strings."}), 400

    if title is not None:
        post["title"] = title.strip()
    if content is not None:
        post["content"] = content.strip()

    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
@limiter.limit("100/hour")
def search_posts():
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