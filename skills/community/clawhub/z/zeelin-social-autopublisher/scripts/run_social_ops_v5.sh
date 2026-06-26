#!/bin/bash
# THUQX AutoOps for OpenClaw 0.5 — 四平台一键运营
# 兼容旧用法: bash scripts/run_social_ops_v5.sh "主题"
# Hermes / agent 推荐用法:
#   bash scripts/run_social_ops_v5.sh --topic "主题" --platforms twitter,weibo --dry-run --report-file /tmp/report.json
# 环境变量:
#   OPENCLAW_CDP_PORT, THUQX_PLATFORM_PAUSE, THUQX_CONTENT_JSON, THUQX_CONTENT_OUT,
#   THUQX_REPORT_FILE, THUQX_CONTINUE_ON_ERROR, THUQX_SKIP_CDP_CHECK
set -euo pipefail

SKILLS_BASE="${OPENCLAW_SKILLS_ROOT:-$HOME/.openclaw/workspace/skills}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/_thuqx_cdp_common.sh"

BASE_PAUSE="${THUQX_PLATFORM_PAUSE:-2}"
TOPIC=""
PLATFORMS_RAW="${THUQX_PLATFORMS:-twitter,weibo,xhs,wechat}"
DRY_RUN=0
SKIP_GEN=0
NO_CDP_CHECK="${THUQX_SKIP_CDP_CHECK:-0}"
CONTENT_JSON="${THUQX_CONTENT_JSON:-}"
CONTENT_OUT="${THUQX_CONTENT_OUT:-}"
MATERIALS_OUT="${THUQX_MATERIALS_OUT:-}"
REPORT_FILE="${THUQX_REPORT_FILE:-}"
CONTINUE_ON_ERROR="${THUQX_CONTINUE_ON_ERROR:-1}"

usage() {
  cat <<'EOF'
用法:
  bash scripts/run_social_ops_v5.sh "主题"
  bash scripts/run_social_ops_v5.sh --topic "主题" [选项]

选项:
  --topic TEXT              运营主题
  --platforms LIST          平台列表: twitter,weibo,xhs,wechat
  --content-json PATH       使用已有 JSON，跳过内容生成
  --content-out PATH        将生成/读取到的最终内容 JSON 落盘
  --materials-out PATH      将抓取到的参考素材 JSON 落盘
  --report-file PATH        输出结构化执行报告 JSON
  --dry-run                 只生成内容与报告，不真正发帖
  --skip-content-gen        强制跳过内容生成，需配合 --content-json
  --continue-on-error       默认行为；单平台失败继续跑后续平台
  --fail-fast               任一平台失败即退出
  --no-cdp-check            跳过 Chrome CDP 检查
  --help                    显示帮助

环境变量:
  THUQX_CONTENT_JSON, THUQX_CONTENT_OUT, THUQX_REPORT_FILE,
  THUQX_MATERIALS_OUT, THUQX_PLATFORM_PAUSE, THUQX_CONTINUE_ON_ERROR, THUQX_SKIP_CDP_CHECK
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --topic)
      TOPIC="${2:-}"
      shift 2
      ;;
    --platforms)
      PLATFORMS_RAW="${2:-}"
      shift 2
      ;;
    --content-json)
      CONTENT_JSON="${2:-}"
      shift 2
      ;;
    --content-out)
      CONTENT_OUT="${2:-}"
      shift 2
      ;;
    --materials-out)
      MATERIALS_OUT="${2:-}"
      shift 2
      ;;
    --report-file)
      REPORT_FILE="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --skip-content-gen)
      SKIP_GEN=1
      shift
      ;;
    --continue-on-error)
      CONTINUE_ON_ERROR=1
      shift
      ;;
    --fail-fast)
      CONTINUE_ON_ERROR=0
      shift
      ;;
    --no-cdp-check)
      NO_CDP_CHECK=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    --*)
      echo "ERROR: Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [ -z "${TOPIC}" ]; then
        TOPIC="$1"
        shift
      else
        echo "ERROR: Unexpected argument: $1" >&2
        usage >&2
        exit 2
      fi
      ;;
  esac
done

TOPIC="${TOPIC:-AI认知债务}"

normalize_platforms() {
  python3 - "$PLATFORMS_RAW" <<'PY'
import sys

aliases = {
    "twitter": "twitter",
    "x": "twitter",
    "weibo": "weibo",
    "wb": "weibo",
    "xhs": "xhs",
    "xiaohongshu": "xhs",
    "rednote": "xhs",
    "wechat": "wechat",
    "weixin": "wechat",
}

raw = sys.argv[1]
items = []
seen = set()
for part in raw.replace(" ", ",").split(","):
    token = part.strip().lower()
    if not token:
        continue
    if token not in aliases:
        print(token)
        sys.exit(1)
    normalized = aliases[token]
    if normalized not in seen:
        seen.add(normalized)
        items.append(normalized)

if not items:
    print("EMPTY")
    sys.exit(1)

print(",".join(items))
PY
}

