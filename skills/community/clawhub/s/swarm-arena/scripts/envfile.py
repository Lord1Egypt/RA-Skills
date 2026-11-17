#!/usr/bin/env python3
"""envfile.py — minimal .env loader, stdlib only.

load(path) reads KEY=VALUE lines ('#' comments and blanks skipped, optional
matching single/double quotes stripped, no expansion) into os.environ. Names already present in the environment always
win — the file only fills what is missing. Returns the number of vars set.
"""

import os


def load(path):
    try:
        with open(path) as f:
            lines = f.readlines()
    except OSError:
        return 0
    count = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key and key not in os.environ:
            os.environ[key] = value
            count += 1
    return count
