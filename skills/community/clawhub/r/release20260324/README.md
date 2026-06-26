<p align="center">
  <img alt="OpenPaperGraph" src="figures/logo-part-light-full.png" width="420">
</p>

<h3 align="center">The research copilot for the OpenClaw era</h3>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/dependencies-3-green.svg" alt="3 Dependencies">
  <img src="https://img.shields.io/badge/LLM_providers-20+-orange.svg" alt="20+ LLM Providers">
  <img src="https://img.shields.io/badge/data_sources-8-purple.svg" alt="8 Data Sources">
  <img src="https://img.shields.io/badge/license-PolyForm%20Noncommercial%201.0.0-lightgrey.svg" alt="License">
</p>

<p align="center">
  <a href="README_CN.md">中文</a> | English
</p>

<p align="center">
  <b>Search 8 sources. Build citation graphs. Generate AI summaries.</b><br>
  Works as a Claude Code / OpenClaw <code>/opg</code> skill or standalone CLI.<br>
  No API keys required. 3 pip packages. One-line install.
</p>

---

## Why OpenPaperGraph?

In the age of AI agents like **Claude Code** and **OpenClaw**, researchers need tools that work *with* their workflow — not against it. OpenPaperGraph is designed to be the **research backbone** for AI-assisted development:

- **Agent-native** — JSON stdout, zero interactive input, composable with any AI tool
- **Multi-source resilient** — 8 data sources with automatic fallbacks; never blocked by a single API
- **Local-first** — your data stays on disk as simple JSON files, no cloud lock-in
- **Minimal footprint** — 3 dependencies, no database, no Docker (optional GROBID excepted)

---

## Quick Start

### Claude Code / OpenClaw Users

```bash
# One-line setup
bash install.sh --global

# Then in Claude Code:
#   /opg Search papers about LLM agent security
#   /opg Build a citation graph from ARXIV:1706.03762
```

### Standalone CLI

```bash
pip install httpx pymupdf scholarly

# Search → Build → Explore → Export
python openpapergraph_cli.py search "prompt injection" --limit 5 --pretty
python openpapergraph_cli.py graph ARXIV:1706.03762 -o graph.json
python openpapergraph_cli.py serve graph.json        # -> http://localhost:8787
python openpapergraph_cli.py export graph.json --format bibtex -o refs.bib
```

> No API keys needed. All core features work with free public APIs.

---

## Features at a Glance

| | Command | Description |
|---|---------|------------|
| **Discover** | `search` | Multi-source search across arXiv + DBLP + Semantic Scholar |
| | `recommend` | Related paper recommendations via S2 API |
| | `monitor` | Track recently published papers on a topic |
| **Build** | `graph` | Build citation networks from titles, IDs, PDFs, or BibTeX |
| | `graph-from-pdf` | Build graph directly from PDF reference lists |
| | `pdf` | Extract and resolve references from a PDF |
| | `zotero` | Import papers from Zotero library |
| **Manage** | `serve` | Interactive browser-based graph editor (persistent) |
| | `remove-seed` | Remove a seed paper and its exclusive connections |
| | `remove-paper` | Remove a non-seed paper from a graph |
| **Analyze** | `analyze` | Topic analysis: keywords, year trends, top authors |
| | `summary` | AI-powered or extractive research summaries |
| **Export** | `export` | BibTeX / CSV / Markdown / JSON |
| | `export-html` | Self-contained interactive HTML visualization |
| **Util** | `conferences` | List supported conference venue filters |
| | `llm-providers` | Show 20+ LLM providers and config status |

**Common flags**: `--output` / `-o` (save to file), `--pretty` (formatted JSON), `--quiet` (suppress progress)

---

## Typical Workflow

```
  Search          Build            Explore           Analyze          Export
  ──────>        ──────>          ──────>           ──────>         ──────>
  search    graph / graph-from-pdf   serve        analyze + summary    export / export-html
  recommend                      (browser UI)                       (bibtex, csv, md, html)
  monitor                        add / convert
                                 remove
```

