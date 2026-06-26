---
name: browser-file-upload
description: >
  MUST be used for any browser file upload task.
  Provides reliable, step-by-step automation for uploading files via agent-browser CLI.
  Includes strict execution protocol, fallback strategies, and path normalization.
---

# Browser File Upload (Industrial-Grade)

Automates file uploads to web pages using agent-browser CLI with high reliability.

---

# 🔥 Execution Protocol (MANDATORY)

You MUST follow strict state-machine execution:

1. Execute ONLY ONE command at a time
2. WAIT for result before next step
3. VERIFY success before continuing
4. If failed → retry or fallback
5. DO NOT skip steps
6. DO NOT batch commands
7. DO NOT assume elements exist

---

# 🔥 Standard Upload Pipeline (REQUIRED)

Follow this exact sequence:

## Step 1 — Open Page
agent-browser open <url>

## Step 2 — Wait for Load
agent-browser wait 2000

If page is slow:
agent-browser wait --load networkidle

---

## Step 3 — Trigger File Input

Try in order:

1. agent-browser find text "选择文件" click
2. agent-browser find text "上传" click
3. agent-browser click "[type=file]"

If all fail:
agent-browser snapshot

---

## Step 4 — Upload File

Preferred selector:
agent-browser upload "[type=file]" <file-path>

If selector known:
agent-browser upload "<selector>" <file-path>

---

## Step 5 — Verify Upload (IMPORTANT)

agent-browser snapshot

Check:
- File name appears
- No error message
- Input is not empty

If failed → retry upload once

---

# 🔥 Strategy Selection

Priority:

1. ✅ Python script (MOST STABLE)
2. ⚠️ agent-browser commands (when selector known)

---

# 🔥 Python Script Mode (Recommended)

Use for robust execution:

```bash
python scripts/upload_file.py <url> <file-path> [selector] [wait_ms]
