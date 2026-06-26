# Security Guide — Resumex OpenClaw Skill v2.0.0

> OpenClaw's automated review flagged several items before install. This document addresses every one of them directly.

---

## OpenClaw's Flagged Items — Addressed

### ✅ Source verification

**Flag:** *"the skill owner and homepage are unknown — prefer skills with a known repository or author."*

**Response:**
- **Author:** Atharva Badgujar
- **Organization:** Resumex (https://resumex.dev)
- **Source repository:** https://github.com/atharva-badgujar/resume-builder/tree/main/openclaw-skill/resumex
- **API documentation:** https://resumex.dev/api-docs
- **Contact:** Via https://resumex.dev

The frontmatter of `SKILL.md` now includes `homepage` and `repository` fields. All files are plain, readable Python and Markdown — no compiled or obfuscated code.

---

### ✅ Review code locally

**Flag:** *"inspect job_applier.py and send_pdf.py yourself to ensure behavior matches expectations."*

**What each file does:**

#### `job_applier.py` (555 lines)
- Accepts resume data as **CLI arguments** (`--name`, `--email`, `--phone`, `--location`, `--linkedin`, `--website`, `--summary`, `--url`)
- Opens the job URL in a Playwright browser
- Tries to fill standard form fields (name, email, phone, location, LinkedIn, cover letter)
- If a PDF upload is required: returns `"manual_required"` — does NOT submit
- If form is fillable: submits, returns `"applied"`
- Returns a JSON object on stdout: `{"status": "...", "notes": "...", "filled_url": "..."}`
- **Makes NO network calls other than loading the target job URL**
- **Does NOT read any files from disk** (all data is passed as CLI args)
- **Does NOT log anywhere** (output goes only to the calling agent via stdout)

#### `send_pdf.py` (372 lines)
- Makes ONE call: `GET https://resumex.dev/api/v1/agent` to fetch your resume
- Formats a plain-text resume summary
- If Telegram credentials are provided: makes one call to `https://api.telegram.org/bot.../sendMessage`
- If Telegram credentials are absent: prints the formatted resume to stdout only
- **No other network calls**

Both files: fully readable, no obfuscation, no dynamic code execution (`eval`, `exec`), no file writes, no subprocess spawning.

---

### ✅ Limit automation / AUTO_APPLY_MODE

**Flag:** *"do not set AUTO_APPLY_MODE=true until you have tested the flow manually."*

**Default behavior:** `AUTO_APPLY_MODE` defaults to `false`. The agent always shows you the job list and waits for you to type which ones to apply to (e.g. `"1,3,5"`).

**How to test safely:**
1. Set `AUTO_APPLY_MODE=false` (default)
2. Run `"search for [role] jobs in [location]"` — just shows you the list, no applying
3. Use `"apply to 1"` for a single job first — watch what happens
4. Only after you are satisfied, enable `AUTO_APPLY_MODE=true` if desired

**Risk if AUTO_APPLY_MODE=true:** Applications will be submitted in your name without per-job confirmation. Once submitted, they cannot be undone. **We do not recommend this setting.**

---

### ✅ Minimize credential scope

**Flag:** *"create and use a Resumex API key that can be revoked and has minimum permissions possible."*

**How Resumex API keys work:**
- Each key is scoped to **your account only** — no cross-account access possible
- Keys are **revocable at any time**: Dashboard → Resumex API → Revoke Key
- When revoked, the key stops working immediately for all callers
- Each key is independent — create a dedicated one for this skill

**Recommendation:** Generate a dedicated `rx_...` key for this OpenClaw skill. If you ever suspect it was leaked, revoke it without affecting your web app session.

---

### ✅ Sandbox installs

**Flag:** *"run pip install and playwright's browser installer in a controlled environment (virtualenv or sandboxed VM)."*

**Recommended install:**
```bash
# Create an isolated environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt    # playwright + requests only (no stealth)

# Install Chromium browser binary (~300MB, stored in ~/.cache/ms-playwright/)
python3 -m playwright install chromium
```

**Alternative — skip Playwright entirely:**
If you prefer not to install a browser binary, you can skip auto-apply. The agent will gracefully fall back:
> When `job_applier.py` is unavailable, the agent provides pre-filled copy-paste data for each job, and a direct link to apply manually.

---

### ✅ playwright-stealth removed

**Flag:** *"playwright-stealth is intended to evade bot detection — acceptable for convenience but potentially abusive; consider removing it."*

**Action taken:** `playwright-stealth` has been **completely removed** from this skill:
- Removed from `requirements.txt`
- Removed all imports and `stealth_sync()` calls from `job_applier.py`

**What this means:** The browser automation runs transparently. Job portals can detect it as an automated browser if they have bot-detection in place. In those cases, the browser session may show a CAPTCHA or fail, and `job_applier.py` will return `"manual_required"` — the agent will then give you a direct link and pre-filled data to apply manually. This is the honest, transparent behavior.

---

### ✅ Telegram token transparency

**Flag:** *"if you provide TELEGRAM_BOT_TOKEN, know it will be used to call api.telegram.org."*

**Explicit statement:**
- `TELEGRAM_BOT_TOKEN` is **only used when you explicitly say "send my resume on Telegram"** (triggers `send_pdf.py`)
- It is passed directly to `https://api.telegram.org/bot<TOKEN>/sendMessage`
- It is **never logged to disk**, **never sent to Resumex**, **never used for any other purpose**
- If you do not set this variable, Telegram delivery is disabled — the skill works fully without it
- You can revoke the token at any time via BotFather → `/mybots` → Revoke

---

## All Environment Variables — Complete Reference

| Variable | Required | Default | What it does | Who receives it |
|---|---|---|---|---|
| `RESUMEX_API_KEY` | **Yes** | none | Auth for all Resumex API calls | `resumex.dev` only |
| `TELEGRAM_BOT_TOKEN` | No | none | Sends resume summary to Telegram | `api.telegram.org` only, only when triggered |
| `TELEGRAM_CHAT_ID` | No | none | Your Telegram destination ID | Used locally only, not transmitted separately |
| `AUTO_APPLY_MODE` | No | `false` | Skip per-job confirmation prompt | Not transmitted — local flag only |
| `HEADLESS_BROWSER` | No | `true` | Show/hide browser window | Not transmitted — local flag only |

No other environment variables are read by this skill.

---

## What This Skill Can and Cannot Do

| Capability | Can | Cannot |
|---|---|---|
| Read your Resumex resume | ✅ Yes, via `/api/v1/agent` with your key | ❌ Cannot access other users' resumes |
| Edit your Resumex resume | ✅ Yes, with your explicit instruction | ❌ Cannot delete your account or keys |
| Search for jobs | ✅ Yes, using agent's built-in search | ❌ Cannot access portals that require login |
| Fill job application forms | ✅ Yes, from data in your resume | ❌ Cannot bypass 2FA or CAPTCHAs |
| Submit applications | ✅ Yes, only with your approval | ❌ Cannot submit without your selection (unless AUTO_APPLY_MODE=true) |
| Send Telegram messages | ✅ Yes, only when you request it | ❌ Cannot read your Telegram messages |
| Log to Job Tracker | ✅ Yes, to your own Resumex account | ❌ Cannot log to another user's account |
| Access local files | ❌ No | — |
| Spawn background processes | ❌ No | — |
| Install system software | ❌ No (pip packages only, in your env) | — |
| Read other env variables | ❌ No (only the 5 listed above) | — |

---

## Reporting Issues

If you find behavior that does not match this security guide, please open an issue at:  
https://github.com/atharva-badgujar/resume-builder/issues

Or contact us at: https://resumex.dev
