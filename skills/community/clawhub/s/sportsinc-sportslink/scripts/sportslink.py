#!/usr/bin/env python3
"""Sports Inc SportsLink API adapter — pull dealer invoices ("documents") and
mark them consumed.

Sports Inc is a buying group that does NOT send individual vendor invoices;
instead its SportsLink REST API exposes the dealer's documents from the
SportsWeb Invoice Center. This module is the SOURCE adapter for that API: it
authenticates, pages, normalises each SI document into a common invoice shape
(the same shape a PDF-extracted invoice would have, so downstream matching is
source-agnostic), and marks documents historical once they've been imported.

It is **customer-agnostic** — every Sports Inc dealer uses this same API — so it
carries no BaconCo/Odoo specifics. The payable-matching workflow consumes its
output; this adapter never touches Odoo.

Actions
-------
    list            GET active documents (normalised). Auto-pages.
                    Input (all optional): {"active": true, "lines": true,
                      "ediOnly": true, "poNumber": "...", "siDocNumber": 123,
                      "siDocStartDate": "2024-01-01", "siDocEndDate": "...",
                      "supplierDocStartDate": "...", "supplierDocEndDate": "...",
                      "page": 1, "pageSize": 200, "all": true,
                      "orderBy": "SIDocDate", "orderByDescending": false}
                    Defaults: active=true, lines=true, all=true (page to the end).
    get             Convenience: one/few docs by identifier.
                    Input: {"poNumber": "P13189"}  or  {"siDocNumber": 12345}
    mark-historical Mark documents consumed (PATCH status isActive=false) AFTER
                    they've been billed. Input: {"siDocNumbers": [12345, 23456]}.
                    Honors dry_run / SPORTSINC_DRY_RUN.

    The two actions below cover documents the API has no lines for (scanned/OCR
    docs, `has_lines: false`), whose line detail exists only in the SportsWeb
    Invoice Center PDF. They bracket the agent's own reading of that PDF:

    fetch-invoice-doc   Get a header-only document's PDF and make it readable —
                    text layer inline, or a file path for a scanned one.
                    Input: {"si_doc_number": 12345, "stash": "auto"} or, while
                    the portal flow is uncaptured, {"pdf_path": "/tmp/inv.pdf"}.
    reconcile-lines Check the lines the agent extracted against the API's
                    authoritative header money, and emit the finished invoice.
                    Input: {"si_doc_number": 12345, "lines": [...]}.

Environment
-----------
    SPORTSINC_API_KEY       Required. Sent as the `X-API-KEY` header.
    SPORTSINC_API_URL       Optional. Default https://api.sportsinc.com/
    SPORTSINC_DRY_RUN       Optional. If truthy, `mark-historical` is simulated.
    SPORTSINC_WEB_USERNAME  Portal login for `fetch-invoice-doc` (separate from
    SPORTSINC_WEB_PASSWORD  the API key). SPORTSINC_WEB_BASE_URL overrides the
                            default https://www.sportsinc.us/.
    SPORTSINC_PDF_DIR       Optional. Where scanned PDFs are stashed for reading.

Operational notes
-----------------
    * Do not pull before ~10:30am ET — SI's internal processing runs first.
    * Line-item data is EDI-only; scanned/OCR documents have header totals but
      no `lines` (`has_lines: false`). Use `ediOnly: true` to fetch only
      documents that carry lines.
    * `is_credit: true` marks a credit memo — handle separately, never as a bill.
    * EXACTLY-ONCE: import first, mark-historical AFTER the bill is created.
      Never mark on read (the API's `moveToHistorical=true` GET flag is
      deliberately NOT used here) — a crash between read and bill would drop the
      invoice.

Every command prints one JSON object on stdout, or {"error": {...}} with a
non-zero exit. Args are the 2nd CLI arg or JSON on stdin.
"""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Any

# Sibling modules (invoice_pdf, invoice_lines, sportsweb_browser) import by bare
# name regardless of CWD. They are imported lazily inside their handlers so the
# API actions keep working without pypdf/playwright installed.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import requests
except ImportError:  # pragma: no cover - surfaced at runtime
    requests = None  # type: ignore


DOCUMENTS_PATH = "dealers/documents/"
STATUS_PATH = "dealers/documents/status"

