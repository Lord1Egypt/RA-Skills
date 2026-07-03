"""Savings measurement. Token figures are estimates (chars/4), labelled as such
wherever surfaced — never reported as exact token counts."""


def _est_tokens(chars: int) -> int:
    return round(chars / 4)


def measure(before: str, after: str) -> dict:
    cb, ca = len(before), len(after)
    pct = round((cb - ca) / cb * 100, 1) if cb else 0.0
    return {
        "chars_before": cb,
        "chars_after": ca,
        "lines_before": before.count("\n"),
        "lines_after": after.count("\n"),
        "est_tokens_before": _est_tokens(cb),
        "est_tokens_after": _est_tokens(ca),
        "pct_chars_saved": pct,
    }
