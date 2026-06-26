"""档位鉴权：免费额度 + 付费激活码"""
from __future__ import annotations
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path


USAGE_FILE = Path.home() / ".openclaw" / "resume-rocket-usage.json"


def _load_usage() -> dict:
    if USAGE_FILE.exists():
        try:
            return json.loads(USAGE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_usage(u: dict) -> None:
    USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    USAGE_FILE.write_text(json.dumps(u, ensure_ascii=False, indent=2), encoding="utf-8")


def _verify_license(license_key: str) -> str:
    """
    本地离线校验（MVP 用）：
    激活码格式 = tier-YYYYMMDD-hash
    tier: S(single) / M(monthly) / P(pro)
    YYYYMMDD: 到期日
    hash: HMAC(secret, tier+date)[:8]
    正式上线后改为服务端校验。
    """
    secret = os.getenv("RR_LICENSE_SECRET", "openclaw-resume-rocket-2026")
    if not license_key or license_key.count("-") != 2:
        return "free"
    tier_code, expire, h = license_key.split("-")
    if datetime.now().strftime("%Y%m%d") > expire:
        return "free"
    want = hashlib.sha256(f"{secret}|{tier_code}|{expire}".encode()).hexdigest()[:8]
    if want != h:
        return "free"
    return {"S": "single", "M": "monthly", "P": "pro"}.get(tier_code, "free")


def check_tier(requested: str) -> str:
    key = os.getenv("RR_LICENSE_KEY", "")
    actual = _verify_license(key) if key else "free"

    if requested == "pro" and actual != "pro":
        return actual
    if requested == "monthly" and actual not in ("monthly", "pro"):
        return actual
    if requested == "single" and actual not in ("single", "monthly", "pro"):
        return actual

    if requested == "free":
        usage = _load_usage()
        today = datetime.now().strftime("%Y-%m-%d")
        used = usage.get(today, 0)
        if used >= 1 and actual == "free":
            print(f"[Resume Rocket] 今日免费额度已用完（{used}/1）。升级 ¥29 单次 解锁无限。")
            print("[Resume Rocket] 购买链接：https://clawhub.com/skill/resume-rocket")
            return "free-exceeded"
        usage[today] = used + 1
        _save_usage(usage)

    return requested if actual == "free" else actual
