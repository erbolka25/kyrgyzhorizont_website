# ---------------------------------------------------------
#  Kyrgyz Horizont — Flask App (English only + WhatsApp)
#  Stable Production Build — Clean & Ready for Deployment
# ---------------------------------------------------------

from flask import Flask, render_template, request, url_for, jsonify
from datetime import datetime
import os
import logging
import smtplib
import ssl
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------
# APP CONFIG
# ---------------------------------------------------------

app = Flask(__name__)

# Analytics (optional)
app.config["GA4_MEASUREMENT_ID"] = os.getenv("GA4_MEASUREMENT_ID", "")
app.config["META_PIXEL_ID"] = os.getenv("META_PIXEL_ID", "")

# Email settings
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")  # Gmail App Password
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", EMAIL_SENDER)

# Logging
handler = RotatingFileHandler("app.log", maxBytes=500_000, backupCount=3, encoding="utf-8")
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# SITE SETTINGS
# ---------------------------------------------------------

SITE = {
    "name": "Kyrgyz Horizont",
    "tagline": "Authentic small-group adventures in Kyrgyzstan",
    "domain": "https://kyrgyzhorizont.com",
}

WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "996507282027")
WHATSAPP_LINK = (
    f"https://wa.me/{WHATSAPP_NUMBER}"
    f"?text=Hi!%20I%20want%20to%20plan%20a%20trip%20in%20Kyrgyzstan."
)

# ---------------------------------------------------------
# TOURS
# ---------------------------------------------------------

TOURS = [
    {
        "slug": "ala-kul-trek",
        "title": "Ala-Kul Trek (3D/2N)",
        "price": 249,
        "duration": "3 days",
        "level": "Moderate",
        "image": "image/ala-kul.jpg",
        "alt": "Ala-Kul glacier lake",
        "summary": "Alpine lake trek with panoramic passes.",
    },
    {
        "slug": "issyk-kul-classic",
        "title": "Issyk-Kul Classic (2D/1N)",
        "price": 189,
        "duration": "2 days",
        "level": "Easy",
        "image": "image/yssuk-kul.jpg",
        "alt": "Issyk-Kul lake",
        "summary": "Beaches, canyons and petroglyphs.",
    },
    {
        "slug": "song-kol-yurt",
        "title": "Song-Kol Yurt Stay",
        "price": 159,
        "duration": "2 days",
        "level": "Easy",
        "image": "image/sunset.jpg",
        "alt": "Song-Kol lake at sunset",
        "summary": "Yurt stay, horses and nomadic shepherd culture.",
    },
]

# ---------------------------------------------------------
# GLOBAL TEMPLATE VARIABLES
# ---------------------------------------------------------

@app.context_processor
def inject_globals():
    return {
        "site": SITE,
        "WHATSAPP_LINK": WHATSAPP_LINK,
        "WHATSAPP_NUMBER": WHATSAPP_NUMBER,
        "tours": TOURS,
        "GA4_MEASUREMENT_ID": app.config.get("GA4_MEASUREMENT_ID"),
        "META_PIXEL_ID": app.config.get("META_PIXEL_ID"),
    }

# ---------------------------------------------------------
# SEO META
# ---------------------------------------------------------

def site_meta(**extra):
    default_img = url_for("static", filename="image/cover-default.webp")
    base = {
        "title": f"{SITE['name']} — {SITE['tagline']}",
        "description": "Custom travel planning and local support across Kyrgyzstan.",
        "image": default_img,
        "url": request.base_url,
    }
    base.update(extra)
    return base

# ---------------------------------------------------------
# EMAIL SENDER (UTF-8 SAFE)
# ---------------------------------------------------------

