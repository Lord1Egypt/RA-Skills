import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


BASE_URL = os.environ.get("UEXX_DATA_BASE_URL", "https://bbs.uexx.com").rstrip("/")
STATE_DIR = Path(os.environ.get("UEXX_DATA_STATE_DIR", Path.home() / ".uexx-data-cloud"))
KEY_FILE = STATE_DIR / "free_key.json"


class UEXXError(RuntimeError):
    pass


def request_json(path: str, method: str = "GET", api_key: str | None = None, body: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None
    headers = {"Accept": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE_URL + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode("utf-8"))
        except Exception:
            payload = {"detail": str(exc)}
        raise UEXXError(payload.get("detail") or payload.get("message") or str(exc)) from exc


def save_key(payload: dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    payload = dict(payload)
    payload["saved_at"] = time.time()
    KEY_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_key() -> str | None:
    if not KEY_FILE.exists():
        return None
    try:
        payload = json.loads(KEY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None
    key = payload.get("api_key")
    if not key:
        return None
    return str(key)


def get_or_create_key() -> str:
    key = load_key()
    if key:
        return key
    payload = request_json("/api/v1/free-key", method="POST")
    key = payload.get("api_key")
    if not key:
        raise UEXXError("Free Key response did not include api_key")
    save_key(payload)
    return str(key)


def authed_get(path: str) -> dict[str, Any]:
    key = get_or_create_key()
    try:
        return request_json(path, api_key=key)
    except UEXXError as exc:
        if "invalid or missing" in str(exc).lower() or "expired" in str(exc).lower():
            if KEY_FILE.exists():
                KEY_FILE.unlink()
            key = get_or_create_key()
            return request_json(path, api_key=key)
        raise