```bash
# 1. Find seed papers
python openpapergraph_cli.py search "attention is all you need" --limit 5 --pretty

# 2. Build citation network
python openpapergraph_cli.py graph ARXIV:1706.03762 -o graph.json

# 3. Explore interactively (add papers, expand seeds — all changes saved)
python openpapergraph_cli.py serve graph.json

# 4. Analyze
python openpapergraph_cli.py analyze graph.json --pretty
python openpapergraph_cli.py summary graph.json --style overview --pretty

# 5. Export
python openpapergraph_cli.py export graph.json --format bibtex -o refs.bib
python openpapergraph_cli.py export-html graph.json -o graph.html --summary
```

---

## Architecture: Multi-Source by Design

OpenPaperGraph reduces dependency on any single data source by combining 8 academic databases with intelligent fallbacks:

| Task | Primary Sources | Fallback |
|------|----------------|----------|
| **Search** | arXiv + DBLP + Semantic Scholar | Deduplicated, sorted by citations |
| **References** | Download PDF -> parse reference list | S2 API |
| **Citations** | Google Scholar | S2 API |
| **Recommendations** | S2 Recommendations API | — |
| **PDF download** | arXiv -> Unpaywall (Open Access) | Direct URL |
| **Reference resolution** | arXiv -> CrossRef -> OpenAlex | Multi-cascade |

The tool continues to work even when individual APIs are down or rate-limited.

---

## Installation

### Prerequisites

- **Python 3.8+**
- **pip** package manager
- **Internet connection** (for querying academic APIs)

### Core Dependencies (3 packages)

```bash
pip install httpx pymupdf scholarly
```

| Package | Purpose |
|---------|---------|
| `httpx` | HTTP client for all API calls |
| `pymupdf` | PDF text extraction |
| `scholarly` | Google Scholar access (falls back to S2 if not installed) |

### Optional

```bash
pip install openai  # For LLM-powered summaries (20+ providers supported)
```

### API Keys (all optional)

```bash
export S2_API_KEY="..."          # Recommended: avoid S2 rate limiting (free key)
export OPENAI_API_KEY="sk-..."   # Or any of 20+ LLM providers for AI summaries
```

> **All commands work without any API keys.** arXiv, DBLP, CrossRef, OpenAlex, and Unpaywall are completely free.

---

## Commands Reference

<details>
<summary><b>search</b> — Multi-source paper search</summary>

```bash
python openpapergraph_cli.py search "transformer attention" --limit 10
python openpapergraph_cli.py search "large language model" --source arxiv
python openpapergraph_cli.py search "reinforcement learning" --source dblp --venue NeurIPS
```

| Flag | Default | Description |
|------|---------|-------------|
| `--source` | `all` | `all`, `arxiv`, `dblp`, or `s2` |
| `--venue` | — | `ICLR`, `NeurIPS`, `ICML`, `ACL`, `EMNLP`, `NAACL`, `WebConf`, `KDD` |
| `--limit` | 20 | Max results |
| `--offset` | 0 | Pagination offset |

</details>

<details>
<summary><b>graph</b> — Build citation network</summary>

Accepts multiple input formats:

| Input Type | Example |
|------------|---------|
| arXiv ID | `ARXIV:1706.03762` |
| DOI | `DOI:10.1145/3295222` |
| S2 hex ID | `204e3073870fae3d05bcbc2f6a8e263d9b72e776` |
| Paper title | `"attention is all you need"` |
| PDF file | `paper.pdf` |
| BibTeX file | `refs.bib` |
| Zotero JSON | `zotero_export.json` |

```bash
python openpapergraph_cli.py graph ARXIV:1706.03762 -o graph.json
python openpapergraph_cli.py graph "attention is all you need" "BERT" paper.pdf -o graph.json --depth 2
```

