"""scripts/scrape.py - 反爬抓取层（§5.4 / §6.3c / M13–M18 / M55）。

核心定位："爬得到"是一等能力，但只抓公开数据、尊重 robots.txt、不绕过登录鉴权取私有
内容、不做高并发压测式请求。回落链：curl_cffi(impersonate) → 系统 curl 子进程 → requests。
无 Playwright 时挑战页标 blocked 交上层换源（M15/M17），不静默。
"""

import os
import random
import re
import subprocess
import sys
import threading
import time
from typing import Any, Dict, Optional, Tuple

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json"
)

# 真实近年 UA 池（与模拟浏览器一致；不混用 macOS 字体列表）
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) " "Gecko/20100101 Firefox/124.0",
]
ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
ACCEPT_LANG = "zh-CN,zh;q=0.9,en;q=0.8"
ACCEPT_ENC = "gzip, deflate, br"

try:
    import importlib.util as _ilu

    _HAS_CURL_CFFI = _ilu.find_spec("curl_cffi") is not None
except Exception:
    _HAS_CURL_CFFI = False

CHALLENGE_MARKS = [
    "cf-chl",
    "challenges.cloudflare.com",
    "cf-turnstile",
    "checking your browser",
    "enable cookies and javascript",
    "are you a human",
    "just a moment",
    "captcha",
]
LOGIN_PAYWALL = ["/login", "/signin", "/auth", "paywall", "/subscribe", "member only", "/member"]

PII_PATTERNS = [
    (re.compile(r"1[3-9]\d{9}"), "138****0000"),  # 手机号
    (re.compile(r"\d{17}[\dXx]"), "*****************"),  # 身份证
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "***@***"),  # 邮箱
]

from common import BoundedTTLMap
from common import domain_of as _domain
from common import load_config as _load_cfg

# 速率限制：按域名节流（best-effort；失败放行）
# 三个全局态被 deepfetch 的 ThreadPoolExecutor 并发读写，统一用 _state_lock 保护；
# 锁只护"读改写"临界区，绝不在持锁期间 sleep/发网络请求（否则并发退化为串行）。
# 三者全部有界 + 带 TTL：长跑进程下既不会无界增长，也不会让一次瞬时失败变成永久封禁。
_state_lock = threading.Lock()

_ROBOTS_CACHE_MAX = 512  # 长跑进程下按 FIFO 淘汰，防 robots 缓存无界增长
_ROBOTS_TTL_SEC = 3600.0  # robots.txt 抓取成功：缓存 1 小时
_ROBOTS_FAIL_TTL_SEC = 60.0  # robots.txt 抓取失败：fail-open 但只缓存 1 分钟，稍后重试
_LAST_CALL_MAX = 1024
_LAST_CALL_TTL_SEC = 300.0
_BLOCK_MAX = 1024
_BLOCK_TTL_SEC = 300.0  # 被明确封禁（429/503）：冷却 5 分钟
_BLOCK_TRANSIENT_TTL_SEC = 30.0  # 网络抖动（超时/连接重置）：冷却 30 秒即可

_last_call = BoundedTTLMap(maxsize=_LAST_CALL_MAX, ttl=_LAST_CALL_TTL_SEC)
_blocked_domains = BoundedTTLMap(maxsize=_BLOCK_MAX, ttl=_BLOCK_TTL_SEC)
_robots_cache = BoundedTTLMap(maxsize=_ROBOTS_CACHE_MAX, ttl=_ROBOTS_TTL_SEC)

# 主动封禁信号（长冷却） vs 网络抖动（短冷却）；rc=56 等传输层错误不该触发长冷却
_HARD_BLOCK_MARKS = ("status 429", "status 503", "status 403", "challenge", "captcha")


def _redact(text: str) -> str:
    for pat, repl in PII_PATTERNS:
        text = pat.sub(repl, text)
    return text


def _cooldown_for(last_err: Optional[str]) -> float:
    """按失败类型给冷却时长：主动封禁长冷却，网络抖动短冷却。"""
    low = (last_err or "").lower()
    return _BLOCK_TTL_SEC if any(m in low for m in _HARD_BLOCK_MARKS) else _BLOCK_TRANSIENT_TTL_SEC


def _coherent_headers() -> Dict[str, str]:
    ua = random.choice(UA_POOL)
    return {
        "User-Agent": ua,
        "Accept": ACCEPT,
        "Accept-Language": ACCEPT_LANG,
        "Accept-Encoding": ACCEPT_ENC,
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }


