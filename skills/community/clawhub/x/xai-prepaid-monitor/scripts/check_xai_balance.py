#!/usr/bin/env python3
import json
import os
import sys
import urllib.error
import urllib.request


def cents_to_usd_str(cents: int) -> str:
    return f"${cents / 100:.2f}"


def main() -> int:
    team_id = os.getenv("XAI_TEAM_ID")
    management_key = os.getenv("XAI_MANAGEMENT_KEY")
    warn_below_cents = int(
        os.getenv("XAI_BALANCE_WARN_BELOW_CENTS", "300")
    )
    critical_below_cents = int(
        os.getenv("XAI_BALANCE_CRITICAL_BELOW_CENTS", "200")
    )

    if not team_id:
        print(json.dumps({"ok": False, "error": "XAI_TEAM_ID not set"}))
        return 1
    if not management_key:
        print(json.dumps({"ok": False, "error": "XAI_MANAGEMENT_KEY not set"}))
        return 1

    url = (
        "https://management-api.x.ai/v1/billing/teams/"
        f"{team_id}/postpaid/invoice/preview"
    )
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {management_key}",
            "Accept": "application/json",
            "User-Agent": "openclaw-xai-balance-check/1.0",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        print(
            json.dumps(
                {"ok": False, "status": e.code, "error": body[:1000]}
            )
        )
        return 2
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 2

    core = data.get("coreInvoice") or {}
    total_cents = abs(
        int((core.get("prepaidCredits") or {}).get("val", "0"))
    )
    used_cents = abs(
        int((core.get("prepaidCreditsUsed") or {}).get("val", "0"))
    )
    remaining_cents = max(total_cents - used_cents, 0)

    status = "ok"
    if remaining_cents < critical_below_cents:
        status = "critical"
    elif remaining_cents < warn_below_cents:
        status = "warn"

    print(
        json.dumps(
            {
                "ok": True,
                "status": status,
                "total_cents": total_cents,
                "used_cents": used_cents,
                "remaining_cents": remaining_cents,
                "total": cents_to_usd_str(total_cents),
                "used": cents_to_usd_str(used_cents),
                "remaining": cents_to_usd_str(remaining_cents),
                "warn_below": cents_to_usd_str(warn_below_cents),
                "critical_below": cents_to_usd_str(critical_below_cents),
                "billing_cycle": data.get("billingCycle"),
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
