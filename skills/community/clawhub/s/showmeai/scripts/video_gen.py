#!/usr/bin/env python3
"""Backward-compatible video entry point; waits until the final file is downloaded."""

from __future__ import annotations

import sys

from showmeai import main


def legacy_args(argv: list[str]) -> list[str]:
    translated: list[str] = ["video"]
    for item in argv:
        if item in {"--save"}:
            continue
        translated.append(item)
    return translated


if __name__ == "__main__":
    raise SystemExit(main(legacy_args(sys.argv[1:])))
