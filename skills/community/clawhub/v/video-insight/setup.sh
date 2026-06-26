#!/usr/bin/env bash
# video-insight setup — non-interactive by default, --interactive for prompts
# Supports: macOS / Linux / WSL / Windows VM
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="${SKILL_DIR}/.venv"
INTERACTIVE=false

for arg in "$@"; do
    case "$arg" in
        --interactive) INTERACTIVE=true ;;
        --help|-h) echo "Usage: setup.sh [--interactive]"; exit 0 ;;
    esac
done

log()  { echo "[setup] $*" >&2; }
warn() { echo "[setup] ⚠️  $*" >&2; }
ok()   { echo "[setup] ✅ $*" >&2; }

# ── Platform detection ──
OS="$(uname -s)"
ARCH="$(uname -m)"
IS_WSL=false
IS_MACOS=false
IS_LINUX=false

case "$OS" in
    Linux)
        IS_LINUX=true
        if grep -qi microsoft /proc/version 2>/dev/null; then
            IS_WSL=true
        fi
        ;;
    Darwin) IS_MACOS=true ;;
    MINGW*|MSYS*|CYGWIN*)
        warn "Native Windows detected. Recommend running under WSL."
        IS_LINUX=true
        ;;
    *) warn "Unknown OS: $OS. Proceeding anyway." ;;
esac

log "Platform: $OS ($ARCH) | WSL=$IS_WSL | macOS=$IS_MACOS"

# ── Python check ──
PYTHON=""
for py in python3 python; do
    if command -v "$py" >/dev/null 2>&1; then
        PYTHON="$py"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "❌ Python 3 not found. Please install Python 3.8+ first." >&2
    exit 1
fi

PY_VERSION=$("$PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
log "Python: $PYTHON ($PY_VERSION)"

PY_MAJOR=$("$PYTHON" -c "import sys; print(sys.version_info.major)")
PY_MINOR=$("$PYTHON" -c "import sys; print(sys.version_info.minor)")
if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 8 ]; }; then
    echo "❌ Python 3.8+ required, found $PY_VERSION" >&2
    exit 1
fi

# ── ffmpeg check ──
if ! command -v ffmpeg >/dev/null 2>&1; then
    warn "ffmpeg not found. Bilibili video processing requires ffmpeg."
    if $IS_MACOS; then
        log "Install: brew install ffmpeg"
    elif $IS_LINUX; then
        log "Install: sudo apt install ffmpeg (or equivalent)"
    fi
    if $INTERACTIVE; then
        read -rp "Continue without ffmpeg? [y/N] " ans
        [[ "$ans" =~ ^[Yy] ]] || exit 1
    else
        warn "Continuing without ffmpeg. Bilibili support will be limited."
    fi
else
    ok "ffmpeg found: $(ffmpeg -version 2>&1 | head -1)"
fi

# ── Create venv ──
if [ ! -d "$VENV_DIR" ]; then
    log "Creating virtual environment..."
    "$PYTHON" -m venv "$VENV_DIR" 2>/dev/null || {
        warn "venv creation failed. Trying without ensurepip..."
        "$PYTHON" -m venv --without-pip "$VENV_DIR" 2>/dev/null || {
            warn "venv not available. Will use system Python with --break-system-packages."
            VENV_DIR=""
        }
    }
fi

if [ -n "$VENV_DIR" ] && [ -f "${VENV_DIR}/bin/python3" ]; then
    PIP="${VENV_DIR}/bin/pip"
    VPYTHON="${VENV_DIR}/bin/python3"
    ok "venv ready: $VENV_DIR"
elif [ -n "$VENV_DIR" ] && [ -f "${VENV_DIR}/Scripts/pip.exe" ]; then
    PIP="${VENV_DIR}/Scripts/pip.exe"
    VPYTHON="${VENV_DIR}/Scripts/python.exe"
    ok "venv ready (Windows): $VENV_DIR"
else
    PIP="pip3"
    VPYTHON="$PYTHON"
    warn "No venv — installing to user/system Python"
fi

# Ensure pip exists in venv
if [ -n "$VENV_DIR" ] && ! command -v "$PIP" >/dev/null 2>&1; then
    "$VPYTHON" -m ensurepip --upgrade 2>/dev/null || true
fi

# ── Pip install helper ──
pip_install() {
    if [ -n "$VENV_DIR" ]; then
        "$PIP" install --quiet "$@" 2>/dev/null || "$PIP" install "$@"
    else
        "$PIP" install --quiet --break-system-packages "$@" 2>/dev/null || \
        "$PIP" install --quiet --user "$@" 2>/dev/null || \
        "$PIP" install "$@"
    fi
}

# ── Core dependencies ──
log "Installing core dependencies..."
pip_install yt-dlp youtube-transcript-api innertube requests

ok "Core dependencies installed"

# ── GPU detection and whisper ──
GPU_AVAILABLE=false
GPU_INFO=""

if command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi >/dev/null 2>&1; then
    GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo "unknown")
    GPU_AVAILABLE=true
fi

log ""
log "═══════════════════════════════════════════════"
if $GPU_AVAILABLE; then
    log "🎮 GPU detected: $GPU_INFO"
    log "  Whisper will use CUDA (faster transcription)"
    log "  Installing faster-whisper with CUDA support..."
    pip_install faster-whisper
    # Verify CUDA actually works with ctranslate2
    if "$VPYTHON" -c "import ctranslate2; ctranslate2.get_supported_compute_types('cuda')" >/dev/null 2>&1; then
        ok "faster-whisper with CUDA ready"
    else
        warn "ctranslate2 CUDA not functional. Whisper will fallback to CPU."
        warn "Possible causes:"
        warn "  - Missing CUDA libraries (libcublas, libcudnn)"
        warn "  - CUDA version mismatch"
        warn "  - WSL CUDA driver not properly configured"
        log "  Whisper will still work, just slower (CPU mode)."
    fi
else
    log "💻 No GPU detected — Whisper will use CPU mode"
    log "  Bilibili transcription will be slower but functional."
    if $IS_WSL; then
        log "  WSL tip: ensure NVIDIA drivers are installed on Windows host"
        log "  and nvidia-smi is accessible from WSL."
    fi
    log "  Installing faster-whisper (CPU)..."
    pip_install faster-whisper
    ok "faster-whisper (CPU) ready"
fi
log "═══════════════════════════════════════════════"
log ""

# ── Create cache directory ──
CACHE_DIR="${HOME}/.cache/video-insight"
mkdir -p "$CACHE_DIR"
ok "Cache directory: $CACHE_DIR"

# ── Verify installation ──
log "Verifying installation..."
VERIFY_OK=true

for mod in yt_dlp youtube_transcript_api innertube requests; do
    if "$VPYTHON" -c "import $mod" 2>/dev/null; then
        ok "$mod"
    else
        warn "Failed to import $mod"
        VERIFY_OK=false
    fi
done

# faster-whisper is optional
if "$VPYTHON" -c "import faster_whisper" 2>/dev/null; then
    ok "faster-whisper"
else
    warn "faster-whisper not available (Bilibili transcription won't work)"
fi

if $VERIFY_OK; then
    log ""
    ok "Setup complete! Run: video-insight --url 'https://...'"
else
    warn "Some dependencies failed. Check errors above."
    exit 1
fi
