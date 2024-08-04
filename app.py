from flask import Flask, render_template, request
import logging
from logging import Formatter, FileHandler
from supabase import create_client, Client
from forms import *
import subprocess

app = Flask(__name__)
app.config.from_object('config')

# Supabase configuration
SUPABASE_URL = "https://sndaxdsredktgpsakage.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNuZGF4ZHNyZWRrdGdwc2FrYWdlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyMjcxOTIyNywiZXhwIjoyMDM4Mjk1MjI3fQ.62q7Xfaifhqg26p6wapWd-bOfekg3ACHw85W4p0h8yM"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

subprocess.run(["python", "trashdetector.py"])

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')
    
@app.route('/leaderboard')
def leaderboard():
    try:
        response = supabase.table('leaderboard').select('*').order('aura', desc=True).execute()
        entries = response.data
        app.logger.info(f"Supabase response: {response}")
        return render_template('pages/leaderboard.html', entries=entries)
    except Exception as e:
        app.logger.error(f"Error fetching leaderboard entry: {str(e)}")
        return render_template('errors/500.html'), 500

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)

@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)

@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    import logging
    from logging import Formatter, FileHandler
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    app.run(debug=True)
