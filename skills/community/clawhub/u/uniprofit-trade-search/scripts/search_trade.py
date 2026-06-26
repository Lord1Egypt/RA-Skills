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
    parser.add_argument("--source", choices=["importers", "exhibition", "requirements"], required=True)
    parser.add_argument("--filters", default="{}", help="JSON object string")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=20)
    args = parser.parse_args()

    try:
        filters = json.loads(args.filters)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON for --filters: {exc}") from exc
    if not isinstance(filters, dict):
        raise SystemExit("--filters must be a JSON object")

    base_url = _require_env("UNIPROFIT_API_BASE_URL").rstrip("/")
    api_key = _require_env("UNIPROFIT_TRADE_SEARCH_KEY")

    body = json.dumps(
        {
            "source": args.source,
            "filters": filters,
            "page": args.page,
            "page_size": args.page_size,
        },
        ensure_ascii=False,
    ).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url}/openclaw/search/query",
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
