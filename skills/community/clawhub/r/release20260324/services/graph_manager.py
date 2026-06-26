"""Graph management — add papers, convert to seed, persist to JSON.

Provides the core logic for interactive graph editing from the HTML viewer.
All mutations are written back to the graph JSON file (source of truth).
"""
import sys
import re
import json
from typing import Optional, List, Tuple

from schemas import Paper, GraphData


def _title_similarity(a: str, b: str) -> float:
    """Jaccard similarity on word sets, with containment boost.

    If the shorter title's words are mostly contained in the longer title
    (e.g. truncated title), use containment ratio instead of Jaccard.
    This handles cases like 'Paper Title: Full Subtitle' vs 'Paper Title: Full'.
    """
    wa = set(re.sub(r'[^a-z0-9\s]', '', a.lower()).split())
    wb = set(re.sub(r'[^a-z0-9\s]', '', b.lower()).split())
    if not wa or not wb:
        return 0.0
    intersection = len(wa & wb)
    jaccard = intersection / len(wa | wb)
    # Containment: what fraction of the *shorter* set is in the longer?
    shorter = min(len(wa), len(wb))
    containment = intersection / shorter if shorter > 0 else 0.0
    # Use containment if shorter title has >= 5 words and >= 80% contained
    if shorter >= 5 and containment >= 0.8:
        return max(jaccard, containment)
    return jaccard


def _normalize_key(paper: Paper) -> str:
    """Stable dedup key: prefer DOI > arXiv ID > normalized title+year."""
    if paper.doi:
        return f"doi:{paper.doi.lower()}"
    if paper.arxiv_id:
        aid = re.sub(r'v\\d+$', '', paper.arxiv_id)
        return f"arxiv:{aid.lower().replace('arxiv:', '')}"
    norm_title = re.sub(r'[^a-z0-9]', '', (paper.title or '').lower())
    return f"title:{norm_title}:{paper.year or 'x'}"


def find_existing(graph: GraphData, paper: Paper) -> Optional[Paper]:
    """Find a paper in the graph by DOI, arXiv ID, or fuzzy title match."""
    key = _normalize_key(paper)
    for node in graph.nodes:
        if _normalize_key(node) == key:
            return node
        if paper.title and node.title and _title_similarity(paper.title, node.title) >= 0.85:
            if paper.year and node.year and abs(paper.year - node.year) <= 1:
                return node
            if not paper.year or not node.year:
                return node
    return None


def _dedup_edges(edges: list) -> list:
    seen = set()
    result = []
    for e in edges:
        key = (e["source"], e["target"])
        if key not in seen:
            seen.add(key)
            result.append(e)
    return result


def dedup_and_merge_nodes(graph: GraphData) -> int:
    """Find duplicate nodes in graph, merge them, and rewrite edges.

    Merge rules:
    - seed paper wins over non-seed (keep seed's ID, merge non-seed's info in)
    - same status → merge into the one with more complete metadata
    - all edges pointing to/from the removed node are rewritten to the kept node
    - seed_papers list is updated accordingly

    Returns number of nodes removed.
    """
    merged_count = 0
    # Build groups of duplicate nodes using _normalize_key + fuzzy title
    # Process in order so we can track which nodes have been consumed
    consumed = set()  # IDs of nodes that were merged into another
    id_remap = {}     # old_id → new_id for edge rewriting

    node_list = list(graph.nodes)
    for i, a in enumerate(node_list):
        if a.id in consumed:
            continue
        for j in range(i + 1, len(node_list)):
            b = node_list[j]
            if b.id in consumed:
                continue
            if not _is_same_paper(a, b):
                continue

            # Found duplicate: decide which to keep
            # Rule: seed wins; if both same status, keep whichever has more info
            if a.is_seed and not b.is_seed:
                keep, remove = a, b
            elif b.is_seed and not a.is_seed:
                keep, remove = b, a
            else:
                # Same status — keep the one with more metadata
                def _info_score(p):
                    s = 0
                    if p.doi: s += 1
                    if p.arxiv_id: s += 1
                    if p.abstract: s += 1
                    if p.year: s += 1
                    if p.authors: s += len(p.authors)
                    if p.url: s += 1
                    if p.pdf_url: s += 1
                    s += p.citation_count
                    return s
                if _info_score(a) >= _info_score(b):
                    keep, remove = a, b
                else:
                    keep, remove = b, a

            # Merge metadata from remove into keep
            _merge_metadata(keep, remove)
            # Also merge fields that _merge_metadata doesn't cover
            if not keep.title and remove.title:
                keep.title = remove.title
            if not keep.authors and remove.authors:
                keep.authors = remove.authors
            if not keep.year and remove.year:
                keep.year = remove.year
            if not keep.source or keep.source == "unknown":
                keep.source = remove.source
            if remove.refs_expanded and not keep.refs_expanded:
                keep.refs_expanded = True
            if remove.cites_expanded and not keep.cites_expanded:
                keep.cites_expanded = True
            if remove.is_seed:
                keep.is_seed = True

            consumed.add(remove.id)
            id_remap[remove.id] = keep.id
            merged_count += 1
            print(f"[dedup] Merged '{remove.title[:50] if remove.title else remove.id}' → '{keep.title[:50] if keep.title else keep.id}'", file=sys.stderr)

    if not id_remap:
        return 0

    # Remove consumed nodes
    graph.nodes = [n for n in graph.nodes if n.id not in consumed]

    # Rewrite edges
    for e in graph.edges:
        if e["source"] in id_remap:
            e["source"] = id_remap[e["source"]]
        if e["target"] in id_remap:
            e["target"] = id_remap[e["target"]]

    # Dedup edges after rewrite (merging may create duplicates)
    graph.edges = _dedup_edges(graph.edges)

    # Remove self-loops
    graph.edges = [e for e in graph.edges if e["source"] != e["target"]]

    # Update seed_papers list
    new_seeds = []
    seen_seeds = set()
    for sid in graph.seed_papers:
        actual = id_remap.get(sid, sid)
        if actual not in seen_seeds:
            seen_seeds.add(actual)
            new_seeds.append(actual)
    graph.seed_papers = new_seeds

    print(f"[dedup] Removed {merged_count} duplicate nodes, graph now {len(graph.nodes)} papers, {len(graph.edges)} edges", file=sys.stderr)
    return merged_count


