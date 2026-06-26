#!/bin/bash
# Create a Hermes cron job for the social autopublisher skill.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_NAME="zeelin-social-autopublisher"

TOPIC=""
SCHEDULE=""
MODE="review"
PLATFORMS="twitter,weibo,xhs,wechat"
DELIVER="local"
NAME=""

usage() {
  cat <<'EOF'
用法:
  bash scripts/create_hermes_social_cron.sh --topic "主题" --schedule "every 1d" [选项]

选项:
  --topic TEXT         必填，运营主题
  --schedule TEXT      必填，cron 表达式或自然语言频率
  --mode MODE          review | publish，默认 review
  --platforms LIST     twitter,weibo,xhs,wechat
  --deliver TARGET     默认 local；也可用 origin、telegram、discord 等
  --name TEXT          自定义任务名
  --help               显示帮助
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --topic)
      TOPIC="${2:-}"
      shift 2
      ;;
    --schedule)
      SCHEDULE="${2:-}"
      shift 2
      ;;
    --mode)
      MODE="${2:-}"
      shift 2
      ;;
    --platforms)
      PLATFORMS="${2:-}"
      shift 2
      ;;
    --deliver)
      DELIVER="${2:-}"
      shift 2
      ;;
    --name)
      NAME="${2:-}"
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

if [ -z "${TOPIC}" ] || [ -z "${SCHEDULE}" ]; then
  echo "ERROR: --topic and --schedule are required" >&2
  usage >&2
  exit 2
fi

case "${MODE}" in
  review|publish) ;;
  *)
    echo "ERROR: --mode must be review or publish" >&2
    exit 2
    ;;
esac

if [ -z "${NAME}" ]; then
  NAME="Social Ops ${MODE}: ${TOPIC}"
fi

if [ "${MODE}" = "review" ]; then
  PROMPT=$(cat <<EOF
Use the ${SKILL_NAME} skill.

Run the wrapper script at:
${SCRIPT_DIR}/run_hermes_agent_ops.sh

Task:
- topic: ${TOPIC}
- mode: review
- platforms: ${PLATFORMS}

Requirements:
- Generate content artifacts only; do not publish.
- Return the run directory path.
- Read summary.json and report the next_action field.
- If content is template fallback, explicitly ask for human review before publish.
EOF
)
else
  PROMPT=$(cat <<EOF
Use the ${SKILL_NAME} skill.

Run the wrapper script at:
${SCRIPT_DIR}/run_hermes_agent_ops.sh

Task:
- topic: ${TOPIC}
- mode: publish
- platforms: ${PLATFORMS}

Requirements:
- Publish sequentially, not in parallel.
- Return the run directory path.
- Read report.json and summarize per-platform success/failure.
- If any platform fails, identify the manual follow-up needed.
EOF
)
fi

echo "Creating Hermes cron job:"
echo "  Name: ${NAME}"
echo "  Schedule: ${SCHEDULE}"
echo "  Deliver: ${DELIVER}"
echo "  Skill: ${SKILL_NAME}"
echo ""

hermes cron create "${SCHEDULE}" "${PROMPT}" \
  --name "${NAME}" \
  --deliver "${DELIVER}" \
  --skill "${SKILL_NAME}"
