import argparse
import json
import os
import urllib.error
import urllib.request


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing environment variable: {name}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", type=int, required=True)
    parser.add_argument("--to-email", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--to-name", default="")
    parser.add_argument("--reply-to", default="")
    args = parser.parse_args()

    base_url = _require_env("UNIPROFIT_API_BASE_URL").rstrip("/")
    api_key = _require_env("UNIPROFIT_MAIL_SEND_KEY")

    body = json.dumps(
        {
            "account_id": args.account_id,
            "to_email": args.to_email,
            "to_name": args.to_name or None,
            "subject": args.subject,
            "body": args.body,
            "reply_to": args.reply_to or None,
        },
        ensure_ascii=False,
    ).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url}/openclaw/mail/send",
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-UniProfit-Key": api_key,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(exc.read().decode("utf-8", errors="ignore"))
        return exc.code

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
