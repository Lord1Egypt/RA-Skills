import argparse
import json
import os
import sys
import urllib.error
import urllib.request


EXPECTED_SKILL = "mail_send"
KEY_ENV = "UNIPROFIT_MAIL_SEND_KEY"


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing environment variable: {name}")
    return value


def main() -> int:
    argparse.ArgumentParser().parse_args()

    base_url = _require_env("UNIPROFIT_API_BASE_URL").rstrip("/")
    api_key = _require_env(KEY_ENV)

    req = urllib.request.Request(
        f"{base_url}/openclaw/credential/me",
        headers={"X-UniProfit-Key": api_key},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        print(body)
        return exc.code

    data = payload.get("data") or {}
    print(json.dumps(data, ensure_ascii=False, indent=2))
    if data.get("skill_code") != EXPECTED_SKILL:
        print(f"Credential skill mismatch: expected {EXPECTED_SKILL}, got {data.get('skill_code')}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
