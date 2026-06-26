---
name: scholar-search
description: Search academic papers and authors via the Scholar API (scholar.x49.ai). Use for finding papers by topic, keyword, or natural-language query, discovering authors, getting search suggestions, looking up paper metadata, checking journal rankings (JCR/CCF/FQBJCR), or filtering by open access, year range, paper type, or venue. Covers all academic disciplines. Triggers when user mentions academic papers, scholarly articles, research papers, literature search, journal articles, author lookup, citation counts, open access, or wants to search scholarly databases.
allowed-tools: Bash
argument-hint: "[search query]"
effort: high
metadata:
  skill-author: scholar.x49.ai
---

# Scholar Search

Search academic papers and authors via the Scholar API at `https://scholar.x49.ai`.

## When to Use This Skill

Use this skill when the user needs to:
- Search for academic papers by topic, keyword, or natural-language query
- Find papers from specific years, venues, authors, or institutions
- Get search autocomplete suggestions
- Look up detailed metadata for one or more papers by their `paper_ref`
- Find researchers by name and get their profiles
- List an author's representative or recent papers
- Check journal rankings (JCR, CCF, FQBJCR tiers)
- Filter by open access, paper type, or citation count

## API Configuration

The API base URL is `https://scholar.x49.ai/api/v1`.

Authentication uses a Bearer token. Resolve the key in this order:

1. Environment variable `SCHOLAR_API_KEY`
2. Built-in free key: `psk_tLzPCmJdUw5oAHGeXL2H_fMrDdSyiF_SBJfn2p5uCO4`

Users can get their own higher-quota key at: https://scholar.x49.ai/docs?section=api-keys

**Always construct API calls like this:**

```bash
SCHOLAR_KEY="${SCHOLAR_API_KEY:-psk_tLzPCmJdUw5oAHGeXL2H_fMrDdSyiF_SBJfn2p5uCO4}"
BASE="https://scholar.x49.ai/api/v1"
```

---

## Endpoints

### 1. Paper Search: `POST /papers/search`

The primary search endpoint. Supports two modes via the same URL:

- **Standard** (`mode=standard`): Exact keyword matching, larger result pool
- **Semantic** (`mode=semantic`): Natural-language understanding, more relevant results

The two modes consume separate monthly quotas.

```bash
SCHOLAR_KEY="${SCHOLAR_API_KEY:-psk_tLzPCmJdUw5oAHGeXL2H_fMrDdSyiF_SBJfn2p5uCO4}"
curl -s "https://scholar.x49.ai/api/v1/papers/search" \
  -H "Authorization: Bearer ${SCHOLAR_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "transformer attention mechanism",
    "mode": "standard",
    "limit": 10,
    "sort": "relevance",
    "filters": {}
  }'
```

**Request body fields:**

| Field | Type | Required | Meaning |
|---|---|---|---|
| `query` | string | Conditionally | Natural-language query text. If omitted, provide at least one `author_ref` in filters |
| `mode` | string | No | `standard` (default) or `semantic` |
| `limit` | integer | No | Results per call, 1-100. Default varies |
| `sort` | string | No | `relevance`, `most_cited`, `newest`, or `oldest` |

**Filters object** (nested under `filters`):

| Filter | Type | Meaning |
|---|---|---|
| `year_from` / `year_to` | integer | Publication year range |
| `paper_types` | string[] | e.g. `["article", "review"]` |
| `venues` | string[] | Journal or conference names |
| `concepts` | string[] | Topic or concept labels |
| `institutions` | string[] | Institution names |
| `author_refs` | string[] | Public author references |
| `open_access` | boolean | `true` for open-access papers only |

**Key response fields:**

- `data.items[]` — Paper cards in this batch
- `data.items[].paper_ref` — Stable public reference (use for batch/detail lookups)
- `data.items[].authors[].author_ref` — Use for author detail and papers
- `data.facets` — Aggregated filter values (years, concepts, venues, institutions, paper_types, venue_quality)
- `meta.total_results` — Total matches under current filters
- `meta.limit` — The result cap you requested

---

### 2. Search Suggestions: `GET /search/suggestions`

Get autocomplete suggestions and filter candidate values.

```bash
curl -s "${BASE}/search/suggestions?query=transformer&type=all&limit=5" \
  -H "Authorization: Bearer ${KEY}"
```

**Parameters** (query string):

| Parameter | Type | Required | Meaning |
|---|---|---|---|
| `query` | string | Yes | The typed prefix |
| `type` | string | No | `all` (default), `author`, `venue`, `concept`, `institution`, `paper_type`, `year` |
| `limit` | integer | No | Max suggestions to return |

**Response**: Mixed or typed suggestion items with counts.

---

### 3. Paper Batch Lookup: `POST /papers/batch`

Expand one or more `paper_ref` values into full metadata.