# GET query params we pass straight through (SportsLink param name : type-ish).
_PASSTHROUGH = {
    "poNumber", "supplierDocNumber", "siDocNumber", "siDocDate",
    "siDocStartDate", "siDocEndDate", "supplierDocDate",
    "supplierDocStartDate", "supplierDocEndDate", "fields", "orderBy",
    "orderByDescending",
}


def _fail(error_type: str, message: str, code: int = 1, **extra: Any) -> int:
    print(json.dumps({"error": {"type": error_type, "message": message, **extra}}))
    return code


def _truthy(v: Any) -> bool:
    return str(v).strip().lower() in ("1", "true", "yes", "on")


def _config() -> tuple[str, str]:
    return (
        (os.environ.get("SPORTSINC_API_URL") or "https://api.sportsinc.com/").strip().rstrip("/") + "/",
        (os.environ.get("SPORTSINC_API_KEY") or "").strip(),
    )


class _Client:
    def __init__(self, base_url: str, api_key: str, timeout: int = 30) -> None:
        self._base = base_url
        self._timeout = timeout
        self._s = requests.Session()
        self._s.headers.update({"X-API-KEY": api_key, "Accept": "application/json"})

    def _request(self, method: str, path: str, *, params=None, json_body=None) -> Any:
        url = self._base + path.lstrip("/")
        last_exc = None
        for attempt in range(4):  # resilience: retry transient failures
            try:
                resp = self._s.request(method, url, params=params, json=json_body, timeout=self._timeout)
            except requests.RequestException as exc:  # type: ignore[union-attr]
                last_exc = exc
                time.sleep(2 ** attempt)
                continue
            if resp.status_code == 401:
                raise _ApiError("auth_error", "SportsLink rejected the API key (401).", 401)
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < 3:
                time.sleep(2 ** attempt)
                continue
            if not resp.ok:
                raise _ApiError("api_error", f"{resp.status_code}: {resp.text[:300]}", resp.status_code)
            if resp.status_code == 204 or not resp.content:
                return {}
            try:
                return resp.json()
            except ValueError:
                raise _ApiError("bad_response", f"Non-JSON response: {resp.text[:200]}", resp.status_code)
        raise _ApiError("connection_error", f"SportsLink unreachable: {last_exc}")

    def get_documents(self, params: dict[str, Any]) -> dict[str, Any]:
        return self._request("GET", DOCUMENTS_PATH, params=params)

    def patch_status(self, si_doc_numbers: list[int], is_active: bool) -> Any:
        return self._request("PATCH", STATUS_PATH, json_body={"siDocNumbers": si_doc_numbers, "isActive": is_active})


class _ApiError(RuntimeError):
    def __init__(self, error_type: str, message: str, status: int | None = None) -> None:
        self.error_type = error_type
        self.status = status
        super().__init__(message)


# ── normalisation: SI document -> common invoice shape ───────────────────────


def _num(v: Any) -> Any:
    return v if isinstance(v, (int, float)) else v


# A scanned document does not come back with an empty `lines` array — SportsLink
# returns one **placeholder row**. Observed on siDocNumber 24684277, whose real
# vendor invoice has two lines totalling its 398.40 merchandise total:
#
#   {"supplierItemNumber": "", "upc": null, "size": null, "color": null,
#    "unit": "", "quantityShipped": 0, "netPrice": 0.0, "extension": 0.0,
#    "description": "SEE VENDOR INVOICE FOR DETAIL."}
#
# The row is not blank: it carries SI's own instruction, the same sentence
# printed on the cover page of the PDF. So a free-text `description` is NOT
# evidence of a real line — here it is evidence of the opposite.
#
# A line is real if it **identifies a product** (item number or UPC) or carries
# a **non-zero number**. Description, size, colour and unit are descriptive; on
# their own, with every quantity and price at zero, there is nothing billable.
#
# This matters beyond this skill. `has_lines` was `bool(lines)`, so a stub made
# a scanned document announce itself as EDI-backed, and any consumer branching
# on `has_lines` — the payables workflow does — would line-match against a row
# of zeroes instead of escalating or reading the PDF.
_LINE_IDENTITY_FIELDS = ("supplierItemNumber", "upc")
_LINE_VALUE_FIELDS = (
    "quantityOrdered", "quantityShipped", "quantityBackOrdered",
    "listPrice", "netPrice", "extension", "discountPercent",
)