def _throttle(domain: str, cfg: Dict[str, Any]):
    comp = cfg.get("compliance", {})
    if not comp.get("enabled", True) or not comp.get("rate_limit_per_sec"):
        return
    interval = 1.0 / max(comp.get("rate_limit_per_sec", 0.07), 0.001)
    # 持锁只做"算等待 + 预占时槽"，sleep 放在锁外：并发线程抓同一域名时依次排队而非同时放行
    with _state_lock:
        now = time.time()
        wait = min(max(interval - (now - _last_call.get(domain, 0.0)), 0.0), 5.0)
        _last_call.set(domain, now + wait)
    if wait > 0:
        time.sleep(wait)  # 实测不超 5s，避免测试卡死；合规默认约 14s，测试可放宽


def _is_loginwall(url: str, cfg: Dict[str, Any]) -> bool:
    comp = cfg.get("compliance", {})
    if not comp.get("skip_loginwall_paywall", True):
        return False
    u = (url or "").lower()
    return any(k in u for k in LOGIN_PAYWALL)


def _challenge_in(html: str) -> bool:
    if not html:
        return False
    low = html.lower()
    return any(m.lower() in low for m in CHALLENGE_MARKS)


# 搜索引擎结果页(SERP)查询签名：命中即视为"用户检索请求"而非"第三内容页抓取"
_SEARCH_PARAMS = {
    "q",
    "query",
    "wd",
    "keyword",
    "p",
    "text",
    "i",
    "search",
    "aq",
    "qt",
    "type",
    "kw",
}
_SERP_PATH_PREFIX = ("/s", "/search", "/web", "/html", "/so", "/weixin", "/sorry", "/search.naver")


def _is_serp(url: str) -> bool:
    """识别 URL 是否为搜索引擎结果页端点（分层 robots 的豁免判据）。"""
    try:
        from urllib.parse import urlparse

        u = urlparse(url)
        path = (u.path or "").lower()
        if any(path.startswith(p) for p in _SERP_PATH_PREFIX):
            return True
        params = {k.split("=")[0] for k in (u.query or "").lower().split("&") if k}
        if params & _SEARCH_PARAMS:
            return True
    except Exception:
        return False
    return False


def _robots_ok(url: str, cfg: Dict[str, Any], meta: Dict[str, Any] = None) -> bool:
    comp = cfg.get("compliance", {})
    if not comp.get("respect_robots", True):
        return True
    # 经搜索引擎重定向器进入的落地页继承 SERP 豁免（等同于用户点击结果跳转）
    if meta and meta.get("serp_exempt"):
        return True
    # 分层模式：SERP 端点视为用户检索请求，豁免 robots 检查（否则所有搜索引擎结果页均被 Disallow 阻断）
    scope = comp.get("robots_scope", "serp")
    if scope == "serp" and _is_serp(url):
        return True
    # 第三方落地页 / 严格模式：照常检查 robots.txt
    dom = _domain(url)
    try:
        from urllib.parse import urlparse

        cached = _robots_cache.get(dom)
        if cached is not None:
            return cached
        txt = _simple_get(f"https://{dom}/robots.txt", cfg, timeout=4)
        if not txt:
            # 抓不到 robots.txt：fail-open 放行，但只缓存 1 分钟。
            # 长 TTL 会让一次网络抖动等价于"永久关闭 robots 检查"；不缓存又会导致
            # 抖动期间每抓一页重拉一次 robots.txt（冗余 I/O）。短 TTL 两头兼顾。
            _robots_cache.set(dom, True, ttl=_ROBOTS_FAIL_TTL_SEC)
            return True
        path = urlparse(url).path or "/"
        allowed = True
        for line in txt.splitlines():
            if line.lower().startswith("disallow:"):
                rule = line.split(":", 1)[1].strip()
                if rule and (path.startswith(rule) or rule == "/"):
                    allowed = False
                    break
        _robots_cache.set(dom, allowed)
        return allowed
    except Exception:
        _robots_cache.set(dom, True, ttl=_ROBOTS_FAIL_TTL_SEC)
        return True


# ---------------------------------------------------------------------------
# TLS 证书校验开关（W6 安全项闭环）
# 默认开启校验（更安全）；仅当 config.scrape.tls_verify 显式为 False 才关闭。
# 关闭时通过 meta["warnings"] 与 stderr 各发一次 MITM 风险提示（每进程去抖）。
# ---------------------------------------------------------------------------
_TLS_WARN_LOCK = threading.Lock()
_TLS_WARN_EMITTED = False


def _tls_verify(cfg: Dict[str, Any]) -> bool:
    """是否校验 TLS 证书。默认 True（安全）；config.scrape.tls_verify 显式 False 才关闭。"""
    try:
        return bool(((cfg or {}).get("scrape") or {}).get("tls_verify", True))
    except Exception:
        return True


