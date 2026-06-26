#!/usr/bin/env python3
"""
Extract key learnings and context from current session.

Usage:
    python extract_session.py --session ~/.openclaw/agents/main/sessions/abc123.jsonl
    python extract_session.py --session ~/.openclaw/agents/main/sessions/abc123.jsonl --output summary.md
"""

import argparse
import json
from pathlib import Path
from collections import defaultdict


def extract_user_messages(session_path: Path) -> list:
    """Extract user messages from session."""
    messages = []
    with open(session_path) as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            if data.get("message", {}).get("role") == "user":
                for content in data.get("message", {}).get("content", []):
                    if content.get("type") == "text":
                        messages.append(content.get("text", ""))
    return messages


def extract_tool_usage(session_path: Path) -> dict:
    """Extract tool usage statistics."""
    tools = defaultdict(int)
    with open(session_path) as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            for content in data.get("message", {}).get("content", []):
                if content.get("type") == "toolCall":
                    tool_name = content.get("name", "unknown")
                    tools[tool_name] += 1
    return dict(tools)


def extract_files_touched(session_path: Path) -> set:
    """Extract files that were read or written."""
    files = set()
    with open(session_path) as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            for content in data.get("message", {}).get("content", []):
                if content.get("type") == "toolCall":
                    tool_input = content.get("input", {})
                    # Check for file_path in various tool inputs
                    if "file_path" in tool_input:
                        files.add(tool_input["file_path"])
                    elif "path" in tool_input:
                        files.add(tool_input["path"])
    return files


def get_session_metadata(session_path: Path) -> dict:
    """Get session start/end times and message count."""
    first_timestamp = None
    last_timestamp = None
    message_count = 0

    with open(session_path) as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            timestamp = data.get("timestamp")
            if data.get("type") == "message":
                message_count += 1
                if not first_timestamp:
                    first_timestamp = timestamp
                last_timestamp = timestamp

    return {
        "start": first_timestamp,
        "end": last_timestamp,
        "messages": message_count
    }


def generate_summary(session_path: Path) -> str:
    """Generate session summary."""
    metadata = get_session_metadata(session_path)
    user_messages = extract_user_messages(session_path)
    tools = extract_tool_usage(session_path)
    files = extract_files_touched(session_path)

    summary = f"""# Session Summary

**Date:** {metadata['start'][:10] if metadata['start'] else 'Unknown'}
**Duration:** {metadata['start'][:16] if metadata['start'] else '?'} to {metadata['end'][11:16] if metadata['end'] else '?'}
**Messages:** {metadata['messages']}

## User Requests

"""
    for i, msg in enumerate(user_messages[:10], 1):  # First 10 requests
        preview = msg[:100] + "..." if len(msg) > 100 else msg
        summary += f"{i}. {preview}\n"

    if len(user_messages) > 10:
        summary += f"\n... and {len(user_messages) - 10} more requests\n"

    summary += "\n## Tools Used\n\n"
    for tool, count in sorted(tools.items(), key=lambda x: x[1], reverse=True):
        summary += f"- **{tool}**: {count} calls\n"

    if files:
        summary += "\n## Files Touched\n\n"
        for file in sorted(files)[:20]:  # First 20 files
            summary += f"- `{file}`\n"
        if len(files) > 20:
            summary += f"\n... and {len(files) - 20} more files\n"

    summary += """
## Key Learnings

<!-- Extract and document key insights from this session -->

-

## Context to Preserve

<!-- Important context that should be remembered -->

-
"""

    return summary


def main():
    parser = argparse.ArgumentParser(description="Extract session summary")
    parser.add_argument("--session", required=True, help="Session JSONL file path")
    parser.add_argument("--output", help="Output file (default: stdout)")

    args = parser.parse_args()

    session_path = Path(args.session).expanduser()
    if not session_path.exists():
        print(f"Error: Session not found: {session_path}")
        return 1

    summary = generate_summary(session_path)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(summary)
        print(f"Summary written to: {output_path}")
    else:
        print(summary)


if __name__ == "__main__":
    main()
