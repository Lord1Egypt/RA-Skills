# Local file upload flow

`create` never accepts a filesystem path. Local files are uploaded first via a
short-lived presigned PUT, then submitted with `--source upload`.

```bash
export TRANSCRIBE_API_KEY=tsk_live_...

# 1. Upload. Duration comes from --duration, or from ffprobe when installed.
#    Files over 50 MB warn on stderr; over 500 MB the CLI refuses and points
#    at the resumable tus flow (POST /api/v1/uploads/tus) or the web app.
UP=$(transcribe-so upload ./interview.mp3)
UPLOAD_ID=$(echo "$UP" | jq -r .upload_id)
DURATION=$(echo "$UP" | jq -r .duration_seconds)

# 2. Price it (free). Note: the quote's transcription_id is NOT the job id.
transcribe-so quote --source upload --upload-id "$UPLOAD_ID" --duration "$DURATION" \
  | jq '{billed_minutes, retail_usd}'

# 3. Transcribe under an explicit budget (quote -> create -> wait -> result).
transcribe-so run --source upload \
  --upload-id "$UPLOAD_ID" \
  --duration "$DURATION" \
  --max-usd 5 \
  > result.json

jq '.chapters[] | {title, start_seconds}' result.json

# 4. Subtitles, if wanted (the one command that prints raw text, not JSON).
ID=$(jq -r .id result.json)
transcribe-so subtitles "$ID" --format srt > interview.srt
```

Notes:

- The presigned URL expires in 900 seconds; `upload` PUTs immediately, so this
  only matters if you script the raw API yourself.
- At the account's concurrency cap, `source=upload` jobs are REJECTED with a
  fair-use error instead of queueing (URL sources queue FIFO). Wait for a
  running job to finish, then submit again; do not hammer retry.
- Step 3's `run` uses only the create 202 id internally; you never touch the
  quote's `transcription_id`.
