#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Iterable


EMBEDDING_MODEL = "text-embedding-v4"
RERANK_MODEL = "qwen3-rerank"
EMBEDDING_DIMENSIONS = 1024
DEFAULT_ROOT_DIR = "/var/openclaw-kb"
DEFAULT_TOPK = 10
DEFAULT_TOPN = 10
DEFAULT_RETRIEVAL_MODE = "hybrid"
EMBEDDING_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings"
RERANK_URL = "https://dashscope.aliyuncs.com/compatible-api/v1/reranks"
BM25_K1 = 1.2
BM25_B = 0.75
RRF_K = 60
TOKENIZER_NAME = "jieba_v1"
RETRIEVAL_MODES = {"semantic", "keyword", "hybrid"}
DEFAULT_PROTECTED_TOKEN_PATTERN = r"[A-Za-z0-9]+(?:[._:/-][A-Za-z0-9]+)*"
PROTECTED_TERMS_KEY = "protected_terms"


class KBError(RuntimeError):
    pass


def load_requests():
    try:
        import requests
    except ImportError as exc:
        raise KBError("Missing dependency 'requests'. Run: python3 -m pip install -r requirements.txt") from exc
    return requests


def load_numpy():
    try:
        import numpy as np
    except ImportError as exc:
        raise KBError("Missing dependency 'numpy'. Run: python3 -m pip install -r requirements.txt") from exc
    return np


def load_faiss():
    try:
        import faiss
    except ImportError as exc:
        raise KBError("Missing dependency 'faiss-cpu'. Run: python3 -m pip install -r requirements.txt") from exc
    return faiss


def load_jieba():
    try:
        import jieba
    except ImportError as exc:
        raise KBError("Missing dependency 'jieba'. Run: python3 -m pip install -r requirements.txt") from exc
    return jieba


def now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data, *, indent: int | None = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        if indent is None:
            json.dump(data, handle, ensure_ascii=False, separators=(",", ":"))
        else:
            json.dump(data, handle, ensure_ascii=False, indent=indent)


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def collapse_text(text: str) -> str:
    return re.sub(r"\s+", " ", normalize_text(text)).strip()


def stable_id(*parts: str) -> str:
    payload = "\n".join(parts).encode("utf-8")
    return hashlib.sha1(payload).hexdigest()


def file_sha1(path: Path) -> str:
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sanitize_component(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._\-\u4e00-\u9fff]+", "_", name.strip())
    cleaned = re.sub(r"_+", "_", cleaned)
    cleaned = cleaned.strip(" ._")
    return cleaned or "file"


def load_api_key() -> str:
    api_key = os.getenv("BAILIAN-SK") or os.getenv("BAILIAN_SK")
    if not api_key:
        raise KBError("Missing API key. Set environment variable BAILIAN-SK or BAILIAN_SK.")
    return api_key


def kb_dir(root_dir: Path, kb_name: str) -> Path:
    safe_kb = sanitize_component(kb_name)
    return root_dir / safe_kb


def kb_paths(root_dir: Path, kb_name: str) -> dict[str, Path]:
    root = kb_dir(root_dir, kb_name)
    return {
        "root": root,
        "config": root / "config.json",
        "protected_terms": root / "protected_terms.json",
        "manifest": root / "manifest.json",
        "vectors": root / "vectors.jsonl",
        "index": root / "index.faiss",
        "bm25": root / "bm25.json",
    }


def normalize_retrieval_mode(value: str | None) -> str:
    mode = (value or DEFAULT_RETRIEVAL_MODE).strip().lower()
    if mode not in RETRIEVAL_MODES:
        allowed = ", ".join(sorted(RETRIEVAL_MODES))
        raise KBError(f"Unsupported retrieval mode: {value}. Expected one of: {allowed}")
    return mode


def normalize_protected_term(term: str) -> str:
    value = collapse_text(term)
    if not value:
        raise KBError("Protected term must not be empty.")
    return value


def normalize_protected_terms(terms: Iterable[str] | None) -> list[str]:
    ordered_terms = []
    seen = set()
    for raw in terms or []:
        term = normalize_protected_term(str(raw))
        key = term.casefold()
        if key in seen:
            continue
        seen.add(key)
        ordered_terms.append(term)
    return ordered_terms


def default_kb_config(root_dir: Path, kb_name: str) -> dict:
    return {
        "root_dir": str(root_dir),
        "kb_name": kb_name,
        "embedding_model": EMBEDDING_MODEL,
        "embedding_dimensions": EMBEDDING_DIMENSIONS,
        "rerank_model": RERANK_MODEL,
        "retrieval_mode": DEFAULT_RETRIEVAL_MODE,
        "bm25_k1": BM25_K1,
        "bm25_b": BM25_B,
        "bm25_tokenizer": TOKENIZER_NAME,
        "topk": DEFAULT_TOPK,
        "topN": DEFAULT_TOPN,
        "updated_at": now_iso(),
    }


def read_kb_protected_terms(paths: dict[str, Path], *, fallback_config: dict | None = None) -> list[str]:
    protected_terms = read_json(paths["protected_terms"], default=None)
    if protected_terms is None:
        return normalize_protected_terms((fallback_config or {}).get(PROTECTED_TERMS_KEY, []))
    if not isinstance(protected_terms, list):
        raise KBError(f"{paths['protected_terms']} must contain a JSON array of protected terms.")
    return normalize_protected_terms(protected_terms)


def write_kb_protected_terms(paths: dict[str, Path], terms: Iterable[str]) -> None:
    write_json(paths["protected_terms"], normalize_protected_terms(terms))


def write_kb_config(paths: dict[str, Path], config: dict) -> None:
    payload = dict(config)
    payload.pop(PROTECTED_TERMS_KEY, None)
    write_json(paths["config"], payload)


