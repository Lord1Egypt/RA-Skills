"""Semantic paper parser — Document → PaperContent.

Supported formats: PDF, Markdown (.md), DOCX, plain text.

Two modes (eng decision: dual-mode):
  - Mode A (builtin / lightweight): text extraction + LLM direct extraction (no embeddings)
  - Mode B (agent / full):  text extraction + FAISS semantic search + LLM extraction
"""

import asyncio
import logging
import os
import re
from typing import Optional

from paper2spec.llm import achat, chat
from paper2spec.models import PaperContent
from paper2spec.pdf_utils import PDFExtractor
from paper2spec.prompts import (
    DATA_DESCRIPTION_PROMPT,
    METHODOLOGY_PROMPT,
    SIGNAL_LOGIC_PROMPT,
    SYSTEM_PROMPT,
)

logger = logging.getLogger(__name__)

# ── Optional heavy deps (Mode B) ────────────────────────────

_faiss = None
_splitter_cls = None
_embeddings = None


def _ensure_mode_b_deps():
    """Lazy-load FAISS + sentence-transformers (eng decision #8)."""
    global _faiss, _splitter_cls, _embeddings
    if _faiss is not None:
        return
    try:
        from langchain_community.vectorstores import FAISS
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_community.embeddings import HuggingFaceEmbeddings

        _faiss = FAISS
        _splitter_cls = RecursiveCharacterTextSplitter
        _embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        logger.info("Mode B deps loaded (FAISS + bge-small-en)")
    except ImportError as e:
        raise ImportError(
            "Mode B requires: pip install langchain-community langchain-text-splitters "
            "sentence-transformers faiss-cpu"
        ) from e


# ── Public API ───────────────────────────────────────────────


def parse_pdf(pdf_path: str, *, mode: str = "builtin", model: Optional[str] = None) -> PaperContent:
    """Synchronous entry point: PDF path → PaperContent.

    Args:
        pdf_path: Path to the PDF file.
        mode: "builtin" (Mode A, no embeddings) or "agent" (Mode B, FAISS).
        model: Override LLM model string.
    """
    return asyncio.run(aparse_pdf(pdf_path, mode=mode, model=model))


async def aparse_pdf(
    pdf_path: str, *, mode: str = "builtin", model: Optional[str] = None
) -> PaperContent:
    """Async entry point: PDF path → PaperContent."""
    logger.info("Parsing %s (mode=%s)", pdf_path, mode)

    # 1. Extract text
    full_text = await asyncio.to_thread(PDFExtractor.extract_text, pdf_path)
    logger.info("Extracted %d chars from PDF", len(full_text))

    # 2. Parse
    return await _parse_text(full_text, source=pdf_path, mode=mode, model=model)


def parse_text(text: str, *, source: str = "text", mode: str = "builtin", model: Optional[str] = None) -> PaperContent:
    """Sync: raw text → PaperContent."""
    return asyncio.run(_parse_text(text, source=source, mode=mode, model=model))


def parse_markdown(md_path: str, *, mode: str = "builtin", model: Optional[str] = None) -> PaperContent:
    """Sync: Markdown file → PaperContent."""
    return asyncio.run(aparse_markdown(md_path, mode=mode, model=model))


async def aparse_markdown(
    md_path: str, *, mode: str = "builtin", model: Optional[str] = None
) -> PaperContent:
    """Async: Markdown file → PaperContent."""
    logger.info("Parsing Markdown %s (mode=%s)", md_path, mode)
    with open(md_path, "r", encoding="utf-8") as f:
        full_text = f.read()
    logger.info("Read %d chars from Markdown", len(full_text))
    return await _parse_text(full_text, source=md_path, mode=mode, model=model)


def parse_docx(docx_path: str, *, mode: str = "builtin", model: Optional[str] = None) -> PaperContent:
    """Sync: DOCX file → PaperContent. Requires python-docx."""
    return asyncio.run(aparse_docx(docx_path, mode=mode, model=model))


