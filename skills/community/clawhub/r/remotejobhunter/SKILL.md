---
name: remote-job-hunter
description: "Automates daily remote job search, matching, and email reports. Invoke when the user asks to search remote jobs, find job matches, run job hunting, or set up daily job alerts. Triggers on keywords: 'job hunt', 'find remote jobs', 'search jobs', 'job alert', 'remote work', 'daily job search'."
agent_created: true
---

# Remote Job Hunter

Automated remote job search tool. Searches multiple sources, matches against user's profile, verifies job links are still open, and delivers reports via email or console.

## When to Use

Invoke this skill when the user:
- Asks to search for remote jobs or job opportunities
- Wants to find job matches based on their resume/skills
- Requests a daily job hunting setup or job alerts
- Says keywords like "job hunt", "find remote jobs", "search jobs", "job alert", "remote work"

## Quick Commands

The skill provides these entry points for the agent to call directly:

### 1. Instant Job Search (run now, output to console)
```bash
python3 run_now.py --dry-run
```
This runs the full pipeline (search -> match -> verify) and prints results to console without sending email. Use this when the user wants to see jobs immediately.

### 2. Full Pipeline with Email Report
```bash
python3 daily_scheduler.py
```
Runs the complete pipeline and sends email report if matches are found. Use for scheduled daily runs.

### 3. Setup / Reconfigure
```bash
python3 setup.py
```
Interactive setup. Use when config.json is missing or user wants to change settings.

### 4. Quick Setup from Template (non-interactive)
```bash
python3 setup.py --quick --name "User Name" --title "Job Title" --email "user@example.com"
```
Generates config.json without interactive prompts. Use when user provides info inline.

## Agent Usage Guide

### If user says "帮我搜一下远程工作" or "find me remote jobs":
1. Check if `config.json` exists. If not, ask user for: name, job title, email.
2. Run: `python3 run_now.py --dry-run`
3. Show the user the top matches from the output.

### If user says "set up daily job alerts" or "每天帮我找":
1. Ensure `config.json` exists (run setup.py if needed).
2. Run: `python3 daily_scheduler.py` once to test.
3. Help user set up cron or TRAE automation to run daily.

### If user wants to change keywords, skills, or filters:
- Edit `config.json` directly — it's plain JSON. No need to re-run setup.
- Key fields to modify:
  - `search.keywords` — what jobs to search for
  - `profile.skills` — your skills for matching
  - `search.location_filter` — region preferences
  - `email.*` — where to send reports

## Configuration

`config.json` controls all behavior. Key sections:

| Section | Purpose |
|---------|---------|
| `profile` | Name, title, skills, interests, dealbreakers |
| `search.keywords` | Search terms (auto-generated from title + skills) |
| `search.location_filter` | Region filtering mode and keywords |
| `search.platforms` | Which job sources to query |
| `email` | SMTP settings for daily reports |
| `cover_letter` | Style settings for cover letter drafts |

### Location Filter Modes
- `"all"` — no filtering, show all remote jobs
- `"exclude_only"` — only remove jobs matching exclusion keywords
- `"include_global"` — prioritize preferred regions + exclude unwanted

## File Structure

```
remote-job-hunter/
├── SKILL.md              # Agent instructions (this file)
├── run_now.py            # Instant search entry point (agent-friendly)
├── daily_scheduler.py    # Full pipeline with email
├── setup.py              # Interactive or quick setup
├── config.json           # User configuration (generated)
├── config.template.json  # Config template
├── scripts/
│   ├── search_jobs.py    # Multi-source search
│   ├── match_jobs.py     # Resume-to-job scoring
│   ├── verify_jobs.py    # Link verification
│   └── send_email.py     # Email reports
└── README.md             # Human documentation
```

## Troubleshooting

**No config.json found:** Run `python3 setup.py` or `python3 setup.py --quick` with required flags.

**No jobs found:** Check `config.json` -> `search.keywords`. Try setting `location_filter.mode` to `"all"`.

**Email not received:** Check spam folder; verify SMTP credentials in `config.json`.

**SMTP / Gmail App Password:** Generate at https://myaccount.google.com/apppasswords

---

**License**: MIT-0
