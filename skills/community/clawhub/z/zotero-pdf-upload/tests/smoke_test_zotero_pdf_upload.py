#!/usr/bin/env python3
"""Smoke tests for zotero-pdf-upload skill utilities (no network)."""


import json
import os
import sys
import tempfile
from pathlib import Path

# Allow importing from scripts/ directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from zotero_client import load_api_key, parse_zotero_library_url, resolve_library_settings
from zotero_workflow import _extract_created_item_key


def _test_parse_url() -> None:
    # Group URL
    parsed = parse_zotero_library_url("https://www.zotero.org/groups/6320165/my-group/library")
    assert parsed.get("libraryType") == "group", parsed
    assert parsed.get("libraryId") == "6320165", parsed

    # User URL with numeric ID
    parsed2 = parse_zotero_library_url("www.zotero.org/users/123456/library")
    assert parsed2.get("libraryType") == "user", parsed2
    assert parsed2.get("libraryId") == "123456", parsed2

    # Collection key extraction
    parsed3 = parse_zotero_library_url(
        "https://www.zotero.org/groups/6320165/my-group/collections/ABCD1234"
    )
    assert parsed3.get("collectionKey") == "ABCD1234", parsed3

    # Personal URL (username, no numeric ID)
    parsed4 = parse_zotero_library_url("https://www.zotero.org/myusername/library")
    assert parsed4.get("libraryType") == "user", parsed4
    assert parsed4.get("username") == "myusername", parsed4
    assert "libraryId" not in parsed4, parsed4

    # Personal URL with collection
    parsed5 = parse_zotero_library_url(
        "https://www.zotero.org/myuser/collections/WXYZ5678"
    )
    assert parsed5.get("libraryType") == "user", parsed5
    assert parsed5.get("username") == "myuser", parsed5
    assert parsed5.get("collectionKey") == "WXYZ5678", parsed5

    # Non-zotero URL should not trigger personal URL fallback
    parsed6 = parse_zotero_library_url("https://example.com/someuser/library")
    assert not parsed6, parsed6


def _test_secret_loading_precedence() -> None:
    old = os.environ.get("ZOTERO_API_KEY")
    try:
        with tempfile.TemporaryDirectory(prefix="zotero-pdf-upload-test-") as td:
            secret_path = Path(td) / "zotero.key"
            secret_path.write_text("path-key", encoding="utf-8")

            cfg = {"apiKeyPath": str(secret_path), "apiKey": "inline-key"}
            os.environ["ZOTERO_API_KEY"] = "env-key"
            key, source = load_api_key(cfg)
            assert key == "env-key" and source == "env:ZOTERO_API_KEY", (key, source)

            del os.environ["ZOTERO_API_KEY"]
            key2, source2 = load_api_key(cfg)
            assert key2 == "path-key" and source2.startswith("path:"), (key2, source2)

            secret_path.unlink()
            key3, source3 = load_api_key(cfg)
            assert key3 == "inline-key" and source3 == "inline:apiKey", (key3, source3)
    finally:
        if old is None:
            os.environ.pop("ZOTERO_API_KEY", None)
        else:
            os.environ["ZOTERO_API_KEY"] = old


def _test_resolve_library_settings() -> None:
    # Legacy groupUrl field still works
    cfg = {
        "zotero": {
            "groupUrl": "https://www.zotero.org/groups/6320165/my-group/library",
            "apiKey": "abc",
        }
    }
    settings = resolve_library_settings(cfg)
    assert settings.library_type == "group", settings
    assert settings.library_id == "6320165", settings
    assert settings.api_key == "abc", settings

    # New unified "url" field works for group URLs
    cfg2 = {
        "zotero": {
            "url": "https://www.zotero.org/groups/999/test/library",
            "apiKey": "xyz",
        }
    }
    settings2 = resolve_library_settings(cfg2)
    assert settings2.library_type == "group", settings2
    assert settings2.library_id == "999", settings2


def _test_resolve_personal_url_with_explicit_id() -> None:
    """Personal URL + explicit libraryId should work without network."""
    cfg = {
        "zotero": {
            "url": "https://www.zotero.org/myusername/library",
            "libraryId": "7654321",
            "apiKey": "test-key",
        }
    }
    settings = resolve_library_settings(cfg)
    assert settings.library_type == "user", settings
    assert settings.library_id == "7654321", settings


def _test_extract_created_item_key() -> None:
    resp = {"successful": {"0": {"key": "ITEM1234"}}}
    assert _extract_created_item_key(resp) == "ITEM1234"


def _test_choose_collection_heuristic() -> None:
    from zotero_client import ZoteroClient

    item = {
        "title": "Practical Alignment Evaluation for LLM Agents",
        "abstractNote": "benchmark and alignment evaluation methods",
        "tags": ["alignment", "llm"],
    }
    collections = [
        {"key": "ABCD1234", "data": {"name": "LLM Safety Alignment"}},
        {"key": "WXYZ5678", "data": {"name": "Computer Vision"}},
    ]

    best, score, reason = ZoteroClient.find_best_matching_collection(item=item, collections=collections)
    assert best is not None, (best, score, reason)
    assert (best.get("key") or best.get("data", {}).get("key")) == "ABCD1234", (best, score, reason)


def main() -> int:
    _test_parse_url()
    _test_secret_loading_precedence()
    _test_resolve_library_settings()
    _test_resolve_personal_url_with_explicit_id()
    _test_extract_created_item_key()
    _test_choose_collection_heuristic()

    print("Smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
