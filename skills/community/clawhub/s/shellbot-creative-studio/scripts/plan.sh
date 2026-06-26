#!/usr/bin/env bash
# shellbot-creative-studio — creative brief to storyboard
# Usage: plan --brief "..." [--format product-marketing|explainer|social-ad]
#             [--duration 30-120] [--aspect 16:9|9:16] [--fps 30]
#             [--framework aida|general] [--output <path>] [--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/config.sh"
source "${SCRIPT_DIR}/lib/output.sh"

BRIEF=""
FORMAT="product-marketing"
DURATION=45
ASPECT="16:9"
FPS=30
FRAMEWORK="general"
OUTPUT=""
DRY_RUN=false
BRIEF_FILE=""

usage() {
  cat >&2 <<'EOF'
Usage: plan --brief "..." [options]

Options:
  --brief       Creative brief text or JSON (required unless --brief-file)
  --brief-file  Path to brief JSON file
  --format      Output format: product-marketing, explainer, social-ad (default: product-marketing)
  --duration    Target duration in seconds: 15-120 (default: 45)
  --aspect      Aspect ratio: 16:9, 9:16 (default: 16:9)
  --fps         Frames per second: 24, 30, 60 (default: 30)
  --framework   Narrative framework: aida, general (default: general)
  --output      Output file path (.json)
  --dry-run     Show the command without executing
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --brief)      BRIEF="$2"; shift 2 ;;
    --brief-file) BRIEF_FILE="$2"; shift 2 ;;
    --format)     FORMAT="$2"; shift 2 ;;
    --duration)   DURATION="$2"; shift 2 ;;
    --aspect)     ASPECT="$2"; shift 2 ;;
    --fps)        FPS="$2"; shift 2 ;;
    --framework)  FRAMEWORK="$2"; shift 2 ;;
    --output)     OUTPUT="$2"; shift 2 ;;
    --dry-run)    DRY_RUN=true; shift ;;
    -h|--help)    usage; exit 0 ;;
    *)            log_error "Unknown option: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$BRIEF" && -z "$BRIEF_FILE" ]]; then
  log_error "--brief or --brief-file is required"
  usage
  exit 1
fi

PYTHON_DIR="${SCRIPT_DIR}/python"
OUTPUT_FILE="${OUTPUT:-./storyboard.json}"

# If brief is a string (not JSON), wrap it
if [[ -n "$BRIEF" && ! "$BRIEF" =~ ^\{ ]]; then
  # Create a temporary brief JSON
  BRIEF_FILE=$(mktemp /tmp/creative-brief-XXXX.json)
  jq -n --arg brief "$BRIEF" --arg format "$FORMAT" \
    '{brief: $brief, format: $format}' > "$BRIEF_FILE"
  TEMP_BRIEF=true
fi

if [[ "$FRAMEWORK" == "aida" ]]; then
  # Use AIDA-specific planner
  if [[ -n "$BRIEF_FILE" ]]; then
    local_cmd="python3 ${PYTHON_DIR}/brief_to_aida_plan.py --in '${BRIEF_FILE}' --out '${OUTPUT_FILE}' --duration-sec ${DURATION} --fps ${FPS}"
  else
    log_error "AIDA framework requires a structured brief JSON file (--brief-file)"
    log_error "Required fields: product_name, audience, problem, solution, use_cases, cta, incentive"
    exit 1
  fi
else
  # Use general storyboard planner
  local_cmd="python3 ${PYTHON_DIR}/brief_to_storyboard.py --brief '${BRIEF:-$(cat "$BRIEF_FILE")}' --format '${FORMAT}' --duration ${DURATION} --aspect-ratio '${ASPECT}' --out '${OUTPUT_FILE}'"
fi

if [[ "$DRY_RUN" == "true" ]]; then
  json_output "$(json_build command="$local_cmd" framework="$FRAMEWORK" dry_run=true)"
  # Clean up temp file
  [[ "${TEMP_BRIEF:-false}" == "true" ]] && rm -f "$BRIEF_FILE"
  exit 0
fi

log_info "Generating storyboard (${FRAMEWORK} framework)..."

if [[ "$FRAMEWORK" == "aida" ]]; then
  python3 "${PYTHON_DIR}/brief_to_aida_plan.py" \
    --in "$BRIEF_FILE" \
    --out "$OUTPUT_FILE" \
    --duration-sec "$DURATION" \
    --fps "$FPS"
else
  python3 "${PYTHON_DIR}/brief_to_storyboard.py" \
    --brief "${BRIEF:-$(cat "$BRIEF_FILE")}" \
    --format "$FORMAT" \
    --duration "$DURATION" \
    --aspect-ratio "$ASPECT" \
    --out "$OUTPUT_FILE"
fi

# Clean up temp file
[[ "${TEMP_BRIEF:-false}" == "true" ]] && rm -f "$BRIEF_FILE"

if [[ -f "$OUTPUT_FILE" ]]; then
  log_ok "Storyboard saved to ${OUTPUT_FILE}"
  cat "$OUTPUT_FILE"
else
  json_error "Failed to generate storyboard"
fi
