---
name: remote-job-hunter
description: Automatically find remote jobs every day and match them to your resume. Use when the user wants to search for remote jobs, find jobs that match their skills, apply to jobs automatically, get a daily job search summary, find out what skills they are missing for their target roles, or receive WhatsApp alerts for new job matches. Searches 5 platforms daily (Remotive, RemoteOK, Jobicy, WeWorkRemotely, Himalayas), scores each job against your resume using NLP (0–100% match), identifies skill gaps with upskill recommendations, and generates a daily report. Supports .docx and .pdf resumes. Works for any role — AI/ML, QA Automation, Software Engineering, DevOps. Say things like "find me remote jobs", "search jobs matching my resume", "what skills am I missing", "run my daily job search", "apply to best matching jobs", or "send me a WhatsApp job summary".
---

# Remote Job Hunter

> Find remote jobs daily, match them to your resume, and know exactly what to upskill.

[![clawhub](https://img.shields.io/badge/clawhub-remote--job--hunter-blue)](https://clawhub.ai)
[![version](https://img.shields.io/badge/version-1.0.1-green)](https://github.com/RajkiranVS/openclaw-remote-job-hunter)
[![platforms](https://img.shields.io/badge/platforms-5-orange)](https://github.com/RajkiranVS/openclaw-remote-job-hunter)

## What it does

Every day, automatically:

1. 🔍 **Searches 5 job platforms** — Remotive, RemoteOK, Jobicy, WeWorkRemotely, Himalayas
2. 📊 **Scores every job** against your resume (0–100% NLP match)
3. 🎯 **Finds your skill gaps** — tells you exactly what to learn, ranked by how many jobs need it
4. 📱 **Sends a WhatsApp summary** of top matches via your OpenClaw agent
5. 🤖 **Auto-apply engine** — coming in v1.1.0 (not in current release)

## Why it beats manual job searching

| Manual search | remote-job-hunter |
|---------------|-------------------|
| 1–2 hours/day | 0 minutes/day |
| Miss jobs posted overnight | Catches everything daily at 7 AM |
| No idea how well you match | Exact % score per job |
| No skill gap visibility | Top 10 gaps with effort level |
| Apply to everything | Only apply to strong matches |

## Install
```bash
npx clawhub install remote-job-hunter
```

## Quick Start
```bash
# 1. Copy and fill in your profile (2 minutes)
cp config/profile.template.json my-profile.json

# 2. Run your first job search
python3 src/main.py \
  --profile-config my-profile.json \
  --profile-meta profiles/ai-ml.json \
  --output daily_report.md

# 3. Read your results
cat daily_report.md
```

## Supported Role Domains

| Domain | Target Roles |
|--------|-------------|
| `ai-ml` | AI/ML Architect, MLOps Engineer, GenAI Engineer, Data Scientist, LLM Engineer |
| `qa-automation` | TOSCA Lead, Test Architect, QA Automation Engineer, SDET, Test Lead |
| `software-dev` | Full Stack, Backend, Frontend, Software Engineer |
| `devops` | DevOps Engineer, Platform Engineer, SRE, Cloud Engineer |

## Sample Output
```
📊 Summary:
   Total jobs: 18
   🟢 80%+ match: 7

⚠️  Top skill gaps:
   - GCP (2 jobs) — Medium term
   - LangChain (1 job) — Quick win
   - Spark (1 job) — Long term
```

## Setting up daily WhatsApp summaries

Add to your OpenClaw cron:
```
Run: cd /path/to/remote-job-hunter && python3 src/main.py
  --profile-config my-profile.json
  --profile-meta profiles/ai-ml.json
  --output daily_report.md
Then read the report and send me a WhatsApp with top 3 matches and skill gaps.
```

## Security

- ✅ No credentials stored in config files
- ✅ Outbound requests only to public job board APIs
- ✅ All data written locally — nothing sent externally
- ✅ Input sanitization on all job content before agent processing
- ✅ Verified clean by VirusTotal (72/72 vendors undetected)

## Requirements
```
pymupdf>=1.23.0
```

## Roadmap

- ✅ v1.0.0 — Multi-platform search, NLP scoring, skill gap analysis
- ✅ v1.0.1 — Security hardening, input sanitization
- 🔄 v1.1.0 — Playwright auto-apply engine (Tier 1: email, Tier 2: form fill, Tier 3: platform login)
- 📋 v1.2.0 — Cover letter generation per application
- 📋 v1.3.0 — Application tracking dashboard

## Author

**Rajkiran Veldur** — AI/ML Solutions Architect  
[linkedin.com/in/rajkiranveldur](https://linkedin.com/in/rajkiranveldur) · [github.com/RajkiranVS/openclaw-remote-job-hunter](https://github.com/RajkiranVS/openclaw-remote-job-hunter)
