#!/usr/bin/env python3
"""Backward-compatible image entry point; use showmeai.py image for new integrations."""

from __future__ import annotations

import sys

from showmeai import main


def legacy_args(argv: list[str]) -> list[str]:
    translated: list[str] = ["image"]
    skip = {"--save", "--oss"}
    index = 0
    while index < len(argv):
        item = argv[index]
        if item in skip:
            index += 1
            continue
        if item == "--input":
            translated.append("--input")
        elif item == "--format":
            translated.append("--output-format")
        else:
            translated.append(item)
        index += 1
    return translated


if __name__ == "__main__":
    raise SystemExit(main(legacy_args(sys.argv[1:])))
