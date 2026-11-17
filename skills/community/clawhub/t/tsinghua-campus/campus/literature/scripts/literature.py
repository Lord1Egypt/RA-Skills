"""literature.py — 文献检索子 SKILL 统一入口

多源文献检索（基于共享文献引擎）：
  - Scopus（agent/literature/scopus_client.py，付费 API）
  - arXiv（开放预印本，物理/数学/计算机/生物）
  - OpenAlex（开放学术元数据，免费，可选 Key）
  - Crossref（DOI 元数据，免费，无需 Key）

JSON 输出。凭据走 campus keyring（creds.py add ...）/ 统一 .env（OPENALEX_API_KEY）。
与 agent 项目 .env 完全解耦——通过 subprocess env 注入 scopus_client。

用法:
  literature.py status                                # 凭据状态 + 各源说明
  literature.py search --query <检索式> [--source scopus|arxiv|openalex|crossref|all]
                                                  [--count N] [--date 年份]
  literature.py abstract --doi <doi> [--source scopus|openalex|crossref]
  literature.py full --query <检索式> [--count N]    # 搜索+摘要（默认 scopus）
  literature.py sources                              # 列出可用源 + 是否配置

本子 SKILL 需要的凭据:
  - scopus_api_key:     Scopus API Key（dev.elsevier.com 申请，文献检索必需）
  - scopus_inst_token:  Scopus 机构 Token（可选，提升配额）
  - OPENALEX_API_KEY:   OpenAlex 可选 Key（.env，提升 $0.01→$1/天 额度，免费来源不强制）
"""
import sys
import os
import json
import subprocess
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "creds", "scripts"))
import common
import creds
import vault

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env")
SCOPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "agent", "literature", "scopus_client.py")
HTTP_TIMEOUT = 20

# 公共 User-Agent（OpenAlex 推荐 mailto）
MAILTO = "tsinghua-campus-skill@local"
NS_ATOM = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


# ==================== 凭据 ====================

def _get_key(key):
    """从凭据保险箱取明文（统一走 vault.vault_get）。"""
    try:
        return vault.vault_get(key)
    except Exception:
        return ""


