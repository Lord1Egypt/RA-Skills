---
name: opg
description: "Academic literature discovery and citation network analysis. Multi-source search across arXiv, DBLP, Semantic Scholar, and Google Scholar. Build citation networks (references from PDF parsing, citations from Google Scholar), get recommendations, monitor new papers, analyze topics, parse PDFs, import from Zotero, generate research summaries, export as BibTeX/CSV/Markdown/JSON, and generate interactive HTML graph visualizations. Use when user asks about finding papers, literature review, citation analysis, research trends, or visualizing citation networks."
allowed-tools: Read, Write, Edit, Bash
---

# OpenPaperGraph — Literature Discovery & Citation Analysis

You are a research assistant with access to a CLI tool for academic literature discovery and analysis.

## Setup

The CLI is located at: `SKILL_DIR/openpapergraph_cli.py`

Before first use, ensure dependencies are installed:
```bash
pip install httpx pymupdf scholarly
```

All commands output JSON to stdout. Run from the `SKILL_DIR` directory.

## Architecture: Multi-Source

This tool reduces dependency on any single data source:

| Task | Primary Sources | Fallback |
|---|---|---|
| Search | arXiv + DBLP + S2 | Deduplicated, sorted by citations |
| References | Download PDF → parse reference list | S2 API |
| Citations | Google Scholar | S2 API |
| Citation counts | Google Scholar | S2 |
| Recommendations | S2 Recommendations API | — |
| Reference resolution | arXiv → S2 → CrossRef → OpenAlex | Multi-cascade |

## Available Commands

### 1. Search Papers

Multi-source search across arXiv, DBLP, and Semantic Scholar. Supports conference filtering.

```bash
python SKILL_DIR/openpapergraph_cli.py search "QUERY" --source SOURCE --venue VENUE --limit N
```

- `--source`: `all` (default, multi-source), `arxiv`, `dblp`, or `s2`
- `--venue`: Filter by conference — `ICLR`, `NeurIPS`, `ICML`, `ACL`, `EMNLP`, `NAACL`, `WebConf`, `KDD`
- `--limit`: Max results (default 20)

**When to use**: User asks to find papers, search for literature, or look up specific topics/conferences.

### 2. Build Citation Network

Construct a citation graph from seed papers. References come from PDF parsing (downloaded from arXiv/Unpaywall), citations from Google Scholar. Falls back to S2 when needed.

```bash
python SKILL_DIR/openpapergraph_cli.py graph PAPER_ID1 PAPER_ID2 --depth 1 --output graph.json
```

- Paper IDs can be: S2 hex ID (`204e3073...`), arXiv ID (`ARXIV:1706.03762`), DOI (`DOI:10.1145/...`), paper title (`"attention is all you need"`), PDF path (`paper.pdf`), BibTeX file (`refs.bib`), or Zotero CSL-JSON export (`zotero.json`)
- `--depth`: Expansion depth (1 or 2, default 1)
- `--output`: Save graph to file for later analysis/export

**When to use**: User wants to explore the citation landscape around specific papers.

### 3. Paper Recommendations

Get related paper recommendations based on one or more papers (via S2 Recommendations API).

```bash
python SKILL_DIR/openpapergraph_cli.py recommend PAPER_ID1 PAPER_ID2 --limit 10
```

- Also accepts paper titles and PDF paths as input

**When to use**: User wants to discover related or similar papers they may have missed.

### 4. Monitor New Papers

Check for recently published papers on a research topic (multi-source: arXiv + DBLP + S2, citation counts enriched via Google Scholar).

```bash
python SKILL_DIR/openpapergraph_cli.py monitor "TOPIC" --year-from 2025 --limit 20
```

**When to use**: User wants to stay updated on latest publications in a field.

### 5. Topic Analysis

Analyze a citation graph for topics, keyword distribution, year trends, and top authors.

```bash
python SKILL_DIR/openpapergraph_cli.py analyze graph.json
```

**When to use**: User wants to understand the thematic structure of a set of papers.

### 6. Research Summary

Generate a research summary from a citation graph. Uses LLM if any provider is configured, otherwise falls back to extractive analysis.

```bash
python SKILL_DIR/openpapergraph_cli.py summary graph.json --style STYLE
python SKILL_DIR/openpapergraph_cli.py summary graph.json --provider deepseek --model deepseek-chat
```

- `--style`: `overview` (default), `trends`, or `gaps`
- `--provider`: LLM provider name (e.g. `openai`, `deepseek`, `qwen`, `zhipu`, `moonshot`)
- `--model`: Override the provider's default model

**When to use**: User wants a quick overview of a research area or to identify trends/gaps.

### 7. PDF Reference Extraction

Extract references from a PDF paper, resolving via multi-source cascade (arXiv → S2 → CrossRef → OpenAlex).

