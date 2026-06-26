#!/usr/bin/env bash
# shellbot-creative-studio — Remotion render
# Usage: remotion_render --project <dir> [--composition <id>] [--output <path>]
#                        [--codec h264|h265] [--crf 18|23] [--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/config.sh"
source "${SCRIPT_DIR}/lib/output.sh"

PROJECT=""
COMPOSITION=""
OUTPUT=""
CODEC="h264"
CRF=18
DRY_RUN=false

usage() {
  cat >&2 <<'EOF'
Usage: remotion_render --project <dir> [options]

Options:
  --project      Remotion project directory (required)
  --composition  Composition ID to render (auto-detected if omitted)
  --output       Output file path (default: out/<composition>.mp4)
  --codec        Video codec: h264, h265 (default: h264)
  --crf          Quality (lower=better): 0-51 (default: 18)
  --dry-run      Show the command without executing
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)     PROJECT="$2"; shift 2 ;;
    --composition) COMPOSITION="$2"; shift 2 ;;
    --output)      OUTPUT="$2"; shift 2 ;;
    --codec)       CODEC="$2"; shift 2 ;;
    --crf)         CRF="$2"; shift 2 ;;
    --dry-run)     DRY_RUN=true; shift ;;
    -h|--help)     usage; exit 0 ;;
    *)             log_error "Unknown option: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$PROJECT" ]]; then
  log_error "--project is required"
  usage
  exit 1
fi

if [[ ! -d "$PROJECT" ]]; then
  log_error "Project directory not found: ${PROJECT}"
  exit 1
fi

# Auto-detect composition if not specified
if [[ -z "$COMPOSITION" ]]; then
  # Try to get it from the render script in package.json
  COMPOSITION=$(cd "$PROJECT" && node -e "
    const pkg = require('./package.json');
    const render = pkg.scripts?.render || '';
    const parts = render.split(' ');
    const idx = parts.indexOf('src/index.ts');
    if (idx >= 0 && parts[idx+1]) console.log(parts[idx+1]);
  " 2>/dev/null || true)

  if [[ -z "$COMPOSITION" ]]; then
    # Try listing compositions
    COMPOSITION=$(cd "$PROJECT" && npx remotion compositions src/index.ts --quiet 2>/dev/null | head -1 || true)
  fi

  if [[ -z "$COMPOSITION" ]]; then
    log_error "Could not auto-detect composition. Use --composition to specify."
    exit 1
  fi

  log_info "Auto-detected composition: ${COMPOSITION}"
fi

OUTPUT="${OUTPUT:-${PROJECT}/out/${COMPOSITION}.mp4}"

local_cmd="cd '${PROJECT}' && npx remotion render src/index.ts '${COMPOSITION}' '${OUTPUT}' --codec=${CODEC} --pixel-format=yuv420p --crf=${CRF}"

if [[ "$DRY_RUN" == "true" ]]; then
  json_output "$(json_build command="$local_cmd" composition="$COMPOSITION" output="$OUTPUT" dry_run=true)"
  exit 0
fi

log_info "Rendering ${COMPOSITION} → ${OUTPUT}"
log_info "Codec: ${CODEC}, CRF: ${CRF}"

mkdir -p "$(dirname "$OUTPUT")"

(cd "$PROJECT" && npx remotion render src/index.ts "$COMPOSITION" "$OUTPUT" \
  --codec="$CODEC" \
  --pixel-format=yuv420p \
  --crf="$CRF")

if [[ -f "$OUTPUT" ]]; then
  local size
  size=$(ls -lh "$OUTPUT" | awk '{print $5}')
  log_ok "Rendered: ${OUTPUT} (${size})"
  json_output "$(json_build status=completed composition="$COMPOSITION" output="$OUTPUT" size="$size")"
else
  json_error "Render failed — no output file at ${OUTPUT}"
fi
