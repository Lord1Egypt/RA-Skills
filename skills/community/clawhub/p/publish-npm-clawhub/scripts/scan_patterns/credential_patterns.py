"""Patterns for local credential/account access that deserve manual review."""

LOCAL_CREDENTIAL_SOURCE_PATTERNS = [
    r"~/.openclaw/openclaw\.json",
    r"~/.openclaw/secrets\.json",
    r"\bopenclaw\.json\b",
    r"\bcredentials\.json\b",
    r"channels\.[a-z0-9_-]+\.(accounts|defaultAccount|botToken|appId|appSecret)\b",
]

LOCAL_CREDENTIAL_DISCLOSURE_PATTERNS = [
    r"stored locally",
    r"local-only",
    r"local direct",
    r"writes?.{0,80}credentials\.json",
    r"reuse[s]?\s+openclaw",
    r"read[s]?.{0,80}configured.{0,40}accounts",
    r"will call the openclaw cli",
    r"important to be aware of",
    r"why (?:these|those) permissions are needed",
    r"本地",
    r"本机",
    r"直连",
    r"复用\s*OpenClaw",
    r"写入.{0,40}credentials\.json",
]
