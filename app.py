import os
from datetime import timedelta

from flask import Flask, redirect, render_template, request, session, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import (BooleanField, EmailField, PasswordField, StringField,
                     SubmitField)
from wtforms.validators import DataRequired

from model.check_login import exist_user, is_existed

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
csrf = CSRFProtect(app)


class LoginForm(FlaskForm):
    """使用flask的wtforms防火墙创建特殊输入框等"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    Checkbox = BooleanField('Checkbox')
    submit = SubmitField('GO~')


class RegisterForm(FlaskForm):
    """使用flask的wtforms防火墙创建特殊输入框等"""

    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    Checkbox = BooleanField('Checkbox')
    submit = SubmitField('Join us~')


# /或者index
@app.route('/')
@app.route('/index')
def index():
    """index函数：作为主页的处理函数"""
    return render_template('index.html')


# skipcq: PY-S6007
@app.route('/login', methods=['GET', 'POST'])
def login():
    """作为登录界面的处理函数，主要是对于用户的登录状态进行判断，如果用户已经登录，则直接跳转到主页，否则跳转到登录界面"""
    login_form = LoginForm()
    # register_form = RegisterForm()
    # sourcery skip: assign-if-exp, merge-nested-ifs, reintroduce-else, swap-nested-ifs
    if (
        request.method == 'POST'
        and (
            login_form.validate_on_submit()
            and request.form.get('submit') == 'GO~'
        )
    ):  # 判断是否为登录
        username = login_form.username.data
        password = login_form.password.data
        rbpwd = login_form.Checkbox.data
        if is_existed(username, password):
            session['username'] = username
            if rbpwd:
                session.permanent = True
            # 转到页面
            return redirect(url_for('welcome'))
        if exist_user(username):
            return render_template(
                'login.html',
                message="密码错误!!!笨蛋!",
                login_form=login_form,
            )
        return render_template(
            'login.html',
            message="骗子！你根本不存在！",
            login_form=login_form,
        )
    # return render_template(
    #     'login.html', login_form=login_form, register_form=register_form
    # )
    return render_template('login.html', login_form=login_form)


@app.route('/welcome', methods=['GET'])
def welcome():
    """作为欢迎界面的处理函数，登录完跳转到这个页面进行欢迎，如果是没有登录跳转到这个界面则会让用户强制跳转到登录界面进行登录"""
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('login'))


if __name__ == "__main__":
    # port8080
    app.run(host='127.0.0.1', port=5000)
