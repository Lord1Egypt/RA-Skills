#!/usr/bin/env bash
# shellbot-creative-studio — end-to-end production pipeline
# Usage: pipeline --brief <json_or_string> [--template cinematic-product-16x9]
#                 [--output-dir ./creative-output] [--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/config.sh"
source "${SCRIPT_DIR}/lib/output.sh"
source "${SCRIPT_DIR}/lib/provider_router.sh"

BRIEF=""
BRIEF_FILE=""
TEMPLATE="aida-classic-16x9"
OUTPUT_DIR="./creative-output"
FRAMEWORK="general"
DURATION=45
ASPECT="16:9"
FPS=30
DRY_RUN=false
SKIP_RENDER=false

usage() {
  cat >&2 <<'EOF'
Usage: pipeline --brief "..." [options]

End-to-end creative production pipeline:
  1. Generate storyboard from brief
  2. Generate visual assets for each scene
  3. Upscale hero images
  4. Generate video clips for hero scenes
  5. Generate voiceover per scene
  6. Generate background music
  7. Bootstrap Remotion project
  8. Render final video

Options:
  --brief        Creative brief text or JSON (required unless --brief-file)
  --brief-file   Path to brief JSON file
  --template     Remotion template (default: aida-classic-16x9)
  --output-dir   Output directory (default: ./creative-output)
  --framework    Narrative framework: aida, general (default: general)
  --duration     Target duration in seconds (default: 45)
  --aspect       Aspect ratio: 16:9, 9:16 (default: 16:9)
  --fps          Frames per second (default: 30)
  --skip-render  Stop before Remotion render (useful for review)
  --dry-run      Show all commands without executing
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --brief)       BRIEF="$2"; shift 2 ;;
    --brief-file)  BRIEF_FILE="$2"; shift 2 ;;
    --template)    TEMPLATE="$2"; shift 2 ;;
    --output-dir)  OUTPUT_DIR="$2"; shift 2 ;;
    --framework)   FRAMEWORK="$2"; shift 2 ;;
    --duration)    DURATION="$2"; shift 2 ;;
    --aspect)      ASPECT="$2"; shift 2 ;;
    --fps)         FPS="$2"; shift 2 ;;
    --skip-render) SKIP_RENDER=true; shift ;;
    --dry-run)     DRY_RUN=true; shift ;;
    -h|--help)     usage; exit 0 ;;
    *)             log_error "Unknown option: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$BRIEF" && -z "$BRIEF_FILE" ]]; then
  log_error "--brief or --brief-file is required"
  usage
  exit 1
fi

export CREATIVE_OUTPUT_DIR="$OUTPUT_DIR"
ensure_output_dirs "$OUTPUT_DIR"

DRY_FLAG=""
if [[ "$DRY_RUN" == "true" ]]; then
  DRY_FLAG="--dry-run"
fi

log_info "========================================"
log_info "  Creative Studio Pipeline"
log_info "  Template: ${TEMPLATE}"
log_info "  Output:   ${OUTPUT_DIR}"
log_info "========================================"

# ─── Step 1: Generate storyboard ────────────────────────────────────────────
log_info ""
log_info "STEP 1/7: Generating storyboard..."

PLAN_ARGS=(--duration "$DURATION" --aspect "$ASPECT" --fps "$FPS" --framework "$FRAMEWORK" --output "${OUTPUT_DIR}/manifests/storyboard.json")

if [[ -n "$BRIEF_FILE" ]]; then
  PLAN_ARGS+=(--brief-file "$BRIEF_FILE")
else
  PLAN_ARGS+=(--brief "$BRIEF")
fi

bash "${SCRIPT_DIR}/plan.sh" "${PLAN_ARGS[@]}" $DRY_FLAG > "${OUTPUT_DIR}/manifests/plan-output.json" 2>&1 || true
log_ok "Step 1 complete"

