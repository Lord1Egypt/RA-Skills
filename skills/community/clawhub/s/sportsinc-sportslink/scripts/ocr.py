"""Deterministic OCR for scanned invoice pages — text before pixels.

A 300dpi scan costs a lot to put in front of a model and cannot be diffed,
grepped, or logged. So the scanned vendor-invoice pages are OCR'd first and the
*text* goes into context; the image stays on disk as the fallback for when the
text is not good enough.

That ordering is only safe because of what happens downstream: extracted lines
are checked against the API's `merchandiseTotal` before anything is billable. A
misread digit — the characteristic OCR failure — breaks that tie and comes back
`needs_review` rather than reaching a bill. OCR is allowed to be imperfect here
precisely because it is not the last word.

## Engines

Tried in order, first available wins:

* **rapidocr** (`rapidocr-onnxruntime`) — pip-only, no system binary, works the
  same on Windows and Linux. The default, and the reason this is practical to
  ship: nothing to install outside Python.
* **tesseract** (`pytesseract` + the `tesseract` binary) — used when present,
  since a site that already has it usually has it tuned.

Both return word boxes with coordinates, which matters: an invoice line is a
*row across columns*, and a reading order that loses the layout turns
`80  $2.29  $183.20` into three unrelated numbers. `layout_text` reassembles
rows by vertical position and pads by horizontal position, so the text handed to
the agent still looks like the table it came from.

## Confidence

Every row carries the minimum confidence of its parts, and the page reports a
mean. Low confidence is not an error — it is a hint about which rows to
cross-check against the image, and it travels with the text so the agent can
weigh it.
"""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# Rows whose worst *value-bearing* token falls below this are flagged.
#
# Deliberately not the worst token overall. On a real Champro scan the money read
# at 1.00 across the board while the rows scored 0.68 on `0EA` / `OPR` — the
# backorder zeros, which nothing downstream consumes. Flagging on that would mark
# every line item on every invoice as suspect, and an alarm that always fires is
# the same as no alarm: the agent opens the image every time and OCR-first buys
# nothing. What matters is the confidence of the numbers reconciliation will
# actually use.
_LOW_CONFIDENCE = 0.75

# Characters an OCR engine commonly returns in place of digits. A token made
# only of these (after stripping currency and punctuation) is a number it
# misread — `$O` for `$0` — and counts as value-bearing even though it contains
# no digit.
_DIGIT_LOOKALIKES = set("OoQDlItTSsZzBg")
_VALUE_STRIP = "$€£,.-%()"

# Two boxes belong to the same row when their vertical centres are within this
# fraction of the taller one's height.
_ROW_TOLERANCE = 0.6

# Character cell width as a fraction of median text height, used to convert x
# positions into column padding.
_CHAR_WIDTH_RATIO = 0.55

_MAX_COLUMNS = 200  # guard against a runaway pad on a wide scan


class OcrUnavailable(RuntimeError):
    """No usable OCR engine is installed."""


# ── engines ──────────────────────────────────────────────────────────────────


def _rapidocr(image_path: str) -> list[dict[str, Any]]:
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()
    result, _elapsed = engine(image_path)
    boxes: list[dict[str, Any]] = []
    for polygon, text, confidence in result or []:
        xs = [point[0] for point in polygon]
        ys = [point[1] for point in polygon]
        boxes.append({
            "text": str(text),
            "confidence": float(confidence),
            "x0": min(xs), "x1": max(xs), "y0": min(ys), "y1": max(ys),
        })
    return boxes


def _tesseract(image_path: str) -> list[dict[str, Any]]:
    import pytesseract
    from PIL import Image

    data = pytesseract.image_to_data(
        Image.open(image_path), output_type=pytesseract.Output.DICT
    )
    boxes: list[dict[str, Any]] = []
    for index, text in enumerate(data["text"]):
        text = (text or "").strip()
        if not text:
            continue
        try:
            confidence = float(data["conf"][index])
        except (TypeError, ValueError):
            confidence = -1.0
        if confidence < 0:
            continue
        left, top = data["left"][index], data["top"][index]
        boxes.append({
            "text": text,
            "confidence": confidence / 100.0,  # tesseract reports 0-100
            "x0": left, "x1": left + data["width"][index],
            "y0": top, "y1": top + data["height"][index],
        })
    return boxes


_ENGINES = {"rapidocr": _rapidocr, "tesseract": _tesseract}
_PREFERENCE = ("rapidocr", "tesseract")


def _is_available(name: str) -> bool:
    if name == "rapidocr":
        try:
            import rapidocr_onnxruntime  # noqa: F401
        except Exception:  # noqa: BLE001 — a broken install is unavailable too
            return False
        return True
    if name == "tesseract":
        try:
            import pytesseract  # noqa: F401
        except ImportError:
            return False
        import shutil

        return bool(shutil.which("tesseract"))
    return False


def available_engines() -> list[str]:
    """Installed engines, most preferred first."""

    return [name for name in _PREFERENCE if _is_available(name)]


def _select(requested: str | None) -> str:
    """Resolve the engine to use. `requested` may be a name, `auto`, or `off`."""

    choice = (requested or os.environ.get("SPORTSINC_OCR") or "auto").strip().lower()
    if choice == "off":
        raise OcrUnavailable("OCR is disabled (SPORTSINC_OCR=off).")
    if choice != "auto":
        if choice not in _ENGINES:
            raise OcrUnavailable(
                f"Unknown OCR engine {choice!r}. Known: {', '.join(_ENGINES)}, auto, off."
            )
        if not _is_available(choice):
            raise OcrUnavailable(f"OCR engine {choice!r} is not installed.")
        return choice
    engines = available_engines()
    if not engines:
        raise OcrUnavailable(
            "No OCR engine is installed, so scanned pages cannot be turned into text. "
            "Install one with `pip install rapidocr-onnxruntime` (pip-only, no system "
            "package). Until then the page images are the only way to read a scan."
        )
    return engines[0]


