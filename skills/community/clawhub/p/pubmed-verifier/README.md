# PubMed Citation Verifier 🔬

Batch-verify PMID citations against PubMed API. Built for researchers, medical writers, and evidence-based medicine teams.

## Why?

Academic projects routinely contain hundreds of PMID citations. Manual verification is tedious and error-prone. During our own 225-reference audit, we found 3 invalid PMIDs and 6 cross-domain mismatches — errors that would have undermined the entire project.

## Features

- **Batch verification** — Scan entire project directories, extract all PMIDs, verify against PubMed in one run
- **Existence check** — Confirm every PMID resolves to a real article
- **Metadata validation** — Title, authors, journal, date, DOI all retrieved
- **Content matching** — Keyword overlap scoring flags potentially irrelevant citations
- **Smart cross-domain detection** — Flags low-match items for human review without auto-deleting valid cross-references (e.g., HLH guidelines cited in disease-specific MAS cases)
- **Replacement search** — Find correct PMIDs for broken citations via PubMed search
- **Multiple output formats** — HTML report, JSON, or terminal summary

## Quick Start

```bash
# Install
openclaw skills install docsor1212/pubmed-verifier

# Verify all PMIDs in a project
python3 scripts/verify_pmids.py --source /path/to/project --output report.html

# Verify specific PMIDs
python3 scripts/verify_pmids.py --pmids 31018962,22213727,999999999

# With content matching
python3 scripts/verify_pmids.py --source ./papers --match-keywords --threshold 0.2
```

## Use Cases

| Scenario | Example |
|----------|---------|
| **Systematic review QA** | Verify all 200+ references before submission |
| **Medical website audit** | Check evidence citations across clinical case library |
| **Paper manuscript check** | Validate every PMID in your draft |
| **Teaching material review** | Ensure lecture citations are accurate |
| **Evidence library maintenance** | Periodic batch verification of reference databases |

## Real-World Results

Audited a 35-file pediatric rheumatology evidence library (225 PMID citations):
- **222** citations: valid and content-matched ✅
- **3** citations: invalid PMIDs found and corrected
- **6** cross-domain citations: correctly flagged, reviewed, confirmed appropriate
- Total time: ~5 minutes for full audit

## Technical Details

- **API**: PubMed E-utilities (esummary, esearch) — no API key required
- **Rate limit**: 3 req/s (free), 0.4s batch delay built-in
- **Batch size**: 50 PMIDs per request
- **File types**: `.html`, `.md`, `.txt`, `.json`, `.htm`
- **PMID patterns**: `PMID: 12345678`, `PubMed: 12345678`, `pubmed.ncbi.nlm.nih.gov/12345678/`

## License

MIT
