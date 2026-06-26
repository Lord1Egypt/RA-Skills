"""
skill.py
--------
OpenClaw skill: Superwise Drift Detection

Generic drift detection skill for any tabular model. Works with any model that
exposes an inference endpoint returning JSON records, and any training data
that can be provided as a CSV.

How this skill fits into OpenClaw:
  - A backend server (e.g., Render Flask app) handles ingestion and exposes /run-check
  - OpenClaw calls GET /run-check on a schedule or via Telegram command
  - The skill queries Superwise for drift results and fires a Telegram alert if needed

For the Prophet/ETF reference implementation see examples/etf_prophet/.

Credentials required in .env:
    SUPERWISE_CLIENT_ID
    SUPERWISE_SECRET_TOKEN
    SUPERWISE_TRAINING_DATASET_ID    (from setup_dataset.py)
    SUPERWISE_TRAINING_DATASET_NAME
    SUPERWISE_INFERENCE_DATASET_ID
    SUPERWISE_INFERENCE_DATASET_NAME
    INFERENCE_ENDPOINT_URL           (your model's prediction endpoint)
    TELEGRAM_BOT_TOKEN
    TELEGRAM_CHAT_ID
"""

import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

from superwise_ingest import SuperwiseIngester

load_dotenv()

# ── OpenClaw skill metadata ───────────────────────────────────────────────────

SKILL_META = {
    "name": "superwise_drift_check",
    "description": (
        "Generic tabular model drift detection using Superwise. "
        "Ingests inference data, compares against training baseline via Superwise, "
        "and sends a Telegram alert when drift is detected."
    ),
    "version": "1.0.5",
    "trigger": {
        "telegram_command": "/drift_check",
        "schedule": "0 6 * * *",   # 06:00 UTC daily — adjust to your inference cadence
    },
    "webhook_url": "${RENDER_APP_URL}/run-check",
    "method": "GET",
    "mcp_servers": [
        "https://docs.superwise.ai/mcp",           # API + guides
        "https://mcp.sdk.docs.superwise.ai/mcp",   # Python SDK reference
    ],
}

# ── Drift thresholds (mirrors Superwise severity conventions) ─────────────────
# These are informational — the authoritative drift calculation lives in Superwise.
# Adjust to match whatever thresholds you configure in your Superwise policy.
DRIFT_MODERATE = 0.10
DRIFT_HIGH = 0.20


# ── Inference data fetching ───────────────────────────────────────────────────

def _fetch_inference_records() -> list[dict]:
    """
    Fetch new inference records from the model's prediction endpoint.

    The endpoint should return JSON: {"records": [{col: val, ...}, ...]}
    Adapt the response parsing below if your endpoint uses a different shape.
    """
    url = os.getenv("INFERENCE_ENDPOINT_URL")
    if not url:
        raise RuntimeError("INFERENCE_ENDPOINT_URL is not set in .env")

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        records = data.get("records", [])
        print(f"[skill] Fetched {len(records)} inference records from {url}")
        return records
    except requests.RequestException as exc:
        raise RuntimeError(f"[skill] Failed to fetch inference records: {exc}") from exc


# ── Inference ingestion ───────────────────────────────────────────────────────

def _ingest_inference_records(records: list[dict]) -> dict:
    """Push new inference records into the Superwise inference dataset."""
    import time, uuid

    client_id = os.getenv("SUPERWISE_CLIENT_ID")
    client_secret = os.getenv("SUPERWISE_SECRET_TOKEN")
    dataset_id = os.getenv("SUPERWISE_INFERENCE_DATASET_ID")
    dataset_name = os.getenv("SUPERWISE_INFERENCE_DATASET_NAME")

    if not all([client_id, client_secret, dataset_id, dataset_name]):
        raise RuntimeError(
            "Missing one or more Superwise env vars: "
            "SUPERWISE_CLIENT_ID, SUPERWISE_SECRET_TOKEN, "
            "SUPERWISE_INFERENCE_DATASET_ID, SUPERWISE_INFERENCE_DATASET_NAME"
        )

    ingester = SuperwiseIngester(client_id=client_id, client_secret=client_secret)

    posted = 0
    for record in records:
        record["row_id"] = str(uuid.uuid4())
        if ingester._post_record(dataset_id, record):
            posted += 1
        time.sleep(0.05)

    print(f"[skill] Ingested {posted}/{len(records)} inference records")
    return {"ingested": posted, "total": len(records)}


# ── Drift check via Superwise ─────────────────────────────────────────────────

_POLICIES_BASE = "https://api.superwise.ai/v1/policies"
_POLL_INTERVAL = 15   # seconds between status polls
_POLL_MAX = 12        # max polls before giving up (~3 minutes)


