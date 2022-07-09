from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, \
    BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError
from flask_login import current_user

from sevgenn_flask_blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('User name: ',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm the password: ',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'The username you have chosen is already taken. '
                'Please choose another one.'
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email address is already taken. '
                'Please use another one.'
            )


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('User name: ',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    picture = FileField('Update a profile picture: ',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'The username you have chosen is already taken. '
                    'Please choose another one.'
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'This email address is already taken.'
                    'Please use another one.'
                )


class RequestResetForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    submit = SubmitField('Change the password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with this email address.'
                'You can register it.'
            )


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm the password: ',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Change the password')
