---
name: pubmed-verifier
description: PubMed citation verifier / PubMed文献引用验证 — detect AI-fabricated references with fuzzy matching / 模糊匹配检测AI编造文献
  Keywords: PMID验证, PubMed引用核查, 文献审计, AI幻觉检测, 学术写作, 医学文献,
  批量验证, 引用核对, 论文引用检查, reference validation, citation audit,
  PubMed API, systematic review QA, academic integrity, pharmacovigilance.
  Triggers: "验证PMID", "检查引用", "核查文献", "PMID检查", "引用验证",
  "verify PMIDs", "check citations", "validate references", "audit PMID",
  "文献验证", "引用核对", "batch verify references", "检查引用", "验证文献".
---

# PubMed Citation Verifier v2.1

Five-state batch verification of PMID citations via PubMed E-utilities API, with SQLite caching, CSV support, and Crossref DOI verification.

## Verdict Types

| Icon | Verdict | Meaning |
|------|---------|---------|
| ✅ | Correct | PMID exists AND matches claimed paper (title + author/journal) |
| ⚠️ | Mismatch | PMID exists but points to a **different** paper (most common AI hallucination!) |
| 🔶 | Partial | Some metadata matches (e.g., author+journal match but title differs) |
| ❌ | Invalid | PMID not found in PubMed |
| ❓ | Unknown | Insufficient claimed metadata for cross-check |

## Quick Start

```bash
# Verify all PMIDs in a project directory (auto-parses citation context)
python3 scripts/verify_pmids.py --source /path/to/project --output report.html

# Verify specific PMIDs
python3 verify_pmids.py --pmids 31018962,22213727

# Verify with explicit claimed metadata (JSON)
python3 verify_pmids.py --claims '[{"pmid":"34078778","title":"JIA pathogenesis","authors":["Zaripova"],"journal":"Pediatr Rheumatol Online J","year":"2021"}]' --output report.html

# Verify with claims file (JSON or CSV)
python3 verify_pmids.py --claims-file claims.csv --suggest --output report.html

# Verify + DOI cross-check via Crossref
python3 verify_pmids.py --source /path/to/files --verify-doi --output report.html

# Full pipeline with all features
python3 verify_pmids.py --source /path/to/files --verify-doi --suggest --output report.html
```

## What's New in v2.1

| Feature | Description |
|---------|-------------|
| **SQLite Cache** | Verified PMIDs cached locally at `~/.cache/pubmed-verifier/cache.db`. 30-day default expiry. Re-runs on large projects take seconds instead of minutes. |
| **CSV Claims** | `--claims-file` now accepts `.csv` files in addition to JSON. Auto-detects format. Semicolon or pipe-delimited authors supported. |
| **Crossref DOI** | `--verify-doi` cross-references article DOIs via Crossref API for extra confidence. |
| **Retry Logic** | Automatic 3-retry with exponential backoff (1s→2s→4s) on transient API failures. Zero external dependencies. |
| **Dual Fuzzy Matching** | Title matching uses word-level Jaccard overlap (≥50%) + SequenceMatcher (≥90%) as supplementary. |

## How It Works

### 1. Extract PMIDs + Parse Citation Context

Scans files for common PMID patterns (`PMID: 12345678`, PubMed URLs, etc.).

**Automatically parses surrounding citation text** to extract claimed metadata:
- Author surnames (e.g., `Ravelli A, Martini A` → `["Ravelli", "Martini"]`)
- Paper title (between author and journal)
- Journal name (from `<i>...</i>` tags or position)
- Publication year (`20xx` / `19xx`)

Supported file types: `.html`, `.md`, `.txt`, `.json`, `.htm`

### 2. Fetch PubMed Metadata (with Cache)

Each PMID queried via PubMed `esummary` API. Results cached in SQLite for 30 days (configurable via `--cache-days`). Use `--no-cache` to force fresh queries.

Batch requests (50/call, 0.4s delay, 3-retry with exponential backoff).

### 3. Cross-Check: Claimed vs Actual