| Flag | Default | Description |
|------|---------|-------------|
| `--depth` | 1 | Expansion depth (2 = refs of refs) |
| `--include-unresolved` | false | Keep unresolved PDF references |
| `--use-grobid` | false | Use GROBID for PDF parsing |

#### Default Retrieval Limits

Each seed paper retrieves references and citations with the following built-in limits:

| Data | Source | Default Limit |
|------|--------|---------------|
| **References** | PDF parsing (local) | Unlimited (all refs in PDF) |
| **References** | S2 API (fallback) | 100 per paper |
| **Citations** | Google Scholar | 50 per paper |
| **Citations** | S2 API (fallback) | 50 per paper |
| **Depth > 1 expansion** | S2 API | 20 refs × top 10 cited papers |

These limits are hardcoded to balance completeness with API rate limits. They are not currently configurable via CLI flags. For papers with hundreds of citations, only the first 50 are retrieved; the remaining can be discovered by converting those papers to seeds via `serve`.

</details>

<details>
<summary><b>recommend</b> — Paper recommendations</summary>

```bash
python openpapergraph_cli.py recommend ARXIV:1706.03762 --limit 10 --pretty
```

Uses S2 Recommendations API. Accepts paper ID or title.

</details>

<details>
<summary><b>monitor</b> — Track new papers</summary>

```bash
python openpapergraph_cli.py monitor "LLM agent security" --year 2025 --limit 20
```

</details>

<details>
<summary><b>analyze</b> — Topic analysis</summary>

```bash
python openpapergraph_cli.py analyze graph.json --pretty
```

Returns: keywords, year distribution, top authors, topic clusters.

</details>

<details>
<summary><b>summary</b> — Research summary</summary>

```bash
python openpapergraph_cli.py summary graph.json --style overview --pretty
python openpapergraph_cli.py summary graph.json --provider deepseek --model deepseek-chat
```

Styles: `overview`, `trends`, `gaps`. Without LLM key, uses extractive analysis.

</details>

<details>
<summary><b>pdf</b> — PDF reference extraction</summary>

```bash
python openpapergraph_cli.py pdf paper.pdf --pretty
python openpapergraph_cli.py pdf paper.pdf --use-grobid  # Better accuracy
```

</details>

<details>
<summary><b>serve</b> — Interactive graph server</summary>

**Prerequisite**: You need a graph JSON file first. Build one with `graph` or `graph-from-pdf`:

```bash
# 1. Build a graph first
python openpapergraph_cli.py graph ARXIV:1706.03762 -o graph.json

# 2. Then start the server
python openpapergraph_cli.py serve graph.json --port 8787
# Open http://localhost:8787 in your browser
```

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | 8787 | HTTP server port |
| `--title` | `"Paper Graph"` | Page title shown in browser |

#### Browser UI Features

**Graph Visualization** (powered by vis.js)
- Interactive force-directed network layout with drag, zoom, and pan
- Color-coded nodes: seeds (purple stars), references (blue, left), citations (green, right)
- Year-based gradient coloring with a visual legend
- Hover tooltips showing title, authors, year, citation count, and abstract
- Click a node to highlight its direct connections

**Toolbar & Search**
- Real-time search across titles, authors, and years
- Filter by node type (All / Seed / Reference / Citation) and source database
- Paper count statistics displayed as chips (seeds, refs, cites)

**Add Paper** (server mode only)
- Click `+ Add Paper` button to open a modal with three input tabs:
  - **Title** — enter a paper title; the system resolves it via arXiv + Semantic Scholar
  - **BibTeX** — paste a BibTeX entry for direct import
  - **PDF** — drag-and-drop or click to upload a PDF; extracts metadata and references automatically
- Toggle **"Treat as Seed Paper"** to trigger full expansion (references + citations)
- Same retrieval limits as `graph` command (50 citations, 100 S2 refs per paper)
- SSE-powered real-time progress bar during graph expansion

