# Literature Search — API Reference

## Overview

This skill uses two **free, no-API-key-required** data sources:

| Database | API | Key Required? | Rate Limit |
|---|---|---|---|
| PubMed (NCBI) | E-utilities | ❌ No | 3 req/sec (without key) |
| Semantic Scholar | REST API v1 | ❌ No | 100 req/5min (anonymous) |

Optional paid/registered APIs (used only when user provides key):
- Web of Science Starter API
- Springer Nature Metadata API

---

## 1. PubMed (NCBI E-utilities) — ✅ No Key Required

### Endpoints Used

| Tool | URL | Purpose |
|---|---|---|
| esearch | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` | Get PMID list |
| efetch | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi` | Fetch full metadata XML |

### esearch Parameters

| Param | Description | Example |
|---|---|---|
| `db` | Database | `pubmed` |
| `term` | Search query (supports MeSH) | `cognitive behavioral therapy` |
| `retmax` | Max results | `50` |
| `retstart` | Offset (pagination) | `0` |
| `sort` | Sort order | `relevance` |
| `email` | Your email (courtesy) | `yourname@example.com` |

### efetch Parameters

| Param | Description | Example |
|---|---|---|
| `db` | Database | `pubmed` |
| `id` | PMID(s), comma-separated | `12345678,87654321` |
| `retmode` | Output format | `xml` |

### Response Fields Used (XML)

- `//PubmedArticle/MedlineCitation/PMID` → `pmid`
- `//ArticleTitle` → `title`
- `//Abstract/AbstractText` → `abstract`
- `//Author/LastName` + `ForeName` → `authors`
- `//Journal/Title` → `journal`
- `//PubDate/Year` → `year`
- `//ArticleId[@IdType='doi']` → `doi`
- `//MeshHeading/DescriptorName` → `keywords` (MeSH terms)
- `//PublicationType` → `publication_types`

### Rate Limits

- **Without API key**: 3 requests/second
- **With API key**: 10 requests/second
- Set `EMAIL` env var for NCBI to contact you if issues arise
- Script内置 0.34s 延迟以遵守限速

### NCBI Account (Optional, for Higher Rate Limit)

1. Go to https://www.ncbi.nlm.nih.gov/account/
2. Register for a free account
3. Set `NCBI_API_KEY` env var → rate limit increases to 10 req/sec
4. Add `&api_key=YOUR_KEY` to esearch/efetch URLs

---

## 2. Semantic Scholar — ✅ No Key Required

### Endpoint Used

```
GET https://api.semanticscholar.org/graph/v1/paper/search
```

### Query Parameters

| Param | Description | Example |
|---|---|---|
| `query` | Search query string | `cognitive behavioral therapy` |
| `fields` | Comma-separated fields to return | `title,authors,year,venue,doi,abstract,citationCount,fieldsOfStudy` |
| `limit` | Results per request (max 500) | `100` |
| `offset` | Pagination offset | `0` |

### Response Fields Used

| Field | Description | Mapping |
|---|---|---|
| `title` | Paper title | `title` |
| `authors[].name` | Author names | `authors` |
| `year` | Publication year | `year` |
| `venue` | Journal/conference name | `journal` |
| `doi` | DOI identifier | `doi` |
| `abstract` | Abstract text | `abstract` |
| `citationCount` | Number of citations | `citations` |
| `influentialCitationCount` | High-impact citations | `influential_citations` |
| `fieldsOfStudy` | Fields (CS, Psychology, etc.) | `keywords`, `fields_of_study` |
| `externalIds.DOI` | DOI in externalIds | `doi` |

### Rate Limits

- **Anonymous**: 100 requests / 5 minutes
- **With API key**: 1 req/sec (up to 10,000/day)
- Script内置 6s 延迟以遵守限速
- Get free API key at: https://www.semanticscholar.org/product#api

---

## 3. Journal Level Lookup (Optional)

`scripts/journal_level.py` provides journal quartile/IF lookup.
See `SKILL.md` Step 3 for usage.

Data sources:
- JCR (Clarivate) — requires institution access
- ScimagoJR — free, no key: https://www.scimagojr.com/

---

## 4. Storing API Keys (Optional)

When the user provides API keys for WoS/Springer (optional upgrades), store them as:

```bash
export NCBI_API_KEY="your-ncbi-key"      # PubMed higher rate limit
export S2_API_KEY="your-s2-key"          # Semantic Scholar higher rate limit
export WOS_API_KEY="your-wos-key"        # Optional: WoS Starter API
export SPRINGER_API_KEY="your-springer-key"  # Optional: Springer API
```

The bundled scripts `search_pubmed.py` and `search_semantic.py` work **without any keys**.

---

## 5. APA Citation Format

When generating citations, use APA 7th edition:

```
Author, A. A., & Author, B. B. (Year). Title of article. Journal Name, Volume(Issue), pages. https://doi.org/xxxxx
```

PubMed provides PMID-based links: `https://pubmed.ncbi.nlm.nih.gov/PMID/`
Semantic Scholar provides paper URLs: `https://www.semanticscholar.org/paper/PAPER_ID`
