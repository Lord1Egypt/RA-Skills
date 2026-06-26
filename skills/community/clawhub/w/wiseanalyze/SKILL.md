---
name: wisediag-checkup
description: "Medical Checkup Report Analysis — Upload a PDF checkup report (via URL or local file binary upload) for AI-powered health interpretation with abnormal item detection, clinical explanations, lifestyle assessment, and personalized recommendations. Supports health questionnaires for tailored analysis. Triggered when the user asks to analyze a checkup report and provides a PDF URL or local file path. Can also be invoked explicitly: say 'Use WiseAnalyze to analyze this checkup report'."
registry:
  homepage: https://github.com/wisediag/WiseDiag-Checkup
  author: wisediag
env_vars:
  - WISEDIAG_API_KEY
credentials:
  required: true
---

## When to Use This Skill

Activate this skill when any of the following conditions are met:

- The user sends a **PDF link** of a checkup report and asks to analyze or interpret it
- The user provides **local files** (PDF or images) of a checkup report and asks to analyze them
- The user says things like "help me analyze my checkup report", "look at my health report", "interpret this medical report", or similar requests (in any language)
- The user mentions checkup report analysis needs and provides a PDF URL or local file paths

**Note:** This skill supports both **publicly accessible PDF URLs** and **local file uploads** (PDF and images). The most common usage scenario is **uploading local files via binary stream** (`--file`), as users typically have report files saved on their device rather than hosted at a public URL.

**How to choose (mutually exclusive — pick one):**
- If the user provides a **local file path** (e.g. `/home/user/report.pdf`, `C:\Users\...\report.pdf`, or relative path) → use `--file` (binary upload). **This is the primary and most common usage.**
- If the user provides a **URL** (starts with `http://` or `https://`) → use `--url`
- Do NOT use `--url` and `--file` together in one command

---

# ⚠️ Privacy Warning

**IMPORTANT - READ BEFORE INSTALLING:**

This skill **uploads your checkup report to WiseDiag's cloud servers** (via PDF URL or direct binary file upload) for AI-powered health analysis.

**Do NOT use with sensitive or confidential medical documents** unless:
- You trust WiseDiag's data handling policies
- You accept that file contents will be transmitted and processed remotely

**For sensitive documents, use offline/local checkup report analysis tools instead.**

---

# WiseAnalyze Skill (powered by WiseDiag)

An AI-powered medical checkup report analysis tool. Submit a checkup report (via **local file upload** or **publicly accessible PDF URL**), and the system will return a **structured health interpretation** including abnormal items, clinical explanations, lifestyle advice, and personalized recommendations.

The analysis uses an **async task model** with 4 separate sub-commands. You (the Agent) must call each step and handle polling yourself.

## Installation

```bash
pip install -r requirements.txt
```

## 🔑 API Key Setup (Required)