**Convert to Seed**
- Hover over any non-seed node and click **"Convert to Seed Paper"** in the tooltip
- Triggers full expansion: downloads PDF, parses references, fetches citations
- Confirmation dialog with live progress tracking

**Remove Seed**
- Source panel lists all seed papers with reference/citation counts
- Click **Remove** to delete a seed and its exclusive connections
- Confirmation dialog prevents accidental deletion

**Metadata Enrichment**
- **Enrich** button fills in missing metadata (abstracts, citation counts, DOIs) for all papers

**Persistence**
- All mutations (add, convert, remove, enrich) are saved to the JSON file immediately
- Refresh the page at any time — your changes are preserved

**Sidebar**
- Scrollable paper list sorted by citation count, grouped by type
- Click any paper to locate and highlight it in the graph
- External links to Semantic Scholar, arXiv, and DOI pages

</details>

<details>
<summary><b>export</b> / <b>export-html</b> — Export graph data</summary>

```bash
python openpapergraph_cli.py export graph.json --format bibtex -o refs.bib
python openpapergraph_cli.py export graph.json --format csv -o papers.csv
python openpapergraph_cli.py export graph.json --format markdown -o papers.md
python openpapergraph_cli.py export-html graph.json -o graph.html --summary --inline
```

</details>

<details>
<summary><b>remove-seed</b> / <b>remove-paper</b> — Remove papers from graph</summary>

```bash
# Remove seed + its exclusive connections
python openpapergraph_cli.py remove-seed graph.json "ClawWorm"

# Remove a non-seed paper
python openpapergraph_cli.py remove-paper graph.json "some paper title"
```

Both support fuzzy title matching. Use `-o` to save to a different file.

</details>

<details>
<summary><b>/opg</b> — Claude Code / OpenClaw skill</summary>

When installed as a skill (`bash install.sh --global`), all commands can be invoked via natural language in Claude Code or OpenClaw:

| What you want | What to type |
|---------------|-------------|
| Search papers | `/opg Search papers about transformer attention` |
| Build graph | `/opg Build a citation network from ARXIV:1706.03762` |
| Recommendations | `/opg Recommend papers similar to ARXIV:1706.03762` |
| Interactive viewer | `/opg Start a graph server for graph.json` |
| Analyze | `/opg Analyze the citation network in graph.json` |
| Export | `/opg Export the citation network as BibTeX` |
| Monitor | `/opg Monitor new papers on LLM agent security since 2025` |
| PDF extraction | `/opg Extract references from paper.pdf` |

| | `/opg` Skill | Python CLI |
|---|-------------|------------|
| **Invocation** | Natural language | Command-line arguments |
| **Output** | AI auto-formats results | Raw JSON (`--pretty` for formatted) |
| **Multi-step** | AI chains steps automatically | Run each step manually |
| **Setup** | `bash install.sh --global` | `pip install httpx pymupdf scholarly` |

</details>

---

## Environment Variables

### S2_API_KEY (Recommended)

Free at [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api). Avoids rate limiting.

```bash
export S2_API_KEY="your_key_here"
```

### LLM API Keys (Optional — pick any one)

<details>
<summary><b>20+ supported providers</b></summary>

#### US Providers

