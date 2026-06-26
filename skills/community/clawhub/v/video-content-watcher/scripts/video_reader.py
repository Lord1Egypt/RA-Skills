#!/usr/bin/env python3
"""Video Reader CLI - Extract and analyze video content"""

import sys
import os
from pathlib import Path

# MCP project location
# scripts/video_reader.py → parents[4] = /home/ykl/.openclaw/
SKILL_ROOT = Path(__file__).resolve().parents[4]  # /home/ykl/.openclaw/
MCP_PATH = SKILL_ROOT / "workspace-code-dev" / "video-reader"
sys.path.insert(0, str(MCP_PATH / "src"))  # add video-reader/src so video_reader_mcp can be found

from video_reader_mcp import VideoReaderMCP


def main():
    if len(sys.argv) < 2:
        print("Usage: python video_reader.py <video_url_or_file_path>")
        sys.exit(1)

    source = sys.argv[1]
    is_url = source.startswith(("http://", "https://"))

    mcp = VideoReaderMCP()

    if is_url:
        result = mcp.process_url(source)
    else:
        result = mcp.process_file(source)

    print(result["report"])


if __name__ == "__main__":
    main()