if ! PLATFORMS="$(normalize_platforms)"; then
  echo "ERROR: Invalid --platforms value: ${PLATFORMS_RAW}" >&2
  exit 2
fi

if [ "${SKIP_GEN}" = "1" ] && [ -z "${CONTENT_JSON}" ]; then
  echo "ERROR: --skip-content-gen requires --content-json PATH" >&2
  exit 2
fi

if [ "${NO_CDP_CHECK}" != "1" ] && [ "${DRY_RUN}" != "1" ]; then
  thuqx_ensure_cdp
fi

if [ -n "${CONTENT_JSON}" ] && [ -f "${CONTENT_JSON}" ]; then
  echo "Using pre-generated JSON: ${CONTENT_JSON}"
  CONTENT="$(cat "${CONTENT_JSON}")"
else
  echo "Generating content for topic: ${TOPIC}"
  GEN_ARGS=(--topic "$TOPIC")
  if [ -n "${CONTENT_OUT}" ]; then
    GEN_ARGS+=(--output "${CONTENT_OUT}")
  fi
  if [ -n "${MATERIALS_OUT}" ]; then
    GEN_ARGS+=(--materials-output "${MATERIALS_OUT}")
  fi
  CONTENT="$(python3 "$SCRIPT_DIR/generate_content.py" "${GEN_ARGS[@]}")"
fi

if [ -z "$CONTENT" ]; then
  echo "ERROR: Content generation failed." >&2
  exit 1
fi

if ! CONTENT="$(printf '%s' "$CONTENT" | python3 -c '
import json
import re
import sys

required = ("twitter", "weibo", "xhs_title", "xhs_body", "wechat_title", "wechat_body")
bad_phrase = re.compile(r"Auto\s*Ops|自动发布|本推文由|本文由|本条由", re.I)

try:
    data = json.load(sys.stdin)
except Exception as exc:
    print(f"invalid json: {exc}", file=sys.stderr)
    sys.exit(1)

if not isinstance(data, dict):
    print("content must be a JSON object", file=sys.stderr)
    sys.exit(1)

for key in required:
    if key not in data or not str(data[key]).strip():
        print(f"missing or empty key: {key}", file=sys.stderr)
        sys.exit(1)
    value = bad_phrase.sub("", str(data[key])).strip()
    value = re.sub(r"\n{3,}", "\n\n", value)
    data[key] = value

checks = [
    ("twitter", len(data["twitter"]) <= 280, "twitter exceeds 280 chars: {}".format(len(data["twitter"]))),
    ("weibo", 350 <= len(data["weibo"]) <= 900, "weibo length out of range: {}".format(len(data["weibo"]))),
    ("xhs_title", len(data["xhs_title"]) <= 20, "xhs_title too long: {}".format(len(data["xhs_title"]))),
    ("xhs_body", 500 <= len(data["xhs_body"]) <= 1200, "xhs_body length out of range: {}".format(len(data["xhs_body"]))),
    ("wechat_title", len(data["wechat_title"]) <= 32, "wechat_title too long: {}".format(len(data["wechat_title"]))),
    ("wechat_body", len(data["wechat_body"]) >= 1200, "wechat_body too short: {}".format(len(data["wechat_body"]))),
]
for _, ok, reason in checks:
    if not ok:
        print(reason, file=sys.stderr)
        sys.exit(1)

print(json.dumps(data, ensure_ascii=False))
')"; then
  echo "ERROR: content JSON failed platform-level validation." >&2
  exit 1
fi

if [ -n "${CONTENT_OUT}" ]; then
  mkdir -p "$(dirname "${CONTENT_OUT}")"
  printf '%s\n' "$CONTENT" > "${CONTENT_OUT}"
fi

extract() { echo "$CONTENT" | python3 -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }

TW="$(extract twitter)"
WB="$(extract weibo)"
XT="$(extract xhs_title)"
XB="$(extract xhs_body)"
WT="$(extract wechat_title)"
WBODY="$(extract wechat_body)"

echo ""
echo "========== THUQX 四平台顺序运营 =========="
echo "Twitter → 微博 → 小红书 → 微信公众号(草稿)"
echo "========================================="
echo ""

FAIL=0
STARTED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
RESULTS_TMP="$(mktemp)"
cleanup() {
  rm -f "${RESULTS_TMP}"
}
trap cleanup EXIT

sleep_jitter() {
  [ "${DRY_RUN}" = "1" ] && return 0
  local extra=$((RANDOM % 7))
  sleep $((BASE_PAUSE + extra))
}

record_result() {
  local platform="$1"
  local status="$2"
  local exit_code="$3"
  printf '%s\t%s\t%s\n' "${platform}" "${status}" "${exit_code}" >> "${RESULTS_TMP}"
}

