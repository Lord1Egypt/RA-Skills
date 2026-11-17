#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic review rules for yotta-dev-mcp.

This file is rule data: it contains the literal markers the engine must
detect, and is exempted by the project publish preflight in the same way as
other signature rule tables.
"""

import re

REVIEW_RULES = [
    ("bare-except", "medium", re.compile(r"^\s*except\s*:"),
     "Catch a specific exception instead of a bare except."),
    ("eval-exec", "high", re.compile(r"(?<![\w.$])(?:eval|exec)\s*\("),
     "Avoid dynamic evaluation; use explicit parsing or dispatch."),
    ("shell-true", "high", re.compile(r"\bshell\s*=\s*True\b"),
     "Do not invoke a shell with untrusted input; pass an argument list."),
    ("debug-print", "low", re.compile(r"^\s*print\s*\("),
     "Replace debug output with structured logging or remove it."),
    ("todo-comment", "info", re.compile(r"\b(?:TODO|FIXME)\b"),
     "Track the unfinished work or remove the stale marker."),
    ("mutable-default", "medium", re.compile(r"def\s+\w+\s*\([^)]*=\s*(?:\[\]|\{\})"),
     "Use None as the default and create the mutable value inside the function."),
]
