# Privacy Policy — Resumex OpenClaw Skill v2.0.0

**Last updated:** April 2026  
**Skill author:** Resumex (https://resumex.dev)  
**Source repository:** https://github.com/atharva-badgujar/resume-builder/tree/main/openclaw-skill/resumex  
**License:** MIT-0

---

> This document tells you exactly what data this skill accesses, where it goes, and what never leaves your machine. Read this before installing.

---

## 1. What data this skill accesses

| Data | Source | Used for | Sent to |
|---|---|---|---|
| Your resume (profile, experience, skills, education, projects, achievements) | Resumex API | Job matching, form-filling | Resumex API only (for edits) — otherwise stays in memory |
| `RESUMEX_API_KEY` | Your OpenClaw environment | Authenticating all Resumex API calls | Resumex API (`https://resumex.dev/api/v1/*`) |
| `TELEGRAM_BOT_TOKEN` | Your OpenClaw environment | Sending resume summary messages | Telegram API (`https://api.telegram.org`) — **only when you explicitly ask to send your resume** |
| `TELEGRAM_CHAT_ID` | Your OpenClaw environment | Addressing the Telegram message | Used locally with bot token — not sent separately |
| Job application form data (name, email, phone, location, LinkedIn) | Extracted from your resume | Pre-filling job application forms | The job portal's website — submitted only with your approval |
| Job application results | Local execution of `job_applier.py` | Logging to Resumex Job Tracker | Resumex API (`/api/v1/jobs`) |

---

## 2. What this skill does NOT do

- ❌ Does **not** train any AI model on your resume data
- ❌ Does **not** send your resume to any third-party service other than those listed above
- ❌ Does **not** share your API keys, tokens, or credentials with anyone — they stay in your OpenClaw runtime
- ❌ Does **not** store your data on any server outside Resumex
- ❌ Does **not** log your resume data to disk (no local plaintext files of your personal info)
- ❌ Does **not** call OpenAI, Anthropic, Google, or any other AI API on your behalf
- ❌ Does **not** submit job applications without your explicit approval (unless you opt in via `AUTO_APPLY_MODE=true`)
- ❌ Does **not** use bot-detection evasion techniques — `playwright-stealth` has been intentionally removed from this skill (see §4)
- ❌ Does **not** obfuscate any code — all files (`job_applier.py`, `send_pdf.py`) are plain, readable Python

---

## 3. Outbound network calls — complete list

Every outbound network call this skill makes is listed here. There are no hidden calls.

| Call | When | What is sent | Why |
|---|---|---|---|
| `GET https://resumex.dev/api/v1/agent` | Every time you ask to view/edit resume or search jobs | `RESUMEX_API_KEY` (Authorization header) | Fetch your resume workspace |
| `POST https://resumex.dev/api/v1/agent` | When modifying array fields (experience, projects, etc.) | `RESUMEX_API_KEY` + full modified workspace JSON | Save changes |
| `PATCH https://resumex.dev/api/v1/agent` | When editing profile fields or skills | `RESUMEX_API_KEY` + only changed fields | Partial update |
| `POST https://resumex.dev/api/v1/jobs` | After each job application attempt | `RESUMEX_API_KEY` + job entry (role, company, URL, date, status) | Log to your Job Tracker |
| `POST https://api.telegram.org/bot.../sendMessage` | Only when you say "send my resume on Telegram" | `TELEGRAM_BOT_TOKEN` (in URL) + formatted resume text | Deliver to your Telegram |
| Job portal websites (LinkedIn, Indeed, Greenhouse, etc.) | Only after you explicitly approve each job | Name, email, phone, location, LinkedIn URL (form fields) | Submit your application |

**No other outbound calls exist in this skill.**

---

## 4. Why `playwright-stealth` was removed

The `playwright-stealth` package is designed to make Playwright's automated browser appear to be a regular human-operated browser, bypassing bot-detection heuristics used by websites.

Although this is often used for convenience (to avoid CAPTCHAs), we removed it from this skill because:

1. **Transparency to portals:** Job portals have a right to know if their sites are being accessed by automated tools. Using stealth to bypass this is ethically questionable.
2. **OpenClaw's safety warning:** OpenClaw flagged this package as "intended to evade bot detection — potentially abusive."
3. **Principle of minimum surprise:** This skill should be as transparent as possible about what it does.

**What this means for you:** Some job portals may detect the automated browser and show a CAPTCHA or block the session. In those cases, `job_applier.py` returns `"status": "manual_required"` and the agent gives you a pre-filled link to apply manually. This is the correct, honest behavior.

---

## 5. Credential security

| Credential | How it's used | How to revoke |
|---|---|---|
| `RESUMEX_API_KEY` (`rx_...`) | Bearer token on all Resumex API calls. Scoped to your account only — no one else can use it. | Dashboard → Resumex API → Revoke Key |
| `TELEGRAM_BOT_TOKEN` | Passed to Telegram's sendMessage API. Only used when you explicitly request Telegram delivery. | BotFather → /mybots → Revoke token |
| `TELEGRAM_CHAT_ID` | Your personal Telegram chat ID. Used only as the destination for messages. | N/A — not a secret, just a number |

**Recommendations:**
- Generate a **dedicated Resumex API key** for this skill. If you revoke it, the skill loses access immediately.
- Do not share your API key. Each person should use their own `rx_...` key.
- If you suspect your key was compromised, revoke it immediately at https://resumex.dev/dashboard.

---

## 6. `AUTO_APPLY_MODE` — explicit warning

By default, this skill **always asks for your approval** before submitting any job application.

If you set `AUTO_APPLY_MODE=true` in your OpenClaw environment:
- The agent will apply to **all found jobs without asking you first**
- Applications will be submitted in your name without per-job confirmation
- This setting is **irreversible per session** — once a form is submitted, you cannot undo it

**We strongly recommend keeping `AUTO_APPLY_MODE=false` (the default) until you have manually tested the flow end-to-end.**

---

## 7. Playwright browser installation

When you use auto-apply, the skill installs `playwright` and downloads a Chromium browser (~300MB). This happens locally on your machine:

```bash
pip3 install -r requirements.txt    # installs playwright package
python3 -m playwright install chromium  # downloads Chromium browser binary
```

**We recommend doing this in a Python virtual environment** to isolate the install:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

The browser binary is stored in `~/.cache/ms-playwright/` and used only by this skill.

---

## 8. Source verification

- **Source code:** All skill files are open and readable — no minified, compiled, or obfuscated code
- **Repository:** https://github.com/atharva-badgujar/resume-builder/tree/main/openclaw-skill/resumex
- **Author:** Atharva Badgujar (Resumex)
- **Contact:** https://resumex.dev
- **API documentation:** https://resumex.dev/api-docs

If you are unsure about any file's behavior, review it before installing. The two scripts are:
- [`job_applier.py`](job_applier.py) — Opens a browser, fills form fields from your resume, returns JSON result. 555 lines, fully readable.
- [`send_pdf.py`](send_pdf.py) — Fetches resume from Resumex API, formats it, sends via Telegram. 372 lines, fully readable.

---

## 9. Changes to this policy

If this skill is updated, the PRIVACY.md version date will be updated. Check the version header before re-installing an updated skill.
