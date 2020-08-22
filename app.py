from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

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

        session['username'] = user.username
    
    return redirect(f'/users/{user.username}')

@app.route('/login')
def get_login_form_route():
    """Login registration route"""

    form = LoginForm()

    return render_template('login_form.html', form=form)

@app.route('/login', methods=['POST'])
def post_user_login_route():
    """User login route"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        user = User.authenticate(username=username, pwd=pwd)

        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        
        return redirect('/login')

@app.route('/users/<username>')
def users_route(username):
    """Show user info GET route"""

    if 'username' in session:
        user = User.query.filter_by(username=username).first()
        feedback = Feedback.query.filter_by(username=username)
        return render_template('/user_info.html', user=user, feedback=feedback)

    return redirect('/login')

@app.route('/users/<username>/feedback/add')
def get_feedback_form_route(username):
    """Feedback form GET route"""

    if 'username' in session:
        form = FeedbackForm()
        return render_template('/feedback_form.html', form=form)
    
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['POST'])
def post_feedback_form_route(username):
    """Feedback form POST route"""

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data


        if 'username' in session:
            user_feedback = Feedback(title=title, content=content, username=username)
            db.session.add(user_feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
        
        return redirect('/login')

@app.route('/feedback/<int:id>/update')
def update_feedback_form_route(id):
    """Edit feedback route"""

    if 'username' in session:
        user_feedback = Feedback.query.get_or_404(id)
        print('***************************')
        print(user_feedback)
        form = FeedbackForm(obj=user_feedback)
        return render_template('/feedback_form.html', form=form)
    
    return redirect('/login')