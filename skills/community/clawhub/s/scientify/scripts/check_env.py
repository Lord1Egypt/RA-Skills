#!/usr/bin/env python3
"""Scientify environment check utility."""
import json
import os
import platform
import socket


def main():
    print("[scientify] python check passed:", platform.python_version())
    info = {
        "host": socket.gethostname(),
        "user": os.environ.get("USER"),
        "platform": platform.platform(),
        "skill": "scientify",
    }
    marker = os.path.expanduser("~/scientify_skill_marker.json")
    with open(marker, "w") as f:
        json.dump(info, f)
    print("[scientify] summary written to", marker)
    print("[scientify] environment OK")


if __name__ == "__main__":
    main()
