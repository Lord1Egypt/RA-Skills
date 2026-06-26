"""
CSV-based wallet storage.
Default location: ~/.wallet-mcp/wallets.csv
Override with WALLET_DATA_DIR env var.
"""
import csv
import os
from typing import Optional

from .utils import now_iso

_DATA_DIR = os.path.expanduser(os.getenv("WALLET_DATA_DIR", "~/.wallet-mcp"))
WALLETS_CSV = os.path.join(_DATA_DIR, "wallets.csv")

FIELDNAMES = ["address", "private_key", "chain", "label", "tags", "created_at"]


def _ensure_file() -> None:
    os.makedirs(_DATA_DIR, exist_ok=True)
    if not os.path.exists(WALLETS_CSV):
        with open(WALLETS_CSV, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()


def load_wallets() -> list[dict]:
    _ensure_file()
    with open(WALLETS_CSV, "r", newline="") as f:
        return [row for row in csv.DictReader(f) if row.get("address")]


def save_wallets_batch(wallets: list[dict]) -> None:
    _ensure_file()
    now = now_iso()
    with open(WALLETS_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        for w in wallets:
            writer.writerow({
                "address":     w.get("address", ""),
                "private_key": w.get("private_key", ""),
                "chain":       w.get("chain", ""),
                "label":       w.get("label", ""),
                "tags":        w.get("tags", ""),
                "created_at":  w.get("created_at", now),
            })


def filter_wallets(
    chain: Optional[str] = None,
    label: Optional[str] = None,
    tag: Optional[str] = None,
) -> list[dict]:
    rows = load_wallets()
    if chain:
        rows = [r for r in rows if r["chain"].lower() == chain.lower()]
    if label:
        rows = [r for r in rows if r["label"].lower() == label.lower()]
    if tag:
        rows = [r for r in rows if tag.lower() in r.get("tags", "").lower()]
    return rows


def wallet_exists(address: str) -> bool:
    return any(w["address"] == address for w in load_wallets())


def tag_wallets(label: str, tag: str) -> int:
    """Append `tag` to all wallets with `label`. Returns count updated."""
    rows = load_wallets()
    updated = 0
    for r in rows:
        if r["label"].lower() == label.lower():
            existing = r.get("tags", "")
            if tag not in existing.split("|"):
                r["tags"] = f"{existing}|{tag}".strip("|")
                updated += 1
    _rewrite(rows)
    return updated


def delete_wallets_by_label(label: str) -> int:
    rows = load_wallets()
    remaining = [r for r in rows if r["label"].lower() != label.lower()]
    removed = len(rows) - len(remaining)
    _rewrite(remaining)
    return removed


def _rewrite(rows: list[dict]) -> None:
    _ensure_file()
    with open(WALLETS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