async def aparse_docx(
    docx_path: str, *, mode: str = "builtin", model: Optional[str] = None
) -> PaperContent:
    """Async: DOCX file → PaperContent. Requires python-docx."""
    logger.info("Parsing DOCX %s (mode=%s)", docx_path, mode)
    try:
        import docx
    except ImportError as e:
        raise ImportError(
            "DOCX support requires: pip install python-docx  "
            "(or: uv sync --extra docx)"
        ) from e

    doc = await asyncio.to_thread(docx.Document, docx_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    full_text = "\n\n".join(paragraphs)
    logger.info("Extracted %d chars from DOCX (%d paragraphs)", len(full_text), len(paragraphs))
    return await _parse_text(full_text, source=docx_path, mode=mode, model=model)


_FORMAT_DISPATCH = {
    ".pdf": aparse_pdf,
    ".md": aparse_markdown,
    ".markdown": aparse_markdown,
    ".docx": aparse_docx,
    ".txt": None,  # handled specially
}


def parse_document(path: str, *, mode: str = "builtin", model: Optional[str] = None) -> PaperContent:
    """Sync: auto-detect format from extension and parse.

    Supported: .pdf, .md, .markdown, .docx, .txt
    """
    return asyncio.run(aparse_document(path, mode=mode, model=model))


async def aparse_document(
    path: str, *, mode: str = "builtin", model: Optional[str] = None
) -> PaperContent:
    """Async: auto-detect format from extension and parse."""
    ext = os.path.splitext(path)[1].lower()
    if ext not in _FORMAT_DISPATCH:
        raise ValueError(
            f"Unsupported file format '{ext}'. "
            f"Supported: {', '.join(sorted(_FORMAT_DISPATCH.keys()))}"
        )
    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        return await _parse_text(text, source=path, mode=mode, model=model)
    handler = _FORMAT_DISPATCH[ext]
    return await handler(path, mode=mode, model=model)


async def _parse_text(
    full_text: str,
    *,
    source: str = "text",
    mode: str = "builtin",
    model: Optional[str] = None,
) -> PaperContent:
    """Core parsing logic: text → PaperContent."""
    pc = PaperContent(full_text=full_text)
    pc.title = _extract_title(source, full_text)
    pc.abstract = _extract_abstract(full_text)

    if mode == "agent":
        # Mode B: FAISS semantic retrieval → LLM
        _ensure_mode_b_deps()
        vectorstore = await _build_vectorstore(full_text)
        # 3 section extractions are independent → run in parallel
        pc.methodology, pc.data_description, pc.signal_logic = await asyncio.gather(
            _extract_section_semantic(vectorstore, METHODOLOGY_PROMPT, _methodology_queries(), model=model),
            _extract_section_semantic(vectorstore, DATA_DESCRIPTION_PROMPT, _data_queries(), model=model),
            _extract_section_semantic(vectorstore, SIGNAL_LOGIC_PROMPT, _signal_queries(), model=model),
        )
    else:
        # Mode A (builtin): send as much text as fits in LLM context.
        # pymupdf4llm markdown averages ~3K chars/page, so 100K covers
        # ~33 pages — enough for most quant finance papers.
        # Papers exceeding this still keep head + tail for coverage.
        if len(full_text) > 100_000:
            ctx = full_text[:90_000] + "\n\n[...truncated...]\n\n" + full_text[-10_000:]
        else:
            ctx = full_text
        # 3 section extractions are independent → run in parallel
        pc.methodology, pc.data_description, pc.signal_logic = await asyncio.gather(
            _extract_section_direct(ctx, METHODOLOGY_PROMPT, model=model),
            _extract_section_direct(ctx, DATA_DESCRIPTION_PROMPT, model=model),
            _extract_section_direct(ctx, SIGNAL_LOGIC_PROMPT, model=model),
        )

    logger.info(
        "Parsed: title=%s, methodology=%d chars, data=%d chars, signal=%d chars",
        pc.title[:50],
        len(pc.methodology),
        len(pc.data_description),
        len(pc.signal_logic),
    )
    return pc


# ── Heuristic extractors ─────────────────────────────────────


def _extract_title(source: str, full_text: str) -> str:
    title_match = re.search(r"^#\s+(.+?)$", full_text[:500], re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    return os.path.basename(source).replace(".pdf", "").replace("_", " ")


def _extract_abstract(full_text: str) -> str:
    m = re.search(
        r"(?:^|\n)#*\s*Abstract\s*\n+(.*?)(?:\n#{1,3}\s+|\n\n[A-Z])",
        full_text[:3000],
        re.IGNORECASE | re.DOTALL,
    )
    if m:
        return m.group(1).strip()
    return full_text[:1500]


# ── Mode A: direct extraction ────────────────────────────────


async def _extract_section_direct(ctx: str, prompt_template: str, *, model: Optional[str] = None) -> str:
    prompt = prompt_template.format(context=ctx)
    return await achat(prompt, system=SYSTEM_PROMPT, model=model)


# ── Mode B: semantic retrieval extraction ─────────────────────


async def _build_vectorstore(full_text: str):
    splitter = _splitter_cls(chunk_size=1500, chunk_overlap=200)
    docs = splitter.create_documents([full_text])
    vectorstore = await asyncio.to_thread(_faiss.from_documents, docs, _embeddings)
    logger.info("Built FAISS index: %d chunks", len(docs))
    return vectorstore


def _retrieve_context(vectorstore, queries: list[str], k: int = 3) -> str:
    seen: set[str] = set()
    unique = []
    for q in queries:
        for doc in vectorstore.similarity_search(q, k=k):
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                unique.append(doc.page_content)
    return "\n\n".join(unique)


async def _extract_section_semantic(
    vectorstore, prompt_template: str, queries: list[str], *, model: Optional[str] = None
) -> str:
    ctx = _retrieve_context(vectorstore, queries)
    prompt = prompt_template.format(context=ctx)
    return await achat(prompt, system=SYSTEM_PROMPT, model=model)


# ── Query banks ──────────────────────────────────────────────


def _methodology_queries() -> list[str]:
    return [
        "trading strategy methodology how the strategy works",
        "signal generation entry exit rules portfolio construction",
        "investment approach alpha generation process",
        "portfolio formation rebalancing weighting scheme",
        "cross-sectional sorting quantile double sort factor",
    ]


def _data_queries() -> list[str]:
    return [
        "data sample CRSP Compustat database time period frequency",
        "asset universe filters exclusions selection criteria",
        "fundamental data price volume alternative data",
        "stock selection market capitalization exchange NYSE AMEX NASDAQ",
        "benchmark S&P 500 CRSP value-weighted index",
    ]


def _signal_queries() -> list[str]:
    return [
        "buy signal long position entry when to buy",
        "sell signal short exit when to sell",
        "technical indicators threshold parameter formula",
        "if then conditional logic rule trading condition",
        "momentum return reversal factor ranking sorting",
        "Table results performance backtest empirical",
    ]
