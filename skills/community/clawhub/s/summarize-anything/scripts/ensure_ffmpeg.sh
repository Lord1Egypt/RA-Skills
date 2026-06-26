#!/usr/bin/env bash
set -euo pipefail

run_with_optional_sudo() {
  if [[ "${EUID:-$(id -u)}" -eq 0 ]]; then
    "$@"
    return
  fi

  if command -v sudo >/dev/null 2>&1; then
    sudo "$@"
    return
  fi

  "$@"
}

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

if command -v ffmpeg >/dev/null 2>&1; then
  command -v ffmpeg
  exit 0
fi

if command -v brew >/dev/null 2>&1; then
  retry_command 3 brew install ffmpeg || true
  if command -v ffmpeg >/dev/null 2>&1; then
    command -v ffmpeg
    exit 0
  fi
fi

if command -v apt-get >/dev/null 2>&1; then
  retry_command 3 run_with_optional_sudo apt-get update || true
  retry_command 3 run_with_optional_sudo apt-get install -y ffmpeg || true
  if command -v ffmpeg >/dev/null 2>&1; then
    command -v ffmpeg
    exit 0
  fi
fi

if command -v dnf >/dev/null 2>&1; then
  retry_command 3 run_with_optional_sudo dnf install -y ffmpeg || true
  if command -v ffmpeg >/dev/null 2>&1; then
    command -v ffmpeg
    exit 0
  fi
fi

if command -v yum >/dev/null 2>&1; then
  retry_command 3 run_with_optional_sudo yum install -y ffmpeg || true
  if command -v ffmpeg >/dev/null 2>&1; then
    command -v ffmpeg
    exit 0
  fi
fi

if command -v pacman >/dev/null 2>&1; then
  retry_command 3 run_with_optional_sudo pacman -Sy --noconfirm ffmpeg || true
  if command -v ffmpeg >/dev/null 2>&1; then
    command -v ffmpeg
    exit 0
  fi
fi

echo "Failed to provision ffmpeg. Tried PATH, Homebrew, apt-get, dnf, yum, and pacman." >&2
exit 1
