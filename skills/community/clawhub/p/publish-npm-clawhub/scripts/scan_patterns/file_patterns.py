"""Local file-access signatures that should not live next to network sends."""

FILE_PATTERNS = [
    r"readFile",
    r"readFileSync",
    r"fs\.read",
    r"open\(",
    r"read_text\(",
    r"json\.load\(",
    r"yaml\.safe_load\(",
]
