from __future__ import annotations


NETWORK_RISK_RULES = (
    {
        "label": "external-post",
        "severity": 1.0,
        "patterns": (
            r"requests\.post\s*\(",
            r"curl\b[^\n]{0,120}-x\s+post\b",
            r"invoke-webrequest\b[^\n]{0,120}-method\s+post\b",
            r"method\s*:\s*[\"']post[\"']",
        ),
    },
    {
        "label": "network-download",
        "severity": 1.0,
        "patterns": (
            r"\bcurl\s+https?://",
            r"\bwget\s+https?://",
            r"invoke-webrequest\s+https?://",
        ),
    },
)
