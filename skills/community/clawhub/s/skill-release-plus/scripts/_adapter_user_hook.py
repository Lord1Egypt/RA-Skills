#!/usr/bin/env python3
"""
_adapter_user_hook.py — Custom user hook adapter.

Lets users implement their own publish target via a shell script. The script
receives the package path + metadata via stdin (JSON) and environment variables,
and is expected to:
  - exit 0 on success
  - print a JSON object to stdout with at least {"ok": true, "url": "..."}
  - exit non-zero on failure (stderr captured)

Usage:
  --target user-hook:./my-hook.sh
  --target user-hook:/abs/path/to/publisher.py

Environment passed to the hook:
  SRP_HOOK_SLUG           slug
  SRP_HOOK_VERSION        version
  SRP_HOOK_CHANGELOG      changelog text
  SRP_HOOK_TAR_PATH       absolute path to the tar.gz package
  SRP_HOOK_SKILL_DIR      absolute path to the source skill directory
  SRP_HOOK_DISPLAY_NAME   display name (defaults to slug)

Stdin: JSON with the same fields above.

Example minimal hook (bash):
  #!/bin/bash
  set -e
  echo "Publishing $SRP_HOOK_SLUG v$SRP_HOOK_VERSION to my-private-hub..."
  curl -F "package=@$SRP_HOOK_TAR_PATH" https://my-hub.example.com/publish
  echo '{"ok": true, "url": "https://my-hub.example.com/skills/'"$SRP_HOOK_SLUG"'"}'
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Optional

from _lib_adapters_base import BaseAdapter, PublishResult, InspectResult


class UserHookAdapter(BaseAdapter):
    target_name = "user-hook"

    def __init__(self, cfg: dict, hook_path: str):
        super().__init__(cfg)
        self.hook_path = os.path.abspath(os.path.expanduser(hook_path))

    def publish(
        self,
        slug: str,
        version: str,
        changelog: str,
        tar_path: str,
        skill_dir: str,
        extra: dict = None,
    ) -> PublishResult:
        extra = extra or {}

        # Validate hook
        if not os.path.isfile(self.hook_path):
            return self._err(f"hook script not found: {self.hook_path}")
        if not os.access(self.hook_path, os.X_OK):
            return self._err(
                f"hook script not executable (chmod +x {self.hook_path})"
            )

        # Build env + stdin payload
        payload = {
            "slug": slug,
            "version": version,
            "changelog": changelog,
            "tar_path": os.path.abspath(tar_path),
            "skill_dir": os.path.abspath(skill_dir),
            "display_name": extra.get("display_name") or slug,
        }
        env = os.environ.copy()
        env["SRP_HOOK_SLUG"] = slug
        env["SRP_HOOK_VERSION"] = version
        env["SRP_HOOK_CHANGELOG"] = changelog or ""
        env["SRP_HOOK_TAR_PATH"] = payload["tar_path"]
        env["SRP_HOOK_SKILL_DIR"] = payload["skill_dir"]
        env["SRP_HOOK_DISPLAY_NAME"] = payload["display_name"]

        try:
            proc = subprocess.run(
                [self.hook_path],
                input=json.dumps(payload),
                capture_output=True, text=True,
                env=env, timeout=300,
            )
        except subprocess.TimeoutExpired:
            return self._err(f"hook timeout (300s): {self.hook_path}")
        except Exception as e:
            return self._err(f"hook execution error: {e}")

        if proc.returncode != 0:
            return self._err(
                f"hook exited {proc.returncode}: "
                f"{(proc.stderr or proc.stdout).strip()[:500]}",
                raw={"stdout": proc.stdout, "stderr": proc.stderr},
            )

        # Parse hook stdout as JSON (best effort)
        stdout = proc.stdout.strip()
        url = ""
        raw_result = None
        if stdout:
            try:
                hook_result = json.loads(stdout)
                if isinstance(hook_result, dict):
                    url = hook_result.get("url", "")
                    raw_result = hook_result
                    if hook_result.get("ok") is False:
                        return self._err(
                            f"hook returned ok=false: {hook_result.get('error', '')}",
                            raw=hook_result,
                        )
            except json.JSONDecodeError:
                # Non-JSON stdout is fine; just no url
                raw_result = {"stdout": stdout}

        return self._ok(
            slug=slug, version=version, url=url,
            action="user-hook", raw=raw_result,
        )

    def check_slug_available(self, slug: str) -> Optional[bool]:
        return None  # Cannot determine; hook owns this

    def inspect(self, slug: str) -> InspectResult:
        return InspectResult(
            exists=None,
            error="user-hook adapter does not support inspect",
        )


__all__ = ["UserHookAdapter"]
