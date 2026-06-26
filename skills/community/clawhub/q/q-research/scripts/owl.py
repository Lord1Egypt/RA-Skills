#!/usr/bin/env python3
"""
owl - Structured research assistant following a precise 6-step protocol:

  Step 1 · Search arXiv for the topic
  Step 2 · Open 5 promising papers (download PDF → convert via markitdown)
  Step 3 · Read title + abstract + intro of each
  Step 4 · Claude keeps the best 2 (explains why)
  Step 5 · Search web for: explanation · GitHub · survey · citations
  Step 6 · Write a 5-bullet summary of what was learned

Usage:
    owl "diffusion models"
    owl "LoRA fine-tuning" --category cs.LG --output report.md
    owl "protein structure prediction" --since year

Install:
    pip install requests markitdown
    chmod +x owl.py
    cp owl.py /usr/local/bin/owl

API keys:
    SERPER_API_KEY     Serper.dev  (Google search)
    OPENROUTER_API_KEY  OPENROUTER.AI      (paper selection + synthesis)
"""

import argparse
import http.client
import requests
import json
import os
import re
import sys
import time
import gzip
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import web_fetcher
# ── ANSI ──────────────────────────────────────────────────────────────────────

_TTY = sys.stdout.isatty()
def _c(code, t): return f"\033[{code}m{t}\033[0m" if _TTY else t
BOLD    = lambda t: _c("1",    t)
DIM     = lambda t: _c("2",    t)
CYAN    = lambda t: _c("36",   t)
GREEN   = lambda t: _c("32",   t)
YELLOW  = lambda t: _c("33",   t)
RED     = lambda t: _c("31",   t)
MAGENTA = lambda t: _c("35",   t)
BLUE    = lambda t: _c("34",   t)

def step(n: int, label: str) -> None:
    print(BOLD(f"\n  Step {n} · {label}"))

def ok(msg: str)   -> None: print(GREEN(  f"       ✓ {msg}"))
def info(msg: str) -> None: print(DIM(    f"         {msg}"))
def warn(msg: str) -> None: print(YELLOW( f"       ⚠ {msg}"))
def err(msg: str)  -> None: print(RED(    f"       ✗ {msg}"), file=sys.stderr)

# ── arXiv ─────────────────────────────────────────────────────────────────────

NS        = {"atom": "http://www.w3.org/2005/Atom"}
ARXIV_API = "https://export.arxiv.org/api/query"
ARXIV_ABS = "https://arxiv.org/abs"
ARXIV_PDF = "https://arxiv.org/pdf"

TIME_ALIASES = {
    "hour": "qdr:h", "day": "qdr:d",
    "week": "qdr:w", "month": "qdr:m", "year": "qdr:y",
}


