#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


DEFAULT_AGENT_CANDIDATES = [
    Path("/Applications/商汤输入法AudioClaw.app/Contents/Resources/claws/picoclaw/audioclaw-darwin-arm64"),
    Path("/Applications/商汤输入法AudioClaw.app/Contents/Resources/claws/picoclaw/audioclaw-darwin-amd64"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Organize copied clipboard text with audioclaw.")
    parser.add_argument("--text-file", required=True)
    parser.add_argument("--agent-bin", default="")
    parser.add_argument("--session", default="")
    parser.add_argument("--output-markdown", default="")
    return parser.parse_args()


def resolve_agent_bin(explicit: str) -> Path:
    candidates: list[Path] = []
    if explicit.strip():
        candidates.append(Path(explicit).expanduser())
    candidates.extend(DEFAULT_AGENT_CANDIDATES)
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    raise SystemExit("AudioClaw CLI not found. Expected it inside 商汤输入法AudioClaw.app.")


def extract_agent_reply(output: str) -> str:
    lines = [line.rstrip() for line in output.splitlines() if line.strip()]
    for index in range(len(lines) - 1, -1, -1):
        line = lines[index]
        if line.startswith("🦞 "):
            first_line = line[2:].strip()
            tail = lines[index + 1 :]
            return "\n".join([first_line] + tail).strip()
    return "\n".join(lines).strip()


def build_prompt(text: str) -> str:
    return (
        "请把下面这段用户刚刚复制的文本整理成一份清晰、可直接阅读的中文 Markdown。\n\n"
        "输出结构：\n"
        "1. 一句话摘要\n"
        "2. 关键信息\n"
        "3. 整理稿\n"
        "4. 关键词\n"
        "5. 如果存在待办或行动项，请提取出来\n\n"
        "要求：\n"
        "1. 不要编造原文里没有的新事实。\n"
        "2. 可以轻微修正明显错别字或排版问题。\n"
        "3. 输出只要 Markdown 正文，不要解释过程。\n\n"
        f"原始文本如下：\n{text}"
    )


def main() -> int:
    args = parse_args()
    text_path = Path(args.text_file).expanduser().resolve()
    text = text_path.read_text(encoding="utf-8").strip()
    if not text:
        raise SystemExit("Clipboard text is empty.")
    agent_bin = resolve_agent_bin(args.agent_bin)
    out_dir = text_path.parent
    output_markdown = Path(args.output_markdown).expanduser().resolve() if args.output_markdown else out_dir / "clipboard_notes.md"
    session = args.session.strip() or f"realtime_interpreter_clipboard_{int(time.time())}"
    prompt = build_prompt(text)

    command = [
        str(agent_bin),
        "agent",
        "--session",
        session,
        "--message",
        prompt,
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        sys.stderr.write((completed.stderr or completed.stdout or "audioclaw agent failed").strip() + "\n")
        return completed.returncode or 1

    reply = extract_agent_reply(completed.stdout)
    if not reply:
        sys.stderr.write("Could not extract organizer reply from audioclaw output.\n")
        return 1

    output_markdown.write_text(reply.strip() + "\n", encoding="utf-8")
    manifest = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "session": session,
        "text_file": str(text_path),
        "output_markdown": str(output_markdown),
        "agent_bin": str(agent_bin),
    }
    (out_dir / "clipboard_notes.meta.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