# If dry run, output the plan for all remaining steps
if [[ "$DRY_RUN" == "true" ]]; then
  log_info ""
  log_info "STEP 2/7: Would generate images for each scene"
  log_info "STEP 3/7: Would upscale hero images"
  log_info "STEP 4/7: Would generate video clips for hero scenes"
  log_info "STEP 5/7: Would generate voiceover per scene"
  log_info "STEP 6/7: Would generate background music"
  log_info "STEP 7/7: Would bootstrap Remotion project and render"
  log_info ""

  json_output "$(json_build \
    status=dry_run \
    template="$TEMPLATE" \
    output_dir="$OUTPUT_DIR" \
    steps=7 \
    framework="$FRAMEWORK" \
    duration="$DURATION")"
  exit 0
fi

# ─── Step 2: Generate scene images ──────────────────────────────────────────
log_info ""
log_info "STEP 2/7: Generating scene images..."

STORYBOARD="${OUTPUT_DIR}/manifests/storyboard.json"
if [[ -f "$STORYBOARD" ]]; then
  SCENE_COUNT=$(jq '.scenes | length' "$STORYBOARD" 2>/dev/null || echo 0)

  for i in $(seq 0 $((SCENE_COUNT - 1))); do
    SCENE_ID=$(jq -r ".scenes[$i].id" "$STORYBOARD")
    ASSET_HINT=$(jq -r ".scenes[$i].asset_hint // .scenes[$i].assetHint // .scenes[$i].visual_prompt // empty" "$STORYBOARD")

    if [[ -n "$ASSET_HINT" ]]; then
      log_info "  Scene ${SCENE_ID}: generating image..."
      bash "${SCRIPT_DIR}/image.sh" \
        --prompt "$ASSET_HINT" \
        --size "$ASPECT" \
        --output "${OUTPUT_DIR}/assets/${SCENE_ID}.png" \
        > /dev/null 2>&1 || log_warn "  Failed to generate image for ${SCENE_ID}"
    fi
  done
  log_ok "Step 2 complete (${SCENE_COUNT} scenes)"
else
  log_warn "No storyboard found, skipping image generation"
fi

# ─── Step 3: Upscale hero images ────────────────────────────────────────────
log_info ""
log_info "STEP 3/7: Upscaling hero images..."

# Upscale first and last scene images (attention + CTA)
for img in "${OUTPUT_DIR}/assets/"*.png; do
  [[ -f "$img" ]] || continue
  local base
  base=$(basename "$img" .png)
  bash "${SCRIPT_DIR}/edit.sh" \
    --input "$img" \
    --action upscale \
    --scale 2 \
    --output "${OUTPUT_DIR}/assets/${base}-upscaled.png" \
    > /dev/null 2>&1 || log_warn "  Failed to upscale ${base}"
done
log_ok "Step 3 complete"

# ─── Step 4: Generate video clips ───────────────────────────────────────────
log_info ""
log_info "STEP 4/7: Generating video clips for hero scenes..."

if [[ -f "$STORYBOARD" ]]; then
  # Generate video for the first scene (attention-grabber)
  FIRST_ASSET="${OUTPUT_DIR}/assets/$(jq -r '.scenes[0].id' "$STORYBOARD").png"
  FIRST_PROMPT=$(jq -r '.scenes[0].asset_hint // .scenes[0].assetHint // .scenes[0].visual_prompt // "cinematic opening"' "$STORYBOARD")

  if [[ -f "$FIRST_ASSET" ]]; then
    bash "${SCRIPT_DIR}/video.sh" \
      --prompt "$FIRST_PROMPT" \
      --image "$FIRST_ASSET" \
      --duration 5 \
      --aspect "$ASPECT" \
      --output "${OUTPUT_DIR}/scenes/hero-clip.mp4" \
      > /dev/null 2>&1 || log_warn "  Failed to generate hero clip"
  fi
fi
log_ok "Step 4 complete"

# ─── Step 5: Generate voiceover ─────────────────────────────────────────────
log_info ""
log_info "STEP 5/7: Generating voiceover per scene..."

