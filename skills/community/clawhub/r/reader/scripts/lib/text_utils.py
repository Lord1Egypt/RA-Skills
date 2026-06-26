#!/usr/bin/env python3
import html
import re

def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def normalize_text(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\r', '', text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def load_input(file_path=None, text=None):
    if file_path:
        raw = read_text_file(file_path)
    else:
        raw = text or ""
    return normalize_text(raw)

def sentence_split(text: str):
    parts = re.split(r'(?<=[.!?。！？])\s+', text)
    return [p.strip() for p in parts if p.strip()]

def paragraph_split(text: str):
    return [p.strip() for p in text.split("\n\n") if p.strip()]

def summarize_simple(text: str, max_sentences: int = 3) -> str:
    sentences = sentence_split(text)
    if not sentences:
        return ""
    return " ".join(sentences[:max_sentences])

def extract_key_points(text: str, limit: int = 5):
    paras = paragraph_split(text)
    if paras:
        return paras[:limit]
    return sentence_split(text)[:limit]

def extract_action_items(text: str):
    hits = []
    for sentence in sentence_split(text):
        lower = sentence.lower()
        if (
            lower.startswith("action:") or
            "action:" in lower or
            "todo" in lower or
            "next step" in lower or
            "follow up" in lower or
            "need to" in lower or
            "should" in lower or
            "must" in lower
        ):
            cleaned = re.sub(r'^\s*action:\s*', '', sentence, flags=re.IGNORECASE).strip()
            hits.append(cleaned)
    return hits[:10]

def extract_questions(text: str):
    return [s for s in sentence_split(text) if "?" in s or "？" in s][:10]
