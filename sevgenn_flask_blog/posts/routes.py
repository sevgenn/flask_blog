from flask import Blueprint, request, render_template, flash, redirect, \
    url_for, abort
from flask_login import login_required, current_user

from sevgenn_flask_blog.models import Post
from sevgenn_flask_blog.posts.forms import PostForm
from sevgenn_flask_blog import db

posts = Blueprint('posts', __name__)


@posts.route('/allposts')
@login_required
def allposts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created.desc()).paginate(page=page,
                                                              per_page=5)
    return render_template('allposts.html', title='Posts', posts=posts)


@posts.route('/post.new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.title.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post was created!', 'success')
        return redirect(url_for('posts.allposts'))
    return render_template('create_post.html', title='New Post', form=form,
                           legend='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title='post.title', post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        flash('Your post was updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template('create_post.html', title='Update Post', form=form,
                           legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post was deleted', 'success')
    return redirect(url_for('posts.allposts'))
