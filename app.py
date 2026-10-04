from datetime import datetime
from pathlib import Path
import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sökväg till JSON-filen där alla inlägg sparas
DATA_FILE = Path(__file__).parent / "guestbook.json"


def load_entries():
    """Läs alla inlägg från JSON-filen. Returnerar en tom lista om filen saknas eller är trasig."""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_entries(entries):
    """Skriv alla inlägg till JSON-filen."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    # Nyaste inlägget högst upp
    entries = list(reversed(load_entries()))
    return render_template("index.html", entries=entries)


@app.route("/add", methods=["POST"])
def add_entry():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    homepage = request.form.get("homepage", "").strip()
    comment = request.form.get("comment", "").strip()

    # Enkel validering: namn och kommentar måste vara ifyllda
    if name and comment:
        entries = load_entries()
        entries.append(
            {
                "name": name,
                "email": email,
                "homepage": homepage,
                "comment": comment,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        )
        save_entries(entries)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
