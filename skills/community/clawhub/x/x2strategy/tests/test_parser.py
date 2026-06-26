"""Tests for paper2spec.parser — Mode A, Mode B, and helper functions.

Strategy:
  - Unit tests: mock ``achat`` to be deterministic — test truncation logic,
    branch selection, title/abstract extraction, query banks.
  - Integration tests: use real FAISS (if available) with mock LLM to verify
    the chunking → retrieval → prompt pipeline end-to-end.
  - Skip markers: Mode B tests require ``[agent]`` extras.
"""

import asyncio
import os
import textwrap
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from paper2spec.models import PaperContent
from paper2spec.parser import (
    _extract_abstract,
    _extract_title,
    _methodology_queries,
    _data_queries,
    _signal_queries,
    _parse_text,
    _retrieve_context,
    parse_text,
)


# ── Helpers ──────────────────────────────────────────────────


def _fake_achat(prompt: str, *, system: str = "", model=None) -> str:
    """Return a deterministic stub based on which prompt template was used."""
    if "methodology" in prompt.lower()[:200]:
        return "MOCKED_METHODOLOGY"
    if "signal" in prompt.lower()[:200]:
        return "MOCKED_SIGNAL"
    if "data" in prompt.lower()[:200]:
        return "MOCKED_DATA"
    return "MOCKED_UNKNOWN"


async def _async_fake_achat(prompt: str, *, system: str = "", model=None) -> str:
    return _fake_achat(prompt, system=system, model=model)


def _get_prompt(call):
    """Extract the prompt string from a mock call."""
    return call.args[0] if call.args else call.kwargs.get("prompt", "")


# ── Title extraction ─────────────────────────────────────────


class TestExtractTitle:
    def test_markdown_h1(self):
        text = "# My Great Paper\n\nAbstract goes here"
        assert _extract_title("some.pdf", text) == "My Great Paper"

    def test_first_h1_only(self):
        text = "# First Title\n\n# Second Title\n\n"
        assert _extract_title("x.pdf", text) == "First Title"

    def test_fallback_to_filename(self):
        text = "No heading here, just plain text about trading."
        assert _extract_title("my_cool_paper.pdf", text) == "my cool paper"

    def test_fallback_strips_extension(self):
        assert _extract_title("/path/to/Value_and_Momentum.pdf", "") == "Value and Momentum"

    def test_h1_in_first_500_chars(self):
        # Title heading beyond 500 chars should NOT be found
        text = "x" * 501 + "\n# Late Title\n"
        title = _extract_title("fallback.pdf", text)
        assert title == "fallback"  # falls back to filename

    def test_strips_whitespace(self):
        text = "#   Spaced Out Title   \n\nBody"
        assert _extract_title("x.pdf", text) == "Spaced Out Title"


# ── Abstract extraction ──────────────────────────────────────


class TestExtractAbstract:
    def test_standard_abstract(self):
        text = textwrap.dedent("""\
            # Title

            ## Abstract

            This paper studies momentum strategies.
            We find significant alpha.

            ## Introduction

            The literature on momentum...
        """)
        abstract = _extract_abstract(text)
        assert "momentum strategies" in abstract
        assert "Introduction" not in abstract

    def test_abstract_with_hash(self):
        text = "### Abstract\n\nShort abstract here.\n\n## Section 1"
        assert "Short abstract here" in _extract_abstract(text)

    def test_no_abstract_section(self):
        text = "Some paper text without an abstract heading. " * 20
        # Should fall back to first 1500 chars
        abstract = _extract_abstract(text)
        assert len(abstract) <= 1500

    def test_abstract_case_insensitive(self):
        text = "\nABSTRACT\n\nWe study factor investing.\n\n## Intro"
        assert "factor investing" in _extract_abstract(text)


# ── Query banks ──────────────────────────────────────────────


