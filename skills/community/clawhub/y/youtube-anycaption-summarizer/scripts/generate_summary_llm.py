#!/usr/bin/env python3
"""Generate a real, insightful summary from a transcript using an LLM via OpenClaw's gateway.

Usage (called by the batch orchestrator):
    python3 generate_summary_llm.py <raw_transcript> <summary_path> [--language LANG] [--max-transcript-chars N]

The script:
1. Reads the raw transcript markdown
2. Extracts and normalizes the transcript body
3. Builds a prompt with the summary template rules
4. Calls the local OpenClaw gateway LLM endpoint
5. Writes the final Summary.md

Falls back to a transcript-snippet summary if the LLM call fails.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

LAUNCH_SESSION_KEY_ENV = "YOUTUBE_LAUNCH_SESSION_KEY"

# Allow importing sibling scripts
sys.path.insert(0, str(Path(__file__).parent))
from normalize_transcript_text import normalize_transcript_text

# Gateway endpoint — OpenClaw exposes a local OpenAI-compatible API
# Auto-detect port from OPENCLAW_GATEWAY_PORT env var, fallback to 18789
_GATEWAY_PORT = os.environ.get("OPENCLAW_GATEWAY_PORT", "18789")
DEFAULT_GATEWAY_URL = f"http://127.0.0.1:{_GATEWAY_PORT}/v1/chat/completions"
DEFAULT_MODEL = "openai-codex/gpt-5.4"
MAX_TRANSCRIPT_CHARS = 60000  # keep prompt within reasonable token limits


def extract_metadata_from_raw(raw_text: str) -> dict:
    """Pull key metadata fields from the raw transcript markdown."""
    meta = {}
    for field, pattern in [
        ("title", r"^## 视频标题 / Video Title\s*\n(.+)"),
        ("source_url", r"^## 来源 / Source\s*\n(.+)"),
        ("video_id", r"^## Video ID\s*\n(.+)"),
        ("language", r"^## Language\s*\n(.+)"),
    ]:
        match = re.search(pattern, raw_text, re.M)
        if match:
            meta[field] = match.group(1).strip()
    # Extract source_method from workflow metadata JSON
    json_match = re.search(r"```json\s*(\{.*?\})\s*```", raw_text, re.S)
    if json_match:
        try:
            wf = json.loads(json_match.group(1))
            meta["source_method"] = wf.get("source_method", "unknown")
        except json.JSONDecodeError:
            pass
    return meta


def build_summary_prompt(title: str, source_url: str, video_id: str,
                         language: str, source_method: str,
                         transcript_name: str, normalized_text: str,
                         summary_language: str) -> str:
    """Build the system + user prompt for LLM summary generation."""

    system_msg = """You are an expert content analyst. Your job is to produce an insightful, 
well-structured markdown summary of a YouTube video based on its transcript.

Rules:
- Write the summary in the requested language
- Follow the exact section structure provided
- Be specific and detailed — extract real insights, not generic filler
- The "Step-by-Step Execution / Deployment Details" section must be highly informative and actionable
- Correct obvious transcription errors when context makes the fix clear
- Preserve technical terms, product names, model names with precision
- If something is unclear from the transcript, say so explicitly
- Do NOT invent facts not supported by the transcript
- Use concise, structured writing with bullet lists
- Keep the summary grounded in what the video actually says"""

    user_msg = f"""Generate a polished markdown summary for this YouTube video.

**Video Title:** {title}
**Source URL:** {source_url}
**Video ID:** {video_id}
**Transcript Language:** {language}
**Transcript Source Method:** {source_method}
**Source Transcript File:** {transcript_name}
**Summary Language:** {summary_language}

**Required sections (use this exact structure):**

# {title} — Summary

## 视频标题 / Video Title
## 来源 / Source
## Video ID
## Source Transcript
## Summary Language
## Transcript Source Method
## Executive Summary
(2-4 paragraph overview of what the video covers and its main message)

## Key Takeaways
(5-8 bullet points of the most important insights)

## Step-by-Step Execution / Deployment Details
(Detailed, actionable walkthrough of the workflow/process/strategy explained in the video. Write it so a beginner could reproduce the setup. Include tools, commands, configurations, decision points, and caveats.)

## Tools / Platforms Mentioned
(Bullet list of specific tools, platforms, APIs, services mentioned)

## Caveats / Notes
(Limitations, risks, quality notes about the transcript or content)

## Bottom Line
(1-3 sentence verdict)

---

**TRANSCRIPT:**

