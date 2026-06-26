# Guide 05 — Chunking Standards

## Purpose

Chunking determines the retrieval unit — the piece of text returned to the LLM when a query matches. Chunks that are too large dilute relevance; chunks that are too small lack context. This guide defines chunk sizes, overlap, strategies, and determinism requirements by content type.

---

## The Golden Rule of Chunking

**The same normalized source input must always produce the same chunk set.** Given identical normalized text and the same `chunker_version`, the pipeline must produce:
- Identical chunk boundaries
- Identical chunk text
- Identical `content_hash` values
- Identical `doc_id` values

Non-deterministic chunking (e.g., using random seeds, model sampling) is prohibited in production pipelines.

---

## Chunking Parameters by Content Type

| Content Type | Token Range | Overlap | Strategy |
|---|---|---|---|
| Messages (Slack, short DMs) | 150–300 | 30 | Sentence window |
| Long email threads | 200–400 | 30 | Split at reply boundaries first, then sentence window within each reply |
| Meeting transcripts | 150–250 | 20 | Split at speaker turns first, then chunk within each speaker turn |
| Documents (Drive, PDFs, long-form) | 300–500 | 50 | Hierarchical: paragraph-level chunking with heading structure preserved |
| Tasks and tickets (ClickUp, Jira, etc.) | Up to 512 | N/A | One chunk per task; split only if token limit exceeded |
| Code files | 200–400 | 50 | Function/class boundary-aware; never split in the middle of a function |
| Structured data (tables, CSV rows) | N/A | N/A | One row or logical unit per chunk; include column headers in every chunk |

**Token count approximation:** Use the fixed heuristic of **4 characters per token** for fast, deterministic token estimation without requiring a tokenizer in the ingestion pipeline.

---

## Chunking Strategies Explained

### 1. Sentence Window (Messages, Short Content)

Chunk at sentence boundaries. Use sliding window with overlap to preserve context across chunk edges.

```python
import re

def chunk_sentence_window(
    text: str,
    max_tokens: int = 256,
    overlap_tokens: int = 30,
    chars_per_token: int = 4,
) -> list[str]:
    """Chunk text using a sliding sentence window."""
    
    max_chars = max_tokens * chars_per_token
    overlap_chars = overlap_tokens * chars_per_token
    
    # Split into sentences (simple heuristic; use a proper sentence splitter for production)
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    
    chunks = []
    current_chunk = []
    current_len = 0
    
    for sentence in sentences:
        sent_len = len(sentence)
        
        if current_len + sent_len > max_chars and current_chunk:
            chunks.append(" ".join(current_chunk))
            # Keep overlap: retain last N chars worth of sentences
            overlap_kept = []
            overlap_len = 0
            for s in reversed(current_chunk):
                if overlap_len + len(s) <= overlap_chars:
                    overlap_kept.insert(0, s)
                    overlap_len += len(s)
                else:
                    break
            current_chunk = overlap_kept
            current_len = overlap_len
        
        current_chunk.append(sentence)
        current_len += sent_len
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks
```

### 2. Reply-Boundary Chunking (Email Threads)

Split first at reply boundaries, then apply sentence window within each reply segment.

```python
REPLY_DELIMITERS = [
    r"^On .+wrote:$",
    r"^-----Original Message-----",
    r"^From:.+Sent:",
    r"^>{1,}\s",
]

def chunk_email_thread(text: str, max_tokens: int = 350) -> list[str]:
    """Split email thread at reply boundaries, then chunk each segment."""
    delimiter_pattern = "|".join(REPLY_DELIMITERS)
    
    # Split at reply delimiters
    segments = re.split(delimiter_pattern, text, flags=re.MULTILINE)
    segments = [s.strip() for s in segments if s.strip()]
    
    chunks = []
    for segment in segments:
        if len(segment) / 4 <= max_tokens:
            chunks.append(segment)
        else:
            chunks.extend(chunk_sentence_window(segment, max_tokens=max_tokens))
    
    return chunks
```

### 3. Speaker-Turn Chunking (Meeting Transcripts)

Split at speaker turn boundaries (identified by speaker attribution markers), then chunk within turns if they are long. Speaker attribution is **critical** — never split a speaker attribution from the text that follows it.

```python
def chunk_transcript(
    transcript_segments: list[dict],
    max_tokens: int = 200,
    overlap_tokens: int = 20,
    context_header: str = "",
) -> list[dict]:
    """
    Chunk a meeting transcript at speaker turns.
    Each segment is dict: {"speaker": "Jane", "text": "...", "start_ms": 0}
    """
    chunks = []
    
    for segment in transcript_segments:
        speaker = segment["speaker"]
        text = segment["text"]
        turn_text = f"[{speaker}]: {text}"
        
        if len(turn_text) / 4 <= max_tokens:
            # Fits in one chunk
            chunks.append({
                "text": turn_text,
                "context_header": context_header,
                "speaker": speaker,
                "start_ms": segment.get("start_ms", 0),
            })
        else:
            # Split long turn with overlap
            sub_chunks = chunk_sentence_window(text, max_tokens=max_tokens, overlap_tokens=overlap_tokens)
            for i, sub in enumerate(sub_chunks):
                chunks.append({
                    "text": f"[{speaker}]: {sub}",
                    "context_header": context_header,
                    "speaker": speaker,
                    "start_ms": segment.get("start_ms", 0),
                    "sub_chunk_index": i,
                })
    
    return chunks
```