class TestQueryBanks:
    def test_methodology_queries_non_empty(self):
        qs = _methodology_queries()
        assert len(qs) >= 3
        assert all(isinstance(q, str) and len(q) > 10 for q in qs)

    def test_data_queries_non_empty(self):
        qs = _data_queries()
        assert len(qs) >= 3

    def test_signal_queries_non_empty(self):
        qs = _signal_queries()
        assert len(qs) >= 3

    def test_no_duplicate_queries(self):
        all_queries = _methodology_queries() + _data_queries() + _signal_queries()
        assert len(all_queries) == len(set(all_queries)), "Duplicate queries found"


# ── Mode A: truncation logic ─────────────────────────────────


class TestModeATruncation:
    """Verify the 100K truncation boundary and content preservation."""

    @pytest.fixture
    def short_text(self):
        """50K chars — should NOT be truncated."""
        return "A" * 50_000

    @pytest.fixture
    def medium_text(self):
        """99K chars — should NOT be truncated (just under threshold)."""
        return "B" * 99_000

    @pytest.fixture
    def long_text(self):
        """150K chars — SHOULD be truncated."""
        # Use distinct patterns to verify head/tail preservation
        head = "H" * 90_000
        middle = "M" * 50_000
        tail = "T" * 10_000
        return head + middle + tail

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_short_text_not_truncated(self, mock_achat, short_text):
        mock_achat.side_effect = _async_fake_achat
        pc = await _parse_text(short_text, source="test.pdf", mode="builtin")
        # The prompt should contain the full text (50K chars)
        # Verify achat was called 3 times (methodology, data, signal)
        assert mock_achat.call_count == 3
        # Each call's prompt should contain the full text without truncation marker
        for call in mock_achat.call_args_list:
            prompt = call.args[0] if call.args else call.kwargs.get("prompt", "")
            assert "[...truncated...]" not in prompt

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_medium_text_not_truncated(self, mock_achat, medium_text):
        mock_achat.side_effect = _async_fake_achat
        pc = await _parse_text(medium_text, source="test.pdf", mode="builtin")
        for call in mock_achat.call_args_list:
            prompt = call.args[0] if call.args else call.kwargs.get("prompt", "")
            assert "[...truncated...]" not in prompt

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_long_text_truncated(self, mock_achat, long_text):
        mock_achat.side_effect = _async_fake_achat
        pc = await _parse_text(long_text, source="test.pdf", mode="builtin")
        # Each prompt should contain the truncation marker
        for call in mock_achat.call_args_list:
            prompt = call.args[0] if call.args else call.kwargs.get("prompt", "")
            assert "[...truncated...]" in prompt

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_truncation_preserves_head_and_tail(self, mock_achat, long_text):
        mock_achat.side_effect = _async_fake_achat
        await _parse_text(long_text, source="test.pdf", mode="builtin")
        prompt = mock_achat.call_args_list[0].args[0]
        # Head (H chars) should be there
        assert "H" * 100 in prompt
        # Tail (T chars) should be there
        assert "T" * 100 in prompt

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_truncation_drops_middle(self, mock_achat, long_text):
        mock_achat.side_effect = _async_fake_achat
        await _parse_text(long_text, source="test.pdf", mode="builtin")
        prompt = mock_achat.call_args_list[0].args[0]
        # Middle (M chars) should be largely absent
        # There are 50K M chars in the original, but the truncated context
        # should not contain a long run of M's
        assert "M" * 1000 not in prompt

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_exact_boundary(self, mock_achat):
        """100_000 chars exactly — should NOT truncate."""
        text = "X" * 100_000
        mock_achat.side_effect = _async_fake_achat
        await _parse_text(text, source="test.pdf", mode="builtin")
        prompt = mock_achat.call_args_list[0].args[0]
        assert "[...truncated...]" not in prompt

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_one_over_boundary(self, mock_achat):
        """100_001 chars — should truncate."""
        text = "X" * 100_001
        mock_achat.side_effect = _async_fake_achat
        await _parse_text(text, source="test.pdf", mode="builtin")
        prompt = mock_achat.call_args_list[0].args[0]
        assert "[...truncated...]" in prompt

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_truncated_size(self, mock_achat):
        """Truncated context should be ~100K (90K head + marker + 10K tail)."""
        text = "X" * 200_000
        mock_achat.side_effect = _async_fake_achat
        await _parse_text(text, source="test.pdf", mode="builtin")
        prompt = mock_achat.call_args_list[0].args[0]
        # The context portion is 90K + ~20 (marker) + 10K = ~100020
        # Plus the prompt template wrapping
        # Just check it's significantly less than 200K
        assert len(prompt) < 150_000


