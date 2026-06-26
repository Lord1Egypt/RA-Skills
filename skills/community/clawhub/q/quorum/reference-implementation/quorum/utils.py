# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Utility functions used across the Quorum codebase.
"""

import json
import re
from typing import Any


def extract_json_from_response(response_text: str) -> str:
    """
    Extract JSON content from a response that may be wrapped in markdown fences.

    This function handles common patterns where LLMs wrap JSON responses in
    markdown code blocks, which can cause JSON parsing to fail. It does not
    handle nested backticks in JSON string values.

    Args:
        response_text: Raw response text that may contain fenced JSON

    Returns:
        Cleaned JSON string ready for parsing

    Examples:
        >>> extract_json_from_response('{"key": "value"}')
        '{"key": "value"}'

        >>> extract_json_from_response('```json\\n{"key": "value"}\\n```')
        '{"key": "value"}'

        >>> extract_json_from_response('```\\n{"key": "value"}\\n```')
        '{"key": "value"}'
    """
    text = response_text.strip()

    # If no fences, return as-is
    if not text.startswith('```'):
        return text

    # Handle compact fences (no newlines): ```json{"key": "value"}```
    compact_match = re.match(r'```(?:json|JSON)?\s*(.+?)```$', text)
    if compact_match and '\n' not in text:
        return compact_match.group(1).strip()

    # Handle multi-line fences
    lines = text.split('\n')
    if not lines[0].startswith('```'):
        return text

    # Skip the opening fence line
    content_start = 1

    # Find the closing ``` that's on its own line
    content_end = len(lines)
    for i in range(len(lines) - 1, 0, -1):  # Search backwards
        line = lines[i].strip()
        if line == '```':
            content_end = i
            break

    # If we found both opening and closing fences, extract the content
    if content_end > content_start:
        content_lines = lines[content_start:content_end]
        extracted = '\n'.join(content_lines).strip()
        return extracted

    # Fallback: if we can't find proper closing fence,
    # try to extract everything after the first line
    if len(lines) > 1:
        remaining = '\n'.join(lines[1:])
        # Try to remove trailing ``` if it exists
        if remaining.rstrip().endswith('```'):
            remaining = remaining.rstrip()[:-3].rstrip()
        return remaining

    # Final fallback: return original text
    return text