def search_arxiv(query: str, n: int = 10,
                 category: str = "", sort_by: str = "relevance") -> list[dict]:
    sq = f"cat:{category} AND ({query})" if category else query
    params = {
        "search_query": f"all:{sq}",
        "start": 0, "max_results": n,
        "sortBy": sort_by, "sortOrder": "descending",
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    try:
        import requests
        r = requests.get(url, timeout=30)
        r.raise_for_status()
    except Exception as e:
        err(f"arXiv request failed: {e}")
        return []

    root = ET.fromstring(r.text)
    out  = []
    for entry in root.findall("atom:entry", NS):
        raw_id   = entry.findtext("atom:id", "", NS)
        arxiv_id = raw_id.split("/abs/")[-1]
        title    = (entry.findtext("atom:title",   "", NS) or "").strip().replace("\n", " ")
        abstract = (entry.findtext("atom:summary", "", NS) or "").strip().replace("\n", " ")
        published= (entry.findtext("atom:published", "", NS) or "")[:10]
        authors  = [a.findtext("atom:name", "", NS)
                    for a in entry.findall("atom:author", NS)]
        cats     = [t.get("term", "") for t in entry.findall("atom:category", NS)]
        out.append(dict(
            id=arxiv_id, title=title, authors=authors,
            abstract=abstract, published=published, categories=cats,
            url=f"{ARXIV_ABS}/{arxiv_id}", pdf_url=f"{ARXIV_PDF}/{arxiv_id}.pdf",
        ))
    return out


# ── PDF → Markdown via markitdown ────────────────────────────────────────────

def pdf_to_markdown(pdf_url: str, arxiv_id: str,
                    tmp_dir: str = "/tmp/owl_papers",
                    max_chars: int = 8_000) -> str:
    """
    Download PDF and convert to Markdown via markitdown.
    max_chars is intentionally modest here — we only need title + abstract + intro
    for the selection step (Step 3). Full text is fetched later for the best 2.
    """
    import subprocess

    os.makedirs(tmp_dir, exist_ok=True)
    safe_id  = re.sub(r"[^\w.-]", "_", arxiv_id)
    pdf_path = os.path.join(tmp_dir, f"{safe_id}.pdf")
    md_path  = os.path.join(tmp_dir, f"{safe_id}.md")

    if not os.path.exists(pdf_path):
        try:
            req = urllib.request.Request(pdf_url,
                                         headers={"User-Agent": "owl/3.0"})
            with urllib.request.urlopen(req, timeout=30) as resp, \
                 open(pdf_path, "wb") as fout:
                fout.write(resp.read())
        except Exception as e:
            err(f"download failed for {arxiv_id}: {e}")
            return ""

    if not os.path.exists(md_path):
        try:
            from markitdown import MarkItDown
            result = MarkItDown().convert(pdf_path)
            text   = result.text_content or ""
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(text)
        except ImportError:
            try:
                proc = subprocess.run(
                    ["markitdown", pdf_path, "-o", md_path],
                    capture_output=True, text=True, timeout=60,
                )
                if proc.returncode != 0:
                    err(f"markitdown CLI error: {proc.stderr[:100]}")
                    return ""
            except FileNotFoundError:
                err("markitdown not installed — run: pip install markitdown")
                return ""
        except Exception as e:
            err(f"markitdown failed: {e}")
            return ""

    try:
        with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        text = re.sub(r"\n{4,}", "\n\n\n", text)
        text = re.sub(r" {3,}", "  ", text)
        return text[:max_chars]
    except Exception as e:
        err(f"could not read markdown for {arxiv_id}: {e}")
        return ""


def pdf_to_markdown_full(arxiv_id: str,
                         tmp_dir: str = "/tmp/owl_papers",
                         max_chars: int = 40_000) -> str:
    """Return as much of the converted markdown as possible for the final 2 papers."""
    #md_path = os.path.join(tmp_dir, f"{re.sub(r'[^\\w.-]', '_', arxiv_id)}.md")
    safe_id = re.sub(r'[^\w.-]', '_', arxiv_id)
    md_path = os.path.join(tmp_dir, f"{safe_id}.md")
    if not os.path.exists(md_path):
        return ""
    try:
        with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        text = re.sub(r"\n{4,}", "\n\n\n", text)
        text = re.sub(r" {3,}", "  ", text)
        return text[:max_chars]
    except Exception:
        return ""


# ── Google / Serper ───────────────────────────────────────────────────────────

def search_google(query: str, api_key: str, n: int = 5) -> list[dict]:
    conn = http.client.HTTPSConnection("google.serper.dev")
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    payload = json.dumps({"q": query, "num": n})
    try:
        conn.request("POST", "/search", payload, headers)
        res  = conn.getresponse()
        body = res.read().decode("utf-8")
    except Exception as e:
        err(f"Serper request failed: {e}")
        return []
    finally:
        conn.close()

    if res.status != 200:
        err(f"Serper HTTP {res.status}")
        return []

    data    = json.loads(body)
    results = []
    if ab := data.get("answerBox"):
        snippet = ab.get("answer") or ab.get("snippet") or ""
        if snippet:
            results.append(dict(title=ab.get("title","Answer"), snippet=snippet,
                                url="", label="AnswerBox"))
    for i, r in enumerate(data.get("organic", [])[:n], 1):
        results.append(dict(
            label=f"W{i}", title=r.get("title",""),
            snippet=r.get("snippet",""), url=r.get("link",""),
        ))
    return results





def fetch_page(url: str, max_chars: int = 5000) -> str:
    if not url or not url.startswith("http"):
        return ""

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(req, timeout=12) as resp:
            data = resp.read(100_000)

            # ✅ 处理 gzip
            if resp.headers.get("Content-Encoding") == "gzip":
                data = gzip.decompress(data)

            # ✅ 自动编码检测（简单版）
            try:
                raw = data.decode("utf-8")
            except UnicodeDecodeError:
                raw = data.decode("latin-1", errors="ignore")

        # ✅ 去 script/style
        raw = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.S | re.I)
        raw = re.sub(r"<style[^>]*>.*?</style>", " ", raw, flags=re.S | re.I)

        # ✅ 去 HTML 标签
        raw = re.sub(r"<[^>]+>", " ", raw)

        # ✅ 清理空白
        raw = re.sub(r"\s+", " ", raw).strip()

        return raw[:max_chars]

    except Exception as e:
        print(f"[fetch_page error] {url}: {e}")
        return ""

