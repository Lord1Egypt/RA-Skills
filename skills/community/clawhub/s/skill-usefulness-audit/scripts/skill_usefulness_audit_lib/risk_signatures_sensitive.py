from __future__ import annotations


SENSITIVE_RISK_RULES = (
    {
        "label": "protected-path-access",
        "severity": 2.0,
        "patterns": (
            r"\.ssh(?:[\\/]|$)",
            r"\.aws(?:[\\/]|$)",
            r"\.env\b",
            r"\bid_rsa\b",
            r"\bcredentials\b",
        ),
    },
)
