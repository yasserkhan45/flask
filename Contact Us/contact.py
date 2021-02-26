from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')