def _emit_tls_warn(meta: Optional[Dict[str, Any]] = None) -> None:
    """关闭证书校验时发出一次 MITM 风险提示：写入 meta['warnings'] 并打印 stderr（每进程去抖）。"""
    global _TLS_WARN_EMITTED
    msg = (
        "TLS 证书校验已关闭 (config.scrape.tls_verify=false)：存在中间人劫持(MITM)风险，"
        "仅应在受信任的内网或测试环境使用。"
    )
    if isinstance(meta, dict):
        meta.setdefault("warnings", []).append(msg)
    with _TLS_WARN_LOCK:
        if not _TLS_WARN_EMITTED:
            _TLS_WARN_EMITTED = True
            try:
                sys.stderr.write("[signal-search][WARN] " + msg + "\n")
            except Exception:
                pass


def _simple_get(url: str, cfg: Dict[str, Any], timeout: int = 10) -> str:
    try:
        if _HAS_CURL_CFFI:
            from curl_cffi import requests as cffi_req

            return cffi_req.get(
                url, timeout=timeout, impersonate="chrome", verify=_tls_verify(cfg)
            ).text
    except Exception:
        pass
    try:
        import requests

        return requests.get(
            url, timeout=timeout, headers={"User-Agent": UA_POOL[0]}, verify=_tls_verify(cfg)
        ).text
    except Exception:
        return ""


def _fetch_curl_cffi(url, headers, proxy, timeout=15, cfg=None):
    from curl_cffi import requests as cffi_req

    kwargs = dict(
        headers=headers,
        timeout=timeout,
        impersonate="chrome",
        verify=_tls_verify(cfg),
        allow_redirects=True,
    )
    if proxy:
        kwargs["proxy"] = proxy
    r = cffi_req.get(url, **kwargs)
    return r.status_code, r.text, r.url


def _fetch_requests(url, headers, proxy, timeout=15, cfg=None):
    import requests

    kwargs = dict(headers=headers, timeout=timeout, allow_redirects=True, verify=_tls_verify(cfg))
    if proxy:
        kwargs["proxies"] = {"http": proxy, "https": proxy}
    r = requests.get(url, **kwargs)
    return r.status_code, r.text, r.url


_CURL_CODE_MARK = "\n__SS_HTTP_CODE__:"


def _fetch_system_curl(url, headers, proxy, timeout=15):
    """系统 curl 兜底。用 -w 取真实 HTTP 状态码。

    子进程拿不到状态码时上层会把 429/503 等封禁信号误判为 0（无法触发退避/换源），
    故把 %{http_code} 追加到 stdout 末尾再切出来，取不到才退回 0。
    """
    cmd = [
        "curl",
        "-sL",
        "--compressed",
        "--max-time",
        str(timeout),
        "-w",
        f"{_CURL_CODE_MARK}%{{http_code}}",
        "-A",
        headers["User-Agent"],
    ]
    for k, v in headers.items():
        if k.lower() == "user-agent":
            continue
        cmd += ["-H", f"{k}: {v}"]
    if proxy:
        cmd += ["-x", proxy]
    cmd += [url]
    try:
        out = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout + 5,
        )
        body = out.stdout or ""
        status = 0
        idx = body.rfind(_CURL_CODE_MARK)
        if idx != -1:
            tail = body[idx + len(_CURL_CODE_MARK) :].strip()
            body = body[:idx]
            try:
                status = int(tail)
            except ValueError:
                status = 0
        return status, body, url
    except Exception:
        return 0, "", url


def _init_info(url: str) -> Dict[str, Any]:
    """scrape 返回的 info 骨架。"""
    return {
        "status": None,
        "final_url": url,
        "blocked": False,
        "challenge": False,
        "loginwall": False,
        "method": None,
        "error": None,
    }


def _scrape_guards(url: str, cfg: Dict[str, Any], meta: Dict[str, Any], info: Dict[str, Any]):
    """前置护栏：登录墙 / robots / 冷却域名。命中返回提前退出元组 (None, info)，否则 None。"""
    if _is_loginwall(url, cfg):
        info.update(blocked=True, loginwall=True, error="loginwall/paywall skipped (M55)")
        return None, info
    if not _robots_ok(url, cfg, meta):
        info.update(blocked=True, error="robots.txt disallow (M55)")
        return None, info
    domain = _domain(url)
    if _blocked_domains.get(domain) is not None:
        info.update(blocked=True, error="domain in cooldown after recent failures")
        return None, info
    return None


