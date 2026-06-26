#!/usr/bin/env python3
"""
Resumex → Telegram Resume Sender
Part of the Resumex OpenClaw Skill v1.0.1

Fetches your active resume via the Resumex API and sends a formatted
summary to a Telegram chat. Falls back to stdout if no bot token is set.

Usage:
    python3 send_pdf.py \
        --api-key  rx_your_key           (or set RESUMEX_API_KEY env var) \
        --chat-id  123456789             (or set TELEGRAM_CHAT_ID env var) \
        [--bot-token YOUR_BOT_TOKEN]     (or set TELEGRAM_BOT_TOKEN env var)

Get your Chat ID: message @userinfobot on Telegram.
Get a Bot Token:  message @BotFather on Telegram → /newbot.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

# ── Constants ─────────────────────────────────────────────────────────────────

RESUMEX_API   = "https://resumex.dev/api/v1/agent"
TELEGRAM_BASE = "https://api.telegram.org/bot"
REQUEST_TIMEOUT = 15


# ── API helpers ───────────────────────────────────────────────────────────────

def _json_request(url: str, payload: dict | None = None, method: str | None = None) -> dict:
    """
    Make a JSON HTTP request. GET by default, POST if payload is given.
    Raises RuntimeError on HTTP errors with the response body included.
    """
    data = json.dumps(payload).encode("utf-8") if payload else None
    resolved_method = method or ("POST" if data else "GET")
    req = urllib.request.Request(
        url,
        data=data,
        method=resolved_method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error reaching {url}: {exc.reason}") from exc


def fetch_workspace(api_key: str) -> dict:
    """Fetch the full workspace from the Resumex API."""
    req = urllib.request.Request(
        RESUMEX_API,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc

    if not payload.get("success"):
        raise RuntimeError(f"Resumex API error: {payload.get('error', 'Unknown error')}")

    return payload["data"]


def get_active_resume(workspace: dict) -> dict:
    """Extract the active resume's data dict from the workspace."""
    active_id = workspace.get("activeResumeId")
    resumes = workspace.get("resumes", [])

    for resume in resumes:
        if resume.get("id") == active_id:
            return resume.get("data", {})

    # Fallback: return first resume if activeResumeId is unset
    if resumes:
        print("[warn] activeResumeId not found — using first resume.", file=sys.stderr)
        return resumes[0].get("data", {})

    raise RuntimeError(
        "No resume data found in workspace. "
        "Please open resumex.dev/app and save your profile first."
    )


# ── Formatter ─────────────────────────────────────────────────────────────────

def _esc(text: str) -> str:
    """Escape Markdown special characters for Telegram MarkdownV2."""
    # MarkdownV2 reserved: _ * [ ] ( ) ~ ` > # + - = | { } . !
    for ch in r"\_*[]()~`>#+-=|{}.!":
        text = text.replace(ch, f"\\{ch}")
    return text