def send_email(name, email, message, tour="", phone="", source="contact"):
    # Если env не настроен — просто логируем, но сайт не падает
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        app.logger.warning("EMAIL_SENDER/EMAIL_PASSWORD not set. Skipping email send.")
        return False

    subject_owner = "New Travel Request — Kyrgyz Horizont"

    body_owner = f"""
New message from Kyrgyz Horizont:

Name: {name}
Email: {email}
Phone: {phone}
Tour: {tour}
Source: {source}

Message:
{message}

Time (UTC): {datetime.utcnow().isoformat()}
"""

    msg_owner = (
        f"Subject: {subject_owner}\n"
        f"Content-Type: text/plain; charset=utf-8\n\n"
        f"{body_owner}"
    )

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg_owner.encode("utf-8"))
        return True

    except Exception as e:
        app.logger.error(f"Email send error: {e}")
        return False

# ---------------------------------------------------------
# ROUTES (важно: имена функций = endpoint для url_for)
# ---------------------------------------------------------

@app.route("/")
def index():
    return render_template(
        "index.html",
        meta=site_meta(
            title="Kyrgyz Horizont — Travel Planning",
            description="Independent trip planning with full WhatsApp support."
        )
    )

@app.route("/contact")
def contact():
    return render_template(
        "contact.html",
        meta=site_meta(
            title="Contact Kyrgyz Horizont",
            description="Fast support via WhatsApp and email."
        )
    )

@app.route("/gallery")
@app.route("/gallery/")
def gallery():
    return render_template(
        "gallery.html",
        meta=site_meta(
            title="Gallery — Kyrgyzstan",
            description="Beautiful landscapes of Kyrgyzstan."
        )
    )

@app.route("/solo")
@app.route("/solo/")
def solo():
    return render_template(
        "solo.html",
        meta=site_meta(
            title="Solo Travel in Kyrgyzstan",
            description="Safe routes and 24/7 support."
        )
    )

@app.route("/plan")
@app.route("/plan/")
def plan_page():
    return render_template(
        "plan.html",
        meta=site_meta(
            title="Plan My Trip",
            description="Personal itinerary prepared within 24 hours."
        )
    )

@app.route("/regions")
@app.route("/regions/")
def regions():
    return render_template(
        "regions.html",
        meta=site_meta(
            title="Regions of Kyrgyzstan",
            description="Discover Issyk-Kul, Osh, Naryn, Karakol and more."
        )
    )

@app.route("/about")
@app.route("/about/")
def about():
    return render_template(
        "about.html",
        meta=site_meta(
            title="About Kyrgyz Horizont",
            description="Meet Erbol — your personal trip planner."
        )
    )

# ---------------------------------------------------------
# CONTACT FORM API
# ---------------------------------------------------------

@app.post("/send_message")
def send_message_route():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    tour = request.form.get("tour", "").strip()
    message = request.form.get("message", "").strip()
    dates = request.form.get("dates", "").strip()
    budget = request.form.get("budget", "").strip()
    style = request.form.get("style", "").strip()
    regions = request.form.get("regions", "").strip()
    source = request.form.get("source", "contact").strip()

    if not (name and email and message):
        return jsonify({"ok": False, "error": "Missing fields"}), 400

    # Build full message with optional plan fields
    full_message = message
    extras = []
    if dates:    extras.append(f"Dates: {dates}")
    if budget:   extras.append(f"Budget: {budget}")
    if style:    extras.append(f"Style: {style}")
    if regions:  extras.append(f"Regions: {regions}")
    if extras:
        full_message = "\n".join(extras) + "\n\n" + message

    # Save message locally
    try:
        with open("messages.txt", "a", encoding="utf-8") as f:
            f.write(
                f"{datetime.utcnow().isoformat()}\t{name}\t{email}\t{phone}\t{tour}\t{full_message}\n"
            )
    except Exception as e:
        app.logger.error(f"Write error: {e}")

    # Send email to owner
    email_ok = send_email(name, email, full_message, tour=tour, phone=phone, source=source)

    return jsonify({"ok": True, "email_sent": email_ok})

# ---------------------------------------------------------
# 404 PAGE
# ---------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", meta=site_meta(title="404 — Page Not Found")), 404

# ---------------------------------------------------------
# START APP
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
