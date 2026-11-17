#!/usr/bin/env python3
"""Offline correctness tests for the header-only PDF fallback.

No network and no portal: PDFs are generated in-process (reportlab when it is
available, otherwise a hand-built minimal PDF) and the SportsLink header is a
literal. Exercises the two halves the agent's reading sits between —
`invoice_pdf` (bytes → readable) and `invoice_lines` (extracted lines → checked
invoice) — with particular attention to the cases that must NOT come back
`verified`.

    python3 scripts/_selftest.py

Exits non-zero on the first failed assertion. `pypdf` is required; reportlab is
optional (its tests are skipped with a note when it is missing).
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from invoice_lines import money, normalise_lines, quantity, reconcile  # noqa: E402
from invoice_pdf import extract_text, prepare  # noqa: E402

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas as _canvas
except ImportError:  # pragma: no cover — optional
    _canvas = None


# --- fixtures --------------------------------------------------------------

# A header exactly as `sportslink._normalise` emits it for a scanned document:
# money present, `lines` empty, `has_lines` false.
HEADER = {
    "source": "sports_inc",
    "po_number": "P09409",
    "si_doc_number": 23962348,
    "invoice_number": "6164920830",
    "invoice_date": "2026-02-16",
    "due_date": "2026-05-10",
    "supplier": "Acme Athletic",
    "is_credit": False,
    "has_lines": False,
    "total": 60.06,
    "charges": {
        "merchandise": 51.00,
        "freight": 8.58,
        "freight_allowance": None,
        "si_upcharge": 0.48,
        "svc_handle": None,
        "sales_tax": None,
        "excise_tax": None,
        "discount": None,
    },
    "lines": [],
}

# 12.75 × 1 + 12.75 × 3 = 51.00 — ties to HEADER's merchandise total.
GOOD_LINES = [
    {"item": "JP1477", "upc": "197612326076", "size": "S", "qty_shipped": 1,
     "net_price": 12.75, "extension": 12.75, "description": "TF SHRT TIGHT M BLACK"},
    {"item": "JP1477", "upc": "197612326083", "size": "M", "qty_shipped": 3,
     "net_price": 12.75, "extension": 38.25, "description": "TF SHRT TIGHT M BLACK"},
]


def _text_pdf() -> bytes:
    """A PDF with a real text layer, laid out like a scanned invoice's columns."""

    import io

    buffer = io.BytesIO()
    pdf = _canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 10)
    rows = [
        "ACME ATHLETIC — INVOICE 6164920830",
        "PO P09409                      Date 02/16/2026",
        "",
        "ITEM      UPC            SIZE  QTY   NET     EXT",
        "JP1477    197612326076   S     1     12.75   12.75",
        "JP1477    197612326083   M     3     12.75   38.25",
        "",
        "Merchandise 51.00   Freight 8.58   Upcharge 0.48   TOTAL 60.06",
    ]
    y = 720
    for row in rows:
        pdf.drawString(60, y, row)
        y -= 16
    pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def _si_download_pdf() -> bytes:
    """A two-document Sports Inc download, shaped like the real thing.

    Landscape SI cover page (native text, no line detail, "SEE VENDOR INVOICE FOR
    DETAIL") followed by a portrait *scan* of the vendor invoice — twice, one
    pair per SI document. The scanned pages are drawn as embedded images with no
    text, exactly like the 300dpi scans Sports Inc bundles.
    """

    import io

    from reportlab.lib.utils import ImageReader
    from PIL import Image, ImageDraw

    def _scan(invoice_no: str) -> ImageReader:
        img = Image.new("RGB", (1240, 1754), "white")
        draw = ImageDraw.Draw(img)
        draw.text((80, 80), f"CHAMPRO  INVOICE #: {invoice_no}", fill="black")
        draw.text((80, 120), "SKU  COLOR  SIZE  ORDERED  SHIPPED  UNIT  TOTAL", fill="black")
        return ImageReader(img)

    buffer = io.BytesIO()
    pdf = _canvas.Canvas(buffer)
    for si_doc, supplier_doc, merch in (("24682750", "SI3503366", "05.19"),
                                        ("24684277", "SI3503509", "398.40")):
        pdf.setPageSize((792, 612))  # landscape — the SI cover
        pdf.setFont("Helvetica", 9)
        for offset, row in enumerate((
            "SPORTS, INC.   SI STORE:   PO NUMBER:",
            "SUPPLIER INFORMATION   DOCUMENT NUMBER   DOCUMENT DATE",
            "MERCHANDISE TOTAL   SALES TAX   FREIGHT CHARGE",
            "SI DOCUMENT NUMBER:   DOCUMENT DATE:   DUE DATE:   SI UPCHARGE",
            "SEE VENDOR INVOICE FOR DETAIL.",
            "BACON & COMPANY INC   P13554",
            supplier_doc,
            si_doc,
            merch,
        )):
            pdf.drawString(50, 550 - offset * 16, row)
        pdf.showPage()

        pdf.setPageSize((595.2, 842.15))  # portrait — the scanned vendor invoice
        pdf.drawImage(_scan(supplier_doc), 0, 0, width=595.2, height=842.15)
        pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def _image_only_pdf() -> bytes:
    """A one-page PDF whose only content is a scanned image — no text at all."""

    import io

    from reportlab.lib.utils import ImageReader
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (1240, 1754), "white")
    ImageDraw.Draw(img).rectangle((80, 80, 1160, 400), outline="black")
    buffer = io.BytesIO()
    pdf = _canvas.Canvas(buffer, pagesize=letter)
    pdf.drawImage(ImageReader(img), 0, 0, width=612, height=792)
    pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def _issue_codes(result: dict) -> set[str]:
    return {issue["code"] for issue in result["reconciliation"]["issues"]}