def format_resume_message(data: dict, parse_mode: str = "Markdown") -> str:
    """
    Build a Telegram-ready resume summary string.
    Uses basic Markdown (not V2) for broad compatibility.
    """
    profile    = data.get("profile", {})
    experience = data.get("experience", [])
    education  = data.get("education", [])
    skills     = data.get("skills", [])
    projects   = data.get("projects", [])
    achievements = data.get("achievements", [])

    name = (profile.get("fullName") or "").strip() or "Your Resume"
    lines: list[str] = []

    # ── Header ────────────────────────────────────────────────────────────────
    lines += [f"📄 *{name}*", ""]

    # ── Contact ───────────────────────────────────────────────────────────────
    contact_fields = [
        ("📧", profile.get("email")),
        ("📱", profile.get("phone")),
        ("📍", profile.get("location")),
        ("🔗", profile.get("linkedin")),
        ("🐙", profile.get("github")),
        ("🌐", profile.get("website")),
    ]
    for icon, value in contact_fields:
        if value and value.strip():
            lines.append(f"{icon} {value.strip()}")

    # ── Summary ───────────────────────────────────────────────────────────────
    summary = (profile.get("summary") or "").strip()
    if summary:
        lines += ["", "*Summary*", summary[:400] + ("…" if len(summary) > 400 else "")]

    # ── Experience ────────────────────────────────────────────────────────────
    if experience:
        lines += ["", f"*Experience* ({len(experience)} role{'s' if len(experience) != 1 else ''})"]
        for entry in experience[:4]:
            role    = (entry.get("role") or "").strip()
            company = (entry.get("company") or "").strip()
            start   = (entry.get("startDate") or "").strip()
            end     = (entry.get("endDate") or "Present").strip()
            if role or company:
                lines.append(f"  • *{role}* @ {company}  _{start} – {end}_")
        if len(experience) > 4:
            lines.append(f"  _…and {len(experience) - 4} more_")

    # ── Education ─────────────────────────────────────────────────────────────
    if education:
        lines += ["", "*Education*"]
        for entry in education[:3]:
            degree      = (entry.get("degree") or "").strip()
            institution = (entry.get("institution") or "").strip()
            end         = (entry.get("endDate") or "").strip()
            score       = (entry.get("score") or "").strip()
            score_type  = (entry.get("scoreType") or "").strip()
            score_str   = f" · {score} {score_type}" if score else ""
            lines.append(f"  • {degree} — {institution} ({end}){score_str}")

    # ── Skills ────────────────────────────────────────────────────────────────
    if skills:
        lines += ["", "*Skills*"]
        for group in skills[:5]:
            category   = (group.get("category") or "Skills").strip()
            skill_list = group.get("skills", [])
            if skill_list:
                shown = ", ".join(skill_list[:8])
                extra = f" +{len(skill_list) - 8} more" if len(skill_list) > 8 else ""
                lines.append(f"  *{category}:* {shown}{extra}")

    # ── Projects ──────────────────────────────────────────────────────────────
    if projects:
        lines += ["", f"*Projects* ({len(projects)})"]
        for proj in projects[:3]:
            proj_name = (proj.get("name") or "").strip()
            tags      = proj.get("tags", [])
            tag_str   = f" [{', '.join(tags[:3])}]" if tags else ""
            if proj_name:
                lines.append(f"  • {proj_name}{tag_str}")
        if len(projects) > 3:
            lines.append(f"  _…and {len(projects) - 3} more_")

    # ── Achievements ──────────────────────────────────────────────────────────
    if achievements:
        lines += ["", "*Achievements*"]
        for ach in achievements[:3]:
            title = (ach.get("title") or "").strip()
            year  = (ach.get("year") or "").strip()
            year_str = f" ({year})" if year else ""
            if title:
                lines.append(f"  • {title}{year_str}")
        if len(achievements) > 3:
            lines.append(f"  _…and {len(achievements) - 3} more_")

    # ── Footer ────────────────────────────────────────────────────────────────
    subdomain = (data.get("subdomain") or "").strip()
    lines.append("")
    if subdomain:
        lines.append(f"🌐 Portfolio: https://{subdomain}.resumex.dev")
    lines.append("✏️  Edit: https://resumex.dev/app")
    lines.append("📥 PDF: Open portfolio → Ctrl+P → Save as PDF")

    return "\n".join(lines)


# ── Telegram helpers ──────────────────────────────────────────────────────────