# ── Claude API ────────────────────────────────────────────────────────────────

_FALLBACK_MODEL  = "claude-sonnet-4-20250514"
_SELECTION_MODEL = "claude-opus-4-20250514"   # preferred for step 4 judgement
_resolved_model: str | None = None            # cached after first resolution


def resolve_model(key: str) -> str:
    """
    Query the Anthropic models list and return the best available model for
    paper selection (prefers Opus > Sonnet by capability tier).
    Result is cached for the lifetime of the process.
    """
    global _resolved_model
    if _resolved_model:
        return _resolved_model

    try:
        conn = http.client.HTTPSConnection("api.anthropic.com")
        conn.request("GET", "/v1/models", headers={
            "x-api-key":         key,
            "anthropic-version": "2023-06-01",
        })
        resp = conn.getresponse()
        if resp.status == 200:
            data   = json.loads(resp.read().decode())
            models = [m["id"] for m in data.get("data", [])]
            conn.close()
            # Prefer opus → sonnet → fallback
            for preferred in (_SELECTION_MODEL, _FALLBACK_MODEL):
                if any(preferred in m for m in models):
                    _resolved_model = preferred
                    return _resolved_model
            # Use first available model from the list
            if models:
                _resolved_model = models[0]
                return _resolved_model
        conn.close()
    except Exception:
        pass

    _resolved_model = _FALLBACK_MODEL
    return _resolved_model


def call_claude(prompt: str, key: str,
                max_tokens: int = 2048, stream: bool = False,
                model: str | None = None) -> str:
    
    payload = json.dumps({
        "model":      model,
        "max_tokens": max_tokens,
        "messages":   [{"role": "user", "content": prompt}],
        "reasoning": {"enabled": True}
    })
    
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError("No API key provided and OPENROUTER_API_KEY is not set.")

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=payload
    )
    
    response.raise_for_status()
    #print(response.status_code)
    data = response.json()
    #print(data['choices'][0]['message'])
    return data['choices'][0]['message']['content']


def call_claude_json(prompt: str, key: str, model: str | None = None) -> dict:
    """Call Claude and parse the response as JSON (no streaming)."""
    raw = call_claude(prompt, key, stream=False, model=model)
    try:
        clean = re.sub(r"```json|```", "", raw).strip()
        return json.loads(clean)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}|\[.*\]", raw, re.S)
        if m:
            return json.loads(m.group())
        return {}


# ── Step 4: LLM selects best 2 papers ────────────────────────────────────────