def _policy_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _parse_policy_results(policy: dict) -> list[dict]:
    """
    Extract per-feature drift scores from a Superwise policy response.

    The exact field name for per-feature scores is not confirmed from docs alone —
    Superwise's schema panels are JS-rendered. We try the most likely candidates
    in order. On first run with real credentials, check superwise_policy_debug.json
    to see the raw response and confirm which field is correct, then update this
    function if needed.

    Known confirmed fields:
        policy["status"]           — top-level: "healthy" | "unhealthy" | "pending" | "error"
        policy["last_evaluation"]  — timestamp of last run

    Candidate per-feature fields (order of likelihood):
        policy["groups"]       — most common pattern in monitoring APIs
        policy["results"]
        policy["evaluations"]
        policy["metrics"]
    """
    import json
    import logging

    # Always dump the raw response at DEBUG level for schema discovery
    logging.debug(f"[skill] Raw policy response:\n{json.dumps(policy, indent=2, default=str)}")

    status = policy.get("status", "unknown")
    results = []

    # Try known candidate field names for per-feature breakdown
    for field in ("groups", "results", "evaluations", "metrics", "dimensions"):
        groups = policy.get(field)
        if groups and isinstance(groups, list) and len(groups) > 0:
            print(f"[skill] Per-feature scores found in policy['{field}']")
            for g in groups:
                feature = (
                    g.get("name") or g.get("feature") or
                    g.get("dimension") or g.get("column") or "unknown"
                )
                score = (
                    g.get("drift_score") or g.get("score") or
                    g.get("value") or g.get("distance") or
                    g.get("distance_score") or 0.0
                )
                group_status = g.get("status", status)
                results.append({
                    "feature": str(feature),
                    "drift_score": float(score),
                    "status": group_status,
                })
            return results

    # Fallback: no per-feature breakdown — report top-level status
    # status_reason may contain the actual score when present
    score_val = None
    status_reason = policy.get("status_reason")
    if isinstance(status_reason, dict):
        score_val = (
            status_reason.get("score") or status_reason.get("distance") or
            status_reason.get("drift_score") or status_reason.get("value")
        )
    if score_val is None:
        score_val = 1.0 if status == "unhealthy" else 0.0

    print(f"[skill] Policy status={status} (distribution_compare returns top-level status only)")
    results.append({
        "feature": "overall",
        "drift_score": float(score_val),
        "status": status,
    })
    return results


def _collect_policy_ids() -> list[tuple[str, str]]:
    """
    Collect all policy IDs from env vars.
    Returns list of (label, policy_id) tuples.

    Reads:
      SUPERWISE_DRIFT_POLICY_ID        — primary policy (required)
      SUPERWISE_DRIFT_POLICY_ID_*      — additional per-column policies (optional)
                                         e.g. SUPERWISE_DRIFT_POLICY_ID_hour_bucket=...
    """
    policies = []
    primary = os.getenv("SUPERWISE_DRIFT_POLICY_ID")
    if primary:
        policies.append(("primary", primary))

    for key, val in sorted(os.environ.items()):
        if key.startswith("SUPERWISE_DRIFT_POLICY_ID_") and val:
            label = key[len("SUPERWISE_DRIFT_POLICY_ID_"):].lower()
            policies.append((label, val))

    return policies


def _check_drift() -> list[dict]:
    """
    Trigger all configured Superwise drift policy evaluations and return results.

    Reads SUPERWISE_DRIFT_POLICY_ID (primary) plus any
    SUPERWISE_DRIFT_POLICY_ID_<column> env vars set by setup_drift_policy.py.
    Triggers and polls each policy, returning a combined result list.

    Returns:
        List of dicts: [{"feature": str, "drift_score": float, "status": str}, ...]
        Returns [] if no policy IDs are configured.
    """
    import json
    import time

    policies = _collect_policy_ids()
    if not policies:
        print(
            "[skill] No SUPERWISE_DRIFT_POLICY_ID vars set. "
            "Run setup_drift_policy.py first, then add the IDs to .env."
        )
        return []

    client_id = os.getenv("SUPERWISE_CLIENT_ID")
    client_secret = os.getenv("SUPERWISE_SECRET_TOKEN")
    if not client_id or not client_secret:
        print("[skill] SUPERWISE_CLIENT_ID or SUPERWISE_SECRET_TOKEN not set.")
        return []

    from superwise_api.superwise_client import SuperwiseClient
    sw = SuperwiseClient(client_id=client_id, client_secret=client_secret)
    token = sw.configuration.access_token
    headers = _policy_headers(token)
    auto_trigger = os.getenv("SUPERWISE_AUTO_TRIGGER", "true").lower() == "true"

    print(f"[skill] Checking {len(policies)} policy/policies: {[label for label, _ in policies]}")

    all_results = []
    for label, policy_id in policies:
        print(f"[skill] ── Policy: {label} ({policy_id}) ──")

        if auto_trigger:
            try:
                resp = requests.post(
                    f"{_POLICIES_BASE}/{policy_id}/trigger", headers=headers, timeout=15
                )
                if resp.status_code in (200, 202, 204):
                    print(f"[skill] Triggered successfully.")
                else:
                    print(f"[skill] Trigger returned HTTP {resp.status_code}: {resp.text}")
            except requests.RequestException as exc:
                print(f"[skill] WARNING: Could not trigger policy: {exc}")

        time.sleep(5)
        policy: dict = {}
        for attempt in range(1, _POLL_MAX + 1):
            try:
                resp = requests.get(
                    f"{_POLICIES_BASE}/{policy_id}", headers=headers, timeout=15
                )
                resp.raise_for_status()
                policy = resp.json()
            except requests.RequestException as exc:
                print(f"[skill] Poll {attempt}/{_POLL_MAX} failed: {exc}")
                time.sleep(_POLL_INTERVAL)
                continue

            status = policy.get("status", "unknown")
            is_running = policy.get("is_running", False)
            is_triggered = policy.get("is_triggered", False)
            print(f"[skill] Poll {attempt}/{_POLL_MAX} — status={status} running={is_running} triggered={is_triggered}")

            if not is_running and not is_triggered and status != "pending":
                break
            time.sleep(_POLL_INTERVAL)
        else:
            print(f"[skill] Policy still running after {_POLL_MAX} polls — using last known state.")

        if not policy:
            print(f"[skill] No data retrieved for policy {label}.")
            continue

        results = _parse_policy_results(policy)
        # Tag each result with the column label if it came back as "overall"
        for r in results:
            if r["feature"] == "overall" and label != "primary":
                r["feature"] = label
        all_results.extend(results)

    # Save last policy response for debugging
    debug_path = "superwise_policy_debug.json"
    try:
        with open(debug_path, "w") as f:
            json.dump(policy, f, indent=2, default=str)
        print(f"[skill] Raw policy response saved to {debug_path}")
    except Exception:
        pass

    return all_results


