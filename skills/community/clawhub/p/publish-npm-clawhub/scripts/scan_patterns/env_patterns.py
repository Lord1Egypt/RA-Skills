"""Environment-access signatures that should not live next to network sends."""

ENV_PATTERNS = [
    r"process\.env",
    r"os\.getenv",
    r"os\.environ",
    r"System\.getenv",
]
