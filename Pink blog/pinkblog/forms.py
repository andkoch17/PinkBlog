from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from pinkblog.models import User

class RegisterationForm(FlaskForm):
    username = StringField('Имя', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Адрес электронной почты', 
                            validators=[DataRequired(), Email()])
    password = PasswordField('Пароль',
                                validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', 
                                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегестрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Это имя уже занято, пожалуйтса выберте другое')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Этот адрес электронный почты уже занят, пожалуйста выберите другой')


class LoginForm(FlaskForm):
    email = StringField('Адрес электронной почты', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    username = StringField('Имя',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Адрес электронной почты',
                        validators=[Email(), DataRequired()])
    picture = FileField('Изменить аватар профиля',
                        validators=[FileAllowed(['jpg', 'png', 'jfif'])])
    submit = SubmitField('Подтвердить изменения')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()

            if user:
                raise ValidationError('Это имя уже занято, пожалуйтса выберте другое')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError('Этот адрес электронный почты уже занят, пожалуйста выберите другой')


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    submit = SubmitField('Запостить')


class PostCommentForm(FlaskForm):
    content = TextAreaField('Текст комментария', validators=[DataRequired()])
    submit = SubmitField('Отправить')