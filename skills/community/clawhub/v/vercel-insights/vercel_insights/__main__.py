"""Entry point, path-robust so it runs from anywhere and uninstalled.

Both of these work:

    python3 -m vercel_insights --help                    # from the repo root
    python3 /abs/path/vercel_insights/__main__.py --help # from any directory

The hazard both forms share is this package's own directory being on
``sys.path``. This package contains a module named ``http``, which shadows the
standard library package of the same name that ``requests`` depends on, and the
failure is not a clean one: ``urllib3`` imports ``http.client``, gets this
module instead, and dies on its relative import.

Run as a plain script, Python itself puts this file's own directory on
``sys.path``, which is both useless (the package lives one level up) and
actively harmful. Run as a module the directory is not added automatically, but
nothing stops it being there already: ``PYTHONPATH`` pointing straight at the
package is enough, and then ``python3 -m vercel_insights`` breaks in exactly
the same way. So the repair runs for both invocation forms, and both steps have
to happen before anything else is imported: drop this directory from
``sys.path``, then add the package's parent.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.realpath(__file__))
_PARENT = os.path.dirname(_HERE)

# Unconditional on purpose: see the module docstring. Under -m the package is
# already imported by the time this runs, so removing the entry cannot make it
# unimportable; what it does is keep the stdlib reachable for everything
# imported below.
sys.path[:] = [entry for entry in sys.path if os.path.realpath(entry or ".") != _HERE]
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

def _missing_dependency_message(missing: str) -> str:
    """Explain an absent runtime dependency instead of dumping a traceback.

    This is the likeliest first run failure there is. ``requests`` is the only
    runtime dependency, and the documented invocation is ``python3 -m
    vercel_insights``, so anyone whose ``python3`` is a system interpreter
    without ``requests`` meets a ``ModuleNotFoundError`` as the very first thing
    the tool ever shows them. A traceback is the wrong answer to that: it names
    the wrong problem (an import line) rather than the real one (the wrong
    interpreter), and the contract says no traceback reaches the user.

    When a virtualenv sits next to the package and already has the dependency,
    its interpreter is named outright, because that is almost always the fix.
    """
    lines = [
        f"error: {missing!r} is not importable by this interpreter, and it is "
        "the only runtime dependency this tool has.",
        f"  interpreter: {sys.executable}",
    ]
    venv_dir = os.path.join(_PARENT, ".venv")
    candidate = os.path.join(venv_dir, "bin", "python")
    # Compare prefixes, not resolved interpreter paths: a virtualenv's
    # bin/python is usually a symlink to the very interpreter running now, so
    # realpath equality would wrongly conclude they are the same environment and
    # suppress the one hint that actually fixes this.
    in_that_venv = os.path.realpath(sys.prefix) == os.path.realpath(venv_dir)
    if os.path.exists(candidate) and not in_that_venv:
        lines.append(f"  a virtualenv next to the package already has it: {candidate}")
        lines.append(f"  so run: {candidate} -m vercel_insights ...")
    else:
        lines.append(f"  install it with: {sys.executable} -m pip install requests")
        lines.append(
            "  if that reports an externally managed environment (PEP 668, which "
            "Debian, Ubuntu, Fedora and Homebrew Python all set), make a "
            "virtualenv instead:"
        )
        lines.append("    python3 -m venv .venv && .venv/bin/python -m pip install requests")
        lines.append("    .venv/bin/python -m vercel_insights ...")
    return "\n".join(lines)


try:
    from vercel_insights.cli import main  # noqa: E402  (the path fix must come first)
except ModuleNotFoundError as exc:  # pragma: no cover - covered by an out-of-process test
    # Only speak for a genuinely absent dependency. A ModuleNotFoundError from
    # inside the package is a real bug and must keep its traceback.
    if exc.name in ("requests", "urllib3", "charset_normalizer", "idna", "certifi"):
        print(_missing_dependency_message(exc.name or "requests"), file=sys.stderr)
        raise SystemExit(2) from None
    raise

if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
