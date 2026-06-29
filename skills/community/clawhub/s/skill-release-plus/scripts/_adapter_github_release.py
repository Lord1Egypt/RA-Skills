#!/usr/bin/env python3
"""
_adapter_github_release.py — GitHub Releases adapter.

Publishes a skill to GitHub by:
  1. Pushing the skill folder to a target GitHub repository
     (auto-creates the repo if missing)
  2. Creating a tag v<version> on the latest commit
  3. Creating a GitHub Release with the tar.gz package as an attached asset

Uses pure git + GitHub REST API (no `gh` CLI dependency).

Config (via SRP_* env or CLI):
  SRP_GITHUB_TOKEN              required; PAT with repo scope
  SRP_GITHUB_OWNER              required; user/org under which the repo lives
                                (auto-detected from token if omitted)
  SRP_GITHUB_REPO               optional; default = skill slug
                                ⚠️ Can also be "<owner>/<repo>/<subdir>" form
                                for monorepo layout (e.g. suite repos)
  SRP_GITHUB_BRANCH             optional; default = main
  SRP_GITHUB_BASIC_AUTH_HEADER  optional; if "true", use Basic Auth header instead
                                of HTTPS URL embedding (needed in some corp networks
                                where token-in-URL is rejected)
"""
from __future__ import annotations

import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from typing import Optional, Tuple

from _lib_adapters_base import BaseAdapter, PublishResult, InspectResult


GITHUB_API = "https://api.github.com"