| Provider | Env Variable | Default Model |
|----------|-------------|---------------|
| OpenAI | `OPENAI_API_KEY` | `gpt-4o-mini` |
| Anthropic | `ANTHROPIC_API_KEY` | `claude-sonnet-4-20250514` |
| Google Gemini | `GEMINI_API_KEY` | `gemini-2.0-flash` |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek-chat` |
| Groq | `GROQ_API_KEY` | `llama-3.1-8b-instant` |
| Together AI | `TOGETHER_API_KEY` | `Llama-3.1-8B-Instruct-Turbo` |
| Fireworks AI | `FIREWORKS_API_KEY` | `llama-v3p1-8b-instruct` |
| Mistral | `MISTRAL_API_KEY` | `mistral-small-latest` |
| xAI (Grok) | `XAI_API_KEY` | `grok-3-mini-fast` |
| Perplexity | `PERPLEXITY_API_KEY` | `sonar` |
| OpenRouter | `OPENROUTER_API_KEY` | `llama-3.1-8b-instruct:free` |

#### Chinese Providers

| Provider | Env Variable | Default Model |
|----------|-------------|---------------|
| Zhipu | `ZHIPUAI_API_KEY` | `glm-4-flash` |
| Moonshot | `MOONSHOT_API_KEY` | `moonshot-v1-8k` |
| Baichuan | `BAICHUAN_API_KEY` | `Baichuan2-Turbo` |
| Yi | `YI_API_KEY` | `yi-lightning` |
| Qwen | `DASHSCOPE_API_KEY` | `qwen-turbo` |
| Doubao | `ARK_API_KEY` | `doubao-lite-32k` |
| MiniMax | `MINIMAX_API_KEY` | `MiniMax-Text-01` |
| Stepfun | `STEPFUN_API_KEY` | `step-1-flash` |
| SenseTime | `SENSENOVA_API_KEY` | `SenseChat-Turbo` |

#### Custom / Self-hosted

```bash
export LLM_API_KEY="your_key"
export LLM_BASE_URL="http://localhost:11434/v1"  # e.g. Ollama
export LLM_MODEL="llama3"
```

</details>

---

## Graph JSON Format

```jsonc
{
  "nodes": [
    {
      "id": "ARXIV:1706.03762",
      "title": "Attention is All you Need",
      "authors": ["Ashish Vaswani", "Noam Shazeer"],
      "year": 2017,
      "citation_count": 169932,
      "is_seed": true,
      "source": "semantic_scholar"
    }
  ],
  "edges": [
    { "source": "paper_A_id", "target": "paper_B_id", "type": "cites" }
  ],
  "seed_papers": ["ARXIV:1706.03762"],
  "total_papers": 90
}
```

**Edge convention**: `A -> B` means **A cites B**.

---

## GROBID Setup (Optional)

[GROBID](https://github.com/kermitt2/grobid) provides structured PDF extraction with **70-90% resolve rate** (vs 40-60% with regex).

```bash
# Quick start
docker run -d --name grobid -p 8070:8070 lfoppiano/grobid:0.8.1
curl -s http://localhost:8070/api/isalive  # verify

# Use with any PDF command
python openpapergraph_cli.py pdf paper.pdf --use-grobid
```

<details>
<summary>Docker Compose (persistent)</summary>

```yaml
services:
  grobid:
    image: lfoppiano/grobid:0.8.1
    ports:
      - "8070:8070"
    restart: unless-stopped
```

</details>

---

## Python API

```python
import sys; sys.path.insert(0, "/path/to/skill-version")

from services.semantic_scholar import search
total, papers = search("transformer attention", limit=10)

from services.graph_builder import build_graph
graph = build_graph(paper_ids=["ARXIV:1706.03762"], depth=1)

