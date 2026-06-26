#!/usr/bin/env python3
"""Archive a tax year and roll forward expected document patterns."""

import argparse
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple


BASE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tax")
DOCUMENTS_FILE = os.path.join(BASE_DIR, "documents.json")
YEAR_STATE_FILE = os.path.join(BASE_DIR, "year_state.json")
EXPECTED_DOCUMENTS_FILE = os.path.join(BASE_DIR, "expected_documents.json")


def ensure_base_dir() -> None:
    os.makedirs(BASE_DIR, exist_ok=True)


def load_json(path: str, default: Dict[str, Any]) -> Dict[str, Any]:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path: str, data: Dict[str, Any]) -> None:
    ensure_base_dir()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def filter_by_tax_year(items: List[Dict[str, Any]], tax_year: int) -> List[Dict[str, Any]]:
    return [item for item in items if item.get("tax_year") == tax_year]


def normalized_doc_key(document: Dict[str, Any]) -> Tuple[str, str]:
    document_type = str(document.get("document_type", "")).strip()
    issuer = str(document.get("issuer", "")).strip()
    return (document_type, issuer)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Archive a tax year and roll forward expected document patterns."
    )
    parser.add_argument(
        "--tax-year",
        type=int,
        required=True,
        help="Tax year to archive",
    )

    args = parser.parse_args()
    tax_year = args.tax_year
    next_year = tax_year + 1
    now_iso = datetime.now().isoformat(timespec="seconds")

    documents_data = load_json(DOCUMENTS_FILE, {"documents": []})
    year_state_data = load_json(YEAR_STATE_FILE, {"years": {}})
    expected_data = load_json(EXPECTED_DOCUMENTS_FILE, {"years": {}})

    archived_year_docs = filter_by_tax_year(documents_data.get("documents", []), tax_year)

    # 1. Update current tax year state to archived
    if "years" not in year_state_data:
        year_state_data["years"] = {}

    existing_year_state = year_state_data["years"].get(str(tax_year), {})
    existing_year_state["state"] = "archived"
    existing_year_state["updated_at"] = now_iso
    year_state_data["years"][str(tax_year)] = existing_year_state

    # 2. Prepare expected documents container for next year
    if "years" not in expected_data:
        expected_data["years"] = {}

    next_year_bucket = expected_data["years"].get(str(next_year), {})
    expected_documents = next_year_bucket.get("expected_documents", [])

    existing_keys = {
        (
            str(item.get("document_type", "")).strip(),
            str(item.get("issuer", "")).strip(),
        )
        for item in expected_documents
    }

    added_count = 0

    for doc in archived_year_docs:
        doc_key = normalized_doc_key(doc)
        if doc_key == ("", ""):
            continue
        if doc_key in existing_keys:
            continue

        expected_documents.append(
            {
                "document_type": doc_key[0],
                "issuer": doc_key[1],
                "reason": f"appeared_in_prior_year_{tax_year}",
                "status": "awaiting",
                "source_tax_year": tax_year,
                "created_at": now_iso,
            }
        )
        existing_keys.add(doc_key)
        added_count += 1

    next_year_bucket["expected_documents"] = expected_documents
    next_year_bucket["updated_at"] = now_iso
    expected_data["years"][str(next_year)] = next_year_bucket

    save_json(YEAR_STATE_FILE, year_state_data)
    save_json(EXPECTED_DOCUMENTS_FILE, expected_data)

    print(f"Archived tax year: {tax_year}")
    print(f"  State updated to: archived")
    print(f"  Documents reviewed: {len(archived_year_docs)}")
    print(f"  Expected documents added for {next_year}: {added_count}")
    print(f"  Saved year state to: {YEAR_STATE_FILE}")
    print(f"  Saved expected documents to: {EXPECTED_DOCUMENTS_FILE}")


if __name__ == "__main__":
    main()
