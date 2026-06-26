#!/bin/bash
# Hermes agent wrapper for THUQX social autopublisher.
# This script standardizes workspace paths, dry-run behavior, artifact locations,
# and the JSON payload shape that Hermes should consume.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUNNER="${SCRIPT_DIR}/run_social_ops_v5.sh"

TOPIC=""
MODE="publish"
PLATFORMS="${THUQX_PLATFORMS:-twitter,weibo,xhs,wechat}"
ARTIFACT_DIR="${THUQX_ARTIFACT_DIR:-/tmp/hermes-social-ops}"
CONTENT_JSON=""
JOB_ID="${THUQX_JOB_ID:-}"
MATERIALS_JSON=""
PASS_THROUGH=()

usage() {
  cat <<'EOF'
用法:
  bash scripts/run_hermes_agent_ops.sh --topic "主题" [选项]

选项:
  --topic TEXT              必填，运营主题
  --mode MODE               review | publish，默认 publish
  --platforms LIST          twitter,weibo,xhs,wechat
  --artifact-dir PATH       工件目录，默认 /tmp/hermes-social-ops
  --content-json PATH       复用已审核内容 JSON
  --materials-json PATH     复用或输出参考素材 JSON 路径
  --job-id TEXT             任务标识；默认自动生成
  --help                    显示帮助

其余未知参数会透传给 run_social_ops_v5.sh。
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --topic)
      TOPIC="${2:-}"
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
    --artifact-dir)
      ARTIFACT_DIR="${2:-}"
      shift 2
      ;;
    --content-json)
      CONTENT_JSON="${2:-}"
      shift 2
      ;;
    --materials-json)
      MATERIALS_JSON="${2:-}"
      shift 2
      ;;
    --job-id)
      JOB_ID="${2:-}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      PASS_THROUGH+=("$1")
      shift
      ;;
  esac
done

if [ -z "${TOPIC}" ] && [ -z "${CONTENT_JSON}" ]; then
  echo "ERROR: --topic is required" >&2
  usage >&2
  exit 2
fi

if [ -z "${TOPIC}" ]; then
  TOPIC="reuse-approved-content"
fi

case "${MODE}" in
  review|publish) ;;
  *)
    echo "ERROR: --mode must be review or publish" >&2
    exit 2
    ;;
esac

if [ -z "${JOB_ID}" ]; then
  sanitized="$(printf '%s' "${TOPIC}" | tr ' /' '__' | tr -cd '[:alnum:]_-' | cut -c1-32)"
  ts="$(date +%Y%m%d-%H%M%S)"
  JOB_ID="${ts}-${sanitized:-social-ops}"
fi

RUN_DIR="${ARTIFACT_DIR%/}/${JOB_ID}"
CONTENT_OUT="${RUN_DIR}/content.json"
REPORT_FILE="${RUN_DIR}/report.json"
SUMMARY_FILE="${RUN_DIR}/summary.json"
DEFAULT_MATERIALS_JSON="${RUN_DIR}/materials.json"

mkdir -p "${RUN_DIR}"

RUN_ARGS=(
  --topic "${TOPIC}"
  --platforms "${PLATFORMS}"
  --content-out "${CONTENT_OUT}"
  --materials-out "${MATERIALS_JSON:-${DEFAULT_MATERIALS_JSON}}"
  --report-file "${REPORT_FILE}"
)

if [ "${MODE}" = "review" ]; then
  RUN_ARGS+=(--dry-run)
fi

if [ -n "${CONTENT_JSON}" ]; then
  RUN_ARGS+=(--content-json "${CONTENT_JSON}" --skip-content-gen)
fi

if [ "${#PASS_THROUGH[@]}" -gt 0 ]; then
  RUN_ARGS+=("${PASS_THROUGH[@]}")
fi

bash "${RUNNER}" "${RUN_ARGS[@]}"

python3 - "${SUMMARY_FILE}" "${REPORT_FILE}" "${CONTENT_OUT}" "${MATERIALS_JSON:-${DEFAULT_MATERIALS_JSON}}" "${JOB_ID}" "${MODE}" "${RUN_DIR}" "${TOPIC}" <<'PY'
import json
import sys
from pathlib import Path

summary_file, report_file, content_out, materials_out, job_id, mode, run_dir, topic = sys.argv[1:]

report = json.loads(Path(report_file).read_text(encoding="utf-8"))
content = json.loads(Path(content_out).read_text(encoding="utf-8"))
materials_path = Path(materials_out)
materials = []
if materials_path.is_file():
    try:
        materials = json.loads(materials_path.read_text(encoding="utf-8"))
    except Exception:
        materials = []

failed_platforms = [item["platform"] for item in report.get("results", []) if item.get("status") == "failed"]
dry_run_platforms = [item["platform"] for item in report.get("results", []) if item.get("status") == "dry_run"]

summary = {
    "job_id": job_id,
    "mode": mode,
    "topic": topic,
    "run_dir": run_dir,
    "artifacts": {
        "report": report_file,
        "content": content_out,
        "materials": str(materials_path) if materials_path.is_file() else None,
    },
    "ok": report.get("ok", False),
    "next_action": (
        "human_review_content_then_publish"
        if mode == "review"
        else ("done" if report.get("ok", False) else "inspect_failed_platforms")
    ),
    "human_review_required": mode == "review",
    "platform_status": {
        item["platform"]: item["status"] for item in report.get("results", [])
    },
    "failed_platforms": failed_platforms,
    "dry_run_platforms": dry_run_platforms,
    "materials_count": len(materials),
    "materials_preview": materials[:3],
    "content_preview": {
        "twitter": content.get("twitter", "")[:280],
        "weibo": content.get("weibo", "")[:200],
        "xhs_title": content.get("xhs_title", ""),
        "wechat_title": content.get("wechat_title", ""),
    },
    "quality_hints": {
        "twitter_len": len(content.get("twitter", "")),
        "weibo_len": len(content.get("weibo", "")),
        "xhs_title_len": len(content.get("xhs_title", "")),
        "wechat_body_len": len(content.get("wechat_body", "")),
    },
}

Path(summary_file).write_text(json.dumps(summary, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False))
PY
