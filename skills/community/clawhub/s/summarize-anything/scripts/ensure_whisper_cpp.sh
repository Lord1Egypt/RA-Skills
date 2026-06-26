#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
RUNTIME_DIR="${SKILL_DIR}/runtime"
BIN_DIR="${RUNTIME_DIR}/bin"
SRC_DIR="${RUNTIME_DIR}/src"
TARGET="${BIN_DIR}/whisper-cli"

mkdir -p "${BIN_DIR}" "${SRC_DIR}" "${RUNTIME_DIR}/cache" "${RUNTIME_DIR}/work"

retry_command() {
  local attempts="$1"
  shift
  local delay=2
  local i

  for ((i = 1; i <= attempts; i++)); do
    if "$@"; then
      return 0
    fi

    if [[ "${i}" -lt "${attempts}" ]]; then
      echo "Retry ${i}/${attempts} failed for: $*" >&2
      sleep "${delay}"
      if [[ "${delay}" -lt 20 ]]; then
        delay=$((delay * 2))
      fi
    fi
  done

  return 1
}

if [[ -L "${TARGET}" && -x "${TARGET}" ]]; then
  echo "${TARGET}"
  exit 0
fi

if [[ -e "${TARGET}" ]]; then
  rm -f "${TARGET}"
fi

if command -v whisper-cli >/dev/null 2>&1; then
  ln -sf "$(command -v whisper-cli)" "${TARGET}"
  echo "${TARGET}"
  exit 0
fi

if command -v brew >/dev/null 2>&1; then
  if ! brew list whisper-cpp >/dev/null 2>&1; then
    retry_command 3 brew install whisper-cpp || true
  fi
  if command -v whisper-cli >/dev/null 2>&1; then
    ln -sf "$(command -v whisper-cli)" "${TARGET}"
    echo "${TARGET}"
    exit 0
  fi
fi

if command -v git >/dev/null 2>&1 && command -v cmake >/dev/null 2>&1; then
  REPO_DIR="${SRC_DIR}/whisper.cpp"
  if [[ ! -d "${REPO_DIR}" ]]; then
    retry_command 5 git clone --depth=1 https://github.com/ggml-org/whisper.cpp.git "${REPO_DIR}" || true
  fi

  if [[ -d "${REPO_DIR}/.git" ]]; then
    retry_command 3 git -C "${REPO_DIR}" fetch --depth=1 origin || true
  fi

  if [[ -d "${REPO_DIR}" ]]; then
    retry_command 3 cmake -S "${REPO_DIR}" -B "${REPO_DIR}/build" -DWHISPER_BUILD_TESTS=OFF -DWHISPER_BUILD_EXAMPLES=ON >/dev/null || true
    retry_command 3 cmake --build "${REPO_DIR}/build" --config Release --target whisper-cli -j 4 >/dev/null || true
  fi

  BUILT_BIN="$(find "${REPO_DIR}/build" -type f -name whisper-cli | head -n 1)"
  if [[ -n "${BUILT_BIN}" && -x "${BUILT_BIN}" ]]; then
    ln -sf "${BUILT_BIN}" "${TARGET}"
    echo "${TARGET}"
    exit 0
  fi
fi

echo "Failed to provision whisper-cli inside ${BIN_DIR}. Tried PATH, Homebrew, and source build with git/cmake." >&2
exit 1