# ── Mode A: output structure ──────────────────────────────────


class TestModeAOutput:
    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_returns_paper_content(self, mock_achat):
        mock_achat.side_effect = _async_fake_achat
        text = "# Test Paper\n\n## Abstract\n\nWe study things.\n\n## Intro\n\nHello"
        pc = await _parse_text(text, source="test.pdf", mode="builtin")
        assert isinstance(pc, PaperContent)
        assert pc.title == "Test Paper"
        assert pc.full_text == text
        assert pc.methodology == "MOCKED_METHODOLOGY"
        assert pc.signal_logic == "MOCKED_SIGNAL"
        assert pc.data_description == "MOCKED_DATA"

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_abstract_extracted(self, mock_achat):
        mock_achat.side_effect = _async_fake_achat
        text = "# Title\n\n## Abstract\n\nMomentum is profitable.\n\n## Introduction"
        pc = await _parse_text(text, source="x.pdf", mode="builtin")
        assert "Momentum is profitable" in pc.abstract

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_three_llm_calls(self, mock_achat):
        mock_achat.side_effect = _async_fake_achat
        await _parse_text("some text", source="x.pdf", mode="builtin")
        assert mock_achat.call_count == 3


# ── Sync wrapper ──────────────────────────────────────────────


class TestSyncWrapper:
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    def test_parse_text_sync(self, mock_achat):
        mock_achat.side_effect = _async_fake_achat
        pc = parse_text("# Title\n\nBody text", source="test", mode="builtin")
        assert isinstance(pc, PaperContent)
        assert pc.methodology == "MOCKED_METHODOLOGY"


# ── Mode B: unit tests (mocked FAISS) ────────────────────────


class TestModeBBranching:
    """Verify that mode='agent' takes the FAISS path."""

    @pytest.mark.asyncio
    @patch("paper2spec.parser._extract_section_semantic", new_callable=AsyncMock)
    @patch("paper2spec.parser._build_vectorstore", new_callable=AsyncMock)
    @patch("paper2spec.parser._ensure_mode_b_deps")
    async def test_agent_mode_calls_semantic(self, mock_deps, mock_build, mock_extract):
        mock_build.return_value = MagicMock()  # fake vectorstore
        mock_extract.return_value = "semantic result"

        pc = await _parse_text("some text", source="test.pdf", mode="agent")

        mock_deps.assert_called_once()
        mock_build.assert_called_once()
        assert mock_extract.call_count == 3  # methodology, data, signal
        assert pc.methodology == "semantic result"
        assert pc.data_description == "semantic result"
        assert pc.signal_logic == "semantic result"

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_builtin_mode_does_not_call_semantic(self, mock_achat):
        mock_achat.side_effect = _async_fake_achat
        with patch("paper2spec.parser._ensure_mode_b_deps") as mock_deps:
            await _parse_text("text", source="x.pdf", mode="builtin")
            mock_deps.assert_not_called()


# ── Mode B: retrieve_context ─────────────────────────────────


