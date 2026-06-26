---
name: wisediag-analyze
description: "Medical Checkup Report Analysis — Upload a PDF checkup report (via URL or local file binary upload) for AI-powered health interpretation with abnormal item detection, clinical explanations, lifestyle assessment, and personalized recommendations. Supports health questionnaires for tailored analysis. Triggered when the user asks to analyze a checkup report and provides a PDF URL or local file path. Can also be invoked explicitly: say 'Use WiseAnalyze to analyze this checkup report'."
registry:
  homepage: https://github.com/wisediag/WiseAnalyze
  author: wisediag
env_vars:
  - WISEDIAG_API_KEY
credentials:
  required: true
---

# ⚠️ Privacy Warning

**IMPORTANT - READ BEFORE INSTALLING:**

This tool **sends your checkup report to WiseDiag's cloud servers** (via PDF URL or direct binary file upload) for AI-powered health analysis.

**Do NOT use with sensitive or confidential medical documents** unless:
- You trust WiseDiag's data handling policies
- You accept that file contents will be transmitted and processed remotely

**For sensitive documents, use offline/local checkup report analysis tools instead.**

---

# WiseAnalyze (OpenClaw Skill, powered by WiseDiag)

An AI-powered medical checkup report analysis tool that provides **structured health interpretations** from PDF checkup reports.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-green.svg)

## Features

- **PDF checkup report analysis**: submit via publicly accessible PDF URL or upload local files directly
- **Local file binary upload**: supports PDF and image files (JPG/PNG) via multipart/form-data
- **Async task model**: 4 separate sub-commands (submit → start → query → save)
- **Health questionnaire support**: provide symptoms and history for personalized analysis
- **Structured output**: abnormal items, clinical explanations, lifestyle advice, recommendations
- **Markdown output**: human-readable Markdown report
- **Health profile linking**: optionally link reports to existing member profiles
- **Agent-friendly**: machine-readable output for easy parsing by AI agents

## Installation

```bash
pip install -r requirements.txt
```

## 🔑 API Key Setup (Required)

