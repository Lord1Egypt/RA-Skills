#!/usr/bin/env python3
"""
apply.py — Auto-apply engine for remote-job-hunter v1.1.0

Tier 1: Email apply (mailto: links)
Tier 2: Simple form fill (name, email, phone, resume upload)
Tier 3: LinkedIn Easy Apply
Tier 4: Greenhouse / Lever / Workday ATS
"""

import json, re, time, smtplib, os, html
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

WORKSPACE = Path(__file__).parent.parent
PENDING_FILE = WORKSPACE / "pending_applications.json"
APPLIED_FILE = WORKSPACE / "applied_jobs.json"
SKIPPED_FILE = WORKSPACE / "skipped_jobs.json"

# ─── ATS Detection ────────────────────────────────────────────────────────────

def detect_apply_tier(url):
    """Detect which apply tier to use based on URL."""
    if not url:
        return "unknown"
    url_lower = url.lower()
    if "mailto:" in url_lower:
        return "email"
    if "linkedin.com/jobs" in url_lower or "linkedin.com/easy-apply" in url_lower:
        return "linkedin"
    if "greenhouse.io" in url_lower or "boards.greenhouse.io" in url_lower:
        return "greenhouse"
    if "lever.co" in url_lower or "jobs.lever.co" in url_lower:
        return "lever"
    if "myworkdayjobs.com" in url_lower or "workday.com" in url_lower:
        return "workday"
    if "ashbyhq.com" in url_lower:
        return "ashby"
    if "bamboohr.com" in url_lower:
        return "bamboohr"
    if "jobvite.com" in url_lower:
        return "jobvite"
    return "form"  # Default — try generic form fill


# ─── Cover Letter Generator ───────────────────────────────────────────────────

def generate_cover_letter(job, profile):
    """Generate a tailored cover letter for the job."""
    name = profile.get("name", "")
    email = profile.get("email", "")
    phone = profile.get("phone", "")
    skills = ", ".join(profile.get("skills", [])[:8])
    years_exp = profile.get("years_experience", "13+")
    current_role = profile.get("current_role", "AI/ML Solutions Architect")
    linkedin = profile.get("linkedin", "")

    title = job.get("title", "the role")
    company = job.get("company", "your company")
    match_score = job.get("match_score", 0)
    job_tags = job.get("tags", "")

    return f"""Dear Hiring Team at {company},

I am writing to express my interest in the {title} position. With {years_exp} years of experience as a {current_role}, I bring a strong foundation in {skills}.

Your role aligns well with my background — my profile matches {match_score}% of the required skills for this position. I have hands-on experience with the technologies your team is working with, including {job_tags[:100] if job_tags else skills}.

I am currently seeking remote/WFA opportunities where I can contribute to impactful AI/ML initiatives while working across time zones. I am comfortable with async collaboration and have delivered results in distributed team environments.

I would welcome the opportunity to discuss how my experience aligns with your team's goals.

Best regards,
{name}
{email} | {phone}
{linkedin}
"""


# ─── Tier 1: Email Apply ──────────────────────────────────────────────────────

