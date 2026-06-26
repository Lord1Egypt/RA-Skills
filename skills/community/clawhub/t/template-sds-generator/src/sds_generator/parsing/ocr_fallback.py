from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

import fitz

from sds_generator.config_loader import PROJECT_ROOT, load_defaults
from sds_generator.exceptions import OCRUnavailableError

from .ocr_backends import OCRLineResult, OCRPageResult, resolve_ocr_backend


def _cache_root() -> Path:
    override = os.environ.get("SDS_GENERATOR_OCR_CACHE_DIR")
    if override:
        return Path(override)
    relative_root = str(load_defaults().get("parsing", {}).get("ocr_cache_dir", ".cache/ocr"))
    root = Path(relative_root)
    return root if root.is_absolute() else PROJECT_ROOT / root


def _cache_key(pdf_path: Path, *, page_number: int, backend_name: str) -> str:
    try:
        stat = pdf_path.stat()
        fingerprint = f"{pdf_path.resolve()}:{stat.st_size}:{stat.st_mtime_ns}"
    except FileNotFoundError:
        fingerprint = str(pdf_path)
    payload = f"{fingerprint}:{page_number}:{backend_name}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _cache_path(pdf_path: Path, *, page_number: int, backend_name: str, cache_root: Path) -> Path:
    return cache_root / f"{_cache_key(pdf_path, page_number=page_number, backend_name=backend_name)}.json"


def _serialize_result(result: OCRPageResult) -> dict[str, object]:
    return {
        "page_number": result.page_number,
        "text": result.text,
        "confidence": result.confidence,
        "backend_name": result.backend_name,
        "engine_version": result.engine_version,
        "image_width": result.image_width,
        "image_height": result.image_height,
        "lines": [
            {
                "text": line.text,
                "left": line.left,
                "top": line.top,
                "width": line.width,
                "height": line.height,
                "confidence": line.confidence,
            }
            for line in result.lines
        ],
    }


def _load_cached_result(cache_path: Path) -> OCRPageResult:
    payload = json.loads(cache_path.read_text(encoding="utf-8"))
    return OCRPageResult(
        page_number=int(payload["page_number"]),
        text=str(payload.get("text", "")),
        confidence=float(payload["confidence"]) if payload.get("confidence") is not None else None,
        backend_name=str(payload["backend_name"]),
        engine_version=str(payload["engine_version"]) if payload.get("engine_version") is not None else None,
        cache_hit=True,
        image_width=int(payload["image_width"]) if payload.get("image_width") is not None else None,
        image_height=int(payload["image_height"]) if payload.get("image_height") is not None else None,
        lines=[
            OCRLineResult(
                text=str(line.get("text", "")),
                left=float(line.get("left", 0.0)),
                top=float(line.get("top", 0.0)),
                width=float(line.get("width", 0.0)),
                height=float(line.get("height", 0.0)),
                confidence=float(line["confidence"]) if line.get("confidence") is not None else None,
            )
            for line in payload.get("lines", [])
        ],
    )


def run_ocr_for_pages(pdf_path: Path, page_numbers: list[int]) -> dict[int, OCRPageResult]:
    try:
        backend = resolve_ocr_backend()
    except OCRUnavailableError as exc:
        raise OCRUnavailableError(
            f"OCR is not configured for {pdf_path.name}. Unable to process scanned pages: {sorted(set(page_numbers))}."
        ) from exc
    cache_root = _cache_root()
    cache_root.mkdir(parents=True, exist_ok=True)
    render_scale = float(load_defaults().get("parsing", {}).get("ocr_render_scale", 2.0))

    results: dict[int, OCRPageResult] = {}
    with fitz.open(pdf_path) as document, tempfile.TemporaryDirectory(prefix="ocr-pages-") as temp_dir:
        temp_root = Path(temp_dir)
        for page_number in sorted(set(page_numbers)):
            cache_path = _cache_path(pdf_path, page_number=page_number, backend_name=backend.name, cache_root=cache_root)
            if cache_path.exists():
                results[page_number] = _load_cached_result(cache_path)
                continue

            page = document.load_page(page_number - 1)
            pixmap = page.get_pixmap(matrix=fitz.Matrix(render_scale, render_scale), alpha=False)
            image_path = temp_root / f"{pdf_path.stem}-page-{page_number}.png"
            pixmap.save(str(image_path))

            result = backend.recognize_image(
                image_path,
                page_number=page_number,
                image_width=pixmap.width,
                image_height=pixmap.height,
            )
            cache_path.write_text(json.dumps(_serialize_result(result), ensure_ascii=False, indent=2), encoding="utf-8")
            results[page_number] = result
    return results