check_dependency() {
  local target="$1"
  if [ ! -e "${target}" ]; then
    echo "ERROR: Missing dependency: ${target}" >&2
    return 1
  fi
}

run_platform() {
  local order="$1"
  local platform="$2"
  local label="$3"
  local prefix="$4"
  shift 4

  echo "[${order}] ${label}..."

  if [ "${DRY_RUN}" = "1" ]; then
    echo "  [${prefix}] dry-run: skipped publish"
    record_result "${platform}" "dry_run" 0
    sleep_jitter
    return 0
  fi

  set +e
  "$@" 2>&1 | sed "s/^/  [${prefix}] /"
  local status=${PIPESTATUS[0]}
  set -e

  if [ "${status}" -eq 0 ]; then
    record_result "${platform}" "success" "${status}"
  else
    record_result "${platform}" "failed" "${status}"
    FAIL=$((FAIL + 1))
    if [ "${CONTINUE_ON_ERROR}" != "1" ]; then
      echo "ERROR: ${platform} failed with exit code ${status}; aborting due to --fail-fast." >&2
      exit "${status}"
    fi
  fi

  sleep_jitter
}

should_run() {
  local wanted="$1"
  case ",${PLATFORMS}," in
    *,"${wanted}",*) return 0 ;;
    *) return 1 ;;
  esac
}

if should_run twitter; then
  check_dependency "$SKILLS_BASE/zeelin-twitter-web-autopost/scripts/tweet.sh"
  run_platform "1/4" "twitter" "Twitter Ops" "Twitter" \
    bash "$SKILLS_BASE/zeelin-twitter-web-autopost/scripts/tweet.sh" "$TW"
else
  record_result "twitter" "skipped" 0
fi

if should_run weibo; then
  check_dependency "$SKILLS_BASE/zeelin-weibo-autopost/scripts/run_weibo_ops.sh"
  run_platform "2/4" "weibo" "Weibo Ops" "Weibo" \
    bash "$SKILLS_BASE/zeelin-weibo-autopost/scripts/run_weibo_ops.sh" "$WB"
else
  record_result "weibo" "skipped" 0
fi

if should_run xhs; then
  check_dependency "$SKILLS_BASE/zeelin-xiaohongshu-autopost/scripts/cdp_xhs_publish_v5.py"
  run_platform "3/4" "xhs" "Xiaohongshu Ops" "XHS" \
    python3 "$SKILLS_BASE/zeelin-xiaohongshu-autopost/scripts/cdp_xhs_publish_v5.py" "$XT" "$XB"
else
  record_result "xhs" "skipped" 0
fi

if should_run wechat; then
  check_dependency "$SKILLS_BASE/zeelin-wechat-autopost/scripts/cdp_wechat_publish_v10.py"
  run_platform "4/4" "wechat" "WeChat Ops (draft)" "WeChat" \
    python3 "$SKILLS_BASE/zeelin-wechat-autopost/scripts/cdp_wechat_publish_v10.py" "$WT" "$WBODY"
else
  record_result "wechat" "skipped" 0
fi

if [ -n "${REPORT_FILE}" ]; then
  mkdir -p "$(dirname "${REPORT_FILE}")"
fi

REPORT_JSON="$(python3 - "${RESULTS_TMP}" "${TOPIC}" "${PLATFORMS}" "${DRY_RUN}" "${CONTENT_OUT}" "${MATERIALS_OUT}" "${STARTED_AT}" <<'PY'
import json
import sys
from datetime import datetime, timezone

results_path, topic, platforms, dry_run, content_out, materials_out, started_at = sys.argv[1:]
results = []
with open(results_path, "r", encoding="utf-8") as fh:
    for line in fh:
        platform, status, exit_code = line.rstrip("\n").split("\t")
        results.append(
            {
                "platform": platform,
                "status": status,
                "exit_code": int(exit_code),
            }
        )

payload = {
    "topic": topic,
    "requested_platforms": [p for p in platforms.split(",") if p],
    "dry_run": dry_run == "1",
    "started_at": started_at,
    "finished_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "content_output": content_out or None,
    "materials_output": materials_out or None,
    "results": results,
}
payload["ok"] = all(item["status"] in {"success", "skipped", "dry_run"} for item in results)
print(json.dumps(payload, ensure_ascii=False))
PY
)"

if [ -n "${REPORT_FILE}" ]; then
  printf '%s\n' "${REPORT_JSON}" > "${REPORT_FILE}"
fi

echo ""
echo "========================================="
if [ "$FAIL" -eq 0 ]; then
  echo "All 4 platforms Ops finished successfully."
else
  echo "WARNING: $FAIL platform(s) may need a manual check."
fi
echo "========================================="
echo "${REPORT_JSON}"

[ "$FAIL" -gt 0 ] && exit 1
exit 0
