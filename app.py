import random
import string
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_babel import Babel, _
import re
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super-secret-key"  # necesario para sesiones

# Idiomas soportados
app.config['LANGUAGES'] = ['en', 'no']

# Inicializar Babel con locale selector
def get_locale():
    if 'lang' in session:
        return session['lang']
    return request.accept_languages.best_match(app.config['LANGUAGES'])

babel = Babel(app, locale_selector=get_locale)

API_URL = "https://api.xposedornot.com/v1/check-email/{}"

def get_logo_url(name):
    domain_guess = name.lower().replace(" ", "") + ".com"
    return f"https://logo.clearbit.com/{domain_guess}"

# Ruta para cambiar idioma
@app.route("/change_language/<lang>")
def change_language(lang):
    if lang in app.config['LANGUAGES']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('dashboard'))

# Main dashboard with clickable boxes
@app.route("/")
def dashboard():
    boxes = [
        {"title": _("Email Breach Checker"), "icon": "./static/Carta 1.png", "link": "/checker"},
        {"title": _("Password Generator"), "icon": "./static/Llave 1.png", "link": "/generator"},
        {"title": _("Strength Check"), "icon": "./static/Candado 1.png", "link": "/strength"}
    ]
    return render_template("dashboard.html", boxes=boxes, locale=get_locale())

# Email Breach Checker page
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
                    current_year = datetime.now().year  # or use a mapping if you want
                    for item in raw_breaches:
                        if isinstance(item, list):
                            for b in item:
                                breaches.append({
                                    "name": b,
                                    "logo": get_logo_url(b),
                                    "year": current_year
                                })
                        elif isinstance(item, str):
                            breaches.append({
                                "name": item,
                                "logo": get_logo_url(item),
                                "year": current_year
                            })
                elif response.status_code == 404:
                    breaches = []
                else:
                    breaches = [{"error": _("Error %(code)s", code=response.status_code)}]
            except Exception as e:
                breaches = [{"error": str(e)}]
    return render_template("checker.html", breaches=breaches, locale=get_locale())

# Generator page
@app.route("/generator")
def generator():
    return render_template("generator.html", locale=get_locale())

@app.route("/generate_password", methods=["POST"])
def generate_password():
    data = request.get_json() or {}
    length = int(data.get("length", 12))
    use_upper = data.get("uppercase", True)
    use_lower = data.get("lowercase", True)
    use_digits = data.get("digits", True)
    use_symbols = data.get("symbols", True)

    pool = ""
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += "!@#$%&*"

    if not pool:
        return jsonify({"error": _("Please select at least one character type.")}), 400

    if length < 4 or length > 128:
        return jsonify({"error": _("Password length must be between 4 and 128.")}), 400

    password = "".join(random.choice(pool) for _ in range(length))
    return jsonify({"password": password})

# Strength page
@app.route("/strength")
def strength():
    return render_template("strength.html", locale=get_locale())

@app.route("/check_strength", methods=["POST"])
def check_strength():
    data = request.get_json() or {}
    password = data.get("password", "")

    if not password:
        return jsonify({"error": _("Password cannot be empty.")}), 400

    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append(_("Use at least 8 characters."))

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append(_("Include at least one uppercase letter."))

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append(_("Include at least one lowercase letter."))

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append(_("Include at least one number."))

    if re.search(r"[!@#$%&*]", password):
        score += 1
    else:
        feedback.append(_("Include at least one symbol."))

    strength_levels = [
        _("Very Weak"),
        _("Weak"),
        _("Medium"),
        _("Strong"),
        _("Very Strong")
    ]
    strength = strength_levels[score-1] if score > 0 else _("Very Weak")

    return jsonify({
        "strength": strength,
        "score": score,
        "feedback": feedback
    })

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