def select_best_papers(query: str, papers: list[dict], key: str) -> tuple[list[dict], str, str]:
    """
    Resolve the best available model via the Anthropic API, then ask it to
    pick the 2 most relevant papers and explain why.
    Returns (selected_papers, explanation_text, model_used).
    """
    #model = resolve_model(key)
    model = "anthropic/claude-sonnet-4.6"

    parts = [
        f"Research topic: {query}\n",
        "Below are 5 arXiv papers. Based on the title, abstract, and introduction "
        "of each, select the 2 most relevant and high-quality papers for this topic.\n",
    ]
    for i, p in enumerate(papers, 1):
        authors = ", ".join(p.get("authors", [])[:3])
        content = p.get("intro_text") or p.get("abstract", "(no abstract)")
        parts.append(f"\n--- Paper {i} ---")
        parts.append(f"Title    : {p['title']}")
        parts.append(f"Authors  : {authors}")
        parts.append(f"Published: {p.get('published','')}")
        parts.append(f"Abstract + Intro:\n{content[:2000]}")

    parts.append("""
---
Respond ONLY with valid JSON in this exact format (no markdown, no explanation outside JSON):
{
  "selected": [1, 3],
  "reason_1": "One sentence why paper 1 was selected.",
  "reason_2": "One sentence why paper 3 was selected.",
  "dropped": "One sentence on why the other 3 were less relevant."
}
""")
    prompt = "\n".join(parts)
    result = call_claude_json(prompt, key, model=model)

    selected_indices = result.get("selected", [1, 2])
    selected = [papers[i - 1] for i in selected_indices if 1 <= i <= len(papers)]
    if len(selected) < 2:
        selected = papers[:2]

    explanation = (
        f"Kept paper {selected_indices[0]}: {result.get('reason_1','')}\n"
        f"Kept paper {selected_indices[1]}: {result.get('reason_2','')}\n"
        f"Dropped others: {result.get('dropped','')}"
    )
    return selected, explanation, model



def build_summary_prompt(query: str, papers: list[dict], web_results: dict[str, list]) -> str:
    parts = [
        f"You are OWL, an expert research analyst.\n",
        f"Topic: {query}\n",
        "=" * 70,
        "PAPERS (title + abstract + intro + full text where available)",
        "=" * 70,
    ]

    for i, p in enumerate(papers, 1):
        authors = ", ".join(p.get("authors", [])[:4])
        parts.append(f"\n[P{i}] {p['title']}")
        parts.append(f"Authors  : {authors}  |  Published: {p.get('published','')}")
        parts.append(f"URL      : {p.get('url','')}")
        parts.append(f"PDF      : {p.get('pdf_url','')}")
        full = p.get("full_text", "")
        if full:
            parts.append(f"\nFull text (from PDF via markitdown):\n{full}")
        else:
            parts.append(f"\nAbstract:\n{p.get('abstract','')}")
        parts.append("-" * 60)

    parts += ["\n" + "=" * 70, "WEB SEARCH RESULTS", "=" * 70]

    for search_type, results in web_results.items():
        parts.append(f"\n── {search_type.upper()} SEARCH ──")
        for r in results:
            parts.append(f"\n[{r['label']}] {r['title']}")
            if r.get("url"):   parts.append(f"URL    : {r['url']}")
            if r.get("snippet"): parts.append(f"Snippet: {r['snippet']}")
            if r.get("page_content"): parts.append(f"Content:\n{r['page_content']}")
            parts.append("")

    parts += [
        "\n" + "=" * 70,
        "YOUR TASK",
        "=" * 70,
        f"""
Write a research summary with exactly this structure:

# 🦉 OWL Research Summary: {query}
*{datetime.now().strftime("%Y-%m-%d")} · 2 papers · 4 web searches*

## Selected Papers

**[P1] {papers[0]['title'] if papers else 'Paper 1'}**
Authors: ...  |  {papers[0].get('published','') if papers else ''}
🔗 {papers[0].get('url','') if papers else ''}  |  📄 {papers[0].get('pdf_url','') if papers else ''}

**[P2] {papers[1]['title'] if len(papers) > 1 else 'Paper 2'}**
Authors: ...  |  {papers[1].get('published','') if len(papers) > 1 else ''}
🔗 {papers[1].get('url','') if len(papers) > 1 else ''}  |  📄 {papers[1].get('pdf_url','') if len(papers) > 1 else ''}

## 5-Bullet Summary

Write exactly 5 bullets. Each bullet must:
- Be 3–5 sentences long
- Include at least one specific fact, number, method name, or result from the sources
- Reference sources inline: [P1], [P2], or [W1]-[W4] etc.
- Cover a different aspect: e.g. what it is / how it works / key results / tools/repos / open questions

• **[Bullet title]**: ...
• **[Bullet title]**: ...
• **[Bullet title]**: ...
• **[Bullet title]**: ...
• **[Bullet title]**: ...

## Web Sources

List each web result with title and URL.

---
Rules:
- Only use facts from the provided material — no invention
- Every bullet must cite at least one source
- The 5 bullets are the centrepiece — make them dense, specific, and informative
""",
    ]
    return "\n".join(parts)


