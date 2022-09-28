from datetime import datetime
from operator import truediv
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Regexp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is a very hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[DataRequired()])
    emailAddress = EmailField('What is your UofT Email address?',validators=[DataRequired()])
    # Regexp('\w?@.?utoronto.?',message='Please enter a UofT email')
    submit = SubmitField('Submit')


@app.route('/', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.emailAddress.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.emailAddress.data
        substring = 'utoronto'
        if substring in form.emailAddress.data:
            session['isValidEmail'] = True
        else:
            session['isValidEmail'] = False
        return redirect(url_for('index'))
    # return render_template('index.html', current_time=datetime.utcnow())
    return render_template('index.html', name=session.get('name'), form=form, emailAddress=session.get('email'), isValidEmail=session.get('isValidEmail'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)