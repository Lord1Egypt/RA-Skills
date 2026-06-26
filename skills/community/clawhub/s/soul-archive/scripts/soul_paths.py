#!/usr/bin/env python3
"""
🧬 Soul Archive — Path Resolver (with silent auto-migration)

Single source of truth for where Soul Archive data lives.

Public API:
  resolve_soul_dir(override=None)  → Path     # the canonical entry point
  get_default_soul_dir()           → Path     # alias

Resolution order (highest to lowest priority):
  1. Explicit `override` argument (e.g. from --soul-dir CLI flag)
  2. SOUL_DIR environment variable
  3. ~/.agent-commons/skills_data/soul-archive/   (the canonical location)

Auto-migration:
  When `resolve_soul_dir()` is invoked and the canonical location does not yet
  exist but legacy data is present at ~/.skills_data/soul-archive/, the legacy
  directory is silently moved into place. This is invisible to callers — they
  always get the canonical path back.

  No prompts. No CLI flags to remember. The data simply ends up where it
  belongs the next time any Soul Archive entry point runs.

This module has zero dependencies beyond stdlib.
"""

from __future__ import annotations

# ── Windows console safety: force UTF-8 on stdout/stderr so Chinese / emoji
#    don't blow up under the default cp936 codec on Windows PowerShell / cmd.
#    No-op on POSIX terminals that are already UTF-8.
#    Applied at module import time so the diagnostic __main__ block (and any
#    caller that prints from this module) is also protected — matches the
#    pattern used by the 8 sibling entrypoint scripts.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    _sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

import os
import shutil
from pathlib import Path
from typing import Optional


# Canonical data location ---------------------------------------------------

AGENT_COMMONS_ROOT = Path.home() / ".agent-commons"
SOUL_ROOT = AGENT_COMMONS_ROOT / "skills_data" / "soul-archive"

# Internal: legacy location, used only by the auto-migrator on first run
# after upgrade. New users / new installs never see this path.
_LEGACY_SOUL_ROOT = Path.home() / ".skills_data" / "soul-archive"


def _silently_migrate_if_needed() -> None:
    """
    Best-effort migration from the historical legacy location to the canonical one.

    Conditions to act:
      - Legacy dir exists AND has profile.json (real data, not an empty placeholder)
      - Canonical location does NOT yet have profile.json (don't clobber existing)
      - Legacy and canonical paths are not the same directory (defensive)

    On any error, swallow silently — the user's data is never made worse than it was.
    Callers always get a usable canonical path back from resolve_soul_dir().

    Cross-platform notes:
      - Uses pathlib + shutil.move; both work on POSIX and Windows.
      - shutil.move falls back to copy+remove if os.rename can't do an atomic
        rename (e.g. across Windows drive letters or POSIX filesystems). This is
        slower but still correct.
      - All filesystem errors are caught — never raise to the caller.
    """
    try:
        if not _LEGACY_SOUL_ROOT.exists():
            return
        if not (_LEGACY_SOUL_ROOT / "profile.json").exists():
            return
        if (SOUL_ROOT / "profile.json").exists():
            # New location already populated — nothing to do, even if legacy still exists.
            return

        # Defensive: never move a directory onto itself (e.g. via a SOUL_DIR override).
        try:
            if _LEGACY_SOUL_ROOT.resolve() == SOUL_ROOT.resolve():
                return
        except OSError:
            return

        # Make sure the parent of the canonical location exists.
        SOUL_ROOT.parent.mkdir(parents=True, exist_ok=True)

        # If the canonical dir exists but is empty/partial (no profile.json), get rid of
        # it so shutil.move can do an in-place rename.
        if SOUL_ROOT.exists():
            try:
                # Only remove if essentially empty — refuse to clobber non-trivial content.
                contents = list(SOUL_ROOT.iterdir())
                if not contents:
                    SOUL_ROOT.rmdir()
                else:
                    # Bail — something we don't understand is there. Don't risk data loss.
                    return
            except OSError:
                return

        shutil.move(str(_LEGACY_SOUL_ROOT), str(SOUL_ROOT))
    except Exception:
        # Migration is opportunistic. If anything blocks it, fall through and let
        # resolve_soul_dir() return whatever path makes sense; the user's data is
        # untouched and the migration can be retried on the next call.
        pass


def resolve_soul_dir(override: Optional[Path] = None) -> Path:
    """
    Resolve the active Soul Archive data directory.

    Side effect: on first call after a Soul Archive upgrade where data still lives at
    the historical ~/.skills_data/soul-archive/ path, this function will silently
    move it to ~/.agent-commons/skills_data/soul-archive/ before returning.

    Override priority:
      1. `override` argument
      2. SOUL_DIR env var
      3. The canonical location (with silent migration if needed)

    The return value is always a usable directory path (callers may need to mkdir it,
    but it points at the correct place).
    """
    if override is not None:
        return Path(override).expanduser()

    env = os.environ.get("SOUL_DIR")
    if env:
        return Path(env).expanduser()

    # Trigger silent migration if applicable, then return canonical location.
    _silently_migrate_if_needed()
    return SOUL_ROOT


def get_default_soul_dir() -> Path:
    """Convenience wrapper for the most common case (no override)."""
    return resolve_soul_dir()


# Internal helpers (kept for diagnostic / legacy callers; not part of the
# documented user-facing surface)

def _is_co_located_with_agent_commons(soul_dir: Path) -> bool:
    """Check whether the given soul_dir lives under ~/.agent-commons/."""
    try:
        soul_dir.resolve().relative_to(AGENT_COMMONS_ROOT.resolve())
        return True
    except (ValueError, OSError):
        return False


__all__ = [
    "SOUL_ROOT",
    "resolve_soul_dir",
    "get_default_soul_dir",
]


if __name__ == "__main__":
    # Diagnostic mode — show where data ends up after any silent migration.
    # (UTF-8 stdout/stderr guard is already applied at module import time above.)
    print("🧬 Soul Archive — path resolver")
    print(f"  $HOME                = {Path.home()}")
    print(f"  resolved soul_dir    = {resolve_soul_dir()}")
    print(f"  exists?              = {resolve_soul_dir().exists()}")