def _is_placeholder_line(line: dict[str, Any]) -> bool:
    """True for a row that identifies no product and carries no non-zero number."""

    if not isinstance(line, dict):
        return True
    if any(str(line.get(field) or "").strip() for field in _LINE_IDENTITY_FIELDS):
        return False
    for field in _LINE_VALUE_FIELDS:
        value = line.get(field)
        if isinstance(value, bool) or value is None:
            continue
        if isinstance(value, (int, float)):
            if value != 0:
                return False
        elif str(value).strip() not in ("", "0", "0.0", "0.00", "0.000"):
            return False
    return True


def _normalise(item: dict[str, Any]) -> dict[str, Any]:
    raw_lines = item.get("lines") or []
    lines = [line for line in raw_lines if not _is_placeholder_line(line)]
    placeholders = len(raw_lines) - len(lines)
    # Keep whatever the dropped rows said. SI's placeholder carries a note —
    # "SEE VENDOR INVOICE FOR DETAIL." — which is both the reason the row is
    # empty and the instruction for what to do about it. Discarding it silently
    # would throw away the vendor's own explanation.
    placeholder_note = next(
        (
            " ".join(str(line.get("description")).split())
            for line in raw_lines
            if _is_placeholder_line(line) and str(line.get("description") or "").strip()
        ),
        None,
    )
    return {
        "source": "sports_inc",
        "po_number": item.get("poNumber"),
        "si_doc_number": item.get("siDocNumber"),
        "invoice_number": item.get("supplierDocNumber") or (
            str(item["siDocNumber"]) if item.get("siDocNumber") is not None else None
        ),
        "supplier_doc_number": item.get("supplierDocNumber"),
        "invoice_date": item.get("supplierDocDate") or item.get("siDocDate"),
        "si_doc_date": item.get("siDocDate"),
        "due_date": item.get("dueDate"),
        "supplier": item.get("supplier"),
        "is_credit": bool(item.get("isCredit", False)),
        # Real lines only — a placeholder row is not line data, and treating it
        # as such is how a scanned document gets billed as if it were EDI.
        "has_lines": bool(lines),
        "placeholder_lines": placeholders,
        "placeholder_note": placeholder_note,
        "total": item.get("docTotal"),
        "charges": {
            "merchandise": item.get("merchandiseTotal"),
            "freight": item.get("freightAmount"),
            "freight_allowance": item.get("freightAllowance"),
            "si_upcharge": item.get("siUpcharge"),
            "svc_handle": item.get("svcHandleCharge"),
            "sales_tax": item.get("salesTax"),
            "excise_tax": item.get("exciseTax"),
            "discount": item.get("discountAmount"),
        },
        "terms_of_payment": item.get("termsOfPayment"),
        "tracking_number": item.get("trackingNumber"),
        "lines": [
            {
                "item": ln.get("supplierItemNumber"),
                "upc": ln.get("upc"),
                "description": ln.get("description"),
                "size": ln.get("size"),
                "color": ln.get("color"),
                "unit": ln.get("unit"),
                "qty_ordered": ln.get("quantityOrdered"),
                "qty_shipped": ln.get("quantityShipped"),
                "qty_backordered": ln.get("quantityBackOrdered"),
                "list_price": ln.get("listPrice"),
                "discount_pct": ln.get("discountPercent"),
                "net_price": ln.get("netPrice"),
                "extension": ln.get("extension"),
            }
            for ln in lines
        ],
    }


# ── param building ───────────────────────────────────────────────────────────