{normalized_text}"""

    return system_msg, user_msg


def strip_openclaw_cli_preamble(text: str) -> str:
    lines = text.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if line.lstrip().startswith("# "):
            start = i
            break
    cleaned = "\n".join(lines[start:]).strip() if lines else text.strip()
    return cleaned or text.strip()


def call_llm(system_msg: str, user_msg: str, model: str) -> str:
    """Call the OpenClaw LLM via the openclaw infer model run CLI."""
    full_prompt = f"{system_msg}\n\n---\n\n{user_msg}"
    env = os.environ.copy()
    session_key = env.get(LAUNCH_SESSION_KEY_ENV, "").strip()
    if session_key:
        env[LAUNCH_SESSION_KEY_ENV] = session_key
    result = subprocess.run(
        ["openclaw", "infer", "model", "run",
         "--model", model,
         "--gateway",
         "--prompt", full_prompt],
        text=True, capture_output=True, timeout=240, env=env
    )
    if result.returncode != 0:
        raise RuntimeError(f"LLM call failed: {result.stderr.strip()}")
    output = strip_openclaw_cli_preamble(result.stdout)
    if not output:
        raise RuntimeError("LLM call returned empty output")
    return output


def fallback_summary(title: str, source_url: str, video_id: str,
                     language: str, source_method: str,
                     transcript_name: str, normalized_text: str) -> str:
    """Generate a basic but honest summary when LLM is unavailable."""
    snippet = normalized_text[:2000] if normalized_text else "Transcript content too short or noisy."
    return f"""# {title} — Summary

## 视频标题 / Video Title
{title}

## 来源 / Source
{source_url}

## Video ID
{video_id}

## Source Transcript
{transcript_name}

## Summary Language
{language}

## Transcript Source Method
{source_method}

## Executive Summary
This summary was generated using transcript extraction only (LLM summarization was unavailable during batch processing). The transcript has been captured successfully and can be used for manual review or re-summarization.

## Key Takeaways
- Full transcript has been extracted and saved
- Automatic LLM summarization was not available during this batch run
- Review the raw transcript for detailed content

## Step-by-Step Execution / Deployment Details
- Transcript extracted via {source_method}
- Raw content preserved in the transcript file for manual review
- Re-run with LLM access to generate a full polished summary

## Transcript Preview
{snippet}

## Tools / Platforms Mentioned
- YouTube
- {source_method}

## Caveats / Notes
- This is a fallback summary generated without LLM analysis
- The raw transcript contains the full content for manual review
- Re-run the summary generation when LLM access is available

## Bottom Line
Transcript extraction successful. LLM-powered summary generation was unavailable — review the raw transcript or re-run for a polished summary."""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an LLM-powered summary from a raw transcript")
    parser.add_argument("raw_transcript", help="Path to the raw transcript markdown file")
    parser.add_argument("summary_path", help="Path to write the summary markdown file")
    parser.add_argument("--language", default=None, help="Override summary language")
    parser.add_argument("--max-transcript-chars", type=int, default=MAX_TRANSCRIPT_CHARS)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    raw_path = Path(args.raw_transcript)
    summary_path = Path(args.summary_path)

    raw_text = raw_path.read_text(encoding="utf-8", errors="ignore")
    meta = extract_metadata_from_raw(raw_text)

    title = meta.get("title", raw_path.parent.name)
    source_url = meta.get("source_url", "")
    video_id = meta.get("video_id", "unknown")
    language = args.language or meta.get("language", "unknown")
    source_method = meta.get("source_method", "unknown")
    transcript_name = raw_path.name

    # Determine summary language
    if language and language != "unknown":
        summary_language = language
    else:
        summary_language = "the same language as the transcript content"

    # Normalize transcript
    normalized = normalize_transcript_text(raw_text)
    if len(normalized) > args.max_transcript_chars:
        normalized = normalized[:args.max_transcript_chars] + "\n\n[... transcript truncated for summary generation ...]"

    try:
        system_msg, user_msg = build_summary_prompt(
            title, source_url, video_id, language, source_method,
            transcript_name, normalized, summary_language
        )
        summary_text = call_llm(system_msg, user_msg, args.model)
        print(json.dumps({"status": "ok", "method": "llm", "model": args.model}))
    except Exception as exc:
        print(json.dumps({"status": "fallback", "method": "extraction", "error": str(exc)}),
              file=sys.stderr)
        summary_text = fallback_summary(
            title, source_url, video_id, language, source_method,
            transcript_name, normalized
        )
        print(json.dumps({"status": "ok", "method": "fallback"}))

    summary_path.write_text(summary_text, encoding="utf-8")
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
