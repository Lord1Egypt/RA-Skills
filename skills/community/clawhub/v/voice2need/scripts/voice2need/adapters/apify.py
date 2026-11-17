"""Bounded Apify runs with resumable starts and per-item dataset provenance.

API references: https://docs.apify.com/api/v2/actors-runs-post and
https://docs.apify.com/api/v2/dataset-items-get (checked 2026-09-15).
"""

import hashlib
import json
import math
import re
import time

from voice2need.runtime import SourceError, require_env

API = "https://api.apify.com/v2"
TERMINAL = {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}
ACTIVE = {"READY", "RUNNING", "TIMING-OUT", "ABORTING"}


def positive_int(value, name, maximum=1000000):
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise SourceError("invalid-input", f"{name} must be an integer between 1 and {maximum}")
    return value


def _run_data(response):
    value = response.data.get("data") if isinstance(response.data, dict) else None
    if not isinstance(value, dict) or not value.get("id") or value.get("status") not in TERMINAL | ACTIVE:
        raise SourceError("schema-drift", "Apify response lacks a recognized run ID/status")
    return value


def run_actor(ctx, actor_id, input_data, *, max_charge_usd=1, max_polls=30,
              poll_seconds=2, max_dataset_pages=100, max_items=10000,
              page_size=1000, on_page=None, actor_timeout_seconds=300):
    """Return (items, first_raw_ref, info); info.item_raw_refs aligns with items.

    Repeating the same request in a run resumes its cached POST; it never starts a
    replacement Actor after failure or a polling deadline. on_page receives each
    dataset page before the next request, so callers can preserve normalized data
    even if a later request fails. Poll exhaustion leaves the remote run bounded
    by its server timeout and charge cap; it is reported explicitly as partial.
    """
    if not isinstance(actor_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+(?:[~/][A-Za-z0-9_-]+)?", actor_id):
        raise SourceError("invalid-input", "Invalid Apify Actor identifier")
    if not isinstance(input_data, dict):
        raise SourceError("invalid-input", "Actor input must be an object")
    if isinstance(max_charge_usd, bool) or not isinstance(max_charge_usd, (int, float)) or not math.isfinite(max_charge_usd) or max_charge_usd <= 0:
        raise SourceError("invalid-input", "A positive finite max_charge_usd is required")
    positive_int(max_polls, "max_polls", 1000)
    positive_int(max_dataset_pages, "max_dataset_pages", 10000)
    positive_int(max_items, "max_items")
    positive_int(page_size, "page_size", 10000)
    positive_int(actor_timeout_seconds, "actor_timeout_seconds", 3600)
    if isinstance(poll_seconds, bool) or not isinstance(poll_seconds, (int, float)) or not math.isfinite(poll_seconds) or not 0 <= poll_seconds <= 60:
        raise SourceError("invalid-input", "poll_seconds must be between 0 and 60")
    actor_id = actor_id.replace("/", "~")
    options = {"maxTotalChargeUsd": max_charge_usd, "maxItems": max_items,
               "timeout": actor_timeout_seconds, "waitForFinish": 0, "restartOnError": "false"}
    digest = hashlib.sha256(json.dumps([actor_id, input_data, options], sort_keys=True).encode()).hexdigest()
    state_key = "apify-" + digest
    saved = ctx.get_checkpoint(state_key) or {}
    headers = {"Authorization": "Bearer " + require_env("APIFY_API_TOKEN")}
    if saved.get("run"):
        state, last_raw = saved["run"], saved["raw"]
    else:
        response = ctx.request("POST", f"{API}/acts/{actor_id}/runs", params=options,
                               headers=headers, json_body=input_data, cache=True)
        state, last_raw = _run_data(response), response.raw
        ctx.checkpoint(state_key, {"run": state, "raw": last_raw})
    polls = 0
    while state["status"] not in TERMINAL and polls < max_polls:
        if poll_seconds:
            time.sleep(poll_seconds)
        response = ctx.request("GET", f"{API}/actor-runs/{state['id']}", headers=headers, cache=False)
        state, last_raw = _run_data(response), response.raw
        polls += 1
        ctx.checkpoint(state_key, {"run": state, "raw": last_raw})
    info = {"run_id": state["id"], "actor_id": actor_id, "actor_status": state["status"],
            "dataset_id": state.get("defaultDatasetId"), "polls": polls,
            "max_charge_usd": max_charge_usd, "usage_total_usd": state.get("usageTotalUsd"),
            "item_raw_refs": [], "dataset_pages": 0, "dataset_exhausted": False,
            "status": "complete", "gaps": []}
    if state["status"] not in TERMINAL:
        info.update(status="partial", remote_run_may_continue=True)
        info["gaps"].append({"reason": "actor-poll-limit", "run_id": state["id"]})
        return [], last_raw, info
    if state["status"] != "SUCCEEDED":
        info["status"] = "timeout" if state["status"] == "TIMED-OUT" else "provider-failed"
        info["gaps"].append({"reason": "actor-not-succeeded", "actor_status": state["status"]})
    usage = state.get("usageTotalUsd")
    if isinstance(usage, (int, float)) and usage >= max_charge_usd:
        info["gaps"].append({"reason": "actor-charge-cap-reached"})
    dataset_id = state.get("defaultDatasetId")
    if not dataset_id:
        if state["status"] == "SUCCEEDED":
            raise SourceError("schema-drift", "Succeeded Apify run has no dataset ID")
        return [], last_raw, info
    items, first_raw = [], None
    for _ in range(max_dataset_pages):
        limit = min(page_size, max_items - len(items))
        if limit <= 0:
            break
        response = ctx.request("GET", f"{API}/datasets/{dataset_id}/items", headers=headers,
                               params={"format": "json", "clean": "false", "skipEmpty": "false",
                                       "skipHidden": "false", "offset": len(items), "limit": limit})
        page = response.data
        if not isinstance(page, list) or any(not isinstance(item, dict) for item in page) or len(page) > limit:
            raise SourceError("schema-drift", "Apify dataset page is not a bounded object array")
        first_raw = first_raw or response.raw
        refs = [dict(response.raw, locator=f"$.data[{i}]") for i in range(len(page))]
        if on_page:
            on_page(page, refs)
        items.extend(page)
        info["item_raw_refs"].extend(refs)
        info["dataset_pages"] += 1
        if len(page) < limit:
            info["dataset_exhausted"] = True
            break
    if not info["dataset_exhausted"]:
        info["gaps"].append({"reason": "dataset-cap", "returned": len(items)})
    if info["status"] == "complete":
        info["status"] = "partial" if info["gaps"] else ("complete" if items else "no-results")
    return items, first_raw or last_raw, info
