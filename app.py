from flask import Flask, render_template, request, session, redirect, url_for
from flask_babel import Babel, _
import requests

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
    return render_template("checker.html", breaches=breaches, locale=get_locale())

# generator placeholder
@app.route("/generator")
def generator():
    return render_template("generator.html", locale=get_locale())

# strength page
@app.route("/strength")
def strength():
    return render_template("strength.html", locale=get_locale())

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
