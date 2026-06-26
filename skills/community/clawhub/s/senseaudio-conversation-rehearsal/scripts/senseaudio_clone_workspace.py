#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import uuid
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple

from senseaudio_platform_token import apple_script


BASE_URL = "https://platform.senseaudio.cn/api"
DEFAULT_TIMEOUT = 120
DEFAULT_TOKEN_ENV = "SENSEAUDIO_PLATFORM_TOKEN"
DEFAULT_HEADERS = {
    "x-platform": "WEB",
    "x-version": "1.0.2",
    "x-language": "zh-cn",
    "x-product": "SenseAudio",
}
ALLOWED_SUFFIXES = {".mp3", ".wav", ".aac"}


def build_headers(token: str, content_type: Optional[str] = "application/json") -> Dict[str, str]:
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Codex-SenseAudio-Clone/1.0",
        "x-machine": str(uuid.uuid4()),
        **DEFAULT_HEADERS,
    }
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def parse_json_response(response) -> Any:
    charset = response.headers.get_content_charset() or "utf-8"
    raw = response.read().decode(charset, "replace")
    if not raw:
        return {}
    return json.loads(raw)


def request_json(
    method: str,
    path: str,
    token: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    payload: Optional[Dict[str, Any]] = None,
) -> Any:
    url = BASE_URL + path
    if params:
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        if query:
            url = f"{url}?{query}"
    data = None
    headers = build_headers(token)
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT) as response:
            return parse_json_response(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"{method} {path} failed with HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"{method} {path} network error: {exc}") from exc


def request_json_via_browser(method: str, path: str, *, params: Optional[Dict[str, Any]] = None, payload: Optional[Dict[str, Any]] = None) -> Any:
    url = BASE_URL + path
    if params:
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        if query:
            url = f"{url}?{query}"
    script = f"""
(() => {{
  const done = arguments[0];
  fetch({json.dumps(url)}, {{
    method: {json.dumps(method)},
    credentials: 'include',
    headers: {{'Content-Type': 'application/json'}},
    body: {json.dumps(json.dumps(payload, ensure_ascii=False) if payload is not None else None)}
  }})
    .then(async response => {{
      const text = await response.text();
      done(JSON.stringify({{ok: response.ok, status: response.status, text}}));
    }})
    .catch(error => done(JSON.stringify({{ok: false, status: 0, text: String(error)}})));
}})()
"""
    raw = apple_script(script)
    parsed = json.loads(raw) if raw else {}
    if not parsed.get("ok"):
        raise RuntimeError(f"{method} {path} via browser failed with HTTP {parsed.get('status')}: {parsed.get('text')}")
    text = parsed.get("text", "")
    return json.loads(text) if text else {}


def encode_multipart(fields: Dict[str, str], files: Iterable[Tuple[str, Path]]) -> Tuple[bytes, str]:
    boundary = f"----CodexSenseAudio{uuid.uuid4().hex}"
    chunks = []
    for name, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
                str(value).encode("utf-8"),
                b"\r\n",
            ]
        )
    for field_name, file_path in files:
        mime_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                (
                    f'Content-Disposition: form-data; name="{field_name}"; '
                    f'filename="{file_path.name}"\r\n'
                ).encode("utf-8"),
                f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"),
                file_path.read_bytes(),
                b"\r\n",
            ]
        )
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def create_clone(
    token: str,
    audio_path: Path,
    *,
    slot_id: Optional[str] = None,
    voice_name: str = "",
) -> Any:
    validate_audio(audio_path)
    fields: Dict[str, str] = {"filename": audio_path.name}
    if slot_id:
        fields["slot_id"] = str(slot_id)
    if voice_name:
        fields["voice_name"] = voice_name
    body, content_type = encode_multipart(fields, [("file", audio_path)])
    request = urllib.request.Request(
        BASE_URL + "/voice/clone",
        data=body,
        headers=build_headers(token, content_type=content_type),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT) as response:
            return parse_json_response(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"POST /voice/clone failed with HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"POST /voice/clone network error: {exc}") from exc


def create_clone_via_browser(
    audio_path: Path,
    *,
    slot_id: Optional[str] = None,
    voice_name: str = "",
) -> Any:
    validate_audio(audio_path)
    encoded_audio = base64.b64encode(audio_path.read_bytes()).decode("ascii")
    mime_type = mimetypes.guess_type(audio_path.name)[0] or "application/octet-stream"
    script = f"""
(() => {{
  const done = arguments[0];
  const decodeBase64 = base64 => Uint8Array.from(atob(base64), c => c.charCodeAt(0));
  const bytes = decodeBase64({json.dumps(encoded_audio)});
  const file = new File([bytes], {json.dumps(audio_path.name)}, {{ type: {json.dumps(mime_type)} }});
  const formData = new FormData();
  formData.append('file', file);
  formData.append('filename', {json.dumps(audio_path.name)});
  if ({json.dumps(slot_id or '')}) formData.append('slot_id', {json.dumps(slot_id or '')});
  if ({json.dumps(voice_name)}) formData.append('voice_name', {json.dumps(voice_name)});
  fetch({json.dumps(BASE_URL + '/voice/clone')}, {{
    method: 'POST',
    credentials: 'include',
    body: formData
  }})
    .then(async response => {{
      const text = await response.text();
      done(JSON.stringify({{ok: response.ok, status: response.status, text}}));
    }})
    .catch(error => done(JSON.stringify({{ok: false, status: 0, text: String(error)}})));
}})()
"""
    raw = apple_script(script)
    parsed = json.loads(raw) if raw else {}
    if not parsed.get("ok"):
        raise RuntimeError(f"POST /voice/clone via browser failed with HTTP {parsed.get('status')}: {parsed.get('text')}")
    text = parsed.get("text", "")
    return json.loads(text) if text else {}


def list_slots(token: str, *, page: int = 1, size: int = 20, status: int = -1) -> Any:
    return request_json("GET", "/user/voice/slots", token, params={"page": page, "size": size, "status": status})


def list_slots_via_browser(*, page: int = 1, size: int = 20, status: int = -1) -> Any:
    return request_json_via_browser("GET", "/user/voice/slots", params={"page": page, "size": size, "status": status})


def list_available_voices(token: str, *, page: int = 1, size: int = 100, voice_type: str = "voice_clone") -> Any:
    params = {"page": page, "size": size}
    if voice_type:
        params["voice_type"] = voice_type
    return request_json("GET", "/voice/my/available", token, params=params)


def list_available_voices_via_browser(*, page: int = 1, size: int = 100, voice_type: str = "voice_clone") -> Any:
    params = {"page": page, "size": size}
    if voice_type:
        params["voice_type"] = voice_type
    return request_json_via_browser("GET", "/voice/my/available", params=params)


def reselect_slot(token: str, slot_id: str) -> Any:
    return request_json("POST", "/user/voice/slots/reselect", token, payload={"slot_id": slot_id})


def reselect_slot_via_browser(slot_id: str) -> Any:
    return request_json_via_browser("POST", "/user/voice/slots/reselect", payload={"slot_id": slot_id})


def flatten_voice_items(payload: Any) -> list[dict]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("list", "items", "voices", "data"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def extract_voice_id(payload: Any) -> str:
    if isinstance(payload, dict):
        for key in ("voice_id", "id"):
            value = payload.get(key)
            if value:
                return str(value)
        for key in ("data", "voice", "item", "result"):
            nested = payload.get(key)
            voice_id = extract_voice_id(nested)
            if voice_id:
                return voice_id
    if isinstance(payload, list):
        for item in payload:
            voice_id = extract_voice_id(item)
            if voice_id:
                return voice_id
    return ""


def pick_latest_clone_voice(voices_payload: Any, *, preferred_name: str = "") -> Optional[dict]:
    items = flatten_voice_items(voices_payload)
    if not items:
        return None
    preferred_name = preferred_name.strip().lower()
    if preferred_name:
        for item in items:
            name = str(item.get("voice_name") or item.get("name") or "").strip().lower()
            if name == preferred_name:
                return item
    def sort_key(item: dict) -> tuple:
        created = item.get("created_at") or item.get("create_time") or item.get("updated_at") or 0
        return (created, str(item.get("id") or item.get("voice_id") or ""))
    items.sort(key=sort_key, reverse=True)
    return items[0]


def validate_audio(audio_path: Path) -> None:
    if not audio_path.exists():
        raise RuntimeError(f"Audio sample not found: {audio_path}")
    if audio_path.suffix.lower() not in ALLOWED_SUFFIXES:
        raise RuntimeError("Voice clone sample must be .mp3, .wav, or .aac")
    if audio_path.stat().st_size > 50 * 1024 * 1024:
        raise RuntimeError("Voice clone sample must be smaller than 50MB")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect or create SenseAudio workspace clone voices with an authorized platform token.")
    parser.add_argument("--mode", choices=["slots", "available", "create", "reselect"], required=True)
    parser.add_argument("--token", default="")
    parser.add_argument("--token-env", default=DEFAULT_TOKEN_ENV)
    parser.add_argument("--browser-session", action="store_true")
    parser.add_argument("--audio-path", default="")
    parser.add_argument("--slot-id", default="")
    parser.add_argument("--voice-name", default="")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--size", type=int, default=100)
    parser.add_argument("--status", type=int, default=-1)
    args = parser.parse_args()

    token = args.token or os.getenv(args.token_env, "")
    use_browser_session = args.browser_session or not token

    if args.mode == "slots":
        result = (
            list_slots_via_browser(page=args.page, size=args.size, status=args.status)
            if use_browser_session
            else list_slots(token, page=args.page, size=args.size, status=args.status)
        )
    elif args.mode == "available":
        result = (
            list_available_voices_via_browser(page=args.page, size=args.size)
            if use_browser_session
            else list_available_voices(token, page=args.page, size=args.size)
        )
    elif args.mode == "reselect":
        if not args.slot_id:
            raise SystemExit("--slot-id is required for reselect mode.")
        result = reselect_slot_via_browser(args.slot_id) if use_browser_session else reselect_slot(token, args.slot_id)
    else:
        if not args.audio_path:
            raise SystemExit("--audio-path is required for create mode.")
        result = (
            create_clone_via_browser(
                Path(args.audio_path),
                slot_id=args.slot_id or None,
                voice_name=args.voice_name,
            )
            if use_browser_session
            else create_clone(
                token,
                Path(args.audio_path),
                slot_id=args.slot_id or None,
                voice_name=args.voice_name,
            )
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
