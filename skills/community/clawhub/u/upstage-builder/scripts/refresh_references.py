#!/usr/bin/env python3
"""Refresh upstage-builder reference files from upstream sources.

Usage:
  python skills/upstage-builder/scripts/refresh_references.py
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DIR = ROOT / "references"
API_DOCS_URL = "https://console.upstage.ai/api/docs/for-agents/raw"

SECTION_PATTERNS = {
    "chat-completions.md": [r"^## 1\. Chat Completions API$"],
    "embeddings.md": [r"^## 2\. Embeddings API$"],
    "document-processing.md": [
        r"^## Supported File Formats \(Document APIs\)$",
        r"^## 3\. Document OCR API$",
        r"^## 4\. Document Parse API$",
        r"^## 10\. Document Split API$",
    ],
    "document-classification.md": [r"^## 5\. Document Classification API$"],
    "information-extraction.md": [
        r"^## 6\. Information Extraction API$",
        r"^## 7\. Schema Generation API$",
        r"^## 8\. Prebuilt Information Extraction API$",
    ],
    "agent-api.md": [r"^## 9\. Agent API$"],
    "common-patterns.md": [
        r"^## Error Handling$",
        r"^## Rate Limits$",
        r"^## Supported Languages$",
        r"^## Common Patterns$",
        r"^## Additional Resources$",
    ],
}

TITLES = {
    "chat-completions.md": "Chat Completions API",
    "embeddings.md": "Embeddings API",
    "document-processing.md": "Document Processing APIs",
    "document-classification.md": "Document Classification API",
    "information-extraction.md": "Information Extraction API",
    "agent-api.md": "Agent API",
    "common-patterns.md": "Common Patterns, Errors, and Limits",
}


def fetch_text(url: str) -> str:
    req = Request(url)
    with urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def split_sections(raw: str) -> dict[str, str]:
    lines = raw.splitlines()
    heading_idx: list[tuple[int, str]] = []
    for idx, line in enumerate(lines):
        if line.startswith("## "):
            heading_idx.append((idx, line.strip()))

    sections: dict[str, str] = {}
    for i, (start, heading) in enumerate(heading_idx):
        end = heading_idx[i + 1][0] if i + 1 < len(heading_idx) else len(lines)
        sections[heading] = "\n".join(lines[start:end]).strip() + "\n"
    return sections


def build_api_reference_files(raw: str) -> dict[str, str]:
    sections = split_sections(raw)
    outputs: dict[str, str] = {}
    for filename, patterns in SECTION_PATTERNS.items():
        chunks: list[str] = []
        for pattern in patterns:
            rx = re.compile(pattern)
            matched = [body for heading, body in sections.items() if rx.match(heading)]
            if not matched:
                raise RuntimeError(f"Missing expected section for {filename}: {pattern}")
            chunks.extend(matched)
        outputs[filename] = (
            f"<!-- Source: {API_DOCS_URL} -->\n"
            f"# {TITLES[filename]}\n\n"
            + "\n\n---\n\n".join(chunks)
            + "\n"
        )
    return outputs


def main() -> None:
    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)

    api_raw = fetch_text(API_DOCS_URL)
    for filename, content in build_api_reference_files(api_raw).items():
        (REFERENCE_DIR / filename).write_text(content)
        print(f"updated {filename}")


if __name__ == "__main__":
    main()
