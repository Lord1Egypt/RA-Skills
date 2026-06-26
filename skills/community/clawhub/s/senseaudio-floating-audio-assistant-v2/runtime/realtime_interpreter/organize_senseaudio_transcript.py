#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path


DEFAULT_AGENT_CANDIDATES = [
    Path("/Applications/商汤输入法AudioClaw.app/Contents/Resources/claws/picoclaw/audioclaw-darwin-arm64"),
    Path("/Applications/商汤输入法AudioClaw.app/Contents/Resources/claws/picoclaw/audioclaw-darwin-amd64"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Organize a saved SenseAudio transcript with audioclaw agent.")
    parser.add_argument("--transcript-json", required=True)
    parser.add_argument("--agent-bin", default="")
    parser.add_argument("--session", default="")
    parser.add_argument("--output-markdown", default="")
    parser.add_argument("--template-file", default="", help="Optional custom organization prompt template. Use {asr} as the transcript placeholder.")
    parser.add_argument(
        "--mode",
        default="summary",
        choices=["summary", "keywords", "meeting", "study", "todo"],
        help="How audioclaw should organize the transcript.",
    )
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
    clean = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", output)
    lines = [
        line.rstrip()
        for line in clean.splitlines()
        if line.strip() and not is_debug_noise(line)
    ]
    for index in range(len(lines) - 1, -1, -1):
        line = lines[index]
        if line.startswith("🦞 "):
            first_line = line[2:].strip()
            tail = lines[index + 1 :]
            return "\n".join([first_line] + tail).strip()
    for index in range(len(lines) - 1, -1, -1):
        line = lines[index]
        if "Response:" in line:
            first_line = line.split("Response:", 1)[1].strip()
            tail = lines[index + 1 :]
            return "\n".join([first_line] + tail).strip()
    return "\n".join(lines).strip()


def is_debug_noise(line: str) -> bool:
    return bool(re.search(r"\bDBG\b|bus\.go:\d+|Drained buffered messages during close", line))


def is_completion_stub(text: str) -> bool:
    normalized = re.sub(r"\s+", "", text)
    return normalized in {
        "已完成ASR内容整理并按要求输出结果。",
        "已完成ASR内容整理并按要求输出结果",
    }


def is_substantive_reply(text: str) -> bool:
    cleaned = text.strip()
    if not cleaned or is_completion_stub(cleaned):
        return False
    return len(cleaned) >= 20


def extract_message_content_from_tool_call(tool_call: dict) -> str:
    function = tool_call.get("function") if isinstance(tool_call, dict) else None
    if not isinstance(function, dict) or function.get("name") != "message":
        return ""
    raw_arguments = function.get("arguments")
    if isinstance(raw_arguments, dict):
        content = raw_arguments.get("content")
        return str(content or "").strip()
    if isinstance(raw_arguments, str):
        try:
            payload = json.loads(raw_arguments)
        except json.JSONDecodeError:
            return ""
        if isinstance(payload, dict):
            return str(payload.get("content") or "").strip()
    return ""


def extract_agent_reply_from_session(organizer_home: Path) -> str:
    sessions_dir = organizer_home / "workspace" / "sessions"
    if not sessions_dir.exists():
        return ""
    candidates = sorted(
        sessions_dir.glob("*.jsonl"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )
    tool_message_contents: list[str] = []
    assistant_contents: list[str] = []
    for path in candidates:
        for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                item = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            if not isinstance(item, dict):
                continue
            if item.get("role") != "assistant":
                continue
            tool_calls = item.get("tool_calls")
            if isinstance(tool_calls, list):
                for tool_call in tool_calls:
                    content = extract_message_content_from_tool_call(tool_call)
                    if is_substantive_reply(content):
                        tool_message_contents.append(content)
            content = str(item.get("content") or "").strip()
            if is_substantive_reply(content):
                assistant_contents.append(content)
        if tool_message_contents or assistant_contents:
            break
    if tool_message_contents:
        return tool_message_contents[-1]
    if assistant_contents:
        return assistant_contents[-1]
    return ""


def format_segments(segments: list[dict]) -> str:
    rows: list[str] = []
    timestamps = [
        int(item["timestamp_end"])
        for item in segments
        if isinstance(item, dict) and item.get("timestamp_end") is not None
    ]
    base_timestamp = min(timestamps) if timestamps else None
    for item in segments:
        text = str(item.get("text") or "").strip()
        if not text:
            continue
        timestamp_end = item.get("timestamp_end")
        if timestamp_end is None:
            rows.append(text)
            continue
        normalized_timestamp = int(timestamp_end)
        if base_timestamp is not None:
            normalized_timestamp = max(0, normalized_timestamp - base_timestamp)
        seconds = normalized_timestamp / 1000
        minutes = int(seconds // 60)
        remain = seconds - minutes * 60
        rows.append(f"[{minutes:02d}:{remain:05.2f}] {text}")
    return "\n".join(rows)


def load_template(path_text: str) -> str:
    if not path_text.strip():
        return ""
    path = Path(path_text).expanduser().resolve()
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def build_prompt(payload: dict, mode: str, template: str = "") -> str:
    transcript_text = str(payload.get("transcript_text") or "").strip()
    local_fast_text = str(payload.get("local_fast_transcript_text") or "").strip()
    segments = payload.get("segments") or []
    segment_text = format_segments(segments if isinstance(segments, list) else [])
    source_text = segment_text or transcript_text
    if local_fast_text and local_fast_text not in source_text:
        source_text = (
            source_text
            + "\n\n本地快字幕补充（可能包含未被 SenseAudio 最终确认的尾段；仅在 SenseAudio 明显缺尾时参考）：\n"
            + local_fast_text
        )
    if not source_text:
        raise SystemExit("Transcript is empty, nothing to organize.")
    common_rules = (
        "共同要求：\n"
        "1. 只能基于原始 ASR 内容整理，不要编造新事实。\n"
        "2. 可以结合上下文轻微修正明显的口误或同音错字。\n"
        "3. 输出直接给 Markdown 正文，不要解释你是怎么做的。\n\n"
    )
    if template.strip():
        normalized_template = template.strip()
        if "{asr}" in normalized_template or "{{asr}}" in normalized_template:
            custom_body = normalized_template.replace("{{asr}}", source_text).replace("{asr}", source_text)
            return "请按照下面的自定义整理模板处理这份 SenseAudio ASR。\n\n" + common_rules + "自定义模板：\n" + custom_body
        return (
            "请按照下面的自定义整理模板处理这份 SenseAudio ASR。\n\n"
            + common_rules
            + "自定义模板：\n"
            + normalized_template
            + "\n\n原始 ASR 如下：\n"
            + source_text
        )
    mode_prompts = {
        "summary": (
            "请把下面这份 SenseAudio ASR 结果整理成一份清晰、可直接阅读的中文 Markdown 项目纪要。\n\n"
            "输出结构：\n"
            "1. 一句话摘要\n"
            "2. 关键信息\n"
            "3. 整理稿\n"
            "4. 关键词\n"
            "5. 待办/结论\n\n"
        ),
        "keywords": (
            "请从下面这份 SenseAudio ASR 结果中提取最有价值的关键信息，并整理成一份中文 Markdown。\n\n"
            "输出结构：\n"
            "1. 一句话摘要\n"
            "2. 关键词（8-15个）\n"
            "3. 关键事实/数字/对象\n"
            "4. 可行动信息\n\n"
        ),
        "meeting": (
            "请把下面这份 SenseAudio ASR 结果整理成一份会议纪要风格的中文 Markdown。\n\n"
            "输出结构：\n"
            "1. 会议主题\n"
            "2. 核心结论\n"
            "3. 讨论要点\n"
            "4. 决策事项\n"
            "5. 待办事项（责任人未知就不要编造）\n\n"
        ),
        "study": (
            "请把下面这份 SenseAudio ASR 结果整理成一份学习笔记风格的中文 Markdown。\n\n"
            "输出结构：\n"
            "1. 本段主要内容\n"
            "2. 知识点整理\n"
            "3. 关键概念/术语\n"
            "4. 值得复习的问题\n\n"
        ),
        "todo": (
            "请把下面这份 SenseAudio ASR 结果专门整理成“待办与行动项提取”风格的中文 Markdown。\n\n"
            "输出结构：\n"
            "1. 一句话摘要\n"
            "2. 明确待办\n"
            "3. 隐含行动项\n"
            "4. 风险/阻塞\n"
            "5. 仍需确认的问题\n\n"
        ),
    }
    return mode_prompts[mode] + common_rules + f"原始 ASR 如下：\n{source_text}"


def default_output_path(run_dir: Path, mode: str) -> Path:
    filename_map = {
        "summary": "organized_notes.md",
        "keywords": "keywords_notes.md",
        "meeting": "meeting_notes.md",
        "study": "study_notes.md",
        "todo": "todo_notes.md",
    }
    return run_dir / filename_map[mode]


def isolated_audioclaw_home(transcript_path: Path) -> Path:
    root = transcript_path.parents[4]
    home = root / "state" / "realtime_interpreter" / "audioclaw_organizer_home"
    workspace = home / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    source_config = Path.home() / ".audioclaw" / "config.json"
    target_config = home / "config.json"
    if source_config.exists():
        config = json.loads(source_config.read_text(encoding="utf-8"))
        defaults = config.setdefault("agents", {}).setdefault("defaults", {})
        defaults["workspace"] = str(workspace)
        defaults["max_tokens"] = min(int(defaults.get("max_tokens") or 4096), 4096)
        defaults["summarize_message_threshold"] = 4
        target_config.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    elif not target_config.exists():
        raise SystemExit("AudioClaw config not found in the configured AudioClaw home.")

    sessions = workspace / "sessions"
    if sessions.exists():
        for item in sessions.glob("agent_main_main*"):
            try:
                item.unlink()
            except OSError:
                pass
    return home


def main() -> int:
    args = parse_args()
    transcript_path = Path(args.transcript_json).expanduser().resolve()
    payload = json.loads(transcript_path.read_text(encoding="utf-8"))
    template = load_template(args.template_file)
    prompt = build_prompt(payload, args.mode, template)
    agent_bin = resolve_agent_bin(args.agent_bin)
    run_dir = transcript_path.parent
    session = args.session.strip() or f"realtime_interpreter_{args.mode}_{run_dir.name}"
    output_markdown = Path(args.output_markdown).expanduser().resolve() if args.output_markdown else default_output_path(run_dir, args.mode)

    command = [
        str(agent_bin),
        "agent",
        "--debug",
        "--session",
        session,
        "--message",
        prompt,
    ]
    env = dict(**os.environ)
    organizer_home = isolated_audioclaw_home(transcript_path)
    env["AUDIOCLAW_HOME"] = str(organizer_home)
    completed = subprocess.run(command, capture_output=True, text=True, check=False, env=env)
    if completed.returncode != 0:
        sys.stderr.write((completed.stderr or completed.stdout or "audioclaw agent failed").strip() + "\n")
        return completed.returncode or 1

    session_reply = extract_agent_reply_from_session(organizer_home)
    reply_source = "audioclaw_session" if session_reply else "process_output"
    reply = session_reply or extract_agent_reply(completed.stdout)
    if not reply:
        sys.stderr.write("Could not extract organizer reply from audioclaw output.\n")
        return 1

    output_markdown.write_text(reply.strip() + "\n", encoding="utf-8")
    manifest = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "mode": args.mode,
        "session": session,
        "transcript_json": str(transcript_path),
        "output_markdown": str(output_markdown),
        "agent_bin": str(agent_bin),
        "template_file": str(Path(args.template_file).expanduser().resolve()) if args.template_file.strip() else "",
        "template_used": bool(template),
        "reply_source": reply_source,
    }
    (run_dir / f"{output_markdown.stem}.meta.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
