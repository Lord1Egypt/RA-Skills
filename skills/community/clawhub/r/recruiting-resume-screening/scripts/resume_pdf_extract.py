#!/usr/bin/env python3
"""Multi-backend PDF extraction & triage for Chinese resume screening.

Runs available PDF text backends (PyMuPDF / pdfplumber / pdfminer.six)
against each PDF, cleans the output, scores it, and writes the best
extraction to <output_dir>/<basename>.txt. A `summary.json` and a
Markdown table are also emitted so a downstream screening step can
decide which resumes are high / medium / low quality.

Usage
-----
    python3 resume_pdf_extract.py path/to/resume.pdf --output-dir /tmp/out
    python3 resume_pdf_extract.py path/to/resume_dir --output-dir /tmp/out

Install (any subset works; more backends → better triage):
    pip install --user pymupdf pdfplumber pdfminer.six

License: MIT. See repository LICENSE.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Dict, List, Optional


# Keyword bag used to compute a coarse "is this actually a resume" hit score.
# Tuned for Chinese tech / product / market resumes — extend per locale.
KEYWORDS = [
    "工作经历", "工作经验", "项目经验", "教育背景", "教育经历",
    "实习经历", "实习经验", "技能", "项目", "负责", "主导", "参与",
    "团队", "毕业", "学位", "本科", "硕士", "博士", "GPA",
    "Python", "Java", "C++", "JavaScript", "TypeScript", "Go",
    "算法", "模型", "数据", "产品", "运营", "市场", "增长",
]

# Tracking/decoration patterns we strip from raw text before scoring.
TRACKING_LINE = re.compile(r"^[A-Za-z0-9_\-]{16,}$")
SHORT_FRAGMENT = re.compile(r"^[\s\W]{0,2}[A-Za-z0-9]{1,2}[\s\W]{0,2}$")
# Drop decorative lines made of one repeated glyph, but keep normal Chinese lines.
REPEATED_CHAR_LINE = re.compile(r"^\s*(\S)(?:\s*\1){2,}\s*$")


# ---------------------------------------------------------------------------
# Backend wrappers
# ---------------------------------------------------------------------------


def _try_import(module: str):
    try:
        return __import__(module)
    except Exception:
        return None


def _warn(backend: str, path: Path, err: Exception) -> None:
    print(f"warn: {backend} failed on {path.name}: {type(err).__name__}: {err}",
          file=sys.stderr)


def _extract_fitz(path: Path) -> Optional[str]:
    fitz = _try_import("fitz")
    if fitz is None:
        return None
    try:
        with fitz.open(path) as doc:
            return "\n".join(page.get_text() for page in doc)
    except Exception as e:
        _warn("fitz", path, e)
        return None


def _extract_pdfplumber(path: Path) -> Optional[str]:
    pdfplumber = _try_import("pdfplumber")
    if pdfplumber is None:
        return None
    try:
        chunks: List[str] = []
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                chunks.append(text)
        return "\n".join(chunks)
    except Exception as e:
        _warn("pdfplumber", path, e)
        return None


def _extract_pdfminer(path: Path) -> Optional[str]:
    try:
        from pdfminer.high_level import extract_text  # type: ignore
    except Exception:
        return None
    try:
        return extract_text(str(path))
    except Exception as e:
        _warn("pdfminer", path, e)
        return None


BACKENDS: Dict[str, Callable[[Path], Optional[str]]] = {
    "fitz": _extract_fitz,
    "pdfplumber": _extract_pdfplumber,
    "pdfminer": _extract_pdfminer,
}


# ---------------------------------------------------------------------------
# Cleaning + scoring
# ---------------------------------------------------------------------------


def clean_text(raw: str) -> str:
    """Normalize Unicode, fold whitespace, drop tracking/fragment lines."""
    if not raw:
        return ""
    text = unicodedata.normalize("NFKC", raw)
    text = text.replace("　", " ")
    text = re.sub(r"[ \t]+", " ", text)

    keep: List[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            keep.append("")
            continue
        if TRACKING_LINE.match(stripped):
            continue
        if SHORT_FRAGMENT.match(stripped):
            continue
        if REPEATED_CHAR_LINE.match(stripped):
            continue
        keep.append(stripped)

    cleaned = "\n".join(keep)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


@dataclass
class BackendResult:
    backend: str
    chars: int
    lines: int
    keyword_hits: int
    score: float
    quality: str
    text: str


def score_text(text: str) -> BackendResult:
    if not text:
        return BackendResult("none", 0, 0, 0, 0.0, "low", "")
    lines = [l for l in text.splitlines() if l.strip()]
    chars = len(text)
    line_count = len(lines)
    keyword_hits = sum(1 for kw in KEYWORDS if kw.lower() in text.lower())

    # Score: weighted blend of size + keyword recall, with a noise penalty.
    # Chinese resume PDFs often contain vertical tracking strings split into many
    # one- or two-character lines; without this penalty they can beat clean text.
    size_component = min(chars, 8000) / 80.0          # up to ~100
    line_component = min(line_count, 200) / 2.0       # up to ~100
    keyword_component = min(keyword_hits, 20) * 5.0   # up to ~100
    short_noise = sum(1 for line in lines if len(line.strip()) <= 2)
    noise_ratio = short_noise / max(line_count, 1)
    noise_penalty = min(35.0, noise_ratio * 60.0)
    score = round(max(0.0, (size_component + line_component + keyword_component) / 3.0 - noise_penalty), 2)

    if chars >= 2600 and line_count >= 55 and score >= 65:
        quality = "high"
    elif chars >= 1600 and line_count >= 35 and score >= 35:
        quality = "medium"
    else:
        quality = "low"

    return BackendResult(
        backend="",
        chars=chars,
        lines=line_count,
        keyword_hits=keyword_hits,
        score=score,
        quality=quality,
        text=text,
    )


# ---------------------------------------------------------------------------
# Triage driver
# ---------------------------------------------------------------------------


def triage_pdf(path: Path) -> Dict:
    candidates: List[BackendResult] = []
    for name, fn in BACKENDS.items():
        raw = fn(path)
        if raw is None:
            continue
        cleaned = clean_text(raw)
        result = score_text(cleaned)
        result.backend = name
        candidates.append(result)

    if not candidates:
        return {
            "file": str(path),
            "backend": None,
            "chars": 0,
            "lines": 0,
            "keyword_hits": 0,
            "score": 0.0,
            "quality": "low",
            "reason": "no available backend produced text",
        }

    best = max(candidates, key=lambda r: r.score)
    return {
        "file": str(path),
        "backend": best.backend,
        "chars": best.chars,
        "lines": best.lines,
        "keyword_hits": best.keyword_hits,
        "score": best.score,
        "quality": best.quality,
        "text": best.text,
        "candidates": [
            {
                **{k: v for k, v in asdict(c).items() if k != "text"},
            }
            for c in candidates
        ],
    }


def iter_pdfs(target: Path):
    if target.is_file():
        yield target
        return
    for entry in sorted(target.rglob("*.pdf")):
        if entry.is_file():
            yield entry


def render_markdown(rows: List[Dict]) -> str:
    header = "| 文件 | 后端 | 质量 | 字符数 | 行数 | 关键词命中 | 评分 |\n"
    sep = "| --- | --- | --- | ---: | ---: | ---: | ---: |\n"
    body = "".join(
        "| {file} | {backend} | {quality} | {chars} | {lines} | {kw} | {score} |\n".format(
            file=Path(row["file"]).name,
            backend=row.get("backend") or "—",
            quality=row.get("quality", "low"),
            chars=row.get("chars", 0),
            lines=row.get("lines", 0),
            kw=row.get("keyword_hits", 0),
            score=row.get("score", 0.0),
        )
        for row in rows
    )
    return header + sep + body


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("target", type=Path, help="PDF file or directory")
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="Directory to write best-text .txt files and summary.json")
    parser.add_argument("--no-markdown", action="store_true",
                        help="Suppress the Markdown table on stdout")
    args = parser.parse_args()

    if not args.target.exists():
        print(f"error: target does not exist: {args.target}", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)

    available: List[str] = []
    for name in BACKENDS:
        module_name = {"fitz": "fitz", "pdfplumber": "pdfplumber",
                       "pdfminer": "pdfminer.high_level"}[name]
        try:
            __import__(module_name.split(".")[0])
            available.append(name)
        except Exception:
            pass
    if not available:
        print("error: no PDF backend available. Install at least one of "
              "pymupdf / pdfplumber / pdfminer.six", file=sys.stderr)
        return 2

    rows: List[Dict] = []
    for pdf in iter_pdfs(args.target):
        result = triage_pdf(pdf)
        text = result.pop("text", "") if isinstance(result, dict) else ""
        if result.get("backend"):
            out_path = args.output_dir / f"{pdf.stem}.{result['backend']}.txt"
            out_path.write_text(text, encoding="utf-8")
            result["output"] = str(out_path)
        rows.append(result)

    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2),
                            encoding="utf-8")

    if not args.no_markdown:
        print(render_markdown(rows))

    print(f"\nbackends available: {', '.join(available)}", file=sys.stderr)
    print(f"summary: {summary_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