# ── layout ───────────────────────────────────────────────────────────────────


def _group_rows(boxes: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """Group boxes into visual rows by vertical position.

    An invoice line is a row across columns; grouping by reading order alone
    would scatter a line's quantity, price and extension into separate lines of
    text and make them unrelatable.
    """

    ordered = sorted(boxes, key=lambda box: ((box["y0"] + box["y1"]) / 2, box["x0"]))
    rows: list[dict[str, Any]] = []
    for box in ordered:
        centre = (box["y0"] + box["y1"]) / 2
        height = max(box["y1"] - box["y0"], 1.0)
        for row in rows:
            if abs(centre - row["centre"]) <= max(height, row["height"]) * _ROW_TOLERANCE:
                row["boxes"].append(box)
                row["centre"] = sum(
                    (b["y0"] + b["y1"]) / 2 for b in row["boxes"]
                ) / len(row["boxes"])
                row["height"] = max(row["height"], height)
                break
        else:
            rows.append({"centre": centre, "height": height, "boxes": [box]})

    rows.sort(key=lambda row: row["centre"])
    return [sorted(row["boxes"], key=lambda box: box["x0"]) for row in rows]


def _median_height(boxes: list[dict[str, Any]]) -> float:
    heights = sorted(max(box["y1"] - box["y0"], 1.0) for box in boxes)
    if not heights:
        return 12.0
    return heights[len(heights) // 2]


def is_value_token(text: str) -> bool:
    """Would reconciliation care whether this token was read correctly?

    True for anything carrying a digit, and for a token made entirely of
    digit-lookalikes once currency and punctuation are stripped — `$O` is a
    misread `$0`, and its confidence is worth reporting. False for words:
    a shaky `ROYAL` or `Pro Sock` costs nothing, because no arithmetic
    downstream consumes it.
    """

    stripped = "".join(char for char in (text or "") if char not in _VALUE_STRIP).strip()
    if not stripped:
        return False
    if any(char.isdigit() for char in stripped):
        return True
    if all(char in _DIGIT_LOOKALIKES for char in stripped):
        return True
    # A misread can delete the very digit that would have identified the token:
    # `0 PR` comes back as `OPR`, which carries no digit at all. Short tokens
    # containing a lookalike are therefore treated as value-bearing too — the
    # quantity columns are exactly where this happens, and a misread quantity is
    # the most expensive thing OCR can get wrong.
    return len(stripped) <= 4 and any(char in _DIGIT_LOOKALIKES for char in stripped)


def layout_text(boxes: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    """Render boxes as column-preserving text. Returns `(text, rows)`.

    Each row carries two confidences: `confidence`, the worst token of any kind,
    and `value_confidence`, the worst token that carries a number. Flagging uses
    the second — see `_LOW_CONFIDENCE`.
    """

    if not boxes:
        return "", []

    char_width = max(_median_height(boxes) * _CHAR_WIDTH_RATIO, 1.0)
    lines: list[str] = []
    rows: list[dict[str, Any]] = []

    for row_boxes in _group_rows(boxes):
        rendered: list[str] = []
        cursor = 0
        for box in row_boxes:
            column = min(int(box["x0"] / char_width), _MAX_COLUMNS)
            if column > cursor:
                rendered.append(" " * (column - cursor))
            elif rendered:
                rendered.append(" ")
            rendered.append(box["text"])
            cursor = column + len(box["text"])
        line = "".join(rendered).rstrip()
        value_boxes = [box for box in row_boxes if is_value_token(box["text"])]
        row: dict[str, Any] = {
            "text": line,
            "confidence": round(min(box["confidence"] for box in row_boxes), 3),
            "value_confidence": (
                round(min(box["confidence"] for box in value_boxes), 3)
                if value_boxes else None
            ),
        }
        if value_boxes:
            worst = min(value_boxes, key=lambda box: box["confidence"])
            if worst["confidence"] < _LOW_CONFIDENCE:
                row["weakest_value"] = worst["text"]
        lines.append(line)
        rows.append(row)

    return "\n".join(lines), rows


# ── entry point ──────────────────────────────────────────────────────────────


def read_image(image_path: str, *, engine: str | None = None) -> dict[str, Any]:
    """OCR one page image into column-preserving text.

    Returns `{engine, text, rows, mean_confidence, low_confidence_rows,
    box_count}`. Raises `OcrUnavailable` when no engine can run — the caller is
    expected to fall back to the image.
    """

    name = _select(engine)
    try:
        boxes = _ENGINES[name](image_path)
    except OcrUnavailable:
        raise
    except Exception as exc:  # noqa: BLE001 — engine failures are not fatal
        raise OcrUnavailable(f"OCR engine {name!r} failed on {image_path}: {exc}") from exc

    text, rows = layout_text(boxes)
    confidences = [box["confidence"] for box in boxes]
    mean = sum(confidences) / len(confidences) if confidences else 0.0
    # Only rows whose *numbers* are shaky. A row full of confidently-read money
    # and one uncertain colour is not worth opening the image for.
    low = [
        row for row in rows
        if row["value_confidence"] is not None
        and row["value_confidence"] < _LOW_CONFIDENCE
    ]

    return {
        "engine": name,
        "text": text,
        "rows": rows,
        "box_count": len(boxes),
        "mean_confidence": round(mean, 3),
        "low_confidence_rows": low,
    }


__all__ = ("OcrUnavailable", "available_engines", "layout_text", "read_image")
