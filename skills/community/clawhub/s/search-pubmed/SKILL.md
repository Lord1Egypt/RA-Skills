---
name: search-pubmed
description: >
  Search biomedical literature on PubMed via NCBI E-Utilities.
  Use this skill whenever the user needs to search for scientific papers,
  biomedical articles, life science research, or any PubMed-indexed content.
  Triggers: 'search literature', 'find papers', 'PubMed', 'NCBI', 'PMID',
  'biomedical', 'scientific articles', 'life science', 'organism research',
  'gene/disease/drug papers'. Also use for any mention of searching literature
  about bacteria, plants, animals, diseases, genes, proteins, drugs, or
  clinical/biological topics — even if the user doesn't explicitly say 'PubMed'.
---

# PubMed Literature Search

Search PubMed (and other NCBI databases) via the E-Utilities API, using a bundled
Python script that wraps Biopython's `Bio.Entrez`.

## Quick start

```bash
python scripts/search_pubmed.py "<query>" [--max N] [--db DB] [--pmid ID] [--full]
```

The script lives at `scripts/search_pubmed.py` relative to this skill directory.
Run it from the workspace root, using the skill's install path to locate the script.

If the skill is installed at `.claude/skills/search-pubmed/`, invoke it as:
```bash
python .claude/skills/search-pubmed/scripts/search_pubmed.py "cancer AND immunotherapy"
```

## Common patterns

### Keyword search (default)
```bash
python .claude/skills/search-pubmed/scripts/search_pubmed.py "Sinorhizobium fredii biofilm"
```

### Control result count
```bash
python .claude/skills/search-pubmed/scripts/search_pubmed.py "CRISPR" --max 20
```

### Boolean logic (AND / OR / NOT)
```bash
python .claude/skills/search-pubmed/scripts/search_pubmed.py "hopanoid AND rhizobium"
python .claude/skills/search-pubmed/scripts/search_pubmed.py "mouse OR rat"
```

### Field-qualified search
```bash
python .claude/skills/search-pubmed/scripts/search_pubmed.py "hopanoid[Title/Abstract]"
python .claude/skills/search-pubmed/scripts/search_pubmed.py "Smith J[Author] AND 2024[Date - Publication]"
```

### PMID lookup
```bash
# Fast — title / author / journal / DOI only (1 request)
python .claude/skills/search-pubmed/scripts/search_pubmed.py --pmid 41185614

# With abstract (2 requests)
python .claude/skills/search-pubmed/scripts/search_pubmed.py --pmid 41185614 --full

# Multiple PMIDs
python .claude/skills/search-pubmed/scripts/search_pubmed.py --pmid 41185614,42332334 --full
```

### Other NCBI databases
```bash
python .claude/skills/search-pubmed/scripts/search_pubmed.py "TP53" --db nucleotide
python .claude/skills/search-pubmed/scripts/search_pubmed.py "cancer" --db pmc
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `query` | Search keywords (Entrez syntax supported) | Required (or use `--pmid`) |
| `--max N` | Maximum results to return | `10` |
| `--db NAME` | Target NCBI database | `pubmed` |
| `--email ADDR` | NCBI contact email (optional, avoids warning) | — |
| `--api-key KEY` | NCBI API Key (optional, raises rate limit) | — |
| `--pmid ID` | Lookup by PMID directly, skip search | — |
| `--full` | Include abstract text (with `--pmid`) | off |

## Output format

Each result includes:
- **PMID** — PubMed ID (clickable link: `https://pubmed.ncbi.nlm.nih.gov/PMID`)
- **Title** — article title
- **Author** — first author | last author
- **Source** — journal abbreviation
- **Date** — publication date
- **DOI** — digital object identifier (when available)

## Rate limits

| Condition | Limit |
|-----------|-------|
| No API key | 3 requests/sec |
| With API key (`--api-key`) | 10 requests/sec |

A typical search uses 2 requests (search + summaries). PMID lookup uses 1 (or 2 with `--full`).
Staying within the rate limit is generally not a concern for interactive use.

## Search tips

1. **Start broad, then narrow.** Use `AND` to add terms, not to restrict fields.
2. **Try synonyms and alternative classifications.** Example: *Sinorhizobium fredii*
   is also classified as *Ensifer fredii* — search both with `"Sinorhizobium fredii" OR "Ensifer fredii"`.
3. **Zero results is information.** A null result may indicate a genuine research gap
   — tell the user this explicitly.
4. **Use `[Title/Abstract]` qualifier** for precision when a broad search returns
   too many off-topic hits.
5. **When cross-searching two topics** (e.g., organism X + pathway Y), if the
   AND query returns 0, run them separately to show the user the landscape —
   how many papers exist on each side of the gap.
6. **A PubMed gap doesn't mean a total gap.** When you identify a research gap in
   PubMed, suggest the user cross-check gene/protein databases (NCBI Gene, UniProt,
   KEGG) for genomic evidence — genes may be annotated but unstudied in the literature.

## Dependencies

- Python 3.6+
- `biopython` package: `pip install biopython`

## Bundled resources

- `scripts/search_pubmed.py` — the search executable
- `references/entrez-help.md` — NCBI Entrez query syntax reference
