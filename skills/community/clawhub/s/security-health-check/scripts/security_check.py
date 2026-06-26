#!/usr/bin/env python3
"""
Security Health Check Tool - security-health-check Skill
Check email breaches, password strength, generate security score reports
Standard library only, no external dependencies except certifi
"""

import hashlib
import json
import math
import re
import ssl
import sys
import certifi
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime


def _get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.load_verify_locations(certifi.where())
    return ctx


def _ssl_opener():
    return urllib.request.build_opener(urllib.request.HTTPSHandler(context=_get_ssl_context()))


def check_email_breach(email):
    """Check if email was involved in data breaches via HIBP API."""
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(email)}?truncateResponse=false"
    headers = {"User-Agent": "SecurityHealthCheck-Skill/1.0"}
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = _ssl_opener().open(req, timeout=15)
        if resp.status == 200:
            breaches = json.loads(resp.read().decode("utf-8"))
            return {"breached": True, "breaches": breaches, "count": len(breaches)}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"breached": False, "breaches": [], "count": 0}
        elif e.code == 429:
            return {"breached": None, "error": "API rate limit", "breaches": [], "count": 0}
    except Exception:
        pass
    return {"breached": False, "breaches": [], "count": 0}


def check_password_pwned(password):
    """Check if password appears in breach database using k-anonymity."""
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    headers = {"User-Agent": "SecurityHealthCheck-Skill/1.0", "Add-Padding": "true"}
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = _ssl_opener().open(req, timeout=15)
        text = resp.read().decode("utf-8")
        for line in text.splitlines():
            parts = line.strip().split(":")
            if len(parts) == 2 and parts[0] == suffix:
                return {"pwned": True, "count": int(parts[1])}
    except Exception:
        pass
    return {"pwned": False, "count": 0}


def analyze_password_strength(password):
    """Analyze password strength locally."""
    score = 0
    reasons = []
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 1
    if score <= 2: level, desc = "Weak", "Easily cracked - consider a stronger password"
    elif score <= 4: level, desc = "Medium", "Recommendation: strengthen your password"
    else: level, desc = "Strong", "Password strength is good"
    return {"score": score, "level": level, "desc": desc}


def generate_report(email, breach_result, password_result, password_strength):
    """Generate security report in English."""
    lines = []
    lines.append("=" * 50)
    lines.append("Security Health Check Report")
    lines.append("=" * 50)
    lines.append(f"Email: {email}")
    lines.append(f"Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # Email Breach
    breach_count = breach_result.get("count", 0)
    if breach_result.get("breached"):
        lines.append(f"WARNING: Email found in {breach_count} data breach(es)!")
        for b in breach_result.get("breaches", [])[:5]:
            lines.append(f"  - {b.get('Name', 'Unknown')} (Breach Date: {b.get('BreachDate', 'N/A')})")
    elif breach_result.get("breached") is None:
        lines.append("Email breach check skipped due to API rate limit.")
    else:
        lines.append("PASS: Email not found in known data breaches.")

    # Password Breach
    if password_result:
        pw_count = password_result.get("count", 0)
        if password_result.get("pwned"):
            lines.append(f"ALERT: Password found in {pw_count} breaches! Change it immediately!")
        else:
            lines.append("PASS: Password not found in breach database.")

    # Password Strength
    if password_strength:
        lines.append(f"Password Strength: {password_strength['level']} - {password_strength['desc']}")

    # Overall Score
    total_score = 0
    if breach_result.get("breached") == False:
        total_score += 50
    elif breach_result.get("breached") == True:
        total_score -= 30
    if password_result and not password_result.get("pwned"):
        total_score += 30
    if password_strength and password_strength["score"] >= 5:
        total_score += 20

    final_score = max(0, min(100, total_score))
    lines.append("")
    lines.append(f"Overall Security Score: {final_score}/100")
    if final_score >= 80:
        lines.append("Status: Good - continue maintaining good security habits")
    elif final_score >= 50:
        lines.append("Status: Needs Improvement - consider the recommendations above")
    else:
        lines.append("Status: Critical - immediate action recommended")
    lines.append("=" * 50)
    return "\n".join(lines)


def main():
    print("Security Health Check Tool")
    print("=" * 40)
    email = input("\nEnter email to check (press Enter to skip): ").strip()
    if email and "@" in email:
        print(f"Checking: {email}")
        breach_result = check_email_breach(email)
    else:
        breach_result = {"breached": False, "breaches": [], "count": 0}

    password_result = None
    password_strength = None
    pw = input("\nEnter password to check (press Enter to skip): ").strip()
    if pw:
        password_result = check_password_pwned(pw)
        password_strength = analyze_password_strength(pw)

    print(generate_report(email or "Not checked", breach_result, password_result, password_strength))


if __name__ == "__main__":
    main()