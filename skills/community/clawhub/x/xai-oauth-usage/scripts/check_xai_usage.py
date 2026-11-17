#!/usr/bin/env python3
"""Read xAI OAuth weekly usage without exposing or mutating credentials."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ENDPOINT = "https://cli-chat-proxy.grok.com/v1/billing?format=credits"
JST = timezone(timedelta(hours=9), name="JST")
JAPANESE_LANGUAGE_ALIASES = {"ja", "ja-jp", "jp", "japanese"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Prevent an Authorization header from following redirects."""

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        return None


class UsageError(Exception):
    def __init__(
        self,
        message: str,
        japanese_message: str,
        *,
        http_status: int | None = None,
    ) -> None:
        super().__init__(message)
        self.japanese_message = japanese_message
        self.http_status = http_status

    def localized(self, language: str) -> str:
        return self.japanese_message if language == "ja" else str(self)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read xAI OAuth weekly usage and reset time."
    )
    parser.add_argument(
        "--auth-file",
        type=Path,
        default=Path.home() / ".hermes" / "auth.json",
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def normalize_language(value: str | None) -> str:
    return "ja" if value and value.strip().lower() in JAPANESE_LANGUAGE_ALIASES else "en"


def detect_language() -> str:
    configured = os.environ.get("HERMES_LANGUAGE")
    if configured and configured.strip():
        return normalize_language(configured)

    hermes = shutil.which("hermes")
    if hermes is None:
        return "en"
    try:
        result = subprocess.run(
            [hermes, "config", "get", "display.language"],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "en"
    if result.returncode != 0:
        return "en"
    return normalize_language(result.stdout)


def read_access_token(auth_file: Path) -> str:
    try:
        store = json.loads(auth_file.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise UsageError(
            f"auth file not found: {auth_file}",
            f"認証ファイルが見つかりません: {auth_file}",
        ) from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise UsageError(
            "could not read Hermes auth store",
            "Hermesの認証情報を読み取れませんでした",
        ) from exc

    token = (
        ((store.get("providers") or {}).get("xai-oauth") or {})
        .get("tokens", {})
        .get("access_token")
    )
    if not isinstance(token, str) or not token.strip():
        raise UsageError(
            "xai-oauth access token is not configured",
            "xai-oauth access tokenが設定されていません",
        )
    return token.strip()


def parse_datetime(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def as_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def fetch_usage(token: str, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(
        ENDPOINT,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "xai-grok-cli/0.2.111",
            "x-grok-client-version": "0.2.111",
            "x-grok-client-mode": "cli",
            "x-grok-client-identifier": "hermes-xai-usage-checker",
        },
    )
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=timeout) as response:
            status = response.status
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise UsageError(
                "xAI rejected the OAuth credential; no reauthentication was attempted",
                "xAIがOAuth credentialを拒否しました。再認証は行っていません",
                http_status=exc.code,
            ) from exc
        raise UsageError(
            "xAI billing endpoint returned an error",
            "xAI billing endpointがエラーを返しました",
            http_status=exc.code,
        ) from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise UsageError(
            "could not reach xAI billing endpoint",
            "xAI billing endpointへ接続できませんでした",
        ) from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UsageError(
            "xAI billing endpoint returned an invalid payload",
            "xAI billing endpointが不正なデータを返しました",
        ) from exc

    if status != 200 or not isinstance(payload, dict):
        raise UsageError(
            "xAI billing endpoint returned an invalid response",
            "xAI billing endpointが不正なレスポンスを返しました",
            http_status=status,
        )

    config = payload.get("config")
    if not isinstance(config, dict):
        raise UsageError(
            "xAI billing response has no usage config",
            "xAI billingレスポンスに利用枠情報がありません",
            http_status=status,
        )

    period = config.get("currentPeriod")
    if not isinstance(period, dict):
        period = {}

    start = parse_datetime(period.get("start") or config.get("billingPeriodStart"))
    end = parse_datetime(period.get("end") or config.get("billingPeriodEnd"))
    used = as_number(config.get("creditUsagePercent"))
    if used is None and (start is not None or end is not None):
        used = 0.0
    remaining = max(0.0, 100.0 - used) if used is not None else None
    remaining_seconds = max(0, int((end - datetime.now(timezone.utc)).total_seconds())) if end else None

    products: list[dict[str, Any]] = []
    raw_products = config.get("productUsage")
    if isinstance(raw_products, list):
        for item in raw_products:
            if not isinstance(item, dict) or not isinstance(item.get("product"), str):
                continue
            product_percent = as_number(item.get("usagePercent"))
            products.append(
                {"product": item["product"], "usage_percent": product_percent or 0.0}
            )

    return {
        "status": "ok",
        "provider": "xai-oauth",
        "source_host": "cli-chat-proxy.grok.com",
        "period_type": period.get("type"),
        "used_percent": used,
        "remaining_percent": remaining,
        "period_start_jst": start.astimezone(JST).isoformat() if start else None,
        "period_end_jst": end.astimezone(JST).isoformat() if end else None,
        "remaining_seconds": remaining_seconds,
        "remaining_hours": round(remaining_seconds / 3600, 2) if remaining_seconds is not None else None,
        "is_unified_billing_user": config.get("isUnifiedBillingUser"),
        "product_usage": products,
    }


def human_duration(seconds: int | None, language: str) -> str:
    if seconds is None:
        return "不明" if language == "ja" else "unknown"
    hours, remainder = divmod(seconds, 3600)
    minutes = remainder // 60
    if language == "ja":
        return f"{hours}時間{minutes}分"
    return f"{hours}h {minutes}m"


def print_human(result: dict[str, Any], language: str) -> None:
    used = result.get("used_percent")
    remaining = result.get("remaining_percent")
    reset = result.get("period_end_jst")
    products = result.get("product_usage") or []
    if language == "ja":
        print("xAI OAuth 利用枠")
        if used is not None and remaining is not None:
            print(f"週間利用率: {used:.1f}%（残り {remaining:.1f}%）")
        print(f"リセット: {reset or '不明'}")
        print(f"残り時間: {human_duration(result.get('remaining_seconds'), language)}")
        if products:
            print("内訳:")
    else:
        print("xAI OAuth Usage")
        if used is not None and remaining is not None:
            print(f"Weekly usage: {used:.1f}% ({remaining:.1f}% remaining)")
        print(f"Reset: {reset or 'unknown'}")
        print(f"Time remaining: {human_duration(result.get('remaining_seconds'), language)}")
        if products:
            print("Breakdown:")
    for item in products:
        print(f"- {item['product']}: {item['usage_percent']:.1f}%")


def main() -> int:
    args = parse_args()
    language = "en" if args.as_json else detect_language()
    try:
        result = fetch_usage(read_access_token(args.auth_file), args.timeout)
    except UsageError as exc:
        result = {
            "status": "error",
            "error": str(exc),
            "http_status": exc.http_status,
        }
        if args.as_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if language == "ja":
                message = f"xAI OAuth利用枠を確認できません: {exc.localized(language)}"
            else:
                message = f"Could not check xAI OAuth usage: {exc.localized(language)}"
            print(message, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result, language)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