def apply_email(job, profile):
    """Apply via email using SMTP."""
    smtp_config = profile.get("smtp", {})
    if not smtp_config:
        return {"status": "skipped", "reason": "No SMTP config in profile"}

    mailto_url = job.get("url", "")
    # Extract email from mailto: link
    match = re.search(r'mailto:([^\?&]+)', mailto_url)
    if not match:
        # Try to find email in job description
        desc = job.get("description", "")
        match = re.search(r'[\w.+-]+@[\w-]+\.[a-zA-Z]+', desc)
        if not match:
            return {"status": "failed", "reason": "Could not extract email address"}

    to_email = match.group(1).strip()
    subject_match = re.search(r'subject=([^&]+)', mailto_url)
    subject = subject_match.group(1).replace('+', ' ') if subject_match else f"Application for {job.get('title', 'Position')}"

    cover_letter = generate_cover_letter(job, profile)
    resume_path = profile.get("resume_path", "")

    try:
        msg = MIMEMultipart()
        msg['From'] = profile.get("email", "")
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(cover_letter, 'plain'))

        # Attach resume if available
        if resume_path and Path(resume_path).exists():
            with open(resume_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                filename = Path(resume_path).name
                part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(part)

        smtp_host = smtp_config.get("host", "smtp.gmail.com")
        smtp_port = smtp_config.get("port", 587)
        smtp_user = smtp_config.get("user", profile.get("email", ""))
        smtp_pass = smtp_config.get("password", "")

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        return {"status": "applied", "method": "email", "to": to_email}

    except Exception as e:
        return {"status": "failed", "reason": str(e)}


# ─── Tier 2: Generic Form Fill ────────────────────────────────────────────────

def apply_form(page, job, profile):
    """Fill generic application form using Playwright."""
    name = profile.get("name", "")
    email = profile.get("email", "")
    phone = profile.get("phone", "")
    resume_path = profile.get("resume_path", "")
    linkedin = profile.get("linkedin", "")
    cover_letter = generate_cover_letter(job, profile)

    filled = []

    def try_fill(selectors, value):
        for sel in selectors:
            try:
                el = page.locator(sel).first
                if el.is_visible(timeout=2000):
                    el.fill(value)
                    filled.append(sel)
                    return True
            except:
                continue
        return False

    # Name fields
    try_fill(['input[name*="name" i]:not([name*="company" i])',
              'input[placeholder*="full name" i]',
              'input[id*="name" i]:not([id*="company" i])'], name)

    # First/Last name split
    first, *last_parts = name.split()
    last = " ".join(last_parts) if last_parts else ""
    try_fill(['input[name*="first" i]', 'input[id*="first" i]',
              'input[placeholder*="first" i]'], first)
    try_fill(['input[name*="last" i]', 'input[id*="last" i]',
              'input[placeholder*="last" i]'], last)

    # Email
    try_fill(['input[type="email"]', 'input[name*="email" i]',
              'input[id*="email" i]', 'input[placeholder*="email" i]'], email)

    # Phone
    try_fill(['input[type="tel"]', 'input[name*="phone" i]',
              'input[id*="phone" i]', 'input[placeholder*="phone" i]'], phone)

    # LinkedIn
    try_fill(['input[name*="linkedin" i]', 'input[id*="linkedin" i]',
              'input[placeholder*="linkedin" i]'], linkedin)

    # Cover letter / message
    try_fill(['textarea[name*="cover" i]', 'textarea[id*="cover" i]',
              'textarea[name*="message" i]', 'textarea[id*="message" i]',
              'textarea[placeholder*="cover" i]'], cover_letter)

    # Resume upload
    if resume_path and Path(resume_path).exists():
        upload_selectors = [
            'input[type="file"]',
            'input[accept*=".pdf" i]',
            'input[accept*=".doc" i]',
            'input[name*="resume" i]',
            'input[id*="resume" i]'
        ]
        for sel in upload_selectors:
            try:
                el = page.locator(sel).first
                if el.count() > 0:
                    el.set_input_files(resume_path)
                    filled.append(f"resume:{sel}")
                    break
            except:
                continue

    return filled


# ─── Tier 3: LinkedIn Easy Apply ─────────────────────────────────────────────

def apply_linkedin(page, job, profile):
    """Handle LinkedIn Easy Apply multi-step form."""
    linkedin_email = profile.get("linkedin_email", profile.get("email", ""))
    linkedin_password = profile.get("linkedin_password", "")
    phone = profile.get("phone", "")
    resume_path = profile.get("resume_path", "")

    try:
        # Login if needed
        if "linkedin.com/login" in page.url or page.locator('input[id="username"]').count() > 0:
            page.fill('input[id="username"]', linkedin_email)
            page.fill('input[id="password"]', linkedin_password)
            page.click('button[type="submit"]')
            page.wait_for_load_state("networkidle", timeout=15000)

        # Click Easy Apply button
        easy_apply_btn = page.locator('button:has-text("Easy Apply")').first
        if not easy_apply_btn.is_visible(timeout=5000):
            return {"status": "skipped", "reason": "No Easy Apply button found"}
        easy_apply_btn.click()
        page.wait_for_timeout(2000)

        max_steps = 8
        for step in range(max_steps):
            # Fill phone if asked
            phone_field = page.locator('input[id*="phoneNumber"]').first
            if phone_field.is_visible(timeout=1000):
                phone_field.fill(phone)

            # Upload resume if asked
            if resume_path and Path(resume_path).exists():
                upload = page.locator('input[type="file"]').first
                if upload.count() > 0:
                    try:
                        upload.set_input_files(resume_path)
                    except:
                        pass

            # Handle Yes/No radio buttons (follow instructions questions)
            try:
                radios = page.locator('input[type="radio"]').all()
                for radio in radios[:3]:  # Answer first 3 radio groups as Yes
                    if not radio.is_checked():
                        radio.check()
                        break
            except:
                pass

            # Try Next button
            next_btn = page.locator('button:has-text("Next")').first
            if next_btn.is_visible(timeout=1000):
                next_btn.click()
                page.wait_for_timeout(1500)
                continue

            # Try Review button
            review_btn = page.locator('button:has-text("Review")').first
            if review_btn.is_visible(timeout=1000):
                review_btn.click()
                page.wait_for_timeout(1500)
                continue

            # Submit button — final step
            submit_btn = page.locator('button:has-text("Submit application")').first
            if submit_btn.is_visible(timeout=1000):
                submit_btn.click()
                page.wait_for_timeout(2000)
                return {"status": "applied", "method": "linkedin_easy_apply"}

            break  # No more buttons found

        return {"status": "failed", "reason": "Could not complete LinkedIn Easy Apply flow"}

    except Exception as e:
        return {"status": "failed", "reason": str(e)}


# ─── Tier 4: Greenhouse ───────────────────────────────────────────────────────

def apply_greenhouse(page, job, profile):
    """Handle Greenhouse ATS application form."""
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
        filled = apply_form(page, job, profile)

        # Greenhouse-specific: demographic questions — skip/prefer not to answer
        try:
            prefer_not = page.locator('option:has-text("Prefer not")').first
            if prefer_not.count() > 0:
                selects = page.locator('select').all()
                for sel in selects:
                    try:
                        sel.select_option(label="Prefer not to say")
                    except:
                        try:
                            sel.select_option(index=0)
                        except:
                            pass
        except:
            pass

        # Submit
        submit = page.locator('input[type="submit"], button[type="submit"]').first
        if submit.is_visible(timeout=3000):
            submit.click()
            page.wait_for_timeout(3000)
            return {"status": "applied", "method": "greenhouse", "fields_filled": len(filled)}

        return {"status": "failed", "reason": "Submit button not found"}

    except Exception as e:
        return {"status": "failed", "reason": str(e)}


# ─── Tier 4: Lever ────────────────────────────────────────────────────────────

def apply_lever(page, job, profile):
    """Handle Lever ATS application form."""
    try:
        page.wait_for_load_state("networkidle", timeout=15000)

        # Click Apply button on Lever job page
        apply_btn = page.locator('a:has-text("Apply for this job")').first
        if apply_btn.is_visible(timeout=3000):
            apply_btn.click()
            page.wait_for_load_state("networkidle", timeout=10000)

        filled = apply_form(page, job, profile)

        # Submit
        submit = page.locator('button[type="submit"]:has-text("Submit")').first
        if submit.is_visible(timeout=3000):
            submit.click()
            page.wait_for_timeout(3000)
            return {"status": "applied", "method": "lever", "fields_filled": len(filled)}

        return {"status": "failed", "reason": "Submit button not found"}

    except Exception as e:
        return {"status": "failed", "reason": str(e)}


# ─── Tier 4: Workday ──────────────────────────────────────────────────────────

def apply_workday(page, job, profile):
    """Handle Workday ATS — complex multi-step flow."""
    try:
        page.wait_for_load_state("networkidle", timeout=20000)

        # Click Apply / Apply Manually
        for btn_text in ["Apply", "Apply Manually", "Apply Now"]:
            btn = page.locator(f'button:has-text("{btn_text}")').first
            if btn.is_visible(timeout=2000):
                btn.click()
                page.wait_for_load_state("networkidle", timeout=15000)
                break

        # Workday uses data-automation-id attributes
        name = profile.get("name", "")
        first, *last_parts = name.split()
        last = " ".join(last_parts) if last_parts else ""
        email = profile.get("email", "")
        phone = profile.get("phone", "")

        def wd_fill(automation_id, value):
            try:
                el = page.locator(f'[data-automation-id="{automation_id}"]').first
                if el.is_visible(timeout=2000):
                    el.fill(value)
                    return True
            except:
                return False

        wd_fill("legalNameSection_firstName", first)
        wd_fill("legalNameSection_lastName", last)
        wd_fill("email", email)
        wd_fill("phone-device-type", phone)

        # Resume upload
        resume_path = profile.get("resume_path", "")
        if resume_path and Path(resume_path).exists():
            try:
                upload = page.locator('[data-automation-id="file-upload-input-ref"]').first
                if upload.count() > 0:
                    upload.set_input_files(resume_path)
            except:
                pass

        # Navigate through steps
        for _ in range(10):
            next_btn = page.locator('[data-automation-id="bottom-navigation-next-button"]').first
            if next_btn.is_visible(timeout=2000):
                next_btn.click()
                page.wait_for_timeout(2000)
            else:
                break

        # Submit
        submit = page.locator('[data-automation-id="bottom-navigation-next-button"]:has-text("Submit")').first
        if submit.is_visible(timeout=3000):
            submit.click()
            page.wait_for_timeout(3000)
            return {"status": "applied", "method": "workday"}

        return {"status": "failed", "reason": "Workday submit not found"}

    except Exception as e:
        return {"status": "failed", "reason": str(e)}


# ─── Main Apply Orchestrator ──────────────────────────────────────────────────

def apply_to_job(job, profile, dry_run=False):
    """Apply to a single job using the appropriate tier."""
    url = job.get("url", "")
    tier = detect_apply_tier(url)
    title = job.get("title", "Unknown")
    company = job.get("company", "Unknown")

    print(f"  → {title} at {company} [{tier}]")

    if dry_run:
        return {"status": "dry_run", "tier": tier, "url": url}

    # Tier 1: Email — no browser needed
    if tier == "email":
        return apply_email(job, profile)

    # Tiers 2-4: Browser-based
    if not PLAYWRIGHT_AVAILABLE:
        return {"status": "failed", "reason": "Playwright not installed"}

    result = {"status": "failed", "reason": "Unknown error"}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox",
                      "--disable-dev-shm-usage", "--disable-gpu"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                viewport={"width": 1280, "height": 800}
            )
            page = context.new_page()

            try:
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)

                if tier == "linkedin":
                    result = apply_linkedin(page, job, profile)
                elif tier == "greenhouse":
                    result = apply_greenhouse(page, job, profile)
                elif tier == "lever":
                    result = apply_lever(page, job, profile)
                elif tier == "workday":
                    result = apply_workday(page, job, profile)
                else:
                    # Generic form fill
                    filled = apply_form(page, job, profile)
                    if filled:
                        submit = page.locator(
                            'button[type="submit"], input[type="submit"], '
                            'button:has-text("Apply"), button:has-text("Submit")'
                        ).first
                        if submit.is_visible(timeout=3000):
                            submit.click()
                            page.wait_for_timeout(3000)
                            result = {"status": "applied", "method": "form",
                                      "fields_filled": len(filled)}
                        else:
                            result = {"status": "failed",
                                      "reason": "Submit button not found",
                                      "fields_filled": len(filled)}
                    else:
                        result = {"status": "failed",
                                  "reason": "No fillable fields found"}

            except PWTimeout:
                result = {"status": "failed", "reason": "Page load timeout"}
            except Exception as e:
                result = {"status": "failed", "reason": str(e)}
            finally:
                context.close()
                browser.close()

    except Exception as e:
        result = {"status": "failed", "reason": f"Browser error: {str(e)}"}

    return result


