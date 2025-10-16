from flask import Flask, render_template, redirect, url_for, request, session
from flask_dance.contrib.google import make_google_blueprint, google
import random, os

app = Flask(__name__)

# ✅ Use environment variable for secret key (secure for Vercel)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super_secret_key_here")

# ✅ Google OAuth setup
# Replace "client_secret.json" with your actual credentials file.
# On Vercel, use an environment variable for this (recommended).
blueprint = make_google_blueprint(
    client_secrets_file="client_secret.json",  # or handle via env var
    redirect_url="http://localhost:5000/callback",

    scope=["profile", "email"],
)
app.register_blueprint(blueprint, url_prefix="/login")

# ✅ Allowed Google account (change this to your real Gmail)
ALLOWED_EMAIL = "bistaaaryash02@gmail.com"

# 🧠 Quiz generator function
def generate_questions(topic, difficulty, num_questions=20):
    base_questions = [
        f"What is {topic}?",
        f"Explain the concept of {topic}.",
        f"Why is {topic} important?",
        f"How does {topic} work?",
        f"What are the types of {topic}?",
        f"Give an example related to {topic}.",
        f"What problems does {topic} solve?",
        f"Describe an application of {topic}.",
        f"What challenges exist in {topic}?",
        f"Who discovered or created {topic}?",
        f"What are the advantages of {topic}?",
        f"What are the disadvantages of {topic}?",
        f"How can {topic} be improved?",
        f"What tools are used in {topic}?",
        f"What are some real-world uses of {topic}?",
        f"Describe a future impact of {topic}.",
        f"How does {topic} relate to AI?",
        f"What mathematical concepts support {topic}?",
        f"What is the most difficult part of understanding {topic}?",
        f"Explain {topic} in simple terms."
    ]
    random.shuffle(base_questions)
    return base_questions[:num_questions]

# 🏠 Home page (login required)
@app.route("/")
def home():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return f"Google login failed: {resp.text}"

    email = resp.json()["email"]

    # ✅ Only allow your Gmail account
    if email != ALLOWED_EMAIL:
        return "<h2>Access denied ❌ — Only authorized user can log in.</h2>"

    session["email"] = email
    return render_template("index.html", email=email)

# 🎯 Quiz generator route
@app.route("/generate", methods=["POST"])
def generate():
    if "email" not in session:
        return redirect(url_for("google.login"))

    topic = request.form.get("topic", "AI")
    difficulty = request.form.get("difficulty", "medium")
    num_questions = int(request.form.get("num_questions", 20))

    questions = generate_questions(topic, difficulty, num_questions)
    return render_template("quiz.html", topic=topic, difficulty=difficulty, questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
