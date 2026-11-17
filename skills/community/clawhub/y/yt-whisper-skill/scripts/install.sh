#!/bin/bash
# Install script for the yt-whisper skill

set -euo pipefail

echo "Installing yt-whisper..."

# Check dependencies
check_dep() {
    if ! command -v "$1" &> /dev/null; then
        echo "Error: $1 is not installed"
        echo "Install with: sudo apt install $2"
        exit 1
    fi
}

echo "Checking dependencies..."
check_dep ffmpeg ffmpeg

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$REPO_ROOT/.venv"

check_dep python3 python3

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/pip" install -U pip wheel setuptools yt-dlp openai-whisper

mkdir -p "$HOME/Transcriptions" "$HOME/Transcriptions/Scripts"

mkdir -p "$INSTALL_DIR"
cp "$SCRIPT_DIR/yt-transcribe.sh" "$INSTALL_DIR/yt-transcribe"
chmod +x "$INSTALL_DIR/yt-transcribe"
cp "$SCRIPT_DIR/yt-transcribe.sh" "$HOME/Transcriptions/Scripts/yt-transcribe.sh"
chmod +x "$HOME/Transcriptions/Scripts/yt-transcribe.sh"


JS_RUNTIME=""
for R in node deno bun quickjs; do
    if command -v "$R" >/dev/null 2>&1; then
        JS_RUNTIME="$R ($(command -v "$R"))"
        break
    fi
done

echo ""
if [ -n "$JS_RUNTIME" ]; then
    echo "✓ JavaScript runtime for yt-dlp: $JS_RUNTIME"
else
    echo "! No JavaScript runtime found (node/deno/bun/quickjs)."
    echo "  yt-dlp needs one to solve YouTube's signature challenges, otherwise"
    echo "  downloads fail with 'HTTP Error 403: Forbidden'."
fi
echo "✓ Installed yt-transcribe to: $INSTALL_DIR/yt-transcribe"
echo "✓ Synced script to: $HOME/Transcriptions/Scripts/yt-transcribe.sh"
echo "✓ Local toolchain ready in: $VENV_DIR"
echo ""
echo "Make sure $INSTALL_DIR is in your PATH:"
echo '  export PATH="$HOME/.local/bin:$PATH"'
echo ""
echo "Usage:"
echo "  yt-transcribe 'https://youtu.be/VIDEO_ID'"
echo ""