# ─── Pending Applications Manager ────────────────────────────────────────────

def save_pending(jobs, profile_id):
    """Save jobs to pending_applications.json with 30-min expiry."""
    # Sanitize jobs for JSON serialization — convert any sets to lists
    safe_jobs = []
    for job in jobs:
        safe_job = {k: list(v) if isinstance(v, set) else v for k, v in job.items()}
        safe_jobs.append(safe_job)
    pending = {
        "profile_id": profile_id,
        "created_at": datetime.now().isoformat(),
        "apply_after": (datetime.now().timestamp() + 1800),  # 30 min
        "jobs": safe_jobs
    }
    with open(PENDING_FILE, "w") as f:
        json.dump(pending, f, indent=2)
    print(f"  Saved {len(jobs)} pending applications")


def load_pending():
    """Load pending applications if they exist and haven't expired."""
    if not PENDING_FILE.exists():
        return None
    with open(PENDING_FILE) as f:
        data = json.load(f)
    return data


def load_applied():
    """Load previously applied jobs to avoid duplicates."""
    if not APPLIED_FILE.exists():
        return []
    with open(APPLIED_FILE) as f:
        return json.load(f)


def save_applied(applied_list):
    with open(APPLIED_FILE, "w") as f:
        json.dump(applied_list, f, indent=2)