# ── CLI ───────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="owl",
        description="6-step research: arXiv → read 5 papers → keep best 2 → web search → 5-bullet summary",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
steps:
  1  Search arXiv for the topic
  2  Open 5 promising papers (PDF → markitdown)
  3  Read title + abstract + intro of each
  4  Claude keeps the best 2 (explains reasoning)
  5  Search web: explanation · GitHub · survey · citations
  6  Write a 5-bullet summary of what was learned

examples:
  owl "diffusion models"
  owl "LoRA fine-tuning" --category cs.LG --output report.md
  owl "protein structure prediction" --since year
  owl "quantum error correction" --arxiv-n 8

environment:
  SERPER_API_KEY     Serper.dev API key
  ANTHROPIC_API_KEY  Anthropic API key
        """
    )
    p.add_argument("query",           nargs="+",           help="research topic")
    p.add_argument("--arxiv-n",       type=int, default=5, metavar="N",
                   help="arXiv candidates to fetch before selection (default: 5)")
    p.add_argument("--category",      default="",          metavar="CAT",
                   help="arXiv category filter, e.g. cs.LG")
    p.add_argument("--sort",          default="relevance",
                   choices=["relevance", "lastUpdatedDate", "submittedDate"])
    p.add_argument("--since",         default="",          metavar="RANGE",
                   help="Google time filter: hour|day|week|month|year")
    p.add_argument("--papers-dir",    default="/tmp/owl_papers", metavar="DIR",
                   help="cache directory for PDFs and markdown files")
    p.add_argument("--serper-key",    default="",          metavar="KEY")
    p.add_argument("--anthropic-key", default="",          metavar="KEY")
    p.add_argument("--output",        default="",          metavar="FILE",
                   help="save summary to FILE (e.g. report.md)")
    p.add_argument("--no-stream",     action="store_true",
                   help="disable streaming for final summary")
    return p


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    #_SERPER_BUNDLED = "7fc2aa"

    parser = build_parser()
    args   = parser.parse_args()

    query         = " ".join(args.query)
    serper_key    = args.serper_key    or os.environ.get("SERPER_API_KEY", "")
    #anthropic_key = args.anthropic_key or os.environ.get("ANTHROPIC_API_KEY", "")

    if not serper_key:
        err("No Serper API key. Set SERPER_API_KEY."); sys.exit(1)

    print(BOLD(f"\n🦉 OWL  ·  \"{query}\""))
    print(DIM(  f"    6-step research pipeline\n"))

    # ══════════════════════════════════════════════════════════════════════════
    # Step 1 — Search arXiv
    # ══════════════════════════════════════════════════════════════════════════
    step(1, "Search arXiv")
    candidates = search_arxiv(query, n=args.arxiv_n,
                               category=args.category, sort_by=args.sort)
    if not candidates:
        err("No arXiv results found."); sys.exit(1)
    ok(f"{len(candidates)} papers found")
    for i, p in enumerate(candidates, 1):
        info(f"[{i}] {p['title'][:70]}")

    # ══════════════════════════════════════════════════════════════════════════
    # Step 2 — Open 5 papers (PDF → markitdown)
    # ══════════════════════════════════════════════════════════════════════════
    step(2, "Open promising papers (PDF → Markdown via markitdown)")
    pool = candidates[:5]
    for p in pool:
        print(DIM(f"         · downloading {p['id']}…"), end="", flush=True)
        text = pdf_to_markdown(p["pdf_url"], p["id"],
                                tmp_dir=args.papers_dir, max_chars=8_000)
        if text:
            p["intro_text"] = text
            ok(f"{len(text)//1024} KB  —  {p['title'][:55]}")
        else:
            p["intro_text"] = p["abstract"]
            warn(f"PDF failed, using abstract  —  {p['title'][:50]}")
        time.sleep(0.5)  # be polite to arXiv

    # ══════════════════════════════════════════════════════════════════════════
    # Step 3 — Read title + abstract + intro
    # ══════════════════════════════════════════════════════════════════════════
    step(3, "Read title + abstract + intro of each paper")
    for i, p in enumerate(pool, 1):
        snippet = (p.get("intro_text") or p.get("abstract",""))[:200].replace("\n"," ")
        info(f"[{i}] {p['title'][:60]}")
        info(f"    {snippet}…")

    # ══════════════════════════════════════════════════════════════════════════
    # Step 4 — LLM selects best 2
    # ══════════════════════════════════════════════════════════════════════════
    step(4, "LLM selects the best 2 papers")
    best, explanation, selection_model = select_best_papers(query, pool, None)
    ok(f"Selected {len(best)} papers  (model: {selection_model})")
    for line in explanation.strip().split("\n"):
        info(line)

    # Reload full text for the 2 selected papers
    for p in best:
        full = pdf_to_markdown_full(p["id"], tmp_dir=args.papers_dir, max_chars=40_000)
        if full:
            p["full_text"] = full
            ok(f"Full text loaded for [{p['id']}]  ({len(full)//1024} KB)")

    # ══════════════════════════════════════════════════════════════════════════
    # Step 5 — 4 targeted web searches
    # ══════════════════════════════════════════════════════════════════════════
    step(5, "Web search: explanation · GitHub · survey · citations")

    web_searches = {
        "explanation": f"{query} explained",
        "github":      f"{query} github implementation",
        "survey":      f"{query} survey review paper",
        "citations":   f"{query} highly cited papers results",
    }

    web_results: dict[str, list] = {}
    for search_type, search_query in web_searches.items():
        info(f"[{search_type}]  '{search_query}'")
        results = search_google(search_query, serper_key, n=4)
        # Fetch page content for top 2 results
        for r in results[:2]:
            if r.get("url"):
                content = web_fetcher.quick_fetch(r["url"])
                if content:
                    r["page_content"] = content[:4000]
        web_results[search_type] = results
        ok(f"{len(results)} results for '{search_type}'")
        for r in results[:3]:
            info(f"  · [{r['label']}] {r['title'][:65]}")
        time.sleep(0.3)

    # ══════════════════════════════════════════════════════════════════════════
    # Step 6 — 5-bullet summary
    # ══════════════════════════════════════════════════════════════════════════
    step(6, "Write 5-bullet summary")
    print(DIM("         Claude is reading all sources and writing the summary…\n"))
    print(BOLD("─" * 72))

    prompt  = build_summary_prompt(query, best, web_results)
    summary = call_claude(prompt, None,
                           max_tokens=3000)
    print()
    print(BOLD("─" * 72))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(summary)
        ok(f"Saved → {os.path.abspath(args.output)}")

    # ── Checklist ──────────────────────────────────────────────────────────────
    full_count = sum(1 for p in best if p.get("full_text"))
    web_count  = sum(len(v) for v in web_results.values())
    paper_titles = [p["title"][:55] + "…" if len(p["title"]) > 55 else p["title"]
                    for p in best]

    print()
    print(BOLD("─" * 72))
    print(BOLD("  ✅ RESEARCH CHECKLIST"))
    print(BOLD("─" * 72))
    print(GREEN("  [✓] Step 1") + f"  Search arXiv                  {len(candidates)} papers found")
    print(GREEN("  [✓] Step 2") + f"  Open 5 papers via markitdown   {len(pool)} PDFs converted")
    print(GREEN("  [✓] Step 3") + f"  Read title + abstract + intro  {len(pool)} papers scanned")
    print(GREEN("  [✓] Step 4") + f"  Keep best 2                    {len(best)} selected via {selection_model}"
          + (f"  ({full_count} with full text)" if full_count else ""))
    for t in paper_titles:
        print(DIM(f"              → {t}"))
    print(GREEN("  [✓] Step 5") + f"  Web search (4 queries)         {web_count} results fetched")
    for stype, results in web_results.items():
        top = results[0]["title"][:50] if results else "—"
        print(DIM(f"              → {stype:<12}  {top}"))
    print(GREEN("  [✓] Step 6") + f"  5-bullet summary               written by Claude")
    if args.output:
        print(DIM(f"              → {os.path.abspath(args.output)}"))
    print(BOLD("─" * 72))
    print()


if __name__ == "__main__":
    main()
