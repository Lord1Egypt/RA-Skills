#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
import time
from pathlib import Path
from typing import Any

from common import (
    DEFAULT_CONFIG_PATH,
    ensure_runtime_dirs,
    load_config,
    load_env_file,
    now_iso,
    python_bin,
    read_json,
    run_json,
    script_path,
    write_json,
    expand_path,
)


def random_sleep(min_seconds: float, max_seconds: float) -> None:
    time.sleep(random.uniform(min_seconds, max_seconds))


def sleep_after_detail_fetch(detail_count: int) -> None:
    if detail_count > 0 and detail_count % 20 == 0:
        random_sleep(40, 70)
    else:
        random_sleep(10, 17)


def state_path(config: dict[str, Any], platform: str) -> Path:
    return expand_path(config["data_dir"]) / platform / "state.json"


def raw_dir(config: dict[str, Any], platform: str) -> Path:
    path = expand_path(config["data_dir"]) / platform / "raw"
    path.mkdir(parents=True, exist_ok=True)
    return path


def note_id(item: dict[str, Any]) -> str:
    return str(item.get("note_id") or item.get("id") or item.get("answer_id") or item.get("article_id") or "").strip()


def save_item(config: dict[str, Any], platform: str, item: dict[str, Any]) -> None:
    item_id = note_id(item)
    if not item_id:
        raise RuntimeError(f"cannot save item without id: {item}")
    payload = dict(item)
    payload["synced_at"] = now_iso()
    write_json(raw_dir(config, platform) / f"{item_id}.json", payload)


def write_sync_state(config: dict[str, Any], platform: str, state: dict[str, Any]) -> None:
    state["last_sync"] = now_iso()
    write_json(state_path(config, platform), state)


def run_limits(pconfig: dict[str, Any], default: int) -> tuple[int, int]:
    legacy = int(pconfig.get("max_per_run", default) or default)
    max_new = int(pconfig.get("max_new_per_run", legacy) or legacy)
    max_scan = int(pconfig.get("max_scan_per_run", legacy) or legacy)
    return max(1, max_new), max(1, max_scan)


def sync_xhs(config: dict[str, Any]) -> dict[str, int]:
    pconfig = config["platforms"]["xhs"]
    max_new, max_scan = run_limits(pconfig, 50)
    load_env_file(config["cookiecloud_env"])
    list_script = script_path(config, "xhs_skill", "xhs_saved_notes.py")
    detail_script = script_path(config, "xhs_skill", "xhs_note_detail.py")
    py = python_bin(config, "xhs_skill")

    args = [py, str(list_script), "--max", str(max_scan), "--json"]
    if pconfig.get("no_headless"):
        args.append("--no-headless")
    listed = run_json(args, timeout=900).get("notes", [])
    if listed:
        random_sleep(18, 30)

    state = read_json(state_path(config, "xhs"), {"seen_ids": {}, "failed_ids": {}})
    created = skipped = failed = scanned = details_fetched = 0
    for card in listed:
        if created >= max_new or scanned >= max_scan:
            break
        scanned += 1
        nid = str(card.get("id") or card.get("note_id") or "").strip()
        if not nid:
            continue
        if nid in state.get("seen_ids", {}) and (raw_dir(config, "xhs") / f"{nid}.json").exists():
            skipped += 1
            continue
        cmd = [py, str(detail_script), "--note-id", nid, "--json"]
        token = card.get("xsecToken") or card.get("xsec_token")
        if token:
            cmd.extend(["--xsec-token", str(token)])
        if pconfig.get("no_headless"):
            cmd.append("--no-headless")
        details_fetched += 1
        try:
            detail = run_json(cmd, timeout=180)
            detail["list_card"] = card
            save_item(config, "xhs", detail)
            state.setdefault("seen_ids", {})[nid] = now_iso()
            created += 1
            write_sync_state(config, "xhs", state)
        except Exception as exc:
            state.setdefault("failed_ids", {})[nid] = {"at": now_iso(), "error": str(exc)[:500]}
            failed += 1
            write_sync_state(config, "xhs", state)
        if details_fetched:
            sleep_after_detail_fetch(details_fetched)
    write_sync_state(config, "xhs", state)
    return {"listed": len(listed), "scanned": scanned, "created": created, "skipped": skipped, "failed": failed}


