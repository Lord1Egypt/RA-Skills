"""One place for turning untrusted text into something safe to put in a prompt.

Customer text reaches the model through packs. These helpers keep it from posing as structure:
a closing tag, a new heading, a new list line, a forged provenance mark.
"""

from __future__ import annotations

import re

_TAG = re.compile(r"(customer|person)[_ -]?message", re.IGNORECASE)
_CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f‪-‮⁦-⁩]")
_PROVENANCE = re.compile(r"\((?:admin|attendant|platform|inferred)\)", re.IGNORECASE)
_LIST_LEAD = re.compile(r"^\s*(?:[-*+#>]+|\d+[.)])\s+")
LINE_JOIN = " ⏎ "


def neutralize_tags(text: str) -> str:
    return _TAG.sub(lambda m: f"{m.group(1)} message", text)


def one_line(text: str) -> str:
    """Join lines with a visible mark so a message cannot start a line of its own in a history."""
    return LINE_JOIN.join(part.strip() for part in text.splitlines() if part.strip())


def clean_fact_value(text: str, limit: int = 300) -> str:
    """A stored fact is one plain line: no control characters, markup or provenance mark."""
    text = _CONTROL.sub(" ", text)
    text = " ".join(text.split())
    text = _LIST_LEAD.sub("", text)
    text = text.replace("**", "").replace("__", "").replace("`", "'")
    text = _PROVENANCE.sub("", text)
    text = neutralize_tags(text)
    return " ".join(text.split())[:limit]


def clean_summary(text: str, limit: int = 2000) -> str:
    """A model-written summary of what a customer said: one plain line, same rules as a fact."""
    return clean_fact_value(text, limit)
