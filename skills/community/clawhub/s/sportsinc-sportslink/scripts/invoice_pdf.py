"""PDF handling for Sports Inc invoice documents — no model calls, no OCR.

This module does the *deterministic* half of the header-only fallback: turn a
SportsWeb PDF into something the agent can actually read, and say which parts of
it are worth reading. It never interprets an invoice — the reading is the
agent's job (see `references/pdf_extraction.md`), and the checking is
`invoice_lines.py`'s job.

## What a Sports Inc download actually looks like

Not one invoice. A download is a **stack of documents**, each of which is:

    [ SI cover page ]  landscape, native text, no line detail — it literally
                       says "SEE VENDOR INVOICE FOR DETAIL." Carries the SI
                       document number and the totals.
    [ vendor invoice ] portrait, usually a 300dpi **scan** — this is where the
                       line items live.

One PDF routinely holds several such pairs (one per SI document on the PO). So
this module classifies every page, groups the pages into documents, and extracts
the scanned pages as PNGs the agent can look at.

That extraction matters more than it sounds: the scans are nested two levels
deep inside Form XObjects, so naive per-page image code finds nothing, and
`extract_text()` over the whole file returns a healthy-looking character count
made up **entirely of SI cover boilerplate** — a document that looks like it has
a text layer while containing zero line detail. Hence per-page classification
rather than one verdict for the file.
"""

from __future__ import annotations

import io
import os
import re
import tempfile
import time
from pathlib import Path
from typing import Any

# A page below this many characters carries no readable content.
_MIN_PAGE_CHARS = 40

# Boilerplate that identifies an SI cover page. Two hits is enough — the wording
# is stable but the text layer's ordering is not.
_SI_COVER_MARKERS = (
    "SI DOCUMENT NUMBER",
    "SPORTS, INC.",
    "SI UPCHARGE",
    "MERCHANDISE TOTAL",
    "SEE VENDOR INVOICE",
)
_SI_COVER_MIN_HITS = 2

# The SI document number as printed on a cover page. Its label and its value are
# not adjacent in the extracted text (labels come out in one run, values in
# another), so match on shape and report every candidate rather than pretending
# to know which is which.
_SI_DOC_CANDIDATE = re.compile(r"(?<!\d)(?<!SI)(?<!SI-)(\d{7,9})(?!\d)")
_SUPPLIER_DOC_CANDIDATE = re.compile(r"\bSI-?\d{6,9}\b")

# Scratch artifacts (stashed PDFs, extracted page images) live here and are
# swept after a day — the source of record is the Invoice Center, not this dir.
_STASH_DIRNAME = "sportsinc_invoices"
_STASH_TTL_SECONDS = 24 * 60 * 60

# Extracted page images are downscaled to this longest edge: enough to read a
# 300dpi scan comfortably, small enough not to bloat the agent's context.
_MAX_IMAGE_EDGE = 2200

_PAGE_MARK = "----- page {n} of {total} -----"


class PdfError(RuntimeError):
    """The PDF could not be opened or read."""


# ── scratch directory ────────────────────────────────────────────────────────


def _stash_dir() -> Path:
    override = (os.environ.get("SPORTSINC_PDF_DIR") or "").strip()
    path = Path(override) if override else Path(tempfile.gettempdir()) / _STASH_DIRNAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def scratch_dir() -> Path:
    """The directory scratch artifacts are written to (honours SPORTSINC_PDF_DIR)."""

    return _stash_dir()


def _sweep(directory: Path) -> None:
    """Drop scratch files older than the TTL. Best-effort; never fatal."""

    cutoff = time.time() - _STASH_TTL_SECONDS
    try:
        for pattern in ("si-*.pdf", "si-*.png", "si-*.jp2", "si-*.jpg"):
            for old in directory.glob(pattern):
                try:
                    if old.stat().st_mtime < cutoff:
                        old.unlink()
                except OSError:
                    continue
    except OSError:
        pass


