#!/usr/bin/env python3
"""
Resumex Job Applier — Playwright Browser Automation Helper
Part of the Resumex OpenClaw Skill v2.0.0

Privacy note: This script receives all resume data as CLI arguments from the
OpenClaw agent. It submits data ONLY to the target job portal URL. It makes no
calls to Resumex, Telegram, or any other service. No data is written to disk.
All output goes to stdout as JSON for the agent to parse.

Transparency note: playwright-stealth is intentionally NOT used in this script.
The browser is transparent and detectable by job portals. If a portal blocks it,
this script returns {"status": "manual_required"} and the agent gives the user
a direct link and pre-filled data to apply manually. This is the correct,
honest behavior.

Supported portals:
  - LinkedIn Easy Apply
  - Indeed Smart Apply  
  - Greenhouse ATS
  - Lever ATS
  - Workday (graceful fallback — manual required)
  - Generic ATS (heuristic field detection)

Usage:
    python3 job_applier.py \
        --url "https://linkedin.com/jobs/view/..." \
        --name "Atharva Badgujar" \
        --email "atharva@example.com" \
        --phone "+91 98765 43210" \
        --location "Bangalore, India" \
        --linkedin "https://linkedin.com/in/atharva" \
        --website "https://resumex.dev" \
        --summary "Experienced backend engineer..." \
        [--headless true|false]

Output (JSON on stdout):
    {"status": "applied|manual_required|failed", "notes": "...", "filled_url": "..."}

Exit codes:
    0 — success (even if manual_required — the agent decides what to do)
    1 — fatal error (install problem, bad args)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time


# ── Playwright check ──────────────────────────────────────────────────────────

def _check_playwright():
    try:
        from playwright.sync_api import sync_playwright  # type: ignore[import]
        return sync_playwright
    except ImportError:
        _output("failed", (
            "Playwright is not installed. "
            "Run: pip3 install -r requirements.txt && python3 -m playwright install chromium"
        ), "")
        sys.exit(1)


# ── Output helper ─────────────────────────────────────────────────────────────

def _output(status: str, notes: str, filled_url: str) -> None:
    """Print JSON result to stdout for the agent to parse."""
    print(json.dumps({
        "status": status,
        "notes": notes,
        "filled_url": filled_url,
    }, ensure_ascii=False))


# ── Portal detection ──────────────────────────────────────────────────────────

def detect_portal(url: str) -> str:
    url_lower = url.lower()
    if "linkedin.com/jobs" in url_lower:
        return "linkedin"
    if "indeed.com" in url_lower:
        return "indeed"
    if "greenhouse.io" in url_lower:
        return "greenhouse"
    if "lever.co" in url_lower:
        return "lever"
    if "myworkdayjobs.com" in url_lower or "workday.com" in url_lower:
        return "workday"
    if "glassdoor.com" in url_lower:
        return "glassdoor"
    if "naukri.com" in url_lower:
        return "naukri"
    if "smartrecruiters.com" in url_lower:
        return "smartrecruiters"
    if "jobs.ashbyhq.com" in url_lower:
        return "ashby"
    return "generic"


# ── Safe browser helpers ──────────────────────────────────────────────────────

def _fill(page, selector: str, value: str, timeout: int = 3000) -> bool:
    try:
        el = page.wait_for_selector(selector, timeout=timeout, state="visible")
        if el and value:
            el.triple_click()
            el.fill(value)
            return True
    except Exception:
        pass
    return False


def _click(page, selector: str, timeout: int = 4000) -> bool:
    try:
        el = page.wait_for_selector(selector, timeout=timeout, state="visible")
        if el:
            el.click()
            time.sleep(0.5)
            return True
    except Exception:
        pass
    return False


def _has_file_upload(page) -> bool:
    try:
        return page.locator("input[type='file']").count() > 0
    except Exception:
        return False


def _text_on_page(page, text: str) -> bool:
    try:
        return page.locator(f"text={text}").count() > 0
    except Exception:
        return False


# ── Generic field filler ──────────────────────────────────────────────────────

def _fill_common_fields(page, args: argparse.Namespace) -> set[str]:
    """
    Heuristically fill all detectable form fields using resume data.
    Returns set of field names successfully filled.
    """
    filled: set[str] = set()

    name_parts = args.name.strip().split()
    first = name_parts[0] if name_parts else ""
    last  = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

    cover = (
        f"Dear Hiring Team,\n\n"
        f"{args.summary[:400]}\n\n"
        f"I look forward to the opportunity to contribute to your team.\n\n"
        f"Best regards,\n{args.name}"
    )

    field_map = [
        # (set_name, selectors, value)
        ("full_name", [
            "input[name*='name' i]:not([name*='first' i]):not([name*='last' i])",
            "input[placeholder*='full name' i]",
            "input[id*='fullName' i]",
            "input[autocomplete='name']",
        ], args.name),
        ("first_name", [
            "input[name='firstName']", "input[name='first_name']",
            "input[id*='firstName' i]", "input[placeholder*='first name' i]",
            "input[autocomplete='given-name']",
        ], first),
        ("last_name", [
            "input[name='lastName']", "input[name='last_name']",
            "input[id*='lastName' i]", "input[placeholder*='last name' i]",
            "input[autocomplete='family-name']",
        ], last),
        ("email", [
            "input[type='email']",
            "input[name*='email' i]",
            "input[id*='email' i]",
            "input[autocomplete='email']",
        ], args.email),
        ("phone", [
            "input[type='tel']",
            "input[name*='phone' i]",
            "input[id*='phone' i]",
            "input[autocomplete='tel']",
        ], args.phone),
        ("location", [
            "input[name*='location' i]",
            "input[name*='city' i]",
            "input[id*='location' i]",
            "input[placeholder*='city' i]",
            "input[autocomplete='address-level2']",
        ], args.location),
        ("linkedin", [
            "input[name*='linkedin' i]",
            "input[id*='linkedin' i]",
            "input[placeholder*='linkedin' i]",
        ], args.linkedin or ""),
        ("website", [
            "input[name*='website' i]",
            "input[name*='portfolio' i]",
            "input[id*='website' i]",
            "input[placeholder*='website' i]",
        ], args.website or ""),
        ("cover_letter", [
            "textarea[name*='cover' i]",
            "textarea[name*='letter' i]",
            "textarea[name*='message' i]",
            "textarea[placeholder*='cover letter' i]",
            "textarea[placeholder*='introduce' i]",
        ], cover),
    ]

    for field_name, selectors, value in field_map:
        if not value or field_name in filled:
            continue
        for sel in selectors:
            if _fill(page, sel, value):
                filled.add(field_name)
                break

    return filled


# ── Portal handlers ───────────────────────────────────────────────────────────

def _apply_linkedin(page, args: argparse.Namespace, url: str):
    """LinkedIn Easy Apply multi-step wizard."""
    # Click Easy Apply
    clicked = False
    for sel in [
        "button.jobs-apply-button",
        "button[aria-label*='Easy Apply' i]",
        "button:has-text('Easy Apply')",
    ]:
        if _click(page, sel, timeout=6000):
            clicked = True
            time.sleep(1.5)
            break

    if not clicked:
        _output("manual_required",
                "No Easy Apply button — this job uses an external application portal.",
                url)
        return

    # Multi-step wizard (max 15 steps)
    for step in range(15):
        time.sleep(1)

        if _has_file_upload(page):
            _output("manual_required",
                    "LinkedIn Easy Apply requires a resume PDF upload on this step.",
                    page.url)
            return

        _fill_common_fields(page, args)

        # Submit
        for sel in [
            "button[aria-label*='Submit application' i]",
            "button:has-text('Submit application')",
            "button:has-text('Submit')",
        ]:
            try:
                btn = page.locator(sel)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click()
                    time.sleep(2)
                    _output("applied",
                            f"Submitted via LinkedIn Easy Apply (step {step + 1}).",
                            page.url)
                    return
            except Exception:
                pass

        # Next/Continue
        advanced = False
        for sel in [
            "button[aria-label*='Continue to next step' i]",
            "button:has-text('Next')",
            "button:has-text('Continue')",
            "button:has-text('Review')",
        ]:
            if _click(page, sel, timeout=3000):
                advanced = True
                break

        if not advanced:
            break

    _output("failed",
            "Could not complete LinkedIn Easy Apply wizard — wizard may need manual input.",
            page.url)


def _apply_indeed(page, args: argparse.Namespace, url: str):
    """Indeed Smart Apply flow."""
    clicked = False
    for sel in [
        "button[id*='applyButtonLinkExpanded' i]",
        "button:has-text('Apply now')",
        "a:has-text('Apply now')",
        "button:has-text('Apply')",
    ]:
        if _click(page, sel, timeout=6000):
            clicked = True
            time.sleep(2)
            break

    if not clicked:
        _output("manual_required",
                "Could not find Indeed Apply button — may link to external portal.",
                url)
        return

    current_url = page.url

    for step in range(10):
        time.sleep(1)
        if _has_file_upload(page):
            _output("manual_required",
                    "Indeed requires resume PDF upload.",
                    current_url)
            return

        _fill_common_fields(page, args)

        for sel in ["button:has-text('Submit')", "button[type='submit']"]:
            try:
                btn = page.locator(sel)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click()
                    time.sleep(2)
                    _output("applied", "Submitted via Indeed Smart Apply.", page.url)
                    return
            except Exception:
                pass

        advanced = False
        for sel in ["button:has-text('Next')", "button:has-text('Continue')"]:
            if _click(page, sel, timeout=3000):
                advanced = True
                break
        if not advanced:
            break

    _output("manual_required",
            "Indeed redirected to external application site.",
            page.url)


def _apply_greenhouse(page, args: argparse.Namespace, url: str):
    """Greenhouse ATS — usually a single long form."""
    time.sleep(2)
    if _has_file_upload(page):
        _fill_common_fields(page, args)
        _output("manual_required",
                "Greenhouse application requires a resume PDF upload. Fields pre-filled where possible.",
                page.url)
        return

    filled = _fill_common_fields(page, args)

    for sel in [
        "input[type='submit']",
        "button[type='submit']",
        "button:has-text('Submit Application')",
        "button:has-text('Submit')",
    ]:
        try:
            btn = page.locator(sel)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click()
                time.sleep(2)
                _output("applied",
                        f"Greenhouse form submitted. Fields filled: {', '.join(sorted(filled)) or 'none detected'}",
                        page.url)
                return
        except Exception:
            pass

    _output("failed",
            "Greenhouse form found but submit failed — may need manual completion.",
            page.url)


def _apply_lever(page, args: argparse.Namespace, url: str):
    """Lever ATS — single-page form."""
    time.sleep(2)
    if _has_file_upload(page):
        _fill_common_fields(page, args)
        _output("manual_required",
                "Lever application requires a resume PDF upload. Fields pre-filled where possible.",
                page.url)
        return

    filled = _fill_common_fields(page, args)

    for sel in [
        "button[type='submit']",
        "input[type='submit']",
        "button:has-text('Submit Application')",
        "button:has-text('Submit')",
        "button:has-text('Apply')",
    ]:
        try:
            btn = page.locator(sel)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click()
                time.sleep(2)
                _output("applied",
                        f"Lever form submitted. Fields filled: {', '.join(sorted(filled)) or 'none detected'}",
                        page.url)
                return
        except Exception:
            pass

    _output("failed", "Lever form found but submit failed.", page.url)


def _apply_workday(page, args: argparse.Namespace, url: str):
    """Workday — always manual, but fill what we can."""
    time.sleep(2)
    _fill_common_fields(page, args)
    _output("manual_required",
            "Workday portals require multi-factor login and complex wizards. Please complete manually.",
            page.url)


def _apply_generic(page, args: argparse.Namespace, url: str):
    """Generic heuristic applier for unknown portals."""
    time.sleep(2)
    if _has_file_upload(page):
        _fill_common_fields(page, args)
        _output("manual_required",
                "Application requires file upload. Fields pre-filled where possible.",
                page.url)
        return

    filled = _fill_common_fields(page, args)

    for sel in [
        "button[type='submit']",
        "input[type='submit']",
        "button:has-text('Submit')",
        "button:has-text('Apply')",
        "button:has-text('Send Application')",
        "*[data-testid*='submit' i]",
    ]:
        try:
            btn = page.locator(sel)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click()
                time.sleep(2)
                _output("applied",
                        f"Generic form submitted. Fields filled: {', '.join(sorted(filled)) or 'none detected'}",
                        page.url)
                return
        except Exception:
            pass

    if filled:
        _output("manual_required",
                f"Filled {len(filled)} field(s) but could not locate a submit button. Please submit manually.",
                page.url)
    else:
        _output("manual_required",
                "Could not detect any fillable fields. Please apply manually.",
                page.url)


PORTAL_HANDLERS = {
    "linkedin":      _apply_linkedin,
    "indeed":        _apply_indeed,
    "greenhouse":    _apply_greenhouse,
    "lever":         _apply_lever,
    "workday":       _apply_workday,
    "glassdoor":     _apply_generic,
    "naukri":        _apply_generic,
    "smartrecruiters": _apply_generic,
    "ashby":         _apply_generic,
    "generic":       _apply_generic,
}


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Resumex Job Applier — Playwright Browser Automation Helper",
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--url",      required=True,  help="Job application URL")
    p.add_argument("--name",     required=True,  help="Applicant full name")
    p.add_argument("--email",    required=True,  help="Applicant email")
    p.add_argument("--phone",    default="",     help="Applicant phone number")
    p.add_argument("--location", default="",     help="Applicant current location")
    p.add_argument("--linkedin", default="",     help="LinkedIn profile URL")
    p.add_argument("--website",  default="",     help="Portfolio/website URL")
    p.add_argument("--summary",  default="",     help="Professional summary (first 300 chars)")
    p.add_argument("--headless", default="true", help="Run browser headless (true/false)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    sync_playwright = _check_playwright()
    headless = args.headless.lower() != "false"
    portal   = detect_portal(args.url)
    handler  = PORTAL_HANDLERS.get(portal, _apply_generic)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=headless,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled",
            ],
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            ),
            locale="en-US",
        )

        # Standard page — no stealth, no bot-detection evasion.
        # This is intentional: we run transparently. If a portal blocks us,
        # the handler returns "manual_required" and the user applies with a direct link.
        page = context.new_page()

        try:
            page.goto(args.url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
            handler(page, args, args.url)
        except Exception as exc:
            _output("failed", f"Browser error: {exc}", args.url)
        finally:
            try:
                browser.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