def _is_same_paper(a: Paper, b: Paper) -> bool:
    """Check if two Paper objects refer to the same real-world paper."""
    if a.id == b.id:
        return True
    # DOI match
    if a.doi and b.doi and a.doi.lower().strip() == b.doi.lower().strip():
        return True
    # arXiv ID match (strip version suffix)
    if a.arxiv_id and b.arxiv_id:
        aid_a = re.sub(r'v\d+$', '', a.arxiv_id.lower().replace('arxiv:', ''))
        aid_b = re.sub(r'v\d+$', '', b.arxiv_id.lower().replace('arxiv:', ''))
        if aid_a == aid_b:
            return True
    # Normalized key match
    if _normalize_key(a) == _normalize_key(b):
        return True
    # Fuzzy title match
    if a.title and b.title and _title_similarity(a.title, b.title) >= 0.85:
        if a.year and b.year:
            return abs(a.year - b.year) <= 1
        return True  # if either year unknown, trust title similarity
    return False


def save_graph(graph: GraphData, path: str):
    """Dedup + merge nodes, then persist graph to JSON file."""
    dedup_and_merge_nodes(graph)
    graph.edges = _dedup_edges(graph.edges)
    graph.total_papers = len(graph.nodes)
    graph.save(path)
    print(f"[graph-manager] Saved graph to {path}: {graph.total_papers} papers, {len(graph.edges)} edges", file=sys.stderr)


def enrich_incomplete_papers(graph: GraphData, graph_path: str) -> int:
    """Enrich papers that are missing year/authors/abstract by re-fetching metadata.

    Tries: S2 API (by paper ID) → arXiv search (by title) → S2 search (by title).
    Returns number of papers enriched.
    """
    from services import semantic_scholar as s2
    from services import arxiv

    incomplete = [p for p in graph.nodes
                  if p.resolved and (not p.year or not p.authors or not p.abstract)]

    if not incomplete:
        return 0

    print(f"[graph-manager] Enriching {len(incomplete)} papers with missing metadata...",
          file=sys.stderr)
    enriched = 0

    for paper in incomplete:
        found = None

        # Strategy 1: S2 API direct lookup by ID (most reliable)
        if paper.id and not paper.id.startswith(("pdf:", "bibtex:", "crossref:", "openalex:", "unresolved:")):
            try:
                result = s2.get_paper(paper.id)
                found = result.get("paper") if isinstance(result, dict) else None
            except Exception:
                pass

        # Strategy 2: arXiv search by title
        if not found and paper.title:
            try:
                _, results = arxiv.search(paper.title, limit=3)
                for r in results:
                    if _title_similarity(paper.title, r.title) >= 0.7:
                        found = r
                        break
            except Exception:
                pass

        # Strategy 3: S2 search by title
        if not found and paper.title:
            try:
                _, results = s2._s2_search(paper.title, limit=3)
                for r in results:
                    if _title_similarity(paper.title, r.title) >= 0.7:
                        found = r
                        break
            except Exception:
                pass

        if found:
            if not paper.year and found.year:
                paper.year = found.year
            if (not paper.authors or paper.authors == []) and found.authors:
                paper.authors = found.authors
            if not paper.abstract and found.abstract:
                paper.abstract = found.abstract
            if not paper.doi and found.doi:
                paper.doi = found.doi
            if not paper.arxiv_id and found.arxiv_id:
                paper.arxiv_id = found.arxiv_id
            if not paper.url and found.url:
                paper.url = found.url
            if found.citation_count and found.citation_count > paper.citation_count:
                paper.citation_count = found.citation_count
            enriched += 1
            print(f"[graph-manager]   Enriched: {paper.title[:50]} → year={paper.year}, "
                  f"authors={len(paper.authors or [])}", file=sys.stderr)

    if enriched:
        save_graph(graph, graph_path)
        print(f"[graph-manager] Enriched {enriched}/{len(incomplete)} papers", file=sys.stderr)

    return enriched


class RateLimitError(Exception):
    """Raised when all sources are rate-limited."""
    def __init__(self, sources: list, message: str = None):
        self.sources = sources
        self.message = message or f"Rate limited by: {', '.join(sources)}"
        super().__init__(self.message)


