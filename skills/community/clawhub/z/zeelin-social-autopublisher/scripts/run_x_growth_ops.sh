#!/bin/bash
# Hermes-ready X growth workflow:
# 1) publish one X post around latest AI topic
# 2) reply in English to up to N mutual-follow / follow-back tweets
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_ROOT="${OPENCLAW_SKILLS_ROOT:-$HOME/.openclaw/workspace/skills}"
POST_RUNNER="${SCRIPT_DIR}/run_hermes_agent_ops.sh"
REPLY_SCRIPT="${SKILLS_ROOT}/zeelin-twitter-web-autopost/scripts/cdp_reply_search_results.py"

TOPIC="${TOPIC:-}"
POST_MODE="${POST_MODE:-publish}"
DO_POST=1
DO_REPLY=1
REPLY_QUERY="${REPLY_QUERY:-(\"follow back\" OR \"follow for follow\" OR f4f OR \"mutual follow\") (AI OR founder OR builder OR startup)}"
REPLY_LIMIT="${REPLY_LIMIT:-8}"
DRY_RUN=0
CONTENT_JSON="${CONTENT_JSON:-}"
ARTIFACT_DIR="${THUQX_ARTIFACT_DIR:-/tmp/hermes-social-ops}"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/run_x_growth_ops.sh --topic "Latest AI infra shift" [options]

Options:
  --topic TEXT           Topic for the X post
  --post-mode MODE       review | publish (default: publish)
  --post-only            Only publish the X post
  --reply-only           Only run mutual-follow replies
  --reply-query TEXT     Search query for growth replies
  --reply-limit N        Number of replies per run (default: 8)
  --content-json PATH    Reuse approved content.json for post publishing
  --dry-run              Do not publish or reply; generate plans only
  --help                 Show help
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --topic)
      TOPIC="${2:-}"
      shift 2
      ;;
    --post-mode)
      POST_MODE="${2:-}"
      shift 2
      ;;
    --post-only)
      DO_REPLY=0
      shift
      ;;
    --reply-only)
      DO_POST=0
      shift
      ;;
    --reply-query)
      REPLY_QUERY="${2:-}"
      shift 2
      ;;
    --reply-limit)
      REPLY_LIMIT="${2:-8}"
      shift 2
      ;;
    --content-json)
      CONTENT_JSON="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [ "${DO_POST}" = "1" ] && [ -z "${TOPIC}" ] && [ -z "${CONTENT_JSON}" ]; then
  echo "ERROR: --topic is required unless --reply-only or --content-json is provided" >&2
  exit 2
fi

if [ ! -f "${REPLY_SCRIPT}" ]; then
  echo "ERROR: Missing reply script: ${REPLY_SCRIPT}" >&2
  exit 1
fi

if [ "${DRY_RUN}" = "1" ]; then
  POST_MODE="review"
fi

if [ "${DO_POST}" = "1" ]; then
  POST_ARGS=(
    --topic "${TOPIC:-AI latest hotspot}"
    --mode "${POST_MODE}"
    --platforms twitter
    --artifact-dir "${ARTIFACT_DIR}"
  )
  if [ -n "${CONTENT_JSON}" ]; then
    POST_ARGS+=(--content-json "${CONTENT_JSON}")
  fi
  echo "[X Growth] Running X post workflow..."
  bash "${POST_RUNNER}" "${POST_ARGS[@]}"
fi

if [ "${DO_REPLY}" = "1" ]; then
  echo "[X Growth] Running English mutual-follow replies..."
  REPLY_ARGS=(
    --query "${REPLY_QUERY}"
    --limit "${REPLY_LIMIT}"
  )
  if [ "${DRY_RUN}" = "1" ]; then
    REPLY_ARGS+=(--dry-run)
  fi
  python3 "${REPLY_SCRIPT}" "${REPLY_ARGS[@]}"
fi
