#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
MODEL_DIR="${SKILL_DIR}/runtime/models"
MODEL_NAME="${1:-small}"
TARGET="${MODEL_DIR}/ggml-${MODEL_NAME}.bin"
SKILL_PARENT="$(cd "${SKILL_DIR}/.." && pwd)"

mkdir -p "${MODEL_DIR}"

retry_download() {
  local url="$1"
  local output="$2"
  local attempts="${3:-10}"
  local delay=2
  local i
  local partial="${output}.part"

  for ((i = 1; i <= attempts; i++)); do
    if curl -L --fail --continue-at - "${url}" -o "${partial}"; then
      local size_bytes
      size_bytes="$(wc -c < "${partial}" | tr -d ' ')"
      if [[ "${size_bytes}" -gt 100000000 ]]; then
        mv "${partial}" "${output}"
        return 0
      fi
    fi

    if [[ "${i}" -lt "${attempts}" ]]; then
      echo "Model download attempt ${i}/${attempts} failed for ${url}; retrying in ${delay}s." >&2
      sleep "${delay}"
      if [[ "${delay}" -lt 30 ]]; then
        delay=$((delay * 2))
      fi
    fi
  done

  rm -f "${partial}"
  return 1
}

if [[ -f "${TARGET}" ]]; then
  SIZE_BYTES="$(wc -c < "${TARGET}" | tr -d ' ')"
  if [[ "${SIZE_BYTES}" -gt 100000000 ]]; then
    echo "${TARGET}"
    exit 0
  fi
  rm -f "${TARGET}"
fi

for CANDIDATE in \
  "${PWD}/ggml-${MODEL_NAME}.bin" \
  "${PWD}/models/ggml-${MODEL_NAME}.bin" \
  "${PWD}/podcast_work/models/ggml-${MODEL_NAME}.bin" \
  "${SKILL_PARENT}/models/ggml-${MODEL_NAME}.bin" \
  "${SKILL_PARENT}/podcast_work/models/ggml-${MODEL_NAME}.bin" \
  "${HOME}/.cache/whisper.cpp/models/ggml-${MODEL_NAME}.bin"
do
  if [[ -f "${CANDIDATE}" ]]; then
    cp "${CANDIDATE}" "${TARGET}"
    echo "${TARGET}"
    exit 0
  fi
done

case "${MODEL_NAME}" in
  tiny|base|small|medium|large-v3|large-v3-turbo)
    URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-${MODEL_NAME}.bin"
    ;;
  *)
    echo "Unsupported model name: ${MODEL_NAME}" >&2
    exit 1
    ;;
esac

retry_download "${URL}" "${TARGET}" 10 || {
  echo "Failed to download ggml-${MODEL_NAME}.bin after multiple attempts." >&2
  exit 1
}
echo "${TARGET}"