```bash
curl -s "${BASE}/papers/batch" \
  -H "Authorization: Bearer ${KEY}" \
  -H "Content-Type: application/json" \
  -d '{"paper_refs":["pap_ebcabae1be4244f3adba","pap_4748c234f5384d0eaee2"]}'
```

**Request body:**

| Field | Type | Required | Meaning |
|---|---|---|---|
| `paper_refs` | string[] | Yes | Public paper references from search results |

**Response**: Array of full paper cards, same structure as search items.

---

### 4. Author Search: `GET /authors/search`

Find authors by name.

```bash
curl -s "${BASE}/authors/search?query=Hyeongwon+Kang&limit=5" \
  -H "Authorization: Bearer ${KEY}"
```

**Parameters** (query string):

| Parameter | Type | Required | Meaning |
|---|---|---|---|
| `query` | string | Yes | Author name or keyword |
| `limit` | integer | No | Max results to return |

**Response**: Author candidates with `author_ref`, `name`, `last_known_institution`, `metrics` (citation_count, paper_count), and `identifiers` (orcid).

---

### 5. Author Detail: `GET /authors/{author_ref}`

Show the full author profile.

```bash
curl -s "${BASE}/authors/aut_d2610a19ad8c4b1ca298" \
  -H "Authorization: Bearer ${KEY}"
```

**Response includes**: name, affiliations (with country, type, years), aliases, identifiers (orcid), metrics (citation_count, h_index, i10_index, paper_count, two_year_mean_citedness), top_venues, topics (with paper_count and score).

---

### 6. Author Papers: `GET /authors/{author_ref}/papers`

List representative or recent papers for one author.

```bash
curl -s "${BASE}/authors/aut_d2610a19ad8c4b1ca298/papers?limit=10" \
  -H "Authorization: Bearer ${KEY}"
```

**Parameters** (query string):

| Parameter | Type | Required | Meaning |
|---|---|---|---|
| `limit` | integer | No | Number of papers to return |

**Response**: Paper cards, same structure as search items. Default sort is `most_cited`.

---

## Common Usage Patterns

### Pattern 1: Quick topic search

User asks: "Find recent papers on CRISPR gene editing"

1. Call `POST /papers/search` with `mode=standard`, `sort=newest`, reasonable `limit`
2. Present results as a formatted list with title, authors, year, venue, citation count
3. Note the `paper_ref` values for any follow-up requests

### Pattern 2: Semantic / discovery search

User asks: "How does transfer learning help in medical image analysis?"

1. Call `POST /papers/search` with `mode=semantic` - this mode understands natural-language queries
2. Present the most relevant results

### Pattern 3: Author workflow

User asks: "Find papers by Yann LeCun"

1. Call `GET /authors/search?query=Yann+LeCun` to find the author
2. Pick the best match from results
3. Call `GET /authors/{author_ref}` for profile details
4. Call `GET /authors/{author_ref}/papers` for their publications

### Pattern 4: Paper detail expansion

User asks: "Get more details on these papers" (after seeing search results)

1. Collect `paper_ref` values from prior results
2. Call `POST /papers/batch` with those refs
3. Present the full metadata

### Pattern 5: Filtered search

User asks: "Find highly-cited open-access review papers on machine learning from Nature or Science published 2022-2025"

1. Build the search with appropriate filters:
   ```json
   {
     "query": "machine learning",
     "mode": "standard",
     "sort": "most_cited",
     "limit": 10,
     "filters": {
       "year_from": 2022,
       "year_to": 2025,
       "paper_types": ["review"],
       "venues": ["Nature", "Science"],
       "open_access": true
     }
   }
   ```

### Pattern 6: Suggestions for autocomplete

User asks: "What are popular topics related to CRISPR?"

1. Call `GET /search/suggestions?query=CRISPR&type=concept&limit=10`
2. Present the concept suggestions with counts

---

## Presenting Results

When displaying search results to the user, format them clearly:

```
### [Paper Title](landing_page_url)
- **Authors**: Author1, Author2, Author3
- **Year**: 2024 | **Venue**: Journal Name (JCR Q1)
- **Citations**: 88 | **Type**: article | **Open Access**: No
- **paper_ref**: pap_xxxxx
> Abstract snippet (first 200 chars)...
```

For author results:

```
### [Author Name]
- **Institution**: University Name
- **Papers**: 42 | **Citations**: 1,230 | **h-index**: 15
- **ORCID**: 0000-xxxx-xxxx-xxxx
- **author_ref**: aut_xxxxx
```

---

## Notes

- The `metrics.relevance` field in search results is typically `null` - this is expected
- Parse JSON responses with `python3 -m json.tool` for readable output when debugging
- Use URL encoding for query parameters with special characters (spaces become `+` or `%20`)
- All date/time fields use ISO 8601 format
- The `venue.quality_signals` array contains JCR, FQBJCR, and CCF tier information when available
