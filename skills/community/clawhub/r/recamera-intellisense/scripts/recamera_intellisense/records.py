"""Record browsing via the relay + nginx autoindex (paths are relative to the slot's data dir)."""

from __future__ import annotations

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from recamera_intellisense._cli import main

    raise SystemExit(main())

import base64
import json
from typing import Any, Dict, List, Optional

from . import _config, _http
from . import relay as _relay
from ._const import IMAGE_EXTENSIONS, MAX_INLINE_BYTES
from ._errors import RecameraError

__all__ = ["list_records", "fetch_record"]

LIST_RECORDS_DEFAULT_LIMIT = 100
LIST_RECORDS_MAX_LIMIT = 500


def _relay_endpoint(uuid: str, rel: str, *, directory: bool = False) -> str:
    rel = rel.strip("/")
    if not rel:
        return f"/storage/relay/{uuid}/"
    if directory:
        return f"/storage/relay/{uuid}/{rel}/"
    return f"/storage/relay/{uuid}/{rel}"


def list_records(
    device_name: Optional[str] = None,
    *,
    path: str = "",
    dev_path: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Dict[str, Any]:
    """List the directory at *path* (relative to the record data directory).

    Returns a paginated dict (matching the MCP `list_records` tool)::

        {
          "entries": [{"name", "is_dir", "size?", "mtime?"}, ...],
          "offset": int,
          "limit": int,
          "total": int,
          "has_more": bool,
        }

    Directories sort first, then entries are ordered by name for stable pagination.
    `limit` defaults to 100 and is clamped to `[1, 500]`; `offset` defaults to 0
    and is clamped to the total entry count.
    """
    dev = _config.resolve(device_name)
    resolved_dev_path, uuid = _relay.ensure_relay_uuid(device_name, dev_path)
    del resolved_dev_path
    endpoint = _relay_endpoint(uuid, path, directory=True)
    body, _ = _http.get_bytes(dev, endpoint)
    entries = _parse_autoindex(body)
    return _paginate_entries(entries, limit=limit, offset=offset)


def _paginate_entries(
    entries: List[Dict[str, Any]],
    *,
    limit: Optional[int],
    offset: Optional[int],
) -> Dict[str, Any]:
    entries = sorted(
        entries,
        key=lambda e: (0 if e.get("is_dir") else 1, str(e.get("name", ""))),
    )
    total = len(entries)
    off = max(0, int(offset) if offset is not None else 0)
    off = min(off, total)
    lim = int(limit) if limit is not None else LIST_RECORDS_DEFAULT_LIMIT
    lim = max(1, min(lim, LIST_RECORDS_MAX_LIMIT))
    end = min(off + lim, total)
    return {
        "entries": entries[off:end],
        "offset": off,
        "limit": lim,
        "total": total,
        "has_more": end < total,
    }


def _parse_autoindex(body: bytes) -> List[Dict[str, Any]]:
    try:
        data = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RecameraError(
            "Directory listing is not JSON (autoindex disabled?)"
        ) from exc
    if isinstance(data, dict) and "code" in data and "name" not in data:
        raise RecameraError(
            f"Directory listing not supported by device "
            f"(code={data.get('code')}): {data.get('message', 'unknown error')}"
        )
    if not isinstance(data, list):
        raise RecameraError("Autoindex response is not a JSON array.")
    out: List[Dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        raw_type = str(item.get("type", "")).lower()
        entry: Dict[str, Any] = {
            "name": item.get("name", ""),
            "is_dir": raw_type == "directory",
        }
        if "size" in item:
            entry["size"] = int(item["size"])
        if item.get("mtime") is not None:
            entry["mtime"] = item.get("mtime")
        out.append(entry)
    return out


def fetch_record(
    device_name: Optional[str] = None,
    *,
    path: str,
    dev_path: Optional[str] = None,
    max_inline_bytes: int = MAX_INLINE_BYTES,
) -> Dict[str, Any]:
    """Fetch a recorded file via the relay.

    Returns one of:
      * `{path, content_type, content_base64, size, url}` — images or payloads ≤ 5 MiB.
      * `{path, url, size, content_type, note}` — payload too large to inline.

    The returned relay `url` needs no credentials, but it embeds a random UUID
    (unguessable, capability-style) and dies with the relay TTL (device default
    300s); still avoid sharing it.
    """
    dev = _config.resolve(device_name)
    _, uuid = _relay.ensure_relay_uuid(device_name, dev_path)
    rel = path.strip("/")
    endpoint = _relay_endpoint(uuid, rel)
    body, ct = _http.get_bytes(dev, endpoint)
    url = _relay.build_relay_url(dev["name"], uuid, rel)
    is_image = any(rel.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)
    if is_image or len(body) <= max_inline_bytes:
        return {
            "path": rel,
            "content_type": ct,
            "content_base64": base64.b64encode(body).decode("ascii"),
            "size": len(body),
            "url": url,
        }
    return {
        "path": rel,
        "url": url,
        "size": len(body),
        "content_type": ct,
        "note": "payload exceeds inline budget; fetch the URL directly — the "
        "relay URL needs no credentials but embeds a random UUID (unguessable) "
        "and dies with the relay TTL (default 300s); still avoid sharing it.",
    }


COMMANDS = {
    "list_records": list_records,
    "fetch_record": fetch_record,
}
