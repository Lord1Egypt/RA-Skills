"""Normalise agent-extracted invoice lines and reconcile them against the API header.

This is the half of the header-only fallback that the model does **not** get to
reason about. The agent reads the PDF and produces line items; this module then
checks that arithmetic against the money SportsLink already told us
authoritatively — `merchandiseTotal`, the charge components, `docTotal` — and
refuses to bless a set of lines that doesn't tie out.

The point is adversarial: a model that misreads a quantity will also cheerfully
confirm its own misreading, so the check has to live in code the model cannot
talk its way past. `verified` means the numbers actually add up. Anything else
comes back `needs_review`, and the caller leaves the SI document active.

Money is handled in `Decimal` throughout — a float sum of forty line extensions
drifts by cents, which is exactly the size of the error we are looking for.
"""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Any

# Canonical line fields, mirroring `sportslink._normalise` so a PDF-extracted
# invoice is indistinguishable downstream from an EDI one.
_CANONICAL_FIELDS = (
    "item", "upc", "description", "size", "color", "unit",
    "qty_ordered", "qty_shipped", "qty_backordered",
    "list_price", "discount_pct", "net_price", "extension",
)

# Aliases the agent might reasonably use when reading a PDF. First match wins.
_ALIASES: dict[str, tuple[str, ...]] = {
    "item": ("item", "item_number", "itemNumber", "supplier_item_number",
             "supplierItemNumber", "style", "style_number", "sku", "part", "part_number"),
    "upc": ("upc", "barcode", "gtin", "ean"),
    "description": ("description", "desc", "product", "product_description"),
    "size": ("size",),
    "color": ("color", "colour"),
    "unit": ("unit", "uom", "unit_of_measure"),
    "qty_ordered": ("qty_ordered", "quantity_ordered", "quantityOrdered", "ordered", "qty_ord"),
    "qty_shipped": ("qty_shipped", "quantity_shipped", "quantityShipped", "shipped",
                    "qty", "quantity", "qty_ship"),
    "qty_backordered": ("qty_backordered", "quantity_backordered", "quantityBackOrdered",
                        "backordered", "back_ordered", "bo", "qty_bo"),
    "list_price": ("list_price", "listPrice", "list", "unit_list", "retail"),
    "discount_pct": ("discount_pct", "discount_percent", "discountPercent", "discount",
                     "disc", "disc_pct"),
    "net_price": ("net_price", "netPrice", "net", "unit_price", "unitPrice", "price",
                  "unit_cost", "cost"),
    "extension": ("extension", "ext", "extended", "extended_price", "amount",
                  "line_total", "lineTotal", "total"),
}

# Tolerances, all in dollars.
#   * a single line may round by a cent or two
#   * the merchandise total may absorb one cent of rounding per line
_LINE_TOLERANCE = Decimal("0.02")
_DEFAULT_TOLERANCE = Decimal("0.05")
_PER_LINE_ROUNDING = Decimal("0.01")

_CENTS = Decimal("0.01")


# ── parsing ──────────────────────────────────────────────────────────────────


def money(value: Any) -> Decimal | None:
    """Parse a money-ish value. Handles `$1,234.56`, `(12.34)`, `12.34-`, `12.34CR`."""

    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))

    text = str(value).strip()
    if not text:
        return None

    negative = False
    if text.startswith("(") and text.endswith(")"):
        negative, text = True, text[1:-1].strip()
    if text[-2:].upper() == "CR":
        negative, text = True, text[:-2].strip()
    if text.endswith("-"):
        negative, text = True, text[:-1].strip()
    if text.startswith("-"):
        negative, text = True, text[1:].strip()

    text = re.sub(r"[^0-9.]", "", text)
    if not text or text.count(".") > 1:
        return None
    try:
        parsed = Decimal(text)
    except InvalidOperation:
        return None
    return -parsed if negative else parsed


