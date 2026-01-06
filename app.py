from flask import Flask, render_template, request, redirect, session, url_for, flash
import json
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "devkey")

DATA_FILE = os.path.join("static", "cms_data.json")

# -------------------- Load / Save CMS Data --------------------
def load_data():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        default = {
            "name": "Bhavani S",
            "title": "Aspiring Software Developer",
            "subtitle": "Python & Django Enthusiast",
            "hero_text": "I build efficient, user-friendly applications with modern web technologies.",
            "image": "static/uploads/default.jpeg",
            "about_text": "I am Bhavani S, a Computer Science Engineering student at PET Engineering College.",
            "skills": [{"name": "Python", "icon": ""}, {"name": "Django", "icon": ""}],
            "achievements": [{"title": "First Prize - Poster", "desc": "Won first prize at college poster competition."}],
            "experience": [{"year": "2025", "role": "Full Stack Developer", "company": "G2G Technologies", "description": "Worked on front and back end."}],
            "projects": [{"name": "To-Do App", "desc": "Simple to-do list with localStorage", "code": "", "demo": ""}],
            "blogs": [{"title": "My First Blog", "excerpt": "Intro to my journey", "content": "I started learning Python...", "date": "2025-01-01"}],
            "contact_email": "sb.bhavani.sb@gmail.com",
            "social_links": {"linkedin": "https://www.linkedin.com/in/sb-bhavani-sb", "github": "https://github.com/Bhavani-SB"}
        }
        with open(DATA_FILE, "w") as f:
            json.dump(default, f, indent=4)
        return default

    try:
        data = json.load(open(DATA_FILE))
    except json.JSONDecodeError:
        data = {}
    for key in ["skills","achievements","experience","projects","blogs","social_links"]:
        if key not in data:
            data[key] = []
    if "contact_email" not in data:
        data["contact_email"] = ""
    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------- Frontend --------------------
@app.route("/")
def home():
    data = load_data()
    current_year = datetime.now().year
    return render_template("index.html", data=data, current_year=current_year)

# -------------------- Admin Login --------------------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == "admin" and request.form.get("password") == "admin123":
            session["admin"] = True
            return redirect("/dashboard")
    return render_template("login.html")

# -------------------- Dashboard --------------------
@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if not session.get("admin"):
        return redirect("/login")

    data = load_data()
    if request.method == "POST":
        # Basic info
        data["name"] = request.form.get("name","").strip()
        data["title"] = request.form.get("title","").strip()
        data["subtitle"] = request.form.get("subtitle","").strip()
        data["hero_text"] = request.form.get("hero_text","").strip()
        data["about_text"] = request.form.get("about_text","").strip()
        
        # dashboard() image upload part
        # Image upload (FIXED & CLEAN)
        if "image" in request.files:
            img = request.files["image"]

            if img and img.filename != "":
                upload_folder = os.path.join("static", "uploads")
                os.makedirs(upload_folder, exist_ok=True)

                filename = img.filename.replace(" ", "_")
                img_path = os.path.join(upload_folder, filename)
                img.save(img_path)

        # 🚀 ONLY relative path
                data["image"] = f"uploads/{filename}"


        # Contact & social
        data["contact_email"] = request.form.get("contact_email","").strip()
        data["social_links"]["linkedin"] = request.form.get("linkedin","").strip()
        data["social_links"]["github"] = request.form.get("github","").strip()

        # Skills
        skill_names = request.form.getlist("skill_name")
        skill_icons = request.form.getlist("skill_icon")
        data["skills"] = [{"name": skill_names[i].strip(), "icon": skill_icons[i].strip() if i < len(skill_icons) else ""} for i in range(len(skill_names)) if skill_names[i].strip()]

        # Achievements
        ach_titles = request.form.getlist("achievements_title")
        ach_descs  = request.form.getlist("achievements_desc")
        data["achievements"] = [{"title": ach_titles[i].strip(), "desc": ach_descs[i].strip() if i < len(ach_descs) else ""} for i in range(len(ach_titles)) if ach_titles[i].strip()]

        # Experience
        exp_years = request.form.getlist("exp_year")
        exp_roles = request.form.getlist("exp_role")
        exp_companies = request.form.getlist("exp_company")
        exp_descs = request.form.getlist("exp_description")
        data["experience"] = [{"year": exp_years[i].strip(), "role": exp_roles[i].strip(), "company": exp_companies[i].strip(), "description": exp_descs[i].strip()} for i in range(len(exp_years)) if exp_years[i].strip() or exp_roles[i].strip()]

        # Projects
        proj_names = request.form.getlist("proj_name")
        proj_descs = request.form.getlist("proj_desc")
        proj_codes = request.form.getlist("proj_code")
        proj_demos = request.form.getlist("proj_demo")
        data["projects"] = [{"name": proj_names[i].strip(), "desc": proj_descs[i].strip(), "code": proj_codes[i].strip(), "demo": proj_demos[i].strip()} for i in range(len(proj_names)) if proj_names[i].strip()]

        # Blogs
        blog_titles = request.form.getlist("blog_title")
        blog_excerpts = request.form.getlist("blog_excerpt")
        blog_contents = request.form.getlist("blog_content")
        blog_dates = request.form.getlist("blog_date")
        data["blogs"] = [{"title": blog_titles[i].strip(), "excerpt": blog_excerpts[i].strip(), "content": blog_contents[i].strip(), "date": blog_dates[i].strip()} for i in range(len(blog_titles)) if blog_titles[i].strip()]

        save_data(data)
        return redirect("/dashboard")

    return render_template("dashboard.html", data=data)

@app.route("/contact", methods=["POST"])
def contact():
    data = load_data()

    name = request.form.get("name")
    user_email = request.form.get("user_email")
    message = request.form.get("message")

    receiver_email = data.get("contact_email")

    msg = EmailMessage()
    msg["Subject"] = f"Portfolio Contact from {name}"
    msg["From"] = "YOUR_GMAIL@gmail.com"      # CMS sender
    msg["To"] = receiver_email                # CMS receiver
    msg["Reply-To"] = user_email               # 👈 KEY POINT

    msg.set_content(f"""
You received a new message from your portfolio website.

Name: {name}
Email: {user_email}

Message:
{message}
""")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("YOUR_GMAIL@gmail.com", "APP_PASSWORD")
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(e)

    return redirect("/#contact")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
