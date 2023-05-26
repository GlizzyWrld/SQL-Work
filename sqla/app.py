from flask import Flask, request, render_template, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag


app = Flask(__name__)

app.debug = True


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///localhostpostgreSQLDB/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'mrhackerman99'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app) 

connect_db(app)

@app.route('/')
def home_page():
    """Shows home page with most recent posts"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(7).all()
    return render_template('posts/home.html', posts=posts)

#User routes

@app.route('/users')
def users_index():
    """Shows the list of users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=['GET'])
def new_user_form():
    """Shows new user form"""
    return render_template('users/new.html')

@app.route('/users/new', methods=['POST'])
def new_user():
    """Shows new user"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url']
        or None
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Shows user edit form"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_users(user_id):
    """Handle form and update existing user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form ['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"{user.fullname} was updated")

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Handle form and delete existing user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"{user.fullname} was deleted")

    return redirect('/users')


# Post routes

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Shows form for new post for user"""
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)

@app.route('/users/<int:user_id>/post/new', methods=['POST'])
def new_posts(user_id):
    """Handle form submission for creating new post"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'], content=request.form['content'], user=user)
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post added")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """Shows a page with post info """
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show form to edit post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    """handle form submission for updating post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    flash(f"Post edited")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Handle form submission to delete post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post deleted")

    return redirect(f"/users/{post.user_id}")

@app.route('/tags')
def index_tags():
    """Show info on all tags"""
    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new')
def tags_new_form():
    """Form for creating new tag"""
    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)

@app.route('/tags/new', methods=['POST'])
def new_tags():
    """Handle form submission for creating a tag"""
    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids).all())
    new_tag = Tag(name=request.form['name'], posts=posts)
    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added")

    return redirect('/tags')

@app.route('tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Edit a an existing tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tags(tag_id):
    """Handle form for updating a tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited")

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def tags_destroy(tag_id):
    """Handle form for deleting a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted")

    return redirect('/tags')

