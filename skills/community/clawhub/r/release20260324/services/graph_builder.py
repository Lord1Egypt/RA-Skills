"""Build citation networks from seed papers or PDFs (sync)."""
import sys
from typing import List

from schemas import Paper, GraphData
from services import semantic_scholar as s2


def build_graph_from_pdfs(
    pdf_paths: List[str],
    depth: int = 0,
    include_unresolved: bool = False,
    use_grobid: bool = False,
) -> GraphData:
    """Build a citation graph from PDF reference lists.

    1. Extract references from each PDF
    2. Resolve via multi-source (S2 + CrossRef + OpenAlex)
    3. Create edges: seed_paper → each resolved reference
    4. Optionally include unresolved references as nodes
    5. Optionally expand resolved papers one more depth level via S2
    """
    from services.pdf_parser import parse_pdf

    nodes: dict = {}
    edges = []
    seed_ids = []
    unresolved_count = 0

    for pdf_path in pdf_paths:
        print(f"[graph-pdf] Processing: {pdf_path}", file=sys.stderr)
        result = parse_pdf(pdf_path, use_grobid=use_grobid)

        resolved_papers = [Paper(**p) for p in result["resolved_papers"]]
        unresolved_refs = result.get("unresolved_references", [])

        # Try to identify the PDF paper itself in S2
        # Use the first few words of the PDF as a search query
        seed_paper = _identify_pdf_paper(pdf_path, result.get("text_length", 0))
        if seed_paper:
            seed_paper.is_seed = True
            nodes[seed_paper.id] = seed_paper
            seed_ids.append(seed_paper.id)
            seed_id = seed_paper.id
        else:
            # Create a synthetic seed node from filename
            import os
            fname = os.path.basename(pdf_path).replace(".pdf", "")
            seed_id = f"pdf:{fname}"
            synthetic = Paper(
                id=seed_id, title=f"[PDF] {fname}",
                is_seed=True, resolved=False, source="pdf_upload",
            )
            nodes[seed_id] = synthetic
            seed_ids.append(seed_id)

        # Add resolved references as nodes + edges
        for paper in resolved_papers:
            if paper.id not in nodes:
                nodes[paper.id] = paper
            edges.append({"source": seed_id, "target": paper.id, "type": "cites"})

        # Add unresolved references as nodes if requested
        if include_unresolved:
            for i, uref in enumerate(unresolved_refs):
                uid = f"unresolved:{seed_id}:{i}"
                title = uref.get("title") or uref.get("raw_text", "Unknown")[:80]
                unresolved_node = Paper(
                    id=uid,
                    title=title,
                    authors=uref.get("authors", []),
                    year=uref.get("year"),
                    resolved=False,
                    source="pdf_extraction",
                )
                nodes[uid] = unresolved_node
                edges.append({"source": seed_id, "target": uid, "type": "cites"})
                unresolved_count += 1

        print(f"[graph-pdf] {len(resolved_papers)} resolved, "
              f"{len(unresolved_refs)} unresolved from {pdf_path}", file=sys.stderr)

    # Optional depth expansion: for resolved papers, fetch their S2 references
    if depth >= 1:
        resolved_nodes = [n for n in nodes.values() if n.resolved and not n.is_seed
                          and n.source == "semantic_scholar" and n.citation_count > 0]
        # Sort by citation count, expand top N
        top_expand = sorted(resolved_nodes, key=lambda n: n.citation_count, reverse=True)[:15]
        for n in top_expand:
            print(f"[graph-pdf] Expanding: {n.title[:40]}...", file=sys.stderr)
            try:
                refs = s2.get_references(n.id, limit=20)
            except Exception:
                continue
            for ref in refs:
                if ref.id and ref.id not in nodes:
                    nodes[ref.id] = ref
                if ref.id:
                    edges.append({"source": n.id, "target": ref.id, "type": "cites"})

    # Deduplicate edges
    seen = set()
    unique_edges = []
    for e in edges:
        key = (e["source"], e["target"])
        if key not in seen:
            seen.add(key)
            unique_edges.append(e)

    graph = GraphData(
        nodes=list(nodes.values()),
        edges=unique_edges,
        seed_papers=seed_ids,
        depth=depth,
        total_papers=len(nodes),
    )
    print(f"[graph-pdf] Final graph: {graph.total_papers} papers, "
          f"{len(unique_edges)} edges ({unresolved_count} unresolved nodes)", file=sys.stderr)
    return graph


