# Paper2Spec — PDF → Strategy Specification

Convert quantitative finance research papers into structured, machine-readable
strategy specifications — with automatic multi-strategy detection.

## What This Does

Given a **PDF** of a quantitative finance paper, paper2spec:

1. **Parses** the paper into structured sections (methodology, signal logic,
   data requirements) via dual-mode extraction (direct LLM or FAISS RAG).
2. **Detects** if the paper contains multiple independent strategies (Layer 0).
3. **Extracts** a complete specification per strategy through 4 focused LLM
   calls (metadata → indicators → logic pipeline → execution plan).
4. **Renders** all outputs in dual format: machine-readable JSON +
   human-readable Markdown.

## Quick Start

### One-Shot Analysis (recommended)

```bash
uv run python scripts/analyze.py paper.pdf -o library/my_paper/
```

Produces:
```
library/my_paper/
├── paper.pdf       # Original PDF (auto-copied)
├── content.json    # PaperContent (machine-readable)
├── content.md      # PaperContent (human-readable)
├── spec.json       # ExtractionResult with all strategies
├── spec.md         # Strategy summary (human-readable)
└── metadata.json   # Analysis metadata
```

### Step-by-Step Pipeline

```bash
# 1. Search for papers (optional)
uv run python scripts/search.py "momentum trading strategy" -n 5

# 2. Parse PDF → PaperContent
uv run python scripts/parse.py paper.pdf -o content.json

# 3. Extract PaperContent → ExtractionResult (multi-strategy)
uv run python scripts/extract.py content.json -o spec.json
```

## Scripts Reference

### `scripts/analyze.py` — Full Pipeline (recommended)

```
uv run python scripts/analyze.py <pdf> [-o DIR] [--parser-mode builtin|agent] [--model MODEL]
```

| Flag | Default | Description |
|------|---------|-------------|
| `-o, --output-dir` | `<PAPER2SPEC_LIBRARY_PATH>/<slug>/` | Output directory |
| `--parser-mode` | `builtin` | `builtin` (fast, <40 pages) or `agent` (FAISS semantic retrieval) |
| `--extractor-mode` | `multilayer` | `multilayer` (recommended) or `single` (legacy) |
| `--model` | env `PAPER2SPEC_MODEL` | Override LLM model |

### `scripts/parse.py` — PDF → PaperContent

```
uv run python scripts/parse.py <pdf> [--mode builtin|agent] [--model MODEL] [-o FILE]
```

### `scripts/extract.py` — PaperContent → ExtractionResult

```
uv run python scripts/extract.py <content.json> [--mode multilayer|single] [--model MODEL] [-o FILE]
```

### `scripts/search.py` — Academic Paper Search

```
uv run python scripts/search.py <query> [--sources arxiv ssrn] [-n 10] [-o FILE]
```

## Output Formats

### ExtractionResult (spec.json)

```json
{
  "paper_title": "Pairs Trading: Does Volatility Timing Matter?",
  "num_detected": 3,
  "strategies": [
    {
      "strategy_name": "Minimum Distance Pairs Trading",
      "strategy_type": "technical",
      "asset_class": ["equity"],
      "description": "...",
      "indicators": [...],
      "logic_pipeline": [...],
      "execution_plan": [...],
      "risk_management": [...]
    }
  ]
}
```

### PaperContent (content.json)

```json
{
  "title": "...",
  "abstract": "...",
  "methodology": "...",
  "data_description": "...",
  "signal_logic": "...",
  "full_text": "..."
}
```

## Parser Mode Selection

Pick automatically based on paper length — do not ask the user:

| Condition | Mode | Reason |
|-----------|------|--------|
| PDF ≤ 60 pages | `builtin` (Mode A) | Fast. 100K char threshold covers ~33 pages. |
| PDF 60-100 pages | `builtin` (Mode A) | Truncation keeps first 90K + last 10K chars. |
| PDF > 100 pages | `agent` (Mode B) | FAISS semantic retrieval. Requires `[agent]` extra. |

## Multi-Strategy Detection

| Paper | Strategies Detected |
|-------|-------------------|
| Tactical Asset Allocation (Faber) | 1: GTAA with SMA timing |
| Pairs Trading (Goncalves-Pinto et al.) | 3: Distance, Stationarity, Cointegration |
| Value and Momentum Everywhere (Asness et al.) | 2: Value Factor, Momentum Factor |

**Detection rules** (conservative):
- Parameter variations → same strategy
- Long-only vs long-short variants → same strategy, different execution plans
- Fundamentally different signal logic → separate strategies

## Module Structure

```
paper2spec/
├── __init__.py        # v0.3.0
├── models.py          # PaperContent, StrategySpec, ExtractionResult
├── parser.py          # PDF → PaperContent (builtin or FAISS)
├── extractor.py       # PaperContent → ExtractionResult (Layer 0-4)
├── render.py          # JSON → Markdown renderers
├── pdf_utils.py       # Hybrid PDF extraction
├── llm.py             # litellm wrapper
├── prompts.py         # Layer 0-4 prompt templates
└── search.py          # arXiv + SSRN search
```

## Limitations

- **Mode A**: Truncates to first 90K + last 10K chars for >100K text.
- **SSRN search**: Best-effort HTML scraping — may break if SSRN changes layout.
- **Tables/formulas**: Not yet extracted (reserved fields in PaperContent).
- **Multi-strategy**: Conservative detector — may merge borderline-distinct strategies.
