"""live_smoke_sources.py - Signal-Search 真源联调抽查（一次性，不入 pytest 套件）。

目的：在真实网络下验证两条原生检索域的「门控兜底链路」：
  A) 主传输（scrape._fetch_system_curl，系统 curl 子进程，绕过 TLS 指纹封禁）真通；
  B) 主传输失败时，注入的 web_fetch 兜底回调真被调用、其结果真被消费
     （finance -> citation.source="eastmoney-web"，academic -> citation.source="arxiv-web"）。

运行：signal-search venv 的 python。
"""

import os
import sys
import time

# 项目根目录（本文件位于 <root>/examples/，故上溯两级即为根），避免硬编码本地绝对路径。
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import academic
import finance
import scrape
from common import load_config

cfg = load_config(os.path.join(ROOT, "config.json"))


def banner(t):
    print("\n" + "=" * 64)
    print(t)
    print("=" * 64)


# ---------------------------------------------------------------------------
# PHASE A：真实主路径（web_fetch=None，只走系统 curl）
# ---------------------------------------------------------------------------
banner("PHASE A  REAL PRIMARY PATH  (web_fetch=None, system curl only)")
print("sandbox outbound curl -> East Money push2 / arXiv / Crossref\n")

print("[Finance]  fetch('600519')  (贵州茅台, 沪市 secid=1.600519)")
t0 = time.time()
f_docs, f_warn = finance.fetch("600519", cfg, web_fetch=None)
print(f"  elapsed={time.time()-t0:.1f}s  docs={len(f_docs)}  warnings={f_warn}")
for d in f_docs:
    print("   name =", d.get("name"), " code =", d.get("code"))
    print("   price line =", (d.get("text", "")[:90]).replace("\n", " | "))
    print("   citation =", d.get("citation"))

print("\n[Academic] search('attention is all you need')  (arXiv + Crossref DOI 回填)")
t0 = time.time()
a_docs, a_warn = academic.search("attention is all you need", cfg, web_fetch=None)
print(f"  elapsed={time.time()-t0:.1f}s  docs={len(a_docs)}  warnings={a_warn}")
for d in a_docs[:3]:
    print("   title =", (d.get("title") or "")[:72])
    print("   citation =", d.get("citation"))


# ---------------------------------------------------------------------------
# PHASE B：强制主传输失败，验证 web_fetch 兜底回调真被调用并消费
# ---------------------------------------------------------------------------
banner("PHASE B  FALLBACK WIRING  (primary forced 403 -> web_fetch must fire)")
_real = scrape._fetch_system_curl


def _fail(url, headers=None, data=None, timeout=12):
    return 403, None, ""  # 模拟东方财富/arXiv 反爬拦截


scrape._fetch_system_curl = _fail

print("[Finance]  primary fails -> web_fetch shim 期望被调用, 结果入 eastmoney-web")
calls = [0]


def _shim(url):
    calls[0] += 1
    return f"<html>eastmoney fallback for {url}</html>"


f_docs, f_warn = finance.fetch("600519", cfg, web_fetch=_shim)
print(f"  web_fetch called = {calls[0]}  docs = {len(f_docs)}  warnings = {f_warn}")
if f_docs:
    print(
        "   citation.source =",
        f_docs[0]["citation"]["source"],
        "| key =",
        f_docs[0]["citation"]["key"],
    )

print("\n[Academic] primary fails -> web_fetch shim 期望被调用, 结果入 arxiv-web")
calls = [0]


def _shim2(url):
    calls[0] += 1
    return f"<html>arxiv fallback for {url}</html>"


a_docs, a_warn = academic.search("attention is all you need", cfg, web_fetch=_shim2)
print(f"  web_fetch called = {calls[0]}  docs = {len(a_docs)}  warnings = {a_warn}")
if a_docs:
    print(
        "   citation.source =",
        a_docs[0]["citation"]["source"],
        "| source url =",
        a_docs[0].get("url"),
    )

scrape._fetch_system_curl = _real
print("\n[done] primary transport restored.")
