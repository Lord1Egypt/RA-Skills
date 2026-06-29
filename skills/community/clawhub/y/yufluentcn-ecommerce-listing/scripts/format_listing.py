"""Listing 结果格式化 — 薄 re-export，实现见 tokenapi-harness。"""

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_SHARED_DIR = _SCRIPTS_DIR.parent.parent / "_shared"
if str(_SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(_SHARED_DIR))
from bootstrap import ensure_harness_packages_path

ensure_harness_packages_path(__file__)

from tokenapi_harness.listing_format import (  # noqa: F401
    FORMATTERS,
    format_listing,
    listing_from_response,
    to_amazon_format,
    to_shopify_format,
    to_tiktok_format,
)