def resolve_paper_by_title(title: str) -> Optional[Paper]:
    """Resolve a paper by title, ID (S2 hex, ARXIV:, DOI:), or search."""
    from services import arxiv
    from services import semantic_scholar as s2

    title = title.strip()
    if not title:
        return None

    rate_limited_sources = []

    # Check if it's already an ID (S2 hex, ARXIV:xxx, DOI:xxx)
    s2_re = re.compile(r'^[0-9a-fA-F]{40}$')
    if s2_re.match(title) or re.match(r'^(ARXIV|DOI):', title, re.IGNORECASE):
        try:
            result = s2.get_paper(title)
            paper = result["paper"]
            print(f"[graph-manager] Resolved by ID: {paper.title} ({paper.id})", file=sys.stderr)
            return paper
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "rate" in err_str:
                rate_limited_sources.append("Semantic Scholar")
            print(f"[graph-manager] ID lookup failed for {title}: {e}", file=sys.stderr)
            if rate_limited_sources:
                raise RateLimitError(rate_limited_sources)
            return None

    # Try arXiv search first — use short query (arXiv API returns junk for long queries)
    try:
        if ':' in title:
            short_query = title.split(':')[0].strip()
        else:
            words = title.split()
            short_query = ' '.join(words[:8])
        short_query = re.sub(r'[:\-,;/()]+', ' ', short_query).strip()
        short_query = re.sub(r'\s+', ' ', short_query)
        print(f"[graph-manager] arXiv search: '{short_query}'", file=sys.stderr)
        total, papers = arxiv.search(short_query, limit=10)
        for p in papers:
            if _title_similarity(title, p.title) >= 0.5:
                print(f"[graph-manager] Resolved via arXiv: {p.title} ({p.id})", file=sys.stderr)
                return p
    except Exception as e:
        err_str = str(e).lower()
        if "429" in err_str or "rate" in err_str:
            rate_limited_sources.append("arXiv")
        print(f"[graph-manager] arXiv search failed: {e}", file=sys.stderr)

    # Try S2 search
    try:
        total, papers = s2._s2_search(title, limit=5)
        for p in papers:
            if _title_similarity(title, p.title) >= 0.5:
                print(f"[graph-manager] Resolved via S2: {p.title} ({p.id})", file=sys.stderr)
                return p
    except Exception as e:
        err_str = str(e).lower()
        if "429" in err_str or "rate" in err_str:
            rate_limited_sources.append("Semantic Scholar")
        print(f"[graph-manager] S2 search failed: {e}", file=sys.stderr)

    # If all failures were rate limits, raise specific error
    if rate_limited_sources:
        raise RateLimitError(rate_limited_sources)

    return None


