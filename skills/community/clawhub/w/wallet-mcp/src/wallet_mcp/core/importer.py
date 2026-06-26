"""
Wallet importer: load wallets from a JSON or CSV file into local storage.

Supports:
  - format='json'  → JSON array exported by exporter.py (or compatible schema)
  - format='csv'   → CSV matching storage schema
  - format='auto'  → detect from file extension
  - label override → replace each wallet's label with a new one
  - tags append    → add extra tags to all imported wallets
  - duplicate skip → wallets already in storage are skipped, not duplicated
"""
import csv
import json
import os
from typing import Optional

from .utils import now_iso, setup_logging

_log = setup_logging()

_REQUIRED = {"address", "private_key", "chain"}


def import_wallets(
    file_path: str,
    fmt: str = "auto",
    label: Optional[str] = None,
    tags: str = "",
) -> dict:
    """
    Import wallets from a JSON or CSV file into local storage.

    Args:
        file_path: path to the source file
        fmt:       'json', 'csv', or 'auto' (detect from file extension)
        label:     override label for all imported wallets;
                   uses the file's own label field when None
        tags:      pipe-separated tags to append to each imported wallet

    Returns:
        {file, format, total_in_file, imported, skipped_duplicates, failed}
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    fmt = _resolve_fmt(fmt, file_path)

    if fmt == "json":
        raw = _read_json(file_path)
    else:
        raw = _read_csv(file_path)

    from .storage import load_wallets, save_wallets_batch
    existing = {w["address"] for w in load_wallets()}

    now = now_iso()
    to_save: list[dict] = []
    failed  = 0
    skipped = 0

    missing_key_count = 0
    for row in raw:
        missing = _REQUIRED - set(row.keys())
        if missing:
            _log.warning(f"Skipping row — missing fields {missing}: {row.get('address','?')}")
            if "private_key" in missing:
                missing_key_count += 1
            failed += 1
            continue

        addr = row["address"].strip()
        if not addr:
            failed += 1
            continue

        if addr in existing:
            skipped += 1
            continue

        # Build merged tags
        file_tags = row.get("tags", "")
        merged_tags = "|".join(t for t in [file_tags, tags] if t).strip("|")

        to_save.append({
            "address":     addr,
            "private_key": row.get("private_key", ""),
            "chain":       row.get("chain", "").lower(),
            "label":       label if label is not None else row.get("label", "imported"),
            "tags":        merged_tags,
            "created_at":  row.get("created_at", now),
        })
        existing.add(addr)

    if to_save:
        save_wallets_batch(to_save)

    _log.info(
        f"Import {file_path}: total={len(raw)} imported={len(to_save)} "
        f"skipped={skipped} failed={failed}"
    )

    result: dict = {
        "file":               file_path,
        "format":             fmt,
        "total_in_file":      len(raw),
        "imported":           len(to_save),
        "skipped_duplicates": skipped,
        "failed":             failed,
    }

    if missing_key_count > 0:
        result["hint"] = (
            f"{missing_key_count} row(s) failed because 'private_key' is missing. "
            "Re-export with --include-keys to import wallets with private keys."
        )

    return result


# ── helpers ────────────────────────────────────────────────────────────────

def _resolve_fmt(fmt: str, path: str) -> str:
    if fmt == "auto":
        ext = os.path.splitext(path)[1].lower()
        if ext == ".json":
            return "json"
        if ext == ".csv":
            return "csv"
        raise ValueError(f"Cannot detect format from extension '{ext}'. Pass fmt='json' or fmt='csv'.")
    fmt = fmt.lower()
    if fmt not in ("json", "csv"):
        raise ValueError(f"Unsupported format '{fmt}'. Choose 'json' or 'csv'.")
    return fmt


def _read_json(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("JSON file must contain a top-level array of wallet objects.")
    return data


def _read_csv(path: str) -> list[dict]:
    with open(path, "r", newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f) if row]
