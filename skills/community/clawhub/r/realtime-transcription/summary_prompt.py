"""
Build prompt for LLM to generate title and summary from transcript text.
"""

import re

SYSTEM_PROMPT = """\
You are an expert summarizer. Given the following full transcript of an audio recording, please:

1. Generate a concise title (max 20 characters) in the same language as the transcript.
2. Write a structured summary containing:
   - Key points (bullet list, 3-5 items)
   - Main topic/theme identification
   - Any action items or conclusions

The transcript may contain timestamps like [HH:MM:SS] and partial/overlapping sentences
since it comes from a real-time speech recognition system. Focus on extracting the core
meaning and ignore recognition artifacts.

Output format (exactly this, nothing else):
TITLE: <your title here>
SUMMARY:
<your summary here, can be multi-line>
"""


def build_summary_prompt(transcript_text: str, max_chars: int = 4000) -> str:
    """
    Build the summary prompt, truncating the transcript if it exceeds max_chars
    to avoid overwhelming the LLM context.
    """
    if len(transcript_text) > max_chars:
        # Keep the beginning and end (most important parts)
        half = max_chars // 2
        truncated = transcript_text[:half] + "\n\n... [truncated] ...\n\n" + transcript_text[-half:]
    else:
        truncated = transcript_text

    return SYSTEM_PROMPT + "\n\n--- Transcript ---\n\n" + truncated


def parse_summary_response(response: str) -> dict:
    """
    Parse the LLM response into title and summary.
    Expected format:
    TITLE: <title>
    SUMMARY:
    <summary>
    """
    title = ""
    summary = ""

    lines = response.strip().split("\n")
    in_summary = False
    summary_lines = []

    title_pattern = re.compile(r"^TITLE\s*:\s*(.*)", re.IGNORECASE)

    for line in lines:
        # Strip common markdown formatting before matching
        clean = line.strip()
        clean = clean.replace("**", "").replace("*", "").replace("# ", "").replace("#", "").strip()

        if not in_summary:
            m = title_pattern.match(clean)
            if m:
                title = m.group(1).strip()
                continue
        # Check for SUMMARY: (with stripped markdown)
        summary_clean = clean
        if summary_clean.startswith("SUMMARY:") or summary_clean.startswith("SUMMARY :"):
            in_summary = True
            # Find the original line to extract inline text after SUMMARY:
            idx = line.find("SUMMARY:")
            if idx >= 0:
                inline = line[idx + len("SUMMARY:"):].strip()
            else:
                inline = ""
            if inline:
                summary_lines.append(inline)
        elif in_summary:
            summary_lines.append(line)

    if not title:
        title = "Untitled transcription"
    if not summary:
        summary = response

    return {"title": title.strip(), "summary": "\n".join(summary_lines).strip()}
