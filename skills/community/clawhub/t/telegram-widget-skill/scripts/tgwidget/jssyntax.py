"""JavaScript syntax check, with the best engine at hand.

1. The `quickjs` Python package (QuickJS, the engine Telegram runs widgets in).
   Its bundled build is older than Telegram's (no class static blocks, no
   regex `d` flag), so when it refuses code that Node accepts, the finding is
   only a warning.
2. `node --check`.
3. A structural check (strings, comments, brackets) when neither is installed.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from typing import Optional, Tuple

from .jslex import LexError, check_brackets, tokenize

try:  # pragma: no cover - depends on the environment
    import quickjs  # type: ignore
except Exception:  # pragma: no cover
    quickjs = None

# QuickJS's Function constructor puts the body after "(function anonymous(\n) {\n"
_QJS_LINE_OFFSET = 2


def available_engine() -> str:
    if quickjs is not None:
        return "quickjs"
    if shutil.which("node"):
        return "node"
    return "basic"


# The Function constructor compiles the widget's code into a function that is never called.
_COMPILE_ONLY = "function compile(src) { new Function(src); }"


def _quickjs(code: str) -> Optional[Tuple[str, Optional[int]]]:
    compile_only = quickjs.Function("compile", _COMPILE_ONLY)
    compile_only.set_time_limit(2)
    compile_only.set_memory_limit(64 * 1024 * 1024)
    try:
        compile_only(code)
    except Exception as e:  # quickjs.JSException
        text = str(e)
        first = text.splitlines()[0] if text else "SyntaxError"
        m = re.search(r"at <input>:(\d+)", text)
        line = int(m.group(1)) - _QJS_LINE_OFFSET if m else None
        return first, (line if line and line > 0 else None)
    return None


def _node(code: str) -> Optional[Tuple[str, Optional[int]]]:
    fd, path = tempfile.mkstemp(suffix=".js", prefix="tgwidget-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            # a function body, like QuickJS's check: `return` is fine, nothing runs
            f.write("(function(){\n" + code + "\n})")
        proc = subprocess.run(["node", "--check", path], capture_output=True, text=True, timeout=30)
    finally:
        os.unlink(path)
    if proc.returncode == 0:
        return None
    err = proc.stderr
    m = re.search(re.escape(path) + r":(\d+)", err)
    line = int(m.group(1)) - 1 if m else None
    msg = next((ln.strip() for ln in err.splitlines() if re.match(r"\s*\w*Error:", ln)), "SyntaxError")
    return msg, (line if line and line > 0 else None)


def _basic(code: str) -> Optional[Tuple[str, Optional[int]]]:
    try:
        tokens = tokenize(code)
    except LexError as e:
        return "SyntaxError: %s" % e, e.line
    err = check_brackets(tokens)
    if err:
        return "SyntaxError: %s" % err, err.line
    return None


def check_syntax(code: str):
    """Returns (problem, line, severity, engine) or None. Lines are 1-based within `code`."""
    engine = available_engine()
    if engine == "quickjs":
        found = _quickjs(code)
        if found and shutil.which("node"):
            if _node(code) is None:
                msg = "%s (refused by the older QuickJS build used for checking, accepted by Node; " \
                      "Telegram's newer QuickJS probably accepts it, but simpler syntax is safer)" % found[0]
                return msg, found[1], "warning", engine
        return (found[0], found[1], "error", engine) if found else None
    if engine == "node":
        found = _node(code)
        return (found[0], found[1], "error", engine) if found else None
    found = _basic(code)
    return (found[0], found[1], "error", engine) if found else None