class TestRetrieveContext:
    """Test the deduplication logic in _retrieve_context."""

    def _make_doc(self, content: str):
        """Create a minimal doc-like object."""
        doc = MagicMock()
        doc.page_content = content
        return doc

    def test_deduplication(self):
        vs = MagicMock()
        # Two queries return overlapping docs
        vs.similarity_search.side_effect = [
            [self._make_doc("chunk A"), self._make_doc("chunk B")],
            [self._make_doc("chunk B"), self._make_doc("chunk C")],
        ]
        result = _retrieve_context(vs, ["q1", "q2"], k=2)
        assert "chunk A" in result
        assert "chunk B" in result
        assert "chunk C" in result
        # chunk B should appear only once
        assert result.count("chunk B") == 1

    def test_empty_results(self):
        vs = MagicMock()
        vs.similarity_search.return_value = []
        result = _retrieve_context(vs, ["q1"], k=3)
        assert result == ""

    def test_preserves_order(self):
        vs = MagicMock()
        vs.similarity_search.side_effect = [
            [self._make_doc("first"), self._make_doc("second")],
            [self._make_doc("third")],
        ]
        result = _retrieve_context(vs, ["q1", "q2"], k=2)
        # first should appear before second, second before third
        assert result.index("first") < result.index("second")
        assert result.index("second") < result.index("third")


# ── Mode B: real FAISS integration ────────────────────────────


def _has_mode_b_deps() -> bool:
    try:
        from langchain_community.vectorstores import FAISS
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return True
    except ImportError:
        return False


@pytest.mark.skipif(not _has_mode_b_deps(), reason="Mode B deps not installed")
class TestModeBIntegration:
    """Integration tests using real FAISS + embeddings but mocked LLM."""

    @pytest.fixture
    def sample_paper_text(self):
        """A synthetic 'paper' with clearly separated sections."""
        return textwrap.dedent("""\
            # Momentum Factor Strategy

            ## Abstract

            We study time-series momentum across equity markets.
            Our strategy generates significant risk-adjusted returns.

            ## Data

            We use CRSP daily stock data from 1990 to 2020.
            The sample includes all NYSE, AMEX, and NASDAQ common stocks
            with share codes 10 and 11. We exclude stocks with price
            below $5 and market cap below the 20th NYSE percentile.
            The risk-free rate is from Kenneth French's data library.

            ## Methodology

            For each stock i at month t, we compute the trailing
            12-month return excluding the most recent month (12-1 momentum).
            Stocks are sorted into quintiles based on this signal.
            The long portfolio holds Q5 (winners), the short portfolio
            holds Q1 (losers). Portfolios are value-weighted and
            rebalanced monthly.

            The momentum signal for stock i is:
            MOM_i,t = (P_i,t-1 / P_i,t-12) - 1

            ## Signal Logic

            Entry: Go long when stock is in top quintile of 12-1 momentum.
            Exit: Sell when stock drops below median momentum.
            Rebalancing: Monthly, at the end of each month.
            Holding period: 1 month until next rebalance.

            ## Results

            The long-short portfolio earns 1.2% per month with t-stat 3.4.
            Table 3 shows the Fama-French five-factor alpha is 0.8% monthly.
            The strategy has a Sharpe ratio of 0.85 and maximum drawdown of 35%.
        """)

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_mode_b_end_to_end(self, mock_achat, sample_paper_text):
        """Full Mode B pipeline: text → chunks → FAISS → retrieve → LLM stub."""
        # Record what contexts get sent to the LLM
        captured_prompts = []

        async def recording_achat(prompt, *, system="", model=None):
            captured_prompts.append(prompt)
            return _fake_achat(prompt, system=system, model=model)

        mock_achat.side_effect = recording_achat
        pc = await _parse_text(sample_paper_text, source="momentum.pdf", mode="agent")

        # Basic output checks
        assert pc.title == "Momentum Factor Strategy"
        assert pc.methodology == "MOCKED_METHODOLOGY"
        assert pc.signal_logic == "MOCKED_SIGNAL"
        assert pc.data_description == "MOCKED_DATA"

        # 3 LLM calls (one per section)
        assert len(captured_prompts) == 3

        # The methodology prompt should contain retrieved chunks about methodology
        methodology_prompt = captured_prompts[0]
        assert "quintile" in methodology_prompt.lower() or "momentum" in methodology_prompt.lower()

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_mode_b_retrieves_relevant_chunks(self, mock_achat, sample_paper_text):
        """Verify semantic retrieval actually finds the right sections."""
        from paper2spec.parser import _build_vectorstore, _retrieve_context

        # Build real vectorstore
        from paper2spec.parser import _ensure_mode_b_deps
        _ensure_mode_b_deps()
        vectorstore = await _build_vectorstore(sample_paper_text)

        # Methodology queries should retrieve methodology-related chunks
        meth_ctx = _retrieve_context(vectorstore, _methodology_queries(), k=3)
        assert "quintile" in meth_ctx.lower() or "momentum" in meth_ctx.lower()
        assert "rebalanced" in meth_ctx.lower() or "portfolio" in meth_ctx.lower()

        # Data queries should retrieve data-related chunks
        data_ctx = _retrieve_context(vectorstore, _data_queries(), k=3)
        assert "crsp" in data_ctx.lower() or "nyse" in data_ctx.lower()

        # Signal queries should retrieve signal-related chunks
        signal_ctx = _retrieve_context(vectorstore, _signal_queries(), k=3)
        assert "long" in signal_ctx.lower() or "entry" in signal_ctx.lower()

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_mode_b_chunking_count(self, mock_achat, sample_paper_text):
        """Verify the text gets chunked into a reasonable number of pieces."""
        from paper2spec.parser import _build_vectorstore, _ensure_mode_b_deps
        _ensure_mode_b_deps()
        vectorstore = await _build_vectorstore(sample_paper_text)
        # Sample text is ~1500 chars → should be 1-3 chunks with 1500 chunk_size
        # (it's actually a bit more due to markdown)
        n_docs = vectorstore.index.ntotal
        assert 1 <= n_docs <= 5, f"Expected 1-5 chunks, got {n_docs}"

    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    async def test_mode_b_large_text(self, mock_achat):
        """Mode B should handle large texts without truncation."""
        # Create 200K text — Mode B should chunk it all, no truncation
        large_text = "# Big Paper\n\n" + ("The momentum strategy. " * 10_000)
        mock_achat.side_effect = _async_fake_achat
        pc = await _parse_text(large_text, source="big.pdf", mode="agent")
        # Should still work — all 3 sections extracted
        assert pc.methodology == "MOCKED_METHODOLOGY"
        assert pc.signal_logic == "MOCKED_SIGNAL"
        assert pc.data_description == "MOCKED_DATA"


