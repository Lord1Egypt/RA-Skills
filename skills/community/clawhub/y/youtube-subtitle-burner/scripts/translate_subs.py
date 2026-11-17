#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Translate subtitle segments from English to Chinese using an LLM.

This is a helper script that formats subtitle segments for LLM translation.
It reads segments with 'text_zh_src' field, batches them, and outputs
segments with 'text_zh' field added.

Usage:
    # Use with an LLM API (requires OPENAI_API_KEY or similar)
    uv run translate_subs.py INPUT_segments.json OUTPUT_translated.json

    # Just format for manual translation (prints batches)
    uv run translate_subs.py INPUT_segments.json --print-only

Translation rules (baked into the LLM prompt):
    - Concise translations suitable for video subtitles (≤20 Chinese chars per segment)
    - Remove [music] and other tag placeholders
    - Keep proper nouns untranslated (Claude, YouTube, Reddit, etc.)
    - Natural, fluent Chinese

Note: For agent-based workflows (Hermes, Claude Code), you can also translate
inline using the agent's LLM instead of running this script separately.
"""
import json
import argparse
import sys
import os

# LLM translation prompt template
TRANSLATION_PROMPT = """Translate the following English subtitle segments into Chinese.
Rules:
1. Concise, natural Chinese suitable for video subtitles (≤20 chars per segment)
2. Remove [music] and similar tags
3. Keep proper nouns untranslated (Claude, YouTube, Reddit, Twitter, etc.)
4. Output ONLY the translated text, one line per segment, preserving order

Segments:
{segments}
"""


def load_segments(filepath):
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def format_batches(segments, batch_size=20):
    """Split segments into batches for LLM processing."""
    batches = []
    for i in range(0, len(segments), batch_size):
        batch = segments[i:i + batch_size]
        lines = []
        for j, s in enumerate(batch):
            lines.append(f"{i + j}: {s['text_zh_src']}")
        batches.append({
            "indices": list(range(i, min(i + batch_size, len(segments)))),
            "prompt": TRANSLATION_PROMPT.format(segments="\n".join(lines))
        })
    return batches


def translate_with_agent(segments):
    """
    Format segments for agent-based translation.
    Returns batches ready for LLM processing.
    The agent should translate each text_zh_src → text_zh.
    """
    batches = format_batches(segments)
    print(f"Total segments: {len(segments)}")
    print(f"Batches: {len(batches)}")
    print()
    for i, batch in enumerate(batches):
        print(f"=== BATCH {i} ({len(batch['indices'])} segments) ===")
        for idx in batch["indices"]:
            s = segments[idx]
            print(f"{s['start']:.2f}|{s['end']:.2f}|{s['text_zh_src']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Translate subtitle segments EN→ZH")
    parser.add_argument("input", help="Input segments JSON")
    parser.add_argument("output", nargs="?", help="Output translated JSON (omit for --print-only)")
    parser.add_argument("--print-only", action="store_true",
                        help="Print batches for manual/agent translation")
    parser.add_argument("--batch-size", type=int, default=20,
                        help="Segments per batch (default: 20)")
    args = parser.parse_args()

    segments = load_segments(args.input)
    print(f"Loaded {len(segments)} segments")

    if args.print_only:
        translate_with_agent(segments)
        return

    if not args.output:
        print("ERROR: output file required (or use --print-only)", file=sys.stderr)
        sys.exit(1)

    # For agent-based workflows: translate using the agent's LLM capability
    # This script provides the batching; actual translation should be done
    # by calling the LLM with each batch prompt.
    #
    # In an agent context (Hermes/Claude Code), the recommended approach is:
    # 1. Run this script with --print-only to see batches
    # 2. Translate each batch using the agent's LLM
    # 3. Write the final translated.json with text_zh fields
    #
    # For standalone use, integrate with your preferred LLM API here.

    print("\n⚠️  This script formats batches for translation.")
    print("For agent-based translation:")
    print("  1. Run with --print-only to see batches")
    print("  2. Translate using your LLM")
    print("  3. Save output with text_zh fields")
    print()

    # Output a template for manual filling
    template = []
    for s in segments:
        template.append({
            "start": s["start"],
            "end": s["end"],
            "text_zh_src": s.get("text_zh_src", ""),
            "text_zh": ""  # Fill in translation
        })

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    print(f"Template written to {args.output} (fill text_zh fields)")


if __name__ == "__main__":
    main()