def normalize_kb_config(
    config: dict | None,
    root_dir: Path,
    kb_name: str,
    *,
    topk: int | None = None,
    topn: int | None = None,
    protected_terms: Iterable[str] | None = None,
) -> dict:
    normalized = dict(config or default_kb_config(root_dir, kb_name))
    normalized["root_dir"] = str(root_dir)
    normalized["kb_name"] = kb_name
    normalized["embedding_model"] = EMBEDDING_MODEL
    normalized["embedding_dimensions"] = EMBEDDING_DIMENSIONS
    normalized["rerank_model"] = RERANK_MODEL
    normalized["retrieval_mode"] = normalize_retrieval_mode(normalized.get("retrieval_mode", DEFAULT_RETRIEVAL_MODE))
    normalized["bm25_k1"] = BM25_K1
    normalized["bm25_b"] = BM25_B
    normalized["bm25_tokenizer"] = TOKENIZER_NAME
    normalized[PROTECTED_TERMS_KEY] = normalize_protected_terms(
        protected_terms if protected_terms is not None else normalized.get(PROTECTED_TERMS_KEY, [])
    )
    normalized["topk"] = normalize_positive(topk if topk is not None else normalized.get("topk", DEFAULT_TOPK), "topk")
    normalized["topN"] = normalize_positive(topn if topn is not None else normalized.get("topN", DEFAULT_TOPN), "topN")
    if normalized["topN"] > normalized["topk"]:
        raise KBError("topN must be less than or equal to topk.")
    normalized["updated_at"] = normalized.get("updated_at", now_iso())
    return normalized


def load_kb_config(root_dir: Path, kb_name: str) -> dict:
    paths = kb_paths(root_dir, kb_name)
    config = read_json(paths["config"], default=None)
    if config is None:
        raise KBError(f"Knowledge base config not found: {kb_name}")
    protected_terms = read_kb_protected_terms(paths, fallback_config=config)
    return normalize_kb_config(config, root_dir, kb_name, protected_terms=protected_terms)


def ensure_kb_config(
    root_dir: Path,
    kb_name: str,
    *,
    topk: int | None = None,
    topn: int | None = None,
) -> dict:
    paths = kb_paths(root_dir, kb_name)
    paths["root"].mkdir(parents=True, exist_ok=True)
    raw_config = read_json(paths["config"], default=None)
    protected_terms = read_kb_protected_terms(paths, fallback_config=raw_config)
    config = normalize_kb_config(raw_config, root_dir, kb_name, topk=topk, topn=topn, protected_terms=protected_terms)
    config["updated_at"] = now_iso()
    write_kb_config(paths, config)
    if not paths["protected_terms"].exists():
        write_kb_protected_terms(paths, config.get(PROTECTED_TERMS_KEY, []))
    return config


def validate_doc_dir(doc_dir: Path, kb_root: Path, kb_name: str) -> Path:
    expected_parent = kb_dir(kb_root, kb_name)
    doc_dir = doc_dir.resolve()
    if doc_dir.parent != expected_parent.resolve():
        raise KBError(f"Document directory must be directly under {expected_parent}")
    return doc_dir


def parse_doc_dir_name(doc_dir: Path) -> tuple[str, str]:
    match = re.match(r"^(\d{12})-(.+)$", doc_dir.name)
    if not match:
        raise KBError("Document directory must match '{ts}-{safe_name}' with ts formatted as yyyyMMddhhmm.")
    return match.group(1), match.group(2)


def find_doc_text_file(doc_dir: Path, safe_name: str) -> Path:
    preferred_candidates = [
        doc_dir / f"{safe_name}.md",
        doc_dir / f"{safe_name}.txt",
    ]
    for candidate in preferred_candidates:
        if candidate.exists():
            return candidate
    fallback_candidates = [
        entry
        for entry in sorted(doc_dir.iterdir(), key=lambda item: item.name)
        if entry.is_file() and entry.name != "summary.txt" and entry.suffix.lower() in {".md", ".txt"}
    ]
    if fallback_candidates:
        return fallback_candidates[0]
    raise KBError(f"Extracted text file not found in {doc_dir}. Expected {safe_name}.md or {safe_name}.txt")


def read_summary(doc_dir: Path) -> str:
    summary_path = doc_dir / "summary.txt"
    if not summary_path.exists():
        return ""
    summary = collapse_text(summary_path.read_text(encoding="utf-8", errors="ignore"))
    if len(summary) > 200:
        raise KBError(f"Summary exceeds 200 characters: {summary_path}")
    return summary


def parse_chunk_id(path: Path) -> str:
    match = re.fullmatch(r"chunk-(\d{5})\.md", path.name)
    if not match:
        raise KBError(f"Invalid chunk filename: {path.name}")
    return match.group(1)


def parse_t2q_name(path: Path) -> tuple[str, str]:
    match = re.fullmatch(r"(\d{5})-q-(\d+)\.md", path.name)
    if not match:
        raise KBError(f"Invalid T2Q filename: {path.name}")
    return match.group(1), match.group(2)


def read_markdown_file(path: Path) -> str:
    return normalize_text(path.read_text(encoding="utf-8", errors="ignore"))


def is_cjk_char(char: str) -> bool:
    return "\u4e00" <= char <= "\u9fff"


def clean_lexical_token(token: str) -> str:
    token = token.strip().lower()
    token = token.strip("`*_#>~[](){}<>\"'.,;:!?，。；：！？、|\\/=+·")
    return token


def should_keep_lexical_token(token: str) -> bool:
    if not token:
        return False
    if not any(char.isalnum() or is_cjk_char(char) for char in token):
        return False
    if all(is_cjk_char(char) for char in token) and len(token) <= 1:
        return False
    if token.isdigit() and len(token) <= 1:
        return False
    return True


@lru_cache(maxsize=128)
def compile_protected_token_re(protected_terms: tuple[str, ...]) -> re.Pattern[str]:
    custom_patterns = [re.escape(term) for term in sorted(protected_terms, key=lambda item: (-len(item), item.casefold()))]
    patterns = custom_patterns + [DEFAULT_PROTECTED_TOKEN_PATTERN]
    return re.compile("|".join(patterns), re.IGNORECASE)


def build_protected_token_matcher(protected_terms: Iterable[str] | None = None) -> re.Pattern[str]:
    return compile_protected_token_re(tuple(normalize_protected_terms(protected_terms)))


def tokenize_lexical_segment(text: str, *, jieba_module=None) -> list[str]:
    if not text.strip():
        return []
    jieba = jieba_module or load_jieba()
    tokens = []
    for raw in jieba.lcut(text, cut_all=False):
        token = clean_lexical_token(raw)
        if should_keep_lexical_token(token):
            tokens.append(token)
    return tokens


