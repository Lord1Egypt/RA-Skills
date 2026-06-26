from __future__ import annotations

import os
import time
from dataclasses import asdict, dataclass
from typing import Dict, Optional

import requests


class BillingError(RuntimeError):
    pass


@dataclass
class BillingResult:
    ok: bool
    code: str
    message: str
    provider_ref: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


class BillingClient:
    def charge(self, call_name: str, amount_usdt: str, user_ref: str, idempotency_key: str) -> BillingResult:
        raise NotImplementedError


class NoopBillingClient(BillingClient):
    def charge(self, call_name: str, amount_usdt: str, user_ref: str, idempotency_key: str) -> BillingResult:
        return BillingResult(ok=True, code="noop", message="noop billing accepted", provider_ref="noop")


class SkillPayBillingClient(BillingClient):
    def __init__(self, api_key: str, base_url: Optional[str] = None, charge_url: Optional[str] = None) -> None:
        self.api_key = api_key
        self.base_url = (base_url or os.getenv("SKILLPAY_BASE_URL") or "https://skillpay.me").rstrip("/")
        self.charge_url = charge_url or os.getenv("SKILLPAY_CHARGE_URL")
        if not self.charge_url:
            charge_path = os.getenv("SKILLPAY_CHARGE_PATH", "/charges")
            self.charge_url = f"{self.base_url}{charge_path}"
        self.session = requests.Session()

    def charge(self, call_name: str, amount_usdt: str, user_ref: str, idempotency_key: str) -> BillingResult:
        payload = {
            "call_name": call_name,
            "amount": amount_usdt,
            "currency": "USDT",
            "user_ref": user_ref,
            "idempotency_key": idempotency_key,
            "timestamp": int(time.time()),
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Idempotency-Key": idempotency_key,
        }

        delay = 0.8
        for attempt in range(3):
            try:
                resp = self.session.post(self.charge_url, json=payload, headers=headers, timeout=12)
                if resp.status_code >= 500:
                    raise BillingError(f"skillpay_server_{resp.status_code}")
                if resp.status_code >= 400:
                    return BillingResult(ok=False, code=f"http_{resp.status_code}", message=resp.text[:200])

                data = {}
                try:
                    data = resp.json()
                except ValueError:
                    pass
                provider_ref = None
                for key in ("id", "charge_id", "reference", "tx_id"):
                    value = data.get(key) if isinstance(data, dict) else None
                    if isinstance(value, str) and value:
                        provider_ref = value
                        break
                return BillingResult(ok=True, code="charged", message="charge accepted", provider_ref=provider_ref)
            except (requests.Timeout, requests.ConnectionError, BillingError) as exc:
                if attempt == 2:
                    return BillingResult(ok=False, code="network_error", message=str(exc))
                time.sleep(delay)
                delay *= 2

        return BillingResult(ok=False, code="unknown", message="billing failed")


def build_billing_client() -> BillingClient:
    mode = os.getenv("SKILLPAY_BILLING_MODE", "skillpay").strip().lower()
    if mode == "noop":
        return NoopBillingClient()

    api_key = os.getenv("SKILLPAY_APIKEY", "").strip()
    if not api_key:
        raise BillingError("missing_skillpay_apikey")
    return SkillPayBillingClient(api_key=api_key)
