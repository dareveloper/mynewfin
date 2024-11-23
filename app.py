from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Function to load data from the JSON file
def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Route to the homepage
@app.route('/')
def home():
    posts = load_data('database.json')[:3]  # Only show 3 posts
    return render_template('index.html', posts=posts)

# Route for viewing a specific post's details
@app.route('/post/<int:post_id>')
def post_detail(post_id):
    posts = load_data('database.json')
    if post_id < len(posts):
        post = posts[post_id]
        return render_template('post_detail.html', post=post)
    else:
        return "Post not found", 404

# Admin route to edit posts
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    posts = load_data('database.json')
    
    # Allow the admin to edit the first 3 posts
    if request.method == 'POST':
        for i in range(3):
            posts[i]['title'] = request.form.get(f'title{i}')
            posts[i]['image'] = request.form.get(f'image{i}')
            posts[i]['description'] = request.form.get(f'description{i}')
        
        with open('database.json', 'w') as f:
            json.dump(posts, f)
        return redirect(url_for('home'))
    
    return render_template('admin.html', posts=posts[:3])  # Pass only the first 3 posts to the admin panel

# Forum route to display forum and handle new comments
@app.route('/forum', methods=['GET', 'POST'])
def forum():
    comments = load_data('comments.json')  # Load comments from the JSON file
    
    if request.method == 'POST':
        new_comment = request.form.get('comment')
        if new_comment:
            comments.append(new_comment)
            with open('comments.json', 'w') as f:
                json.dump(comments, f)
        return redirect(url_for('forum'))
    
    return render_template('forum.html', comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
