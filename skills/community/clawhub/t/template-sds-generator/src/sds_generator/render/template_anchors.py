from __future__ import annotations

import re

from docx.document import Document as DocumentType


def normalize_anchor_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def body_anchor_texts(document: DocumentType) -> list[str]:
    return [normalize_anchor_text(paragraph.text) for paragraph in document.paragraphs if normalize_anchor_text(paragraph.text)]


def find_missing_anchors(document: DocumentType, required_anchors: list[str]) -> list[str]:
    available = set(body_anchor_texts(document))
    return [anchor for anchor in required_anchors if normalize_anchor_text(anchor) not in available]


def find_anchor_occurrences(document: DocumentType, required_anchors: list[str]) -> dict[str, int]:
    available = body_anchor_texts(document)
    counts = {anchor: 0 for anchor in required_anchors}
    for text in available:
        for anchor in required_anchors:
            if text == normalize_anchor_text(anchor):
                counts[anchor] += 1
    return counts


def ordered_anchor_paragraphs(document: DocumentType, anchor_texts: list[str]) -> list[tuple[str, object]]:
    normalized = {normalize_anchor_text(anchor): anchor for anchor in anchor_texts}
    ordered: list[tuple[str, object]] = []
    for paragraph in document.paragraphs:
        text = normalize_anchor_text(paragraph.text)
        if text in normalized:
            ordered.append((normalized[text], paragraph))
    return ordered
