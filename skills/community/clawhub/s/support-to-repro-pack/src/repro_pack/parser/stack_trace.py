"""Stack trace extraction and parsing."""

from __future__ import annotations

import re

from ..models import StackFrame, StackTrace


def _parse_python_trace(block: str) -> StackTrace | None:
    """Parse Python traceback."""
    lines = block.strip().splitlines()
    # Find "Traceback (most recent call last):"
    start = None
    for i, line in enumerate(lines):
        if "Traceback (most recent call last)" in line:
            start = i
            break
    if start is None:
        return None

    frames: list[StackFrame] = []
    exception_line = ""

    frame_pattern = re.compile(r'^\s+File "(.+?)", line (\d+)(?:, in (.+))?')

    for line in lines[start + 1 :]:
        fm = frame_pattern.match(line)
        if fm:
            frames.append(
                StackFrame(
                    file_path=fm.group(1),
                    line_number=int(fm.group(2)),
                    function_name=fm.group(3),
                )
            )
        elif not line.startswith(" ") and line.strip():
            exception_line = line.strip()

    if not exception_line:
        return None

    exc_parts = exception_line.split(":", 1)
    return StackTrace(
        language="python",
        exception_type=exc_parts[0].strip(),
        exception_message=exc_parts[1].strip() if len(exc_parts) > 1 else "",
        frames=frames,
        raw=block,
    )


def _parse_java_trace(block: str) -> StackTrace | None:
    """Parse Java/Kotlin stack trace."""
    lines = block.strip().splitlines()

    # First line: ExceptionType: message
    # Must have "at" frames to distinguish from JS
    exc_pattern = re.compile(r"^([\w.]+(?:Exception|Error|Throwable)):\s*(.*)")
    exc_match = exc_pattern.match(lines[0].strip()) if lines else None
    if not exc_match:
        return None

    # Check for Java-style "at" frames (must have parentheses with file:line)
    has_java_frames = any(re.match(r"^\s+at\s+[\w.$]+\([^)]+:\d+\)", line) for line in lines[1:])
    if not has_java_frames:
        return None

    frames: list[StackFrame] = []
    frame_pattern = re.compile(r"^\s+at\s+([\w.$]+)\(([\w.]+):(\d+)\)")

    for line in lines[1:]:
        fm = frame_pattern.match(line)
        if fm:
            full_method = fm.group(1)
            parts = full_method.rsplit(".", 1)
            frames.append(
                StackFrame(
                    file_path=fm.group(2),
                    line_number=int(fm.group(3)),
                    function_name=parts[-1] if parts else full_method,
                )
            )

    return StackTrace(
        language="java",
        exception_type=exc_match.group(1),
        exception_message=exc_match.group(2),
        frames=frames,
        raw=block,
    )


def _parse_js_trace(block: str) -> StackTrace | None:
    """Parse JavaScript/Node.js stack trace."""
    lines = block.strip().splitlines()

    # First line: ErrorType: message
    exc_pattern = re.compile(r"^(\w*Error):\s*(.*)")
    exc_match = exc_pattern.match(lines[0].strip()) if lines else None
    if not exc_match:
        return None

    frames: list[StackFrame] = []
    # Two forms:
    # 1) at [async] funcName (file:line[:col])
    # 2) at file:line:col
    frame_pattern = re.compile(
        r"^\s+at\s+(?:(?:async\s+)?(.+?)\s+\((.+?):(\d+)(?::\d+)?\)|(.+?):(\d+):\d+)"
    )

    for line in lines[1:]:
        fm = frame_pattern.match(line)
        if fm:
            func = fm.group(1) or None
            fpath = fm.group(2) or fm.group(4)
            lineno = int(fm.group(3) or fm.group(5))
            frames.append(
                StackFrame(
                    file_path=fpath,
                    line_number=lineno,
                    function_name=func,
                )
            )

    return StackTrace(
        language="javascript",
        exception_type=exc_match.group(1),
        exception_message=exc_match.group(2),
        frames=frames,
        raw=block,
    )


def _parse_go_trace(block: str) -> StackTrace | None:
    """Parse Go panic/error trace."""
    lines = block.strip().splitlines()

    panic_pattern = re.compile(r"^(?:panic|runtime error):\s*(.*)")
    panic_match = None
    start = 0
    for i, line in enumerate(lines):
        panic_match = panic_pattern.match(line.strip())
        if panic_match:
            start = i
            break

    if not panic_match:
        return None

    frames: list[StackFrame] = []
    # Go traces alternate: function line, then file:line line
    func_pattern = re.compile(r"^([\w./]+(?:\.\w+)+)\(.*\)")
    file_pattern = re.compile(r"^\s+(.+\.go):(\d+)")

    current_func = None
    for line in lines[start + 1 :]:
        fm = func_pattern.match(line.strip())
        if fm:
            current_func = fm.group(1)
            continue
        fl = file_pattern.match(line)
        if fl:
            frames.append(
                StackFrame(
                    file_path=fl.group(1),
                    line_number=int(fl.group(2)),
                    function_name=current_func,
                )
            )
            current_func = None

    return StackTrace(
        language="go",
        exception_type="panic",
        exception_message=panic_match.group(1),
        frames=frames,
        raw=block,
    )


_PARSERS = [_parse_python_trace, _parse_java_trace, _parse_js_trace, _parse_go_trace]


def extract_stack_traces(text: str) -> list[StackTrace]:
    """Extract all stack traces from text, trying all language parsers."""
    traces: list[StackTrace] = []

    # Split text into potential blocks by blank lines or known markers
    blocks: list[str] = []
    current_block: list[str] = []

    for line in text.splitlines():
        if not line.strip() and current_block:
            blocks.append("\n".join(current_block))
            current_block = []
        else:
            current_block.append(line)
    if current_block:
        blocks.append("\n".join(current_block))

    # Also try the full text as one block
    blocks.append(text)

    seen_raws: set[str] = set()
    for block in blocks:
        for parser in _PARSERS:
            result = parser(block)
            if result and result.raw not in seen_raws:
                seen_raws.add(result.raw)
                traces.append(result)

    return traces