# --- money / quantity parsing ----------------------------------------------


def test_money_parsing() -> None:
    assert money("$1,234.56") == money(1234.56)
    assert money("(12.34)") == money(-12.34)
    assert money("12.34-") == money(-12.34)
    assert money("12.34CR") == money(-12.34)
    assert money("") is None and money(None) is None and money("n/a") is None
    assert quantity("1,200") == 1200
    assert quantity("12.00") == 12
    assert quantity("2.5") is None  # a fractional "quantity" is a misread
    print("PASS test_money_parsing")


def test_alias_normalisation() -> None:
    lines, issues = normalise_lines([
        {"style": "JP1477", "quantity": "3", "unit_price": "$12.75", "amount": "38.25"}
    ])
    assert not issues, issues
    line = lines[0]
    assert line["item"] == "JP1477"
    assert line["qty_shipped"] == 3 and line["qty_ordered"] == 3
    assert line["net_price"] == 12.75 and line["extension"] == 38.25
    print("PASS test_alias_normalisation")


def test_derivation_is_recorded() -> None:
    lines, issues = normalise_lines([{"item": "X", "qty_shipped": 4, "net_price": 2.5}])
    assert not issues, issues
    assert lines[0]["extension"] == 10.0
    assert lines[0]["derived"] == ["extension"]  # derived ⇒ not independent evidence
    print("PASS test_derivation_is_recorded")


# --- reconciliation: the checks that must fail ------------------------------


def test_clean_lines_verify() -> None:
    result = reconcile(HEADER, GOOD_LINES)
    assert result["status"] == "verified", result["reconciliation"]
    assert result["has_lines"] is True and result["lines_source"] == "pdf"
    assert result["reconciliation"]["anchor"] == "merchandise"
    assert result["reconciliation"]["lines_sum"] == 51.00
    # The invoice keeps the shape the payables workflow already consumes.
    assert set(GOOD_LINES[0]) <= set(result["lines"][0])
    print("PASS test_clean_lines_verify")


def test_missing_line_is_caught() -> None:
    result = reconcile(HEADER, GOOD_LINES[:1])  # one of two lines misread away
    assert result["status"] == "needs_review"
    assert "merchandise_variance" in _issue_codes(result)
    print("PASS test_missing_line_is_caught")


def test_misread_quantity_is_caught() -> None:
    bad = [dict(GOOD_LINES[0]), dict(GOOD_LINES[1], qty_shipped=8)]  # 3 read as 8
    result = reconcile(HEADER, bad)
    assert result["status"] == "needs_review"
    # Both the per-line math and the total disagree — either alone is enough.
    assert "line_math_variance" in _issue_codes(result)
    print("PASS test_misread_quantity_is_caught")


def test_transposed_price_is_caught() -> None:
    bad = [dict(GOOD_LINES[0], net_price=21.75, extension=21.75), dict(GOOD_LINES[1])]
    result = reconcile(HEADER, bad)
    assert result["status"] == "needs_review"
    assert "merchandise_variance" in _issue_codes(result)
    print("PASS test_transposed_price_is_caught")


def test_incomplete_line_is_caught() -> None:
    bad = [dict(GOOD_LINES[0]), {"item": "JP1477", "size": "M"}]  # no qty, no money
    result = reconcile(HEADER, bad)
    assert result["status"] == "needs_review"
    assert "missing_fields" in _issue_codes(result)
    print("PASS test_incomplete_line_is_caught")


def test_no_lines_is_caught() -> None:
    result = reconcile(HEADER, [])
    assert result["status"] == "needs_review"
    assert "no_lines" in _issue_codes(result)
    print("PASS test_no_lines_is_caught")


def test_rounding_is_tolerated() -> None:
    # Two lines each a cent light: within the per-line rounding allowance.
    close = [dict(GOOD_LINES[0], net_price=12.745, extension=12.745),
             dict(GOOD_LINES[1], extension=38.245, net_price=12.7483)]
    result = reconcile(HEADER, close)
    assert result["status"] == "verified", result["reconciliation"]
    print("PASS test_rounding_is_tolerated")


def test_doc_total_fallback_anchor() -> None:
    # An OCR gap: no merchandise total, so lines are checked against
    # docTotal - charges = 60.06 - (8.58 + 0.48) = 51.00.
    header = dict(HEADER, charges=dict(HEADER["charges"], merchandise=None))
    result = reconcile(header, GOOD_LINES)
    assert result["reconciliation"]["anchor"] == "doc_total"
    assert result["status"] == "verified", result["reconciliation"]

    short = reconcile(header, GOOD_LINES[:1])
    assert short["status"] == "needs_review"
    assert "doc_total_variance" in _issue_codes(short)
    print("PASS test_doc_total_fallback_anchor")


def test_no_anchor_at_all() -> None:
    header = dict(HEADER, total=None, charges={k: None for k in HEADER["charges"]})
    result = reconcile(header, GOOD_LINES)
    assert result["status"] == "needs_review"
    assert "no_anchor_total" in _issue_codes(result)
    print("PASS test_no_anchor_at_all")


