#!/usr/bin/env python3
"""
_adapter_skillhub_cn.py — SkillHub.cn adapter (Tencent Cloud).

Verified 2026-06-22 against api.skillhub.cn:
  Host: https://api.skillhub.cn
  Auth: Authorization: Bearer skh_xxx
  Publish: POST /api/v1/community/skills/publish (multipart/form-data)
           - field `payload` (JSON): { slug, name, displayName, version, description,
                                      claimSlug?, joinContest?, labels?, category? }
           - field `files` (multipart): each file with `filename="<relative-path>"`
  Slug regex: ^[a-z0-9][a-z0-9-]*[a-z0-9]$
  Rate limit: 3 publish/minute/token (rule "publish.token.minute")
  Owner unpublish: POST /api/v1/community/skills/{slug}/unlist
  Owner delete: DELETE /api/v1/community/skills/{slug} (after unlist)
  Owner relist: POST /api/v1/community/skills/{slug}/relist
  Self skills list: GET /api/v1/users/{handle}/skills
  Auth me: GET /api/v1/auth/me

Real-name (face ID) and review queue are platform-side concerns; they apply
to all publishers regardless of how they publish.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Optional, Tuple

from _lib_adapters_base import BaseAdapter, PublishResult, InspectResult
from _lib_package import build_multipart_from_tarball


API_BASE = "https://api.skillhub.cn"

# Slug regex (matches server-side validation)
import re
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")


class SkillhubCnAdapter(BaseAdapter):
    target_name = "skillhub-cn"

    def __init__(self, cfg: dict):
        super().__init__(cfg)
        self.token = cfg.get("SRP_SKILLHUB_CN_TOKEN", "")
        # Cached identity
        self._handle: Optional[str] = None
        self._user_id: Optional[int] = None

    # ── HTTP helpers ─────────────────────────────────────────────────────

    def _request(self, method: str, path: str, *,
                 body: bytes = None,
                 content_type: str = None,
                 timeout: int = 30) -> Tuple[int, dict]:
        url = f"{API_BASE}{path}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "skill-release-plus",
            "Accept": "application/json",
        }
        if content_type:
            headers["Content-Type"] = content_type
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read() or b"{}"
                try:
                    return resp.status, json.loads(raw)
                except json.JSONDecodeError:
                    return resp.status, {"_raw": raw.decode("utf-8", errors="replace")}
        except urllib.error.HTTPError as e:
            try:
                return e.code, json.loads(e.read() or b"{}")
            except Exception:
                return e.code, {}
        except Exception as e:
            return -1, {"error": str(e)}

    # ── Identity ─────────────────────────────────────────────────────────

    def _ensure_identity(self) -> Optional[str]:
        """Return error message or None on success. Populates self._handle."""
        if self._handle:
            return None
        if not self.token:
            return "SRP_SKILLHUB_CN_TOKEN is not set"
        code, body = self._request("GET", "/api/v1/auth/me")
        if code != 200:
            return f"auth/me failed: HTTP {code} {body.get('error', '')}"
        user = body.get("user", {})
        self._handle = user.get("handle", "")
        self._user_id = user.get("id")
        return None if self._handle else "no handle in auth/me response"

    # ── BaseAdapter overrides ────────────────────────────────────────────

    def check_slug_available(self, slug: str) -> Optional[bool]:
        if not self.token:
            return None
        code, body = self._request(
            "GET",
            f"/api/v1/community/skills/check-slug?slug={slug}",
        )
        if code != 200:
            return None
        return bool(body.get("available", False)) and body.get("reason") != "own"

    def inspect(self, slug: str) -> InspectResult:
        if err := self._ensure_identity():
            return InspectResult(error=err)
        # Check slug ownership/availability
        code, body = self._request(
            "GET",
            f"/api/v1/community/skills/check-slug?slug={slug}",
        )
        if code != 200:
            return InspectResult(error=f"HTTP {code}")
        available = body.get("available", False)
        reason = body.get("reason", "")
        if available and reason == "own":
            # Owner can publish new version
            return InspectResult(
                exists=True,
                display_name=body.get("displayName", slug),
                owner=body.get("ownerHandle", self._handle or ""),
                raw=body,
            )
        if available:
            return InspectResult(exists=False, raw=body)
        # Not available = taken by someone else
        return InspectResult(
            exists=True,
            owner=body.get("ownerHandle", ""),
            display_name=body.get("displayName", slug),
            error="taken by another owner" if reason != "own" else "",
            raw=body,
        )

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

        # 0. Auth check
        if err := self._ensure_identity():
            return self._err(err)

        # 1. Slug regex check (mirrors server-side)
        if not _SLUG_RE.match(slug):
            return self._err(
                f"slug {slug!r} does not match server regex {_SLUG_RE.pattern}"
            )

        # 2. Version required
        if not version:
            return self._err(
                "--version is required for skillhub-cn (no auto-bump)"
            )

        # 3. Description from SKILL.md frontmatter (required field on hub)
        description = extra.get("description") or self._read_description(skill_dir)
        if not description:
            return self._err(
                "description missing; add it to SKILL.md frontmatter or pass --description"
            )

        display_name = extra.get("display_name") or slug

        # 4. Build payload + multipart body
        payload_dict = {
            "slug": slug,
            "name": slug,
            "displayName": display_name,
            "version": version,
            "description": description,
        }
        # Optional changelog field (server may or may not accept; harmless)
        if changelog:
            payload_dict["changelog"] = changelog
        # Allow optional joinContest / claimSlug via extra
        if extra.get("claim_slug"):
            payload_dict["claimSlug"] = True
        if extra.get("join_contest"):
            payload_dict["joinContest"] = True

        fields = {"payload": json.dumps(payload_dict, ensure_ascii=False)}
        body, content_type, file_count = build_multipart_from_tarball(
            fields, tar_path, slug
        )
        if file_count == 0:
            return self._err("no files in package")

        # 5. POST publish (handle 429 with simple retry)
        for attempt in range(3):
            code, resp = self._request(
                "POST",
                "/api/v1/community/skills/publish",
                body=body, content_type=content_type, timeout=60,
            )
            if code in (200, 201):
                action = "publish-update" if resp.get("isUpdate") else "publish-new"
                url = f"https://skillhub.cn/skills/{slug}"
                return self._ok(
                    slug=slug, version=version, url=url, action=action, raw=resp
                )
            if code == 429:
                wait = resp.get("windowSec", 60)
                print(
                    f"  WARN: skillhub-cn rate-limited; waiting {wait}s "
                    f"(attempt {attempt + 1}/3)...",
                    file=sys.stderr,
                )
                time.sleep(wait + 1)
                continue
            # Other error
            return self._err(
                f"publish failed: HTTP {code} {resp.get('error') or resp.get('message', '')}",
                raw=resp,
            )

        return self._err("publish failed after 3 retries (rate-limited)")

    # ── Owner-only helpers (for cleanup / debugging) ─────────────────────

    def unlist(self, slug: str) -> Tuple[bool, str]:
        if err := self._ensure_identity():
            return False, err
        code, body = self._request(
            "POST",
            f"/api/v1/community/skills/{slug}/unlist",
            body=b"{}", content_type="application/json",
        )
        if code == 200 and body.get("unlisted"):
            return True, ""
        return False, f"HTTP {code} {body.get('error', '')}"

    def delete(self, slug: str) -> Tuple[bool, str]:
        if err := self._ensure_identity():
            return False, err
        code, body = self._request(
            "DELETE", f"/api/v1/community/skills/{slug}",
        )
        if code == 200 and body.get("deleted"):
            return True, ""
        return False, f"HTTP {code} {body.get('error', '')}"

    # ── Helpers ──────────────────────────────────────────────────────────

    @staticmethod
    def _read_description(skill_dir: str) -> str:
        """Read description from SKILL.md frontmatter.
        Stdlib-only: handles `description: "..."` single-line and YAML
        folded scalar (`> ` / `|`) multi-line.
        Optionally uses PyYAML when present (faster + more correct on edge
        cases) but never requires it."""
        md_path = os.path.join(skill_dir, "SKILL.md")
        if not os.path.isfile(md_path):
            return ""
        try:
            with open(md_path, encoding="utf-8") as f:
                content = f.read()
            m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
            if not m:
                return ""
            fm_text = m.group(1)

            # Optional: PyYAML if installed (handles edge cases like inline
            # JSON-style maps); otherwise fall through to manual parser.
            try:
                import yaml  # type: ignore
                fm = yaml.safe_load(fm_text) or {}
                desc = fm.get("description", "")
                if isinstance(desc, str) and desc.strip():
                    return " ".join(desc.split())  # collapse whitespace
            except ImportError:
                pass

            # Stdlib fallback: handles `description: "..."` and folded `>`
            lines = fm_text.splitlines()
            for i, line in enumerate(lines):
                stripped = line.strip()
                if not stripped.startswith("description:"):
                    continue
                rest = stripped.split(":", 1)[1].strip()
                if rest in (">", "|", ">-", "|-"):
                    # Folded/literal scalar - collect indented continuation lines
                    out_parts = []
                    for next_line in lines[i + 1:]:
                        if next_line.startswith(" ") or next_line.startswith("\t"):
                            out_parts.append(next_line.strip())
                        else:
                            break
                    return " ".join(out_parts)
                # Single-line value
                return rest.strip('"').strip("'")
        except Exception:
            pass
        return ""


__all__ = ["SkillhubCnAdapter"]
