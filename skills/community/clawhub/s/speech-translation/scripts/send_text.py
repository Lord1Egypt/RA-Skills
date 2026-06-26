#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys


STAGE_TITLES = {
    "transcript": "转写结果",
    "translation": "翻译结果",
}



def build_message(stage: str, body: str) -> str:
    title = STAGE_TITLES.get(stage, stage)
    return f"{title}\n{'-' * 16}\n{body.strip()}"



def main() -> None:
    parser = argparse.ArgumentParser(description="Send text stage message")
    parser.add_argument("--stage", required=True, help="阶段名，如 transcript / translation")
    parser.add_argument(
        "--command-template",
        default=os.environ.get("VOICE_TRANSLATE_TEXT_COMMAND_TEMPLATE", ""),
        help=(
            "发送命令模板。脚本会把消息正文通过 stdin 传入该命令。"
            "例如: python some_sender.py --kind text"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅打印，不实际发送",
    )
    args = parser.parse_args()

    body = sys.stdin.read().strip()
    if not body:
        raise SystemExit("No stdin text provided.")

    message = build_message(args.stage, body)

    if args.dry_run:
        print(message)
        return

    if not args.command_template:
        raise SystemExit(
            "No command template provided. Use --command-template or set VOICE_TRANSLATE_TEXT_COMMAND_TEMPLATE."
        )

    subprocess.run(args.command_template, input=message.encode("utf-8"), shell=True, check=True)


if __name__ == "__main__":
    main()