def telegram_send_message(bot_token: str, chat_id: str, text: str) -> bool:
    """
    Send a plain text message to a Telegram chat.
    Automatically falls back from Markdown to plain text if formatting fails.
    Returns True on success.
    """
    url = f"{TELEGRAM_BASE}{bot_token}/sendMessage"

    # Try Markdown first, fall back to plain text
    for parse_mode in ("Markdown", None):
        payload: dict = {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": False,
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode

        try:
            result = _json_request(url, payload)
            if result.get("ok"):
                return True
            err = result.get("description", "Unknown Telegram error")
            if parse_mode and "can't parse" in err.lower():
                print(f"[warn] Markdown parse failed, retrying as plain text: {err}", file=sys.stderr)
                continue
            print(f"[error] Telegram sendMessage: {err}", file=sys.stderr)
            return False
        except RuntimeError as exc:
            print(f"[error] Telegram request failed: {exc}", file=sys.stderr)
            return False

    return False


def telegram_send_pdf_instructions(bot_token: str, chat_id: str, subdomain: str | None) -> bool:
    """Send a follow-up message with PDF download instructions."""
    if subdomain:
        text = (
            "📎 *Get your PDF:*\n"
            f"1. Open your portfolio: https://{subdomain}.resumex.dev\n"
            "2. Press *Ctrl+P* (or ⌘+P on Mac) → *Save as PDF*\n\n"
            "_Your resume always reflects your latest saved data._"
        )
    else:
        text = (
            "📎 *Get your PDF:*\n"
            "1. Open https://resumex.dev/app\n"
            "2. Click the *Download PDF* button in the top bar,\n"
            "   OR press Ctrl+P → Save as PDF\n\n"
            "_Tip: Publish your resume from the dashboard to get a shareable portfolio link._"
        )
    return telegram_send_message(bot_token, chat_id, text)


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Send a Resumex resume summary to Telegram.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "--api-key",
        default=os.environ.get("RESUMEX_API_KEY"),
        help="Resumex API key (env: RESUMEX_API_KEY)",
    )
    p.add_argument(
        "--chat-id",
        default=os.environ.get("TELEGRAM_CHAT_ID"),
        help="Telegram chat ID to send to (env: TELEGRAM_CHAT_ID). "
             "Get yours by messaging @userinfobot on Telegram.",
    )
    p.add_argument(
        "--bot-token",
        default=os.environ.get("TELEGRAM_BOT_TOKEN"),
        help="Telegram bot token (env: TELEGRAM_BOT_TOKEN)",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    # ── Validate required inputs ──────────────────────────────────────────────
    if not args.api_key:
        print(
            "❌ No RESUMEX_API_KEY provided.\n"
            "   Set the environment variable or pass --api-key.",
            file=sys.stderr,
        )
        sys.exit(1)

    # ── Fetch resume ──────────────────────────────────────────────────────────
    print("[resumex] Fetching resume…", file=sys.stderr)
    try:
        workspace   = fetch_workspace(args.api_key)
        resume_data = get_active_resume(workspace)
    except RuntimeError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        sys.exit(1)

    print("[resumex] Resume fetched successfully.", file=sys.stderr)

    # ── Format the message ────────────────────────────────────────────────────
    message   = format_resume_message(resume_data)
    subdomain = (resume_data.get("subdomain") or "").strip() or None

    # Always print to stdout so the agent can read it
    print(message)

    # ── Send via Telegram if credentials are available ────────────────────────
    if not args.bot_token:
        print(
            "\n[info] TELEGRAM_BOT_TOKEN not set — resume printed above.\n"
            "       To send via Telegram, set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID\n"
            "       in your OpenClaw environment variables.",
            file=sys.stderr,
        )
        return

    if not args.chat_id:
        print(
            "\n[info] TELEGRAM_CHAT_ID not set — resume printed above.\n"
            "       To find your chat ID, message @userinfobot on Telegram,\n"
            "       then set TELEGRAM_CHAT_ID in your OpenClaw environment variables.",
            file=sys.stderr,
        )
        return

    # Send summary message
    print(f"[telegram] Sending summary to chat {args.chat_id}…", file=sys.stderr)
    ok = telegram_send_message(args.bot_token, args.chat_id, message)

    if ok:
        print("[telegram] ✅ Summary sent!", file=sys.stderr)
    else:
        print(
            "[telegram] ⚠️  Failed to send summary.\n"
            "           Check your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Send PDF instructions as a follow-up
    telegram_send_pdf_instructions(args.bot_token, args.chat_id, subdomain)
    print("[telegram] ✅ PDF instructions sent.", file=sys.stderr)


if __name__ == "__main__":
    main()