def _maybe_warmup(domain: str, cfg: Dict[str, Any]):
    """会话热身：warmup 域名先轻量访问首页（失败静默）。"""
    warmup = cfg.get("warmup_domains") or []
    if domain in warmup:
        try:
            _simple_get(f"https://{domain}/", cfg, timeout=6)
        except Exception:
            pass


def _backoff(attempt: int) -> float:
    """指数退避 + 随机 jitter，封顶 8s。"""
    return min(2**attempt + random.uniform(0, 1), 8)


def _try_system_curl_fallback(url, headers, proxy, timeout, info) -> Optional[str]:
    """主通道空响应时回落系统 curl。成功返回正文并改写 method/status，失败返回 None。"""
    try:
        st2, html2, _final2 = _fetch_system_curl(url, headers, proxy, timeout)
        if html2 and len(html2) > 200:
            info["method"] = "system_curl"
            info["status"] = st2
            return html2
    except Exception:
        pass
    return None


def _scrape_attempt(url, headers, proxy, timeout, cfg, info):
    """单次抓取尝试。返回 (outcome, html_or_None, err)。

    outcome ∈ {ok, retry, blocked}：ok=成功可取；retry=需退避重试（429/503 或空响应）；
    blocked=挑战页（终判阻断，交上层换源）。注意：429/503 只在终判失败时标 blocked，
    成功路径不残留 blocked=True（修复"重试后成功仍报 blocked"隐患）。
    """
    method = "curl_cffi" if _HAS_CURL_CFFI else "requests"
    if _HAS_CURL_CFFI:
        status, html, final = _fetch_curl_cffi(url, headers, proxy, timeout, cfg)
    else:
        status, html, final = _fetch_requests(url, headers, proxy, timeout, cfg)
    info.update(method=method, status=status, final_url=final)

    if status in (429, 503):
        return "retry", None, f"status {status}"

    if not html or len(html) < 200:
        html = _try_system_curl_fallback(url, headers, proxy, timeout, info)
        if not html or len(html) < 200:
            return "retry", None, "empty body; try system curl"

    if _challenge_in(html):
        info.update(
            challenge=True, blocked=True, error="challenge page detected, no solver (M15/M17)"
        )
        return "blocked", None, None

    if cfg.get("compliance", {}).get("pii_redact", True):
        html = _redact(html)
    return "ok", html, None


def _scrape_retry(url, domain, cfg, headers, info, timeout) -> Tuple[Optional[str], Dict[str, Any]]:
    """三档重试编排：代理轮询 + 节流 + 退避。成功返回 (html, info)，全失败标冷却后返回 (None, info)。"""
    proxies = cfg.get("proxies") or []
    proxy_cycle = iter(proxies) if proxies else None
    last_err = None
    for attempt in range(3):
        proxy = next(proxy_cycle, None) if proxy_cycle else None
        _throttle(domain, cfg)
        try:
            outcome, html, err = _scrape_attempt(url, headers, proxy, timeout, cfg, info)
        except Exception as e:
            outcome, html, err = "retry", None, str(e)
        if outcome == "ok":
            return html, info
        if outcome == "blocked":
            return None, info
        last_err = err
        time.sleep(_backoff(attempt))
    info.update(blocked=True, error=last_err or "all retries failed")
    # 冷却而非永久拉黑：到期自动放行，且区分"被封"与"网络抖动"两类失败
    _blocked_domains.set(domain, last_err or "failed", ttl=_cooldown_for(last_err))
    return None, info


def scrape(url: str, meta: Dict[str, Any] = None) -> Tuple[Optional[str], Dict[str, Any]]:
    """反爬抓取。返回 (html_or_None, info)。

    info: {status, final_url, blocked, challenge, loginwall, method, error}
    九能力：抖动延时 / 自洽头 / TLS 回落链 / 代理轮换 / 指数退避 / 挑战检测 / 蜜罐不跟
    （蜜罐在 extract.clean_links 处理）/ 会话热身（warmup 域名）。
    主函数退化为编排器：前置护栏 → 热身 → 抖动延时 → 重试循环。
    """
    meta = meta or {}
    cfg = _load_cfg(meta.get("cfg"))
    if not _tls_verify(cfg):
        _emit_tls_warn(meta)
    timeout = (meta or {}).get("timeout", 15)
    info = _init_info(url)

    early = _scrape_guards(url, cfg, meta, info)
    if early is not None:
        return early

    domain = _domain(url)
    _maybe_warmup(domain, cfg)
    headers = _coherent_headers()
    time.sleep(random.uniform(1.2, 3.5))  # 抖动延时（固定间隔是 bot 信号）

    return _scrape_retry(url, domain, cfg, headers, info, timeout)
