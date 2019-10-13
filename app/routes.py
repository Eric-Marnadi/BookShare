from app import app
from app.forms import LoginForm, SignUpForm, AddBook, RequestBook
from flask import render_template, redirect, flash, url_for, sessions, make_response, session, blueprints
from backendshit import add_user, supply_book, check_password, get_name, user_exists, request_book
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', user="Eric", posts=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if check_password(form.username.data, form.password.data):
            session['user'] = form.username.data
            flash("Hello " + get_name(form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit() and form.password.data == form.confirmpassword.data and not user_exists(form.username.data):
        add_user(form.firstname.data, form.lastname.data, form.email.data, form.username.data, form.password.data)
        return redirect(url_for('index'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/supply', methods=['GET','POST'])
def supply():
    form = AddBook()
    if form.validate_on_submit():
        supply_book(form.book.data, form.isbn.data, session['user'])
        return redirect(url_for('index'))
    return render_template('supply.html', title='Add Book', form=form)

@app.route('/request', methods=['GET','POST'])
def request():
    form = RequestBook()
    if form.validate_on_submit():
        request_book(form.book.data, form.isbn.data, session['user'])
        return redirect(url_for('index'))
    return render_template('request.html', title='Request Book', form=form)


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['nm']
    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie('userID', user)
    return resp

@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('userID')
   return '<h1>welcome '+name+'</h1>'