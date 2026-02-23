import json

DB_FILE = 'data.json'


def load_posts():
    """Read all posts from the database file."""
    with open(DB_FILE, 'r') as f:
        return json.load(f)


def save_posts(posts):
    """Write all posts to the database file."""
    with open(DB_FILE, 'w') as f:
        json.dump(posts, f, indent=4)


def get_post_by_id(post_id):
    """Return a single post by its ID, or None if not found."""
    for post in load_posts():
        if post['id'] == post_id:
            return post
    return None