**Get your API key:**
👉 [https://console.wisediag.com/apiKeyManage](https://s.wisediag.com/xsu9x0jq)

```bash
# Temporary (current terminal session)
export WISEDIAG_API_KEY=your_api_key_here

# Permanent (add to ~/.zshrc or ~/.bashrc)
echo 'export WISEDIAG_API_KEY=your_api_key_here' >> ~/.zshrc
source ~/.zshrc
```

## CLI Usage

**You MUST use the provided script sub-commands. Do NOT call any API or HTTP endpoint directly.**

### Step 1: Submit

There are two ways to submit a report — **upload local files** or **by URL**. Only one method can be used per submission.

**Option A: Upload local files (recommended)** — when user provides local file paths, uploads binary stream via multipart/form-data

```bash
cd scripts

# Upload a single PDF
python3 wise_analyze.py submit -f "/path/to/checkup_report.pdf"

# Upload multiple files (PDF + images mixed)
python3 wise_analyze.py submit -f "/path/to/report.pdf" -f "/path/to/page2.jpg"

# With health questionnaire
python3 wise_analyze.py submit -f "/path/to/report.pdf" -q "occasional chest tightness, poor sleep"

# With member ID
python3 wise_analyze.py submit -f "/path/to/report.pdf" -m "HR1017911158367870xxxx"
```

**Option B: Submit via URL** — when user provides a public HTTP/HTTPS link

```bash
cd scripts

# Basic submission with URL
python3 wise_analyze.py submit -u "https://example.com/checkup_report.pdf"

# With health questionnaire
python3 wise_analyze.py submit -u "https://example.com/report.pdf" -q "occasional chest tightness, family history of hypertension, poor sleep quality"

# With member ID
python3 wise_analyze.py submit -u "https://example.com/report.pdf" -m "HR1017911158367870xxxx"
```

**How to choose (mutually exclusive — pick one):**
- User gives a local file path (e.g. `/home/user/report.pdf`, `C:\Users\...\report.pdf`) → use `-f`
- User gives a URL (starts with `http://` or `https://`) → use `-u`
- Do NOT use `-u` and `-f` together in one command

Output: `TASK_ID=c1ecce57-4c9b-4f87-ba94-b81f8404c503`

### Step 2: Start

```bash
python3 wise_analyze.py start -t "c1ecce57-4c9b-4f87-ba94-b81f8404c503"
```

### Step 3: Query (repeat until finished)

```bash
python3 wise_analyze.py query -t "c1ecce57-4c9b-4f87-ba94-b81f8404c503"
```

Output:
```
STATUS=processing
PROGRESS=50
```

Repeat every 3-5 seconds until `STATUS=finish`.

### Step 4: Save

```bash
python3 wise_analyze.py save -t "c1ecce57-4c9b-4f87-ba94-b81f8404c503" -n "report_2025"
```

Report saved to `~/.openclaw/workspace/WiseAnalyze/{name}.md` (Markdown format).

## Sub-commands Reference

### submit

| Flag | Description |
|------|-------------|
| `-u, --url` | Publicly accessible URL of the PDF checkup report (optional, mutually exclusive with `-f`) |
| `-f, --file` | Local file path to upload as binary stream — PDF or image, repeatable for multiple files (optional, mutually exclusive with `-u`) |
| `-q, --questionnaire` | Health questionnaire text: symptoms, family history, lifestyle (optional) |
| `-m, --member-id` | Health profile member ID to link report to existing profile (optional) |

### start

| Flag | Description |
|------|-------------|
| `-t, --task-id` | Task ID from the submit step (required) |

### query

| Flag | Description |
|------|-------------|
| `-t, --task-id` | Task ID to check status (required) |

**Output fields:**
- `STATUS` — `queued`, `processing`, `finish`, or `failed`
- `PROGRESS` — 0-100 percentage
- `COMPLETED_AT` — completion time (only when finished)
- `HAS_RESULT` — `true` or `false` (only when finished)
- `HAS_ABNORMAL` — `true` or `false` (only when finished)

### save

| Flag | Description |
|------|-------------|
| `-t, --task-id` | Task ID to save result (required) |
| `-n, --name` | Output filename stem (default: taskId) |
| `-o, --output` | Output directory (default: ~/.openclaw/workspace/WiseAnalyze) |

## Output Structure

The analysis result includes the following sections:

| Section | Description |
|---------|-------------|
| Self-Reported Health Summary | Generated from questionnaire input (if provided) |
| Abnormal Items Overview | Summary of detected abnormal checkup items |
| Health Advantages | Positive health indicators |
| Detailed Health Consultations | In-depth analysis per abnormal item with clinical definitions |
| Lifestyle Impact | How lifestyle factors affect health |
| Personalized Recommendations | Tailored health improvement plans |
| Regular Review Plan | Short/mid/long-term follow-up schedule |
| References | Medical literature and guideline sources |

## Troubleshooting

**"WISEDIAG_API_KEY is not set" error:**
Make sure you've set the environment variable correctly. Run `echo $WISEDIAG_API_KEY` to check.

**"Authentication failed" error:**
Your API key may be invalid or expired. Visit [https://console.wisediag.com/apiKeyManage](https://s.wisediag.com/xsu9x0jq) to check or regenerate your key.

**"Bad request" error:**
Check that your PDF URL is publicly accessible (if using `-u`), or that file paths exist (if using `-f`). The PDF must not be encrypted and must not exceed 50 pages.

**"File not found" error:**
The local file path provided via `-f` does not exist. Check the path and try again.

**"Task is not finished yet" error on save:**
The task is still processing. Run the query command again to check status before saving.

## Data Privacy

- **URL mode (`-u`)**: The PDF URL is sent to WiseDiag's API; their server downloads and processes it.
- **File upload mode (`-f`)**: Local files are uploaded as binary streams via multipart/form-data to WiseDiag's server for processing.

Files are not permanently stored on WiseDiag servers. Results are returned directly to you.

## License

MIT
