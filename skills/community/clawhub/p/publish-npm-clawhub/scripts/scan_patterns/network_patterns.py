"""Network-call signatures that can trigger ClawHub suspicious scans."""

NETWORK_PATTERNS = [
    r"fetch\(",
    r"axios\.",
    r"requests\.",
    r"httpx\.",
    r"urllib\.request",
    r"aiohttp",
    r"\bcurl\b",
]