def _identify_pdf_paper(pdf_path: str, text_length: int) -> "Paper | None":
    """Try to identify the PDF paper itself.

    Priority:
      1. Extract title from PDF text → search arXiv
      2. Extract title from PDF text → search S2
      3. If all APIs fail, build Paper from PDF text directly (no API needed)
    """
    try:
        import fitz
        doc = fitz.open(pdf_path)
        first_page = doc[0].get_text() if doc.page_count > 0 else ""

        # Also try to get title from largest font on first page
        title_from_font = _extract_title_by_font(doc)
        doc.close()

        lines = [l.strip() for l in first_page.split("\n") if l.strip() and len(l.strip()) > 10]
        if not lines and not title_from_font:
            return None

        from services.reference_resolver import _title_similarity

        # Build candidate titles: font-based title first, then first 3 text lines
        candidates = []
        if title_from_font:
            candidates.append(title_from_font)
        for line in lines[:3]:
            candidate = line.strip()
            if 10 <= len(candidate) <= 200 and candidate != title_from_font:
                candidates.append(candidate)

        # Try API search for each candidate
        for candidate in candidates:
            # 1. Search arXiv first
            try:
                from services import arxiv
                import re as _re
                clean = _re.sub(r'[:\-,;/()]+', ' ', candidate).strip()
                clean = _re.sub(r'\s+', ' ', clean)
                if ':' in candidate:
                    short = candidate.split(':')[0].strip()
                else:
                    short = ' '.join(clean.split()[:8])
                _, papers = arxiv.search(short, limit=5)
                for p in papers:
                    if _title_similarity(candidate, p.title) >= 0.65:
                        return p
            except Exception:
                pass

            # 2. Fallback: S2 direct search (single attempt, no retry on 429)
            try:
                from services.semantic_scholar import _s2_search
                total, papers = _s2_search(candidate, limit=3, max_retries=1)
                for p in papers:
                    if _title_similarity(candidate, p.title) >= 0.7:
                        return p
            except Exception as e:
                err_str = str(e).lower()
                if "429" in err_str or "rate" in err_str:
                    print(f"[identify] S2 rate limited, skipping to PDF fallback", file=sys.stderr)
                    break  # Skip remaining candidates, go straight to PDF fallback

        # 3. All APIs failed — build Paper from PDF text directly
        best_title = title_from_font or (candidates[0] if candidates else None)
        if best_title:
            authors, year = _extract_authors_year_from_text(first_page)

            # Extract arXiv ID from PDF text
            import re as _re2
            arxiv_id = None
            arxiv_match = _re2.search(r'arXiv:\s*(\d{4}\.\d{4,5}(?:v\d+)?)', first_page)
            if arxiv_match:
                arxiv_id = arxiv_match.group(1).split('v')[0]  # Strip version

            import hashlib
            if arxiv_id:
                pid = f"ARXIV:{arxiv_id}"
            else:
                pid = "pdf:" + hashlib.md5(best_title.encode()).hexdigest()[:12]

            print(f"[identify] APIs unavailable, using PDF-extracted title: {best_title} (year={year}, authors={len(authors)}, arxiv={arxiv_id})", file=sys.stderr)
            return Paper(
                id=pid,
                title=best_title,
                authors=authors,
                year=year,
                arxiv_id=arxiv_id,
                is_seed=False,
                resolved=False,
                source="pdf_extraction",
            )
    except Exception as e:
        print(f"[identify] Error: {e}", file=sys.stderr)
    return None