def tokenize_for_bm25(
    text: str,
    *,
    protected_terms: Iterable[str] | None = None,
    matcher: re.Pattern[str] | None = None,
    jieba_module=None,
) -> list[str]:
    text = normalize_text(text)
    tokens = []
    last = 0
    compiled_matcher = matcher or build_protected_token_matcher(protected_terms)
    jieba = jieba_module or load_jieba()
    for match in compiled_matcher.finditer(text):
        tokens.extend(tokenize_lexical_segment(text[last : match.start()], jieba_module=jieba))
        token = clean_lexical_token(match.group(0))
        if should_keep_lexical_token(token):
            tokens.append(token)
        last = match.end()
    tokens.extend(tokenize_lexical_segment(text[last:], jieba_module=jieba))
    return tokens


def chunk_records_only(records: list[dict]) -> list[dict]:
    return [item for item in records if item["kind"] == "chunk"]


def build_bm25_index(chunk_records: list[dict], *, protected_terms: Iterable[str] | None = None) -> dict:
    normalized_protected_terms = normalize_protected_terms(protected_terms)
    matcher = build_protected_token_matcher(normalized_protected_terms)
    jieba = load_jieba()
    postings: dict[str, list[list[str | int]]] = defaultdict(list)
    doc_lengths: dict[str, int] = {}
    total_terms = 0
    for record in chunk_records:
        tokens = tokenize_for_bm25(
            record["text"],
            matcher=matcher,
            jieba_module=jieba,
        )
        doc_lengths[record["id"]] = len(tokens)
        total_terms += len(tokens)
        if not tokens:
            continue
        frequencies = Counter(tokens)
        for term, tf in frequencies.items():
            postings[term].append([record["id"], int(tf)])
    for term in postings:
        postings[term].sort(key=lambda item: item[0])
    doc_count = len(chunk_records)
    return {
        "schema_version": 1,
        "tokenizer": TOKENIZER_NAME,
        "k1": BM25_K1,
        "b": BM25_B,
        "protected_terms": normalized_protected_terms,
        "doc_count": doc_count,
        "avgdl": (float(total_terms) / doc_count) if doc_count else 0.0,
        "doc_lengths": doc_lengths,
        "postings": dict(sorted(postings.items())),
    }


def collect_doc_records(kb_name: str, doc_dir: Path) -> tuple[list[dict], dict]:
    ts, safe_name = parse_doc_dir_name(doc_dir)
    text_path = find_doc_text_file(doc_dir, safe_name)
    summary_path = doc_dir / "summary.txt"
    chunks_dir = doc_dir / "chunks"
    t2q_dir = doc_dir / "t2q"
    if not chunks_dir.is_dir():
        raise KBError(f"Chunks directory not found: {chunks_dir}")
    if not t2q_dir.is_dir():
        raise KBError(f"T2Q directory not found: {t2q_dir}")

    summary = read_summary(doc_dir)
    text_sha1 = file_sha1(text_path)
    total_chunk_count = len(list(chunks_dir.glob("chunk-*.md")))
    chunk_records = []
    chunk_lookup = {}
    for chunk_path in sorted(chunks_dir.glob("chunk-*.md")):
        chunk_id = parse_chunk_id(chunk_path)
        text = read_markdown_file(chunk_path)
        record = {
            "id": stable_id(kb_name, doc_dir.name, "chunk", chunk_id, text),
            "kb": kb_name,
            "doc_id": doc_dir.name,
            "file_name": text_path.name,
            "uploaded_at": ts,
            "kind": "chunk",
            "chunk_id": chunk_id,
            "q_id": None,
            "path": str(chunk_path),
            "source_md_path": str(text_path),
            "source_file_path": str(text_path),
            "summary_path": str(summary_path),
            "summary": summary,
            "raw_sha1": text_sha1,
            "markdown_sha1": text_sha1,
            "chunk_count": total_chunk_count,
            "target_chunk_path": str(chunk_path),
            "text": text,
        }
        chunk_records.append(record)
        chunk_lookup[chunk_id] = record

    t2q_records = []
    for question_path in sorted(t2q_dir.glob("*.md")):
        chunk_id, q_id = parse_t2q_name(question_path)
        if chunk_id not in chunk_lookup:
            raise KBError(f"T2Q file {question_path.name} references missing chunk {chunk_id}")
        text = collapse_text(question_path.read_text(encoding="utf-8", errors="ignore"))
        if not text:
            continue
        t2q_records.append(
            {
                "id": stable_id(kb_name, doc_dir.name, "t2q", chunk_id, q_id, text),
                "kb": kb_name,
                "doc_id": doc_dir.name,
                "file_name": text_path.name,
                "uploaded_at": ts,
                "kind": "t2q",
                "chunk_id": chunk_id,
                "q_id": q_id,
                "path": str(question_path),
                "source_md_path": str(text_path),
                "source_file_path": str(text_path),
                "summary_path": str(summary_path),
                "summary": summary,
                "raw_sha1": text_sha1,
                "markdown_sha1": text_sha1,
                "chunk_count": total_chunk_count,
                "target_chunk_path": chunk_lookup[chunk_id]["path"],
                "text": text,
            }
        )

    summary_record = {
        "doc_id": doc_dir.name,
        "file_name": text_path.name,
        "uploaded_at": ts,
        "source_file_path": str(text_path),
        "source_md_path": str(text_path),
        "summary_path": str(summary_path),
        "summary": summary,
        "chunk_count": len(chunk_records),
        "t2q_count": len(t2q_records),
        "raw_sha1": text_sha1,
        "markdown_sha1": text_sha1,
    }
    return chunk_records + t2q_records, summary_record


def collect_doc_manifest_only(kb_name: str, doc_dir: Path) -> dict:
    _, summary_record = collect_doc_records(kb_name, doc_dir)
    return summary_record


