# Crossref API Reference

The verification/correction step uses the Crossref REST API, the authoritative DOI registry.

## Endpoint

`GET https://api.crossref.org/works/{DOI}`

Returns JSON with a `message` object. No API key is required for basic queries (polite pool).

## Key fields used

| Crossref field | Meaning | Maps to |
| --- | --- | --- |
| `message.title[]` | article title | title |
| `message.author[]` | `given` + `family` | authors |
| `message.container-title[]` | journal / venue name | journal |
| `message.volume`, `issue`, `page` | volume / issue / pages | volume / issue / pages |
| `message.published-print` / `published-online` / `issued` | publication date | year |
| `message.publisher` | publisher | publisher |
| `message.DOI` | DOI | doi |
| `message.type` | crossref type | reference type mapping |
| `message.resource.primary.URL` | publisher landing URL | url |

## Type mapping

`journal-article` → Journal Article (RIS `JOUR`); `book` / `monograph` / `edited-book` → Book (`BOOK`); `book-chapter` → Book Section (`CHAP`); `proceedings-article` → Conference Paper (`CONF`); `dissertation` → Thesis (`THES`); `report` → Report (`RPRT`); everything else defaults to Web Page (`ELEC`).

## Failure modes

- **HTTP 404** — the DOI is not in Crossref (common for Chinese journals or very new/non-registered works). Mark `待人工确认`.
- **Network failure** — the lookup returns `None`; mark `待人工确认` and note the network error.
- **Multiple works** — not applicable for a single DOI; Crossref returns one `message`.

## Adding fields or sources

To extend verification (e.g. PubMed PMID, arXiv, ISBN), add a lookup function beside `lookup_doi` in `scripts/crossref.py` and call it from `crosscheck`. Keep the same normalization contract: return a dict with `title/authors/year/journal/volume/issue/pages/doi/type/url`, then let the existing `crosscheck` fill and compare.
