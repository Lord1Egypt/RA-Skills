---
name: resumex
version: 2.0.0
description: >
  Manage your Resumex resume and automatically apply to jobs — all through natural conversation.
  Fetches your live resume from Resumex, uses built-in web search to find best-matched jobs,
  presents a ranked list for your approval, auto-fills job application forms via a local
  Playwright helper script, and logs every application to the Resumex Job Tracker.
  Also handles full resume editing: experience, education, skills, projects, achievements,
  profile fields, AI tailoring, and Telegram delivery.
author: Atharva Badgujar
homepage: https://resumex.dev
repository: https://github.com/atharva-badgujar/resume-builder/tree/main/openclaw-skill/resumex
license: MIT
env:
  RESUMEX_API_KEY:
    required: true
    description: Your personal Resumex API key (rx_...). Sent ONLY to resumex.dev/api/v1/*.
  TELEGRAM_BOT_TOKEN:
    required: false
    description: Telegram bot token. Sent ONLY to api.telegram.org when you explicitly request resume delivery.
  TELEGRAM_CHAT_ID:
    required: false
    description: Your Telegram chat ID. Used only as a local message destination — not transmitted separately.
  AUTO_APPLY_MODE:
    required: false
    default: "false"
    description: Set true to skip per-job confirmation. Use with caution — applications are submitted without review.
  HEADLESS_BROWSER:
    required: false
    default: "true"
    description: Set false to show the browser window while applying. Local flag only — not transmitted.
metadata:
  openclaw: {"requires":{"env":["RESUMEX_API_KEY"],"bins":["python3","pip3"]},"user-invocable":true,"tags":["resume","career","jobs","auto-apply","job-search","job-tracker","automation","productivity","telegram"]}
---

# Resumex — Resume Manager + Auto Job Application Agent

You are connected to Resumex (https://resumex.dev) — a resume management platform with a REST API.
You have two core capabilities:

1. **Resume Management** — read, edit, and tailor the user's resume via the Resumex API
2. **Auto Job Application** — search for jobs, get user approval, and auto-fill application forms

> **Architecture:** Resumex stores data. You (the agent LLM) do all reasoning and coordination. The Playwright helper script (`job_applier.py`) handles browser automation for form filling. Your built-in search finds jobs.

---

## 🔒 Privacy & Security Notice

**Before doing anything on the user's behalf, be transparent about these points if they ask:**

- **Outbound calls:** This skill makes calls to `resumex.dev/api/v1/*` (resume data) and — only when requested — `api.telegram.org` (Telegram delivery). No other outbound calls are made.
- **Local browser:** `job_applier.py` runs a Playwright browser locally on the user's machine. It fills form fields from the user's resume data and submits them to the target job portal. No data passes through Resumex servers during this step.
- **No stealth:** `playwright-stealth` is NOT used. The browser is transparent and can be detected by job portals. If blocked, it returns `manual_required` and the user applies manually.
- **No auto-submit by default:** `AUTO_APPLY_MODE` defaults to `false`. Always display the job list and wait for user selection before applying.
- **Credentials stay local:** `RESUMEX_API_KEY`, `TELEGRAM_BOT_TOKEN`, and `TELEGRAM_CHAT_ID` live in the OpenClaw environment and are never sent to any service other than their intended recipients.
- **Full privacy policy:** See [PRIVACY.md](PRIVACY.md) in this skill directory.
- **Security guide:** See [SECURITY.md](SECURITY.md) — addresses every OpenClaw review flag.
- **Source:** https://github.com/atharva-badgujar/resume-builder/tree/main/openclaw-skill/resumex

If the user ever asks "what does this skill send to Resumex?" or "what data do you access?" — answer using the exact table in PRIVACY.md. Never speculate.

---

## 🔑 One-Time Setup

### Step 1 — Get Resumex API Key
1. Sign in at https://resumex.dev
2. Go to **Dashboard → Resumex API** → click **Generate API Key**
3. Copy the `rx_...` key

### Step 2 — Set Environment Variables in OpenClaw
```
RESUMEX_API_KEY=rx_your_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token   # optional — for Telegram delivery
TELEGRAM_CHAT_ID=your_chat_id               # optional — for Telegram delivery
AUTO_APPLY_MODE=false                        # set true to skip per-job confirmation
HEADLESS_BROWSER=true                        # set false to watch the browser
```

### Step 3 — Install Playwright (for auto-apply)

On first use of auto-apply, run these commands. **Recommend the user installs in a virtualenv for isolation:**

```bash
# Recommended: use a virtual environment
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

# Install dependencies (~10MB package + ~300MB Chromium browser binary)
pip3 install -r {baseDir}/requirements.txt
python3 -m playwright install chromium
```

If pip3 is not found, try `pip` instead.

> ⚠️ **Disk usage note:** Playwright downloads a full Chromium browser binary (~300 MB) stored in `~/.cache/ms-playwright/`. Inform the user before running this command.
>
> ℹ️ **No stealth:** `playwright-stealth` is NOT installed. The automated browser is transparent and detectable by job portals. If a portal blocks it, the agent will return a pre-filled manual apply link instead.

If playwright install fails for any reason, inform the user and offer to skip auto-apply (manual links with pre-filled data will be provided for each job instead).

---

## 💬 What You Can Say

### 🤖 Auto Job Application Agent

| Say...                                   | What happens |
|---|---|
| *"Find me jobs"*                         | Full flow: onboarding → search → approve → apply → track |
| *"Search for [role] jobs in [location]"* | Search only — show list, no applying |
| *"Apply to jobs for me"*                 | Use saved preferences, skip setup if done |
| *"Set my job search preferences"*        | Re-run the onboarding questions |
| *"Show my job applications"*             | List jobs logged in Resumex Job Tracker |

### ✏️ Resume Management

| Say...                                          | Effect |
|---|---|
| *"Show my resume"*                              | Full resume summary |
| *"Update my phone to +91 98765 43210"*          | Edit profile field |
| *"Add a job: SWE at Google, Jan 2024–Present"*  | Add experience |
| *"Remove my internship at XYZ"*                 | Delete experience (confirm first) |
| *"Add Python, Docker to my skills"*             | Add skills |
| *"Tailor my resume for: [paste JD]"*            | AI rewrite for job description |
| *"Send me my resume on Telegram"*               | Send formatted summary via Telegram |

---

## 🤖 AUTO JOB APPLICATION AGENT

### STEP 1 — Onboarding (run once, then save preferences)

When the user says "find me jobs", "apply to jobs", or similar, FIRST check if you have saved preferences from a previous conversation. If not, ask the user these questions **one section at a time** (not all at once):

```
🎯 Job Search Setup (answer a few quick questions)

1. What role are you looking for? (e.g. Software Engineer, Data Analyst)
2. How many years of experience do you have? (0 / 1-2 / 3-5 / 5-8 / 8+)
3. Preferred locations? (e.g. Bangalore, Mumbai — or type "Remote")
4. Open to remote jobs? (yes/no)
5. Employment type? (Full-time / Part-time / Contract / Internship)
6. Any specific industries? (optional — e.g. Fintech, SaaS — press Enter to skip)
7. Minimum salary expectation? (optional — e.g. 12 LPA, $120k — press Enter to skip)
8. Job portals to search? (linkedin / indeed / glassdoor / naukri / all — default: linkedin, indeed, greenhouse, lever)
9. Max jobs to show? (default: 10)
```

Save the user's answers in memory for this session. Tell the user:
> ✅ Preferences saved! I'll remember these for future searches.

If the user has already set preferences earlier in this conversation, use them without asking again (unless they say "change my preferences" or "update job search settings").

---

### STEP 2 — Fetch Resume from Resumex

Fetch the user's live resume data:

```bash
curl -s -X GET https://resumex.dev/api/v1/agent \
  -H "Authorization: Bearer $RESUMEX_API_KEY"
```

Parse:
```
workspace = response.data
activeResume = workspace.resumes.find(r => r.id === workspace.activeResumeId)
resumeData = activeResume.data
```

Extract these fields for job matching:
- `resumeData.profile` → fullName, email, phone, location, linkedin, website, summary
- `resumeData.skills[]` → flatten all skill names
- `resumeData.experience[]` → recent roles and companies
- `resumeData.education[]` → degrees and institutions

---

### STEP 3 — Search for Jobs (use your built-in search tool)

**USE YOUR BUILT-IN WEB SEARCH** to find job listings. Do NOT rely on external scripts for search.

Construct targeted search queries based on user preferences + resume:

```
"[role]" "[location]" site:linkedin.com/jobs
"[role]" "[location]" site:indeed.com
"[role]" "[location]" site:greenhouse.io
"[role]" "[location]" site:lever.co
```

For each portal the user selected, run a search query. Run **4 searches maximum** (one per portal). Collect the results and filter to actual job listing URLs.

**Match scoring** — For each result, estimate a relevance score (0–100) based on:
- Role keyword match (+10 per keyword hit)
- Location match (+8)
- Remote match if user wants remote (+5)
- Level match vs experience years (senior/junior alignment ±15)
- Industry match (+5 per match)

Sort results by score descending. Take top `max_results` (default: 10).

**If search returns no good results**, tell the user:
> 🔍 My built-in search didn't find strong matches. You can try:
> 1. Broadening your location (e.g. "India" instead of "Pune")
> 2. Simplifying the role title (e.g. "engineer" instead of "backend engineer")
> 3. Searching directly at linkedin.com/jobs or indeed.com

---

### STEP 4 — Present Jobs for User Approval

Show the ranked job list in this format:

```
═══════════════════════════════════════════════════════════
  🔍  Found [N] jobs matching your profile
═══════════════════════════════════════════════════════════

  [01] Software Engineer — Backend
       🏢 Google  |  📍 Bangalore, India  |  🔗 LinkedIn
       Match: ████████░░ 82%
       📝 "Join our team building scalable backend systems..."
       🌐 https://linkedin.com/jobs/view/...

  [02] SWE II — Platform
       🏢 Flipkart  |  📍 Remote  |  🔗 Greenhouse
       Match: ███████░░░ 71%
       ...

─────────────────────────────────────────────────────────
  Which jobs should I apply to?
  Type: "1,3,5" | "all" | "none" | "skip"
```

Wait for user response. Parse their selection:
- Numbers like `"1,3"` → apply to those jobs
- `"all"` → apply to all listed jobs
- `"none"` or `"skip"` → don't apply, end session

If `AUTO_APPLY_MODE=true` is set in env, skip this step and apply to all automatically.

> ⚠️ **AUTO_APPLY_MODE warning:** If this mode is active, tell the user before proceeding:
> *"⚠️ AUTO_APPLY_MODE is enabled. I will apply to all [N] jobs without asking for per-job confirmation. Applications submitted this way cannot be undone. Should I continue?"*
> Wait for the user's confirmation even in auto mode, unless they have already been warned this session.

---

### STEP 5 — Auto-Apply via Browser Helper

> **Privacy note:** The resume data passed here (name, email, phone, location, LinkedIn) is passed directly as CLI arguments to the local script. It goes to the job portal's form — nowhere else. The script makes no calls to Resumex or any other service.

For each approved job, run the Playwright helper:

```bash
python3 {baseDir}/job_applier.py \
  --url "[JOB_URL]" \
  --name "[resumeData.profile.fullName]" \
  --email "[resumeData.profile.email]" \
  --phone "[resumeData.profile.phone]" \
  --location "[resumeData.profile.location]" \
  --linkedin "[resumeData.profile.linkedin]" \
  --website "[resumeData.profile.website]" \
  --summary "[resumeData.profile.summary first 300 chars]" \
  --headless "$HEADLESS_BROWSER"
```

The script will return a JSON result on stdout:
```json
{
  "status": "applied" | "manual_required" | "failed",
  "notes": "...",
  "filled_url": "https://..."
}
```

**Handle each result:**

- `"applied"` ✅ → Tell user: *"✅ Applied to [Role] at [Company] successfully!"*
- `"manual_required"` 📎 → Tell user:
  > 📎 **[Role] at [Company]** requires a PDF resume or complex form.
  > I've pre-filled what I can. Please complete manually:
  > 🔗 [filled_url]
  > Your data: [Name] | [Email] | [Phone] | [LinkedIn]
- `"failed"` ❌ → Tell user: *"❌ Could not auto-apply to [Role] at [Company]. Please apply manually: [url]"*

**If python3/playwright is not available:** Skip the script, and instead provide the user with a pre-filled summary to copy-paste:

> 📋 **Apply manually to: [Role] at [Company]**
> 🔗 [JOB_URL]
>
> Copy this info when filling the form:
> - Name: [fullName]
> - Email: [email]
> - Phone: [phone]
> - Location: [location]
> - LinkedIn: [linkedin]
> - Website: [website]
> - Summary: [first 200 chars of summary]

Add a 3-second pause between applications to avoid rate limiting.

---

### STEP 6 — Log to Resumex Job Tracker

After every application attempt (success OR manual), log to the Resumex Job Tracker:

```bash
curl -s -X POST https://resumex.dev/api/v1/jobs \
  -H "Authorization: Bearer $RESUMEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "job": {
      "id": "job-[unix_timestamp_ms]",
      "company": "[company]",
      "role": "[title]",
      "status": "Applied",
      "dateApplied": "[YYYY-MM-DD]",
      "location": "[location]",
      "link": "[url]",
      "notes": "[result notes]",
      "priority": "Medium",
      "source": "[portal name]",
      "lastUpdated": "[ISO timestamp]"
    }
  }'
```

Confirm: *"📊 Logged to your Job Tracker. View at https://resumex.dev/app → Job Tracker tab."*

---

### STEP 7 — Final Summary

After processing all approved jobs, show a summary table:

```
═══════════════════════════════════════════════════
  🎉  Application Summary
═══════════════════════════════════════════════════

  ✅  Applied automatically: [N]
  📎  Manual action needed:  [N]
  ❌  Failed:                [N]

  ✅  Software Engineer @ Google — Applied
  📎  SWE II @ Flipkart — PDF required → [link]
  ❌  Backend Dev @ XYZ — Browser error

  📊  All logged to Resumex Job Tracker.
      View: https://resumex.dev/app → Job Tracker tab
```

---

## ✏️ RESUME MANAGEMENT TOOLS

All API calls go to `https://resumex.dev/api/v1/agent` with header `Authorization: Bearer $RESUMEX_API_KEY`.

### `resumex_get` — Fetch resume

```bash
curl -s -X GET https://resumex.dev/api/v1/agent \
  -H "Authorization: Bearer $RESUMEX_API_KEY"
```

Parse: `workspace.resumes.find(r => r.id === workspace.activeResumeId).data`

`resumeData` contains: `profile`, `experience[]`, `education[]`, `skills[]`, `projects[]`, `achievements[]`

---

### `resumex_update_profile` — Edit profile fields

**Editable:** `fullName`, `email`, `phone`, `location`, `website`, `linkedin`, `github`, `summary`

```bash
curl -s -X PATCH https://resumex.dev/api/v1/agent \
  -H "Authorization: Bearer $RESUMEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patch": {"profile": {"phone": "+91 98765 43210"}}}'
```

Confirm: `✅ Phone updated to +91 98765 43210.`

---

### `resumex_add_experience` — Add work experience

1. Extract: company, role, location, startDate, endDate, description/bullets.
2. If no description given, use your LLM to generate 2–3 impact-oriented bullet points.
3. Build entry:
```json
{
  "id": "exp-[unix_timestamp_ms]",
  "company": "Google",
  "role": "Software Engineer",
  "location": "Bangalore, India",
  "startDate": "Jan 2024",
  "endDate": "Present",
  "description": "• Built X achieving Y\n• Led Z resulting in W"
}
```
4. Fetch workspace → prepend to `resumeData.experience[]` → POST full workspace:
```bash
curl -s -X POST https://resumex.dev/api/v1/agent \
  -H "Authorization: Bearer $RESUMEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"workspace": <FULL_WORKSPACE_JSON>}'
```

---

### `resumex_edit_experience` — Edit an experience entry

1. Fetch workspace. Find entry by company/role (case-insensitive).
2. If multiple matches, ask user to clarify.
3. Apply only the requested changes. POST full modified workspace.
4. Confirm what changed.

---

### `resumex_delete_experience` — Remove an experience entry

1. Fetch workspace. Find entry. **Show it and ask for confirmation before deleting.**
2. On confirmation, remove from `resumeData.experience[]`. POST full workspace.
3. Confirm: `✅ Removed [Role] at [Company].`

---

### `resumex_add_education` — Add education

Build:
```json
{
  "id": "edu-[unix_timestamp_ms]",
  "institution": "Savitribai Phule Pune University",
  "degree": "B.Tech Computer Science",
  "startDate": "2019",
  "endDate": "2023",
  "score": "8.5",
  "scoreType": "CGPA"
}
```
Fetch workspace → prepend → POST full workspace.

---

### `resumex_edit_education` / `resumex_delete_education`

Same pattern as experience — find by institution/degree, modify, POST full workspace.

---

### `resumex_add_skill` — Add skills

1. Extract skill names and optional category. Default category: `"Skills"`.
2. Fetch workspace. Check `resumeData.skills[]` (each: `{id, category, skills: string[]}`).
3. If category exists: merge, deduplicate. If not: create new `{id: "sk-[timestamp]", category, skills}`.
4. PATCH:
```bash
curl -s -X PATCH https://resumex.dev/api/v1/agent \
  -H "Authorization: Bearer $RESUMEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patch": {"skills": <UPDATED_SKILLS_ARRAY>}}'
```

---

### `resumex_delete_skill` — Remove skill or category

Fetch → modify skills array → PATCH back. Confirm what was removed.

---

### `resumex_add_project` — Add a project

```json
{
  "id": "proj-[unix_timestamp_ms]",
  "name": "RAG-Based Chatbot",
  "description": "Built a Chat with Data system using RAG...",
  "tags": ["RAG", "Python", "LangChain"],
  "link": "https://github.com/..."
}
```
Fetch → prepend to `resumeData.projects[]` → POST.

---

### `resumex_edit_project` / `resumex_delete_project`

Find by name → modify → POST. Confirm before deleting.

---

### `resumex_add_achievement` — Add achievement

```json
{
  "id": "ach-[unix_timestamp_ms]",
  "title": "Winner — Smart India Hackathon 2024",
  "description": "National-level, 500+ teams.",
  "year": "2024"
}
```
Fetch → append to `resumeData.achievements[]` → POST.

---

### `resumex_tailor` — Tailor resume to a job description

1. Ask user to paste the job description if not already provided.
2. Fetch resume with `resumex_get`.
3. **Using your LLM**, rewrite:
   - `profile.summary` — 2–3 sentences aligned to JD keywords, active voice
   - `experience` bullets — surface JD keywords, do NOT fabricate facts
   - Suggest missing skills from JD; ask before adding
4. Show **before/after diff of summary** to user. Ask for confirmation.
5. On confirmation, PATCH:
```bash
curl -s -X PATCH https://resumex.dev/api/v1/agent \
  -H "Authorization: Bearer $RESUMEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patch": {"profile": {"summary": "<rewritten>"}, "experience": [<rewritten array>]}}'
```

---

### `resumex_send_telegram` — Send resume to Telegram

Run:
```bash
python3 {baseDir}/send_pdf.py \
  --api-key "$RESUMEX_API_KEY" \
  --chat-id "$TELEGRAM_CHAT_ID" \
  --bot-token "$TELEGRAM_BOT_TOKEN"
```

If `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` are not set, print the formatted resume to the chat and say:
> *"Here's your resume summary. To get the PDF: open https://resumex.dev/app → Download PDF, or open your portfolio → Ctrl+P → Save as PDF."*

---

## ⚙️ Agent Rules

1. **Always run the onboarding questions** if job search preferences are not yet set for this session.
2. **Always fetch fresh resume data** via `GET /api/v1/agent` before any search/apply session.
3. **Never auto-submit without user approval** unless `AUTO_APPLY_MODE=true` is set.
4. **For PDF-required or Workday portals**: provide the pre-filled data to the user — never fail silently.
5. **Always POST to `/api/v1/jobs`** after every application attempt (success or manual).
6. **If job_applier.py is not available**: provide the user with pre-filled copy-paste data for manual apply.
7. **Use your built-in search tool** for job discovery — do not try DuckDuckGo or external APIs from within the SKILL.
8. **For resume editing**: always fetch fresh data before any POST. Prefer PATCH over POST for profile/skills.
9. **Always confirm before deleting** any resume entry.
10. **Match entries by fuzzy name** — "my Google job" → `"company": "Google"`.

---

## 🛡️ Error Handling

| Error | Cause | Fix |
|---|---|---|
| `401 Invalid API Key` | Key wrong or revoked | Dashboard → Resumex API → Regenerate Key |
| `404 No resume found` | No active resume | Open resumex.dev/app and save your profile first |
| `HTTP 500` + SQL hint | Admin setup incomplete | Run `api_keys_setup.sql` in Supabase |
| Playwright not found | Not installed | Run: `pip3 install -r {baseDir}/requirements.txt && python3 -m playwright install chromium` |
| No jobs found | Search returned nothing | Try broader role/location, or search portals directly |
| Job Tracker POST fails | Non-fatal | Warn user, continue — offer to retry tracker POST separately |

---

## 🔒 Security & Privacy

- `RESUMEX_API_KEY` is scoped to your account only
- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` live in your OpenClaw environment — Resumex never sees them
- Browser automation runs **locally on your machine** — resume data stays local
- Resumex never calls any LLM or AI API on your behalf
- Revoke API access anytime: **Dashboard → Resumex API → Revoke**
- Edits appear live at https://resumex.dev immediately after saving