def test_credit_memo_is_flagged() -> None:
    header = dict(HEADER, is_credit=True, total=-60.06,
                  charges=dict(HEADER["charges"], merchandise=-51.00))
    credit_lines = [dict(line, net_price=-line["net_price"], extension=-line["extension"])
                    for line in GOOD_LINES]
    result = reconcile(header, credit_lines)
    assert result["status"] == "verified", result["reconciliation"]
    assert result["next_step"].startswith("This document is a CREDIT MEMO")
    print("PASS test_credit_memo_is_flagged")


# --- PDF handling -----------------------------------------------------------


def test_image_only_pdf_is_extracted() -> None:
    if _canvas is None:  # pragma: no cover — optional dependency
        print("SKIP test_image_only_pdf_is_extracted (reportlab not installed)")
        return
    prepared = prepare(_image_only_pdf(), label="23962348", stash="auto")
    assert prepared["has_text_layer"] is False
    assert prepared["text"] == ""
    assert prepared["pages"][0]["kind"] == "image"
    # The page image is written out, because a PDF the agent cannot render is
    # not readable — and the PDF is kept as a fallback.
    assert len(prepared["image_paths"]) == 1
    assert os.path.isfile(prepared["image_paths"][0])
    assert prepared["pdf_path"] and os.path.isfile(prepared["pdf_path"])
    assert "SCANNED" in prepared["next_step"]

    never = prepare(_image_only_pdf(), label="23962348", stash="never")
    assert never["pdf_path"] is None and never["image_paths"] == []
    assert "stashing disabled" in never["next_step"]
    print("PASS test_image_only_pdf_is_extracted")


def test_text_pdf_stays_in_memory() -> None:
    if _canvas is None:  # pragma: no cover — optional dependency
        print("SKIP test_text_pdf_stays_in_memory (reportlab not installed)")
        return
    pdf_bytes = _text_pdf()
    extracted = extract_text(pdf_bytes)
    assert extracted["has_text_layer"] is True
    assert "JP1477" in extracted["text"] and "38.25" in extracted["text"]
    assert "----- page 1 of 1 -----" in extracted["text"]

    prepared = prepare(pdf_bytes, label="23962348", stash="auto")
    assert prepared["text_covers_all_pages"] is True
    assert prepared["pdf_path"] is None  # every page readable ⇒ nothing on disk
    assert prepared["image_paths"] == []
    assert "reconcile-lines" in prepared["next_step"]

    both = prepare(pdf_bytes, label="23962348", stash="always")
    assert both["pdf_path"] and os.path.isfile(both["pdf_path"])
    print("PASS test_text_pdf_stays_in_memory")


def test_si_download_is_segmented() -> None:
    """The real download shape: SI cover + scanned vendor invoice, twice.

    Regression guard for the failure this structure caused: judging the text
    layer over the whole file returns a healthy character count made entirely of
    SI cover boilerplate, so the document looks readable while containing no line
    detail at all, and nothing gets written for the agent to look at.
    """

    if _canvas is None:  # pragma: no cover — optional dependency
        print("SKIP test_si_download_is_segmented (reportlab not installed)")
        return

    prepared = prepare(_si_download_pdf(), label="24682750", stash="auto")

    assert prepared["page_count"] == 4
    assert [page["kind"] for page in prepared["pages"]] == [
        "si_cover", "image", "si_cover", "image"
    ]
    # The whole-file verdict is true, but it does NOT cover every page — which is
    # the distinction that keeps the scans from being silently skipped.
    assert prepared["has_text_layer"] is True
    assert prepared["text_covers_all_pages"] is False
    assert prepared["image_pages"] == [2, 4]

    # Both scans were extracted for the agent to read, and the PDF kept as backup.
    assert len(prepared["image_paths"]) == 2
    assert all(os.path.isfile(path) for path in prepared["image_paths"])
    assert prepared["pdf_path"] and os.path.isfile(prepared["pdf_path"])
    assert "SCANNED" in prepared["next_step"]

    # Two documents, each a cover page plus its scanned detail page.
    documents = prepared["documents"]
    assert len(documents) == 2
    assert [doc["si_cover_page"] for doc in documents] == [1, 3]
    assert [doc["detail_pages"] for doc in documents] == [[2], [4]]
    assert all(doc["detail_is_scanned"] for doc in documents)
    assert 24682750 in documents[0]["si_doc_number_candidates"]
    assert 24684277 in documents[1]["si_doc_number_candidates"]
    # The supplier's own document number is captured separately, not mistaken for
    # an SI document number.
    assert documents[0]["supplier_doc_candidates"] == ["SI3503366"]
    assert 3503366 not in documents[0]["si_doc_number_candidates"]
    print("PASS test_si_download_is_segmented")


# --- OCR: layout reconstruction (pure, no engine needed) ---------------------


