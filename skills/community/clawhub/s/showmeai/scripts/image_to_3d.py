#!/usr/bin/env python3
"""Backward-compatible image-to-3D entry point with fixed query mode."""

from __future__ import annotations

import sys

from showmeai import main


def legacy_args(argv: list[str]) -> list[str]:
    translated: list[str] = ["3d"]
    for item in argv:
        if item == "--save":
            continue
        translated.append(item)
    return translated


if __name__ == "__main__":
    raise SystemExit(main(legacy_args(sys.argv[1:])))
