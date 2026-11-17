#!/usr/bin/env python3
"""
pubmed_search.py - PubMed literature search & fetch helper.

Two modes:
  1) Query mode: esearch (get PMIDs) -> efetch (get records)
       python pubmed_search.py --query "metformin AND type 2 diabetes" --retmax 5
  2) PMID mode: fetch specific PMIDs directly (esearch skipped)
       python pubmed_search.py --pmids 38900001 38900002

Output: JSON to stdout
  {"ok": true, "query": "...", "count": 123, "pmids": [...], "articles": [ {...} ]}

Each article: pmid, title, title_zh (optional, via --translate), authors, journal,
pubdate, abstract, doi, doi_url, pubmed_url.

Only Python standard library is used. Network access to NCBI is required.
API key is OPTIONAL: --api-key / env NCBI_API_KEY raises the rate limit
from 3 to 10 req/sec. --email is a NCBI-recommended courtesy field.
When a run looks like bulk retrieval or hits the rate limit, the JSON includes
"api_key_hint": true and a "hint" so the agent can walk the user through
registering an NCBI account and creating an API key (see references/register-api-key.md).
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html import unescape

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
USER_AGENT = "WorkBuddy-PubMed-Skill/1.0 (medical literature lookup)"

MONTH_MAP = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
    "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12",
}


class RateLimitError(RuntimeError):
    """Raised when NCBI returns HTTP 429 (too many requests)."""


def add_courtesy(params, tool=None, email=None, api_key=None):
    """Attach NCBI-recommended courtesy + optional API-key params to a query dict."""
    if tool:
        params["tool"] = tool
    if email:
        params["email"] = email
    if api_key:
        params["api_key"] = api_key
    return params


def build_url(endpoint, params):
    query = urllib.parse.urlencode(params)
    return f"{EUTILS_BASE}/{endpoint}?{query}"


def http_get(url, timeout=30, retries=3):
    """GET with retry + exponential backoff. Returns raw bytes.

    Raises RateLimitError on HTTP 429 so callers can guide the user to an API key.
    """
    last_err = None
    was_429 = False
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.reason}"
            if e.code == 429:
                was_429 = True
            # 429 / 5xx -> retry; 4xx (other) -> fail fast
            if 400 <= e.code < 500 and e.code != 429:
                break
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = str(e)
        time.sleep(1.5 * (attempt + 1))
    if was_429:
        raise RateLimitError(
            "NCBI 触发了访问频率限制（HTTP 429）。注册 NCBI 账户并创建 API key "
            "可把限速从 3 次/秒提升到 10 次/秒。")
    raise RuntimeError(f"Request failed after {retries} attempts: {last_err}")


def esearch(query, retmax=5, sort="relevance", mindate=None, maxdate=None,
            datetype="pdat", tool=None, email=None, api_key=None):
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": str(retmax),
        "sort": sort,
    }
    if mindate:
        params["mindate"] = mindate
        params["datetype"] = datetype
    if maxdate:
        params["maxdate"] = maxdate
        params["datetype"] = datetype
    add_courtesy(params, tool=tool, email=email, api_key=api_key)
    data = http_get(build_url("esearch.fcgi", params))
    result = json.loads(data.decode("utf-8"))
    esearch_result = result.get("esearchresult", {})
    return {
        "count": int(esearch_result.get("count", 0)),
        "pmids": esearch_result.get("idlist", []),
    }


def _text(elem):
    """All inner text of an element, preserving child tag text (e.g. <i>, <b>)."""
    if elem is None:
        return ""
    return "".join(elem.itertext()).strip()


def _format_author(author):
    last = author.findtext("LastName") or ""
    fore = author.findtext("ForeName") or author.findtext("Initials") or ""
    collective = author.findtext("CollectiveName") or ""
    if collective:
        return collective.strip()
    name = f"{last} {fore}".strip()
    return name


def _format_pubdate(article):
    """Extract a YYYY[-MM[-DD]] date from JournalIssue PubDate or ArticleDate."""
    pubdate = article.find(".//Journal/JournalIssue/PubDate")
    if pubdate is not None:
        year = pubdate.findtext("Year") or ""
        month = pubdate.findtext("Month") or ""
        day = pubdate.findtext("Day") or ""
        medline = pubdate.findtext("MedlineDate") or ""
        if month and not month.isdigit():
            month = MONTH_MAP.get(month[:3].lower(), month)
        parts = [p for p in (year, month, day) if p]
        if parts:
            return "-".join(parts)
        if medline:
            return medline.strip()
    art_date = article.find(".//Article/ArticleDate")
    if art_date is not None:
        year = art_date.findtext("Year") or ""
        month = art_date.findtext("Month") or ""
        day = art_date.findtext("Day") or ""
        parts = [p for p in (year, month, day) if p]
        if parts:
            return "-".join(parts)
    return ""


def _format_abstract(article_elem):
    """Join AbstractText sections; prefix section labels like BACKGROUND:."""
    abstract = article_elem.find(".//Abstract")
    if abstract is None:
        return ""
    chunks = []
    for abst in abstract.findall("AbstractText"):
        label = abst.get("Label")
        text = unescape(_text(abst))
        if not text:
            continue
        chunks.append(f"{label}: {text}" if label else text)
    return "\n".join(chunks)


def _extract_doi(article_elem):
    for aid in article_elem.findall(".//ArticleId"):
        if aid.get("IdType") == "doi" and aid.text:
            return aid.text.strip()
    # fallback: ELocationID
    for eloc in article_elem.findall(".//ELocationID"):
        if eloc.get("EIdType") == "doi" and eloc.text:
            return eloc.text.strip()
    return ""


def parse_pubmed_xml(xml_bytes):
    root = ET.fromstring(xml_bytes)
    articles = []
    for pa in root.findall("PubmedArticle"):
        medline = pa.find("MedlineCitation")
        article = medline.find("Article") if medline is not None else None
        if article is None:
            continue
        pmid = (medline.findtext("PMID") or "").strip()
        title = unescape(_text(article.find("ArticleTitle")))
        authors = [_format_author(a) for a in article.findall(".//AuthorList/Author")]
        authors = [a for a in authors if a]
        journal = (article.findtext(".//Journal/Title")
                   or article.findtext(".//Journal/ISOAbbreviation") or "").strip()
        pubdate = _format_pubdate(pa)
        abstract = _format_abstract(pa)
        doi = _extract_doi(pa)
        articles.append({
            "pmid": pmid,
            "title": title,
            "authors": authors,
            "journal": journal,
            "pubdate": pubdate,
            "abstract": abstract,
            "doi": doi,
            "doi_url": f"https://doi.org/{doi}" if doi else "",
            "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
        })
    return articles


def efetch(pmids, tool=None, email=None, api_key=None):
    if not pmids:
        return []
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
        "rettype": "abstract",
    }
    add_courtesy(params, tool=tool, email=email, api_key=api_key)
    data = http_get(build_url("efetch.fcgi", params))
    return parse_pubmed_xml(data)


def main():
    parser = argparse.ArgumentParser(
        description="Search PubMed (esearch) and fetch article records (efetch).")
    parser.add_argument("--query", help="PubMed query string (supports full PubMed syntax)")
    parser.add_argument("--pmids", nargs="+", help="Fetch these PMIDs directly, skip esearch")
    parser.add_argument("--retmax", type=int, default=5, help="Max results (default: 5, max: 50)")
    parser.add_argument("--sort", default="relevance",
                        choices=["relevance", "pub_date", "Author", "JournalName"],
                        help="Sort order for esearch (default: relevance)")
    parser.add_argument("--mindate", help="Min date, format YYYY/MM/DD or YYYY (pairs with datetype)")
    parser.add_argument("--maxdate", help="Max date, format YYYY/MM/DD or YYYY")
    parser.add_argument("--datetype", default="pdat",
                        choices=["pdat", "edat", "mdat"],
                        help="Date type for mindate/maxdate (default: pdat = publication date)")
    parser.add_argument("--email", help="你的邮箱（NCBI 建议填写的礼貌字段，可选）")
    parser.add_argument("--api-key", help="NCBI API key（提升限速，可选；也可用环境变量 NCBI_API_KEY）")
    args = parser.parse_args()

    if not args.query and not args.pmids:
        parser.error("Provide --query or --pmids")
    retmax = max(1, min(args.retmax, 50))

    import os
    api_key = args.api_key or os.environ.get("NCBI_API_KEY") or None
    email = args.email
    tool = "workbuddy_pubmed_skill"

    # 判定是否为"批量"检索：需要更快的限速时才值得引导申请 API key
    is_bulk = (not args.pmids and retmax >= 20) or (args.pmids and len(args.pmids) >= 20)

    out = {"ok": True, "query": args.query or "", "count": None,
           "pmids": [], "articles": [], "api_key_hint": False, "hint": ""}
    try:
        if args.pmids:
            pmids = [re.sub(r"\D", "", p) for p in args.pmids]
            pmids = [p for p in pmids if p]
            out["pmids"] = pmids
            out["count"] = len(pmids)
        else:
            res = esearch(args.query, retmax=retmax, sort=args.sort,
                          mindate=args.mindate, maxdate=args.maxdate,
                          datetype=args.datetype, tool=tool, email=email, api_key=api_key)
            out["count"] = res["count"]
            out["pmids"] = res["pmids"]
            pmids = res["pmids"]
            # Be polite: NCBI asks for <=3 req/sec without API key
            time.sleep(0.4 if api_key else 0.8)

        if pmids:
            out["articles"] = efetch(pmids, tool=tool, email=email, api_key=api_key)
    except RateLimitError as e:
        out = {
            "ok": False, "error": str(e), "query": args.query or "",
            "api_key_hint": True,
            "hint": "你触达了 NCBI 的访问频率上限。注册 NCBI 账户并创建 API key "
                    "可把限速从 3 次/秒提升到 10 次/秒。参阅 references/register-api-key.md "
                    "获取图文并茂的小白注册指南。",
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as e:  # noqa: BLE001 - surface any failure as JSON
        out = {"ok": False, "error": str(e), "query": args.query or ""}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        sys.exit(1)

    if is_bulk and not api_key:
        out["api_key_hint"] = True
        out["hint"] = ("本次为批量检索，未使用 API key 时 NCBI 限速 3 次/秒。"
                       "若需要更快或更大批量，建议注册 NCBI 账户并创建 API key（免费）。"
                       "详见 references/register-api-key.md。")

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