def test_ocr_layout_preserves_columns() -> None:
    """An invoice line is a row across columns, and must survive as one.

    OCR engines return word boxes, not lines. Reading them in raw order turns
    `80  $2.29  $183.20` into three unrelated numbers on three lines, which is
    unextractable. Boxes are therefore grouped by vertical position and padded
    by horizontal position, so the text still looks like the table it came from.
    """

    from ocr import layout_text

    def box(text, x, y, conf=0.99, h=20):
        return {"text": text, "confidence": conf,
                "x0": x, "x1": x + len(text) * 11, "y0": y, "y1": y + h}

    # Deliberately out of reading order, and with the second row's boxes
    # interleaved — the grouping must not depend on input order.
    boxes = [
        box("$183.20", 1064, 656), box("A062RY", 60, 662), box("80EA", 621, 656),
        box("$2.29", 968, 655), box("ROYAL", 214, 662), box("Adult1-1/2\"", 452, 659),
        box("AS1RY-L", 59, 707), box("$215.20", 1064, 704),
        box("80PR", 620, 702, conf=0.62),  # a shaky read
        box("$2.69", 967, 703),
    ]

    text, rows = layout_text(boxes)
    lines = text.splitlines()
    assert len(lines) == 2, f"expected two rows, got {len(lines)}: {lines}"

    # Row one reads left to right, columns intact.
    assert lines[0].split() == ["A062RY", "ROYAL", 'Adult1-1/2"', "80EA", "$2.29", "$183.20"]
    assert lines[1].split() == ["AS1RY-L", "80PR", "$2.69", "$215.20"]
    # Columns are padded, not collapsed — the extension stays on the right.
    assert lines[0].index("$183.20") > lines[0].index("$2.29") > lines[0].index("80EA")

    # A row is only as trustworthy as its worst token, and that travels with it.
    assert rows[0]["confidence"] == 0.99
    assert rows[1]["confidence"] == 0.62
    print("PASS test_ocr_layout_preserves_columns")


def test_ocr_flags_only_shaky_numbers() -> None:
    """Confidence flagging must follow what reconciliation consumes.

    On a real Champro scan the money read at 1.00 while whole rows scored 0.68 —
    dragged down by `0EA`, `OPR` and `$O`, the backorder and freight zeros that
    nothing downstream uses. Flagging on the worst token of any kind marks every
    line item on every invoice as suspect, and an alarm that always fires is the
    same as no alarm: the agent opens the image every time and OCR-first buys
    nothing.
    """

    from ocr import is_value_token, layout_text

    # Words are not value-bearing, however badly they are read.
    for word in ("ROYAL", "Pro Sock", "Subtotal:", "MVP Belt", "CHAMPRO"):
        assert is_value_token(word) is False, word
    # Anything carrying a number is, including misreads that ate the digit:
    # `$O` for `$0`, `OPR` for `0 PR`.
    for value in ("$183.20", "80EA", "0EA", "$O", "OPR", "A062RY", '80 PR'):
        assert is_value_token(value) is True, value

    def box(text, x, conf):
        return {"text": text, "confidence": conf,
                "x0": x, "x1": x + len(text) * 11, "y0": 100, "y1": 120}

    # A line whose money is certain and whose colour is not: not worth opening
    # the image for.
    _, rows = layout_text([
        box("A062RY", 60, 1.00), box("ROYAL", 214, 0.41),
        box("80EA", 620, 0.99), box("$2.29", 968, 1.00), box("$183.20", 1064, 1.00),
    ])
    assert rows[0]["confidence"] == 0.41          # the row's worst token overall
    assert rows[0]["value_confidence"] == 0.99    # but its numbers are solid
    assert "weakest_value" not in rows[0]

    # The reverse: confident words, one doubtful number. This one must flag,
    # and must name the token so the agent knows where to look.
    _, rows = layout_text([
        box("A062RY", 60, 1.00), box("ROYAL", 214, 1.00),
        box("80EA", 620, 0.99), box("$2.29", 968, 1.00), box("$183.20", 1064, 0.44),
    ])
    assert rows[0]["value_confidence"] == 0.44
    assert rows[0]["weakest_value"] == "$183.20"
    print("PASS test_ocr_flags_only_shaky_numbers")


def test_ocr_engine_selection() -> None:
    """`off` and unknown engines must fail loudly, not silently skip OCR."""

    import ocr

    for value in ("off", "definitely-not-an-engine"):
        try:
            ocr._select(value)
        except ocr.OcrUnavailable as exc:
            assert value in str(exc) or "disabled" in str(exc)
        else:  # pragma: no cover
            raise AssertionError(f"expected OcrUnavailable for {value!r}")

    assert ocr.layout_text([]) == ("", [])
    print("PASS test_ocr_engine_selection")


# --- portal driver: the parts that need no browser ---------------------------


def test_row_matching() -> None:
    """Narrowing a PO's rows to one document, the way the Invoice Center shows them."""

    import sportsweb_browser as portal

    rows = [
        {"row_index": 0, "Supplier": "CHAMPRO SPORTS", "Supplier Doc No.": "SI3503366",
         "PO No.": "P13554", "SI Doc No.": "24682750", "Total": "$5.23"},
        {"row_index": 1, "Supplier": "CHAMPRO SPORTS", "Supplier Doc No.": "SI3503509",
         "PO No.": "P13554", "SI Doc No.": "24684277", "Total": "$401.59"},
    ]

    # No document named → the whole PO (one combined download).
    assert portal._match_rows(rows, None, None) == rows

    # By SI doc number, int or str.
    assert [r["row_index"] for r in portal._match_rows(rows, 24684277, None)] == [1]
    assert [r["row_index"] for r in portal._match_rows(rows, "24682750", None)] == [0]

    # The supplier's own number is punctuated differently on the vendor invoice
    # (SI-3503366) than in the portal column (SI3503366) — match on digits.
    assert [r["row_index"] for r in portal._match_rows(rows, None, "SI-3503509")] == [1]

    # A document that isn't there matches nothing, rather than falling back to
    # the first row — reading the wrong invoice is the failure mode that
    # reconciliation cannot catch.
    assert portal._match_rows(rows, 99999999, None) == []
    print("PASS test_row_matching")


