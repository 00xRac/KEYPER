from flask import Flask, render_template, request, session, redirect, url_for
from flask_babel import Babel, _

import requests
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# Flask-Babel configuration
app.config['LANGUAGES'] = ['en', 'no']

# ✅ Use `locale_selector` when initializing Babel (Flask-Babel ≥3.0)
babel = Babel(app, locale_selector=lambda: session.get('lang', request.accept_languages.best_match(app.config['LANGUAGES'])))

# Route to change language
@app.route('/change_language/<lang>')
def change_language(lang):
    if lang in app.config['LANGUAGES']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('dashboard'))

# API for email breaches
API_URL = "https://api.xposedornot.com/v1/check-email/{}"

def get_logo_url(name):
    domain_guess = name.lower().replace(" ", "") + ".com"
    return f"https://logo.clearbit.com/{domain_guess}"

# Dashboard
@app.route("/")
def dashboard():
    boxes = [
        {"title": _("Email Breach Checker"), "icon": "./static/Carta 1.png", "link": "/checker"},
        {"title": _("Password Generator"), "icon": "./static/Llave 1.png", "link": "/generator"},
        {"title": _("Strength Check"), "icon": "./static/Candado 1.png", "link": "/strength"}
    ]
    return render_template("dashboard.html", boxes=boxes)

# Email Breach Checker
@app.route("/checker", methods=["GET", "POST"])
def checker():
    breaches = None
    if request.method == "POST":
        email = request.form.get("email")
        if email:
            try:
                response = requests.get(API_URL.format(email))
                if response.status_code == 200:
                    data = response.json()
                    raw_breaches = data.get("breaches", [])
                    breaches = []
                    for item in raw_breaches:
                        if isinstance(item, list):
                            for b in item:
                                breaches.append({"name": b, "logo": get_logo_url(b)})
                        elif isinstance(item, str):
                            breaches.append({"name": item, "logo": get_logo_url(item)})
                elif response.status_code == 404:
                    breaches = []
                else:
                    breaches = [{"error": f"Error {response.status_code}"}]
            except Exception as e:
                breaches = [{"error": str(e)}]
    return render_template("checker.html", breaches=breaches)

# Password Generator
@app.route("/generator")
def generator():
    return render_template("generator.html")

# Strength Check
@app.route("/strength")
def strength():
    return render_template("strength.html")