def _extract_title_by_font(doc) -> "str | None":
    """Extract title by finding the largest font text on the first page."""
    import re
    try:
        page = doc[0]
        blocks = page.get_text("dict")["blocks"]
        max_size = 0
        title_spans = []

        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    size = span["size"]
                    text = span["text"].strip()
                    if not text or len(text) < 3:
                        continue
                    if size > max_size:
                        max_size = size
                        title_spans = [text]
                    elif abs(size - max_size) < 0.5:
                        title_spans.append(text)

        if title_spans and max_size > 12:  # Title is usually > 12pt
            title = " ".join(title_spans).strip()
            # Filter out arXiv headers, page numbers, etc.
            if (10 <= len(title) <= 300
                and not title.startswith("arXiv:")
                and not title.startswith("http")
                and not re.match(r'^\d+$', title)):
                return title
    except Exception:
        pass
    return None


def _extract_authors_year_from_text(first_page_text: str):
    """Extract authors and year from first page text heuristically.

    Falls back to LLM extraction if regex fails.
    """
    import re
    authors = []
    year = None

    lines = [l.strip() for l in first_page_text.split("\n") if l.strip()]

    # Find year from multiple patterns
    full_text = first_page_text

    # Pattern 1: Explicit date like "12 Mar 2026" or "March 2026"
    m = re.search(r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+((?:19|20)\d{2})\b', full_text)
    if m:
        year = int(m.group(1))

    # Pattern 2: arXiv ID like "arXiv:2603.11853" → year = 2000 + first 2 digits
    if not year:
        m = re.search(r'arXiv:\s*(\d{2})(\d{2})\.\d+', full_text)
        if m:
            year = 2000 + int(m.group(1))

    # Pattern 3: Generic 4-digit year in first 40 lines
    if not year:
        for line in lines[:40]:
            m = re.search(r'\b(19|20)\d{2}\b', line)
            if m:
                y = int(m.group())
                if 1950 <= y <= 2030:
                    year = y
                    break

    # Find authors: lines after title, before abstract
    # Strategy 1: lines with commas or "and" (multi-author on one line)
    for i, line in enumerate(lines[1:12], 1):
        if '@' in line or 'abstract' in line.lower():
            break
        if 'university' in line.lower() or 'department' in line.lower() or 'institute' in line.lower():
            continue
        if ',' in line or ' and ' in line.lower():
            parts = re.split(r',|\band\b', line)
            names = [p.strip() for p in parts if p.strip() and len(p.strip()) > 2
                     and not any(c.isdigit() for c in p) and len(p.strip()) < 40]
            if 1 <= len(names) <= 20:
                authors = names
                break

    # Strategy 2: consecutive lines of single names (one author per line)
    if not authors:
        name_pattern = re.compile(r'^[A-Z][a-z]+ [A-Z][a-z]+')
        consecutive_names = []
        for i, line in enumerate(lines[1:15], 1):
            if 'abstract' in line.lower():
                break
            if name_pattern.match(line) and len(line) < 50 and '@' not in line:
                consecutive_names.append(line.strip())
            elif consecutive_names:
                break  # End of name block
        if len(consecutive_names) >= 2:
            authors = consecutive_names

    # Strategy 3: arXiv API lookup (one attempt, skip if rate limited)
    if not authors:
        arxiv_id_match = re.search(r'arXiv:\s*(\d{4}\.\d{4,5})', first_page_text)
        if arxiv_id_match:
            try:
                from services import arxiv as arxiv_mod
                _, papers = arxiv_mod.search(arxiv_id_match.group(1), limit=1)
                if papers and papers[0].authors:
                    authors = papers[0].authors
                    if not year and papers[0].year:
                        year = papers[0].year
                    print(f"[identify] arXiv API: got {len(authors)} authors", file=sys.stderr)
            except Exception as e:
                print(f"[identify] arXiv API failed (skipping): {e}", file=sys.stderr)

    # Strategy 4: S2 API lookup (one attempt, skip if 429)
    if not authors:
        title_for_search = None
        for line in lines[:5]:
            if len(line) > 15:
                title_for_search = line
                break
        if title_for_search:
            try:
                from services import semantic_scholar as s2
                _, papers = s2.search(title_for_search, limit=1)
                if papers and papers[0].authors:
                    authors = papers[0].authors
                    if not year and papers[0].year:
                        year = papers[0].year
                    print(f"[identify] S2 API: got {len(authors)} authors", file=sys.stderr)
            except Exception as e:
                err_str = str(e).lower()
                if "429" in err_str or "rate" in err_str:
                    print(f"[identify] S2 rate limited (skipping)", file=sys.stderr)
                else:
                    print(f"[identify] S2 failed (skipping): {e}", file=sys.stderr)

    # Strategy 5: LLM fallback for both authors and year
    if not authors or not year:
        llm_authors, llm_year = _llm_extract_metadata(first_page_text[:3000])
        if not authors and llm_authors:
            authors = llm_authors
        if not year and llm_year:
            year = llm_year

    return authors, year


def _llm_extract_metadata(first_page_text: str):
    """Use LLM to extract authors and year from first page text."""
    try:
        from services.llm_client import is_llm_available, llm_chat
        if not is_llm_available():
            return [], None
    except ImportError:
        return [], None

    prompt = f"""Extract the authors and publication year from this academic paper's first page.

Return ONLY a JSON object, no markdown, no explanation:
{{"authors": ["Author Name 1", "Author Name 2"], "year": 2024}}

If you cannot determine authors or year, use empty list or null.

Text:
{first_page_text}"""

    try:
        import json as _json
        response = llm_chat(prompt, max_tokens=500, temperature=0.1)
        if not response:
            return [], None
        response = response.strip()
        if response.startswith("```"):
            response = response.split("\n", 1)[1] if "\n" in response else response
            response = response.rsplit("```", 1)[0] if "```" in response else response
            response = response.strip()
        data = _json.loads(response)
        authors = data.get("authors", [])
        year = data.get("year")
        if isinstance(year, str) and year.isdigit():
            year = int(year)
        if authors:
            print(f"[identify] LLM extracted {len(authors)} authors, year={year}", file=sys.stderr)
        return authors, year
    except Exception as e:
        print(f"[identify] LLM metadata extraction failed: {e}", file=sys.stderr)
        return [], None


def build_graph(seed_ids: List[str], depth: int = 1) -> GraphData:
    nodes: dict = {}
    edges = []
    seed_set = set(seed_ids)

    for pid in seed_ids:
        print(f"[graph] Fetching seed: {pid}", file=sys.stderr)
        result = None
        try:
            result = s2.get_paper(pid)
        except Exception as e:
            print(f"[graph] get_paper failed for {pid}: {e}", file=sys.stderr)

        if result:
            paper = result["paper"]
            paper.is_seed = True
            nodes[paper.id] = paper

            for ref in result["references"]:
                if ref.id and ref.id not in nodes:
                    ref.is_seed = ref.id in seed_set
                    nodes[ref.id] = ref
                if ref.id:
                    edges.append({"source": paper.id, "target": ref.id, "type": "cites"})

            for cite in result["citations"][:50]:
                if cite.id and cite.id not in nodes:
                    cite.is_seed = cite.id in seed_set
                    nodes[cite.id] = cite
                if cite.id:
                    edges.append({"source": cite.id, "target": paper.id, "type": "cites"})
        else:
            # Fallback: try arXiv search by title or ID
            print(f"[graph] Attempting arXiv fallback for {pid}", file=sys.stderr)
            paper = None
            from services import arxiv as arxiv_svc

            if pid.startswith("ARXIV:"):
                try:
                    paper = arxiv_svc.get_by_id(pid)
                    print(f"[graph] arXiv fallback (ID) got: {paper.title}", file=sys.stderr)
                except Exception as e2:
                    print(f"[graph] arXiv fallback (ID) failed: {e2}", file=sys.stderr)

            if not paper:
                # Search arXiv by title — use short query
                try:
                    import re as _re
                    from services.reference_resolver import _title_similarity
                    if ':' in pid:
                        short_q = pid.split(':')[0].strip()
                    else:
                        short_q = ' '.join(pid.split()[:8])
                    short_q = _re.sub(r'[:\-,;/()]+', ' ', short_q).strip()
                    short_q = _re.sub(r'\s+', ' ', short_q)
                    _, arxiv_results = arxiv_svc.search(short_q, limit=10)
                    for ap in arxiv_results:
                        if _title_similarity(pid, ap.title) >= 0.6:
                            paper = ap
                            print(f"[graph] arXiv fallback (search) got: {paper.title}", file=sys.stderr)
                            break
                except Exception as e3:
                    print(f"[graph] arXiv search fallback failed: {e3}", file=sys.stderr)

            if not paper:
                print(f"[graph] Skipping seed {pid} — all sources failed", file=sys.stderr)
                continue

            paper.is_seed = True
            nodes[paper.id] = paper

            # Get refs via PDF download + parse (arXiv papers have PDF)
            try:
                from services.paper_downloader import download_pdf
                from services.pdf_parser import parse_pdf as parse_pdf_refs
                pdf_path = download_pdf(paper)
                if pdf_path:
                    result = parse_pdf_refs(pdf_path)
                    resolved = result.get("resolved_papers", [])
                    refs = [Paper(**p) for p in resolved]
                    print(f"[graph] PDF refs: {len(refs)} from {paper.title[:40]}", file=sys.stderr)
                    for ref in refs:
                        if ref.id and ref.id not in nodes:
                            ref.is_seed = ref.id in seed_set
                            nodes[ref.id] = ref
                        if ref.id:
                            edges.append({"source": paper.id, "target": ref.id, "type": "cites"})
                else:
                    print(f"[graph] No PDF available for {paper.title[:40]}", file=sys.stderr)
            except Exception as e3:
                print(f"[graph] PDF refs failed for {paper.title[:40]}: {e3}", file=sys.stderr)

            # Fallback: S2 refs (may rate limit)
            if not any(e["source"] == paper.id for e in edges):
                try:
                    refs = s2.get_references(paper.id, limit=100)
                    for ref in refs:
                        if ref.id and ref.id not in nodes:
                            ref.is_seed = ref.id in seed_set
                            nodes[ref.id] = ref
                        if ref.id:
                            edges.append({"source": paper.id, "target": ref.id, "type": "cites"})
                except Exception as e3b:
                    print(f"[graph] S2 refs fallback also failed: {e3b}", file=sys.stderr)

            # Get cites via Google Scholar (uses title, no S2 needed)
            try:
                from services import google_scholar as gs
                gs_cites = gs.get_citations(paper.title, limit=50)
                print(f"[graph] GS citations: {len(gs_cites)} for {paper.title[:40]}", file=sys.stderr)
                for cite in gs_cites:
                    if cite.id and cite.id not in nodes:
                        cite.is_seed = cite.id in seed_set
                        nodes[cite.id] = cite
                    if cite.id:
                        edges.append({"source": cite.id, "target": paper.id, "type": "cites"})
            except Exception as e4:
                print(f"[graph] GS cites failed: {e4}", file=sys.stderr)

    if depth > 1:
        non_seed = sorted(
            [n for n in nodes.values() if not n.is_seed and n.citation_count > 0],
            key=lambda n: n.citation_count, reverse=True
        )[:10]
        for n in non_seed:
            print(f"[graph] Expanding: {n.title[:40]}...", file=sys.stderr)
            try:
                refs = s2.get_references(n.id, limit=20)
            except Exception:
                continue
            for ref in refs:
                if ref.id and ref.id not in nodes:
                    nodes[ref.id] = ref
                if ref.id:
                    edges.append({"source": n.id, "target": ref.id, "type": "cites"})

    # Deduplicate edges
    seen = set()
    unique_edges = []
    for e in edges:
        key = (e["source"], e["target"])
        if key not in seen:
            seen.add(key)
            unique_edges.append(e)

    # Use actual resolved node IDs for seed_papers (not input IDs like ARXIV:xxx)
    resolved_seed_ids = [n.id for n in nodes.values() if n.is_seed]

    return GraphData(
        nodes=list(nodes.values()),
        edges=unique_edges,
        seed_papers=resolved_seed_ids,
        depth=depth,
        total_papers=len(nodes),
    )
