# KEYPER

**KEYPER** is a web-based security toolkit built with Flask. It includes an **Email Breach Checker**, a **Password Generator**, and a **Password Strength Checker**. The app supports **English** and **Norwegian** translations via Flask-Babel.

---

## Features

### 1. Email Breach Checker
- Enter your email to check if it has appeared in known data breaches.
- Displays the service logos alongside the breached service names.
- Provides a clean, card-based UI with hover effects.

### 2. Password Generator
- Generate strong passwords with customizable options:
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Symbols
- Configurable password length (4–128 characters).
- Copyable generated password directly from the UI.

### 3. Password Strength Checker
- Evaluate the strength of any password.
- Provides visual feedback on what makes a password weak (length, missing character types, etc.).
- Scores passwords from **Very Weak** to **Very Strong**.

---

## Tech Stack
- **Python 3.13+**
- **Flask** – lightweight web framework
- **Flask-Babel** – multilingual support
- **Requests** – API calls for email breach checking
- **Gunicorn** – production-ready WSGI server
- **Bootstrap 5** – responsive design and UI components
- **Custom CSS** – futuristic, card-based interface

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/keyper.git
cd keyper

