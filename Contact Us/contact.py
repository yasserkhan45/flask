from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
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
    name = None
    email = None
    subject = None
    message = None
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data

        form.name.data = ""
        form.email.data = ""
        form.subject.data = ""
        form.message.data = ""
    return render_template('index.html', form=form,name=name,email=email,subject=subject,message=message)