def _load_env():
    """从统一 .env 读 KEY=VALUE dict。"""
    env = {}
    if not os.path.exists(ENV_PATH):
        return env
    try:
        for line in open(ENV_PATH, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    except Exception:
        pass
    return env


# ==================== HTTP 工具 ====================

def _http_get(url, headers=None, timeout=HTTP_TIMEOUT):
    h = {"User-Agent": f"tsinghua-campus-skill/{MAILTO}"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), r.status
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return body.encode("utf-8"), e.code
    except Exception as e:
        common.output_json({"status": "error", "error": "network", "message": f"HTTP 失败: {e}", "url": url})
        sys.exit(1)


# ==================== Scopus（agent 共享底座）====================

def _run_scopus(args_list):
    """调用 scopus_client（--quiet 静默，无 stderr 噪音），返回 (ok, 结果列表)。"""
    api_key = _get_key("scopus_api_key")
    if not api_key:
        common.output_json({"status": "error", "error": "missing_cred",
                            "message": "缺少 Scopus API Key。请让用户提供 scopus_api_key（dev.elsevier.com 申请），"
                                       "用 creds.py add scopus_api_key --value-stdin 配置。"})
        sys.exit(1)
    env = os.environ.copy()
    env["SCOPUS_API_KEY"] = api_key
    inst = _get_key("scopus_inst_token")
    if inst:
        env["SCOPUS_INST_TOKEN"] = inst

    cmd = [sys.executable, SCOPUS, "--quiet"] + args_list
    r = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    lines = []
    for line in (r.stdout or "").splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                lines.append(json.loads(line))
            except Exception:
                continue
    return r.returncode == 0, lines


def _summarize_scopus(entries, limit=10):
    """从 Scopus search_result 提取简洁条目。"""
    out = []
    for e in entries:
        title = e.get("dc:title", "")
        if isinstance(title, list):
            title = title[0]
        out.append({
            "source": "scopus",
            "title": title,
            "id": e.get("dc:identifier", ""),
            "doi": e.get("prism:doi", ""),
            "year": (e.get("prism:coverDate", "") or "")[:4],
            "cited": e.get("citedby-count", ""),
            "authors": e.get("dc:creator", ""),
        })
    return out[:limit]


def scopus_search(query, count=10, date=None):
    ok, lines = _run_scopus(["search", "-q", query, "--count", str(count)] + (["--date", date] if date else []))
    if not ok:
        raise RuntimeError("Scopus 搜索失败（检查 scopus_api_key 是否有效）")
    meta = next((l for l in lines if l.get("phase") == "search_meta"), {})
    results = [l["data"] for l in lines if l.get("phase") == "search_result"]
    return {
        "total": meta.get("data", {}).get("total", len(results)),
        "results": _summarize_scopus(results, count),
    }


def scopus_abstract(doi):
    ok, lines = _run_scopus(["abstract", "--doi", doi])
    if not ok:
        raise RuntimeError("Scopus 摘要获取失败")
    abs_data = next((l.get("data", {}) for l in lines if l.get("phase") == "abstract_result"), {})
    ar = abs_data.get("abstracts-retrieval-response", abs_data)
    return {
        "source": "scopus",
        "title": ar.get("coredata", {}).get("dc:title", ""),
        "doi": ar.get("coredata", {}).get("prism:doi", ""),
        "abstract": (ar.get("coredata", {}).get("dc:description") or "")[:2000],
        "authors": ar.get("coredata", {}).get("dc:creator", ""),
    }


# ==================== arXiv ====================

def arxiv_search(query, count=10, date=None):
    """arXiv API（Atom XML）。注意：arXiv 无 date 过滤参数（搜索结果自带 published）。"""
    params = {"search_query": f"all:{query}", "start": "0", "max_results": str(count)}
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    body, code = _http_get(url)
    if code != 200:
        raise RuntimeError(f"arXiv HTTP {code}: {body[:200]}")
    try:
        root = ET.fromstring(body)
    except Exception as e:
        raise RuntimeError(f"arXiv XML 解析失败: {e}")
    entries = root.findall("atom:entry", NS_ATOM)
    results = []
    for e in entries:
        title = (e.findtext("atom:title", default="", namespaces=NS_ATOM) or "").strip().replace("\n", " ")
        summary = (e.findtext("atom:summary", default="", namespaces=NS_ATOM) or "").strip()[:1500]
        published = (e.findtext("atom:published", default="", namespaces=NS_ATOM) or "")[:10]
        authors = ", ".join(a.findtext("atom:name", default="", namespaces=NS_ATOM) or ""
                            for a in e.findall("atom:author", NS_ATOM))
        # DOI 在 arxiv:doi 命名空间（如果存在）；否则给 arxiv id
        arxiv_id = (e.findtext("atom:id", default="", namespaces=NS_ATOM) or "").rsplit("/", 1)[-1]
        doi_e = e.find("{http://arxiv.org/schemas/atom}doi")
        doi = doi_e.text.strip() if doi_e is not None and doi_e.text else ""
        results.append({
            "source": "arxiv",
            "title": title,
            "arxiv_id": arxiv_id,
            "doi": doi,
            "year": published[:4],
            "published": published,
            "authors": authors[:300],
            "summary": summary,
        })
        if date and not published.startswith(str(date)):
            continue
    return {"total": len(results), "results": results[:count]}


# ==================== OpenAlex ====================

def openalex_search(query, count=10, date=None):
    """OpenAlex API。免费但建议 User-Agent 含 mailto；可选 key 提升额度。"""
    env = _load_env()
    key = env.get("OPENALEX_API_KEY", "")
    params = {"search": query, "per_page": str(count)}
    if date:
        params["filter"] = f"publication_year:{date}"
    headers = {}
    if key:
        headers["X-API-Key"] = key
    qs = urllib.parse.urlencode(params)
    url = "https://api.openalex.org/works?" + qs
    body, code = _http_get(url, headers=headers)
    if code != 200:
        raise RuntimeError(f"OpenAlex HTTP {code}: {body[:200]}")
    try:
        data = json.loads(body)
    except Exception as e:
        raise RuntimeError(f"OpenAlex JSON 解析失败: {e}")
    results = []
    for w in data.get("results", []):
        # authors
        authors = ", ".join(
            (a.get("author", {}) or {}).get("display_name", "")
            for a in (w.get("authorships") or [])
        )[:300]
        # concepts/topics（可选摘要）
        title = (w.get("title") or "").replace("\n", " ")
        results.append({
            "source": "openalex",
            "title": title,
            "openalex_id": w.get("id", "").rsplit("/", 1)[-1] if w.get("id") else "",
            "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
            "year": str(w.get("publication_year") or ""),
            "cited": w.get("cited_by_count", 0),
            "authors": authors,
            "type": w.get("type", ""),
            "open_access": w.get("open_access", {}).get("is_oa", False),
            "primary_location": (w.get("primary_location") or {}).get("source", {}).get("display_name", ""),
        })
    return {"total": data.get("meta", {}).get("count", len(results)), "results": results[:count]}


def openalex_abstract(doi):
    """按 DOI 取 OpenAlex 元数据（含 abstract_inverted_index，需要重排）。"""
    url = f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}"
    body, code = _http_get(url)
    if code != 200:
        raise RuntimeError(f"OpenAlex HTTP {code}")
    try:
        w = json.loads(body)
    except Exception as e:
        raise RuntimeError(f"OpenAlex JSON 解析失败: {e}")
    # 重排 abstract_inverted_index
    inv = w.get("abstract_inverted_index") or {}
    abstract = _uninvert_abstract(inv)
    return {
        "source": "openalex",
        "title": w.get("title", ""),
        "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
        "abstract": abstract[:2000],
        "cited_by": w.get("cited_by_count", 0),
        "year": w.get("publication_year"),
        "authors": ", ".join(
            (a.get("author", {}) or {}).get("display_name", "")
            for a in (w.get("authorships") or [])
        ),
    }


