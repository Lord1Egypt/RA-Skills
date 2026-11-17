"""Rasterize the actual printed PDF, keeping previews identical to print output."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


def export_previews(pdf_path: Path, output_dir: Path, dpi: int = 144) -> list[Path]:
    if not 72 <= dpi <= 300:
        raise ValueError("preview dpi must be between 72 and 300")
    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp)
        converter = shutil.which("pdftoppm")
        if converter:
            subprocess.run([converter, "-png", "-r", str(dpi), str(pdf_path), str(staging / "page")],
                           check=True, capture_output=True, timeout=120)
        else:
            try:
                import pymupdf
            except ImportError as exc:
                raise RuntimeError("preview export needs Poppler (pdftoppm) or PyMuPDF; PDF remains available") from exc
            with pymupdf.open(pdf_path) as document:
                for number, page in enumerate(document, 1):
                    page.get_pixmap(dpi=dpi, alpha=False).save(staging / f"page-{number}.png")
        pages = sorted(staging.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
        if not pages:
            raise RuntimeError("PDF renderer produced no preview pages")
        output_dir.mkdir(parents=True, exist_ok=True)
        outputs = []
        for number, source in enumerate(pages, 1):
            target = output_dir / f"worksheet-page-{number}.png"
            shutil.copy2(source, target)
            outputs.append(target)
        for old in output_dir.glob("worksheet-page-*.png"):
            if old not in outputs:
                old.unlink()
        return outputs
