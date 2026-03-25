# MasterBlog API
MasterBlog API is a simple RESTful blog backend built with Flask. It allows you to create, read, update, and delete blog posts. The application also supports searching, sorting, pagination, and basic rate limiting to prevent abuse.

## Features
* CRUD operations: Create, Read, Update, Delete posts
* Search: Filter posts by title or content
* Sorting: Sort posts by title or content, ascending or descending
* Pagination: Load posts page by page
* Rate limiting: Prevents too many requests
* CORS enabled: Works with a separate frontend

## Technology Stack
* Backend: Python, Flask, Flask-CORS, Flask-Limiter
* Frontend: Simple HTML/CSS/JavaScript
* API Endpoints
* GET /api/posts – Retrieve all posts
* POST /api/posts – Add a new post
* PUT /api/posts/<id> – Update a post
* DELETE /api/posts/<id> – Delete a post
* GET /api/posts/search?title=&content= – Search posts

## How to Run
* Clone the repository
* Install packages
* Start the server: python backend_app.py
* Open the frontend: http://127.0.0.1:5001/
