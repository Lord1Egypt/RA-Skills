#!/bin/bash
# Create Hermes cron jobs for X posting and/or X mutual-follow engagement.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_NAME="zeelin-social-autopublisher"
SKILL_ROOT="${OPENCLAW_SKILLS_ROOT:-$HOME/.openclaw/workspace/skills}"
POST_SCHEDULE=""
ENGAGE_SCHEDULE=""
DELIVER="origin"
POST_NAME=""
ENGAGE_NAME=""
QUERY='("follow back" OR "follow for follow" OR f4f OR "mutual follow") (AI OR founder OR builder OR startup)'
TOPIC_HINT="Latest AI hotspot with strong opinion"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/create_hermes_x_growth_cron.sh --post-schedule "0 10 * * *" --engage-schedule "0 15 * * *" [options]

Options:
  --post-schedule TEXT     Schedule for AI hotspot posting job
  --engage-schedule TEXT   Schedule for mutual-follow reply job
  --query TEXT             Search query for reply job
  --topic-hint TEXT        Topic hint for posting job
  --deliver TARGET         Delivery target, default origin
  --post-name TEXT         Custom post job name
  --engage-name TEXT       Custom engage job name
  --help                   Show help
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --post-schedule)
      POST_SCHEDULE="${2:-}"
      shift 2
      ;;
    --engage-schedule)
      ENGAGE_SCHEDULE="${2:-}"
      shift 2
      ;;
    --query)
      QUERY="${2:-}"
      shift 2
      ;;
    --topic-hint)
      TOPIC_HINT="${2:-}"
      shift 2
      ;;
    --deliver)
      DELIVER="${2:-}"
      shift 2
      ;;
    --post-name)
      POST_NAME="${2:-}"
      shift 2
      ;;
    --engage-name)
      ENGAGE_NAME="${2:-}"
      shift 2
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

if [ -z "${POST_SCHEDULE}" ] && [ -z "${ENGAGE_SCHEDULE}" ]; then
  echo "ERROR: at least one of --post-schedule or --engage-schedule is required" >&2
  exit 2
fi

if [ -z "${POST_NAME}" ]; then
  POST_NAME="X AI hotspot posting"
fi
if [ -z "${ENGAGE_NAME}" ]; then
  ENGAGE_NAME="X mutual-follow engagement"
fi

if [ -n "${POST_SCHEDULE}" ]; then
  hermes cron create "${POST_SCHEDULE}" "Use the ${SKILL_NAME} skill.

Before posting, gather at least 2 current AI news signals from the web or browser results.
Compress them into one strong X topic with a clear judgment.

Run this script:
${SCRIPT_DIR}/run_x_growth_ops.sh

Arguments:
--topic \"${TOPIC_HINT}\"
--post-only

Requirements:
- Post to X/Twitter only
- Avoid short copy; write a dense single post with a hook, 2-3 concrete signals, and a forward-looking judgment
- Return the run directory path
- Summarize whether the X post succeeded
" --name "${POST_NAME}" --deliver "${DELIVER}" --skill "${SKILL_NAME}"
fi

if [ -n "${ENGAGE_SCHEDULE}" ]; then
  hermes cron create "${ENGAGE_SCHEDULE}" "Use local Chrome/CDP-based X automation, not the official API.

Run this script:
${SCRIPT_DIR}/run_x_growth_ops.sh

Arguments:
--reply-only
--reply-limit 8
--reply-query \"${QUERY}\"

Requirements:
- Search X/Twitter for mutual-follow / follow-back style posts
- Reply in English only
- Keep replies friendly and slightly varied, not copy-pasted word-for-word every time
- Do not exceed 8 replies in one run
- Summarize how many replies succeeded vs failed
- If login is missing, say that X needs relogin in the visible Chrome profile
" --name "${ENGAGE_NAME}" --deliver "${DELIVER}" --skill "${SKILL_NAME}"
fi
