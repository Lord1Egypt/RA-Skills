---
name: batchjob-async-job
description: "Use BatchJob HTTP APIs for strict upload validation, precheck, submit, polling, and cancellation. Full-auto file source resolution (file_id/local path/public URL/channel attachment path) with fallback interaction only when source is not readable."
metadata: { "openclaw": { "emoji": "🧪", "requires": { "bins": ["curl"], "env": ["BATCHJOB_BASE_URL", "BATCHJOB_BEARER_TOKEN"] } } }
---

# BatchJob Async Job Skill

Use this skill when the user wants to run or manage batch jobs through the BatchJob service.

## Required Environment

- `BATCHJOB_BASE_URL`
- `BATCHJOB_BEARER_TOKEN`

All HTTP requests must include:

```bash
-H "Authorization: Bearer ${BATCHJOB_BEARER_TOKEN}"
-H "Content-Type: application/json"
```

## API Endpoints

- `POST /v1/batch/files:upload`
- `POST /v1/batch/jobs:precheck`
- `POST /v1/batch/jobs`
- `GET /v1/batch/jobs/{job_id}`
- `GET /v1/batch/jobs?page=1&page_size=10&status=...`
- `POST /v1/batch/jobs/{job_id}:cancel`

## Automation Policy (Default)

- Always run in full-auto mode.
- Do not ask user for `file_id` first.
- Resolve file source from current message/context, then upload automatically when needed.
- Ask follow-up questions only when no readable file source can be obtained.
- Accepted input file formats for upload: `jsonl`, `csv`, `xlsx`, `xls` (BatchJob normalizes to internal JSONL).
- For `jsonl`, each line must be either:
  - canonical Vertex format (`contents` + optional `generationConfig`)
  - simple prompt format (`prompt` + optional `aspect_ratio` / `image_urls`, where `image_urls` must be publicly reachable URLs)
- If user gives only `model mode` after a file message, treat it as confirmation and continue automatically.

## Guardrails (Must Follow)

- Do not auto-retry by creating a second job unless user explicitly asks.
- Do not auto-rewrite dataset format after a terminal failure unless user explicitly asks.
- Before upload, auto-normalization is allowed only once for known safe mappings (e.g. simple prompt JSONL -> Vertex JSONL).
- Upload failure is terminal for this run: do not continue to precheck/submit when upload fails.
- Never submit when `row_count <= 0`.
- Do not fetch or parse `output_summary_url` automatically; only do it when user asks for detailed failure reason.
- After reaching terminal status (`completed`, `failed`, `partially_failed`), stop execution and return summary immediately.

## JSONL Compatibility Rule (Important)

BatchJob internal execution expects each JSONL line to be a `VertexGeminiImageRequest` shape.

- Canonical line format:
  - `contents[0].parts[0].text` contains prompt text
  - `generationConfig.imageConfig.aspectRatio` is optional
  - `generationConfig.responseModalities` should include `IMAGE` and `TEXT`
- Non-canonical simple JSONL like `{"prompt":"...","aspect_ratio":"1:1"}` is acceptable; server will normalize it to Vertex format.
- If JSONL has neither `contents` nor `prompt`, stop and ask user to provide valid data.
- Explicitly unsupported (must reject before submit):
  - OpenAI Batch style lines containing `method` + `url` + `body` (for example `/v1/chat/completions` payload).
  - This schema will fail with Vertex error: `at least one contents field is required`.

## Dataset Output Rule (Important)

When user asks you to generate a template/demo file for BatchJob image tasks:

- Prefer CSV headers: `prompt,aspect_ratio,image_urls`
- Or JSONL line format with `prompt` / `aspect_ratio` / `image_urls`
- If `image_urls` is provided, it must be publicly accessible (http/https).
- Do NOT generate OpenAI batch envelope (`custom_id` + `method` + `url` + `body`) as final upload file

## User Template Response (Important)

When user asks for format/template, return:

1. A short explanation (`prompt` required, `aspect_ratio`/`image_urls` optional, and `image_urls` must be public URLs).
2. One copyable CSV snippet (default).
3. Optionally one JSONL snippet (simple prompt schema).
4. Local template file paths (if available):
   - `/home/node/.openclaw/workspace/templates/batchjob-input-template.csv`
   - `/home/node/.openclaw/workspace/templates/batchjob-input-template.jsonl`
   - `/home/node/.openclaw/workspace/templates/batchjob-format-guide.md`

Do not output OpenAI batch envelope examples in template replies.

## File Source Resolver (Strict Order)

1. Existing `file_id`:
   - if provided, skip upload.
2. Public `file_url` (`http://` or `https://`):
   - download to temp local file, then upload.
3. Explicit local `file_path`:
   - if readable, upload.
4. Inbound attachment local path from channel/runtime context:
   - examples: `/tmp/...`, `MEDIA:<path>`, `/tmp/openclaw-media/...`.
   - if readable, upload.
5. Channel private file token/object (no local path, no public URL):
   - if runtime has a channel adapter that can download attachment bytes, use it and upload.
   - if not available, enter fallback interaction.