def _uninvert_abstract(inv):
    """OpenAlex 返回 inverted index → 还原为正常文本。"""
    if not inv:
        return ""
    positions = []
    for word, idxs in inv.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    return " ".join(p[1] for p in positions)


# ==================== Crossref ====================

def crossref_search(query, count=10, date=None):
    """Crossref API（DOI 元数据）。免费无需 Key。"""
    params = {"query.bibliographic": query, "rows": str(count)}
    if date:
        params["filter"] = f"from-pub-date:{date}-01-01,until-pub-date:{date}-12-31"
    qs = urllib.parse.urlencode(params)
    url = "https://api.crossref.org/works?" + qs
    body, code = _http_get(url)
    if code != 200:
        raise RuntimeError(f"Crossref HTTP {code}: {body[:200]}")
    try:
        data = json.loads(body)
    except Exception as e:
        raise RuntimeError(f"Crossref JSON 解析失败: {e}")
    msg = data.get("message", {})
    items = msg.get("items", [])
    results = []
    for it in items:
        title = it.get("title", [""])
        if isinstance(title, list):
            title = title[0]
        authors = ", ".join(
            f'{a.get("given","")} {a.get("family","")}'.strip()
            for a in (it.get("author") or [])
        )[:300]
        issued = it.get("issued", {}).get("date-parts", [[None]])[0]
        year = str(issued[0]) if issued and issued[0] else ""
        results.append({
            "source": "crossref",
            "title": (title or "").replace("\n", " "),
            "doi": it.get("DOI", ""),
            "year": year,
            "cited": it.get("is-referenced-by-count", 0),
            "authors": authors,
            "type": it.get("type", ""),
            "container": (it.get("container-title") or [""])[0] if it.get("container-title") else "",
        })
    return {"total": msg.get("total-results", len(results)), "results": results[:count]}


