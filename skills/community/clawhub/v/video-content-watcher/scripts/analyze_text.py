#!/usr/bin/env python3
"""Analyze raw text directly - skip video/audio processing"""

import sys
from pathlib import Path

# MCP project location
SKILL_ROOT = Path(__file__).resolve().parents[4]  # /home/ykl/.openclaw/
MCP_PATH = SKILL_ROOT / "workspace-code-dev" / "video-reader"
sys.path.insert(0, str(MCP_PATH / "src"))

from video_reader_mcp import VideoReaderMCP


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_text.py '<text to analyze>'")
        sys.exit(1)

    text = sys.argv[1]
    mcp = VideoReaderMCP()
    result = mcp.analyze_text(text)
    print(result.get("report", result.get("analysis", "No output")))


if __name__ == "__main__":
    main()
