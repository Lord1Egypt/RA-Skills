#!/usr/bin/env bash
# video-viral-pipeline 依赖安装(macOS 为主；Linux 见注释)
# 安装: 下载/转写/烧字幕所需工具 + 视频号发布工具(可选)
set -uo pipefail

echo "==> 1) 命令行工具: yt-dlp + ffmpeg-full(必须带 libass，否则烧不了字幕)"
if command -v brew >/dev/null; then
  brew list yt-dlp >/dev/null 2>&1 || brew install yt-dlp
  # 注意：homebrew 现在的 ffmpeg 是精简版不含 libass，必须装 ffmpeg-full
  brew list ffmpeg-full >/dev/null 2>&1 || brew install ffmpeg-full
  echo "    提示：把 ffmpeg-full 放进 PATH 前面：echo 'export PATH=\"/usr/local/opt/ffmpeg-full/bin:\$PATH\"' >> ~/.zshrc"
else
  echo "    非 macOS：自行安装 yt-dlp 和带 --enable-libass 的 ffmpeg"
fi

echo "==> 2) Whisper 转写引擎(faster-whisper, 装在独立 venv 避开 Python 版本问题)"
PY312="$(command -v python3.12 || true)"
if [ -n "$PY312" ]; then
  VENV="$HOME/.vvp-whisper"
  [ -d "$VENV" ] || "$PY312" -m venv "$VENV"
  "$VENV/bin/pip" install -q --upgrade pip
  "$VENV/bin/pip" install -q --prefer-binary faster-whisper pysocks "httpx[socks]"
  echo "    faster-whisper 装在 $VENV(用它的 python 跑转写)"
  echo "    模型首次会自动从 HuggingFace 下；国内网络不稳建议用 curl 续传预下到 ~/.cache/xh-models/"
else
  echo "    未找到 python3.12，请先装(brew install python@3.12)，faster-whisper 在 3.14 上无 wheel"
fi

echo "==> 3) (可选)视频号自动发布: social-auto-upload"
read -r -p "    要安装视频号发布工具吗? [y/N] " ans
if [[ "${ans:-N}" =~ ^[Yy]$ ]]; then
  SAU="$HOME/social-auto-upload"
  [ -d "$SAU" ] || git clone --depth 1 https://github.com/dreammis/social-auto-upload.git "$SAU"
  if [ -n "$PY312" ]; then
    [ -d "$SAU/.venv" ] || "$PY312" -m venv "$SAU/.venv"
    "$SAU/.venv/bin/pip" install -q --upgrade pip
    "$SAU/.venv/bin/pip" install -q patchright loguru segno opencv-python-headless requests pyyaml schedule pillow
    "$SAU/.venv/bin/patchright" install chromium
  fi
  # 写 conf.py
  cat > "$SAU/conf.py" <<'CONF'
from pathlib import Path
BASE_DIR = Path(__file__).parent.resolve()
XHS_SERVER = "http://127.0.0.1:11901"
LOCAL_CHROME_PATH = ""
LOCAL_CHROME_HEADLESS = False
DEBUG_MODE = True
CONF
  echo "    已装到 $SAU。登录视频号:"
  echo "      cd $SAU && PYTHONPATH=. .venv/bin/python examples/get_tencent_cookie.py"
  echo "      (会生成二维码 png，用手机微信扫)"
fi

echo "==> 完成。详见 SKILL.md / README.md"