def crossref_abstract(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    body, code = _http_get(url)
    if code != 200:
        raise RuntimeError(f"Crossref HTTP {code}")
    try:
        data = json.loads(body)
    except Exception as e:
        raise RuntimeError(f"Crossref JSON 解析失败: {e}")
    msg = data.get("message", {})
    title = msg.get("title", [""])
    if isinstance(title, list):
        title = title[0]
    return {
        "source": "crossref",
        "title": title,
        "doi": msg.get("DOI", ""),
        "abstract": (msg.get("abstract") or "").replace("<jats:p>", "").replace("</jats:p>", "")[:2000],
        "year": (msg.get("issued", {}).get("date-parts", [[None]])[0] or [None])[0],
        "authors": ", ".join(
            f'{a.get("given","")} {a.get("family","")}'.strip()
            for a in (msg.get("author") or [])
        ),
        "container": (msg.get("container-title") or [""])[0] if msg.get("container-title") else "",
        "publisher": msg.get("publisher", ""),
    }


# ==================== 多源调度 ====================

SEARCH_FUNCS = {
    "scopus": scopus_search,
    "arxiv": arxiv_search,
    "openalex": openalex_search,
    "crossref": crossref_search,
}
ABSTRACT_FUNCS = {
    "scopus": lambda doi: scopus_abstract(doi),
    "openalex": openalex_abstract,
    "crossref": crossref_abstract,
}


def _split_sources(spec):
    """解析 --source 参数。支持 'all' / 'scopus,arxiv' / 'scopus'。"""
    spec = (spec or "scopus").strip().lower()
    if spec == "all":
        return list(SEARCH_FUNCS.keys())
    return [s.strip() for s in spec.split(",") if s.strip()]


def cmd_search(query, count=10, date=None, source="scopus"):
    sources = _split_sources(source)
    out_results = []
    per_source = {}
    failures = {}
    for src in sources:
        fn = SEARCH_FUNCS.get(src)
        if not fn:
            failures[src] = f"未知源 {src}"
            continue
        try:
            r = fn(query, count=count, date=date)
            out_results.extend(r["results"])
            per_source[src] = {"ok": True, "count": r["total"]}
        except Exception as e:
            failures[src] = str(e)[:200]
            per_source[src] = {"ok": False, "error": str(e)[:200]}
    if failures and not out_results:
        common.output_json({"status": "error", "message": "所有源均失败", "per_source": per_source, "failures": failures})
        sys.exit(1)
    common.output_json({
        "status": "ok",
        "query": query,
        "sources": sources,
        "per_source": per_source,
        "failures": failures,
        "total": len(out_results),
        "results": out_results,
    })


def cmd_abstract(doi, source="openalex"):
    """默认 openalex（免费）→ fallback crossref → scopus。"""
    sources = _split_sources(source) if "," in (source or "") else [source]
    last_err = None
    for src in sources:
        fn = ABSTRACT_FUNCS.get(src)
        if not fn:
            last_err = f"{src} 不支持 abstract"
            continue
        try:
            r = fn(doi)
            common.output_json({"status": "ok", **r})
            return
        except Exception as e:
            last_err = str(e)
    common.output_json({"status": "error", "message": f"所有源均未取到摘要：{last_err}", "tried": sources})
    sys.exit(1)


def cmd_full(query, count=5, date=None, source="scopus"):
    """search + abstract（默认 scopus）。其他源只有摘要模式。"""
    sources = _split_sources(source)
    out = []
    per_source = {}
    for src in sources:
        try:
            r = SEARCH_FUNCS[src](query, count=count, date=date)
            items = []
            for hit in r["results"]:
                item = dict(hit)
                # 尝试取摘要
                doi = hit.get("doi")
                if doi and src in ABSTRACT_FUNCS:
                    try:
                        abs_r = ABSTRACT_FUNCS[src](doi)
                        item["abstract"] = abs_r.get("abstract", "")
                    except Exception:
                        item["abstract"] = ""
                else:
                    item["abstract"] = hit.get("summary", "")
                items.append(item)
            out.extend(items)
            per_source[src] = {"ok": True, "count": len(items)}
        except Exception as e:
            per_source[src] = {"ok": False, "error": str(e)[:200]}
    common.output_json({
        "status": "ok",
        "query": query,
        "sources": sources,
        "per_source": per_source,
        "total": len(out),
        "results": out,
    })


def cmd_status():
    """凭据状态 + 各源说明。"""
    scopus_key = _get_key("scopus_api_key")
    scopus_inst = _get_key("scopus_inst_token")
    env = _load_env()
    openalex_key = env.get("OPENALEX_API_KEY", "")
    common.output_json({
        "status": "ok",
        "sources": [
            {
                "name": "scopus",
                "label": "Scopus（Elsevier）",
                "free": False,
                "configured": bool(scopus_key),
                "needs_cred": "scopus_api_key (keyring)",
                "how_to_get": "dev.elsevier.com 注册申请（可走清华 CARSI 机构登录），免费层每日配额",
                "covers": "全学科（生物医学偏弱），付费权威",
            },
            {
                "name": "arxiv",
                "label": "arXiv（预印本）",
                "free": True,
                "configured": True,
                "needs_cred": "无",
                "how_to_get": "无需 Key，HTTP 直接调",
                "covers": "物理/数学/计算机/生物/统计（无中文论文）",
            },
            {
                "name": "openalex",
                "label": "OpenAlex（开放学术元数据）",
                "free": True,
                "configured": True,
                "needs_cred": "OPENALEX_API_KEY（可选，.env 提升额度）",
                "how_to_get": "https://openalex.org/settings/api 注册免费 Key，从 $0.01/天 升到 $1/天",
                "covers": "全学科（替代 Scopus 的免费方案，含引用、机构、主题分类）",
            },
            {
                "name": "crossref",
                "label": "Crossref（DOI 元数据）",
                "free": True,
                "configured": True,
                "needs_cred": "无",
                "how_to_get": "无需 Key",
                "covers": "DOI 已注册的学术论文元数据，与 OpenAlex 互为冗余提高命中率",
            },
        ],
        "required_creds": [
            {"key": "scopus_api_key", "configured": bool(scopus_key),
             "how_to_get": "dev.elsevier.com", "purpose": "Scopus 检索（必需）"},
            {"key": "scopus_inst_token", "configured": bool(scopus_inst),
             "how_to_get": "清华图书馆 Institutional Token", "purpose": "提升 Scopus 配额（可选）"},
            {"key": "OPENALEX_API_KEY", "configured": bool(openalex_key),
             "how_to_get": "openalex.org/settings/api", "purpose": "OpenAlex 高级额度（可选）"},
        ],
    })


def cmd_sources():
    """仅列出源与状态（短输出）。"""
    cmd_status()


def main():
    import argparse
    ap = argparse.ArgumentParser(description="文献检索统一入口（多源）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("search", help="检索（可指定多源 --source scopus,arxiv,openalex,crossref,all）")
    p.add_argument("-q", "--query", required=True)
    p.add_argument("--count", type=int, default=10)
    p.add_argument("--date", help="年份过滤（部分源支持）")
    p.add_argument("--source", default="scopus",
                   help="数据源（逗号分隔）：scopus|arxiv|openalex|crossref|all")
    p.set_defaults(_func=lambda a: cmd_search(a.query, a.count, a.date, a.source))

    p = sub.add_parser("abstract", help="按 DOI 取摘要")
    p.add_argument("--doi", required=True)
    p.add_argument("--source", default="openalex,crossref,scopus",
                   help="数据源（按顺序尝试，第一个成功即返回）")
    p.set_defaults(_func=lambda a: cmd_abstract(a.doi, a.source))

    p = sub.add_parser("full", help="搜索+摘要")
    p.add_argument("-q", "--query", required=True)
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--date")
    p.add_argument("--source", default="scopus")
    p.set_defaults(_func=lambda a: cmd_full(a.query, a.count, a.date, a.source))

    p = sub.add_parser("status", help="凭据 + 各源状态")
    p.set_defaults(_func=lambda a: cmd_status())

    p = sub.add_parser("sources", help="列出可用源（status 别名）")
    p.set_defaults(_func=lambda a: cmd_sources())

    args = ap.parse_args()
    args._func(args)


if __name__ == "__main__":
    main()
