#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  transcribe.sh <audio-file> [--language en] [--operating-point enhanced|standard]
                             [--format txt|json|srt] [--out /path/to/out.ext]
                             [--diarization none|speaker]
                             [--poll-interval 3] [--timeout 600]
                             [--api-key KEY] [--base-url URL]
EOF
  exit 2
}

if [[ "${1:-}" == "" || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
fi

in="${1:-}"
shift || true

language="en"
operating_point="enhanced"
format="txt"
out=""
diarization="none"
poll_interval=3
timeout_seconds=600
api_key="${SPEECHMATICS_API_KEY:-}"
base_url="${SPEECHMATICS_BASE_URL:-https://asr.api.speechmatics.com/v2}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --language) language="${2:-}"; shift 2 ;;
    --operating-point) operating_point="${2:-}"; shift 2 ;;
    --format) format="${2:-}"; shift 2 ;;
    --out) out="${2:-}"; shift 2 ;;
    --diarization) diarization="${2:-}"; shift 2 ;;
    --poll-interval) poll_interval="${2:-}"; shift 2 ;;
    --timeout) timeout_seconds="${2:-}"; shift 2 ;;
    --api-key) api_key="${2:-}"; shift 2 ;;
    --base-url) base_url="${2:-}"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; usage ;;
  esac
done

if [[ ! -f "$in" ]]; then
  echo "File not found: $in" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "Missing dependency: jq" >&2
  exit 1
fi

if [[ -z "$api_key" ]]; then
  cfg="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
  if [[ -f "$cfg" ]]; then
    api_key="$(jq -r '.skills.entries.speechmatics.apiKey // empty' "$cfg" 2>/dev/null || true)"
  fi
fi

if [[ -z "$api_key" ]]; then
  echo "Missing Speechmatics API key. Set SPEECHMATICS_API_KEY, pass --api-key, or add skills.entries.speechmatics.apiKey to openclaw.json" >&2
  exit 1
fi

case "$format" in
  txt)  transcript_format="txt";    ext="txt"  ;;
  json) transcript_format="json-v2"; ext="json" ;;
  srt)  transcript_format="srt";    ext="srt"  ;;
  *) echo "Invalid --format: $format (txt|json|srt)" >&2; exit 1 ;;
esac

if [[ -z "$out" ]]; then
  out="${in%.*}.${ext}"
fi
mkdir -p "$(dirname "$out")"

if [[ "$diarization" == "none" ]]; then
  config_json=$(jq -n \
    --arg language "$language" \
    --arg op "$operating_point" \
    '{type:"transcription", transcription_config:{language:$language, operating_point:$op}}')
else
  config_json=$(jq -n \
    --arg language "$language" \
    --arg op "$operating_point" \
    --arg diar "$diarization" \
    '{type:"transcription", transcription_config:{language:$language, operating_point:$op, diarization:$diar}}')
fi

api_base="${base_url%/}"

submit_resp=$(curl -sS -X POST "${api_base}/jobs" \
  -H "Authorization: Bearer ${api_key}" \
  -F "data_file=@${in}" \
  -F "config=${config_json}")

job_id=$(echo "$submit_resp" | jq -r '.id // empty')
if [[ -z "$job_id" ]]; then
  echo "Failed to submit job: $submit_resp" >&2
  exit 1
fi

echo "Submitted job: $job_id" >&2

started=$(date +%s)
while :; do
  status_resp=$(curl -sS "${api_base}/jobs/${job_id}" \
    -H "Authorization: Bearer ${api_key}")
  status=$(echo "$status_resp" | jq -r '.job.status // empty')
  case "$status" in
    done)
      break
      ;;
    running)
      ;;
    rejected)
      err=$(echo "$status_resp" | jq -r '.job.errors // .job // .')
      echo "Job rejected: $err" >&2
      exit 1
      ;;
    "")
      echo "Unexpected response from /jobs/${job_id}: $status_resp" >&2
      exit 1
      ;;
    *)
      ;;
  esac

  now=$(date +%s)
  if (( now - started > timeout_seconds )); then
    echo "Timeout waiting for job $job_id (status=$status, waited=${timeout_seconds}s)" >&2
    exit 1
  fi
  sleep "$poll_interval"
done

curl -sS "${api_base}/jobs/${job_id}/transcript?format=${transcript_format}" \
  -H "Authorization: Bearer ${api_key}" \
  > "$out"

echo "$out"
