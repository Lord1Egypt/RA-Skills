#!/usr/bin/env bash
# Install xeonupscale skill.
#   1) From clone:   bash install.sh
#   2) Remote:       curl -fsSL <raw>/install.sh | REPO_URL=https://github.com/Wray151/xeonupscale bash
# Override: TARGET=openclaw|claude (default openclaw)
set -euo pipefail

TARGET="${TARGET:-openclaw}"
case "$TARGET" in
  openclaw) DEST="$HOME/.openclaw/workspace/skills/xeonupscale" ;;
  claude)   DEST="$HOME/.claude/skills/xeonupscale" ;;
  *) echo "TARGET must be 'openclaw' or 'claude'"; exit 1 ;;
esac

if [ -f "${BASH_SOURCE[0]:-}" ] && [ -f "$(dirname "${BASH_SOURCE[0]}")/upscale.sh" ]; then
  REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
  : "${REPO_URL:?set REPO_URL=https://github.com/Wray151/xeonupscale when piping}"
  REPO_DIR="$HOME/.local/share/xeonupscale"
  [ -d "$REPO_DIR/.git" ] || git clone --depth 1 "$REPO_URL" "$REPO_DIR"
fi
echo "repo at: $REPO_DIR"

# Static ffmpeg build (works on any glibc 2.17+ Linux x86_64, no apt needed)
FFMPEG_DIR="$REPO_DIR/ffmpeg"
FFMPEG_BIN="$FFMPEG_DIR/ffmpeg"
if [ ! -x "$FFMPEG_BIN" ]; then
  case "$(uname -s)-$(uname -m)" in
    Linux-x86_64)
      URL="https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz" ;;
    Linux-aarch64)
      URL="https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linuxarm64-gpl.tar.xz" ;;
    *) echo "no static ffmpeg build for $(uname -s)-$(uname -m); install ffmpeg manually"; exit 1 ;;
  esac
  echo "downloading ffmpeg from $URL"
  mkdir -p "$FFMPEG_DIR"
  TMP="$(mktemp -t ffmpeg.XXXXXX.tar.xz)"
  curl -fL --retry 3 -o "$TMP" "$URL"
  tar -xJf "$TMP" -C "$FFMPEG_DIR" --strip-components=2 \
    --wildcards '*/bin/ffmpeg' '*/bin/ffprobe'
  rm -f "$TMP"
  chmod +x "$FFMPEG_DIR"/ffmpeg "$FFMPEG_DIR"/ffprobe
fi
echo "ffmpeg: $($FFMPEG_BIN -version | head -1)"

# patch upscale.sh to default to bundled ffmpeg
if ! grep -q "FFMPEG=\"\${FFMPEG:-$FFMPEG_BIN}\"" "$REPO_DIR/upscale.sh" 2>/dev/null; then
  sed -i "s|FFMPEG=\"\${FFMPEG:-ffmpeg}\"|FFMPEG=\"\${FFMPEG:-$FFMPEG_BIN}\"|" "$REPO_DIR/upscale.sh" || true
fi

mkdir -p "$(dirname "$DEST")"
[ -e "$DEST" ] && rm -rf "$DEST"
ln -s "$REPO_DIR" "$DEST"
echo "✓ skill installed at $DEST -> $REPO_DIR"
echo "  在 agent 里 /reset 或开新会话即可使用。"
