from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from billing import BillingError, NoopBillingClient, SkillPayBillingClient, build_billing_client


class _Resp:
    def __init__(self, status_code: int, payload: dict | None = None, text: str = "") -> None:
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self) -> dict:
        return self._payload


class _Session:
    def __init__(self, post_resp: _Resp) -> None:
        self.post_resp = post_resp

    def post(self, url, headers, json, timeout):  # noqa: ANN001
        return self.post_resp


def test_noop_client() -> None:
    client = NoopBillingClient()
    result = client.charge("explain", "0.01", "u", "id")
    assert result.ok


def test_build_client_requires_env(monkeypatch) -> None:
    monkeypatch.delenv("SKILLPAY_APIKEY", raising=False)
    monkeypatch.setenv("SKILLPAY_BILLING_MODE", "skillpay")
    try:
        build_billing_client()
        assert False
    except BillingError as exc:
        assert "missing_skillpay_apikey" in str(exc)


def test_charge_success() -> None:
    client = SkillPayBillingClient(api_key="abc", charge_url="https://example.com/charges")
    client.session = _Session(_Resp(200, {"id": "charge_1"}))
    result = client.charge("explain", "0.01", "u", "id")
    assert result.ok
    assert result.provider_ref == "charge_1"
