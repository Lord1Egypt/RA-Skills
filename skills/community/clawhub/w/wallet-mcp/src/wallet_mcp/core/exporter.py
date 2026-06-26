"""
Wallet exporter: dump a wallet list to JSON or CSV.

Supports:
  - format='json'  → pretty-printed JSON array
  - format='csv'   → standard CSV matching storage schema
  - include_keys   → include or strip private keys from output
  - output_path    → explicit file path, or auto-generated under ~/.wallet-mcp/exports/
"""
import csv
import json
import os
from typing import Optional

from .utils import now_iso, setup_logging

_log = setup_logging()

_EXPORT_FIELDS = ["address", "private_key", "chain", "label", "tags", "created_at"]


def export_wallets(
    wallets: list[dict],
    fmt: str = "json",
    output_path: Optional[str] = None,
    include_keys: bool = False,
) -> dict:
    """
    Export wallet list to a JSON or CSV file.

    Args:
        wallets:      list of wallet dicts (from storage.filter_wallets)
        fmt:          'json' or 'csv'
        output_path:  destination file path; auto-generated if omitted
        include_keys: include private keys in export (default False)

    Returns:
        {path, format, count, include_keys}
    """
    fmt = fmt.lower()
    if fmt not in ("json", "csv"):
        raise ValueError(f"Unsupported format '{fmt}'. Choose 'json' or 'csv'.")

    if not output_path:
        data_dir = os.path.expanduser(os.getenv("WALLET_DATA_DIR", "~/.wallet-mcp"))
        export_dir = os.path.join(data_dir, "exports")
        os.makedirs(export_dir, exist_ok=True)
        ts = now_iso().replace(":", "-").replace("T", "_")[:-1]  # safe filename
        output_path = os.path.join(export_dir, f"wallets_{ts}.{fmt}")
    else:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    rows = _prepare_rows(wallets, include_keys)

    if fmt == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)
    else:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            fields = _EXPORT_FIELDS if include_keys else [x for x in _EXPORT_FIELDS if x != "private_key"]
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    _log.info(f"Exported {len(rows)} wallets → {output_path} (format={fmt}, keys={include_keys})")
    return {
        "path":         output_path,
        "format":       fmt,
        "count":        len(rows),
        "include_keys": include_keys,
    }


def _prepare_rows(wallets: list[dict], include_keys: bool) -> list[dict]:
    rows = []
    for w in wallets:
        row = {f: w.get(f, "") for f in _EXPORT_FIELDS}
        if not include_keys:
            del row["private_key"]
        rows.append(row)
    return rows
