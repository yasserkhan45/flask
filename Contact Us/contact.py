from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from threading import Thread

import os
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = "secretKey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

app.config['MAIL_SUBJECT_PREFIX'] = '[FLASK APP]'
app.config['MAIL_SENDER'] = 'ADMIN <khanyasser88@gmail.com>'
app.config['ADMIN'] = os.environ.get('ADMIN')


db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

def send_mail_async(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, 
    sender = app.config['MAIL_SENDER'],
    recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target = send_mail_async, args = [app, msg])
    thr.start()
    return thr
    
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True)
    email = db.Column(db.String(30), unique = True, index = True)
    subject = db.Column(db.String(150))
    message = db.Column(db.String(300))

    def __repr__(self):
        return '<User %r \nEmail %r \nSubject %r \nMessage %r>' % (self.username, self.email, self.subject, self.message)

class ContactForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('Enter your email-id', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Enter your query/message', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def index():
    name = None
    email = None
    subject = None
    message = None
    form = ContactForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None:
            user = User(username = form.name.data,
            email = form.email.data,
            subject = form.subject.data,
            message = form.message.data)
            db.session.add(user)
            db.session.commit()
            flash('Thanks for contacting us. We\'ll get back to you soon!')
            if app.config['ADMIN']:
                send_mail(app.config['ADMIN'], 'New User', 'mail/new_user', user = user)
        else:
            flash("We've already recieved your request, please wait for us to get back to you!")
        session['name'] = form.name.data
        session['email'] = form.email.data
        session['subject'] = form.subject.data
        session['message'] = form.message.data
        form.name.data = ""
        form.email.data = ""
        form.subject.data = ""
        form.message.data = ""
        return redirect(url_for('index'))
    return render_template('index.html', 
    form = form, 
    name = session.get('name'), 
    email = session.get('email'), 
    subject = session.get('subject'), 
    message = session.get('message'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('505.html'), 505