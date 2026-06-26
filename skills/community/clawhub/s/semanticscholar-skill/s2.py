import time, os, json, requests, sys

GRAPH = "https://api.semanticscholar.org/graph/v1"
RECS = "https://api.semanticscholar.org/recommendations/v1"
DATASETS = "https://api.semanticscholar.org/datasets/v1"
HEADERS = {"x-api-key": os.environ.get("S2_API_KEY", "")}

# Module-level rate coordination
_last_request_time = 0
_MIN_GAP = 1.1  # seconds between requests


def _request(method, url, params=None, json_data=None, max_retries=5):
    global _last_request_time
    # Enforce minimum gap
    elapsed = time.time() - _last_request_time
    if elapsed < _MIN_GAP:
        time.sleep(_MIN_GAP - elapsed)

    for attempt in range(max_retries + 1):
        _last_request_time = time.time()
        try:
            if method == "GET":
                r = requests.get(url, params=params, headers=HEADERS, timeout=30)
            else:
                r = requests.post(url, params=params, json=json_data, headers=HEADERS, timeout=30)
        except (requests.ConnectionError, requests.Timeout) as e:
            if attempt < max_retries:
                wait = min(2 ** (attempt + 1), 60)
                print(f"  [conn-error] {type(e).__name__}, retry {attempt+1}/{max_retries} in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise

        if r.status_code in (429, 504):
            if attempt < max_retries:
                wait = min(2 ** (attempt + 1), 60)
                print(f"  [rate-limit] {r.status_code}, retry {attempt+1}/{max_retries} in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            r.raise_for_status()
        elif r.status_code >= 400:
            r.raise_for_status()
        return r.json()


def s2_get(url, params=None):
    return _request("GET", url, params=params)


def s2_post(url, params=None, json_data=None):
    return _request("POST", url, params=params, json_data=json_data)


# --- Pagination ---

def paginate(url, params=None, max_results=1000):
    params = dict(params or {})
    params.setdefault("limit", 100)
    params["offset"] = 0
    results = []
    while len(results) < max_results:
        r = s2_get(url, params)
        results.extend(r.get("data", []))
        if "next" not in r or len(results) >= max_results:
            break
        params["offset"] = r["next"]
    return results[:max_results]


def paginate_bulk(url, params=None, max_results=10000):
    params = dict(params or {})
    token = None
    results = []
    while len(results) < max_results:
        if token:
            params["token"] = token
        r = s2_get(url, params)
        results.extend(r.get("data", []))
        token = r.get("token")
        if not token or len(results) >= max_results:
            break
    return results[:max_results]


# --- Batch ---

def batch_papers(ids, fields="title,year,citationCount"):
    return s2_post(f"{GRAPH}/paper/batch", params={"fields": fields}, json_data={"ids": ids[:500]})


def batch_authors(ids, fields="name,hIndex,paperCount"):
    return s2_post(f"{GRAPH}/author/batch", params={"fields": fields}, json_data={"ids": ids[:1000]})


# --- High-level search functions ---

_DEFAULT_FIELDS = "title,year,citationCount,authors,venue,externalIds,tldr"
_BULK_FIELDS = "title,year,citationCount,authors,venue,externalIds"  # bulk search doesn't support tldr

def _add_filters(params, year=None, venue=None, fields_of_study=None,
                 min_citations=None, pub_types=None, open_access=False,
                 publication_date=None):
    if year: params["year"] = year
    if publication_date: params["publicationDateOrYear"] = publication_date
    if venue: params["venue"] = venue
    if fields_of_study: params["fieldsOfStudy"] = fields_of_study
    if min_citations: params["minCitationCount"] = str(min_citations)
    if pub_types: params["publicationTypes"] = pub_types
    if open_access: params["openAccessPdf"] = ""
    return params


def search_relevance(query, fields=_DEFAULT_FIELDS, max_results=20, **filters):
    params = _add_filters({"query": query, "fields": fields, "limit": min(max_results, 100)}, **filters)
    if max_results <= 100:
        r = s2_get(f"{GRAPH}/paper/search", params)
        return r.get("data", [])[:max_results]
    return paginate(f"{GRAPH}/paper/search", params, max_results)


def search_bulk(query, fields=_BULK_FIELDS, max_results=100, sort="citationCount:desc", **filters):
    params = _add_filters({"query": query, "fields": fields, "sort": sort}, **filters)
    return paginate_bulk(f"{GRAPH}/paper/search/bulk", params, max_results)


def search_snippets(query, fields="snippet.text,snippet.snippetKind,snippet.section",
                    max_results=10, **filters):
    params = _add_filters({"query": query, "fields": fields, "limit": min(max_results, 100)}, **filters)
    return s2_get(f"{GRAPH}/snippet/search", params).get("data", [])[:max_results]


def get_paper(paper_id, fields=_DEFAULT_FIELDS + ",abstract,references,openAccessPdf"):
    return s2_get(f"{GRAPH}/paper/{paper_id}", {"fields": fields})


def get_citations(paper_id, fields="title,year,citationCount,authors,venue", max_results=100):
    return paginate(f"{GRAPH}/paper/{paper_id}/citations",
                    {"fields": fields, "limit": min(max_results, 1000)}, max_results)


def get_references(paper_id, fields="title,year,citationCount,authors,venue", max_results=100):
    return paginate(f"{GRAPH}/paper/{paper_id}/references",
                    {"fields": fields, "limit": min(max_results, 1000)}, max_results)


def find_similar(paper_id, fields="title,year,citationCount,authors,venue", limit=10, pool="recent"):
    return s2_get(f"{RECS}/papers/forpaper/{paper_id}",
                  {"fields": fields, "limit": limit, "from": pool}).get("recommendedPapers", [])


def recommend(positive_ids, negative_ids=None, fields="title,year,citationCount,authors,venue", limit=10):
    body = {"positivePaperIds": positive_ids}
    if negative_ids:
        body["negativePaperIds"] = negative_ids
    return s2_post(f"{RECS}/papers/", params={"fields": fields, "limit": limit},
                   json_data=body).get("recommendedPapers", [])


# --- Author functions ---

_DEFAULT_AUTHOR_FIELDS = "name,affiliations,paperCount,citationCount,hIndex"


def search_authors(query, fields=_DEFAULT_AUTHOR_FIELDS, max_results=20):
    params = {"query": query, "fields": fields, "limit": min(max_results, 1000)}
    if max_results <= 1000:
        r = s2_get(f"{GRAPH}/author/search", params)
        return r.get("data", [])[:max_results]
    return paginate(f"{GRAPH}/author/search", params, max_results)


def get_author(author_id, fields=_DEFAULT_AUTHOR_FIELDS):
    return s2_get(f"{GRAPH}/author/{author_id}", {"fields": fields})


def get_author_papers(author_id, fields=_DEFAULT_FIELDS, max_results=100):
    return paginate(f"{GRAPH}/author/{author_id}/papers",
                    {"fields": fields, "limit": min(max_results, 1000)}, max_results)


def get_paper_authors(paper_id, fields=_DEFAULT_AUTHOR_FIELDS, max_results=100):
    return paginate(f"{GRAPH}/paper/{paper_id}/authors",
                    {"fields": fields, "limit": min(max_results, 1000)}, max_results)


def match_title(title, fields=_DEFAULT_FIELDS):
    return s2_get(f"{GRAPH}/paper/search/match", {"query": title, "fields": fields})


# --- Utilities ---

def deduplicate(papers):
    seen = set()
    out = []
    for p in papers:
        pid = p.get("paperId")
        if pid and pid not in seen:
            seen.add(pid)
            out.append(p)
    return out


def build_bool_query(phrases=None, required=None, excluded=None, or_terms=None):
    parts = []
    for p in (phrases or []):
        parts.append(f'"{p}"')
    for r in (required or []):
        parts.append(f"+{r}")
    for e in (excluded or []):
        parts.append(f"-{e}")
    if or_terms:
        parts.append("(" + " | ".join(or_terms) + ")")
    return " ".join(parts)


# --- Output formatting ---

def _doi(paper):
    ext = paper.get("externalIds") or {}
    return ext.get("DOI", "")


def _first_author(paper):
    authors = paper.get("authors") or []
    if not authors:
        return ""
    name = authors[0].get("name", "")
    return f"{name} et al." if len(authors) > 1 else name


def format_table(papers, max_rows=30):
    rows = ["| # | Title | Year | Cites | First Author | Venue |",
            "|---|-------|------|-------|-------------|-------|"]
    for i, p in enumerate(papers[:max_rows], 1):
        t = (p.get("title") or "")[:80]
        y = p.get("year") or ""
        c = p.get("citationCount") or 0
        a = _first_author(p)[:25]
        v = (p.get("venue") or "")[:30]
        rows.append(f"| {i} | {t} | {y} | {c} | {a} | {v} |")
    return "\n".join(rows)


def format_details(papers, max_papers=10):
    lines = []
    for i, p in enumerate(papers[:max_papers], 1):
        title = p.get("title") or "Untitled"
        year = p.get("year") or "?"
        cites = p.get("citationCount") or 0
        doi = _doi(p)
        authors = ", ".join(a.get("name", "") for a in (p.get("authors") or [])[:5])
        if len(p.get("authors") or []) > 5:
            authors += " et al."
        tldr = (p.get("tldr") or {}).get("text", "")
        abstract = (p.get("abstract") or "")[:300]
        summary = tldr or (abstract + "..." if len(p.get("abstract") or "") > 300 else abstract)

        lines.append(f"### {i}. {title} ({year})")
        lines.append(f"**Authors:** {authors}")
        lines.append(f"**Citations:** {cites} | **DOI:** {doi}" if doi else f"**Citations:** {cites}")
        if summary:
            lines.append(f"**Summary:** {summary}")
        lines.append("")
    return "\n".join(lines)


def format_results(papers, query_desc=""):
    n = len(papers)
    header = f"## Search Results: {query_desc}\n\n**{n} papers found.**\n" if query_desc else f"**{n} papers found.**\n"
    table = format_table(papers)
    details = format_details(papers[:10])
    return f"{header}\n{table}\n\n---\n\n{details}"


def format_authors(authors, max_rows=20):
    rows = ["| # | Name | Affiliations | Papers | Citations | h-index |",
            "|---|------|-------------|--------|-----------|---------|"]
    for i, a in enumerate(authors[:max_rows], 1):
        name = a.get("name", "")
        affs = ", ".join(a.get("affiliations") or [])[:40]
        pc = a.get("paperCount") or 0
        cc = a.get("citationCount") or 0
        h = a.get("hIndex") or 0
        rows.append(f"| {i} | {name} | {affs} | {pc} | {cc} | {h} |")
    return "\n".join(rows)


def export_bibtex(papers):
    entries = []
    for p in papers:
        bib = (p.get("citationStyles") or {}).get("bibtex")
        if bib:
            entries.append(bib)
    return "\n\n".join(entries)


def export_markdown(papers, query_desc="", path="/tmp/s2_results.md"):
    content = format_results(papers, query_desc)
    with open(path, "w") as f:
        f.write(content)
    print(f"Saved {len(papers)} papers to {path}")
    return path


def export_json(papers, path="/tmp/s2_results.json"):
    with open(path, "w") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(papers)} papers to {path}")
    return path
