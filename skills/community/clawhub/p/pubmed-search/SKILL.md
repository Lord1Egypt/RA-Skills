---
name: pubmed-search
description: Search PubMed (30M+ articles) for abstracts, with auto full-text
  retrieval for PMC OA articles. Covers both open-access and non-open-access
  literature. No API key required.
version: 1.0.0
agent_created: true
metadata:
  emoji: 🔬
  requires:
    bins:
      - node
disable: false
---

# PubMed Search

Search the full PubMed database (30M+ articles) — abstracts for all records, full text for PMC open-access articles.

**What PMC Harvest misses**: PubMed indexes ~30M biomedical articles; only ~4M (13%) are in PMC with full text. This skill retrieves abstracts for the remaining 26M non-OA articles, making it suitable for comprehensive literature review.

## Core Workflow

```
Search PubMed (db=pubmed) → get PMIDs
    → esummary: metadata for all (title, authors, journal, PMID, DOI)
    → efetch: structured abstract XML for any PMID
    → idconv: check if PMID maps to PMCID
        → if PMCID exists → OAI-PMH full text (PMC open access)
        → if no PMCID → abstract only (non-OA)
```

## Features

- **PubMed-wide search** — `db=pubmed`, covers all 30M+ indexed articles
- **Abstract for every article** — `efetch` with `rettype=abstract&retmode=xml`
- **Auto full-text fallback** — if PMID maps to PMCID, retrieves full text via OAI-PMH
- **Batch processing** — search journals, keywords, MeSH terms
- **No API key required** — public NCBI E-utilities (3 req/s rate limit)

## Usage

```bash
# Search PubMed by keyword
node {baseDir}/scripts/pubmed-search.js search --query "myasthenia gravis thymus" --max 20

# Search with year filter
node {baseDir}/scripts/pubmed-search.js search --query "IFN alpha thymic epithelial" --year 2023 --max 30

# Search by journal
node {baseDir}/scripts/pubmed-search.js search --query "\"J Neuroimmunol\"[journal] AND MG" --max 20

# Get abstract for specific PMID
node {baseDir}/scripts/pubmed-search.js abstract --pmid 30311866

# Get abstract + try full text
node {baseDir}/scripts/pubmed-search.js fetch --pmid 30311866

# Test with sample query
node {baseDir}/scripts/pubmed-search.js test
```

## Options

| Flag | Description |
|------|-------------|
| `search` | Search PubMed for articles |
| `--query <text>` | PubMed search query (supports full PubMed syntax) |
| `--year <year>` | Filter by publication year |
| `--max <n>` | Max results (default: 50) |
| `--offset <n>` | Pagination offset (default: 0) |
| `abstract` | Get structured abstract for a PMID |
| `--pmid <id>` | PubMed ID (PMID) |
| `fetch` | Full fetch: abstract + auto full-text if OA |
| `test` | Run test with sample query |

## Programmatic API

```javascript
const pubmed = require('{baseDir}/lib/api.js');

// Search PubMed
const { count, pmids } = await pubmed.searchPubMed('myasthenia gravis', { year: 2025, retmax: 50 });

// Get metadata summaries
const summaries = await pubmed.getSummaries(pmids);

// Get structured abstract
const { title, abstract, authors, journal, doi } = await pubmed.fetchAbstract('30311866');

// Fetch full text (auto maps PMID→PMCID, tries OAI-PMH)
const { available, xml, abstract, reason } = await pubmed.fetchArticle('30311866');

// Check if PMID has PMC full text
const { hasPMC, pmcid } = await pubmed.checkPMC('30311866');

// Batch search multiple journals
const articles = await pubmed.harvestJournals([{ name: 'Neurology', query: '"Neurology"[journal]' }], { year: 2025 });
```

## Journal Query Examples

```javascript
const queries = {
  'Neurology': '"Neurology"[journal]',
  'J Neuroimmunol': '"J Neuroimmunol"[journal]',
  'Muscle Nerve': '"Muscle Nerve"[journal]',
  'J Neurol Sci': '"J Neurol Sci"[journal]',
  'Autoimmun Rev': '"Autoimmun Rev"[journal]',
  'Front Immunol': '"Front Immunol"[journal]',
  'Nat Rev Neurol': '"Nat Rev Neurol"[journal]',
};
```

## PubMed Search Syntax

Full PubMed query syntax is supported:
- `"keyword phrase"[tiab]` — title/abstract search
- `"journal name"[journal]` — journal filter
- `YYYY[dp]` or `YYYY[pdat]` — date filter (dp returns exact matches, pdat returns that year forward)
- `AND`, `OR`, `NOT` — boolean operators
- `gene[mesh]` — MeSH term
- `smith j[author]` — author filter
- `english[lang]` — language filter
- `review[ptyp]` — publication type

## Limitations

- **Non-OA articles**: abstract + metadata only, no full text
- **Rate limit**: ~3 requests/second without API key (built-in 400ms delay between requests)
- **Peak hours**: NCBI recommends avoiding 5AM-9PM ET for large batches
- **Abstract quality**: structured abstracts from PubMed XML; older pre-1975 articles may have limited metadata

## API Reference

- **E-utilities**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils`
  - `esearch.fcgi?db=pubmed` — Search PubMed (30M+ records)
  - `esummary.fcgi?db=pubmed` — Article metadata (JSON)
  - `efetch.fcgi?db=pubmed&rettype=abstract&retmode=xml` — Structured abstract
- **ID Converter**: `https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/` — PMID ↔ PMCID mapping
- **OAI-PMH**: `https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh/GetRecord` — Full text XML (OA only)

Full docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/
