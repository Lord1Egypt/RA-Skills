#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
from typing import Tuple


DEFAULT_PLATFORM_TOKEN_ENV = "SENSEAUDIO_PLATFORM_TOKEN"
DEFAULT_WORKSPACE_URL = "https://senseaudio.cn/workspace/clone-sound"


def parse_zustand_payload(raw: str, key: str = "") -> str:
    if not raw:
        return ""
    normalized_key = key.lower()
    if "token" in normalized_key and len(raw) > 20 and raw[0] not in "{[":
        return raw
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return ""
    if isinstance(payload, dict):
        state = payload.get("state")
        if isinstance(state, dict):
            token = state.get("token")
            if token:
                return str(token)
        token = payload.get("token")
        if token:
            return str(token)
        data = payload.get("data")
        if isinstance(data, dict):
            token = data.get("token")
            if token:
                return str(token)
    return ""


def apple_script(js: str) -> str:
    script = f'''
tell application "Google Chrome"
    if (count of windows) is 0 then
        make new window
    end if
    set matchedTab to missing value
    repeat with w in windows
        repeat with t in tabs of w
            set tabUrl to URL of t
            if tabUrl contains "senseaudio.cn" then
                set matchedTab to t
                exit repeat
            end if
        end repeat
        if matchedTab is not missing value then exit repeat
    end repeat
    if matchedTab is missing value then
        tell front window
            set matchedTab to make new tab with properties {{URL:"{DEFAULT_WORKSPACE_URL}"}}
        end tell
        delay 3
    end if
    return execute matchedTab javascript {json.dumps(js)}
end tell
'''
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "AppleScript failed"
        raise RuntimeError(message)
    return result.stdout.strip()


def resolve_from_chrome() -> Tuple[str, str]:
    script = """
(() => {
  const collect = storage => {
    const items = [];
    for (let i = 0; i < storage.length; i += 1) {
      const key = storage.key(i);
      items.push({ key, raw: storage.getItem(key) || '', storage: storage === window.localStorage ? 'localStorage' : 'sessionStorage' });
    }
    return items;
  };
  return JSON.stringify({
    href: window.location.href,
    localStorage: collect(window.localStorage),
    sessionStorage: collect(window.sessionStorage),
  });
})()
"""
    raw = apple_script(script)
    if not raw:
        return "", ""
    payload = json.loads(raw)
    for storage_name in ("localStorage", "sessionStorage"):
        for item in payload.get(storage_name, []):
            if not isinstance(item, dict):
                continue
            key = str(item.get("key", ""))
            raw_value = str(item.get("raw", ""))
            token = parse_zustand_payload(raw_value, key)
            if token:
                return token, f"{storage_name}:{key}"
    return "", ""


def resolve_platform_token(
    explicit_token: str = "",
    *,
    token_env: str = DEFAULT_PLATFORM_TOKEN_ENV,
    allow_chrome: bool = True,
) -> Tuple[str, str]:
    token = explicit_token.strip()
    if token:
        return token, "explicit"
    token = os.getenv(token_env, "").strip()
    if token:
        return token, f"env:{token_env}"
    if allow_chrome:
        try:
            token, key = resolve_from_chrome()
        except Exception:
            token, key = "", ""
        if token:
            return token, f"chrome_local_storage:{key or 'user'}"
    return "", ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve a SenseAudio workspace platform token from env or Chrome.")
    parser.add_argument("--token", default="")
    parser.add_argument("--token-env", default=DEFAULT_PLATFORM_TOKEN_ENV)
    parser.add_argument("--no-chrome", action="store_true")
    args = parser.parse_args()

    token, source = resolve_platform_token(
        args.token,
        token_env=args.token_env,
        allow_chrome=not args.no_chrome,
    )
    result = {
        "resolved": bool(token),
        "source": source,
        "token": token,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
