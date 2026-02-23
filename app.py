from flask import Flask, render_template, request, redirect, url_for
from storage import load_posts, save_posts, get_post_by_id

app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get and trim the data from the form
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        # Validate that no field is empty or whitespace-only
        if not author or not title or not content:
            error = "All fields are required and must not be blank."
            return render_template('add.html', error=error)

        # Load existing posts
        blog_posts = load_posts()

        # Generate a unique ID (handles empty list)
        new_id = max((post['id'] for post in blog_posts), default=0) + 1

        # Create and append the new post
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }
        blog_posts.append(new_post)

        # Save back to the database
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Get the updated data from the form
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load, update, and save
        blog_posts = load_posts()
        for p in blog_posts:
            if p['id'] == post_id:
                p['author'] = author
                p['title'] = title
                p['content'] = content
                break
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
