# Resumex — OpenClaw Skill v2.0.0

> **Manage your resume AND automatically apply to jobs — all through natural conversation.**

**Author:** Atharva Badgujar • **Homepage:** [resumex.dev](https://resumex.dev) • **Source:** [GitHub](https://github.com/atharva-badgujar/resume-builder/tree/main/openclaw-skill/resumex) • **License:** MIT-0

> 🔒 **Security & Privacy:** Read [PRIVACY.md](PRIVACY.md) for a full account of what data this skill accesses and where it goes. Read [SECURITY.md](SECURITY.md) to see exactly how every OpenClaw review flag was addressed.

This OpenClaw skill connects to your [Resumex](https://resumex.dev) account. The **agent LLM** handles all reasoning, coordination, resume editing, and job searching using its built-in tools. The only helper script is `job_applier.py` — a Playwright browser automation tool for auto-filling job application forms.

---

## How It Works

| Responsibility | Handled by |
|---|---|
| Storing and retrieving resume data | ✅ **Resumex API** |
| Job searching | ✅ **Agent's built-in search tool** |
| AI reasoning (tailoring, cover letters, scoring) | ✅ **Agent LLM** |
| Browser form filling + submission | ✅ **`job_applier.py`** (Playwright, runs locally) |
| Job Tracker logging | ✅ **Resumex `/api/v1/jobs`** |
| Telegram delivery | ✅ **`send_pdf.py`** + your bot token |

---

## ⚡ Quick Start

### 1 — Get your Resumex API Key
1. Sign in at [resumex.dev](https://resumex.dev)
2. **Dashboard → Resumex API → Generate API Key** → copy `rx_...`

### 2 — Set Environment Variables in OpenClaw
```
RESUMEX_API_KEY=rx_your_key_here
TELEGRAM_BOT_TOKEN=...     # optional — Telegram resume delivery
TELEGRAM_CHAT_ID=...       # optional — Telegram resume delivery
AUTO_APPLY_MODE=false      # set true to skip per-job confirmation
HEADLESS_BROWSER=true      # set false to watch the browser while applying
```

### 3 — Install Playwright (for auto-apply)

The agent will run this automatically on first use:
```bash
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

If pip3/playwright are unavailable, the agent gracefully falls back to providing pre-filled copy-paste data for each job.

### 4 — Start chatting 🎉

- *"Find me jobs"*
- *"Search for backend engineer jobs in Bangalore"*
- *"Show my resume"*
- *"Add Python and Docker to my skills"*
- *"Tailor my resume for: [paste JD]"*

## 🛡️ OpenClaw Security Review — Flags Addressed

OpenClaw's automated review flagged several items before install. Here is how each one is resolved:

| Flag | Resolution |
|---|---|
| Unknown author/homepage | Author: **Atharva Badgujar**, Homepage: **resumex.dev**, Source: **GitHub** (all in frontmatter) |
| Review code locally | Both scripts are plain, readable Python. `job_applier.py` = 555 lines. `send_pdf.py` = 372 lines. No obfuscation, no `eval`, no `exec`. See [SECURITY.md](SECURITY.md#-review-code-locally) for a line-by-line summary. |
| Limit automation | `AUTO_APPLY_MODE` defaults to `false`. The agent always asks which jobs to apply to before submitting. See warning below. |
| Minimize credential scope | `RESUMEX_API_KEY` can be revoked anytime at **Dashboard → Resumex API → Revoke**. Create a dedicated key for this skill. |
| Sandbox installs | `requirements.txt` now includes virtualenv instructions in comments. See install guide below. |
| playwright-stealth removed | **Removed entirely** from `requirements.txt` and `job_applier.py`. Browser runs transparently. |
| Telegram token transparency | `TELEGRAM_BOT_TOKEN` is used **only** when you explicitly request Telegram delivery. See [PRIVACY.md §3](PRIVACY.md#3-outbound-network-calls--complete-list). |

---

## 🤖 Auto Job Application Flow

```
"Find me jobs"
    │
    ▼
[1] ONBOARDING   — Agent asks 9 questions (role, location, experience, portals...)
                   Preferences saved for this session, not asked again
    │
    ▼
[2] FETCH RESUME — GET /api/v1/agent → profile, skills, experience
    │
    ▼
[3] SEARCH JOBS  — Agent uses built-in search across LinkedIn, Indeed,
                   Greenhouse, Lever, Glassdoor, Naukri
                   LLM scores each result by match against resume + prefs
    │
    ▼
[4] APPROVAL     — Numbered ranked list shown; user types "1,3,5" or "all"
    │
    ▼
[5] AUTO-APPLY   — Agent calls job_applier.py for each job:
                   ✅ Standard forms  → filled + submitted automatically
                   📎 PDF / Workday   → pre-filled data + link given to user
                   ❌ Failed          → error info + direct link provided
    │
    ▼
[6] JOB TRACKER  — POST /api/v1/jobs for every application
                   View at resumex.dev/app → Job Tracker tab
```

---

## 📋 Supported Job Portals

| Portal | Auto-Submit | When Manual |
|---|---|---|
| LinkedIn Easy Apply | ✅ | External apply or PDF required |
| Indeed Smart Apply | ✅ | External redirect |
| Greenhouse | ✅ (no PDF) | PDF upload required |
| Lever | ✅ (no PDF) | PDF upload required |
| Workday | 📎 Always manual | Complex wizard + MFA |
| Glassdoor | 🔄 Generic filler | Usually redirects to company ATS |
| Naukri | 🔄 Generic filler | PDF or login wall |
| Generic/Other | 🔄 Heuristic | Undetectable fields |

---

## ⚠️ AUTO_APPLY_MODE Warning

`AUTO_APPLY_MODE` is **disabled by default**. When disabled, the agent always:
1. Shows you the ranked job list
2. Waits for you to type which job numbers to apply to (e.g. `"1,3,5"`)
3. Applies only to those jobs

If you set `AUTO_APPLY_MODE=true`:
- **Applications are submitted without per-job confirmation**
- They cannot be undone once submitted
- We **strongly recommend** keeping this `false` until you have manually tested the full flow at least once

---

## 📦 Install Guide (virtualenv — recommended)

```bash
# 1. Create an isolated Python environment
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

# 2. Install dependencies (playwright + requests — no stealth)
pip3 install -r requirements.txt

# 3. Download Chromium browser binary (~300 MB)
#    Stored in ~/.cache/ms-playwright/ — does not affect system Python
python3 -m playwright install chromium
```

> ℹ️ **`playwright-stealth` is NOT installed.** The browser runs transparently and is detectable by job portals. If a portal blocks it, `job_applier.py` returns `manual_required` and the agent gives you a direct apply link with your data pre-filled.

**Prefer not to install a browser?** Skip this step entirely. The agent will provide pre-filled copy-paste data and a direct link for each job — you apply manually.

---

## ✏️ Resume Management

| Say... | Effect |
|---|---|
| *"Show my resume"* | Full formatted resume summary |
| *"Update my phone to +91..."* | Edit any profile field |
| *"Add a job at [Company] as [Role]..."* | Add new experience entry |
| *"Update my role at [Company]"* | Edit existing experience |
| *"Remove my job at [Company]"* | Delete entry (confirm first) |
| *"Add Python, Docker to my skills"* | Add to default Skills group |
| *"Add React under Frameworks"* | Add to named skill category |
| *"Add B.Tech CS at SPPU 2019–2023"* | Add education entry |
| *"Add a project: [name] — [desc]"* | Add project entry |
| *"Tailor my resume for: [JD]"* | AI rewrites summary + bullets for JD |
| *"Send me my resume on Telegram"* | Formatted summary + PDF link to Telegram |

---

## 🔧 Environment Variables — Complete Reference

| Variable | Required | Default | Sent to | Description |
|---|---|---|---|---|
| `RESUMEX_API_KEY` | ✅ **Yes** | none | `resumex.dev` only | Auth for all Resumex API calls. Create a dedicated key; revoke at Dashboard → Resumex API. |
| `TELEGRAM_BOT_TOKEN` | No | none | `api.telegram.org` only | Used **only** when you say "send my resume on Telegram". Never logged or forwarded. |
| `TELEGRAM_CHAT_ID` | No | none | Nowhere (local only) | Your Telegram destination ID. Not transmitted separately. |
| `AUTO_APPLY_MODE` | No | `false` | Nowhere (local flag) | `true` = skip per-job approval. **Use with caution — see warning above.** |
| `HEADLESS_BROWSER` | No | `true` | Nowhere (local flag) | `false` = show browser window while applying. |

No other environment variables are read by this skill.

---

## 📁 Files

| File | Purpose | Lines | Network calls |
|---|---|---|---|
| `SKILL.md` | **Agent instructions** — the LLM reads this to know what to do | ~560 | none |
| `job_applier.py` | **Playwright helper** — fills job application forms (called by agent) | 555 | Job portal URL only |
| `send_pdf.py` | **Telegram helper** — sends resume to Telegram (called by agent) | 372 | `resumex.dev` + `api.telegram.org` |
| `requirements.txt` | Python deps (`playwright`, `requests` — no stealth) | 15 | none |
| `PRIVACY.md` | Full data flow + outbound call declaration | — | none |
| `SECURITY.md` | OpenClaw review flags + how each was resolved | — | none |
| `README.md` | This file | — | none |

---

## 🌐 API Reference

```
Resume:      GET/POST/PATCH https://resumex.dev/api/v1/agent
Job Tracker: GET/POST/PATCH/DELETE https://resumex.dev/api/v1/jobs
```

Full docs: [resumex.dev/api-docs](https://resumex.dev/api-docs)

---

## 🔒 Security & Privacy

- **All skill files are plain, readable code** — no obfuscation, no compiled binaries, no `eval`/`exec`
- **Resume data stays local** — `job_applier.py` runs on your machine, fills forms directly, no proxy
- **`RESUMEX_API_KEY`** is scoped to your account only, revocable at anytime
- **Telegram tokens** never leave your OpenClaw environment except to `api.telegram.org` when triggered
- **`playwright-stealth` has been removed** — browser automation is transparent and detectable
- **The agent LLM** never calls any third-party AI on your behalf
- **Revoke access anytime:** Dashboard → Resumex API → Revoke

📄 [Full Privacy Policy (PRIVACY.md)](PRIVACY.md)  
🛡️ [Security Guide (SECURITY.md)](SECURITY.md)

---

## License

MIT-0 — free to use, modify, and redistribute.