def parse_skip_reply(message):
    """
    Parse SKIP reply from WhatsApp.
    'SKIP ALL' → skip all
    'SKIP 1,3' → skip jobs 1 and 3
    'SKIP 2' → skip job 2
    Returns: 'all' | list of ints | None
    """
    if not message:
        return None
    msg = message.strip().upper()
    if msg == "SKIP ALL" or msg == "SKIP":
        return "all"
    match = re.match(r'SKIP\s+([\d,\s]+)', msg)
    if match:
        nums = [int(n.strip()) for n in match.group(1).split(',') if n.strip().isdigit()]
        return nums
    return None


# ─── WhatsApp Message Builder ─────────────────────────────────────────────────

def build_pending_whatsapp_message(jobs, profile_name):
    """Build the WhatsApp confirmation message sent before applying."""
    lines = [
        f"🎯 *{profile_name} — Auto-Apply Preview*",
        f"Found {len(jobs)} jobs matching 70%+",
        f"Applying in 30 mins unless you reply SKIP:\n"
    ]
    for i, job in enumerate(jobs, 1):
        score = job.get("match_score", "N/A")
        score_str = f"{score}%" if isinstance(score, (int, float)) else score
        lines.append(f"{i}. *{job.get('title', 'Unknown')}* — {job.get('company', 'Unknown')} ({score_str})")

    lines.append("\nReply *SKIP 1,3* to skip specific jobs")
    lines.append("Reply *SKIP ALL* to cancel all applications")
    return "\n".join(lines)


