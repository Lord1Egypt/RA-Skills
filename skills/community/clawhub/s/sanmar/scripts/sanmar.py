#!/usr/bin/env python3
"""SanMar API toolkit — single CLI entrypoint for all sanmar tools.

Usage:
    python3 scripts/sanmar.py <action>   # JSON args on stdin

Each action maps to a deterministic SanMar tool. Arguments are a JSON object
on stdin whose keys match the tool's parameters; the result is a single JSON
object on stdout (or `{"error": {...}}` with a non-zero exit code on failure).

Credentials come from the `SANMAR_*` environment variables by default, or can
be passed inline in the stdin JSON (`customer_number`, `username`, `password`,
`environment`, and `ftp_password` for the SFTP-backed tools).

Actions:
    search-products         Catalog discovery for a style.
                            {"style": "PC55", "color"?, "size"?}
    check-inventory         Live warehouse inventory for one SKU.
                            {"style", "color", "size", "auto_resolve_color"?}
    get-pricing             myPrice + tier pricing for lines.
                            {"lines": [{"style","color","size"}, ...]}
    validate-cart           Pre-submit validation of a draft PO (no commit).
                            {"purchase_order": {...}}
    create-purchase-order   Submit a PO. EXTERNAL WRITE — needs "confirm": true,
                            otherwise returns a dry-run SOAP preview.
                            {"purchase_order": {...}, "confirm": false}
    check-order-status      SanMar order number + shipment progress for a PO.
                            {"po_number": "..."}
    get-tracking            Tracking numbers + carriers for a PO.
                            {"po_number": "..."}
    cancel-order            Reserved stub — SanMar exposes no cancel endpoint.
                            {"po_number": "...", "reason"?, "confirm"?}
    parse-po-pdf            Extract a draft PO from a PDF (show user for approval).
                            {"pdf_path": "/path/to/po.pdf"}
    lookup-mainframe-color  Resolve a marketing color to its mainframe code (SFTP).
                            {"style", "color", "size"?, "force_refresh"?}
"""

from __future__ import annotations

import os
import sys

# Ensure sibling modules import by bare name regardless of CWD.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _cli import run  # noqa: E402
from sanmar_tools import (  # noqa: E402
    sanmar_cancel_order,
    sanmar_check_inventory,
    sanmar_check_order_status,
    sanmar_create_purchase_order,
    sanmar_get_pricing,
    sanmar_get_tracking,
    sanmar_lookup_mainframe_color,
    sanmar_parse_po_pdf,
    sanmar_search_products,
    sanmar_validate_cart,
)

ACTIONS = {
    "search-products": sanmar_search_products,
    "check-inventory": sanmar_check_inventory,
    "get-pricing": sanmar_get_pricing,
    "validate-cart": sanmar_validate_cart,
    "create-purchase-order": sanmar_create_purchase_order,
    "check-order-status": sanmar_check_order_status,
    "get-tracking": sanmar_get_tracking,
    "cancel-order": sanmar_cancel_order,
    "parse-po-pdf": sanmar_parse_po_pdf,
    "lookup-mainframe-color": sanmar_lookup_mainframe_color,
}


if __name__ == "__main__":
    run(
        ACTIONS,
        usage="sanmar.py <" + "|".join(ACTIONS) + ">",
    )
