#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

PYTHON=""
for py in python3.13 python3.12 python3.11 python3.10 python3.9 python3; do
  if command -v "$py" &>/dev/null; then
    ver=$("$py" -c "import sys; print(sys.version_info.minor)" 2>/dev/null || echo 0)
    if [[ "$ver" -ge 9 ]] 2>/dev/null; then
      PYTHON="$py"
      break
    fi
  fi
done

[[ -z "$PYTHON" ]] && {
  echo "Error: Python 3.9+ not found." >&2
  exit 1
}

echo "Using Python: $PYTHON ($($PYTHON --version))"

if [[ ! -d "$DIR/.venv" ]]; then
  echo "Creating venv..."
  "$PYTHON" -m venv --system-site-packages "$DIR/.venv" 2>/dev/null || \
    "$PYTHON" -m venv --without-pip --system-site-packages "$DIR/.venv" 2>/dev/null || \
    "$PYTHON" -m venv --without-pip "$DIR/.venv"
fi

# shellcheck disable=SC1091
source "$DIR/.venv/bin/activate"

if ! python -m pip --version &>/dev/null; then
  echo "Bootstrapping pip..."
  curl -sSL https://bootstrap.pypa.io/get-pip.py | python
fi

python -m pip install --upgrade pip >/dev/null
python -m pip install "openvino==2025.2.0" numpy opencv-python-headless >/dev/null

mkdir -p "$DIR/bin"

if [[ ! -x "$DIR/bin/ffmpeg" || ! -x "$DIR/bin/ffprobe" ]]; then
  if command -v ffmpeg &>/dev/null && command -v ffprobe &>/dev/null; then
    ln -sf "$(command -v ffmpeg)" "$DIR/bin/ffmpeg"
    ln -sf "$(command -v ffprobe)" "$DIR/bin/ffprobe"
    echo "Linked system ffmpeg."
  else
    echo "Downloading static ffmpeg..."
    tmp="$(mktemp -d)"
    curl -sSL https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o "$tmp/ff.tar.xz"
    tar -xf "$tmp/ff.tar.xz" -C "$tmp/"
    cp "$tmp"/ffmpeg-*-amd64-static/ffmpeg "$DIR/bin/ffmpeg"
    cp "$tmp"/ffmpeg-*-amd64-static/ffprobe "$DIR/bin/ffprobe"
    chmod +x "$DIR/bin/ffmpeg" "$DIR/bin/ffprobe"
    rm -rf "$tmp"
  fi
fi

chmod +x "$DIR/install.sh" "$DIR/smartupscale.sh"

# Decode model weights if the ClawHub package omitted the raw .bin file.
# ClawHub only ships text-whitelisted extensions, so the sidecar uses .dat
# (base64-encoded OpenVINO IR weights, decoded on first install).
if [[ ! -f "$DIR/model/realesr-general-x4v3_480x270.bin" ]]; then
  if [[ -f "$DIR/model/realesr-general-x4v3_480x270.weights.dat" ]]; then
    echo "Decoding model weights..."
    base64 -d "$DIR/model/realesr-general-x4v3_480x270.weights.dat" > "$DIR/model/realesr-general-x4v3_480x270.bin"
  fi
fi

for required in \
  "$DIR/model/realesr-general-x4v3_480x270.xml" \
  "$DIR/model/realesr-general-x4v3_480x270.bin"
do
  [[ -f "$required" ]] || {
    echo "Error: missing required model asset: $required" >&2
    exit 1
  }
done

echo "Ready: xeon-smartupscale_v2"
