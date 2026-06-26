#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TopMediai TTS API client functions (requests-based).
Reads API key and base URL from environment/.env:
- TOPMEDIAI_API_KEY (required)
- TOPMEDIAI_BASE_URL (default: https://api.topmediai.com)
"""
import os
from typing import Dict, Any, Optional, NoReturn
import requests
from dotenv import load_dotenv
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parents[1]
_ENV_PATH = _SKILL_ROOT / ".env"
if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH.as_posix())

BASE_URL = os.environ.get("TOPMEDIAI_BASE_URL", "https://api.topmediai.com")
DEFAULT_KEY = os.environ.get("TOPMEDIAI_API_KEY")
DEBUG_MODE = str(os.environ.get("TOPMEDIAI_DEBUG", "0")).lower() in {"1", "true", "yes", "on"}


def _mask_key(value: Optional[str]) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}***{value[-4:]}"


def _debug_request(method: str, url: str, headers: Dict[str, str], payload: Optional[Dict[str, Any]] = None):
    if not DEBUG_MODE:
        return
    safe_headers = dict(headers)
    if "x-api-key" in safe_headers:
        safe_headers["x-api-key"] = _mask_key(str(safe_headers.get("x-api-key")))
    info: Dict[str, Any] = {"debug": {"method": method, "url": url, "headers": safe_headers}}
    if payload is not None:
        info["debug"]["payload"] = payload
    print(info)


def _raise_as_runtime_error(e: Exception, method: str, url: str) -> NoReturn:
    detail = str(e)
    if isinstance(e, requests.HTTPError) and getattr(e, "response", None) is not None:
        resp = e.response
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        detail = f"HTTP {resp.status_code}: {body}"
    msg = f"TopMediai request failed: {method} {url}: {type(e).__name__}: {detail}"
    raise RuntimeError(msg)


def _headers(api_key: Optional[str] = None) -> Dict[str, str]:
    key = api_key or DEFAULT_KEY
    if not key:
        raise RuntimeError(
            "TOPMEDIAI_API_KEY not configured. Edit: {} and set TOPMEDIAI_API_KEY=YOUR_KEY.".format(_ENV_PATH)
        )
    return {"x-api-key": key, "Content-Type": "application/json"}


def get_api_key_info(api_key: Optional[str] = None) -> Dict[str, Any]:
    url = f"{BASE_URL}/v1/get_api_key_info"
    headers = _headers(api_key)
    _debug_request("GET", url, headers=headers)
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        _raise_as_runtime_error(e, "GET", url)


def get_official_voices(api_key: Optional[str] = None) -> Dict[str, Any]:
    url = f"{BASE_URL}/v1/voices_list"
    headers = _headers(api_key)
    _debug_request("GET", url, headers=headers)
    try:
        r = requests.get(url, headers=headers, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        _raise_as_runtime_error(e, "GET", url)


def get_clone_voices(api_key: Optional[str] = None) -> Dict[str, Any]:
    url = f"{BASE_URL}/v1/clone_voices_list"
    headers = _headers(api_key)
    _debug_request("GET", url, headers=headers)
    try:
        r = requests.get(url, headers=headers, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        _raise_as_runtime_error(e, "GET", url)


def get_all_voices(api_key: Optional[str] = None) -> Dict[str, Any]:
    official = get_official_voices(api_key=api_key)
    cloned = get_clone_voices(api_key=api_key)
    return {
        "official_voices": official.get("data", official),
        "clone_voices": cloned.get("data", cloned),
    }


def text_to_speech(text: str, speaker: str, emotion: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
    url = f"{BASE_URL}/v1/text2speech"
    headers = _headers(api_key)
    payload: Dict[str, Any] = {
        "text": text,
        "speaker": speaker,
    }
    if emotion:
        payload["emotion"] = emotion
    _debug_request("POST", url, headers=headers, payload=payload)
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=120)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        _raise_as_runtime_error(e, "POST", url)