```bash
python SKILL_DIR/openpapergraph_cli.py pdf /path/to/paper.pdf
python SKILL_DIR/openpapergraph_cli.py pdf /path/to/paper.pdf --use-grobid
```

- `--use-grobid`: Use GROBID for structured extraction (requires Docker service on port 8070)
- Returns: resolved papers, unresolved references, and resolve rate

**When to use**: User provides a PDF and wants to find/analyze its references.

### 7b. Build Graph from PDF Reference Lists

Build a citation graph directly from one or more PDF papers' reference lists.

```bash
python SKILL_DIR/openpapergraph_cli.py graph-from-pdf paper.pdf [paper2.pdf ...] --output graph.json
python SKILL_DIR/openpapergraph_cli.py graph-from-pdf paper.pdf --depth 1 --include-unresolved -o graph.json
```

- `--depth 0` (default): Only PDF references. `--depth 1`: Also expand resolved papers.
- `--include-unresolved`: Keep unresolved references as nodes in the graph (marked `resolved=false`)
- `--use-grobid`: Use GROBID for structured extraction
- References resolved via: arXiv → Semantic Scholar → CrossRef → OpenAlex (multi-source cascade)

**When to use**: User has PDF papers and wants a citation graph faithful to the actual reference lists.

### 8. Zotero Import

Import papers from a Zotero library or collection.

```bash
python SKILL_DIR/openpapergraph_cli.py zotero --user-id ID --api-key KEY [--collection KEY] [--list-collections]
```

**When to use**: User wants to import their existing Zotero library for analysis.

### 9. Export

Export a citation graph as BibTeX, CSV, Markdown, or JSON. All formats sort papers by year descending.

```bash
python SKILL_DIR/openpapergraph_cli.py export graph.json --format bibtex --output refs.bib
python SKILL_DIR/openpapergraph_cli.py export graph.json --format csv --output papers.csv
python SKILL_DIR/openpapergraph_cli.py export graph.json --format markdown --output papers.md
python SKILL_DIR/openpapergraph_cli.py export graph.json --format json --output papers.json
```

- `--format`: `bibtex` (default), `csv`, `markdown`, or `json`
- CSV/Markdown/JSON include full fields: id, title, authors, year, citations, source, url, doi, arxiv_id, abstract

**When to use**: User wants to save results for use in a reference manager, spreadsheet, or documentation.

### 9b. Export Interactive HTML Graph

Export a citation graph as a self-contained interactive HTML visualization.

```bash
python SKILL_DIR/openpapergraph_cli.py export-html graph.json --output graph.html
python SKILL_DIR/openpapergraph_cli.py export-html graph.json --output graph.html --title "My Research" --summary --inline
```

- `--title`: Custom page title (default: "Paper Graph")
- `--summary`: Pre-generate AI summary at export time (requires LLM API key in env). Result is embedded; API key is NOT.
- `--inline`: Inline vis-network JS for fully offline use (~500KB larger, no CDN needed)
- `--provider` / `--model`: Override LLM provider/model for `--summary`
- **Layout**: Semantic left-to-right hierarchy — References (LEFT) → Seeds (CENTER) → Citations (RIGHT)
- **Node types**: Seeds (purple stars), References (blue circles), Citations (green diamonds), with legend
- **Features**: bidirectional hover linking, type filter, search/filter, in-page export, seed source management (add/remove seeds)
- **Summary modes**: (A) Pre-generate with `--summary`, (B) Runtime API key (20+ providers), (C) Manual copy/paste (CORS-proof)
- Security: API keys are **never** embedded in the HTML output

**When to use**: User wants a visual, interactive exploration of the citation network, or wants to share a browsable graph.

### 9b. Interactive Graph Server (`serve`)

Start a local HTTP server for interactive graph management. Unlike `export-html` (static, read-only), `serve` lets users add papers, convert nodes to seeds, remove seeds, and all changes persist to the graph JSON file.

```bash
python SKILL_DIR/openpapergraph_cli.py serve graph.json --port 8787
```

- `--port`: Server port (default: 8787)
- `--title`: Custom page title
- **Add papers**: "+ Add Paper" button in toolbar. Input via title/ID, BibTeX, or PDF upload. Toggle "Treat as Seed Paper" to control expansion.
- **Seed**: Full expansion — fetches references + citations from S2/Google Scholar, adds nodes + edges
- **Non-seed**: Lightweight — only checks relationships with existing seeds, no expansion
- **Convert to seed**: Click any non-seed paper in the list → "⬆ Convert to Seed" button appears. Also available in the node tooltip when clicking graph nodes.
- **Remove seed**: Seeds/Sources tab → "Remove" button. Deletes seed + exclusive connections.
- **Persistent**: All changes immediately written to graph JSON file. Survives page refresh.
- **Dedup**: Papers matched by DOI > arXiv ID > title+year similarity (no duplicates)

