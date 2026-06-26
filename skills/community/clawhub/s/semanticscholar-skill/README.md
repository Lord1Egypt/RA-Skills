# semanticscholar-skill — Semantic Scholar from the Command Line 📚

[中文文档](README_CN.md) | [Semantic Scholar API Docs](https://api.semanticscholar.org/api-docs/) | [Request API Key](https://www.semanticscholar.org/product/api#api-key)

## What it does

- **Search** the Semantic Scholar corpus by keyword, boolean expression, full-text snippet, title, or author
- **Look up** a paper from any supported ID (DOI, arXiv, PMID, PMCID, CorpusId, MAG, ACL, SHA, URL)
- **Traverse citations** forward and backward with pagination
- **Recommend** similar papers from one seed (`find_similar`) or multi-seed positive/negative sets (`recommend`)
- **Find authors** by name, list their publications, pull h-index / affiliations
- **Batch lookup** up to 500 papers or 1000 authors in a single call
- **Filter** by year, date range, venue, fields of study, min citations, pub types, open access
- **Export** to BibTeX, Markdown, or JSON
- **Rate limiting + retries built in** — 1.1s gap between requests, exponential backoff on 429/504
- **Single-script execution pattern** — avoids sequential API ping-pong; all calls batched into one Python script
- Triggers automatically whenever the user mentions papers, citations, academic search, literature discovery

## Multi-Platform Support

Works with all major AI coding agents that support the [Agent Skills](https://agentskills.io) format:

| Platform | Status | Details |
|----------|--------|---------|
| **Claude Code** | ✅ Full support | Native SKILL.md format |
| **Codex** | ✅ Full support | Native SKILL.md + `agents/openai.yaml` UI metadata |
| **Hermes** | ✅ Full support | `metadata.hermes` tags / category / related_skills |
| **OpenClaw** | ✅ Full support | `metadata.openclaw` namespace |
| **ClawHub** | ✅ Published | `clawhub install semanticscholar-skill` |
| **SkillsMP** | ✅ Indexed | GitHub topics configured |

## Why Semantic Scholar?

Semantic Scholar is **not another preprint server** — it is an academic **graph + semantic index** over the corpus that already includes arXiv and bioRxiv. The question is never "S2 *or* arXiv" but "S2 *on top of* arXiv".

| Dimension | arXiv | bioRxiv | **Semantic Scholar** |
|---|---|---|---|
| What it is | Preprint host (physics / CS / math / stats) | Preprint host (biology / medicine) | Aggregated academic graph over 200M+ papers |
| Corpus scope | ~2.5M arXiv papers only | ~350k bioRxiv/medRxiv papers only | arXiv + bioRxiv + PubMed + conference proceedings + journals + more |
| Search | Keyword / classification code | Keyword / subject area | Keyword + **semantic relevance ranking** + boolean + full-text snippets |
| Citation graph | ❌ not provided | ❌ not provided | ✅ forward + backward citations, influential citation count |
| "Papers like this" | ❌ | ❌ | ✅ `find_similar` + multi-seed `recommend` |
| Author disambiguation | partial (no unified IDs) | partial | ✅ unified `authorId`, affiliations, h-index |
| Venue / year / citation filters | limited | limited | ✅ rich filters: venue, fields of study, min citations, open access, pub types |
| TLDR summaries | ❌ | ❌ | ✅ `tldr` field on most papers |
| BibTeX export | via arxiv.org page | via bioRxiv page | ✅ API `citationStyles` field |

**Practical rule of thumb:**
- Need a specific arXiv or bioRxiv paper by ID → hit the source directly
- Need to **discover** what's relevant / influential / cited / similar → use Semantic Scholar
- Need **both preprints and published literature** in one ranked search → use Semantic Scholar
- Doing literature review, related-work sections, citation analysis → use Semantic Scholar

This skill does not replace arXiv or bioRxiv; it sits above them and adds the graph / ranking / recommendation layer they lack.

## Comparison

### vs. `asta-skill` (our MCP-based sibling)

| Capability | `semanticscholar-skill` | `asta-skill` |
|---|---|---|
| Transport | Python + direct REST (`s2.py`) | MCP (streamable HTTP) |
| Host requirement | Python + `S2_API_KEY` | Host with MCP support |
| Best for | Scripted batch workflows, custom filters | Zero-code agent integration |
| Boolean query builder | ✅ `build_bool_query()` | ❌ |
| Multi-seed recommendations | ✅ `recommend(pos, neg)` | ❌ |
| BibTeX / Markdown / JSON export | ✅ built-in | ❌ |
| Works in Cursor / Windsurf out of the box | ❌ | ✅ |

### vs. no skill (native agent)

| Feature | Native agent | This skill |
|---|---|---|
| Knows S2 API base URL & auth header | Maybe | ✅ |
| Boolean query construction helper | ❌ | ✅ `build_bool_query()` |
| Single-script execution pattern (no ping-pong) | ❌ | ✅ enforced |
| Automatic rate limiting + exponential backoff | ❌ | ✅ |
| BibTeX / Markdown / JSON export | ❌ | ✅ |
| Deduplication helper | ❌ | ✅ `deduplicate()` |
| Phase-based workflow (Plan → Execute → Summarize → Loop) | ❌ | ✅ |

## Prerequisites

- `python3`
- `pip install requests`
- (Optional) A [Semantic Scholar API Key](https://www.semanticscholar.org/product/api#api-key) for higher rate limits:

  ```bash
  export S2_API_KEY=xxxxxxxxxxxxxxxx
  ```

Works unauthenticated with strict rate limits.

## Skill Installation

### Claude Code

```bash
# Global install (all projects)
git clone https://github.com/Agents365-ai/semanticscholar-skill.git ~/.claude/skills/semanticscholar-skill

# Project-level
git clone https://github.com/Agents365-ai/semanticscholar-skill.git .claude/skills/semanticscholar-skill
```

### Codex

```bash
git clone https://github.com/Agents365-ai/semanticscholar-skill.git ~/.codex/skills/semanticscholar-skill
```

### OpenClaw

```bash
git clone https://github.com/Agents365-ai/semanticscholar-skill.git ~/.openclaw/skills/semanticscholar-skill

# Project-level
git clone https://github.com/Agents365-ai/semanticscholar-skill.git skills/semanticscholar-skill
```

### ClawHub

```bash
clawhub install semanticscholar-skill
```

### SkillsMP

```bash
skills install semanticscholar-skill
```

### Installation paths summary

| Platform | Global path | Project path |
|----------|-------------|--------------|
| Claude Code | `~/.claude/skills/semanticscholar-skill/` | `.claude/skills/semanticscholar-skill/` |
| Codex | `~/.codex/skills/semanticscholar-skill/` | N/A |
| OpenClaw | `~/.openclaw/skills/semanticscholar-skill/` | `skills/semanticscholar-skill/` |
| ClawHub | via `clawhub install` | — |
| SkillsMP | via `skills install` | — |

## Usage

Just describe what you want:

```
> Use semanticscholar-skill to search for recent mixture-of-experts papers at NeurIPS since 2023

> Find papers citing "Attention Is All You Need" and rank by citation count

> Use build_bool_query to find "stem-like T cells" in IBD, excluding mesenchymal

> Recommend papers similar to DOI:10.1038/nature14539 and ARXIV:2010.11929, excluding NLP

> Export the top 10 results to BibTeX
```

The skill picks the right search function, applies filters, and runs everything in a single Python script with automatic rate limiting.

## Helper Module

`s2.py` — single-file module imported via `from s2 import *`:

| Category | Functions |
|---|---|
| Paper search | `search_relevance`, `search_bulk`, `search_snippets`, `match_title`, `get_paper`, `get_citations`, `get_references`, `find_similar`, `recommend`, `batch_papers` |
| Author search | `search_authors`, `get_author`, `get_author_papers`, `get_paper_authors`, `batch_authors` |
| Query building | `build_bool_query(phrases, required, excluded, or_terms)` |
| Output | `format_table`, `format_details`, `format_results`, `format_authors`, `export_bibtex`, `export_markdown`, `export_json`, `deduplicate` |

Full API reference in `SKILL.md`.

## Files

- `SKILL.md` — **the only required file**. Loaded by all platforms as the skill instructions.
- `s2.py` — Python helper module (rate limiting, retries, query building, output formatting)
- `agents/openai.yaml` — Codex UI metadata for skill discovery and prompt chips
- `README.md` — this file (English, displayed on GitHub homepage)
- `README_CN.md` — Chinese documentation

## Known Limitations

- **Semantic Scholar free tier is rate-limited** — unauthenticated is ~1 req/sec shared across all users; API key raises your personal ceiling but is not unlimited
- **Bulk search never returns TLDR** — fall back to `abstract` field
- **Not every paper has an abstract** — some only expose title + TLDR
- **Author disambiguation** — common names collide; inspect affiliations before calling `get_author_papers`
- **Fields with large payloads** — avoid `citations` / `references` in `get_paper` fields for highly-cited papers; use `get_citations` (paginated) instead

## License

MIT

## Support

If this skill helps you, consider supporting the author:

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/wechat-pay.png" width="180" alt="WeChat Pay">
      <br>
      <b>WeChat Pay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/alipay.png" width="180" alt="Alipay">
      <br>
      <b>Alipay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/buymeacoffee.png" width="180" alt="Buy Me a Coffee">
      <br>
      <b>Buy Me a Coffee</b>
    </td>
  </tr>
</table>

## Author

**Agents365-ai**

- Bilibili: https://space.bilibili.com/441831884
- GitHub: https://github.com/Agents365-ai
