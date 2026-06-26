#!/usr/bin/env python3
"""Check for possibly missing tax documents by comparing tax years."""

import argparse
import json
import os
from typing import Any, Dict, List, Set, Tuple


BASE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tax")
DOCUMENTS_FILE = os.path.join(BASE_DIR, "documents.json")


def load_json(path: str, default: Dict[str, Any]) -> Dict[str, Any]:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def normalize_doc_key(document: Dict[str, Any]) -> Tuple[str, str]:
    document_type = str(document.get("document_type", "")).strip()
    issuer = str(document.get("issuer", "")).strip()
    return (document_type, issuer)


def documents_for_year(documents: List[Dict[str, Any]], tax_year: int) -> List[Dict[str, Any]]:
    return [doc for doc in documents if doc.get("tax_year") == tax_year]


def key_set(documents: List[Dict[str, Any]]) -> Set[Tuple[str, str]]:
    return {normalize_doc_key(doc) for doc in documents if normalize_doc_key(doc) != ("", "")}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check for possibly missing documents by comparing tax years."
    )
    parser.add_argument(
        "--tax-year",
        type=int,
        required=True,
        help="Current tax year to inspect",
    )
    parser.add_argument(
        "--compare-year",
        type=int,
        required=True,
        help="Prior tax year to compare against",
    )

    args = parser.parse_args()

    data = load_json(DOCUMENTS_FILE, {"documents": []})
    all_documents = data.get("documents", [])

    current_docs = documents_for_year(all_documents, args.tax_year)
    prior_docs = documents_for_year(all_documents, args.compare_year)

    current_keys = key_set(current_docs)
    prior_keys = key_set(prior_docs)

    missing_keys = sorted(prior_keys - current_keys)

    print(f"Tax year checked: {args.tax_year}")
    print(f"Compared against: {args.compare_year}")
    print(f"Documents in {args.compare_year}: {len(prior_docs)}")
    print(f"Documents in {args.tax_year}: {len(current_docs)}")
    print("")

    if not prior_docs:
        print("No prior-year documents found. Nothing to compare.")
        return

    if not missing_keys:
        print("No possible missing documents found based on prior-year document history.")
        return

    print("Possible missing documents:")
    for document_type, issuer in missing_keys:
        print(f"- {document_type} from {issuer}")


if __name__ == "__main__":
    main()
