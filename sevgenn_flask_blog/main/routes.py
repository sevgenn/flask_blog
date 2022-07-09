from flask import Blueprint, render_template

from sevgenn_flask_blog.models import User

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Home page')