def test_cloned_header_guard() -> None:
    """The grid clones its `<thead>` into body cells — a leak must not be parsed.

    The Invoice Center's frozen-header script duplicates the entire header row
    inside individual `<td>`s, so a naive `textContent` read of the PO cell
    returns every column heading followed by "P13554". Reading a row key off
    that would select the wrong invoice, which reconciliation cannot catch, so a
    leak is rejected rather than trimmed.
    """

    import sportsweb_browser as portal

    leaked = (
        "Supplier Supplier Doc No. PO No. SI Doc No. SI Doc Date Due Date "
        "Archived Date Discount Date Total P13554"
    )
    assert portal.looks_like_cloned_header(leaked) is True
    assert portal.looks_like_cloned_header("P13554") is False
    assert portal.looks_like_cloned_header("24682750") is False
    assert portal.looks_like_cloned_header("CHAMPRO SPORTS") is False
    assert portal.looks_like_cloned_header("") is False
    assert portal.looks_like_cloned_header(None) is False
    print("PASS test_cloned_header_guard")


def test_download_formats() -> None:
    """Downloading is two clicks — the dialog's options must all be addressable."""

    import sportsweb_browser as portal

    assert portal.DOWNLOAD_FORMATS["pdf"].endswith("lbPDFPrint']")  # one merged PDF
    assert set(portal.DOWNLOAD_FORMATS) == {
        "pdf", "pdf_zip", "csv", "csv_items", "pdf_and_csv"
    }
    # Every option is matched on its control-name suffix, never the generated
    # `ctl00$ContentPlaceHolder1$` prefix.
    assert all(
        selector.startswith("a[id$='") for selector in portal.DOWNLOAD_FORMATS.values()
    )
    print("PASS test_download_formats")


def test_multi_page_merge() -> None:
    """Rows spanning grid pages download per page and stitch back together.

    Selection does not survive paging — the pager is a postback that re-renders
    the grid — so a PO whose invoices span pages must be fetched a page at a
    time. Merging keeps that invisible downstream: `prepare()` segments the
    combined file exactly as it does a single-page download.
    """

    if _canvas is None:  # pragma: no cover — optional dependency
        print("SKIP test_multi_page_merge (reportlab not installed)")
        return

    from invoice_pdf import merge_pdfs

    # Two separate downloads, each a cover + scan pair, as two grid pages would
    # produce.
    part_one = _si_download_pdf()
    part_two = _si_download_pdf()

    merged = merge_pdfs([part_one, part_two])
    assert merged[:5] == b"%PDF-"

    prepared = prepare(merged, label="merged", stash="never", ocr="off")
    # Each part carries two documents, so the merge must yield four.
    assert prepared["page_count"] == 8
    assert len(prepared["documents"]) == 4, prepared["documents"]
    assert [page["kind"] for page in prepared["pages"]] == [
        "si_cover", "image", "si_cover", "image",
        "si_cover", "image", "si_cover", "image",
    ]

    # A single part is returned untouched rather than rewritten.
    assert merge_pdfs([part_one]) is part_one
    try:
        merge_pdfs([])
    except Exception as exc:  # noqa: BLE001 — PdfError is module-private
        assert "No PDF parts" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected an error when merging nothing")
    print("PASS test_multi_page_merge")


def test_paging_reads_every_page() -> None:
    """A PO larger than one page must not silently return a subset.

    Page 1 alone cannot distinguish "this document is not here" from "this
    document is on page 3", and reporting the first as if it were true is how a
    real invoice goes unbilled.
    """

    import inspect

    import sportsweb_browser as portal

    source = inspect.getsource(portal._fetch)

    # A whole-PO fetch covers every page even when page 1 already matched —
    # otherwise it bills a subset of the PO.
    assert "read_all_rows()" in source
    assert "si_doc_number is None" in source
    # For a single document, narrowing by SI Doc No. beats walking pages.
    assert 'driver.search_in_grid(si_doc_number, "si_doc")' in source
    # The archived fallback pages too.
    assert "driver.show_archived(search, column)" in source

    # Paging is driven by the portal's own state, not by counting links — the
    # pager is `display: none` on a single page.
    paging = inspect.getsource(portal.SportsWebDriver.goto_page)
    assert "page_position()" in paging
    assert "did not move off page" in paging  # progress is verified per hop
    print("PASS test_paging_reads_every_page")


def test_archived_search_columns() -> None:
    """Switching to Archived resets the results — the search must be re-run.

    The archived tab does not inherit the home screen's search, and its own
    search box is column-scoped: the dropdown defaults to
    `-- select search column --`, which matches nothing. Clicking the tab and
    re-reading rows (the original implementation) would read whatever the tab
    happens to show rather than the document that was asked for.
    """

    import sportsweb_browser as portal

    # The dropdown values are the portal's own column names, not display labels.
    assert portal.SEARCH_COLUMNS["po"] == "DealerPONum"
    assert portal.SEARCH_COLUMNS["si_doc"] == "ASWDocNum"
    assert portal.SEARCH_COLUMNS["supplier_doc"] == "SupplierDocNum"
    # `HistoricalDate` is hidden on Active and shown on Archived; it is mapped
    # either way so the caller never has to care which tab is up.
    assert portal.SEARCH_COLUMNS["archived_date"] == "HistoricalDate"

    # `show_archived` takes the search term precisely because the tab switch
    # loses it — a signature that could not express that would be the bug.
    import inspect

    params = inspect.signature(portal.SportsWebDriver.show_archived).parameters
    assert "search" in params and "column" in params
    assert params["column"].default == "po"
    print("PASS test_archived_search_columns")


