#!/usr/bin/env python3
"""
Bootstrap path setup and the rwlib import for rabbit-reads scripts.

Resolves the sibling engine skill `rabbit-writes` by walking up from this
file's own path rather than by arithmetic on the layout, so the skill
directory can move without editing the scripts inside it. Exits 2 with an
install hint when no rwlib is found anywhere above us.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _walk_up(target, predicate=None):
    """Nearest ancestor of HERE (self included) where `target` exists, or None.

    Shared by the engine lookup and the references lookup so both tolerate a
    relocated skill directory the same way.
    """
    cur = HERE
    while True:
        cand = os.path.join(cur, target)
        if os.path.exists(cand):
            if predicate is None or predicate(cand):
                return cand
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


RWLIB_PARENT = _walk_up(os.path.join("rabbit-writes", "scripts"))
SKILLS_DIR = os.path.dirname(os.path.dirname(HERE))

# A scan.py beside these scripts wins over the sibling engine: the standalone
# skill zip vendors the engine next to the reader, the plugin layout does not.
# Either way check_notes ends up with one engine, never two disagreeing ones.
SCAN_PATH = os.path.join(HERE, "scan.py")
if not os.path.isfile(SCAN_PATH) and RWLIB_PARENT:
    SCAN_PATH = os.path.join(RWLIB_PARENT, "scan.py")

for path in (HERE, RWLIB_PARENT):
    if path and os.path.isdir(os.path.join(path, "rwlib")) and path not in sys.path:
        sys.path.insert(0, path)

try:
    from rwlib import cli_error
except (ImportError, ModuleNotFoundError) as exc:
    script_name = os.path.basename(sys.argv[0]) if sys.argv and sys.argv[0] else "script"
    engine_dir = os.path.join(SKILLS_DIR, "rabbit-writes")
    out = [
        "=" * 70,
        "FILE / I/O ERROR: Sibling engine skill `rabbit-writes` is missing.",
        "=" * 70,
        f"Script: {script_name}",
        "Parameter: 'rabbit-writes sibling skill' (expected type: directory path)",
        f"Provided Path: {engine_dir!r}",
        f"Details: {exc}",
        "\nVALID USAGE REQUIREMENT:",
        f"  Install `rabbit-writes` as a sibling directory under: {SKILLS_DIR}",
        f"  Expected structure: {SKILLS_DIR}/rabbit-writes/scripts/rwlib/",
        "=" * 70
    ]
    print("\n".join(out), file=sys.stderr)
    sys.exit(2)


def _has_md(path):
    try:
        return os.path.isdir(path) and any(f.endswith(".md") for f in os.listdir(path))
    except OSError:
        return False


def book_types_dir():
    """This skill's references/book-types directory, or None when absent.

    map_structure enumerates --book-type choices off it and check_notes loads
    the spec out of it, so the lookup lives here rather than twice, one copy
    per script, drifting. None is a working state (the generic grammar, or an
    exit 2 naming what it looked for), not an install error, because the
    reference files can land after the scripts do.
    """
    return _walk_up(os.path.join("references", "book-types"), predicate=_has_md)


def layouts_dir():
    """This skill's references/layouts directory, or None when absent.

    check_notes enumerates --layout choices off it and loads the layout spec
    out of it, the same way book_types_dir feeds --book-type. None is a
    working state (the default layout is built in), not an install error.
    """
    return _walk_up(os.path.join("references", "layouts"), predicate=_has_md)


__all__ = ["HERE", "SKILLS_DIR", "RWLIB_PARENT", "SCAN_PATH", "cli_error",
            "book_types_dir", "layouts_dir"]
