#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"${SCRIPT_DIR}/maintain_runtime.sh" >/dev/null 2>&1 || true
bash "${SCRIPT_DIR}/ensure_ffmpeg.sh" >/dev/null
"${SCRIPT_DIR}/ensure_whisper_cpp.sh" >/dev/null
"${SCRIPT_DIR}/ensure_whisper_model.sh" "${1:-small}" >/dev/null

SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
mkdir -p "${SKILL_DIR}/runtime/cache" "${SKILL_DIR}/runtime/src" "${SKILL_DIR}/runtime/work"

echo "${SKILL_DIR}/runtime"