def zhihu_item_url(item: dict[str, Any]) -> str:
    url = str(item.get("url") or "").strip()
    if url:
        return url
    item_type = str(item.get("type") or "").lower()
    iid = str(item.get("id") or "").strip()
    if item_type == "answer" and iid:
        return f"https://www.zhihu.com/api/v4/answers/{iid}"
    if item_type == "article" and iid:
        return f"https://zhuanlan.zhihu.com/p/{iid}"
    return ""


def sync_zhihu(config: dict[str, Any]) -> dict[str, int]:
    pconfig = config["platforms"]["zhihu"]
    max_new, max_scan = run_limits(pconfig, 100)
    load_env_file(config["cookiecloud_env"])
    collections_script = script_path(config, "zhihu_skill", "zhihu_collections.py")
    items_script = script_path(config, "zhihu_skill", "zhihu_collection_items.py")
    content_script = script_path(config, "zhihu_skill", "zhihu_item_content.py")
    py = python_bin(config, "zhihu_skill")

    collection_ids = [int(x) for x in pconfig.get("collection_ids", []) or []]
    if not collection_ids:
        payload = run_json([py, str(collections_script), "--limit", str(pconfig.get("collection_list_limit", 50)), "--json"], timeout=300)
        collection_ids = [int(c["id"]) for c in payload.get("collections", []) if c.get("id")]
    if collection_ids:
        random_sleep(18, 30)

    state = read_json(state_path(config, "zhihu"), {"seen_ids": {}, "failed_ids": {}})
    created = skipped = failed = listed = scanned = details_fetched = 0
    for cid in collection_ids:
        if created >= max_new or scanned >= max_scan:
            break
        collection_limit = min(int(pconfig.get("max_per_collection", 100) or 100), max_scan - scanned)
        if collection_limit <= 0:
            break
        items = run_json(
            [py, str(items_script), "--collection-id", str(cid), "--limit", str(collection_limit), "--json"],
            timeout=300,
        ).get("items", [])
        listed += len(items)
        for item in items:
            if created >= max_new or scanned >= max_scan:
                break
            scanned += 1
            iid = str(item.get("id") or "").strip()
            if not iid:
                continue
            if iid in state.get("seen_ids", {}) and (raw_dir(config, "zhihu") / f"{iid}.json").exists():
                skipped += 1
                continue
            url = zhihu_item_url(item)
            if not url:
                failed += 1
                state.setdefault("failed_ids", {})[iid] = {"at": now_iso(), "error": "missing url"}
                write_sync_state(config, "zhihu", state)
                continue
            details_fetched += 1
            try:
                detail = run_json([py, str(content_script), "--url", url, "--json"], timeout=300)
                detail["collection_id"] = cid
                detail["list_item"] = item
                save_item(config, "zhihu", detail)
                state.setdefault("seen_ids", {})[iid] = now_iso()
                created += 1
                write_sync_state(config, "zhihu", state)
            except Exception as exc:
                failed += 1
                state.setdefault("failed_ids", {})[iid] = {"at": now_iso(), "error": str(exc)[:500]}
                write_sync_state(config, "zhihu", state)
            if details_fetched:
                sleep_after_detail_fetch(details_fetched)
    write_sync_state(config, "zhihu", state)
    return {"collections": len(collection_ids), "listed": listed, "scanned": scanned, "created": created, "skipped": skipped, "failed": failed}


def main() -> int:
    parser = argparse.ArgumentParser(description="Incrementally fetch favorites through hctec-* skills")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--platform", choices=["xhs", "zhihu", "all"], default="all")
    args = parser.parse_args()

    config = load_config(args.config)
    ensure_runtime_dirs(config)
    results = {}
    if args.platform in ("xhs", "all") and config["platforms"]["xhs"].get("enabled"):
        results["xhs"] = sync_xhs(config)
    if args.platform in ("zhihu", "all") and config["platforms"]["zhihu"].get("enabled"):
        results["zhihu"] = sync_zhihu(config)
    for platform, result in results.items():
        print(f"{platform}: " + ", ".join(f"{k}={v}" for k, v in result.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
