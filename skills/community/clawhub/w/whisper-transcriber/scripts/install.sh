#!/bin/bash

# =============================================================================
# Whisper Transcriber - Cross-platform installer
# =============================================================================
# Installs:
#   - whisper-cli (from whisper.cpp / whisper-cpp package)
#   - ffmpeg
# Optionally downloads a ggml model into assets/models/ (or user dir)
#
# Usage:
#   bash <SKILL_DIR>/scripts/install.sh            # interactive (downloads base by default)
#   bash <SKILL_DIR>/scripts/install.sh base       # download base
#   MODEL=large bash <SKILL_DIR>/scripts/install.sh
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL_DIR_SKILL="${WHISPER_MODEL_DIR:-$SKILL_DIR/assets/models}"
# Default download directory = skill assets/models
MODEL_DIR_USER="${WHISPER_MODEL_DIR_USER:-$MODEL_DIR_SKILL}"

MODEL="${MODEL:-${1:-}}"

model_size() {
  case "$1" in
    tiny) echo "75 MB";;
    base) echo "142 MB";;
    small) echo "466 MB";;
    medium) echo "1.5 GB";;
    large) echo "2.9 GB";;
    *) echo "unknown";;
  esac
}

model_file() {
  case "$1" in
    tiny) echo "ggml-tiny.bin";;
    base) echo "ggml-base.bin";;
    small) echo "ggml-small.bin";;
    medium) echo "ggml-medium.bin";;
    large) echo "ggml-large-v3.bin";;
    *) echo "";;
  esac
}

log() { echo -e "${BLUE}[INFO]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
err() { echo -e "${RED}[ERROR]${NC} $*"; }
ok() { echo -e "${GREEN}[OK]${NC} $*"; }
step() { echo -e "${MAGENTA}[STEP]${NC} $*"; }

need_cmd() {
  command -v "$1" >/dev/null 2>&1
}

detect_pm() {
  if need_cmd brew; then echo brew; return; fi
  if need_cmd apt-get; then echo apt; return; fi
  if need_cmd dnf; then echo dnf; return; fi
  if need_cmd yum; then echo yum; return; fi
  if need_cmd pacman; then echo pacman; return; fi
  if need_cmd zypper; then echo zypper; return; fi
  echo none
}

install_pkgs() {
  local pm="$1"; shift
  local pkgs=("$@")
  case "$pm" in
    brew)
      step "Installing via Homebrew: ${pkgs[*]}"
      brew install "${pkgs[@]}"
      ;;
    apt)
      step "Installing via apt: ${pkgs[*]}"
      sudo apt-get update -y
      sudo apt-get install -y "${pkgs[@]}"
      ;;
    dnf)
      step "Installing via dnf: ${pkgs[*]}"
      sudo dnf install -y "${pkgs[@]}"
      ;;
    yum)
      step "Installing via yum: ${pkgs[*]}"
      sudo yum install -y "${pkgs[@]}"
      ;;
    pacman)
      step "Installing via pacman: ${pkgs[*]}"
      sudo pacman -Sy --noconfirm "${pkgs[@]}"
      ;;
    zypper)
      step "Installing via zypper: ${pkgs[*]}"
      sudo zypper --non-interactive install "${pkgs[@]}"
      ;;
    *)
      err "No supported package manager detected."
      echo "On macOS: install Homebrew then: brew install whisper-cpp ffmpeg"
      echo "On Linux: install packages 'ffmpeg' and 'whisper-cpp' (name varies by distro)"
      echo "On Windows: use PowerShell installer: scripts/install.ps1"
      return 1
      ;;
  esac
}