def resolve_paper_by_bibtex(bibtex: str) -> Optional[Paper]:
    """Parse BibTeX to extract title/DOI/arXiv, then resolve."""
    title = None
    doi = None
    arxiv_id = None
    year = None
    authors = []

    # Extract fields from BibTeX
    title_match = re.search(r'title\s*=\s*\{([^}]+)\}', bibtex, re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()

    doi_match = re.search(r'doi\s*=\s*\{([^}]+)\}', bibtex, re.IGNORECASE)
    if doi_match:
        doi = doi_match.group(1).strip()

    arxiv_match = re.search(r'(?:eprint|arxiv)\s*=\s*\{([^}]+)\}', bibtex, re.IGNORECASE)
    if arxiv_match:
        arxiv_id = arxiv_match.group(1).strip()

    year_match = re.search(r'year\s*=\s*\{?(\d{4})\}?', bibtex, re.IGNORECASE)
    if year_match:
        year = int(year_match.group(1))

    author_match = re.search(r'author\s*=\s*\{([^}]+)\}', bibtex, re.IGNORECASE)
    if author_match:
        raw = author_match.group(1).strip()
        authors = [a.strip() for a in raw.split(' and ')]

    # Try DOI first via S2
    if doi:
        from services import semantic_scholar as s2
        try:
            result = s2.get_paper(f"DOI:{doi}")
            paper = result["paper"]
            print(f"[graph-manager] Resolved via DOI: {paper.title}", file=sys.stderr)
            return paper
        except Exception:
            pass

    # Try arXiv ID via S2
    if arxiv_id:
        from services import semantic_scholar as s2
        try:
            result = s2.get_paper(f"ARXIV:{arxiv_id}")
            paper = result["paper"]
            print(f"[graph-manager] Resolved via arXiv ID: {paper.title}", file=sys.stderr)
            return paper
        except Exception:
            pass

    # Fall back to title search
    if title:
        try:
            paper = resolve_paper_by_title(title)
        except RateLimitError:
            paper = None  # BibTeX has enough info to create a paper below
        if paper:
            # Enrich with BibTeX metadata
            if year and not paper.year:
                paper.year = year
            if authors and not paper.authors:
                paper.authors = authors
            if doi and not paper.doi:
                paper.doi = doi
            return paper

    # If nothing resolved, create a basic Paper from BibTeX fields
    if title:
        return Paper(
            id=f"bibtex:{re.sub(r'[^a-z0-9]', '', title.lower())[:40]}",
            title=title,
            authors=authors,
            year=year,
            doi=doi,
            arxiv_id=arxiv_id,
            resolved=False,
            source="bibtex",
        )

    return None


def resolve_paper_from_pdf(pdf_path: str) -> Tuple[Optional[Paper], list]:
    """Parse PDF, identify the paper, and extract references.

    Returns (paper, resolved_references).
    """
    from services.pdf_parser import parse_pdf
    from services.graph_builder import _identify_pdf_paper

    result = parse_pdf(pdf_path)
    paper = _identify_pdf_paper(pdf_path, result.get("text_length", 0))

    resolved_refs = [Paper(**p) for p in result.get("resolved_papers", [])]

    if not paper:
        import os
        fname = os.path.basename(pdf_path).replace(".pdf", "")
        paper = Paper(
            id=f"pdf:{fname}",
            title=f"[PDF] {fname}",
            resolved=False,
            source="pdf_upload",
        )

    return paper, resolved_refs


def _merge_metadata(existing: Paper, new: Paper):
    """Merge metadata from *new* into *existing* without overwriting present fields."""
    if not existing.doi and new.doi:
        existing.doi = new.doi
    if not existing.arxiv_id and new.arxiv_id:
        existing.arxiv_id = new.arxiv_id
    if not existing.abstract and new.abstract:
        existing.abstract = new.abstract
    if new.citation_count > existing.citation_count:
        existing.citation_count = new.citation_count
    if not existing.pdf_url and new.pdf_url:
        existing.pdf_url = new.pdf_url
    if not existing.url and new.url:
        existing.url = new.url


def _get_seed_references(paper: Paper, **kwargs) -> list:
    """Fetch references for a paper.

    Priority:
    1. PDF download → parse references (regex/GROBID)
    2. LLM extraction from PDF text (if LLM API configured)
    3. Return empty list (no S2/arXiv API calls for refs)
    """
    pdf_path = None

    # Step 1: Download PDF
    try:
        from services.paper_downloader import download_pdf
        pdf_path = download_pdf(paper)
    except Exception as e:
        print(f"[graph-manager] PDF download failed: {e}", file=sys.stderr)

    # Step 2: Parse references from PDF
    if pdf_path:
        try:
            from services.pdf_parser import parse_pdf
            result = parse_pdf(pdf_path)
            resolved = result.get("resolved_papers", [])
            if resolved:
                papers = [Paper(**p) for p in resolved]
                print(f"[graph-manager] PDF refs: {len(papers)} for {paper.title[:50]}", file=sys.stderr)
                return papers
        except Exception as e:
            print(f"[graph-manager] PDF ref extraction failed: {e}", file=sys.stderr)

    # Step 3: LLM fallback — extract references from PDF text via LLM
    if pdf_path:
        refs = _llm_extract_references(pdf_path, paper)
        if refs:
            return refs

    return []


def _llm_extract_references(pdf_path: str, paper: Paper) -> list:
    """Use LLM to extract references from PDF text when regex parsing fails."""
    try:
        from services.llm_client import is_llm_available, llm_chat
        if not is_llm_available():
            return []
    except ImportError:
        return []

    # Extract text from PDF
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        # Get last ~30% of text (where references typically are)
        total_pages = len(doc)
        start_page = max(0, int(total_pages * 0.7))
        text = ""
        for i in range(start_page, total_pages):
            text += doc[i].get_text()
        doc.close()
        if len(text) < 100:
            return []
    except Exception as e:
        print(f"[graph-manager] LLM ref: PDF text extraction failed: {e}", file=sys.stderr)
        return []

    # Truncate to fit in LLM context
    text = text[:12000]

    prompt = f"""Extract all references/bibliography entries from this academic paper text.
For each reference, provide: title, authors (comma-separated), year, and venue/journal.

Return ONLY a JSON array, no markdown, no explanation. Example:
[{{"title": "Attention is All You Need", "authors": "Vaswani, Shazeer, Parmar", "year": 2017, "venue": "NeurIPS"}}]

If you cannot find references, return: []

Text:
{text}"""

    try:
        response = llm_chat(prompt, max_tokens=4000, temperature=0.1)
        if not response:
            return []

        import json as _json
        # Extract JSON from response (handle markdown code blocks)
        response = response.strip()
        if response.startswith("```"):
            response = response.split("\n", 1)[1] if "\n" in response else response
            response = response.rsplit("```", 1)[0] if "```" in response else response
            response = response.strip()

        refs_data = _json.loads(response)
        if not isinstance(refs_data, list):
            return []

        papers = []
        for r in refs_data:
            title = r.get("title", "").strip()
            if not title:
                continue
            authors_raw = r.get("authors", "")
            authors = [a.strip() for a in authors_raw.split(",")] if isinstance(authors_raw, str) else authors_raw
            year = r.get("year")
            if isinstance(year, str) and year.isdigit():
                year = int(year)

            # Create Paper with a title-based ID (will be deduped by find_existing)
            pid = f"llm:{re.sub(r'[^a-z0-9]', '', title.lower())[:50]}"
            papers.append(Paper(
                id=pid,
                title=title,
                authors=authors,
                year=year,
                resolved=False,
                source="llm_extraction",
            ))

        if papers:
            print(f"[graph-manager] LLM extracted {len(papers)} references for {paper.title[:50]}", file=sys.stderr)
        return papers

    except Exception as e:
        print(f"[graph-manager] LLM ref extraction failed: {e}", file=sys.stderr)
        return []


def _get_seed_citations(paper: Paper) -> list:
    """Fetch citations for a paper.

    Priority: Google Scholar → S2 API.
    If both fail twice total, give up and return what we have.
    """
    citations = []
    failures = 0
    MAX_FAILURES = 2

    # 1. Google Scholar (title-based search)
    if paper.title and failures < MAX_FAILURES:
        try:
            from services.google_scholar import get_citations
            gs_cites = get_citations(paper.title, limit=50)
            if gs_cites:
                citations.extend(gs_cites)
                print(f"[graph-manager] Google Scholar: {len(gs_cites)} citations for {paper.title[:50]}", file=sys.stderr)
            else:
                failures += 1
                print(f"[graph-manager] Google Scholar returned 0 citations ({failures}/{MAX_FAILURES} failures)", file=sys.stderr)
        except Exception as e:
            failures += 1
            print(f"[graph-manager] Google Scholar failed ({failures}/{MAX_FAILURES}): {e}", file=sys.stderr)

    # 2. S2 API fallback (only if GS failed and we haven't hit failure limit)
    if not citations and failures < MAX_FAILURES and paper.id and not paper.id.startswith("pdf:"):
        try:
            from services import semantic_scholar as s2
            s2_cites = s2.get_citations(paper.id, limit=50)
            if s2_cites:
                citations.extend(s2_cites)
                print(f"[graph-manager] S2 citations: {len(s2_cites)} for {paper.title[:50]}", file=sys.stderr)
            else:
                failures += 1
                print(f"[graph-manager] S2 citations returned 0 ({failures}/{MAX_FAILURES} failures)", file=sys.stderr)
        except Exception as e:
            failures += 1
            print(f"[graph-manager] S2 citations failed ({failures}/{MAX_FAILURES}): {e}", file=sys.stderr)

    if failures >= MAX_FAILURES:
        print(f"[graph-manager] Citation search hit {MAX_FAILURES} failures, skipping further attempts", file=sys.stderr)

    return citations


def expand_as_seed(graph: GraphData, paper: Paper, graph_path: str,
                   pre_parsed_refs: list = None) -> dict:
    """Expand a paper as seed: fetch references + citations, add to graph, persist.

    Args:
        pre_parsed_refs: If provided (e.g. from PDF upload), skip re-fetching references.

    Returns a summary dict with counts of added nodes/edges.
    """
    # --- Mark as seed & reconcile with existing node ---
    paper.is_seed = True
    if paper.id not in graph.seed_papers:
        graph.seed_papers.append(paper.id)

    existing = find_existing(graph, paper)
    if existing:
        existing.is_seed = True
        if existing.id not in graph.seed_papers:
            graph.seed_papers.append(existing.id)
        paper = existing
    elif paper.id not in {n.id for n in graph.nodes}:
        graph.nodes.append(paper)

    # Progress callback (used by server SSE)
    try:
        from services.graph_server import set_progress
    except ImportError:
        def set_progress(*a, **kw): pass

    # Skip if already expanded
    if paper.refs_expanded and paper.cites_expanded:
        print(f"[graph-manager] {paper.id} already expanded, skipping", file=sys.stderr)
        return {
            "status": "already_expanded",
            "paper_id": paper.id,
            "paper_title": paper.title,
            "new_nodes": 0, "new_edges": 0,
            "total_nodes": len(graph.nodes),
            "total_edges": len(graph.edges),
        }

    nodes_before = len(graph.nodes)
    edges_before = len(graph.edges)
    ids_before = {n.id for n in graph.nodes}

    # --- Fetch references (paper cites these) ---
    if pre_parsed_refs is not None:
        refs = pre_parsed_refs
        set_progress("refs", f"Using {len(refs)} pre-parsed PDF references...", 20)
        print(f"[graph-manager] Using {len(refs)} pre-parsed refs for {paper.title[:50]}", file=sys.stderr)
    else:
        set_progress("refs", "Downloading PDF and extracting references...", 10)
        refs = _get_seed_references(paper)
    set_progress("refs", f"Adding {len(refs)} references to graph...", 40)
    for ref in refs:
        existing_ref = find_existing(graph, ref)
        if existing_ref:
            actual_id = existing_ref.id
            _merge_metadata(existing_ref, ref)
        else:
            actual_id = ref.id
            if ref.id not in {n.id for n in graph.nodes}:
                graph.nodes.append(ref)
        graph.add_edge(paper.id, actual_id, "cites")
    paper.refs_expanded = True
    set_progress("cites", "Searching Google Scholar for citations...", 60)

    # --- Fetch citations (these cite paper) ---
    cites = _get_seed_citations(paper)
    for cite in cites:
        if not cite.id:
            continue
        existing_cite = find_existing(graph, cite)
        if existing_cite:
            actual_id = existing_cite.id
            _merge_metadata(existing_cite, cite)
        else:
            actual_id = cite.id
            if cite.id not in {n.id for n in graph.nodes}:
                graph.nodes.append(cite)
        graph.add_edge(actual_id, paper.id, "cites")
    paper.cites_expanded = True

    set_progress("cites", f"Added {len(cites)} citations. Checking cross-seed edges...", 80)

    # --- Check new papers against existing seeds (fast, no API calls) ---
    # Use the reference data we already have to find cross-seed edges
    newly_added_ids = {n.id for n in graph.nodes} - ids_before
    if newly_added_ids:
        # refs already fetched contain seed papers' IDs — check if any new paper
        # matches a reference of an existing seed (by comparing node IDs in edges)
        seed_ids = set(graph.seed_papers)
        cross_edges = 0
        for new_id in newly_added_ids:
            # Check if this new paper is referenced by any seed (already handled above)
            # Check if this new paper references any seed (from its own refs if available)
            for seed_id in seed_ids:
                if seed_id == new_id:
                    continue
                # If seed's references include this new paper, edge already exists
                # If new paper's title matches a known reference of another seed, add edge
                new_node = graph.find_node(new_id)
                seed_node = graph.find_node(seed_id)
                if new_node and seed_node:
                    # Check by examining existing refs data from PDF parse
                    for ref in refs:
                        if find_existing(graph, ref) and find_existing(graph, ref).id == seed_id:
                            if graph.add_edge(paper.id, seed_id, "cites"):
                                cross_edges += 1
                    for cite in cites:
                        if cite.id and find_existing(graph, cite) and find_existing(graph, cite).id == new_id:
                            if graph.add_edge(new_id, paper.id, "cites"):
                                cross_edges += 1
        if cross_edges:
            print(f"[graph-manager] Cross-seed edges from existing data: +{cross_edges}", file=sys.stderr)

    # --- Dedup edges & persist ---
    set_progress("save", "Saving graph...", 90)
    graph.edges = _dedup_edges(graph.edges)
    save_graph(graph, graph_path)

    # --- Auto-enrich papers missing metadata (authors, year, abstract) ---
    set_progress("enrich", "Enriching incomplete paper metadata...", 93)
    try:
        enriched = enrich_incomplete_papers(graph, graph_path)
        if enriched:
            set_progress("enrich", f"Enriched {enriched} papers with missing metadata", 98)
    except Exception as e:
        print(f"[graph-manager] Auto-enrich failed (non-fatal): {e}", file=sys.stderr)

    new_nodes = len(graph.nodes) - nodes_before
    new_edges = len(graph.edges) - edges_before
    set_progress("done", f"Done! +{new_nodes} papers, +{new_edges} edges", 100, done=True)

    return {
        "status": "ok",
        "paper_id": paper.id,
        "paper_title": paper.title,
        "new_nodes": new_nodes,
        "new_edges": new_edges,
        "total_nodes": len(graph.nodes),
        "total_edges": len(graph.edges),
    }


def _is_same_paper(a: Paper, b: Paper) -> bool:
    """Check if two Paper objects represent the same paper."""
    if a.doi and b.doi and a.doi.lower().strip() == b.doi.lower().strip():
        return True
    if a.arxiv_id and b.arxiv_id and a.arxiv_id.strip() == b.arxiv_id.strip():
        return True
    if a.title and b.title and _title_similarity(a.title, b.title) >= 0.85:
        if a.year and b.year:
            return abs(a.year - b.year) <= 1
        return True
    return False


def _quick_get_paper_refs_titles(paper: Paper) -> list:
    """Quickly get raw reference titles from a paper's PDF (no resolve, no API).

    Returns list of RawReference objects with title/doi/arxiv_id fields.
    Falls back to empty list on any failure.
    """
    try:
        from services.paper_downloader import download_pdf
        pdf_path = download_pdf(paper)
        if not pdf_path:
            return []
    except Exception as e:
        print(f"[add-non-seed] PDF download failed for quick ref check: {e}", file=sys.stderr)
        return []

    try:
        import fitz
        doc = fitz.open(pdf_path)
        text = "".join(page.get_text() for page in doc)
        doc.close()

        from services.pdf_parser import _extract_via_regex
        raw_refs = _extract_via_regex(text)
        print(f"[add-non-seed] Quick PDF ref extraction: {len(raw_refs)} raw refs", file=sys.stderr)
        return raw_refs
    except Exception as e:
        print(f"[add-non-seed] Quick PDF ref extraction failed: {e}", file=sys.stderr)
        return []


def add_non_seed(graph: GraphData, paper: Paper, graph_path: str,
                  pre_parsed_refs: list = None) -> dict:
    """Add a paper as non-seed with bidirectional relationship check against all seeds.

    Direction A (new_paper → seed): Does new paper cite any seed?
      A1: Try quick PDF download + raw ref title matching against seeds
      A2: Fallback — check existing graph edges where X→seed, X matches new paper

    Direction B (seed → new_paper): Does any seed cite new paper?
      Check existing graph edges where seed→X, X matches new paper
    """
    existing = find_existing(graph, paper)
    if existing:
        return {
            "status": "exists",
            "paper_id": existing.id,
            "paper_title": existing.title,
            "message": "Paper already exists in graph",
        }

    paper.is_seed = False
    graph.nodes.append(paper)

    new_edges = 0
    seed_ids = set(graph.seed_papers)
    if not seed_ids:
        save_graph(graph, graph_path)
        return {
            "status": "ok", "paper_id": paper.id, "paper_title": paper.title,
            "new_nodes": 1, "new_edges": 0,
            "total_nodes": len(graph.nodes), "total_edges": len(graph.edges),
        }

    # Build seed Paper lookup for _is_same_paper checks
    seed_nodes = {s: graph.find_node(s) for s in seed_ids}

    # ──────────────────────────────────────────────
    # Direction A: Does new paper cite any seed?
    # ──────────────────────────────────────────────
    a_found_seeds = set()  # seed IDs confirmed cited by new paper

    # A1: Use pre_parsed_refs (PDF upload) or quick PDF download
    raw_refs = pre_parsed_refs
    if not raw_refs:
        # Try quick PDF download + raw extraction (no resolve needed)
        raw_refs_raw = _quick_get_paper_refs_titles(paper)
        if raw_refs_raw:
            # Convert RawReference to mini Paper for _is_same_paper matching
            raw_refs = []
            for r in raw_refs_raw:
                raw_refs.append(Paper(
                    id=r.doi or r.arxiv_id or r.title or "",
                    title=r.title or "",
                    authors=r.authors if isinstance(r.authors, list) else [],
                    year=r.year,
                    citation_count=0,
                    doi=r.doi,
                    arxiv_id=r.arxiv_id,
                    resolved=False,
                ))

    if raw_refs:
        for ref in raw_refs:
            ref_paper = ref if isinstance(ref, Paper) else None
            if ref_paper is None:
                continue
            for sid, snode in seed_nodes.items():
                if sid in a_found_seeds:
                    continue
                if snode and _is_same_paper(ref_paper, snode):
                    if graph.add_edge(paper.id, sid, "cites"):
                        new_edges += 1
                        print(f"[add-non-seed] New paper cites seed {sid} (A1: ref match)", file=sys.stderr)
                    a_found_seeds.add(sid)

    # A2: Fallback for seeds not found in A1 — check graph edges where X→seed
    remaining_seeds = seed_ids - a_found_seeds
    if remaining_seeds:
        for e in graph.edges:
            if e["target"] in remaining_seeds and e["source"] != paper.id:
                source_node = graph.find_node(e["source"])
                if source_node and _is_same_paper(source_node, paper):
                    sid = e["target"]
                    if graph.add_edge(paper.id, sid, "cites"):
                        new_edges += 1
                        print(f"[add-non-seed] New paper cites seed {sid} (A2: edge match)", file=sys.stderr)
                    remaining_seeds.discard(sid)
                    if not remaining_seeds:
                        break

    # ──────────────────────────────────────────────
    # Direction B: Does any seed cite new paper?
    # ──────────────────────────────────────────────
    # B1: Check existing graph edges (seed→X, X matches new paper)
    b_found_seeds = set()
    for e in graph.edges:
        if e["source"] in seed_ids and e["target"] != paper.id:
            target_node = graph.find_node(e["target"])
            if target_node and _is_same_paper(target_node, paper):
                sid = e["source"]
                if graph.add_edge(sid, paper.id, "cites"):
                    new_edges += 1
                    print(f"[add-non-seed] Seed {sid} cites new paper (B1: edge match)", file=sys.stderr)
                b_found_seeds.add(sid)

    # B2: For seeds not found in B1, download seed's PDF and check raw refs
    # This catches cases where seed's references were incompletely extracted during graph build
    b_remaining = seed_ids - b_found_seeds
    if b_remaining:
        for sid in b_remaining:
            snode = seed_nodes.get(sid)
            if not snode:
                continue
            try:
                seed_raw_refs = _quick_get_paper_refs_titles(snode)
                if seed_raw_refs:
                    for r in seed_raw_refs:
                        ref_paper = Paper(
                            id=r.doi or r.arxiv_id or r.title or "",
                            title=r.title or "",
                            authors=r.authors if isinstance(r.authors, list) else [],
                            year=r.year,
                            citation_count=0,
                            doi=r.doi,
                            arxiv_id=r.arxiv_id,
                            resolved=False,
                        )
                        if _is_same_paper(ref_paper, paper):
                            if graph.add_edge(sid, paper.id, "cites"):
                                new_edges += 1
                                print(f"[add-non-seed] Seed {sid} cites new paper (B2: seed PDF ref match)", file=sys.stderr)
                            break
            except Exception as e:
                print(f"[add-non-seed] B2 seed PDF check failed for {sid}: {e}", file=sys.stderr)

    graph.edges = _dedup_edges(graph.edges)
    save_graph(graph, graph_path)

    return {
        "status": "ok",
        "paper_id": paper.id,
        "paper_title": paper.title,
        "new_nodes": 1,
        "new_edges": new_edges,
        "total_nodes": len(graph.nodes),
        "total_edges": len(graph.edges),
    }


def convert_to_seed(graph: GraphData, paper_id: str, graph_path: str) -> dict:
    """Convert an existing non-seed node to seed and expand it."""
    paper = None
    for node in graph.nodes:
        if node.id == paper_id:
            paper = node
            break

    if not paper:
        return {"status": "error", "message": f"Paper {paper_id} not found in graph"}

    if paper.is_seed:
        return {"status": "exists", "message": f"Paper is already a seed", "paper_id": paper.id}

    return expand_as_seed(graph, paper, graph_path)


def enrich_metadata(graph: GraphData, graph_path: str) -> dict:
    """Fill missing year/authors/abstract for papers using S2 batch API.

    Uses S2 POST /paper/batch endpoint (up to 500 IDs per request) for
    papers with S2 hex IDs, and individual lookups for arXiv/DOI IDs.
    """
    import time
    import httpx

    S2_BASE = "https://api.semanticscholar.org/graph/v1"
    FIELDS = "paperId,title,authors,year,citationCount,abstract,url,externalIds"

    def _s2_headers():
        import os
        h = {}
        key = os.environ.get("S2_API_KEY", "")
        if key:
            h["x-api-key"] = key
        return h

    # Find papers needing enrichment
    to_enrich = []
    for node in graph.nodes:
        if not node.year or not node.authors or not node.abstract:
            to_enrich.append(node)

    if not to_enrich:
        print("[enrich] All papers have metadata, nothing to do", file=sys.stderr)
        return {"enriched": 0, "total": len(graph.nodes)}

    print(f"[enrich] {len(to_enrich)} papers need metadata enrichment", file=sys.stderr)

    # Separate by ID type
    s2_hex_nodes = []  # Can use batch API
    other_nodes = []   # Need individual lookup
    for node in to_enrich:
        pid = node.id
        if pid.startswith("ARXIV:") or pid.startswith("DOI:") or pid.startswith("crossref:") or pid.startswith("openalex:"):
            other_nodes.append(node)
        elif pid.startswith("pdf:") or pid.startswith("unresolved:"):
            continue  # Skip synthetic IDs
        else:
            s2_hex_nodes.append(node)

    enriched_count = 0

    # Batch API for S2 hex IDs (up to 500 per request)
    BATCH_SIZE = 100
    for i in range(0, len(s2_hex_nodes), BATCH_SIZE):
        batch = s2_hex_nodes[i:i + BATCH_SIZE]
        ids = [n.id for n in batch]
        print(f"[enrich] Batch {i // BATCH_SIZE + 1}: {len(ids)} papers via S2 batch API",
              file=sys.stderr)
        try:
            with httpx.Client() as client:
                resp = client.post(
                    f"{S2_BASE}/paper/batch",
                    json={"ids": ids},
                    params={"fields": FIELDS},
                    headers=_s2_headers(),
                    timeout=30,
                )
                if resp.status_code == 429:
                    print("[enrich] Rate limited, waiting 5s...", file=sys.stderr)
                    time.sleep(5)
                    resp = client.post(
                        f"{S2_BASE}/paper/batch",
                        json={"ids": ids},
                        params={"fields": FIELDS},
                        headers=_s2_headers(),
                        timeout=30,
                    )
                resp.raise_for_status()
                results = resp.json()

            for node, data in zip(batch, results):
                if not data:
                    continue
                if not node.year and data.get("year"):
                    node.year = data["year"]
                if not node.authors and data.get("authors"):
                    node.authors = [a.get("name", "") for a in data["authors"]]
                if not node.abstract and data.get("abstract"):
                    node.abstract = data["abstract"]
                if not node.doi:
                    ext = data.get("externalIds") or {}
                    if ext.get("DOI"):
                        node.doi = ext["DOI"]
                    if ext.get("ArXiv"):
                        node.arxiv_id = ext["ArXiv"]
                if not node.url and data.get("url"):
                    node.url = data["url"]
                if data.get("citationCount") and (data["citationCount"] > (node.citation_count or 0)):
                    node.citation_count = data["citationCount"]
                enriched_count += 1

        except Exception as e:
            print(f"[enrich] Batch failed: {e}", file=sys.stderr)

        # Rate limit courtesy
        if i + BATCH_SIZE < len(s2_hex_nodes):
            time.sleep(1)

    # Individual lookups for ARXIV:/DOI: IDs
    for node in other_nodes:
        pid = node.id
        lookup_id = pid
        if pid.startswith("crossref:"):
            lookup_id = f"DOI:{pid[len('crossref:'):]}"
        elif pid.startswith("openalex:"):
            continue  # S2 can't look up OpenAlex IDs

        print(f"[enrich] Individual lookup: {lookup_id[:50]}", file=sys.stderr)
        try:
            with httpx.Client() as client:
                resp = client.get(
                    f"{S2_BASE}/paper/{lookup_id}",
                    params={"fields": FIELDS},
                    headers=_s2_headers(),
                    timeout=15,
                )
                if resp.status_code == 429:
                    time.sleep(3)
                    resp = client.get(
                        f"{S2_BASE}/paper/{lookup_id}",
                        params={"fields": FIELDS},
                        headers=_s2_headers(),
                        timeout=15,
                    )
                if resp.status_code == 404:
                    continue
                resp.raise_for_status()
                data = resp.json()

            if not node.year and data.get("year"):
                node.year = data["year"]
            if not node.authors and data.get("authors"):
                node.authors = [a.get("name", "") for a in data["authors"]]
            if not node.abstract and data.get("abstract"):
                node.abstract = data["abstract"]
            if not node.url and data.get("url"):
                node.url = data["url"]
            if data.get("citationCount") and (data["citationCount"] > (node.citation_count or 0)):
                node.citation_count = data["citationCount"]
            enriched_count += 1
            time.sleep(0.5)

        except Exception as e:
            print(f"[enrich] Failed for {lookup_id}: {e}", file=sys.stderr)

    save_graph(graph, graph_path)
    print(f"[enrich] Done: enriched {enriched_count}/{len(to_enrich)} papers", file=sys.stderr)
    return {"enriched": enriched_count, "total": len(graph.nodes)}