def summarize_documents_from_records(records: list[dict]) -> list[dict]:
    documents = {}
    for item in records:
        document = documents.setdefault(
            item["doc_id"],
            {
                "doc_id": item["doc_id"],
                "file_name": item["file_name"],
                "uploaded_at": item["uploaded_at"],
                "source_file_path": item["source_file_path"],
                "source_md_path": item["source_md_path"],
                "summary_path": item["summary_path"],
                "summary": item.get("summary", ""),
                "chunk_count": 0,
                "t2q_count": 0,
                "raw_sha1": item.get("raw_sha1"),
                "markdown_sha1": item.get("markdown_sha1"),
            },
        )
        if item["kind"] == "chunk":
            document["chunk_count"] += 1
        elif item["kind"] == "t2q":
            document["t2q_count"] += 1
    return sorted(documents.values(), key=lambda item: item["doc_id"])


def list_doc_dirs(kb_root: Path, kb_name: str) -> list[Path]:
    root = kb_dir(kb_root, kb_name)
    if not root.exists():
        return []
    return [
        entry
        for entry in sorted(root.iterdir(), key=lambda item: item.name)
        if entry.is_dir() and re.match(r"^\d{12}-.+", entry.name)
    ]


def embed_texts(texts: list[str], batch_size: int = 10) -> list[list[float]]:
    if not texts:
        return []
    requests = load_requests()
    api_key = load_api_key()
    outputs: list[list[float]] = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        payload = {
            "model": EMBEDDING_MODEL,
            "input": batch,
            "dimensions": EMBEDDING_DIMENSIONS,
            "encoding_format": "float",
        }
        response = requests.post(
            EMBEDDING_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=120,
        )
        if response.status_code >= 400:
            raise KBError(f"Embedding request failed: {response.status_code} {response.text}")
        body = response.json()
        if "error" in body:
            raise KBError(f"Embedding request failed: {json.dumps(body['error'], ensure_ascii=False)}")
        outputs.extend(item["embedding"] for item in sorted(body.get("data", []), key=lambda item: item["index"]))
    return outputs


def attach_missing_embeddings(records: list[dict]) -> list[dict]:
    missing_indices = [idx for idx, item in enumerate(records) if "embedding" not in item or not item["embedding"]]
    if not missing_indices:
        return records
    embeddings = embed_texts([records[idx]["text"] for idx in missing_indices])
    if len(embeddings) != len(missing_indices):
        raise KBError("Embedding count mismatch while persisting records.")
    for idx, embedding in zip(missing_indices, embeddings):
        records[idx]["embedding"] = embedding
    return records


def prepare_query_vector(query: str):
    np = load_numpy()
    faiss = load_faiss()
    query_vector = np.asarray([embed_texts([query])[0]], dtype="float32")
    faiss.normalize_L2(query_vector)
    return query_vector


def prepare_keyword_query_terms(query: str, *, protected_terms: Iterable[str] | None = None) -> Counter[str]:
    normalized_protected_terms = normalize_protected_terms(protected_terms)
    return Counter(
        tokenize_for_bm25(
            query,
            matcher=build_protected_token_matcher(normalized_protected_terms),
            jieba_module=load_jieba(),
        )
    )


