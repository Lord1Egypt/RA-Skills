#!/usr/bin/env python3
"""Standalone Zotero Web API helpers for zotero-pdf-upload skill."""


import hashlib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

_COLLECTION_KEY_RE = re.compile(r"^[A-Z0-9]{8}$")


def _normalize_library_type(value: str) -> str:
    value = (value or "").strip().lower()
    if value in {"group", "groups"}:
        return "group"
    if value in {"user", "users"}:
        return "user"
    return ""


@dataclass
class LibrarySettings:
    library_type: str
    library_id: str
    api_key: str
    api_key_source: str = ""


class ConfigError(RuntimeError):
    """Raised when runtime config is invalid."""


def parse_zotero_library_url(url: str) -> Dict[str, str]:
    """Parse common Zotero URLs into library settings.

    Supports URLs like:
    - https://www.zotero.org/groups/6320165/group-name/library
    - https://www.zotero.org/users/123456/library
    - https://www.zotero.org/groups/6320165/group-name/collections/ABCDEFGH
    - https://www.zotero.org/groups/6320165/group-name/items/ITEMKEY
    - https://www.zotero.org/groups/6320165/items?library=groups/6320165
    - https://www.zotero.org/myusername/library          (personal URL)
    - https://www.zotero.org/myusername/collections/KEY   (personal URL)
    """
    raw = (url or "").strip()
    if not raw:
        return {}

    if "://" not in raw:
        raw = f"https://{raw}"

    parsed = urllib.parse.urlparse(raw)
    path_parts = [p for p in parsed.path.split("/") if p]
    query = urllib.parse.parse_qs(parsed.query)

    result: Dict[str, str] = {}

    # Query format used by embedded readers: ?library=groups/6320165
    for q_value in query.get("library", []):
        m = re.search(r"(groups|users)/(\d+)", q_value)
        if m:
            result["libraryType"] = "group" if m.group(1) == "groups" else "user"
            result["libraryId"] = m.group(2)
            break

    if not result:
        for kind in ("groups", "users"):
            if kind in path_parts:
                idx = path_parts.index(kind)
                if idx + 1 < len(path_parts) and path_parts[idx + 1].isdigit():
                    result["libraryType"] = "group" if kind == "groups" else "user"
                    result["libraryId"] = path_parts[idx + 1]
                    break

    # Fallback: personal URL like /myusername/library or /myusername/collections/KEY
    # The first path segment is a username (not "groups" or "users") and the URL
    # host looks like zotero.org.
    if not result and path_parts:
        _RESERVED = {"groups", "users", "support", "settings", "search", "static", "api"}
        first = path_parts[0].lower()
        is_zotero_host = "zotero.org" in (parsed.hostname or "")
        if is_zotero_host and first not in _RESERVED and not first.isdigit():
            # Looks like a personal/username URL
            result["libraryType"] = "user"
            result["username"] = path_parts[0]

    if "collections" in path_parts:
        cidx = path_parts.index("collections")
        if cidx + 1 < len(path_parts):
            key = path_parts[cidx + 1].upper()
            if _COLLECTION_KEY_RE.match(key):
                result["collectionKey"] = key

    return result


def _read_secret_file(path: str) -> str:
    if not path:
        return ""
    p = Path(path).expanduser()
    if not p.exists() or not p.is_file():
        return ""
    return p.read_text(encoding="utf-8").strip()


def load_api_key(config: Dict[str, Any]) -> Tuple[str, str]:
    """Load API key with safe precedence.

    Precedence:
    1) env variable (apiKeyEnv, default ZOTERO_API_KEY)
    2) file path (apiKeyPath)
    3) inline literal (apiKey)
    """
    env_name = (config.get("apiKeyEnv") or "ZOTERO_API_KEY").strip()
    if env_name:
        env_value = (os.environ.get(env_name) or "").strip()
        if env_value:
            return env_value, f"env:{env_name}"

    file_value = _read_secret_file(str(config.get("apiKeyPath") or ""))
    if file_value:
        return file_value, f"path:{config.get('apiKeyPath')}"

    inline = (config.get("apiKey") or "").strip()
    if inline:
        return inline, "inline:apiKey"

    return "", ""


def resolve_user_id_from_key(api_key: str, timeout: int = 30) -> str:
    """Resolve numeric userID by querying GET /keys/{apiKey}.

    The Zotero API returns the userID associated with the given key.
    This is used when a personal URL contains a username instead of an ID.
    """
    url = f"https://api.zotero.org/keys/{api_key}"
    req = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Zotero-API-Version": "3",
            "Accept": "application/json",
            "User-Agent": "zotero-pdf-upload/0.1",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
            user_id = str(data.get("userID") or "").strip()
            if not user_id:
                raise ConfigError("Zotero API /keys/ response did not contain a userID")
            return user_id
    except urllib.error.HTTPError as exc:
        raise ConfigError(f"Failed to resolve userID from API key: HTTP {exc.code}") from exc


