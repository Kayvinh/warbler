from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, URL


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField(
        'Username',
        validators=[DataRequired()],
    )

    email = StringField(
        'E-mail',
        validators=[DataRequired(), Email()],
    )

    password = PasswordField(
        'Password',
        validators=[Length(min=6)],
    )

    image_url = StringField(
        '(Optional) Image URL',
    )


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        'Username',
        validators=[DataRequired()],
    )

    password = PasswordField(
        'Password',
        validators=[Length(min=6)],
    )

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""

class ProfileEditForm(FlaskForm):
    """Form for editing user."""

    username = StringField(
        'Username',
    )

    email = StringField(
        'E-mail',
        validators=[Optional(), Email()]
    )

    image_url = StringField(
        'Image URL',
        validators=[Optional()] # URL() reqauires .TLD which we don't for localhost (consulted docs, this is recommended strategy)
    )

    header_image_url = StringField(
        'Header Image URL',
        validators=[Optional()]
    )

    bio = TextAreaField(
        'Bio',
    )

    password = PasswordField(
        'Password',
        validators=[Length(min=6)],
    )