from __future__ import annotations

import csv
import io
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from sds_generator.exceptions import OCRUnavailableError


@dataclass(slots=True)
class OCRLineResult:
    text: str
    left: float
    top: float
    width: float
    height: float
    confidence: float | None = None


@dataclass(slots=True)
class OCRPageResult:
    page_number: int
    text: str
    confidence: float | None
    backend_name: str
    engine_version: str | None = None
    cache_hit: bool = False
    image_width: int | None = None
    image_height: int | None = None
    lines: list[OCRLineResult] = field(default_factory=list)


class TesseractCLIBackend:
    name = "tesseract_cli"

    def is_available(self) -> bool:
        return shutil.which("tesseract") is not None

    def version(self) -> str | None:
        if not self.is_available():
            return None
        completed = subprocess.run(
            ["tesseract", "--version"],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            return None
        return (completed.stdout or completed.stderr).splitlines()[0].strip() or None

    def recognize_image(
        self,
        image_path: Path,
        *,
        page_number: int,
        image_width: int | None = None,
        image_height: int | None = None,
    ) -> OCRPageResult:
        completed = subprocess.run(
            ["tesseract", str(image_path), "stdout", "--psm", "6", "tsv"],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            message = completed.stderr.strip() or completed.stdout.strip() or "unknown OCR failure"
            raise OCRUnavailableError(f"Tesseract OCR failed for {image_path.name}: {message}")
        text, confidence, lines = _parse_tesseract_tsv(completed.stdout)
        return OCRPageResult(
            page_number=page_number,
            text=text,
            confidence=confidence,
            backend_name=self.name,
            engine_version=self.version(),
            image_width=image_width,
            image_height=image_height,
            lines=lines,
        )


def _parse_tesseract_tsv(tsv_text: str) -> tuple[str, float | None, list[OCRLineResult]]:
    reader = csv.DictReader(io.StringIO(tsv_text), delimiter="\t")
    current_key: tuple[str, str, str, str] | None = None
    current_words: list[str] = []
    current_boxes: list[tuple[float, float, float, float]] = []
    current_confidences: list[float] = []
    lines: list[str] = []
    line_results: list[OCRLineResult] = []
    confidences: list[float] = []

    def flush_current_line() -> None:
        if not current_words:
            return
        line_text = " ".join(current_words).strip()
        if not line_text:
            return
        lines.append(line_text)
        xs = [box[0] for box in current_boxes]
        ys = [box[1] for box in current_boxes]
        rights = [box[2] for box in current_boxes]
        bottoms = [box[3] for box in current_boxes]
        line_results.append(
            OCRLineResult(
                text=line_text,
                left=min(xs) if xs else 0.0,
                top=min(ys) if ys else 0.0,
                width=(max(rights) - min(xs)) if xs and rights else 0.0,
                height=(max(bottoms) - min(ys)) if ys and bottoms else 0.0,
                confidence=(sum(current_confidences) / len(current_confidences)) if current_confidences else None,
            )
        )

    for row in reader:
        text = (row.get("text") or "").strip()
        key = (
            row.get("page_num", ""),
            row.get("block_num", ""),
            row.get("par_num", ""),
            row.get("line_num", ""),
        )
        if current_key is None:
            current_key = key
        elif key != current_key:
            flush_current_line()
            current_words = []
            current_boxes = []
            current_confidences = []
            current_key = key
        if text:
            current_words.append(text)
            try:
                left = float((row.get("left") or "").strip() or 0.0)
                top = float((row.get("top") or "").strip() or 0.0)
                width = float((row.get("width") or "").strip() or 0.0)
                height = float((row.get("height") or "").strip() or 0.0)
            except ValueError:
                left = top = width = height = 0.0
            current_boxes.append((left, top, left + width, top + height))
        conf_text = (row.get("conf") or "").strip()
        if conf_text and conf_text != "-1":
            try:
                confidence = float(conf_text)
            except ValueError:
                continue
            if confidence >= 0:
                confidences.append(confidence)
                current_confidences.append(confidence)
    flush_current_line()

    average_confidence = sum(confidences) / len(confidences) if confidences else None
    return "\n".join(lines).strip(), average_confidence, line_results


def resolve_ocr_backend() -> TesseractCLIBackend:
    backend = TesseractCLIBackend()
    if backend.is_available():
        return backend
    raise OCRUnavailableError("OCR is not configured because no supported OCR backend is available.")