ensure_deps() {
  local pm
  pm="$(detect_pm)"

  if [[ "$(uname -s)" == MINGW* || "$(uname -s)" == MSYS* || "$(uname -s)" == CYGWIN* ]]; then
    err "Detected Windows shell. Please run: powershell -ExecutionPolicy Bypass -File '$SKILL_DIR/scripts/install.ps1'"
    return 1
  fi

  local need=()
  if ! need_cmd ffmpeg; then need+=(ffmpeg); fi

  # whisper-cli binary comes from whisper-cpp on brew; on linux package name may differ.
  if ! need_cmd whisper-cli; then
    if [ "$pm" = "brew" ]; then
      need+=(whisper-cpp)
    else
      # best effort: many distros package it as whisper-cpp
      need+=(whisper-cpp)
    fi
  fi

  if [ ${#need[@]} -eq 0 ]; then
    ok "Dependencies already installed (whisper-cli, ffmpeg)"
    return 0
  fi

  install_pkgs "$pm" "${need[@]}"
}

select_model() {
  local selected="$1"
  if [ -n "$selected" ]; then
    echo "$selected"; return
  fi

  echo -e "${CYAN}Select model to download (optional):${NC}"
  echo "  1) none  (skip download)"
  echo "  2) base  (recommended)"
  echo "  3) small"
  echo "  4) medium"
  echo "  5) large"
  echo ""
  read -r -p "Choice (1-5, default 2): " choice || true
  case "$choice" in
    1) echo "none";;
    3) echo "small";;
    4) echo "medium";;
    5) echo "large";;
    2|"") echo "base";;
    *) warn "Invalid choice; using base"; echo "base";;
  esac
}

sha256_file() {
  local f="$1"
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$f" | awk '{print $1}'
    return 0
  fi
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$f" | awk '{print $1}'
    return 0
  fi
  return 1
}

expected_sha256_for_model() {
  local model_name="$1"
  local cfg="$SKILL_DIR/config.json"
  if [ -f "$cfg" ]; then
    node -e "
      const fs=require('fs');
      try{
        const j=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));
        const v=(j.modelsSha256||{})[process.argv[2]]||'';
        process.stdout.write(String(v));
      }catch(e){process.stdout.write('');}
    " "$cfg" "$model_name"
  fi
}

verify_model_sha256_if_available() {
  local model_name="$1"
  local path="$2"
  local expected actual
  expected="$(expected_sha256_for_model "$model_name")"
  if [ -z "$expected" ]; then return 0; fi
  actual="$(sha256_file "$path" || true)"
  if [ -z "$actual" ]; then
    warn "Cannot compute sha256 (missing shasum/sha256sum); skipping verification"
    return 0
  fi
  if [ "$actual" != "$expected" ]; then
    err "Model sha256 mismatch: $path"
    err "expected: $expected"
    err "actual:   $actual"
    return 1
  fi
  ok "Model sha256 OK: $model_name"
}

download_model() {
  local model_name="$1"
  if [ "$model_name" = "none" ]; then
    warn "Skipping model download"
    return 0
  fi

  local mf
  mf="$(model_file "$model_name")"
  if [ -z "$mf" ]; then
    err "Unknown model: $model_name"
    return 1
  fi

  # Default: download models into the skill's assets/models directory.
  # Repo is protected by .gitignore so large binaries won't be committed/published.
  local target_dir="$MODEL_DIR_SKILL"
  mkdir -p "$target_dir"
  local target="$target_dir/$mf"

  if [ -f "$target" ]; then
    ok "Model already exists: $target"
    return 0
  fi

  local url="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/$mf"
  step "Downloading model: $model_name ($(model_size "$model_name"))"
  log "URL: $url"
  log "To:  $target"

  if need_cmd curl; then
    curl -L --fail --progress-bar "$url" -o "$target"
  elif need_cmd wget; then
    wget -c "$url" -O "$target"
  else
    err "Need curl or wget to download models"
    return 1
  fi

  ok "Model downloaded: $target"
  verify_model_sha256_if_available "$model_name" "$target"
}

main() {
  echo -e "${CYAN}🎤 Whisper Transcriber installer${NC}"
  echo "Skill dir: $SKILL_DIR"
  echo ""

  ensure_deps

  local m
  m="$(select_model "${MODEL}")"
  download_model "$m"

  echo ""
  ok "Done. Try: $SKILL_DIR/scripts/transcribe.sh <audio-file>"
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  echo "Usage: $0 [model]"
  echo "Models: none|tiny|base|small|medium|large"
  exit 0
fi

main "$@"