def _build_params(args: dict[str, Any]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    # Booleans default to the safe/typical values.
    params["active"] = "true" if args.get("active", True) else "false"
    params["lines"] = "true" if args.get("lines", True) else "false"
    if args.get("ediOnly", False):
        params["excludeScannedDocuments"] = "true"
    for key in _PASSTHROUGH:
        if args.get(key) is not None:
            val = args[key]
            params[key] = ("true" if val else "false") if isinstance(val, bool) else val
    return params


# ── actions ──────────────────────────────────────────────────────────────────


def _list(client: _Client, args: dict[str, Any]) -> dict[str, Any]:
    params = _build_params(args)
    page = int(args.get("page", 1))
    page_size = int(args.get("pageSize", 200))
    auto = bool(args.get("all", True))

    invoices: list[dict[str, Any]] = []
    total_count = None
    pages_read = 0
    while True:
        params["page"] = page
        params["pageSize"] = page_size
        payload = client.get_documents(params)
        items = payload.get("items") or []
        invoices.extend(_normalise(it) for it in items)
        total_count = payload.get("totalCount", len(invoices))
        pages_read += 1
        if not auto or not payload.get("hasNextPage") or not items or pages_read >= 50:
            break
        page += 1

    result = {
        "source": "sports_inc",
        "count": len(invoices),
        "total_count": total_count,
        "pages_read": pages_read,
        "invoices": invoices,
    }
    result.update(_line_recovery_signal(invoices))
    return result


def _line_recovery_signal(invoices: list[dict[str, Any]]) -> dict[str, Any]:
    """Name the documents whose lines have to be recovered from the portal.

    A retrieval that quietly hands back some invoices with lines and some
    without leaves it to the caller to *notice* — and the cost of not noticing
    is a bill raised from no line detail at all. So the adapter says it outright:
    which documents need the fallback, and the exact commands to run.

    Credits are excluded: they are never billed, so recovering their lines
    achieves nothing. They are listed separately because they need a human
    either way.
    """

    needs = [
        invoice["si_doc_number"]
        for invoice in invoices
        if not invoice.get("has_lines") and not invoice.get("is_credit")
    ]
    credits = [invoice["si_doc_number"] for invoice in invoices if invoice.get("is_credit")]

    signal: dict[str, Any] = {"needs_line_recovery": needs}
    if credits:
        signal["credits"] = credits
    if needs:
        example = needs[0]
        signal["next_step"] = (
            f"{len(needs)} document(s) have no line detail from the API "
            f"({', '.join(str(n) for n in needs[:10])}"
            + (f", …and {len(needs) - 10} more" if len(needs) > 10 else "")
            + "). These are scanned documents; their lines exist only in the "
            "SportsWeb portal PDF. For EACH one, before billing it: "
            f'`fetch-invoice-doc {{"si_doc_number": {example}}}` → read the returned '
            f'text → `reconcile-lines {{"si_doc_number": {example}, "lines": [...]}}`. '
            "Bill only a `verified` result; escalate `needs_review`. Do NOT bill a "
            "document from header totals alone."
        )
    return signal


def _get(client: _Client, args: dict[str, Any]) -> dict[str, Any]:
    if not (args.get("poNumber") or args.get("siDocNumber") or args.get("supplierDocNumber")):
        raise ValueError("Pass an identifier: poNumber, siDocNumber, or supplierDocNumber.")
    # A specific-doc lookup shouldn't filter by active-only by default.
    q = dict(args)
    q.setdefault("active", False)
    return _list(client, q)


def _mark_historical(client: _Client, args: dict[str, Any]) -> dict[str, Any]:
    nums = args.get("siDocNumbers")
    if not isinstance(nums, list) or not nums:
        raise ValueError("`siDocNumbers` (a non-empty list of integers) is required.")
    nums = [int(n) for n in nums]
    dry = bool(args.get("dry_run")) or _truthy(os.environ.get("SPORTSINC_DRY_RUN", ""))
    if dry:
        return {"dry_run": True, "would_mark_historical": nums, "isActive": False}
    client.patch_status(nums, is_active=False)  # 204 No Content on success
    return {"marked_historical": nums, "isActive": False}


def _get_for_a2a(client: _Client, args: dict[str, Any]) -> dict[str, Any]:
    """A2A-safe action for structured inter-agent requests.

    Contract request (all fields optional):
    {
      "customer_ref": "DEALER-001",     # advisory only — echoed back, NOT a filter
      "date_range": {"start": "2024-01-01", "end": "2024-12-31"},
      "include_historical": false        # false (default) → active/un-imported only
    }

    Unlike the exit-code contract of the other actions, this action always exits
    0 and reports failure IN-BAND via `success: false` + `error`, so an A2A caller
    reads one structured envelope whether the call succeeded or not:
    {"success": true, "invoices": [...], "metadata": {...}, "error": null}
    {"success": false, "invoices": null, "metadata": null, "error": {...}}

    Note on `customer_ref`: the SportsLink API key is issued per dealer and the
    API has no customer filter, so `customer_ref` cannot scope the result. It is
    accepted for auditing and echoed back in `metadata.customer_ref`; downstream
    (Odoo/payable-matching) does any customer-specific handling.
    """
    def _err(error_type: str, message: str, retriable: bool) -> dict[str, Any]:
        return {
            "success": False,
            "invoices": None,
            "metadata": None,
            "error": {"type": error_type, "message": message, "retriable": retriable},
        }

    try:
        customer_ref = args.get("customer_ref")
        date_range = args.get("date_range") or {}
        # Historical inclusion is governed by `include_historical` (NOT by any
        # status string): active=False lifts the active-only filter and returns
        # historical/consumed docs too. Default keeps the safe un-imported inbox.
        include_historical = bool(args.get("include_historical", False))

        list_args: dict[str, Any] = {
            "active": not include_historical,
            "lines": True,
            "all": True,  # Auto-page through all results
        }
        if date_range.get("start"):
            list_args["siDocStartDate"] = date_range["start"]
        if date_range.get("end"):
            list_args["siDocEndDate"] = date_range["end"]

        result = _list(client, list_args)

        return {
            "success": True,
            "invoices": result.get("invoices", []),
            "metadata": {
                "count": result.get("count"),
                "total_count": result.get("total_count"),
                "pages_read": result.get("pages_read"),
                "source": result.get("source"),
                "customer_ref": customer_ref,        # echoed for the caller's audit
                "include_historical": include_historical,
                # An A2A caller cannot read a doc comment, so the contract
                # itself has to carry the obligation: these documents are not
                # billable as returned.
                "needs_line_recovery": result.get("needs_line_recovery", []),
                "credits": result.get("credits", []),
                "next_step": result.get("next_step"),
            },
            "error": None,
        }
    except _ApiError as exc:
        return _err(
            exc.error_type,
            str(exc),
            exc.error_type in ("connection_error", "bad_response"),
        )
    except (KeyError, ValueError, TypeError) as exc:
        return _err("validation_error", str(exc), False)


# ── header-only documents: PDF line extraction ───────────────────────────────
#
# A scanned/OCR document comes back with header money but no `lines`. Its line
# detail exists only in the SportsWeb Invoice Center PDF, so the fallback runs in
# three beats: this module fetches and unpacks the PDF, the *agent* reads it, and
# this module then checks the agent's arithmetic against the API's header. The
# reading is the only fuzzy step, and it is the only one a model touches.


def _one_document(client: _Client, si_doc_number: Any) -> dict[str, Any]:
    """Fetch exactly one document by SI doc number (active or historical)."""

    try:
        doc_number = int(si_doc_number)
    except (TypeError, ValueError):
        raise ValueError(f"`si_doc_number` must be an integer, got {si_doc_number!r}.")
    result = _list(client, {"siDocNumber": doc_number, "active": False, "lines": True})
    invoices = result.get("invoices") or []
    if not invoices:
        raise _ApiError("api_error", f"No SportsLink document found for siDocNumber {doc_number}.")

    # Trust the filter, but verify it. Taking `invoices[0]` blind would operate
    # on the wrong document if the API ever ignored or widened the filter — the
    # same silently-wrong-invoice failure the portal row matching guards against,
    # and just as invisible downstream.
    matched = [
        invoice for invoice in invoices
        if str(invoice.get("si_doc_number")) == str(doc_number)
    ]
    if not matched:
        found = ", ".join(str(invoice.get("si_doc_number")) for invoice in invoices[:10])
        raise _ApiError(
            "api_error",
            f"SportsLink returned {len(invoices)} document(s) for siDocNumber "
            f"{doc_number}, none carrying that number (got: {found}). Refusing to "
            "guess which one was meant.",
        )
    return matched[0]


def _existing_lines_message(invoice: dict[str, Any]) -> str:
    """Explain a refusal to re-read a document the API already has lines for —
    and say whether those lines can actually be trusted.

    "It already has lines" is not the same as "its lines are complete". Running
    the EDI lines through the same reconciliation the PDF path uses answers the
    only question that matters here: do they sum to the merchandise total? If
    they don't, the API's data is *worse* than absent — it looks authoritative
    while being short — and re-reading the PDF is the right call.
    """

    from invoice_lines import reconcile  # noqa: E402  (lazy)

    lines = invoice.get("lines") or []
    summary = "; ".join(
        f"{line.get('item') or '?'}"
        f"{' ' + str(line.get('size')) if line.get('size') else ''}"
        f" ×{line.get('qty_shipped')} @ {line.get('net_price')} = {line.get('extension')}"
        for line in lines[:6]
    )
    if len(lines) > 6:
        summary += f"; …and {len(lines) - 6} more"

    header = f"siDocNumber {invoice.get('si_doc_number')} already has {len(lines)} line "
    header += "item" if len(lines) == 1 else "items"
    header += f" from the API: {summary}. "

    try:
        checked = reconcile(invoice, lines)
    except (KeyError, ValueError, TypeError):
        return header + 'Pass {"force": true} to re-read the PDF anyway.'

    if checked["status"] == "verified":
        return (
            header
            + "They reconcile to the merchandise total, so they are complete — use them "
            + 'instead of re-reading the PDF. Pass {"force": true} only if they are '
            + "known to be wrong for some other reason."
        )
    reasons = "; ".join(issue["message"] for issue in checked["reconciliation"]["issues"][:2])
    # Carry the raw lines. A refusal that only summarises them cannot be
    # diagnosed without going back to the API by hand — which is precisely the
    # detour the placeholder-row investigation took.
    raw = json.dumps(lines[:3], default=str, ensure_ascii=False)
    return (
        header
        + f"They do NOT reconcile to the API's own header ({reasons}) — the EDI data is "
        + "incomplete, which is worse than absent because it looks authoritative. "
        + 'Re-read the PDF with {"force": true}, then reconcile-lines. '
        + f"The lines as received: {raw}"
    )


def _fetch_invoice_doc(client: _Client | None, args: dict[str, Any]) -> dict[str, Any]:
    """Get a header-only document's PDF and hand back something readable.

    Input: {"si_doc_number": 12345, "stash": "auto"|"always"|"never",
            "pdf_path": "/path/to.pdf", "force": false,
            "username"/"password"/"base_url": portal credential overrides}

    `pdf_path` skips the portal entirely and reads a PDF off disk — the manual
    path for a document pulled by hand, and the only path that works until the
    SportsWeb flow is captured.

    The result carries the document's *identity* (PO, invoice number, date,
    supplier, credit flag) but deliberately **not** its money. Extraction should
    be blind to the total it will be checked against — an agent that knows the
    merchandise total can unconsciously bend a misread line to hit it, which is
    precisely the error `reconcile-lines` exists to catch.
    """

    from invoice_pdf import PdfError, prepare, read_pdf_file  # noqa: E402  (lazy)

    si_doc_number = args.get("si_doc_number")
    po_number = args.get("po_number")
    pdf_path = args.get("pdf_path")
    stash = args.get("stash", "auto")

    if si_doc_number is None and not po_number and not pdf_path:
        raise ValueError(
            "Pass `si_doc_number` (one document), `po_number` (every document on a PO — "
            "the portal's own search key), or `pdf_path` for a manually downloaded PDF."
        )

    invoice: dict[str, Any] | None = None
    if si_doc_number is not None and client is not None:
        invoice = _one_document(client, si_doc_number)
        if invoice.get("has_lines") and not args.get("force"):
            raise ValueError(_existing_lines_message(invoice))

    source_url = None
    try:
        portal_meta: dict[str, Any] = {}
        if pdf_path:
            pdf_bytes = read_pdf_file(str(pdf_path))
            source = "manual"
        else:
            from sportsweb_browser import fetch_invoice_pdf  # noqa: E402  (lazy)

            pdf_bytes, source_url, portal_meta = fetch_invoice_pdf(
                si_doc_number=si_doc_number,
                po_number=po_number or (invoice or {}).get("po_number"),
                supplier_doc_number=(invoice or {}).get("supplier_doc_number"),
                credentials_override={
                    key: args[key] for key in ("username", "password", "base_url") if key in args
                },
            )
            source = "sportsweb"
        prepared = prepare(
            pdf_bytes,
            label=str(si_doc_number or po_number or "manual"),
            stash=stash,
            ocr=args.get("ocr"),
        )
    except PdfError as exc:
        raise _ApiError("api_error", str(exc))

    # A download often bundles several SI documents (one cover page + its vendor
    # invoice, repeated). Flag which group belongs to the document asked for, so
    # the agent reads the right pages rather than the first ones.
    if si_doc_number is not None:
        for document in prepared.get("documents", []):
            document["matches_requested"] = int(si_doc_number) in (
                document.get("si_doc_number_candidates") or []
            )
        if not any(d.get("matches_requested") for d in prepared["documents"]):
            prepared.setdefault("notes", []).append(
                f"siDocNumber {si_doc_number} was not found on any cover page in this "
                "PDF — confirm you are reading the right document before extracting."
            )

    # The assembled `text` already carries every page's characters with page
    # marks; repeating them per page would double the payload for nothing.
    pages = [{k: v for k, v in page.items() if k != "text"} for page in prepared["pages"]]

    return {
        "source": "sports_inc",
        "si_doc_number": si_doc_number,
        "po_number": (invoice or {}).get("po_number") or po_number,
        "invoice_number": (invoice or {}).get("invoice_number"),
        "invoice_date": (invoice or {}).get("invoice_date"),
        "supplier": (invoice or {}).get("supplier"),
        "is_credit": (invoice or {}).get("is_credit"),
        "pdf_source": source,
        "source_url": source_url,
        "portal_tab": portal_meta.get("tab"),
        "portal_rows": portal_meta.get("matched_rows"),
        "note": (
            "Header totals are withheld on purpose — extract what the PDF says, not "
            "what a total implies. `reconcile-lines` supplies the check."
        ),
        # Finding a document on the Archived tab means Sports Inc has already
        # marked it historical — which, in this skill's own exactly-once rule,
        # happens only AFTER a bill was created. Worth saying out loud: it is a
        # duplicate-payment tell, not a routing detail.
        **(
            {"already_historical_warning": (
                f"This document was found on the portal's ARCHIVED tab, so it has "
                "already been marked historical. Under the exactly-once rule that "
                "happens only after a bill was created — check whether it has "
                "already been billed before creating another."
            )}
            if portal_meta.get("tab") == "archived" else {}
        ),
        **{k: v for k, v in prepared.items() if k not in ("bytes", "pages")},
        "pages": pages,
        "pdf_bytes": prepared.get("bytes"),
    }


def _reconcile_lines(client: _Client, args: dict[str, Any]) -> dict[str, Any]:
    """Check agent-extracted lines against the API header and emit the invoice.

    Input: {"si_doc_number": 12345, "lines": [{...}, ...], "tolerance": 0.05}

    The header always comes from SportsLink, never from the caller — a check
    against numbers the same agent just read off the PDF verifies nothing. The
    result is `status: "verified"` (bill it like an EDI invoice) or
    `status: "needs_review"` (leave the document active and escalate).

    This never marks anything historical: the exactly-once seam stays where it
    is — the bill gets created first, `mark-historical` after.
    """

    from invoice_lines import reconcile  # noqa: E402  (lazy)

    si_doc_number = args.get("si_doc_number")
    if si_doc_number is None:
        raise ValueError("`si_doc_number` is required so the lines can be checked against the API header.")
    if "lines" not in args:
        raise ValueError("`lines` (the line items you extracted from the PDF) is required.")

    invoice = _one_document(client, si_doc_number)
    return reconcile(invoice, args["lines"], tolerance=args.get("tolerance"))


def _capture_portal(client: _Client | None, args: dict[str, Any]) -> dict[str, Any]:
    """Diagnostic: log in to SportsWeb, run a search, and report what is there.

    Input: {"search": "P13554", "probe_download": false, "headless": true,
            "html_path": "...", "screenshot_path": "..."}

    Read-only apart from `probe_download`, which additionally ticks the first row
    and clicks Downloads to record how the PDF actually comes down (a download
    event, an inline response, or neither). Nothing in the portal is modified
    either way.

    This exists so the open questions in references/sportsweb_flow_notes.md get
    answered by a real run rather than by guesswork — run it once against the
    live portal and paste the output back into that file.
    """

    from invoice_pdf import scratch_dir  # noqa: E402  (lazy)
    from sportsweb_browser import capture_portal  # noqa: E402  (lazy)

    search = args.get("search") or args.get("po_number") or args.get("si_doc_number")
    label = _safe_label(search)
    directory = scratch_dir()

    return capture_portal(
        search=str(search) if search else None,
        archived=bool(args.get("archived")),
        search_column=args.get("search_column", "po"),
        probe_download=bool(args.get("probe_download")),
        download_format=args.get("download_format", "pdf"),
        save_download_to=args.get("save_download_to")
        or (
            str(directory / f"capture-{label}{_DOWNLOAD_SUFFIX.get(args.get('download_format', 'pdf'), '.bin')}")
            if args.get("probe_download")
            else None
        ),
        html_path=args.get("html_path") or str(directory / f"capture-{label}.html"),
        screenshot_path=args.get("screenshot_path") or str(directory / f"capture-{label}.png"),
        credentials_override={
            key: args[key] for key in ("username", "password", "base_url") if key in args
        },
        headless=args.get("headless"),
    )


# So a probed download lands with an extension that opens.
_DOWNLOAD_SUFFIX = {
    "pdf": ".pdf",
    "pdf_zip": ".zip",
    "csv": ".csv",
    "csv_items": ".csv",
    "pdf_and_csv": ".zip",
}


def _safe_label(value: Any) -> str:
    cleaned = "".join(ch for ch in str(value or "portal") if ch.isalnum() or ch in "._-")
    return cleaned or "portal"


ACTIONS = {
    "list": _list,
    "get": _get,
    "mark-historical": _mark_historical,
    "get-for-a2a": _get_for_a2a,
    "fetch-invoice-doc": _fetch_invoice_doc,
    "reconcile-lines": _reconcile_lines,
    "capture-portal": _capture_portal,
}

# Actions that can run without SPORTSINC_API_KEY, and under what condition. A
# manually supplied PDF needs no API call, so the extraction half stays testable
# on a machine that has no key.
def _needs_api_key(action: str, args: dict[str, Any]) -> bool:
    if action == "fetch-invoice-doc":
        return not args.get("pdf_path")
    if action == "capture-portal":
        return False  # portal-only diagnostic; touches no API
    return True

USAGE = "sportslink.py <" + "|".join(ACTIONS) + ">   # JSON args as 2nd arg or on stdin"


def _read_args() -> dict[str, Any]:
    raw = None
    if len(sys.argv) >= 3:
        raw = sys.argv[2]
    elif not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
    raw = (raw or "").strip() or "{}"
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.exit(_fail("invalid_arguments", f"Arguments must be valid JSON: {exc}", 2))
    if not isinstance(parsed, dict):
        sys.exit(_fail("invalid_arguments", "Arguments must be a JSON object.", 2))
    return parsed


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        return _fail("usage", USAGE, 2)
    handler = ACTIONS.get(sys.argv[1])
    if handler is None:
        return _fail("unknown_action", f"Unknown action {sys.argv[1]!r}. Use: {', '.join(ACTIONS)}", 2)
    args = _read_args()
    action = sys.argv[1]

    client: _Client | None = None
    if _needs_api_key(action, args):
        if requests is None:
            return _fail("config_error", "The 'requests' package is required. Install it (see the skill's install deps).", 2)
        base_url, api_key = _config()
        if not api_key:
            return _fail("config_error", "Set SPORTSINC_API_KEY (request one from mhoerner@hq.sportsinc.com).", 2)
        client = _Client(base_url, api_key)

    try:
        result = handler(client, args)
    except _ApiError as exc:
        return _fail(exc.error_type, str(exc), 1, status=exc.status)
    except (KeyError, ValueError, TypeError) as exc:
        return _fail("validation_error", str(exc), 2)
    except Exception as exc:  # noqa: BLE001 — modules that carry their own type
        error_type = getattr(exc, "error_type", None)
        if not error_type:
            raise
        return _fail(error_type, str(exc), 2 if error_type == "config_error" else 1)
    print(json.dumps(result, default=str, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