class GitHubReleaseAdapter(BaseAdapter):
    target_name = "github-release"

    def __init__(self, cfg: dict):
        super().__init__(cfg)
        self.token = cfg.get("SRP_GITHUB_TOKEN", "")
        self.owner = cfg.get("SRP_GITHUB_OWNER", "")
        self.repo_cfg = cfg.get("SRP_GITHUB_REPO", "")  # may include subdir
        self.branch = cfg.get("SRP_GITHUB_BRANCH", "main")
        self.use_basic_auth = (
            cfg.get("SRP_GITHUB_BASIC_AUTH_HEADER", "").lower() == "true"
        )

    # ── HTTP helpers ─────────────────────────────────────────────────────

    def _api_request(self, method: str, path: str,
                     body: dict = None,
                     extra_headers: dict = None) -> Tuple[int, dict]:
        url = f"{GITHUB_API}{path}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "skill-release-plus",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if extra_headers:
            headers.update(extra_headers)
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.status, json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as e:
            try:
                body = json.loads(e.read() or b"{}")
            except Exception:
                body = {}
            return e.code, body
        except Exception as e:
            return -1, {"error": str(e)}

    def _upload_asset(self, upload_url: str, name: str, file_path: str) -> Tuple[int, dict]:
        """Upload a binary asset to a GitHub release. upload_url has `{?name,label}` template."""
        # Strip template and append our own query
        base = upload_url.split("{")[0]
        url = f"{base}?name={name}"
        with open(file_path, "rb") as f:
            data = f.read()
        headers = {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "skill-release-plus",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/octet-stream",
            "Content-Length": str(len(data)),
        }
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.status, json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as e:
            try:
                body = json.loads(e.read() or b"{}")
            except Exception:
                body = {}
            return e.code, body
        except Exception as e:
            return -1, {"error": str(e)}

    # ── git helpers ──────────────────────────────────────────────────────

    def _git(self, cwd: str, *args, env_extra: dict = None) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        if env_extra:
            env.update(env_extra)
        cmd = ["git", *args]
        return subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=120, env=env,
        )

    def _remote_url_with_auth(self, owner: str, repo: str) -> str:
        """Return clone URL. If basic-auth-header mode is on, return plain URL
        and rely on extraHeader; else embed token in URL."""
        if self.use_basic_auth:
            return f"https://github.com/{owner}/{repo}.git"
        # Token embedded
        return f"https://x-access-token:{self.token}@github.com/{owner}/{repo}.git"

    def _git_extra_args_for_auth(self) -> list:
        if self.use_basic_auth:
            cred = f"x-access-token:{self.token}"
            b64 = base64.b64encode(cred.encode()).decode()
            return ["-c", f"http.extraHeader=Authorization: Basic {b64}"]
        return []

    # ── Repo / owner detection ───────────────────────────────────────────

    def _detect_owner(self) -> Optional[str]:
        if self.owner:
            return self.owner
        # Query /user with the token
        code, body = self._api_request("GET", "/user")
        if code == 200 and body.get("login"):
            self.owner = body["login"]
            return self.owner
        return None

    def _parse_repo_target(self, slug: str) -> Tuple[str, str, str]:
        """
        Returns (owner, repo, subdir).
        SRP_GITHUB_REPO formats supported:
          ""                        -> owner from _detect_owner, repo=slug, no subdir
          "myrepo"                  -> repo=myrepo (under self.owner)
          "owner/myrepo"            -> owner+repo
          "owner/myrepo/skills/foo" -> owner+repo+subdir
          "myrepo/skills/foo"       -> repo+subdir (under self.owner)
        """
        owner = self._detect_owner() or ""
        repo_cfg = self.repo_cfg or slug
        parts = [p for p in repo_cfg.split("/") if p]
        if len(parts) == 1:
            return owner, parts[0], ""
        if len(parts) >= 2 and "." not in parts[0] and len(parts[0]) > 0:
            # Heuristic: if first part looks like a username/org name, use it
            # Owner usernames don't contain dots and are typically short
            # We treat first part as owner when there's no explicit override
            owner_part = parts[0]
            repo_part = parts[1]
            subdir = "/".join(parts[2:])
            return owner_part, repo_part, subdir
        return owner, parts[0], "/".join(parts[1:])

    def _ensure_repo_exists(self, owner: str, repo: str) -> Optional[str]:
        """Return error message or None on success."""
        code, body = self._api_request("GET", f"/repos/{owner}/{repo}")
        if code == 200:
            return None
        if code == 404:
            # Create it (under owner if owner == self user, else as org repo)
            # Check if owner is the authenticated user
            who_code, who = self._api_request("GET", "/user")
            create_payload = {
                "name": repo,
                "auto_init": False,
                "private": False,
                "description": "Published by skill-release-plus",
            }
            if who_code == 200 and who.get("login", "").lower() == owner.lower():
                create_code, create_body = self._api_request(
                    "POST", "/user/repos", body=create_payload
                )
            else:
                create_code, create_body = self._api_request(
                    "POST", f"/orgs/{owner}/repos", body=create_payload
                )
            if create_code in (200, 201):
                return None
            return (f"failed to create repo {owner}/{repo}: "
                    f"HTTP {create_code} {create_body.get('message', '')}")
        return f"failed to access {owner}/{repo}: HTTP {code} {body.get('message', '')}"

    # ── Tag/Release helpers ──────────────────────────────────────────────

    def _create_release(self, owner: str, repo: str, version: str,
                        changelog: str) -> Tuple[Optional[dict], Optional[str]]:
        tag = f"v{version}" if not version.startswith("v") else version
        payload = {
            "tag_name": tag,
            "name": f"Release {tag}",
            "body": changelog or f"Release {tag}",
            "draft": False,
            "prerelease": False,
        }
        code, body = self._api_request(
            "POST", f"/repos/{owner}/{repo}/releases", body=payload
        )
        if code in (200, 201):
            return body, None
        # If release already exists, fetch it
        if code == 422 and any("already_exists" in str(e).lower()
                               for e in body.get("errors", [])):
            code2, body2 = self._api_request(
                "GET", f"/repos/{owner}/{repo}/releases/tags/{tag}"
            )
            if code2 == 200:
                return body2, None
        return None, (f"failed to create release {tag}: "
                      f"HTTP {code} {body.get('message', '')}")

    # ── BaseAdapter overrides ────────────────────────────────────────────

    def check_slug_available(self, slug: str) -> Optional[bool]:
        """For GitHub, 'slug availability' = repo doesn't exist yet."""
        owner = self._detect_owner()
        if not owner:
            return None
        repo_cfg = self.repo_cfg or slug
        # Use the first segment as repo for availability check
        repo = repo_cfg.split("/")[1] if "/" in repo_cfg else repo_cfg
        # Adjust if first segment was owner
        parts = [p for p in repo_cfg.split("/") if p]
        if len(parts) >= 2 and "." not in parts[0]:
            owner_to_check = parts[0]
            repo = parts[1]
        else:
            owner_to_check = owner
        code, _ = self._api_request("GET", f"/repos/{owner_to_check}/{repo}")
        if code == 404:
            return True
        if code == 200:
            return False
        return None

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

        # 0. Auth sanity
        if not self.token:
            return self._err("SRP_GITHUB_TOKEN is not set")

        # 1. Resolve target repo / subdir
        owner, repo, subdir = self._parse_repo_target(slug)
        if not owner:
            return self._err("cannot determine GitHub owner (set SRP_GITHUB_OWNER)")

        # 2. Ensure repo exists (create if needed)
        err = self._ensure_repo_exists(owner, repo)
        if err:
            return self._err(err)

        # 3. Resolve version (must be explicit for GitHub release tag)
        if not version:
            return self._err(
                "--version is required for github-release target (cannot auto-detect tag)"
            )

        # 4. Clone target repo into a temp dir, copy skill files, commit + push
        with tempfile.TemporaryDirectory(prefix="srp-gh-") as tmpdir:
            clone_url = self._remote_url_with_auth(owner, repo)
            extra_args = self._git_extra_args_for_auth()

            # Clone (or init empty)
            clone_dir = os.path.join(tmpdir, "repo")
            proc = self._git(
                tmpdir, *extra_args,
                "clone", "--depth", "1", "--branch", self.branch,
                clone_url, "repo",
            )
            if proc.returncode != 0:
                # Maybe empty repo (no branch yet) - init locally
                os.makedirs(clone_dir, exist_ok=True)
                self._git(clone_dir, "init", "-b", self.branch)
                self._git(clone_dir, "remote", "add", "origin", clone_url)

            # Configure identity (use authenticated user)
            user_code, user_body = self._api_request("GET", "/user")
            if user_code == 200:
                self._git(clone_dir, "config", "user.name",
                          user_body.get("name") or user_body.get("login", "skill-release-plus"))
                email = user_body.get("email") or f"{user_body.get('login', 'noreply')}@users.noreply.github.com"
                self._git(clone_dir, "config", "user.email", email)
            else:
                self._git(clone_dir, "config", "user.name", "skill-release-plus")
                self._git(clone_dir, "config", "user.email", "noreply@users.noreply.github.com")

            # Determine destination inside repo
            dest_in_repo = os.path.join(clone_dir, subdir) if subdir else clone_dir
            os.makedirs(dest_in_repo, exist_ok=True)

            # Copy skill files (respecting exclude rules via tar reuse)
            # Extract tar.gz contents (which already has exclusions applied) into dest
            import tarfile
            with tarfile.open(tar_path, "r:gz") as tar:
                # The tarball has entries prefixed with "<slug>/" - strip that prefix
                # when copying to a subdir, but keep when copying to repo root for clarity
                if subdir:
                    # Subdir layout: extract <slug>/* into dest_in_repo/
                    for member in tar.getmembers():
                        if member.name.startswith(slug + "/"):
                            member.name = member.name[len(slug) + 1:]
                        if member.name:
                            tar.extract(member, path=dest_in_repo, set_attrs=False)
                else:
                    # Root layout: extract to repo root keeping slug folder
                    tar.extractall(path=clone_dir)

            # git add + commit + push + tag
            self._git(clone_dir, "add", "-A")
            commit_msg = (
                f"Release {slug} v{version}\n\n{changelog}"
                if changelog else f"Release {slug} v{version}"
            )
            commit_proc = self._git(clone_dir, "commit", "-m", commit_msg)
            if commit_proc.returncode != 0:
                if "nothing to commit" not in commit_proc.stdout + commit_proc.stderr:
                    return self._err(
                        f"git commit failed: {commit_proc.stderr or commit_proc.stdout}"
                    )

            push_proc = self._git(
                clone_dir, *extra_args, "push", "-u", "origin", self.branch,
            )
            if push_proc.returncode != 0:
                return self._err(
                    f"git push failed: {push_proc.stderr or push_proc.stdout}"
                )

        # 5. Create release + upload tar.gz asset
        release, err = self._create_release(owner, repo, version, changelog)
        if err:
            # Push succeeded; release failed - return partial success
            return PublishResult(
                ok=False, target=self.target_name, slug=slug, version=version,
                error=f"push ok but release creation failed: {err}",
                url=f"https://github.com/{owner}/{repo}",
            )

        upload_url = release.get("upload_url", "")
        asset_name = os.path.basename(tar_path)
        if upload_url:
            asset_code, asset_body = self._upload_asset(upload_url, asset_name, tar_path)
            if asset_code not in (200, 201):
                print(
                    f"WARN: asset upload failed: HTTP {asset_code} {asset_body.get('message', '')}",
                    file=sys.stderr,
                )

        release_url = release.get("html_url") or f"https://github.com/{owner}/{repo}/releases/tag/v{version}"
        return self._ok(
            slug=slug,
            version=version,
            url=release_url,
            action="git-tag-and-release",
            raw={"owner": owner, "repo": repo, "subdir": subdir, "release_id": release.get("id")},
        )


__all__ = ["GitHubReleaseAdapter"]