Dual-strategy fuzzy matching:
- **Primary**: Word-level Jaccard overlap ≥ 50% (handles word reordering, abbreviation expansion)
- **Supplementary**: SequenceMatcher ratio ≥ 90% (catches edge cases)

| Field | Match Logic |
|-------|-------------|
| **Title** | Word overlap ≥ 50% OR SequenceMatcher ≥ 90% |
| **Authors** | ≥1 surname hit for single author claim; ≥2 for multiple |
| **Journal** | Containment match (handles abbreviations) |
| **Year** | Exact match |

**Verdict determination:**
- `title_match AND (author_match OR journal_match)` → ✅ Correct
- `author_match AND journal_match AND NOT title_match` → 🔶 Partial
- Otherwise → ⚠️ Mismatch

### 4. Crossref DOI Verification (Optional, `--verify-doi`)

For articles with DOIs, queries Crossref API to cross-verify title/journal/year as an independent data source.

### 5. Auto-Suggest (Optional, `--suggest`)

For mismatches, searches PubMed using claimed metadata to suggest correct PMIDs (top 3 candidates).

### 6. Topic Relevance (Optional, `--match-keywords`)

⚠️ **Note**: This checks *topic relevance* only (via filename keywords), NOT PMID correctness. Auxiliary screening tool.

### 7. Report Output

| Format | Flag | Use case |
|--------|------|----------|
| HTML | `--output report.html` | Visual review with claimed vs actual comparison, verdict column |
| JSON | `--output report.json` | Programmatic processing |
| Text | default (no --output) | Quick terminal review |

## Using --claims / --claims-file

When you have explicit claimed metadata (e.g., from AI-generated documents):

**JSON array format:**
```json
[
  {
    "pmid": "34078778",
    "title": "Juvenile idiopathic arthritis: from pathogenesis to clinical practice",
    "authors": ["Zaripova LN", "Midgley A", "Beresford MW"],
    "journal": "Pediatr Rheumatol Online J",
    "year": "2021"
  }
]
```

**CSV format** (`claims.csv`):
```csv
pmid,title,authors,journal,year
34078778,JIA pathogenesis,Zaripova LN;Midgley A,Pediatr Rheumatol Online J,2021
31018962,FMF classification criteria,Lidar M|Lancet,,2014
```

## CLI Reference

```
python3 scripts/verify_pmids.py [OPTIONS]

Options:
  --source PATH        File or directory to scan for PMIDs
  --pmids P1,P2,...    Comma-separated PMIDs to verify directly
  --claims JSON        JSON string with claimed metadata
  --claims-file FILE   JSON or CSV file with claimed metadata
  --verify-doi         Also verify DOIs via Crossref
  --suggest            Auto-suggest correct PMIDs for mismatches
  --match-keywords     Check topic relevance (auxiliary)
  --threshold FLOAT    Keyword match threshold (default: 0.2)
  --no-cache           Disable cache, always query API
  --cache-days N       Cache validity in days (default: 30)
  --output FILE        Output file (.json or .html)
  --format FORMAT      Output format: json|html|text (default: text)
```

## Fixing Mismatched/Invalid PMIDs

1. Check the report's "Suggested" column (if using `--suggest`)
2. Use PubMed search to find the correct article:
   ```python
   from scripts.verify_pmids import search_pubmed
   results = search_pubmed('Ravelli[au] AND juvenile idiopathic arthritis AND Lancet[jour]')
   for r in results: print(r["pmid"], r.get("title",""))
   ```
3. Verify the replacement and update the source file

## API Limits

- No API key required (public E-utilities)
- 3 requests/second without API key
- Script enforces 0.4s delay between batches, 3-retry with backoff
- Batch size: 50 PMIDs per request
- Cache reduces repeated API calls significantly

## Performance

| Scenario | First run | Cached run |
|----------|-----------|------------|
| 225 PMIDs (MedWiki-Rheum) | ~7 min | ~5 sec |
| Single PMID | ~2s | ~1.4s |

## Files

| File | Purpose |
|------|---------|
| `scripts/verify_pmids.py` | Main verification script (v2.1, 1058 lines, zero external dependencies) |
| `references/api_examples.md` | PubMed E-utilities API examples |
