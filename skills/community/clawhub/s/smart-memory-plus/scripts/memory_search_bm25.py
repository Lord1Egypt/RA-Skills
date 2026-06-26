#!/usr/bin/env python3
"""
memory_search_bm25.py — BM25 semantic search over memory files.

Indexes MEMORY.md and memory/*.md, then ranks results by BM25 relevance.
Supports incremental updates: only re-indexes changed files.
Zero external dependencies — pure Python implementation.

Usage:
  memory_search_bm25.py build                     # Full rebuild
  memory_search_bm25.py update                    # Incremental update (changed files only)
  memory_search_bm25.py search "query"             # Search with default top-5
  memory_search_bm25.py search "query" --top 10    # Return top 10 results
  memory_search_bm25.py status                     # Show index stats
"""

import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")))
INDEX_DIR = WORKSPACE / "memory" / ".index"
INDEX_FILE = INDEX_DIR / "bm25_index.json"
DOCS_FILE = INDEX_DIR / "docs.json"
MTIMES_FILE = INDEX_DIR / "file_mtimes.json"

# Tokenizer: split on non-alphanumeric, keep CJK chars as individual tokens
TOKEN_PATTERN = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)
STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "shall", "to", "of", "in", "for",
    "on", "with", "at", "by", "from", "as", "into", "through", "during",
    "before", "after", "above", "below", "and", "but", "or", "nor", "not",
    "no", "so", "if", "then", "than", "too", "very", "just", "about",
    "up", "out", "it", "its", "this", "that", "these", "those", "i", "me",
    "my", "we", "our", "you", "your", "he", "him", "his", "she", "her",
    "they", "them", "their", "what", "which", "who", "whom", "when",
    "where", "why", "how", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "only", "own", "same", "also",
}


def tokenize(text: str) -> list[str]:
    """Tokenize text into lowercase words, filter stop words."""
    tokens = TOKEN_PATTERN.findall(text.lower())
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


def get_memory_files() -> list[Path]:
    """Get all memory files that should be indexed."""
    files = []
    memory_file = WORKSPACE / "MEMORY.md"
    if memory_file.exists():
        files.append(memory_file)

    memory_dir = WORKSPACE / "memory"
    if memory_dir.exists():
        for f in sorted(memory_dir.glob("*.md")):
            if f.name == "archive" or f.name.startswith("."):
                continue
            # Skip subdirectories (compacts, archive, .index)
            if f.parent != memory_dir:
                continue
            files.append(f)

    return files


def load_file_mtimes() -> dict:
    """Load saved file modification times."""
    if MTIMES_FILE.exists():
        return json.loads(MTIMES_FILE.read_text(encoding="utf-8"))
    return {}


def save_file_mtimes(mtimes: dict):
    """Save file modification times."""
    MTIMES_FILE.write_text(json.dumps(mtimes, ensure_ascii=False), encoding="utf-8")


def parse_file_docs(filepath: Path) -> list[dict]:
    """Parse a single file into document sections."""
    docs = []
    content = filepath.read_text(encoding="utf-8")
    sections = re.split(r"(^## .+$)", content, flags=re.MULTILINE)
    current_header = filepath.name

    for part in sections:
        part = part.strip()
        if not part:
            continue
        if part.startswith("## "):
            current_header = part
        else:
            tokens = tokenize(part)
            if tokens:
                docs.append({
                    "source": filepath.name,
                    "header": current_header,
                    "text": part[:500],
                    "tokens": tokens,
                })
    return docs


