from __future__ import annotations


ENCODING_RISK_RULES = (
    {
        "label": "base64-payload",
        "severity": 1.0,
        "patterns": (
            r"frombase64string",
            r"base64\s+(?:-d|--decode)",
            r"\batob\s*\(",
        ),
    },
)
