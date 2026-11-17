import base64
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request

from catalog import catalog_entry, catalog_from_raw, render_index
from utils import now, sha256_text


class GiteaClient:
    def __init__(self, payload=None):
        platform = (payload or {}).get("platform") or {}
        team = (payload or {}).get("team") or {}
        self.url = (platform.get("giteaUrl") or os.getenv("GITEA_URL") or "").rstrip("/")
        self.token = os.getenv("GITEA_BOT_TOKEN") or ""
        self.owner = platform.get("giteaOwner") or os.getenv("GITEA_ORG") or os.getenv("GITEA_BOT_USERNAME") or ""
        self.repo = team.get("kbRepo") or os.getenv("TEAM_KB_REPO") or "team-kb"
        self.dry_run = str(os.getenv("RESEARCH_KB_DRY_RUN") or "").strip().lower() in {"1", "true", "yes", "on"}
        missing = [
            name for name, value in (
                ("GITEA_URL", self.url),
                ("GITEA_BOT_TOKEN", self.token),
                ("GITEA_OWNER", self.owner),
                ("TEAM_KB_REPO", self.repo),
            ) if not value
        ]
        if missing and not self.dry_run:
            raise RuntimeError("Gitea write configuration is incomplete: " + ", ".join(missing))
        self.last_commit = "dry-run"

    def upsert_text(self, path, content, message):
        if self.dry_run:
            self.last_commit = "dry-run-" + sha256_text(path + content)[:12]
            return {"path": path, "commit": self.last_commit}
        sha = self._existing_sha(path)
        payload = {"message": message, "content": base64.b64encode(content.encode("utf-8")).decode("ascii")}
        if sha:
            payload["sha"] = sha
        response = self._request("PUT", f"/repos/{self._q(self.owner)}/{self._q(self.repo)}/contents/{self._path(path)}", payload)
        commit = response.get("commit") or {}
        self.last_commit = commit.get("id") or commit.get("sha") or "unknown"
        return {"path": path, "commit": self.last_commit}

    def upsert_bytes(self, path, data, message):
        if self.dry_run:
            self.last_commit = "dry-run-" + hashlib.sha256(path.encode("utf-8") + data).hexdigest()[:12]
            return {"path": path, "commit": self.last_commit}
        sha = self._existing_sha(path)
        payload = {"message": message, "content": base64.b64encode(data).decode("ascii")}
        if sha:
            payload["sha"] = sha
        response = self._request("PUT", f"/repos/{self._q(self.owner)}/{self._q(self.repo)}/contents/{self._path(path)}", payload)
        commit = response.get("commit") or {}
        self.last_commit = commit.get("id") or commit.get("sha") or "unknown"
        return {"path": path, "commit": self.last_commit}

    def read_text(self, path):
        if self.dry_run:
            return ""
        try:
            response = self._request("GET", f"/repos/{self._q(self.owner)}/{self._q(self.repo)}/contents/{self._path(path)}")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return ""
            raise
        content = response.get("content") or ""
        return base64.b64decode(content).decode("utf-8", errors="replace") if content else ""

    def exists(self, path):
        if self.dry_run:
            return False
        return self._existing_sha(path) is not None

    def update_catalog(self, page):
        if self.dry_run or not page.get("path"):
            return
        catalog = catalog_from_raw(self.read_text("catalog.json"))
        pages = [item for item in (catalog.get("pages") or []) if item.get("path") != page.get("path")]
        pages.append(catalog_entry(page))
        pages.sort(key=lambda item: item.get("path") or "")
        catalog["version"] = 1
        catalog["updatedAt"] = now()
        catalog["pages"] = pages
        self.upsert_text("catalog.json", json.dumps(catalog, ensure_ascii=False, indent=2), "Update catalog.json")
        self.update_index(catalog)

    def update_index(self, catalog):
        if self.dry_run:
            return
        self.upsert_text("index.md", render_index(catalog), "Update index.md")

    def _existing_sha(self, path):
        try:
            existing = self._request("GET", f"/repos/{self._q(self.owner)}/{self._q(self.repo)}/contents/{self._path(path)}")
            return existing.get("sha")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            raise

    def _request(self, method, endpoint, body=None):
        data = None
        headers = {"Authorization": f"token {self.token}", "Accept": "application/json"}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(self.url + "/api/v1" + endpoint, data=data, headers=headers, method=method)
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}

    @staticmethod
    def _q(value):
        return urllib.parse.quote(str(value), safe="")

    @staticmethod
    def _path(value):
        return urllib.parse.quote(str(value).replace("\\", "/"), safe="/")