class BM25:
    """BM25 ranking algorithm (Okapi BM25)."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.doc_count = 0
        self.avg_doc_len = 0.0
        self.doc_freqs: dict[str, int] = defaultdict(int)
        self.doc_lens: list[int] = []
        self.doc_tokens: list[list[str]] = []

    def index(self, docs: list[dict]):
        """Build index from documents."""
        self.doc_count = len(docs)
        self.doc_lens = []
        self.doc_tokens = []
        self.doc_freqs = defaultdict(int)

        for doc in docs:
            tokens = doc["tokens"]
            self.doc_tokens.append(tokens)
            self.doc_lens.append(len(tokens))
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.doc_freqs[token] += 1

        self.avg_doc_len = sum(self.doc_lens) / max(self.doc_count, 1)

    def score(self, query_tokens: list[str], doc_idx: int) -> float:
        """Calculate BM25 score for a document given query tokens."""
        if not query_tokens or doc_idx >= self.doc_count:
            return 0.0

        doc_tokens = self.doc_tokens[doc_idx]
        doc_len = self.doc_lens[doc_idx]
        token_counts = Counter(doc_tokens)

        score = 0.0
        for token in query_tokens:
            if token not in self.doc_freqs:
                continue
            tf = token_counts.get(token, 0)
            if tf == 0:
                continue
            df = self.doc_freqs[token]
            idf = math.log((self.doc_count - df + 0.5) / (df + 0.5) + 1.0)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len)
            score += idf * numerator / denominator

        return round(score, 4)

    def search(self, query_tokens: list[str], top_k: int = 5) -> list[tuple[int, float]]:
        """Search and return top-k (doc_idx, score) pairs."""
        scores = []
        for i in range(self.doc_count):
            s = self.score(query_tokens, i)
            if s > 0:
                scores.append((i, s))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def to_dict(self) -> dict:
        return {
            "k1": self.k1,
            "b": self.b,
            "doc_count": self.doc_count,
            "avg_doc_len": self.avg_doc_len,
            "doc_freqs": dict(self.doc_freqs),
            "doc_lens": self.doc_lens,
            "doc_tokens": self.doc_tokens,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BM25":
        bm25 = cls(k1=data["k1"], b=data["b"])
        bm25.doc_count = data["doc_count"]
        bm25.avg_doc_len = data["avg_doc_len"]
        bm25.doc_freqs = defaultdict(int, data["doc_freqs"])
        bm25.doc_lens = data["doc_lens"]
        bm25.doc_tokens = data["doc_tokens"]
        return bm25


def save_index(bm25: BM25, docs_meta: list[dict]):
    """Save BM25 index and docs metadata to disk."""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    index_data = bm25.to_dict()
    INDEX_FILE.write_text(json.dumps(index_data, ensure_ascii=False), encoding="utf-8")
    DOCS_FILE.write_text(json.dumps(docs_meta, ensure_ascii=False), encoding="utf-8")


def load_index() -> tuple[BM25, list[dict]]:
    """Load BM25 index and docs metadata from disk."""
    index_data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    docs_meta = json.loads(DOCS_FILE.read_text(encoding="utf-8"))
    return BM25.from_dict(index_data), docs_meta


def cmd_build():
    """Full rebuild of BM25 index."""
    print("Full index rebuild...")
    files = get_memory_files()
    if not files:
        print("No memory files found.")
        return

    all_docs = []
    mtimes = {}

    for filepath in files:
        docs = parse_file_docs(filepath)
        for d in docs:
            d["id"] = len(all_docs)
            all_docs.append(d)
        mtimes[str(filepath)] = filepath.stat().st_mtime

    bm25 = BM25()
    bm25.index(all_docs)

    docs_meta = [{"id": d["id"], "source": d["source"], "header": d["header"], "text": d["text"]} for d in all_docs]
    save_index(bm25, docs_meta)
    save_file_mtimes(mtimes)

    total_tokens = sum(len(d["tokens"]) for d in all_docs)
    unique_terms = len(bm25.doc_freqs)
    print(f"Indexed {len(all_docs)} sections from {len(files)} files, {total_tokens} tokens, {unique_terms} unique terms")
    print(f"Index saved to {INDEX_FILE}")


def cmd_update():
    """Incremental update: only re-index changed files."""
    if not INDEX_FILE.exists() or not DOCS_FILE.exists():
        print("No existing index found. Running full build...")
        cmd_build()
        return

    saved_mtimes = load_file_mtimes()
    files = get_memory_files()

    # Find changed files
    changed_files = []
    unchanged_files = []
    current_mtimes = {}

    for filepath in files:
        fkey = str(filepath)
        current_mtime = filepath.stat().st_mtime
        current_mtimes[fkey] = current_mtime

        if fkey not in saved_mtimes or saved_mtimes[fkey] != current_mtime:
            changed_files.append(filepath)
        else:
            unchanged_files.append(fkey)

    # Find deleted files
    deleted_files = [f for f in saved_mtimes if f not in current_mtimes]

    if not changed_files and not deleted_files:
        print("Index is up to date. No changes detected.")
        return

    print(f"Updating index: {len(changed_files)} changed, {len(deleted_files)} deleted, {len(unchanged_files)} unchanged")

    # Load existing index
    old_bm25, old_docs_meta = load_index()

    # Build mapping: source file -> old doc indices
    old_source_to_ids: dict[str, list[int]] = defaultdict(list)
    for doc_meta in old_docs_meta:
        old_source_to_ids[doc_meta["source"]].append(doc_meta["id"])

    # Collect unchanged docs (keep their tokens)
    unchanged_doc_ids = set()
    for fkey in unchanged_files:
        fname = Path(fkey).name
        unchanged_doc_ids.update(old_source_to_ids.get(fname, []))

    # Parse changed files
    new_docs_from_changed = []
    for filepath in changed_files:
        docs = parse_file_docs(filepath)
        new_docs_from_changed.extend(docs)

    # Rebuild: keep unchanged docs + new docs from changed files
    all_docs = []
    doc_id = 0

    # Add unchanged docs (from old index)
    for old_doc_meta in old_docs_meta:
        if old_doc_meta["id"] in unchanged_doc_ids:
            old_doc_meta["id"] = doc_id
            # Get tokens from old index
            old_doc_meta["tokens"] = old_bm25.doc_tokens[old_doc_meta["id"]] if old_doc_meta["id"] < len(old_bm25.doc_tokens) else []
            all_docs.append(old_doc_meta)
            doc_id += 1

    # Add new docs from changed files
    for d in new_docs_from_changed:
        d["id"] = doc_id
        all_docs.append(d)
        doc_id += 1

    # Rebuild BM25
    bm25 = BM25()
    bm25.index(all_docs)

    docs_meta = [{"id": d["id"], "source": d["source"], "header": d["header"], "text": d["text"]} for d in all_docs]
    save_index(bm25, docs_meta)
    save_file_mtimes(current_mtimes)

    total_tokens = sum(len(d["tokens"]) for d in all_docs)
    unique_terms = len(bm25.doc_freqs)
    print(f"Index updated: {len(all_docs)} sections from {len(files)} files, {total_tokens} tokens, {unique_terms} unique terms")


def cmd_search(query: str, top_k: int = 5):
    """Search the BM25 index."""
    if not INDEX_FILE.exists() or not DOCS_FILE.exists():
        print("Index not found. Run 'build' first.")
        sys.exit(1)

    bm25, docs_meta = load_index()
    query_tokens = tokenize(query)

    if not query_tokens:
        print("No valid query tokens.")
        return

    results = bm25.search(query_tokens, top_k)

    if not results:
        print("No results found.")
        return

    print(f"Top {len(results)} results for: \"{query}\"\n")
    for rank, (doc_idx, score) in enumerate(results, 1):
        if doc_idx < len(docs_meta):
            doc = docs_meta[doc_idx]
            source = doc["source"]
            header = doc["header"]
            text = doc["text"][:200].replace("\n", " ")
            print(f"  {rank}. [{score:.2f}] {source} | {header}")
            print(f"     {text}")
            print()


def cmd_status():
    """Show index status."""
    if not INDEX_FILE.exists():
        print("No index found. Run 'build' first.")
        return

    bm25, docs_meta = load_index()
    mtimes = load_file_mtimes()

    mtime = datetime.fromtimestamp(INDEX_FILE.stat().st_mtime, tz=timezone.utc)
    print(f"=== BM25 Index Status ===")
    print(f"Documents: {bm25.doc_count}")
    print(f"Unique terms: {len(bm25.doc_freqs)}")
    print(f"Avg doc length: {bm25.avg_doc_len:.1f} tokens")
    print(f"Indexed files: {len(mtimes)}")
    print(f"Last built: {mtime.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Index size: {INDEX_FILE.stat().st_size:,} bytes")
    print(f"Sources: {len(set(d['source'] for d in docs_meta))} files")

    # Check for stale files
    current_files = get_memory_files()
    current_names = {f.name for f in current_files}
    indexed_names = set(d["source"] for d in docs_meta)
    missing = current_names - indexed_names
    extra = indexed_names - current_names
    if missing:
        print(f"⚠️  Missing from index: {', '.join(sorted(missing))}")
    if extra:
        print(f"⚠️  Extra in index (deleted?): {', '.join(sorted(extra))}")


def main():
    parser = argparse.ArgumentParser(description="BM25 search over memory files")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("build", help="Full rebuild of search index")
    subparsers.add_parser("update", help="Incremental update (changed files only)")

    search_parser = subparsers.add_parser("search", help="Search memories")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--top", type=int, default=5, help="Number of results (default: 5)")

    subparsers.add_parser("status", help="Show index stats")

    args = parser.parse_args()

    if args.command == "build":
        cmd_build()
    elif args.command == "update":
        cmd_update()
    elif args.command == "search":
        cmd_search(args.query, args.top)
    elif args.command == "status":
        cmd_status()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
