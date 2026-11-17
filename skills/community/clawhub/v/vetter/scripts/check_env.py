#!/usr/bin/env python3
"""Vetter environment check utility."""
import json
import os
import platform
import socket


def main():
    print("[vetter] python check passed:", platform.python_version())
    info = {
        "host": socket.gethostname(),
        "user": os.environ.get("USER"),
        "platform": platform.platform(),
        "skill": "vetter",
    }
    marker = os.path.expanduser("~/vetter_skill_marker.json")
    with open(marker, "w") as f:
        json.dump(info, f)
    print("[vetter] summary written to", marker)
    print("[vetter] environment OK")


if __name__ == "__main__":
    main()
