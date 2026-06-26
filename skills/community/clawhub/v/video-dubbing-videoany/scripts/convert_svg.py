#!/usr/bin/env python3
"""
Backward-compatible entrypoint for legacy script name.
"""
import sys

from guide_video_dubbing import main


if __name__ == "__main__":
    print(
        "Warning: this skill is now video-dubbing guidance. "
        "Use scripts/guide_video_dubbing.py for the primary entrypoint.",
        file=sys.stderr,
    )
    sys.exit(main())