from services.analysis import analyze, summarize
result = analyze(graph.nodes)
```

<details>
<summary><b>Available modules</b></summary>

| Module | Key Functions |
|--------|--------------|
| `services.semantic_scholar` | `search()`, `get_paper()`, `get_references()`, `get_citations()`, `recommend()` |
| `services.arxiv` | `search()` |
| `services.dblp` | `search()` |
| `services.google_scholar` | `search()`, `get_citations()`, `get_citation_count()` |
| `services.graph_builder` | `build_graph()`, `build_graph_from_pdfs()` |
| `services.graph_manager` | `expand_as_seed()`, `add_non_seed()`, `convert_to_seed()` |
| `services.graph_server` | `start_server()` |
| `services.pdf_parser` | `parse_pdf()` |
| `services.reference_resolver` | `resolve_references()` |
| `services.analysis` | `analyze()`, `summarize()` |
| `services.llm_client` | `llm_chat()`, `is_llm_available()`, `list_providers()` |
| `services.export` | `to_bibtex()`, `to_csv()`, `to_markdown()`, `to_json()` |
| `services.html_export` | `export_html()` |
| `services.paper_downloader` | `download_pdf()` |
| `services.zotero` | `get_collections()`, `import_papers()` |

</details>

---

## Troubleshooting

<details>
<summary><b>Common issues</b></summary>

**Q: HTTP 429 from Semantic Scholar**
Set `S2_API_KEY` (free at [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api)).

**Q: Google Scholar returns no results**
GS may rate-limit automated access. Falls back to S2 automatically. Wait a few minutes or use `--source s2`.

**Q: `summary` returns extractive instead of LLM-generated**
No LLM key detected. Set any provider key. Run `llm-providers --pretty` to check.

**Q: Low PDF reference resolve rate**
Try `--use-grobid` (70-90% vs 40-60% with regex). See [GROBID Setup](#grobid-setup-optional).

**Q: `graph` command is slow**
Expected. Building involves PDF download, reference parsing, Google Scholar queries (2s rate limit), and multi-API resolution. A single seed with ~50 refs takes 2-5 minutes.

**Q: `serve` shows empty graph**
Build a graph first with `graph` or `graph-from-pdf`.

**Q: Where are PDFs cached?**
`$TMPDIR/opg_pdf_cache/` (usually `/tmp/opg_pdf_cache/`). Delete to clear.

</details>

---

## File Structure

```
skill-version/
├── README.md                     # This file
├── README_CN.md                  # Chinese version
├── SKILL.md                      # Claude Code / OpenClaw skill definition
├── install.sh                    # One-line installer
├── openpapergraph_cli.py         # CLI entry point (16 commands)
├── schemas.py                    # Data models (Paper, GraphData)
├── requirements.txt              # httpx + pymupdf + scholarly
└── services/
    ├── semantic_scholar.py       # S2 API + multi-source search
    ├── arxiv.py                  # arXiv search
    ├── dblp.py                   # DBLP search + venue filtering
    ├── google_scholar.py         # Google Scholar citations
    ├── paper_downloader.py       # PDF download (arXiv/Unpaywall/URL)
    ├── graph_builder.py          # Citation network construction
    ├── graph_manager.py          # Graph mutations (add/convert/remove)
    ├── graph_server.py           # Interactive HTTP server
    ├── pdf_parser.py             # PDF reference extraction
    ├── reference_resolver.py     # Multi-source reference resolution
    ├── bibtex_parser.py          # BibTeX & Zotero parser
    ├── zotero.py                 # Zotero library import
    ├── export.py                 # BibTeX/CSV/Markdown/JSON export
    ├── html_export.py            # Interactive HTML visualization
    ├── analysis.py               # Topic analysis + summarization
    └── llm_client.py             # 20+ provider LLM client
```

---

## Data Sources

| Source | Coverage | Used For |
|--------|----------|----------|
| **arXiv** | Preprints (CS, physics, math, bio) | Search, PDF download, resolution |
| **DBLP** | CS conferences & journals | Search, conference filtering |
| **Google Scholar** | All disciplines | Citations, citation counts |
| **Semantic Scholar** | 200M+ papers | Search fallback, recommendations |
| **CrossRef** | DOI-registered publications | Reference resolution |
| **OpenAlex** | 250M+ works | Reference resolution |
| **Unpaywall** | Open-access PDFs | PDF download |
| **Zotero** | User's library | Import collections |

---

## Contact

For questions, suggestions, or collaboration: **notyour_mason@outlook.com**

---

## License

OpenPaperGraph is licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE).
