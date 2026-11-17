> **何时读我**：需要完整 API 调用示例与返回字段说明时。
> **最短路径**：SKILL.md 的「What the output looks like」先看输出形态，再来这里对字段。
> **回 INDEX**：[INDEX.md](INDEX.md)

# PubMed E-utilities API Quick Reference

## esummary — Article Metadata

```bash
# Single PMID
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=31018962&retmode=json"

# Batch (comma-separated)
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=31018962,22213727&retmode=json"
```

Response fields: `title`, `authors[].name`, `source` (journal), `pubdate`, `volume`, `pages`, `elocationid` (DOI).

Invalid PMID → `{"result": {"pmid": {"error": "cannot get document summary"}}}` (the exact string has varied over time — the verifier only checks for the presence of an `error` key).

## esearch — Find Articles by Query

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Gattorno+classification+autoinflammatory&retmode=json&retmax=5"
```

Returns `esearchresult.idlist` → array of PMIDs.

## efetch — Full Abstracts

```bash
# efetch supports TEXT and XML only — retmode=json is NOT valid for efetch
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=37635643&rettype=abstract&retmode=text"
```

## Deep Research Workflow (Systematic PubMed Search)

When the user needs comprehensive medical literature research beyond simple PMID verification:

### Step 1: esearch → keyword search → get PMIDs
```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<keywords>&retmax=10&sort=relevance" | grep -oP '<Id>\K\d+'
```

### Step 2: esummary → metadata summaries (fast, compact)
```bash
PMIDS="pmid1,pmid2,pmid3"
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=$PMIDS&retmode=json" > /tmp/pubmed-results.json
python3 -c "
import json
data = json.load(open('/tmp/pubmed-results.json'))
for uid, art in data.get('result', {}).items():
    if uid == 'uids': continue
    authors = ', '.join([a.get('name','') for a in art.get('authors',[])[:6]])
    print(f'PMID {uid}: {art.get(\"title\",\"\")}')
    print(f'  {art.get(\"fulljournalname\",\"\")} {art.get(\"pubdate\",\"\")};{art.get(\"volume\",\"\")}:{art.get(\"pages\",\"\")}')
    print(f'  DOI: {art.get(\"elocationid\",\"\")}')
    print()
"
```

### Step 3: efetch → full abstracts for key papers
```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=$PMIDS&rettype=abstract&retmode=text"
```

### Pitfalls
- **efetch has no JSON mode** — use `retmode=text` (or XML) only
- **esearch may return unrelated results** — always cross-check with esummary titles
- **Rate limit**: 3 req/s without API key. Add `sleep 0.5` between batches
- **Large author lists**: esummary `authors` array can be 50+ — truncate to first 6 for display

## Rate Limits

- Without API key: 3 requests/second
- With API key (`&api_key=YOUR_KEY`): 10 requests/second
- API key obtained from NCBI Settings page
- Etiquette params: `&tool=pubmed-verifier&email=you@lab.org` (added automatically with `--mailto`)

## Europe PMC (fallback source, v2.2.0)

Free, no key, mirrors PubMed; used automatically when NCBI batches fail
(`--meta-source auto`) or forced with `--meta-source europepmc`.

```bash
# Batch lookup by PMID (EXT_ID), SRC:MED restricts to PubMed records
curl -s "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=(EXT_ID:31018962%20OR%20EXT_ID:22213727)%20AND%20SRC:MED&format=json&resultType=lite&pageSize=25"
```

Useful fields: `id` (PMID), `title`, `authorString` (comma-separated),
`journalTitle`, `pubYear`, `doi`, `journalVolume`, `pageInfo`.

## Crossref DOI check (polite pool, v2.2.0)

```bash
# ?mailto= joins the polite pool — more generous rate limits
curl -s "https://api.crossref.org/works/10.1038/nature12968?mailto=you@lab.org"
```

- 429 responses carry `Retry-After` — back off accordingly (v2.2.0 clamps 1–5 s)
- 403/406 usually mean rate limiting — back off and retry later (the tool rotates client identifiers, including a standard browser UA on retry, per the SKILL.md network-hardening table)
- A correct DOI with WRONG paper metadata = spliced/fake citation signature

## arXiv API (export.arxiv.org)

```bash
# one ID per lookup, Atom feed back; arxiv:doi = the version-of-record
# DOI the authors registered — the preprint↔published cross-check uses it
curl -s "https://export.arxiv.org/api/query?id_list=2005.13892&max_results=1"
```

- No `<entry>` in the feed = the ID does not exist (fabrication signal);
  a 200 response that is not an Atom feed (portal/maintenance page) is
  treated as "could not verify", never as "not found"
- Official etiquette: ≥3 s between calls — large batches are paced
  deliberately (progress with ETA goes to stderr)
- `arxiv:journal_ref` / `arxiv:doi` are author-registered fields, shown
  in the audit trail; see SKILL.md v3.3.0 section for the pairing check