def test_archived_fallback_is_automatic() -> None:
    """Active first, then Archived — with no flag from the caller.

    A caller usually cannot know which tab a document is on: "archived" means
    Sports Inc marked it historical, which this skill does *after* billing, so
    the state depends on history the caller may not have. Requiring a flag would
    mean guessing, and guessing wrong reads as "not found".
    """

    import inspect

    import sportsweb_browser as portal

    source = inspect.getsource(portal._fetch)
    # The fallback is unconditional on caller input: it is driven by the Active
    # search coming back empty, not by an argument.
    assert "if not wanted:" in source
    assert "driver.show_archived(search, column)" in source
    assert 'tab = "archived"' in source
    # No `archived` parameter on the fetch path at all — that flag exists only
    # on the capture-portal diagnostic, for deliberately exercising the branch.
    assert "archived" not in inspect.signature(portal.fetch_invoice_pdf).parameters
    assert "archived" in inspect.signature(portal.capture_portal).parameters

    # Which tab served the document is reported, because finding it on Archived
    # is a duplicate-payment tell rather than a routing detail.
    assert '"tab": tab' in source
    print("PASS test_archived_fallback_is_automatic")


def test_portal_credentials_guard() -> None:
    import sportsweb_browser as portal

    for key in ("SPORTSINC_WEB_USERNAME", "SPORTSINC_WEB_PASSWORD"):
        os.environ.pop(key, None)
    try:
        portal.credentials()
    except portal.SportsWebConfigError as exc:
        assert exc.error_type == "config_error"
        assert "never ask for them in chat" in str(exc).lower()
    else:  # pragma: no cover
        raise AssertionError("expected a config error when credentials are absent")

    resolved = portal.credentials({"username": "u@example.com", "password": "pw"})

    # Home and the Invoice Center are DIFFERENT hosts, confirmed from a live run:
    # login lands on swv3/home (the only page with a search box) and searching
    # crosses to swv2h. Conflating them sends every run through a full login,
    # because a session check pointed at swv2h can never find the search box.
    assert resolved["home_url"] == "https://swv3.sportsinc.com/home"
    assert resolved["base_url"] == "https://swv2h.sportsinc.com/"
    assert resolved["home_url"].split("/")[2] != resolved["base_url"].split("/")[2]

    # Login is entered by clicking through the public site; the redirect URL
    # itself 403s on a direct hit.
    assert portal.PUBLIC_SITE_URL == "https://www.sportsinc.us/"
    assert portal.LOGIN_ENTRY_URL == "https://swv3.sportsinc.com/login-redirect"
    print("PASS test_portal_credentials_guard")


def test_no_network_idle_waits() -> None:
    """No wait may depend on `networkidle`.

    The home screen is a Vue app that holds connections open, so that state can
    simply never arrive — and a long wait for an event that will never come is
    indistinguishable from a hang. This is the bug that made a live run look
    frozen, so it gets a guard rather than a comment.
    """

    import ast
    import pathlib

    source = pathlib.Path(__file__).with_name("sportsweb_browser.py").read_text()
    offenders = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call):
            continue
        called = getattr(node.func, "attr", None) or getattr(node.func, "id", None)
        if called != "wait_for_load_state":
            continue
        literals = [arg.value for arg in node.args if isinstance(arg, ast.Constant)]
        literals += [
            kw.value.value for kw in node.keywords if isinstance(kw.value, ast.Constant)
        ]
        if "networkidle" in literals:
            offenders.append(f"sportsweb_browser.py:{node.lineno}")
    assert not offenders, f"networkidle wait reintroduced at {offenders}"
    print("PASS test_no_network_idle_waits")


# --- the seam: a raw SportsLink payload straight through to a checked invoice --


def test_end_to_end_from_api_payload() -> None:
    """A scanned document as SportsLink actually returns it → normalise → reconcile.

    Guards the seam: `reconcile` must consume exactly what `sportslink._normalise`
    emits, so a PDF-extracted invoice is indistinguishable from an EDI one
    downstream. A raw payload (camelCase, no `lines`, omitted OCR fields) goes in;
    a billable invoice comes out.
    """

    import sportslink

    raw = {
        "poNumber": "P09409",
        "siDocNumber": 23962348,
        "siDocDate": "2026-02-16",
        "dueDate": "2026-05-10",
        "supplierDocNumber": "6164920830",
        "supplierDocDate": "2026-02-16",
        "supplier": "Acme Athletic",
        "isCredit": False,
        "merchandiseTotal": 51.00,
        "freightAmount": 8.58,
        "siUpcharge": 0.48,
        "docTotal": 60.06,
        # no `lines` key at all — this is the scanned/OCR case
    }

    class _FakeClient:
        def get_documents(self, _params):
            return {"items": [raw], "totalCount": 1, "hasNextPage": False}

    invoice = sportslink._one_document(_FakeClient(), 23962348)
    assert invoice["has_lines"] is False and invoice["lines"] == []
    assert invoice["charges"]["merchandise"] == 51.00

    result = reconcile(invoice, GOOD_LINES)
    assert result["status"] == "verified", result["reconciliation"]
    assert result["po_number"] == "P09409"          # match key survives
    assert result["invoice_number"] == "6164920830"  # so does the vendor's number
    assert result["total"] == 60.06
    assert len(result["lines"]) == 2

    # The guard against re-reading a document the API already gave lines for.
    class _FakeClientWithLines:
        def get_documents(self, _params):
            return {"items": [dict(raw, lines=[{"supplierItemNumber": "JP1477",
                                                "quantityShipped": 4}])],
                    "totalCount": 1, "hasNextPage": False}

    try:
        sportslink._fetch_invoice_doc(_FakeClientWithLines(), {"si_doc_number": 23962348})
    except ValueError as exc:
        assert "already has 1 line item" in str(exc)
        # Those lines are 4 × nothing against a 51.00 merchandise total, so the
        # refusal must also say they cannot be trusted.
        assert "do NOT reconcile" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected a refusal to re-read a document with EDI lines")
    print("PASS test_end_to_end_from_api_payload")