**When to use**: User wants to interactively build and manage a citation network through the browser, with all changes persisted. Use `export-html` instead when you want a static file for sharing.

### 10. Remove Seed Paper

Remove a seed paper and all papers exclusively connected to it from a graph.

```bash
python SKILL_DIR/openpapergraph_cli.py remove-seed graph.json "paper_id_or_title"
```

- Accepts paper ID or title substring (fuzzy match)
- Removes the seed + papers connected only to that seed (not shared with other seeds)
- Cleans up all incident edges
- Overwrites the graph file (use `-o` to save to a different file)

### 11. Remove Non-Seed Paper

Remove a single non-seed paper from a graph.

```bash
python SKILL_DIR/openpapergraph_cli.py remove-paper graph.json "paper_id_or_title"
```

- Accepts paper ID or title substring (fuzzy match)
- Only works for non-seed papers (use `remove-seed` for seeds)
- Cleans up all incident edges
- Overwrites the graph file (use `-o` to save to a different file)

### 12. List Conferences

Show supported conference venues for filtering.

```bash
python SKILL_DIR/openpapergraph_cli.py conferences
```

### 13. List LLM Providers

Show all 20 supported LLM providers and whether their API key is configured.

```bash
python SKILL_DIR/openpapergraph_cli.py llm-providers
```

## Workflow Guidelines

1. **Start with search** — Help the user find relevant seed papers first (default: multi-source)
2. **Build a graph** — Use seed paper IDs to construct a citation network, save to a `.json` file
3. **Explore interactively** — Use `serve` to open the graph in browser, add papers, convert to seeds (`serve`)
4. **Analyze** — Run topic analysis or generate a summary on the saved graph
5. **Discover more** — Use recommendations to find papers the user may have missed
6. **Export** — Save results as BibTeX/CSV/Markdown/JSON for the user's reference manager
7. **Share** — Generate a static HTML graph for sharing/viewing (`export-html`)

## Output Format

All commands output JSON to stdout. When presenting results to the user:
- Show paper titles, authors, year, and citation counts in a readable format
- For large result sets, summarize the top results and mention the total count
- Paper IDs can be: S2 hex IDs, arXiv IDs (`ARXIV:xxxx`), DOIs (`DOI:xxxx`), paper titles, or PDF file paths
- The `source` field in results indicates where each paper came from (arxiv, semantic_scholar, google_scholar, crossref, openalex, dblp)

## Environment Variables

### `S2_API_KEY` (Recommended)
Semantic Scholar API key. Free at [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api).
- **Purpose**: Authenticates requests to the S2 API (paper search, citation data, recommendations)
- **Why needed**: Without it, S2 enforces strict rate limiting — frequent calls return 429 errors
- **Role**: S2 is the **fallback** in the multi-source architecture — when PDF download or Google Scholar fails, the system falls back to S2. Also the **exclusive source** for the `recommend` command

### LLM Provider API Key (Optional — any one of 20 providers)
The `summary` command supports **20 LLM providers**. Set any one API key to enable LLM-powered summaries:

**US**: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `DEEPSEEK_API_KEY`, `GROQ_API_KEY`, `TOGETHER_API_KEY`, `FIREWORKS_API_KEY`, `MISTRAL_API_KEY`, `XAI_API_KEY`, `PERPLEXITY_API_KEY`, `OPENROUTER_API_KEY`

**Chinese**: `ZHIPUAI_API_KEY` (智谱), `MOONSHOT_API_KEY` (月之暗面), `BAICHUAN_API_KEY` (百川), `YI_API_KEY` (零一万物), `DASHSCOPE_API_KEY` (通义千问), `ARK_API_KEY` (豆包), `MINIMAX_API_KEY`, `STEPFUN_API_KEY` (阶跃星辰), `SENSENOVA_API_KEY` (商汤)

**Custom**: Set `LLM_API_KEY` + `LLM_BASE_URL` + `LLM_MODEL` for any OpenAI-compatible endpoint.

**Additional environment variables:**
- `LLM_PROVIDER`: Explicitly select LLM provider (alternative to `--provider` CLI flag)
- `LLM_MODEL`: Override default model for the selected provider (alternative to `--model` CLI flag)
- `TMPDIR`: Custom directory for PDF download cache (defaults to system temp)

Without any LLM key, `summary` uses extractive analysis and `export-html` hides the AI summary panel. All other commands are unaffected. Run `llm-providers` to check status.

## Cross-Tool Compatibility

This CLI is designed to be called by any AI coding tool (Claude Code, OpenClaw, Codex, etc.):
- All output is structured JSON on stdout
- Errors go to stderr
- Exit code 0 = success, 1 = argument error, 2 = runtime error
- No interactive input required — all parameters via command-line flags
