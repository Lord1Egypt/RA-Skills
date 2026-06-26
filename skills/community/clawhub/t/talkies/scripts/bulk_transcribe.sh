#!/usr/bin/env bash
# Bulk-transcribe a list of files (local paths and/or http(s) URLs) through talkies.
#
# Usage:
#   bulk_transcribe.sh inputs.txt
#
#   inputs.txt has one entry per line — either a local file path or an
#   http(s):// URL. Blank lines and #-comment lines are ignored.
#
# Environment:
#   TALKIES_URL          Base URL of the talkies server (default: http://localhost:8000)
#   TALKIES_AUTH_TOKEN   Optional bearer token (sent on every request if set)
#   TALKIES_MODEL        Model slug (default: whisper-large-v3-turbo)
#   TALKIES_FORMAT       Response format — json|text|verbose_json|srt|vtt (default: text)
#   TALKIES_OUTDIR       Directory for per-input output files (default: ./out)
#   TALKIES_LANGUAGE     ISO-639-1 language hint (default: omitted — backend decides)
#   TALKIES_DIARIZE      "true" to request stereo diarization (default: omitted)
#
# Output:
#   $TALKIES_OUTDIR/<basename>.<ext> per input, where <ext> matches $TALKIES_FORMAT.
#   Exit 0 if every input succeeded, 1 if any failed.

set -euo pipefail

TALKIES_URL="${TALKIES_URL:-http://localhost:8000}"
TALKIES_MODEL="${TALKIES_MODEL:-whisper-large-v3-turbo}"
TALKIES_FORMAT="${TALKIES_FORMAT:-text}"
TALKIES_OUTDIR="${TALKIES_OUTDIR:-./out}"

if [[ $# -lt 1 ]]; then
    echo "usage: $0 <inputs.txt>" >&2
    exit 2
fi

inputs_file="$1"
if [[ ! -f "$inputs_file" ]]; then
    echo "error: inputs file not found: $inputs_file" >&2
    exit 2
fi

mkdir -p "$TALKIES_OUTDIR"

auth_args=()
if [[ -n "${TALKIES_AUTH_TOKEN:-}" ]]; then
    auth_args=(-H "Authorization: Bearer ${TALKIES_AUTH_TOKEN}")
fi

case "$TALKIES_FORMAT" in
    json|verbose_json) ext="json" ;;
    text) ext="txt" ;;
    srt) ext="srt" ;;
    vtt) ext="vtt" ;;
    *) echo "error: unsupported TALKIES_FORMAT=$TALKIES_FORMAT" >&2; exit 2 ;;
esac

fail=0
total=0
ok=0

# Verify the server is reachable before churning through the list.
if ! curl -sf "${auth_args[@]}" "$TALKIES_URL/healthz" >/dev/null; then
    echo "error: $TALKIES_URL/healthz unreachable — is the container running?" >&2
    exit 2
fi

while IFS= read -r line || [[ -n "$line" ]]; do
    # Skip blanks + comments.
    line="${line%%#*}"
    line="$(echo -n "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
    [[ -z "$line" ]] && continue

    total=$((total + 1))
    basename_raw="$(basename "${line%%\?*}")"
    basename_safe="${basename_raw%.*}"
    out_path="${TALKIES_OUTDIR}/${basename_safe}.${ext}"

    form_args=(
        -F "model=${TALKIES_MODEL}"
        -F "response_format=${TALKIES_FORMAT}"
    )
    [[ -n "${TALKIES_LANGUAGE:-}" ]] && form_args+=(-F "language=${TALKIES_LANGUAGE}")
    [[ -n "${TALKIES_DIARIZE:-}" ]] && form_args+=(-F "diarization=${TALKIES_DIARIZE}")

    if [[ "$line" =~ ^https?:// ]]; then
        form_args+=(-F "file_path=${line}")
        echo "[talkies] URL → ${out_path}: ${line}"
    else
        if [[ ! -f "$line" ]]; then
            echo "[talkies] SKIP (missing local file): ${line}" >&2
            fail=$((fail + 1))
            continue
        fi
        form_args+=(-F "file=@${line}")
        echo "[talkies] FILE → ${out_path}: ${line}"
    fi

    http_code="$(
        curl -s -o "$out_path" -w '%{http_code}' \
            "${auth_args[@]}" \
            "${form_args[@]}" \
            "${TALKIES_URL}/v1/audio/transcriptions" \
            || echo "000"
    )"

    if [[ "$http_code" == "200" ]]; then
        ok=$((ok + 1))
        continue
    fi

    echo "[talkies] FAIL ($http_code) for ${line}:" >&2
    cat "$out_path" >&2 || true
    echo >&2
    rm -f "$out_path"
    fail=$((fail + 1))
done < "$inputs_file"

echo "[talkies] done — ${ok}/${total} succeeded, ${fail} failed"
[[ $fail -eq 0 ]] || exit 1
