# PubMed E-utilities API Quick Reference

## esummary — Article Metadata

```bash
# Single PMID
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=31018962&retmode=json"

# Batch (comma-separated)
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=31018962,22213727&retmode=json"
```

Response fields: `title`, `authors[].name`, `source` (journal), `pubdate`, `volume`, `pages`, `elocationid` (DOI).

Invalid PMID → `{"result": {"pmid": {"error": "invalid_id"}}}`.

## esearch — Find Articles by Query

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Gattorno+classification+autoinflammatory&retmode=json&retmax=5"
```

Returns `esearchresult.idlist` → array of PMIDs.

## Rate Limits

- Without API key: 3 requests/second
- With API key (`&api_key=YOUR_KEY`): 10 requests/second
- API key obtained from NCBI Settings page