def resolve_library_settings(raw_config: Dict[str, Any], require_api_key: bool = True) -> LibrarySettings:
    zotero = raw_config.get("zotero") if isinstance(raw_config.get("zotero"), dict) else {}

    # Accept unified "url" field, falling back to legacy "groupUrl" / "libraryUrl"
    url_value = str(
        zotero.get("url") or zotero.get("groupUrl") or zotero.get("libraryUrl") or ""
    )
    parsed = parse_zotero_library_url(url_value)

    library_type = _normalize_library_type(str(zotero.get("libraryType") or parsed.get("libraryType") or ""))
    library_id = str(zotero.get("libraryId") or parsed.get("libraryId") or "").strip()

    # Load the API key early so we can use it for user ID resolution if needed
    api_key, source = load_api_key(zotero)
    if require_api_key and not api_key:
        raise ConfigError(
            "Missing Zotero API key. Set zotero.apiKeyEnv or zotero.apiKeyPath or zotero.apiKey"
        )

    # If a personal URL was detected (has username but no libraryId),
    # resolve the numeric userID from the API key.
    if not library_id and parsed.get("username") and library_type == "user":
        if not api_key:
            raise ConfigError(
                "Personal URL detected but no API key available to resolve userID. "
                "Provide zotero.libraryId explicitly or configure an API key."
            )
        timeout = int(zotero.get("timeoutSec", 30))
        library_id = resolve_user_id_from_key(api_key, timeout=timeout)

    if not library_type:
        raise ConfigError("Cannot determine library type. Provide a Zotero URL or set zotero.libraryType.")
    if not library_id:
        raise ConfigError("Cannot determine library ID. Provide a Zotero URL or set zotero.libraryId.")

    return LibrarySettings(
        library_type=library_type,
        library_id=library_id,
        api_key=api_key,
        api_key_source=source,
    )


