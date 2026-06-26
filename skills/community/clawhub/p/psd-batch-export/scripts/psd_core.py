"""Production helpers for the psd-batch-export skill.

This module keeps the stable, machine-readable interface separate from the
legacy console-first scripts. The legacy scripts remain importable and runnable.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import time
from pathlib import Path
from typing import Any

import pandas as pd
from psd_tools import PSDImage

from batch_from_excel import batch_export, generate_intelligent_report, match_columns, verify_export
from render_psd_batch import find_fonts, get_text_style, prerender_background, render_with_background
from template_loader import TEMPLATES, get_psd_path


SKILL_ROOT = Path(__file__).resolve().parent.parent
REFERENCES_DIR = SKILL_ROOT / "references"
TEMPLATES_JSON = REFERENCES_DIR / "templates.json"

EXIT_SUCCESS = 0
EXIT_INPUT_ERROR = 1
EXIT_DEPENDENCY_ERROR = 2
EXIT_VERIFY_ERROR = 3
EXIT_UNEXPECTED_ERROR = 4


class PsdBatchError(Exception):
    """Known production error with a stable exit code."""

    def __init__(self, message: str, exit_code: int = EXIT_INPUT_ERROR, *, errors: list[str] | None = None):
        super().__init__(message)
        self.exit_code = exit_code
        self.errors = errors or [message]


def now() -> float:
    return time.perf_counter()


def runtime(start: float) -> float:
    return round(time.perf_counter() - start, 3)


def write_json(path: str | Path | None, payload: dict[str, Any]) -> None:
    if not path:
        return
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def normalize_sheet(sheet: str | int) -> str | int:
    return int(sheet) if isinstance(sheet, str) and sheet.isdigit() else sheet


def load_table(data_path: str | Path, sheet: str | int = 0) -> pd.DataFrame:
    path = Path(data_path)
    if not path.exists():
        raise PsdBatchError(f"Data file not found: {path}")
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls", ".xlsm"}:
        return pd.read_excel(path, sheet_name=normalize_sheet(sheet)).dropna(how="all")
    if suffix == ".csv":
        return pd.read_csv(path).dropna(how="all")
    if suffix == ".tsv":
        return pd.read_csv(path, sep="\t").dropna(how="all")
    raise PsdBatchError(f"Unsupported data file extension: {suffix}")


def resolve_psd(psd_or_template: str | Path) -> Path:
    candidate = Path(psd_or_template)
    if candidate.exists():
        return candidate
    psd_path = get_psd_path(str(psd_or_template))
    if psd_path and psd_path.exists():
        return psd_path
    raise PsdBatchError(f"PSD/template not found: {psd_or_template}")


def package_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def diagnose() -> dict[str, Any]:
    start = now()
    fonts = find_fonts()
    template_files = []
    for slug, meta in TEMPLATES.items():
        psd_path = get_psd_path(slug)
        template_files.append(
            {
                "slug": slug,
                "name": meta.get("name"),
                "psd": str(psd_path) if psd_path else None,
                "exists": bool(psd_path and psd_path.exists()),
            }
        )

    required_packages = ["PIL", "psd_tools", "pandas", "openpyxl"]
    optional_packages = ["pytesseract", "openai", "anthropic"]
    missing_required = [pkg for pkg in required_packages if not package_available(pkg)]
    warnings: list[str] = []
    if missing_required:
        warnings.append(f"Missing required Python packages: {', '.join(missing_required)}")
    if not fonts:
        warnings.append("No .ttf/.otf fonts found in bundled or system font directories.")
    if not TEMPLATES_JSON.exists():
        warnings.append("Template catalog is missing: references/templates.json")

    return {
        "status": "ok" if not missing_required else "error",
        "inputs": {},
        "layers": [],
        "mapping": [],
        "capacity_risks": [],
        "fonts": {
            "count": len(fonts),
            "sample": [Path(f).name for f in fonts[:10]],
            "font_dir": str(SKILL_ROOT / "fonts"),
        },
        "templates": template_files,
        "dependencies": {
            "required": {pkg: package_available(pkg) for pkg in required_packages},
            "optional": {pkg: package_available(pkg) for pkg in optional_packages},
            "tesseract_cmd": shutil.which("tesseract"),
            "llm_api_key_configured": bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")),
        },
        "outputs": {},
        "warnings": warnings,
        "errors": missing_required,
        "runtime_sec": runtime(start),
    }


def normalize_report(raw: dict[str, Any], *, psd_path: Path, data_path: Path | None = None, start: float | None = None) -> dict[str, Any]:
    layers = raw.get("text_layers") or []
    capacity = raw.get("capacity") or []
    risks = [item for item in capacity if item.get("risk")]
    mapping = raw.get("column_mapping") or []
    fonts = raw.get("font_recommendations") or []
    warnings = list(raw.get("warnings") or [])
    errors: list[str] = []

    return {
        "status": "ok" if not errors else "error",
        "inputs": {
            "psd": str(psd_path),
            "data": str(data_path) if data_path else None,
        },
        "layers": layers,
        "mapping": mapping,
        "capacity_risks": risks,
        "fonts": {
            "available": raw.get("available_fonts", []),
            "recommendations": fonts,
        },
        "outputs": {},
        "warnings": warnings,
        "errors": errors,
        "runtime_sec": runtime(start) if start is not None else 0.0,
    }


def analyze(psd: str | Path, data: str | Path | None = None, *, sheet: str | int = 0, font: str | None = None) -> dict[str, Any]:
    start = now()
    psd_path = resolve_psd(psd)
    df = load_table(data, sheet) if data else None
    raw = generate_intelligent_report(psd_path, data, df, manual_font=font)
    return normalize_report(raw, psd_path=psd_path, data_path=Path(data) if data else None, start=start)


def strict_failures(report: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for item in report.get("mapping", []):
        if item.get("confidence") in {"low", "none"}:
            failures.append(f"Low-confidence column mapping: {item.get('layer')} -> {item.get('excel_col')}")
    for item in report.get("capacity_risks", []):
        failures.append(
            f"Capacity risk: {item.get('name')} data max {item.get('data_max_len')} > capacity {item.get('capacity')}"
        )
    for item in report.get("fonts", {}).get("recommendations", []):
        if item.get("confidence") == "not found":
            failures.append(f"Font not found: {item.get('layer')} uses {item.get('psd_font')}")
    return failures


def preview(
    psd: str | Path,
    data: str | Path,
    out: str | Path,
    *,
    rows: int = 3,
    sheet: str | int = 0,
    font: str | None = None,
    color: tuple[int, int, int] | None = None,
    font_size: int | None = None,
    align: str = "center",
    dpi: int = 300,
    strict: bool = False,
) -> dict[str, Any]:
    start = now()
    psd_path = resolve_psd(psd)
    data_path = Path(data)
    df = load_table(data_path, sheet)
    report = analyze(psd_path, data_path, sheet=sheet, font=font)
    failures = strict_failures(report) if strict else []
    if failures:
        report["status"] = "error"
        report["errors"] = failures
        report["runtime_sec"] = runtime(start)
        raise PsdBatchError("Strict preview checks failed", EXIT_VERIFY_ERROR, errors=failures)

    psd_obj = PSDImage.open(str(psd_path))
    layers = [(l.name, l.text.strip("\x00").strip()) for l in psd_obj.descendants() if l.kind == "type"]
    if report.get("mapping"):
        mapping = [(m["layer"], m["original"], m["excel_col"], m["confidence"]) for m in report["mapping"]]
    else:
        mapping = match_columns(layers, df.columns)
    layer_to_col = {ln: cn for ln, _, cn, conf in mapping if cn and conf != "none"}

    bg_cache = prerender_background(psd_path)
    template_styles = []
    for layer in psd_obj.descendants():
        if layer.kind != "type":
            continue
        style = get_text_style(layer)
        if not style:
            continue
        style["layer_name"] = layer.name
        template_styles.append(style)

    fonts = [font] if font else find_fonts()[:5]
    effective_color = color
    preview_dir = Path(out) / "dryrun_preview"
    preview_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for index, (_, row) in enumerate(df.head(max(rows, 0)).iterrows(), start=1):
        styles = copy.deepcopy(template_styles)
        for style in styles:
            col = layer_to_col.get(style.get("layer_name"))
            if col and col in df.columns and pd.notna(row[col]):
                style["text"] = str(row[col]).strip()
        image = render_with_background(bg_cache, styles, fonts, effective_color, font_size, align)
        output_file = preview_dir / f"preview_{index:03d}.png"
        image.save(str(output_file), "PNG", dpi=(dpi, dpi))
        outputs.append(str(output_file))

    report["status"] = "ok"
    report["outputs"] = {
        "preview_dir": str(preview_dir),
        "preview_png": outputs,
        "rows": len(outputs),
        "text_color": list(effective_color) if effective_color is not None else "psd-layer",
    }
    report["runtime_sec"] = runtime(start)
    return report


def export_batch(
    psd: str | Path,
    data: str | Path,
    out: str | Path,
    *,
    sheet: str | int = 0,
    font: str | None = None,
    color: tuple[int, int, int] | None = None,
    font_size: int | None = None,
    align: str = "center",
    dpi: int = 300,
    cols: str | None = None,
    verify_samples: int = 3,
    ocr: bool = False,
    ocr_lang: str | None = None,
    tesseract_cmd: str | None = None,
    tessdata_dir: str | None = None,
    strict: bool = False,
) -> dict[str, Any]:
    start = now()
    psd_path = resolve_psd(psd)
    data_path = Path(data)
    preflight = analyze(psd_path, data_path, sheet=sheet, font=font)
    effective_color = color
    failures = strict_failures(preflight) if strict else []
    if failures:
        preflight["status"] = "error"
        preflight["errors"] = failures
        preflight["runtime_sec"] = runtime(start)
        raise PsdBatchError("Strict export checks failed", EXIT_VERIFY_ERROR, errors=failures)

    count = batch_export(
        data_path,
        psd_path,
        out,
        font=font,
        color=effective_color,
        font_size=font_size,
        align=align,
        dpi=dpi,
        cols=cols,
        sheet=normalize_sheet(sheet),
        dry_run=False,
        analyze_only=False,
        verify_samples=verify_samples,
        ocr=ocr,
        ocr_lang=ocr_lang,
        tesseract_cmd=tesseract_cmd,
        tessdata_dir=tessdata_dir,
    )

    output_dir = Path(out)
    verify_report_path = output_dir / "verify_report" / "report.json"
    verify_payload = None
    if verify_report_path.exists():
        verify_payload = json.loads(verify_report_path.read_text(encoding="utf-8"))
    psd_files = sorted((output_dir / "psd").glob("*.psd")) if (output_dir / "psd").exists() else []
    png_files = sorted((output_dir / "png").glob("*.png")) if (output_dir / "png").exists() else []

    result = preflight
    result["status"] = "ok" if not (verify_payload and not verify_payload.get("ok", True)) else "error"
    result["outputs"] = {
        "output_dir": str(output_dir),
        "psd_dir": str(output_dir / "psd"),
        "png_dir": str(output_dir / "png"),
        "verify_report": str(verify_report_path) if verify_report_path.exists() else None,
        "generated_psd": len(psd_files),
        "generated_png": len(png_files),
        "reported_count": count,
        "text_color": list(effective_color) if effective_color is not None else "psd-layer",
    }
    if verify_payload and not verify_payload.get("ok", True):
        result["errors"] = list(verify_payload.get("errors") or [])
    result["verify"] = verify_payload
    result["runtime_sec"] = runtime(start)
    return result


def verify_output(
    out: str | Path,
    *,
    samples: int = 3,
    dpi: int = 300,
    color: tuple[int, int, int] | None = None,
    ocr: bool = False,
    ocr_lang: str | None = None,
    tesseract_cmd: str | None = None,
    tessdata_dir: str | None = None,
) -> dict[str, Any]:
    start = now()
    output_dir = Path(out)
    psd_dir = output_dir / "psd"
    png_dir = output_dir / "png"
    if not output_dir.exists():
        raise PsdBatchError(f"Output directory not found: {output_dir}")
    expected = len(list(psd_dir.glob("*.psd"))) if psd_dir.exists() else len(list(png_dir.glob("*.png")))
    effective_color = color
    raw = verify_export(
        output_dir,
        expected,
        sample_count=samples,
        dpi=dpi,
        color=effective_color,
        ocr=ocr,
        ocr_lang=ocr_lang,
        tesseract_cmd=tesseract_cmd,
        tessdata_dir=tessdata_dir,
    )
    return {
        "status": "ok" if raw.get("ok") else "error",
        "inputs": {"output_dir": str(output_dir)},
        "layers": [],
        "mapping": [],
        "capacity_risks": [],
        "fonts": {},
        "outputs": {
            "verify_report": raw.get("report_dir"),
            "text_color": list(effective_color) if effective_color is not None else "psd-layer",
        },
        "warnings": [],
        "errors": list(raw.get("errors") or ([] if raw.get("ok") else [raw.get("error", "verification failed")])),
        "verify": raw,
        "runtime_sec": runtime(start),
    }


def templates_payload(slug: str | None = None) -> dict[str, Any]:
    start = now()
    if slug:
        item = TEMPLATES.get(slug)
        if not item:
            raise PsdBatchError(f"Unknown template: {slug}")
        payload: Any = {**item, "resolved_psd": str(get_psd_path(slug))}
    else:
        payload = [{**meta, "id": key, "resolved_psd": str(get_psd_path(key))} for key, meta in TEMPLATES.items()]
    return {
        "status": "ok",
        "inputs": {"slug": slug},
        "layers": [],
        "mapping": [],
        "capacity_risks": [],
        "fonts": {},
        "templates": payload,
        "outputs": {},
        "warnings": [],
        "errors": [],
        "runtime_sec": runtime(start),
    }
