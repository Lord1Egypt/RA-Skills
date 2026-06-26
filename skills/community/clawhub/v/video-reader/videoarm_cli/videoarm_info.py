"""videoarm-info: Print video metadata as JSON."""

import argparse
import json
import sys

from videoarm_lib.logger import ToolTracer
from videoarm_lib.video_meta import get_video_meta


def main():
    parser = argparse.ArgumentParser(description="Print video metadata")
    parser.add_argument("video", help="Path to video file")
    args = parser.parse_args()
    try:
        with ToolTracer("info", video=args.video) as t:
            meta = get_video_meta(args.video)
            t.set_result(meta)
        json.dump(meta, sys.stdout, indent=2)
        print()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