Resolver output must be normalized to one of:
- `file_id`
- `file_path` (readable local file)

## Execution Flow

1. Confirm `model` and `mode`; if missing, use safe defaults (`model=google/gemini-2.5-flash-image`, `mode=fast`) and tell user.
2. Resolve file source using resolver above.
3. If resolver gives `file_path`, upload via `POST /v1/batch/files:upload` to get `file_id`.
   - For `.jsonl`, inspect a few non-empty lines first:
     - if `contents` exists, upload as-is.
     - if only `prompt`/`aspect_ratio`/`image_urls` exists, upload as-is (server will normalize).
     - if `method` + `url` + `body` exists, stop and ask user to switch to BatchJob schema.
     - if structure is unknown, stop and ask user for valid schema.
   - Backward compatibility fallback:
   - if upload fails with `unsupported file type` for `csv/xlsx/xls`, convert once to JSONL and retry upload once.
   - do not retry more than once.
   - If upload returns validation error (`unsupported schema`, `no valid data rows`), stop immediately and return fix guidance.
4. Run precheck with `record_count` (prefer uploaded file `row_count`).
5. Submit job with `file_id`.
6. Poll job status until terminal (`completed`, `failed`, `partially_failed`) with bounded timeout:
   - interval: 5 seconds
   - max polls: 12 (about 60 seconds)
   - if still non-terminal after max polls: return current status and `job_id`, then stop.
7. Return concise summary with `job_id`, status, progress, and `output_summary_url`.

When user only asks for estimate, stop at precheck and do not submit.

## Fallback Interaction (Only When Needed)

Use this when resolver cannot read file bytes from current channel/context:

`我拿到了“文件引用”，但当前运行环境无法直接读取该附件内容。请任选其一：`
`1) 直接发一个可公网下载的 URL`
`2) 提供本机可读路径（如 /tmp/xxx.csv）`
`3) 先把文件上传到 BatchJob，给我 file_id`

If the current channel supports resending as direct attachment path in context, also ask user to resend once.

## File Source Playbook

### A) Public URL -> Local Temp File

```bash
FILE_URL="https://example.com/input.jsonl"
EXT="${FILE_URL##*.}"
FILE_PATH="$(mktemp "/tmp/batchjob-input.XXXXXX.${EXT:-jsonl}")"
curl -fL --retry 3 --connect-timeout 10 "$FILE_URL" -o "$FILE_PATH"
```

### A2) JSONL Schema Sanity Check

Use this before upload to avoid wrong schema submission.

```bash
SRC_JSONL="/tmp/input.jsonl"
FIRST_LINE="$(grep -m1 -v '^[[:space:]]*$' "$SRC_JSONL")"
echo "$FIRST_LINE" | jq -e '
  (has("contents")) or
  (has("prompt")) and ( (has("method")|not) and (has("url")|not) and (has("body")|not) )
' >/dev/null || {
  echo "JSONL schema invalid for BatchJob: requires contents or prompt-only schema"
  exit 1
}
```

### B) Feishu/Channel Attachment Path

If message context already includes local attachment path, treat it as `FILE_PATH` directly.

```bash
FILE_PATH="/tmp/openclaw-media/your-uploaded-file.jsonl"
```

If only a channel token/link is provided but no downloadable URL and no local path, try channel adapter download first. If adapter is unavailable, use fallback interaction.

## Curl Templates

```bash
FILE_PATH="/path/to/input.jsonl"
FILE_NAME="$(basename "${FILE_PATH}")"
test -f "${FILE_PATH}" || { echo "文件 ${FILE_PATH} 不存在"; exit 1; }
FILE_CONTENT_B64="$(base64 < "${FILE_PATH}" | tr -d '\n')"

curl -sS "${BATCHJOB_BASE_URL}/v1/batch/files:upload" \
  -H "Authorization: Bearer ${BATCHJOB_BEARER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"filename\":\"${FILE_NAME}\",\"mode\":\"fast\",\"content\":\"${FILE_CONTENT_B64}\"}"
```

```bash
curl -sS "${BATCHJOB_BASE_URL}/v1/batch/jobs:precheck" \
  -H "Authorization: Bearer ${BATCHJOB_BEARER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"record_count": 100, "model": "google/gemini-2.5-flash-image", "mode": "fast"}'
```

```bash
curl -sS "${BATCHJOB_BASE_URL}/v1/batch/jobs" \
  -H "Authorization: Bearer ${BATCHJOB_BEARER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"file_id": "your-file-id", "model": "google/gemini-2.5-flash-image", "mode": "fast"}'
```

```bash
curl -sS "${BATCHJOB_BASE_URL}/v1/batch/jobs/${JOB_ID}" \
  -H "Authorization: Bearer ${BATCHJOB_BEARER_TOKEN}"
```

```bash
curl -sS "${BATCHJOB_BASE_URL}/v1/batch/jobs/${JOB_ID}:cancel" \
  -H "Authorization: Bearer ${BATCHJOB_BEARER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"reason":"user requested cancellation"}'
```
