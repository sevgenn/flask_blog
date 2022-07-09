"""Модуль служебных утилит."""

import os
from secrets import token_hex
from PIL import Image
from flask import current_app, url_for
from flask_mail import Message
from sevgenn_flask_blog import mail


def save_picture(form_picture):
    """Изменяет аватарку пользователя под заданный размер. Возвращает имя файла."""
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,
                                'static/profile_pictures', picture_fn)

    im = Image.open(form_picture)
    output_size = (150, 150)
    im.thumbnail(output_size)
    im.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', sender=os.getenv('MAIL_USERNAME'),
                  recipients=[user.email])
    msg.body = f"""To reset the password, follow the following link: 
                {url_for('users.reset_token', token=token, _external=True)}. 
                If you have not made this request, then just ignore this letter."""
    mail.send(msg)
