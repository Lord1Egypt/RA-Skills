#!/usr/bin/env python3
"""Lightweight structural checks for generated Word .docx files."""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree

PLACEHOLDER_PATTERNS = (
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
    r"\?\?",
    r"\[\[",
    r"\]\]",
)

# LaTeX control sequences that should never survive into a finished .docx.
# Their presence means pandoc emitted the raw source instead of rendered output.
LATEX_COMMAND_PATTERN = re.compile(
    r"\\(?:cite[a-zA-Z]*|ref|eqref|autoref|cref|Cref|label|textbf|textit|emph|"
    r"section|subsection|subsubsection|begin|end|includegraphics|caption|"
    r"footnote|item|hline|toprule|midrule|bottomrule)\b"
)
# Any LaTeX macro applied to an argument, e.g. \foo{...} — catches custom macros
# (\newcommand) that pandoc could not expand, not just the curated list above.
# Requiring a trailing brace keeps backslashed file paths from matching.
GENERIC_LATEX_MACRO_PATTERN = re.compile(r"\\[a-zA-Z]+\s*\{")
# pandoc citeproc leftovers, e.g. [@smith2020] — citations were never resolved.
CITEPROC_LEFTOVER_PATTERN = re.compile(r"\[@[\w:.\-]+(?:\s*;\s*@[\w:.\-]+)*\]")
# Inline math left as raw LaTeX. Either a `$...$` span with a backslash macro,
# or a tight `$...$` subscript/superscript with no spaces (e.g. $x_i$, $x^2$).
# Currency like "$5 ... file_name ... $10" needs spaces, so it is not matched.
RAW_MATH_PATTERN = re.compile(
    r"\$[^$\n]*\\[a-zA-Z]+[^$\n]*\$|\$[^$\n\s]*[_^][^$\n\s]*\$"
)
# pandoc-crossref renders unresolved \ref/\eqref as a literal "[?]".
BROKEN_CROSSREF = "[?]"

# LaTeX bibliography styles that produce numbered [1] citations. If the source
# uses one of these but the docx rendered author-date (citeproc's default), the
# Word citations silently diverge from the compiled PDF.
NUMERIC_BIB_STYLES = frozenset({
    "plain", "unsrt", "abbrv", "ieeetr", "ieee", "ieeetran", "acm", "siam", "vancouver",
})
BIBSTYLE_PATTERN = re.compile(r"\\bibliographystyle\{([^}]+)\}")
NUMERIC_CITE_PATTERN = re.compile(r"\[\d+(?:\s*[,–-]\s*\d+)*\]")
AUTHOR_DATE_CITE_PATTERN = re.compile(r"\([A-Z][A-Za-z'’.-]+(?:\s+et al\.?)?,?\s+\d{4}[a-z]?\)")


def citation_style_finding(docx_text: str, source_tex: str) -> str | None:
    """Warn when a numeric \\bibliographystyle renders as author-date in Word.

    citeproc defaults to author-date, so a numeric LaTeX style needs an explicit
    numeric CSL (e.g. --csl=ieee.csl) or the docx citations will not match the
    PDF's [1] style. Conservative: only fires when the source is numeric AND the
    docx clearly shows author-date citations with no numbered ones.
    """
    if not source_tex:
        return None
    match = BIBSTYLE_PATTERN.search(source_tex)
    if not match or match.group(1).strip().lower() not in NUMERIC_BIB_STYLES:
        return None
    if AUTHOR_DATE_CITE_PATTERN.search(docx_text) and not NUMERIC_CITE_PATTERN.search(docx_text):
        return (
            f"Citation style mismatch: source uses numeric \\bibliographystyle{{{match.group(1).strip()}}} "
            "but the Word citations render author-date. Pass a numeric CSL "
            "(e.g. --csl=ieee.csl) so Word matches the PDF's [1] style."
        )
    return None


@dataclass
class WordGuardResult:
    path: str
    ok: bool
    text_length: int
    paragraph_count: int
    findings: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check a generated .docx file.")
    parser.add_argument("docx_path")
    parser.add_argument("--min-chars", type=int, default=200)
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", type=Path, help="Optional report path.")
    return parser.parse_args()