class ZoteroClient:
    BASE_URL = "https://api.zotero.org"

    def __init__(self, api_key: str, library_id: str, library_type: str = "user", timeout: int = 30):
        if not api_key:
            raise ConfigError("api_key is required")
        self.api_key = api_key
        self.library_id = str(library_id)
        self.library_type = _normalize_library_type(library_type) or "user"
        self.timeout = int(timeout)

    @property
    def _library_path(self) -> str:
        return f"/{self.library_type}s/{self.library_id}"

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        payload: Any = None,
        form: Optional[Dict[str, Any]] = None,
        extra_headers: Optional[Dict[str, str]] = None,
        expect_json: bool = True,
    ) -> Any:
        query = urllib.parse.urlencode(params or {})
        url = f"{self.BASE_URL}{path}"
        if query:
            url = f"{url}?{query}"

        body = None
        headers = {
            "Zotero-API-Key": self.api_key,
            "Zotero-API-Version": "3",
            "Accept": "application/json" if expect_json else "*/*",
            "User-Agent": "zotero-pdf-upload/0.1",
        }

        if payload is not None and form is not None:
            raise ValueError("payload and form cannot both be set")

        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif form is not None:
            body = urllib.parse.urlencode(form).encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        if extra_headers:
            headers.update(extra_headers)

        req = urllib.request.Request(url, method=method.upper(), headers=headers, data=body)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read()
                if not raw:
                    return {} if expect_json else ""
                text = raw.decode("utf-8", errors="replace")
                return json.loads(text) if expect_json else text
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code} for {method.upper()} {path}: {detail}")

    def list_collections(self, limit: int = 100, start: int = 0) -> List[Dict[str, Any]]:
        path = f"{self._library_path}/collections"
        data = self._request(
            "GET",
            path,
            params={"format": "json", "include": "data", "limit": int(limit), "start": int(start)},
        )
        return data if isinstance(data, list) else []

    def list_collections_paged(self, max_items: int = 500, page_size: int = 100) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        start = 0
        while len(out) < max_items:
            batch = self.list_collections(limit=min(page_size, max_items - len(out)), start=start)
            if not batch:
                break
            out.extend(batch)
            if len(batch) < page_size:
                break
            start += len(batch)
        return out

    @staticmethod
    def _norm_text(text: str) -> str:
        return " ".join((text or "").lower().split())

    @staticmethod
    def _collection_name(collection: Dict[str, Any]) -> str:
        data = collection.get("data", {}) if isinstance(collection, dict) else {}
        return str(data.get("name") or collection.get("name") or "")

    @staticmethod
    def _tokenize_for_match(text: str) -> List[str]:
        value = text or ""
        latin = re.findall(r"[a-zA-Z][a-zA-Z0-9\-]{1,}", value.lower())
        cjk = re.findall(r"[\u4e00-\u9fff]{2,}", value)
        stop = {"the", "and", "for", "with", "paper", "papers", "study", "using", "from", "into"}
        return [t for t in latin if t not in stop] + cjk

    @classmethod
    def find_best_matching_collection(
        cls,
        item: Dict[str, Any],
        collections: Sequence[Dict[str, Any]],
        collection_name_hint: str = "",
    ) -> Tuple[Optional[Dict[str, Any]], float, str]:
        hint_norm = cls._norm_text(collection_name_hint)

        item_text = " ".join(
            [
                str(item.get("title") or ""),
                str(item.get("abstractNote") or item.get("summary") or ""),
                " ".join(item.get("tags", []) if isinstance(item.get("tags"), list) else []),
            ]
        )
        item_tokens = set(cls._tokenize_for_match(item_text))

        best: Optional[Dict[str, Any]] = None
        best_score = 0.0
        best_reason = ""

        for col in collections:
            name = cls._collection_name(col)
            if not name:
                continue

            name_norm = cls._norm_text(name)
            name_tokens = set(cls._tokenize_for_match(name))
            score = 0.0
            reasons: List[str] = []

            if hint_norm:
                if name_norm == hint_norm:
                    score += 80.0
                    reasons.append("exact-name-hint")
                elif hint_norm in name_norm or name_norm in hint_norm:
                    score += 35.0
                    reasons.append("partial-name-hint")

            overlap = len(name_tokens & item_tokens)
            if overlap > 0:
                score += float(overlap) * 2.0
                reasons.append(f"token-overlap={overlap}")

            if overlap > 0 and len(name_tokens) > 1:
                score += 0.5

            if score > best_score:
                best = col
                best_score = score
                best_reason = ",".join(reasons) if reasons else "score"

        if best is None:
            return None, 0.0, "no-collection-match"
        if best_score < 2.0 and not hint_norm:
            return None, best_score, "weak-collection-match"
        return best, best_score, best_reason

    @staticmethod
    def suggest_collection_name(item: Dict[str, Any]) -> str:
        title = " ".join((item.get("title") or "").split())
        if len(title) > 28:
            title = f"{title[:28].rstrip()}…"
        if not title:
            title = "untitled-item"

        tags = item.get("tags", []) if isinstance(item.get("tags"), list) else []
        first_tag = str(tags[0]).strip() if tags else "General"
        return f"{first_tag}-{title}"

    @staticmethod
    def _split_name(full_name: str, creator_type: str = "author") -> Dict[str, str]:
        full_name = " ".join((full_name or "").split())
        if not full_name:
            return {"firstName": "", "lastName": "", "creatorType": creator_type}

        parts = full_name.split(" ")
        if len(parts) == 1:
            return {"name": parts[0], "creatorType": creator_type}

        return {
            "firstName": " ".join(parts[:-1]),
            "lastName": parts[-1],
            "creatorType": creator_type,
        }

    def create_collection(self, name: str, parent_collection_key: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"name": name}
        if parent_collection_key:
            payload["parentCollection"] = parent_collection_key

        return self._request(
            "POST",
            f"{self._library_path}/collections",
            params={"format": "json"},
            payload=[payload],
        )

    @staticmethod
    def _normalize_tags(tags: Sequence[Any]) -> List[Dict[str, str]]:
        out: List[Dict[str, str]] = []
        for tag in tags:
            value = str(tag).strip()
            if value:
                out.append({"tag": value})
        return out

    def build_item_payload(
        self,
        item: Dict[str, Any],
        collection_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        creators: List[Dict[str, str]] = []
        for creator in item.get("creators", []):
            if isinstance(creator, dict):
                creators.append(
                    {
                        "firstName": str(creator.get("firstName") or ""),
                        "lastName": str(creator.get("lastName") or ""),
                        "creatorType": str(creator.get("creatorType") or "author"),
                    }
                )
            else:
                creators.append(self._split_name(str(creator), creator_type="author"))

        payload = {
            "itemType": item.get("itemType", "journalArticle"),
            "title": item.get("title", ""),
            "creators": creators,
            "abstractNote": item.get("abstractNote", ""),
            "date": item.get("date", ""),
            "url": item.get("url", ""),
            "DOI": item.get("DOI", ""),
            "archive": item.get("archive", ""),
            "archiveLocation": item.get("archiveLocation", ""),
            "extra": item.get("extra", ""),
            "tags": self._normalize_tags(item.get("tags", [])),
            "collections": [collection_key] if collection_key else [],
        }

        return payload

    @staticmethod
    def _extract_success_key(resp: Dict[str, Any]) -> Optional[str]:
        successful = resp.get("successful") if isinstance(resp, dict) else None
        if not isinstance(successful, dict):
            return None
        first = next(iter(successful.values()), {})
        if isinstance(first, dict):
            return str(first.get("key") or "") or None
        return None

    def create_item(self, item_payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "POST",
            f"{self._library_path}/items",
            params={"format": "json"},
            payload=[item_payload],
        )

    @staticmethod
    def _md5_file(path: str) -> str:
        md5 = hashlib.md5()
        with open(path, "rb") as f:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                md5.update(chunk)
        return md5.hexdigest()

    def _create_attachment_item(self, parent_item_key: str, pdf_path: str, title: str = "") -> str:
        filename = os.path.basename(pdf_path)
        payload = {
            "itemType": "attachment",
            "parentItem": parent_item_key,
            "linkMode": "imported_file",
            "title": title or filename,
            "accessDate": "",
            "note": "",
            "tags": [],
            "relations": {},
            "contentType": "application/pdf",
            "charset": "",
            "filename": filename,
            "md5": None,
            "mtime": None,
        }

        resp = self.create_item(payload)
        key = self._extract_success_key(resp)
        if not key:
            raise RuntimeError(f"failed to create attachment item metadata: {resp}")
        return key

    def _authorize_file_upload(self, attachment_key: str, pdf_path: str) -> Dict[str, Any]:
        stat = os.stat(pdf_path)
        form = {
            "md5": self._md5_file(pdf_path),
            "filename": os.path.basename(pdf_path),
            "filesize": str(stat.st_size),
            "mtime": str(int(stat.st_mtime * 1000)),
        }
        path = f"{self._library_path}/items/{attachment_key}/file"
        try:
            return self._request("POST", path, form=form, extra_headers={"If-None-Match": "*"})
        except Exception as exc:
            if "HTTP 412" in str(exc) and "file exists" in str(exc).lower():
                return {"exists": 1}
            raise

    @staticmethod
    def _upload_file_bytes(upload_info: Dict[str, Any], pdf_path: str, timeout: int = 120) -> None:
        url = str(upload_info.get("url") or "")
        content_type = str(upload_info.get("contentType") or "")
        prefix = upload_info.get("prefix")
        suffix = upload_info.get("suffix")

        if not (url and content_type and isinstance(prefix, str) and isinstance(suffix, str)):
            raise RuntimeError(f"invalid upload authorization response: {upload_info}")

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        body = prefix.encode("utf-8") + pdf_bytes + suffix.encode("utf-8")
        req = urllib.request.Request(
            url,
            method="POST",
            data=body,
            headers={
                "Content-Type": content_type,
                "User-Agent": "zotero-pdf-upload/0.1",
            },
        )

        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status not in (200, 201, 204):
                raise RuntimeError(f"unexpected upload HTTP status: {resp.status}")

    def _register_file_upload(self, attachment_key: str, upload_key: str) -> None:
        path = f"{self._library_path}/items/{attachment_key}/file"
        try:
            self._request(
                "POST",
                path,
                form={"upload": upload_key},
                extra_headers={"If-None-Match": "*"},
                expect_json=False,
            )
            return
        except Exception as exc:
            if "HTTP 412" not in str(exc):
                raise

        self._request("POST", path, form={"upload": upload_key}, expect_json=False)

    def upload_pdf_attachment(self, parent_item_key: str, pdf_path: str, title: str = "") -> Dict[str, Any]:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(pdf_path)

        attachment_key = self._create_attachment_item(parent_item_key=parent_item_key, pdf_path=pdf_path, title=title)
        auth = self._authorize_file_upload(attachment_key=attachment_key, pdf_path=pdf_path)

        if isinstance(auth, dict) and int(auth.get("exists", 0)) == 1:
            return {"status": "exists", "attachment_key": attachment_key}

        upload_key = str(auth.get("uploadKey") if isinstance(auth, dict) else "")
        if not upload_key:
            raise RuntimeError(f"missing uploadKey in upload authorization: {auth}")

        self._upload_file_bytes(upload_info=auth, pdf_path=pdf_path, timeout=max(120, self.timeout))
        self._register_file_upload(attachment_key=attachment_key, upload_key=upload_key)

        return {
            "status": "uploaded",
            "attachment_key": attachment_key,
            "upload_key": upload_key,
        }


__all__ = [
    "ConfigError",
    "LibrarySettings",
    "ZoteroClient",
    "load_api_key",
    "parse_zotero_library_url",
    "resolve_library_settings",
    "resolve_user_id_from_key",
]