def quantity(value: Any) -> int | None:
    """Parse a quantity. Accepts `12`, `12.00`, `1,200`; rejects fractional units."""

    parsed = money(value)
    if parsed is None:
        return None
    if parsed != parsed.to_integral_value():
        return None
    return int(parsed)


def percent(value: Any) -> Decimal | None:
    if value is None:
        return None
    text = str(value).replace("%", "")
    return money(text)


def _pick(raw: dict[str, Any], field: str) -> Any:
    for alias in _ALIASES[field]:
        if alias in raw and raw[alias] not in (None, ""):
            return raw[alias]
    return None


def _text(value: Any) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(str(value).split())
    return cleaned or None


def _f(value: Decimal | None) -> float | None:
    """Decimal → JSON-safe float, at cent precision."""

    return None if value is None else float(value.quantize(_CENTS))


# ── normalisation ────────────────────────────────────────────────────────────


def normalise_lines(raw_lines: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Coerce agent-supplied lines into the canonical shape.

    Returns `(lines, issues)`. Missing money is **derived only when the
    arithmetic is unambiguous** (extension from qty×net, or net from
    extension÷qty) and every derivation is recorded on the line's `derived`
    list — a derived number is not independent evidence, so the reconciler
    knows not to count it as a passing check.
    """

    if not isinstance(raw_lines, list) or not raw_lines:
        return [], [{"code": "no_lines", "message": "`lines` must be a non-empty list."}]

    lines: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    for index, raw in enumerate(raw_lines):
        if not isinstance(raw, dict):
            issues.append({
                "code": "bad_line",
                "line": index + 1,
                "message": f"Line {index + 1} is not an object.",
            })
            continue

        line: dict[str, Any] = {field: None for field in _CANONICAL_FIELDS}
        line["item"] = _text(_pick(raw, "item"))
        line["upc"] = _text(_pick(raw, "upc"))
        line["description"] = _text(_pick(raw, "description"))
        line["size"] = _text(_pick(raw, "size"))
        line["color"] = _text(_pick(raw, "color"))
        line["unit"] = _text(_pick(raw, "unit"))

        qty_shipped = quantity(_pick(raw, "qty_shipped"))
        qty_ordered = quantity(_pick(raw, "qty_ordered"))
        net_price = money(_pick(raw, "net_price"))
        extension = money(_pick(raw, "extension"))
        derived: list[str] = []

        # Derive the one missing leg of qty × net = extension, when the other two
        # are present. Never derive a quantity — a wrong quantity is the failure
        # mode this whole path exists to catch.
        if extension is None and qty_shipped is not None and net_price is not None:
            extension = (Decimal(qty_shipped) * net_price).quantize(_CENTS)
            derived.append("extension")
        elif net_price is None and extension is not None and qty_shipped:
            net_price = (extension / Decimal(qty_shipped)).quantize(_CENTS)
            derived.append("net_price")

        line["qty_shipped"] = qty_shipped
        line["qty_ordered"] = qty_ordered if qty_ordered is not None else qty_shipped
        line["qty_backordered"] = quantity(_pick(raw, "qty_backordered"))
        line["list_price"] = _f(money(_pick(raw, "list_price")))
        line["discount_pct"] = _f(percent(_pick(raw, "discount_pct")))
        line["net_price"] = _f(net_price)
        line["extension"] = _f(extension)
        if derived:
            line["derived"] = derived

        missing = [
            name for name, value in (
                ("qty_shipped", qty_shipped),
                ("net_price", net_price),
                ("extension", extension),
            ) if value is None
        ]
        if missing:
            issues.append({
                "code": "missing_fields",
                "line": index + 1,
                "item": line["item"],
                "message": (
                    f"Line {index + 1} ({line['item'] or 'unidentified'}) is missing "
                    + ", ".join(missing)
                    + " — it cannot be verified. Re-read that row, or escalate."
                ),
            })

        lines.append(line)

    return lines, issues


# ── reconciliation ───────────────────────────────────────────────────────────


def _charge_sum(charges: dict[str, Any]) -> Decimal | None:
    """Reassemble docTotal's non-merchandise half.

    docTotal = merchandise + siUpcharge + svcHandle + freight + salesTax
               + exciseTax - discount - freightAllowance
    """

    positives = ("si_upcharge", "svc_handle", "freight", "sales_tax", "excise_tax")
    negatives = ("discount", "freight_allowance")
    total = Decimal("0")
    seen = False
    for key in positives:
        value = money(charges.get(key))
        if value is not None:
            total += value
            seen = True
    for key in negatives:
        value = money(charges.get(key))
        if value is not None:
            total -= value
            seen = True
    return total if seen else None


def reconcile(
    invoice: dict[str, Any],
    raw_lines: Any,
    *,
    tolerance: Any = None,
) -> dict[str, Any]:
    """Check agent-extracted lines against the API's authoritative header money.

    `invoice` is a normalised invoice from `sportslink.list`/`get` — the header
    must come from the API, never from the PDF the agent just read, or the check
    verifies nothing.

    Returns the invoice with `lines` filled in, plus a `reconciliation` block and
    a top-level `status` of `verified` or `needs_review`.
    """

    abs_tolerance = money(tolerance) if tolerance is not None else _DEFAULT_TOLERANCE
    if abs_tolerance is None or abs_tolerance < 0:
        raise ValueError("`tolerance` must be a non-negative number of dollars.")

    lines, issues = normalise_lines(raw_lines)
    charges = invoice.get("charges") or {}

    merchandise = money(charges.get("merchandise"))
    doc_total = money(invoice.get("total"))
    other_charges = _charge_sum(charges)

    extensions = [money(line.get("extension")) for line in lines]
    have_all_extensions = lines and all(value is not None for value in extensions)
    lines_sum = sum((value for value in extensions if value is not None), Decimal("0"))

    checks: list[dict[str, Any]] = []

    # 1. Per-line arithmetic. A line whose extension we derived ourselves passes
    #    trivially, so it is reported as `derived`, not as a passing check.
    line_failures = 0
    for index, line in enumerate(lines, start=1):
        qty = line.get("qty_shipped")
        net = money(line.get("net_price"))
        ext = money(line.get("extension"))
        if qty is None or net is None or ext is None:
            continue
        if "extension" in (line.get("derived") or []) or "net_price" in (line.get("derived") or []):
            continue
        variance = (Decimal(qty) * net - ext).copy_abs()
        if variance > _LINE_TOLERANCE:
            line_failures += 1
            issues.append({
                "code": "line_math_variance",
                "line": index,
                "item": line.get("item"),
                "message": (
                    f"Line {index} ({line.get('item') or 'unidentified'}): "
                    f"{qty} × {net} = {(Decimal(qty) * net).quantize(_CENTS)}, but the "
                    f"extension reads {ext.quantize(_CENTS)} "
                    f"(off by {variance.quantize(_CENTS)})."
                ),
            })
    checks.append({
        "check": "line_math",
        "passed": line_failures == 0,
        "failed_lines": line_failures,
    })

    # 2. The anchor check: extensions must sum to the merchandise total. When the
    #    header has no merchandiseTotal (an OCR gap — SportsLink simply omits
    #    fields it doesn't have), fall back to reassembling docTotal.
    anchor = None
    if merchandise is not None:
        anchor = "merchandise"
        allowance = max(abs_tolerance, _PER_LINE_ROUNDING * len(lines))
        variance = (lines_sum - merchandise).copy_abs()
        passed = have_all_extensions and variance <= allowance
        checks.append({
            "check": "merchandise_total",
            "passed": bool(passed),
            "lines_sum": _f(lines_sum),
            "expected": _f(merchandise),
            "variance": _f(variance),
            "allowance": _f(allowance),
        })
        if not passed:
            issues.append({
                "code": "merchandise_variance",
                "message": (
                    f"Extracted lines sum to {lines_sum.quantize(_CENTS)}, but SportsLink "
                    f"reports a merchandise total of {merchandise.quantize(_CENTS)} "
                    f"(off by {variance.quantize(_CENTS)}, allowance "
                    f"{allowance.quantize(_CENTS)}). A line is missing, doubled, or misread."
                ) if have_all_extensions else (
                    "Not every line has an extension, so the merchandise total cannot "
                    "be checked."
                ),
            })
    elif doc_total is not None and other_charges is not None:
        anchor = "doc_total"
        implied = doc_total - other_charges
        allowance = max(abs_tolerance, _PER_LINE_ROUNDING * len(lines))
        variance = (lines_sum - implied).copy_abs()
        passed = have_all_extensions and variance <= allowance
        checks.append({
            "check": "doc_total_reassembly",
            "passed": bool(passed),
            "lines_sum": _f(lines_sum),
            "expected": _f(implied),
            "variance": _f(variance),
            "allowance": _f(allowance),
        })
        if not passed:
            issues.append({
                "code": "doc_total_variance",
                "message": (
                    f"The header has no merchandise total, so lines were checked against "
                    f"docTotal minus charges = {implied.quantize(_CENTS)}; the extracted "
                    f"lines sum to {lines_sum.quantize(_CENTS)} (off by "
                    f"{variance.quantize(_CENTS)})."
                ),
            })
    else:
        issues.append({
            "code": "no_anchor_total",
            "message": (
                "The SportsLink header carries neither a merchandise total nor enough "
                "of docTotal + charges to check the extracted lines against. Nothing "
                "can be verified — escalate this document."
            ),
        })

    # 3. Informational: does docTotal reassemble from the extracted lines? Never
    #    the deciding check (charge fields go missing on OCR docs), but a mismatch
    #    here alongside a clean merchandise check usually means a charge was
    #    dropped, which is worth showing a reviewer.
    if doc_total is not None and other_charges is not None and have_all_extensions:
        implied_total = lines_sum + other_charges
        checks.append({
            "check": "doc_total_informational",
            "passed": bool((implied_total - doc_total).copy_abs() <= max(abs_tolerance, _PER_LINE_ROUNDING * len(lines))),
            "implied_total": _f(implied_total),
            "doc_total": _f(doc_total),
            "variance": _f((implied_total - doc_total).copy_abs()),
        })

    blocking = {
        "no_lines", "bad_line", "missing_fields", "line_math_variance",
        "merchandise_variance", "doc_total_variance", "no_anchor_total",
    }
    status = "needs_review" if any(i["code"] in blocking for i in issues) else "verified"

    result = dict(invoice)
    result["lines"] = lines
    result["has_lines"] = bool(lines)
    result["lines_source"] = "pdf"
    result["status"] = status
    result["reconciliation"] = {
        "status": status,
        "anchor": anchor,
        "line_count": len(lines),
        "lines_sum": _f(lines_sum),
        "tolerance": _f(abs_tolerance),
        "checks": checks,
        "issues": issues,
    }

    if status == "verified":
        result["next_step"] = (
            "Lines tie to the SportsLink header. Hand this invoice to the payables "
            "workflow exactly like an EDI one, and mark-historical only after the "
            "bill is created."
        )
    else:
        result["next_step"] = (
            "Lines do NOT tie to the SportsLink header — do not bill from them. "
            "Leave the SI document active and escalate with the issues below. "
            "Re-reading the PDF and re-running is fine; overriding the check is not."
        )

    if invoice.get("is_credit"):
        result["next_step"] = (
            "This document is a CREDIT MEMO — never create it as a payable, whatever "
            "the reconciliation says. " + result["next_step"]
        )

    return result


__all__ = ("money", "normalise_lines", "quantity", "reconcile")