def test_placeholder_lines_do_not_count_as_line_data() -> None:
    """A scanned document comes back with a row of nothing, not an empty array.

    Observed live on siDocNumber 24684277: SportsLink returned one line with no
    item, no UPC, zero quantity and zero price, against a 398.40 merchandise
    total whose real vendor invoice has two lines. `has_lines` was `bool(lines)`,
    so that stub made a scanned document announce itself as EDI-backed — and any
    consumer branching on `has_lines` (the payables workflow does) would
    line-match against zeroes instead of escalating.
    """

    import sportslink

    # Verbatim from the live API for siDocNumber 24684277. Note the row is NOT
    # blank: it carries SI's own instruction, the same sentence printed on the
    # cover page of the PDF. A free-text description is therefore not evidence
    # of a real line — here it is evidence of the opposite.
    placeholder = {"supplierItemNumber": "", "upc": None,
                   "description": "SEE VENDOR INVOICE FOR DETAIL.",
                   "size": None, "color": None, "unit": "", "quantityOrdered": 0,
                   "quantityShipped": 0, "quantityBackOrdered": 0, "listPrice": 0.0,
                   "discountPercent": None, "netPrice": 0.0, "extension": 0.0}
    real = {"supplierItemNumber": "A062RY", "size": 'Adult 1-1/2"',
            "quantityShipped": 80, "netPrice": 2.29, "extension": 183.20}
    # Zero shipped but it identifies an item and carries a backorder — a real
    # line, and one that must survive the filter.
    backordered = {"supplierItemNumber": "AS1RY-L", "quantityShipped": 0,
                   "quantityBackOrdered": 80, "netPrice": 2.69, "extension": 0.0}

    assert sportslink._is_placeholder_line(placeholder) is True
    assert sportslink._is_placeholder_line({}) is True
    assert sportslink._is_placeholder_line(real) is False
    assert sportslink._is_placeholder_line(backordered) is False
    # String zeroes are just as empty as numeric ones.
    assert sportslink._is_placeholder_line(dict(placeholder, netPrice="0.00")) is True
    assert sportslink._is_placeholder_line(dict(placeholder, upc="0")) is False

    # A description alone never rescues a row — that was the bug. What rescues
    # it is identifying a product or carrying a number.
    assert sportslink._is_placeholder_line(
        dict(placeholder, description="ANY FREE TEXT AT ALL")
    ) is True
    assert sportslink._is_placeholder_line(
        {"description": "MVP BELT ROYAL", "quantityShipped": 80,
         "netPrice": 2.29, "extension": 183.20}
    ) is False
    assert sportslink._is_placeholder_line(
        {"upc": "197612326076", "quantityShipped": 0, "quantityBackOrdered": 80}
    ) is False

    raw = {"poNumber": "P13554", "siDocNumber": 24684277, "merchandiseTotal": 398.40,
           "docTotal": 401.59, "siUpcharge": 3.19}

    scanned = sportslink._normalise(dict(raw, lines=[placeholder]))
    assert scanned["has_lines"] is False, "a placeholder row is not line data"
    assert scanned["lines"] == []
    assert scanned["placeholder_lines"] == 1  # dropped, but never silently
    # SI's own explanation is kept rather than thrown away with the row.
    assert scanned["placeholder_note"] == "SEE VENDOR INVOICE FOR DETAIL."

    mixed = sportslink._normalise(dict(raw, lines=[real, placeholder]))
    assert mixed["has_lines"] is True
    assert len(mixed["lines"]) == 1 and mixed["placeholder_lines"] == 1
    print("PASS test_placeholder_lines_do_not_count_as_line_data")


def test_retrieval_names_documents_needing_recovery() -> None:
    """A retrieval must say which documents are not billable as returned.

    Handing back a mixed batch — some invoices with lines, some without — leaves
    the caller to *notice*, and the cost of not noticing is a bill raised from
    header totals with no line detail behind them. So the adapter names them and
    spells out the commands, rather than trusting anyone to read a doc section.
    """

    import sportslink

    placeholder = {"supplierItemNumber": "", "unit": "",
                   "description": "SEE VENDOR INVOICE FOR DETAIL.",
                   "quantityShipped": 0, "netPrice": 0.0, "extension": 0.0}
    real = {"supplierItemNumber": "A062RY", "quantityShipped": 80,
            "netPrice": 2.29, "extension": 183.20}

    items = [
        {"siDocNumber": 1, "merchandiseTotal": 5.19, "lines": [placeholder]},
        {"siDocNumber": 2, "merchandiseTotal": 398.40, "lines": [real]},
        {"siDocNumber": 3, "isCredit": True, "lines": [placeholder]},
    ]

    class _Fake:
        def get_documents(self, _params):
            return {"items": items, "hasNextPage": False}

    result = sportslink._list(_Fake(), {})

    # Only the scanned, non-credit document needs recovery.
    assert result["needs_line_recovery"] == [1]
    # Credits are listed apart: never billed, so recovering their lines achieves
    # nothing, but they still need a human.
    assert result["credits"] == [3]
    # The instruction is concrete — the actual commands, with a real doc number.
    assert '"si_doc_number": 1' in result["next_step"]
    assert "fetch-invoice-doc" in result["next_step"]
    assert "reconcile-lines" in result["next_step"]
    assert "header totals alone" in result["next_step"]

    # A clean batch says nothing, so the signal means something when it appears.
    class _AllEdi:
        def get_documents(self, _params):
            return {"items": [items[1]], "hasNextPage": False}

    clean = sportslink._list(_AllEdi(), {})
    assert clean["needs_line_recovery"] == []
    assert "next_step" not in clean

    # The A2A contract carries the same obligation — its caller cannot read
    # documentation.
    a2a = sportslink._get_for_a2a(_Fake(), {})
    assert a2a["metadata"]["needs_line_recovery"] == [1]
    assert a2a["metadata"]["credits"] == [3]
    assert "fetch-invoice-doc" in a2a["metadata"]["next_step"]
    print("PASS test_retrieval_names_documents_needing_recovery")


