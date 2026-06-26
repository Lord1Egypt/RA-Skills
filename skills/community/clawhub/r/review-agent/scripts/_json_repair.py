#!/usr/bin/env python3
"""Lenient JSON parser for LLM-generated output.

LLMs regularly emit JSON with the following defects:
  1. Markdown code fence wrapping (```json ... ```)
  2. Prose before/after the JSON body
  3. Unescaped newlines inside string values
  4. Unescaped double quotes inside string values (e.g., 他说："好"。)
  5. Trailing commas
  6. Comments (// ...) inside the JSON

This module tries progressively harder to parse, so the main scripts don't have
to duplicate fixes. Primary entry: `parse_lenient_json(text, expected="object"|"array"|"any")`.

Exposes `(parsed_value, error_string_or_None)` tuple.
"""
from __future__ import annotations
import json
import re
from typing import Any, Optional, Tuple


def _strip_code_fence(text: str) -> str:
    m = re.search(r"```(?:json|jsonc|json5)?\s*(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1)
    return text


def _extract_outermost(text: str, kind: str) -> Optional[str]:
    """Find the outermost { ... } or [ ... ] block.
    kind: 'object' | 'array' | 'any'.
    """
    candidates = []
    if kind in ("object", "any"):
        s = text.find("{"); e = text.rfind("}")
        if s >= 0 and e > s: candidates.append((s, e, "{", "}"))
    if kind in ("array", "any"):
        s = text.find("["); e = text.rfind("]")
        if s >= 0 and e > s: candidates.append((s, e, "[", "]"))
    if not candidates:
        return None
    # Prefer the candidate that starts earliest
    candidates.sort(key=lambda x: x[0])
    s, e, _, _ = candidates[0]
    return text[s:e+1]


def _fix_newlines_in_strings(s: str) -> str:
    """Replace bare \\n\\r inside quoted string values with their escaped forms."""
    def _repl(mo):
        return mo.group(0).replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    # Match a string (handles already-escaped quotes via \\.)
    return re.sub(r'"(?:[^"\\]|\\.)*"', _repl, s, flags=re.DOTALL)


def _fix_unescaped_inner_quotes(s: str) -> str:
    """Walk char-by-char; inside a string, if a `"` is not followed by JSON
    structural whitespace/char (, } ] : end-of-input), treat it as literal and
    escape it. This catches the common case:
        {"reply_text": "她说："好"，我同意。"}
    which Python's json module would fail on.
    """
    out: list[str] = []
    i, n = 0, len(s)
    in_string = False
    while i < n:
        c = s[i]
        if not in_string:
            out.append(c)
            if c == '"':
                in_string = True
            i += 1
            continue
        # inside string
        if c == "\\":
            # escape sequence: pass through current and next char verbatim
            out.append(c)
            if i + 1 < n:
                out.append(s[i+1])
                i += 2
            else:
                i += 1
            continue
        if c == '"':
            # is this a real closing quote, or an unescaped inner quote?
            j = i + 1
            while j < n and s[j] in " \t\n\r":
                j += 1
            if j >= n or s[j] in ",}]:":
                # real closing
                out.append(c)
                in_string = False
                i += 1
            else:
                # unescaped inner quote — escape it
                out.append("\\")
                out.append(c)
                i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _strip_trailing_commas(s: str) -> str:
    # Remove commas immediately before a } or ]
    return re.sub(r",(\s*[}\]])", r"\1", s)


def _strip_line_comments(s: str) -> str:
    # Remove // ... line comments, but only when NOT inside a string.
    # Simple heuristic: track string state.
    out = []
    i, n = 0, len(s)
    in_string = False
    while i < n:
        c = s[i]
        if not in_string:
            if c == '"':
                out.append(c); in_string = True; i += 1; continue
            if c == "/" and i + 1 < n and s[i+1] == "/":
                # skip to end of line
                while i < n and s[i] != "\n":
                    i += 1
                continue
            out.append(c); i += 1
        else:
            if c == "\\" and i + 1 < n:
                out.append(c); out.append(s[i+1]); i += 2; continue
            if c == '"':
                out.append(c); in_string = False; i += 1; continue
            out.append(c); i += 1
    return "".join(out)


def parse_lenient_json(text: str, expected: str = "any") -> Tuple[Optional[Any], Optional[str]]:
    """Parse LLM-generated JSON, applying repair passes as needed.

    expected: 'object' | 'array' | 'any'
    Returns (parsed, error_message_or_None).
    """
    original_text = text or ""
    if not original_text.strip():
        return None, "empty input"

    # Pass 0: strip code fences, extract outermost block
    stripped = _strip_code_fence(original_text)
    body = _extract_outermost(stripped, expected)
    if body is None:
        return None, f"no outer {expected} block found"

    # Pass 1: as-is
    try:
        v = json.loads(body)
        if _type_ok(v, expected):
            return v, None
    except json.JSONDecodeError:
        pass

    # Pass 2: fix newlines inside strings
    try:
        fixed = _fix_newlines_in_strings(body)
        v = json.loads(fixed)
        if _type_ok(v, expected):
            return v, None
    except json.JSONDecodeError:
        pass

    # Pass 3: strip trailing commas + line comments
    try:
        fixed = _strip_trailing_commas(_strip_line_comments(body))
        v = json.loads(fixed)
        if _type_ok(v, expected):
            return v, None
    except json.JSONDecodeError:
        pass

    # Pass 4: escape unescaped inner quotes (heuristic)
    try:
        fixed = _fix_unescaped_inner_quotes(body)
        v = json.loads(fixed)
        if _type_ok(v, expected):
            return v, None
    except json.JSONDecodeError:
        pass

    # Pass 5: combined — all repairs stacked
    try:
        fixed = _strip_trailing_commas(
            _strip_line_comments(
                _fix_unescaped_inner_quotes(
                    _fix_newlines_in_strings(body)
                )
            )
        )
        v = json.loads(fixed)
        if _type_ok(v, expected):
            return v, None
    except json.JSONDecodeError as e:
        return None, f"failed after 5 repair passes: {e}; body head: {body[:300]}"
    return None, "parse exhausted all passes"


def _type_ok(v: Any, expected: str) -> bool:
    if expected == "any": return True
    if expected == "object" and isinstance(v, dict): return True
    if expected == "array" and isinstance(v, list): return True
    return False


# Self-test
if __name__ == "__main__":
    import sys
    tests = [
        # (input, expected_type, should_succeed)
        ('{"a": 1}', "object", True),
        ('```json\n{"a": 1}\n```', "object", True),
        ('here is the result:\n{"a": 1}\nthanks!', "object", True),
        ('{"text": "line one\nline two"}', "object", True),  # unescaped newline
        ('{"text": "她说："好"，我同意"}', "object", True),  # unescaped inner quotes
        ('[{"a": 1}, {"b": 2},]', "array", True),  # trailing comma
        ('{"a": 1, // comment\n"b": 2}', "object", True),
        ('```\n{"x": "multi\nline with \"quotes\" inside"}\n```', "object", True),
        ('not json at all', "object", False),
    ]
    failed = 0
    for i, (inp, typ, should_ok) in enumerate(tests):
        v, err = parse_lenient_json(inp, typ)
        ok = (v is not None) == should_ok
        status = "✓" if ok else "✗"
        print(f"{status} test {i}: expected={'OK' if should_ok else 'FAIL'}, got={'OK' if v else 'FAIL'}")
        if not ok:
            failed += 1
            print(f"   input: {inp!r}")
            print(f"   err:   {err}")
            print(f"   got:   {v}")
    sys.exit(1 if failed else 0)
