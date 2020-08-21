from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///hashing_exercise"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_route():
    """Home Route"""

    return redirect('/register')

@app.route('/register')
def get_reg_form_route():
    """New user registration route"""

    form = RegisterForm()

    return render_template('register_form.html', form=form)

@app.route('/register', methods=['POST'])
def post_user_reg_route():
    """New user registration route"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, pwd=pwd, email=email, first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()
    
    return redirect('/secret')

@app.route('/secret')
def secret_route():
    return '<h3>You made it!</h3>'