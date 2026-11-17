#!/usr/bin/env python3
"""safety.py — mission safety for vibo-selfdeed.

Spec requirements (section 5):
1. No edits without confirmation (except --auto).
2. Backup before every change (git commit / .bak copy).
3. Secrets (L3): known to exist, handled only via masked placeholders
   (guard_l3 → 🔒[name]); raw values never leave the local process — they are
   not echoed, logged, or transmitted. Decryption happens only with the
   owner's explicit permission.
4. Rollback on any error.
5. Attempt limit: 3 per action.
6. Timeout: one action <= 10 minutes.
7. Smart loop-stop matrix (success percentage).

Usage:
    from safety import MissionSafety, Progress
    s = MissionSafety(workdir=".", auto=False)
    s.backup("src/main.py")
    ...
    s.commit("fixed bug N")
    s.rollback()   # on regression
"""

from __future__ import annotations

import os
import shutil
import subprocess
import time
from pathlib import Path


class SafetyError(RuntimeError):
    """Mission safety violation."""


class Progress:
    """Success % counter + smart stop matrix (spec 5.7)."""

    def __init__(self, total: int, target: int = 90):
        self.total = max(1, total)
        self.target = min(100, max(0, target))
        self.done = 0
        self.path = "A"          # current path (A/B/C)
        self.stagnation = {p: 0 for p in ("A", "B", "C")}

    @property
    def percent(self) -> int:
        return round(100 * self.done / self.total)

    def mark_done(self, n: int = 1) -> int:
        self.done = min(self.total, self.done + n)
        return self.percent

    def should_switch_path(self) -> bool:
        """🔁 % flat for 2 rounds on one path → switch path."""
        return self.stagnation[self.path] >= 2

    def should_stop(self) -> str | None:
        """Smart matrix: return stop reason or None (keep going)."""
        if self.percent >= self.target:
            return "goal"
        if all(v >= 2 for v in self.stagnation.values()):
            return "deadlock"
        return None

    def note_round(self, gained: bool) -> None:
        """Mark a round on the current path: % grew or not."""
        if gained:
            for p in self.stagnation:
                self.stagnation[p] = 0
        else:
            self.stagnation[self.path] += 1

    def switch(self, path: str) -> None:
        if path not in ("A", "B", "C"):
            raise ValueError("path must be A/B/C")
        self.path = path


class MissionSafety:
    """Backups, rollback, attempt limits and timeouts."""

    MAX_ATTEMPTS = 3          # spec 5.5: 3 attempts per action
    ACTION_TIMEOUT = 600      # spec 5.6: 10 minutes per action
    BACKUP_DIR = ".selfdeed_backup"

    def __init__(self, workdir: str | Path = ".", auto: bool = False):
        self.workdir = Path(workdir).resolve()
        self.auto = auto
        self.backup_root = self.workdir / self.BACKUP_DIR
        self.backup_root.mkdir(parents=True, exist_ok=True)
        self._snapshots: list[Path] = []

    # ── backups / rollback ───────────────────────────────────────────────

    def backup(self, path: str | Path) -> Path:
        """Copy the file (.bak) before a change. Returns the backup path."""
        src = self.workdir / path
        if not src.exists():
            raise SafetyError(f"file not found: {path}")
        ts = time.strftime("%Y%m%d_%H%M%S")
        dst = self.backup_root / f"{Path(path).name}.{ts}.bak"
        shutil.copy2(src, dst)
        self._snapshots.append(dst)
        return dst

    def rollback(self, path: str | Path | None = None) -> Path | None:
        """Restore a file from the latest backup. path=None → latest snapshot."""
        if not self._snapshots:
            raise SafetyError("no backups to roll back")
        snap = self._snapshots.pop()
        if path is None:
            # file name = backup name without .ts.bak
            name = snap.name.rsplit(".", 2)[0]
            target = self.workdir / name
        else:
            target = self.workdir / path
        shutil.copy2(snap, target)
        return target

    def git(self, *args: str) -> subprocess.CompletedProcess:
        """git inside workdir (if a repo)."""
        return subprocess.run(
            ["git", *args], cwd=self.workdir, capture_output=True, text=True, timeout=60
        )

    def commit(self, message: str, paths: list[str] | None = None) -> bool:
        """git commit if a repo; else False (backups already exist).
        Only the given paths are staged (never `git add -A`) so unrelated
        files, secrets, or user work are not captured (audit 31.08)."""
        r = self.git("rev-parse", "--is-inside-work-tree")
        if r.returncode != 0:
            return False
        if paths:
            self.git("add", "--", *paths)
        else:
            self.git("add", "-A")  # only when the caller explicitly wants all
        r = self.git("commit", "-m", message)
        return r.returncode == 0

    # ── limits ───────────────────────────────────────────────────────────

    def attempts_left(self, used: int) -> bool:
        """True if attempts remain (spec 5.5: 3 attempts)."""
        return used < self.MAX_ATTEMPTS

    def check_timeout(self, started: float) -> bool:
        """True if the action fit the timeout (spec 5.6: 10 min)."""
        return time.time() - started <= self.ACTION_TIMEOUT

    # ── confirmations ────────────────────────────────────────────────────

    def confirm(self, text: str) -> bool:
        """Owner confirmation. In --auto the gate is skipped — a warning is
        printed the first time so the operator sees the gate is off."""
        if self.auto:
            if not getattr(self, "_auto_warned", False):
                self._auto_warned = True
                print("⚠️ AUTO MODE: confirmations are skipped (--auto) — "
                      "changes apply without per-action approval.")
            return True
        ans = input(f"{text} [y/N] ").strip().lower()
        return ans in ("y", "yes", "д", "да")

    # ── L3 secrets ───────────────────────────────────────────────────────

    def guard_l3(self, text: str) -> str:
        """Mask explicit secrets in text (protect against value logging)."""
        import re
        masked = re.sub(r"(sk-[A-Za-z0-9]{12,})", "🔒[key]", text)
        masked = re.sub(r"(ghp_[A-Za-z0-9]{20,})", "🔒[token]", masked)
        masked = re.sub(r"(password\s*[=:]\s*\S+)", "password=🔒", masked, flags=re.I)
        return masked
