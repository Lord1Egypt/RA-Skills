# Convert NotebookLM Export to Editable PPTX Workflow

Use this workflow when the user provides a local `.pptx` or `.pdf` file and wants to convert a NotebookLM-exported deck into an editable `.pptx`.

Follow these steps in order: identify the source file → upload it → run the conversion script in background → **read the log every 5 seconds and report progress** → deliver.

---

## 1. Confirm the source file

The user must provide a local `.pptx` or `.pdf` file.

- If the file path is ambiguous, ask the user for the full absolute path.
- If the file extension is not `.pptx` or `.pdf`, stop and explain that this workflow only supports those two input types.

---

## 2. Upload the source file to OSS

```bash
$PYTHON_CMD scripts/upload_files.py "/absolute/path/to/source.pptx"
```

or

```bash
$PYTHON_CMD scripts/upload_files.py "/absolute/path/to/source.pdf"
```

- Extract the OSS URL from the `[OK] ... -> https://...` output line.
- Call this value `SOURCE_URL`.

---

## 3. Run the conversion script

Run in the **background**, then read the progress log file every 5 seconds until done.

### 3a. Choose a log path and start in background

```bash
PPT_LOG=/tmp/ppt_editable_$(date +%s).log

$PYTHON_CMD scripts/run_editable_convert.py \
  --file-url "SOURCE_URL" \
  --file-type "pptx" \
  --log_path "$PPT_LOG" \
  -o /absolute/path/to/output_editable.pptx \
  > /dev/null 2>&1 &

echo "Log: $PPT_LOG"
```

or for pdf:

```bash
$PYTHON_CMD scripts/run_editable_convert.py \
  --file-url "SOURCE_URL" \
  --file-type "pdf" \
  --log_path "$PPT_LOG" \
  -o /absolute/path/to/output_editable.pptx \
  > /dev/null 2>&1 &
```

- **`--file-url`** (required): OSS URL of the uploaded source file.
- **`--file-type`** (recommended): explicitly pass `pptx` or `pdf`.
- **`--log_path`** (required): pass the pre-chosen path.
- **`-o`** (required): absolute output path for the converted `.pptx`.

### 3b. Monitor progress （REQUIRED）

> **STRICT RULES — no exceptions:**
> 1. **Read the log exactly every 5 seconds.** Do NOT extend the interval, do NOT skip reads.
> 2. **Before every read, check if the process is still alive.** If alive → only read log, NEVER restart.

**Every 5 seconds, run this exact sequence:**

```bash
# Step 1: extract PID from log
PPT_PID=$(grep '^\[PID\]' "$PPT_LOG" | tail -1 | awk '{print $2}')
# Step 2: check if process is alive
kill -0 "$PPT_PID" 2>/dev/null && PPT_ALIVE=true || PPT_ALIVE=false
# Step 3: read the log regardless
tail -20 "$PPT_LOG"
```

- If process is **RUNNING** → report status to user, wait 5s, repeat. Do NOT touch the script.
- If process is **not running** AND log ends with `[DONE]` or `[ERROR]` → stop polling, proceed to deliver/handle error.
- If process is **not running** AND no `[DONE]`/`[ERROR]` in log → the script crashed; report error to user, ask whether to retry.

Each line is plain text:
- `[PID] <pid>` — process ID written at startup
- `[START]` — job started
- `[PHASE] <message>` — in progress
- `[PROGRESS] <message>` — heartbeat progress update
- `[DONE] saved=<path> download_url=<url>` — finished
- `[ERROR] <message>` — failed

**After each read, report status to the user:**

```text
[Main stage] | [current action]
Example: Converting HTML | Converting batch 2/4
```

Progress phases:

| Message contains | Main stage |
|-----------------|------------|
| "Capturing screenshots" / "Screenshots captured" | Capturing screenshots |
| "Uploading screenshot" / "Screenshot upload complete" | Uploading screenshots |
| "Building nano HTML" / "Nano HTML ready" | Building nano HTML |
| "Converting HTML" / "Converted batch" | Converting HTML |
| "Exporting editable PPTX" / "Export complete" | Exporting PPTX |

**Stop polling** as soon as you see `[DONE]` or `[ERROR]`.

---

## 4. Deliver

Provide all of the following:
1. Download link (`download_url` from the completion event)
2. Local `.pptx` absolute path
3. The original filename used as the source

### Failure

Briefly explain the error.
