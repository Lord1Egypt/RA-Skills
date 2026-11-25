#!/usr/bin/env bash
# Submit one Zooop AI task. Prints the JSON response from POST /v1/tasks.
#
# Three modes:
#   submit.sh <interfaceId> <versionId> '<params-json>'
#   submit.sh --ai-tool  <slug>         '<params-json>'
#   submit.sh --template <slug>         '<params-json>'
#
# Examples:
#   submit.sh d2c0... pro '{"prompt":"a red panda eating noodles","aspect_ratio":"1:1"}'
#   submit.sh --ai-tool background-removal '{"image_url":"https://storage.zooop.ai/…"}'
#   submit.sh --template superhero-movie-poster '{"image_urls":["https://storage.zooop.ai/…"],"hero_name":"DAFU"}'
#
# Discover identifiers via:
#   GET /v1/models?type=<type>&subtype=<subType>     (raw path)
#   GET /v1/ai-tools[?type=image|video]              (curated tools)
#   GET /v1/templates[?type=image|video]             (gallery templates)
#
# Timeout / duplicate safety: a submit can succeed server-side (task created,
# credits charged) yet still time out before the JSON reaches you — cold
# starts + media probing + workflow dispatch run synchronously, so the FIRST
# submit of a session is the slowest. This script attaches an Idempotency-Key
# so a retry returns the ORIGINAL taskId instead of creating a duplicate. The
# default key is sha256(body), so the safe recovery from a timeout is to
# **re-run the identical command** (same args, same params) — do NOT tweak the
# params to "avoid a duplicate", that changes the hash and defeats the dedup.
# Set ZOOOP_IDEMPOTENCY_KEY to force a specific key (e.g. a unique value per
# submission when you intentionally want N tasks from identical params).
set -euo pipefail

: "${ZOOOP_API_KEY:?ZOOOP_API_KEY must be set — visit https://zooop.ai/user?tab=apiKeys to create one}"
HOST="${ZOOOP_API_HOST:-https://api.zooop.ai}"

if [[ ${1:-} == "--ai-tool" ]]; then
  if [[ $# -lt 3 ]]; then
    echo "usage: $0 --ai-tool <slug> <params-json>" >&2
    exit 64
  fi
  SLUG="$2"
  PARAMS="$3"
  BODY=$(printf '{"aiTool":"%s","params":%s}' "$SLUG" "$PARAMS")
elif [[ ${1:-} == "--template" ]]; then
  if [[ $# -lt 3 ]]; then
    echo "usage: $0 --template <slug> <params-json>" >&2
    exit 64
  fi
  SLUG="$2"
  PARAMS="$3"
  BODY=$(printf '{"template":"%s","params":%s}' "$SLUG" "$PARAMS")
else
  if [[ $# -lt 3 ]]; then
    echo "usage: $0 <interfaceId> <versionId> <params-json>" >&2
    echo "       $0 --ai-tool <slug> <params-json>" >&2
    echo "       $0 --template <slug> <params-json>" >&2
    exit 64
  fi
  INTERFACE_ID="$1"
  VERSION_ID="$2"
  PARAMS="$3"
  # interfaceId / versionId are caller-supplied identifiers; we wrap them in
  # JSON quotes via printf %s, so embedded quotes in the caller's input would
  # break the JSON — that's a caller mistake, not a security issue (the auth
  # header already gates request submission).
  BODY=$(printf '{"interfaceId":"%s","versionId":"%s","params":%s}' "$INTERFACE_ID" "$VERSION_ID" "$PARAMS")
fi

# Default Idempotency-Key = sha256(body). Deterministic, so a retry of the
# identical submit is short-circuited server-side (returns the first taskId,
# 24h window). Portable across sha256sum / shasum / openssl.
sha256_hex() {
  if command -v sha256sum >/dev/null 2>&1; then
    printf '%s' "$1" | sha256sum | cut -d' ' -f1
  elif command -v shasum >/dev/null 2>&1; then
    printf '%s' "$1" | shasum -a 256 | cut -d' ' -f1
  else
    printf '%s' "$1" | openssl dgst -sha256 | sed 's/^.*= *//'
  fi
}
IDEMPOTENCY_KEY="${ZOOOP_IDEMPOTENCY_KEY:-$(sha256_hex "$BODY")}"

# --max-time caps the WHOLE request so a stalled submit fails cleanly (curl
# exit 28) instead of hanging until an outer command-timeout hard-kills it with
# no exit code and no body. Retrying that clean timeout with the same
# Idempotency-Key is safe. --connect-timeout fails fast on DNS / connect
# issues. Both overridable via env for slow links.
curl -fsS \
  --connect-timeout "${ZOOOP_CONNECT_TIMEOUT:-15}" \
  --max-time "${ZOOOP_SUBMIT_MAX_TIME:-100}" \
  -X POST "$HOST/v1/tasks" \
  -H "Authorization: Bearer $ZOOOP_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $IDEMPOTENCY_KEY" \
  --data "$BODY"