def _safe_name(label: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", str(label)).strip("-")
    return cleaned or "unknown"


# ── reading ──────────────────────────────────────────────────────────────────


def _reader(pdf_bytes: bytes):
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover — runtime guard
        raise PdfError(
            "pypdf is required to read invoice PDFs. Install it (see the skill's "
            "install deps) with `pip install pypdf`."
        ) from exc
    try:
        return PdfReader(io.BytesIO(pdf_bytes))
    except Exception as exc:  # noqa: BLE001 — pypdf raises a zoo of types
        raise PdfError(f"Could not open the PDF ({len(pdf_bytes)} bytes): {exc}") from exc


def _page_images(page: Any, depth: int = 0) -> list[Any]:
    """Every image on a page, walking **nested Form XObjects**.

    Sports Inc's scans sit two Form levels down (`/I1 Do` → `/I0 Do` → image), so
    a one-level `/Subtype /Image` scan over the page's resources comes back empty
    on exactly the pages that matter.
    """

    if depth > 6:
        return []
    resources = page.get("/Resources") or {}
    xobjects = resources.get("/XObject")
    if not xobjects:
        return []
    found: list[Any] = []
    try:
        entries = xobjects.get_object().items()
    except Exception:  # noqa: BLE001 — a malformed resource dict is not fatal
        return []
    for _name, ref in entries:
        try:
            obj = ref.get_object()
        except Exception:  # noqa: BLE001
            continue
        if obj.get("/Subtype") == "/Image":
            found.append(obj)
        else:
            found.extend(_page_images(obj, depth + 1))
    return found


def _write_image(image_obj: Any, destination: Path) -> tuple[str, str | None]:
    """Write one embedded image as PNG. Returns `(path, note)`.

    Falls back to dumping the raw stream when Pillow is unavailable or cannot
    decode the codec (SI's scans are JPEG 2000, which needs Pillow built with
    openjpeg). A raw dump is still better than nothing — the agent is told what
    it got.
    """

    try:
        raw = image_obj.get_data()
    except Exception as exc:  # noqa: BLE001
        raise PdfError(f"Could not read an embedded image: {exc}") from exc

    try:
        from PIL import Image
    except ImportError:
        fallback = destination.with_suffix(".jp2")
        fallback.write_bytes(raw)
        return str(fallback), (
            "Pillow is not installed, so the page image could not be converted to "
            "PNG; the raw encoded stream was written instead."
        )

    try:
        with Image.open(io.BytesIO(raw)) as img:
            converted = img.convert("RGB")
            if max(converted.size) > _MAX_IMAGE_EDGE:
                converted.thumbnail((_MAX_IMAGE_EDGE, _MAX_IMAGE_EDGE))
            converted.save(destination, format="PNG")
        return str(destination), None
    except Exception as exc:  # noqa: BLE001 — codec support varies by build
        fallback = destination.with_suffix(".jp2")
        fallback.write_bytes(raw)
        return str(fallback), (
            f"Pillow could not decode this page image ({exc}); the raw encoded "
            "stream was written instead. Read the stashed PDF page instead."
        )


# ── classification ───────────────────────────────────────────────────────────


def _classify(text: str, image_count: int) -> str:
    stripped = text.strip()
    if len(stripped) >= _MIN_PAGE_CHARS:
        upper = stripped.upper()
        hits = sum(1 for marker in _SI_COVER_MARKERS if marker in upper)
        return "si_cover" if hits >= _SI_COVER_MIN_HITS else "text"
    return "image" if image_count else "blank"


def _group_documents(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group pages into documents: one SI cover plus the detail pages after it.

    A PDF that starts with detail pages (a single-document download with no
    cover) yields one group with no cover page — which is fine, and reported.
    """

    documents: list[dict[str, Any]] = []
    for page in pages:
        if page["kind"] == "si_cover" or not documents:
            documents.append({
                "si_cover_page": page["page"] if page["kind"] == "si_cover" else None,
                "si_doc_number_candidates": page.get("si_doc_number_candidates", []),
                "supplier_doc_candidates": page.get("supplier_doc_candidates", []),
                "detail_pages": [],
                "detail_is_scanned": False,
            })
            if page["kind"] == "si_cover":
                continue
        current = documents[-1]
        current["detail_pages"].append(page["page"])
        if page["kind"] == "image":
            current["detail_is_scanned"] = True
    return documents


# ── the one call the CLI action makes ────────────────────────────────────────


def _ocr_page(image_path: str, engine: str | None) -> dict[str, Any] | None:
    """OCR one extracted page image, or None if that is not possible.

    Text beats pixels: it is a fraction of the context cost, and it can be
    diffed, grepped and logged. The image stays on disk either way — OCR is the
    first attempt, not the only one.
    """

    try:
        from ocr import OcrUnavailable, read_image  # noqa: E402  (lazy)
    except ImportError:  # pragma: no cover — sibling module always present
        return None
    try:
        return read_image(image_path, engine=engine)
    except OcrUnavailable as exc:
        return {"engine": None, "text": "", "unavailable": str(exc)}
    except Exception as exc:  # noqa: BLE001 — OCR must never sink the fetch
        return {"engine": None, "text": "", "unavailable": f"OCR failed: {exc}"}


def prepare(
    pdf_bytes: bytes,
    *,
    label: str,
    stash: str = "auto",
    ocr: str | None = None,
) -> dict[str, Any]:
    """Classify every page, extract scanned pages as images, OCR them, and group
    the result into documents.

    `stash`:
      * `"auto"`   — write page images for scanned pages, and keep a copy of the
                     PDF when any page is scanned (default).
      * `"always"` — also keep the PDF when every page has text.
      * `"never"`  — write nothing to disk. A scanned document then comes back
                     with no way to read it, and `next_step` says so.

    `ocr`: `"auto"` (default — use the best installed engine), `"off"`, or an
    engine name. Honours `SPORTSINC_OCR` when unset.
    """

    if stash not in ("auto", "always", "never"):
        raise ValueError("`stash` must be one of: auto, always, never")

    reader = _reader(pdf_bytes)
    directory = None if stash == "never" else _stash_dir()
    if directory is not None:
        _sweep(directory)

    pages: list[dict[str, Any]] = []
    notes: list[str] = []
    total = len(reader.pages)

    for index, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:  # noqa: BLE001 — one bad page shouldn't sink the doc
            text = ""
        images = _page_images(page)
        kind = _classify(text, len(images))

        entry: dict[str, Any] = {
            "page": index,
            "kind": kind,
            "chars": len(text.strip()),
            "image_paths": [],
        }
        if kind == "si_cover":
            # Candidates, not conclusions: the cover's labels and values are not
            # adjacent in the text layer, so the number cannot be read off a label.
            entry["si_doc_number_candidates"] = [
                int(match) for match in _SI_DOC_CANDIDATE.findall(text)
            ]
            entry["supplier_doc_candidates"] = sorted(
                set(_SUPPLIER_DOC_CANDIDATE.findall(text))
            )
        if kind in ("text", "si_cover"):
            entry["text"] = text

        if kind == "image" and directory is not None:
            for position, image_obj in enumerate(images, start=1):
                suffix = "" if len(images) == 1 else f"-{position}"
                target = directory / f"si-{_safe_name(label)}-p{index}{suffix}.png"
                try:
                    written, note = _write_image(image_obj, target)
                except PdfError as exc:
                    notes.append(f"page {index}: {exc}")
                    continue
                entry["image_paths"].append(written)
                if note:
                    notes.append(f"page {index}: {note}")

            # Read the scan into text. The image remains on disk regardless —
            # OCR is the cheap first attempt, not a replacement for looking.
            if entry["image_paths"] and ocr != "off":
                read = _ocr_page(entry["image_paths"][0], ocr)
                if read and read.get("text"):
                    entry["ocr"] = {
                        "engine": read["engine"],
                        "mean_confidence": read["mean_confidence"],
                        "box_count": read["box_count"],
                        "low_confidence_rows": read["low_confidence_rows"],
                    }
                    entry["text"] = read["text"]
                elif read and read.get("unavailable"):
                    notes.append(f"page {index}: {read['unavailable']}")

        pages.append(entry)

    documents = _group_documents(pages)

    text_pages = [p for p in pages if p["kind"] in ("text", "si_cover")]
    image_pages = [p["page"] for p in pages if p["kind"] == "image"]
    ocr_pages = [p["page"] for p in pages if p.get("ocr")]
    unreadable = [p["page"] for p in pages if p["kind"] == "image" and not p.get("ocr")]
    chars = sum(p["chars"] for p in pages)

    # Assemble every page that has text, native or OCR'd, in page order. OCR
    # pages are labelled with their engine and confidence — the agent must be
    # able to tell a transcription from the document's own text layer, because
    # only one of them can misread a digit.
    readable = [p for p in pages if p.get("text")]
    readable.sort(key=lambda p: p["page"])
    blocks = []
    for page in readable:
        mark = _PAGE_MARK.format(n=page["page"], total=total)
        if page.get("ocr"):
            mark += (
                f"  [OCR: {page['ocr']['engine']}, "
                f"mean confidence {page['ocr']['mean_confidence']}]"
            )
        blocks.append(mark + "\n" + page["text"])
    assembled = "\n".join(blocks)

    keep_pdf = stash == "always" or (stash == "auto" and bool(image_pages))
    pdf_path = None
    if keep_pdf and directory is not None:
        pdf_path = directory / f"si-{_safe_name(label)}.pdf"
        try:
            pdf_path.write_bytes(pdf_bytes)
        except OSError as exc:
            raise PdfError(f"Could not write the invoice PDF to {pdf_path}: {exc}") from exc
        pdf_path = str(pdf_path)

    image_paths = [path for p in pages for path in p["image_paths"]]

    if ocr_pages and not unreadable:
        next_step = (
            f"Line detail is on scanned page(s) {image_pages}, which have been OCR'd into "
            "`text` (look for the [OCR:…] page markers). Read the text — the SI cover "
            "pages carry no line items (they say \"SEE VENDOR INVOICE FOR DETAIL\"), so "
            "skip them. OCR misreads digits occasionally, so if a row looks wrong, or if "
            f"`reconcile-lines` reports a variance, read the image in `image_paths` before "
            "escalating. See references/pdf_extraction.md."
        )
    elif image_pages and image_paths:
        next_step = (
            f"Line detail is on the SCANNED page(s) {image_pages} and OCR did not produce "
            "text for "
            + (f"page(s) {unreadable}" if unreadable else "them")
            + " — read the extracted image(s) in `image_paths` instead. The SI cover pages "
            "carry no line items (they say \"SEE VENDOR INVOICE FOR DETAIL\"); skip them. "
            "See references/pdf_extraction.md, then pass each document's lines to "
            "`reconcile-lines` separately."
        )
    elif image_pages:
        next_step = (
            f"Page(s) {image_pages} are scans and no image could be written "
            f"({'stashing disabled' if directory is None else 'extraction failed'}), so "
            "the line detail cannot be read. Re-run with stash=\"auto\"."
        )
    elif text_pages:
        next_step = (
            "Every page has a text layer — read `text` (skipping any SI cover page, "
            "which carries no line items), then pass each document's lines to "
            "`reconcile-lines`."
        )
    else:
        next_step = "This PDF has no readable pages at all — escalate it."

    return {
        "page_count": total,
        "pages": pages,
        "documents": documents,
        "text": assembled,
        "chars": chars,
        "has_text_layer": bool(text_pages),
        "text_covers_all_pages": not image_pages and bool(text_pages),
        # Every page now has readable text, whether native or transcribed —
        # this is the flag that says the images are a cross-check rather than
        # the only way in.
        "readable_text_covers_all_pages": bool(readable) and not unreadable,
        "ocr_pages": ocr_pages,
        "ocr_engine": next((p["ocr"]["engine"] for p in pages if p.get("ocr")), None),
        "pages_without_text": unreadable,
        "image_pages": image_pages,
        "image_paths": image_paths,
        "pdf_path": pdf_path,
        "bytes": len(pdf_bytes),
        "notes": notes,
        "next_step": next_step,
    }


def merge_pdfs(parts: list[bytes]) -> bytes:
    """Concatenate PDFs in order.

    Row selection in the Invoice Center is per page, so a PO whose invoices span
    several pages has to be downloaded a page at a time. Stitching the parts back
    together keeps the rest of the pipeline oblivious: `prepare()` segments the
    combined file into documents exactly as it does a single-page download.
    """

    if not parts:
        raise PdfError("No PDF parts to merge.")
    if len(parts) == 1:
        return parts[0]

    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError as exc:  # pragma: no cover — runtime guard
        raise PdfError("pypdf is required to merge multi-page downloads.") from exc

    writer = PdfWriter()
    for index, part in enumerate(parts, start=1):
        try:
            reader = PdfReader(io.BytesIO(part))
            for page in reader.pages:
                writer.add_page(page)
        except Exception as exc:  # noqa: BLE001
            raise PdfError(f"Could not merge PDF part {index} of {len(parts)}: {exc}") from exc

    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def read_pdf_file(path: str) -> bytes:
    """Read a PDF off disk — the manual path, for a document pulled by hand."""

    file_path = Path(path).expanduser()
    if not file_path.is_file():
        raise PdfError(f"PDF file not found: {file_path}")
    try:
        return file_path.read_bytes()
    except OSError as exc:
        raise PdfError(f"Could not read {file_path}: {exc}") from exc


def extract_text(pdf_bytes: bytes) -> dict[str, Any]:
    """Text-only view of a PDF, for callers that just want the characters."""

    prepared = prepare(pdf_bytes, label="probe", stash="never")
    return {
        "page_count": prepared["page_count"],
        "pages": [page.get("text", "") for page in prepared["pages"]],
        "text": prepared["text"],
        "chars": prepared["chars"],
        "has_text_layer": prepared["has_text_layer"],
    }


__all__ = ("PdfError", "extract_text", "prepare", "read_pdf_file", "scratch_dir")
