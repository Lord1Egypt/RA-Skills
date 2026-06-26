"""Utilities for cleaning email text."""

from __future__ import annotations

import re

# Patterns that indicate start of quoted reply history
_QUOTE_BOUNDARY_PATTERNS = [
    # "On [date], [name] wrote:" (Gmail/Outlook)
    re.compile(r"^On .{10,80} wrote:\s*$", re.MULTILINE),
    # "From: ..." followed by "Sent: ..." (Outlook style)
    re.compile(r"^From:\s+.+\nSent:\s+", re.MULTILINE),
    # Lines starting with "> " (traditional quote markers) — 3+ consecutive
    re.compile(r"(?:^> .+\n){3,}", re.MULTILINE),
    # "---------- Forwarded message ----------"
    re.compile(r"^-{5,}\s*Forwarded message\s*-{5,}", re.MULTILINE),
    # Outlook separator line
    re.compile(r"^_{20,}\s*$", re.MULTILINE),
    # "-----Original Message-----"
    re.compile(r"^-{3,}\s*Original Message\s*-{3,}", re.MULTILINE | re.IGNORECASE),
]


def decode_html_entities(text: str) -> str:
    """Decode HTML entities like &amp; &lt; &gt; &quot; in email text."""
    import html

    return html.unescape(text)


def strip_quoted_text(text: str) -> str:
    """Remove quoted reply history from email body, keeping only the new content.

    Truncates at the first detected quote boundary.
    If the result is too short (< 50 chars), returns the original text.
    """
    if not text:
        return text

    earliest_pos = len(text)
    for pattern in _QUOTE_BOUNDARY_PATTERNS:
        match = pattern.search(text)
        if match and match.start() < earliest_pos:
            earliest_pos = match.start()

    if earliest_pos < len(text):
        stripped = text[:earliest_pos].rstrip()
        if len(stripped) >= 50:
            return stripped

    return text


def detect_language(text: str) -> str:
    """Detect language of text. Returns ISO 639-1 code (e.g. 'en', 'de', 'ar').

    Simple heuristic based on character scripts and common words.
    """
    if not text:
        return "en"

    # Check for Arabic script (Unicode range \u0600-\u06FF)
    arabic_chars = sum(1 for c in text if "\u0600" <= c <= "\u06ff")
    if arabic_chars > len(text) * 0.1:
        return "ar"

    # Check for common German words
    lower = text.lower()
    german_words = [
        "der",
        "die",
        "das",
        "und",
        "ist",
        "nicht",
        "sie",
        "ich",
        "ein",
        "eine",
        "wir",
        "sehr",
        "geehrter",
        "geehrte",
        "mit",
        "freundlichen",
        "grüßen",
        "bitte",
        "können",
    ]
    german_hits = sum(1 for w in german_words if re.search(r"\b" + re.escape(w) + r"\b", lower))

    # Check for common French words
    french_words = [
        "vous",
        "nous",
        "est",
        "les",
        "une",
        "pour",
        "dans",
        "avec",
        "sur",
        "que",
        "qui",
        "sont",
        "cette",
        "mais",
        "bonjour",
        "merci",
        "monsieur",
        "madame",
    ]
    french_hits = sum(1 for w in french_words if re.search(r"\b" + re.escape(w) + r"\b", lower))

    # Check for common Spanish words
    spanish_words = ["usted", "nosotros", "para", "como", "pero", "hola", "gracias", "señor", "señora", "estimado", "estimada", "por", "favor", "también"]
    spanish_hits = sum(1 for w in spanish_words if re.search(r"\b" + re.escape(w) + r"\b", lower))

    scores = {"de": german_hits, "fr": french_hits, "es": spanish_hits}
    best = max(scores, key=scores.get)
    if scores[best] >= 2:
        return best

    return "en"
