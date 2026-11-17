# uni-course-scheduler

> AI-powered university course planning assistant — analyze course catalogs, get smart course recommendations, build conflict-free weekly timetables, and export Excel (local + cloud) and ICS calendar files (cloud standard mode only).

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Default language:** English (this README). The Skill itself responds in the user's preferred language; this file is the default documentation language only.

---

## What it does

`uni-course-scheduler` is an AI Skill that helps university students plan their semester:

- **Catalog analysis** — parses a school's official course catalog (program handbook text) into structured course data: codes, names, credits/points, prerequisites, term availability, and timetable slots.
- **Course recommendation** — recommends courses matched to the student's goals (e.g. GPA-first, ML specialization), flags enrollment priority, and validates prerequisites.
- **Weekly schedule** — builds a conflict-free weekly timetable from the real timetable, respecting preferences like "no 8am classes" or "keep 12:00–13:00 free".
- **Excel export** — generates a 6-sheet (local) or 7-sheet (cloud) Excel workbook, including `Weekly Timetable`, `Degree Planner`, and (cloud) `Degree Audit & Risk Assessment`.
- **ICS calendar** — exports a downloadable `.ics` file for Apple Calendar / Google Calendar (cloud mode).

Supports **international credit systems** (US / AU / UK / ECTS / CN / HK / SG) and **undergraduate and graduate** students.

---

## How it works (two modes)

This Skill ships in two execution modes:

### 1. Local personal mode (free)
The agent itself researches the official course catalog, verifies it, and produces a 6-sheet Excel + a textual weekly overview.
- Free, single-school, single-student, personal use only.
- No batch pipeline, no standardized decision report, no downloadable `.ics` calendar, no deep degree audit.

### 2. Cloud standard mode (paid)
A fixed production-grade cloud pipeline (`catalog → recommend → schedule → decision → ICS → degree-audit`) processes the catalog text and returns:
- Batch / multi-school / multi-student execution.
- Standardized 8-dimension **Decision Report**.
- **Degree Audit & Risk Assessment** sheet (prerequisite chains, credit progress, overload risks).
- **Downloadable `.ics` calendar** (university term dates, weekly recurrence, correct IANA timezone).

> **Offline-cloud note:** Like most hosted LLM pipelines, the cloud executor has no internet access. The local agent (or the user) must first paste the official catalog text. The pipeline never fabricates data — anything not found in the input is reported honestly as missing.

---

## Cloud platform (choose your payment)

The cloud command is platform-agnostic; the platform is chosen by your payment method:

| Your payment | Platform | Price | Server | Token env |
|---|---|---|---|---|
| China mainland payment (Alipay/WeChat/UnionPay) | Shengsuanyun | ¥0.5/run | `loomloom.shengsuanyun.com` | `LOOMLOOM_TOKEN_SHENGSUANYUN` |
| International credit card (Visa/MC) | CogFoundry | $0.10/run | `loomloom.cogfoundry.ai` | `LOOMLOOM_TOKEN_COGFOUNDRY` |

On first cloud use, the assistant asks which payment you use and configures the matching server. See `references/loomloom-setup.md` for full setup.

---

## Install

### Prerequisites
- An AI assistant that supports custom Skills (e.g. WorkBuddy / Claude Code / Codex / Cursor-style agent).
- For **cloud mode**: a platform account + balance.

### Option A — drag & drop (friendliest)
1. Download the `uni-course-scheduler.zip` release.
2. Drag the ZIP into your AI chat and say: **"Please install this planning Skill for me."**
3. The AI agent installs it and you can start.

### Option B — manual install
```bash
# 1. Unzip the package (installs as a plain skill folder — no background service, no cron, no persistent state)
mkdir -p ~/.workbuddy/skills && cd ~/.workbuddy/skills
unzip /path/to/uni-course-scheduler.zip

# 2. Verify the folder structure
ls ~/.workbuddy/skills/uni-course-scheduler   # SKILL.md, scripts/, references/
```

### Cloud setup (optional, for cloud mode)
```bash
# Install the LoomLoom CLI (buyer flow)
# See references/loomloom-setup.md for full instructions
loomloom login          # sign in with your key
loomloom market list    # verify connectivity
```

---

## Usage

### Plan a course schedule
1. Tell the agent your school, major, year, and goals (e.g. "GPA first, prefer no 8am classes").
2. Provide the official catalog text — let the local agent fetch it, or paste it.
3. Choose a mode: **Local (free)** or **Cloud (paid)**.
4. Confirm the fee (cloud) and receive: an Excel workbook (`.xlsx`) + a downloadable `.ics` calendar (cloud).

### Collect a course catalog
See `references/catalog-collection.md` for a reusable prompt and quality gates (≥500 chars, ≥5 courses, official source).

---

## Project structure

```
uni-course-scheduler/
├── SKILL.md                      # Main skill instructions (both modes)
├── README.md                     # This file (English)
├── README.zh-CN.md               # Chinese version of this README
├── LICENSE                       # MIT (local code); cloud TemplateSpec proprietary
├── agents/
│   └── openai.yaml               # OpenAI / compatible agent metadata
├── references/
│   ├── catalog-collection.md     # How to collect & verify catalogs
│   ├── excel-output-spec.md      # Excel workbook schema
│   ├── cloud-output-format.md    # Cloud pipeline output format
│   ├── interaction-flow.md       # End-to-end user flow
│   ├── local-validation.md       # Local output validation rules
│   └── loomloom-setup.md         # Cloud setup (dual-platform)
└── scripts/
    ├── generate_excel.py         # Build the Excel workbook from JSON
    ├── generate_ics.py           # Render .ics from cloud ICS data
    ├── anti_hallucination_check.py  # Anti-hallucination validation
    ├── validate_schedule.py      # Schedule conflict validation
    ├── local_audit.py            # Local output audit
    └── check_github_downloads.py # Download stats helper
```

---

## Quality & anti-hallucination

- **No fabrication:** data not present in the input is labeled `NOT_FOUND` / missing — never invented.
- **Honest empty:** for garbage/empty input returns an honest empty result with guidance, not a hallucination.
- **Validation:** local scripts run schedule-conflict checks and an anti-hallucination audit on every output.

---

## License

**MIT License (local Skill).** The local skill files are open source under MIT. The cloud TemplateSpec (prompts, orchestration, output contracts) remains the author's proprietary asset and is licensed per paid call — it is not covered by MIT. See [LICENSE](LICENSE).

---

## Support / Feedback

- Author: ez-hq
- Found a bug or have a catalog request? Open an issue in the repository.