def test_document_identity_is_verified() -> None:
    """A lookup must return the document that was asked for, or refuse.

    `invoices[0]` was taken on faith. If the API ever ignores or widens the
    `siDocNumber` filter, that silently operates on a different invoice — the
    same wrong-document failure the portal row matching guards against, and just
    as invisible once the lines are downstream.
    """

    import sportslink

    raw = {"poNumber": "P13554", "siDocNumber": 24684277, "merchandiseTotal": 398.40,
           "docTotal": 401.59, "siUpcharge": 3.19}

    class _Fake:
        def __init__(self, items):
            self.items = items

        def get_documents(self, _params):
            return {"items": self.items, "hasNextPage": False}

    assert sportslink._one_document(_Fake([raw]), 24684277)["si_doc_number"] == 24684277

    # A different document comes back → refuse rather than use it.
    try:
        sportslink._one_document(_Fake([dict(raw, siDocNumber=24682750)]), 24684277)
    except Exception as exc:  # noqa: BLE001 — _ApiError is module-private
        assert "none carrying that number" in str(exc)
        assert "24682750" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected a refusal when the returned document differs")

    # The right one is picked out of a wider result set.
    wide = [dict(raw, siDocNumber=24682750), raw]
    assert sportslink._one_document(_Fake(wide), 24684277)["si_doc_number"] == 24684277
    print("PASS test_document_identity_is_verified")


def test_existing_lines_guard_reports_completeness() -> None:
    """"Has lines" is not "has complete lines".

    Refusing to re-read a PDF because the API already has line items is only
    right when those lines actually tie to the header. Partial EDI data is worse
    than none — it looks authoritative while being short — so the guard runs the
    same reconciliation and says which case this is.
    """

    import sportslink

    header = {
        "si_doc_number": 24684277, "po_number": "P13554", "is_credit": False,
        "total": 401.59,
        "charges": {"merchandise": 398.40, "si_upcharge": 3.19, "freight": None,
                    "freight_allowance": None, "svc_handle": None, "sales_tax": None,
                    "excise_tax": None, "discount": None},
    }
    both = [
        {"item": "A062RY", "size": 'Adult 1-1/2"', "qty_shipped": 80,
         "net_price": 2.29, "extension": 183.20},
        {"item": "AS1RY-L", "size": "L", "qty_shipped": 80,
         "net_price": 2.69, "extension": 215.20},
    ]

    complete = sportslink._existing_lines_message(dict(header, lines=both))
    assert "2 line items" in complete
    assert "reconcile to the merchandise total" in complete
    assert "use them" in complete

    partial = sportslink._existing_lines_message(dict(header, lines=both[:1]))
    assert "1 line item" in partial and "1 line items" not in partial
    assert "do NOT reconcile" in partial
    assert "incomplete" in partial
    assert '{"force": true}' in partial
    # A refusal must carry the raw lines it is refusing over. Without them the
    # only way to see why a line was judged real is to go back to the API by
    # hand — which is exactly what happened chasing the placeholder row.
    assert '"qty_shipped": 80' in partial and '"net_price": 2.29' in partial
    print("PASS test_existing_lines_guard_reports_completeness")


TESTS = (
    test_money_parsing,
    test_alias_normalisation,
    test_derivation_is_recorded,
    test_clean_lines_verify,
    test_missing_line_is_caught,
    test_misread_quantity_is_caught,
    test_transposed_price_is_caught,
    test_incomplete_line_is_caught,
    test_no_lines_is_caught,
    test_rounding_is_tolerated,
    test_doc_total_fallback_anchor,
    test_no_anchor_at_all,
    test_credit_memo_is_flagged,
    test_image_only_pdf_is_extracted,
    test_text_pdf_stays_in_memory,
    test_si_download_is_segmented,
    test_ocr_layout_preserves_columns,
    test_ocr_flags_only_shaky_numbers,
    test_ocr_engine_selection,
    test_row_matching,
    test_cloned_header_guard,
    test_download_formats,
    test_multi_page_merge,
    test_paging_reads_every_page,
    test_archived_search_columns,
    test_archived_fallback_is_automatic,
    test_portal_credentials_guard,
    test_no_network_idle_waits,
    test_placeholder_lines_do_not_count_as_line_data,
    test_retrieval_names_documents_needing_recovery,
    test_document_identity_is_verified,
    test_existing_lines_guard_reports_completeness,
    test_end_to_end_from_api_payload,
)


if __name__ == "__main__":
    for test in TESTS:
        test()
    print(f"\nALL {len(TESTS)} TESTS PASSED")
