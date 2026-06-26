#!/usr/bin/env python3
"""
Subtitle Generator - CLI entry point
Usage:
    python scripts/main.py <视频文件> [srt|vtt] [语言] [--notify]

Options:
    --notify    完成后打印通知标记，主会话 AI 会自动通过 message 工具发送 Telegram 通知

Examples:
    python scripts/main.py video.mp4 srt zh --notify
    python scripts/main.py video.mp4 vtt en --notify
"""
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

# Dynamically find the actual Python version's site-packages in the venv
def _get_venv_site_packages(venv_path: Path) -> Path | None:
    lib_dir = venv_path / "lib"
    if not lib_dir.exists():
        return None
    for p in lib_dir.iterdir():
        if p.is_dir() and p.name.startswith("python"):
            site = p / "site-packages"
            if site.exists():
                return site
    return None

_WHISPER_VENV_PATH = Path.home() / ".whisper-venv"
_WHISPER_VENV_SITE = _get_venv_site_packages(_WHISPER_VENV_PATH)
if _WHISPER_VENV_SITE is not None:
    sys.path.insert(0, str(_WHISPER_VENV_SITE))


def _check_ffmpeg() -> None:
    """Check ffmpeg is available and raise a clear error if not."""
    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            "ffmpeg 未找到，请先安装 ffmpeg：\n"
            "  Windows: winget install ffmpeg  或  https://ffmpeg.org/download.html\n"
            "  macOS:  brew install ffmpeg\n"
            "  Linux:  sudo apt install ffmpeg  或  sudo yum install ffmpeg"
        )

# Add skills subtitle-generator to path for imports
SKILL_ROOT = Path(__file__).parent.parent
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from subtitle.processor import SubtitleProcessor


def send_notification(message: str) -> None:
    """Send completion notification via openclaw system event (cross-platform)."""
    openclaw_cmd = shutil.which("openclaw")
    if openclaw_cmd is None:
        # Last resort: try common nvm path (Linux/WSL)
        openclaw_cmd = str(Path.home() / ".nvm/versions/node/v24.14.0/bin/openclaw")
    try:
        result = subprocess.run(
            [openclaw_cmd, "system", "event", "--text", message, "--mode", "now"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        print(f"[通知] {result.stdout.strip()}", file=sys.stderr)
    except Exception as e:
        print(f"[通知失败] {e}", file=sys.stderr)


def main() -> None:
    import sys as _sys
    if _sys.stdin.isatty():
        print("⚠️ 建议后台运行：exec background:true command:\"python3 ... --notify\"")

    parser = argparse.ArgumentParser(description="Subtitle Generator")
    parser.add_argument("video_path", help="Path to video file")
    parser.add_argument("output_format", nargs="?", default="srt", choices=["srt", "vtt"])
    parser.add_argument("language", nargs="?", default=None)
    parser.add_argument("--notify", action="store_true", help="发送 Telegram 通知（主会话 AI 会自动通过 message 工具发送）")
    args = parser.parse_args()

    video_name = Path(args.video_path).stem

    try:
        _check_ffmpeg()
        processor = SubtitleProcessor()
        result_path = processor.process(
            args.video_path,
            output_format=args.output_format,
            language=args.language,
        )
        msg = f"✅ 字幕生成完成：{result_path.name}（{processor.last_segment_count} 条）"
        print(msg)

        if args.notify:
            # 通知主会话 AI：通过 openclaw system event 唤醒主会话，主会话收到后会用 message 工具发送 Telegram 通知
            notify_msg = f"【字幕生成完成】\n文件：{result_path.name}\n条数：{processor.last_segment_count}\n路径：{result_path}"
            send_notification(notify_msg)

    except Exception as e:
        err_msg = f"❌ 字幕生成失败：{e}"
        print(err_msg, file=sys.stderr)
        if args.notify:
            send_notification(f"【字幕生成失败】{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