### 4. Hierarchical Paragraph Chunking (Documents)

Preserve document structure. Chunk at paragraph boundaries. Include the nearest heading as a context header for each chunk, so chunks are self-contained without requiring the reader to know which section they came from.

```python
def chunk_document_hierarchical(
    markdown_text: str,
    max_tokens: int = 400,
    overlap_tokens: int = 50,
) -> list[dict]:
    """
    Chunk a Markdown document hierarchically.
    Splits at paragraph boundaries, tracks heading context.
    """
    lines = markdown_text.split("\n")
    chunks = []
    current_heading = ""
    current_paragraphs = []
    current_len = 0
    
    for line in lines:
        # Track heading context
        if line.startswith("#"):
            if current_paragraphs and current_len > 0:
                _flush_doc_chunk(current_paragraphs, current_heading, max_tokens, overlap_tokens, chunks)
                current_paragraphs = []
                current_len = 0
            current_heading = line.lstrip("#").strip()
            continue
        
        # Empty line = paragraph boundary
        if not line.strip():
            if current_len > 0 and current_len >= (max_tokens * 4 * 0.7):  # 70% full → flush
                _flush_doc_chunk(current_paragraphs, current_heading, max_tokens, overlap_tokens, chunks)
                current_paragraphs = []
                current_len = 0
            continue
        
        current_paragraphs.append(line)
        current_len += len(line)
    
    if current_paragraphs:
        _flush_doc_chunk(current_paragraphs, current_heading, max_tokens, overlap_tokens, chunks)
    
    return chunks

def _flush_doc_chunk(paragraphs, heading, max_tokens, overlap_tokens, chunks):
    text = " ".join(paragraphs)
    header = f"[Section: {heading}] " if heading else ""
    if len(text) / 4 <= max_tokens:
        chunks.append({"text": text, "section_heading": heading, "context_header": header})
    else:
        for sub in chunk_sentence_window(text, max_tokens, overlap_tokens):
            chunks.append({"text": sub, "section_heading": heading, "context_header": header})
```

---

## Context Headers

For threaded conversations, meeting transcripts, and email threads, prepend a **context header** to each chunk. The context header is separate from the chunk body's token count.

The context header ensures the chunk is self-contained — a retrieval result makes sense without the reader having to navigate back to the source.

**Format by type:**

| Source | Context Header Format |
|---|---|
| Slack thread | `[Channel: #sales-emea] [Thread from: Jane Smith, Apr 30 2024]` |
| Email thread | `[Subject: Q2 Budget Review] [From: jane@company.com, Apr 30 2024]` |
| Meeting transcript | `[Meeting: Q3 Forecast Review \| Date: 2024-04-30 \| Attendees: Jane, Bob, Alice]` |
| Document section | `[Document: Product Roadmap Q4 \| Section: Engineering Priorities]` |

---

## Chunk Metadata Fields

Every chunk must carry these fields in its payload:

```python
def build_chunk_payload(
    parent_metadata: dict,
    chunk_text: str,
    chunk_index: int,
    chunk_total: int,
    chunk_strategy: str,
    context_header: str = "",
) -> dict:
    import hashlib
    
    content_hash = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()
    token_count = len(chunk_text) // 4  # 4 chars per token approximation
    
    payload = {
        **parent_metadata,  # Inherit all parent document metadata
        "doc_id": f"{parent_metadata['source_type']}_{parent_metadata['source_record_id']}_{chunk_index}",
        "chunk_index": chunk_index,
        "chunk_total": chunk_total,
        "content_hash": content_hash,
        "token_count": token_count,
        "chunk_strategy": chunk_strategy,
        "context_header": context_header,
    }
    return payload
```

---

## Chunking Rules (Summary)

1. Every chunk carries the full universal metadata payload (`chunk_index`, `chunk_total`, `parent_doc_id` — no exceptions).
2. Chunks must not split mid-sentence. Always break at sentence or structural boundaries.
3. Context headers are prepended but do NOT count toward the chunk's token limit.
4. Token counts are approximated at **4 characters per token** — do not call a tokenizer for this.
5. The `chunk_strategy` field must accurately reflect the strategy used.
6. Chunk size and overlap values must be validated with retrieval testing before production deployment.
7. When re-ingesting a document that now produces **fewer chunks** than before, delete the out-of-range chunks (those with `chunk_index` ≥ new total) from Qdrant.

---

## Common Mistakes

| Mistake | Impact | Fix |
|---|---|---|
| Splitting a speaker attribution from its text | Destroys attribution in retrieval | Always keep `[Speaker]:` + text together |
| Including quoted email content in chunks | Duplicate information in the index | Strip quoted content during normalization |
| Using model token counters in the chunking loop | Non-determinism if model version changes | Use 4 chars/token heuristic |
| Creating chunks of 50 tokens or less | Too small to carry useful context | Enforce minimum chunk size of 100 tokens |
| Ignoring section headings in documents | Chunks lack context, retrieval suffers | Always prepend heading as context header |
| Not deleting stale chunks after re-ingestion | Index accumulates orphan chunks | Always compare old vs. new `chunk_total` |
