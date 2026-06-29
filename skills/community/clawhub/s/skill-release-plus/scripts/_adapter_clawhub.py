#!/usr/bin/env python3
"""
_adapter_clawhub.py — clawhub.com adapter (wraps the `clawhub` CLI).

Why CLI wrap instead of raw HTTP:
  - clawhub.com auth flow is browser-OAuth based; CLI handles token persistence
  - CLI also handles slug validation / package upload / staging in a stable way
  - We just need SRP_CLAWHUB_TOKEN for non-interactive login

Note on cn.clawhub-mirror.com:
  - That is a READ-ONLY mirror of clawhub.com (ByteDance Volcano Engine).
  - Publishing here auto-syncs to the mirror. So Chinese users just install
    from the mirror URL; no separate publish target needed.

Auth:
  - Reads token from SRP_CLAWHUB_TOKEN env var (set by _lib_config)
  - Calls `clawhub login --token "$SRP_CLAWHUB_TOKEN" --no-browser` if needed
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from typing import Optional

from _lib_adapters_base import BaseAdapter, PublishResult, InspectResult


class ClawhubAdapter(BaseAdapter):
    target_name = "clawhub"

    def __init__(self, cfg: dict):
        super().__init__(cfg)
        self.token = cfg.get("SRP_CLAWHUB_TOKEN", "")
        self.cli = shutil.which("clawhub")

    # ── Helpers ──────────────────────────────────────────────────────────

    def _ensure_login(self) -> Optional[str]:
        """Return error message if not logged in / cannot log in, else None."""
        if not self.cli:
            return ("clawhub CLI not found in PATH. Install with: "
                    "npm install -g clawhub")
        if not self.token:
            return "SRP_CLAWHUB_TOKEN is not set"

        # Always re-login non-interactively (idempotent; ensures fresh token)
        try:
            proc = subprocess.run(
                [self.cli, "login", "--token", self.token, "--no-browser"],
                capture_output=True, text=True, timeout=30,
            )
            if proc.returncode != 0:
                err = (proc.stderr or proc.stdout).strip()
                return f"clawhub login failed: {err}"
        except subprocess.TimeoutExpired:
            return "clawhub login timeout (30s)"
        except Exception as e:
            return f"clawhub login error: {e}"
        return None

    # ── BaseAdapter overrides ────────────────────────────────────────────

    def check_slug_available(self, slug: str) -> Optional[bool]:
        """Use `clawhub inspect <slug>` to check existence."""
        if not self.cli:
            return None
        try:
            proc = subprocess.run(
                [self.cli, "inspect", slug],
                capture_output=True, text=True, timeout=15,
            )
            # Available means inspect returns "Skill not found"
            combined = (proc.stdout + proc.stderr).lower()
            if "not found" in combined or "skill not found" in combined:
                return True
            if proc.returncode == 0 and "owner:" in combined:
                return False
            return None
        except Exception:
            return None

    def inspect(self, slug: str) -> InspectResult:
        if not self.cli:
            return InspectResult(error="clawhub CLI not in PATH")
        try:
            proc = subprocess.run(
                [self.cli, "inspect", slug],
                capture_output=True, text=True, timeout=15,
            )
            stdout = proc.stdout
            stderr = proc.stderr
            if "not found" in (stdout + stderr).lower():
                return InspectResult(exists=False)
            # Best-effort parse of the human-readable output
            out = {}
            for line in stdout.splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    out[k.strip().lower()] = v.strip()
            return InspectResult(
                exists=True,
                version=out.get("latest", ""),
                display_name=out.get("name", "") or slug,
                owner=out.get("owner", ""),
                license=out.get("license", ""),
                raw=stdout,
            )
        except Exception as e:
            return InspectResult(error=str(e))

    def publish(
        self,
        slug: str,
        version: str,
        changelog: str,
        tar_path: str,
        skill_dir: str,
        extra: dict = None,
    ) -> PublishResult:
        """
        clawhub publish expects a SKILL FOLDER (not a tar).
        We pass `skill_dir` (the clean copy directory) directly.

        Note: clawhub auto-detects slug from SKILL.md frontmatter, but we pass
        --slug explicitly for clarity.
        """
        extra = extra or {}

        err = self._ensure_login()
        if err:
            return self._err(err)

        # Build command (use ABSOLUTE path per ref_clawhub_cli_publish_workflow.md)
        abs_skill_dir = os.path.abspath(skill_dir)
        cmd = [self.cli, "publish", abs_skill_dir, "--slug", slug]

        if extra.get("display_name"):
            cmd.extend(["--name", extra["display_name"]])
        if version:
            cmd.extend(["--version", version])
        if changelog:
            cmd.extend(["--changelog", changelog])

        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120,
            )
        except subprocess.TimeoutExpired:
            return self._err("clawhub publish timeout (120s)")
        except Exception as e:
            return self._err(f"clawhub publish error: {e}")

        if proc.returncode != 0:
            err_msg = (proc.stderr or proc.stdout).strip()
            return self._err(
                f"clawhub publish failed (exit {proc.returncode}): {err_msg}",
                raw={"stdout": proc.stdout, "stderr": proc.stderr},
            )

        # Try to extract the published ID / URL from stdout (best effort)
        stdout = proc.stdout
        published_id = ""
        url = f"https://clawhub.com/skills/{slug}"
        for line in stdout.splitlines():
            line_l = line.lower()
            if "id:" in line_l or "uuid" in line_l:
                # Heuristic capture
                parts = line.split(":")
                if len(parts) >= 2:
                    published_id = parts[-1].strip()
                    break

        return self._ok(
            slug=slug,
            version=version,
            url=url,
            action="publish",
            raw={"published_id": published_id, "stdout": stdout},
        )


__all__ = ["ClawhubAdapter"]