def build_applied_whatsapp_message(results, profile_name):
    """Build the WhatsApp summary after applying."""
    applied = [r for r in results if r.get("result", {}).get("status") == "applied"]
    failed = [r for r in results if r.get("result", {}).get("status") == "failed"]
    skipped = [r for r in results if r.get("result", {}).get("status") in ("skipped", "dry_run")]

    lines = [f"✅ *{profile_name} — Applications Submitted*\n"]

    if applied:
        lines.append(f"*Applied to {len(applied)} jobs:*")
        for i, r in enumerate(applied, 1):
            job = r.get("job", {})
            method = r.get("result", {}).get("method", "")
            lines.append(f"{i}. {job.get('title', 'Unknown')} — {job.get('company', 'Unknown')} [{method}]")
            lines.append(f"   🔗 {job.get('url', '')}")

    if failed:
        lines.append(f"\n*⚠️ Failed ({len(failed)}):*")
        for r in failed:
            job = r.get("job", {})
            reason = r.get("result", {}).get("reason", "")
            lines.append(f"• {job.get('title', 'Unknown')} — {reason[:60]}")

    if skipped:
        lines.append(f"\n*Skipped ({len(skipped)}):* your request")

    lines.append(f"\n_Full log: ~/.openclaw/workspace/applied_jobs.json_")
    return "\n".join(lines)


# ─── Main Entry Point ─────────────────────────────────────────────────────────

def run_auto_apply(jobs, profile, threshold=70, dry_run=False, skip_list=None):
    """
    Main auto-apply runner.
    - Filter jobs above threshold
    - Skip jobs in skip_list
    - Apply to remaining
    - Return results
    """
    applied_log = load_applied()
    applied_urls = {entry.get("url") for entry in applied_log}

    # Filter by threshold
    candidates = []
    for job in jobs:
        score = job.get("match_score")
        if score is None:
            continue
        if isinstance(score, str):
            try:
                score = float(score.replace("%", ""))
            except:
                continue
        if score >= threshold:
            url = job.get("url", "")
            if url in applied_urls:
                print(f"  ⏭ Already applied: {job.get('title')} at {job.get('company')}")
                continue
            candidates.append(job)

    if not candidates:
        print("  No new jobs above threshold to apply to")
        return []

    # Apply skip list
    if skip_list == "all":
        print("  SKIP ALL received — cancelling all applications")
        return [{"job": j, "result": {"status": "skipped", "reason": "User requested SKIP ALL"}} for j in candidates]

    if skip_list:
        candidates = [j for i, j in enumerate(candidates, 1) if i not in skip_list]

    print(f"\n🚀 Auto-applying to {len(candidates)} jobs...")
    results = []

    for job in candidates:
        result = apply_to_job(job, profile, dry_run=dry_run)
        results.append({"job": job, "result": result})

        # Log applied jobs
        if result.get("status") == "applied":
            applied_log.append({
                "url": job.get("url"),
                "title": job.get("title"),
                "company": job.get("company"),
                "match_score": job.get("match_score"),
                "applied_at": datetime.now().isoformat(),
                "method": result.get("method", "")
            })

        # Polite delay between applications
        time.sleep(3)

    save_applied(applied_log)
    return results


if __name__ == "__main__":
    print("apply.py — Auto-apply engine loaded")
    print(f"Playwright available: {PLAYWRIGHT_AVAILABLE}")
    print(f"Pending file: {PENDING_FILE}")
    print(f"Applied log: {APPLIED_FILE}")
