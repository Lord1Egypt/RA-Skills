"""Stockquant skill - A-share trading all-in-one (quotes / k-line / picker / sell-plan).

Merges the old `stockpicker` (selection) + `stock` (quote+kline) skills.
No watchlist persistence: holdings are always supplied by the caller (host
module passes `code:qty/avail@cost` triples to `sell-plan`). The skill is
broker-agnostic; it returns text recommendations and machine-readable
ORDER signature lines, but never talks to any specific brokerage client.

Strategies:
  A - Low-suction on divergence after recent limit-up (main).
  B - Oversold bounce after recent limit-down (auxiliary).

Data source: East Money public endpoints (push2.eastmoney.com,
push2ex.eastmoney.com) -- no key required.

CLI (常用):
  python stockquant.py --capital 10000 --market main --top 30   # 选股 (brief, 默认)
  python stockquant.py quote <code> [<code>...]                 # 现价
  python stockquant.py kline <code> [--period day|week|month] [--count 30]
  python stockquant.py sell-plan <code>:<qty>@<cost> [...]      # 持仓策略建议
    e.g. sell-plan 000949:1200@7.97 002324:500@17.11 603057:300@28.29
  python stockquant.py intraday-track                            # 盘中跟踪今日推荐的实时表现

CLI (调试子命令, 任务中不用):
  python stockquant.py market
  python stockquant.py sector-rank [--type industry|concept] [--top 20]
  python stockquant.py zt-pool|dt-pool|zb-pool|lb-pool [--date YYYYMMDD]
  python stockquant.py screen-a [--days 2] [--market all|main|gem|star]
  python stockquant.py screen-b [--days 2] [--min-rebound 5.0]
  python stockquant.py score <code...> [--strategy A|B]
  python stockquant.py recommend [--capital 10000] [--market main] \\
                                 [--strategy A,B] [--threshold 5] [--top 30]
  python stockquant.py eval [--date YYYYMMDD]                    # T+1 复盘 (次日 K 线)
  python stockquant.py stats [--days 30]                         # 近 N 日策略统计
"""
import sys
import os
import json
import time
import math
import random
import re
import shutil
import argparse
import datetime
import requests
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor, as_completed

# Force UTF-8 stdout/stderr so emoji and CJK print on Windows (GBK) terminals
# and when captured as subprocess by the Android agent harness.
try:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ==========================================================================
# Global constants
# ==========================================================================
TIMEOUT = 15
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.dirname(_SCRIPT_DIR)           # .../stockquant/
_CACHE_DIR = os.path.join(_SKILL_DIR, "cache")
_WS_DIR = os.path.dirname(os.path.dirname(_SKILL_DIR))  # .../workspace/ (for node_modules)
_H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
_REF_EM = "https://finance.eastmoney.com"

# East Money market-filter ("fs") expressions
_FS_ALL_A = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23"     # all A-share: main+gem+star
_FS_MAIN  = "m:0+t:6,m:1+t:2"                        # SH + SZ main board
_FS_GEM   = "m:0+t:13"                               # ChiNext
_FS_STAR  = "m:1+t:23"                               # STAR market
_FS_SH    = "m:1+t:2,m:1+t:23"                       # all Shanghai A
_FS_SZ    = "m:0+t:6,m:0+t:13"                       # all Shenzhen A

_MARKET_FS_MAP = {
    "all":     _FS_ALL_A,
    "main":    _FS_MAIN,
    "gem":     _FS_GEM,
    "star":    _FS_STAR,
    "sh":      _FS_SH,
    "sz":      _FS_SZ,
    "main_sh": "m:1+t:2",
    "main_sz": "m:0+t:6",
}

# Bad-news title patterns (used by strategy B to filter land-mine stocks).
# Match is case-sensitive substring ("in" operator). Prefer high-precision
# phrases to avoid false positives (don't just use "诉讼" or "辞职").
_BAD_NEWS_PATTERNS = [
    # Shareholder reduce / block-trade sell-off
    "减持计划", "减持股份", "计划减持", "拟减持", "询价转让",
    "被动减持", "减持进展",
    # Regulatory investigation / punishment
    "被立案", "立案调查", "立案通知书", "涉嫌信息披露违法",
    "涉嫌违法违规", "涉嫌内幕", "涉嫌操纵",
    "行政处罚", "处罚决定", "监管措施", "警示函", "通报批评", "公开谴责",
    # Earnings disaster
    "业绩预亏", "业绩预减", "预计亏损", "亏损预告", "首亏", "续亏",
    "业绩大幅下滑", "持续经营能力",
    # Asset / goodwill impairment (prefer "计提"/"准备" prefixes to avoid false
    # positives from "减值测试报告" routine compliance announcements)
    "商誉减值", "计提减值", "减值准备", "大额减值",
    # Share freeze / margin-call
    "股份被冻结", "司法冻结", "股权被冻结", "股份被司法",
    "质押平仓", "质押违约", "股份被强制",
    # Delisting / ST risk
    "退市风险警示", "退市整理", "终止上市", "被实施退市",
    "实施其他风险警示", "实施风险警示", "被实施ST", "被实施*ST",
    # Controlling shareholder / exec issues
    "控股股东被立案", "实际控制人被立案", "被执行人", "限制消费令",
    "失信被执行",
]

# Major A-share indexes (secid, display name)
_INDEX_LIST = [
    ("1.000001", "上证指数"),
    ("0.399001", "深证成指"),
    ("0.399006", "创业板指"),
    ("1.000688", "科创50"),
    ("1.000016", "上证50"),
    ("0.399300", "沪深300"),
]


# ==========================================================================
# Cache helpers - per-day JSON under ${SKILL_DIR}/stockquant/cache/YYYYMMDD/
# ==========================================================================

def _today():
    return datetime.datetime.now().strftime("%Y%m%d")


def _cache_path(name, date=None):
    d = date or _today()
    sub = os.path.join(_CACHE_DIR, d)
    os.makedirs(sub, exist_ok=True)
    return os.path.join(sub, name)


def _cache_get(name, date=None, ttl_sec=None):
    """Read cache. If ttl_sec given, return None when file older than ttl."""
    p = _cache_path(name, date)
    if not os.path.exists(p):
        return None
    if ttl_sec is not None:
        age = time.time() - os.path.getmtime(p)
        if age > ttl_sec:
            return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _cache_set(name, data, date=None):
    p = _cache_path(name, date)
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        print(f"WARN: cache write failed: {e}", file=sys.stderr)


def _cache_get_stale(name, max_days=3):
    """Read the most recent cache entry across the last `max_days` day-dirs,
    ignoring TTL. Used as a last-resort fallback when upstream APIs are down.

    Returns (data, cache_date_str) or (None, None) if nothing found.
    Looks today first, then today-1, today-2 ... up to max_days back.
    """
    today = datetime.datetime.now()
    for delta in range(max_days + 1):
        d = (today - datetime.timedelta(days=delta)).strftime("%Y%m%d")
        p = os.path.join(_CACHE_DIR, d, name)
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f), d
            except Exception:
                continue
    return None, None


# Auto-GC: called once at CLI startup. Keeps only cache/YYYYMMDD/ dirs within
# the last `keep_days` days. Non-date subdirs are left alone. Failures are
# swallowed silently -- stale cache is not a correctness issue.
_CACHE_KEEP_DAYS = 7

def _gc_cache(keep_days=_CACHE_KEEP_DAYS):
    if not os.path.isdir(_CACHE_DIR):
        return
    cutoff = (
        datetime.datetime.now() - datetime.timedelta(days=keep_days)
    ).strftime("%Y%m%d")
    try:
        entries = os.listdir(_CACHE_DIR)
    except Exception:
        return
    removed = 0
    for name in entries:
        # Only touch dirs whose name looks like YYYYMMDD
        if len(name) != 8 or not name.isdigit():
            continue
        if name >= cutoff:
            continue
        full = os.path.join(_CACHE_DIR, name)
        if not os.path.isdir(full):
            continue
        try:
            shutil.rmtree(full)
            removed += 1
        except Exception as e:
            print(f"WARN: cache gc failed for {name}: {e}", file=sys.stderr)
    if removed:
        print(
            f"INFO: cache gc removed {removed} stale day-dirs (keep={keep_days}d)",
            file=sys.stderr,
        )


# ==========================================================================
# HTTP helper -- module-level requests.Session for connection pooling.
#
# Why Session: East Money's push2 endpoints tend to reject new TCP connections
# opened in bursts (typical RemoteDisconnected symptom). Sharing a keep-alive
# pool dramatically reduces that friction. The HTTPAdapter is mounted with a
# generous pool size so the ThreadPoolExecutor used by kline/batch-quote
# fetchers can reuse sockets without contention.
# ==========================================================================

_SESSION = requests.Session()
_ADAPTER = HTTPAdapter(pool_connections=8, pool_maxsize=32)
_SESSION.mount("http://", _ADAPTER)
_SESSION.mount("https://", _ADAPTER)
_SESSION.headers.update({**_H, "Referer": _REF_EM})

# Network-layer transient errors (TCP reset / remote disconnected / timeout /
# chunked-encoding mid-response). These deserve aggressive retry even in
# "fast-fail" mode because they're usually upstream pressure, not our fault.
_NET_ERRORS = (
    requests.exceptions.ConnectionError,
    requests.exceptions.Timeout,
    requests.exceptions.ChunkedEncodingError,
)


def _get_json(url, retries=3):
    """GET + JSON parse with exponential-backoff retry. Uses shared session.
    Backoff: 0.8s, 1.6s, 3.2s + small random jitter to avoid lock-step
    retries slamming the upstream at the same moment.
    """
    last_err = None
    for i in range(retries + 1):
        try:
            r = _SESSION.get(url, timeout=TIMEOUT)
            return r.json()
        except Exception as e:
            last_err = e
            if i < retries:
                time.sleep(0.8 * (2 ** i) + random.random() * 0.3)
    raise RuntimeError(f"fetch failed: {url[:120]}... err={last_err}")


def _get_json_fast_fail(url, retries=1):
    """Fast-fail variant that distinguishes network-layer vs HTTP-layer errors.

    - Network-layer transients (RemoteDisconnected / ConnectionError /
      Timeout / ChunkedEncoding): retried up to 3 times with 0.5/1.0/2.0s
      backoff + jitter. East Money's push2 commonly drops connections under
      load; retrying these is almost always worth it.
    - Other errors (HTTP 4xx/5xx / JSON parse): short-circuit after `retries`
      attempts with 0.3s backoff. Semantic failures won't heal by waiting.
    """
    last_err = None
    net_attempts = 0
    http_attempts = 0
    net_backoffs = (0.5, 1.0, 2.0)
    while True:
        try:
            r = _SESSION.get(url, timeout=5)
            return r.json()
        except _NET_ERRORS as e:
            last_err = e
            if net_attempts >= len(net_backoffs):
                break
            time.sleep(net_backoffs[net_attempts] + random.random() * 0.2)
            net_attempts += 1
        except Exception as e:
            last_err = e
            if http_attempts >= retries:
                break
            time.sleep(0.3)
            http_attempts += 1
    raise RuntimeError(f"fetch failed (fast): {url[:120]}... err={last_err}")


# ==========================================================================
# Network-layer preflight probe
# ==========================================================================
# Motivation: on real phones / flaky carrier networks the East Money push2
# endpoints can all simultaneously reject TCP (RemoteDisconnected) for 1-3
# minutes. Without a preflight the `recommend` orchestrator burns ~60s
# hitting dead URLs, falls back to whatever partial data slips through, and
# returns 1-2 stocks. That misleads the LLM into placing a single-ticker
# buy when the REAL problem is "data source is down".
#
# The preflight probes 4 canonical endpoints in parallel with 3s timeout:
#   em_clist    -- full-market stock list (used by all screening strategies)
#   em_sector   -- sector ranking (strategy C hard dep)
#   em_kline    -- single-stock kline (strategy E + sell-plan)
#   sina        -- alternate source (used by market-overview / get_market_list
#                  fallback); probing it tells us if at least *any* mainland
#                  finance data path is alive.
#
# Decision ladder: 0 EM alive -> raise hard; 1 EM alive -> warn + continue
# (strategies C/D will likely return []); 2+ EM alive -> continue silently.
# ==========================================================================

_PREFLIGHT_PROBES = {
    "em_clist":  "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=1&fs=m:0+t:6&fields=f12",
    "em_sector": "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=1&fs=m:90+t:2&fields=f12",
    "em_kline":  "http://push2.eastmoney.com/api/qt/stock/kline/get?secid=0.000001&klt=101&lmt=1",
    "sina":      "https://hq.sinajs.cn/list=s_sh000001",
    # webquotepic image service: served from a different EM subdomain than
    # push2 APIs; usually stays alive when push2 gets WAF-throttled. Used
    # purely as a diagnostic signal -- "network is fine, just push2 is
    # rate-limited" vs "phone-level connectivity is dead". Lets the LLM /
    # user distinguish a wait-it-out condition from an unrecoverable one.
    "em_pic":    "http://webquotepic.eastmoney.com/GetPic.aspx?nid=1.000001&imageType=KXL",
    # Tencent QQ stock (qt.gtimg.cn) -- independent upstream. Survives
    # when both EM push2 and Sina are WAF-blocked; different IP range.
    # Used as Tier-2.5 fallback in get_market_list and batch quote path.
    "tencent":   "http://qt.gtimg.cn/q=sz000001",
    # 同花顺 V6 line API (d.10jqka.com.cn) -- independent provider.
    # Returns daily k-line JSONP data; tested alive 2026-05 during
    # EM push2 + Sina dual outage. Used as Tier-5 kline fallback.
    "10jqka":    "http://d.10jqka.com.cn/v6/line/sz_000001/01/last.js",
}


def _preflight_connectivity_check():
    """Parallel probe of core data endpoints; returns {probe_name: 'ok'|'fail'}.

    Each probe is capped at 3s; the whole call finishes in <=5s even when
    every endpoint is stuck. Uses the shared _SESSION so we benefit from
    any existing keep-alive socket.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    def _probe(name, url):
        try:
            r = _SESSION.get(url, timeout=3)
            # Any 2xx/3xx is "ok"; 4xx/5xx treated as fail (API itself is sick).
            if 200 <= r.status_code < 400:
                return (name, "ok")
            return (name, f"fail(http{r.status_code})")
        except Exception as e:
            return (name, f"fail({type(e).__name__})")

    results = {}
    with ThreadPoolExecutor(max_workers=len(_PREFLIGHT_PROBES)) as ex:
        futures = [ex.submit(_probe, n, u) for n, u in _PREFLIGHT_PROBES.items()]
        try:
            for f in as_completed(futures, timeout=5):
                try:
                    name, status = f.result()
                    results[name] = status
                except Exception as e:
                    # Record unexpected future-level error; don't crash the probe.
                    results[f"_future_err_{len(results)}"] = f"fail({type(e).__name__})"
        except Exception:
            # Overall timeout; whatever we've collected is returned as-is.
            pass
    # Fill any missing probes as fail (probe function itself timed out).
    for name in _PREFLIGHT_PROBES:
        results.setdefault(name, "fail(timeout)")
    return results


def _print_data_source_status(probe, ts_tier, ts_info,
                              em_alive, em_data_total,
                              sina_alive, em_pic_alive):
    """Print a structured DATA_SOURCE_STATUS block to stdout.

    Designed to be quoted verbatim by the LLM agent to the user so the
    user understands which sources are live, which got blocked / banned,
    which strategies will run on degraded data, and (when relevant) what
    actions can recover full functionality (set tushare token, switch
    network, wait for WAF cool-down).

    Always printed -- healthy runs make the block tiny ("all primary OK"),
    while degraded runs are explicit about what's missing.
    """
    em_dead = (em_alive == 0)
    em_partial = (0 < em_alive < em_data_total)
    em_full = (em_alive == em_data_total)
    ts_usable = ts_tier in ("basic", "full")
    print()
    print("═══ DATA_SOURCE_STATUS ═══")
    # Primary EM
    if em_full:
        em_line = "PRIMARY (东方财富 push2): OK ({}/{} endpoints)".format(em_alive, em_data_total)
    elif em_partial:
        em_line = "PRIMARY (东方财富 push2): DEGRADED ({}/{} endpoints alive)".format(
            em_alive, em_data_total)
    else:
        if em_pic_alive:
            em_line = "PRIMARY (东方财富 push2): WAF_BLOCKED (限流; webquotepic 仍存活)"
        else:
            em_line = "PRIMARY (东方财富 push2): DEAD (网络层异常)"
    print("  " + em_line)
    # Sina
    sina_line = "SECONDARY (Sina hq): OK" if sina_alive else "SECONDARY (Sina hq): DEAD"
    print("  " + sina_line)
    # Tencent QQ stock (Backup-2.5)
    tx_alive = probe.get("tencent", "fail") == "ok" if probe else False
    tx_line = "BACKUP-2.5 (Tencent qt): OK" if tx_alive else "BACKUP-2.5 (Tencent qt): DEAD"
    print("  " + tx_line)
    # 10jqka kline probe
    jq_alive = probe.get("10jqka", "fail") == "ok" if probe else False
    jq_line = "BACKUP-5 (10jqka kline): OK" if jq_alive else "BACKUP-5 (10jqka kline): DEAD"
    print("  " + jq_line)
    # Tushare
    if ts_tier == "unset":
        ts_line = "TIER2 (tushare): UNSET (未配置 token)"
    elif ts_tier == "skipped":
        ts_line = "TIER2 (tushare): SKIPPED (用户已禁用)"
    elif ts_tier == "auth_failed":
        ts_line = "TIER2 (tushare): AUTH_FAILED ({})".format(ts_info.get("reason", ""))
    elif ts_tier == "network_failed":
        ts_line = "TIER2 (tushare): NETWORK_FAILED ({})".format(ts_info.get("reason", ""))
    elif ts_tier == "basic":
        ts_line = "TIER2 (tushare): READY (basic 120pt; daily/snapshot ok, moneyflow gated)"
    elif ts_tier == "full":
        ts_line = "TIER2 (tushare): READY (full 2000pt; daily + moneyflow ok)"
    elif ts_tier == "probe_failed":
        ts_line = "TIER2 (tushare): PROBE_FAILED ({})".format(ts_info.get("reason", ""))
    else:
        ts_line = "TIER2 (tushare): {}".format(ts_tier)
    print("  " + ts_line)
    # Strategy availability summary -- only print when degraded.
    if not em_full:
        print()
        print("[策略影响]")
        if em_dead:
            if ts_usable:
                # Tushare substitutes
                snap_via = "tushare snapshot"
                sector_via = "tushare 行业聚合"
                # D-strategy: tushare full has moneyflow API; basic tier
                # falls back to Sina vip per-stock parallel enrichment
                # (top-500 by amount, ~12s, REAL 5d cumulative).
                if ts_tier == "full":
                    inflow_status = "tushare moneyflow 5日聚合"
                else:
                    inflow_status = "Sina vip 单股资金流并行 (top-500, ~12s, real 5d)"
                kline_via = "tushare daily (Tier-4 已有)"
                print(f"  C 板块滞涨: USE {sector_via} (T-1 基础, 板块定义≈申万行业)")
                print(f"  D 主力资金: USE {inflow_status}")
                print(f"  E 箱体突破: USE {snap_via} + {kline_via}")
            elif sina_alive:
                snap_via_2 = "Tencent qt batch (Tier-2.5, ~5s, full fields)"
                print("  C 板块滞涨: SKIPPED (无板块替代源, Sina 不提供)")
                print("  D 主力资金: USE Sina vip 单股资金流并行 (top-500, ~12s, real 5d)")
                print(f"  E 箱体突破: USE {snap_via_2}")
            elif tx_alive:
                print("  C 板块滞涨: SKIPPED (无板块替代源)")
                print("  D 主力资金: SKIPPED (Tencent 不提供主力)")
                print("  E 箱体突破: USE Tencent qt batch (Tier-2.5, ~5s, 有换手率)")
            # else: NETWORK_DEAD branch already raised above
        else:
            # em_partial -- some EM endpoints alive, others not
            if probe.get("em_clist") != "ok":
                print("  ⚠️ em_clist 挂; 全市场快照将走 stale-cache → tushare → Sina → Tencent")
            if probe.get("em_sector") != "ok":
                print("  ⚠️ em_sector 挂; C 策略将走 stale-cache → tushare 行业聚合")
            if probe.get("em_kline") != "ok":
                print("  ⚠️ em_kline 挂; K线将走 Sina/Tencent QT/EM-quote/tushare daily 链")
        # Action hint
        print()
        print("[行动建议]")
        if em_dead and not ts_usable:
            if ts_tier in ("unset", "skipped"):
                print("  → 立即配置 tushare token 解锁 Tier-2 全市场替代:")
                print("    `python ${SKILL_DIR}/stockquant/scripts/stockquant.py "
                      "tushare-token --set <YOUR_TOKEN>`")
                print("    (注册 tushare.pro 即送 120 积分; 实名+学校单位可到 2000)")
            elif ts_tier == "auth_failed":
                print("  → 重新设置 tushare token (当前 token 鉴权失败):")
                print("    `python ${SKILL_DIR}/stockquant/scripts/stockquant.py "
                      "tushare-token --set <NEW_TOKEN>`")
        elif em_dead and ts_tier == "basic":
            print("  ℹ️ 当前 tushare basic tier 仅支持 C/E; 若需 D 策略请升级到 2000 积分")
            print("    (tushare.pro 个人中心填实名/学校/单位可申请加分)")
    # Always print closer for easy parsing.
    print("═══════════════════════════")
    print()


# ==========================================================================
# Low-level East Money fetchers
# ==========================================================================

def _fetch_pool(kind, date=None):
    """East Money pool endpoint. kind: zt|dt|zb|lb."""
    path = {
        "zt": "getTopicZTPool",
        "dt": "getTopicDTPool",
        "zb": "getTopicZBPool",
        "lb": "getTopicLBPool",
    }[kind]
    sort_by = {
        "zt": "fbt:asc",
        "dt": "fund:desc",
        "zb": "fbt:asc",
        "lb": "lbc:desc",
    }[kind]
    d = date or _today()
    url = (
        f"http://push2ex.eastmoney.com/{path}?"
        f"ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.ztzt"
        f"&Pageindex=0&pagesize=800&sort={sort_by}&date={d}"
    )
    js = _get_json(url)
    return (js or {}).get("data") or {}


def _fetch_market_list(fs, page_size=100):
    """Fetch full A-share market list via EM clist/get, auto-paginating.

    EM clist/get enforces a hard 100-row limit per page regardless of pz.
    We paginate until we have all rows (total reported in first response).

    Partial-success policy: if an individual page raises (typically a
    RemoteDisconnected mid-stream), we skip that page and continue instead
    of aborting the whole fetch. After `max_consecutive_fails` consecutive
    page failures we give up -- at that point we're almost certainly
    WAF-banned and further retries just make it worse. The fetched prefix
    is still returned so downstream can salvage what it has.
    Page 1 failure is treated as a hard error: without a valid `total`
    we can't size the job, and an empty prefix is useless.
    """
    fields = "f2,f3,f5,f6,f7,f8,f9,f10,f12,f14,f15,f16,f17,f18,f20,f21,f62,f100,f103"
    rows = []
    pn = 1
    total = None
    consecutive_fails = 0
    max_consecutive_fails = 3
    last_page_err = None
    while True:
        url = (
            f"http://push2.eastmoney.com/api/qt/clist/get?"
            f"pn={pn}&pz={page_size}&po=1&np=1&fltt=2&invt=2"
            f"&fs={fs}&fid=f3&fields={fields}"
        )
        try:
            js = _get_json(url)
        except Exception as e:
            last_page_err = e
            if pn == 1:
                raise                                      # page 1 fatal -- no total, no prefix
            consecutive_fails += 1
            print(f"WARN: clist page {pn} failed ({type(e).__name__}); skip",
                  file=sys.stderr)
            if consecutive_fails >= max_consecutive_fails:
                print(f"WARN: clist aborted after {consecutive_fails} consecutive "
                      f"page failures (last: {e}); returning partial "
                      f"{len(rows)} rows", file=sys.stderr)
                break
            pn += 1
            time.sleep(0.3 + random.random() * 0.3)        # back off a bit before next page
            continue
        consecutive_fails = 0
        d = (js or {}).get("data") or {}
        batch = d.get("diff") or []
        if not batch:
            break
        rows.extend(batch)
        if total is None:
            total = int(d.get("total") or 0)
        # Stop when we have fetched all, or response under page_size
        if len(rows) >= total or len(batch) < page_size:
            break
        pn += 1
        if pn > 80:                                       # hard safety cap (~8000 rows)
            break
        # Throttle to avoid EM WAF rate-limit; jitter so parallel runs
        # from different machines/times don't lock-step.
        time.sleep(0.08 + random.random() * 0.12)
    return rows


def _fetch_sector_rank(sector_type="industry", top=30, fast_fail=False):
    """Industry (m:90+t:2) or concept (m:90+t:3) sector ranking.

    Fields include multi-day pct columns (f164=5d, f167=10d, f170=20d) which
    EM clist exposes natively; these are used as a Tier-1.5 fallback when
    the dedicated sector K-line endpoint is unreachable, avoiding the
    "same-day pct as N-day approximation" degradation in strategy C.
    """
    t_code = {"industry": "2", "concept": "3", "region": "1"}.get(sector_type, "2")
    fs = f"m:90+t:{t_code}"
    # f164=5d pct, f167=10d pct, f170=20d pct (EM board/index convention)
    fields = "f2,f3,f4,f12,f14,f62,f104,f105,f128,f136,f164,f167,f170"
    url = (
        f"http://push2.eastmoney.com/api/qt/clist/get?"
        f"pn=1&pz={top}&po=1&np=1&fltt=2&invt=2"
        f"&fs={fs}&fid=f3&fields={fields}"
    )
    js = _get_json_fast_fail(url) if fast_fail else _get_json(url)
    d = (js or {}).get("data") or {}
    return d.get("diff") or []


def _fetch_index(secid):
    url = (
        f"http://push2.eastmoney.com/api/qt/stock/get?"
        f"secid={secid}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f59,f60,f170,f171"
    )
    js = _get_json(url)
    return (js or {}).get("data")


def _fetch_sina_indexes(sids):
    """Batch fetch indexes via Sina `hq.sinajs.cn/list=s_xxx`.

    Fallback for _fetch_index when EM push2 is down. Sina's s_* format:
        var hq_str_s_sh000001="上证指数,4099.235,-7.020,-0.17,47529685,475296";
    Fields: [name, price, change_v, pct, vol_shou, amount_wanyuan]

    Args:
      sids: list of EM-style secids like "1.000001" (market.code).
            "1.*" -> SH, "0.*" -> SZ.
    Returns:
      dict {sid: {name, price, change, pct, vol, amount_yuan}};
      missing sids absent from dict (partial OK).
    """
    if not sids:
        return {}
    # Build sid -> sina symbol map
    sina_sym_map = {}
    for sid in sids:
        try:
            m, c = sid.split(".", 1)
            prefix = "s_sh" if m == "1" else "s_sz"
            sina_sym_map[sid] = f"{prefix}{c}"
        except ValueError:
            continue
    if not sina_sym_map:
        return {}
    url = "https://hq.sinajs.cn/list=" + ",".join(sina_sym_map.values())
    try:
        r = requests.get(
            url,
            headers={**_H, "Referer": "https://finance.sina.com.cn"},
            timeout=5,
        )
        r.encoding = "gbk"
        text = r.text
    except Exception as e:
        print(f"WARN: Sina index batch failed: {type(e).__name__}", file=sys.stderr)
        return {}
    # Invert map: sina_sym -> sid (for parsing)
    sym_to_sid = {v: k for k, v in sina_sym_map.items()}
    out = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("var hq_str_"):
            continue
        try:
            head, body = line.split("=", 1)
            sym = head[len("var hq_str_"):].strip()
            body = body.strip().strip(";").strip('"')
            if not body:
                continue
            parts = body.split(",")
            if len(parts) < 6:
                continue
            sid = sym_to_sid.get(sym)
            if not sid:
                continue
            out[sid] = {
                "name": parts[0],
                "price": float(parts[1]),
                "change": float(parts[2]),
                "pct": float(parts[3]),
                "vol": float(parts[4]),                    # 手 (100 shares)
                "amount": float(parts[5]) * 10000,         # 万元 -> 元, align with EM f48
            }
        except Exception:
            continue
    return out


def _code_to_em_secid(code):
    """Convert 6-digit A-share code to EM secid (market.code) format."""
    c = code.strip()
    if len(c) != 6 or not c.isdigit():
        return None
    if c[0] == "6" or c.startswith("688"):
        return f"1.{c}"                                    # Shanghai
    return f"0.{c}"                                        # Shenzhen (main/GEM)


def _fetch_market_by_codes(codes, batch_size=100):
    """Quote specific A-share codes via EM ulist.np/get (no WAF risk).

    Far lighter than clist pagination: one 100-code request instead of
    40 clist pages for the whole market. Fields match clist (f2/f3/f6/...)
    so rows are fully compatible with scoring.
    """
    if not codes:
        return []
    fields = ("f2,f3,f5,f6,f7,f8,f9,f10,f12,f14,f15,f16,f17,f18,"
              "f20,f21,f62,f100,f103")
    rows = []
    for i in range(0, len(codes), batch_size):
        chunk = codes[i:i + batch_size]
        secids = [s for s in (_code_to_em_secid(c) for c in chunk) if s]
        if not secids:
            continue
        url = (
            f"http://push2.eastmoney.com/api/qt/ulist.np/get?"
            f"secids={','.join(secids)}&fields={fields}&fltt=2&invt=2"
        )
        js = _get_json(url)
        diff = (js or {}).get("data", {}).get("diff") or []
        for r in diff:
            row = _norm_clist_row(r)
            row["_source"] = "em_ulist"
            rows.append(row)
        if i + batch_size < len(codes):
            time.sleep(0.08)                               # gentle between batches
    return rows


def _code_to_sina(code):
    """Convert 6-digit A-share code to Sina prefix format."""
    c = code.strip()
    if len(c) != 6 or not c.isdigit():
        return None
    # 6/9 = Shanghai; 0/3 = Shenzhen (0 main + 3 GEM + 688 = STAR in sh)
    if c[0] == "6" or c.startswith("688"):
        return f"sh{c}"
    return f"sz{c}"


def _fetch_sina_batch(codes, batch_size=400):
    """Fallback quote source when EM clist is rate-limited.

    Sina returns GBK-encoded JS-var lines. Fields (index):
      0=name, 1=open, 2=prev_close, 3=price, 4=high, 5=low,
      8=volume(shares), 9=amount(yuan), 30=date, 31=time.
    Limitations vs EM clist: no turnover%, no volume_ratio, no main_inflow,
    no float_mv, no industry. These fields are filled with 0/empty so the
    scoring function degrades gracefully (loses some +points but doesn't crash).
    """
    if not codes:
        return []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://finance.sina.com.cn",
    }
    rows = []
    for i in range(0, len(codes), batch_size):
        chunk = codes[i:i + batch_size]
        sina_codes = [s for s in (_code_to_sina(c) for c in chunk) if s]
        if not sina_codes:
            continue
        url = "http://hq.sinajs.cn/list=" + ",".join(sina_codes)
        try:
            r = requests.get(url, headers=headers, timeout=TIMEOUT)
            r.encoding = "gbk"
            text = r.text
        except Exception as e:
            print(f"WARN: sina batch fetch failed: {e}", file=sys.stderr)
            continue
        for line in text.splitlines():
            if '"' not in line:
                continue
            head, _, rest = line.partition('"')
            fields_str, _, _ = rest.rpartition('"')
            if not fields_str:
                continue
            # head like: var hq_str_sh600519=
            var = head.replace("var hq_str_", "").strip().rstrip("=").strip()
            if len(var) < 8:
                continue
            code = var[2:]                                 # strip sh/sz/hk
            parts = fields_str.split(",")
            if len(parts) < 10:
                continue
            prev = _num(parts[2])
            price = _num(parts[3])
            pct = round((price - prev) / prev * 100, 2) if prev > 0 else 0.0
            high = _num(parts[4]); low = _num(parts[5])
            amplitude = round((high - low) / prev * 100, 2) if prev > 0 else 0.0
            rows.append({
                "code": code,
                "name": parts[0],
                "price": round(price, 2),
                "pct": pct,
                "vol": _num(parts[8]),
                "amount": _num(parts[9]),
                "amplitude": amplitude,
                "turnover": 0.0,                           # unavailable in sina
                "pe": 0.0,
                "volume_ratio": 0.0,
                "high": high,
                "low": low,
                "open": _num(parts[1]),
                "prev_close": prev,
                "total_mv": 0.0,
                "float_mv": 0.0,
                "main_inflow": 0.0,
                "industry": "",
                "concept": "",
                "_source": "sina",
            })
        time.sleep(0.05)                                   # gentle on sina
    return rows


def _fetch_tencent_batch(codes, batch_size=100):
    """Tier-2.5 fallback: Tencent QQ stock batch quote (qt.gtimg.cn).

    Independent of EM push2 and Sina; survives when both are WAF-blocked.
    Tencent returns 88 ~-delimited fields per stock. Fields used:
      [0]=market_status(51=正常), [1]=name, [2]=code, [3]=price,
      [4]=prev_close, [5]=open, [6]=vol(手), [31]=change(元),
      [32]=pct(%), [33]=high, [34]=low, [36]=vol(手),
      [37]=amount(万元), [38]=turnover(%), [39]=pe, [43]=amplitude(%),
      [44]=total_mv(亿), [45]=float_mv(亿), [62]=main_inflow(万? varies).

    Limitations vs EM: no volume_ratio, no industry/concept tags.
    These fields are zero-filled so scoring degrades gracefully.
    """
    if not codes:
        return []
    rows = []
    for i in range(0, len(codes), batch_size):
        chunk = codes[i:i + batch_size]
        tx_codes = [s for s in (_code_to_sina(c) for c in chunk) if s]
        if not tx_codes:
            continue
        url = "http://qt.gtimg.cn/q=" + ",".join(tx_codes)
        try:
            r = _SESSION.get(url, timeout=TIMEOUT)
            if r.status_code != 200:
                continue
            r.encoding = "gbk"
            text = r.text
        except Exception as e:
            print(f"WARN: tencent batch fetch failed: {e}", file=sys.stderr)
            continue
        for line in text.splitlines():
            if '"' not in line:
                continue
            # Line format: v_sz000001="51~平安银行~000001~..."
            m = re.search(r'v_(\w+)="(.+?)"', line)
            if not m:
                continue
            code, data = m.group(1), m.group(2)
            code = code[2:]                                # strip sh/sz prefix
            parts = data.split("~")
            if len(parts) < 40:
                continue
            prev = _num(parts[4])
            price = _num(parts[3])
            pct = _num(parts[32])
            high = _num(parts[33])
            low = _num(parts[34])
            # amplitude: use field[43] if present, else compute from high/low
            amp = _num(parts[43]) if len(parts) > 43 else 0.0
            if amp == 0.0 and prev > 0 and high > 0 and low > 0:
                amp = round((high - low) / prev * 100, 2)
            # name: field[1], strip special chars that qt includes
            name = parts[1].strip()
            rows.append({
                "code": code,
                "name": name,
                "price": round(price, 2),
                "pct": pct,
                "vol": _num(parts[6]),                    # 手 -> shares, same as EM
                "amount": round(_num(parts[37]) * 10000, 2) if _num(parts[37]) else 0,
                "amplitude": amp,
                "turnover": _num(parts[38]),
                "pe": _num(parts[39]),
                "volume_ratio": 0.0,                      # unavailable
                "high": high,
                "low": low,
                "open": _num(parts[5]),
                "prev_close": prev,
                # market cap fields are in 亿, convert to 元
                "total_mv": round(_num(parts[45]) * 1e8, 2) if _num(parts[45]) else 0,
                "float_mv": round(_num(parts[44]) * 1e8, 2) if _num(parts[44]) else 0,
                "main_inflow": 0.0,                       # unavailable in tencent
                "industry": "",
                "concept": "",
                "_source": "tencent",
            })
        time.sleep(0.02)                                   # polite to tencent
    return rows


# ==========================================================================
# Default A-share code universe (used as Tier-3 fallback when EM clist is
# down AND no cache AND caller didn't pass fallback_codes).
# ==========================================================================
# Rationale: when the phone loses access to East Money but Sina still
# works, we still want screening to produce *some* candidates. Sina's
# batch API (_fetch_sina_batch) needs an explicit code list, so we
# synthesize one covering the full A-share symbol space. Non-existent
# codes (gaps in the number space) are silently filtered by Sina
# (they return blank fields), so overshooting is cheap -- a 15k probe
# finishes in 10-15s with the default 400/batch.
# ==========================================================================

# Lazily-computed module-level cache so repeated screen_* calls in one
# recommend run don't regenerate the 15k-element list every time.
_DEFAULT_A_SHARE_CODES_CACHE = None


def _build_default_a_share_codes():
    """Generate the canonical A-share 6-digit code universe.

    Ranges covered (rough):
      - 600000-605999  Shanghai main board (incl. 603/605 extensions)
      - 688000-688999  STAR market
      - 000001-003999  Shenzhen main + SME
      - 300000-301999  ChiNext
    Gaps in each range (unlisted codes) are harmless: Sina drops them.
    """
    global _DEFAULT_A_SHARE_CODES_CACHE
    if _DEFAULT_A_SHARE_CODES_CACHE is not None:
        return _DEFAULT_A_SHARE_CODES_CACHE
    codes = []
    for i in range(600000, 606000):
        codes.append(f"{i:06d}")
    for i in range(688000, 689000):
        codes.append(f"{i:06d}")
    for i in range(1, 4000):
        codes.append(f"{i:06d}")
    for i in range(300000, 302000):
        codes.append(f"{i:06d}")
    _DEFAULT_A_SHARE_CODES_CACHE = codes
    return codes


def _fetch_em_announcements(code, page_size=20):
    """Primary source: East Money np-anotice-stock (no key required)."""
    url = (
        f"https://np-anotice-stock.eastmoney.com/api/security/ann?"
        f"page_index=1&page_size={page_size}&ann_type=A&sr=-1"
        f"&stock_list={code}&client_source=web"
    )
    try:
        js = _get_json(url)
    except Exception:
        return []
    return ((js or {}).get("data") or {}).get("list") or []


def _fetch_cninfo_announcements(code, page_size=20):
    """Fallback source: 巨潮资讯 (http://www.cninfo.com.cn). This is the
    official SSE/SZSE-mandated disclosure site -- EM itself scrapes from here,
    so plausibly more authoritative than EM when EM is flaky.

    cninfo's hisAnnouncement/query requires a (code, orgId) pair. orgId
    follows a simple convention for ~99% of A-shares:
      SH (6/688/605/603/601/600) -> "gssh0" + code  column=sse
      SZ (0/3)                    -> "gssz0" + code  column=szse
    For the few exceptions this pattern doesn't match, the endpoint returns
    an empty list -- which is equivalent to "no recent ann" and lets
    has_bad_news fail-open (not worse than the EM-down case).

    Output shape is mapped to match EM's response: [{notice_date, title}].
    """
    c = (code or "").strip()
    if not c.isdigit() or len(c) != 6:
        return []
    if c[0] == "6" or c.startswith("688"):
        org_id = f"gssh0{c}"
        column = "sse"
    else:
        org_id = f"gssz0{c}"
        column = "szse"
    url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
    form = {
        "stock": f"{c},{org_id}",
        "tabName": "fulltext",
        "pageSize": str(page_size),
        "pageNum": "1",
        "column": column,
        "category": "",
        "plate": "",
        "seDate": "",
        "searchkey": "",
        "secid": "",
        "sortName": "",
        "sortType": "",
        "isHistory": "false",
    }
    # cninfo requires its own Referer/Origin; the shared _SESSION's default
    # Referer (EM) causes cninfo to silently return 0 results (HTTP 200 but
    # totalAnnouncement=0). Use an independent requests.post with cninfo
    # headers. Validated via smoke test: proper headers -> 1255 entries.
    cninfo_headers = {
        "User-Agent": _H["User-Agent"],
        "Referer": "http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?"
                   "url=disclosure/list/search",
        "Origin": "http://www.cninfo.com.cn",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    }
    try:
        r = requests.post(url, data=form, headers=cninfo_headers, timeout=8)
        if r.status_code != 200:
            return []
        js = r.json()
    except Exception:
        return []
    anns = (js or {}).get("announcements") or []
    out = []
    for a in anns:
        ts_ms = a.get("announcementTime") or 0
        try:
            nd = datetime.datetime.fromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d")
        except Exception:
            nd = ""
        out.append({
            "notice_date": nd,
            "title": a.get("announcementTitle") or "",
        })
    return out


def _fetch_announcements(code, page_size=20):
    """Fetch recent announcements with dual-source fallback.
      1. EM np-anotice-stock -- primary (richer fields, faster).
      2. 巨潮资讯 cninfo     -- fallback when EM empty/fails.
    Joint failure ~= two independent sources both down, extremely rare.
    Output: list of {notice_date, title, ...}.
    """
    lst = _fetch_em_announcements(code, page_size)
    if lst:
        return lst
    # EM returned 0 rows or raised -> try cninfo
    alt = _fetch_cninfo_announcements(code, page_size)
    if alt:
        print(f"INFO: announcements for {code}: EM empty, cninfo fallback "
              f"yielded {len(alt)} entries", file=sys.stderr)
    return alt


def has_bad_news(code, days=7, use_cache=True):
    """Return (bad: bool, matched_title: str|None) -- checks last `days` days.

    Cached per-code-per-date (TTL 1h). Pure GET; no side-effects.
    """
    key = f"ann_{code}.json"
    items = None
    if use_cache:
        cached = _cache_get(key, ttl_sec=3600)
        if cached is not None:
            items = cached
    if items is None:
        items = _fetch_announcements(code)
        _cache_set(key, items)
    if not items:
        return False, None
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    for it in items:
        nd = it.get("notice_date") or ""
        try:
            dt = datetime.datetime.strptime(nd[:10], "%Y-%m-%d")
        except Exception:
            continue
        if dt < cutoff:
            continue
        title = it.get("title", "") or ""
        for pat in _BAD_NEWS_PATTERNS:
            if pat in title:
                return True, f"[{nd[:10]}] {title[:50]} (命中: {pat})"
    return False, None


def is_trading_day_probe():
    """Probe whether today is a trading day via zt-pool emptiness.

    Returns (is_trading: bool, reason: str). Weekends are always non-trading.
    During trading day pre-open (before 09:15) zt-pool will be empty too;
    caller should treat "weekday-but-empty-pool" as holiday OR pre-open.
    """
    now = datetime.datetime.now()
    if now.weekday() >= 5:
        return False, "周末非交易日"
    try:
        pool = get_pool("zt")
    except Exception:
        return True, ""                                    # fail-open
    if not pool:
        # Before 09:30 weekday is normal "empty pool"; otherwise holiday
        if now.hour < 9 or (now.hour == 9 and now.minute < 30):
            return True, "盘前时段"
        return False, "工作日但涨停池为空（可能是法定节假日）"
    return True, ""


# --------------------------------------------------------------------------
# Intraday-strict freshness guard.
# 盘中（9:30~11:30 / 13:00~15:00）实时数据失败时，**禁止**回退到 stale cache
# (cache 里是昨日 / 上一交易日的快照; 用昨天的 price 给今天 T+1 决策会产生
# 系统性误判)。盘前/盘后/午休/非交易日维持原 stale fallback 逻辑——那些
# 时段本来就用上一交易日数据，stale 是合规的。
#
# Module-level fail log: each time stale cache is denied during an intraday
# session AND the upstream call has no live tier to fall through to (i.e.
# would have served stale otherwise), the layer name is appended here.
# `recommend()` clears this at start and aggregates it into
# meta["data_quality_critical"] / meta["data_quality"]["intraday_stale_denied"]
# so `_print_next_step_block` can hard-terminate with an explicit warning
# instead of silently serving yesterday's prices.
# --------------------------------------------------------------------------
_INTRADAY_STRICT_DENIALS = []  # list[dict]: {layer, key, error, ts}


def _is_intraday_session():
    """Return True iff now is within A-share continuous-trading hours
    (9:30~11:30 or 13:00~15:00) on a trading day.

    Pre-open (<9:30) / lunch (11:30~13:00) / after-close (>=15:00) /
    weekends all return False -- those windows can legitimately use stale
    cache because the user is making decisions on yesterday's settled
    prices anyway.
    """
    now = datetime.datetime.now()
    if now.weekday() >= 5:
        return False
    hm = now.hour * 100 + now.minute
    if 930 <= hm < 1130:
        return True
    if 1300 <= hm < 1500:
        return True
    return False


def _record_intraday_stale_denial(layer, key, err):
    """Log a denied-stale-fallback event so recommend() can surface it."""
    try:
        _INTRADAY_STRICT_DENIALS.append({
            "layer": layer,
            "key": key,
            "error": f"{type(err).__name__}: {str(err)[:120]}",
            "ts": datetime.datetime.now().strftime("%H:%M:%S"),
        })
    except Exception:
        pass


def _maybe_stale_cache(key, max_days, layer):
    """Wrapper for `_cache_get_stale` honoring the intraday-strict policy.

    Returns (stale_data, stale_date) when allowed; (None, None) when
    denied. Caller should treat (None, None) as "no stale available" and
    continue to the next fallback (e.g. live Sina) or raise.
    """
    if _is_intraday_session():
        _record_intraday_stale_denial(layer, key, RuntimeError("intraday-strict"))
        return None, None
    return _cache_get_stale(key, max_days=max_days)


# ==========================================================================
# Basic helpers
# ==========================================================================

def _secid(code):
    c = code.strip()
    if c.isdigit():
        if len(c) == 5:
            return f"116.{c}"
        return f"1.{c}" if c[0] == "6" else f"0.{c}"
    return f"105.{c.upper()}"


def _get_market(code):
    """Classify A-share market from code prefix."""
    c = (code or "").strip()
    if not c.isdigit():
        return "other"
    if len(c) == 5:
        return "hk"
    if c.startswith("688"):
        return "star"
    if c.startswith(("60", "900")):
        return "main_sh"
    if c.startswith("00"):
        return "main_sz"
    if c.startswith("30"):
        return "gem"
    if c.startswith(("43", "83", "87", "88", "92")):
        return "bse"
    return "other"


def _is_in_market(code, market):
    m = _get_market(code)
    market = (market or "all").lower()
    if market == "all":
        return m in ("main_sh", "main_sz", "gem", "star")
    if market == "main":
        return m in ("main_sh", "main_sz")
    if market == "sh":
        return m in ("main_sh", "star")
    if market == "sz":
        return m in ("main_sz", "gem")
    return m == market


def _is_risky_name(name):
    """ST / *ST / 退 / N / C etc."""
    if not name:
        return False
    n = name.replace(" ", "")
    return ("ST" in n) or n.startswith(("*", "退")) or ("退市" in n)


def _fmt_amount(val):
    """Format yuan amount: 亿 / 万."""
    if val is None:
        return "-"
    try:
        v = float(val)
    except Exception:
        return "-"
    if v == 0:
        return "-"
    if abs(v) >= 1e8:
        return f"{v/1e8:.2f}亿"
    if abs(v) >= 1e4:
        return f"{v/1e4:.0f}万"
    return f"{v:.0f}"


def _fmt_time(t):
    """Format HHMMSS int (e.g. 93045) to HH:MM:SS."""
    if not t:
        return "-"
    try:
        s = str(int(t)).zfill(6)
    except Exception:
        return str(t)
    return f"{s[:2]}:{s[2:4]}:{s[4:6]}"


def _num(v):
    """Coerce to float; return 0.0 on '-' or missing."""
    if v is None or v == "-" or v == "":
        return 0.0
    try:
        return float(v)
    except Exception:
        return 0.0


def _calc_shares(price, capital, min_trade_value, max_position_pct=100.0):
    """Max 100-share lots fitting within capital (or `max_position_pct`% of it).

    Args:
        max_position_pct: per-stock cap as % of capital (default 100 = no cap).
            Rationale: limit single-stock exposure to e.g. 40% so when only 1-2
            candidates survive filters, we don't end up all-in on one ticker.

    Small-capital auto-disable: if capital * pct% < min_trade_value, the cap
    is too tight to buy even one valid lot -- fall back to full capital.
    E.g. capital=10000 + pct=40 + min_trade=5000: pct_cap=4000 < 5000, so use
    full 10000 (hard 40% cap only meaningful for capital >= min_trade/pct*100,
    e.g. >=12500 at pct=40). This matches real-world small-retail accounts
    where diversification is simply not possible.

    Returns (shares, cost). shares=0 means price too high to fit.
    """
    if price <= 0:
        return 0, 0.0
    pct_cap = capital * (max_position_pct / 100.0)
    if pct_cap < min_trade_value:
        effective_cap = capital                            # auto-disable for small accounts
    else:
        effective_cap = pct_cap                            # hard cap active
    max_lots = int(effective_cap // (price * 100))         # floor
    if max_lots < 1:
        return 0, 0.0
    shares = max_lots * 100
    cost = shares * price
    if cost < min_trade_value:
        return 0, 0.0                                      # cannot meet min_trade
    return shares, round(cost, 2)


# --------------------------------------------------------------------------
# Capital allocation planner (fixed per-stock target, score-descending fill)
# --------------------------------------------------------------------------
# Goal: turn the scored candidate list into an actionable "buy plan" that a
# human trader can execute directly. Rules (user-specified):
#   (1) Fixed per-stock target (default 10000 RMB), NOT capital / N.
#   (2) Iterate candidates from highest final_score down.
#   (3) Share sizing per candidate:
#         - lot_cost = 100 * price
#         - if lot_cost <= target:
#             shares = floor(target / price / 100) * 100   # as many 100-lots
#                                                            # as fit in target
#         - elif lot_cost <= capital / 2:
#             shares = 100                                   # single lot,
#                                                            # even if > target
#         - else:                                            # single lot >
#             skip                                           # half of total
#                                                            # capital -> too
#                                                            # concentrated
#   (4) Accumulate until cumulative cost would exceed total capital.
#       - If the candidate's plan overshoots remaining budget, try 100 shares
#         fallback; if still overshoots, skip and try next cheaper candidate.
#   (5) No hard Top-N cap -- keep allocating until capital is exhausted.
# --------------------------------------------------------------------------
def _build_allocation_plan(final, capital, per_target=10000.0):
    """Build an actionable allocation plan with fixed per-stock target.

    Args:
        final: list of scored candidates (already sorted by score DESC) with
            price / stop_profit / stop_loss / strategy / score fields populated.
        capital: total capital (RMB).
        per_target: fixed target RMB per stock (default 10000).

    Returns dict with:
        items: list of {rank, code, name, strategy, price, shares, cost,
                        pct_of_capital, cum_cost, cum_pct,
                        stop_profit, stop_loss, industry, score, prob}
        used:            total RMB allocated across items
        remaining_cash:  capital - used
        skipped:         list of {code, name, reason}
        per_target:      per-stock target (echoed for display)
    """
    items = []
    skipped = []
    used = 0.0
    half_cap = capital * 0.5

    for c in final:
        price = float(c.get("price") or 0)
        if price <= 0:
            continue
        lot_cost = 100.0 * price
        # Rule (3) branch 3: single lot too expensive -> skip
        if lot_cost > half_cap:
            skipped.append({
                "code": c.get("code"),
                "name": c.get("name"),
                "reason": f"单手{lot_cost:.0f}元 > 半仓{half_cap:.0f}元",
            })
            continue
        # Rule (3): decide shares
        if lot_cost <= per_target:
            shares = int(per_target / price / 100) * 100
            if shares < 100:
                shares = 100
        else:
            shares = 100                                   # lot > target but
                                                           # <= half_cap: buy
                                                           # a single lot
        cost = shares * price
        remaining = capital - used
        # Rule (4): overshoot handling
        if cost > remaining:
            # Try 100-share fallback if current plan was multi-lot
            if shares > 100 and 100 * price <= remaining:
                shares = 100
                cost = 100 * price
            else:
                skipped.append({
                    "code": c.get("code"),
                    "name": c.get("name"),
                    "reason": f"剩余{remaining:.0f}元不足单手{lot_cost:.0f}元",
                })
                continue
        used += cost
        items.append({
            "rank": len(items) + 1,
            "code": c.get("code"),
            "name": c.get("name"),
            "strategy": c.get("strategy", "-"),
            "score": c.get("score"),
            "price": round(price, 2),
            "shares": shares,
            "cost": round(cost, 2),
            "pct_of_capital": round(cost / capital * 100, 1),
            "cum_cost": round(used, 2),
            "cum_pct": round(used / capital * 100, 1),
            "stop_profit": c.get("stop_profit"),
            "stop_loss": c.get("stop_loss"),
            "industry": c.get("industry", "-"),
            "prob": c.get("next_day_prob") or "-",
        })
        # Early stop: remaining can't fit even the cheapest lot (~2 RMB * 100)
        if capital - used < 200:
            break

    return {
        "items": items,
        "used": round(used, 2),
        "remaining_cash": round(capital - used, 2),
        "skipped": skipped,
        "per_target": per_target,
    }


def _render_allocation_markdown(plan, capital, title_note=None, comment=None):
    """Render an allocation plan dict as a stdout markdown block.

    Shared by (a) print_recommend final section and (b) `allocate`
    subcommand. Kept free of side effects other than print() so callers
    can decide where/when to invoke.

    Args:
        plan: dict returned by _build_allocation_plan.
        capital: total capital (used for the title banner only; plan already
            carries per-item pct_of_capital).
        title_note: optional extra note appended to the title banner, e.g.
            "LLM 调整后" or "按优先级顺序".
        comment: optional free-form comment string; printed verbatim BEFORE
            the table so the caller can prepend reasoning.
    """
    plan_items = plan.get("items") or []
    per_target = plan.get("per_target", 10000)
    banner_bits = [f"目标 {per_target:.0f}元/只"]
    if title_note:
        banner_bits.append(title_note)
    else:
        banner_bits.append("按得分高到低")
    banner_bits.append(f"总资金 {capital:.0f}元")
    print(f"\n## 💰 资金分配方案 ({', '.join(banner_bits)})\n")
    if comment:
        # Verbatim echo; keep newlines / markdown exactly as caller passed.
        print(comment.rstrip() + "\n")
    if not plan_items:
        print("(无可分配候选：单手成本均 > 半仓或资金不足)")
    else:
        print("| 优先级 | 代码 | 名称 | 策略 | 得分 | 现价 | 股数 | 投入资金 "
              "| 占比 | 累计资金 | 累计占比 | 止盈 | 止损 | 行业 | 冲高概率 |")
        print("|---:|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|:---:|")
        for it in plan_items:
            print(f"| #{it['rank']} | {it['code']} | {it['name']} "
                  f"| {it['strategy']} | {it.get('score', 0)} "
                  f"| {it['price']} | {it['shares']} | {it['cost']:.0f} "
                  f"| {it['pct_of_capital']}% | {it['cum_cost']:.0f} "
                  f"| {it['cum_pct']}% | {it.get('stop_profit', '-')} "
                  f"| {it.get('stop_loss', '-')} | {it.get('industry', '-')} "
                  f"| {it.get('prob', '-')} |")
        used = plan.get("used", 0)
        rem = plan.get("remaining_cash", 0)
        print(f"\n**合计投入：{used:.0f} 元 "
              f"({used/capital*100:.1f}%)  |  剩余现金：{rem:.0f} 元**")
    skipped = plan.get("skipped") or []
    if skipped:
        print("\n### 跳过候选 (不纳入买入计划)")
        for s in skipped[:8]:                              # cap at 8 rows
            print(f"- {s['code']} {s['name']}：{s['reason']}")
        if len(skipped) > 8:
            print(f"- ...（共 {len(skipped)} 只被跳过）")


# --------------------------------------------------------------------------
# Allocation context cache (used by `allocate` subcommand for 2nd-pass lookup)
# --------------------------------------------------------------------------
# Design: at end of `recommend()`, snapshot the per-stock fields needed by
# the allocation renderer (name / strategy / stop_profit / stop_loss /
# industry / score / prob / price) into a single JSON file so that a later
# `allocate --codes 600759,...` invocation can reconstruct the full table
# without re-running the full screener. Cache key is flat code->fields.
# --------------------------------------------------------------------------
_ALLOC_CTX_NAME = "last_allocation_ctx.json"

def _alloc_ctx_path():
    return _cache_path(_ALLOC_CTX_NAME)                    # under today's dir

def _save_allocation_context(final, capital):
    """Persist per-stock fields for the `allocate` subcommand.

    Only essential fields are saved to keep the file small (a few KB).
    Written under today's cache dir; _gc_cache handles rotation.
    """
    try:
        items = {}
        for c in final:
            code = c.get("code")
            if not code:
                continue
            items[code] = {
                "code": code,
                "name": c.get("name"),
                "strategy": c.get("strategy", "-"),
                "price": c.get("price"),
                "stop_profit": c.get("stop_profit"),
                "stop_loss": c.get("stop_loss"),
                "industry": c.get("industry", "-"),
                "score": c.get("score"),
                "next_day_prob": c.get("next_day_prob") or "-",
            }
        payload = {
            "timestamp": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            "capital_default": capital,
            "items": items,
        }
        with open(_alloc_ctx_path(), "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"WARN: save allocation context failed: {e}", file=sys.stderr)

def _load_allocation_context(max_days=2):
    """Load last allocation context; scan today and up to max_days back."""
    today = datetime.datetime.now()
    for delta in range(max_days + 1):
        d = (today - datetime.timedelta(days=delta)).strftime("%Y%m%d")
        p = os.path.join(_CACHE_DIR, d, _ALLOC_CTX_NAME)
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f), d
            except Exception:
                continue
    return None, None


def _get_trading_days(n=30, use_cache=True):
    """Return the last `n` real A-share trading days (ascending YYYYMMDD list).

    Source: Shanghai Composite daily k-line from East Money -- this is the
    authoritative exchange calendar (skips weekends AND all holidays including
    spring festival / may-day / nat-day / etc, covers schedule adjustments).

    Cached under today's cache dir, so it auto-refreshes on day rollover.
    Returns [] on any API failure; caller falls back to weekday-skip logic.
    """
    # Process-level memoization: once we've tried and failed this run,
    # DO NOT retry for 60 seconds -- prevents 30+ redundant retries when
    # _trading_date_offset is called per-candidate during Phase-2.
    cache_mem = getattr(_get_trading_days, "_mem", None)
    if cache_mem is not None:
        data, expiry = cache_mem
        if time.time() < expiry:
            return data

    key = "trading_days.json"
    if use_cache:
        c = _cache_get(key, ttl_sec=86400)            # 24h TTL (key already per-day)
        if c:
            _get_trading_days._mem = (c, time.time() + 60)
            return c
    # Use Sina daily k-line on SSE Composite Index (sh000001) as trading
    # calendar source. Any bar present = a real trading day.
    url = (
        "https://quotes.sina.cn/cn/api/json_v2.php/"
        f"CN_MarketData.getKLineData?symbol=sh000001&scale=240&ma=no&datalen={max(n, 30)}"
    )
    try:
        resp = _SINA_SESSION.get(url, timeout=5)
        if resp.status_code != 200:
            raise RuntimeError(f"status {resp.status_code}")
        arr = resp.json()
    except Exception as e:
        _get_trading_days._mem = ([], time.time() + 60)
        print(f"WARN: trading calendar fetch failed ({type(e).__name__}); "
              "falling back to weekday-skip offset for this run.",
              file=sys.stderr)
        return []
    if not isinstance(arr, list):
        _get_trading_days._mem = ([], time.time() + 60)
        return []
    days = []
    for item in arr:
        d_str = (item.get("day") or "")[:10]
        if len(d_str) == 10 and d_str[4] == "-" and d_str[7] == "-":
            days.append(d_str.replace("-", ""))
    if not days:
        _get_trading_days._mem = ([], time.time() + 60)
        return []
    _cache_set(key, days)
    _get_trading_days._mem = (days, time.time() + 60)
    return days


def _trading_date_offset(days_back):
    """Return the i-th trading day before today as YYYYMMDD.

    Primary: uses SSE calendar from _get_trading_days() -- covers weekends,
    public holidays (spring fest / may-day / nat-day / qingming / etc),
    and schedule adjustments correctly.

    Fallback (API down): original weekday-skip logic -- misses holidays but
    never crashes, degrading to prior behavior.
    """
    cal = _get_trading_days(30)
    if cal:
        today_str = datetime.datetime.now().strftime("%Y%m%d")
        past = [d for d in cal if d < today_str]      # Exclude today itself
        if len(past) >= days_back:
            return past[-days_back]
        # Calendar too short -- fall through to weekday logic
    # Fallback: weekday-skip (pre-calendar behavior)
    d = datetime.datetime.now()
    while days_back > 0:
        d -= datetime.timedelta(days=1)
        if d.weekday() < 5:
            days_back -= 1
    return d.strftime("%Y%m%d")


# ==========================================================================
# Daily K-line (for position indicators: 10d_low_distance, rise_10d, MA20, seal-body)
# ==========================================================================

def _sina_symbol(code):
    """6-digit A-share code -> Sina symbol (sh600xxx / sz000xxx)."""
    c = code.strip()
    if len(c) != 6 or not c.isdigit():
        return None
    return ("sh" if (c[0] == "6" or c.startswith("688")) else "sz") + c


# Shared Session for Sina k-line endpoint -- keep-alive reduces per-request
# latency from ~150ms to ~30ms for repeat calls (8-way concurrent batches).
_SINA_SESSION = requests.Session()
_SINA_SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://finance.sina.com.cn",
})


def _fetch_qt_kline(code, scale, n):
    """Fallback k-line source: Tencent QT (web.ifzq.gtimg.cn).

    Used when Sina's json_v2.php endpoint is down (returns 0 bars).
    QT is a second independent upstream so the joint-failure rate
    with Sina is ~product-of-two ~ <0.1%.

    QT URL format:
      daily (qfq):  /appstock/app/fqkline/get?param=sh600519,day,,,30,qfq
      minute:       /appstock/app/minute/kline?param=sh600519,30,,,30  (different path)
    We only support daily here (scale=240); minute fallback is not worth
    the complexity because minute data is only used for 15m features
    where a single missing stock's features degrade gracefully.

    QT daily payload (indexed-array, ascending):
      data.sh600519.day = [
        ["2024-04-22", "1810.00", "1815.00", "1820.00", "1809.00", "1234.56", ...], ...
      ]
    Field order: [date, open, close, high, low, volume_in_shou, ...]
    Note: QT's position 5 is volume in 手 (100-share lots); multiply by 100
    for shares. Amount (元) is sometimes position 6, sometimes absent;
    we zero-fill amount when absent since scoring treats amount=0 as unknown
    (fail-open) rather than "zero trading".
    """
    if scale != 240:
        return []                                          # only daily supported
    sym = _sina_symbol(code)                               # sh/sz prefix is shared convention
    if not sym:
        return []
    url = (
        "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?"
        f"param={sym},day,,,{n},qfq"
    )
    try:
        resp = _SESSION.get(url, timeout=5)
        if resp.status_code != 200:
            return []
        js = resp.json()
    except Exception:
        return []
    data = (js or {}).get("data") or {}
    # data has a single key matching the symbol (sometimes lowercase)
    sym_data = data.get(sym) or data.get(sym.lower()) or {}
    # QT uses "day" or "qfqday" depending on fqt setting
    bars = sym_data.get("qfqday") or sym_data.get("day") or []
    rows = []
    for b in bars:
        if not isinstance(b, (list, tuple)) or len(b) < 6:
            continue
        try:
            rows.append({
                "ts": b[0],                                 # "YYYY-MM-DD"
                "open": float(b[1]),
                "close": float(b[2]),
                "high": float(b[3]),
                "low": float(b[4]),
                "vol": float(b[5]) * 100,                   # 手 -> 股
                "amount": float(b[6]) if len(b) > 6 else 0.0,
            })
        except (ValueError, TypeError):
            continue
    return rows


# Dedicated session for EM push2his kline endpoint. The shared _SESSION
# defaults to Referer=finance.eastmoney.com which historically caused EM
# kline path to reject our UA (see _fetch_daily_kline docstring). Using
# Referer=quote.eastmoney.com bypasses that block. Kept on a separate
# Session so any future change to _SESSION's auth/headers does not
# accidentally re-break this fallback.
_EM_KLINE_SESSION = requests.Session()
_EM_KLINE_SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://quote.eastmoney.com/",
})


def _em_kline_secid(code):
    """6-digit A-share code -> EM secid ('1.600519' for SH, '0.000001' for SZ)."""
    c = code.strip()
    if len(c) != 6 or not c.isdigit():
        return None
    return ("1." if (c[0] == "6" or c.startswith("688")) else "0.") + c


def _fetch_em_kline(code, scale, n):
    """Tier-3 k-line fallback: EM push2his (different subdomain than push2).

    Used when both Sina and Tencent QT return 0 bars. EM serves kline data
    via push2his.eastmoney.com which is a separate subdomain from the
    push2 APIs that get WAF-throttled, so this can survive when push2
    itself is down. Headers must use Referer=quote.eastmoney.com rather
    than the shared _SESSION's finance.eastmoney.com to avoid UA-block
    on the kline path.

    Endpoint:
      /api/qt/stock/kline/get?secid=0.000001&klt=101&fqt=1&end=...&lmt=N
        klt=101  daily
        fqt=1    forward-adjusted (qfq)
      Returns klines as comma-joined strings:
      "YYYY-MM-DD,open,close,high,low,vol_in_shou,amount,..."
    """
    if scale != 240:
        return []                                          # only daily supported
    secid = _em_kline_secid(code)
    if not secid:
        return []
    url = (
        "http://push2his.eastmoney.com/api/qt/stock/kline/get?"
        f"secid={secid}&fields1=f1,f2,f3,f4,f5,f6"
        f"&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"
        f"&klt=101&fqt=1&lmt={n}"
        f"&ut=fa5fd1943c7b386f172d6893dbfba10b"
    )
    try:
        resp = _EM_KLINE_SESSION.get(url, timeout=5)
        if resp.status_code != 200:
            return []
        js = resp.json()
    except Exception:
        return []
    klines = ((js or {}).get("data") or {}).get("klines") or []
    rows = []
    for line in klines:
        parts = line.split(",")
        if len(parts) < 7:
            continue
        try:
            rows.append({
                "ts": parts[0],                            # "YYYY-MM-DD"
                "open": float(parts[1]),
                "close": float(parts[2]),
                "high": float(parts[3]),
                "low": float(parts[4]),
                "vol": float(parts[5]) * 100,              # 手 -> 股
                "amount": float(parts[6]),
            })
        except (ValueError, TypeError):
            continue
    return rows


# ==========================================================================
# 163 (NetEase) historical k-line via plain CSV.
# ==========================================================================
# quotes.money.163.com hosts a 10+ year stable CSV endpoint. No auth, no
# UA games, no rate limit observed in practice. Returns GBK-encoded CSV
# with a richer field set than other free sources (includes 换手率, 总市值,
# 流通市值 -- handy for filling fields tushare basic-tier can't give us).
#
# URL form:
#   http://quotes.money.163.com/service/chddata.html?
#     code=<0|1><6digit>&start=YYYYMMDD&end=YYYYMMDD&fields=...
#   prefix 0 = Shanghai, 1 = Shenzhen (note: opposite of Sina/EM!)
#
# CSV header (GBK):
#   日期,股票代码,名称,收盘价,最高价,最低价,开盘价,前收盘,涨跌额,
#   涨跌幅,换手率,成交量,成交金额,总市值,流通市值,成交笔数
#
# Returns rows in DESCENDING date order from 163 (most recent first); we
# reverse to ASCENDING for consistency with all other kline fetchers.
# ==========================================================================

def _163_symbol(code):
    """Build 163 secid: 0=Shanghai, 1=Shenzhen (opposite of EM/Sina)."""
    c = (code or "").strip()
    if len(c) != 6 or not c.isdigit():
        return None
    return ("0" if (c[0] == "6" or c.startswith("688")) else "1") + c


def _fetch_163_kline(code, n=30):
    """Fetch up to `n` daily bars from NetEase 163 quotes CSV.

    Returns rows in ASCENDING date order with the same dict shape as other
    `_fetch_*_kline` helpers (ts/open/close/high/low/vol/amount), plus
    bonus fields (turnover, total_mv, float_mv) when available -- callers
    that don't care can ignore them. Empty list on any error.

    163 only supports a date-range query, so we ask for ~1.6x calendar
    days back to cover weekends/holidays and trim to last `n` bars.
    """
    sym = _163_symbol(code)
    if not sym:
        return []
    end_dt = datetime.datetime.now()
    start_dt = end_dt - datetime.timedelta(days=int(n * 1.6) + 5)
    end = end_dt.strftime("%Y%m%d")
    start = start_dt.strftime("%Y%m%d")
    # Field codes: TCLOSE/HIGH/LOW/TOPEN/LCLOSE/CHG/PCHG/TURNOVER/VOTURNOVER
    #              VATURNOVER/TCAP/MCAP
    fields = ("TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;"
              "VOTURNOVER;VATURNOVER;TCAP;MCAP")
    url = (
        "http://quotes.money.163.com/service/chddata.html?"
        f"code={sym}&start={start}&end={end}&fields={fields}"
    )
    try:
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            return []
        # 163 sends GBK; resp.text uses charset auto-detect which sometimes
        # mis-detects. Force decode.
        try:
            text = resp.content.decode("gbk")
        except UnicodeDecodeError:
            text = resp.content.decode("utf-8", errors="replace")
    except Exception:
        return []
    lines = text.splitlines()
    if len(lines) < 2:
        return []
    rows = []
    # Skip header (lines[0]). Body in DESCENDING date.
    for line in lines[1:]:
        parts = line.split(",")
        if len(parts) < 13:
            continue
        try:
            ts = parts[0].strip()                          # "YYYY-MM-DD"
            close = parts[3]
            high = parts[4]
            low = parts[5]
            opn = parts[6]
            # 163 marks suspended/halted days with "None" in price columns.
            if "None" in (close, high, low, opn):
                continue
            row = {
                "ts": ts,
                "open": float(opn),
                "close": float(close),
                "high": float(high),
                "low": float(low),
                "vol": float(parts[11] or 0),              # already in shares
                "amount": float(parts[12] or 0),           # in yuan
            }
            # Bonus fields (silent if not parseable)
            try:
                row["turnover"] = float(parts[10] or 0)
            except (ValueError, IndexError):
                pass
            try:
                row["total_mv"] = float(parts[13] or 0)
                row["float_mv"] = float(parts[14] or 0)
            except (ValueError, IndexError):
                pass
            row["_source"] = "163"
            rows.append(row)
        except (ValueError, TypeError, IndexError):
            continue
    rows.sort(key=lambda r: r["ts"])                       # ASC
    if len(rows) > n:
        rows = rows[-n:]
    return rows



def _10jqka_symbol(code):
    """Convert stock code to 同花顺 line API symbol.

    sz_XXXXXX for Shenzhen, sh_XXXXXX for Shanghai.
    """
    code = str(code).zfill(6)
    if code.startswith('6'):
        return f'sh_{code}'
    return f'sz_{code}'


def _fetch_10jqka_kline(code, n=30):
    """Fetch up to `n` daily bars from 同花顺 (10jqka) V6 line API.

    Endpoint: http://d.10jqka.com.cn/v6/line/{sym}/01/last.js
    Returns daily klines in ASCENDING date order as a list of dicts:
      {ts, open, close, high, low, vol, amount, turnover, _source="10jqka"}
    Empty list on any error.

    The API returns a JSONP callback with a semicolon-separated `data` string
    where each record is: YYYYMMDD,open,high,low,close,volume,amount,turnover,,,0
    Only the most recent 140 bars are available via this endpoint.
    """
    sym = _10jqka_symbol(code)
    if not sym:
        return []
    url = f'http://d.10jqka.com.cn/v6/line/{sym}/01/last.js'
    try:
        resp = requests.get(url, headers={**_H, "Referer": "http://stockpage.10jqka.com.cn/"}, timeout=10)
        if resp.status_code != 200:
            return []
        text = resp.text
    except Exception:
        return []
    # Extract JSON from JSONP callback
    m = re.search(r'quotebridge[^(]*\((.*)\)', text, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
    except (json.JSONDecodeError, ValueError):
        return []
    kline_str = str(data.get('data', ''))
    if not kline_str:
        return []
    records = kline_str.split(';')
    rows = []
    for rec in records:
        parts = rec.split(',')
        if len(parts) < 8:
            continue
        try:
            date_str = parts[0].strip()                     # "YYYYMMDD"
            if len(date_str) != 8 or not date_str.isdigit():
                continue
            opn = float(parts[1])
            high = float(parts[2])
            low = float(parts[3])
            close = float(parts[4])
            vol = float(parts[5])                           # shares
            amount = float(parts[6])                        # yuan
            turnover = float(parts[7] or 0)                  # turnover rate %
            if close <= 0 and opn <= 0:
                continue                                    # skip suspended day
            row = {
                "ts": f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}",
                "open": opn,
                "close": close,
                "high": high,
                "low": low,
                "vol": vol,
                "amount": amount,
                "turnover": turnover,
                "_source": "10jqka",
            }
            rows.append(row)
        except (ValueError, TypeError, IndexError):
            continue
    # Ensure ASC order (API may return DESC)
    rows.sort(key=lambda r: r["ts"])
    if len(rows) > n:
        rows = rows[-n:]
    return rows


# ==========================================================================
# Multi-source field merger with conflict detection.
# ==========================================================================
# Strategy: instead of a single hard-priority fallback chain, gather field
# values from ALL successful sources, expose conflicts (numeric spread or
# categorical mismatch) to the LLM as a `_data_quality` meta block, and
# let the LLM apply soft judgement.
#
# Two primitives:
#   _merge_numeric(values_by_source, field) -> dict
#   _merge_categorical(values_by_source, field) -> dict
#
# Output dict shape:
#   {
#     "value": canonical_value,            # highest-priority non-conflict choice
#     "sources": [src_id, ...],            # ordered by priority
#     "values": {src_id: raw_value, ...},  # full breakdown
#     "conflict": bool,
#     "spread_pct": float | None,          # numeric only; max-min over mean
#     "single_source": bool,
#     "note": str | None,                  # human-readable when conflict
#     "ts_ms": int,                        # merge timestamp
#   }
#
# Source priority registry: hard-coded per field. Higher index = higher
# priority. EM push2 wins when alive (real-time intraday), tushare wins
# for T-1 close-basis fields where EM doesn't apply, etc.
# ==========================================================================

# Per-field source priority. Sources listed left = lowest priority,
# right = highest. Unknown sources fall back to alphabetical order.
_MERGE_FIELD_PRIORITY = {
    # Real-time price chain: EM > Sina > QT > tushare > 163
    "price":            ["163", "tushare", "qt", "sina", "em"],
    "pct":              ["163", "tushare", "qt", "sina", "em"],
    "open":             ["163", "tushare", "qt", "sina", "em"],
    "high":             ["163", "tushare", "qt", "sina", "em"],
    "low":              ["163", "tushare", "qt", "sina", "em"],
    "prev_close":       ["163", "tushare", "qt", "sina", "em"],
    "vol":              ["163", "tushare", "qt", "sina", "em"],
    "amount":           ["163", "tushare", "qt", "sina", "em"],
    # Liquidity / valuation: tushare daily_basic (when permitted) > EM > 163
    "turnover":         ["sina_vip", "163", "tushare", "em"],
    "pe":               ["em", "tushare"],
    "total_mv":         ["em", "tushare", "163"],
    "float_mv":         ["em", "tushare", "163"],
    # Money flow: EM multiday > Sina vip > tushare moneyflow
    "main_inflow_1d":   ["tushare", "sina_vip", "em"],
    "main_inflow_5d":   ["tushare", "sina_vip", "em"],
    "main_inflow_pct_5d": ["tushare", "sina_vip", "em"],
    # Categorical: EM is canonical, tushare uses 申万 (slightly different)
    "industry":         ["tushare", "163", "em"],
    "concept":          ["tushare", "em"],
    "name":             ["tushare", "163", "qt", "sina", "em"],
}

# Default conflict thresholds (numeric % spread). Currency / inflow can
# legitimately diverge more than tight intraday quotes; turnover is most
# tightly defined.
_MERGE_CONFLICT_THRESHOLD_PCT = {
    "price": 0.5,
    "pct": 5.0,                     # pct itself is a percentage; use abs diff
    "open": 0.5,
    "high": 0.5,
    "low": 0.5,
    "prev_close": 0.5,
    "vol": 5.0,                     # vol can lag intraday
    "amount": 5.0,
    "turnover": 10.0,
    "pe": 5.0,
    "total_mv": 5.0,
    "float_mv": 5.0,
    "main_inflow_1d": 30.0,         # different sources count differently
    "main_inflow_5d": 30.0,
    "main_inflow_pct_5d": 30.0,
}

# Special-case categorical normalization. tushare's 申万 industry names
# don't exactly match EM's classification; treat semantic equivalents as
# non-conflicts. Extend as observed in the wild.
# EM 申万一级 vs tushare 申万 vs 163 三套行业分类经常出现"同物异名"，
# 这里维护一份双向 alias 表。对于"罗马数字 Ⅰ/Ⅱ/Ⅲ 后缀"和"制造/原料/开发"
# 这类常见同义后缀，在 _normalize_categorical 里统一剥离，不需在此重复列。
_INDUSTRY_ALIASES = {
    "白酒": ["饮料制造", "酒类", "酒"],
    "饮料制造": ["白酒", "酒类"],
    "银行": ["国有大型银行", "股份制银行", "城商行"],
    "证券": ["券商", "证券公司"],
    "房地产": ["房地产开发"],
    "电池": ["锂电池", "动力电池"],
    # Real-world conflicts observed in 2026-05 phone log:
    "电力": ["新型电力", "新能源发电", "电力供应"],
    "新型电力": ["电力", "新能源发电"],
    "化学原料": ["化工原料", "基础化工", "化工"],
    "化工原料": ["化学原料", "基础化工"],
    "通用设备": ["机械基件", "机械设备", "通用机械"],
    "机械基件": ["通用设备", "机械设备"],
    "地面兵装": ["运输设备", "兵器装备", "国防军工"],
}


def _merge_numeric(values_by_source, field, ts_ms=None):
    """Merge numeric values from multiple sources.

    `values_by_source`: {source_id: numeric_value}, None / non-numeric
        entries are filtered out.
    Returns a dict matching the schema documented at the top of this
    section. Empty `values_by_source` -> {value: None, ...}.
    """
    if ts_ms is None:
        ts_ms = int(time.time() * 1000)
    # Filter non-numeric / None values
    cleaned = {}
    for src, v in values_by_source.items():
        if v is None:
            continue
        try:
            cleaned[src] = float(v)
        except (TypeError, ValueError):
            continue
    if not cleaned:
        return {
            "value": None, "sources": [], "values": {},
            "conflict": False, "spread_pct": None, "single_source": False,
            "note": "no_data", "ts_ms": ts_ms,
        }
    # Pick canonical: highest priority source present
    priority = _MERGE_FIELD_PRIORITY.get(field, [])
    ranked_sources = sorted(
        cleaned.keys(),
        key=lambda s: priority.index(s) if s in priority else -1,
        reverse=True,
    )
    canonical = cleaned[ranked_sources[0]]
    # Spread analysis (only when 2+ sources)
    if len(cleaned) < 2:
        return {
            "value": canonical, "sources": ranked_sources,
            "values": cleaned, "conflict": False, "spread_pct": None,
            "single_source": True, "note": None, "ts_ms": ts_ms,
        }
    vals = list(cleaned.values())
    vmin, vmax = min(vals), max(vals)
    # Special-case for `pct` (which is itself a percentage): use absolute
    # diff in percentage points instead of relative spread.
    if field == "pct":
        spread = abs(vmax - vmin)                                # pp
        threshold = _MERGE_CONFLICT_THRESHOLD_PCT.get(field, 5.0)
        conflict = spread > threshold
        note = (f"pct_spread={spread:.2f}pp" if conflict else None)
        return {
            "value": canonical, "sources": ranked_sources,
            "values": cleaned, "conflict": conflict,
            "spread_pct": spread, "single_source": False,
            "note": note, "ts_ms": ts_ms,
        }
    # Generic relative spread; guard division by zero
    mean = sum(vals) / len(vals)
    if abs(mean) < 1e-9:
        # All values near zero -- treat absolute diff
        spread_pct = abs(vmax - vmin) * 100
    else:
        spread_pct = abs(vmax - vmin) / abs(mean) * 100
    threshold = _MERGE_CONFLICT_THRESHOLD_PCT.get(field, 10.0)
    conflict = spread_pct > threshold
    note = None
    if conflict:
        note = (f"spread {spread_pct:.1f}% > {threshold:.1f}% threshold; "
                f"min={vmin}, max={vmax}")
    return {
        "value": canonical, "sources": ranked_sources, "values": cleaned,
        "conflict": conflict, "spread_pct": round(spread_pct, 2),
        "single_source": False, "note": note, "ts_ms": ts_ms,
    }


_ROMAN_SUFFIX_RE = re.compile(r"[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩIVX]+$")


def _normalize_categorical(field, raw_value):
    """Normalize categorical strings for fair comparison.

    For the `industry` field we strip trailing Roman-numeral level suffix
    (申万 一/二/三级行业 like "证券Ⅱ" / "房地产Ⅱ" / "银行Ⅱ") so that the
    base name matches across data sources. EM uses Ⅱ on the level-2 view
    while tushare/163 typically drop it; without this stripping every
    bank/securities/realestate pick falsely flags as a conflict.
    """
    if raw_value is None:
        return None
    s = str(raw_value).strip()
    if not s:
        return None
    if field == "industry":
        # Strip trailing Roman-numeral suffix: "证券Ⅱ" -> "证券"
        s = _ROMAN_SUFFIX_RE.sub("", s).strip() or s
    return s


def _categorical_equivalent(field, a, b):
    """Return True if two categorical values are semantically equivalent."""
    if a == b:
        return True
    if field == "industry":
        if a in _INDUSTRY_ALIASES.get(b, []):
            return True
        if b in _INDUSTRY_ALIASES.get(a, []):
            return True
    return False


def _merge_categorical(values_by_source, field, ts_ms=None):
    """Merge categorical (string) values across sources.

    Conflict := two normalized values disagree AND aren't aliases. Note
    field is set to "category_diff" listing the divergent values.
    """
    if ts_ms is None:
        ts_ms = int(time.time() * 1000)
    cleaned = {}
    for src, v in values_by_source.items():
        nv = _normalize_categorical(field, v)
        if nv is not None:
            cleaned[src] = nv
    if not cleaned:
        return {
            "value": None, "sources": [], "values": {},
            "conflict": False, "single_source": False,
            "note": "no_data", "ts_ms": ts_ms,
        }
    priority = _MERGE_FIELD_PRIORITY.get(field, [])
    ranked_sources = sorted(
        cleaned.keys(),
        key=lambda s: priority.index(s) if s in priority else -1,
        reverse=True,
    )
    canonical = cleaned[ranked_sources[0]]
    if len(cleaned) < 2:
        return {
            "value": canonical, "sources": ranked_sources,
            "values": cleaned, "conflict": False,
            "single_source": True, "note": None, "ts_ms": ts_ms,
        }
    # Pairwise equivalence check
    distinct = []
    for v in cleaned.values():
        if not any(_categorical_equivalent(field, v, d) for d in distinct):
            distinct.append(v)
    conflict = len(distinct) > 1
    note = None
    if conflict:
        note = "category_diff: " + " vs ".join(distinct)
    return {
        "value": canonical, "sources": ranked_sources, "values": cleaned,
        "conflict": conflict, "single_source": False,
        "note": note, "ts_ms": ts_ms,
    }


# Field-type registry: which merger to apply.
_MERGE_FIELD_TYPE = {
    "price": "numeric", "pct": "numeric",
    "open": "numeric", "high": "numeric", "low": "numeric",
    "prev_close": "numeric", "vol": "numeric", "amount": "numeric",
    "turnover": "numeric", "pe": "numeric",
    "total_mv": "numeric", "float_mv": "numeric",
    "main_inflow_1d": "numeric", "main_inflow_5d": "numeric",
    "main_inflow_pct_5d": "numeric",
    "industry": "categorical", "concept": "categorical",
    "name": "categorical",
}


def merge_field(values_by_source, field):
    """Dispatch to the right merger based on field type registry."""
    ftype = _MERGE_FIELD_TYPE.get(field, "numeric")
    if ftype == "categorical":
        return _merge_categorical(values_by_source, field)
    return _merge_numeric(values_by_source, field)


def merge_records_by_source(records_by_source, fields):
    """Merge a dict of {source_id: record_dict} into a unified record.

    `records_by_source`: e.g. {"em": {price: 1375, pct: -0.71, ...},
                               "tushare": {price: 1375.5, pct: -0.65, ...},
                               "sina_vip": {main_inflow_5d: -4.08e9, ...}}
    `fields`: list of field names to merge.
    Returns:
      {
        "fields": {field: canonical_value, ...},   # flat values
        "_data_quality": {field: merge_dict, ...}, # per-field merge meta
      }
    """
    out_values = {}
    out_quality = {}
    for f in fields:
        vbs = {}
        for src, rec in records_by_source.items():
            if rec is None:
                continue
            if f in rec and rec[f] is not None:
                vbs[src] = rec[f]
        if not vbs:
            continue
        merged = merge_field(vbs, f)
        out_values[f] = merged["value"]
        out_quality[f] = merged
    return {"fields": out_values, "_data_quality": out_quality}


# Per-source field whitelist: which fields each source can ACTUALLY provide.
# Critical because some sources (Sina free hq) fill in placeholder zeros for
# unsupported fields (turnover=0.0, pe=0.0, ...) which would be treated as
# real values by the merger and trigger spurious conflicts.
_SOURCE_FIELDS = {
    "em":         ["price", "pct", "open", "high", "low", "prev_close",
                   "vol", "amount", "turnover", "pe", "total_mv", "float_mv",
                   "main_inflow_1d", "main_inflow_5d", "main_inflow_pct_5d",
                   "industry", "concept", "name"],
    "em_ulist":   ["price", "pct", "open", "high", "low", "prev_close",
                   "vol", "amount", "turnover", "pe", "total_mv", "float_mv",
                   "main_inflow_1d", "industry", "name"],
    "sina":       ["price", "pct", "open", "high", "low", "prev_close",
                   "vol", "amount", "name"],
    "sina_vip":   ["main_inflow_1d", "main_inflow_5d", "turnover", "price",
                   "pct"],
    "tushare":    ["price", "pct", "open", "high", "low", "prev_close",
                   "vol", "amount", "industry", "name"],
    "163":        ["price", "pct", "open", "high", "low", "prev_close",
                   "vol", "amount", "turnover", "total_mv", "float_mv"],
    "qt":         ["price", "pct", "open", "high", "low", "prev_close",
                   "vol", "amount", "name"],
}

# Source aliases for normalization. Multiple internal source IDs may map to
# the same logical source for priority/conflict purposes.
_SOURCE_ALIAS = {
    "em_ulist": "em",       # EM single-quote -> same WAF/service as clist
    "em_clist": "em",
    "em_kline": "em",
    "em_sector": "em",
    "em_q": "em",
    "sina_hq": "sina",
}

# Common-known field aliases between candidate dicts and the canonical
# merger field names. Candidate dicts (from screen_strategy_*) sometimes
# call 1-day inflow `main_inflow` rather than `main_inflow_1d`.
_FIELD_ALIAS_TO_CANON = {
    "main_inflow": "main_inflow_1d",
}


def _project_source_record(source_id, raw_record):
    """Filter a raw record to only the fields this source can vouch for.

    Drops keys that aren't in the source's whitelist, drops None values,
    renames known aliases (e.g. main_inflow -> main_inflow_1d), and
    normalizes unit conventions to a single canonical unit per field
    (so the merger compares apples to apples):

      vol: canonical = SHARES (股). EM clist returns 手 (lots = 100 shares);
           Sina/tushare return shares directly. EM's internal value is left
           untouched in main code paths; only the projected copy is scaled.

    Returns a fresh dict (does not mutate input).
    """
    canon_src = _SOURCE_ALIAS.get(source_id, source_id)
    allowed = set(_SOURCE_FIELDS.get(canon_src, []))
    out = {}
    if not isinstance(raw_record, dict):
        return out
    for k, v in raw_record.items():
        canon_k = _FIELD_ALIAS_TO_CANON.get(k, k)
        if canon_k not in allowed:
            continue
        if v is None:
            continue
        # Drop placeholder zeros for fields where 0 means "no data" (Sina hq
        # fills 0 for unsupported fields). Distinguish:
        # - main_inflow_*: 0 is legitimate (perfectly balanced flow)
        # - turnover, pe, total_mv, float_mv: 0 means unavailable
        if canon_src == "sina" and canon_k in ("turnover", "pe", "total_mv",
                                                "float_mv"):
            if v == 0 or v == 0.0:
                continue
        # Drop empty strings for categorical fields.
        if isinstance(v, str) and not v.strip():
            continue
        # Unit normalization: EM clist `vol` is in 手 (lots) -> scale to
        # shares for fair comparison with Sina/tushare.
        if canon_src == "em" and canon_k == "vol":
            try:
                v = float(v) * 100
            except (TypeError, ValueError):
                pass
        out[canon_k] = v
    return out


_MERGE_TARGET_FIELDS = [
    "price", "pct", "open", "high", "low", "prev_close",
    "vol", "amount", "turnover", "main_inflow_1d", "main_inflow_5d",
    "industry", "name",
]


def enrich_top_candidates(candidates, max_depth=20, market_list=None):
    """Apply multi-source enrichment + merge to top-N candidates.

    For each of the top `max_depth` candidates:
      1. Treat the candidate's existing fields as record from its primary
         source (`_source` attribute, defaulting to "em").
      2. Add EM single-quote (batched ulist call - 1 request for all N).
      3. Add Sina hq quote (batched - 1 request for all N).
      4. Add Sina vip moneyflow (parallel per-stock - N requests via thread
         pool, ~3-5s for 20 stocks).
      5. Add tushare snapshot lookup (cached full-market data; zero cost
         when token configured AND snapshot was already pulled this run).
      6. Merge into a unified record with `_data_quality` block tracking
         conflicts and source provenance per-field.
      7. Attach `_data_quality` to the candidate dict in place.

    Mutates `candidates` -- attaches a `_data_quality` key on each top-N
    item. Other fields are NOT overwritten so downstream allocation /
    sizing / persistence remain stable. Returns the same list.

    `market_list`: pre-fetched full market_list dict (for tushare lookup
    short-circuit). Pass None to re-fetch lazily.
    """
    if not candidates:
        return candidates
    targets = candidates[:max_depth]
    codes = [c["code"] for c in targets if c.get("code")]
    if not codes:
        return candidates
    t_start = time.time()
    em_quotes = {}
    sina_quotes = {}
    # 1. EM single-quote batch (lighter than clist; usually survives clist
    #    rate-limit since it's a different endpoint).
    try:
        em_rows = _fetch_market_by_codes(codes)
        em_quotes = {r["code"]: r for r in em_rows if r.get("code")}
    except Exception as e:
        print(f"WARN: enrich EM single-quote failed: {type(e).__name__}: {e}",
              file=sys.stderr)
    # 2. Sina hq batch.
    try:
        sina_rows = _fetch_sina_batch(codes)
        sina_quotes = {r["code"]: r for r in sina_rows if r.get("code")}
    except Exception as e:
        print(f"WARN: enrich Sina hq failed: {type(e).__name__}: {e}",
              file=sys.stderr)
    # 3. Sina vip moneyflow parallel.
    try:
        vip_5d = enrich_main_inflow_5d_for_codes(codes, max_workers=10)
    except Exception as e:
        print(f"WARN: enrich Sina vip failed: {type(e).__name__}: {e}",
              file=sys.stderr)
        vip_5d = {}
    # 4. Tushare snapshot lookup (only if token configured).
    tushare_lookup = {}
    if _get_tushare_token():
        try:
            ts_rows = _fetch_tushare_market_snapshot("all")    # cached
            tushare_lookup = {r["code"]: r for r in ts_rows if r.get("code")}
        except Exception as e:
            print(f"WARN: enrich tushare snapshot failed: {type(e).__name__}",
                  file=sys.stderr)
    # 5. Merge per-candidate.
    enriched = 0
    conflicts_total = 0
    for c in targets:
        code = c.get("code")
        if not code:
            continue
        primary_src = c.get("_source") or "em"
        records_by_source = {}
        # Primary source: the candidate dict itself
        rec_primary = _project_source_record(primary_src, c)
        if rec_primary:
            canon_p = _SOURCE_ALIAS.get(primary_src, primary_src)
            records_by_source[canon_p] = rec_primary
        # EM single-quote (collapses into "em" via alias)
        if code in em_quotes:
            rec_em = _project_source_record("em_ulist", em_quotes[code])
            if rec_em:
                if "em" in records_by_source:
                    # Extend existing em record with new fields; don't
                    # overwrite (clist data is generally fresher for fields
                    # both endpoints provide).
                    for k, v in rec_em.items():
                        if k not in records_by_source["em"]:
                            records_by_source["em"][k] = v
                else:
                    records_by_source["em"] = rec_em
        # Sina hq
        if code in sina_quotes:
            rec_sina = _project_source_record("sina", sina_quotes[code])
            if rec_sina:
                records_by_source["sina"] = rec_sina
        # Sina vip moneyflow (only main_inflow_5d in this lightweight call)
        if code in vip_5d:
            records_by_source["sina_vip"] = {"main_inflow_5d": vip_5d[code]}
        # Tushare snapshot
        if code in tushare_lookup:
            rec_ts = _project_source_record("tushare", tushare_lookup[code])
            if rec_ts:
                records_by_source["tushare"] = rec_ts
        # Apply merger
        if records_by_source:
            merged = merge_records_by_source(records_by_source,
                                             _MERGE_TARGET_FIELDS)
            c["_data_quality"] = merged["_data_quality"]
            enriched += 1
            for f, m in merged["_data_quality"].items():
                if m.get("conflict"):
                    conflicts_total += 1
    dt = time.time() - t_start
    print(f"INFO: enriched {enriched}/{len(targets)} candidates in {dt:.1f}s "
          f"({conflicts_total} field-conflicts flagged)", file=sys.stderr)
    return candidates


# ==========================================================================
# Sina-vip per-stock money flow (free, no auth, daily granularity).
# ==========================================================================
# Endpoint:
#   http://vip.stock.finance.sina.com.cn/quotes_service/api/
#     json_v2.php/MoneyFlow.ssl_qsfx_lscjfb?
#     daima=<sh|sz><6digit>&num=N&page=1&sort=opendate&asc=0
#
# Response: JSON array, descending opendate, length up to N. Fields:
#   opendate     "YYYY-MM-DD"
#   trade        close price
#   changeratio  daily pct (decimal)
#   turnover     turnover rate (%)
#   netamount    total net inflow (yuan)
#   ratioamount  net inflow ratio
#   r0_net       超大单净流入 (yuan)
#   r1_net       大单净流入 (yuan)
#   r2_net       中单净流入 (yuan)
#   r3_net       小单净流入 (yuan)
# Main money convention: main_net = r0_net + r1_net  (超大单 + 大单)
#
# Used to enrich D-strategy candidates when EM moneyflow is rate-limited
# AND the user's tushare tier doesn't include moneyflow (120pt accounts).
# Per-call cost ~3KB; ThreadPoolExecutor parallelism keeps total time
# under ~10s for ~50 candidates.
# ==========================================================================

_SINA_VIP_BASE = ("http://vip.stock.finance.sina.com.cn/quotes_service/api/"
                  "json_v2.php/MoneyFlow.ssl_qsfx_lscjfb")
_SINA_VIP_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "http://vip.stock.finance.sina.com.cn/",
}


def _sina_vip_daima(code):
    """6-digit code -> Sina vip prefixed symbol (sh/sz)."""
    c = (code or "").strip()
    if len(c) != 6 or not c.isdigit():
        return None
    return ("sh" if (c[0] == "6" or c.startswith("688")) else "sz") + c


def _fetch_sina_vip_moneyflow(code, num=10):
    """Pull last `num` daily moneyflow rows for one stock.

    Returns list[dict] in DESCENDING date order (newest first), each row:
      {date, close, pct, turnover, net_total, net_main, net_super,
       net_big, net_mid, net_small, _source='sina_vip'}
    Empty list on error. Safe to retry; Sina vip endpoint has no
    observable per-IP rate limit at this query rate.
    """
    daima = _sina_vip_daima(code)
    if not daima:
        return []
    url = (f"{_SINA_VIP_BASE}?daima={daima}&num={num}"
           "&page=1&sort=opendate&asc=0")
    try:
        resp = requests.get(url, timeout=6, headers=_SINA_VIP_HEADERS)
        if resp.status_code != 200:
            return []
        # Sina returns "null" (literal text) for halted/unknown stocks.
        text = resp.text.strip()
        if text in ("null", "", "[]"):
            return []
        arr = resp.json()
    except Exception:
        return []
    if not isinstance(arr, list):
        return []
    out = []
    for it in arr:
        try:
            r0 = float(it.get("r0_net") or 0)              # 超大单
            r1 = float(it.get("r1_net") or 0)              # 大单
            r2 = float(it.get("r2_net") or 0)              # 中单
            r3 = float(it.get("r3_net") or 0)              # 小单
            out.append({
                "date": (it.get("opendate") or "").replace("-", ""),
                "close": float(it.get("trade") or 0),
                "pct": float(it.get("changeratio") or 0) * 100,
                "turnover": float(it.get("turnover") or 0),
                "net_total": float(it.get("netamount") or 0),
                "net_main": r0 + r1,                       # 主力净 = 超大+大
                "net_super": r0,
                "net_big": r1,
                "net_mid": r2,
                "net_small": r3,
                "_source": "sina_vip",
            })
        except (ValueError, TypeError):
            continue
    return out


def _fetch_sina_vip_main_inflow_5d(code):
    """Convenience: 5-day cumulative MAIN money net inflow for one stock.

    Pulls 8 most recent flow rows (covers weekend gaps) and sums r0+r1
    over the most recent 5 trading days. Returns float (yuan) or None on
    failure / insufficient data.
    """
    rows = _fetch_sina_vip_moneyflow(code, num=8)
    if not rows or len(rows) < 5:
        return None
    return sum(r["net_main"] for r in rows[:5])


def enrich_main_inflow_5d_for_codes(codes, max_workers=8):
    """Parallel per-stock 5d main-inflow lookup via Sina vip.

    Returns {code: cumulative_5d_yuan}. Skips codes with no result.
    Designed for D-strategy stage-2 enrichment where the universe is
    already narrowed (~30-100 candidates) so wall-clock cost stays
    bounded (~3-8s on healthy network).

    No internal cache -- caller is expected to memoize at strategy
    layer if needed.
    """
    if not codes:
        return {}
    out = {}
    # Bound the worker pool; Sina vip handles ~10 concurrent fine but
    # going higher risks soft throttling.
    workers = min(max_workers, len(codes))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(_fetch_sina_vip_main_inflow_5d, c): c for c in codes}
        for fu in as_completed(futures):
            c = futures[fu]
            try:
                v = fu.result()
            except Exception:
                v = None
            if v is not None:
                out[c] = v
    return out


# ==========================================================================
# Tushare Tier-4 fallback (HTTP API, no SDK dependency)
# ==========================================================================
# Tushare (tushare.pro) is a free A-share data provider. We DON'T ship the
# `tushare` Python SDK -- we hit the official HTTP endpoint directly with
# stdlib `requests`. Token is per-user, persisted in skill config dir so
# it survives across runs. User can opt to skip permanently.
#
# Tier-4 role: only kicks in when Sina + QT + EM all return 0 bars.
# Empty return on any failure (no token / network / quota / parse error)
# -- the caller treats empty as "this tier did not help".
# ==========================================================================

_TUSHARE_STATE_DIR = os.path.join(_SKILL_DIR, "config")
_TUSHARE_STATE_FILE = os.path.join(_TUSHARE_STATE_DIR, "tushare_state.json")
_TUSHARE_API_URL = "http://api.tushare.pro"


def _load_tushare_state():
    """Return persisted tushare state dict; {} when missing or corrupt."""
    try:
        with open(_TUSHARE_STATE_FILE, "r", encoding="utf-8") as f:
            obj = json.load(f)
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


def _save_tushare_state(state):
    """Persist state dict to skill config dir (creates dir if needed)."""
    os.makedirs(_TUSHARE_STATE_DIR, exist_ok=True)
    with open(_TUSHARE_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def _get_tushare_token():
    """Return token string, or None if unset / skipped / empty."""
    state = _load_tushare_state()
    if state.get("skip"):
        return None
    tok = (state.get("token") or "").strip()
    return tok if tok else None


def _get_tushare_status():
    """Return 'ready' / 'skipped' / 'unset' for LLM gating logic."""
    state = _load_tushare_state()
    if state.get("skip"):
        return "skipped"
    if (state.get("token") or "").strip():
        return "ready"
    return "unset"


def _ts_code_from_a(code):
    """6-digit A-share code -> tushare ts_code (e.g. 600519 -> 600519.SH)."""
    c = code.strip()
    if len(c) != 6 or not c.isdigit():
        return None
    return c + (".SH" if (c[0] == "6" or c.startswith("688")) else ".SZ")


# Tushare error codes that indicate a bad / revoked token (not quota or network).
_TUSHARE_AUTH_ERROR_CODES = {-1000, -2001, -2002, -2003}


def _fetch_tushare_kline(code, n=30):
    """Tier-4 k-line fallback: tushare HTTP `daily` endpoint.

    Returns ascending-order list of bar dicts {ts, open, close, high,
    low, vol, amount}. Empty list on any failure.

    Progressive-disclosure side-effects (printed to stdout so the LLM
    agent can react):
      HINT: tushare_token_unset  -- user has not set a token yet
      HINT: tushare_auth_failed  -- token set but server rejected it

    Both hints include a JSON payload for the agent to parse.
    `skip` state is completely silent (user opted out).
    """
    status = _get_tushare_status()
    if status == "skipped":
        return []                                          # user opted out, stay silent
    if status == "unset":
        print(
            'HINT: tushare_token_unset {'
            '"ask_user":"K线第4级备用数据源需要 tushare token，请提供，或回复跳过禁用此功能",'
            '"if_user_provides_token":"run: stockquant.py tushare-token --set <TOKEN>",'
            '"if_user_skips":"run: stockquant.py tushare-token --skip",'
            '"after_set":"re-run the original command to continue"'
            '}',
            file=sys.stderr,
        )
        return []
    token = _get_tushare_token()                          # status=="ready" guaranteed
    ts_code = _ts_code_from_a(code)
    if not ts_code:
        return []
    end = datetime.datetime.now().strftime("%Y%m%d")
    # Pad lookback ~1.6x to cover weekends + holidays so we still get n bars.
    start_dt = datetime.datetime.now() - datetime.timedelta(days=int(n * 1.6) + 5)
    start = start_dt.strftime("%Y%m%d")
    payload = {
        "api_name": "daily",
        "token": token,
        "params": {"ts_code": ts_code, "start_date": start, "end_date": end},
        "fields": "trade_date,open,high,low,close,vol,amount",
    }
    try:
        resp = requests.post(_TUSHARE_API_URL, json=payload, timeout=8)
        if resp.status_code != 200:
            return []
        js = resp.json()
    except Exception:
        return []
    if not isinstance(js, dict) or js.get("code") != 0:
        err_code = js.get("code") if isinstance(js, dict) else None
        if err_code in _TUSHARE_AUTH_ERROR_CODES:
            print(
                'HINT: tushare_auth_failed {'
                '"ask_user":"tushare token 验证失败(error ' + str(err_code) + '），请重新提供 token，或回复跳过禁用此功能",'
                '"if_user_provides_token":"run: stockquant.py tushare-token --set <TOKEN>",'
                '"if_user_skips":"run: stockquant.py tushare-token --skip",'
                '"after_set":"re-run the original command to continue"'
                '}',
                file=sys.stderr,
            )
        return []
    data = js.get("data") or {}
    fields = data.get("fields") or []
    items = data.get("items") or []
    if not items:
        return []
    idx = {f: i for i, f in enumerate(fields)}
    needed = ("trade_date", "open", "high", "low", "close", "vol", "amount")
    if any(k not in idx for k in needed):
        return []
    rows = []
    for it in items:
        try:
            td = str(it[idx["trade_date"]])
            if len(td) != 8:
                continue
            ts_str = f"{td[:4]}-{td[4:6]}-{td[6:8]}"
            rows.append({
                "ts": ts_str,
                "open": float(it[idx["open"]]),
                "close": float(it[idx["close"]]),
                "high": float(it[idx["high"]]),
                "low": float(it[idx["low"]]),
                "vol": float(it[idx["vol"]]) * 100,         # tushare 手 -> 股
                "amount": float(it[idx["amount"]]) * 1000,  # tushare 千元 -> 元
            })
        except (ValueError, TypeError, KeyError, IndexError):
            continue
    rows.sort(key=lambda r: r["ts"])                       # ascending
    if len(rows) > n:
        rows = rows[-n:]
    return rows


# ==========================================================================
# Tushare Tier-2 fallback for FULL-MARKET data (snapshot/sector/moneyflow)
# ==========================================================================
# When EM push2 is WAF-throttled, the entire `recommend` pipeline used to
# die because there was no equivalent bulk source. Tushare exposes the
# right shape of data via `daily` + `daily_basic` (snapshot), `concept_detail`
# (sector) and `moneyflow` (main inflow), provided the user holds enough
# account points. We probe once per 24h and cache the resolved "tier":
#
#   unset           -- no token configured
#   skipped         -- user opted out via tushare-token --skip
#   basic   (120)   -- snapshot + kline ok; sector/moneyflow gated
#   full    (2000)  -- snapshot + kline + sector + moneyflow all ok
#   auth_failed     -- token rejected by server (user must re-set)
#   network_failed  -- tushare host itself unreachable (probe will retry)
#
# Snapshot returns data in `_norm_clist_row` schema so existing strategy
# code can consume it with zero awareness of the source. Some EM-only
# fields (main_inflow, concept) come back None on basic tier; strategies
# that depend on them MUST check and skip / degrade explicitly.
# ==========================================================================

_TUSHARE_TIER_FILE = os.path.join(_TUSHARE_STATE_DIR, "tushare_tier.json")
_TUSHARE_TIER_TTL_SEC = 86400                              # 24h cache


def _ts_post(api_name, params=None, timeout=8, fields=None):
    """Lightweight wrapper around tushare HTTP POST endpoint.

    Returns (ok, data_dict_or_err_str). data has 'fields' (list[str]) and
    'items' (list[list]) on success. Used by tier probe and by snapshot/
    sector/moneyflow fetchers.
    """
    token = _get_tushare_token()
    if not token:
        return False, "no_token"
    payload = {
        "api_name": api_name,
        "token": token,
        "params": params or {},
        "fields": fields or "",
    }
    try:
        resp = requests.post(_TUSHARE_API_URL, json=payload, timeout=timeout)
    except Exception as e:
        return False, f"network:{type(e).__name__}"
    if resp.status_code != 200:
        return False, f"http:{resp.status_code}"
    try:
        js = resp.json()
    except Exception:
        return False, "bad_json"
    if not isinstance(js, dict):
        return False, "bad_shape"
    code = js.get("code")
    if code != 0:
        if code in _TUSHARE_AUTH_ERROR_CODES:
            return False, f"auth:{code}"
        # Non-auth error often means insufficient points for this api.
        return False, f"api_err:{code}:{js.get('msg', '')[:80]}"
    return True, (js.get("data") or {})


def _detect_tushare_tier():
    """Probe tushare account capability; return tier string + diagnostic dict.

    Probe order (cheap -> expensive):
      1. `daily` with 1-day filter   -- 120 pts, validates token at all
      2. `moneyflow` with 1 stock    -- 2000 pts, gates D-strategy support
    `concept_detail` (also 2000 pts) is implied OK if moneyflow works,
    saving one round-trip.

    Returns (tier_str, info_dict) where tier_str in:
      unset / auth_failed / network_failed / basic / full
    info_dict carries the per-probe outcome for the LLM-facing status block.
    """
    token = _get_tushare_token()
    if not token:
        return "unset", {"reason": "no_token"}
    today = datetime.datetime.now().strftime("%Y%m%d")
    # Probe 1: daily (basic tier marker). Use a tiny single-stock filter.
    ok1, data1 = _ts_post(
        "daily",
        params={"ts_code": "600519.SH", "start_date": today, "end_date": today},
        fields="ts_code,trade_date,close",
        timeout=6,
    )
    if not ok1:
        if isinstance(data1, str) and data1.startswith("auth"):
            return "auth_failed", {"reason": data1}
        if isinstance(data1, str) and data1.startswith("network"):
            return "network_failed", {"reason": data1}
        # api_err on daily for a known-good ts_code => account too low to
        # even call daily (very rare; <120 pts shouldn't happen post-2024).
        return "auth_failed", {"reason": data1}
    # Probe 2: moneyflow (full tier marker).
    ok2, data2 = _ts_post(
        "moneyflow",
        params={"ts_code": "600519.SH", "start_date": today, "end_date": today},
        fields="ts_code,trade_date,buy_lg_amount",
        timeout=6,
    )
    if ok2:
        return "full", {"daily": "ok", "moneyflow": "ok"}
    # daily ok but moneyflow blocked => basic tier (very common for 120pt users)
    return "basic", {"daily": "ok", "moneyflow": str(data2)[:80]}


def _get_tushare_tier(force_probe=False):
    """Return cached tier; auto-refresh on TTL expiry or `force_probe`.

    Idempotent and safe to call multiple times in one CLI run; first call
    pays the probe cost (<2 RPCs, ~1-2s), subsequent calls hit the cache.
    """
    state = _load_tushare_state()
    if state.get("skip"):
        return "skipped", {"reason": "user_skipped"}
    # Cached tier under a separate file so token CRUD doesn't clobber it.
    cached = None
    try:
        if os.path.exists(_TUSHARE_TIER_FILE):
            with open(_TUSHARE_TIER_FILE, "r", encoding="utf-8") as f:
                cached = json.load(f)
    except Exception:
        cached = None
    now = time.time()
    if (not force_probe) and isinstance(cached, dict) and cached.get("tier"):
        ts = cached.get("ts", 0)
        if (now - ts) < _TUSHARE_TIER_TTL_SEC:
            return cached["tier"], cached.get("info", {})
    tier, info = _detect_tushare_tier()
    try:
        os.makedirs(_TUSHARE_STATE_DIR, exist_ok=True)
        with open(_TUSHARE_TIER_FILE, "w", encoding="utf-8") as f:
            json.dump({"tier": tier, "info": info, "ts": now}, f,
                      ensure_ascii=False, indent=2)
    except Exception:
        pass                                                # cache best-effort
    return tier, info


def _ts_to_a_code(ts_code):
    """tushare ts_code (e.g. 600519.SH) -> 6-digit A-share code."""
    if not ts_code or "." not in ts_code:
        return ""
    return ts_code.split(".", 1)[0]


# Process-wide cache for stock_basic (rate-limited 1/min on 120pt accounts).
# Persisted to disk so reruns within the day reuse the same map even on
# brand-new processes. 24h TTL.
_TUSHARE_STOCK_BASIC_FILE = os.path.join(_TUSHARE_STATE_DIR, "tushare_stock_basic.json")
_TUSHARE_STOCK_BASIC_TTL_SEC = 86400
_TUSHARE_STOCK_BASIC_MEMO = None                            # in-process cache


def _get_tushare_stock_basic_maps():
    """Return (name_map, industry_map) keyed by ts_code.

    Three-tier read:
      1. In-process memo (zero cost, populated by first call this run).
      2. On-disk JSON cache up to 24h old.
      3. Live `stock_basic` API call (rate-limited 1/min at 120pt tier).
    Empty maps on permanent failure.
    """
    global _TUSHARE_STOCK_BASIC_MEMO
    if _TUSHARE_STOCK_BASIC_MEMO is not None:
        return _TUSHARE_STOCK_BASIC_MEMO
    # Disk cache
    try:
        if os.path.exists(_TUSHARE_STOCK_BASIC_FILE):
            with open(_TUSHARE_STOCK_BASIC_FILE, "r", encoding="utf-8") as f:
                cached = json.load(f)
            if isinstance(cached, dict):
                ts = cached.get("ts", 0)
                if (time.time() - ts) < _TUSHARE_STOCK_BASIC_TTL_SEC:
                    nm = cached.get("name_map") or {}
                    im = cached.get("industry_map") or {}
                    _TUSHARE_STOCK_BASIC_MEMO = (nm, im)
                    return _TUSHARE_STOCK_BASIC_MEMO
    except Exception:
        pass
    # Live call
    name_map, industry_map = {}, {}
    ok_s, data_s = _ts_post(
        "stock_basic",
        params={"list_status": "L"},
        fields="ts_code,name,industry,market",
        timeout=15,
    )
    if ok_s and isinstance(data_s, dict):
        items_s = data_s.get("items") or []
        fields_s = data_s.get("fields") or []
        idx_s = {n: i for i, n in enumerate(fields_s)}
        for it in items_s:
            try:
                ts = it[idx_s["ts_code"]]
                name_map[ts] = it[idx_s["name"]] if "name" in idx_s else ""
                industry_map[ts] = it[idx_s["industry"]] if "industry" in idx_s else ""
            except (IndexError, KeyError):
                continue
        # Persist to disk only if we got a non-trivial result.
        if name_map:
            try:
                os.makedirs(_TUSHARE_STATE_DIR, exist_ok=True)
                with open(_TUSHARE_STOCK_BASIC_FILE, "w", encoding="utf-8") as f:
                    json.dump({
                        "ts": time.time(),
                        "name_map": name_map,
                        "industry_map": industry_map,
                    }, f, ensure_ascii=False)
            except Exception:
                pass
    _TUSHARE_STOCK_BASIC_MEMO = (name_map, industry_map)
    return _TUSHARE_STOCK_BASIC_MEMO


def _fetch_tushare_market_snapshot(market="all", trade_date=None):
    """Tier-2 full-market snapshot when EM clist is unreachable.

    Returns a list of dicts in `_norm_clist_row` schema (T-1 close basis
    when called intraday before 16:00; same-day after 16:00 publish).
    Empty list on failure / token unset / insufficient permissions.

    `market` mirrors the CLI flag: main/all/gem/star/sh/sz. We honour it
    by post-filtering the unioned daily_basic+daily result.

    Field caveats vs EM clist:
      - main_inflow:    None  (requires moneyflow, full tier only; aggregated
                              by `_fetch_tushare_main_inflow_5d` if needed)
      - concept:        ""    (requires concept_detail; lazy-aggregated)
      - amplitude:      derived from high/low/pre_close
    """
    # Don't gate on tier -- just try. If account lacks points, the API
    # call returns api_err and we degrade to []. Tier info is for the
    # status-report block only, never for blocking. User may upgrade
    # account at any time without needing to update the skill.
    if not _get_tushare_token():
        return []
    # Resolve trade_date: tushare returns nothing for non-trading dates and
    # for current day before ~16:00 publish. We fall back to most recent
    # trading day in a small lookback window.
    if not trade_date:
        trade_date = datetime.datetime.now().strftime("%Y%m%d")
    # Probe 1: daily for the trade_date (full market via empty ts_code).
    ok_d, data_d = _ts_post(
        "daily",
        params={"trade_date": trade_date},
        fields="ts_code,trade_date,open,high,low,close,pre_close,pct_chg,vol,amount",
        timeout=15,
    )
    if not ok_d or not isinstance(data_d, dict):
        return []
    items_d = data_d.get("items") or []
    if not items_d:
        # Likely non-trading day or pre-publish; walk back up to 5 calendar days.
        for delta in range(1, 6):
            prev = (datetime.datetime.strptime(trade_date, "%Y%m%d")
                    - datetime.timedelta(days=delta)).strftime("%Y%m%d")
            ok_d, data_d = _ts_post(
                "daily",
                params={"trade_date": prev},
                fields="ts_code,trade_date,open,high,low,close,pre_close,pct_chg,vol,amount",
                timeout=15,
            )
            items_d = (data_d or {}).get("items") or [] if ok_d else []
            if items_d:
                trade_date = prev
                break
        if not items_d:
            return []
    fields_d = data_d.get("fields") or []
    idx_d = {name: i for i, name in enumerate(fields_d)}
    # Probe 2: daily_basic for same trade_date (turnover/PE/MV).
    ok_b, data_b = _ts_post(
        "daily_basic",
        params={"trade_date": trade_date},
        fields="ts_code,turnover_rate,volume_ratio,pe,total_mv,circ_mv",
        timeout=15,
    )
    basic_map = {}
    if ok_b and isinstance(data_b, dict):
        items_b = data_b.get("items") or []
        fields_b = data_b.get("fields") or []
        idx_b = {name: i for i, name in enumerate(fields_b)}
        for it in items_b:
            try:
                ts = it[idx_b["ts_code"]]
            except (IndexError, KeyError):
                continue
            basic_map[ts] = it
    # Probe 3: stock_basic for name+industry. tushare 120pt accounts have
    # a hard 1-call-per-minute limit on this endpoint, so we cache the
    # result process-wide for the whole run (industry classification
    # changes very rarely; 1-day cache is conservative).
    name_map, industry_map = _get_tushare_stock_basic_maps()
    # Build normalized rows.
    rows = []
    for it in items_d:
        try:
            ts = it[idx_d["ts_code"]]
            code = _ts_to_a_code(ts)
            if not code:
                continue
            # Apply market filter post-hoc; reuse existing _is_in_market.
            if market and market != "all":
                if not _is_in_market(code, market):
                    continue
            close = float(it[idx_d["close"]] or 0)
            high = float(it[idx_d["high"]] or 0)
            low = float(it[idx_d["low"]] or 0)
            pre_close = float(it[idx_d["pre_close"]] or 0)
            amplitude = ((high - low) / pre_close * 100) if pre_close else 0.0
            b = basic_map.get(ts)
            turnover = float(b[idx_b["turnover_rate"]] or 0) if b else None
            vratio = float(b[idx_b["volume_ratio"]] or 0) if b else None
            pe = float(b[idx_b["pe"]] or 0) if b else None
            total_mv = (float(b[idx_b["total_mv"]] or 0) * 10000) if b else None
            float_mv = (float(b[idx_b["circ_mv"]] or 0) * 10000) if b else None
            rows.append({
                "code": code,
                "name": name_map.get(ts, "") or "",
                "price": close,
                "pct": float(it[idx_d["pct_chg"]] or 0),
                "vol": float(it[idx_d["vol"]] or 0) * 100,    # tushare 手 -> 股
                "amount": float(it[idx_d["amount"]] or 0) * 1000,  # 千元 -> 元
                "amplitude": amplitude,
                "turnover": turnover,
                "pe": pe,
                "volume_ratio": vratio,
                "high": high,
                "low": low,
                "open": float(it[idx_d["open"]] or 0),
                "prev_close": pre_close,
                "total_mv": total_mv,
                "float_mv": float_mv,
                "main_inflow": None,                          # tier-2 cannot provide
                "industry": industry_map.get(ts, "") or "",
                "concept": "",                                # tier-2 cannot provide
                "_source": "tushare",
                "_trade_date": trade_date,
                "_data_lag_t1": True,                         # T-1 marker for callers
            })
        except (ValueError, TypeError, KeyError, IndexError):
            continue
    return rows


def _fetch_tushare_industry_sector_rank(snapshot_rows=None, top=30):
    """Tier-2 industry-sector rank by aggregating snapshot rows.

    No extra API calls when `snapshot_rows` is provided -- we just group by
    `industry` field. Returns rows in the same schema as `get_sector_rank`:
      {code, name, pct, main_inflow, up_count, down_count,
       leader_name, leader_pct}
    `code` is empty (tushare lacks an industry-board code), `main_inflow`
    is None on basic tier (no moneyflow). Sorted by avg pct desc.

    Returns [] if snapshot fetch fails. We deliberately DO NOT support
    sector_type='concept' here -- concept aggregation needs concept_detail
    which is per-concept and would explode call count; recommend C only
    uses industry, so this covers the real use-case.
    """
    if snapshot_rows is None:
        snapshot_rows = _fetch_tushare_market_snapshot(market="all")
    if not snapshot_rows:
        return []
    by_ind = {}
    for r in snapshot_rows:
        ind = (r.get("industry") or "").strip()
        if not ind:
            continue
        slot = by_ind.setdefault(ind, {
            "name": ind,
            "pcts": [],
            "up": 0,
            "down": 0,
            "leader_name": "",
            "leader_pct": -1e9,
        })
        pct = r.get("pct")
        if pct is None:
            continue
        slot["pcts"].append(pct)
        if pct > 0:
            slot["up"] += 1
        elif pct < 0:
            slot["down"] += 1
        if pct > slot["leader_pct"]:
            slot["leader_pct"] = pct
            slot["leader_name"] = r.get("name", "") or ""
    rows = []
    for slot in by_ind.values():
        if not slot["pcts"]:
            continue
        avg_pct = sum(slot["pcts"]) / len(slot["pcts"])
        rows.append({
            "code": "",                                       # tushare 无行业板块代码
            "name": slot["name"],
            "pct": avg_pct,
            "main_inflow": None,                              # tier-2 cannot provide
            "up_count": slot["up"],
            "down_count": slot["down"],
            "leader_name": slot["leader_name"],
            "leader_pct": slot["leader_pct"] if slot["leader_pct"] > -1e8 else 0.0,
            "_source": "tushare",
            "_data_lag_t1": True,
        })
    rows.sort(key=lambda x: x["pct"], reverse=True)
    return rows[:top]


# Cached 5-day moneyflow keyed by trade_date so multiple recommend calls
# in one CLI run reuse the same per-day pull. Cleared by _CLI_RUN_BOOT.
_TS_MONEYFLOW_CACHE = {}


def _fetch_tushare_moneyflow_day(trade_date):
    """Pull full-market moneyflow for one trade_date.

    Returns {code: net_main_inflow_yuan} where net_main = (buy_lg+buy_elg) -
    (sell_lg+sell_elg) in yuan. Empty dict on failure (e.g. 1500-pt account
    cannot call moneyflow -> api_err -> {}).
    """
    if trade_date in _TS_MONEYFLOW_CACHE:
        return _TS_MONEYFLOW_CACHE[trade_date]
    if not _get_tushare_token():
        _TS_MONEYFLOW_CACHE[trade_date] = {}
        return {}
    ok, data = _ts_post(
        "moneyflow",
        params={"trade_date": trade_date},
        fields="ts_code,buy_lg_amount,sell_lg_amount,buy_elg_amount,sell_elg_amount",
        timeout=15,
    )
    if not ok or not isinstance(data, dict):
        _TS_MONEYFLOW_CACHE[trade_date] = {}
        return {}
    items = data.get("items") or []
    fields = data.get("fields") or []
    idx = {n: i for i, n in enumerate(fields)}
    out = {}
    for it in items:
        try:
            ts = it[idx["ts_code"]]
            code = _ts_to_a_code(ts)
            if not code:
                continue
            # tushare moneyflow buy_*_amount unit: 万元 -> yuan = *10000
            buy_lg = float(it[idx["buy_lg_amount"]] or 0) * 10000
            sell_lg = float(it[idx["sell_lg_amount"]] or 0) * 10000
            buy_elg = float(it[idx["buy_elg_amount"]] or 0) * 10000
            sell_elg = float(it[idx["sell_elg_amount"]] or 0) * 10000
            out[code] = (buy_lg + buy_elg) - (sell_lg + sell_elg)
        except (ValueError, TypeError, KeyError, IndexError):
            continue
    _TS_MONEYFLOW_CACHE[trade_date] = out
    return out


def _fetch_tushare_main_inflow_5d(codes=None):
    """Tier-2 5-day cumulative main-money net inflow for `codes` (or all).

    Returns {code: cumulative_net_inflow_yuan}. Walks the most recent
    trading days backward, summing daily moneyflow until 5 valid days
    accumulated (or 10 calendar days exhausted). Empty dict on auth /
    permission failure.

    `codes`: optional list of 6-digit A-share codes. When None, returns
    inflow for every stock present in moneyflow output.
    """
    if not _get_tushare_token():
        return {}
    today = datetime.datetime.now()
    accumulated_days = 0
    cumulative = {}                                          # code -> running sum
    code_set = set(codes) if codes else None
    for delta in range(0, 12):                               # walk back up to 12 cal days
        if accumulated_days >= 5:
            break
        d = today - datetime.timedelta(days=delta)
        if d.weekday() >= 5:
            continue                                          # skip weekends quickly
        td = d.strftime("%Y%m%d")
        day_map = _fetch_tushare_moneyflow_day(td)
        if not day_map:
            continue                                          # holiday / pre-publish / api fail
        accumulated_days += 1
        for code, net in day_map.items():
            if code_set is not None and code not in code_set:
                continue
            cumulative[code] = cumulative.get(code, 0.0) + net
    return cumulative


def _fetch_sina_kline(code, scale, n):
    """Fetch k-lines from Sina (scale=240 day, 60/30/15/5 minute).

    Sina returns an array of objects with string fields:
      {day, open, high, low, close, volume, amount}
    where `day` is "YYYY-MM-DD" for daily and "YYYY-MM-DD HH:MM:SS" for minute.
    Ascending order. Empty list on failure.
    """
    sym = _sina_symbol(code)
    if not sym:
        return []
    url = (
        "https://quotes.sina.cn/cn/api/json_v2.php/"
        f"CN_MarketData.getKLineData?symbol={sym}&scale={scale}&ma=no&datalen={n}"
    )
    try:
        resp = _SINA_SESSION.get(url, timeout=5)
        if resp.status_code != 200:
            return []
        arr = resp.json()
    except Exception:
        return []
    if not isinstance(arr, list):
        return []
    rows = []
    for item in arr:
        try:
            rows.append({
                "ts": item.get("day", ""),                  # "YYYY-MM-DD [HH:MM:SS]"
                "open": float(item.get("open", 0)),
                "close": float(item.get("close", 0)),
                "high": float(item.get("high", 0)),
                "low": float(item.get("low", 0)),
                "vol": float(item.get("volume", 0)),
                "amount": float(item.get("amount", 0) or 0),
            })
        except (ValueError, TypeError):
            continue
    return rows


def _fetch_daily_kline(code, n=30):
    """Fetch up to `n` recent daily k-lines for a single stock.

    Returns a list of dicts {date, open, close, high, low, vol, amount}
    in ASCENDING date order. Empty list on failure.

    Six-source fallback chain (each on a different provider/domain
    so a single WAF rule can't take all six at once):
      1. Sina quotes.sina.cn  -- primary (20-year stable endpoint)
      2. Tencent QT ifzq.gtimg.cn  -- fallback when Sina returns 0 bars
      3. EM push2his.eastmoney.com  -- third-tier on a separate subdomain
      4. Tushare api.tushare.pro  -- auth-backed independent channel
      5. 同花顺 d.10jqka.com.cn  -- V6 line API, semicolon-separated daily
         bars; tested 2026-05 alive through EM + Sina dual outage
      6. NetEase 163 quotes.money.163.com  -- pure CSV, most WAF-resistant

    Joint failure is extremely improbable; we never fall through to
    empty unless every upstream is down at once.
    """
    # Try Sina first (primary)
    raw = _fetch_sina_kline(code, scale=240, n=n)
    if not raw:
        # Fall back to QT. A 0-row Sina response may mean upstream hiccup
        # or a genuinely new/halted stock. QT disambiguates.
        raw = _fetch_qt_kline(code, scale=240, n=n)
    if not raw:
        # Tier-3: EM on a separate subdomain. Survives push2 WAF outages.
        raw = _fetch_em_kline(code, scale=240, n=n)
    if not raw:
        # Tier-4: tushare HTTP API (no-op when no token is configured).
        raw = _fetch_tushare_kline(code, n=n)
    if not raw:
        # Tier-5: 同花顺 V6 line API, confirmed alive during mid-2026
        # EM push2 + Sina dual outage. Returns up to 140 recent bars.
        raw = _fetch_10jqka_kline(code, n=n)
    if not raw:
        # Tier-6: NetEase 163 CSV -- currently returns 502 from mainland
        # mobile networks as of mid-2026; function kept ready for recovery.
        raw = _fetch_163_kline(code, n=n)
    rows = []
    for r in raw:
        ts = r.get("ts", "")
        date_str = ts[:10].replace("-", "")
        if len(date_str) != 8:
            continue
        rows.append({
            "date": date_str,
            "open": r["open"],
            "close": r["close"],
            "high": r["high"],
            "low": r["low"],
            "vol": r["vol"],
            "amount": r["amount"],
        })
    return rows


def get_daily_kline(code, n=30, use_cache=True):
    """Cached per-code daily k-line (under today's cache dir, TTL 5 min).

    Historical rows are immutable so cache can be long, but the LAST row
    may be today (still updating intraday) -- TTL 300s refreshes it.
    """
    key = f"kline_d_{code}.json"
    if use_cache:
        c = _cache_get(key, ttl_sec=300)
        if c is not None:
            return c
    rows = _fetch_daily_kline(code, n=n)
    if rows:
        _cache_set(key, rows)
    return rows


def get_daily_klines_batch(codes, n=30, workers=8, use_cache=True):
    """Batch-fetch daily k-lines for multiple codes in parallel.

    Returns dict {code: rows}. Missing/failed codes get empty list.
    Uses ThreadPoolExecutor -- EM push2his endpoint handles 8-10 concurrent
    requests without rate-limit issues.
    """
    if not codes:
        return {}
    out = {}
    # First pass: read cache synchronously (cheap I/O).
    todo = []
    if use_cache:
        for code in codes:
            key = f"kline_d_{code}.json"
            c = _cache_get(key, ttl_sec=300)
            if c is not None:
                out[code] = c
            else:
                todo.append(code)
    else:
        todo = list(codes)
    if not todo:
        return out
    # Second pass: parallel fetch for cache-miss codes.
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(_fetch_daily_kline, code, n): code for code in todo}
        for fut in as_completed(futures):
            code = futures[fut]
            try:
                rows = fut.result()
            except Exception:
                rows = []
            out[code] = rows
            if rows:
                _cache_set(f"kline_d_{code}.json", rows)
    return out


def compute_kline_indicators(kline_rows, today_price, today_low, seal_date):
    """Compute 4 daily-line position indicators from ascending k-line list.

    Args:
      kline_rows: ascending list of {date, open, close, high, low, ...}
      today_price: current intraday close/last price (from ulist quote)
      today_low: current intraday low (from ulist quote)
      seal_date: YYYYMMDD of the limit-up event to reference

    Returns dict with keys:
      distance_10d_low  - (today - 10d_low) / 10d_low * 100 (percent)
      rise_10d          - (today - close_10d_ago) / close_10d_ago * 100
      above_ma20_loose  - today >= MA20 * 0.95
      ma20              - MA20 value
      low_above_half_seal_body - today_low >= midpoint of seal-day body
    """
    result = {
        "distance_10d_low": None,
        "rise_10d": None,
        "above_ma20_loose": None,
        "ma20": None,
        "low_above_half_seal_body": None,
    }
    if not kline_rows or len(kline_rows) < 10:
        return result

    today_str = datetime.datetime.now().strftime("%Y%m%d")
    # Exclude today if present in kline (intraday API may or may not include it)
    past = [k for k in kline_rows if k["date"] < today_str]
    if len(past) < 10:
        # Not enough history excluding today -- fall back to include all
        past = kline_rows

    # Most recent 10 historical days (excluding today)
    last_10 = past[-10:]
    lowest_10d = min(k["low"] for k in last_10)
    close_10d_ago = past[-10]["close"]                     # exactly 10 days ago
    ma_window = past[-20:] if len(past) >= 20 else past
    ma20 = sum(k["close"] for k in ma_window) / len(ma_window)

    if lowest_10d > 0:
        result["distance_10d_low"] = round((today_price - lowest_10d) / lowest_10d * 100, 2)
    if close_10d_ago > 0:
        result["rise_10d"] = round((today_price - close_10d_ago) / close_10d_ago * 100, 2)
    result["ma20"] = round(ma20, 2)
    result["above_ma20_loose"] = today_price >= ma20 * 0.95

    # Seal-day body midpoint (open+close)/2: today_low must not break below it.
    seal_row = next((k for k in past if k["date"] == seal_date), None)
    if seal_row is not None:
        body_mid = (seal_row["open"] + seal_row["close"]) / 2
        if body_mid > 0 and today_low > 0:
            result["low_above_half_seal_body"] = today_low >= body_mid

    return result


# ==========================================================================
# Minute K-line (intraday features for next-day premium prediction)
# ==========================================================================

# klt codes: 5=5min, 15=15min, 30=30min, 60=60min, 101=day, 102=week, 103=month
_KLT_15MIN = 15
_KLT_60MIN = 60


def _fetch_minute_kline(code, klt, n):
    """Fetch `n` recent minute-level k-lines (ascending) via Sina.

    `klt` is the minute scale (5 / 15 / 30 / 60). Data is NOT forward-adjusted
    (no fqt option), but for intraday features this is fine: no dividend/split
    event within a single session.
    """
    return _fetch_sina_kline(code, scale=klt, n=n)


def get_minute_klines_batch(codes, klt, n, workers=8, use_cache=True):
    """Batch-fetch minute k-lines in parallel. Cache key includes klt + n."""
    if not codes:
        return {}
    out = {}
    todo = []
    if use_cache:
        for code in codes:
            key = f"kline_m{klt}_{n}_{code}.json"
            c = _cache_get(key, ttl_sec=300)               # intraday data, 5 min TTL
            if c is not None:
                out[code] = c
            else:
                todo.append(code)
    else:
        todo = list(codes)
    if not todo:
        return out
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_fetch_minute_kline, c, klt, n): c for c in todo}
        for fut in as_completed(futs):
            code = futs[fut]
            try:
                rows = fut.result()
            except Exception:
                rows = []
            out[code] = rows
            if rows:
                _cache_set(f"kline_m{klt}_{n}_{code}.json", rows)
    return out


def _today_rows(rows):
    """Filter rows to today's session only (ts starts with today's date)."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return [r for r in rows if r.get("ts", "").startswith(today)]


def _kline_body_trend(rows):
    """Linear-ish trend of closes. Returns 'up' / 'flat' / 'down' + slope%."""
    if len(rows) < 2:
        return "flat", 0.0
    first, last = rows[0]["close"], rows[-1]["close"]
    if first <= 0:
        return "flat", 0.0
    slope = (last - first) / first * 100
    if slope > 0.5:
        return "up", round(slope, 2)
    if slope < -0.5:
        return "down", round(slope, 2)
    return "flat", round(slope, 2)


def _upper_shadow_ratio(row):
    """Upper shadow length / total range. >0.5 = long upper shadow."""
    high = row["high"]
    low = row["low"]
    top_body = max(row["open"], row["close"])
    rng = high - low
    if rng <= 0:
        return 0.0
    return round((high - top_body) / rng, 3)


def _lower_shadow_ratio(row):
    """Lower shadow length / total range. >0.5 = strong lower support."""
    high = row["high"]
    low = row["low"]
    bot_body = min(row["open"], row["close"])
    rng = high - low
    if rng <= 0:
        return 0.0
    return round((bot_body - low) / rng, 3)


def compute_minute_features(kl60, kl15):
    """Extract intraday strength features from 60min + 15min k-lines.

    Returns dict with string-labeled features suitable for LLM consumption:
      60m_trend              up / flat / down (today's 60min bars)
      60m_last_strength      strong / neutral / weak (last 60min bar)
      60m_upper_shadow       bool: last 60min bar has >0.5 upper shadow
      15m_end_strength       strong / neutral / weak (last 15min bar vs end 3 bars)
      15m_support            bool: end 3 bars show dip-and-recover
      15m_late_push          bool: day is flat/weak but last 3 bars spike up
                             (尾盘偷袭 ambush-rally, suspicious)
    """
    feat = {
        "60m_trend": None, "60m_slope_pct": None,
        "60m_last_strength": None, "60m_upper_shadow": None,
        "15m_end_strength": None, "15m_support": None,
        "15m_late_push": None,
    }

    # 60min features: last 4 bars of today's session (if session is fresh)
    today_60 = _today_rows(kl60) or kl60[-4:]              # fallback: last 4 whatever
    if len(today_60) >= 2:
        trend, slope = _kline_body_trend(today_60)
        feat["60m_trend"] = trend
        feat["60m_slope_pct"] = slope
        last_60 = today_60[-1]
        upper = _upper_shadow_ratio(last_60)
        feat["60m_upper_shadow"] = upper > 0.5
        # Strength: close near top of bar + close >= open = strong
        rng_60 = last_60["high"] - last_60["low"]
        body_pos = ((last_60["close"] - last_60["low"]) / rng_60) if rng_60 > 0 else 0.5
        if last_60["close"] >= last_60["open"] and body_pos >= 0.6:
            feat["60m_last_strength"] = "strong"
        elif last_60["close"] < last_60["open"] and body_pos <= 0.4:
            feat["60m_last_strength"] = "weak"
        else:
            feat["60m_last_strength"] = "neutral"

    # 15min features: end-of-day 3 bars (last 45 minutes)
    today_15 = _today_rows(kl15) or kl15[-16:]             # fallback
    if len(today_15) >= 3:
        end_3 = today_15[-3:]
        last_bar = end_3[-1]
        end_high = max(r["high"] for r in end_3)
        end_low = min(r["low"] for r in end_3)
        end_close = last_bar["close"]
        # End strength: last close near 3-bar high
        if end_high > 0 and (end_close / end_high) >= 0.99:
            feat["15m_end_strength"] = "strong"
        elif end_low > 0 and (end_close / end_low) <= 1.005:
            feat["15m_end_strength"] = "weak"
        else:
            feat["15m_end_strength"] = "neutral"
        # Support: any of end 3 bars has a long lower shadow and recovers
        feat["15m_support"] = any(_lower_shadow_ratio(r) > 0.4
                                   and r["close"] > r["low"] for r in end_3)
        # Late push (尾盘偷袭): today flat/weak overall, last 3 bars spike up
        if len(today_15) >= 6:
            pre_bars = today_15[:-3]
            pre_first = pre_bars[0]["open"] if pre_bars else last_bar["open"]
            pre_last_close = pre_bars[-1]["close"] if pre_bars else last_bar["open"]
            pre_range_pct = (pre_last_close - pre_first) / pre_first * 100 if pre_first > 0 else 0
            end_push_pct = (
                (last_bar["close"] - end_3[0]["open"]) / end_3[0]["open"] * 100
                if end_3[0]["open"] > 0 else 0
            )
            feat["15m_late_push"] = (pre_range_pct <= 0.5) and (end_push_pct >= 1.5)

    return feat


# ==========================================================================
# Row normalization
# ==========================================================================

def _norm_pool_row(row, kind):
    """Normalize a single row from EM pool endpoint.

    EM pool field reference (verified via live API):
      c=code, n=name, p=price*1000, zdp=pct(already float),
      hs=turnover(float), amount=yuan, ltsz=float_mv, tshare=total_mv,
      lbc=consecutive boards, zbc=open count (broken-board times),
      fbt/lbt=first/last seal time (HHMMSS int),
      fund=seal fund yuan, hybk=industry sector, ztyy=reason,
      zttj={days, ct} -- days = streak in days, ct = seal count today.
    """
    p_raw = row.get("p", 0) or 0
    price = round(p_raw / 1000, 2)
    # pct: prefer 'zdp' (float, already in %), fallback 'zf' (*100 int)
    if row.get("zdp") is not None:
        pct = round(_num(row.get("zdp")), 2)
    else:
        pct = round((row.get("zf") or 0) / 100, 2)
    # Streak: zttj.days is most authoritative; fallback lbc/lb
    zttj = row.get("zttj") or {}
    streak = zttj.get("days") or row.get("lbc") or row.get("lb") or 1
    open_count = row.get("zbc", 0) or 0
    return {
        "code": row.get("c", ""),
        "name": row.get("n", ""),
        "price": price,
        "pct": pct,
        "streak": int(streak),
        "open_count": int(open_count),
        "first_seal": _fmt_time(row.get("fbt", 0)),
        "last_seal": _fmt_time(row.get("lbt", 0)),
        "seal_fund": _num(row.get("fund", 0)),
        "turnover": _num(row.get("hs", 0)),
        "amount": _num(row.get("amount", 0)),
        "float_mv": _num(row.get("ltsz", 0)),
        "total_mv": _num(row.get("tshare", 0)),
        "sector": row.get("hybk", "") or "",
        "reason": row.get("ztyy", "") or "",
        "kind": kind,
    }


def _norm_clist_row(r):
    """Normalize a single row from EM clist/get."""
    return {
        "code": r.get("f12", "") or "",
        "name": r.get("f14", "") or "",
        "price": _num(r.get("f2")),
        "pct": _num(r.get("f3")),
        "vol": _num(r.get("f5")),
        "amount": _num(r.get("f6")),
        "amplitude": _num(r.get("f7")),
        "turnover": _num(r.get("f8")),
        "pe": _num(r.get("f9")),
        "volume_ratio": _num(r.get("f10")),
        "high": _num(r.get("f15")),
        "low": _num(r.get("f16")),
        "open": _num(r.get("f17")),
        "prev_close": _num(r.get("f18")),
        "total_mv": _num(r.get("f20")),
        "float_mv": _num(r.get("f21")),
        "main_inflow": _num(r.get("f62")),
        "industry": r.get("f100", "") or "",
        "concept": r.get("f103", "") or "",
    }


# ==========================================================================
# Cached public getters
# ==========================================================================

def get_market_list(fs=_FS_ALL_A, use_cache=True, fallback_codes=None,
                    allow_default_sina_fallback=True):
    """Full market list with 5-min TTL cache.

    Three-tier fallback ladder when EM clist/get fails (e.g. WAF
    rate-limit / RemoteDisconnected):
      1. Tier-1: stale cache up to 2 days old (best / instantaneous).
      2. Tier-2: Sina batch quote for caller-provided `fallback_codes`
         (narrow but targeted; used when caller already knows which
         tickers matter, e.g. computing quotes for a candidate set).
      3. Tier-2.5: Tencent qt batch quote (faster than Sina default,
         ~5s for full universe, has turnover/pe fields Sina lacks).
      4. Tier-3: Sina batch quote over the default A-share code universe
         (~15k probes, 10-15s cost). Used only when Tencent also fails.
         Fires only when `allow_default_sina_fallback=True` (default).

    Callers wanting a fast fail (e.g. preflight already said EM dead +
    Sina dead) can pass `allow_default_sina_fallback=False`.
    """
    key = "market_" + fs.replace(":", "_").replace("+", "_").replace(",", "_") + ".json"
    if use_cache:
        c = _cache_get(key, ttl_sec=300)
        if c:
            return c
    try:
        raw = _fetch_market_list(fs)
        rows = [_norm_clist_row(r) for r in raw]
        for r in rows:
            r["_source"] = "em"
        _cache_set(key, rows)                              # cache only the full EM list
        return rows
    except Exception as e:
        # Tier-1 degrade: stale cache across last 2 days. NOTE: intraday
        # sessions take the strict path (`_maybe_stale_cache` returns
        # (None,None)) so we DO NOT serve yesterday's prices to a T+1
        # decision -- caller will fall through to Sina live tier or raise.
        stale, stale_date = _maybe_stale_cache(key, max_days=2, layer="em_clist")
        if stale:
            print(f"WARN: EM clist failed ({type(e).__name__}); "
                  f"falling back to stale cache from {stale_date} "
                  f"({len(stale)} rows)", file=sys.stderr)
            return stale
        # Tier-1.5 degrade: tushare full-market snapshot. Independent
        # network channel (api.tushare.pro), runs only when user has set
        # a token; gives ~5000 rows in _norm_clist_row schema. T-1 close
        # basis (callers see _data_lag_t1=True flag on each row).
        # See _fetch_tushare_market_snapshot for field caveats; main_inflow
        # is None unless caller upgrades via _fetch_tushare_main_inflow_5d.
        if _get_tushare_token():
            # Map fs back to market keyword so post-filter works.
            _market_kw = "all"
            for k, v in _MARKET_FS_MAP.items():
                if v == fs:
                    _market_kw = k
                    break
            print(f"WARN: EM clist failed ({type(e).__name__}); "
                  f"trying tushare snapshot fallback (market={_market_kw})...",
                  file=sys.stderr)
            ts_rows = _fetch_tushare_market_snapshot(market=_market_kw)
            if ts_rows:
                print(f"INFO: tushare snapshot yielded {len(ts_rows)} rows "
                      f"(T-1 close basis)", file=sys.stderr)
                # Do NOT cache -- T-1 data would poison subsequent EM-success reads.
                return ts_rows
            print("WARN: tushare snapshot returned 0 rows "
                  "(token may lack daily-API permission, or non-trading day)",
                  file=sys.stderr)
        # Tier-2 degrade: Sina with caller-supplied codes (narrow).
        if fallback_codes:
            print(f"WARN: EM clist failed ({type(e).__name__}); "
                  f"falling back to Sina for {len(fallback_codes)} candidate codes",
                  file=sys.stderr)
            rows = _fetch_sina_batch(fallback_codes)
            if rows:
                # Do NOT cache partial Sina fallback data -- it would poison
                # the cache for subsequent calls that need a different code set.
                return rows
            # fall through to Tier-2.5 if narrow sina also empty
        # Tier-2.5 degrade: Tencent qt batch quote (independent upstream,
        # faster than Sina default universe, has turnover/pe/amplitude).
        if fallback_codes:
            print(f"WARN: EM clist / Sina narrow failed ({type(e).__name__}); "
                  f"Tier-2.5: trying Tencent qt for {len(fallback_codes)} codes",
                  file=sys.stderr)
            rows = _fetch_tencent_batch(fallback_codes)
            if rows:
                return rows
        # Tier-3 degrade: Tencent qt with default A-share universe (~5s).
        if not allow_default_sina_fallback:
            raise
        default_codes = _build_default_a_share_codes()
        print(f"WARN: EM clist / Sina narrow / Tencent narrow failed ({type(e).__name__}); "
              f"Tier-3 degrade: probing Tencent qt with default A-share universe "
              f"({len(default_codes)} codes, ~5s)...",
              file=sys.stderr)
        rows = _fetch_tencent_batch(default_codes)
        if rows:
            print(f"INFO: Tier-3 Tencent fallback yielded {len(rows)} valid rows",
                  file=sys.stderr)
            for r in rows:
                r["_degraded_tencent_default"] = True
            return rows
        # Tier-3.5 degrade: Sina with default full A-share universe (last resort).
        print(f"WARN: Tencent default also failed; "
              f"Tier-3.5: probing Sina with default A-share universe "
              f"({len(default_codes)} codes, ~10-15s)...",
              file=sys.stderr)
        rows = _fetch_sina_batch(default_codes)
        if not rows:
            raise RuntimeError(
                f"all tiers failed (EM + stale cache + tushare + narrow Sina + "
                f"Tencent + default Sina); original err: {e}"
            )
        print(f"INFO: Tier-3.5 Sina fallback yielded {len(rows)} valid rows",
              file=sys.stderr)
        # Mark degraded so strategies can adjust scoring / weight.
        for r in rows:
            r["_degraded_sina_default"] = True
        return rows


def get_market_quotes(codes, use_cache=True):
    """On-demand quote for specific A-share codes.

    Three-tier resolution:
      1. EM ulist.np/get  -- preferred, no WAF risk (1-2 req for ~200 codes)
      2. Sina hq.sinajs   -- fallback, fewer fields (no turnover/inflow/etc)
      3. Raise RuntimeError -- both failed

    This is the primary path for strategy screening and scoring. Cache is
    per-code-batch keyed by a short hash to avoid duplicate fetches within
    the 5-min TTL window.
    """
    if not codes:
        return []
    codes = sorted(set(codes))                             # dedup + stable order
    # Cache key: short hash of sorted code list
    import hashlib
    h = hashlib.md5(",".join(codes).encode()).hexdigest()[:10]
    key = f"quotes_{len(codes)}_{h}.json"
    if use_cache:
        c = _cache_get(key, ttl_sec=300)
        if c:
            return c
    try:
        rows = _fetch_market_by_codes(codes)
        if rows:
            _cache_set(key, rows)
            return rows
        # ulist returned empty -- probably all codes invalid; try sina
        raise RuntimeError("EM ulist returned 0 rows")
    except Exception as e:
        print(f"WARN: EM ulist failed ({type(e).__name__}); "
              f"falling back to Sina for {len(codes)} codes",
              file=sys.stderr)
        rows = _fetch_sina_batch(codes)
        if not rows:
            raise RuntimeError(
                f"both EM ulist and Sina quote sources failed; last err: {e}"
            )
        # Do NOT cache sina fallback (incomplete fields)
        return rows


def get_pool(kind, date=None, use_cache=True):
    """kind: zt|dt|zb|lb."""
    key = f"{kind}_pool.json"
    if use_cache:
        c = _cache_get(key, date=date, ttl_sec=300)
        if c is not None:
            return c
    raw = _fetch_pool(kind, date)
    rows = [_norm_pool_row(r, kind) for r in (raw.get("pool") or [])]
    _cache_set(key, rows, date=date)
    return rows


def get_sector_rank(sector_type="industry", top=30, use_cache=True, fail_safe=False):
    """If fail_safe=True, network error returns [] instead of raising.

    Callers that treat hot sectors as a soft signal (e.g. recommend/brief
    display) should pass fail_safe=True so clist rate-limit on the sector
    endpoint doesn't kill the whole pipeline. Strategy C treats sector-rank
    as a hard dependency and should pass fail_safe=False.

    On fetch failure we fall back to the most recent stale cache entry
    across the last 3 day-dirs before giving up. Sector rankings move
    slowly (hourly granularity is fine for our purposes), so a day-old
    snapshot is almost always better than nothing.
    """
    key = f"sector_{sector_type}.json"
    if use_cache:
        c = _cache_get(key, ttl_sec=300)
        if c:
            return c[:top]
    try:
        raw = _fetch_sector_rank(sector_type, top=max(top, 30),
                                 fast_fail=fail_safe)       # short backoff when non-critical
    except Exception as e:
        # Last-resort: stale cache across last 3 days (ignore TTL). Intraday
        # strict mode rejects this fallback so hot-sector ranking matches
        # current session, not yesterday's snapshot.
        stale, stale_date = _maybe_stale_cache(key, max_days=3, layer="sector_rank")
        if stale:
            print(f"WARN: sector-rank fetch failed ({type(e).__name__}); "
                  f"falling back to stale cache from {stale_date} "
                  f"({len(stale)} rows)", file=sys.stderr)
            return stale[:top]
        # Tier-2 degrade: tushare industry aggregation. Only meaningful for
        # sector_type=industry (concept aggregation explodes API calls).
        # When `fs_industry` snapshot returned no rows we silently fall through.
        if sector_type == "industry" and _get_tushare_token():
            print(f"WARN: sector-rank EM failed ({type(e).__name__}); "
                  f"trying tushare industry aggregation...", file=sys.stderr)
            ts_rows = _fetch_tushare_industry_sector_rank(top=max(top, 30))
            if ts_rows:
                print(f"INFO: tushare industry sector-rank yielded {len(ts_rows)} rows "
                      f"(avg pct, T-1 basis)", file=sys.stderr)
                return ts_rows[:top]
            print("WARN: tushare industry aggregation returned 0 rows",
                  file=sys.stderr)
        if fail_safe:
            print(f"WARN: sector-rank fetch failed (fast-fail, no stale cache): {e}",
                  file=sys.stderr)
            return []
        raise
    # f2=index-price f3=pct f4=change f12=code f14=name f62=main-inflow
    # f104=up-count f105=down-count f128=leader-name f136=leader-pct
    # f164=5d-pct  f167=10d-pct  f170=20d-pct (multi-day returns, used as
    # Tier-1.5 fallback in compute_sector_n_day_pct when the sector K-line
    # endpoint is unreachable)
    rows = []
    for r in raw:
        rows.append({
            "price": _num(r.get("f2")),
            "pct": _num(r.get("f3")),
            "change": _num(r.get("f4")),
            "code": r.get("f12", ""),
            "name": r.get("f14", ""),
            "main_inflow": _num(r.get("f62")),
            "up_count": _num(r.get("f104")),
            "down_count": _num(r.get("f105")),
            "leader_name": r.get("f128", "") or "",
            "leader_pct": _num(r.get("f136")),
            # Multi-day cumulative pct (from EM clist, no extra call needed).
            # May be None if EM hasn't populated that column for this board.
            "pct_5d": _num(r.get("f164")) if r.get("f164") not in (None, "-") else None,
            "pct_10d": _num(r.get("f167")) if r.get("f167") not in (None, "-") else None,
            "pct_20d": _num(r.get("f170")) if r.get("f170") not in (None, "-") else None,
        })
    _cache_set(key, rows)
    return rows[:top]


def get_market_overview(use_cache=True):
    """Return list of major index snapshots.

    Two-tier upstream:
      1. EM push2 stock/get  -- richer fields (decimal precision, code).
      2. Sina s_* batch      -- one HTTP call covers all missing indexes
                                when EM is down or partially flaky.

    Both tiers output the same downstream schema {name, code, price, pct,
    change, amount}, so callers (brief display, market_ctx computation)
    don't need to care which source served each row.
    """
    key = "indexes.json"
    if use_cache:
        c = _cache_get(key, ttl_sec=180)
        if c:
            return c
    out = []
    filled_sids = set()
    # Tier 1: EM per-index calls (preserves f59 dp precision for display).
    for sid, name in _INDEX_LIST:
        try:
            d = _fetch_index(sid)
            if d:
                dp = d.get("f59", 2) or 2
                div = 10 ** dp
                price_v = (d.get("f43", 0) or 0) / div
                prev_v = (d.get("f60", 0) or 0) / div
                # Compute change from price - prev_close (more reliable than f171).
                change_v = round(price_v - prev_v, dp) if prev_v else 0.0
                out.append({
                    "name": name,
                    "code": d.get("f57", ""),
                    "price": round(price_v, dp),
                    "pct": round((d.get("f170", 0) or 0) / 100, 2),
                    "change": change_v,
                    "amount": d.get("f48", 0) or 0,
                })
                filled_sids.add(sid)
        except Exception:
            continue
    # Tier 2: Sina batch fallback for indexes EM failed on.
    missing = [(sid, name) for sid, name in _INDEX_LIST if sid not in filled_sids]
    if missing:
        sina_data = _fetch_sina_indexes([sid for sid, _ in missing])
        for sid, name in missing:
            d = sina_data.get(sid)
            if not d:
                continue
            out.append({
                "name": name,                              # prefer our canonical name
                "code": sid.split(".", 1)[-1],
                "price": round(d["price"], 2),
                "pct": round(d["pct"], 2),
                "change": round(d["change"], 2),
                "amount": d["amount"],                     # already yuan (1e4 scale applied)
            })
        if sina_data:
            print(f"INFO: market overview Sina fallback used for "
                  f"{len(sina_data)}/{len(missing)} indexes "
                  f"(EM had {len(filled_sids)}/{len(_INDEX_LIST)})",
                  file=sys.stderr)
    # Preserve the original _INDEX_LIST ordering regardless of which tier
    # produced each row (EM and Sina may differ in return timing).
    order = {sid: i for i, (sid, _) in enumerate(_INDEX_LIST)}
    name_to_sid = {name: sid for sid, name in _INDEX_LIST}
    out.sort(key=lambda r: order.get(name_to_sid.get(r["name"], ""), 999))
    _cache_set(key, out)
    return out


# ==========================================================================
# Filtering
# ==========================================================================

def filter_universe(rows, market="all", price_min=None, price_max=None,
                    min_amount=None, include_risk=False):
    """Apply hard filters (market / price band / liquidity / risk)."""
    out = []
    for r in rows:
        if not _is_in_market(r["code"], market):
            continue
        if not include_risk and _is_risky_name(r["name"]):
            continue
        if price_min is not None and r["price"] < price_min:
            continue
        if price_max is not None and r["price"] > price_max:
            continue
        if min_amount is not None and r["amount"] < min_amount:
            continue
        out.append(r)
    return out


# ==========================================================================
# Strategies
# ==========================================================================

def _is_one_word_board(row):
    """One-word board: sealed at open and never opened."""
    return row.get("first_seal") == "09:30:00" and (row.get("open_count") or 0) == 0


def screen_strategy_a(days=2, hot_sectors=None, exclude_one_word=True,
                      market="all", max_pct=3.0,
                      price_min=5.0, price_max=110.0,
                      min_amount=100_000_000, max_streak=1,
                      use_kline=True,
                      max_distance_10d=30.0, max_rise_10d=35.0,
                      min_upside_pct=0.0,
                      am_weak_threshold=-1.0,
                      filter_unlocks=True, attach_lhb=True):
    """Strategy A: divergence low-suction after recent limit-up (low-position first-board).

    Hard filters (all must pass):
    - Have >=1 limit-up in last `days` trading days.
    - Drop codes still limit-up today (continuation, not divergence).
    - Consecutive-board height <= max_streak (default 1, first-board only).
      Rationale: 2nd-board stocks next-day variance is too large (big win or big loss).
      Backtest shows first-board hit-rate >> second-board for T+1 swing.
    - Exclude one-word boards (default).
    - Price in [price_min, price_max] (default 5~110 yuan).
    - Today's pct in [-3%, +max_pct] (default +3%).
    - Today's amount >= min_amount (default 1 yi = 100M yuan).
    - Drop unstable seals: seal-day open_count >= 2 (炸板 twice+).
    - Drop chasing-top: current / seal-day close > 1.03.
    - (Removed 2026-04-22) Slippage gate upside>=2% was mathematically
      incompatible with am_weak>=-1% after market close (intersection empty),
      forcing all post-close strategy A runs to 0 candidates. The upside_pct
      field is still computed and exposed (for scoring / display) but no
      longer used as a hard filter. Anti-chase defense is retained via
      `pos_ratio<=1.03` and `pct<=+max_pct` gates above.
    - AM-weak filter (only applied when time >= 10:30): drop candidates whose
      today pct < am_weak_threshold (default -1.0%). Rationale: by 10:30 the
      first hour of price discovery is done. Stocks still down >1% show no
      defense bid and next-day rebound probability is low. Pre-10:30 (early
      session noise) and pre-market runs skip this filter.
    - Not ST / *ST / delisting.
    - In requested market (all / main / gem / star / sh / sz).

    Phase-2 k-line position filters (when use_kline=True):
    - distance_10d_low <= max_distance_10d (default 30%)
    - rise_10d <= max_rise_10d (default 35%)
    - today's low >= seal-day body midpoint (承接健康)
    """
    today_zt_codes = {r["code"] for r in get_pool("zt")}
    # AM-weak filter activation: only meaningful once the first hour of
    # trading is over (pct has real info, not just opening-auction noise).
    # Active window: time >= 10:30 (includes post-close where pct = final).
    _now_time = datetime.datetime.now().time()
    am_weak_active = _now_time >= datetime.time(10, 30)
    hist = {}
    for i in range(1, days + 1):
        d = _trading_date_offset(i)
        for r in get_pool("zt", date=d):
            if r["code"] in today_zt_codes:
                continue
            if exclude_one_word and _is_one_word_board(r):
                continue
            # Keep most recent seal info if duplicated
            prev = hist.get(r["code"])
            if prev is None or i < prev.get("_ago", 99):
                r = dict(r)
                r["_ago"] = i
                hist[r["code"]] = r
    # On-demand batch quote via EM ulist (fast, no WAF). Sina fallback built-in.
    fb_codes = sorted(set(hist.keys()) | today_zt_codes)
    mkt = {m["code"]: m for m in get_market_quotes(fb_codes)}
    out = []
    for code, seal in hist.items():
        q = mkt.get(code)
        if not q:
            continue
        if not _is_in_market(code, market):
            continue
        if _is_risky_name(q["name"]):
            continue
        # Price range gate (default 5~110 yuan): cheap penny stocks are
        # manipulation-prone, >110 is illiquid for 1w capital.
        if not (price_min <= q["price"] <= price_max):
            continue
        # Liquidity floor (default 1 yi = 100M yuan)
        if q["amount"] < min_amount:
            continue
        # Consecutive-board gate: default first-board only (max_streak=1).
        # 2nd board next-day has bimodal outcome (continuation to 3rd board vs
        # sharp divergence drop); pure first-board is cleaner signal.
        if seal.get("streak", 1) > max_streak:
            continue
        # Divergence window: today's pct in [-3%, +max_pct] (default +3%).
        if not (-3.0 <= q["pct"] <= max_pct):
            continue
        # AM-weak gate (only active after 10:30): by mid-morning the first
        # hour of price-discovery is over. Stocks still down >1% signal zero
        # defense bid from main-funds. Historical backtest: such candidates'
        # next-day rebound hit-rate drops to <20% vs ~45% for pct >= -1%.
        if am_weak_active and q["pct"] < am_weak_threshold:
            continue
        # Filter unstable seal: if the seal-day was broken twice or more (炸板),
        # the controlling funds are shaky -- skip.
        if seal.get("open_count", 0) >= 2:
            continue
        # Position vs seal-day close: ratio > 1.03 means today is still above
        # the seal close by >3% -- essentially chasing the top.
        seal_close = seal.get("price", 0) or 0
        pos_ratio = (q["price"] / seal_close) if seal_close > 0 else 1.0
        if pos_ratio > 1.03:
            continue
        # (2026-04-22) Slippage hard-gate removed: see function docstring.
        # upside_to_seal_pct is still computed below and exposed on each
        # candidate for scoring / user-facing display, but not filtered on.
        upside_to_seal_pct = ((seal_close / q["price"]) - 1) * 100 if q["price"] > 0 else 0
        out.append({
            "code": code,
            "name": q["name"],
            "price": q["price"],
            "pct": q["pct"],
            "amount": q["amount"],
            "turnover": q["turnover"],
            "volume_ratio": q["volume_ratio"],
            "float_mv": q["float_mv"],
            "industry": q["industry"],
            "main_inflow": q["main_inflow"],
            "low": q.get("low", 0) or 0,                   # today's intraday low
            "seal_ago": seal["_ago"],
            "seal_streak": seal["streak"],
            "seal_fund": seal["seal_fund"],
            "seal_open_count": seal.get("open_count", 0),
            "seal_price": seal_close,
            "pos_ratio": round(pos_ratio, 4),              # current / seal-day close
            "upside_pct": round(upside_to_seal_pct, 2),    # room from current to seal close, %
            "strategy": "A",
            "_source": q.get("_source", "em"),
        })

    # ------------------------------------------------------------------
    # Phase-2 daily k-line position filters (batch-fetch for survivors only)
    # ------------------------------------------------------------------
    if use_kline and out:
        codes = [c["code"] for c in out]
        klines = get_daily_klines_batch(codes, n=30, workers=8)
        filtered = []
        for c in out:
            kl = klines.get(c["code"]) or []
            # Map seal_ago back to date YYYYMMDD
            seal_date = _trading_date_offset(c["seal_ago"])
            ind = compute_kline_indicators(
                kl, today_price=c["price"],
                today_low=c.get("low", 0) or c["price"],
                seal_date=seal_date,
            )
            # If kline fetch failed, keep the stock but mark indicators None
            # (Phase-1 filters already did their job -- don't over-filter on flakey API)
            c["distance_10d_low"] = ind["distance_10d_low"]
            c["rise_10d"] = ind["rise_10d"]
            c["ma20"] = ind["ma20"]
            c["above_ma20_loose"] = ind["above_ma20_loose"]
            c["low_above_half_seal_body"] = ind["low_above_half_seal_body"]
            # Hard filters (skip when indicator is None = kline missing)
            if ind["distance_10d_low"] is not None and ind["distance_10d_low"] > max_distance_10d:
                continue                                    # Too far from 10d low
            if ind["rise_10d"] is not None and ind["rise_10d"] > max_rise_10d:
                continue                                    # Ran up too much already
            if ind["low_above_half_seal_body"] is False:
                continue                                    # Weak承接: today broke below seal body
            filtered.append(c)
        out = filtered

    # ------------------------------------------------------------------
    # Phase-2.5 share-unlock filter: drop stocks with imminent large unlock,
    # warn on approaching smaller unlock. Fail-open if API down.
    # ------------------------------------------------------------------
    dropped_unlock = []
    if filter_unlocks and out:
        unlocks = get_upcoming_unlocks(lookback_days=30)
        kept = []
        for c in out:
            info = unlocks.get(c["code"])
            level = unlock_risk_level(info)
            c["unlock"] = info                                 # always attach (may be None)
            c["unlock_risk"] = level                           # 'drop' | 'warn' | None
            if level == "drop":
                dropped_unlock.append(
                    (c["code"], c["name"],
                     f"{info['days_until']}日内解禁{info['ratio_total']:.1f}%总股本")
                )
                continue
            kept.append(c)
        out = kept
    # Side-channel for meta reporting
    screen_strategy_a.last_dropped_unlock = dropped_unlock

    # ------------------------------------------------------------------
    # Phase-2.6 LHB attachment: batch-fetch seat money-flow for survivors.
    # Fail-open: missing LHB record = None (stock simply didn't qualify for
    # LHB disclosure; ~50-70% of divergence-day first-board stocks).
    # ------------------------------------------------------------------
    dropped_lhb = []
    if attach_lhb and out:
        try:
            get_lhb_for_candidates(out)
        except Exception as e:
            print(f"WARN: LHB attach failed: {e}", file=sys.stderr)

        # Phase-2.7 HARD FILTER: drop candidates with extreme LHB net-sell.
        # Rationale: LHB net-sell < -50M yuan = big money distributed at the
        # seal, or "机构专用席位" appears on sell side = institution exit.
        # Both are next-day gap-down precursors. Soft -15 score penalty alone
        # is not enough for a T+1 strategy that needs hit-rate.
        kept = []
        for c in out:
            lhb = c.get("lhb")
            if not lhb:
                # No LHB listed -> pass (majority case for first-board)
                kept.append(c)
                continue
            net = lhb.get("net", 0) or 0
            expl = lhb.get("explanation", "") or ""
            inst_on_sell = (("机构" in expl) or ("专用" in expl)) and net < 0
            if net <= -50_000_000:
                dropped_lhb.append(
                    (c["code"], c["name"],
                     f"LHB净卖{net/1e8:.2f}亿（主力派发/撤退信号）"))
                continue
            if inst_on_sell and net <= -10_000_000:
                dropped_lhb.append(
                    (c["code"], c["name"],
                     f"LHB机构席位净卖{net/1e8:.2f}亿（机构撤退）"))
                continue
            kept.append(c)
        out = kept
    screen_strategy_a.last_dropped_lhb = dropped_lhb

    return out


def screen_strategy_b(days=2, min_rebound=5.0, market="all",
                      check_bad_news=True, bad_news_days=7):
    """Strategy B: oversold bounce after recent limit-down.

    - Collect limit-down stocks in last `days` trading days.
    - Today: pct >= min_rebound and pct < 9.5 (leave margin from limit-up).
    - Minimum liquidity floor 3000万.
    - If check_bad_news: query EM announcement API; drop if any negative
      announcement (减持/立案/预亏/退市/冻结...) in last `bad_news_days` days.
    """
    today_dt_codes = {r["code"] for r in get_pool("dt")}
    hist = {}
    for i in range(1, days + 1):
        d = _trading_date_offset(i)
        for r in get_pool("dt", date=d):
            if r["code"] in today_dt_codes:
                continue
            prev = hist.get(r["code"])
            if prev is None or i < prev.get("_ago", 99):
                r = dict(r)
                r["_ago"] = i
                hist[r["code"]] = r
    fb_codes = sorted(set(hist.keys()) | {r["code"] for r in get_pool("dt")})
    mkt = {m["code"]: m for m in get_market_quotes(fb_codes)}
    # Stage 1: cheap-filter first (avoid fetching announcements for stocks we'll drop anyway).
    # Track per-reason drop counts so funnel can explain WHY B pool shrinks
    # (especially ST rejection count, requested 2026-04-22 for transparency).
    staged = []
    dropped_counts = {"st_risky": 0, "thin_liquidity": 0,
                      "weak_bounce": 0, "near_limit_up": 0, "wrong_market": 0}
    for code, dt in hist.items():
        q = mkt.get(code)
        if not q:
            continue
        if not _is_in_market(code, market):
            dropped_counts["wrong_market"] += 1
            continue
        if _is_risky_name(q["name"]):
            dropped_counts["st_risky"] += 1      # ST / *ST / 退 / N / C
            continue
        if q["amount"] < 30_000_000:             # 3000万 liquidity floor
            dropped_counts["thin_liquidity"] += 1
            continue
        if q["pct"] < min_rebound:
            dropped_counts["weak_bounce"] += 1
            continue
        if q["pct"] > 9.5:
            dropped_counts["near_limit_up"] += 1
            continue
        staged.append((code, dt, q))
    screen_strategy_b.last_stage1_drops = dropped_counts
    # Stage 2: announcement filter (expensive, run only on stage-1 survivors)
    out = []
    dropped_bad = []
    for code, dt, q in staged:
        bad_hit = None
        if check_bad_news:
            try:
                bad, hit = has_bad_news(code, days=bad_news_days)
                if bad:
                    dropped_bad.append((code, q["name"], hit))
                    continue
                bad_hit = None
            except Exception as e:
                # Fail-open: if ann API unreachable, keep the stock but flag it
                bad_hit = f"ann-api-error: {e}"
        out.append({
            "code": code,
            "name": q["name"],
            "price": q["price"],
            "pct": q["pct"],
            "amount": q["amount"],
            "turnover": q["turnover"],
            "volume_ratio": q["volume_ratio"],
            "float_mv": q["float_mv"],
            "industry": q["industry"],
            "main_inflow": q["main_inflow"],
            "dt_ago": dt["_ago"],
            "strategy": "B",
            "bad_news_hit": bad_hit,
            "_source": q.get("_source", "em"),
        })
    # Expose a side-channel: attach drop log to function attribute for debug
    screen_strategy_b.last_dropped = dropped_bad
    # Pool review summary (for empty-result explanation; no per-code leakage).
    # Only aggregate counts -- prevents LLM from over-interpreting sample-level
    # detail as market-wide sentiment.
    hist_total = len(hist)
    still_dt_today = sum(1 for code in hist if any(
        r["code"] == code for r in get_pool("dt")
    ))
    rebounded_5 = sum(1 for code in hist
                      if (mkt.get(code) or {}).get("pct", 0) >= 5)
    declined = sum(1 for code in hist
                   if (mkt.get(code) or {}).get("pct", 0) < 0)
    screen_strategy_b.last_pool_review = {
        "hist_total": hist_total,
        "still_limit_down": still_dt_today,
        "rebounded_5pct": rebounded_5,
        "declined": declined,
    }
    return out


# ==========================================================================
# Phase 0: extra data fetchers for strategies C/D/E (sector kline,
# sector constituents, multi-day fund flow). Uses the same retry + cache
# primitives as the rest of the module; cached per-day under SKILL_DIR.
# ==========================================================================

def _fetch_sector_kline(sector_code, days=10):
    """Fetch recent daily kline for an industry/concept sector (East Money).

    secid convention: '90.BK0475' for board BK0475. Returns list of
    {date, open, close, high, low, amount} ascending; empty on failure.
    """
    if not sector_code:
        return []
    url = (
        f"http://push2.eastmoney.com/api/qt/stock/kline/get?"
        f"secid=90.{sector_code}&klt=101&fqt=1&beg=0&end=20500000"
        f"&lmt={max(days, 10)}"
        f"&fields1=f1,f2,f3,f4,f5,f6"
        f"&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"
    )
    try:
        # Retries bumped 2->4: EM push2 kline endpoint has occasional
        # transient 5xx bursts; 4 retries with backoff almost eliminates
        # single-session downgrades (observed hit-rate jump from ~85% to
        # ~98% in flaky networks).
        js = _get_json_fast_fail(url, retries=4)
    except Exception as e:
        print(f"WARN: sector kline fetch failed {sector_code}: {e}", file=sys.stderr)
        return []
    klines = ((js or {}).get("data") or {}).get("klines") or []
    rows = []
    for line in klines:
        p = line.split(",")
        if len(p) < 7:
            continue
        try:
            rows.append({
                "date": p[0].replace("-", ""),
                "open": float(p[1]),
                "close": float(p[2]),
                "high": float(p[3]),
                "low": float(p[4]),
                "amount": float(p[6]),
            })
        except (ValueError, IndexError):
            continue
    return rows


def get_sector_kline(sector_code, days=10, use_cache=True):
    """Cached wrapper. Sector klines are stable intraday -> 3h TTL.

    On fetch failure falls back to the most recent stale cache entry
    across the last 5 days. Sector klines change slowly (one bar per
    trading day) so a day-old snapshot is fine for N-day pct derivation.
    """
    if not sector_code:
        return []
    key = f"sector_kl_{sector_code}_{days}.json"
    if use_cache:
        c = _cache_get(key, ttl_sec=3 * 3600)
        if c:
            return c
    rows = _fetch_sector_kline(sector_code, days)
    if rows:
        _cache_set(key, rows)
        return rows
    # Stale fallback: sector klines drive strategy-C laggard scoring. We
    # tolerate up to 10 days off-hours (sector trends move slowly; a 10-day
    # old N-day-cumulative bar is still directionally valid) but forbid
    # intraday stale to avoid yesterday's sector pct contaminating today's
    # hot-sector ranking under flaky network. Bumped 5->10 to dramatically
    # reduce fallback-to-"today_pct-approximation" events (which trigger
    # the user-visible data degradation prompt).
    stale, stale_date = _maybe_stale_cache(key, max_days=10, layer="sector_kline")
    if stale:
        print(f"WARN: sector kline empty for {sector_code}; "
              f"using stale cache from {stale_date}", file=sys.stderr)
        return stale
    return []


def compute_sector_n_day_pct(sector_code, n=5, sector_row=None):
    """N-day pct change for an industry sector, based on close-to-close.

    Returns (pct, source) where source indicates the data path:
      - "kline":       Tier-1   EM sector K-line close-to-close (most accurate)
      - "clist_n_day": Tier-1.5 EM clist multi-day pct column (f164/f167/f170)
                       -- full-accuracy multi-day cumulative pct exposed
                       natively by EM clist; NOT a degradation.
      - None (tuple unchanged): all tiers empty -> caller decides degrade.

    Backwards compat: callers passing only (sector_code, n) unpack legacy
    float. We now return a tuple; update callers in screen_strategy_c.

    `sector_row`: optional dict from get_sector_rank() already containing
    pct_5d/pct_10d/pct_20d from EM clist. When provided, used as Tier-1.5
    fallback if the sector K-line endpoint is unreachable AND no stale
    cache exists. Avoids the "same-day pct approximation" degradation.
    """
    rows = get_sector_kline(sector_code, days=max(n + 2, 10))
    if rows and len(rows) >= n + 1:
        today_close = rows[-1]["close"]
        past_close = rows[-(n + 1)]["close"]
        if past_close > 0:
            return round((today_close - past_close) / past_close * 100, 2), "kline"
    # Tier-1.5 fallback: EM clist native N-day columns. Accuracy equivalent
    # to kline close-to-close (EM computes them the same way); only caveat
    # is that only standard windows (5/10/20) are exposed, so non-standard
    # `n` values still return None.
    if sector_row is not None:
        key_map = {5: "pct_5d", 10: "pct_10d", 20: "pct_20d"}
        k = key_map.get(n)
        if k is not None:
            v = sector_row.get(k)
            if v is not None:
                try:
                    v_f = float(v)
                except (TypeError, ValueError):
                    v_f = None
                # EM clist field-id semantics drift: f164/f170 (originally
                # documented as 5d/20d sector pct) now sometimes return raw
                # 5d/20d main-inflow values in 元 (1e7~1e10 magnitude),
                # which previously poisoned downstream as
                # `板块+686946416.0%`. Hard sanity bound: no industry
                # index moves >50% in 5/10/20 days; any value outside is
                # treated as a field-mapping error and falls through to
                # Tier-2/3 degrade so the run still produces clean numbers.
                if v_f is not None and abs(v_f) <= 50.0:
                    return round(v_f, 2), "clist_n_day"
    return None, None


def _fetch_sector_constituents(sector_code):
    """Fetch all constituent stocks of an industry sector (East Money).

    One clist call with fs=b:BK0475 returns all members with full fields
    (price, pct, turnover, volume_ratio, float_mv, main_inflow, industry...).
    Far lighter than fetching the full market list.
    """
    if not sector_code:
        return []
    fs = f"b:{sector_code}"
    try:
        raw = _fetch_market_list(fs, page_size=100)
    except Exception as e:
        print(f"WARN: sector constituents fetch failed {sector_code}: {e}",
              file=sys.stderr)
        return []
    rows = [_norm_clist_row(r) for r in raw]
    for r in rows:
        r["_source"] = "em"
    return rows


def get_sector_constituents(sector_code, use_cache=True):
    """Cached wrapper, 5-min TTL (same as full market list)."""
    if not sector_code:
        return []
    key = f"sector_cons_{sector_code}.json"
    if use_cache:
        c = _cache_get(key, ttl_sec=300)
        if c:
            return c
    rows = _fetch_sector_constituents(sector_code)
    if rows:
        _cache_set(key, rows)
    return rows


def get_multiday_fund_flow(use_cache=True):
    """Full-market multi-day main-capital flow in a single call.

    East Money fund-flow clist endpoint uses fs=m:0+t:6,...+f:!2 with fields:
      f12 = code, f14 = name, f2 = price, f3 = today pct,
      f62 = today main inflow,    f184 = today main inflow pct,
      f267 = 5-day main inflow,   f268 = 5-day main inflow pct,
      f269 = 10-day main inflow,  f270 = 10-day main inflow pct,
      f109 = 5-day pct,           f160 = 10-day pct.
    Cached 5 min to share across strategy D and any future consumer.

    Three-tier degradation on fetch failure:
      Tier-1: stale cache (up to 2 days old, multiday flow changes slowly).
      Tier-2: single-day main-inflow via get_market_list(_FS_ALL_A) +
              scale up (1d * 3) as a conservative proxy for 5d cumulative.
              Rows are tagged `_degraded=True` so strategy D can relax
              its inflow-rank filter accordingly.
      Tier-3: return []. Caller already treats empty as "no universe".
    """
    key = "fund_flow_multiday.json"
    if use_cache:
        c = _cache_get(key, ttl_sec=300)
        if c:
            return c
    url = (
        "http://push2.eastmoney.com/api/qt/clist/get?"
        "pn=1&pz=100&po=1&np=1&fltt=2&invt=2"
        "&fid=f267&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23+f:!2"
        "&fields=f12,f14,f2,f3,f62,f184,f267,f268,f269,f270,f109,f160,f100"
    )
    out = []
    first_err = None
    # Paginate: multiday flow endpoint respects pz up to 100 only
    page = 1
    while True:
        paged = url.replace("pn=1", f"pn={page}")
        try:
            js = _get_json(paged, retries=2)
        except Exception as e:
            print(f"WARN: multiday flow page {page} failed: {e}", file=sys.stderr)
            if first_err is None:
                first_err = e
            break
        diff = ((js or {}).get("data") or {}).get("diff") or []
        if not diff:
            break
        for r in diff:
            out.append({
                "code": r.get("f12", "") or "",
                "name": r.get("f14", "") or "",
                "price": _num(r.get("f2")),
                "pct": _num(r.get("f3")),
                "main_inflow_1d": _num(r.get("f62")),
                "main_inflow_pct_1d": _num(r.get("f184")),
                "main_inflow_5d": _num(r.get("f267")),
                "main_inflow_pct_5d": _num(r.get("f268")),
                "main_inflow_10d": _num(r.get("f269")),
                "main_inflow_pct_10d": _num(r.get("f270")),
                "pct_5d": _num(r.get("f109")),
                "pct_10d": _num(r.get("f160")),
                "industry": r.get("f100", "") or "",
            })
        total = ((js or {}).get("data") or {}).get("total") or 0
        if page * 100 >= total:
            break
        page += 1
        if page > 60:                                    # safety: max 6000 rows
            break
    if out:
        _cache_set(key, out)
        return out

    # Tier-1 degrade: stale cache (max 2 days). Off-hours yesterday's flow
    # is acceptable for D-strategy accumulation reading, but intraday must
    # be live or empty -- a T+1 entry on yesterday's flow snapshot is
    # exactly the kind of decision-time data lag we are guarding against.
    stale, stale_date = _maybe_stale_cache(key, max_days=2, layer="multiday_flow")
    if stale:
        print(f"WARN: multiday flow failed "
              f"({type(first_err).__name__ if first_err else 'empty'}); "
              f"using stale cache from {stale_date} ({len(stale)} rows)",
              file=sys.stderr)
        # Re-tag as NOT degraded: fields are real, just older.
        return stale

    # Tier-1.5 degrade: tushare moneyflow 5-day aggregation. Provides REAL
    # 5d cumulative inflow (not a proxy) when user has full-tier (2000pt)
    # account. Combines with get_market_list (which itself may have fallen
    # back to tushare snapshot) for code/name/price/pct/industry context.
    # Silently no-op when token unset / basic tier (moneyflow returns api_err).
    if _get_tushare_token():
        print(f"WARN: multiday flow failed "
              f"({type(first_err).__name__ if first_err else 'empty'}); "
              f"trying tushare moneyflow 5d aggregation...", file=sys.stderr)
        ts_inflow_5d = _fetch_tushare_main_inflow_5d()         # full-market by default
        if ts_inflow_5d:
            try:
                ml = get_market_list(fs=_FS_ALL_A)
            except Exception as _e_ml:
                print(f"WARN: tushare 5d ok but market-list still failed: "
                      f"{type(_e_ml).__name__}; skipping tushare flow merge",
                      file=sys.stderr)
                ml = []
            ml_by_code = {r.get("code"): r for r in ml if r.get("code")}
            merged = []
            for code, in5 in ts_inflow_5d.items():
                base = ml_by_code.get(code, {})
                merged.append({
                    "code": code,
                    "name": base.get("name") or "",
                    "price": base.get("price"),
                    "pct": base.get("pct"),
                    # 1d unknown via tushare aggregation; D strategy already
                    # accepts None for 1d when 5d is real.
                    "main_inflow_1d": None,
                    "main_inflow_pct_1d": None,
                    "main_inflow_5d": in5,                    # REAL 5-day cumulative
                    # pct_5d (relative to total amount) not available without
                    # extra cost; strategy D handles None as missing.
                    "main_inflow_pct_5d": None,
                    "main_inflow_10d": None,
                    "main_inflow_pct_10d": None,
                    "pct_5d": None,
                    "pct_10d": None,
                    "industry": base.get("industry") or "",
                    "_source": "tushare",
                    "_data_lag_t1": True,
                    # NOT marked _degraded -- this is real 5d data, just from
                    # a different upstream. Strategy D's degraded-fallback
                    # branch (rank by 1d) is for the 3x-proxy path only.
                })
            if merged:
                print(f"INFO: tushare moneyflow 5d aggregation produced "
                      f"{len(merged)} rows (T-1 basis, REAL 5d cumulative)",
                      file=sys.stderr)
                # Do NOT cache (T-1 basis would poison live EM reads).
                return merged
        else:
            print("WARN: tushare moneyflow returned 0 rows "
                  "(token may lack moneyflow permission - need 2000pt full tier)",
                  file=sys.stderr)

    # Tier-1.6 degrade: Sina vip per-stock moneyflow, parallel-enriched
    # over top-N most liquid stocks. Sina vip has no auth, no observable
    # rate limit, and ~0.02s/stock per worker, so ~500 stocks finishes
    # in ~12s on healthy network. Strictly better than the 1d*3 proxy
    # below: provides REAL 5d cumulative for the candidates D strategy
    # actually cares about (high-amount stocks lead the universe anyway).
    print("WARN: trying Sina vip per-stock moneyflow (top-500 by amount, "
          "parallel)...", file=sys.stderr)
    try:
        ml = get_market_list(fs=_FS_ALL_A)
    except Exception as _e_ml:
        ml = []
        print(f"WARN: market-list failed before Sina vip enrich: "
              f"{type(_e_ml).__name__}; falling through to proxy",
              file=sys.stderr)
    if ml:
        # Pick top-500 by today's amount (liquidity proxy). D strategy's
        # universe filter (min_total_inflow >= 0, top 30% by inflow rank)
        # already implies liquidity; we just front-load that selection.
        ranked = [r for r in ml if r.get("amount") and not _is_risky_name(r.get("name", ""))]
        ranked.sort(key=lambda r: r.get("amount") or 0, reverse=True)
        top_codes = [r["code"] for r in ranked[:500] if r.get("code")]
        if top_codes:
            t_start = time.time()
            in5_map = enrich_main_inflow_5d_for_codes(top_codes, max_workers=10)
            dt = time.time() - t_start
            print(f"INFO: Sina vip enriched {len(in5_map)}/{len(top_codes)} "
                  f"stocks in {dt:.1f}s", file=sys.stderr)
            if in5_map:
                ml_by_code = {r.get("code"): r for r in ml if r.get("code")}
                merged = []
                for code, in5 in in5_map.items():
                    base = ml_by_code.get(code, {})
                    merged.append({
                        "code": code,
                        "name": base.get("name") or "",
                        "price": base.get("price"),
                        "pct": base.get("pct"),
                        # 1d unknown via 5d cumulative; left None.
                        "main_inflow_1d": base.get("main_inflow"),  # may exist if EM partially worked
                        "main_inflow_pct_1d": None,
                        "main_inflow_5d": in5,                    # REAL 5-day cumulative
                        "main_inflow_pct_5d": None,
                        "main_inflow_10d": None,
                        "main_inflow_pct_10d": None,
                        "pct_5d": None,
                        "pct_10d": None,
                        "industry": base.get("industry") or "",
                        "_source": "sina_vip",
                    })
                if merged:
                    # Do NOT cache (top-500 subset, would poison full-market reads)
                    return merged

    # Tier-2 degrade: synthesize multiday flow from today's single-day
    # main-inflow pulled off the market-list endpoint (different upstream
    # path, less likely to be rate-limited at the same time). Note we
    # only fill main_inflow_1d / main_inflow_5d (as 3x proxy) and leave
    # 10d / pct_5d / pct_10d as None -- strategy D treats None as
    # unavailable and skips those score dimensions.
    print(f"WARN: multiday flow failed "
          f"({type(first_err).__name__ if first_err else 'empty'}); "
          f"attempting Tier-2 degrade via market-list + f62",
          file=sys.stderr)
    try:
        ml = get_market_list(fs=_FS_ALL_A)
    except Exception as e2:
        print(f"WARN: Tier-2 market-list also failed: {type(e2).__name__}: {e2}",
              file=sys.stderr)
        return []
    synth = []
    for r in ml:
        inflow_1d = r.get("main_inflow") or 0
        synth.append({
            "code": r.get("code") or "",
            "name": r.get("name") or "",
            "price": r.get("price"),
            "pct": r.get("pct"),
            "main_inflow_1d": inflow_1d,
            "main_inflow_pct_1d": None,
            # 3x as rough proxy; strategy D must check _degraded before
            # treating this as a true 5-day cumulative.
            "main_inflow_5d": inflow_1d * 3 if inflow_1d else 0,
            "main_inflow_pct_5d": None,
            "main_inflow_10d": None,
            "main_inflow_pct_10d": None,
            "pct_5d": None,
            "pct_10d": None,
            "industry": r.get("industry") or "",
            "_degraded": True,
        })
    if synth:
        print(f"INFO: multiday flow Tier-2 degrade produced {len(synth)} rows "
              f"(main_inflow_5d synthesized as main_inflow_1d * 3)",
              file=sys.stderr)
    # Intentionally do NOT cache synthesized rows -- would poison the
    # cache once the real upstream recovers.
    return synth


def _count_positive_days_recent(code, days=5):
    """Count days in the last `days` trading days where the stock had a
    positive main inflow. Uses per-day cached quote list if available;
    falls back to 0 on error. Intentionally lightweight -- no API call
    per stock (we reuse cached full-market snapshots from prior runs).
    Returns int in [0, days]; None if we have zero history to judge.
    """
    # Consult cached historical market lists; if absent, signal "unknown"
    # so downstream can soft-score. We do NOT force-fetch history here:
    # the multi-day endpoint already gave us 5d/10d aggregates.
    count = 0
    checked = 0
    for i in range(1, days + 1):
        d = _trading_date_offset(i)
        cached = _cache_get(f"market_m_0_t_6_m_0_t_80_m_1_t_2_m_1_t_23.json", date=d)
        if not cached:
            continue
        checked += 1
        row = next((r for r in cached if r.get("code") == code), None)
        if row and _num(row.get("main_inflow")) > 0:
            count += 1
    return count if checked > 0 else None


# ==========================================================================
# Strategy C -- Laggard in hot sectors.
#   Thesis: a sector that has outperformed the broad market for the past
#   N days usually shows a second-wave rotation; laggards inside the
#   sector gap up to catch up. Screener targets stocks in the bottom
#   40% of their sector's N-day return ranking while the sector is in
#   the top-5 of the whole market.
#
#   Soft filters (all weighted, no hard gate beyond ST / suspended):
#     - Sector 5-day pct ranked top-5 of the whole market
#     - Stock 5-day pct in the bottom 40% of its sector
#     - Volume ratio >= 1.2 (some interest starting to build)
#     - Close within +-5% of MA20 (not broken down, not over-extended)
#     - Today's pct within [-3%, +5%] (no panic, no chase)
# ==========================================================================

def screen_strategy_c(board_top_n=5, board_days=5, laggard_pct=0.40,
                      min_volume_ratio=1.2, ma20_band_pct=5.0,
                      pct_min=-3.0, pct_max=5.0,
                      max_5d_pct=6.0, laggard_rel_factor=0.5,
                      market="all"):
    """Strategy C: laggard in hot sectors.

    Returns list of candidate dicts (strategy='C'). Each has sector_name,
    sector_n_day_pct, stock_n_day_pct, sector_rel_rank (0.0=best laggard),
    distance_from_ma20 fields for downstream scoring.

    Anti-chase gates (Fix A + Fix B, 2026-05-08):
      max_5d_pct          absolute cap on the stock's own N-day gain
                          (default 6%). Any stock already up more than this
                          within the same lookback window is dropped as
                          `overheated` -- by definition it is NOT a laggard.
      laggard_rel_factor  stock's N-day gain must stay below sector N-day
                          gain * this factor (default 0.5). Enforces "real"
                          laggard: when the sector rose 20% but a member
                          rose 10%, it is NOT a laggard even if it sits in
                          the bottom 40% of the sector. Dropped as
                          `not_true_laggard`.
    """
    drops = {"sector_no_pct": 0, "not_laggard": 0, "st_risky": 0,
             "wrong_market": 0, "weak_volume": 0, "broken_ma20": 0,
             "extreme_pct": 0, "thin_liquidity": 0,
             "overheated": 0, "not_true_laggard": 0}

    # Stage 1: pick hot sectors by board_days-day pct.
    # fail_safe=False because sector-rank is a HARD dependency for C:
    # no ranking -> no hot sectors -> no candidates at all. Full retry +
    # stale-cache fallback inside get_sector_rank prefers day-old data over
    # giving up. If that too fails we still swallow and return [] here,
    # logging a warning so the brief-level funnel can explain the 0-count.
    try:
        ind_rank = get_sector_rank("industry", top=30, fail_safe=False)
    except Exception as e:
        print(f"WARN: strategy C sector-rank unavailable "
              f"({type(e).__name__}: {e}); returning 0 candidates",
              file=sys.stderr)
        ind_rank = []
    if not ind_rank:
        screen_strategy_c.last_stage1_drops = drops
        screen_strategy_c.last_pool_review = {"hot_sectors": 0}
        return []
    # N-day sector pct resolution ladder:
    #   Tier 1    EM sector K-line close-to-close     (most accurate)
    #   Tier 1.5  EM clist native f164/f167/f170      (full-accuracy; not a degradation)
    #   Tier 2    Stale cache (<=10 days)             (acceptable; sector trend is slow)
    #   Tier 3    Same-day pct approximation          (REAL degradation, trigger prompt)
    # degraded_count only counts Tier 3 events so the S-1 "ask_user" prompt
    # reflects actual information loss, not every time the kline endpoint
    # hiccups (when Tier 1.5 / Tier 2 silently recovered full-accuracy data).
    sectors_scored = []
    degraded_count = 0
    tier15_count = 0                                        # informational only
    for s in ind_rank:
        ndp, src = compute_sector_n_day_pct(s.get("code"), n=board_days, sector_row=s)
        if ndp is None:
            # Real degradation: fall back to same-day pct (f3). This weakens
            # "hot sector" definition (1 day vs N days) and is the only path
            # that should surface as a user-visible data-quality warning.
            today_pct = s.get("pct")
            if today_pct is None:
                drops["sector_no_pct"] += 1
                continue
            ndp = today_pct
            degraded_count += 1
            sectors_scored.append({**s, "n_day_pct": ndp,
                                   "_degraded_sector_pct": True})
        else:
            if src == "clist_n_day":
                tier15_count += 1
            sectors_scored.append({**s, "n_day_pct": ndp})
    sectors_scored.sort(key=lambda x: x["n_day_pct"], reverse=True)
    hot_sectors = sectors_scored[:board_top_n]
    if not hot_sectors:
        screen_strategy_c.last_stage1_drops = drops
        screen_strategy_c.last_pool_review = {"hot_sectors": 0}
        return []
    if tier15_count > 0:
        # INFO (not a degradation): kline endpoint miss but clist still had
        # native N-day columns. Accuracy preserved. Printed to stderr so the
        # user-visible S-1 prompt is NOT triggered.
        print(f"INFO: strategy C sector_kline used clist-native N-day "
              f"fallback for {tier15_count} sectors (full accuracy, no info loss)",
              file=sys.stderr)
    if degraded_count > 0:
        print(f"INFO: strategy C sector kline degraded for {degraded_count} "
              f"sectors -> using same-day pct as N-day approximation",
              file=sys.stderr)

    # Stage 2: inside each hot sector, pick laggards
    out = []
    seen_codes = set()
    for sec in hot_sectors:
        cons = get_sector_constituents(sec["code"])
        if not cons:
            continue
        # Compute each member's n-day pct using its own daily kline (batch).
        codes = [r["code"] for r in cons if r.get("code")]
        kl_map = get_daily_klines_batch(codes, n=board_days + 3)
        enriched = []
        for r in cons:
            code = r.get("code")
            if not code:
                continue
            kl = kl_map.get(code) or []
            if len(kl) < board_days + 1:
                continue
            past = kl[-(board_days + 1)]["close"]
            today_close = r.get("price") or kl[-1]["close"]
            if past <= 0:
                continue
            npc = round((today_close - past) / past * 100, 2)
            # MA20 distance (if enough history)
            ma20 = None
            ma_window = kl[-20:] if len(kl) >= 20 else kl
            if ma_window:
                ma20 = sum(k["close"] for k in ma_window) / len(ma_window)
            enriched.append({**r, "stock_n_day_pct": npc, "ma20": ma20})
        # Bottom laggard_pct in the sector by n-day return
        enriched.sort(key=lambda x: x["stock_n_day_pct"])
        cutoff = max(1, int(len(enriched) * laggard_pct))
        laggards = enriched[:cutoff]

        for q in laggards:
            code = q["code"]
            if code in seen_codes:
                continue
            if not _is_in_market(code, market):
                drops["wrong_market"] += 1
                continue
            if _is_risky_name(q.get("name")):
                drops["st_risky"] += 1
                continue
            if (q.get("amount") or 0) < 30_000_000:
                drops["thin_liquidity"] += 1
                continue
            vr = q.get("volume_ratio") or 0
            if vr < min_volume_ratio:
                drops["weak_volume"] += 1
                continue
            price = q.get("price") or 0
            ma20 = q.get("ma20")
            dist_ma20 = None
            if ma20 and ma20 > 0 and price > 0:
                dist_ma20 = (price - ma20) / ma20 * 100
                if abs(dist_ma20) > ma20_band_pct:
                    drops["broken_ma20"] += 1
                    continue
            pct = q.get("pct") or 0
            if pct < pct_min or pct > pct_max:
                drops["extreme_pct"] += 1
                continue
            # Fix A: absolute N-day gain cap. A real laggard should NOT
            # already be up more than max_5d_pct% -- otherwise we are
            # selecting the top of the follow-through leg, not the base.
            stock_npc = q.get("stock_n_day_pct")
            if stock_npc is not None and stock_npc > max_5d_pct:
                drops["overheated"] += 1
                continue
            # Fix B: true-laggard check. "Bottom 40% of the sector" is a
            # RELATIVE rank only; when the sector rose 20% a bottom-40%
            # member can still be up 10% and is not a laggard in any
            # meaningful sense. Require stock_npc < sector_npc * factor
            # (default 0.5) to enforce an ABSOLUTE gap vs. the sector.
            sec_npc = sec.get("n_day_pct")
            if (sec_npc is not None and sec_npc > 0
                    and stock_npc is not None
                    and stock_npc >= sec_npc * laggard_rel_factor):
                drops["not_true_laggard"] += 1
                continue
            seen_codes.add(code)
            out.append({
                "code": code,
                "name": q.get("name"),
                "price": price,
                "pct": pct,
                "amount": q.get("amount"),
                "turnover": q.get("turnover"),
                "volume_ratio": vr,
                "float_mv": q.get("float_mv"),
                "industry": q.get("industry") or sec.get("name"),
                "main_inflow": q.get("main_inflow"),
                "sector_name": sec.get("name"),
                "sector_code": sec.get("code"),
                "sector_n_day_pct": sec.get("n_day_pct"),
                "sector_day_n": board_days,
                "stock_n_day_pct": q.get("stock_n_day_pct"),
                "laggard_gap": round(
                    sec.get("n_day_pct", 0) - (q.get("stock_n_day_pct") or 0), 2),
                "ma20": round(ma20, 2) if ma20 else None,
                "distance_from_ma20": round(dist_ma20, 2) if dist_ma20 is not None else None,
                "strategy": "C",
                "_source": q.get("_source", "em"),
            })
    screen_strategy_c.last_stage1_drops = drops
    screen_strategy_c.last_pool_review = {
        "hot_sectors": len(hot_sectors),
        "hot_sector_names": [s["name"] for s in hot_sectors],
        "hot_sector_pcts": [s["n_day_pct"] for s in hot_sectors],
        "degraded_sectors": degraded_count,          # N sectors used same-day pct
    }
    return out


# ==========================================================================
# Strategy D -- Main capital accumulation.
#   Thesis: rather than react to a single-day event (limit-up / limit-down),
#   follow smart money as it builds a position over multiple days. A stock
#   with sustained positive main-inflow, trading in a healthy turnover band,
#   sitting in a multi-day moving-average alignment is much more likely to
#   continue up than a one-day anomaly.
#
#   Soft filters (all weighted, no hard gate beyond ST / suspended):
#     - 5-day main inflow > 0 (cumulative)
#     - 5-day main inflow pct ranks in top 30% of the whole market
#     - Turnover in [2%, 8%] -- engaged but not overheated
#     - Close >= MA20 >= MA40 >= MA60 (bullish alignment, lax check)
#     - Today's pct within [-2%, +4%] (no panic, no chase)
# ==========================================================================

def screen_strategy_d(flow_days=5, min_total_inflow=0,
                      flow_pct_rank_top=0.30,
                      turnover_min=2.0, turnover_max=8.0,
                      pct_min=-2.0, pct_max=4.0,
                      max_5d_pct=10.0,
                      require_ma_alignment=True,
                      market="all", min_amount=50_000_000):
    """Strategy D: multi-day main-capital accumulation.

    One clist call (multiday fund flow) gives us the whole universe; the
    per-candidate kline batch is only for surviving stocks.

    Anti-chase gate (Fix A, 2026-05-08):
      max_5d_pct  absolute cap on the stock's own 5-day gain (default 10%).
                  D by design requires MA-aligned momentum confirmation
                  which IS a lagging signal; the 10% cap keeps the pick at
                  the START of a confirmed leg rather than mid-way through
                  a +15~20% run. Rows with pct_5d == None (degraded data
                  source) bypass this filter to stay lenient.
    """
    drops = {"negative_flow": 0, "low_flow_rank": 0, "st_risky": 0,
             "wrong_market": 0, "thin_liquidity": 0,
             "turnover_out_of_band": 0, "extreme_pct": 0,
             "ma_not_aligned": 0, "no_kline": 0, "overheated": 0}

    flow_rows = get_multiday_fund_flow()
    if not flow_rows:
        screen_strategy_d.last_stage1_drops = drops
        screen_strategy_d.last_pool_review = {"universe": 0}
        return []

    # Detect degradation: if the multiday flow source had to synthesize
    # from single-day inflow, the ranking key `main_inflow_pct_5d` is
    # None for every row. Fall back to ranking by absolute `main_inflow_1d`.
    degraded = bool(flow_rows and flow_rows[0].get("_degraded"))

    # Stage 1: inflow filter (cheap, no extra API)
    stage1 = []
    for r in flow_rows:
        code = r.get("code")
        if not code:
            continue
        if not _is_in_market(code, market):
            drops["wrong_market"] += 1
            continue
        if _is_risky_name(r.get("name")):
            drops["st_risky"] += 1
            continue
        in5 = r.get("main_inflow_5d") or 0
        if in5 <= min_total_inflow:
            drops["negative_flow"] += 1
            continue
        stage1.append(r)
    # Rank by flow pct (primary) or absolute 1d inflow (degraded fallback).
    if degraded:
        stage1.sort(key=lambda x: x.get("main_inflow_1d") or 0, reverse=True)
    else:
        stage1.sort(key=lambda x: x.get("main_inflow_pct_5d") or 0, reverse=True)
    cutoff = max(1, int(len(stage1) * flow_pct_rank_top))
    stage2_src = stage1[:cutoff]
    drops["low_flow_rank"] = max(0, len(stage1) - cutoff)

    # Stage 2: fetch market quotes for stage2 codes to get turnover / volume_ratio
    codes = [r["code"] for r in stage2_src]
    if not codes:
        screen_strategy_d.last_stage1_drops = drops
        screen_strategy_d.last_pool_review = {"universe": len(flow_rows)}
        return []
    quote_map = {}
    try:
        for q in get_market_quotes(codes):
            quote_map[q["code"]] = q
    except Exception as e:
        print(f"WARN: strategy D quote fetch failed: {e}", file=sys.stderr)

    # Stage 3: batch kline for MA alignment + position reference
    kl_map = get_daily_klines_batch(codes, n=65) if require_ma_alignment else {}

    out = []
    for r in stage2_src:
        code = r["code"]
        q = quote_map.get(code, {})
        if (q.get("amount") or 0) < min_amount:
            drops["thin_liquidity"] += 1
            continue
        turnover = q.get("turnover") or 0
        if turnover < turnover_min or turnover > turnover_max:
            drops["turnover_out_of_band"] += 1
            continue
        pct = r.get("pct") or 0
        if pct < pct_min or pct > pct_max:
            drops["extreme_pct"] += 1
            continue
        # Fix A: absolute 5-day gain cap. D's MA-alignment gate is already
        # a trailing signal; without this cap it routinely selects stocks
        # mid-way through a +15% leg. `pct_5d` comes from EM f109; Sina /
        # degraded tushare paths leave it None -- skip the filter in that
        # case to stay lenient on degraded data.
        pct_5d_raw = r.get("pct_5d")
        if pct_5d_raw is not None and pct_5d_raw > max_5d_pct:
            drops["overheated"] += 1
            continue
        ma20 = ma40 = ma60 = None
        aligned = None
        dist_ma20 = None
        if require_ma_alignment:
            kl = kl_map.get(code) or []
            if len(kl) < 20:
                drops["no_kline"] += 1
                continue
            closes = [k["close"] for k in kl]
            if len(closes) >= 20:
                ma20 = sum(closes[-20:]) / 20
            if len(closes) >= 40:
                ma40 = sum(closes[-40:]) / 40
            if len(closes) >= 60:
                ma60 = sum(closes[-60:]) / 60
            price = r.get("price") or 0
            # Lax alignment: close >= MA20*0.98 and MA20 >= MA40*0.98
            # (don't require strict >= at every level; moving averages lag)
            checks = []
            if ma20:
                checks.append(price >= ma20 * 0.98)
            if ma20 and ma40:
                checks.append(ma20 >= ma40 * 0.98)
            if ma40 and ma60:
                checks.append(ma40 >= ma60 * 0.98)
            aligned = all(checks) if checks else False
            if not aligned:
                drops["ma_not_aligned"] += 1
                continue
            if ma20 and ma20 > 0 and price > 0:
                dist_ma20 = round((price - ma20) / ma20 * 100, 2)
        out.append({
            "code": code,
            "name": r.get("name"),
            "price": r.get("price"),
            "pct": pct,
            "amount": q.get("amount"),
            "turnover": turnover,
            "volume_ratio": q.get("volume_ratio"),
            "float_mv": q.get("float_mv"),
            "industry": r.get("industry") or q.get("industry"),
            "main_inflow": q.get("main_inflow") or r.get("main_inflow_1d"),
            "main_inflow_5d": r.get("main_inflow_5d"),
            "main_inflow_pct_5d": r.get("main_inflow_pct_5d"),
            "main_inflow_10d": r.get("main_inflow_10d"),
            "main_inflow_pct_10d": r.get("main_inflow_pct_10d"),
            "pct_5d": r.get("pct_5d"),
            "pct_10d": r.get("pct_10d"),
            "ma20": round(ma20, 2) if ma20 else None,
            "ma40": round(ma40, 2) if ma40 else None,
            "ma60": round(ma60, 2) if ma60 else None,
            "ma_aligned": aligned,
            "distance_from_ma20": dist_ma20,
            "strategy": "D",
            "_source": q.get("_source", "em"),
        })
    screen_strategy_d.last_stage1_drops = drops
    screen_strategy_d.last_pool_review = {
        "universe": len(flow_rows),
        "after_flow_filter": len(stage1),
        "after_flow_rank": cutoff,
        "final": len(out),
        "degraded_single_day": degraded,    # True = 5d cumulative synthesized
    }
    return out


# ==========================================================================
# Strategy E -- 60-day box breakout.
#   Thesis: stocks that traded in a narrow range for months accumulate
#   hidden demand. A volume-confirmed breakout above the box top often
#   triggers a trend change with multi-week follow-through. Strategy E
#   targets the *pre-* and *just-* breakout state, not the chase.
#
#   Soft filters:
#     - 60-day high/low range < 25%
#     - Today's close >= box 90th percentile (near or at breakout)
#     - Volume ratio >= 1.8 (confirmation)
#     - Close > MA20 (momentum up-slope)
#     - 10-day cumulative main inflow > 0 (some accumulation)
#     - Not in limit-up / limit-down today (leave room)
# ==========================================================================

def screen_strategy_e(box_days=60, box_range_max_pct=25.0,
                      breakout_percentile=0.90, min_volume_ratio=1.8,
                      require_main_inflow_10d=True,
                      max_5d_pct=15.0,
                      market="all", min_amount=50_000_000,
                      max_universe=3000, sample=None):
    """Strategy E: 60-day narrow-box breakout.

    Args:
      sample: optional int -> only fetch klines for a random sample of
              `sample` codes (debug mode, avoids full-market hammer).

    Anti-chase gate (Fix A, 2026-05-08):
      max_5d_pct  absolute cap on 5-day gain (default 15%, more lenient
                  than C/D since a valid breakout by definition lifts the
                  close 5-10% off the box). Above 15% means the breakout
                  is already 2+ bars old -- the "just-breakout" window is
                  closed and entering now is chasing the follow-through.
    """
    drops = {"wrong_market": 0, "st_risky": 0, "thin_liquidity": 0,
             "no_kline": 0, "box_too_wide": 0, "not_near_top": 0,
             "weak_volume": 0, "below_ma20": 0, "no_inflow": 0,
             "limit_day": 0, "overheated": 0}

    # Universe: use cached full-market clist (5-min TTL). This already
    # holds price/volume/turnover/main_inflow/industry for every code.
    # Degradation: when the combined _FS_ALL_A clist is rate-limited
    # (happens most often mid-day), retry by splitting into the three
    # sub-fs (main / gem / star) in separate calls. Rate-limit often
    # only hits a single fs, so 1-of-3 success is already useful.
    universe = []
    universe_degraded_parts = []
    try:
        universe = get_market_list(fs=_FS_ALL_A)
    except Exception as e:
        print(f"WARN: strategy E _FS_ALL_A failed: {e}; "
              f"attempting per-market fallback", file=sys.stderr)
        for label, fs in (("main", _FS_MAIN),
                          ("gem", _FS_GEM),
                          ("star", _FS_STAR)):
            try:
                part = get_market_list(fs=fs)
                if part:
                    universe.extend(part)
                    universe_degraded_parts.append(label)
            except Exception as e2:
                print(f"WARN: strategy E sub-fs {label} failed: "
                      f"{type(e2).__name__}", file=sys.stderr)
        if not universe:
            print(f"WARN: strategy E universe fetch fully failed "
                  f"(all 3 sub-fs exhausted)", file=sys.stderr)
            screen_strategy_e.last_stage1_drops = drops
            screen_strategy_e.last_pool_review = {
                "universe": 0,
                "degraded_split_fetch": True,
            }
            return []
        print(f"INFO: strategy E universe degraded split fetch succeeded "
              f"({len(universe)} rows from {','.join(universe_degraded_parts)})",
              file=sys.stderr)

    # Stage 1: cheap filters (no kline yet)
    stage1 = []
    for r in universe:
        code = r.get("code")
        if not code:
            continue
        if not _is_in_market(code, market):
            drops["wrong_market"] += 1
            continue
        if _is_risky_name(r.get("name")):
            drops["st_risky"] += 1
            continue
        if (r.get("amount") or 0) < min_amount:
            drops["thin_liquidity"] += 1
            continue
        vr = r.get("volume_ratio") or 0
        if vr < min_volume_ratio:
            drops["weak_volume"] += 1
            continue
        pct = r.get("pct") or 0
        if abs(pct) >= 9.5:
            drops["limit_day"] += 1
            continue
        stage1.append(r)

    # Hard cap universe size to protect against runaway API usage
    if len(stage1) > max_universe:
        # Rank by volume_ratio desc: most likely breakouts get the budget
        stage1.sort(key=lambda x: x.get("volume_ratio") or 0, reverse=True)
        stage1 = stage1[:max_universe]

    if sample is not None and sample > 0 and len(stage1) > sample:
        import random
        stage1 = random.sample(stage1, sample)

    if not stage1:
        screen_strategy_e.last_stage1_drops = drops
        screen_strategy_e.last_pool_review = {
            "universe": len(universe),
            "degraded_split_fetch": bool(universe_degraded_parts),
        }
        return []

    # Stage 2: batch kline for box analysis (concurrent, cached)
    codes = [r["code"] for r in stage1]
    kl_map = get_daily_klines_batch(codes, n=box_days + 5, workers=8)

    out = []
    for r in stage1:
        code = r["code"]
        kl = kl_map.get(code) or []
        if len(kl) < box_days:
            drops["no_kline"] += 1
            continue
        box = kl[-box_days:]
        box_highs = [k["high"] for k in box]
        box_lows = [k["low"] for k in box]
        hi = max(box_highs)
        lo = min(box_lows)
        if lo <= 0:
            drops["no_kline"] += 1
            continue
        box_range_pct = (hi - lo) / lo * 100
        if box_range_pct > box_range_max_pct:
            drops["box_too_wide"] += 1
            continue
        # Where is today in the box?
        closes = sorted(k["close"] for k in box)
        p90_idx = int(len(closes) * breakout_percentile)
        p90_idx = min(max(p90_idx, 0), len(closes) - 1)
        p90 = closes[p90_idx]
        price = r.get("price") or kl[-1]["close"]
        if price < p90:
            drops["not_near_top"] += 1
            continue
        # MA20 slope check
        closes_all = [k["close"] for k in kl]
        ma20 = sum(closes_all[-20:]) / 20 if len(closes_all) >= 20 else None
        if ma20 and price < ma20:
            drops["below_ma20"] += 1
            continue
        # Fix A (2026-05-08): compute 5-day pct from the kline we already
        # have (no extra API call). kl[-1] is today, kl[-6] is 5 trading
        # days ago => (today_close - d5_close) / d5_close * 100.
        # Drop if the box has already been breached by more than max_5d_pct.
        pct_5d_e = None
        if len(closes_all) >= 6 and closes_all[-6] > 0:
            pct_5d_e = round(
                (closes_all[-1] - closes_all[-6]) / closes_all[-6] * 100, 2)
            if pct_5d_e > max_5d_pct:
                drops["overheated"] += 1
                continue
        if require_main_inflow_10d and (r.get("main_inflow") or 0) < 0:
            # Using today's inflow as a cheap proxy; multiday would need
            # an extra API call. If user sets require_main_inflow_10d=False
            # this check is bypassed.
            drops["no_inflow"] += 1
            continue
        box_position = (price - lo) / (hi - lo) * 100 if hi > lo else 100.0
        out.append({
            "code": code,
            "name": r.get("name"),
            "price": price,
            "pct": r.get("pct"),
            "amount": r.get("amount"),
            "turnover": r.get("turnover"),
            "volume_ratio": r.get("volume_ratio"),
            "float_mv": r.get("float_mv"),
            "industry": r.get("industry"),
            "main_inflow": r.get("main_inflow"),
            "box_days": box_days,
            "box_high": round(hi, 2),
            "box_low": round(lo, 2),
            "box_range_pct": round(box_range_pct, 2),
            "box_position_pct": round(box_position, 1),
            "ma20": round(ma20, 2) if ma20 else None,
            "distance_from_ma20": round((price - ma20) / ma20 * 100, 2) if ma20 else None,
            "pct_5d": pct_5d_e,                        # for chase-penalty scoring
            "strategy": "E",
            "_source": r.get("_source", "em"),
        })
    screen_strategy_e.last_stage1_drops = drops
    screen_strategy_e.last_pool_review = {
        "universe": len(universe),
        "stage1": len(stage1),
        "final": len(out),
        "degraded_split_fetch": bool(universe_degraded_parts),
    }
    # Sort by how close to breakout (higher box_position first)
    out.sort(key=lambda x: x.get("box_position_pct") or 0, reverse=True)
    return out


# ==========================================================================
# Strategy F1 -- Low-Vol Consolidation + First Breakout Day.
# ==========================================================================
#   Thesis: catch a stock on Day-1 of a new leg, NOT on Day-3/4 after the
#   leg has already started. Pattern: price has been quietly consolidating
#   for 10+ days (cumulative pct within +-3%) on shrinking volume; today
#   prints a moderate breakout candle (vol_ratio 1.2-2.5, pct +1..+4%,
#   close > MA20). The narrow band cap on today's pct is intentional --
#   limit-up days (+10%) are NOT F1; those are already chase territory.
# ==========================================================================

def screen_strategy_f1(min_amount=50_000_000,
                       max_10d_pct=3.0, min_10d_pct=-3.0,
                       max_60d_amplitude_pct=25.0,
                       today_pct_min=1.0, today_pct_max=4.0,
                       today_vr_min=1.2, today_vr_max=2.5,
                       require_above_ma20=True,
                       market="all", sample=None):
    """Strategy F1: low-vol consolidation + first breakout day.

    Returns candidate dicts (strategy='F1').
    """
    drops = {"wrong_market": 0, "st_risky": 0, "thin_liquidity": 0,
             "weak_pct_today": 0, "vol_out_of_band": 0,
             "no_kline": 0, "10d_not_consolidating": 0,
             "amplitude_too_wide": 0, "below_ma20": 0}

    universe = get_market_list()
    if not universe:
        screen_strategy_f1.last_stage1_drops = drops
        screen_strategy_f1.last_pool_review = {"universe": 0}
        return []

    # Stage 1: cheap filters using market quote fields directly.
    stage1 = []
    for r in universe:
        code = r.get("code")
        if not code or not _is_in_market(code, market):
            drops["wrong_market"] += 1
            continue
        if _is_risky_name(r.get("name")):
            drops["st_risky"] += 1
            continue
        amount = r.get("amount") or 0
        if amount < min_amount:
            drops["thin_liquidity"] += 1
            continue
        pct = r.get("pct")
        if pct is None or pct < today_pct_min or pct > today_pct_max:
            drops["weak_pct_today"] += 1
            continue
        vr = r.get("volume_ratio")
        if vr is None or vr < today_vr_min or vr > today_vr_max:
            drops["vol_out_of_band"] += 1
            continue
        stage1.append(r)

    if not stage1:
        screen_strategy_f1.last_stage1_drops = drops
        screen_strategy_f1.last_pool_review = {
            "universe": len(universe), "after_stage1": 0, "final": 0,
        }
        return []

    # Optional debug-only sampling (rate-limit safety on F1 first run).
    if sample and len(stage1) > sample:
        stage1 = stage1[:sample]

    # Stage 2: kline-based checks. F1 needs at least 25 days for the
    # consolidation window + MA20.
    codes = [r["code"] for r in stage1]
    kl_map = get_daily_klines_batch(codes, n=30, workers=8)

    out = []
    for r in stage1:
        code = r["code"]
        kl = kl_map.get(code) or []
        if len(kl) < 20:
            drops["no_kline"] += 1
            continue
        closes = [k["close"] for k in kl]
        highs = [k["high"] for k in kl]
        lows = [k["low"] for k in kl]
        # 10-day cumulative pct (today's close vs 10 days ago).
        # Note: kl[-1] is today, kl[-11] is 10 days ago.
        if len(closes) >= 11 and closes[-11] > 0:
            cum10 = (closes[-1] - closes[-11]) / closes[-11] * 100
        else:
            cum10 = None
        if cum10 is None or cum10 > max_10d_pct or cum10 < min_10d_pct:
            drops["10d_not_consolidating"] += 1
            continue
        # 60-day price amplitude: (max - min) / min * 100, capped to
        # screen out wide-swinging volatile names.
        wnd = closes[-60:] if len(closes) >= 60 else closes
        if wnd:
            lo, hi = min(wnd), max(wnd)
            amp = (hi - lo) / lo * 100 if lo > 0 else 0
            if amp > max_60d_amplitude_pct:
                drops["amplitude_too_wide"] += 1
                continue
        else:
            amp = None
        # MA20: today's close must be above MA20.
        ma20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else None
        if require_above_ma20:
            if ma20 is None or closes[-1] < ma20:
                drops["below_ma20"] += 1
                continue
        ma40 = sum(closes[-40:]) / 40 if len(closes) >= 40 else None
        ma60 = sum(closes[-60:]) / 60 if len(closes) >= 60 else None
        # 5-day pct from kline so evidence_card / pattern_match have it.
        # Without this F1 evidence cards always print "缺 5日涨幅数据"
        # because EM clist's f109 isn't merged into the F1 stage1 dict.
        if len(closes) >= 6 and closes[-6] > 0:
            cum5 = round((closes[-1] - closes[-6]) / closes[-6] * 100, 2)
        else:
            cum5 = None
        out.append({
            "code": code,
            "name": r.get("name"),
            "price": r.get("price") or closes[-1],
            "pct": r.get("pct"),
            "amount": r.get("amount"),
            "turnover": r.get("turnover"),
            "volume_ratio": r.get("volume_ratio"),
            "float_mv": r.get("float_mv"),
            "industry": r.get("industry"),
            "main_inflow": r.get("main_inflow"),
            "pct_5d": cum5,
            "pct_10d": round(cum10, 2),
            "amplitude_60d_pct": round(amp, 2) if amp is not None else None,
            "ma20": round(ma20, 2) if ma20 else None,
            "ma40": round(ma40, 2) if ma40 else None,
            "ma60": round(ma60, 2) if ma60 else None,
            "strategy": "F1",
            "_source": r.get("_source", "em"),
        })
    screen_strategy_f1.last_stage1_drops = drops
    screen_strategy_f1.last_pool_review = {
        "universe": len(universe),
        "after_stage1": len(stage1),
        "final": len(out),
    }
    # Sort by today's pct descending (stronger breakout candle first).
    out.sort(key=lambda x: x.get("pct") or 0, reverse=True)
    return out


# ==========================================================================
# Strategy F2 -- Silent Accumulation (anti-pattern of D).
# ==========================================================================
#   Thesis: D's classical signal (MA-aligned + strong main inflow + volume
#   confirm) catches stocks AFTER main capital has finished accumulating
#   and is mid-distribution. F2 catches main capital DURING accumulation:
#   money is quietly flowing in but the price hasn't lifted off yet. This
#   is the T-3~T-5 entry zone, before the run.
#
#   Hard filters (all required):
#     - 5-day cumulative main inflow > 20,000,000 (some money in, not huge)
#     - 5-day cumulative pct < 3% AND > -3% (price NOT lifted yet)
#     - Today's volume ratio in [0.8, 1.5] (NO breakout volume yet)
#     - Today's pct in [-2%, +3%] (NO chase candle)
#     - Price within MA20 +/- 5% (consolidation zone)
#     - NOT MA-aligned (intentional negative of D)
#     - Today's amount >= 50_000_000 (liquidity floor)
#     - 5-day inflow / float_mv ratio >= 0.5% (meaningful for the cap)
# ==========================================================================

def screen_strategy_f2(min_inflow_5d=10_000_000,
                       min_inflow_ratio_pct=0.3,
                       max_5d_pct=4.0, min_5d_pct=-4.0,
                       vol_ratio_lo=0.6, vol_ratio_hi=1.8,
                       pct_min=-3.0, pct_max=4.0,
                       ma20_band_pct=6.0,
                       require_ma_not_aligned=True,
                       market="all", min_amount=50_000_000):
    """Strategy F2: silent accumulation (anti-D).

    Aims to catch main capital BEFORE the price kicks off, not after. The
    classical D signal (MA-aligned + strong inflow + volume) is by
    construction a trailing signal -- it fires only AFTER 3-5 trading
    days of price advance, when retail starts noticing. F2 inverts every
    one of those dimensions: small but positive inflow, NO price kick,
    NO volume spike, NOT MA-aligned, sitting around MA20.

    Returns candidate dicts (strategy='F2').
    """
    drops = {"negative_flow": 0, "weak_flow": 0, "st_risky": 0,
             "wrong_market": 0, "thin_liquidity": 0,
             "already_running": 0, "vol_breakout": 0,
             "chase_candle": 0, "no_kline": 0,
             "out_of_ma20_band": 0, "already_aligned": 0,
             "low_inflow_ratio": 0}

    flow_rows = get_multiday_fund_flow()
    if not flow_rows:
        screen_strategy_f2.last_stage1_drops = drops
        screen_strategy_f2.last_pool_review = {"universe": 0}
        return []

    degraded = bool(flow_rows and flow_rows[0].get("_degraded"))
    # Stage 1: cheap filters (no extra API yet)
    stage1 = []
    for r in flow_rows:
        code = r.get("code")
        if not code:
            continue
        if not _is_in_market(code, market):
            drops["wrong_market"] += 1
            continue
        if _is_risky_name(r.get("name")):
            drops["st_risky"] += 1
            continue
        in5 = r.get("main_inflow_5d") or 0
        if in5 < min_inflow_5d:
            drops["weak_flow"] += 1
            continue
        # Price must NOT have lifted yet -- F2's key differentiator.
        # Using EM-native pct_5d (f109) when available; fall back to None
        # which lets the stock through to stage-2 kline computation.
        p5 = r.get("pct_5d")
        if p5 is not None and (p5 > max_5d_pct or p5 < min_5d_pct):
            drops["already_running"] += 1
            continue
        stage1.append(r)

    if not stage1:
        screen_strategy_f2.last_stage1_drops = drops
        screen_strategy_f2.last_pool_review = {
            "universe": len(flow_rows),
            "degraded_single_day": degraded,
        }
        return []

    # Stage 2: fetch live quote (for volume_ratio, turnover, amount) and
    # daily kline (for MA20 + actual 5d pct when EM f109 was unavailable).
    codes = [r["code"] for r in stage1]
    quote_map = {}
    try:
        for q in get_market_quotes(codes):
            quote_map[q["code"]] = q
    except Exception as e:
        print(f"WARN: strategy F2 quote fetch failed: {e}", file=sys.stderr)
    kl_map = get_daily_klines_batch(codes, n=25, workers=8)

    out = []
    for r in stage1:
        code = r["code"]
        q = quote_map.get(code, {})
        amount = q.get("amount") or 0
        if amount < min_amount:
            drops["thin_liquidity"] += 1
            continue
        # No volume kick -- F2 explicitly avoids the breakout-day pattern
        # because by the time vol_ratio > 1.5 main capital has already
        # tipped its hand and the meat is gone.
        vr = q.get("volume_ratio") or 0
        if vr < vol_ratio_lo or vr > vol_ratio_hi:
            drops["vol_breakout"] += 1
            continue
        # No chase candle today
        pct_today = q.get("pct") if q.get("pct") is not None else (r.get("pct") or 0)
        if pct_today < pct_min or pct_today > pct_max:
            drops["chase_candle"] += 1
            continue
        # Kline-derived checks: 5d pct (verify EM stage1 cut) + MA20 band
        # + MA-NOT-aligned (the deliberate negation of D's gate).
        kl = kl_map.get(code) or []
        if len(kl) < 20:
            drops["no_kline"] += 1
            continue
        closes = [k["close"] for k in kl]
        price = q.get("price") or kl[-1]["close"]
        # Recompute 5d pct from kline for stage1 rows that had p5==None.
        if r.get("pct_5d") is None and len(closes) >= 6 and closes[-6] > 0:
            kl_p5 = (closes[-1] - closes[-6]) / closes[-6] * 100
            if kl_p5 > max_5d_pct or kl_p5 < min_5d_pct:
                drops["already_running"] += 1
                continue
            r["pct_5d"] = round(kl_p5, 2)
        ma20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else None
        ma40 = sum(closes[-40:]) / 40 if len(closes) >= 40 else None
        ma60 = sum(closes[-60:]) / 60 if len(closes) >= 60 else None
        # MA20 band: price must be near MA20 (consolidation zone)
        if ma20 and ma20 > 0:
            dist_ma20 = (price - ma20) / ma20 * 100
            if abs(dist_ma20) > ma20_band_pct:
                drops["out_of_ma20_band"] += 1
                continue
        else:
            dist_ma20 = None
        # NOT MA-aligned: explicit negation of D. Strict bullish stack
        # (close > MA20 > MA40 > MA60) means main capital already finished
        # the prep work and is now in distribution.
        if require_ma_not_aligned and ma20 and ma40 and ma60:
            strict_aligned = (price > ma20 and ma20 > ma40 and ma40 > ma60)
            if strict_aligned:
                drops["already_aligned"] += 1
                continue
        # Inflow vs cap size: 50M into a 500B cap is a rounding error.
        # Require inflow/float_mv >= min_inflow_ratio_pct (default 0.5%).
        float_mv = q.get("float_mv") or r.get("float_mv") or 0
        if float_mv > 0:
            ratio_pct = (r.get("main_inflow_5d") or 0) / float_mv * 100
            if ratio_pct < min_inflow_ratio_pct:
                drops["low_inflow_ratio"] += 1
                continue
        else:
            ratio_pct = None
        out.append({
            "code": code,
            "name": r.get("name") or q.get("name"),
            "price": price,
            "pct": pct_today,
            "amount": amount,
            "turnover": q.get("turnover"),
            "volume_ratio": vr,
            "float_mv": float_mv if float_mv > 0 else None,
            "industry": r.get("industry") or q.get("industry"),
            "main_inflow": q.get("main_inflow") or r.get("main_inflow_1d"),
            "main_inflow_5d": r.get("main_inflow_5d"),
            "main_inflow_pct_5d": r.get("main_inflow_pct_5d"),
            "main_inflow_ratio_pct": (round(ratio_pct, 2)
                                      if ratio_pct is not None else None),
            "pct_5d": r.get("pct_5d"),
            "ma20": round(ma20, 2) if ma20 else None,
            "ma40": round(ma40, 2) if ma40 else None,
            "ma60": round(ma60, 2) if ma60 else None,
            "distance_from_ma20": round(dist_ma20, 2) if dist_ma20 is not None else None,
            "ma_aligned": False,                   # by construction
            "strategy": "F2",
            "_source": q.get("_source", "em"),
        })
    screen_strategy_f2.last_stage1_drops = drops
    screen_strategy_f2.last_pool_review = {
        "universe": len(flow_rows),
        "after_stage1": len(stage1),
        "final": len(out),
        "degraded_single_day": degraded,
    }
    # Sort by inflow ratio (most concentrated accumulation first).
    out.sort(key=lambda x: x.get("main_inflow_ratio_pct") or 0, reverse=True)
    return out


# ==========================================================================
# Strategy F3 -- Sector Kickoff (a sector turning hot TODAY for the
# first time in the past 5 days; pick its yet-to-move members).
# ==========================================================================
#   Thesis: by the time a sector has been in the top 10 by 5-day
#   performance, the obvious leaders have already run +20-40% and the
#   laggard rotation chase is over. F3 looks for a sector that is HOT
#   today (top 5 by 1-day pct) but was COLD over the past 5 days
#   (NOT in top 10 by 5-day pct). That is "first day of new rotation",
#   when capital is just starting to move in. The picks are MEMBERS of
#   that sector that themselves haven't moved yet (own 5d pct < 3%).
# ==========================================================================

def screen_strategy_f3(today_sector_top=5,
                       sector_5d_excluded_top=10,
                       require_leaders=2,
                       leader_pct_threshold=5.0,
                       member_5d_max=3.0,
                       member_today_min=-1.0,
                       member_today_max=4.0,
                       min_amount=30_000_000,
                       market="all"):
    """Strategy F3: sector kickoff. Returns candidate dicts (strategy='F3').

    Universe is constrained to members of "new-hot" sectors only. Note
    that 5-day sector pct is provided directly by EM sector_rank as
    `pct_5d`; if that field is missing (tushare aggregation fallback),
    F3 degrades to "today's top sectors that have today_pct >= 3%".
    """
    drops = {"no_new_hot_sector": 0, "no_leaders": 0,
             "wrong_market": 0, "st_risky": 0, "thin_liquidity": 0,
             "member_already_running": 0, "weak_pct_today": 0,
             "no_member_data": 0}

    today_sectors = get_sector_rank("industry", top=20, fail_safe=True)
    if not today_sectors:
        screen_strategy_f3.last_stage1_drops = drops
        screen_strategy_f3.last_pool_review = {"sectors": 0}
        return []

    # Sort today by `pct` descending (today's 1-day move) and by `pct_5d`
    # descending (past 5-day move). Then form the "new hot" set.
    by_today = sorted(today_sectors,
                      key=lambda s: s.get("pct") or 0, reverse=True)
    today_top = by_today[:today_sector_top]
    # When pct_5d is missing (tushare degrade), `cold_5d_set` falls back
    # to "all sectors except today's top 5 themselves" so F3 can still
    # pick something instead of returning empty.
    has_5d = any(s.get("pct_5d") is not None for s in today_sectors)
    if has_5d:
        by_5d = sorted([s for s in today_sectors
                        if s.get("pct_5d") is not None],
                       key=lambda s: s.get("pct_5d") or 0, reverse=True)
        hot_5d_names = {s["name"] for s in by_5d[:sector_5d_excluded_top]
                        if s.get("name")}
    else:
        hot_5d_names = set()                        # degrade: skip 5d cut

    new_hot = [s for s in today_top
               if s.get("name") and s["name"] not in hot_5d_names]
    if not new_hot:
        drops["no_new_hot_sector"] += 1
        screen_strategy_f3.last_stage1_drops = drops
        screen_strategy_f3.last_pool_review = {
            "sectors": len(today_sectors),
            "today_top": len(today_top),
            "new_hot": 0,
        }
        return []

    # For each new-hot sector, pull constituents and pick non-running
    # members. Skip sectors lacking >=N leaders today (avoids selecting
    # a "noise" sector with one freak +5% gainer).
    sector_picks = []
    for sec in new_hot:
        sec_code = sec.get("code")
        members = get_sector_constituents(sec_code) or []
        if not members:
            drops["no_member_data"] += 1
            continue
        # Count today leaders in this sector
        leaders = [m for m in members
                   if (m.get("pct") or 0) >= leader_pct_threshold]
        if len(leaders) < require_leaders:
            drops["no_leaders"] += 1
            continue
        for m in members:
            code = m.get("code")
            if not code or not _is_in_market(code, market):
                drops["wrong_market"] += 1
                continue
            if _is_risky_name(m.get("name")):
                drops["st_risky"] += 1
                continue
            amount = m.get("amount") or 0
            if amount < min_amount:
                drops["thin_liquidity"] += 1
                continue
            pct_today = m.get("pct")
            if (pct_today is None or pct_today < member_today_min
                    or pct_today > member_today_max):
                drops["weak_pct_today"] += 1
                continue
            # Sector-member 5d pct check requires kline; defer to stage 2.
            sector_picks.append((sec, m))

    if not sector_picks:
        screen_strategy_f3.last_stage1_drops = drops
        screen_strategy_f3.last_pool_review = {
            "sectors": len(today_sectors),
            "new_hot": len(new_hot),
            "after_member_filter": 0,
        }
        return []

    # Stage 2: kline-based 5d pct. Only fetch for unique codes.
    unique_codes = list({m["code"] for _, m in sector_picks})
    kl_map = get_daily_klines_batch(unique_codes, n=15, workers=8)

    out = []
    seen = set()
    for sec, m in sector_picks:
        code = m["code"]
        if code in seen:
            continue
        kl = kl_map.get(code) or []
        if len(kl) >= 6 and kl[-6]["close"] > 0:
            mp5 = (kl[-1]["close"] - kl[-6]["close"]) / kl[-6]["close"] * 100
        else:
            mp5 = None
        if mp5 is not None and mp5 > member_5d_max:
            drops["member_already_running"] += 1
            continue
        seen.add(code)
        out.append({
            "code": code,
            "name": m.get("name"),
            "price": m.get("price"),
            "pct": m.get("pct"),
            "amount": m.get("amount"),
            "turnover": m.get("turnover"),
            "volume_ratio": m.get("volume_ratio"),
            "float_mv": m.get("float_mv"),
            "industry": m.get("industry") or sec.get("name"),
            "main_inflow": m.get("main_inflow"),
            "pct_5d": round(mp5, 2) if mp5 is not None else None,
            "sector_name": sec.get("name"),
            "sector_pct_today": sec.get("pct"),
            "sector_pct_5d": sec.get("pct_5d"),
            "sector_leaders": len([
                x for x in get_sector_constituents(sec.get("code")) or []
                if (x.get("pct") or 0) >= leader_pct_threshold
            ]),
            "strategy": "F3",
            "_source": m.get("_source", "em"),
        })
    screen_strategy_f3.last_stage1_drops = drops
    screen_strategy_f3.last_pool_review = {
        "sectors": len(today_sectors),
        "new_hot": len(new_hot),
        "new_hot_names": [s.get("name") for s in new_hot],
        "after_member_filter": len(sector_picks),
        "final": len(out),
        "degraded_no_5d": not has_5d,
    }
    out.sort(key=lambda x: x.get("sector_pct_today") or 0, reverse=True)
    return out


# ==========================================================================
# Unified scoring model (strategies C/D/E).
#
# Design rationale: the common thread across C/D/E is that the LLM should
# compare candidates from different strategies on the same 0-100 scale.
# The old model (_score_strategy_a/b) used strategy-specific dimensions
# that were not directly comparable, which forced the LLM to learn two
# scoring semantics. The unified model uses five universal dimensions
# scored out of 100 total; each strategy contributes a strategy_bonus
# reflecting its own thesis signal:
#
#   [Position]          0-15  (ma20 band, multi-day trend, box position)
#   [Capital]           0-25  (main-inflow 5d / 10d cumulative)
#   [Volume]            0-10  (volume_ratio 1.2~3 healthy, extremes bad)
#   [Sector]            0-15  (industry in top-5 hot sectors or relative rank)
#   [Quality]           0-10  (float_mv sweet spot + turnover band)
#   [Strategy-specific] 0-25  (C: laggard gap; D: flow rank; E: box tightness)
# ==========================================================================

def _unified_score(c, hot_sectors=None, market_ctx=None, sector_pct_map=None):
    """Unified 0-100 scoring for strategies C/D/E. Writes breakdown into
    the candidate dict for downstream transparency.
    """
    hot = set(hot_sectors or [])
    strat = c.get("strategy", "?")
    score_pos = 0.0
    score_cap = 0.0
    score_vol = 0.0
    score_sec = 0.0
    score_qlt = 0.0
    score_st = 0.0

    # (1) Position -- penalize overextension, reward healthy pullback.
    dist_ma20 = c.get("distance_from_ma20")
    if dist_ma20 is not None:
        if -3 <= dist_ma20 <= 3:
            score_pos += 10                              # sitting on MA20
        elif -5 <= dist_ma20 <= 5:
            score_pos += 7
        elif -7 <= dist_ma20 <= 10:
            score_pos += 3
        # Extremes (<-7 broken, >10 over-extended) gets 0
    if c.get("ma_aligned") is True:
        score_pos += 5                                   # multi-timeframe bullish
    bp = c.get("box_position_pct")
    if bp is not None:
        if 85 <= bp <= 100:
            score_pos += 5                               # near breakout top
        elif 70 <= bp < 85:
            score_pos += 2

    # (2) Capital -- reward sustained inflow, more weight the longer.
    mi5 = c.get("main_inflow_5d") or 0
    if mi5 > 500_000_000:
        score_cap += 15
    elif mi5 > 100_000_000:
        score_cap += 10
    elif mi5 > 0:
        score_cap += 5
    mi10 = c.get("main_inflow_10d") or 0
    if mi10 > 1_000_000_000:
        score_cap += 10
    elif mi10 > 200_000_000:
        score_cap += 6
    elif mi10 > 0:
        score_cap += 3
    mi1 = c.get("main_inflow") or 0
    if mi1 > 50_000_000 and score_cap < 20:
        score_cap += 5                                   # strong today tops up
    if mi1 < -50_000_000:
        score_cap -= 10                                  # today dumping

    # (3) Volume -- healthy expansion vs abnormal spike
    vr = c.get("volume_ratio") or 0
    if 1.2 <= vr <= 2.5:
        score_vol += 10
    elif 2.5 < vr <= 3.5:
        score_vol += 7
    elif 0.8 <= vr < 1.2:
        score_vol += 3
    elif vr > 5:
        score_vol -= 5                                   # panic volume / distribution

    # (4) Sector -- in hot set or relative rank
    ind = (c.get("industry") or "").strip()
    if ind and ind in hot:
        score_sec += 15
    elif ind:
        score_sec += 5                                   # baseline
    # Sector outperformance bonus (if sector_pct_map includes this industry)
    if sector_pct_map and ind:
        sp = sector_pct_map.get(ind)
        worst = None
        if market_ctx:
            probes = [p for p in (market_ctx.get("sh_pct"),
                                  market_ctx.get("gem_pct")) if p is not None]
            if probes:
                worst = min(probes)
        if sp is not None and worst is not None:
            if sp - worst >= 3.0:
                score_sec = min(15, score_sec + 3)       # sector resilient

    # (5) Quality -- float mv sweet spot, turnover band
    fmv = c.get("float_mv") or 0
    yi = fmv / 1e8
    if 50 <= yi <= 300:
        score_qlt += 6
    elif 20 <= yi < 50 or 300 < yi <= 600:
        score_qlt += 3
    to = c.get("turnover") or 0
    if 2 <= to <= 8:
        score_qlt += 4
    elif 1 <= to < 2 or 8 < to <= 15:
        score_qlt += 2

    # (6) Strategy-specific bonus (max 25)
    if strat == "C":
        gap = c.get("laggard_gap") or 0                  # sector up - stock up
        if gap >= 8:
            score_st += 20
        elif gap >= 4:
            score_st += 12
        elif gap >= 1:
            score_st += 5
        # Sector own strength
        sndp = c.get("sector_n_day_pct") or 0
        if sndp >= 10:
            score_st += 5
        elif sndp >= 5:
            score_st += 3
    elif strat == "D":
        mp5 = c.get("main_inflow_pct_5d") or 0           # pct of cum volume
        if mp5 >= 15:
            score_st += 15
        elif mp5 >= 8:
            score_st += 10
        elif mp5 >= 3:
            score_st += 5
        mp10 = c.get("main_inflow_pct_10d") or 0
        if mp10 >= 8:
            score_st += 5
        elif mp10 >= 3:
            score_st += 3
        # Price-action consistency with accumulation
        p5 = c.get("pct_5d") or 0
        if 2 <= p5 <= 12:
            score_st += 5                                # moderate follow-through
        elif p5 > 20:
            score_st -= 5                                # already ran too far
    elif strat == "E":
        br = c.get("box_range_pct") or 100
        if br <= 12:
            score_st += 15                               # tightest box = best spring
        elif br <= 18:
            score_st += 10
        elif br <= 22:
            score_st += 5
        bp = c.get("box_position_pct") or 0
        if bp >= 95:
            score_st += 10                               # at the very top, decisive
        elif bp >= 90:
            score_st += 5

    # Fix D (2026-05-08): chase-penalty. Subtract points based on the
    # stock's own 5-day gain so candidates already deep into a leg rank
    # BELOW genuine catch-up / early-stage candidates with identical
    # position/capital/volume/sector profiles. Formula:
    #   penalty = max(0, (pct_5d - 3) * 0.5), capped at 8 points.
    # Rationale: first 3% gain is free (normal volatility); each additional
    # percent costs 0.5 points up to an 8-point ceiling so the penalty
    # never dominates the full 100-point scale.
    # Source field differs by strategy:
    #   C uses `stock_n_day_pct` (already populated in Stage-2)
    #   D uses `pct_5d` from EM f109 clist
    #   E uses `pct_5d` we now compute in Stage-2 (2026-05-08 change)
    _chase_pct = (c.get("pct_5d")
                  if c.get("pct_5d") is not None
                  else c.get("stock_n_day_pct"))
    score_chase = 0.0
    if _chase_pct is not None and _chase_pct > 3.0:
        score_chase = min(8.0, (_chase_pct - 3.0) * 0.5)

    total = (score_pos + score_cap + score_vol + score_sec + score_qlt + score_st
             - score_chase)
    total = max(0.0, min(100.0, total))
    c["score_pos"] = round(score_pos, 1)
    c["score_cap"] = round(score_cap, 1)
    c["score_vol"] = round(score_vol, 1)
    c["score_sec"] = round(score_sec, 1)
    c["score_qlt"] = round(score_qlt, 1)
    c["score_st"] = round(score_st, 1)
    c["score_chase_penalty"] = round(score_chase, 1)   # transparent on output
    return total


# ==========================================================================
# Scoring (0-100 composite)
# ==========================================================================

def score_candidates(cands, hot_sectors=None,
                     market_ctx=None, sector_pct_map=None):
    """Score C/D/E candidates on a 0-100 scale (unified weighted model).

    Dimensions (see `_unified_score`):
      Position / Capital / Volume / Sector / Quality / Strategy-specific

    Macro-context delta adds on top (market_delta / sector_rel_delta /
    flow_x_macro_delta); kept as separate fields for output-table
    transparency and LLM decision surface.

    Strategies A (first-board divergence) and B (oversold bounce) have
    been retired 2026-04-22 per user directive -- they are gambling-chain
    plays (second-hand premium) with near-zero real EV. C/D/E target
    sector-rotation / capital-accumulation / box-breakout which have
    multi-day information flow and genuine positive expectancy.
    """
    for c in cands:
        s = _unified_score(c, hot_sectors=hot_sectors,
                           market_ctx=market_ctx,
                           sector_pct_map=sector_pct_map)
        s += _market_context_delta(c, market_ctx, sector_pct_map)
        c["score"] = round(min(max(s, 0), 100), 1)
    return sorted(cands, key=lambda x: x["score"], reverse=True)


def _market_context_delta(c, market_ctx, sector_pct_map):
    """Market-context score modifier for strategies C/D/E.

    All three strategies are long-biased and benefit from a rising broad
    market (unlike old A/B which had asymmetric sensitivity). So the
    market-trend factor is symmetric across C/D/E. Three additive parts:

      1. broad market trend    : rising = tailwind, crash = risk-off
      2. sector vs broad market: sector leading = higher conviction
      3. fund-flow x macro     : defensive inflow on down days = stealth

    Returns total delta (roughly bounded to [-10, +10]) so the 0-100
    unified base score still dominates ranking. Also writes
    c["market_delta"] / c["sector_rel_delta"] / c["flow_x_macro_delta"]
    for output-table transparency.
    """
    c["market_delta"] = 0
    c["sector_rel_delta"] = 0
    c["flow_x_macro_delta"] = 0
    if not market_ctx:
        return 0.0

    sh_pct = market_ctx.get("sh_pct")
    gem_pct = market_ctx.get("gem_pct")
    probes = [p for p in (sh_pct, gem_pct) if p is not None]
    if not probes:
        return 0.0
    worst = min(probes)
    avg = sum(probes) / len(probes)

    # (1) Broad-market trend (symmetric: all three are long-biased)
    if avg >= 1.0:
        market_delta = 5
    elif avg >= 0.3:
        market_delta = 3
    elif avg >= -0.3:
        market_delta = 0
    elif avg >= -1.0:
        market_delta = -3
    elif avg >= -2.0:
        market_delta = -6
    else:
        market_delta = -10                                  # crash day, risk-off

    # (2) Sector vs broad market relative strength
    sector_rel_delta = 0
    if sector_pct_map:
        ind = (c.get("industry") or "").strip()
        if ind:
            sp = sector_pct_map.get(ind)
            if sp is not None:
                rel = sp - avg
                if rel >= 3.0:
                    sector_rel_delta = 5
                elif rel >= 1.5:
                    sector_rel_delta = 3
                elif rel <= -2.0:
                    sector_rel_delta = -3

    # (3) Fund-flow x macro interaction
    flow_x_macro_delta = 0
    mi = c.get("main_inflow") or 0
    if worst < -0.5 and mi > 50_000_000:
        flow_x_macro_delta = 3                              # defensive accumulation
    elif worst > 0.5 and mi < -50_000_000:
        flow_x_macro_delta = -3                             # distribution despite tailwind

    c["market_delta"] = market_delta
    c["sector_rel_delta"] = sector_rel_delta
    c["flow_x_macro_delta"] = flow_x_macro_delta
    return float(market_delta + sector_rel_delta + flow_x_macro_delta)


# ==========================================================================
# Layer 4: LLM hints (rule-based reject / warn / boost / next-day probability).
#
# Design goal: Python emits deterministic tags so the LLM only handles the
# narrow semantic layer (news cross-check, narrative decision). Strategies
# C/D/E each have their own reject/boost patterns but share universal
# over-extension and panic-volume hard rejects.
# ==========================================================================

def _apply_llm_hints(results, market_ctx, top5_sectors, meta,
                     bad_news_map=None):
    """Annotate each C/D/E candidate with reject/warn/boost tags and
    a next_day_prob bucket (high/mid/low).

    Universal hard rejects:
      - distance_from_ma20 > 12      (over-extended, mean-reversion risk)
      - volume_ratio > 5             (panic / distribution suspected)
      - main_inflow < -100M today    (big outflow, smart money exiting)

    Strategy-specific rejects:
      C: sector_n_day_pct < broad_avg + 1  -> sector_cooling (warn)
      D: pct_5d > 20                       -> late_entry (reject)
         main_inflow_pct_5d < 2            -> weak_accumulation (warn)
      E: price < box_high * 0.95           -> below_box_top (warn)

    Boosts (strategy-specific):
      C: laggard_gap >= 5 and sector_n_day_pct >= 5
      D: main_inflow_pct_5d >= 15 and main_inflow_pct_10d >= 8
      E: box_range_pct <= 15 and box_position_pct >= 90 and volume_ratio >= 2

    Universal boosts:
      - industry in top5_sectors                (hot sector)
      - distance_from_ma20 between -3 and +3    (healthy MA20 support)

    next_day_prob:
      low  : any reject OR distance_from_ma20>10 OR volume_ratio>5
      high : >=2 boosts, OR >=1 boost with no warnings
      mid  : default
    """
    sh_pct = (market_ctx or {}).get("sh_pct")
    gem_pct = (market_ctx or {}).get("gem_pct")
    probes = [p for p in (sh_pct, gem_pct) if p is not None]
    broad_avg = sum(probes) / len(probes) if probes else 0.0
    top5 = set(top5_sectors or [])

    for c in results:
        strat = c.get("strategy", "?")
        reject = []
        warn = []
        boost = []

        # ---------- UNIVERSAL hard rejects ----------
        dist = c.get("distance_from_ma20")
        if dist is not None and dist > 12:
            reject.append("over_extended")
        vr = c.get("volume_ratio") or 0
        if vr > 5:
            reject.append("panic_volume")
        mi = c.get("main_inflow") or 0
        if mi < -100_000_000:
            reject.append("big_outflow_today")

        # ---------- STRATEGY-specific checks ----------
        if strat == "C":
            sndp = c.get("sector_n_day_pct") or 0
            if sndp < broad_avg + 1.0:
                warn.append("sector_cooling")
            gap = c.get("laggard_gap") or 0
            if gap >= 5 and sndp >= 5:
                boost.append("laggard_in_hot_sector")
        elif strat == "D":
            p5 = c.get("pct_5d") or 0
            if p5 > 20:
                reject.append("late_entry")                # already ran, no room
            mp5 = c.get("main_inflow_pct_5d") or 0
            mp10 = c.get("main_inflow_pct_10d") or 0
            if mp5 < 2:
                warn.append("weak_accumulation")
            if mp5 >= 15 and mp10 >= 8:
                boost.append("sustained_accumulation")
        elif strat == "E":
            bh = c.get("box_high") or 0
            price = c.get("price") or 0
            if bh > 0 and price < bh * 0.95:
                warn.append("below_box_top")
            br = c.get("box_range_pct") or 100
            bp = c.get("box_position_pct") or 0
            if br <= 15 and bp >= 90 and vr >= 2:
                boost.append("tight_box_breakout")

        # ---------- SOFT warn: news ----------
        if bad_news_map is not None:
            hit = bad_news_map.get(c.get("code"))
            if hit:
                warn.append(f"bad_news:{hit[:30]}")

        # ---------- SOFT warn: sector rotation ----------
        industry = (c.get("industry") or "").strip()
        if industry and industry not in top5 and strat != "E":
            warn.append("sector_not_top5")

        # ---------- UNIVERSAL boosts ----------
        if industry in top5:
            boost.append("hot_sector")
        if dist is not None and -3 <= dist <= 3:
            boost.append("at_ma20_support")
        if c.get("ma_aligned") is True:
            boost.append("ma_bullish_alignment")

        # ---------- NEXT-DAY PROBABILITY BUCKET ----------
        # Ordering matters: hard rejects immediately force `low`.
        if reject:
            prob = "low"
        elif dist is not None and dist > 10:
            prob = "low"
        elif vr > 5:
            prob = "low"
        elif len(boost) >= 2:
            prob = "high"
        elif len(boost) >= 1 and not warn:
            prob = "high"
        else:
            prob = "mid"

        c["reject_reasons"] = reject
        c["soft_warnings"] = warn
        c["boost_reasons"] = boost
        c["next_day_prob"] = prob

    # Aggregate advisory: how many of Top10 are hard-rejected
    top10 = results[:10]
    reject_in_top10 = sum(1 for c in top10 if c.get("reject_reasons"))
    meta["reject_count_top10"] = reject_in_top10
    meta["advisory_avoid"] = reject_in_top10 >= 6
    meta["market_ctx"] = {"sh_pct": sh_pct, "gem_pct": gem_pct}
    meta["top5_sectors"] = sorted(top5)


def _scan_bad_news_for_final(results, days=7, strategies=("C", "D", "E")):
    """Scan announcement bad-news titles for final candidates.

    Strategies C/D/E all hold overnight so announcement risk applies
    uniformly. Returns {code: matched_title}. Fail-safe: any error
    returns empty dict (cache layer handles transient flakiness).
    """
    result = {}
    codes = [c.get("code") for c in results
             if c.get("strategy") in strategies and c.get("code")]
    for code in codes:
        try:
            bad, hit = has_bad_news(code, days=days)
            if bad and hit:
                result[code] = hit
        except Exception as e:
            # Silently skip per-code failure; announcement API is flaky.
            print(f"WARN: bad-news scan failed for {code}: {type(e).__name__}", file=sys.stderr)
    return result


# ==========================================================================
# Pattern matcher + Evidence card + Confidence voting.
#
# The LLM historically got a flat candidate dict and had to guess whether
# the data support or contradict a "buy" decision. Two failure modes
# observed in real trades:
#   1. The LLM pattern-matched naively ("F2 hit, main capital in, BUY")
#      and missed bearish co-signals in the same data (upper shadow,
#      distance from 60-day high, overheated cluster).
#   2. The LLM ignored that two strategies with conflicting signals
#      actually reduces confidence, not increases it (e.g. F2 says
#      "still quiet", F1 says "already breaking out" -- these aren't
#      both right; something is staler than the other).
#
# The three helpers below address both. They are intentionally string-
# based (not scores) so the LLM can read them in plain language:
#   - _match_patterns(c, kl) -> list of pattern label strings
#   - _build_evidence_card(c, kl, market_ctx) -> dict of bullish/
#       bearish/uncertain signal lists
#   - _vote_confidence(candidates_by_code) -> per-code confidence label
#       based on cross-strategy agreement
# ==========================================================================

# Pattern labels (closed set; LLM trained to interpret these strings):
#   bottom_first_rally  : 60d pullback >=15%, recent consolidation, today
#                         moderate up candle with above-avg volume
#   gravestone_after_run: 5d pct >=5%, today long upper shadow, close
#                         flat/down -- distribution warning
#   low_vol_consolidation: 10d pct in +-3%, 10d avg volume < 30d avg volume
#   distribution_top    : 5d pct >=10%, today vol_ratio >=2, pct <2%
#                         (heavy volume without price follow-through)
#   breakout_initial    : 10d pct in +-3% consolidation, today pct 1-4%
#                         with vol_ratio 1.2-2.5 (F1 archetype)
#   silent_accumulation : 5d pct in +-3%, main_inflow_5d positive and
#                         >=0.3% of float MV, not MA-aligned (F2 archetype)
#   sector_initial_move : own 5d pct small AND sector today_rank in top5
#                         AND sector 5d_rank outside top10 (F3 archetype)
#   overheated_chase    : 5d pct >=10%, close within 5% of 60d high,
#                         today pct >=3%
_PATTERN_LABELS = (
    "bottom_first_rally",
    "gravestone_after_run",
    "low_vol_consolidation",
    "distribution_top",
    "breakout_initial",
    "silent_accumulation",
    "sector_initial_move",
    "overheated_chase",
)


def _match_patterns(c, kl=None):
    """Return list of pattern labels that fit candidate `c`.

    `c` is an enriched candidate dict (has pct, pct_5d, volume_ratio,
    close, ma20, etc.). `kl` is an optional list of daily kline rows
    (at least 60 days recommended for full pattern coverage).
    """
    out = []
    pct = c.get("pct") or 0
    p5 = c.get("pct_5d")
    vr = c.get("volume_ratio") or 0
    ma20 = c.get("ma20")
    ma40 = c.get("ma40")
    ma60 = c.get("ma60")
    price = c.get("price") or 0
    closes = [k["close"] for k in kl] if kl else []
    highs = [k["high"] for k in kl] if kl else []
    lows = [k["low"] for k in kl] if kl else []
    opens = [k["open"] for k in kl] if kl else []
    vols = [k.get("volume") or 0 for k in kl] if kl else []

    # Distance to 60-day high / low
    dist_high = dist_low = None
    if closes:
        wnd = closes[-60:] if len(closes) >= 60 else closes
        hi60 = max(wnd)
        lo60 = min(wnd)
        if hi60 > 0:
            dist_high = (hi60 - price) / hi60 * 100   # positive = below high
        if lo60 > 0:
            dist_low = (price - lo60) / lo60 * 100    # positive = above low

    # 1. bottom_first_rally: deep pullback from 60d high + today's up candle
    if (dist_high is not None and dist_high >= 15
            and p5 is not None and -3 <= p5 <= 3
            and 1 <= pct <= 6 and vr >= 1.2):
        out.append("bottom_first_rally")

    # 2. gravestone_after_run: runup + today's upper-shadow reversal
    if p5 is not None and p5 >= 5 and kl:
        t = kl[-1]
        body = abs(t["close"] - t["open"])
        upper = t["high"] - max(t["close"], t["open"])
        rng = t["high"] - t["low"]
        if rng > 0 and upper >= 2 * body and upper / rng >= 0.5 and pct <= 2:
            out.append("gravestone_after_run")

    # 3. low_vol_consolidation: 10d flat + recent volume below 30d avg
    if (p5 is not None and -3 <= p5 <= 3 and len(vols) >= 30):
        recent_avg = sum(vols[-10:]) / 10
        base_avg = sum(vols[-30:]) / 30
        if base_avg > 0 and recent_avg / base_avg < 0.8:
            out.append("low_vol_consolidation")

    # 4. distribution_top: high vr but price not following
    if (p5 is not None and p5 >= 10 and vr >= 2.0 and pct < 2):
        out.append("distribution_top")

    # 5. breakout_initial (F1 archetype)
    p10 = c.get("pct_10d")
    if (p10 is not None and -3 <= p10 <= 3
            and 1 <= pct <= 4 and 1.2 <= vr <= 2.5
            and ma20 is not None and price >= ma20):
        out.append("breakout_initial")

    # 6. silent_accumulation (F2 archetype)
    inflow_ratio = c.get("main_inflow_ratio_pct")
    if (p5 is not None and -3 <= p5 <= 3
            and inflow_ratio is not None and inflow_ratio >= 0.3
            and not c.get("ma_aligned", False)):
        out.append("silent_accumulation")

    # 7. sector_initial_move (F3 archetype)
    if (c.get("sector_pct_today") is not None
            and c.get("sector_pct_today") >= 3
            and (c.get("sector_pct_5d") is None
                 or c.get("sector_pct_5d") < 3)
            and p5 is not None and p5 < 5):
        out.append("sector_initial_move")

    # 8. overheated_chase
    if (p5 is not None and p5 >= 10
            and dist_high is not None and dist_high <= 5
            and pct >= 3):
        out.append("overheated_chase")

    return out


def _build_evidence_card(c, kl=None, market_ctx=None, hot_sectors=None):
    """Return an evidence card dict with bullish/bearish/uncertain signals.

    Each signal is a short Chinese string (human-readable to LLM), along
    with the numeric value that triggered it so the LLM can quote it
    back to the user.
    """
    bullish = []
    bearish = []
    uncertain = []

    pct = c.get("pct")
    p5 = c.get("pct_5d")
    vr = c.get("volume_ratio")
    price = c.get("price")
    ma20 = c.get("ma20")
    ma40 = c.get("ma40")
    ma60 = c.get("ma60")
    inflow = c.get("main_inflow")
    inflow_5d = c.get("main_inflow_5d")
    inflow_ratio = c.get("main_inflow_ratio_pct")
    industry = c.get("industry")
    sector_name = c.get("sector_name") or industry

    # --- bullish signals ---
    if inflow_ratio is not None and inflow_ratio >= 0.5:
        bullish.append(f"主力5日净流入占流通市值 {inflow_ratio}% (≥0.5% 显著)")
    if inflow is not None and inflow > 50_000_000:
        bullish.append(f"今日主力净流入 {inflow/1e8:.2f} 亿 (≥5千万)")
    if p5 is not None and -3 <= p5 <= 3 and inflow_5d is not None and inflow_5d > 0:
        bullish.append(f"5日横盘 {p5}% + 资金净流入 {inflow_5d/1e8:.2f} 亿 = 吸筹形态")
    if ma20 is not None and price is not None and 0 < (price - ma20) / ma20 * 100 <= 3:
        bullish.append(f"刚站上MA20 (距MA20 +{(price-ma20)/ma20*100:.2f}%)")
    if c.get("sector_pct_today") is not None and c["sector_pct_today"] >= 3:
        bullish.append(f"所属板块「{sector_name}」今日 +{c['sector_pct_today']:.1f}% 领涨")
    if hot_sectors and industry and industry in hot_sectors:
        bullish.append(f"所属行业「{industry}」位于今日热门板块")
    # MA multi-head (ma20>ma40>ma60) but NOT for F2 (F2 requires NOT aligned)
    if (c.get("strategy") != "F2" and ma20 and ma40 and ma60
            and ma20 > ma40 > ma60):
        bullish.append("MA20>MA40>MA60 均线多头排列")

    # --- bearish signals ---
    if p5 is not None and p5 >= 10:
        bearish.append(f"5日已涨 {p5}% (>10% 上方套牢盘沉重)")
    if pct is not None and pct >= 7:
        bearish.append(f"今日已涨 {pct}% (追涨风险高)")
    if vr is not None and vr >= 3:
        bearish.append(f"量比 {vr} 放到 3倍以上 (可能派发/诱多)")
    # 60d high distance via kline
    if kl:
        closes = [k["close"] for k in kl]
        wnd = closes[-60:] if len(closes) >= 60 else closes
        if wnd and price is not None:
            hi60 = max(wnd)
            if hi60 > 0:
                dh = (hi60 - price) / hi60 * 100
                if dh <= 3:
                    bearish.append(f"距60日高点仅 {dh:.1f}% (接近套牢盘密集区)")
        # Upper shadow check
        t = kl[-1]
        body = abs(t["close"] - t["open"])
        rng = t["high"] - t["low"]
        upper = t["high"] - max(t["close"], t["open"])
        if rng > 0 and upper >= 2 * body and upper / rng >= 0.5:
            bearish.append(
                f"今日长上影 (上影/实体={upper/max(body,1e-6):.1f}x); "
                "高位冲高回落警示")
    # Inflow contradiction
    if inflow is not None and inflow < -30_000_000:
        bearish.append(f"今日主力净流出 {abs(inflow)/1e8:.2f} 亿 (大额出货)")
    # Market weakness context
    if market_ctx:
        sh = market_ctx.get("sh_pct")
        gem = market_ctx.get("gem_pct")
        if sh is not None and sh < -1.5:
            bearish.append(f"上证今日 {sh}% (大盘弱势, 追涨胜率降低)")
        if gem is not None and gem < -2.0:
            bearish.append(f"创业板今日 {gem}% (小盘风险偏好低)")

    # --- uncertain signals ---
    if p5 is None:
        uncertain.append("缺 5日涨幅数据 (可能是次新股/刚恢复交易)")
    if vr is None:
        uncertain.append("缺 量比数据")
    if inflow is None and c.get("strategy") in ("F2", "D"):
        uncertain.append("资金流数据缺失 (降级源/限流)")
    # Contradictory signals detection
    if p5 is not None and p5 < -2 and pct is not None and pct >= 3:
        uncertain.append(f"5日跌 {p5}% 但今日大涨 {pct}% (V形反转? 或诱多?)")

    return {
        "bullish": bullish,
        "bearish": bearish,
        "uncertain": uncertain,
    }


_BULLISH_PATTERN_LABELS = frozenset({
    "breakout_initial", "silent_accumulation", "sector_initial_move",
    "bottom_first_rally", "low_vol_consolidation",
})
_BEARISH_PATTERN_LABELS = frozenset({
    "gravestone_after_run", "distribution_top", "overheated_chase",
})


def _vote_confidence(code_candidates):
    """Compute confidence label given all candidate rows sharing the
    same code. Rules:
      - CONFLICTED: F1 + F2 on the same bar (mutually exclusive)
      - HIGH:   (a) >=2 strategies, no contradiction, bearish<=2; OR
                (b) single strategy + pattern-resonance: bullish>=3,
                    bearish<=1, AND >=2 bullish pattern_labels with no
                    bearish pattern_labels (e.g. F2 picks that also
                    qualify for silent_accumulation + low_vol_consolidation)
      - MED:    single strategy, bullish>=2, bearish<=1
      - LOW:    everything else
    Returns (label, rationale_str).
    """
    strategies = sorted({c.get("strategy") for c in code_candidates
                         if c.get("strategy")})
    n_strat = len(strategies)

    # Aggregate evidence + patterns across entries for this code
    all_bull = []
    all_bear = []
    pattern_set = set()
    for c in code_candidates:
        ec = c.get("evidence_card") or {}
        all_bull.extend(ec.get("bullish", []))
        all_bear.extend(ec.get("bearish", []))
        for p in (c.get("pattern_labels") or []):
            pattern_set.add(p)

    # Detect strategy-level contradiction: F1 (breakout day) vs F2 (still
    # silent) on the same code is logically impossible in the same bar
    # (one is wrong). Mark as contradiction.
    strat_contradiction = ("F1" in strategies and "F2" in strategies)

    if strat_contradiction:
        return ("CONFLICTED",
                f"策略冲突: {'+'.join(strategies)} "
                "(F1说已突破/F2说仍沉默, 二者不可同时为真)")

    if n_strat >= 2 and len(all_bear) <= 2:
        return ("HIGH",
                f"{n_strat}策略共振: {'+'.join(strategies)}; "
                f"看多{len(all_bull)}项/看空{len(all_bear)}项")

    # Pattern-resonance HIGH: single strategy is fine if multiple bullish
    # pattern archetypes co-fire AND no bearish pattern is present. This
    # catches the common "F2 silent_accumulation also tagged
    # low_vol_consolidation" case which the strict 2-strategy gate misses
    # when the default engine set (C/F1/F2/F3) makes co-hits structurally
    # rare (F1+F2 are mutually exclusive by design; C/F3 are sector-driven
    # and rarely overlap with bottom-up F1/F2).
    bull_patterns = pattern_set & _BULLISH_PATTERN_LABELS
    bear_patterns = pattern_set & _BEARISH_PATTERN_LABELS
    if (n_strat == 1 and len(all_bull) >= 3 and len(all_bear) <= 1
            and len(bull_patterns) >= 2 and not bear_patterns):
        return ("HIGH",
                f"单策略{strategies[0]}+形态共振({'+'.join(sorted(bull_patterns))}); "
                f"看多{len(all_bull)}/看空{len(all_bear)}")

    if n_strat == 1 and len(all_bull) >= 2 and len(all_bear) <= 1:
        return ("MED",
                f"单策略{strategies[0]}+看多{len(all_bull)}/看空{len(all_bear)}")
    return ("LOW",
            f"单策略{strategies[0] if strategies else '?'}; "
            f"看多{len(all_bull)}/看空{len(all_bear)}")


def _build_must_verify_hint(c, kl=None):
    """Return a dict of specific verification steps the LLM MUST run
    before confirming a BUY. This prevents the classic "too eager on
    partial signal" failure mode.
    """
    strat = c.get("strategy", "?")
    code = c.get("code")
    checks = []

    # Strategy-specific checks (universal checks moved to global section in evidence card output)
    if strat == "F1":
        checks.append({
            "check": "突破真实性",
            "how": "需要午后收盘价仍站稳今日开盘价+1%以上；"
                   "若尾盘回到开盘以下 → 放弃 (假突破)",
        })
    if strat == "F2":
        checks.append({
            "check": "吸筹连续性",
            "how": f"明日需继续观察: 若资金回流 ≥50% 今日流入额 → 弃",
        })
        checks.append({
            "check": "MA20 失守",
            "how": "若次日收盘跌破 MA20 → 立即止损, 吸筹逻辑被证伪",
        })
    if strat == "F3":
        checks.append({
            "check": "板块持续性",
            "how": "次日板块涨幅≥+1% 才可持股; 若板块回吐 → 板块轮动失败",
        })
    if strat == "C":
        checks.append({
            "check": "板块惯性",
            "how": "热板滞涨股要求板块本身持续强势; "
                   "若板块当日/次日跑输指数 → 放弃",
        })

    return {
        "code": code,
        "strategy": strat,
        "must_verify": checks,
    }


def _build_devil_advocate(c, evidence_card):
    """Return self-challenge questions the LLM should answer before buy.
    Each question is designed to surface a hidden bearish case.
    """
    questions = []
    p5 = c.get("pct_5d")
    strat = c.get("strategy", "?")
    bullish_n = len(evidence_card.get("bullish", []))
    bearish_n = len(evidence_card.get("bearish", []))

    # Strategy-agnostic challenges moved to global section in evidence card output

    if bearish_n >= 2:
        questions.append(
            f"看空信号已有 {bearish_n} 项 (对看多 {bullish_n} 项); "
            "是否有足够理由认为看多主导? 若不能说服自己 → 放弃")

    if strat == "F2":
        questions.append(
            "主力资金净流入的『主力』是否只是 ETF 被动买盘? "
            "若是 → 不构成吸筹, 只是指数权重股的跟随")
    if strat == "F1":
        questions.append(
            "『首日突破』的 10 日盘整区间，是否只是前期暴跌后的反弹平台? "
            "若是 → 实际是弱反弹不是新 leg")
    if strat == "F3":
        questions.append(
            "这个板块的异动是消息面驱动吗? 若纯靠某个利好催化 "
            "→ 利好消化后 1-2 日内回吐率很高, 不建议参与")
    if p5 is not None and p5 >= 5:
        questions.append(
            f"5日已涨 {p5}%, 若主力在当前价位派发, 接盘者是否有足够利润预期? "
            "若答案是否定 → 说明属于追涨接盘, 放弃")

    return questions


# ==========================================================================
# Recommendation (position sizing + stop levels)
# ==========================================================================

def recommend(capital=10000, market="all",
              strategies=("C", "F1", "F2", "F3"),
              threshold_pct=5.0, top=8, min_trade_value=5000,
              check_bad_news=True, max_per_sector=2,
              stop_loss_pct=3.5, max_position_pct=40.0,
              e_sample=None,
              max_5d_c=6.0, max_5d_d=10.0, max_5d_e=15.0,
              laggard_rel_factor=0.5):
    """Orchestrate strategies C (laggard), D (accumulation), E (breakout).

    Args:
      strategies: tuple of strategy codes to run (subset of C/D/E)
      e_sample: optional int, pass-through to screen_strategy_e.sample
                (debug-only; limits E's universe for rate-limit safety)
      max_5d_c/d/e: absolute 5-day gain caps (Fix A, 2026-05-08). Drop
                candidates already up more than this -- they are no
                longer "laggard" (C) / "early leg" (D) / "just-breakout"
                (E). Pass 999 to disable for a specific strategy.
      laggard_rel_factor: Fix B true-laggard test -- stock 5d pct must
                stay below sector 5d pct * this factor (default 0.5).

    Returns (results, meta) where meta has funnel info for transparency.
    """
    # Capital persisted in meta so _print_next_step_block can expose it in
    # [STATE] for the S5 "C path" (LLM reallocation) without widening the
    # function signature.
    meta = {"warnings": [], "funnel": {}, "capital": capital}

    # Reset intraday-strict denial log at the start of every recommend
    # invocation. Any stale-cache fallback denied during this run (because
    # we are inside continuous-trading hours and refuse to serve yesterday's
    # prices for a T+1 entry decision) gets appended by `_maybe_stale_cache`
    # and aggregated into meta below for `_print_next_step_block` to expose.
    _INTRADAY_STRICT_DENIALS.clear()

    # 0.-1 HARD GATE: tushare token state. Must be EITHER explicitly set
    # (and tier-probe succeeds) OR explicitly skipped before we run any
    # strategy. Rationale: in degraded-network scenarios (EM partial /
    # Sina dead) the script silently produced 20 candidates with garbage
    # numerics + 50% prob=low + 7 reject_reason hits -- effectively
    # poisoned data the LLM cannot distinguish from healthy output.
    # We refuse to run until the user makes the explicit decision so the
    # backstop source is either ready or knowingly off. Returns an empty
    # result + abort_reason so print_recommend short-circuits to a clean
    # HINT block (no funnel, no table, no NEXT_STEP).
    _ts_status = _get_tushare_status()
    if _ts_status == "unset":
        print(
            'HINT: tushare_token_required {'
            '"ask_user":"运行选股前需要确认 tushare 备用源状态。请提供 tushare token '
            '（tushare.pro 注册即送 120 积分），或回复跳过永久禁用此功能",'
            '"example_set":"python ${SKILL_DIR}/stockquant/scripts/stockquant.py '
            'tushare-token --set <TOKEN>",'
            '"example_skip":"python ${SKILL_DIR}/stockquant/scripts/stockquant.py '
            'tushare-token --skip",'
            '"after":"set 或 skip 成功后直接重跑原命令；本次脚本已停止以避免污染数据"'
            '}'
        )
        meta["abort_reason"] = "tushare_token_required"
        meta["info_sufficiency"] = "insufficient"
        meta["info_insufficient"] = True
        meta["tushare"] = {"tier": "unset", "info": {"reason": "no_token"}}
        return [], meta
    # status == "ready" -> validate token actually works via tier probe.
    # status == "skipped" -> proceed without tushare.
    if _ts_status == "ready":
        try:
            _ts_tier_gate, _ts_info_gate = _get_tushare_tier()
        except Exception as _e:
            _ts_tier_gate = "probe_failed"
            _ts_info_gate = {"reason": f"{type(_e).__name__}: {_e}"}
        if _ts_tier_gate == "auth_failed":
            print(
                'HINT: tushare_auth_failed {'
                '"ask_user":"已配置的 tushare token 鉴权失败，请重新提供有效 token，'
                '或回复跳过永久禁用此功能",'
                '"example_set":"python ${SKILL_DIR}/stockquant/scripts/stockquant.py '
                'tushare-token --set <NEW_TOKEN>",'
                '"example_skip":"python ${SKILL_DIR}/stockquant/scripts/stockquant.py '
                'tushare-token --skip",'
                '"after":"set 或 skip 后直接重跑原命令；本次脚本已停止"'
                '}'
            )
            meta["abort_reason"] = "tushare_auth_failed"
            meta["info_sufficiency"] = "insufficient"
            meta["info_insufficient"] = True
            meta["tushare"] = {"tier": _ts_tier_gate, "info": _ts_info_gate}
            return [], meta

    # 0.0 Network preflight: fail fast when every East Money endpoint is
    # unreachable. Without this guard we silently burn 60+ seconds on dead
    # TCP, end up with partial candidates, and mislead the LLM into
    # placing a single-ticker buy (root-cause seen on real phone runs).
    # See _preflight_connectivity_check docstring for probe rationale.
    _probe_result = _preflight_connectivity_check()
    meta["preflight"] = _probe_result
    # Count only DATA-source EM probes (em_clist / em_sector / em_kline).
    # em_pic is a diagnostic-only probe (image service on a different EM
    # subdomain) -- excluded from the alive count but used to disambiguate
    # "WAF rate-limit on push2" vs "phone-level network dead".
    _em_data_keys = [k for k in _PREFLIGHT_PROBES
                     if k.startswith("em_") and k != "em_pic"]
    _em_data_total = len(_em_data_keys)
    _em_alive = sum(1 for k in _em_data_keys if _probe_result.get(k) == "ok")
    _sina_alive = _probe_result.get("sina") == "ok"
    _em_pic_alive = _probe_result.get("em_pic") == "ok"
    # Resolve tushare tier for the DATA_SOURCE_STATUS block.
    # Prefer the gate-stage probe result (already executed above when
    # _ts_status == "ready") so the status block reflects the *real* token
    # state regardless of EM health. Previously we only probed when EM was
    # degraded, which mis-printed "UNSET" on healthy-EM runs even after the
    # user had successfully saved a token.
    if _ts_status == "ready":
        _ts_tier = _ts_tier_gate
        _ts_info = _ts_info_gate
    elif _ts_status == "skipped":
        _ts_tier = "skipped"
        _ts_info = {"reason": "user_skipped"}
    else:
        _ts_tier = "unset"
        _ts_info = {}
    _ts_usable = _ts_tier in ("basic", "full")
    meta["tushare"] = {"tier": _ts_tier, "info": _ts_info}
    # Progressive-disclosure: when no usable channel detected up-front,
    # emit a structured HINT to stdout (so the LLM sees an actionable
    # ask_user template w/ example commands) but DO NOT abort -- still
    # let strategies run; some Stage-1 paths have intra-call retry /
    # stale-cache fallback that may still salvage partial candidates.
    # Final sufficiency is judged at the bottom of recommend() after
    # everything has been tried (see meta["info_insufficient"]).
    meta["preflight_all_dead"] = (
        _em_alive == 0 and not _sina_alive and not _ts_usable
    )
    if meta["preflight_all_dead"]:
        if _em_pic_alive and _ts_tier in ("unset", "skipped"):
            # Network is fine, push2 just WAF-throttled, and user has no
            # tushare token. This is the most common recoverable case --
            # surface a token_unset HINT mirroring _fetch_tushare_kline's
            # JSON shape so the LLM can route via ask_user immediately.
            print(
                'HINT: tushare_token_unset {'
                '"ask_user":"网络主源(东财push2)被限流，需要 tushare token 解锁备用全市场源'
                '（tushare.pro 注册即送 120 积分），请提供 token，或回复跳过",'
                '"example_set":"python ${SKILL_DIR}/stockquant/scripts/stockquant.py '
                'tushare-token --set <TOKEN>",'
                '"example_skip":"python ${SKILL_DIR}/stockquant/scripts/stockquant.py '
                'tushare-token --skip",'
                '"after":"set/skip 成功后直接重跑原命令，无需 sleep"'
                '}'
            )
        elif _em_pic_alive and _ts_tier == "auth_failed":
            print(
                'HINT: tushare_auth_failed {'
                '"ask_user":"tushare token 鉴权失败，请重新提供 token，或回复跳过",'
                '"example_set":"python ${SKILL_DIR}/stockquant/scripts/stockquant.py '
                'tushare-token --set <NEW_TOKEN>",'
                '"example_skip":"python ${SKILL_DIR}/stockquant/scripts/stockquant.py '
                'tushare-token --skip",'
                '"after":"set/skip 成功后直接重跑原命令"'
                '}'
            )
        else:
            print(
                'HINT: network_layer_dead {'
                '"diagnose":"webquotepic 也不可达，疑似设备网络层异常 (carrier/DNS/VPN)",'
                '"ask_user":"建议换 WiFi 或关闭 VPN 后重试；是否继续等待并重试？",'
                '"after":"换网络后重跑原命令；真实网络故障靠重试无法解决"'
                '}'
            )
    elif _em_alive == 0:
        # EM 全挂; 看 tushare/Sina 能补到什么程度
        if _ts_usable:
            meta["warnings"].append(
                f"⚠️ EM 全挂; 启用 tushare Tier-2 替代 (tier={_ts_tier}, T-1 close basis)。"
                f"snapshot + 行业板块聚合可用; "
                f"{'D策略 5日资金可用' if _ts_tier == 'full' else 'D策略主力资金不可用 (basic tier)'}; "
                f"E策略可用。"
                f"{'(EM 限流, 非网络故障)' if _em_pic_alive else '(EM 网络层异常)'}"
            )
            print(f"WARN: preflight EM dead; tushare tier={_ts_tier} will substitute: "
                  f"{_probe_result}", file=sys.stderr)
        else:
            meta["warnings"].append(
                f"⚠️ EM 全挂但 Sina 可用：将走 Tier-3 Sina 全市场 fallback "
                f"（慢 10-15s，字段精度降级：无板块/无主力资金/无换手率）。"
                f"策略 C/D 几乎无候选，策略 E 仍可跑。"
                f"{'(网络通畅, push2 被限流)' if _em_pic_alive else '(网络层异常)'} "
                f"probe={_probe_result}"
            )
            print(f"WARN: preflight EM dead, Sina alive, no tushare; Tier-3 Sina degrade: "
                  f"{_probe_result}", file=sys.stderr)
    elif _em_alive < _em_data_total:
        meta["warnings"].append(
            f"⚠️ 网络部分可用：仅 {_em_alive}/{_em_data_total} EM 端点存活（{_probe_result}）。"
            f"结果可靠性降低，建议重试或换网络"
        )
        print(f"WARN: preflight only {_em_alive}/{_em_data_total} EM endpoints alive: "
              f"{_probe_result}", file=sys.stderr)

    # Emit a structured DATA_SOURCE_STATUS block so the LLM can quote it
    # verbatim to the user (per agent's "数据源透明" requirement). Always
    # printed -- healthy runs show 'all primary OK' which is informative.
    _print_data_source_status(_probe_result, _ts_tier, _ts_info,
                              _em_alive, _em_data_total, _sina_alive,
                              _em_pic_alive)

    # 0. Trading-day / weekend warnings
    is_trading, reason = is_trading_day_probe()
    now = datetime.datetime.now()
    if not is_trading:
        meta["warnings"].append(
            f"⚠️ 非交易时段：{reason}（建议下一个交易日开盘前 09:15~09:25 再跑）")
    if now.weekday() == 4:                                # Friday
        meta["warnings"].append(
            "⚠️ 今日周五：隔日持仓需过双休日，消息面风险放大，建议降低仓位")

    # 0.2 Intraday-late-session warning (10:30~13:30 no-go-zone)
    if is_trading:
        _t = now.time()
        if datetime.time(10, 30) <= _t < datetime.time(11, 30):
            meta["warnings"].append(
                "🚨【盘时警告】当前 10:30~11:30 上午中段，已过首小时价格发现期。"
                "**结果仅供观察，不建议下单**。最佳下一时点：14:30~14:50 尾盘。"
            )
        elif datetime.time(11, 30) <= _t < datetime.time(13, 0):
            meta["warnings"].append(
                "🚨【盘时警告】当前 11:30~13:00 午休非交易时段。"
                "**结果仅供观察，不建议下单**。等 13:00 开盘 + 30min 再重跑。"
            )
        elif datetime.time(13, 0) <= _t < datetime.time(13, 30):
            meta["warnings"].append(
                "🚨【盘时警告】当前 13:00~13:30 下午开盘前 30min，方向未定。"
                "**结果仅供观察，不建议下单**。等 13:30 后确认方向再入场。"
            )

    # 0.5 Macro probe: SH + GEM pct as a SCORING FACTOR, not a gate.
    market_ctx = {"sh_pct": None, "gem_pct": None}
    try:
        mkt_overview = get_market_overview()
        sh = next((x for x in mkt_overview if x["name"] == "上证指数"), None)
        cyb = next((x for x in mkt_overview if x["name"] == "创业板指"), None)
        probes = [p for p in (sh, cyb) if p]
        if probes:
            worst = min(probes, key=lambda p: p["pct"])
            meta["market"] = {
                "sh_pct": sh["pct"] if sh else None,
                "sh_price": sh["price"] if sh else None,
                "cyb_pct": cyb["pct"] if cyb else None,
                "cyb_price": cyb["price"] if cyb else None,
                "worst_name": worst["name"],
                "worst_pct": worst["pct"],
            }
            market_ctx = {
                "sh_pct": sh["pct"] if sh else None,
                "gem_pct": cyb["pct"] if cyb else None,
            }
            both_pct = " / ".join(f"{p['name']} {p['pct']:+.2f}%" for p in probes)
            # Advisory-only: score factor handles ranking.
            if worst["pct"] < -2.0:
                meta["warnings"].append(
                    f"🛑 大盘重挫（{both_pct}）：C/D/E 全部 long-biased，-10 重罚。"
                    f"建议空仓或只观察强势板块龙头。"
                )
            elif worst["pct"] < -1.0:
                meta["warnings"].append(
                    f"⚠️ 大盘弱势（{both_pct}）：-6 分数惩罚，建议降仓位。"
                )
            # Expose single market-trend delta for LLM context
            _probe = {"strategy": "C"}                    # any of C/D/E same weight
            meta["market"]["market_trend_delta"] = int(_market_context_delta(
                _probe, market_ctx, None))
    except Exception as e:
        print(f"WARN: macro probe failed: {type(e).__name__}: {e}", file=sys.stderr)

    # 1. Hot sectors cache (reused by scoring + LLM hints)
    ind_rank = get_sector_rank("industry", top=15, fail_safe=True)
    hot_by_pct = {s["name"] for s in ind_rank[:10]}
    # `main_inflow` may be None when tushare industry-aggregation fallback
    # is in use (Sina/EM-only fields missing) -> treat None as 0.
    hot_by_flow = {s["name"] for s in ind_rank
                   if (s.get("main_inflow") or 0) > 0}
    hot_sectors = hot_by_pct | hot_by_flow
    meta["funnel"]["hot_sectors"] = len(hot_sectors)
    # Snapshot sector rank so market log can persist today's hot boards.
    # Keep compact fields only (name/pct/main_inflow) for disk efficiency.
    meta["sector_rank_top15"] = [
        {"name": s.get("name"), "pct": s.get("pct"),
         "main_inflow": s.get("main_inflow")} for s in (ind_rank or [])
    ]
    if not ind_rank:
        meta["warnings"].append("⚠️ 板块榜接口失败（可能被限流）；热板加分维度丢失")
    sector_pct_map = {s["name"]: s.get("pct") for s in ind_rank if s.get("name")}
    top5_sectors_cached = {s["name"] for s in ind_rank[:5] if s.get("name")}

    # 2. Screen -- run each requested engine independently
    pool_c = pool_d = pool_e = pool_f1 = pool_f2 = pool_f3 = []
    if "C" in strategies:
        try:
            pool_c = screen_strategy_c(market=market,
                                       max_5d_pct=max_5d_c,
                                       laggard_rel_factor=laggard_rel_factor)
            meta["funnel"]["strategy_C"] = len(pool_c)
            meta["funnel"]["C_stage1_drops"] = getattr(
                screen_strategy_c, "last_stage1_drops", {})
            meta["c_pool_review"] = getattr(
                screen_strategy_c, "last_pool_review", None)
        except Exception as e:
            print(f"WARN: strategy C failed: {type(e).__name__}: {e}", file=sys.stderr)
            meta["warnings"].append(f"⚠️ 策略C异常：{e}")
    if "D" in strategies:
        try:
            pool_d = screen_strategy_d(market=market, max_5d_pct=max_5d_d)
            meta["funnel"]["strategy_D"] = len(pool_d)
            meta["funnel"]["D_stage1_drops"] = getattr(
                screen_strategy_d, "last_stage1_drops", {})
            meta["d_pool_review"] = getattr(
                screen_strategy_d, "last_pool_review", None)
        except Exception as e:
            print(f"WARN: strategy D failed: {type(e).__name__}: {e}", file=sys.stderr)
            meta["warnings"].append(f"⚠️ 策略D异常：{e}")
    if "E" in strategies:
        try:
            pool_e = screen_strategy_e(market=market, sample=e_sample,
                                       max_5d_pct=max_5d_e)
            meta["funnel"]["strategy_E"] = len(pool_e)
            meta["funnel"]["E_stage1_drops"] = getattr(
                screen_strategy_e, "last_stage1_drops", {})
            meta["e_pool_review"] = getattr(
                screen_strategy_e, "last_pool_review", None)
        except Exception as e:
            print(f"WARN: strategy E failed: {type(e).__name__}: {e}", file=sys.stderr)
            meta["warnings"].append(f"⚠️ 策略E异常：{e}")
    if "F1" in strategies:
        try:
            pool_f1 = screen_strategy_f1(market=market)
            meta["funnel"]["strategy_F1"] = len(pool_f1)
            meta["funnel"]["F1_stage1_drops"] = getattr(
                screen_strategy_f1, "last_stage1_drops", {})
            meta["f1_pool_review"] = getattr(
                screen_strategy_f1, "last_pool_review", None)
        except Exception as e:
            print(f"WARN: strategy F1 failed: {type(e).__name__}: {e}", file=sys.stderr)
            meta["warnings"].append(f"⚠️ 策略F1异常：{e}")
    if "F2" in strategies:
        try:
            pool_f2 = screen_strategy_f2(market=market)
            meta["funnel"]["strategy_F2"] = len(pool_f2)
            meta["funnel"]["F2_stage1_drops"] = getattr(
                screen_strategy_f2, "last_stage1_drops", {})
            meta["f2_pool_review"] = getattr(
                screen_strategy_f2, "last_pool_review", None)
        except Exception as e:
            print(f"WARN: strategy F2 failed: {type(e).__name__}: {e}", file=sys.stderr)
            meta["warnings"].append(f"⚠️ 策略F2异常：{e}")
    if "F3" in strategies:
        try:
            pool_f3 = screen_strategy_f3(market=market)
            meta["funnel"]["strategy_F3"] = len(pool_f3)
            meta["funnel"]["F3_stage1_drops"] = getattr(
                screen_strategy_f3, "last_stage1_drops", {})
            meta["f3_pool_review"] = getattr(
                screen_strategy_f3, "last_pool_review", None)
        except Exception as e:
            print(f"WARN: strategy F3 failed: {type(e).__name__}: {e}", file=sys.stderr)
            meta["warnings"].append(f"⚠️ 策略F3异常：{e}")
    pool = pool_c + pool_d + pool_e + pool_f1 + pool_f2 + pool_f3

    # Detect data source degradation
    sources = {c.get("_source", "em") for c in pool}
    if "sina" in sources:
        meta["warnings"].append(
            "⚠️ 行情主源（东财 clist）失败，已降级到新浪备用源。打分质量降低。")
        meta["data_source"] = "sina_fallback"
    else:
        meta["data_source"] = "em"

    # Aggregate stage1 degradation flags across all three strategies so
    # print_recommend can expose a compact [DATA_QUALITY] section and the
    # LLM can reference it accurately in its terminate text.
    dq = {}
    c_review = meta.get("c_pool_review") or {}
    d_review = meta.get("d_pool_review") or {}
    e_review = meta.get("e_pool_review") or {}
    if c_review.get("degraded_sectors", 0) > 0:
        dq["strategy_C_sector_kline"] = {
            "degraded": True,
            "degraded_sector_count": c_review["degraded_sectors"],
            "note": "板块 K 线 API 失败，热门板块已降级用当日涨幅近似 N 日累计",
        }
    if d_review.get("degraded_single_day"):
        dq["strategy_D_multiday_flow"] = {
            "degraded": True,
            "note": "多日主力资金流 API 失败，5日累计已降级用单日 *3 近似 "
                    "(排序改用单日净流入绝对值)",
        }
    if e_review.get("degraded_split_fetch"):
        dq["strategy_E_universe"] = {
            "degraded": True,
            "note": "_FS_ALL_A 合并清单 API 失败，已降级分别拉取 main/gem/star 三个子市场",
        }
    if dq:
        meta["data_quality"] = dq
        meta["warnings"].append(
            f"⚠️ 数据源降级：{len(dq)}/3 个策略 Stage1 使用 fallback 路径，"
            f"结果质量略降，详见 [DATA_QUALITY] 段")

    # Aggregate intraday-strict denials. Any entry here means a stale
    # fallback was refused during continuous-trading hours -- the upstream
    # call either succeeded via live tier or raised; either way the LLM
    # must be told because the data graph may have holes (and we'd rather
    # tell the user 'today's data is partial' than silently mix yesterday).
    if _INTRADAY_STRICT_DENIALS:
        meta.setdefault("data_quality", {})
        meta["data_quality"]["intraday_stale_denied"] = list(_INTRADAY_STRICT_DENIALS)
        # Critical flag controls the brief output: when True,
        # `_print_next_step_block` skips PASS_TOP10 entirely and emits a
        # hard-terminate banner instead of letting the LLM act on a
        # potentially-corrupted snapshot.
        meta["data_quality_critical"] = True
        layers = sorted({d["layer"] for d in _INTRADAY_STRICT_DENIALS})
        meta["warnings"].append(
            f"🛑 盘中实时数据失败（拒绝 stale cache）：受影响层 = {layers}；"
            f"已停止入场决策，等待数据恢复后重跑")

    # 3. Unified scoring (C/D/E share _unified_score + _market_context_delta)
    ranked = score_candidates(pool, hot_sectors=hot_sectors,
                              market_ctx=market_ctx,
                              sector_pct_map=sector_pct_map)
    meta["funnel"]["scored"] = len(ranked)
    # Snapshot top-50 scored candidates for the post-hoc candidates log.
    # Kept as lightweight dicts (essential scoring + strategy-specific fields)
    # so backtest / "why missed" analysis can reconstruct the pool.
    meta["ranked_all"] = ranked[:50]

    # 4. Sector diversification: cap picks per industry (default 2)
    if max_per_sector and max_per_sector > 0 and ranked:
        sector_count = {}
        deduped = []
        dropped_by_sector = 0
        for c in ranked:
            ind = (c.get("industry") or "").strip()
            if not ind:
                deduped.append(c)                          # keep unknown-sector as-is
                continue
            n = sector_count.get(ind, 0)
            if n >= max_per_sector:
                dropped_by_sector += 1
                continue
            sector_count[ind] = n + 1
            deduped.append(c)
        ranked = deduped
        meta["funnel"]["sector_diversified_dropped"] = dropped_by_sector
        meta["funnel"]["sectors_in_top"] = len(
            [k for k, v in sector_count.items() if v > 0])

    # 5. Position sizing (max lots within capital, must meet min_trade_value)
    final = []
    skipped_price = 0
    for c in ranked:
        shares, cost = _calc_shares(c["price"], capital, min_trade_value,
                                    max_position_pct=max_position_pct)
        if shares == 0:
            skipped_price += 1
            continue
        c["shares"] = shares
        c["cost"] = cost
        c["stop_profit"] = round(c["price"] * (1 + threshold_pct / 100), 2)
        c["stop_loss"] = round(c["price"] * (1 - stop_loss_pct / 100), 2)
        final.append(c)
        if len(final) >= top:
            break
    meta["funnel"]["skipped_for_price"] = skipped_price
    meta["funnel"]["final"] = len(final)

    # 6. LLM hints layer (reject/warn/boost tags + next_day_prob bucket)
    top5_sectors = top5_sectors_cached
    bad_news_map = None
    if check_bad_news and final:
        try:
            bad_news_map = _scan_bad_news_for_final(final, days=7)
        except Exception as e:
            print(f"WARN: bad-news scan failed: {e}", file=sys.stderr)
            bad_news_map = {}

    _apply_llm_hints(final, market_ctx, top5_sectors, meta,
                     bad_news_map=bad_news_map)

    # 6.5 Multi-source enrichment + merge for top-20 candidates.
    # Pulls EM single-quote, Sina hq, Sina vip moneyflow, tushare snapshot
    # in parallel and attaches a `_data_quality` block per candidate listing
    # all sources, conflict flags (numeric spread > threshold or category
    # mismatch), and per-field provenance. The LLM uses this metadata to
    # apply soft judgement -- e.g. lower confidence when one source dissents
    # significantly, or skip the candidate when too many fields conflict.
    # No-op for empty `final`; bounded cost ~5s for 20 candidates.
    if final:
        try:
            enrich_top_candidates(final, max_depth=20)
            # Surface quality summary in meta for the LLM.
            n_with_dq = sum(1 for c in final if c.get("_data_quality"))
            n_conflicts = sum(
                sum(1 for f, m in (c.get("_data_quality") or {}).items()
                    if m.get("conflict"))
                for c in final
            )
            meta["multi_source_merge"] = {
                "candidates_enriched": n_with_dq,
                "field_conflicts": n_conflicts,
            }
        except Exception as e:
            print(f"WARN: multi-source enrichment failed: "
                  f"{type(e).__name__}: {e}", file=sys.stderr)
            meta["multi_source_merge"] = {"error": f"{type(e).__name__}"}

    # 6.6 Strict reject filter. Picks that triggered any hard-reject tag
    # (over_extended / panic_volume / big_outflow_today / late_entry, etc.)
    # in _apply_llm_hints must NOT enter the recommendation table or
    # capital allocation -- log analysis showed 5/20 picks carrying 🚫
    # tags were still listed as Top-N rows, leading the LLM to cite
    # `🚫big_outflow_today prob=low` rows as legitimate buys. Stash them
    # under meta["rejected_picks"] so the [DATA] REJECT_LIST block in
    # NEXT_STEP can still surface them for transparency / audit.
    _rejected_after_hints = [
        c for c in final if (c.get("reject_reasons") or [])
    ]
    if _rejected_after_hints:
        meta["rejected_picks"] = _rejected_after_hints
        meta["funnel"]["rejected_after_hints"] = len(_rejected_after_hints)
        final = [c for c in final if not (c.get("reject_reasons") or [])]
        meta["funnel"]["final"] = len(final)

    # 6.7 Evidence card + pattern match + confidence + devil-advocate.
    # Attached to each final pick to give the LLM structured bullish /
    # bearish / uncertain signal lists, explicit pattern labels, and a
    # confidence label (HIGH / MED / LOW / CONFLICTED) derived from
    # cross-strategy agreement. These fields are consumed verbatim by
    # the print_recommend layer and also by the NEXT_STEP prompt block;
    # design intent is that the LLM stops pattern-matching from raw
    # numbers and reads plain-language signals instead -- the core
    # failure mode in recent loss analyses was "LLM cited 3 bullish
    # numbers, ignored 2 bearish numbers in the same dict, confirmed
    # BUY". Now the card forces the bearish list to be visible.
    try:
        # Fetch fresh kline for final picks (bounded cost, small N).
        final_codes = [c["code"] for c in final]
        kl_map_final = (get_daily_klines_batch(final_codes, n=60, workers=8)
                        if final_codes else {})
        # Cross-strategy aggregation: group duplicate-code entries first
        by_code_all = {}
        for c in ranked:                            # aggregate across all ranked
            by_code_all.setdefault(c["code"], []).append(c)

        for c in final:
            kl = kl_map_final.get(c["code"]) or []
            ec = _build_evidence_card(
                c, kl=kl, market_ctx=market_ctx, hot_sectors=hot_sectors)
            c["evidence_card"] = ec
            c["pattern_labels"] = _match_patterns(c, kl=kl)
            # Confidence voting reads ALL entries with this code across
            # strategies (not just the one copy in `final`), since a
            # stock may be hit by F2 AND F3 but only enter `final` once.
            related = by_code_all.get(c["code"], [c])
            # Ensure each related has evidence card (so vote can count)
            for rc in related:
                if "evidence_card" not in rc:
                    rc["evidence_card"] = _build_evidence_card(
                        rc, kl=kl, market_ctx=market_ctx,
                        hot_sectors=hot_sectors)
            label, why = _vote_confidence(related)
            c["confidence_label"] = label
            c["confidence_reason"] = why
            c["must_verify_before_buy"] = _build_must_verify_hint(c, kl=kl)
            c["devil_advocate_questions"] = _build_devil_advocate(c, ec)
        meta["enrichment"] = {
            "evidence_cards_built": len(final),
            "patterns_detected": sum(
                len(c.get("pattern_labels") or []) for c in final),
        }
    except Exception as e:
        print(f"WARN: evidence/pattern enrichment failed: "
              f"{type(e).__name__}: {e}", file=sys.stderr)
        meta["enrichment"] = {"error": f"{type(e).__name__}: {e}"}

    # 7. Capital allocation plan (fixed per-stock target, score-descending).
    # Kept AFTER _apply_llm_hints + reject filter so `final` is fully
    # decorated AND clean of hard-rejects; the planner only reads
    # price / strategy / stop / score / industry / prob fields.
    try:
        plan = _build_allocation_plan(final, capital, per_target=10000.0)
        meta["allocation_plan"] = plan
    except Exception as e:
        print(f"WARN: allocation plan build failed: {e}", file=sys.stderr)
        meta["allocation_plan"] = {"items": [], "used": 0,
                                   "remaining_cash": capital,
                                   "skipped": [], "per_target": 10000.0}

    # 8. Persist per-stock context for the 2nd-pass `allocate` subcommand.
    # This lets the LLM reorder / prune picks after risk review and call
    # `python stockquant.py allocate --codes ... --capital ... --comment ...`
    # to get an authoritative Python-formatted table (no LLM arithmetic).
    _save_allocation_context(final, capital)

    # 9. Info-sufficiency self-evaluation. Replaces the old preflight
    # hard-stop: instead of refusing to run when sources look bad, we
    # let every fallback path run to completion, then judge the actual
    # yield. Three buckets the LLM consumes via meta + the HINT block
    # printed by print_recommend:
    #   - len(final) >= 5 : sufficient (even if degraded; just note it)
    #   - 1 <= len(final) < 5 : partial (let the LLM ask the user
    #                           whether to act on a thin pool or retry)
    #   - len(final) == 0 : insufficient (must ask user; do NOT auto-wait)
    n_final = len(final)
    if n_final == 0:
        sufficiency = "insufficient"
    elif n_final < 5:
        sufficiency = "partial"
    else:
        sufficiency = "sufficient"
    meta["info_sufficiency"] = sufficiency
    meta["info_insufficient"] = (sufficiency != "sufficient")

    return final, meta


# ==========================================================================
# Daily logging + post-hoc evaluation (eval + stats).
# Design: one JSONL per day under logs/recommend/YYYYMMDD.jsonl; each line
# is one final pick. The eval command reads a given day's file, fetches the
# NEXT trading day's daily k-line, and determines whether stop-profit /
# stop-loss triggered. stats aggregates the last N days of eval output.
# Goal: transform strategy tuning from vibes-driven to data-driven.
# ==========================================================================

_LOGS_DIR = os.path.join(_SKILL_DIR, "logs")

def _log_path(kind, date):
    """kind: 'recommend' | 'eval'. Returns full path for the jsonl file."""
    sub = os.path.join(_LOGS_DIR, kind)
    os.makedirs(sub, exist_ok=True)
    return os.path.join(sub, f"{date}.jsonl")


# ==========================================================================
# Verbose-log side-channel (Q4 output-size pruning)
# ==========================================================================
# The agent-facing stdout has a hard head-truncation cap (20000 chars in
# UnifiedActionExecutor). A full `brief` run legitimately emits ~30-60KB
# because of per-strategy funnel drops + allocation baseline + per-candidate
# soft/boost reasons. We split the output into two channels:
#
#   stdout:           decision-critical data the LLM MUST see every step
#                     (NEXT_STEP block, final Top-N table, DATA_QUALITY,
#                     funnel summary, market gate)
#   verbose log file: drill-down detail the LLM only reads on demand
#                     (Stage1 drops dict, allocation baseline table,
#                     per-candidate soft_warnings/boost_reasons, hot-sector
#                     top-10 breakdown)
#
# The verbose path is printed at the TOP of stdout so the LLM can `read_file`
# it when (and only when) it needs to justify or double-check a decision.

_VERBOSE_LOG_FH = None
_VERBOSE_LOG_PATH = None


def _open_verbose_log():
    """Open a per-run verbose log file under skill/logs/verbose/<ts>.txt.

    Idempotent; subsequent calls return the same handle. Failure to open
    degrades silently (verbose-only content then disappears); the main
    stdout path is never blocked by verbose-log I/O.
    """
    global _VERBOSE_LOG_FH, _VERBOSE_LOG_PATH
    if _VERBOSE_LOG_FH is not None:
        return _VERBOSE_LOG_PATH
    try:
        sub = os.path.join(_LOGS_DIR, "verbose")
        os.makedirs(sub, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(sub, f"{ts}.txt")
        _VERBOSE_LOG_FH = open(path, "w", encoding="utf-8")
        _VERBOSE_LOG_PATH = path
        # Header so `read_file` consumers immediately see what this is.
        _VERBOSE_LOG_FH.write(
            f"# stockquant verbose log\n# generated {datetime.datetime.now().isoformat()}\n"
            f"# consumed by: agent on-demand via read_file\n\n"
        )
        _VERBOSE_LOG_FH.flush()
    except Exception:
        _VERBOSE_LOG_FH = None
        _VERBOSE_LOG_PATH = None
    return _VERBOSE_LOG_PATH


def _vprint(*args, **kwargs):
    """Write to the verbose log only (never stdout).

    Signature mirrors print() for drop-in substitution. sep/end supported.
    """
    if _VERBOSE_LOG_FH is None:
        return
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")
    try:
        _VERBOSE_LOG_FH.write(sep.join(str(a) for a in args) + end)
    except Exception:
        pass


def _v_or_print(*args, **kwargs):
    """Write to verbose log if open, else to stdout.

    Used for content that is "nice to have for drill-down" but OK on stdout
    when no verbose log is active (legacy / non-brief CLI runs).
    """
    if _VERBOSE_LOG_FH is not None:
        _vprint(*args, **kwargs)
    else:
        print(*args, **kwargs)


def _flush_verbose_log():
    """Flush + close the verbose log file handle."""
    global _VERBOSE_LOG_FH
    if _VERBOSE_LOG_FH is not None:
        try:
            _VERBOSE_LOG_FH.flush()
            _VERBOSE_LOG_FH.close()
        except Exception:
            pass
        _VERBOSE_LOG_FH = None


def _build_pick_row(c, ts, today, kind="pick", run_args=None):
    """Flatten one candidate/pick into a JSONL row.

    Union schema across C/D/E strategies plus common fields. Strategy-specific
    fields (e.g. box_high for E, main_inflow_5d for D, laggard_gap for C) are
    recorded as-is; keys absent on the source dict are simply not included by
    dict.get -> None paths. Downstream analysis can group by `strategy` and
    select relevant columns.
    """
    row = {
        "ts": ts,
        "date": today,
        "kind": kind,                                      # "pick" or "cand"
        "code": c.get("code"),
        "name": c.get("name"),
        "strategy": c.get("strategy"),
        "score": c.get("score"),
        # Common price + volume fields -----------------------------------
        "price": c.get("price"),
        "pct": c.get("pct"),
        "amount": c.get("amount"),
        "turnover": c.get("turnover"),
        "volume_ratio": c.get("volume_ratio"),
        "float_mv": c.get("float_mv"),
        "main_inflow": c.get("main_inflow"),
        "industry": c.get("industry"),
        # Final-pick-only: position sizing + stops (None for candidate rows) ---
        "shares": c.get("shares"),
        "cost": c.get("cost"),
        "stop_profit": c.get("stop_profit"),
        "stop_loss": c.get("stop_loss"),
        # MA features (all strategies populate distance_from_ma20) --------
        "ma20": c.get("ma20"),
        "ma40": c.get("ma40"),
        "ma60": c.get("ma60"),
        "distance_from_ma20": c.get("distance_from_ma20"),
        "ma_aligned": c.get("ma_aligned"),
        # Strategy C specific ---------------------------------------------
        "sector_name": c.get("sector_name"),
        "sector_code": c.get("sector_code"),
        "sector_n_day_pct": c.get("sector_n_day_pct"),
        "stock_n_day_pct": c.get("stock_n_day_pct"),
        "laggard_gap": c.get("laggard_gap"),
        # Strategy D specific ---------------------------------------------
        "main_inflow_5d": c.get("main_inflow_5d"),
        "main_inflow_pct_5d": c.get("main_inflow_pct_5d"),
        "main_inflow_10d": c.get("main_inflow_10d"),
        "main_inflow_pct_10d": c.get("main_inflow_pct_10d"),
        "pct_5d": c.get("pct_5d"),
        "pct_10d": c.get("pct_10d"),
        # Strategy E specific ---------------------------------------------
        "box_days": c.get("box_days"),
        "box_high": c.get("box_high"),
        "box_low": c.get("box_low"),
        "box_range_pct": c.get("box_range_pct"),
        "box_position_pct": c.get("box_position_pct"),
        # LLM hints produced by _apply_llm_hints (final picks only) ------
        "reject_reasons": c.get("reject_reasons"),
        "soft_warnings": c.get("soft_warnings"),
        "boost_reasons": c.get("boost_reasons"),
        "next_day_prob": c.get("next_day_prob"),
        # Data provenance -------------------------------------------------
        "_source": c.get("_source"),
    }
    if run_args is not None:
        row["run_args"] = run_args
    return row


def _append_recommend_log(results, meta, run_args):
    """Append final picks + candidates pool + session snapshot to JSONL logs.

    Three sibling log files under SKILL_DIR/logs/<kind>/YYYYMMDD.jsonl:

      recommend/YYYYMMDD.jsonl
        One row per final pick. Schema is a superset of the old layout so
        existing evaluate_recommendations() still parses without change.
        Includes full C/D/E strategy fields + LLM hint tags.

      candidates/YYYYMMDD.jsonl
        One row per ranked candidate (top-50 from meta['ranked_all']).
        Used for backtest / post-hoc "why missed" analysis: reconstructs
        the full scored pool including candidates not in the final top-N.

      market/YYYYMMDD.jsonl
        One row per recommend invocation: session-level snapshot --
        market_ctx, funnel counts, sector_rank_top15, warnings, hot
        sectors names. This is the index for joining per-pick rows.

    Skips non-trading days entirely: data is stale snapshot, logging would
    pollute downstream eval.
    """
    is_trading, _ = is_trading_day_probe()
    if not is_trading:
        return
    if not results:
        return
    today = _today()
    ts = datetime.datetime.now().isoformat(timespec="seconds")

    # 1. Final picks log (backwards-compatible with evaluate_recommendations)
    pick_path = _log_path("recommend", today)
    try:
        with open(pick_path, "a", encoding="utf-8") as f:
            for c in results:
                row = _build_pick_row(c, ts, today, kind="pick",
                                      run_args=run_args)
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"WARN: recommend-log write failed: {e}", file=sys.stderr)

    # 2. Full candidate pool (top-50 scored, before sector dedup + top-N cut)
    try:
        cand_path = _log_path("candidates", today)
        ranked_all = meta.get("ranked_all") or []
        picked_codes = {c.get("code") for c in results}
        with open(cand_path, "a", encoding="utf-8") as f:
            for c in ranked_all:
                is_picked = c.get("code") in picked_codes
                row = _build_pick_row(c, ts, today, kind="cand")
                row["is_final_pick"] = is_picked            # join key for eval
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"WARN: candidates-log write failed: {e}", file=sys.stderr)

    # 3. Session snapshot (one row per invocation -- market + funnel + sectors)
    try:
        market_path = _log_path("market", today)
        snapshot = {
            "ts": ts,
            "date": today,
            "kind": "session",
            "market": meta.get("market"),
            "funnel": meta.get("funnel"),
            "sector_rank_top15": meta.get("sector_rank_top15"),
            "c_pool_review": meta.get("c_pool_review"),
            "d_pool_review": meta.get("d_pool_review"),
            "e_pool_review": meta.get("e_pool_review"),
            "warnings": meta.get("warnings"),
            "data_source": meta.get("data_source"),
            "final_count": len(results),
            "run_args": run_args,
        }
        with open(market_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(snapshot, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"WARN: market-log write failed: {e}", file=sys.stderr)


def track_recommendations(date=None):
    """Intraday live-tracking of TODAY'S recommend output vs current quote.

    Intent (added 2026-04-22): after user runs `recommend` at 09:15 pre-open,
    this command at 10:00 / 13:00 / 14:45 gives a live quality-check on
    the picks without re-running the whole screening pipeline. Answers:
      - Is each pick moving in the expected direction?
      - Has stop-profit or stop-loss already been hit intraday?
      - Has the list as a whole beaten / lagged the broad market?

    NOT a backtest: backtest is `eval` (T+1 daily kline-based). This reads
    the CURRENT quote only and compares against the snapshot saved at
    recommend time.

    Args:
      date: YYYYMMDD; defaults to today. Rarely useful for past dates (quote
            is live, not historical), so use `eval` for past-day analysis.
    """
    if date is None:
        date = _today()
    rec_path = _log_path("recommend", date)
    if not os.path.exists(rec_path):
        print(f"(no recommend log for {date}; expected at {rec_path})")
        print(f"提示: 请先跑 `python stockquant.py recommend ...` 生成快照。")
        return
    # Read all rows, group by ts (one recommend invocation = one group),
    # keep only the LATEST group (user usually cares about the most recent run).
    rows = []
    with open(rec_path, "r", encoding="utf-8") as f:
        for ln in f:
            try:
                rows.append(json.loads(ln))
            except Exception:
                continue
    if not rows:
        print(f"(recommend log at {rec_path} is empty)")
        return
    # Group by ts; latest group = max ts.
    latest_ts = max(r.get("ts", "") for r in rows)
    picks = [r for r in rows if r.get("ts") == latest_ts]
    codes = [p["code"] for p in picks if p.get("code")]
    if not codes:
        print(f"(latest recommend group at {latest_ts} has no valid codes)")
        return

    # Fetch current quotes in one batch.
    now_map = {m["code"]: m for m in get_market_quotes(codes)}

    # Fetch broad-market reference for context (reuse cache if available).
    try:
        mkt_list = get_market_overview(use_cache=True) or []
        sh = next((x for x in mkt_list if x.get("name") == "上证指数"), None)
        gem = next((x for x in mkt_list if x.get("name") == "创业板指"), None)
        sh_now = (sh or {}).get("pct")
        gem_now = (gem or {}).get("pct")
    except Exception:
        sh_now, gem_now = None, None

    # Per-pick tracking.
    print(f"\n## INTRADAY TRACK  (recommend @ {latest_ts})")
    run_at = datetime.datetime.now().isoformat(timespec="seconds")
    print(f"checked_at: {run_at}")
    sh_s = f"{sh_now:+.2f}%" if sh_now is not None else "n/a"
    gem_s = f"{gem_now:+.2f}%" if gem_now is not None else "n/a"
    print(f"market_now: 上证 {sh_s} | 创业板 {gem_s}\n")
    print("| # | 代码 | 名称 | 策略 | 推荐价 | 当前价 | 涨跌% | 止盈 | 止损 | 状态 |")
    print("|---|------|------|------|--------|--------|-------|------|------|------|")
    hit_tp = 0      # 触发止盈
    hit_sl = 0      # 触发止损
    gained = 0      # 正收益
    lost = 0        # 负收益
    total = 0
    sum_delta = 0.0
    for idx, p in enumerate(picks, 1):
        code = p["code"]
        name = p.get("name", "")
        strat = p.get("strategy", "?")
        rec_price = p.get("price") or 0
        stop_tp = p.get("stop_profit") or 0
        stop_sl = p.get("stop_loss") or 0
        q = now_map.get(code)
        if not q:
            print(f"| {idx} | {code} | {name} | {strat} | {rec_price} | n/a | n/a | {stop_tp} | {stop_sl} | ⚠️ 行情缺失 |")
            continue
        now_price = q.get("price") or 0
        total += 1
        if rec_price > 0 and now_price > 0:
            delta_pct = (now_price - rec_price) / rec_price * 100
        else:
            delta_pct = 0.0
        sum_delta += delta_pct
        # Status: triggered stops (based on current price; TRUE 盘中触及 would
        # need intraday high/low which we don't fetch here -- approximate).
        if stop_tp > 0 and now_price >= stop_tp:
            status = "✅ 达止盈"
            hit_tp += 1
        elif stop_sl > 0 and now_price <= stop_sl:
            status = "❌ 破止损"
            hit_sl += 1
        elif delta_pct > 0:
            status = "⏳ 区间内(盈)"
            gained += 1
        elif delta_pct < 0:
            status = "⏳ 区间内(亏)"
            lost += 1
        else:
            status = "⏳ 持平"
        delta_s = f"{delta_pct:+.2f}%"
        print(f"| {idx} | {code} | {name} | {strat} | {rec_price} | {now_price} | "
              f"{delta_s} | {stop_tp} | {stop_sl} | {status} |")

    # Aggregate summary.
    if total > 0:
        avg_delta = sum_delta / total
        print(f"\n## 汇总")
        print(f"- 覆盖: **{total}** 只 (缺失 {len(picks) - total} 只)")
        print(f"- 平均偏差: **{avg_delta:+.2f}%** (相对推荐时价)")
        if sh_now is not None:
            alpha = avg_delta - sh_now
            print(f"- 相对上证 alpha: **{alpha:+.2f}%**")
        print(f"- 状态分布: 止盈 **{hit_tp}** | 止损 **{hit_sl}** | "
              f"区间内盈 **{gained}** | 区间内亏 **{lost}**")
        if hit_sl > 0:
            print(f"- ⚠️ 已有 {hit_sl} 只跌破止损, 按纪律应立即止损出局")
        if hit_tp > 0:
            print(f"- 🎯 已有 {hit_tp} 只达到止盈目标, 考虑部分或全部了结")


def evaluate_recommendations(date=None):
    """Evaluate recommendations from `date` (YYYYMMDD, default=last trading day).

    For each pick, fetch the next trading day's daily kline (open/high/low/close),
    determine whether stop-profit or stop-loss was hit (using intra-day high/low,
    since daily granularity only), compute actual realized % if stop hit early
    (prefer stop-profit over stop-loss when both within range -- optimistic
    assumption since stop-profit usually triggers in morning rally), else use
    the close price as exit.

    Writes to logs/eval/YYYYMMDD.jsonl and prints summary.
    """
    if date is None:
        date = _trading_date_offset(1)                     # last trading day
    rec_path = _log_path("recommend", date)
    if not os.path.exists(rec_path):
        print(f"(no recommendation log for {date}; expected at {rec_path})")
        return
    rows = []
    with open(rec_path, "r", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            try:
                rows.append(json.loads(ln))
            except Exception:
                continue
    if not rows:
        print(f"(empty log for {date})")
        return
    # Find the next trading day after `date`. We use the index k-line of a
    # representative picks for existence check -- simpler: get_pool("zt") was
    # non-empty on that next day indicates it was a trading day. But simplest:
    # loop forward 1..7 days, query the stock's daily kline ending that day,
    # keep rows where the last kline date > `date`.
    codes = sorted({r["code"] for r in rows if r.get("code")})
    if not codes:
        print("(no codes in log)")
        return
    # Pull 5 days of kline ending today (or recent) for each code
    klines = get_daily_klines_batch(codes, n=5, workers=8)
    eval_rows = []
    stats = {
        "total": 0, "stop_profit_hit": 0, "stop_loss_hit": 0,
        "closed_positive": 0, "closed_negative": 0,
        "sum_return_pct": 0.0, "returns": [],
    }
    for r in rows:
        code = r["code"]
        kl = klines.get(code) or []
        # Find the first kline strictly after `date`
        date_ymd = date if len(date) == 8 else date.replace("-", "")
        next_kl = None
        for k in kl:
            kd = str(k.get("date", "")).replace("-", "")
            if kd > date_ymd:
                next_kl = k
                break
        if not next_kl:
            continue                                       # no next-day data yet
        entry = r.get("price") or 0
        sp = r.get("stop_profit") or 0
        sl = r.get("stop_loss") or 0
        high = next_kl.get("high") or 0
        low = next_kl.get("low") or 0
        close = next_kl.get("close") or 0
        opn = next_kl.get("open") or 0
        # Decide triggered outcome (daily-resolution approximation):
        # - If low <= stop_loss AND high >= stop_profit: both hit intra-day.
        #   We can't know order from daily K alone; conservative: assume
        #   stop-loss hits first (opening gap-down is common in losers).
        # - Else whichever triggered.
        sp_hit = high >= sp and sp > 0
        sl_hit = low <= sl and sl > 0
        outcome = "close"
        exit_price = close
        if sp_hit and sl_hit:
            outcome = "both_stop_loss_assumed"
            exit_price = sl
        elif sp_hit:
            outcome = "stop_profit"
            exit_price = sp
        elif sl_hit:
            outcome = "stop_loss"
            exit_price = sl
        ret_pct = ((exit_price / entry) - 1) * 100 if entry > 0 else 0
        # Also track opening gap and intraday range for context
        open_gap = ((opn / entry) - 1) * 100 if entry > 0 else 0
        eval_row = {
            "date": date,
            "next_date": str(next_kl.get("date", "")),
            "code": code,
            "name": r.get("name"),
            "strategy": r.get("strategy"),
            "score": r.get("score"),
            "entry": entry,
            "stop_profit": sp,
            "stop_loss": sl,
            "next_open": opn,
            "next_high": high,
            "next_low": low,
            "next_close": close,
            "outcome": outcome,
            "exit_price": round(exit_price, 2),
            "return_pct": round(ret_pct, 2),
            "open_gap_pct": round(open_gap, 2),
            "lhb_tag": r.get("lhb_tag"),
            "seal_streak": r.get("seal_streak"),
            "industry": r.get("industry"),
        }
        eval_rows.append(eval_row)
        stats["total"] += 1
        stats["sum_return_pct"] += ret_pct
        stats["returns"].append(ret_pct)
        if outcome == "stop_profit":
            stats["stop_profit_hit"] += 1
        elif outcome in ("stop_loss", "both_stop_loss_assumed"):
            stats["stop_loss_hit"] += 1
        elif ret_pct > 0:
            stats["closed_positive"] += 1
        else:
            stats["closed_negative"] += 1
    # Persist eval rows
    eval_path = _log_path("eval", date)
    try:
        with open(eval_path, "w", encoding="utf-8") as f:
            for row in eval_rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"WARN: eval write failed: {e}", file=sys.stderr)
    # Print summary
    _print_eval_summary(date, eval_rows, stats, rec_path, eval_path)


def _print_eval_summary(date, rows, stats, rec_path, eval_path):
    print(f"# 复盘 {date}  共 {len(rows)} 只\n")
    if not rows:
        print("(no picks had next-day data available; check that "
              f"the T+1 trading day has occurred.)\n"
              f"- log: {rec_path}")
        return
    tot = stats["total"]
    avg_ret = stats["sum_return_pct"] / tot if tot else 0
    wins = stats["stop_profit_hit"] + stats["closed_positive"]
    winrate = wins / tot * 100 if tot else 0
    print(f"- 触发止盈：**{stats['stop_profit_hit']}** / {tot}  "
          f"({stats['stop_profit_hit']/tot*100:.1f}%)")
    print(f"- 触发止损：**{stats['stop_loss_hit']}** / {tot}  "
          f"({stats['stop_loss_hit']/tot*100:.1f}%)")
    print(f"- 平盘正收益：{stats['closed_positive']} / {tot}")
    print(f"- 平盘负收益：{stats['closed_negative']} / {tot}")
    print(f"- **总胜率（止盈+平盘正）：{winrate:.1f}%**")
    print(f"- **平均实际收益：{avg_ret:+.2f}%**  "
          f"(最佳 {max(stats['returns']):+.2f}% / 最差 {min(stats['returns']):+.2f}%)")
    print(f"\n## 明细\n")
    print("| # | 代码 | 名称 | 策略 | 得分 | 买入 | 止盈 | 止损 "
          "| 次日开 | 次日高 | 次日低 | 次日收 | 结局 | 收益% |")
    print("|---:|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---:|")
    # Sort by return desc so "best / worst" is obvious
    for i, r in enumerate(sorted(rows, key=lambda x: -x["return_pct"]), 1):
        oc = {"stop_profit": "✓止盈", "stop_loss": "✗止损",
              "both_stop_loss_assumed": "✗两触(按止损)",
              "close": "平盘"}.get(r["outcome"], r["outcome"])
        print(f"| {i} | {r['code']} | {r['name']} | {r['strategy']} | {r['score']} "
              f"| {r['entry']} | {r['stop_profit']} | {r['stop_loss']} "
              f"| {r['next_open']} | {r['next_high']} | {r['next_low']} | {r['next_close']} "
              f"| {oc} | {r['return_pct']:+.2f} |")
    print(f"\n- log: `{rec_path}` → `{eval_path}`")


def stats_recommendations(days=30):
    """Aggregate eval logs from the last N calendar days -- strategy dashboard.

    Provides overall, per-strategy, per-LHB-tag, per-streak breakdowns, so
    the user can see which factors correlate with actual next-day outcomes.
    """
    cutoff = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y%m%d")
    eval_dir = os.path.join(_LOGS_DIR, "eval")
    if not os.path.isdir(eval_dir):
        print(f"(no eval logs at {eval_dir}; run 'eval' first)")
        return
    files = sorted(
        f for f in os.listdir(eval_dir)
        if f.endswith(".jsonl") and f[:-6] >= cutoff
    )
    if not files:
        print(f"(no eval logs in the last {days} days)")
        return
    all_rows = []
    for fn in files:
        p = os.path.join(eval_dir, fn)
        try:
            with open(p, "r", encoding="utf-8") as f:
                for ln in f:
                    ln = ln.strip()
                    if not ln:
                        continue
                    try:
                        all_rows.append(json.loads(ln))
                    except Exception:
                        continue
        except Exception:
            continue
    if not all_rows:
        print("(no eval rows)")
        return
    # Overall
    print(f"# 策略统计（近 {days} 天，覆盖 {len(files)} 个交易日）\n")
    _print_stats_block("总体", all_rows)
    # By strategy
    for strat in ("A", "B"):
        subset = [r for r in all_rows if r.get("strategy") == strat]
        if subset:
            _print_stats_block(f"策略 {strat}", subset)
    # By LHB tag bucket
    print("\n## 按龙虎榜标签\n")
    print("| 标签 | 样本 | 胜率 | 止盈率 | 止损率 | 平均收益% |")
    print("|---|---:|---:|---:|---:|---:|")
    tags = {}
    for r in all_rows:
        t = r.get("lhb_tag") or "-"
        tags.setdefault(t, []).append(r)
    for t in sorted(tags, key=lambda k: -len(tags[k])):
        s = _compute_stats(tags[t])
        print(f"| {t} | {s['tot']} | {s['winrate']:.1f}% "
              f"| {s['sp_rate']:.1f}% | {s['sl_rate']:.1f}% | {s['avg']:+.2f} |")
    # By streak (first vs second board)
    print("\n## 按连板高度\n")
    print("| 连板 | 样本 | 胜率 | 止盈率 | 止损率 | 平均收益% |")
    print("|---:|---:|---:|---:|---:|---:|")
    streaks = {}
    for r in all_rows:
        st = r.get("seal_streak") or 0
        streaks.setdefault(st, []).append(r)
    for st in sorted(streaks):
        s = _compute_stats(streaks[st])
        print(f"| {st} | {s['tot']} | {s['winrate']:.1f}% "
              f"| {s['sp_rate']:.1f}% | {s['sl_rate']:.1f}% | {s['avg']:+.2f} |")


def _compute_stats(rows):
    """Shared aggregator -- total, winrate%, stop-profit rate%, stop-loss rate%, avg return%."""
    tot = len(rows)
    if tot == 0:
        return {"tot": 0, "winrate": 0, "sp_rate": 0, "sl_rate": 0, "avg": 0}
    sp = sum(1 for r in rows if r.get("outcome") == "stop_profit")
    sl = sum(1 for r in rows
             if r.get("outcome") in ("stop_loss", "both_stop_loss_assumed"))
    wins = sp + sum(1 for r in rows
                    if r.get("outcome") == "close" and (r.get("return_pct") or 0) > 0)
    avg = sum(r.get("return_pct", 0) or 0 for r in rows) / tot
    return {
        "tot": tot, "winrate": wins / tot * 100,
        "sp_rate": sp / tot * 100, "sl_rate": sl / tot * 100, "avg": avg,
    }


def _print_stats_block(title, rows):
    s = _compute_stats(rows)
    print(f"## {title}\n")
    print(f"- 样本：{s['tot']}")
    print(f"- 胜率：**{s['winrate']:.1f}%**")
    print(f"- 止盈率：{s['sp_rate']:.1f}%  |  止损率：{s['sl_rate']:.1f}%")
    print(f"- 平均收益：**{s['avg']:+.2f}%**\n")


# ==========================================================================
# Output formatters (markdown)
# ==========================================================================

def print_market():
    items = get_market_overview()
    if not items:
        print("(no data)")
        return
    # Trading-day warning header
    is_trading, reason = is_trading_day_probe()
    now = datetime.datetime.now()
    if not is_trading:
        print(f"⚠️ 非交易时段：{reason}")
    if now.weekday() == 4:
        print("⚠️ 今日周五：隔日持仓需过双休日，消息面风险放大")
    print("# 大盘指数")
    print("| 指数 | 现值 | 涨跌% | 涨跌点 | 成交额 |")
    print("|---|---:|---:|---:|---:|")
    for i in items:
        tag = "🟢" if i["pct"] >= 0 else "🔴"
        print(f"| {i['name']} | {i['price']} | {tag} {i['pct']:+.2f}% "
              f"| {i['change']:+.2f} | {_fmt_amount(i['amount'])} |")
    sh = next((x for x in items if x["name"] == "上证指数"), None)
    if sh and sh["pct"] < -2:
        print("\n⚠️ 上证跌幅 > 2%，建议空仓观望。")
    elif sh and sh["pct"] < -1:
        print("\n⚠️ 上证跌幅 > 1%，策略 A 仅选强势热门板块。")


def print_sector_rank(sector_type="industry", top=20):
    rows = get_sector_rank(sector_type, top=top)
    if not rows:
        print("(no data)")
        return
    name = {"industry": "行业", "concept": "概念", "region": "地域"}.get(sector_type, sector_type)
    print(f"# {name}板块榜 Top{top}")
    print("| # | 板块 | 涨跌% | 主力净流入 | 上涨 | 下跌 | 领涨股 | 领涨% |")
    print("|---:|---|---:|---:|---:|---:|---|---:|")
    for i, r in enumerate(rows, 1):
        print(f"| {i} | {r['name']} | {r['pct']:+.2f} | {_fmt_amount(r['main_inflow'])} "
              f"| {int(r['up_count'])} | {int(r['down_count'])} | {r['leader_name']} "
              f"| {r['leader_pct']:+.2f} |")


def print_pool(kind, date=None):
    title = {"zt": "涨停池", "dt": "跌停池", "zb": "炸板池", "lb": "连板池"}[kind]
    rows = get_pool(kind, date=date)
    if not rows:
        print(f"(empty {title})")
        return
    print(f"# {title} ({date or _today()}) 合计 {len(rows)}")
    print("| # | 代码 | 名称 | 现价 | 涨跌% | 连板 | 首封 | 最后封 | 封单 | 换手% | 成交额 | 行业 |")
    print("|---:|---|---|---:|---:|---:|---|---|---:|---:|---:|---|")
    for i, r in enumerate(rows, 1):
        print(f"| {i} | {r['code']} | {r['name']} | {r['price']} | {r['pct']:+.2f} "
              f"| {r['streak']} | {r['first_seal']} | {r['last_seal']} "
              f"| {_fmt_amount(r['seal_fund'])} | {r['turnover']:.1f} "
              f"| {_fmt_amount(r['amount'])} | {r['sector']} |")


def print_screen(cands, title):
    if not cands:
        print(f"(empty {title})")
        return
    print(f"# {title} 合计 {len(cands)}")
    print("| # | 代码 | 名称 | 现价 | 涨跌% | 换手% | 量比 | 流通市值 | 主力净流入 | 行业 | 备注 |")
    print("|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|")
    for i, c in enumerate(cands, 1):
        notes = []
        if c.get("strategy") == "A":
            notes.append(f"前{c.get('seal_ago', 0)}日{c.get('seal_streak', 1)}板")
        if c.get("strategy") == "B":
            notes.append(f"前{c.get('dt_ago', 0)}日跌停")
        note = "; ".join(notes)
        print(f"| {i} | {c['code']} | {c['name']} | {c['price']} | {c['pct']:+.2f} "
              f"| {c['turnover']:.1f} | {c['volume_ratio']:.2f} "
              f"| {_fmt_amount(c['float_mv'])} | {_fmt_amount(c['main_inflow'])} "
              f"| {c['industry']} | {note} |")


def print_score(cands):
    if not cands:
        print("(no candidates)")
        return
    print(f"# 打分结果 Top{len(cands)}")
    print("| # | 代码 | 名称 | 策略 | 得分 | 现价 | 涨跌% | 换手% | 量比 | 行业 |")
    print("|---:|---|---|:---:|---:|---:|---:|---:|---:|---|")
    for i, c in enumerate(cands, 1):
        print(f"| {i} | {c['code']} | {c['name']} | {c.get('strategy', '-')} "
              f"| {c.get('score', 0)} | {c['price']} | {c['pct']:+.2f} "
              f"| {c['turnover']:.1f} | {c['volume_ratio']:.2f} | {c['industry']} |")


def _print_next_step_block(results, meta):
    """Progressive-disclosure NEXT_STEP section (C/D/E oriented).

    Printed at the TOP of recommend/brief output so downstream truncation
    (agent prompt cap / logcat single-line cut) cannot strip the TASK
    instructions. The block is machine-parseable tagged text for the LLM.

    Redesigned 2026-04-22 for strategies C (laggard) / D (accumulation) /
    E (box breakout). A/B-specific minute-K pattern matrices, LHB hints,
    unlock warnings are all retired with the strategies themselves.
    """
    if not results:
        # Empty-candidate branch: auto-terminate with funnel breakdown.
        f = meta.get("funnel", {})
        c_cnt = f.get("strategy_C", 0)
        d_cnt = f.get("strategy_D", 0)
        e_cnt = f.get("strategy_E", 0)
        f2_cnt = f.get("strategy_F2", 0)
        c_review = meta.get("c_pool_review") or {}
        d_review = meta.get("d_pool_review") or {}
        e_review = meta.get("e_pool_review") or {}
        f2_review = meta.get("f2_pool_review") or {}

        sep_empty = "=" * 72
        print(sep_empty)
        print("⚠️ 本次候选 0 只 — 按纪律今日空仓")
        print(sep_empty)
        print()
        print("[Python] 漏斗统计 (每阶段过滤结果):")
        print(f"  策略C（热门板块滞涨股）: 通过 {c_cnt} 只")
        if c_review:
            hot_n = c_review.get("hot_sectors", 0)
            names = c_review.get("hot_sector_names") or []
            pcts = c_review.get("hot_sector_pcts") or []
            if hot_n:
                hint = ", ".join(
                    f"{n}({p:+.1f}%)" for n, p in zip(names, pcts)
                ) or "-"
                print(f"    热门板块 Top{hot_n}: {hint}")
            else:
                print(f"    无热门板块可用（板块接口失败或全市场弱势）")
        c_drops = f.get("C_stage1_drops") or {}
        if c_drops:
            print(f"    Stage1 裁掉分布: {dict(c_drops)}")
        print(f"  策略D（多日主力资金累积）: 通过 {d_cnt} 只")
        if d_review:
            uni = d_review.get("universe", 0)
            aff = d_review.get("after_flow_filter", 0)
            rnk = d_review.get("after_flow_rank", 0)
            print(f"    全市场 {uni} 只 → 5日净流入>0 {aff} 只 → 流入占比 Top30% {rnk} 只")
        d_drops = f.get("D_stage1_drops") or {}
        if d_drops:
            print(f"    Stage1 裁掉分布: {dict(d_drops)}")
        print(f"  策略E（60日箱体突破）: 通过 {e_cnt} 只")
        if e_review:
            uni = e_review.get("universe", 0)
            s1 = e_review.get("stage1", 0)
            print(f"    全市场 {uni} 只 → Stage1(量能+流动性等) {s1} 只 → 窄箱突破 {e_cnt} 只")
        e_drops = f.get("E_stage1_drops") or {}
        if e_drops:
            print(f"    Stage1 裁掉分布: {dict(e_drops)}")
        # F1 funnel (low-vol consolidation + first breakout)
        if "strategy_F1" in f:
            f1_cnt = f.get("strategy_F1", 0)
            f1_review = meta.get("f1_pool_review") or {}
            print(f"  策略F1（缩量横盘+首日突破）: 通过 {f1_cnt} 只")
            if f1_review:
                uni = f1_review.get("universe", 0)
                s1 = f1_review.get("after_stage1", 0)
                print(f"    全市场 {uni} 只 → Stage1(量价+流动性) {s1} 只 → "
                      f"盘整突破 {f1_cnt} 只")
            f1_drops = f.get("F1_stage1_drops") or {}
            if f1_drops:
                print(f"    Stage1 裁掉分布: {dict(f1_drops)}")
        # F3 funnel (sector kickoff)
        if "strategy_F3" in f:
            f3_cnt = f.get("strategy_F3", 0)
            f3_review = meta.get("f3_pool_review") or {}
            print(f"  策略F3（板块异动初动）: 通过 {f3_cnt} 只")
            if f3_review:
                new_hot = f3_review.get("new_hot", 0)
                names = f3_review.get("new_hot_names") or []
                print(f"    新热板块 {new_hot} 个 ({', '.join(names[:5])}) → "
                      f"成员 {f3_cnt} 只")
            f3_drops = f.get("F3_stage1_drops") or {}
            if f3_drops:
                print(f"    Stage1 裁掉分布: {dict(f3_drops)}")
        # F2 funnel (silent accumulation -- anti-D pattern)
        if "strategy_F2" in f:
            print(f"  策略F2（主力悄悄吸筹）: 通过 {f2_cnt} 只")
            if f2_review:
                uni = f2_review.get("universe", 0)
                s1 = f2_review.get("after_stage1", 0)
                print(f"    池 {uni} 只 → Stage1(流入≥1000万+5d≤±4%) {s1} 只 → "
                      f"全条件 {f2_cnt} 只")
            f2_drops = f.get("F2_stage1_drops") or {}
            if f2_drops:
                print(f"    Stage1 裁掉分布: {dict(f2_drops)}")
        # Data-quality block: when one or more Stage1 sources ran on
        # fallback, the 0-candidate outcome may be a false negative
        # (data layer suppressed a real candidate, not real market
        # weakness). Tell the LLM to call this out explicitly.
        dq = meta.get("data_quality") or {}
        if dq:
            print()
            print("[DATA_QUALITY] 本次 Stage1 数据源降级清单（可能导致 0 候选偏假阴性）:")
            for key in ("strategy_C_sector_kline",
                        "strategy_D_multiday_flow",
                        "strategy_E_universe"):
                if key in dq:
                    info = dq[key]
                    print(f"  - {key}: {info.get('note', '')}")
        print()
        print("[LLM_TASK] 立即 terminate success（不 ask_user / 不自行放宽），")
        print("  terminate 的 text 必须包含:")
        print("  (1) 结论: 按策略纪律今日 0 候选，空仓终止不建仓")
        print("  (2) 原因: 引用上面 [Python] 漏斗统计各阶段数字")
        if dq:
            print("  (2.5) 数据源说明: 引用上面 [DATA_QUALITY] 条目，明确告知用户"
                  "\"本次 X 个策略 Stage1 走了 fallback 路径，0 候选可能偏保守\"")
        print("  (3) 扩大池方法（如用户要求）:")
        print("      · --market main→all 包含创业板/科创板")
        print("      · --strategy 单独跑某一个引擎（如 C / D / E 三选一）排查")
        print(sep_empty)
        print()
        return
    advisory = bool(meta.get("advisory_avoid"))
    rej_cnt = meta.get("reject_count_top10", 0)
    top5 = meta.get("top5_sectors") or []
    mctx = meta.get("market_ctx") or {}
    sh_p = mctx.get("sh_pct")
    gem_p = mctx.get("gem_pct")

    pass_list = [c for c in results if not (c.get("reject_reasons") or [])]
    # Picks that fired hard-reject tags during _apply_llm_hints are now
    # filtered out of `final` (recommend step 6.6) so they no longer pollute
    # the recommendation table. They are still surfaced here via
    # meta["rejected_picks"] so the agent can audit *why* a strong-score
    # candidate was dropped without scrolling into the verbose log.
    reject_list = [c for c in results if (c.get("reject_reasons") or [])]
    reject_list = reject_list + list(meta.get("rejected_picks") or [])

    # Stable re-rank: higher boost count first, then existing score.
    pass_list.sort(key=lambda c: (-len(c.get("boost_reasons") or []),
                                   -(c.get("score") or 0)))
    pass_top_n = pass_list[:10]

    has_warn_bad_news = any(
        any(str(w).startswith("bad_news") for w in (c.get("soft_warnings") or []))
        for c in pass_top_n
    )

    # Resolve run-time / data snapshot date for [STATE] anchor so LLM cannot
    # invent dates on weekends / holidays.
    _now = datetime.datetime.now()
    _is_trading, _nt_reason = is_trading_day_probe()
    _wd_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][_now.weekday()]
    if not _is_trading:
        _session_tag = f"非交易日({_nt_reason})"
    else:
        _hm = _now.hour * 100 + _now.minute
        if _hm < 915:
            _session_tag = "盘前"
        elif _hm < 930:
            _session_tag = "集合竞价"
        elif _hm < 1500:
            _session_tag = "盘中"
        else:
            _session_tag = "盘后"
    _run_at_str = f"{_now.strftime('%Y-%m-%d %H:%M')} {_wd_cn} ({_session_tag})"
    if _is_trading and (_now.hour * 100 + _now.minute) >= 930:
        _data_date_str = _now.strftime("%Y-%m-%d") + " (日内/盘中快照)"
    else:
        try:
            _t1 = _trading_date_offset(1)
            if _t1 and len(_t1) == 8:
                _data_date_str = f"{_t1[:4]}-{_t1[4:6]}-{_t1[6:]} (上一交易日收盘)"
            else:
                _data_date_str = "上一交易日收盘 (日历查询失败)"
        except Exception:
            _data_date_str = "上一交易日收盘"

    sep = "═" * 72

    # ----- Hard short-circuit: intraday-strict data quality critical -----
    # When live upstream failed during continuous-trading hours and stale
    # cache was refused (intraday-strict policy, see `_maybe_stale_cache`),
    # the candidate set may be silently incomplete or stitched with stale
    # rows -- absolutely DO NOT let the LLM treat it as actionable. Replace
    # the entire NEXT_STEP block with a terminate-only banner so the agent
    # cannot fall back into PICK_BUY flow on corrupted data.
    if meta.get("data_quality_critical"):
        denials = (meta.get("data_quality") or {}).get("intraday_stale_denied") or []
        print(sep)
        print("## NEXT_STEP  (LLM 只看本块)")
        print(sep)
        print("\n[STATE]")
        print(f"run_at: {_run_at_str}")
        print(f"data_date: {_data_date_str}")
        print("data_quality: 🛑 critical_intraday_stale_denied   "
              "# 盘中实时数据失败，已拒绝使用昨日 cache（避免 T+1 决策被污染）")
        print("should_terminate: true                       "
              "# 数据不可信，禁止入场")
        print("session_not_for_entry: true                  "
              "# Agent 不得进 PICK_BUY 下单流程")
        sh_s = f"{sh_p:+.2f}%" if sh_p is not None else "n/a"
        gem_s = f"{gem_p:+.2f}%" if gem_p is not None else "n/a"
        print(f"market: 上证 {sh_s} | 创业板 {gem_s}")

        print("\n[DATA_FAIL] 盘中拒绝 stale cache 的数据层清单:")
        for d in denials:
            print(f"  - layer={d.get('layer','?')} "
                  f"key={d.get('key','?')} "
                  f"err={d.get('error','?')} ts={d.get('ts','?')}")

        print("\n[TASK]  必须先 ask_user 告知数据失败情况，由用户决定下一步")
        print("        （**禁止静默 terminate / 禁止照旧入场 / 禁止用昨日数据替代**）:")
        print()
        print("  Step-1: 调用 ask_user，message 模板（按当前数据填充 <…> 占位）:")
        print("  ┌─────────────────────────────────────────────────────────┐")
        print("  │ ⚠️ 盘中实时行情接口失败                                  │")
        print("  │ 受影响数据层：<引用 [DATA_FAIL] 的 layer 列表>          │")
        print("  │ 当前时间：<引用 [STATE].run_at>                         │")
        print("  │                                                          │")
        print("  │ 已**拒绝使用昨日 cache 数据**避免对今日 T+1 决策造成污染。│")
        print("  │ 请选择：                                                │")
        print("  │   N - 立即终止本次任务（推荐，等接口恢复后重新发起）     │")
        print("  │   <数字> - 等待该分钟数后**自动重试 1 次**（如 5 = 5min）│")
        print("  │   IGNORE - 知情同意：仅做分析不下单（PICK_BUY 任务勿选） │")
        print("  └─────────────────────────────────────────────────────────┘")
        print()
        print("  Step-2: 按用户回复执行:")
        print("    · 'N' / 'no' / '终止' / 空回复 → terminate success")
        print("      text: 引用 [DATA_FAIL] 受影响层 + 建议（重试时点 / 切 WiFi / 关 VPN）")
        print("    · 数字 N → wait(N*60) → 重发本命令（python stockquant.py --capital ... ）")
        print("      若重试仍 critical: 再次 ask_user，**最多重试 2 次**后强制 terminate")
        print("    · 'IGNORE' → 仅 PICK_ANALYZE 类任务可选；PICK_BUY 必须强制按 'N' 处理")
        print(sep)
        return                                             # short-circuit
    # ----- (end of critical short-circuit) -----

    print(sep)
    print("## NEXT_STEP  (LLM 只看本块；下方漏斗/表格是给人看的，跳过)")
    print(sep)

    # ----- [ROUTE_HINT] -----
    print("\n[ROUTE_HINT] (to model router / deployment layer — not a data field)")
    print("difficulty: HIGH")
    print("reasoning_required: STRONG")
    print("thinking_budget: enable_thinking=TRUE (prefer reasoning/thinking/o1-style/R1-class models)")
    print("task_nature: 多引擎候选交叉评估 + 风险复核 + 结构化推荐撰写 (1200~2000 字)")
    print("subtasks:")
    print("  (a) PASS_TOP10 × 3 条硬约束 matrix 复核 (S1)")
    print("  (b) PASS_TOP10 × 策略 boost 标签评分 (S2)")
    print("  (c) Top5 综合排序 + 风险复核 + 首选/次选/备选档次 (S3)")
    print("  (d) 逐只 4~6 行 stock-specific 核心逻辑/风险/概率 bullets (S4)")
    print("  (e) 操作建议 Markdown 表 + 纪律声明 (S5~S6)")
    print("routing_directive: 若路由系统按 prompt 内容分级, 请将本轮切至最强推理模型;")
    print("                   若 LLM 本身, 必须进入深度思考 (chain-of-thought) 模式,")
    print("                   禁止 quick-draft / 只抄字段 / 简写式输出.")

    # ----- [TASK_TLDR] -----
    # Minimum contract surfaced at TOP — even if [TASK] is truncated
    # downstream, the LLM still sees these 3 non-negotiable rules.
    print("\n[TASK_TLDR] (3 条硬规则, 必须遵守)")
    print("  🚫 禁止跳过推理直接 terminate — 必须先完成 S0→S6 完整流程")
    print("  ✅ 顺序: S0(宏观)→S1(硬约束表)→S2(boost表)→S2.5(风险复核)→S3(Top5)→S4(逐只)→S5(allocate)→S6(声明)")
    print("  ⚠ 数据降级必须先 ask_user, 禁止静默继续")

    # ----- [STATE] -----
    _session_no_entry = False
    _no_entry_reason = ""
    if _is_trading:
        _hm = _now.hour * 100 + _now.minute
        if 1030 <= _hm < 1130:
            _session_no_entry = True
            _no_entry_reason = "10:30~11:30 上午中段（已过首小时价格发现）"
        elif 1130 <= _hm < 1300:
            _session_no_entry = True
            _no_entry_reason = "11:30~13:00 午休（pct 快照失真）"
        elif 1300 <= _hm < 1330:
            _session_no_entry = True
            _no_entry_reason = "13:00~13:30 下午开盘前半段（方向未定）"
    print("\n[STATE]")
    print(f"run_at: {_run_at_str}")
    print(f"data_date: {_data_date_str}")
    # Expose capital so S5 C-path reallocation can reference [STATE].capital
    # instead of re-deriving it from text prose.
    _capital = meta.get("capital")
    if _capital is not None:
        print(f"capital: {_capital:.0f}   # 总资金 (元), 按 10000元/只 规则分配")
    if _session_no_entry:
        print(f"should_terminate: true    # 盘时不宜入场: {_no_entry_reason}")
        print(f"session_not_for_entry: true   # Agent 不应进 PICK_BUY 下单流程，仅输出分析")
    elif advisory:
        print(f"should_terminate: true    # Top10 命中 HARD reject {rej_cnt}/10，结构普遍偏弱")
    else:
        print(f"should_terminate: false   # HARD reject {rej_cnt}/10 通过")
    sh_s = f"{sh_p:+.2f}%" if sh_p is not None else "n/a"
    gem_s = f"{gem_p:+.2f}%" if gem_p is not None else "n/a"
    print(f"market: 上证 {sh_s} | 创业板 {gem_s}")
    _macro = (meta or {}).get("market") or {}
    _mtd = _macro.get("market_trend_delta")
    if _mtd is not None:
        _worst_pct = _macro.get("worst_pct")
        _worst_s = f"{_worst_pct:+.2f}%" if _worst_pct is not None else "n/a"
        print(f"market_trend_factor: worst={_worst_s} → C/D/E 统一 {_mtd:+d}   # 已计入 score；板块相对强弱±5 + 资金×大盘±3 按票叠加")
    print(f"top5_sectors: {', '.join(top5) if top5 else '(无数据)'}")

    # ----- [DATA] PASS_TOP10 -----
    print("\n[DATA] PASS_TOP10 (已按 boost+score 重排；做 matrix/精选从这里面挑)")
    print("  legend: 🟢 PICK (boost≥2 + prob=high + 无 soft_warnings) "
          "| 🟡 RISK (任 1 项 soft_warning 或 prob=mid) "
          "| 🔴 AVOID (prob=low 或 含 bad_news; 必须在 S2.5 标 HIGH 风险)")
    if not pass_top_n:
        print("  (无通过候选)")
    else:
        for idx, c in enumerate(pass_top_n, 1):
            b = c.get("boost_reasons") or []
            w = c.get("soft_warnings") or []
            b_str = ",".join(b) if b else "-"
            w_str = ",".join(w) if w else ""
            prob = c.get("next_day_prob") or "-"
            warn_seg = f" warn={w_str}" if w_str else ""
            price = c.get("price") or 0
            stop = c.get("stop_loss") or 0
            alloc = int(round(c.get("cost") or 0))
            pct = c.get("pct")
            pct_s = f"{pct:+.2f}%" if pct is not None else "n/a"
            turnover = c.get("turnover")
            tov_s = f"{turnover:.1f}%" if turnover is not None else "n/a"
            vr = c.get("volume_ratio")
            vr_s = f"{vr:.2f}" if vr is not None else "-"
            dist_ma20 = c.get("distance_from_ma20")
            ma_s = f"{dist_ma20:+.1f}%" if dist_ma20 is not None else "-"
            news_hit = any(str(x).startswith("bad_news:") for x in w)
            news_flag = "warn" if news_hit else "ok"
            st_flag = 1 if _is_risky_name(c.get("name")) else 0
            strat = c.get("strategy") or "?"
            # ----- Visual three-state tag ------------------------------------
            # Encodes the three "risk gates" of the pipeline into a single
            # leftmost glyph that the LLM can match by sight:
            #   🟢 = clean (LLM may accept directly into Top5 ordering)
            #   🟡 = caution (LLM must elaborate risk in S2.5)
            #   🔴 = strongly avoid (LLM must mark HIGH in S2.5; cannot enter Top5)
            # Note: 🔴 candidates are NOT fully filtered out at the Python
            # level because some soft signals (e.g. ST-name + prob=low) are
            # too aggressive to hard-reject without context; we surface the
            # warning visually and rely on S2.5 to enforce.
            if prob == "low" or news_hit or st_flag == 1:
                tag = "🔴"
            elif w or prob == "mid":
                tag = "🟡"
            elif len(b) >= 2 and prob == "high":
                tag = "🟢"
            else:
                tag = "🟡"                                 # default conservative
            # Strategy-specific compact fields
            if strat == "C":
                ext = (f"sector_pct={c.get('sector_n_day_pct', '-')}% "
                       f"laggard_gap={c.get('laggard_gap', '-')}")
            elif strat == "D":
                mp5 = c.get("main_inflow_pct_5d")
                mi5 = c.get("main_inflow_5d") or 0
                mi5_yi = mi5 / 1e8
                aligned = c.get("ma_aligned")
                aligned_s = "yes" if aligned is True else ("no" if aligned is False else "-")
                ext = (f"flow5d={mi5_yi:.2f}亿 "
                       f"flow_pct5d={mp5 if mp5 is not None else '-'}% "
                       f"ma_aligned={aligned_s}")
            elif strat == "E":
                ext = (f"box_range={c.get('box_range_pct', '-')}% "
                       f"box_pos={c.get('box_position_pct', '-')}%")
            else:
                ext = "-"
            print(f"  {tag} {idx:>2}. {c['code']} {c['name']:<6} "
                  f"strategy={strat} news={news_flag} st={st_flag}  "
                  f"price={price} stop={stop} alloc={alloc}元  "
                  f"score={c.get('score', 0):>3} pct={pct_s} tov={tov_s} vr={vr_s} ma20={ma_s} "
                  f"{ext} sector={c.get('industry', '-')} "
                  f"prob={prob} boost={b_str}{warn_seg}")
    if reject_list:
        print(f"\n[DATA] REJECT_LIST ({len(reject_list)} 只, 已剔除, 不在 PASS 中):")
        for c in reject_list:
            r = ",".join(c.get("reject_reasons") or [])
            print(f"  × {c['code']} {c['name']} reason={r}")

    # ----- [DATA_QUALITY] multi-source merge results (progressive disclosure) -----
    # Printed only when at least one candidate has a `_data_quality` block
    # (always True post block-B integration, but the helper bails on legacy
    # results without the field). The legend is one-shot per recommend run
    # so the LLM doesn't have to reason about the format from scratch.
    cands_with_dq = [c for c in pass_top_n if c.get("_data_quality")]
    if cands_with_dq:
        # Aggregate stats
        ms_meta = meta.get("multi_source_merge") or {}
        n_enriched = ms_meta.get("candidates_enriched", len(cands_with_dq))
        n_conflicts = ms_meta.get("field_conflicts", 0)
        # Per-candidate conflict / single-source enumeration
        conflict_rows = []
        single_src_rows = []
        for c in cands_with_dq:
            dq = c.get("_data_quality") or {}
            conflicts_here = []
            singles_here = []
            for f, m in dq.items():
                if m.get("conflict"):
                    conflicts_here.append((f, m))
                elif m.get("single_source"):
                    # Only flag CRITICAL single-source fields; price/pct are
                    # universal so single-source is uninteresting noise.
                    if f in ("main_inflow_1d", "main_inflow_5d", "turnover",
                             "industry"):
                        singles_here.append((f, m))
            if conflicts_here:
                conflict_rows.append((c, conflicts_here))
            if singles_here:
                single_src_rows.append((c, singles_here))

        print(f"\n[DATA_QUALITY] 多源交叉验证 (top-{len(pass_top_n)} 候选, "
              f"已 enrich={n_enriched}, 字段冲突={n_conflicts})")
        print("  legend:")
        print("    · ✅ all-source-agree    所有源对该字段达成一致(spread<阈值或类别等价)")
        print("    · ⚠️ CONFLICT           多源同字段差异>阈值, 取 priority 最高源为 canonical;")
        print("                            LLM 应**降级置信度** + 文中明确告知用户")
        print("    · 🟡 SINGLE_SOURCE      仅 1 源提供该字段(无法交叉验证);")
        print("                            LLM 应在文中标注\"未交叉验证\" 但不必否决")
        print("  field 含义: price/pct/turnover 为实时价量, main_inflow_5d 为 5 日累计主力净流入,")
        print("            industry 为行业归属(白酒≡饮料制造等别名已自动归一)")
        print("  conflict 阈值: price=0.5% / pct=5pp / 资金流=30% / 类别=非别名差异")

        if conflict_rows:
            print(f"\n  [CONFLICT_DETAIL] {len(conflict_rows)} 只候选有字段冲突:")
            for c, items in conflict_rows:
                print(f"    ⚠️ {c['code']} {c['name']}:")
                for f, m in items:
                    vals_str = ", ".join(
                        f"{src}={v}" for src, v in m.get("values", {}).items()
                    )
                    sp = m.get("spread_pct")
                    sp_str = (f"spread={sp:.1f}%" if sp is not None
                              else "category-mismatch")
                    print(f"        {f}: canonical={m['value']} ({sp_str})")
                    print(f"            sources: {vals_str}")
                    if m.get("note"):
                        print(f"            note: {m['note']}")
        else:
            print("\n  [CONFLICT_DETAIL] (无冲突 - 所有源一致)")

        if single_src_rows:
            print(f"\n  [SINGLE_SOURCE_NOTES] 关键字段仅来自单一源(LLM 文中需标注):")
            for c, items in single_src_rows[:10]:               # cap noise
                fields_str = ", ".join(
                    f"{f}={m['sources'][0] if m.get('sources') else '?'}"
                    for f, m in items
                )
                print(f"    🟡 {c['code']} {c['name']}: {fields_str}")
            if len(single_src_rows) > 10:
                print(f"    ... ({len(single_src_rows) - 10} 只省略)")

        print("  [LLM_ACTION]")
        print("    · 撰写 S4 个股 bullets 时, 对有 CONFLICT 标记的字段:")
        print("       (1) 先列 canonical 值; (2) 一行点出 \"⚠️ 多源差异(具体数值)\";")
        print("       (3) 概率/置信度档位下调一级(high→mid, mid→low)")
        print("    · 对 SINGLE_SOURCE 关键字段(资金流/换手率/行业): 仅在 S4 末段标注")
        print("       \"<字段>由 <源> 单源提供\", 不影响档位但读者需知情")
        print("    · 若同一候选 ≥3 字段冲突: 移入备选档(不进首选/次选), 并在 S3 风险复核")
        print("       明确说明 \"数据源分歧严重, 建议等数据稳定再入场\"")

    # ----- [ALLOCATION] actionable buy list (LLM should quote verbatim in S5) -----
    # This mirrors meta["allocation_plan"] but rendered as compact key=value
    # lines so the LLM sees the exact shares/cost/stops next to PASS_TOP10.
    alloc = meta.get("allocation_plan") or {}
    alloc_items = alloc.get("items") or []
    if alloc_items:
        print(f"\n[ALLOCATION] BUY_PLAN "
              f"(target={alloc.get('per_target', 10000):.0f}元/只, "
              f"used={alloc.get('used', 0):.0f}元, "
              f"remaining_cash={alloc.get('remaining_cash', 0):.0f}元)")
        for it in alloc_items:
            print(f"  #{it['rank']:<2} {it['code']} {it['name']:<6} "
                  f"strategy={it['strategy']} price={it['price']} "
                  f"shares={it['shares']} cost={it['cost']:.0f}元 "
                  f"pct={it['pct_of_capital']}% cum_pct={it['cum_pct']}% "
                  f"stop_profit={it.get('stop_profit', '-')} "
                  f"stop_loss={it.get('stop_loss', '-')} "
                  f"sector={it.get('industry', '-')} "
                  f"prob={it.get('prob', '-')}")
        alloc_skipped = alloc.get("skipped") or []
        if alloc_skipped:
            print(f"  skipped={len(alloc_skipped)} "
                  f"(reasons: 单手>半仓 或 剩余资金不足)")

    # ----- [TASK] -----
    print("\n[TASK] 严格按 S0→S6 顺序输出完整分析报告 (预期 1200~2000 字):")

    # Soft data-quality gate: when one or more strategies ran on a fallback
    # source (sector_kline / multiday_flow / split_universe degraded), we
    # MUST surface this to the user up-front so they can choose to abort,
    # not silently produce an analysis that may be missing a whole signal
    # axis. Critical (intraday-strict) cases are handled in the short-
    # circuit branch above; here we handle the "degraded but still has
    # candidates" case.
    _dq_soft = meta.get("data_quality") or {}
    # Drop the intraday_stale_denied subkey (already covered upstream)
    _dq_soft_layers = sorted(
        k for k in _dq_soft.keys() if k != "intraday_stale_denied"
    )
    if _dq_soft_layers:
        print()
        print("  S-1. 【数据降级告知（必须先 ask_user，禁止静默继续）】")
        print(f"       本次有 {len(_dq_soft_layers)} 个策略 Stage1 走了 fallback 路径:")
        for k in _dq_soft_layers:
            note = (_dq_soft.get(k) or {}).get("note", "")
            print(f"         - {k}: {note}")
        print("       调用 ask_user (message 模板):")
        print('         "⚠️ 本次选股有 N 项数据降级（{layers}），')
        print('          受影响信号: 主力资金/板块涨幅/E 策略覆盖度其中之一。')
        print('          继续分析可能漏判某些维度，是否仍要继续？')
        print('          Y = 继续按降级数据出报告（建议降仓位/降股数）')
        print('          N = 终止本次任务，等数据恢复后重发"')
        print("       根据回复:")
        print("         · 'Y'/'yes'/'继续' → 进入 S0；S5 allocate 时 --capital 改为原值的 60%")
        print("         · 'N'/'no'/'终止'/空 → terminate success，text 引用降级清单")

    print("  S0. ⚠ THINKING REQUIRED: 本轮为多步矩阵推理+排序+叙事复合任务, 禁止 quick-draft.")
    print("      · 必须先内部走一遍 S1~S6 的逻辑链, 再逐段输出 (chain-of-thought).")
    print("      · 禁止只抄 [DATA] 字段标签就拼凑结论; 每条 bullet 必须是 stock-specific 推理.")
    if advisory:
        print(f'  S1. show_output: "⚠️ Top10 HARD reject {rej_cnt}/10，结构普遍偏弱，建议空仓观望"')
        print("  S2. terminate")
    elif not pass_top_n:
        print('  S1. show_output: "本期无可选候选 (已被 Layer 4 过滤)"')
        print("  S2. terminate")
    else:
        print("  S0. 【宏观情绪确认】先读上方 [MACRO_SENTIMENT] 情绪得分:")
        print("      🔴≤-1: 收紧选股, 防御优先 | 🟡 0: 默认 | 🟢≥+1: 可略激进")
        print()
        print("  S1. 【硬约束复核】对 [DATA] PASS_TOP10 前 8 只输出表:")
        print("      | # | 代码 | 名称 | 过度延伸(ma20>+12%) | 恐慌量能(vr>5) | 大流出(<-1亿) | D追高(pct_5d>20) | 结论 |")
        print("      PASS 内所有票三项均已 Python 过滤 → 结论列写 ✅通过")
        print()
        print("  S2. 【优先上浮打分】对前 8 只逐票查 boost 标签:")
        print("      | # | 代码 | 名称 | 热门板块 | MA20支撑 | 均线多头 | 策略专属 | 合计 |")
        print("      热门板块=hot_sector | MA20支撑=at_ma20_support(|偏离|≤3%) | 均线多头=ma_bullish_alignment(仅D)")
        print("      策略专属: C=laggard_in_hot_sector | D=sustained_accumulation | E=tight_box_breakout")
        print()
        print("  S2.5 【🔒 风险复核 (必填)】对前 8 只输出表:")
        print("      | # | 代码 | 名称 | 策略 | 结构 | 消息面 | 风险 | LLM调整 | 理由 |")
        print("      结构按策略: C看sector_pct/laggard_gap | D看flow5d/flow_pct5d/ma_aligned | E看box_range/box_pos/vr")
        print("      消息面: news=warn→引用命中关键词 | news=ok→清爽")
        print("      | 风险 | 触发条件 | LLM调整 |")
        print("      | HIGH | bad_news / st=1 / late_entry / D:flow_pct5d<2 / E:box_pos<85 | -15~-10 |")
        print("      | MID  | tov>15 / sector_cooling / weak_accumulation / below_box_top | -8~-3 |")
        print("      | LOW  | 结构干净 + ≥2项boost | +3~+10 |")
        print("      🚫 禁同档化 / 禁漏LLM调整 / bad_news必HIGH")
        print()
        print("  S3. 【精选Top5】final_score = python_score + LLM调整, DESC排前5")
        print("      | 排名 | 代码 | 名称 | 策略 | python | LLM | final | 风险 | 入围理由 |")
        print("      🚫 禁直接抄score前5 / HIGH不进Top5 / 同sector≥3需轮换 / 必须明示公式")
        print()
        print("  S4. 【逐只分析】Top5每只4~6行bullet:")
        print("      ### N. 代码 名称 ★首选/次选/备选")
        print("      💡 核心逻辑(≥3条,按策略选): 板块热度 | 资金/滞涨/箱体(策略专属) | dist_ma20 | tov+vr | S2.5复核")
        print("      ⚠️ 风险提示(1~2条,stock-specific): 禁通用话术(破位即砍/注意风险)")
        print("      📊 冲高概率: 引用 [DATA] prob (high/mid/low)")
        if has_warn_bad_news:
            print("      ⚠ bad_news票: 明确写\"命中公告关键词XX,建议stock skill交叉验证\"")
        print()
        print("  S5. 【操作建议表】调用 Python allocate (禁手算):")
        print("      1) 整理S3 Top5代码为逗号列表")
        print("      2) 总结S1~S4核心推理为300~500字markdown(引用具体字段,禁通用话术)")
        print("      3) 执行: python stockquant.py allocate --codes C1,C2,... --capital [STATE].capital --comment \"...\"")
        print("      4) 把Python输出(comment+表+合计+跳过)原样写入,一字不改")
        print("      🚫 禁手算股数/资金 | 禁跳过allocate抄baseline | 禁通用comment")
        print()
        print("  S6. 【末尾声明】引用 [STATE].data_date / [STATE].run_at | 禁保证盈利 | 止盈+5% | 仓位≤alloc上限")
        print()
        print("  S7. 报告完成 → terminate success 汇报")

    print(sep)


def print_recommend(results, meta, capital, threshold):
    # Hard-gate abort short-circuit. When recommend() refused to run due
    # to tushare token state (unset / auth_failed), it already emitted a
    # structured HINT line on stdout. Skip the full NEXT_STEP / funnel /
    # table here so the agent's 20KB head budget is not wasted on
    # placeholder zeros and (more importantly) so the agent cannot
    # mistake a `# 推荐 Top0` block for a legitimate "no candidates today"
    # outcome -- which would invite premature `terminate success`.
    abort = meta.get("abort_reason")
    if abort:
        print()
        print("═══ ABORT_REQUIRED ═══")
        print(f"reason: {abort}")
        ts = meta.get("tushare") or {}
        print(f"tushare: tier={ts.get('tier')} info={ts.get('info')}")
        print("action: 见上方 HINT 行的 ask_user / example_set / example_skip "
              "字段，按渐进式披露指引调用 ask_user 让用户决定，"
              "不要 wait/sleep，不要默认 terminate。")
        print("══════════════════════")
        return
    # NEXT_STEP goes FIRST so it survives any downstream truncation
    # (agent prompt cap / logcat single-line cut). The human-facing
    # funnel/tables below are intentionally demoted.
    # ------ macro-sentiment: inject financial news context before stock-picking ------
    _render_macro_sentiment()
    _print_next_step_block(results, meta)
    # Announce verbose log path so the agent can read_file drill-down
    # detail on demand (Stage1 drops / alloc baseline / soft+boost
    # reasons live there, not stdout). Printed ONCE near the top so it
    # is never stripped by the agent's 20KB head truncation.
    if _VERBOSE_LOG_PATH:
        print()
        print(f"[VERBOSE_LOG_PATH] {_VERBOSE_LOG_PATH}")
        print("  drill-down detail (Stage1 drops / alloc baseline / soft_warnings / boost_reasons).")
        print("  read_file this path ONLY when you need to justify a specific pick or debug 0-candidate.")
    # Progressive-disclosure: emit a top-level HINT when the run yielded
    # 0 or <5 candidates. The agent must NOT auto-wait or sleep -- it
    # should ask_user using the example commands embedded in the HINT
    # JSON. Mirrors the shape of HINT: tushare_token_unset so the agent
    # parser sees a uniform contract across error paths.
    suff = meta.get("info_sufficiency")
    if suff in ("insufficient", "partial"):
        n = len(results)
        ts_tier = (meta.get("tushare") or {}).get("tier", "unset")
        token_path_unset = ts_tier in ("unset", "skipped", "auth_failed")
        if suff == "insufficient":
            ask = (f"本次未筛出任何候选 (final=0)。已尝试源："
                   f"EM/Sina/tushare(tier={ts_tier})。是否：(a) 提供 tushare token 解锁备用源 "
                   f"(b) 接受 0 候选并终止本轮 (c) 5-30 分钟后重试")
        else:
            ask = (f"本次仅筛出 {n} 只候选 (<5, 数据源降级)。是否：(a) 接受这 {n} 只继续走分配 "
                   f"(b) 提供 tushare token 重跑解锁更多候选 (c) 终止本轮")
        hint_obj = {
            "ask_user": ask,
            "candidates_count": n,
            "tushare_tier": ts_tier,
        }
        if token_path_unset:
            hint_obj["example_set_token"] = (
                "python ${SKILL_DIR}/stockquant/scripts/stockquant.py "
                "tushare-token --set <TOKEN>"
            )
            hint_obj["example_skip_token"] = (
                "python ${SKILL_DIR}/stockquant/scripts/stockquant.py "
                "tushare-token --skip"
            )
        hint_obj["after"] = "set/skip 后直接重跑原命令，或按用户答复 terminate；不要 sleep/wait"
        # Inline JSON (single-line) so logcat truncation cannot break parsing.
        import json as _json
        print()
        print(f"HINT: info_{suff} {_json.dumps(hint_obj, ensure_ascii=False)}")
    print()
    print(f"# 推荐 Top{len(results)}  资金={capital:.0f}  止盈门限={threshold}%")
    # Warnings first
    for w in meta.get("warnings", []):
        print(f"\n{w}")
    # Data-quality section: only printed when at least one strategy
    # Stage1 ran on a fallback/degraded source. Kept compact + action-
    # oriented so the LLM can cite specific degrade paths in terminate text.
    dq = meta.get("data_quality") or {}
    if dq:
        print("\n## [DATA_QUALITY] 本次运行数据源降级说明")
        for key in ("strategy_C_sector_kline",
                    "strategy_D_multiday_flow",
                    "strategy_E_universe"):
            if key in dq:
                info = dq[key]
                extra = ""
                if "degraded_sector_count" in info:
                    extra = f"（{info['degraded_sector_count']} 个板块）"
                print(f"- **{key}** [DEGRADED]{extra}：{info.get('note', '')}")
        print("- ⚠️ 提示：LLM 在 terminate text 或推荐说明里请明确提及"
              "\"部分数据源降级\"，避免误判为真正的 0 候选/弱候选。")
    # Funnel for strategies C/D/E
    f = meta.get("funnel", {})
    print("\n## 选股漏斗")
    print(f"- 热门板块识别：**{f.get('hot_sectors', 0)}** 个")
    if "strategy_C" in f:
        print(f"- 策略C（热门板块滞涨股）候选：**{f['strategy_C']}** 只")
        cdr = f.get("C_stage1_drops") or {}
        if cdr:
            # Drill-down distribution goes to verbose only; stdout keeps
            # the total-count summary which is enough for routine decisions.
            _v_or_print(f"    [C_stage1_drops] {dict(cdr)}")
    if "strategy_D" in f:
        print(f"- 策略D（多日主力累积）候选：**{f['strategy_D']}** 只")
        ddr = f.get("D_stage1_drops") or {}
        if ddr:
            _v_or_print(f"    [D_stage1_drops] {dict(ddr)}")
    if "strategy_E" in f:
        print(f"- 策略E（60日箱体突破）候选：**{f['strategy_E']}** 只")
        edr = f.get("E_stage1_drops") or {}
        if edr:
            _v_or_print(f"    [E_stage1_drops] {dict(edr)}")
    if "strategy_F1" in f:
        print(f"- 策略F1（缩量横盘+首日突破）候选：**{f['strategy_F1']}** 只")
        f1dr = f.get("F1_stage1_drops") or {}
        if f1dr:
            _v_or_print(f"    [F1_stage1_drops] {dict(f1dr)}")
    if "strategy_F2" in f:
        print(f"- 策略F2（主力悄悄吸筹）候选：**{f['strategy_F2']}** 只")
        f2dr = f.get("F2_stage1_drops") or {}
        if f2dr:
            _v_or_print(f"    [F2_stage1_drops] {dict(f2dr)}")
    if "strategy_F3" in f:
        print(f"- 策略F3（板块异动初动）候选：**{f['strategy_F3']}** 只")
        f3dr = f.get("F3_stage1_drops") or {}
        if f3dr:
            _v_or_print(f"    [F3_stage1_drops] {dict(f3dr)}")
    print(f"- 打分排序：**{f.get('scored', 0)}** 只")
    if "sector_diversified_dropped" in f:
        print(f"- 行业分散过滤剔除：{f['sector_diversified_dropped']} 只"
              f"（覆盖 {f.get('sectors_in_top', 0)} 个行业）")
    print(f"- 因价格 / 资金限制过滤：{f.get('skipped_for_price', 0)} 只")
    print(f"- **最终推荐：{f.get('final', 0)} 只**")

    if not results:
        print("\n(无符合条件的候选股。可能原因：非交易日 / 大盘环境不佳 / "
              "三引擎全部被过滤 / 价格超出资金范围。)")
        return
    print("\n## 最终推荐\n")
    print("| # | 代码 | 名称 | 策略 | 得分 | 现价 | 股数 | 资金 | 止盈 | 止损 "
          "| 涨跌% | 换手% | 量比 | MA20偏离 | 行业 | 策略指标 | 提示 |")
    print("|---:|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|")
    for i, c in enumerate(results, 1):
        strat = c.get("strategy", "-")
        # Per-strategy compact descriptor (right before the hint column)
        if strat == "C":
            sec_pct = c.get("sector_n_day_pct")
            gap = c.get("laggard_gap")
            note = (f"板块{sec_pct:+.1f}%，落后{gap}"
                    if sec_pct is not None and gap is not None else "-")
        elif strat == "D":
            mi5 = c.get("main_inflow_5d") or 0
            mp5 = c.get("main_inflow_pct_5d")
            aligned = c.get("ma_aligned")
            ma_s = "多头" if aligned is True else ("不齐" if aligned is False else "-")
            mp5_s = f"{mp5}%" if mp5 is not None else "-"
            note = f"5日流入{mi5/1e8:.2f}亿({mp5_s}) {ma_s}"
        elif strat == "E":
            br = c.get("box_range_pct")
            bp = c.get("box_position_pct")
            note = (f"箱幅{br}% 位置{bp}%"
                    if br is not None and bp is not None else "-")
        elif strat == "F1":
            p10 = c.get("pct_10d")
            amp = c.get("amplitude_60d_pct")
            note = (f"10日{p10:+.1f}% 60日振幅{amp}%"
                    if p10 is not None and amp is not None else "-")
        elif strat == "F2":
            in5 = c.get("main_inflow_5d") or 0
            rat = c.get("main_inflow_ratio_pct")
            p5 = c.get("pct_5d")
            note = (f"5d流入{in5/1e8:.2f}亿 占{rat}% 5d{p5:+.1f}%"
                    if rat is not None else "-")
        elif strat == "F3":
            sec = c.get("sector_name", "-")
            spt = c.get("sector_pct_today")
            mp5 = c.get("pct_5d")
            note = (f"板块{sec}今+{spt:.1f}% 自身5d{mp5:+.1f}%"
                    if spt is not None and mp5 is not None else "-")
        else:
            note = "-"
        vr = c.get("volume_ratio")
        vr_s = f"{vr:.2f}" if vr is not None else "-"
        dm = c.get("distance_from_ma20")
        dm_s = f"{dm:+.1f}%" if dm is not None else "-"
        rej = c.get("reject_reasons") or []
        warn = c.get("soft_warnings") or []
        bst = c.get("boost_reasons") or []
        prob = c.get("next_day_prob") or "-"
        # stdout: only decision-critical hints (reject_reasons + prob).
        # verbose: full soft_warnings/boost_reasons breakdown so the LLM
        # can justify a specific pick on demand via read_file.
        hint_parts = []
        if rej:
            hint_parts.append("🚫" + ",".join(rej))
        hint_parts.append(f"prob={prob}")
        hint_str = " ".join(hint_parts)
        if (warn or bst) and _VERBOSE_LOG_FH is not None:
            _vprint(f"[HINT_DETAIL] {c['code']} {c['name']}: "
                    f"warnings={warn} boosts={bst}")
        price = c.get("price") or 0
        pct = c.get("pct") or 0
        tov = c.get("turnover") or 0
        print(f"| {i} | {c['code']} | {c['name']} | {strat} | {c.get('score', 0)} "
              f"| {price} | {c.get('shares', 0)} | {c.get('cost', 0):.0f} "
              f"| {c.get('stop_profit', 0)} | {c.get('stop_loss', 0)} | {pct:+.2f} "
              f"| {tov:.1f} | {vr_s} | {dm_s} "
              f"| {c.get('industry', '-')} | {note} | {hint_str} |")

    # ----- Evidence / Pattern / Confidence card per pick -----
    # Per-pick: confidence + patterns + multi-directional signals.
    # Universal must_verify checks and devil_advocate questions are
    # surfaced ONCE as a global section (before per-stock) to avoid
    # repeating identical text N times.
    has_card = any(c.get("evidence_card") for c in results)
    if has_card:
        print("\n## 证据卡 / 形态 / 置信度 (每只必读)")

        # ----- Global pre-buy checks (apply to ALL candidates) -----
        print("\n### 🔍 买入前全局必验 (每只买入前均须确认)")
        print("- **分时量价背离**: 调用 fetch_minute_price_volume 看早盘量价配合；价涨量缩→放弃")
        print("- **大单异动**: 调用 fetch_big_order_flow 检查近30分钟大额抛单；连续>500万卖单→放弃")
        print("- **次日压力测试**: 若明日开盘即跌该股 ATR×2, 买入理由是否还成立？否→放弃")
        print("- **历史假信号**: 该信号在过去20交易日出现过几次？每次之后5日走势如何？假信号率>60%→放弃")

        for i, c in enumerate(results, 1):
            ec = c.get("evidence_card") or {}
            patt = c.get("pattern_labels") or []
            conf = c.get("confidence_label") or "-"
            creason = c.get("confidence_reason") or ""
            print(f"\n### {i}. {c['code']} {c['name']} "
                  f"[{c.get('strategy','?')}] 置信度={conf}")
            if creason:
                print(f"- **置信度理由**: {creason}")
            if patt:
                print(f"- **形态**: {', '.join(patt)}")
            bull = ec.get("bullish") or []
            bear = ec.get("bearish") or []
            uncr = ec.get("uncertain") or []
            if bull:
                print("- **看多信号**:")
                for s in bull:
                    print(f"  - ✅ {s}")
            if bear:
                print("- **看空信号**:")
                for s in bear:
                    print(f"  - ❌ {s}")
            if uncr:
                print("- **存疑**:")
                for s in uncr:
                    print(f"  - ❓ {s}")
            # Strategy-specific verify checks
            mv = c.get("must_verify_before_buy") or {}
            checks = mv.get("must_verify") or []
            if checks:
                print("- **策略专属必验**:")
                for ch in checks:
                    print(f"  - 🔍 **{ch['check']}**: {ch['how']}")
            # Strategy-specific devil_advocate
            dev = c.get("devil_advocate_questions") or []
            if dev:
                print("- **反方质询 (自问自答后再决定)**:")
                for q in dev:
                    print(f"  - 🤔 {q}")

    # ----- Capital allocation plan (baseline, score-ordered) -----
    # LLM is expected to produce its S3 final pick order, then invoke
    # `python stockquant.py allocate --codes ... --capital ... --comment "..."`
    # to get the authoritative table; this baseline is a sanity reference only.
    # When verbose-log is open we redirect the baseline table there and leave
    # a one-line pointer on stdout -- keeps the 20KB head budget focused on
    # decision-critical sections (NEXT_STEP + Top-N + DATA_QUALITY).
    plan = meta.get("allocation_plan") or {}
    if _VERBOSE_LOG_FH is not None:
        import contextlib as _cl
        import io as _io
        _buf = _io.StringIO()
        with _cl.redirect_stdout(_buf):
            _render_allocation_markdown(plan, capital, title_note="baseline: 按得分高到低")
        _vprint(_buf.getvalue(), end="")
        print()
        print("[ALLOCATION_BASELINE] 按得分高到低的 baseline 分配表已写入 verbose log。")
        print("  → LLM 产出最终选股顺序后请调用:")
        print("    python ${SKILL_DIR}/stockquant/scripts/stockquant.py allocate "
              "--codes <c1,c2,...> --capital <元> --comment \"...\"")
        print("    生成权威分配表；不要手算资金/股数。")
    else:
        _render_allocation_markdown(plan, capital, title_note="baseline: 按得分高到低")

    # NEXT_STEP was already printed at the TOP of this function via
    # _print_next_step_block() - no tail duplication here. Rationale:
    # placing it first ensures survival across downstream truncation
    # (see bug 2026-04-18: agent cap stripped 2452 bytes off the tail).


# ==========================================================================
# Merged from legacy `stock` skill: quote / search / kline CLI helpers.
# These expose the stockquant data layer to callers (Agent or human) via a
# plain `quote/kline/search` subcommand, replacing the now-deleted stock.py.
# ==========================================================================

def _secid_for_quote(code):
    """East Money security id encoding (same rule as legacy stock._secid)."""
    c = code.strip()
    if c.isdigit():
        if len(c) == 5:                                    # Hong Kong 5-digit
            return f"116.{c}"
        return f"1.{c}" if c[0] == "6" else f"0.{c}"
    return f"105.{c.upper()}"                              # US ticker


def _quote_em(code):
    """Single-code real-time quote via East Money push2. None on failure."""
    sid = _secid_for_quote(code)
    url = (f"https://push2.eastmoney.com/api/qt/stock/get?secid={sid}"
           "&fields=f43,f44,f45,f46,f47,f48,f57,f58,f59,f60,f116,f117,f170,f171")
    try:
        d = requests.get(url, headers={**_H, "Referer": _REF_EM},
                         timeout=TIMEOUT).json().get("data")
        if not d:
            return None
        dp = d.get("f59", 2)
        div = 10 ** dp
        return {
            "code": d.get("f57", ""), "name": d.get("f58", ""),
            "price": round(d.get("f43", 0) / div, dp),
            "pct": round(d.get("f170", 0) / 100, 2),
            "change": round(d.get("f171", 0) / div, dp),
            "open": round(d.get("f46", 0) / div, dp),
            "high": round(d.get("f44", 0) / div, dp),
            "low": round(d.get("f45", 0) / div, dp),
            "prev_close": round(d.get("f60", 0) / div, dp),
            "vol": d.get("f47", 0), "amount": d.get("f48", 0),
            "total_mv": d.get("f116", 0), "float_mv": d.get("f117", 0),
        }
    except Exception:
        return None


def _quote_sina(code):
    """Sina fallback for A-share/HK quote. None on failure."""
    c = code.strip()
    if not c.isdigit():
        return None
    sc = f"hk{c}" if len(c) == 5 else (f"sh{c}" if c[0] == "6" else f"sz{c}")
    try:
        text = requests.get(f"https://hq.sinajs.cn/list={sc}",
                            headers={**_H, "Referer": "https://finance.sina.com.cn"},
                            timeout=TIMEOUT).text.strip()
        if '=""' in text or not text:
            return None
        inner = text.split('"')[1] if '"' in text else ""
        if not inner:
            return None
        f = inner.split(",")
        if len(f) < 10:
            return None
        p, prev = float(f[3]), float(f[2])
        return {
            "code": c, "name": f[0], "price": p,
            "pct": round((p - prev) / prev * 100, 2) if prev else 0.0,
            "change": round(p - prev, 2),
            "open": float(f[1]), "high": float(f[4]), "low": float(f[5]),
            "prev_close": prev,
            "vol": int(float(f[8])), "amount": float(f[9]),
            "total_mv": 0.0, "float_mv": 0.0,
        }
    except Exception:
        return None


def query_quote(code):
    """Cross-source quote: try EM then Sina. Never raises."""
    for fn in (_quote_em, _quote_sina):
        r = fn(code)
        if r and r.get("price"):
            return r
    return {"code": code, "name": "NOT_FOUND", "error": "quote APIs failed"}


def print_quotes(codes):
    """Print JSON array of quotes for batch `codes`."""
    print(json.dumps([query_quote(c) for c in codes],
                     ensure_ascii=False, indent=2))


def search_code(keyword, count=5):
    """Search by name/pinyin via East Money suggest API."""
    try:
        url = (f"https://searchapi.eastmoney.com/api/suggest/get?"
               f"input={keyword}&type=14&count={count}")
        data = requests.get(url, headers={**_H, "Referer": _REF_EM},
                            timeout=TIMEOUT).json()
        tbl = (data.get("QuotationCodeTable") or {}).get("Data") or []
        return [{"code": i["Code"], "name": i["Name"]} for i in tbl]
    except Exception as e:
        return [{"error": str(e)}]


def print_search(keyword, count=5):
    print(json.dumps(search_code(keyword, count), ensure_ascii=False, indent=2))


def _fmt_amount(val):
    """Human-readable amount: 亿 / 万 / raw."""
    if val >= 1e8:
        return f"{val / 1e8:.2f}亿"
    if val >= 1e4:
        return f"{val / 1e4:.0f}万"
    return f"{val:.0f}"


def print_kline_cli(code, period="day", count=30):
    """Print k-line as markdown table. Reuses stockquant's Sina-backed fetcher.

    period=day/week/month. Note: only `day` is cached; week/month fall through
    to _fetch_sina_kline with the appropriate scale code.
    """
    if period == "day":
        rows = get_daily_kline(code, n=count)
    else:
        # Sina scale codes: week=1200 (for 5-day minute agg no), month=5000.
        # Actually weekly/monthly is rarely needed by sell-plan; provide best-
        # effort via existing _fetch_sina_kline for completeness.
        scale = {"week": 1200, "month": 5000}.get(period, 240)
        raw = _fetch_sina_kline(code, scale=scale, n=count)
        rows = [{"date": r.get("ts", "")[:10].replace("-", ""),
                 "open": r["open"], "close": r["close"],
                 "high": r["high"], "low": r["low"],
                 "vol": r["vol"], "amount": r["amount"]}
                for r in raw if r.get("ts")]
    if not rows:
        print(f"No K-line data for {code}")
        return
    q = query_quote(code)
    name = q.get("name") if q and q.get("name") not in ("NOT_FOUND", "") else ""
    print(f"{name}({code}) {period.upper()} K-line (last {len(rows)})")
    cols = ["日期", "开盘", "收盘", "最高", "最低", "成交量", "成交额"]
    print("| " + " | ".join(cols) + " |")
    print("|" + "|".join(["------"] * len(cols)) + "|")
    for r in rows:
        print(f"| {r['date']} | {r['open']} | {r['close']} | {r['high']} | "
              f"{r['low']} | {r['vol']} | {_fmt_amount(r['amount'])} |")


# ==========================================================================
# sell-plan: holdings strategy advisor (regime-based progressive disclosure)
# ==========================================================================
# Two-phase pipeline (both phases share the same `sell-plan` subcommand):
#
#   PHASE 1 (no --plan):
#     Inputs : code:qty/avail@cost ... --cash N
#     Output : [STATE] / [HOLDINGS_DATA] / [REGIME_CLASSIFY] / [REGIME_RULES]
#              / [CADENCE_HINT] / [TASK]
#     Role   : Python hard-classifies each holding into a regime + soft pct
#              ranges. LLM reads, picks specific upper/lower percentages and
#              order ladder, then re-invokes sell-plan with --plan '<json>'.
#
#   PHASE 2 (with --plan):
#     Inputs : same holdings + same --cash + --plan '<json>'
#     Output : [VALIDATION] / [FINAL_PLAN] / [ACTION_PLAN] (with 📎PLAN: lines)
#     Hard rules enforced:
#       - per-code: sum(sell_qty) <= avail_qty                (T+1 lock)
#       - global  : sum(buy_qty * buy_price) <= cash          (no overdraft)
#       - all qty are 100-share multiples (rounded down)
#       - per-order price_pct must lie in the regime's allowed range
#       - RANGE_BOTH/RANGE_BOTH_TIGHT: min(sell_price)-max(buy_price) must
#         clear fee_floor_pct (round-trip fee + slippage cushion)
#
# Philosophy:
#   - Python = HARD compute (regime, soft ranges, validators).
#   - LLM    = SOFT decide (which pct in range, single vs ladder, cash quota,
#              regime override-to-conservative with reason).
#   - Each stock is independent; no cross-stock cash pre-allocation.
# ==========================================================================

# Regime classification thresholds (centralised; surfaced in [REGIME_RULES]).
_REGIME_THRESHOLDS = {
    "DEEP_LOSS_PCT": -4.5,
    "TREND_UP_PCT": 5.0,
    "HIGH_BAND_LO": 2.0,
    "OSC_LARGE_ATR_LO": 1.5,
    "OSC_LARGE_SPAN_LO": 5.0,
    "OSC_LARGE_PROFIT_LO": -4.0,
    "OSC_LARGE_PROFIT_HI": 4.0,
    "OSC_SMALL_ATR_LO": 0.5,
    "OSC_SMALL_SPAN_LO": 2.0,
    "OSC_SMALL_PROFIT_LO": -3.0,
    "OSC_SMALL_PROFIT_HI": 2.0,
    "FLAT_DEAD_ATR_HI": 0.5,
    "FLAT_DEAD_VOL_HI": 0.5,
    "LOW_DIP_PROFIT_LO": -3.0,
    "LOW_DIP_PROFIT_HI": 0.0,
    "ATR_RANGE_MULT_LO": 0.8,
    "ATR_RANGE_MULT_HI": 1.5,
    "TREND_DOWN_VOL_LO": 1.2,
    "OSC_LARGE_FEE_FLOOR": 0.8,
    "OSC_SMALL_FEE_FLOOR": 1.0,
    # BREAKOUT_ADD: 回本/起涨小区间, MA5↑ + 量能配合 + 主力净流入≥0 → 单侧加仓
    "BREAKOUT_PROFIT_LO": 0.0,
    "BREAKOUT_PROFIT_HI": 2.0,
    "BREAKOUT_VOL_LO": 1.2,
    "BREAKOUT_BAND_MULT_LO": 0.4,
    "BREAKOUT_BAND_MULT_HI": 0.8,
}


def _parse_holding_token(token):
    """Parse strict `code:qty/avail@cost` (no backward compat).

    avail (T+1 unlock count) and cost are both required:
      - avail caps how many shares can be sold today (T+1 lock).
      - cost is required for accurate regime classification (DEEP_LOSS,
        HIGH_BAND, etc.) and profit_pct math.
    Returns (code, qty, avail, cost).
    """
    token = token.strip()
    if not token:
        raise ValueError("empty token")
    if "@" not in token:
        raise ValueError(
            f"missing '@cost' in '{token}'; format is code:qty/avail@cost")
    head, cost_s = token.split("@", 1)
    try:
        cost = float(cost_s.strip())
    except ValueError as e:
        raise ValueError(f"bad cost '{cost_s}' in '{token}': {e}")
    if cost <= 0:
        raise ValueError(f"cost must be > 0 in '{token}'")
    if ":" not in head:
        raise ValueError(
            f"missing ':qty/avail' in '{token}'; format is code:qty/avail@cost")
    code_s, qty_part = head.split(":", 1)
    code = code_s.strip()
    if not code:
        raise ValueError(f"missing code in '{token}'")
    if "/" not in qty_part:
        raise ValueError(
            f"missing '/avail' in '{token}'; "
            "T+1 lock requires explicit avail (e.g. 1200/800 = 800 sellable)")
    qty_s, avail_s = qty_part.split("/", 1)
    try:
        qty = int(qty_s.strip())
        avail = int(avail_s.strip())
    except ValueError as e:
        raise ValueError(f"bad qty/avail '{qty_part}' in '{token}': {e}")
    if qty < 0 or avail < 0:
        raise ValueError(f"qty/avail must be >= 0 in '{token}'")
    if avail > qty:
        raise ValueError(f"avail({avail}) > qty({qty}) in '{token}'")
    return code, qty, avail, cost


def _ma_trend(closes, window=5, flat_slope_pct=0.3):
    """Classify MA trend via per-bar % slope of last `window` closes.

    Returns (trend, ma_value). trend in {up, down, flat, unknown}.
    """
    if not closes or len(closes) < window:
        return "unknown", None
    recent = closes[-window:]
    ma = sum(recent) / window
    if recent[0] == 0:
        return "unknown", ma
    slope_pct = (recent[-1] - recent[0]) / recent[0] / (window - 1) * 100
    if slope_pct > flat_slope_pct:
        return "up", ma
    if slope_pct < -flat_slope_pct:
        return "down", ma
    return "flat", ma


def _compute_range_metrics(quote, hist_rows, today_bar=None):
    """Compute ATR14 / 10-day span / intraday range / 5-day vol ratio.

    hist_rows: ascending-ordered daily bars EXCLUDING today's bar.
    today_bar: today's daily bar dict (vol/high/low) if present in kline,
               else None. Using kline's own today-vol avoids unit mismatch
               between quote.vol (手) and kline.vol (股 after ×100).
    quote: dict from query_quote (high/low/prev_close used for intraday range).
    Returns dict with float fields (None if data insufficient).
    """
    out = {"atr14_pct": None, "atr5_pct": None, "recent10_span_pct": None,
           "intraday_range_pct": None, "vol_ratio_5d": None}
    if hist_rows and len(hist_rows) >= 14:
        # ATR14 (full window)
        atr_window_14 = hist_rows[-14:]
        prev_close = (hist_rows[-15]["close"] if len(hist_rows) >= 15
                      else atr_window_14[0]["close"])
        trs = []
        for r in atr_window_14:
            tr = max(r["high"] - r["low"],
                     abs(r["high"] - prev_close),
                     abs(r["low"] - prev_close))
            trs.append(tr)
            prev_close = r["close"]
        atr14 = sum(trs) / len(trs)
        last_close = atr_window_14[-1]["close"]
        if last_close > 0:
            out["atr14_pct"] = atr14 / last_close * 100
        # ATR5 (short window, less contaminated by ancient crashes)
        if len(hist_rows) >= 6:
            atr_window_5 = hist_rows[-5:]
            pc5 = hist_rows[-6]["close"] if len(hist_rows) >= 6 else atr_window_5[0]["close"]
            trs5 = []
            for r in atr_window_5:
                tr = max(r["high"] - r["low"],
                         abs(r["high"] - pc5),
                         abs(r["low"] - pc5))
                trs5.append(tr)
                pc5 = r["close"]
            atr5 = sum(trs5) / len(trs5)
            lc5 = atr_window_5[-1]["close"]
            if lc5 > 0:
                out["atr5_pct"] = atr5 / lc5 * 100
    if hist_rows and len(hist_rows) >= 10:
        sw = hist_rows[-10:]
        hi = max(r["high"] for r in sw)
        lo = min(r["low"] for r in sw)
        avg_close = sum(r["close"] for r in sw) / len(sw)
        if avg_close > 0:
            out["recent10_span_pct"] = (hi - lo) / avg_close * 100
    th = quote.get("high")
    tl = quote.get("low")
    pc = quote.get("prev_close")
    if th and tl and pc and pc > 0 and th > 0 and tl > 0 and th > tl:
        out["intraday_range_pct"] = (th - tl) / pc * 100
    # Volume ratio: use today_bar.vol (consistent unit with hist_rows.vol).
    today_vol = today_bar.get("vol") if today_bar else None
    if today_vol and hist_rows and len(hist_rows) >= 5:
        avg5 = sum(r["vol"] for r in hist_rows[-5:]) / 5
        if avg5 > 0:
            out["vol_ratio_5d"] = today_vol / avg5
    return out


def _classify_regime(profit_pct, ma5_trend, atr14_pct, span10_pct,
                     vol_ratio, main_inflow, now_time,
                     is_trading=True, atr5_pct=None):
    """Hard-classify a holding into one of 11 regimes.

    Returns dict with: regime, action_type, upper_pct_range, lower_pct_range,
    max_sell_frac, max_buy_frac, sell_ladder_hint, min_spread_pct, reason.
    See [REGIME_RULES] block for the full table.

    `is_trading` is required so that clock-priority regimes (CLOSE_RUSH /
    TAIL_EXIT) only fire during actual continuous-bidding hours, not after
    market close or on non-trading days.

    Note: Cash availability is intentionally NOT a classification input.
    Buy-side qty = sell-side qty for fixed-qty hedge (T+0 反复做差价); the
    buy notional comes from sell proceeds. The host module guarantees cash
    sufficiency at order placement time.
    """
    T = _REGIME_THRESHOLDS
    base = dict(regime="HOLD", action_type="NO_OP",
                upper_pct_range=None, lower_pct_range=None,
                max_sell_frac=0.0, max_buy_frac=0.0,
                sell_ladder_hint="none", min_spread_pct=None,
                reason="default hold")

    # 0. MARKET_CLOSED (non-trading day or >=15:00) - no orders possible.
    if not is_trading or now_time >= datetime.time(15, 0):
        return dict(base, regime="MARKET_CLOSED", action_type="NO_OP",
                    reason="非交易时段, 无法挂单, 仅汇总观察")

    # 1. CLOSE_RUSH (14:55-15:00 only, supersedes everything else)
    if now_time >= datetime.time(14, 55):
        return dict(base, regime="CLOSE_RUSH", action_type="SELL_AT_CURRENT",
                    max_sell_frac=1.0, sell_ladder_hint="single",
                    reason="14:55+ 收盘冲刺，挂现价/对手价快速出货")

    # 2. DEEP_LOSS (hard stop)
    if profit_pct is not None and profit_pct <= T["DEEP_LOSS_PCT"]:
        return dict(base, regime="DEEP_LOSS", action_type="SELL_ALL",
                    max_sell_frac=1.0, sell_ladder_hint="single",
                    reason=f"profit {profit_pct:+.2f}% ≤ {T['DEEP_LOSS_PCT']}%, 纪律止损")

    # 3. TAIL_EXIT (after 14:30 + still red + MA5 not strongly up)
    if (now_time >= datetime.time(14, 30) and profit_pct is not None
            and profit_pct < 0 and ma5_trend != "up"):
        return dict(base, regime="TAIL_EXIT", action_type="SELL_AT_CURRENT",
                    max_sell_frac=1.0, sell_ladder_hint="single",
                    reason=f"14:30+ 浮亏 {profit_pct:+.2f}% & MA5≠up, 尾盘不救")

    # 4. TREND_UP — main rally up, default NO_OP to avoid 卖飞主升浪.
    # LLM may downgrade to HIGH_BAND via --override to take partial profit.
    if (profit_pct is not None and profit_pct >= T["TREND_UP_PCT"]
            and ma5_trend == "up"):
        return dict(base, regime="TREND_UP", action_type="NO_OP",
                    upper_pct_range=None, lower_pct_range=None,
                    max_sell_frac=0.0, max_buy_frac=0.0,
                    sell_ladder_hint="none", min_spread_pct=None,
                    reason=(f"profit {profit_pct:+.2f}% & MA5↑, "
                            "主升浪默认持仓不动(避免T飞); "
                            "如需部分止盈→override 到 HIGH_BAND"))

    # 5. HIGH_BAND
    if (profit_pct is not None
            and T["HIGH_BAND_LO"] <= profit_pct < T["TREND_UP_PCT"]):
        return dict(base, regime="HIGH_BAND", action_type="SELL_AT_HIGH",
                    upper_pct_range=(1.0, 3.0),
                    max_sell_frac=0.2, sell_ladder_hint="single",
                    reason=f"profit {profit_pct:+.2f}% ∈ [+2%,+5%), 高点小幅减")

    # 5b. BREAKOUT_ADD — 回本/起涨区单侧加仓 (盖在 HIGH_BAND 之下、TREND_DOWN/HOLD 之上)
    # 触发: profit ∈ [0%, +2%) & MA5↑ & 量比≥1.2 & 主力净流入≥0 & 有 atr14
    # 用 LOW_BUY_ONLY action_type 复用 default-order 生成器与 buy 校验白名单
    if (profit_pct is not None
            and T["BREAKOUT_PROFIT_LO"] <= profit_pct < T["BREAKOUT_PROFIT_HI"]
            and ma5_trend == "up"
            and vol_ratio is not None and vol_ratio >= T["BREAKOUT_VOL_LO"]
            and (main_inflow is None or main_inflow >= 0)
            and atr14_pct is not None and atr14_pct > 0):
        lo_mult = T["BREAKOUT_BAND_MULT_LO"]
        hi_mult = T["BREAKOUT_BAND_MULT_HI"]
        lower = (round(-atr14_pct * hi_mult, 2),
                 round(-atr14_pct * lo_mult, 2))
        return dict(base, regime="BREAKOUT_ADD", action_type="LOW_BUY_ONLY",
                    lower_pct_range=lower,
                    max_buy_frac=0.3, sell_ladder_hint="none",
                    reason=(f"profit {profit_pct:+.2f}% MA5↑ 量比{vol_ratio:.2f} "
                            f"主力净流入{'≥0' if main_inflow is None else f'{main_inflow/10000:+.0f}万'}, "
                            "回本/起涨区浅回踩加仓 (frac≤0.3)"))

    # 6. TREND_DOWN (MA5 down + still red + volume rising = real breakdown)
    if (ma5_trend == "down" and profit_pct is not None and profit_pct < 0
            and vol_ratio is not None and vol_ratio >= T["TREND_DOWN_VOL_LO"]):
        return dict(base, regime="TREND_DOWN", action_type="BREAK_EXIT",
                    max_sell_frac=1.0, sell_ladder_hint="single",
                    reason=(f"MA5↓ profit {profit_pct:+.2f}% 量比{vol_ratio:.2f}, "
                            "破位放量出局"))

    # 7. FLAT_DEAD (must precede OSC checks - too narrow / dead volume)
    if (ma5_trend == "flat"
            and ((atr14_pct is not None and atr14_pct < T["FLAT_DEAD_ATR_HI"])
                 or (vol_ratio is not None and vol_ratio < T["FLAT_DEAD_VOL_HI"]))):
        a_str = f"{atr14_pct:.2f}" if atr14_pct is not None else "?"
        v_str = f"{vol_ratio:.2f}" if vol_ratio is not None else "?"
        return dict(base, regime="FLAT_DEAD", action_type="NO_OP",
                    reason=f"MA5平 atr14={a_str}% vol_ratio={v_str}, 震幅/量能不足")

    def _atr_band(atr_pct):
        # Soft band [atr*0.8, atr*1.5] - LLM picks specific pct in here.
        lo = atr_pct * T["ATR_RANGE_MULT_LO"]
        hi = atr_pct * T["ATR_RANGE_MULT_HI"]
        return (round(lo, 2), round(hi, 2))

    # 8. OSC_LARGE
    if (ma5_trend == "flat" and atr14_pct is not None and span10_pct is not None
            and profit_pct is not None
            and atr14_pct >= T["OSC_LARGE_ATR_LO"]
            and span10_pct >= T["OSC_LARGE_SPAN_LO"]
            and T["OSC_LARGE_PROFIT_LO"] <= profit_pct <= T["OSC_LARGE_PROFIT_HI"]):
        b = _atr_band(atr14_pct)
        return dict(base, regime="OSC_LARGE", action_type="RANGE_BOTH",
                    upper_pct_range=b,
                    lower_pct_range=(round(-b[1], 2), round(-b[0], 2)),
                    max_sell_frac=0.5, max_buy_frac=0.5,
                    sell_ladder_hint="double",
                    min_spread_pct=T["OSC_LARGE_FEE_FLOOR"],
                    reason=(f"MA5平 atr14={atr14_pct:.2f}% span10={span10_pct:.1f}% "
                            f"profit{profit_pct:+.2f}%, 大震荡双边挂单"))

    # 9. OSC_SMALL
    if (ma5_trend == "flat" and atr14_pct is not None and span10_pct is not None
            and profit_pct is not None
            and T["OSC_SMALL_ATR_LO"] <= atr14_pct < T["OSC_LARGE_ATR_LO"]
            and span10_pct >= T["OSC_SMALL_SPAN_LO"]
            and T["OSC_SMALL_PROFIT_LO"] <= profit_pct <= T["OSC_SMALL_PROFIT_HI"]):
        b = _atr_band(atr14_pct)
        return dict(base, regime="OSC_SMALL", action_type="RANGE_BOTH_TIGHT",
                    upper_pct_range=b,
                    lower_pct_range=(round(-b[1], 2), round(-b[0], 2)),
                    max_sell_frac=0.3, max_buy_frac=0.3,
                    sell_ladder_hint="single",
                    min_spread_pct=T["OSC_SMALL_FEE_FLOOR"],
                    reason=(f"MA5平 atr14={atr14_pct:.2f}% span10={span10_pct:.1f}% "
                            f"profit{profit_pct:+.2f}%, 小震荡谨慎双边"))

    # 10. LOW_DIP (only-buy below cost: dip-buy if not breaking down).
    # Cash availability is NOT checked; host module guarantees it.
    if (profit_pct is not None
            and T["LOW_DIP_PROFIT_LO"] < profit_pct < T["LOW_DIP_PROFIT_HI"]
            and ma5_trend in ("flat", "up")
            and (main_inflow is None or main_inflow >= 0)):
        # ATR decay guard: if ancient crashes inflated ATR14 compared to recent ATR5,
        # cap the effective ATR to prevent unrealistically wide buy bands.
        effective_atr = atr14_pct if atr14_pct else None
        decay_note = ""
        if atr14_pct and atr5_pct and atr5_pct > 0:
            if atr14_pct > atr5_pct * 2.0:
                effective_atr = atr5_pct * 1.5  # cap: recent vol × 1.5
                decay_note = (f" (ATR14={atr14_pct:.2f}%>>ATR5={atr5_pct:.2f}%,"
                              f" capped→{effective_atr:.2f}%)")
        if effective_atr is not None and effective_atr > 0:
            b = _atr_band(effective_atr)
            lower = (round(-b[1], 2), round(-b[0], 2))
        else:
            lower = (-3.0, -1.5)
        return dict(base, regime="LOW_DIP", action_type="LOW_BUY_ONLY",
                    lower_pct_range=lower,
                    max_buy_frac=0.5, sell_ladder_hint="none",
                    reason=(f"profit {profit_pct:+.2f}% MA5={ma5_trend} "
                            f"& 主力净流入≥0, 下沿低吸{decay_note}"
                            f" (现金由顶层保证)"))

    # HOLD (catch-all)
    p_str = f"{profit_pct:+.2f}%" if profit_pct is not None else "?"
    return dict(base, regime="HOLD", action_type="NO_OP",
                reason=f"profit {p_str} MA5={ma5_trend}, 不符合任何明确档位, 持有观察")


def _round_lot(qty, lot=100):
    """Round down to nearest 100-share lot (A-share trading unit)."""
    if qty is None or qty <= 0:
        return 0
    return int(qty // lot) * lot


def _compute_session_meta(now):
    """Compute session classification + key time deltas (objective only)."""
    is_trading, nt_reason = is_trading_day_probe()
    hm = now.hour * 100 + now.minute
    am_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    pm_open = now.replace(hour=13, minute=0, second=0, microsecond=0)
    pm_close = now.replace(hour=15, minute=0, second=0, microsecond=0)
    tail_14_30 = now.replace(hour=14, minute=30, second=0, microsecond=0)
    tail_14_55 = now.replace(hour=14, minute=55, second=0, microsecond=0)
    if not is_trading:
        sess_code = "CLOSED"
        sess_desc = f"非交易日({nt_reason})"
    elif hm < 930:
        sess_code = "PRE_AM"
        sess_desc = "盘前 (<09:30)"
    elif hm < 1130:
        sess_code = "AM_TRADING"
        sess_desc = "上午连续竞价 (9:30-11:30)"
    elif hm < 1300:
        sess_code = "LUNCH"
        sess_desc = "午休 (11:30-13:00)"
    elif hm < 1455:
        sess_code = "PM_TRADING"
        sess_desc = "下午连续竞价 (13:00-14:55)"
    elif hm < 1500:
        sess_code = "CLOSE_RUSH"
        sess_desc = "收盘冲刺 (14:55-15:00)"
    else:
        sess_code = "CLOSED"
        sess_desc = "已收盘 (≥15:00)"

    def _to_s(td):
        return max(0, int(td.total_seconds()))

    return {
        "is_trading": is_trading, "nt_reason": nt_reason,
        "session_code": sess_code, "session_desc": sess_desc,
        "secs_to_am_open": _to_s(am_open - now),
        "secs_to_pm_open": _to_s(pm_open - now),
        "secs_to_tail_14_30": _to_s(tail_14_30 - now),
        "secs_to_close_rush": _to_s(tail_14_55 - now),
        "secs_to_close": _to_s(pm_close - now),
    }


def _suggest_orders(code, name, qty_total, avail, price, regime, target_yuan):
    """Build default suggested order strings (LLM may copy as-is or override).

    Strategy: fixed-qty hedge per order. Each order ~target_yuan notional;
    sell_qty == buy_qty for OSC/RANGE regimes (T+0 反复做差价 - 持仓中性).
    Returns list of "code:side:qty@spec" strings (or [] for NO_OP).
    """
    atype = regime["action_type"]
    if atype == "NO_OP" or not price or price <= 0:
        return []
    # shares per single order ~ target_yuan worth, lot-rounded, min 100
    spo = max(100, _round_lot(target_yuan / price))

    # Full-exit defensive regimes: sell all avail in one tier.
    if atype in ("SELL_AT_CURRENT", "BREAK_EXIT"):
        q = _round_lot(avail)
        return [f"{code}:sell:{q}@current"] if q > 0 else []
    if atype == "SELL_ALL":
        q = _round_lot(avail)
        return [f"{code}:sell:{q}@bid1"] if q > 0 else []

    out = []
    # Sell side (PARTIAL_SELL / SELL_AT_HIGH / RANGE_BOTH(_TIGHT))
    if regime["upper_pct_range"] and regime["max_sell_frac"] > 0:
        lo, hi = regime["upper_pct_range"]
        mid = round((lo + hi) / 2, 2)
        cap_sell = _round_lot(avail * regime["max_sell_frac"])
        sell_q = min(spo, cap_sell)
        if sell_q >= 100:
            if regime["sell_ladder_hint"] == "double" and sell_q >= 200:
                # Two tiers: lower-mid and upper-mid pct, qty 50/50
                pct1 = round((lo + mid) / 2, 2)
                pct2 = round((mid + hi) / 2, 2)
                half = _round_lot(sell_q / 2)
                out.append(f"{code}:sell:{half}@{pct1:+.2f}")
                out.append(f"{code}:sell:{half}@{pct2:+.2f}")
            else:
                out.append(f"{code}:sell:{sell_q}@{mid:+.2f}")

    # Buy side (RANGE_BOTH(_TIGHT) / LOW_BUY_ONLY); qty matches sell side
    # for hedge unless LOW_BUY_ONLY (no sell side, then use spo capped).
    if regime["lower_pct_range"] and regime["max_buy_frac"] > 0:
        lo, hi = regime["lower_pct_range"]
        mid = round((lo + hi) / 2, 2)
        cap_buy = _round_lot(qty_total * regime["max_buy_frac"])
        if atype == "LOW_BUY_ONLY":
            buy_q = min(spo, cap_buy)
        else:
            # Hedge: match sell qty (sum of sells) but cap by buy frac.
            # Token format is "code:side:qty@spec" so qty needs @ stripped.
            sell_total = sum(int(s.split(":")[2].split("@")[0]) for s in out
                             if ":sell:" in s)
            buy_q = min(sell_total, cap_buy) if sell_total else 0
        if buy_q >= 100:
            out.append(f"{code}:buy:{buy_q}@{mid:+.2f}")
    return out


def _build_plan_rows(holdings, now, target_yuan=10000.0, is_trading=True):
    """Batch-fetch quotes + daily k-lines, classify regime, return enriched rows.

    `now` is the wall-clock used for time-of-day regime gates (e.g. CLOSE_RUSH).
    `is_trading` is propagated into regime classification so clock-priority
    regimes never fire outside trading hours. `target_yuan` controls suggested
    per-order notional (single-trade total ~target, balances fee impact).

    Today's bar (if present in daily k-line) is split out and passed to the
    metrics function as `today_bar` so that vol_ratio_5d uses a consistent
    unit (kline vol vs kline 5-day avg vol), avoiding the quote.vol(手) vs
    kline.vol(股) unit mismatch.
    """
    codes = [h[0] for h in holdings]
    quotes = {c: query_quote(c) for c in codes}
    klines = get_daily_klines_batch(codes, n=30, workers=min(8, len(codes)))
    today_str = now.strftime("%Y%m%d")
    rows = []
    for code, qty, avail, cost in holdings:
        q = quotes.get(code) or {}
        name = q.get("name", "?")
        price = q.get("price")
        pct_today = q.get("pct")
        main_inflow = q.get("main_inflow")
        kl = klines.get(code) or []
        # Split today's bar (potentially partial) from history.
        hist = [r for r in kl if r.get("date") != today_str]
        today_bar = next((r for r in kl if r.get("date") == today_str), None)
        closes = [r["close"] for r in hist if r.get("close")]
        ma5_trend, ma5_val = _ma_trend(closes, window=5)
        ma10_trend, ma10_val = _ma_trend(closes, window=10)
        # 10-day low for LOW_DIP support validation
        low_10d = None
        if len(hist) >= 10:
            lows_10 = [r["low"] for r in hist[-10:] if r.get("low")]
            if lows_10:
                low_10d = min(lows_10)
        metrics = _compute_range_metrics(q, hist, today_bar=today_bar)
        profit_pct = None
        if cost and price and cost > 0:
            profit_pct = (price - cost) / cost * 100
        regime = _classify_regime(
            profit_pct=profit_pct, ma5_trend=ma5_trend,
            atr14_pct=metrics["atr14_pct"],
            span10_pct=metrics["recent10_span_pct"],
            vol_ratio=metrics["vol_ratio_5d"],
            main_inflow=main_inflow,
            now_time=now.time(),
            is_trading=is_trading,
            atr5_pct=metrics.get("atr5_pct"),
        )
        # Post-classify sanity: LOW_DIP buy price must not break the 10-day
        # swing low (hard floor).  MA10 is a soft lagging level—a healthy
        # pullback to MA10 is a legit dip-buy opportunity, not a falling knife.
        if regime.get("regime") == "LOW_DIP" and price and price > 0:
            lr = regime.get("lower_pct_range")
            if lr:
                buy_pct = round((lr[0] + lr[1]) / 2, 2)
                buy_price = round(price * (1 + buy_pct / 100), 2)
                if low_10d and buy_price < low_10d:
                    regime = dict(regime, regime="HOLD", action_type="NO_OP",
                                  reason=(f"LOW_DIP buy@{buy_pct:+.2f}%={buy_price}"
                                          f" 跌破 10d-low={low_10d:.2f}, 降级HOLD"))
        suggest = _suggest_orders(code, name, qty, avail, price, regime,
                                  target_yuan)
        rows.append({
            "code": code, "name": name, "qty": qty, "avail": avail, "cost": cost,
            "price": price, "pct_today": pct_today, "main_inflow": main_inflow,
            "ma5_trend": ma5_trend, "ma5": ma5_val,
            "atr14_pct": metrics["atr14_pct"],
            "atr5_pct": metrics.get("atr5_pct"),
            "span10_pct": metrics["recent10_span_pct"],
            "intraday_range_pct": metrics["intraday_range_pct"],
            "vol_ratio_5d": metrics["vol_ratio_5d"],
            "profit_pct": profit_pct,
            "regime": regime,
            "suggest_orders": suggest,
        })
    return rows


def _fmt_v(v, suf="", sign=False):
    """Pretty print float|None with optional sign + suffix."""
    if v is None:
        return "-"
    if isinstance(v, float):
        return (f"{v:+.2f}{suf}" if sign else f"{v:.2f}{suf}")
    return f"{v}{suf}"


def _render_state_block(now, sess_meta, target_yuan, holdings_count,
                        fee_floor_pct):
    wd_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][now.weekday()]
    print("\n[STATE]")
    print(f"run_at: {now.strftime('%Y-%m-%d %H:%M')} {wd_cn}   "
          f"# {sess_meta['session_desc']}")
    print(f"session: {sess_meta['session_code']}")
    print(f"holdings_count: {holdings_count}")
    print(f"target_yuan_per_order: {target_yuan:.0f}元   "
          f"# 单笔目标总价 (qty×price≈{target_yuan:.0f}元, 控手续费占比)")
    print(f"fee_floor_pct: {fee_floor_pct:.2f}%   "
          f"# 双边差价最低门槛 (round-trip 手续费+滑点缓冲)")
    if sess_meta["is_trading"]:
        print(f"seconds_to_am_open: {sess_meta['secs_to_am_open']}")
        print(f"seconds_to_pm_open: {sess_meta['secs_to_pm_open']}")
        print(f"seconds_to_tail_14_30: {sess_meta['secs_to_tail_14_30']}")
        print(f"seconds_to_close_rush: {sess_meta['secs_to_close_rush']}")
        print(f"seconds_to_close: {sess_meta['secs_to_close']}")


def _render_holdings_data(rows):
    print("\n[HOLDINGS_DATA]  (每只客观特征, LLM 在 S1/S2 中使用)")
    print("| # | 代码 | 名称 | 总持仓 | 可用 | 成本 | 现价 | 今日% | profit% "
          "| MA5 | 趋势 | atr14% | atr5% | span10% | 盘中振幅% | 量比5d | 主力净流入(万) |")
    print("|---:|---|---|---:|---:|---:|---:|---:|---:|---:|:--:|---:|---:|---:|---:|---:|---:|")
    for i, p in enumerate(rows, 1):
        infl = p["main_inflow"]
        infl_w = (infl / 10000.0) if isinstance(infl, (int, float)) else None
        # ATR decay warning: flag when ancient crashes have inflated ATR14 vs recent ATR5
        atr5_str = _fmt_v(p.get("atr5_pct"), "%")
        a14 = p.get("atr14_pct")
        a5 = p.get("atr5_pct")
        if a14 and a5 and a5 > 0 and a14 > a5 * 2.0:
            atr5_str += " ⚠"  # decay warning
        print(f"| {i} | `{p['code']}` | {p['name']} | {p['qty']} | {p['avail']} "
              f"| {_fmt_v(p['cost'])} | {_fmt_v(p['price'])} | "
              f"{_fmt_v(p['pct_today'], '%', sign=True)} | "
              f"{_fmt_v(p['profit_pct'], '%', sign=True)} | "
              f"{_fmt_v(p['ma5'])} | {p['ma5_trend']} | "
              f"{_fmt_v(a14, '%')} | "
              f"{atr5_str} | "
              f"{_fmt_v(p['span10_pct'], '%')} | "
              f"{_fmt_v(p['intraday_range_pct'], '%')} | "
              f"{_fmt_v(p['vol_ratio_5d'])} | "
              f"{_fmt_v(infl_w, sign=True)} |")


def _fmt_pct_range(rng):
    """Format (lo, hi) tuple as '[+lo%, +hi%]' or '-' if None."""
    if not rng:
        return "-"
    lo, hi = rng
    return f"[{lo:+.2f}%, {hi:+.2f}%]"


def _render_regime_classify(rows):
    print("\n[REGIME_CLASSIFY]  (Python 硬分类 + 默认建议 order, LLM 默认采纳或按面微调)")
    print("| 代码 | regime | action_type | 默认建议 --order (拷贝即可) | 理由 |")
    print("|---|---|---|---|---|")
    for p in rows:
        r = p["regime"]
        sug = p.get("suggest_orders") or []
        sug_str = " ".join(sug) if sug else "(留空 = NO_OP)"
        print(f"| `{p['code']}` | {r['regime']} | {r['action_type']} | "
              f"`{sug_str}` | {r['reason']} |")
    print("\n软区间详情 (LLM 要调整 pct/qty 时参考):")
    print("| 代码 | upper_pct_range (sell) | lower_pct_range (buy) | "
          "max_sell_frac | max_buy_frac | min_spread% | sell_ladder |")
    print("|---|---|---|---:|---:|---:|---|")
    for p in rows:
        r = p["regime"]
        ms = (f"{r['min_spread_pct']:.2f}%"
              if r["min_spread_pct"] is not None else "-")
        print(f"| `{p['code']}` | "
              f"{_fmt_pct_range(r['upper_pct_range'])} | "
              f"{_fmt_pct_range(r['lower_pct_range'])} | "
              f"{r['max_sell_frac']:.2f} | {r['max_buy_frac']:.2f} | "
              f"{ms} | {r['sell_ladder_hint']} |")


def _render_regime_rules():
    T = _REGIME_THRESHOLDS
    print("\n[REGIME_RULES]  (11 档 regime 决策矩阵, 第一命中)")
    print("| regime | 触发条件 | action_type | LLM 软决策空间 |")
    print("|---|---|---|---|")
    print( "| MARKET_CLOSED    | 非交易日 / >=15:00                                   "
           "| NO_OP            | 不挂单, 仅汇总观察 |")
    print(f"| CLOSE_RUSH       | 交易日 14:55-15:00                                  "
          f"| SELL_AT_CURRENT  | 单档卖现价, 全部 avail |")
    print(f"| DEEP_LOSS        | profit_pct ≤ {T['DEEP_LOSS_PCT']}%                   "
          f"| SELL_ALL         | 单档卖 bid1, 全部 avail |")
    print(f"| TAIL_EXIT        | 14:30+ & profit<0 & MA5≠up                          "
          f"| SELL_AT_CURRENT  | 单档卖现价, 全部 avail |")
    print(f"| TREND_UP         | profit ≥ +{T['TREND_UP_PCT']}% & MA5↑               "
          f"| NO_OP            | 主升浪默认不动 (避免T飞); 想止盈→override→HIGH_BAND |")
    print(f"| HIGH_BAND        | +{T['HIGH_BAND_LO']}% ≤ profit < +{T['TREND_UP_PCT']}%"
          f"| SELL_AT_HIGH     | 单档 ∈ [+1%,+3%], frac≤0.2 |")
    print(f"| TREND_DOWN       | MA5↓ & profit<0 & vol_ratio ≥ {T['TREND_DOWN_VOL_LO']}"
          f"| BREAK_EXIT       | 单档现价, 全部 avail |")
    print(f"| OSC_LARGE        | MA5平 & atr14 ≥ {T['OSC_LARGE_ATR_LO']}% & "
          f"span10 ≥ {T['OSC_LARGE_SPAN_LO']}% & profit ∈ "
          f"[{T['OSC_LARGE_PROFIT_LO']}%, {T['OSC_LARGE_PROFIT_HI']}%]"
          f"| RANGE_BOTH       | 双边: upper ∈ atr×[0.8,1.5], "
          f"lower ∈ -atr×[0.8,1.5], frac≤0.5, "
          f"spread≥{T['OSC_LARGE_FEE_FLOOR']}% |")
    print(f"| OSC_SMALL        | MA5平 & atr14 ∈ "
          f"[{T['OSC_SMALL_ATR_LO']}%, {T['OSC_LARGE_ATR_LO']}%) & "
          f"span10 ≥ {T['OSC_SMALL_SPAN_LO']}% & profit ∈ "
          f"[{T['OSC_SMALL_PROFIT_LO']}%, {T['OSC_SMALL_PROFIT_HI']}%]"
          f"| RANGE_BOTH_TIGHT | 双边谨慎: frac≤0.3, "
          f"spread≥{T['OSC_SMALL_FEE_FLOOR']}% |")
    print(f"| FLAT_DEAD        | MA5平 & (atr14 < {T['FLAT_DEAD_ATR_HI']}% 或 "
          f"vol_ratio < {T['FLAT_DEAD_VOL_HI']})"
          f"| NO_OP            | 不操作 (震幅不够覆盖手续费) |")
    print(f"| LOW_DIP          | profit ∈ ({T['LOW_DIP_PROFIT_LO']}%, "
          f"{T['LOW_DIP_PROFIT_HI']}%) & MA5平/上 & 主力流入≥0 & cash>0  "
          f"| LOW_BUY_ONLY     | 单档买, lower ∈ -atr×[0.8,1.5], frac≤0.5, "
          f"ATR14>>ATR5时自动缩窄 |")
    print(f"| BREAKOUT_ADD     | profit ∈ [{T['BREAKOUT_PROFIT_LO']}%, "
          f"{T['BREAKOUT_PROFIT_HI']}%) & MA5↑ & 量比≥{T['BREAKOUT_VOL_LO']} "
          f"& 主力流入≥0  "
          f"| LOW_BUY_ONLY     | 回本起涨加仓: lower ∈ -atr×[{T['BREAKOUT_BAND_MULT_LO']},"
          f"{T['BREAKOUT_BAND_MULT_HI']}], frac≤0.3 |")
    print( "| HOLD             | 其他 (无明确档位)                                   "
           "| NO_OP            | 持有观察, 下一轮重评 |")


def _render_cadence_hint(sess_meta):
    print("\n[CADENCE_HINT]  (wait 节奏矩阵, LLM 在 S5 中选值)")
    print("| session | 建议 wait_seconds | 理由 |")
    print("|---|---:|---|")
    if sess_meta["is_trading"]:
        print(f"| PRE_AM (<09:30)         | {sess_meta['secs_to_am_open']} "
              f"| 等到开盘再查 |")
        print( "| AM_TRADING / PM_TRADING | 300 "
               "| 5 分钟重查, 平衡刷屏与漏波动 |")
        print(f"| LUNCH (11:30-13:00)     | {sess_meta['secs_to_pm_open']} "
              f"| 午休期价格不更新, 等到下午 |")
        print( "| CLOSE_RUSH (14:55+)     | 60  "
               "| 冲刺期高频监控 |")
        print( "| CLOSED (≥15:00)         | 0   "
               "| 立即终止, 无需 wait |")
    else:
        print( "| CLOSED (非交易日)       | 0   "
               "| 立即终止 |")


def _render_phase1_task():
    print("\n=== NEXT_STEP ===")
    print("S0. 【宏观背景】先读上方 [MACRO_SENTIMENT] 情绪得分和信号：")
    print("    - 若宏观偏空 (🔴 ≤-1): LOW_DIP 买入暂缓或不执行, 止损收紧; 优先观望等利空消化")
    print("    - 若宏观偏多 (🟢 ≥+1): 可以正常甚至略激进; 中性 (🟡) → 按默认策略")
    print("S1. 【默认采纳】逐只看 [REGIME_CLASSIFY] 的 `默认建议 --order` 列，如无特殊看法 → 原样拼到 Phase 2 调用。")
    print("S2. 【可选微调】参考 [HOLDINGS_DATA] 主力流入 + 量比5d:")
    print("    - 强 (流入>0 & 量比≥1.5) → sell pct 偏软区间 hi 端; 弱 → 偏 lo 端;")
    print("    - buy_qty 默认 = sell_qty (持仓中性 T+0 对冲); 不想下跳买就删掉 buy 那一项。")
    print("    - 只能在该 regime 的 upper/lower_pct_range 区间内调 pct；qty 依然为 100 整倍。")
    print("S2.5. 【LOW_DIP 检验】当 regime=LOW_DIP 时逐下验证:")
    print("    | 检查项 | 条件 | 不满足→动作 |")
    print("    | ATR衰减 | atr14% > atr5%×2 (⚠标记) | 主动收窄买入价 或→HOLD |")
    print("    | 价格支撑 | buy_price ≥ 10日最低价 | →HOLD (趋势反转) |")
    print("    | 资金确认 | 主力净流入≥0 | →HOLD (前提失效) |")
    print("S3. 【override (可选)】该只 K 线/资金面强烈反对 Python 判断时:")
    print("    - 防御档: HOLD/FLAT_DEAD/MARKET_CLOSED (放弃) | DEEP_LOSS/TAIL_EXIT/TREND_DOWN/CLOSE_RUSH (升级全卖);")
    print("    - 减仓档: HIGH_BAND (TREND_UP 主升浪默认 NO_OP, 想小幅止盈→override 到 HIGH_BAND, 软区间 [+1%,+3%], frac≤0.2);")
    print("    - 调用时加 --override <code>=<REGIME>:<原因>; 不允覆盖到激进档 (OSC_*/LOW_DIP)。")
    print("S4. 【调 Phase 2】拼一条命令 (不要的持仓不给 --order, 默认 NO_OP):")
    print("    python stockquant.py sell-plan <同样 holdings tokens> \\")
    print("      [--target-yuan 10000] \\")
    print("      --order 000949:sell:100@+1.50 --order 000949:buy:100@-1.50 \\")
    print("      --order 002324:sell:500@bid1 --override 002324=DEEP_LOSS:K线跌破年线")
    print("S5. 【读结论】Phase 2 输出 [ACTION_PLAN] 是人人可读的中文建议 + 机器可读 📍ORDER 签名行;")
    print("    有错 → Python exit 2 + ❌ 详情; 修正 --order 重跑即可.")


def _resolve_price(price, price_pct, price_type):
    """Convert price_pct/price_type into concrete limit price."""
    if price_type == "bid1":
        return round(price * 0.995, 2)
    if price_type == "current":
        return round(price, 2)
    if price_pct is not None:
        return round(price * (1 + price_pct / 100), 2)
    return None


def _validate_one_order(order):
    """Per-order syntactic validation. Returns (errs_list, normalized_dict).

    Normalized dict has fields: side, qty (lot-rounded), price_pct, price_type.
    """
    errs = []
    side = order.get("side")
    if side not in ("sell", "buy"):
        errs.append(f"side='{side}' 必须是 'sell' 或 'buy'")
        return errs, None
    qty = order.get("qty", 0)
    if not isinstance(qty, (int, float)) or qty <= 0:
        errs.append(f"qty={qty} 必须是正数")
        return errs, None
    qty_int = int(qty)
    qty_lot = _round_lot(qty_int)
    if qty_lot != qty_int:
        errs.append(f"qty={qty_int} 非 100 整数倍 (round_down→{qty_lot})")
    if qty_lot == 0:
        errs.append(f"qty={qty_int} round_down 后为 0")
        return errs, None
    price_type = order.get("price_type")
    price_pct = order.get("price_pct")
    if price_type and price_type not in ("bid1", "current"):
        errs.append(f"price_type='{price_type}' 仅支持 'bid1' 或 'current'")
    if price_type is None and price_pct is None:
        errs.append("必须提供 price_pct 或 price_type 之一")
        return errs, None
    return errs, {"side": side, "qty": qty_lot,
                  "price_pct": price_pct, "price_type": price_type}


# Action-type ↔ side compatibility (B1: symmetric guard).
_BUY_OK_ATYPES = {"RANGE_BOTH", "RANGE_BOTH_TIGHT", "LOW_BUY_ONLY"}
_SELL_OK_ATYPES = {
    "SELL_AT_CURRENT", "SELL_ALL", "PARTIAL_SELL", "SELL_AT_HIGH",
    "BREAK_EXIT", "RANGE_BOTH", "RANGE_BOTH_TIGHT",
}
# Regimes where price_pct MUST be used (price_type forbidden) — they have a
# soft pct range LLM has to soft-pick within.
_RANGE_REGIMES = {"OSC_LARGE", "OSC_SMALL", "TREND_UP", "HIGH_BAND", "LOW_DIP", "BREAKOUT_ADD"}
# Regime override whitelist (B2): LLM may only force into these defensive
# regimes. NO_OP-class means "give up" → orders MUST be []. Sell-class means
# "escalate to full exit" → orders must be sell-only with price_type=current
# /bid1 (no soft range). HIGH_BAND class is a controlled trim path used when
# Python defaults TREND_UP to NO_OP but LLM sees room for partial profit
# (small frac, single-tier, soft pct range). Anything else (e.g. override
# into LOW_DIP or OSC_*) is rejected to prevent T+0 hedging on rallies.
_OVERRIDE_NOOP = {"HOLD", "FLAT_DEAD", "MARKET_CLOSED"}
_OVERRIDE_SELL_ALL = {"DEEP_LOSS", "TAIL_EXIT", "TREND_DOWN", "CLOSE_RUSH"}
_OVERRIDE_TRIM = {"HIGH_BAND"}
_OVERRIDE_ALLOWED = _OVERRIDE_NOOP | _OVERRIDE_SELL_ALL | _OVERRIDE_TRIM


def _parse_order_token(s):
    """Parse `code:side:qty@spec` into a dict.

    spec ∈ { '+1.50', '-2.20', '1.5', 'bid1', 'current' }.
    Returns (code, order_dict) where order_dict has side/qty/price_pct/price_type.
    Raises ValueError on malformed input.
    """
    s = s.strip()
    if "@" not in s or s.count(":") < 2:
        raise ValueError(
            f"格式应为 code:side:qty@spec, got '{s}' "
            "(例: 000949:sell:300@+1.5  或  000949:sell:500@bid1)")
    head, spec = s.split("@", 1)
    parts = head.split(":")
    if len(parts) != 3:
        raise ValueError(f"head '{head}' 期望 3 段 code:side:qty")
    code, side, qty_s = parts[0].strip(), parts[1].strip().lower(), parts[2].strip()
    if not code:
        raise ValueError(f"'{s}' 缺 code")
    if side not in ("sell", "buy"):
        raise ValueError(f"'{s}' side='{side}' 必须是 sell 或 buy")
    try:
        qty = int(qty_s)
    except ValueError:
        raise ValueError(f"'{s}' qty='{qty_s}' 必须是整数")
    spec = spec.strip()
    price_pct = None
    price_type = None
    if spec in ("bid1", "current"):
        price_type = spec
    else:
        try:
            price_pct = float(spec)
        except ValueError:
            raise ValueError(
                f"'{s}' spec='{spec}' 必须是数值百分比 (如 +1.5/-2.2) 或 bid1/current")
    return code, {"side": side, "qty": qty,
                  "price_pct": price_pct, "price_type": price_type}


def _parse_override_token(s):
    """Parse `code=REGIME:reason` into (code, regime, reason)."""
    s = s.strip()
    if "=" not in s or ":" not in s.split("=", 1)[1]:
        raise ValueError(
            f"格式应为 code=REGIME:reason, got '{s}' "
            "(例: 002324=DEEP_LOSS:K线跌破年线)")
    code, rest = s.split("=", 1)
    regime, reason = rest.split(":", 1)
    code, regime, reason = code.strip(), regime.strip(), reason.strip()
    if not code or not regime or not reason:
        raise ValueError(f"'{s}' code/regime/reason 都不能为空")
    return code, regime, reason


def _validate_and_render_phase2(rows, orders_list, overrides_list, fee_floor_pct):
    """Validate LLM's --order list + --override list against per-stock regimes.

    On any ❌ → exit 2. On success → emit [ACTION_PLAN] natural-language
    suggestions + 📍ORDER signature lines (no cash gate; host module is
    responsible for cash sufficiency).
    """
    print("\n[VALIDATION]")

    # ---- Parse --order list ----
    orders_by_code = {}
    for tok in orders_list or []:
        try:
            code, od = _parse_order_token(tok)
        except ValueError as ex:
            print(f"❌ --order '{tok}' 解析失败: {ex}")
            sys.exit(2)
        orders_by_code.setdefault(code, []).append(od)

    # ---- Parse --override list ----
    overrides_by_code = {}
    for tok in overrides_list or []:
        try:
            code, regime, reason = _parse_override_token(tok)
        except ValueError as ex:
            print(f"❌ --override '{tok}' 解析失败: {ex}")
            sys.exit(2)
        overrides_by_code[code] = (regime, reason)

    rows_by_code = {r["code"]: r for r in rows}

    # ---- Coverage check: every order/override code must be a known holding ----
    for code in list(orders_by_code.keys()) + list(overrides_by_code.keys()):
        if code not in rows_by_code:
            print(f"❌ code={code} 不在 holdings 输入中 (--order / --override "
                  "只能引用 holdings token 中已声明的代码)")
            sys.exit(2)

    final_orders = []
    has_error = False
    print("| 代码 | 校验项 | 状态 | 详情 |")
    print("|---|---|:-:|---|")

    for code, row in rows_by_code.items():
        regime_info = row["regime"]
        price = row["price"]
        avail = row["avail"]
        # Regime override gate (B2: hard whitelist + required reason).
        ovr = overrides_by_code.get(code)
        override_active = ovr is not None
        regime_in_plan = ovr[0] if override_active else regime_info["regime"]
        if override_active:
            if regime_in_plan not in _OVERRIDE_ALLOWED:
                print(f"| `{code}` | regime override | ❌ | "
                      f"Python={regime_info['regime']} → LLM={regime_in_plan}; "
                      f"仅允许覆盖到防御档 {sorted(_OVERRIDE_ALLOWED)} |")
                has_error = True
                continue
            ovr_reason = ovr[1]
            print(f"| `{code}` | regime override | ⚠️ | "
                  f"Python={regime_info['regime']} → "
                  f"LLM={regime_in_plan}; reason={ovr_reason} |")
            if regime_in_plan in _OVERRIDE_NOOP:
                regime_info = dict(regime_info, regime=regime_in_plan,
                                   action_type="NO_OP",
                                   upper_pct_range=None, lower_pct_range=None,
                                   max_sell_frac=0.0, max_buy_frac=0.0,
                                   sell_ladder_hint="none",
                                   min_spread_pct=None)
            elif regime_in_plan in _OVERRIDE_TRIM:
                # HIGH_BAND: controlled partial trim with soft pct range.
                # Mirrors the natural HIGH_BAND classification spec.
                regime_info = dict(regime_info, regime=regime_in_plan,
                                   action_type="SELL_AT_HIGH",
                                   upper_pct_range=(1.0, 3.0),
                                   lower_pct_range=None,
                                   max_sell_frac=0.2, max_buy_frac=0.0,
                                   sell_ladder_hint="single",
                                   min_spread_pct=None)
            else:  # SELL_ALL class → full-exit, single-tier
                atype = ("SELL_AT_CURRENT" if regime_in_plan == "CLOSE_RUSH"
                         else "SELL_ALL" if regime_in_plan == "DEEP_LOSS"
                         else "BREAK_EXIT" if regime_in_plan == "TREND_DOWN"
                         else "SELL_AT_CURRENT")
                regime_info = dict(regime_info, regime=regime_in_plan,
                                   action_type=atype,
                                   upper_pct_range=None, lower_pct_range=None,
                                   max_sell_frac=1.0, max_buy_frac=0.0,
                                   sell_ladder_hint="single",
                                   min_spread_pct=None)
        orders = orders_by_code.get(code, [])
        # NO_OP override must come with no orders.
        if override_active and regime_in_plan in _OVERRIDE_NOOP and orders:
            print(f"| `{code}` | NO_OP override | ❌ | "
                  f"覆盖到 {regime_in_plan} 后不允许再给 --order |")
            has_error = True
            continue
        if not orders:
            print(f"| `{code}` | NO_OP | ✅ | 无 --order, 本回合不操作 |")
            final_orders.append({"code": code, "name": row["name"],
                                 "side": "NOOP", "qty": 0, "price": None,
                                 "tier": 0, "price_pct": None,
                                 "price_type": None,
                                 "regime": regime_in_plan})
            continue
        if price is None:
            print(f"| `{code}` | 缺现价 | ❌ | quote 失败, 无法解析挂价 |")
            has_error = True
            continue

        sum_sell = 0
        sell_prices, buy_prices = [], []
        rendered_for_code = []
        per_code_error = False
        for idx, raw_order in enumerate(orders, 1):
            errs, no = _validate_one_order(raw_order)
            if errs:
                for e in errs:
                    print(f"| `{code}` | order#{idx} | ❌ | {e} |")
                has_error = True
                per_code_error = True
                continue
            side = no["side"]
            qty = no["qty"]
            limit_price = _resolve_price(price, no["price_pct"], no["price_type"])
            if limit_price is None or limit_price <= 0:
                print(f"| `{code}` | order#{idx} 价格解析 | ❌ | 无法解析价格 |")
                has_error = True
                per_code_error = True
                continue
            # Range gate: if regime has upper/lower_pct_range, price_pct must be inside
            if no["price_pct"] is not None:
                pct = no["price_pct"]
                if side == "sell" and regime_info["upper_pct_range"]:
                    lo, hi = regime_info["upper_pct_range"]
                    if not (lo <= pct <= hi):
                        print(f"| `{code}` | order#{idx} sell pct={pct:+.2f}% | ❌ "
                              f"| 超出 regime upper_pct_range "
                              f"[{lo:+.2f}%, {hi:+.2f}%] |")
                        has_error = True
                        per_code_error = True
                        continue
                if side == "buy" and regime_info["lower_pct_range"]:
                    lo, hi = regime_info["lower_pct_range"]
                    if not (lo <= pct <= hi):
                        print(f"| `{code}` | order#{idx} buy pct={pct:+.2f}% | ❌ "
                              f"| 超出 regime lower_pct_range "
                              f"[{lo:+.2f}%, {hi:+.2f}%] |")
                        has_error = True
                        per_code_error = True
                        continue
            # Action-type ↔ side compatibility (B1).
            atype = regime_info["action_type"]
            if side == "buy" and atype not in _BUY_OK_ATYPES:
                print(f"| `{code}` | order#{idx} buy | ❌ | "
                      f"regime {regime_info['regime']} (action={atype}) "
                      f"不允许 buy; buy 仅在 OSC_LARGE/OSC_SMALL/LOW_DIP/BREAKOUT_ADD 下合法 |")
                has_error = True
                per_code_error = True
                continue
            if side == "sell" and atype not in _SELL_OK_ATYPES:
                print(f"| `{code}` | order#{idx} sell | ❌ | "
                      f"regime {regime_info['regime']} (action={atype}) "
                      f"不允许 sell; 该档应 orders=[] 或 override 到防御档 |")
                has_error = True
                per_code_error = True
                continue
            # B4: RANGE-class regimes forbid price_type (must use price_pct).
            if (regime_info["regime"] in _RANGE_REGIMES
                    and no["price_type"] is not None):
                print(f"| `{code}` | order#{idx} price_type | ❌ | "
                      f"regime {regime_info['regime']} 必须用 price_pct "
                      f"(在软区间内软选), 禁用 price_type='{no['price_type']}' |")
                has_error = True
                per_code_error = True
                continue

            if side == "sell":
                sum_sell += qty
                sell_prices.append(limit_price)
            else:
                buy_prices.append(limit_price)

            rendered_for_code.append({
                "code": code, "name": row["name"], "tier": idx,
                "side": side.upper(), "qty": qty, "price": limit_price,
                "price_pct": no["price_pct"], "price_type": no["price_type"],
                "regime": regime_in_plan,
            })

        # Per-code aggregate gates
        if sum_sell > avail:
            print(f"| `{code}` | T+1 校验 | ❌ | "
                  f"sum(sell qty)={sum_sell} > avail({avail}); 违反 T+1 锁仓 |")
            has_error = True
            per_code_error = True

        max_frac = regime_info["max_sell_frac"] or 0
        if (avail > 0 and sum_sell > avail * max_frac + 1e-6
                and max_frac < 1.0):
            print(f"| `{code}` | sell_frac 校验 | ❌ | "
                  f"sum_sell/avail={sum_sell}/{avail}="
                  f"{(sum_sell/avail):.2f} > max_sell_frac={max_frac} |")
            has_error = True
            per_code_error = True

        # B3: per-stock buy_frac gate (cap addon size relative to total qty).
        sum_buy = sum(o["qty"] for o in rendered_for_code if o["side"] == "BUY")
        max_bf = regime_info["max_buy_frac"] or 0
        qty_total = row["qty"]
        if (max_bf > 0 and qty_total > 0
                and sum_buy > qty_total * max_bf + 1e-6):
            print(f"| `{code}` | buy_frac 校验 | ❌ | "
                  f"sum_buy/qty={sum_buy}/{qty_total}="
                  f"{(sum_buy/qty_total):.2f} > max_buy_frac={max_bf}; "
                  f"单只加仓上限超出 |")
            has_error = True
            per_code_error = True
        if max_bf == 0 and sum_buy > 0:
            # Defensive: if regime_info says no buy quota but B1 guard let
            # buy through (e.g. unusual atype), still block here.
            print(f"| `{code}` | buy_frac 校验 | ❌ | "
                  f"regime {regime_info['regime']} max_buy_frac=0 不允许 buy |")
            has_error = True
            per_code_error = True

        # Spread gate (only when both sides exist + min_spread defined)
        min_spread = regime_info["min_spread_pct"]
        if min_spread and sell_prices and buy_prices and price > 0:
            spread = (min(sell_prices) - max(buy_prices)) / price * 100
            if spread < min_spread:
                print(f"| `{code}` | 双边差价 | ❌ | "
                      f"min(sell)-max(buy)={min(sell_prices):.2f}-"
                      f"{max(buy_prices):.2f}={spread:+.2f}% < "
                      f"fee_floor {min_spread:.2f}% |")
                has_error = True
                per_code_error = True
            else:
                print(f"| `{code}` | 双边差价 | ✅ | "
                      f"spread={spread:+.2f}% ≥ fee_floor {min_spread:.2f}% |")

        if not per_code_error:
            print(f"| `{code}` | 整体 | ✅ | sum_sell={sum_sell}/{avail}, "
                  f"orders={len(rendered_for_code)} |")
            final_orders.extend(rendered_for_code)

    if has_error:
        print("\n❌ 校验未通过, 请按以上 ❌ 逐条修正 --order / --override 后重跑")
        sys.exit(2)

    # ---- ACTION_PLAN: natural-language suggestions + machine signature ----
    print("\n[ACTION_PLAN]  (\u4eba\u4eba\u53ef\u8bfb\u4e2d\u6587\u5efa\u8bae + 📍ORDER \u673a\u5668\u53ef\u8bfb\u7b7e\u540d\u884c)")
    # group final_orders by code preserving insertion order
    by_code = {}
    for o in final_orders:
        by_code.setdefault(o["code"], []).append(o)

    for code, ords in by_code.items():
        row = rows_by_code[code]
        name = row["name"]
        price = row["price"]
        if ords and ords[0]["side"] == "NOOP":
            regime_label = row["regime"]["regime"]
            reason = row["regime"]["reason"]
            profit_pct = row.get("profit_pct")
            profit_str = f"; 盈亏 {profit_pct:+.2f}%" if profit_pct is not None else ""
            print(f"\n* `{code}` ({name}) — 现价 {price:.2f}元, regime={regime_label}{profit_str}")
            print(f"    - 不操作: {reason}")
            continue
        regime = ords[0].get("regime", row["regime"]["regime"])
        sells = [o for o in ords if o["side"] == "SELL"]
        buys = [o for o in ords if o["side"] == "BUY"]
        sell_total_value = sum(o["qty"] * o["price"] for o in sells)
        buy_total_value = sum(o["qty"] * o["price"] for o in buys)
        print(f"\n* `{code}` ({name}) — 现价 {price:.2f}元, regime={regime}:")
        for o in sells:
            offset = (f"{o['price_pct']:+.2f}%" if o.get("price_pct") is not None
                      else o.get("price_type") or "-")
            tot = o["qty"] * o["price"]
            print(f"    - **卖出 {o['qty']} 股 @ {o['price']:.2f}元** "
                  f"(现价 {offset}, 单笔总价 {tot:.0f}元)")
        for o in buys:
            offset = (f"{o['price_pct']:+.2f}%" if o.get("price_pct") is not None
                      else o.get("price_type") or "-")
            tot = o["qty"] * o["price"]
            print(f"    - **买入 {o['qty']} 股 @ {o['price']:.2f}元** "
                  f"(现价 {offset}, 单笔总价 {tot:.0f}元)")
        if sells and buys:
            net = buy_total_value - sell_total_value
            sp = (min(o["price"] for o in sells)
                  - max(o["price"] for o in buys))
            sp_pct = sp / price * 100 if price > 0 else 0
            print(f"    - 双边对冲: 卖出收回 {sell_total_value:.0f}元, "
                  f"买入支出 {buy_total_value:.0f}元, "
                  f"净{('买入' if net > 0 else '卖出' if net < 0 else '中性')} "
                  f"{abs(net):.0f}元; 差价 {sp_pct:+.2f}%")
        elif sells:
            print(f"    - 单边减仓: 卖出收回约 {sell_total_value:.0f}元")
        elif buys:
            print(f"    - 单边加仓: 买入支出约 {buy_total_value:.0f}元")

    # Machine-readable signature lines for upstream orchestration to grep.
    print("\n--- \u673a\u5668\u53ef\u8bfb\u7b7e\u540d (\u987a\u5e8f\u4e00\u884c\u4e00\u7b14) ---")
    for o in final_orders:
        if o["side"] == "NOOP":
            print(f"📍ORDER:{o['code']}:NOOP")
            continue
        print(f"📍ORDER:{o['code']}:{o['side']}:{o['qty']}"
              f"@{o['price']:.2f}")
    n_active = len([o for o in final_orders if o['side'] != 'NOOP'])
    print(f"📍ORDER_TOTAL:orders={n_active}")


# ==========================================================================
# Macro sentiment – financial news scanning for market backdrop
# ==========================================================================

# Keyword scoring for A-share market sentiment (checked against news headlines).
# Weight: -2.5 = strong negative, +2.5 = strong positive. Headlines matched
# by substring; multiple hits accumulate. Deduped across all search queries.

_MACRO_NEGATIVE = [
    ("301调查", -2.5), ("关税加征", -2.5), ("贸易战", -2.5),
    ("关税升级", -2.5), ("实体清单", -2.5), ("对华制裁", -2.5),
    ("脱钩", -2.0), ("供应链转移", -1.5),
    ("台海军演", -2.0), ("军事演习", -1.5),
    ("加息", -1.5), ("缩表", -1.0), ("通胀超预期", -1.0),
    ("人民币贬值", -1.0), ("资金外流", -1.0), ("外资撤离", -1.5),
    ("监管约谈", -1.5), ("立案调查", -2.0), ("退市风险", -2.0),
    ("IPO加速", -1.0), ("解禁潮", -1.0),
]

_MACRO_POSITIVE = [
    ("暂停关税", +2.5), ("取消关税", +2.5), ("贸易协议", +2.5),
    ("达成协议", +2.0), ("豁免关税", +2.0),
    ("降息", +2.0), ("降准", +2.0), ("LPR下调", +1.5),
    ("万亿刺激", +2.5), ("特别国债", +2.0), ("减税", +1.5),
    ("减费降税", +1.5), ("稳增长", +1.0),
    ("外资流入", +1.5), ("北向资金流入", +1.5), ("人民币升值", +1.0),
    ("回购潮", +1.0),
]


def _fetch_macro_sentiment(now=None):
    """Fetch financial news headlines and score macro sentiment.

    Uses Playwright (Edge headless) to search so.com for financial headlines,
    keyword-match them against _MACRO_NEGATIVE/_MACRO_POSITIVE, and return
    a structured block for LLM consumption.

    Returns dict with keys: score (float), signals (list), suggestions (list),
    headlines (list), error (str or None).
    """
    import json as _json, subprocess as _sp, tempfile as _tmp
    from urllib.parse import quote as _url_quote

    result = {"score": 0.0, "signals": [], "suggestions": [],
              "headlines": [], "error": None}
    now = now or datetime.datetime.now()

    # Build Playwright script — 2 targeted searches to cover:
    #   1) trade/geopolitics  2) monetary/regulatory
    queries = [
        "财经头条 特朗普 关税 301 贸易",
        "央行 货币 降息 降准 监管 立案 A股",
    ]

    try:
        js = [
            "const { chromium } = require('playwright-core');",
            "(async () => {",
            "  const browser = await chromium.launch({",
            "    executablePath: 'C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe',",
            "    headless: true, args: ['--no-sandbox']",
            "  });",
            "  const page = await browser.newPage();",
            "  await page.setExtraHTTPHeaders({",
            "    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'",
            "  });",
            "  const allR = [];",
        ]
        for i, q in enumerate(queries):
            eq = _url_quote(q)
            vn = f"items{i}"
            js.append(f"  await page.goto('https://www.so.com/s?q={eq}',"
                      f"{{ waitUntil: 'domcontentloaded', timeout: 12000 }});")
            js.append("  await page.waitForTimeout(1500);")
            js.append(f"  const {vn} = await page.evaluate(() => {{")
            js.append("    const els = document.querySelectorAll('.res-list h3 a, .result h3 a');")
            js.append("    return [...els].slice(0, 6).map(a => a.textContent.trim()).filter(Boolean);")
            js.append("  });")
            js.append(f"  allR.push(...{vn});")
        js.append("  console.log(JSON.stringify([...new Set(allR)]));")
        js.append("  await browser.close();")
        js.append("})();")

        tmpf = _tmp.NamedTemporaryFile(mode='w', suffix='.js',
                                        delete=False, encoding='utf-8',
                                        dir=_WS_DIR)
        tmpf.write('\n'.join(js))
        tmpf.close()
        try:
            proc = _sp.run(['node', tmpf.name], capture_output=True,
                          text=True, encoding='utf-8', timeout=40,
                          cwd=_WS_DIR)
        finally:
            os.unlink(tmpf.name)

        if proc.returncode != 0:
            result["error"] = f"playwright exit {proc.returncode}: {proc.stderr[:200]}"
            return result

        # Parse JSON from stdout – it's the last line or last array
        output = proc.stdout.strip()
        headlines = None
        for line in reversed(output.split('\n')):
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                try:
                    headlines = _json.loads(line)
                    break
                except _json.JSONDecodeError:
                    continue
        if not headlines:
            result["error"] = f"no json array in output: {output[:200]}"
            return result

        result["headlines"] = headlines[:30]

        # ---- Score headlines ----
        total = 0.0
        seen = {}  # kw -> {weight, snippet}
        for hl in headlines:
            for kw, w in _MACRO_NEGATIVE:
                if kw in hl and kw not in seen:
                    total += w
                    seen[kw] = {"weight": w, "snippet": hl[:100]}
            for kw, w in _MACRO_POSITIVE:
                if kw in hl and kw not in seen:
                    total += w
                    seen[kw] = {"weight": w, "snippet": hl[:100]}

        result["score"] = round(total, 1)

        for kw, v in seen.items():
            w = v["weight"]
            tag = ("强空" if w <= -2 else "偏空" if w < 0
                   else "强多" if w >= 2 else "偏多")
            result["signals"].append({
                "keyword": kw, "weight": w, "snippet": v["snippet"], "tag": tag,
            })

        # ---- Generate suggestions ----
        s = result["score"]
        if s <= -3:
            result["suggestions"] = [
                "选股: 偏防御 (医药/消费/公用), 避开出口依赖型",
                "买入: 仓位缩至 50%, 止损收紧到 -2.5%",
                "卖出: 止损阈值收紧 0.5%, 浮盈的考虑部分止盈",
                "仓位: 总仓位降到 50% 以下, 留现金等利空消化",
            ]
        elif s <= -1:
            result["suggestions"] = [
                "选股: 中性偏防御, 出口票谨慎",
                "买入: 仓位缩 30%, 等利空消化再补",
                "卖出: 止损按标准执行, 不松",
            ]
        elif s >= 3:
            result["suggestions"] = [
                "选股: 可激进, 成长型板块优先",
                "买入: 正常仓位, 可适当加量",
                "卖出: 止盈放宽, 不必急于卖",
            ]
        elif s >= 1:
            result["suggestions"] = [
                "选股: 正常, 略偏乐观", "买入: 正常仓位",
            ]
        else:
            result["suggestions"] = [
                "选股: 按正常策略, 无宏观偏向",
                "买入/卖出: 按默认规则",
            ]

    except _sp.TimeoutExpired:
        result["error"] = "search timeout"
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"

    return result


def _render_macro_sentiment(ms=None):
    """Print [MACRO_SENTIMENT] block from _fetch_macro_sentiment result."""
    if ms is None:
        ms = _fetch_macro_sentiment()

    s = ms["score"]
    emoji = "🟢" if s >= 1 else ("🔴" if s <= -1 else "🟡")
    label = ("偏多" if s >= 1 else ("偏空" if s <= -1 else "中性"))

    print("\n[MACRO_SENTIMENT] (宏观情绪快照, LLM 在所有 S 步骤前先读取)")
    print(f"  情绪得分: {emoji} {s:+.1f} ({label})")

    if ms.get("error"):
        print(f"  ⚠ 采集错误: {ms['error'][:120]}")
        print(f"  → LLM 按中性处理, 不做宏观偏向调整")
        return

    if ms.get("signals"):
        print("  关键信号:")
        for sig in ms["signals"]:
            print(f"    • {sig['snippet']} [{sig['tag']}]")
    else:
        print("  关键信号: (无重大宏观事件)")

    if ms.get("suggestions"):
        print("  建议倾向:")
        for sug in ms["suggestions"]:
            print(f"    • {sug}")


def sell_plan(holdings, target_yuan=10000.0, orders_list=None,
              overrides_list=None, fee_floor_pct=0.8):
    """Two-phase sell-plan dispatcher.

    Phase 1 (orders_list=None and overrides_list=None): emit regime classify
    + suggested default orders + soft ranges; LLM either copies the suggested
    --order tokens as-is or tweaks pct/qty within range.

    Phase 2 (orders_list non-empty OR overrides_list non-empty): validate
    against per-stock regimes (T+1 / lot-100 / pct-range / sell_frac /
    buy_frac / spread); emit natural-language [ACTION_PLAN] + 📍ORDER
    signature lines.

    Cash availability is intentionally NOT a parameter; per the策略 design,
    buy_qty defaults to sell_qty for fixed-qty hedge (T+0 反复做差价 - 持仓
    中性), so buy notional comes from sell proceeds. Host module guarantees
    cash sufficiency at order placement time.
    """
    if not holdings:
        print("❌ sell-plan 需要至少 1 个持仓参数。例:")
        print("  Phase 1: python stockquant.py sell-plan "
              "000949:1200/800@7.97 002324:500/500@17.11")
        print("  Phase 2: python stockquant.py sell-plan "
              "000949:1200/800@7.97 002324:500/500@17.11 \\")
        print("           --order 000949:sell:100@+1.5 "
              "--order 000949:buy:100@-1.5 \\")
        print("           --override 002324=DEEP_LOSS:K线跌破年线")
        return

    now = datetime.datetime.now()
    sess_meta = _compute_session_meta(now)
    rows = _build_plan_rows(holdings, now, target_yuan=target_yuan,
                            is_trading=sess_meta["is_trading"])

    is_phase2 = bool(orders_list) or bool(overrides_list)
    sep = "═" * 72
    phase = 2 if is_phase2 else 1
    print(sep)
    print(f"## SELL_PLAN  Phase {phase}/2  "
          + ("(Python 硬验证 + 出最终建议)" if is_phase2
             else "(出 regime + 默认建议 order, LLM 默认采纳)"))
    print(sep)
    _render_state_block(now, sess_meta, target_yuan, len(rows), fee_floor_pct)
    _render_macro_sentiment()
    _render_holdings_data(rows)

    if is_phase2:
        _validate_and_render_phase2(rows, orders_list or [],
                                    overrides_list or [], fee_floor_pct)
    else:
        _render_regime_classify(rows)
        _render_regime_rules()
        _render_cadence_hint(sess_meta)
        _render_phase1_task()
    print(sep)


# ==========================================================================
# `allocate` subcommand - 2nd-pass Python-formatted allocation table.
# ==========================================================================
# Flow (intended use after `recommend`):
#   1. User/LLM runs `python stockquant.py recommend --capital X ...`
#      -> outputs baseline table + writes last_allocation_ctx.json cache.
#   2. LLM performs S1~S4 (硬约束/风险复核/综合评分/精选Top5) and decides
#      a FINAL ordered code list, possibly different from baseline.
#   3. LLM calls `python stockquant.py allocate --codes C1,C2,...
#      --capital X --comment "LLM 推理理由..."`
#      -> Python looks up each code in the context cache, falls back to
#         live quote for any unknown code, applies the FIXED 10000元/只
#         allocation rule, and prints an authoritative markdown table
#         with the LLM's comment preserved verbatim above it.
#   4. LLM pastes the Python output into show_output directly (no math).
#
# This avoids LLM arithmetic mistakes (股数 / 累计 / 占比) entirely while
# still honoring LLM's qualitative risk judgment on ORDERING and INCLUSION.
# ==========================================================================

def cli_allocate(codes, capital, comment=None, per_target=10000.0):
    """Render an allocation table for the given ordered code list.

    Args:
        codes: list of stock codes in LLM-decided priority order.
        capital: total capital (RMB).
        comment: optional free-form markdown/text to echo verbatim before
            the table (typically the LLM's reasoning summary).
        per_target: fixed target RMB per stock (default 10000).
    """
    if not codes:
        print("❌ allocate: --codes 不能为空", file=sys.stderr)
        sys.exit(2)
    ctx, ctx_date = _load_allocation_context()
    ctx_items = (ctx or {}).get("items", {}) if ctx else {}
    enriched = []
    missing_codes = []
    stale_ctx_date = None
    today = datetime.datetime.now().strftime("%Y%m%d")
    if ctx_date and ctx_date != today:
        stale_ctx_date = ctx_date                          # note in header
    for code in codes:
        cached = ctx_items.get(code)
        if cached and cached.get("price"):
            enriched.append({
                "code": code,
                "name": cached.get("name") or code,
                "strategy": cached.get("strategy", "-"),
                "price": cached.get("price"),
                "stop_profit": cached.get("stop_profit"),
                "stop_loss": cached.get("stop_loss"),
                "industry": cached.get("industry", "-"),
                "score": cached.get("score", "-"),
                "next_day_prob": cached.get("next_day_prob", "-"),
            })
            continue
        # Cache miss: live quote + default stops (±5%).
        missing_codes.append(code)
        q = query_quote(code)
        price = q.get("price") if q else None
        if not price:
            print(f"WARN: allocate: {code} 无现价, 跳过", file=sys.stderr)
            continue
        enriched.append({
            "code": code,
            "name": q.get("name", code),
            "strategy": "-",
            "price": price,
            "stop_profit": round(price * 1.05, 2),
            "stop_loss": round(price * 0.95, 2),
            "industry": "-",
            "score": "-",
            "next_day_prob": "-",
        })
    if not enriched:
        print("❌ allocate: 所有代码都无法取价, 终止", file=sys.stderr)
        sys.exit(2)
    plan = _build_allocation_plan(enriched, capital, per_target=per_target)
    # Prepend cache status so LLM sees whether the numbers are fresh.
    note_bits = ["LLM 精选后 Python 整理", "按优先级顺序"]
    if stale_ctx_date:
        note_bits.append(f"⚠️ 上下文来自 {stale_ctx_date}, 非当日")
    if missing_codes:
        note_bits.append(f"⚠️ {len(missing_codes)} 只 cache 缺失, 止盈/损用±5%默认")
    _render_allocation_markdown(
        plan, capital,
        title_note=", ".join(note_bits),
        comment=comment,
    )
    # Echo footer with operational hint so LLM/human knows next step.
    print("\n---")
    print("> 上表由 `stockquant.py allocate` 生成, 直接粘到 show_output 作为 S5 操作表.")

    # ------ Machine-friendly handoff lines for the agent runtime ------
    # The LLM's failure mode (observed: 2026-04-27 case) is to "decide" the
    # PICKED list itself by re-sorting [DATA] by score DESC -- bypassing the
    # full PASS_TOP10 → S2.5 risk → S3 final_score → allocate filter chain.
    # By emitting an explicit copy-this-line marker right at the tail of
    # allocate output, we downgrade the LLM task from "rank/select" to
    # "locate-and-copy" -- a retrieval task it handles much more reliably.
    plan_items = plan.get("items") or []
    if plan_items:
        codes_pipe = "|".join(it["code"] for it in plan_items)
        shares_pipe = "|".join(f"{it['code']}={it['shares']}"
                               for it in plan_items)
        used = plan.get("used", 0)
        rem = plan.get("remaining_cash", 0)
        print()
        print("📎PICKED:" + codes_pipe
              + "    # ← LLM 必须把这一行原样写入 fact.PICKED；禁止改顺序/增删/重排")
        print("📋BUY_PLAN_SHARES:" + shares_pipe
              + "    # ← 下单时各只 shares 直接抄此处，禁止手算")
        print(f"📋BUY_PLAN_TOTAL:used={used:.0f}元 "
              f"remaining_cash={rem:.0f}元 picks={len(plan_items)}只")
    else:
        # Empty plan path: still emit a PICKED:0 marker so downstream knows
        # this branch is not "agent forgot to copy" but "no eligible items".
        print()
        print("📎PICKED:    # 空：本次无可分配候选（资金不足或单手>半仓全部跳过）")
        print("📋BUY_PLAN_TOTAL:used=0元 picks=0只 → 不入场")


# ==========================================================================
# analyze: per-stock comprehensive snapshot for LLM consumption
# ==========================================================================
# Pure data interface: emits structured markdown blocks (basics, today's
# quote, daily-K position, 15min-K features, fund flow, sector context,
# announcements) for each requested ticker. The LLM combines these with the
# user's prompt to produce its own analysis -- we do NOT prescribe actions.
#
# Accepts 6-digit codes OR Chinese names (full / abbrev). Unresolved names
# are echoed under a "未匹配" tail section so the LLM can ask the user to
# clarify without aborting the whole run.
# ==========================================================================

def _resolve_query_to_code(query, market_index):
    """Resolve a user query to a 6-digit A-share code.

    Matching priority (stops at first hit):
      1. Pure 6-digit numeric  -> treat as code; name looked up from index.
      2. Exact name match      -> row whose `name` == query.
      3. Substring fuzzy       -> rows whose `name` contains the query;
                                  prefer shortest name (most specific),
                                  tie-break by code.
    Returns (code, name) or (None, None) when nothing matches.
    """
    q = (query or "").strip()
    if not q:
        return None, None
    if q.isdigit() and len(q) == 6:
        row = market_index.get(q)
        return q, (row.get("name", "") if row else "")
    exact = None
    fuzzy = []
    for code, row in market_index.items():
        nm = row.get("name") or ""
        if not nm:
            continue
        if nm == q:
            exact = (code, nm)
            break
        if q in nm:
            fuzzy.append((code, nm))
    if exact:
        return exact
    if fuzzy:
        fuzzy.sort(key=lambda x: (len(x[1]), x[0]))
        return fuzzy[0]
    return None, None


def _fmt_money(n):
    """Format a CNY amount with sign and 亿/万 unit. Returns '0' for 0/None."""
    if n is None or n == 0:
        return "0"
    sign = "+" if n > 0 else ""
    absn = abs(n)
    if absn >= 1e8:
        return f"{sign}{n/1e8:.2f} 亿"
    if absn >= 1e4:
        return f"{sign}{n/1e4:.1f} 万"
    return f"{sign}{n:.0f}"


def _downsample_kline(rows, recent=20, mid=60, stride_mid=2, stride_far=5):
    """Progressive downsampling: near-term dense, far-term sparser.

    Mental model for a typical analyze call with 120 daily bars:
      dist_from_end < 20          -> keep every bar      (~1 month daily)
      20 <= dist_from_end < 60    -> keep every 2nd bar  (1-3 month, half-weekly)
      dist_from_end >= 60         -> keep every 5th bar  (3+ month, weekly)

    Rationale: recent price action matters bar-by-bar for tactical entries;
    older history only contributes trend / S-R context, which a weekly
    skeleton captures without burning LLM context.

    Args:
      rows: ASC-ordered kline rows; last element = most recent bar.
      recent: bars within this distance from the end are kept in full.
      mid: bars within [recent, mid) are kept every `stride_mid`-th.
      stride_mid / stride_far: stride for the 2nd / 3rd tier.

    Returns the downsampled list (ASC). Empty input -> empty output.
    """
    if not rows:
        return []
    n = len(rows)
    out = []
    for i, r in enumerate(rows):
        dist = n - 1 - i                                   # 0 = most recent
        if dist < recent:
            keep = True
        elif dist < mid:
            keep = ((dist - recent) % stride_mid == 0)
        else:
            keep = ((dist - mid) % stride_far == 0)
        if keep:
            out.append(r)
    return out


def _session_label_now():
    """Coarse Beijing-time session tag for the analyze header."""
    now = datetime.datetime.now()
    if now.weekday() >= 5:
        return "weekend (non-trading)"
    hm = now.hour * 60 + now.minute
    if hm < 9 * 60 + 15:
        return "pre-open"
    if hm < 9 * 60 + 30:
        return "call-auction"
    if hm < 11 * 60 + 30:
        return "AM-session"
    if hm < 13 * 60:
        return "lunch-break"
    if hm < 15 * 60:
        return "PM-session"
    if hm < 15 * 60 + 30:
        return "close-rush"
    return "after-close"


def analyze(queries, include_news=True, days=120, minutes=32,
            no_sample=False, compact=False):
    """Emit comprehensive per-stock snapshots for LLM consumption.

    Args:
      queries: list of user inputs -- 6-digit codes / Chinese names.
      include_news: when False, skips announcement fetch (faster by ~1s/stock).
      days: daily-K window fetched (default 120 = ~half year). Hard-capped at 240.
      minutes: 15min-K bar count (default 32 = 2 trading days).
      no_sample: when True, print all `days` raw daily bars (no downsampling).
      compact: when True, revert to the old summary view (MA + last-5 bars
               + minute features only) -- useful for small-context models.
    """
    days = max(5, min(days, 240))
    minutes = max(5, min(minutes, 80))
    if not queries:
        print("❌ analyze 需要至少 1 个查询（代码或名称）。例:")
        print("   python stockquant.py analyze 600519 000001 茅台 比亚迪")
        return

    # ---- Step 1: market-list builds the name->code index ----
    # Skip tier-3 sina fallback here -- it's a 15s probe that only buys us
    # name matching, and we'd rather fail name matching loudly than make
    # the user wait 15s on every analyze call in a flaky-network window.
    mlist = []
    try:
        mlist = get_market_list(use_cache=True,
                                allow_default_sina_fallback=False)
    except Exception as e:
        print(f"⚠️ 市场列表获取失败 ({type(e).__name__})；"
              f"名称匹配降级为仅代码匹配",
              file=sys.stderr)
    mindex = {r["code"]: r for r in mlist if r.get("code")}

    # ---- Step 2: resolve queries ----
    # Dedup by resolved code: if multiple inputs hit the same ticker
    # (e.g. both "600519" and "茅台"), keep only the first so the report
    # doesn't show the same stock twice. Order of first-hit preserved.
    resolved = []          # [(original_query, code, name)]
    unresolved = []
    seen_codes = set()
    for q in queries:
        code, name = _resolve_query_to_code(q, mindex)
        if not code:
            unresolved.append(q)
            continue
        if code in seen_codes:
            print(f"INFO: query '{q}' resolves to {code} (already included); skip dup",
                  file=sys.stderr)
            continue
        seen_codes.add(code)
        resolved.append((q, code, name))

    if not resolved:
        print("❌ 所有查询均无法解析为 A 股代码：")
        for q in unresolved:
            print(f"  - \"{q}\"")
        print("提示：支持 6 位代码、完整名称（如 \"贵州茅台\"）、"
              "或包含关键词的简称（如 \"茅台\"）")
        return

    codes = [c for _, c, _ in resolved]

    # ---- Step 3: parallel batch fetches (all cached) ----
    # Quotes (today's intraday snapshot with turnover/flow/industry)
    quotes = {}
    try:
        qrows = get_market_quotes(codes)
        quotes = {r["code"]: r for r in qrows}
    except Exception as e:
        print(f"⚠️ 行情抓取失败 ({type(e).__name__})；仅使用 market-list 行情",
              file=sys.stderr)
    # Fill gaps from the market-list snapshot (may be up to 5min stale).
    for code in codes:
        if code not in quotes and code in mindex:
            quotes[code] = mindex[code]

    # Fetch `days` of daily bars so downsampling has enough far-term history.
    # 15min bars: use `minutes` (user-configurable); 60min bars: fixed 16
    # (1 trading day) since only compute_minute_features needs them.
    dklines = get_daily_klines_batch(codes, n=days) or {}
    m15 = get_minute_klines_batch(codes, klt=15, n=minutes) or {}
    m60 = get_minute_klines_batch(codes, klt=60, n=16) or {}

    # Industry-sector rank (pct + main-inflow for each sector).
    ind_rank = []
    try:
        ind_rank = get_sector_rank("industry", top=100, use_cache=True,
                                   fail_safe=True)
    except Exception:
        pass
    ind_map = {}
    for i, s in enumerate(ind_rank):
        ind_map[s.get("name", "")] = (s, i + 1)

    # Multi-day fund flow (5d/10d main inflow accumulated).
    mdflow = {}
    try:
        mdf_rows = get_multiday_fund_flow(use_cache=True)
        mdflow = {r["code"]: r for r in mdf_rows}
    except Exception:
        pass

    # Major indexes snapshot.
    overview = []
    try:
        overview = get_market_overview(use_cache=True)
    except Exception as e:
        print(f"⚠️ 大盘概览获取失败 ({type(e).__name__})", file=sys.stderr)

    # ---- Step 4: render ----
    now = datetime.datetime.now()
    print("═══ 大盘背景 ═══")
    print(f"时间: {now:%Y-%m-%d %H:%M}  |  session: {_session_label_now()}")
    if overview:
        for r in overview:
            pct = r.get("pct", 0) or 0
            sgn = "+" if pct >= 0 else ""
            print(f"- {r.get('name','?')} ({r.get('code','?')}): "
                  f"{r.get('price','?')}  {sgn}{pct}%")
    else:
        print("- (大盘数据不可用)")
    print()

    _render_macro_sentiment()

    for q, code, name in resolved:
        qt = quotes.get(code) or {}
        shown_name = name or qt.get("name") or "?"
        print(f"═══ 个股: {shown_name} ({code}) ═══")
        # Echo the raw query when it differs from both code and matched
        # name -- helps the LLM verify it hit the right ticker.
        if q != code and q != shown_name:
            print(f"(查询词 \"{q}\" 模糊匹配到 {shown_name})")
        print()

        # 4.1 Basics
        industry = qt.get("industry") or "-"
        concept = (qt.get("concept") or "").strip()
        total_mv = qt.get("total_mv") or 0
        float_mv = qt.get("float_mv") or 0
        pe = qt.get("pe")
        print("[基本]")
        print(f"- 行业: {industry}")
        if concept:
            print(f"- 概念: {concept[:120]}")
        mv_parts = []
        if total_mv:
            mv_parts.append(f"总市值 {total_mv/1e8:.1f} 亿")
        if float_mv:
            mv_parts.append(f"流通 {float_mv/1e8:.1f} 亿")
        if pe is not None and pe != 0:
            mv_parts.append(f"PE(TTM) {pe:.1f}")
        if mv_parts:
            print("- " + " | ".join(mv_parts))
        print()

        # 4.2 Today's quote
        print("[今日行情]")
        price = qt.get("price")
        pct = qt.get("pct")
        if price is None:
            print("- 无行情 (停牌 / 退市 / 数据源异常)")
        else:
            sgn = "+" if (pct or 0) >= 0 else ""
            print(f"- 现价 {price}  {sgn}{pct}%")
            print(f"- 开 {qt.get('open','-')}  高 {qt.get('high','-')}  "
                  f"低 {qt.get('low','-')}  昨收 {qt.get('prev_close','-')}")
            vol = qt.get("vol") or 0
            amt = qt.get("amount") or 0
            bits = [f"成交 {vol/1e4:.1f} 万手 / {amt/1e8:.2f} 亿"]
            if qt.get("turnover"):
                bits.append(f"换手 {qt['turnover']:.2f}%")
            if qt.get("amplitude"):
                bits.append(f"振幅 {qt['amplitude']:.2f}%")
            if qt.get("volume_ratio"):
                bits.append(f"量比 {qt['volume_ratio']:.2f}")
            print("- " + " | ".join(bits))
        print()

        # 4.3 Daily K-line: raw series + MA summary
        # Default: progressive downsampling (recent dense, far sparse).
        # With --no-sample: emit all `days` raw bars.
        # With --compact: emit only last 5 raw bars (old summary behavior).
        # NOTE: the daily-K cache key is stored without `n`, so an earlier
        # call with larger `n` can leave more rows in cache than the user
        # asked for on this call -- slice to honour --days deterministically.
        drows = dklines.get(code) or []
        if drows and len(drows) > days:
            drows = drows[-days:]
        if compact:
            header = f"[日 K 摘要 (近 5 日 + 指标)]"
        elif no_sample:
            header = f"[日 K 原始序列 (近 {len(drows)} 日, 无采样)]"
        else:
            header = (f"[日 K 序列 (近 {len(drows)} 日, 采样规则: "
                      f"20 日内每天 / 20-60 日每 2 天 / 60+ 日每 5 天)]")
        print(header)
        if drows:
            closes = [float(r["close"]) for r in drows]
            highs = [float(r["high"]) for r in drows]
            lows = [float(r["low"]) for r in drows]
            cur = closes[-1]

            def _ma(k):
                return sum(closes[-k:]) / k if len(closes) >= k else None

            ma5, ma10, ma20, ma60 = _ma(5), _ma(10), _ma(20), _ma(60)

            def fv(v):
                return f"{v:.2f}" if v is not None else "-"

            print(f"- MA5/10/20/60: {fv(ma5)} / {fv(ma10)} / {fv(ma20)} / {fv(ma60)}")
            lo, hi = min(lows), max(highs)
            if hi > lo:
                pos = (cur - lo) / (hi - lo) * 100
                print(f"- {len(drows)}日区间 [{lo:.2f} ~ {hi:.2f}]  "
                      f"当前位置 {pos:.0f}% 分位")
            tags = []
            if ma5 is not None:
                tags.append("站上 MA5" if cur > ma5 else "跌破 MA5")
            if ma5 is not None and ma20 is not None:
                tags.append("MA5>MA20 (多头)" if ma5 > ma20 else "MA5<MA20 (空头)")
            if ma20 is not None and ma60 is not None:
                tags.append("MA20>MA60" if ma20 > ma60 else "MA20<MA60")
            if tags:
                print(f"- 趋势: {' / '.join(tags)}")

            # Decide which rows to emit.
            if compact:
                emit_rows = drows[-5:]
                label = "近 5 日"
            elif no_sample:
                emit_rows = drows
                label = f"OHLCV 序列 {len(emit_rows)} 根"
            else:
                emit_rows = _downsample_kline(drows)
                label = f"OHLCV 序列 (采样后 {len(emit_rows)}/{len(drows)} 根)"

            print(f"- {label}:")
            for r in emit_rows:
                d = r["date"]
                op = float(r["open"]) or 0
                pct_r = ((float(r["close"]) - op) / op * 100) if op else 0
                sgn = "+" if pct_r >= 0 else ""
                print(f"    {d}  O{r['open']} H{r['high']} L{r['low']} "
                      f"C{r['close']}  {sgn}{pct_r:.2f}%  "
                      f"vol {int(r.get('vol', 0)):,}")
        else:
            print("- (日 K 数据不可用)")
        print()

        # 4.4 15-minute K-line: full raw series + minute features
        # 15min bars are cheap (32 rows ~= 2.4KB), no downsampling needed.
        # `--compact` reverts to the last-5-bars summary.
        kl15 = m15.get(code) or []
        kl60 = m60.get(code) or []
        if compact:
            print("[15 分钟 K 摘要 (最后 5 根 + 特征)]")
        else:
            print(f"[15 分钟 K 原始序列 (近 {len(kl15)} 根 ~= {len(kl15)//16} 交易日)]")
        if kl15:
            emit_m = kl15[-5:] if compact else kl15
            for r in emit_m:
                # ts like '2026-04-23 14:30:00' -> 'MM-DD HH:MM' for clarity
                # across multi-day 15min series.
                ts_full = r.get("ts", "")
                if len(ts_full) >= 16:
                    tm = ts_full[5:16]                     # 'MM-DD HH:MM'
                else:
                    tm = ts_full
                print(f"    {tm}  O{r['open']} H{r['high']} L{r['low']} "
                      f"C{r['close']}  vol {int(r.get('vol', 0)):,}")
            try:
                feats = compute_minute_features(kl60, kl15)
                active = [f"{k}={v}" for k, v in feats.items() if v is not None]
                if active:
                    print("- 特征: " + " | ".join(active))
            except Exception as e:
                print(f"- 特征计算失败 ({type(e).__name__})")
        else:
            print("- (15 分钟 K 不可用)")
        print()

        # 4.5 Fund flow
        print("[资金面]")
        inflow_today = qt.get("main_inflow")
        if inflow_today is not None:
            print(f"- 今日主力净流入: {_fmt_money(inflow_today)}")
        md = mdflow.get(code)
        if md:
            if md.get("main_inflow_5d") is not None:
                pct5 = md.get("main_inflow_pct_5d") or 0
                print(f"- 5 日累计主力: {_fmt_money(md['main_inflow_5d'])}"
                      f"  ({pct5:+.2f}% of 流通)")
            if md.get("main_inflow_10d") is not None:
                print(f"- 10 日累计主力: {_fmt_money(md['main_inflow_10d'])}")
            if md.get("pct_5d") is not None:
                print(f"- 5 日涨幅: {md['pct_5d']:+.2f}%  "
                      f"10 日: {md.get('pct_10d', 0):+.2f}%")
        elif inflow_today is None:
            print("- (资金面数据不可用)")
        print()

        # 4.6 Sector context (industry only; concept sectors are noisier)
        print("[板块]")
        if industry and industry in ind_map:
            s, rank = ind_map[industry]
            pct_s = s.get("pct", 0) or 0
            sgn = "+" if pct_s >= 0 else ""
            total = len(ind_rank)
            print(f"- 行业: {industry}  今日 {sgn}{pct_s:.2f}%  "
                  f"排名 {rank}/{total}")
            leader = s.get("leader_name")
            lp = s.get("leader_pct")
            if leader:
                print(f"  领涨: {leader}  "
                      f"({(lp or 0):+.2f}%)")
            inflow_s = s.get("main_inflow")
            if inflow_s is not None:
                print(f"  板块资金: {_fmt_money(inflow_s)}")
        elif industry and industry != "-":
            print(f"- 行业: {industry}  (板块排名未命中缓存)")
        print()

        # 4.7 Announcements + bad-news check (opt-out via --no-news)
        if include_news:
            print("[公告 / 新闻 (近 15 条)]")
            try:
                anns = _fetch_announcements(code, page_size=20)
            except Exception as e:
                anns = []
                print(f"- 公告接口失败 ({type(e).__name__})")
            if anns:
                for a in anns[:15]:
                    d = (a.get("notice_date") or "")[:10]
                    t = (a.get("title") or "")[:70]
                    print(f"- {d}  {t}")
            else:
                print("- (无近期公告)")
            try:
                bad, matched = has_bad_news(code, days=7)
                if bad:
                    print(f"- ⚠️ 7 日内负面标题命中: {matched}")
                else:
                    print("- ✅ 7 日内无负面新闻命中")
            except Exception:
                pass
            print()

    # ---- Step 5: unresolved list (always last, highly visible) ----
    if unresolved:
        print("═══ 未匹配查询 ═══")
        for q in unresolved:
            print(f"- \"{q}\" 未匹配到 A 股；请确认拼写或改用 6 位代码")
        print()

    # ---- Step 6: ANALYSIS_HINT -- tell the LLM how to read all of the above.
    # Progressive-disclosure principle: SKILL.md only says "invoke analyze",
    # the interpretation framework lives alongside the data so it's always
    # in-context when the LLM needs it and never burdens skill discovery.
    print("═══ ANALYSIS_HINT (LLM 解读指南) ═══")
    print("""
[多维交叉原则]
任一单一维度都不足以下结论。按"趋势 × 节奏 × 驱动 × 博弈"四维联动交叉验证：
  - 趋势(日K):  均线排列 + 位置分位 + 近期 tape 量价 → 上涨/下跌/震荡
  - 节奏(15min): 最后若干根的量价 + 60m_trend/15m_end_strength 等特征 → 当下进/出窗口
  - 驱动(资金+板块+公告): 主力连续性 + 板块共振 + 公告基本面 → 动能是否可持续
  - 博弈(腹黑): 利益方图谱 + 信息不对称 + 异常归因(who benefits) + 动机行为一致性 → 幕后意图

[各数据块怎么看]
- [基本]      行业 / 概念决定了它被放在哪个板块轮动里；PE 极端值(>80 或 <0) 是风险信号
- [今日行情]  换手率 < 1% 滞涨、2%~5% 健康、>10% 过热；量比 > 2 今日资金关注异常
- [日 K 序列] MA 多头排列(5>10>20>60)+站上 MA20 = 强势；60 日位置 >80% 分位 = 高位注意回调，<20% = 低位关注反弹；tape 看"放量突破/缩量回调/放量滞涨"经典形态
- [15 分钟 K] 盘中决策主要看这段。放量突破 15min 前高 = 动能上；跌破 15min 低点 = 动能下；尾盘 14:30 后放量是次日延续信号
- [资金面]    今日流入 + 5 日累计 + 10 日累计 三档连续正 = 主力真建仓；只今日正 5/10 日负 = 可能只是短线
- [板块]      板块排名 Top10 + 个股跟涨 = 强势共振；板块强但个股跟不上 = 掉队标的；板块弱个股强 = 龙头(注意风险集中)
- [公告/新闻] 负面命中(问询函/减持/业绩预警/立案调查) → 降低所有做多结论的置信度，通常直接 avoid；正面催化(新业务/大订单/子公司挂牌) → 加分但不改变基本面定性

[腹黑分析（幕后博弈）—— 必做！]
核心问题："当前价格水平上，谁想让你买？谁想让你卖？为什么？"

按以下通用博弈框架推导，不预设具体场景，适用于任何个股：

Step A — 利益相关方图谱
  扫描 [公告/新闻] 列表，识别所有利益方：大股东、高管、定增对象、机构投资者、游资、散户
  对每一方在当前价格水平上判断：他们希望涨还是跌？有能力影响价格吗？

Step B — 信息不对称分析
  把 [公告/新闻] 按时间排序，与 [日K序列] 的涨跌节点对齐
  找：公告日期前后 3 个交易日内是否有异常的涨跌/放量？
  判断：是"消息提前反应"（信息泄漏）还是"消息后反应"（市场消化）？
  特别关注：利好发布前涨 = 配合出货嫌疑；利空发布前跌 = 知情出逃嫌疑

Step C — 异常归因（who benefits）
  扫描 [日K序列] 和 [资金面] 中出现的每一项异常：
    - 单日天量（>2倍均量）→ 当天谁在买谁在卖？次日走势确认方向
    - 资金连续流入但股价横盘/微跌 → 吸筹（低位）还是托市（高位）？
    - 资金大幅流出但股价不跌甚至涨 → 谁在接盘？
    - PE 极端值/分位极端值 → 估值是"真便宜"还是"周期顶部的假便宜"？
  对每一项异常反问：这个异常的受益者是谁？

Step D — 动机-行为一致性检验
  对比公告中的"官方说法"和实际价格行为是否一致：
    - 公告说"业绩向好"，但高管在减持 → 言行不一，信减持
    - 公告说"回购彰显信心"，但回购量极小 → 做样子
    - 公告密集期 + 股价高位 → "利好轰炸"配合出货
  不一致 = 风险信号，一致 = 可信度加分

[腹黑分析输出格式]
对每只分析标的，输出 2~4 条"博弈剧本"，每条含：
  - 剧本名称（自由命名，反映核心博弈逻辑）
  - 概率估计（基于证据强度，各剧本概率之和≤100%）
  - 关键证据（引用具体公告日期/资金数字/K线形态，必须来自 Python 输出数据）
  - 对做多/做空决策的影响（利好/利空/中性）

[未来走势分析三步走]
1. 先定性: 日 K 趋势是 上涨 / 下跌 / 震荡？(看 MA 排列 + 位置分位 + 60 日区间)
2. 再看节奏: 15min 级别当前位置处在 "启动 / 加速 / 顶背离 / 高位震荡 / 破位" 的哪一段？
3. 最后看驱动: 资金面 + 板块 + 公告是否支撑当前趋势？不支撑就是虚涨/恐慌杀跌

[常见用户意图的回答套路]
- "能不能买 X"      → 按多维给 [支持多的证据] / [支持空的证据] / [中性] 三类证据分别列出；不给是否买的硬结论，让用户权衡
- "X 走势怎么看"    → (1) 定性一句话; (2) 近 N 日关键行为(突破/回踩/放量); (3) 支撑 / 阻力位(MA20, 60 日高/低, 前期密集成交区); (4) 触发场景: 站稳 X 看 Y / 跌破 X 看 Z
- "持有的能不能拿"  → 趋势未破 + 公告无利空 + 资金未大流出 = 可持; 任一破坏 = 减仓预警
- "对比 X 和 Y"     → 逐维度打分(趋势/节奏/驱动/公告/腹黑) 对比表，突出差异项
- "从腹黑角度分析"  → 按 [腹黑分析] Step A~D 博弈框架排查 + 输出剧本列表
- "今天是否推荐买入"→ 综合趋势+60m_15m节奏+腹黑风险+获利预测概率给出判断

[获利预测标准格式]
每次分析给出三种场景的概率和空间：
  - 场景A(乐观): 概率X%，目标价Y，获利Z%，触发条件___
  - 场景B(中性): 概率X%，目标价Y，获利Z%，触发条件___
  - 场景C(悲观): 概率X%，目标价Y，获利Z%，触发条件___
概率之和=100%。概率分配必须基于数据（均线位置/资金方向/分位/公告），不能拍脑袋。

[横向对比标准格式]
多只股票对比时，用一个 Markdown 对比表。列由 LLM 根据当前标的实际情况灵活选取，建议包含以下核心维度（不强制全列，根据数据可用性增减）：
  核心列：股票 | PE | 市值 | 120日分位 | MA排列 | 近期涨幅 | 主力资金
  风险列：选择当前标的最突出的1-2个风险维度（如减持/解禁/锁仓比例/商誉/质押等）
  催化列：选择当前标的最突出的1-2个催化维度（如新品/政策/并购/板块轮动等）
末尾给出优先级排序 + 仓位建议 + 每只一句话定性。

[硬纪律]
- 禁止脑算均线 / 涨跌幅 / 分位，全部引用 Python 输出的数字
- 所有结论必须给依据(引用具体字段 + 数值), 不做无依据的定性判断
- 用户没明说时间周期就默认"短中期 1-4 周"视角
- 腹黑分析必须有公告/资金/K线的具体数据支撑，不能纯猜测
- 对比分析必须用表格呈现，不能大段文字糊过去""")


# ==========================================================================
# CLI
# ==========================================================================

def _build_cli():
    p = argparse.ArgumentParser(
        prog="stockquant.py",
        description="A-share trading all-in-one (quotes / k-line / picker / sell-plan)."
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("market", help="Overview of major A-share indexes.")

    s = sub.add_parser("sector-rank", help="Industry / concept sector ranking.")
    s.add_argument("--type", choices=["industry", "concept", "region"], default="industry")
    s.add_argument("--top", type=int, default=20)

    for k, desc in [("zt-pool", "涨停池"), ("dt-pool", "跌停池"),
                    ("zb-pool", "炸板池"), ("lb-pool", "连板池")]:
        z = sub.add_parser(k, help=desc)
        z.add_argument("--date", help="YYYYMMDD (default today)")

    # ---- Strategy C: laggard in hot sectors ----
    sc = sub.add_parser("screen-c",
                        help="Strategy C: laggard stocks inside top-5 hot sectors.")
    sc.add_argument("--market", default="all", choices=list(_MARKET_FS_MAP.keys()))
    sc.add_argument("--board-top", type=int, default=5,
                    help="Number of hottest sectors to scan (default 5)")
    sc.add_argument("--board-days", type=int, default=5,
                    help="Sector lookback in trading days (default 5)")
    sc.add_argument("--laggard-pct", type=float, default=0.40,
                    help="Bottom X%% of sector is the laggard pool (default 0.40)")

    # ---- Strategy D: multi-day main-capital accumulation ----
    sd = sub.add_parser("screen-d",
                        help="Strategy D: multi-day main-capital accumulation.")
    sd.add_argument("--market", default="all", choices=list(_MARKET_FS_MAP.keys()))
    sd.add_argument("--flow-days", type=int, default=5,
                    help="Cumulative main-inflow window (default 5)")
    sd.add_argument("--no-ma-alignment", action="store_true",
                    help="Skip the close>=MA20>=MA40>=MA60 alignment check")

    # ---- Strategy E: 60-day box breakout ----
    se = sub.add_parser("screen-e",
                        help="Strategy E: 60-day narrow-box breakout.")
    se.add_argument("--market", default="all", choices=list(_MARKET_FS_MAP.keys()))
    se.add_argument("--box-days", type=int, default=60)
    se.add_argument("--box-range-max", type=float, default=25.0,
                    help="Max 60-day high/low gap %% (default 25)")
    se.add_argument("--sample", type=int, default=None,
                    help="Debug: only scan N random codes (rate-limit safety)")

    r = sub.add_parser("recommend", help="One-shot: screen + score + sizing.")
    r.add_argument("--capital", type=float, default=10000)
    r.add_argument("--market", default="all", choices=list(_MARKET_FS_MAP.keys()))
    r.add_argument("--strategy", default="C,F1,F2,F3",
                   help="Comma list: subset of C/E/F1/F2/F3 "
                        "(default C,F1,F2,F3; D deprecated as trailing signal)")
    r.add_argument("--threshold", type=float, default=5.0,
                   help="Target profit %% (default 5)")
    r.add_argument("--top", type=int, default=8,
                   help="Max candidates to return (default 8; kept small so "
                        "LLM can cross-verify each pick in depth)")
    r.add_argument("--min-trade", type=float, default=5000,
                   help="Min trade value to avoid high fee ratio (default 5000)")
    r.add_argument("--no-check-news", action="store_true",
                   help="Skip announcement bad-news scan (faster, less safe)")
    r.add_argument("--max-per-sector", type=int, default=2,
                   help="Max picks per industry sector in final Top-N "
                        "(default 2; 0 disables diversification)")
    r.add_argument("--stop-loss-pct", type=float, default=3.5,
                   help="Stop-loss %% below entry price (default 3.5)")
    r.add_argument("--max-position-per-stock-pct", type=float, default=40.0,
                   help="Max per-stock exposure as %% of capital (default 40)")
    r.add_argument("--e-sample", type=int, default=None,
                   help="Strategy E debug-only sample size (rate-limit safety)")
    r.add_argument("--no-log", action="store_true",
                   help="Skip appending this run to logs/recommend/YYYYMMDD.jsonl")

    # brief: one-shot LLM-friendly aggregate of market + sector-rank + recommend.
    br = sub.add_parser(
        "brief",
        help="One-shot aggregate for LLM: market + sector-rank + recommend."
    )
    br.add_argument("--capital", type=float, default=10000,
                    help="Available capital (default 10000)")
    br.add_argument("--market", default="main",
                    choices=list(_MARKET_FS_MAP.keys()),
                    help="Market scope (default main = Shanghai/Shenzhen main board)")
    br.add_argument("--top", type=int, default=8,
                    help="Number of recommend candidates to return (default 8)")
    br.add_argument("--strategy", default="C,F1,F2,F3",
                    help="Comma list: subset of C/E/F1/F2/F3 "
                         "(default C,F1,F2,F3)")

    # eval: post-hoc evaluation of previous day's recommendations
    e = sub.add_parser("eval",
                       help="Evaluate previous trading day's recommendations "
                            "against next-day actual outcome.")
    e.add_argument("--date", help="YYYYMMDD (default: last trading day)")

    # intraday-track: live quality-check of today's recommend snapshot
    it = sub.add_parser("intraday-track",
                        help="Compare TODAY's recommend snapshot against "
                             "current quote; show stop-profit/loss hits.")
    it.add_argument("--date", help="YYYYMMDD (default: today)")

    # stats: aggregate metrics over the last N days of eval logs
    st = sub.add_parser("stats",
                        help="Aggregate strategy performance over recent eval logs.")
    st.add_argument("--days", type=int, default=30,
                    help="Lookback calendar days (default 30)")

    # ------ merged-in from legacy `stock` skill ------
    q = sub.add_parser("quote", help="Real-time quote (EM / Sina fallback).")
    q.add_argument("codes", nargs="+", help="One or more stock codes, e.g. 600519 000001")

    sr = sub.add_parser("search", help="Search by Chinese name or pinyin.")
    sr.add_argument("keyword")
    sr.add_argument("--count", type=int, default=5)

    k = sub.add_parser("kline", help="Daily / weekly / monthly k-line as markdown.")
    k.add_argument("code")
    k.add_argument("--period", choices=["day", "week", "month"], default="day")
    k.add_argument("--count", type=int, default=30)

    # ------ allocate: 2nd-pass allocation table (LLM-driven priority list) ------
    al = sub.add_parser(
        "allocate",
        help="Render allocation table for LLM-chosen code list. "
             "Reads last recommend cache; falls back to live quote."
    )
    al.add_argument("--codes", required=True,
                    help="Comma-separated code list in LLM priority order, "
                         "e.g. 600759,601169,002667")
    al.add_argument("--capital", type=float, required=True,
                    help="Total capital (RMB)")
    al.add_argument("--comment", default=None,
                    help="Free-form markdown/text printed verbatim BEFORE the "
                         "table (typically LLM's reasoning summary)")
    al.add_argument("--per-target", type=float, default=10000.0,
                    help="Fixed RMB target per stock (default 10000)")

    # ------ sell-plan: holdings strategy advisor (regime-based, two-phase) ------
    sp = sub.add_parser(
        "sell-plan",
        help="Two-phase sell-plan. Phase 1: emit regime + suggested orders. "
             "Phase 2 (--order/--override): validate + emit natural-language "
             "[ACTION_PLAN] + 📍ORDER signature lines."
    )
    sp.add_argument("tokens", nargs="+",
                    help="Holding tokens, strict format code:qty/avail@cost "
                         "(qty=\u603b\u6301\u4ed3, avail=T+1\u53ef\u5356, cost=\u6210\u672c; \u5168\u90e8\u5fc5\u586b)")
    sp.add_argument("--target-yuan", type=float, default=10000.0,
                    help="单笔目标总价 (默认 10000 元/亇; 控手续费占比)")
    sp.add_argument("--fee-floor-pct", type=float, default=0.8,
                    help="\u53cc\u8fb9\u5dee\u4ef7\u6700\u4f4e\u95e8\u69db %% (\u9ed8\u8ba4 0.8)")
    sp.add_argument("--order", action="append", default=None, dest="orders",
                    help="Phase 2 \u8ba2\u5355 (\u53ef\u591a\u4e2a): code:side:qty@spec\u3002"
                         "\u4f8b: 000949:sell:100@+1.5 / 000949:buy:100@-1.5 / "
                         "002324:sell:500@bid1\u3002\u4e0d\u7ed9\u67d0\u4e2a code = NO_OP\u3002")
    sp.add_argument("--override", action="append", default=None,
                    dest="overrides",
                    help="Phase 2 regime \u8986\u76d6 (\u53ef\u591a\u4e2a): "
                         "code=REGIME:reason\u3002\u4f8b: 002324=DEEP_LOSS:K\u7ebf\u8dcc\u7834\u5e74\u7ebf\u3002"
                         "\u4ec5\u5141\u8bb8\u8986\u76d6\u5230\u9632\u5fa1\u6863\u3002")

    # ------ tushare-token: persist user-supplied token for Tier-4 fallback ------
    tt = sub.add_parser(
        "tushare-token",
        help="Manage tushare API token (used as Tier-4 k-line fallback).")
    tt_grp = tt.add_mutually_exclusive_group(required=True)
    tt_grp.add_argument("--status", action="store_true",
                        help="Print state: ready / skipped / unset")
    tt_grp.add_argument("--set", dest="set_token", metavar="TOKEN",
                        help="Save user token (plain JSON, per-user file).")
    tt_grp.add_argument("--skip", action="store_true",
                        help="Mark permanently skipped; agent stops asking.")
    tt_grp.add_argument("--clear", action="store_true",
                        help="Erase saved state; next run prompts again.")

    # ------ analyze: comprehensive per-stock snapshot ------
    an = sub.add_parser(
        "analyze",
        help="Per-stock comprehensive snapshot for LLM consumption "
             "(basics/quote/K-line/flow/sector/news). "
             "Usage: analyze <query> [<query>...] -- 6-digit code or Chinese name."
    )
    an.add_argument("queries", nargs="+",
                    help="6-digit codes or Chinese names (full/abbrev). "
                         "Unresolved names are echoed at tail; the command "
                         "never aborts due to a single bad query.")
    an.add_argument("--no-news", action="store_true",
                    help="Skip announcement + bad-news fetch (faster ~1s/stock)")
    an.add_argument("--days", type=int, default=120,
                    help="Daily-K window in trading days (default 120 ~= half year, "
                         "capped at 240). Downsampling keeps recent 20 daily, "
                         "20-60 every 2, 60+ every 5 (weekly).")
    an.add_argument("--minutes", type=int, default=32,
                    help="15min-K bar count (default 32 = 2 trading days, "
                         "capped at 80)")
    an.add_argument("--no-sample", action="store_true",
                    help="Disable daily-K downsampling; emit all `--days` raw bars")
    an.add_argument("--compact", action="store_true",
                    help="Summary view: MA + last-5 daily bars + minute features only")

    # ------ macro-sentiment: financial news scan for market backdrop ------
    ms = sub.add_parser(
        "macro-sentiment",
        help="Scan financial news headlines and score macro sentiment. "
             "Outputs structured [MACRO_SENTIMENT] block for LLM consumption."
    )

    return p


_KNOWN_CMDS = {
    "market", "sector-rank", "zt-pool", "dt-pool", "zb-pool", "lb-pool",
    "screen-c", "screen-d", "screen-e",
    "recommend", "brief", "eval", "intraday-track", "stats",
    # merged-in from legacy stock skill
    "quote", "search", "kline",
    # holdings advisor
    "sell-plan",
    # 2nd-pass allocation after LLM risk review
    "allocate",
    # per-stock comprehensive analysis (pure data for LLM)
    "analyze",
    # macro sentiment snapshot (financial news scan for market backdrop)
    "macro-sentiment",
    # tushare token management (Tier-4 k-line fallback enablement)
    "tushare-token",
}


def _cli_main(argv=None):
    # argv[0] resolution rules (strict, LLM-friendly):
    #   (1) known subcommand -> run it directly
    #   (2) -h / --help       -> argparse help
    #   (3) bare flag form    -> auto-prepend "brief"
    #   (4) empty argv        -> default to "brief"
    #   (5) anything else     -> HARD FAIL with explicit error
    if argv is None:
        argv = sys.argv[1:]
    argv = list(argv)
    if not argv:
        argv = ["brief"]
    else:
        first = argv[0]
        if first in _KNOWN_CMDS or first in ("-h", "--help"):
            pass                                           # (1)(2) legal
        elif first.startswith("-"):
            argv = ["brief"] + argv                        # (3) flag form
        else:
            print(
                f"❌ 未知参数 '{first}'。任务/用户描述里的"
                f"'策略C / 策略D / strategyC / C' 等字眼"
                f"**不是子命令**，请勿添加。\n"
                f"正确用法：\n"
                f"  python stockquant.py --capital <元> --market main --top 30\n"
                f"（不要加子命令；默认即跑完整报告 = 大盘 + 板块 + C/D/E 三引擎推荐）\n"
                f"可选子命令（仅工程调试时用，常规任务禁用）：\n"
                f"  {sorted(_KNOWN_CMDS)}",
                file=sys.stderr
            )
            sys.exit(2)

    args = _build_cli().parse_args(argv)
    _gc_cache()                                            # Auto-clean old cache dirs

    if args.cmd == "market":
        print_market()
    elif args.cmd == "sector-rank":
        print_sector_rank(args.type, args.top)
    elif args.cmd in ("zt-pool", "dt-pool", "zb-pool", "lb-pool"):
        print_pool(args.cmd.split("-")[0], getattr(args, "date", None))
    elif args.cmd == "screen-c":
        ind = get_sector_rank("industry", top=15, fail_safe=True)
        hot = {s["name"] for s in ind}
        mctx = {"sh_pct": None, "gem_pct": None}
        sector_pct_map = {s["name"]: s.get("pct") for s in ind if s.get("name")}
        cands = screen_strategy_c(board_top_n=args.board_top,
                                  board_days=args.board_days,
                                  laggard_pct=args.laggard_pct,
                                  market=args.market)
        scored = score_candidates(cands, hot_sectors=hot,
                                  market_ctx=mctx, sector_pct_map=sector_pct_map)
        print_screen(scored, f"策略C候选（热门板块滞涨，近{args.board_days}日）")
    elif args.cmd == "screen-d":
        ind = get_sector_rank("industry", top=15, fail_safe=True)
        hot = {s["name"] for s in ind}
        mctx = {"sh_pct": None, "gem_pct": None}
        sector_pct_map = {s["name"]: s.get("pct") for s in ind if s.get("name")}
        cands = screen_strategy_d(flow_days=args.flow_days,
                                  require_ma_alignment=not args.no_ma_alignment,
                                  market=args.market)
        scored = score_candidates(cands, hot_sectors=hot,
                                  market_ctx=mctx, sector_pct_map=sector_pct_map)
        print_screen(scored, f"策略D候选（{args.flow_days}日主力累积）")
    elif args.cmd == "screen-e":
        ind = get_sector_rank("industry", top=15, fail_safe=True)
        hot = {s["name"] for s in ind}
        mctx = {"sh_pct": None, "gem_pct": None}
        sector_pct_map = {s["name"]: s.get("pct") for s in ind if s.get("name")}
        cands = screen_strategy_e(box_days=args.box_days,
                                  box_range_max_pct=args.box_range_max,
                                  market=args.market, sample=args.sample)
        scored = score_candidates(cands, hot_sectors=hot,
                                  market_ctx=mctx, sector_pct_map=sector_pct_map)
        print_screen(scored, f"策略E候选（{args.box_days}日箱体突破）")
    elif args.cmd == "recommend":
        # Open verbose side-channel: drill-down detail (Stage1 drops,
        # alloc baseline, per-candidate soft/boost reasons) is routed
        # there so stdout stays under the agent's 20KB head-truncation.
        _open_verbose_log()
        strategies = tuple(s.strip().upper()
                           for s in args.strategy.split(",") if s.strip())
        res, meta = recommend(capital=args.capital, market=args.market,
                              strategies=strategies, threshold_pct=args.threshold,
                              top=args.top, min_trade_value=args.min_trade,
                              check_bad_news=not args.no_check_news,
                              max_per_sector=args.max_per_sector,
                              stop_loss_pct=args.stop_loss_pct,
                              max_position_pct=args.max_position_per_stock_pct,
                              e_sample=args.e_sample)
        print_recommend(res, meta, args.capital, args.threshold)
        if not args.no_log:
            run_args = {
                "capital": args.capital, "market": args.market,
                "strategies": list(strategies), "top": args.top,
                "stop_loss_pct": args.stop_loss_pct,
                "max_position_pct": args.max_position_per_stock_pct,
                "e_sample": args.e_sample,
            }
            _append_recommend_log(res, meta, run_args)
        _flush_verbose_log()
    elif args.cmd == "brief":
        # One-shot aggregate for LLM. Each segment isolated by fat banner;
        # any segment failure is caught locally so later segments still run.
        import traceback as _tb

        # Open verbose side-channel first so segment print functions can
        # route drill-down detail there (see _vprint / _v_or_print).
        _open_verbose_log()

        def _banner(tag):
            print()
            print("=" * 72)
            print(f"### {tag}")
            print("=" * 72)
            print()

        _banner("SEGMENT 1/3 MARKET (大盘闸门)")
        try:
            print_market()
        except Exception as ex:
            print(f"[BRIEF_ERR] market failed: {ex}")
            _tb.print_exc()

        _banner("SEGMENT 2/3 SECTOR-RANK Top 10 (板块热度)")
        try:
            print_sector_rank("industry", 10)
        except Exception as ex:
            print(f"[BRIEF_ERR] sector-rank failed: {ex}")
            _tb.print_exc()

        strategies = tuple(s.strip().upper()
                           for s in args.strategy.split(",") if s.strip())
        _banner(
            f"SEGMENT 3/3 RECOMMEND "
            f"(market={args.market}, top={args.top}, strategies={','.join(strategies)})"
        )
        try:
            res, meta = recommend(
                capital=args.capital, market=args.market,
                strategies=strategies, threshold_pct=5.0,
                top=args.top, min_trade_value=5000,
                check_bad_news=True, max_per_sector=2,
                stop_loss_pct=3.5, max_position_pct=40.0,
            )
            print_recommend(res, meta, args.capital, 5.0)
            run_args = {
                "capital": args.capital, "market": args.market,
                "strategies": list(strategies), "top": args.top,
                "stop_loss_pct": 3.5, "max_position_pct": 40.0,
                "source": "brief",
            }
            _append_recommend_log(res, meta, run_args)
        except Exception as ex:
            print(f"[BRIEF_ERR] recommend failed: {ex}")
            _tb.print_exc()

        _banner("END OF BRIEF")
        _flush_verbose_log()
    elif args.cmd == "eval":
        evaluate_recommendations(date=args.date)
    elif args.cmd == "intraday-track":
        track_recommendations(date=args.date)
    elif args.cmd == "stats":
        stats_recommendations(days=args.days)
    elif args.cmd == "quote":
        print_quotes(args.codes)
    elif args.cmd == "search":
        print_search(args.keyword, args.count)
    elif args.cmd == "kline":
        print_kline_cli(args.code, period=args.period, count=args.count)
    elif args.cmd == "allocate":
        codes = [c.strip() for c in args.codes.split(",") if c.strip()]
        cli_allocate(codes, args.capital, comment=args.comment,
                     per_target=args.per_target)
    elif args.cmd == "sell-plan":
        parsed = []
        for tok in args.tokens:
            try:
                parsed.append(_parse_holding_token(tok))
            except ValueError as ex:
                print(f"❌ 解析持仓参数 '{tok}' 失败: {ex}", file=sys.stderr)
                sys.exit(2)
        sell_plan(parsed, target_yuan=args.target_yuan,
                  orders_list=args.orders, overrides_list=args.overrides,
                  fee_floor_pct=args.fee_floor_pct)
    elif args.cmd == "analyze":
        analyze(args.queries,
                include_news=not args.no_news,
                days=args.days,
                minutes=args.minutes,
                no_sample=args.no_sample,
                compact=args.compact)
    elif args.cmd == "macro-sentiment":
        ms = _fetch_macro_sentiment()
        _render_macro_sentiment(ms)
    elif args.cmd == "tushare-token":
        if args.status:
            print(_get_tushare_status())
        elif args.set_token:
            _save_tushare_state({
                "token": args.set_token.strip(),
                "skip": False,
                "saved_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
            print("OK tushare token saved -> Tier-4 k-line fallback enabled.")
            # Bootstrap probe: run tier detect + warm stock_basic cache.
            # Critical for free 120pt accounts where stock_basic throttles
            # progressively (1/min -> 1/hour after a few calls). One success
            # right after --set persists 24h on disk and prevents the rest
            # of the pipeline from racing the rate-limit later.
            try:
                tier, tinfo = _get_tushare_tier(force_probe=True)
                print(f"   tier probe: {tier} ({tinfo})")
            except Exception as _e:
                print(f"   tier probe failed: {type(_e).__name__}: {_e}")
            try:
                nm, im = _get_tushare_stock_basic_maps()
                if nm:
                    print(f"   stock_basic warmed: {len(nm)} stocks cached "
                          "(name+industry, 24h TTL)")
                else:
                    print("   stock_basic warm: empty (rate-limited or no perm); "
                          "will retry on first recommend run")
            except Exception as _e:
                print(f"   stock_basic warm failed: {type(_e).__name__}: {_e}")
        elif args.skip:
            _save_tushare_state({
                "token": "",
                "skip": True,
                "saved_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
            print("OK tushare marked as skipped (agent will stop asking).")
        elif args.clear:
            try:
                os.remove(_TUSHARE_STATE_FILE)
                print("OK tushare state cleared.")
            except FileNotFoundError:
                print("(nothing to clear)")


if __name__ == "__main__":
    _cli_main()
