from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_mail import Mail
app = Flask(__name__)
app.config['SECRET_KEY'] = "secretKey"

class ContactForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('Enter your email-id', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Enter your query/message', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['email'] = form.email.data
        session['subject'] = form.subject.data
        session['message'] = form.message.data
        form.name.data = ""
        form.email.data = ""
        form.subject.data = ""
        form.message.data = ""
        flash('Thanks for contacting us. We\'ll get back to you soon!')
        return redirect(url_for('index'))
    return render_template('index.html', form=form,name=session.get('name'),email=session.get('email'),subject=session.get('subject'),message=session.get('message'))
