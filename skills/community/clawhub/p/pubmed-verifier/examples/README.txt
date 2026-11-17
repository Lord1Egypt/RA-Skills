refs_list.sample.txt — sample input for --parse-text (numbered list,
inline PMID/DOI/arXiv routing, one title-only entry, one broken line)

claims.sample.csv — reference format for --claims-file

- pmid column: PubMed pipeline (full five-state verification)
- rows with only arxiv_id (+title): arXiv pipeline (official API check)
- doi column: DOI-splice cross-check against the PubMed-registered DOI
  (PMID rows) / version-of-record pairing check (arXiv rows, v3.3.0) /
  full five-state verdicts (doi-only rows, v3.4.0)
- title: required for verdicts beyond existence-check
- expected verdicts (as of v3.4.0): the 31018962 row carries a
  deliberately inexact title → partial (title mismatch, everything else
  matches — demonstrates the partial rung, not a data error); the
  1706.03762 row → correct; the doi-only 10.1371 row → correct (its
  second author "Other" is a synthetic placeholder; v3.8.0's
  mis-attribution cap means a wrong author set would drop it to partial); the 24476887 row
  (STAP cells) is RETRACTED on purpose → RETRACTED flag with a partial
  cap — it demonstrates retraction detection, not a data error

Run:  python3 scripts/verify_pmids.py --claims-file examples/claims.sample.csv

Lint first (offline, v3.5.0): python3 scripts/verify_pmids.py --lint-claims examples/claims.sample.csv

Bibliography (v3.6.0): refs.sample.bib audits a .bib file directly —
python3 scripts/verify_pmids.py --bibliography examples/refs.sample.bib
Since v6.3.0 the same samples also ship as refs.sample.bib.txt /
refs.sample.ris.txt (extension-neutral copies the --bibliography format
sniffer reads directly), so the command above runs on every distribution
channel — try it with the .txt copy if your package has no .bib file:
python3 scripts/verify_pmids.py --bibliography examples/refs.sample.bib.txt

RIS (v3.7.0): refs.sample.ris audits Zotero/EndNote/Mendeley exports —
python3 scripts/verify_pmids.py --bibliography examples/refs.sample.ris
(the refs.sample.ris.txt copy works identically)

Claims JSON (v5.8.0): claims.sample.json shows the three row types in
JSON form — a PMID row with full claimed metadata, a DOI-only row, and
an arXiv row (v3.1.0):
python3 scripts/verify_pmids.py --claims-file examples/claims.sample.json
Lint it offline first: --lint-claims examples/claims.sample.json

Plain-text list (v5.8.0): refs.sample.txt shows the three routing shapes
in one list — an inline-PMID entry, an inline-DOI entry and a title-only
entry (resolves via PubMed title search, honestly labeled):
python3 scripts/verify_pmids.py --parse-text examples/refs.sample.txt
