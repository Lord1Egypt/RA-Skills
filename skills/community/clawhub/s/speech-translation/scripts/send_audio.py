#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import shlex
import subprocess



def main() -> None:
    parser = argparse.ArgumentParser(description="Send audio stage message")
    parser.add_argument("--stage", required=True, help="阶段名，如 audio")
    parser.add_argument("audio_file", help="音频文件路径")
    parser.add_argument(
        "--command-template",
        default=os.environ.get("VOICE_TRANSLATE_AUDIO_COMMAND_TEMPLATE", ""),
        help=(
            "发送命令模板，需包含 {audio_file} 占位符。"
            "例如: python some_sender.py --file {audio_file}"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅打印，不实际发送",
    )
    args = parser.parse_args()

    audio_path = Path(args.audio_file).expanduser().resolve()
    if not audio_path.exists():
        raise SystemExit(f"Audio file not found: {audio_path}")

    if not args.command_template:
        raise SystemExit(
            "No command template provided. Use --command-template or set VOICE_TRANSLATE_AUDIO_COMMAND_TEMPLATE."
        )

    command = args.command_template.format(audio_file=shlex.quote(str(audio_path)))

    if args.dry_run:
        print(command)
        return

    subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    main()