# ── Telegram delivery ─────────────────────────────────────────────────────────

def _send_telegram(message: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[skill] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set — skipping alert.")
        return False

    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"},
            timeout=10,
        )
        resp.raise_for_status()
        return True
    except requests.RequestException as exc:
        print(f"[skill] Telegram send failed: {exc}")
        return False


# ── Message formatting ────────────────────────────────────────────────────────

def _format_drift_message(drift_results: list[dict], model_name: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    high = [r for r in drift_results if r.get("drift_score", 0) > DRIFT_HIGH]
    moderate = [r for r in drift_results if DRIFT_MODERATE < r.get("drift_score", 0) <= DRIFT_HIGH]

    if high:
        lines = [
            f"⚠️ <b>Drift Detected — {model_name}</b>",
            "",
            "Features with high drift from training baseline:",
            "",
        ]
        for r in high:
            lines.append(f"• <b>{r['feature']}</b> — score: {r['drift_score']:.4f} (High)")
        if moderate:
            lines.append("")
            lines.append("<i>Also worth monitoring (moderate drift):</i>")
            for r in moderate:
                lines.append(f"  • {r['feature']} — score: {r['drift_score']:.4f}")
        lines += ["", "Model predictions may no longer be reliable.", f"\nLast checked: {now}"]
    elif drift_results:
        lines = [
            f"✅ <b>Drift Check — {model_name}</b> — No significant drift detected.",
            "",
            "Feature drift scores (all below alert threshold):",
        ]
        for r in drift_results:
            lines.append(f"  <code>{r['feature']}</code>  {r['drift_score']:.4f}")
        lines.append(f"\nLast checked: {now}")
    else:
        lines = [
            f"ℹ️ <b>Drift Check — {model_name}</b>",
            "",
            "No drift results available yet.",
            "Ensure your Superwise drift policy is configured (see SKILL.md).",
            f"\nLast checked: {now}",
        ]

    return "\n".join(lines)


# ── Public entrypoint ─────────────────────────────────────────────────────────

def run(inference_records: list[dict] | None = None) -> dict:
    """
    OpenClaw skill entrypoint. Also callable standalone via `python skill.py`.

    Flow:
      1. Fetch inference records (from endpoint or passed in directly)
      2. Ingest records into the Superwise inference dataset
      3. Query Superwise for drift results
      4. Send Telegram alert

    Args:
        inference_records: Pre-fetched records to ingest. If None, fetches from
                           INFERENCE_ENDPOINT_URL.

    Returns:
        {
            "sent":         bool,
            "alert_fired":  bool,
            "high_drift_features": list[str],
            "ingest_result": dict,
        }
    """
    model_name = os.getenv("MODEL_NAME", "tabular_model")

    if inference_records is None:
        inference_records = _fetch_inference_records()

    ingest_result = _ingest_inference_records(inference_records)

    drift_results = _check_drift()

    high_drift = [r for r in drift_results if r.get("drift_score", 0) > DRIFT_HIGH]
    message = _format_drift_message(drift_results, model_name)
    sent = _send_telegram(message)

    print(f"[skill] Message preview:\n{'─' * 40}\n{message}\n{'─' * 40}")

    return {
        "sent": sent,
        "alert_fired": len(high_drift) > 0,
        "high_drift_features": [r["feature"] for r in high_drift],
        "ingest_result": ingest_result,
    }


if __name__ == "__main__":
    result = run()
    print(f"\n[skill] Done: {result}")
