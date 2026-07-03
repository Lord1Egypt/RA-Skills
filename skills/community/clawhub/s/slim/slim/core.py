"""Core text-slimming transforms.

`slim_text` applies lossless-of-signal cleanups (ANSI removal, trailing
whitespace, blank-line and repeated-line collapse). `truncate_middle` is the
lossy head+tail clamp for very large dumps; it is applied only by plugins that
opt in, never by `slim_text`.
"""
import re

_ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
_BLANK_RUN = re.compile(r"\n[ \t]*\n(?:[ \t]*\n)+")


def _dedupe_consecutive(lines: list[str]) -> list[str]:
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        j = i
        while j < n and lines[j] == lines[i]:
            j += 1
        count = j - i
        if count >= 3 and lines[i].strip():
            out.append(lines[i])
            out.append(f"  ... (repeated {count}x)")
        else:
            out.extend(lines[i:j])
        i = j
    return out


def slim_text(text: str) -> str:
    text = _ANSI.sub("", text)
    lines = [ln.rstrip() for ln in text.split("\n")]
    lines = _dedupe_consecutive(lines)
    text = "\n".join(lines)
    return _BLANK_RUN.sub("\n\n", text)


def truncate_middle(text: str, head: int = 20, tail: int = 10) -> str:
    has_trailing = text.endswith("\n")
    lines = text.split("\n")
    if has_trailing:
        lines = lines[:-1]
    if len(lines) <= head + tail:
        return text
    elided = len(lines) - head - tail
    kept = (
        lines[:head]
        + [f"  ... ({elided} lines elided by slim) ..."]
        + lines[-tail:]
    )
    out = "\n".join(kept)
    return out + "\n" if has_trailing else out
