#!/usr/bin/env python3
"""
学术论文检索小助手（松哥版）
===========================
支持: OpenAlex, Semantic Scholar, Crossref, arXiv, PubMed

多源检索 + 跨库 enrichment，自动补全论文元数据（摘要/引用数/期刊卷期页）

Author: 松哥 (Zhang JinSong)
License: MIT

使用说明:
  - OpenAlex / Crossref / arXiv / PubMed 无需配置，直接可用
  - Semantic Scholar API Key（可选）：免费申请 https://www.semanticscholar.org/product/api
    有 key 可解除速率限制（约 1 req/s → 更多请求）；无 key 完全可用，仅受速率限制
    配置方式（Linux/Mac）: 在 ~/.bashrc 中加入: export S2_API_KEY='your-key'
    配置方式（Windows）: setx S2_API_KEY "your-key"（需重启终端）
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ---------------------------------------------------------------------------
# HTTP Session with automatic retry
# ---------------------------------------------------------------------------
def _create_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

SESSION = _create_session()

def _safe_get(d: Any, *keys, default=None):
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, {})
        else:
            return default
    return d if d != {} else default

# ---------------------------------------------------------------------------
# OpenAlex（无需 API key，200亿+学术记录）
# ---------------------------------------------------------------------------
OPENALEX_BASE = "https://api.openalex.org"

def search_openalex(
    query: str,
    max_results: int = 10,
    year: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    journal_issn: Optional[str] = None,
    concept_id: Optional[str] = None,
    author: Optional[str] = None,
    sort: str = "relevance",
) -> List[Dict[str, Any]]:
    filters = []
    if year:
        filters.append(f"publication_year:{year}")
    if start_date:
        filters.append(f"from_publication_date:{start_date}")
    if end_date:
        filters.append(f"to_publication_date:{end_date}")
    if journal_issn:
        filters.append(f"primary_location.source.issn:{journal_issn}")
    if concept_id:
        filters.append(f"concepts.id:{concept_id}")
    if author:
        filters.append(f"authorships.author.orcid:{author}")

    params = {"search": query, "per_page": min(max_results, 200), "sort": sort}
    if filters:
        params["filter"] = ",".join(filters)

    papers = []
    cursor = "*"
    while cursor and len(papers) < max_results:
        p = {**params, "cursor": cursor}
        try:
            resp = SESSION.get(f"{OPENALEX_BASE}/works", params=p, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"OpenAlex error: {e}", file=sys.stderr)
            break

        for work in data.get("results", []):
            authors = [
                a.get("author", {}).get("display_name")
                for a in work.get("authorships", [])
                if a.get("author", {}).get("display_name")
            ]
            doi = (work.get("doi") or "").replace("https://doi.org/", "")
            abstract = ""
            inv_idx = work.get("abstract_inverted_index")
            if inv_idx:
                try:
                    max_pos = max(max(pos) for pos in inv_idx.values())
                    word_map = {pos: w for w, positions in inv_idx.items() for pos in positions}
                    abstract = " ".join(word_map[i] for i in range(max_pos + 1) if i in word_map)
                except:
                    pass
            if not abstract:
                abstract = work.get("abstract") or ""

            venue = _safe_get(work, "primary_location", "source", "display_name") or ""
            volume = work.get("volume")
            biblio = work.get("biblio", {})
            pages = f"{biblio.get('first_page', '')}-{biblio.get('last_page', '')}".strip("-") or None

            papers.append({
                "title": work.get("title", "No title"),
                "authors": authors,
                "year": work.get("publication_year"),
                "published": str(work.get("publication_year")) if work.get("publication_year") else "",
                "doi": doi,
                "journal": venue,
                "volume": volume,
                "pages": pages,
                "abstract": abstract,
                "citation_count": work.get("cited_by_count", 0),
                "url": f"https://openalex.org/{work['id'].split('/')[-1]}" if work.get("id") else "",
                "pdf_url": _safe_get(work, "primary_location", "pdf_url") or "",
                "source": "openalex",
            })
            if len(papers) >= max_results:
                break
        cursor = data.get("meta", {}).get("next_cursor")
        time.sleep(0.1)
    return papers[:max_results]

# ---------------------------------------------------------------------------
# Semantic Scholar（无需 key，速率限制 1 req/s）
# ---------------------------------------------------------------------------
def _get_s2_client(api_key: Optional[str] = None):
    try:
        from semanticscholar import SemanticScholar
    except ImportError:
        sys.exit("Error: semanticscholar 未安装。运行: pip install semanticscholar")
    return SemanticScholar(api_key=api_key if api_key else None)

def search_semantic_scholar(
    query: str,
    max_results: int = 10,
    year: Optional[int] = None,
    min_citations: Optional[int] = None,
    author: Optional[str] = None,
    api_key: Optional[str] = None,
    enrich: bool = False,
) -> List[Dict[str, Any]]:
    sch = _get_s2_client(api_key)
    papers = []
    try:
        results = sch.search_paper(query, limit=max_results * 2)
        for paper in results:
            if year and paper.year != year:
                continue
            if min_citations and (paper.citationCount or 0) < min_citations:
                continue
            if author and paper.authors:
                if not any(author.lower() in (a.name or "").lower() for a in paper.authors):
                    continue
            papers.append({
                "title": paper.title,
                "authors": [a.name for a in paper.authors] if paper.authors else [],
                "year": paper.year,
                "published": str(paper.year) if paper.year else "",
                "doi": getattr(paper.externalIds, "DOI", "") if hasattr(paper, "externalIds") else "",
                "citation_count": paper.citationCount or 0,
                "paper_id": paper.paperId,
                "abstract": getattr(paper, "abstract", "") or "",
                "url": getattr(paper, "url", "") or f"https://www.semanticscholar.org/paper/{paper.paperId}",
                "source": "semantic",
            })
            if len(papers) >= max_results:
                break
    except Exception as e:
        print(f"Semantic Scholar error: {e}", file=sys.stderr)

    if enrich:
        for p in papers:
            try:
                detail = sch.get_paper(p["paper_id"])
                if detail:
                    p["abstract"] = detail.abstract or p["abstract"]
                    p["citation_count"] = detail.citationCount or p["citation_count"]
                    p["influential_citations"] = getattr(detail, "influentialCitationCount", 0)
                    if detail.fieldsOfStudy:
                        p["fields_of_study"] = [f.name for f in detail.fieldsOfStudy]
                    if detail.openAccessPdf and detail.openAccessPdf.get("url"):
                        p["pdf_url"] = detail.openAccessPdf["url"]
            except:
                pass
            time.sleep(1.0)  # 无 key 限速 1 req/s
    return papers[:max_results]

# ---------------------------------------------------------------------------
# Crossref（补充元数据，无需 key）
# ---------------------------------------------------------------------------
CROSSREF_BASE = "https://api.crossref.org"

def fetch_crossref_metadata(doi_list: List[str]) -> Dict[str, Dict]:
    meta_map = {}
    for i in range(0, len(doi_list), 50):
        chunk = doi_list[i:i+50]
        params = {"filter": f"doi:{','.join(chunk)}", "rows": len(chunk)}
        try:
            resp = SESSION.get(f"{CROSSREF_BASE}/works", params=params, timeout=30)
            resp.raise_for_status()
            for item in resp.json().get("message", {}).get("items", []):
                doi = item.get("DOI", "").lower()
                authors = [f"{a.get('given','')} {a.get('family','')}".strip() for a in item.get("author", [])]
                issued = item.get("issued", {}).get("date-parts", [[None]])[0]
                meta_map[doi] = {
                    "title": _safe_get(item, "title", 0) or "",
                    "authors": [a for a in authors if a],
                    "year": issued[0] if issued else "",
                    "published": str(issued[0]) if issued else "",
                    "journal": _safe_get(item, "container-title", 0) or "",
                    "volume": item.get("volume", ""),
                    "pages": item.get("page", ""),
                    "abstract": item.get("abstract", ""),
                    "doi": doi,
                    "url": f"https://doi.org/{doi}",
                    "source": "crossref",
                }
        except Exception as e:
            print(f"Crossref error: {e}", file=sys.stderr)
        time.sleep(0.1)
    return meta_map

def enrich_with_crossref(papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    dois = [p["doi"].lower() for p in papers if p.get("doi")]
    if not dois:
        return papers
    print(f"→  正在用 Crossref 补充 {len(dois)} 篇论文元数据…", file=sys.stderr)
    meta = fetch_crossref_metadata(dois)
    for p in papers:
        doi = p.get("doi", "").lower()
        if doi in meta:
            m = meta[doi]
            for field in ("pages", "volume", "journal", "abstract", "issue"):
                if not p.get(field) and m.get(field):
                    p[field] = m[field]
    return papers

# ---------------------------------------------------------------------------
# Multi-source pipeline（OpenAlex 搜 → S2 补 → Crossref 补）
# ---------------------------------------------------------------------------
def multi_source_search(
    query: str,
    max_results: int,
    openalex_filter: Dict[str, Any],
    api_key: Optional[str] = None,
    crossref_enrich: bool = True,
) -> List[Dict[str, Any]]:
    print("🔍  Step 1/3: 搜索 OpenAlex…", file=sys.stderr)
    papers = search_openalex(query=query, max_results=max_results, **openalex_filter)
    print(f"✔  找到 {len(papers)} 篇论文。", file=sys.stderr)
    if not papers:
        return []

    print("📊  Step 2/3: 用 Semantic Scholar 补充引用数和摘要…", file=sys.stderr)
    sch = _get_s2_client(api_key)
    for p in papers:
        if not p.get("doi"):
            continue
        try:
            s2_paper = sch.get_paper(f"DOI:{p['doi']}")
            if s2_paper:
                p["citation_count"] = s2_paper.citationCount or p["citation_count"]
                p["influential_citations"] = getattr(s2_paper, "influentialCitationCount", 0)
                if not p.get("abstract") and s2_paper.abstract:
                    p["abstract"] = s2_paper.abstract
                if s2_paper.openAccessPdf and s2_paper.openAccessPdf.get("url"):
                    p["pdf_url"] = s2_paper.openAccessPdf["url"]
                if s2_paper.fieldsOfStudy:
                    p["fields_of_study"] = [f.name for f in s2_paper.fieldsOfStudy]
                p["s2_id"] = s2_paper.paperId
        except:
            pass
        time.sleep(1.0)  # 无 key 限速
    print("✔  Semantic Scholar 补充完成。", file=sys.stderr)

    if crossref_enrich:
        print("📖  Step 3/3: 用 Crossref 补充期刊卷期页信息…", file=sys.stderr)
        papers = enrich_with_crossref(papers)
    return papers

# ---------------------------------------------------------------------------
# Legacy arXiv / PubMed
# ---------------------------------------------------------------------------
try:
    import arxiv
except ImportError:
    arxiv = None

try:
    from Bio import Entrez
except ImportError:
    Entrez = None

def search_arxiv(query, max_results=10, category=None, author=None, year=None,
                 start_date=None, end_date=None, sort_by="relevance"):
    if not arxiv:
        sys.exit("Error: arxiv 未安装。运行: pip install arxiv")
    from datetime import datetime
    q = query
    if category:
        q = f"cat:{category} AND {q}"
    if author:
        q = f"{q} AND au:{author}"
    sort_order = arxiv.SortCriterion.Relevance
    if sort_by == "date":
        sort_order = arxiv.SortCriterion.SubmittedDate
    s = arxiv.Search(query=q, max_results=max_results, sort_by=sort_order)
    results = []
    for p in s.results():
        pub = p.published.date()
        if year and pub.year != year:
            continue
        if start_date and pub < datetime.strptime(start_date, "%Y-%m-%d").date():
            continue
        if end_date and pub > datetime.strptime(end_date, "%Y-%m-%d").date():
            continue
        results.append({
            "title": p.title,
            "authors": [a.name for a in p.authors],
            "year": pub.year,
            "published": p.published.strftime("%Y-%m-%d"),
            "arxiv_id": p.entry_id.split("/")[-1],
            "categories": p.categories,
            "abstract": p.summary,
            "pdf_url": p.pdf_url,
            "doi": p.doi or "",
            "source": "arxiv",
        })
        if len(results) >= max_results:
            break
    return results

def search_pubmed(query, max_results=10, start_date=None, end_date=None,
                  publication_type=None, author=None):
    if not Entrez:
        sys.exit("Error: biopython 未安装。运行: pip install biopython")
    from datetime import datetime
    Entrez.email = "user@example.com"
    q = query
    if publication_type:
        q += f" AND {publication_type}[Publication Type]"
    if author:
        q += f" AND {author}[Author]"
    if start_date and end_date:
        q += f" AND {start_date}:{end_date}[Date - Publication]"
    elif start_date:
        q += f" AND {start_date}:3000[Date - Publication]"
    elif end_date:
        q += f" AND 1900:{end_date}[Date - Publication]"
    h = Entrez.esearch(db="pubmed", term=q, retmax=max_results)
    rec = Entrez.read(h)
    h.close()
    pmids = rec["IdList"]
    papers = []
    for pid in pmids:
        h = Entrez.efetch(db="pubmed", id=pid, rettype="abstract", retmode="xml")
        rec = Entrez.read(h)
        h.close()
        article = rec["PubmedArticle"][0]["MedlineCitation"]["Article"]
        authors = []
        for a in article.get("AuthorList", []):
            last = a.get("LastName", "")
            init = a.get("Initials", "")
            if last:
                authors.append(f"{last} {init}".strip())
        abstract = ""
        if "Abstract" in article and "AbstractText" in article["Abstract"]:
            abstract = " ".join(str(t) for t in article["Abstract"]["AbstractText"])
        date = article.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
        pub_date = f"{date.get('Year','')}-{date.get('Month','')}-{date.get('Day','')}".strip("-")
        doi = ""
        for eid in article.get("ELocationID", []):
            if eid.attributes.get("EIdType") == "doi":
                doi = str(eid)
        papers.append({
            "title": article.get("ArticleTitle", ""),
            "authors": authors,
            "journal": article.get("Journal", {}).get("Title", ""),
            "published": pub_date,
            "year": pub_date[:4],
            "pmid": pid,
            "doi": doi,
            "abstract": abstract,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pid}/",
            "source": "pubmed",
        })
    return papers

# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------
def _bibtex_key(paper: Dict) -> str:
    first_author = paper.get("authors", ["Unknown"])[0].split()[-1].lower()
    year = paper.get("year") or paper.get("published", "0000")[:4]
    title_word = (paper.get("title") or "").split()[0].lower() if paper.get("title") else ""
    return f"{first_author}{year}{title_word}"

def format_text(papers: List[Dict], source_label: str = "mixed") -> str:
    if not papers:
        return "未找到结果。"
    lines = [f"共找到 {len(papers)} 篇论文：\n"]
    for i, p in enumerate(papers, 1):
        lines.append(f"\n{i}. {p.get('title', 'No title')}")
        authors = p.get("authors", [])
        if authors:
            a_str = ", ".join(authors[:5])
            if len(authors) > 5:
                a_str += " et al."
            lines.append(f"   作者: {a_str}")
        lines.append(f"   年份: {p.get('year') or p.get('published', 'N/A')}")
        if p.get("journal"):
            lines.append(f"   期刊: {p['journal']}")
        if p.get("doi"):
            lines.append(f"   DOI: {p['doi']}")
        if p.get("citation_count") is not None:
            lines.append(f"   引用: {p['citation_count']}")
        abstract = p.get("abstract", "")
        if abstract:
            lines.append(f"   摘要: {abstract[:200]}…" if len(abstract) > 200 else f"   摘要: {abstract}")
        if p.get("pdf_url"):
            lines.append(f"   PDF: {p['pdf_url']}")
        lines.append(f"   来源: {p.get('source', source_label)}")
    return "\n".join(lines)

def format_json_output(papers: List[Dict]) -> str:
    return json.dumps(papers, indent=2, ensure_ascii=False)

def format_bibtex(papers: List[Dict]) -> str:
    entries = []
    for p in papers:
        key = _bibtex_key(p)
        entry = f"@article{{{key},\n"
        entry += f"  title={{{p.get('title', 'No title')}}},\n"
        if p.get("authors"):
            entry += f"  author={{{' and '.join(p['authors'])}}},\n"
        year = p.get("year") or (p.get("published") or "0000")[:4]
        entry += f"  year={{{year}}},\n"
        if p.get("journal"):
            entry += f"  journal={{{p['journal']}}},\n"
        if p.get("volume"):
            entry += f"  volume={{{p['volume']}}},\n"
        if p.get("pages"):
            entry += f"  pages={{{p['pages']}}},\n"
        if p.get("doi"):
            entry += f"  doi={{{p['doi']}}},\n"
        if p.get("url"):
            entry += f"  url={{{p['url']}}},\n"
        entry = entry.rstrip(",\n") + "\n}\n"
        entries.append(entry)
    return "\n".join(entries)

def format_ris(papers: List[Dict]) -> str:
    entries = []
    for p in papers:
        entry = "TY  - JOUR\n"
        entry += f"TI  - {p.get('title', 'No title')}\n"
        for a in p.get("authors", []):
            entry += f"AU  - {a}\n"
        year = (p.get("published") or "")[:4]
        entry += f"PY  - {year}\n"
        if p.get("published"):
            entry += f"DA  - {p['published']}\n"
        if p.get("journal"):
            entry += f"JO  - {p['journal']}\n"
        if p.get("volume"):
            entry += f"VL  - {p['volume']}\n"
        if p.get("pages"):
            entry += f"SP  - {p['pages']}\n"
        if p.get("doi"):
            entry += f"DO  - {p['doi']}\n"
        if p.get("abstract"):
            entry += f"AB  - {p['abstract']}\n"
        if p.get("url"):
            entry += f"UR  - {p['url']}\n"
        entry += "ER  -\n\n"
        entries.append(entry)
    return "".join(entries)

def format_markdown(papers: List[Dict]) -> str:
    if not papers:
        return "# 搜索结果\n\n未找到结果。"
    lines = [f"# 搜索结果：共 {len(papers)} 篇论文\n"]
    for i, p in enumerate(papers, 1):
        lines.append(f"\n## {i}. {p.get('title', 'No title')}\n")
        if p.get("authors"):
            lines.append(f"**作者:** {', '.join(p['authors'][:5])}{' et al.' if len(p['authors']) > 5 else ''}\n")
        year = p.get("year") or p.get("published", "")
        lines.append(f"**年份:** {year}\n")
        if p.get("journal"):
            lines.append(f"**期刊:** {p['journal']}\n")
        if p.get("doi"):
            lines.append(f"**DOI:** {p['doi']}\n")
        if p.get("citation_count") is not None:
            lines.append(f"**引用数:** {p['citation_count']}\n")
        if p.get("abstract"):
            lines.append(f"**摘要:** {p['abstract']}\n")
        if p.get("pdf_url"):
            lines.append(f"**PDF:** [下载]({p['pdf_url']})\n")
        lines.append(f"**来源:** {p.get('source', 'unknown')}\n")
    return "".join(lines)

def format_output(papers: List[Dict], fmt: str) -> str:
    fmt = fmt.lower()
    if fmt == "json":
        return format_json_output(papers)
    elif fmt == "bibtex":
        return format_bibtex(papers)
    elif fmt == "ris":
        return format_ris(papers)
    elif fmt == "markdown":
        return format_markdown(papers)
    else:
        return format_text(papers)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="学术论文检索小助手（松哥版）| OpenAlex · Semantic Scholar · Crossref · arXiv · PubMed",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("source", choices=["openalex","semantic","multi","crossref","arxiv","pubmed"],
                        help="数据源: openalex(推荐无需key) | semantic | multi(自动补全) | crossref | arxiv | pubmed")
    parser.add_argument("query", nargs="?", default="", help="搜索关键词")
    parser.add_argument("-n","--max-results", type=int, default=10)
    parser.add_argument("-f","--format", choices=["text","json","bibtex","ris","markdown"], default="text")
    parser.add_argument("-o","--output", help="保存结果到文件")
    parser.add_argument("--year", type=int)
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--author")
    parser.add_argument("--journal-issn")
    parser.add_argument("--concept-id")
    parser.add_argument("--semantic-api-key", help="Semantic Scholar API Key（可选，有 key 速率更快）")
    parser.add_argument("--min-citations", type=int)
    parser.add_argument("--enrich-s2", action="store_true")
    parser.add_argument("--crossref-enrich", action="store_true", default=True)
    parser.add_argument("--doi-file", help="从文件读取 DOI 列表（crossref 模式）")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--output-dir", default="downloads")
    parser.add_argument("--sort-by", default="relevance")
    parser.add_argument("--category", help="arXiv 学科分类，如 cs.LG")
    parser.add_argument("--publication-type", help="PubMed 文献类型")

    args = parser.parse_args()

    papers = []
    if args.source == "openalex":
        papers = search_openalex(args.query, args.max_results, args.year,
                                 args.start_date, args.end_date,
                                 args.journal_issn, args.concept_id,
                                 args.author, args.sort_by)
        if args.crossref_enrich:
            papers = enrich_with_crossref(papers)

    elif args.source == "semantic":
        papers = search_semantic_scholar(args.query, args.max_results, args.year,
                                          args.min_citations, args.author,
                                          args.semantic_api_key, args.enrich_s2)

    elif args.source == "multi":
        papers = multi_source_search(args.query, args.max_results,
                                      {"year": args.year, "start_date": args.start_date,
                                       "end_date": args.end_date, "journal_issn": args.journal_issn,
                                       "concept_id": args.concept_id, "author": args.author,
                                       "sort": args.sort_by},
                                      args.semantic_api_key, args.crossref_enrich)

    elif args.source == "crossref":
        dois = []
        if args.doi_file:
            with open(args.doi_file) as f:
                dois = [l.strip() for l in f if l.strip()]
        elif args.query:
            dois = [args.query]
        else:
            sys.exit("crossref 模式需要提供 DOI 或 --doi-file")
        meta = fetch_crossref_metadata(dois)
        papers = list(meta.values())

    elif args.source == "arxiv":
        papers = search_arxiv(args.query, args.max_results, args.category,
                               args.author, args.year,
                               args.start_date, args.end_date, args.sort_by)
        if args.download and papers:
            Path(args.output_dir).mkdir(exist_ok=True)
            for i, p in enumerate(papers):
                if p.get("pdf_url"):
                    try:
                        r = requests.get(p["pdf_url"], timeout=30)
                        r.raise_for_status()
                        fn = Path(args.output_dir) / f"{p.get('arxiv_id','paper')}_{i}.pdf"
                        fn.write_bytes(r.content)
                        print(f"已下载: {fn.name}", file=sys.stderr)
                    except Exception as e:
                        print(f"下载失败: {e}", file=sys.stderr)

    elif args.source == "pubmed":
        papers = search_pubmed(args.query, args.max_results,
                                args.start_date, args.end_date,
                                args.publication_type, args.author)

    formatted = format_output(papers, args.format)
    if args.output:
        Path(args.output).write_text(formatted, encoding="utf-8")
        print(f"已保存到 {args.output}", file=sys.stderr)
    else:
        print(formatted)

if __name__ == "__main__":
    main()