if [[ -f "$STORYBOARD" ]]; then
  for i in $(seq 0 $((SCENE_COUNT - 1))); do
    SCENE_ID=$(jq -r ".scenes[$i].id" "$STORYBOARD")
    VO_TEXT=$(jq -r ".scenes[$i].voiceover // .scenes[$i].narration // empty" "$STORYBOARD")

    if [[ -n "$VO_TEXT" ]]; then
      log_info "  Scene ${SCENE_ID}: generating voiceover..."
      bash "${SCRIPT_DIR}/voice.sh" \
        --text "$VO_TEXT" \
        --output "${OUTPUT_DIR}/audio/vo-${SCENE_ID}.mp3" \
        > /dev/null 2>&1 || log_warn "  Failed to generate VO for ${SCENE_ID}"
    fi
  done
fi
log_ok "Step 5 complete"

# ─── Step 6: Generate background music ──────────────────────────────────────
log_info ""
log_info "STEP 6/7: Generating background music..."

bash "${SCRIPT_DIR}/music.sh" \
  --prompt "cinematic background music, subtle and professional, suitable for product video" \
  --duration "$DURATION" \
  --output "${OUTPUT_DIR}/audio/music.mp3" \
  > /dev/null 2>&1 || log_warn "  Failed to generate music"

log_ok "Step 6 complete"

# ─── Step 7: Remotion assembly ──────────────────────────────────────────────
log_info ""
log_info "STEP 7/7: Bootstrapping Remotion project..."

REMOTION_DIR="${OUTPUT_DIR}/remotion-project"

bash "${SCRIPT_DIR}/remotion_init.sh" \
  --template "$TEMPLATE" \
  --output "$REMOTION_DIR" \
  --no-install --no-verify \
  > /dev/null 2>&1

# Copy generated assets into Remotion public/
mkdir -p "${REMOTION_DIR}/public/assets" "${REMOTION_DIR}/public/audio"
cp "${OUTPUT_DIR}/assets/"*.png "${REMOTION_DIR}/public/assets/" 2>/dev/null || true
cp "${OUTPUT_DIR}/audio/"*.mp3 "${REMOTION_DIR}/public/audio/" 2>/dev/null || true
cp "${OUTPUT_DIR}/scenes/"*.mp4 "${REMOTION_DIR}/public/assets/" 2>/dev/null || true

log_ok "Remotion project ready at ${REMOTION_DIR}"

if [[ "$SKIP_RENDER" == "true" ]]; then
  log_info "Skipping render (--skip-render). Review project at: ${REMOTION_DIR}"
  json_output "$(json_build \
    status=ready_for_review \
    output_dir="$OUTPUT_DIR" \
    remotion_project="$REMOTION_DIR" \
    storyboard="${OUTPUT_DIR}/manifests/storyboard.json")"
  exit 0
fi

# Install deps and render
log_info "Installing dependencies and rendering..."
(cd "$REMOTION_DIR" && npm install --loglevel=error 2>&1) || log_warn "npm install had warnings"

bash "${SCRIPT_DIR}/remotion_render.sh" \
  --project "$REMOTION_DIR" \
  --output "${OUTPUT_DIR}/final/output.mp4"

log_info ""
log_info "========================================"
log_ok "  Pipeline complete!"
log_info "  Final video: ${OUTPUT_DIR}/final/output.mp4"
log_info "  Storyboard:  ${OUTPUT_DIR}/manifests/storyboard.json"
log_info "  Assets:      ${OUTPUT_DIR}/assets/"
log_info "  Audio:       ${OUTPUT_DIR}/audio/"
log_info "  Remotion:    ${REMOTION_DIR}/"
log_info "========================================"

json_output "$(json_build \
  status=completed \
  output="${OUTPUT_DIR}/final/output.mp4" \
  remotion_project="$REMOTION_DIR" \
  storyboard="${OUTPUT_DIR}/manifests/storyboard.json")"