**Get your API key:** 👉 [https://console.wisediag.com/apiKeyManage](https://s.wisediag.com/xsu9x0jq)

The API key MUST be set as an environment variable. The script reads it automatically.

```bash
export WISEDIAG_API_KEY=your_api_key
```

## How to Analyze a Report (Step-by-Step)

**NEVER call any API or HTTP endpoint directly. ONLY use the script sub-commands below.**

**⚠️ IMPORTANT: Each command makes HTTP requests to an external API and may take 10-30 seconds to complete. Do NOT kill or interrupt a running command — wait for it to finish. The script prints progress messages so you can see it is still working.**

The workflow has 4 steps. You MUST follow them in order.

---

### Step 1: Submit local files or PDF URL

There are two ways to submit — pick one (mutually exclusive):

**Option A: Upload local files (recommended)** — when user provides local file paths

```bash
cd scripts
python3 wise_analyze.py submit -f "/path/to/checkup_report.pdf"
python3 wise_analyze.py submit -f "/path/to/report.pdf" -f "/path/to/scan.jpg"
```

**Option B: Submit via URL** — when user provides a public HTTP/HTTPS link

```bash
cd scripts
python3 wise_analyze.py submit -u "https://example.com/checkup_report.pdf"
```

With optional health questionnaire (recommended for better results):

```bash
python3 wise_analyze.py submit -f "/path/to/report.pdf" -q "occasional chest tightness, family history of hypertension, poor sleep quality"
```

With optional member ID to link to a health profile:

```bash
python3 wise_analyze.py submit -f "/path/to/report.pdf" -m "HR1017911158367870xxxx"
```

**Output:** The script prints `TASK_ID=<id>`. Save this task ID for the next steps.

**How to choose (mutually exclusive — pick one):**
- User gives a local file path (e.g. `/home/user/report.pdf`, `C:\Users\...\report.pdf`) → use `-f`
- User gives a URL (starts with `http://` or `https://`) → use `-u`
- Do NOT use `-u` and `-f` together in one command

---

### Step 2: Start interpretation

```bash
cd scripts
python3 wise_analyze.py start -t "<task_id>"
```

**Output:** Prints confirmation that interpretation has started.

---

### Step 3: Poll for progress (YOU must repeat this)

**⚠️ CRITICAL: You MUST NOT skip this step. Do NOT jump directly to Step 4.**

```bash
cd scripts
python3 wise_analyze.py query -t "<task_id>"
```

**Output:** The script prints machine-readable status:

```
STATUS=processing
PROGRESS=50
```

**Polling rules:**
- If `STATUS=queued` or `STATUS=processing` → **tell the user the current progress percentage**, then wait and poll again using **dynamic intervals based on progress**:
  - `PROGRESS` 0–30%: wait **10 seconds** before next query
  - `PROGRESS` 30–70%: wait **8 seconds** before next query
  - `PROGRESS` 70%+: wait **5 seconds** before next query
- If `STATUS=finish` → proceed to Step 4
- If `STATUS=failed` → the task failed, inform the user

**You MUST:**
1. Keep calling the query command until STATUS is `finish` or `failed`. Do NOT give up after one check.
2. **Report each polling result to the user** so they can see the analysis progress (e.g. "Analysis progress: 50%..."). Do NOT silently poll without updating the user.
3. Never skip Step 3 and go directly to Step 4. The `save` command will fail if the task is not finished.

---

### Step 4: Save the result

```bash
cd scripts
python3 wise_analyze.py save -t "<task_id>" -n "report_2025"
```

**Output:** The command saves the report and prints `REPORT_PATH=<path>`.

If `-n` is not provided, the task ID is used as the filename.

**⚠️ IMPORTANT — How to present the result to the user:**

After the save command completes, you MUST:
1. Read the saved `.md` file using the path printed in `REPORT_PATH=`
2. Output a brief one-sentence introduction (e.g. "以下是您的体检报告分析结果：")
3. Output the full report content **directly** as-is (rendered Markdown) — do NOT summarize, condense, reorganize, or rephrase any part of it
4. After the full report, append a short "关键提醒" section: extract 2-3 most critical items from the report that need immediate attention, keep each point to one sentence
5. Do NOT omit or shorten the report body itself — the full report must be shown in its entirety between the intro and the closing reminder

---

## Sub-commands Reference

### submit

| Flag | Description |
|------|-------------|
| `-u, --url` | Publicly accessible URL of the PDF checkup report (optional, requires --url or --file) |
| `-f, --file` | Local file path to upload, PDF or image (optional, repeatable for multiple files) |
| `-q, --questionnaire` | Health questionnaire text: symptoms, family history, lifestyle (optional but recommended) |
| `-m, --member-id` | Health profile member ID to link report to existing profile (optional) |

### start

| Flag | Description |
|------|-------------|
| `-t, --task-id` | Task ID returned from the submit step (required) |

### query

| Flag | Description |
|------|-------------|
| `-t, --task-id` | Task ID to check status (required) |

### save

| Flag | Description |
|------|-------------|
| `-t, --task-id` | Task ID to save result (required) |
| `-n, --name` | Output filename stem (default: taskId) |
| `-o, --output` | Output directory (default: current working directory) |

## Data Privacy

**What happens to your files:**
1. When using `--url`: The PDF URL is sent to WiseDiag's analysis API, downloaded and processed on their servers
2. When using `--file`: Local files are uploaded directly to WiseDiag's servers via multipart/form-data
3. AI-powered health interpretation results are returned to you
4. Files are not permanently stored on WiseDiag servers

**For sensitive documents, use offline/local checkup report analysis tools instead.**

## License

MIT