def extract_text(document_xml: bytes) -> tuple[str, int]:
    root = ElementTree.fromstring(document_xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs: list[str] = []
    for paragraph in root.findall(".//w:p", ns):
        parts = [node.text or "" for node in paragraph.findall(".//w:t", ns)]
        text = "".join(parts).strip()
        if text:
            paragraphs.append(text)
    return "\n".join(paragraphs), len(paragraphs)


def check_docx(path: Path, min_chars: int, source_tex: str = "") -> WordGuardResult:
    findings: list[str] = []
    text = ""
    paragraph_count = 0

    if not path.exists():
        return WordGuardResult(str(path), False, 0, 0, ["file does not exist"])
    if path.suffix.lower() != ".docx":
        findings.append("file extension is not .docx")

    names: set[str] = set()
    try:
        with zipfile.ZipFile(path) as docx:
            names = set(docx.namelist())
            for required in ("[Content_Types].xml", "word/document.xml"):
                if required not in names:
                    findings.append(f"missing {required}")
            if "word/document.xml" in names:
                text, paragraph_count = extract_text(docx.read("word/document.xml"))
    except zipfile.BadZipFile:
        return WordGuardResult(str(path), False, 0, 0, ["not a valid zip/docx file"])
    except ElementTree.ParseError as exc:
        findings.append(f"word/document.xml parse error: {exc}")

    if len(text) < min_chars:
        findings.append(f"text is too short: {len(text)} chars < {min_chars}")
    if paragraph_count == 0:
        findings.append("no non-empty paragraphs found — docx may be empty or corrupted")
        # Check if images exist but text was lost (broken image conversion)
        has_images = any(name.startswith("word/media/") for name in names)
        if has_images:
            findings.append(
                "Images found in docx but no text — pandoc image conversion likely failed. "
                "Verify: (1) images are PNG/JPG format, (2) `--resource-path` and `--extract-media` flags used, "
                "(3) pandoc ran from the `final_paper/` directory so relative paths resolve."
            )
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            findings.append(f"unresolved placeholder pattern found: {pattern}")

    # Formatting correctness: raw LaTeX must not leak into the rendered docx.
    latex_tokens: set[str] = {m.group(0) for m in LATEX_COMMAND_PATTERN.finditer(text)}
    latex_tokens.update(m.group(0).rstrip("{").strip() for m in GENERIC_LATEX_MACRO_PATTERN.finditer(text))
    if latex_tokens:
        sample = ", ".join(sorted(latex_tokens)[:6])
        findings.append(
            f"Unrendered LaTeX commands in text (e.g. {sample}) — pandoc emitted raw source "
            "instead of rendered output. Flatten \\input/\\include and expand custom macros "
            "(\\newcommand) before conversion."
        )
    if BROKEN_CROSSREF in text:
        findings.append(
            "Broken cross-references '[?]' — \\ref/\\eqref did not resolve. "
            "Add `--filter pandoc-crossref` (and matching \\label definitions)."
        )
    citeproc_hits = CITEPROC_LEFTOVER_PATTERN.findall(text)
    if citeproc_hits:
        findings.append(
            f"Unresolved citation markers found ({len(citeproc_hits)}, e.g. {citeproc_hits[0]}). "
            "Run pandoc with --citeproc and --bibliography=references.bib so citations render."
        )
    if RAW_MATH_PATTERN.search(text):
        findings.append(
            "Raw inline LaTeX math (e.g. `$\\alpha$`) survived into the docx — math was not "
            "converted to Word equations. Verify the source compiles and pandoc handled the math."
        )

    # Chinese encoding checks: detect garbled text / mojibake
    has_chinese = bool(re.search(r"[一-鿿]", text))
    if has_chinese:
        garbled = re.findall(r"[\x80-\xff]{4,}", text)
        if garbled:
            findings.append(f"Possible garbled Chinese text: {len(garbled)} suspicious byte sequences. Re-export with UTF-8 encoding.")
        # Check for common encoding corruption patterns
        corruption = re.findall(r"鍚堛[劧渚佃繚閫嗘]", text)  # common gbk-decoded-as-utf8 pattern
        if corruption:
            findings.append("Chinese encoding corruption detected: GBK text decoded as UTF-8. Re-export with proper encoding.")

    style_finding = citation_style_finding(text, source_tex)
    if style_finding:
        findings.append(style_finding)

    return WordGuardResult(str(path), not findings, len(text), paragraph_count, findings)


def to_markdown(result: WordGuardResult) -> str:
    lines = [
        "# Word Guard Report",
        "",
        f"- Path: `{result.path}`",
        f"- Status: {'PASS' if result.ok else 'FAIL'}",
        f"- Text length: {result.text_length}",
        f"- Paragraph count: {result.paragraph_count}",
        "",
        "## Findings",
        "",
    ]
    if result.findings:
        lines.extend(f"- {finding}" for finding in result.findings)
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    docx_path = Path(args.docx_path)
    source_tex = ""
    sibling_tex = docx_path.parent / "main.tex"
    if sibling_tex.exists():
        source_tex = sibling_tex.read_text(encoding="utf-8", errors="ignore")
    result = check_docx(docx_path, args.min_chars, source_tex)
    markdown = to_markdown(result)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")

    if args.json:
        print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
    if args.markdown or not args.json:
        print(markdown)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
