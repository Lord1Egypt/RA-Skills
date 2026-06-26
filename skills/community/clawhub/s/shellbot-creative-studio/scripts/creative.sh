#!/usr/bin/env bash
# shellbot-creative-studio — main router
# Usage: creative <command> [args...]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/config.sh"
source "${SCRIPT_DIR}/lib/output.sh"

usage() {
  cat >&2 <<'EOF'
Usage: creative <command> [args...]

Commands:
  image       Generate images (T2I, reference-guided)
  edit        Edit images (upscale, remove-bg, inpaint, outpaint, style-transfer, relight)
  video       Generate video clips (T2V, I2V)
  voice       Text-to-speech narration
  music       Background music generation
  sfx         Sound effects generation
  remotion    Remotion project management (init, render)
  plan        Creative brief to storyboard
  pipeline    End-to-end production pipeline
  status      Check async task status
  providers   Show available providers and capabilities

Version: 1.0.0
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

COMMAND="$1"
shift

case "$COMMAND" in
  image)      exec bash "${SCRIPT_DIR}/image.sh" "$@" ;;
  edit)       exec bash "${SCRIPT_DIR}/edit.sh" "$@" ;;
  video)      exec bash "${SCRIPT_DIR}/video.sh" "$@" ;;
  voice)      exec bash "${SCRIPT_DIR}/voice.sh" "$@" ;;
  music)      exec bash "${SCRIPT_DIR}/music.sh" "$@" ;;
  sfx)        exec bash "${SCRIPT_DIR}/sfx.sh" "$@" ;;
  plan)       exec bash "${SCRIPT_DIR}/plan.sh" "$@" ;;
  pipeline)   exec bash "${SCRIPT_DIR}/pipeline.sh" "$@" ;;
  status)     exec bash "${SCRIPT_DIR}/status.sh" "$@" ;;
  providers)  exec bash "${SCRIPT_DIR}/providers.sh" "$@" ;;
  remotion)
    # Sub-route: remotion init | remotion render
    if [[ $# -lt 1 ]]; then
      log_error "Usage: creative remotion <init|render> [args...]"
      exit 1
    fi
    SUB="$1"; shift
    case "$SUB" in
      init)   exec bash "${SCRIPT_DIR}/remotion_init.sh" "$@" ;;
      render) exec bash "${SCRIPT_DIR}/remotion_render.sh" "$@" ;;
      *)      log_error "Unknown remotion subcommand: ${SUB}. Use: init, render"; exit 1 ;;
    esac
    ;;
  -h|--help|help)
    usage
    exit 0
    ;;
  *)
    log_error "Unknown command: ${COMMAND}"
    usage
    exit 1
    ;;
esac