# ── Mode B: dependency guard ──────────────────────────────────


class TestModeBDependencyGuard:
    def test_ensure_deps_raises_without_packages(self):
        """If langchain is not installed, _ensure_mode_b_deps should raise ImportError."""
        import paper2spec.parser as p
        # Save and reset module-level state
        old_faiss, old_splitter, old_emb = p._faiss, p._splitter_cls, p._embeddings
        p._faiss = None
        p._splitter_cls = None
        p._embeddings = None
        try:
            # Must also null submodule entries so Python doesn't resolve from cache
            with patch.dict("sys.modules", {
                "langchain_community": None,
                "langchain_community.vectorstores": None,
                "langchain_community.embeddings": None,
                "langchain_text_splitters": None,
            }):
                with pytest.raises(ImportError, match="Mode B requires"):
                    p._ensure_mode_b_deps()
        finally:
            p._faiss = old_faiss
            p._splitter_cls = old_splitter
            p._embeddings = old_emb


# ── PDF path (mocked extraction) ──────────────────────────────


class TestParsePDF:
    @pytest.mark.asyncio
    @patch("paper2spec.parser.achat", new_callable=AsyncMock)
    @patch("paper2spec.parser.PDFExtractor.extract_text")
    async def test_aparse_pdf(self, mock_extract, mock_achat):
        from paper2spec.parser import aparse_pdf
        mock_extract.return_value = "# PDF Title\n\n## Abstract\n\nExtracted text.\n\n## Intro"
        mock_achat.side_effect = _async_fake_achat

        pc = await aparse_pdf("/fake/path.pdf", mode="builtin")
        mock_extract.assert_called_once_with("/fake/path.pdf")
        assert pc.title == "PDF Title"
        assert pc.methodology == "MOCKED_METHODOLOGY"
