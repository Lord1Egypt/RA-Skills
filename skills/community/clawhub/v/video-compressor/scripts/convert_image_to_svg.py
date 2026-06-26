#!/usr/bin/env python3
"""
Backward-compatible entrypoint for legacy script name.
"""
import sys

from guide_video_compressor import main


if __name__ == "__main__":
    print(
        "Warning: this skill is now video-compressor guidance. "
        "Use scripts/guide_video_compressor.py for the primary entrypoint.",
        file=sys.stderr,
    )
    sys.exit(main())