def rerank_documents(query: str, documents: list[str], top_n: int) -> list[dict]:
    if not documents:
        return []
    requests = load_requests()
    api_key = load_api_key()
    payload = {
        "model": RERANK_MODEL,
        "query": query,
        "documents": documents[:200],
        "top_n": min(top_n, len(documents[:200])),
        "instruct": "Given a user query, rank the most relevant passages for retrieval.",
    }
    response = requests.post(
        RERANK_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    if response.status_code >= 400:
        raise KBError(f"Rerank request failed: {response.status_code} {response.text}")
    body = response.json()
    if "error" in body:
        raise KBError(f"Rerank request failed: {json.dumps(body['error'], ensure_ascii=False)}")
    output = body.get("output", {})
    return [
        {"index": item["index"], "relevance_score": item["relevance_score"]}
        for item in output.get("results", body.get("results", []))
    ]


def write_faiss_index(index_path: Path, embeddings: list[list[float]]) -> None:
    np = load_numpy()
    faiss = load_faiss()
    vectors = np.asarray(embeddings, dtype="float32")
    if vectors.ndim != 2 or vectors.shape[1] != EMBEDDING_DIMENSIONS:
        raise KBError(f"Unexpected embedding matrix shape: {vectors.shape}")
    faiss.normalize_L2(vectors)
    index = faiss.IndexFlatIP(EMBEDDING_DIMENSIONS)
    index.add(vectors)
    faiss.write_index(index, str(index_path))


def persist_kb_artifacts(paths: dict[str, Path], records: list[dict], manifest: dict, *, protected_terms: Iterable[str] | None = None) -> None:
    if records:
        attach_missing_embeddings(records)
        write_jsonl(paths["vectors"], records)
        write_faiss_index(paths["index"], [item["embedding"] for item in records])
        write_json(paths["bm25"], build_bm25_index(chunk_records_only(records), protected_terms=protected_terms), indent=None)
    else:
        write_jsonl(paths["vectors"], [])
        if paths["index"].exists():
            paths["index"].unlink()
        if paths["bm25"].exists():
            paths["bm25"].unlink()
    write_json(paths["manifest"], manifest)


def load_kb_bundle(
    kb_root: Path,
    kb_name: str,
    *,
    load_vector_index: bool,
    load_bm25_index: bool,
    config: dict | None = None,
) -> tuple[dict, list[dict], object | None, dict | None]:
    paths = kb_paths(kb_root, kb_name)
    effective_config = config or load_kb_config(kb_root, kb_name)
    vectors = read_jsonl(paths["vectors"])
    index = None
    if load_vector_index and paths["index"].exists():
        faiss = load_faiss()
        index = faiss.read_index(str(paths["index"]))
    bm25_index = None
    if load_bm25_index:
        bm25_index = read_json(paths["bm25"], default=None)
        if bm25_index is None:
            bm25_index = build_bm25_index(chunk_records_only(vectors), protected_terms=effective_config.get(PROTECTED_TERMS_KEY, []))
    return effective_config, vectors, index, bm25_index


def build_kb_manifest(root_dir: Path, kb_name: str, config: dict, records: list[dict], *, extra: dict | None = None) -> dict:
    document_summaries = summarize_documents_from_records(records)
    manifest = {
        "kb_name": kb_name,
        "root_dir": str(root_dir),
        "indexed_at": now_iso(),
        "embedding_model": EMBEDDING_MODEL,
        "embedding_dimensions": EMBEDDING_DIMENSIONS,
        "rerank_model": RERANK_MODEL,
        "retrieval_mode": config["retrieval_mode"],
        "bm25_k1": BM25_K1,
        "bm25_b": BM25_B,
        "bm25_tokenizer": TOKENIZER_NAME,
        PROTECTED_TERMS_KEY: config.get(PROTECTED_TERMS_KEY, []),
        "topk": config["topk"],
        "topN": config["topN"],
        "protected_term_count": len(config.get(PROTECTED_TERMS_KEY, [])),
        "document_count": len(document_summaries),
        "vector_count": len(records),
        "chunk_count": sum(1 for item in records if item["kind"] == "chunk"),
        "t2q_count": sum(1 for item in records if item["kind"] == "t2q"),
        "bm25_doc_count": sum(1 for item in records if item["kind"] == "chunk"),
        "documents": document_summaries,
    }
    if extra:
        manifest.update(extra)
    return manifest


def index_kb(root_dir: Path, kb_name: str, doc_dir: Path, *, topk: int | None, topn: int | None) -> dict:
    config = ensure_kb_config(root_dir, kb_name, topk=topk, topn=topn)
    doc_dir = validate_doc_dir(doc_dir, root_dir, kb_name)
    paths = kb_paths(root_dir, kb_name)
    doc_records, doc_manifest = collect_doc_records(kb_name, doc_dir)
    existing_records = [item for item in read_jsonl(paths["vectors"]) if item["doc_id"] != doc_manifest["doc_id"]]
    merged_records = existing_records + doc_records
    merged_records.sort(key=lambda item: (item["doc_id"], item["kind"], item["chunk_id"] or "", item["q_id"] or ""))
    manifest = build_kb_manifest(root_dir, kb_name, config, merged_records)
    persist_kb_artifacts(paths, merged_records, manifest, protected_terms=config.get(PROTECTED_TERMS_KEY, []))
    return manifest


def rebuild_kb(root_dir: Path, kb_name: str, *, topk: int | None, topn: int | None) -> dict:
    config = ensure_kb_config(root_dir, kb_name, topk=topk, topn=topn)
    paths = kb_paths(root_dir, kb_name)
    records = []
    for doc_dir in list_doc_dirs(root_dir, kb_name):
        doc_records, _ = collect_doc_records(kb_name, doc_dir)
        records.extend(doc_records)
    records.sort(key=lambda item: (item["doc_id"], item["kind"], item["chunk_id"] or "", item["q_id"] or ""))
    manifest = build_kb_manifest(
        root_dir,
        kb_name,
        config,
        records,
        extra={"rebuilt": True},
    )
    persist_kb_artifacts(paths, records, manifest, protected_terms=config.get(PROTECTED_TERMS_KEY, []))
    return manifest


def delete_from_index(root_dir: Path, kb_name: str, doc_id: str) -> dict:
    paths = kb_paths(root_dir, kb_name)
    config = load_kb_config(root_dir, kb_name)
    existing_records = read_jsonl(paths["vectors"])
    if not existing_records and not paths["manifest"].exists():
        raise KBError(f"Knowledge base index not found: {kb_name}")

    remaining_records = [item for item in existing_records if item["doc_id"] != doc_id]
    deleted_count = len(existing_records) - len(remaining_records)
    manifest = build_kb_manifest(
        root_dir,
        kb_name,
        config,
        remaining_records,
        extra={
            "deleted_doc_id": doc_id,
            "deleted_vector_count": deleted_count,
        },
    )
    persist_kb_artifacts(paths, remaining_records, manifest, protected_terms=config.get(PROTECTED_TERMS_KEY, []))
    return manifest


def refresh_keyword_assets(root_dir: Path, kb_name: str, config: dict, *, extra: dict | None = None) -> dict:
    paths = kb_paths(root_dir, kb_name)
    records = read_jsonl(paths["vectors"])
    manifest = build_kb_manifest(root_dir, kb_name, config, records, extra=extra)
    if records:
        write_json(paths["bm25"], build_bm25_index(chunk_records_only(records), protected_terms=config.get(PROTECTED_TERMS_KEY, [])), indent=None)
    elif paths["bm25"].exists():
        paths["bm25"].unlink()
    write_json(paths["manifest"], manifest)
    return manifest


def add_protected_terms(root_dir: Path, kb_name: str, terms: Iterable[str]) -> dict:
    config = ensure_kb_config(root_dir, kb_name)
    requested_terms = normalize_protected_terms(terms)
    existing_terms = list(config.get(PROTECTED_TERMS_KEY, []))
    seen = {term.casefold() for term in existing_terms}
    added_terms = []
    for term in requested_terms:
        key = term.casefold()
        if key in seen:
            continue
        seen.add(key)
        existing_terms.append(term)
        added_terms.append(term)
    config[PROTECTED_TERMS_KEY] = existing_terms
    config["updated_at"] = now_iso()
    paths = kb_paths(root_dir, kb_name)
    write_kb_config(paths, config)
    write_kb_protected_terms(paths, existing_terms)
    manifest = refresh_keyword_assets(
        root_dir,
        kb_name,
        config,
        extra={
            "protected_terms_updated": True,
            "protected_terms_added": added_terms,
            "protected_terms_removed": [],
        },
    )
    return {
        "kb_name": kb_name,
        "root_dir": str(root_dir),
        PROTECTED_TERMS_KEY: existing_terms,
        "added_terms": added_terms,
        "removed_terms": [],
        "protected_term_count": len(existing_terms),
        "bm25_refreshed": True,
        "manifest": manifest,
    }


def delete_protected_terms(root_dir: Path, kb_name: str, terms: Iterable[str]) -> dict:
    config = load_kb_config(root_dir, kb_name)
    requested_terms = normalize_protected_terms(terms)
    requested_keys = {term.casefold() for term in requested_terms}
    existing_terms = list(config.get(PROTECTED_TERMS_KEY, []))
    updated_terms = [term for term in existing_terms if term.casefold() not in requested_keys]
    removed_terms = [term for term in existing_terms if term.casefold() in requested_keys]
    removed_keys = {term.casefold() for term in removed_terms}
    missing_terms = [term for term in requested_terms if term.casefold() not in removed_keys]
    config[PROTECTED_TERMS_KEY] = updated_terms
    config["updated_at"] = now_iso()
    paths = kb_paths(root_dir, kb_name)
    write_kb_config(paths, config)
    write_kb_protected_terms(paths, updated_terms)
    manifest = refresh_keyword_assets(
        root_dir,
        kb_name,
        config,
        extra={
            "protected_terms_updated": True,
            "protected_terms_added": [],
            "protected_terms_removed": removed_terms,
        },
    )
    return {
        "kb_name": kb_name,
        "root_dir": str(root_dir),
        PROTECTED_TERMS_KEY: updated_terms,
        "added_terms": [],
        "removed_terms": removed_terms,
        "missing_terms": missing_terms,
        "protected_term_count": len(updated_terms),
        "bm25_refreshed": True,
        "manifest": manifest,
    }


def vector_search(records: list[dict], index, query_vector, top_k: int) -> list[dict]:
    if not records or index is None:
        return []
    scores, indices = index.search(query_vector, top_k)
    chunk_lookup = {
        (item["doc_id"], item["chunk_id"]): item
        for item in records
        if item["kind"] == "chunk"
    }
    merged = {}
    for idx, score in zip(indices[0], scores[0]):
        if idx < 0:
            continue
        row = dict(records[idx])
        target_chunk_id = row["chunk_id"]
        canonical = chunk_lookup.get((row["doc_id"], target_chunk_id), row)
        key = canonical["id"]
        existing = merged.get(key)
        matched_via = {row["kind"]}
        if existing:
            matched_via.update(existing.get("matched_via", []))
        collapsed = dict(canonical)
        collapsed["vector_score"] = max(float(score), existing["vector_score"] if existing else float(score))
        collapsed["matched_by"] = ["semantic"]
        collapsed["matched_via"] = sorted(matched_via)
        merged[key] = collapsed
    return sorted(merged.values(), key=lambda item: item["vector_score"], reverse=True)


def keyword_search(records: list[dict], bm25_index: dict | None, query_terms: Counter[str], top_k: int) -> list[dict]:
    if not records or not bm25_index:
        return []
    postings = bm25_index.get("postings", {})
    if not postings:
        return []
    doc_count = int(bm25_index.get("doc_count", 0))
    if doc_count <= 0:
        return []
    doc_lengths = bm25_index.get("doc_lengths", {})
    avgdl = float(bm25_index.get("avgdl", 0.0))
    k1 = float(bm25_index.get("k1", BM25_K1))
    b = float(bm25_index.get("b", BM25_B))
    chunk_lookup = {item["id"]: item for item in records if item["kind"] == "chunk"}
    scores: dict[str, float] = defaultdict(float)
    for term, qtf in query_terms.items():
        term_postings = postings.get(term)
        if not term_postings:
            continue
        df = len(term_postings)
        idf = math.log(1.0 + (doc_count - df + 0.5) / (df + 0.5))
        for doc_key, tf in term_postings:
            doc_length = float(doc_lengths.get(doc_key, 0))
            denominator = float(tf) + k1 * (1.0 - b + (b * doc_length / avgdl if avgdl else 0.0))
            if denominator <= 0:
                continue
            scores[str(doc_key)] += qtf * idf * (float(tf) * (k1 + 1.0) / denominator)
    ranked = []
    for doc_key, score in scores.items():
        canonical = chunk_lookup.get(doc_key)
        if canonical is None:
            continue
        row = dict(canonical)
        row["bm25_score"] = float(score)
        row["matched_by"] = ["keyword"]
        row["matched_via"] = ["chunk"]
        ranked.append(row)
    ranked.sort(key=lambda item: item["bm25_score"], reverse=True)
    return ranked[:top_k]


def recall_limit(topk: int, rerank: bool) -> int:
    return max(topk, 20) if rerank else topk


def resolve_query_limits(config: dict | None, topk: int | None, topn: int | None) -> tuple[int, int]:
    config = config or {}
    effective_topk = normalize_positive(topk if topk is not None else config.get("topk", DEFAULT_TOPK), "topk")
    effective_topn = normalize_positive(topn if topn is not None else config.get("topN", DEFAULT_TOPN), "topN")
    if effective_topn > effective_topk:
        raise KBError("topN must be less than or equal to topk.")
    return effective_topk, effective_topn


def sort_candidates_by_score(candidates: list[dict], field: str) -> list[dict]:
    return sorted(candidates, key=lambda item: item.get(field, float("-inf")), reverse=True)


def fuse_ranked_candidates(semantic_candidates: list[dict], keyword_candidates: list[dict]) -> list[dict]:
    merged = {}
    for method, candidates in (("semantic", semantic_candidates), ("keyword", keyword_candidates)):
        for rank, candidate in enumerate(candidates, start=1):
            key = candidate["id"]
            existing = merged.get(key)
            row = dict(existing or candidate)
            row["fusion_score"] = float(row.get("fusion_score", 0.0)) + (1.0 / (RRF_K + rank))
            matched_by = set(row.get("matched_by", []))
            matched_by.update(candidate.get("matched_by", []))
            matched_by.add(method)
            row["matched_by"] = sorted(matched_by)
            matched_via = set(row.get("matched_via", []))
            matched_via.update(candidate.get("matched_via", []))
            row["matched_via"] = sorted(matched_via)
            if "vector_score" in candidate:
                row["vector_score"] = max(float(candidate["vector_score"]), float(row.get("vector_score", float("-inf"))))
            if "bm25_score" in candidate:
                row["bm25_score"] = max(float(candidate["bm25_score"]), float(row.get("bm25_score", float("-inf"))))
            merged[key] = row
    return sorted(
        merged.values(),
        key=lambda item: (
            item.get("fusion_score", float("-inf")),
            item.get("vector_score", float("-inf")),
            item.get("bm25_score", float("-inf")),
        ),
        reverse=True,
    )


def finalize_results(
    query: str,
    retrieval_mode: str,
    semantic_candidates: list[dict],
    keyword_candidates: list[dict],
    *,
    topk: int,
    topn: int,
    rerank: bool,
) -> list[dict]:
    if retrieval_mode == "semantic":
        merged = sort_candidates_by_score(semantic_candidates, "vector_score")
    elif retrieval_mode == "keyword":
        merged = sort_candidates_by_score(keyword_candidates, "bm25_score")
    else:
        merged = fuse_ranked_candidates(
            sort_candidates_by_score(semantic_candidates, "vector_score"),
            sort_candidates_by_score(keyword_candidates, "bm25_score"),
        )
    if not merged:
        return []
    if not rerank:
        final = merged[:topn]
    else:
        rerank_candidates = merged[: recall_limit(topk, rerank=True)]
        reranked = rerank_documents(query, [item["text"] for item in rerank_candidates], top_n=topn)
        final = []
        for item in reranked:
            row = dict(rerank_candidates[item["index"]])
            row["rerank_score"] = float(item["relevance_score"])
            final.append(row)
    for item in final:
        item["retrieval_mode"] = retrieval_mode
    return final


def recall_one_kb(
    root_dir: Path,
    kb_name: str,
    *,
    topk: int | None,
    topn: int | None,
    rerank: bool,
    retrieval_mode: str,
    query_vector=None,
    query_terms: Counter[str] | None = None,
    config: dict | None = None,
) -> tuple[list[dict], list[dict], tuple[int, int]]:
    mode = normalize_retrieval_mode(retrieval_mode)
    effective_config, records, index, bm25_index = load_kb_bundle(
        root_dir,
        kb_name,
        load_vector_index=mode in {"semantic", "hybrid"},
        load_bm25_index=mode in {"keyword", "hybrid"},
        config=config,
    )
    effective_topk, effective_topn = resolve_query_limits(effective_config, topk, topn)
    candidate_limit = recall_limit(effective_topk, rerank)
    semantic_candidates = []
    keyword_candidates = []
    if mode in {"semantic", "hybrid"}:
        if query_vector is None:
            raise KBError("Missing query vector for semantic retrieval.")
        semantic_candidates = vector_search(records, index, query_vector, top_k=candidate_limit)
    if mode in {"keyword", "hybrid"}:
        if query_terms is None:
            raise KBError("Missing query terms for keyword retrieval.")
        keyword_candidates = keyword_search(records, bm25_index, query_terms, top_k=candidate_limit)
    return semantic_candidates, keyword_candidates, (effective_topk, effective_topn)


def search_one_kb(
    root_dir: Path,
    kb_name: str,
    query: str,
    *,
    topk: int | None,
    topn: int | None,
    rerank: bool,
    retrieval_mode: str,
) -> list[dict]:
    mode = normalize_retrieval_mode(retrieval_mode)
    config = load_kb_config(root_dir, kb_name)
    query_vector = prepare_query_vector(query) if mode in {"semantic", "hybrid"} else None
    query_terms = (
        prepare_keyword_query_terms(query, protected_terms=config.get(PROTECTED_TERMS_KEY, []))
        if mode in {"keyword", "hybrid"}
        else None
    )
    semantic_candidates, keyword_candidates, (effective_topk, effective_topn) = recall_one_kb(
        root_dir,
        kb_name,
        topk=topk,
        topn=topn,
        rerank=rerank,
        retrieval_mode=mode,
        query_vector=query_vector,
        query_terms=query_terms,
        config=config,
    )
    return finalize_results(
        query,
        mode,
        semantic_candidates,
        keyword_candidates,
        topk=effective_topk,
        topn=effective_topn,
        rerank=rerank,
    )


def list_kb_names(root_dir: Path) -> list[str]:
    if not root_dir.exists():
        return []
    names = []
    for entry in sorted(root_dir.iterdir(), key=lambda item: item.name):
        if entry.is_dir() and (entry / "config.json").exists():
            config = read_json(entry / "config.json", default={})
            names.append(config.get("kb_name", entry.name))
    return names


def search_across_kbs(
    root_dir: Path,
    query: str,
    *,
    topk: int | None,
    topn: int | None,
    rerank: bool,
    retrieval_mode: str,
) -> list[dict]:
    mode = normalize_retrieval_mode(retrieval_mode)
    effective_topk, effective_topn = resolve_query_limits(None, topk, topn)
    query_vector = prepare_query_vector(query) if mode in {"semantic", "hybrid"} else None
    semantic_candidates = []
    keyword_candidates = []
    for kb_name in list_kb_names(root_dir):
        try:
            config = load_kb_config(root_dir, kb_name)
            query_terms = (
                prepare_keyword_query_terms(query, protected_terms=config.get(PROTECTED_TERMS_KEY, []))
                if mode in {"keyword", "hybrid"}
                else None
            )
            kb_semantic, kb_keyword, _ = recall_one_kb(
                root_dir,
                kb_name,
                topk=effective_topk,
                topn=effective_topn,
                rerank=rerank,
                retrieval_mode=mode,
                query_vector=query_vector,
                query_terms=query_terms,
                config=config,
            )
            semantic_candidates.extend(kb_semantic)
            keyword_candidates.extend(kb_keyword)
        except KBError:
            continue
    return finalize_results(
        query,
        mode,
        semantic_candidates,
        keyword_candidates,
        topk=effective_topk,
        topn=effective_topn,
        rerank=rerank,
    )


def render_markdown_results(results: list[dict]) -> str:
    if not results:
        return "No results.\n"
    grouped = {}
    for item in results:
        grouped.setdefault(item["doc_id"], {"file_name": item["file_name"], "uploaded_at": item["uploaded_at"], "summary": item.get("summary", ""), "chunks": []})
        grouped[item["doc_id"]]["total_chunks"] = max(
            item.get("chunk_count", 0),
            grouped[item["doc_id"]].get("total_chunks", 0),
        )
        grouped[item["doc_id"]]["chunks"].append(item)
    sections = []
    for doc_id in sorted(grouped.keys()):
        entry = grouped[doc_id]
        lines = [
            f"## {entry['file_name']}",
            "",
            f"- uploaded at {entry['uploaded_at']}",
            f"- summary: {entry['summary'] or ''}",
            f"- total chunks: {entry.get('total_chunks', 0)}",
            "",
        ]
        seen_chunks = set()
        for chunk in sorted(entry["chunks"], key=lambda item: item["chunk_id"]):
            if chunk["chunk_id"] in seen_chunks:
                continue
            seen_chunks.add(chunk["chunk_id"])
            lines.extend(
                [
                    f"### Chunk {chunk['chunk_id']}",
                    "",
                    chunk["text"],
                    "",
                ]
            )
        sections.append("\n".join(lines).rstrip())
    return "\n\n".join(sections) + "\n"


def normalize_positive(value: int, field: str) -> int:
    if value <= 0:
        raise KBError(f"{field} must be positive.")
    return int(value)


def module_available(name: str) -> bool:
    try:
        __import__(name)
        return True
    except Exception:
        return False


def run_doctor(root_dir: Path) -> int:
    python_version = sys.version.split()[0]
    version_parts = tuple(int(part) for part in python_version.split(".")[:2])
    checks = {
        "python": python_version,
        "python_compatible": version_parts >= (3, 10),
        "python_required": ">=3.10",
        "api_key_present": bool(os.getenv("BAILIAN-SK") or os.getenv("BAILIAN_SK")),
        "requests": module_available("requests"),
        "numpy": module_available("numpy"),
        "faiss": module_available("faiss"),
        "jieba": module_available("jieba"),
        "root_dir": str(root_dir),
        "root_dir_exists": root_dir.exists(),
        "root_dir_writable": os.access(root_dir, os.W_OK) if root_dir.exists() else os.access(root_dir.parent, os.W_OK),
    }
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Operate an OpenClaw knowledge base with Bailian, FAISS, and BM25.")
    parser.add_argument("--root-dir", default=DEFAULT_ROOT_DIR, help="Knowledge-base root directory.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Check runtime and dependency availability.")
    doctor.set_defaults(func=cmd_doctor)

    index = subparsers.add_parser("index", help="Index one document directory and refresh both vector and BM25 KB indexes.")
    index.add_argument("--kb", required=True, help="Knowledge-base name.")
    index.add_argument("--doc-dir", required=True, help="Document directory, e.g. /root/regulation/{ts}-xx")
    index.add_argument("--topk", type=int, help="FAISS recall top-k to store in KB config.")
    index.add_argument("--topN", type=int, help="Rerank top-N to store in KB config.")
    index.set_defaults(func=cmd_index)

    rebuild = subparsers.add_parser("rebuild", help="Rebuild one KB from all document directories, including FAISS and BM25 artifacts.")
    rebuild.add_argument("--kb", required=True, help="Knowledge-base name.")
    rebuild.add_argument("--topk", type=int, help="FAISS recall top-k to store in KB config.")
    rebuild.add_argument("--topN", type=int, help="Rerank top-N to store in KB config.")
    rebuild.set_defaults(func=cmd_rebuild)

    delete = subparsers.add_parser("delete", help="Delete one document from the KB-level vector and BM25 indexes and persist the result.")
    delete.add_argument("--kb", required=True, help="Knowledge-base name.")
    delete.add_argument("--doc-id", required=True, help="Document directory name, e.g. {ts}-xx")
    delete.set_defaults(func=cmd_delete)

    protect_add = subparsers.add_parser("protect-add", help="Add protected terms to one KB and refresh BM25 metadata.")
    protect_add.add_argument("--kb", required=True, help="Knowledge-base name.")
    protect_add.add_argument("--term", dest="terms", action="append", required=True, help="Protected term to add. Repeatable.")
    protect_add.set_defaults(func=cmd_protect_add)

    protect_delete = subparsers.add_parser("protect-delete", help="Delete protected terms from one KB and refresh BM25 metadata.")
    protect_delete.add_argument("--kb", required=True, help="Knowledge-base name.")
    protect_delete.add_argument("--term", dest="terms", action="append", required=True, help="Protected term to delete. Repeatable.")
    protect_delete.set_defaults(func=cmd_protect_delete)

    query = subparsers.add_parser("query", help="Query one KB or all KBs and return Markdown.")
    query.add_argument("--kb", help="Knowledge-base name. Omit to search across all KBs.")
    query.add_argument("--query", required=True, help="Question text.")
    query.add_argument(
        "--retrieval-mode",
        default=DEFAULT_RETRIEVAL_MODE,
        choices=sorted(RETRIEVAL_MODES),
        help="Retrieval mode: hybrid (default), semantic, or keyword.",
    )
    query.add_argument("--topk", type=int, help="FAISS recall top-k override.")
    query.add_argument("--topN", type=int, help="Rerank top-N override.")
    query.add_argument("--rerank", action="store_true", help="Enable rerank.")
    query.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    query.set_defaults(func=cmd_query)

    return parser.parse_args()


def cmd_doctor(args: argparse.Namespace) -> int:
    return run_doctor(Path(args.root_dir))


def cmd_index(args: argparse.Namespace) -> int:
    manifest = index_kb(
        root_dir=Path(args.root_dir).expanduser(),
        kb_name=args.kb,
        doc_dir=Path(args.doc_dir).expanduser(),
        topk=args.topk,
        topn=args.topN,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def cmd_rebuild(args: argparse.Namespace) -> int:
    manifest = rebuild_kb(
        root_dir=Path(args.root_dir).expanduser(),
        kb_name=args.kb,
        topk=args.topk,
        topn=args.topN,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    manifest = delete_from_index(
        root_dir=Path(args.root_dir).expanduser(),
        kb_name=args.kb,
        doc_id=args.doc_id,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def cmd_protect_add(args: argparse.Namespace) -> int:
    result = add_protected_terms(
        root_dir=Path(args.root_dir).expanduser(),
        kb_name=args.kb,
        terms=args.terms,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_protect_delete(args: argparse.Namespace) -> int:
    result = delete_protected_terms(
        root_dir=Path(args.root_dir).expanduser(),
        kb_name=args.kb,
        terms=args.terms,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    root_dir = Path(args.root_dir).expanduser()
    if args.kb:
        results = search_one_kb(
            root_dir,
            args.kb,
            args.query,
            topk=args.topk,
            topn=args.topN,
            rerank=args.rerank,
            retrieval_mode=args.retrieval_mode,
        )
    else:
        results = search_across_kbs(
            root_dir,
            args.query,
            topk=args.topk,
            topn=args.topN,
            rerank=args.rerank,
            retrieval_mode=args.retrieval_mode,
        )
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(render_markdown_results(results), end="")
    return 0


def main() -> int:
    try:
        args = parse_args()
        return args.func(args)
    except KBError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
