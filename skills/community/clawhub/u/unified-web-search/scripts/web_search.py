"""
联网搜索模块 - 统一接口，自动选择服务商

使用方法：
    from web_search import search

    result = search("关键词")
    if result["success"]:
        print(result["answer"])
"""

import json
import os
import re
import urllib.request
import urllib.error
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from urllib.parse import urlparse

# ============================================================================
# 配置管理
# ============================================================================

CONFIG_DIR = Path.home() / ".unified-web-search"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

# 平台别名 → 域名（合并进 sites；Volcengine/Tavily/Bailian 按各自能力路由）
_PLATFORM_SITES: Dict[str, List[str]] = {
    "xiaohongshu": ["xiaohongshu.com", "xhslink.com"],
    "xhs": ["xiaohongshu.com", "xhslink.com"],
    "wechat": ["mp.weixin.qq.com"],
    "weixin": ["mp.weixin.qq.com"],
    "weibo": ["weibo.com", "weibo.cn"],
    "zhihu": ["zhihu.com"],
    "bilibili": ["bilibili.com", "b23.tv"],
    "douyin": ["douyin.com"],
    "gov": ["gov.cn"],
    "arxiv": ["arxiv.org"],
}

_FRESHNESS_BUCKETS = (7, 30, 180, 365)

# 纯国内平台别名（命中则不必调 Tavily）
_DOMESTIC_PLATFORM_KEYS = frozenset({
    "xiaohongshu", "xhs", "wechat", "weixin", "weibo", "zhihu", "bilibili", "douyin", "gov",
})

# 火山引擎 time_range 枚举（freshness 天数 → TimeRange；180 天无精确档位，走 OneYear）
_FRESHNESS_TO_TIMERANGE = {
    7: "OneWeek",
    30: "OneMonth",
    180: "OneYear",
    365: "OneYear",
}


def _load_config() -> dict:
    """加载配置文件"""
    if CONFIG_FILE.exists():
        try:
            import yaml
            with open(CONFIG_FILE) as f:
                return yaml.safe_load(f) or {}
        except Exception:
            pass
    return {}


def _get_bailian_key() -> str:
    """获取百炼 API Key"""
    key = os.getenv("BAILIAN_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
    if key and len(key) > 20 and "..." not in key:
        return key
    config = _load_config()
    cfg_key = config.get("bailian", {}).get("api_key", "")
    if cfg_key and "..." not in cfg_key and len(cfg_key) > 20:
        return cfg_key
    return ""


def _is_valid_key(key: str, min_len: int = 10) -> bool:
    k = (key or "").strip()
    return bool(k) and len(k) >= min_len and "..." not in k


def _collect_env_keys(
    *env_names: str,
    numbered_prefix: str = "",
    config_section: str = "",
    config_key: str = "api_key",
    min_len: int = 10,
) -> List[str]:
    """从环境变量收集密钥：主变量、逗号分隔、VAR_2/VAR_3…、config.yaml。"""
    keys: List[str] = []
    seen: set = set()

    def add(raw: str) -> None:
        for part in re.split(r"[,;\s]+", raw):
            k = part.strip()
            if _is_valid_key(k, min_len) and k not in seen:
                seen.add(k)
                keys.append(k)

    for name in env_names:
        val = os.getenv(name, "")
        if val:
            add(val)

    prefix = numbered_prefix or (env_names[0] if env_names else "")
    if prefix:
        for i in range(2, 21):
            val = os.getenv(f"{prefix}_{i}", "")
            if val:
                add(val)

    if config_section:
        config = _load_config()
        section = config.get(config_section, {})
        cfg_val = section.get(config_key, "")
        if isinstance(cfg_val, str) and cfg_val:
            add(cfg_val)
        elif isinstance(cfg_val, list):
            for item in cfg_val:
                if isinstance(item, str):
                    add(item)

    return keys


def _get_tavily_keys() -> List[str]:
    """获取 Tavily API Key 池（TAVILY_API_KEY、TAVILY_API_KEY_2…）"""
    return _collect_env_keys(
        "TAVILY_API_KEY",
        numbered_prefix="TAVILY_API_KEY",
        config_section="tavily",
        min_len=20,
    )


def _get_tavily_key() -> str:
    keys = _get_tavily_keys()
    return keys[0] if keys else ""


def _get_zhipu_key() -> str:
    keys = _collect_env_keys(
        "ZHIPU_API_KEY",
        numbered_prefix="ZHIPU_API_KEY",
        config_section="zhipu",
        min_len=20,
    )
    return keys[0] if keys else ""


def _get_tencent_wsa_keys() -> List[str]:
    """腾讯云 WSA（TENCENT_WSA_APIKEY / TENCENT_WSA_API_KEY 及 _2…）"""
    return _collect_env_keys(
        "TENCENT_WSA_APIKEY",
        "TENCENT_WSA_API_KEY",
        numbered_prefix="TENCENT_WSA_APIKEY",
        config_section="tencent_wsa",
        min_len=10,
    )


def _get_volcengine_search_key() -> str:
    """获取火山引擎联网搜索 API Key（WEB_SEARCH_API_KEY）"""
    key = os.getenv("WEB_SEARCH_API_KEY")
    if key and len(key) > 10 and "..." not in key:
        return key
    config = _load_config()
    cfg_key = config.get("volcengine_search", {}).get("api_key", "")
    if cfg_key and "..." not in cfg_key and len(cfg_key) > 10:
        return cfg_key
    return ""


# ============================================================================
# 参数解析与后处理
# ============================================================================

def _parse_iso_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def _freshness_bucket_for_span(span_days: int) -> int:
    for bucket in _FRESHNESS_BUCKETS:
        if span_days <= bucket:
            return bucket
    return 365


def _resolve_time_filters(
    freshness: Optional[int],
    start_date: Optional[str],
    end_date: Optional[str],
) -> Dict[str, Any]:
    """统一日期/时效参数 → 各后端可用的规格 + 后处理窗口。"""
    start = _parse_iso_date(start_date)
    end = _parse_iso_date(end_date)
    today = date.today()

    if start and not end:
        end = today
    if end and not start:
        start = end - timedelta(days=6)

    if start and end and start > end:
        start, end = end, start

    effective_freshness = freshness
    if start and end:
        span = (end - start).days + 1
        if effective_freshness is None:
            effective_freshness = _freshness_bucket_for_span(span)

    return {
        "start": start,
        "end": end,
        "freshness": effective_freshness,
        "has_exact_range": bool(start and end),
        "volc_time_range": (
            f"{start.isoformat()}..{end.isoformat()}" if start and end else None
        ),
    }


def _expand_platforms(
    sites: Optional[List[str]], platforms: Optional[List[str]]
) -> Optional[List[str]]:
    merged: List[str] = []
    seen = set()
    for item in sites or []:
        key = item.strip().lower()
        if key and key not in seen:
            seen.add(key)
            merged.append(item.strip())
    for platform in platforms or []:
        key = platform.strip().lower()
        for domain in _PLATFORM_SITES.get(key, [platform.strip()]):
            dkey = domain.lower()
            if dkey and dkey not in seen:
                seen.add(dkey)
                merged.append(domain)
    return merged or None


def _sites_pipe(sites: Optional[List[str]]) -> str:
    if not sites:
        return ""
    return "|".join(s.strip() for s in sites if s and str(s).strip())


def _domain_from_url(url: str) -> str:
    try:
        host = (urlparse(url).netloc or "").lower()
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        return ""


def _domain_matches_site(host: str, site: str) -> bool:
    site = site.strip().lower().lstrip(".")
    if not site or not host:
        return False
    if site.startswith("*."):
        return host == site[2:] or host.endswith("." + site[2:])
    if site.startswith("."):
        return host.endswith(site) or host == site[1:]
    return host == site or host.endswith("." + site)


def _source_in_sites(source: dict, sites: List[str]) -> bool:
    host = _domain_from_url(source.get("url", ""))
    site_name = (source.get("site_name") or "").lower()
    return any(
        _domain_matches_site(host, s) or s.lower() in site_name for s in sites
    )


def _source_in_exclude(source: dict, exclude_sites: List[str]) -> bool:
    host = _domain_from_url(source.get("url", ""))
    site_name = (source.get("site_name") or "").lower()
    return any(
        _domain_matches_site(host, s) or s.lower() in site_name for s in exclude_sites
    )


def _parse_source_date(source: dict) -> Optional[date]:
    for key in ("published_date", "publish_time", "published"):
        raw = source.get(key)
        if not raw:
            continue
        text = str(raw).strip()
        if not text:
            continue
        # ISO datetime
        try:
            return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
        except ValueError:
            pass
        # YYYY-MM-DD prefix
        m = re.match(r"(\d{4}-\d{2}-\d{2})", text)
        if m:
            try:
                return datetime.strptime(m.group(1), "%Y-%m-%d").date()
            except ValueError:
                pass
    return None


def _post_filter_sources(
    sources: List[dict],
    *,
    start: Optional[date],
    end: Optional[date],
    sites: Optional[List[str]],
    exclude_sites: Optional[List[str]],
    auth_level: int = 0,
) -> List[dict]:
    filtered = []
    for src in sources:
        if sites and not _source_in_sites(src, sites):
            continue
        if exclude_sites and _source_in_exclude(src, exclude_sites):
            continue
        if auth_level > 0:
            level = src.get("auth_info_level")
            if level is not None and int(level) < auth_level:
                continue
        if start and end:
            pub = _parse_source_date(src)
            if pub is not None and (pub < start or pub > end):
                continue
        filtered.append(src)
    return filtered


def _apply_post_filters(result: dict, filters: Dict[str, Any]) -> dict:
    if not result.get("success"):
        return result
    sources = _post_filter_sources(
        list(result.get("sources") or []),
        start=filters.get("start"),
        end=filters.get("end"),
        sites=filters.get("post_filter_sites"),
        exclude_sites=filters.get("post_filter_exclude"),
        auth_level=filters.get("post_filter_auth_level") or 0,
    )
    result = dict(result)
    result["sources"] = sources
    if filters.get("provider_notes"):
        result["filter_notes"] = filters["provider_notes"]
    return result


# ============================================================================
# 搜索实现
# ============================================================================

def _bailian_search(
    query: str,
    strategy: str = "max",
    freshness: int = None,
    sites: list = None,
) -> dict:
    """百炼搜索（阿里云）— 不支持精确日期、exclude_sites、auth_level"""
    api_key = _get_bailian_key()
    if not api_key:
        return {"success": False, "error": "百炼密钥未配置", "provider": "bailian"}

    endpoint = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    search_options = {"search_strategy": strategy}
    if freshness:
        search_options["freshness"] = freshness
    if sites:
        search_options["assigned_site_list"] = sites

    payload = {
        "model": "qwen-plus",
        "messages": [{"role": "user", "content": query}],
        "enable_search": True,
        "search_options": search_options,
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=60) as response:
            raw = json.loads(response.read().decode("utf-8"))
            answer = raw.get("choices", [{}])[0].get("message", {}).get("content", "")
            sources = []
            if "search_info" in raw.get("output", {}):
                for item in raw["output"]["search_info"].get("search_results", []):
                    sources.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "snippet": item.get("snippet", ""),
                    })
            return {"success": True, "answer": answer, "sources": sources, "provider": "bailian"}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}", "provider": "bailian"}
    except Exception as e:
        return {"success": False, "error": str(e), "provider": "bailian"}


_TAVILY_ROTATABLE_HTTP = frozenset({401, 429, 432, 433})


def _tavily_search_with_key(
    api_key: str,
    query: str,
    freshness: int = None,
    sites: list = None,
    exclude_sites: list = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    topic: str = "general",
) -> dict:
    endpoint = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": 5,
        "search_depth": "basic",
        "include_answer": True,
        "topic": topic if topic in ("general", "news", "finance") else "general",
    }
    if start_date and end_date:
        payload["start_date"] = start_date.isoformat()
        payload["end_date"] = end_date.isoformat()
    elif freshness:
        payload["days"] = min(freshness, 30)
    if sites:
        payload["include_domains"] = sites
    if exclude_sites:
        payload["exclude_domains"] = exclude_sites

    try:
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=30) as response:
            raw = json.loads(response.read().decode("utf-8"))
            answer = raw.get("answer", "")
            sources = []
            for item in raw.get("results", []):
                sources.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("content", ""),
                    "published_date": item.get("published_date", ""),
                })
            return {"success": True, "answer": answer, "sources": sources, "provider": "tavily"}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}", "provider": "tavily", "http_code": e.code}
    except Exception as e:
        return {"success": False, "error": str(e), "provider": "tavily"}


def _tavily_search(
    query: str,
    freshness: int = None,
    sites: list = None,
    exclude_sites: list = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    topic: str = "general",
) -> dict:
    """Tavily — 主力 Key 优先；432/433 时标记主力耗尽并切备用 Key。"""
    keys = _get_tavily_keys()
    if not keys:
        return {"success": False, "error": "Tavily密钥未配置", "provider": "tavily"}

    primary_key, backup_keys = keys[0], keys[1:]
    result = _tavily_search_with_key(
        primary_key, query, freshness, sites, exclude_sites, start_date, end_date, topic,
    )
    if result.get("success"):
        return result

    last_err = result.get("error", "")
    http_code = result.get("http_code")
    if http_code in _TAVILY_ROTATABLE_HTTP:
        _mark_tavily_primary_exhausted()
        for idx, backup_key in enumerate(backup_keys):
            result = _tavily_search_with_key(
                backup_key, query, freshness, sites, exclude_sites,
                start_date, end_date, topic,
            )
            if result.get("success"):
                result = dict(result)
                result["key_rotated"] = idx + 2
                result["using_backup_key"] = True
                return result
            last_err = result.get("error", "")
            http_code = result.get("http_code")
            if http_code not in _TAVILY_ROTATABLE_HTTP:
                return result

    return {"success": False, "error": last_err or "Tavily全部密钥不可用", "provider": "tavily"}


_ZHIPU_RECENCY = {7: "oneWeek", 30: "oneMonth", 180: "oneYear", 365: "oneYear"}

_TAVILY_STATE_NAME = "tavily-key-state.json"


def _tavily_state_path() -> Path:
    hermes = os.getenv("HERMES_HOME", "").strip()
    if hermes:
        base = Path(hermes).expanduser() / ".unified-web-search"
    else:
        base = CONFIG_DIR
    base.mkdir(parents=True, exist_ok=True)
    return base / _TAVILY_STATE_NAME


def _load_tavily_state() -> dict:
    path = _tavily_state_path()
    if path.is_file():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _save_tavily_state(state: dict) -> None:
    path = _tavily_state_path()
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _mark_tavily_primary_exhausted() -> None:
    """主力 Key（TAVILY_API_KEY）当月额度耗尽时标记，路由切智谱优先。"""
    state = _load_tavily_state()
    state["primary_exhausted_month"] = date.today().strftime("%Y-%m")
    state["primary_exhausted_at"] = datetime.now().isoformat(timespec="seconds")
    _save_tavily_state(state)


def _is_tavily_primary_available() -> bool:
    """主力 Key 当月是否仍有免费额度（未触发 432）。"""
    if not _get_tavily_keys():
        return False
    state = _load_tavily_state()
    return state.get("primary_exhausted_month") != date.today().strftime("%Y-%m")


def _zhipu_item_url(item: dict) -> str:
    """智谱部分结果 link 为空，尝试 refer / 正文中的 URL。"""
    for field in ("link", "url", "refer"):
        val = (item.get(field) or "").strip()
        if val.startswith("http://") or val.startswith("https://"):
            return val
    refer = item.get("refer") or ""
    m = re.search(r"https?://[^\s\]>\"']+", refer)
    return m.group(0) if m else ""


def _source_dedup_key(source: dict) -> str:
    url = (source.get("url") or "").strip()
    if url:
        return url
    title = (source.get("title") or "").strip()
    snippet = (source.get("snippet") or "")[:80]
    if title or snippet:
        return f"nourl:{title}:{snippet}"
    return ""


def _is_empty_search_result(merged: dict) -> bool:
    """成功但无 answer 且无 sources → 视为空结果，应 fallback。"""
    if not merged.get("success"):
        return False
    if (merged.get("answer") or "").strip():
        return False
    return not (merged.get("sources") or [])


def _zhipu_search(
    query: str,
    count: int = 5,
    freshness: int = None,
    intensity: str = "normal",
) -> dict:
    """智谱 Web Search API — open.bigmodel.cn/api/paas/v4/web_search"""
    api_key = _get_zhipu_key()
    if not api_key:
        return {"success": False, "error": "智谱密钥未配置", "provider": "zhipu"}

    engine = "search_pro" if intensity == "deep" else "search_std"
    payload: Dict[str, Any] = {
        "search_query": query[:70],
        "search_engine": engine,
        "count": min(max(count, 1), 50),
        "search_intent": False,
    }
    if freshness:
        payload["search_recency_filter"] = _ZHIPU_RECENCY.get(freshness, "noLimit")

    endpoint = "https://open.bigmodel.cn/api/paas/v4/web_search"
    try:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = json.loads(response.read().decode("utf-8"))
            if raw.get("error"):
                err = raw["error"]
                msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
                return {"success": False, "error": msg, "provider": "zhipu"}

            sources = []
            snippets = []
            for item in raw.get("search_result") or []:
                snippet = item.get("content", "")
                if snippet:
                    snippets.append(snippet)
                sources.append({
                    "title": item.get("title", ""),
                    "url": _zhipu_item_url(item),
                    "snippet": snippet[:300],
                    "published_date": item.get("publish_date", ""),
                    "site_name": item.get("media", ""),
                })
            if not sources and not snippets:
                return {"success": False, "error": "智谱返回空结果", "provider": "zhipu"}
            answer = "\n\n".join(snippets[:3]) if snippets else ""
            return {"success": True, "answer": answer, "sources": sources, "provider": "zhipu"}
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")[:200]
        except Exception:
            pass
        return {"success": False, "error": f"HTTP {e.code}: {body}", "provider": "zhipu"}
    except Exception as e:
        return {"success": False, "error": str(e), "provider": "zhipu"}


def _tencent_wsa_search_with_key(api_key: str, query: str) -> dict:
    endpoint = "https://api.wsa.cloud.tencent.com/SearchPro"
    payload = {"Query": query}
    try:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json; charset=utf-8",
        }
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = json.loads(response.read().decode("utf-8"))
            resp = raw.get("Response") or {}
            err = resp.get("Error")
            if err:
                code = err.get("Code", "")
                msg = err.get("Message", "")
                rotatable = code in ("UnauthorizedOperation", "AuthFailure", "RequestLimitExceeded")
                return {
                    "success": False,
                    "error": f"[{code}] {msg}",
                    "provider": "tencent",
                    "rotatable": rotatable,
                }

            sources = []
            snippets = []
            for page in resp.get("Pages") or []:
                if isinstance(page, str):
                    try:
                        page = json.loads(page)
                    except json.JSONDecodeError:
                        continue
                if not isinstance(page, dict):
                    continue
                snippet = page.get("passage", "")
                if snippet:
                    snippets.append(snippet)
                sources.append({
                    "title": page.get("title", ""),
                    "url": page.get("url", ""),
                    "snippet": snippet[:300],
                    "published_date": page.get("date", ""),
                    "site_name": page.get("site", ""),
                })
            answer = "\n\n".join(snippets[:3]) if snippets else ""
            return {"success": True, "answer": answer, "sources": sources, "provider": "tencent"}
    except urllib.error.HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP {e.code}",
            "provider": "tencent",
            "rotatable": e.code in (401, 429),
        }
    except Exception as e:
        return {"success": False, "error": str(e), "provider": "tencent"}


def _tencent_wsa_search(query: str) -> dict:
    """腾讯云 WSA SearchPro — 多 Key 轮换"""
    keys = _get_tencent_wsa_keys()
    if not keys:
        return {"success": False, "error": "腾讯云WSA密钥未配置", "provider": "tencent"}

    last_err = ""
    for idx, api_key in enumerate(keys):
        result = _tencent_wsa_search_with_key(api_key, query)
        if result.get("success"):
            if idx > 0:
                result = dict(result)
                result["key_rotated"] = idx + 1
            return result
        last_err = result.get("error", "")
        if result.get("rotatable") and idx < len(keys) - 1:
            continue
        return result

    return {"success": False, "error": last_err or "腾讯云WSA全部密钥不可用", "provider": "tencent"}


def _volcengine_search(
    query: str,
    count: int = 5,
    time_range: str = None,
    auth_level: int = 0,
    sites: list = None,
    exclude_sites: list = None,
) -> dict:
    """火山引擎联网搜索（Search Infinity API）"""
    api_key = _get_volcengine_search_key()
    if not api_key:
        return {
            "success": False,
            "error": "火山引擎联网搜索密钥未配置（需设置 WEB_SEARCH_API_KEY）",
            "provider": "volcengine",
        }

    endpoint = "https://open.feedcoopapi.com/search_api/web_search"
    volc_filter: Dict[str, Any] = {}
    sites_pipe = _sites_pipe(sites)
    block_pipe = _sites_pipe(exclude_sites)
    if sites_pipe:
        volc_filter["Sites"] = sites_pipe
    if block_pipe:
        volc_filter["BlockHosts"] = block_pipe
    if auth_level > 0:
        volc_filter["AuthInfoLevel"] = auth_level

    payload = {
        "Query": query,
        "SearchType": "web",
        "Count": count,
        "NeedSummary": True,
    }
    if time_range:
        payload["TimeRange"] = time_range
    if volc_filter:
        payload["Filter"] = volc_filter

    try:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "X-Traffic-Tag": "skill_web_search_common",
        }
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=30) as response:
            raw = json.loads(response.read().decode("utf-8"))

            error = (raw.get("ResponseMetadata") or {}).get("Error")
            if error:
                code = error.get("Code", "")
                msg = error.get("Message", "")
                return {"success": False, "error": f"[{code}] {msg}", "provider": "volcengine"}

            result = raw.get("Result", {})
            summaries = []
            sources = []

            for item in result.get("WebResults") or []:
                summary = item.get("Summary") or item.get("Snippet", "")
                if summary:
                    summaries.append(summary)
                publish_time = item.get("PublishTime") or ""
                sources.append({
                    "title": item.get("Title", ""),
                    "url": item.get("Url", ""),
                    "snippet": (item.get("Summary") or item.get("Snippet", ""))[:300],
                    "site_name": item.get("SiteName", ""),
                    "auth_info": item.get("AuthInfoDes", ""),
                    "auth_info_level": item.get("AuthInfoLevel", 0),
                    "publish_time": publish_time,
                })

            answer = "\n\n".join(summaries) if summaries else ""
            return {"success": True, "answer": answer, "sources": sources, "provider": "volcengine"}

    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")[:200]
        except Exception:
            pass
        return {"success": False, "error": f"HTTP {e.code}: {body}", "provider": "volcengine"}
    except Exception as e:
        return {"success": False, "error": str(e), "provider": "volcengine"}


def _volc_time_range_from_filters(time_spec: Dict[str, Any]) -> Optional[str]:
    if time_spec.get("volc_time_range"):
        return time_spec["volc_time_range"]
    freshness = time_spec.get("freshness")
    return _FRESHNESS_TO_TIMERANGE.get(freshness) if freshness else None


def _build_filter_plan(
    time_spec: Dict[str, Any],
    sites: Optional[List[str]],
    exclude_sites: Optional[List[str]],
    auth_level: int,
    topic: str,
) -> Dict[str, Any]:
    """按后端能力决定：原生传参 vs 后处理。"""
    notes = []
    post_sites = None
    post_exclude = None
    post_auth = 0

    # Bailian: no native exclude/date/auth — post-filter when needed
    if exclude_sites:
        post_exclude = exclude_sites
        notes.append("bailian: exclude_sites via post-filter")
    if sites:
        notes.append("bailian: sites via assigned_site_list")
    if time_spec.get("has_exact_range"):
        notes.append("bailian: exact dates via freshness fallback + post-filter")
    if auth_level > 0:
        notes.append("bailian: auth_level not supported natively")

    return {
        "start": time_spec.get("start"),
        "end": time_spec.get("end"),
        "freshness": time_spec.get("freshness"),
        "volc_time_range": _volc_time_range_from_filters(time_spec),
        "sites": sites,
        "exclude_sites": exclude_sites,
        "auth_level": auth_level,
        "topic": topic,
        # Post-filter only where native API didn't apply (per-provider handled in merge)
        "post_filter_sites": post_sites,
        "post_filter_exclude": post_exclude,
        "post_filter_auth_level": post_auth,
        "provider_notes": notes,
    }


def _available_providers() -> List[str]:
    """仅返回已配置密钥的后端，避免无效请求。"""
    out: List[str] = []
    if _get_bailian_key():
        out.append("bailian")
    if _get_tavily_keys():
        out.append("tavily")
    if _get_volcengine_search_key():
        out.append("volcengine")
    if _get_zhipu_key():
        out.append("zhipu")
    if _get_tencent_wsa_keys():
        out.append("tencent")
    return out


def _is_domestic_domain(site: str) -> bool:
    s = site.strip().lower()
    markers = (
        ".cn", "gov.cn", "edu.cn", "xiaohongshu.com", "xhslink.com",
        "weibo.com", "weibo.cn", "zhihu.com", "mp.weixin.qq.com",
        "bilibili.com", "douyin.com", "b23.tv",
    )
    return any(m in s for m in markers)


def _is_domestic_only_context(
    merged_sites: Optional[List[str]], platforms: Optional[List[str]]
) -> bool:
    if platforms and all(p.strip().lower() in _DOMESTIC_PLATFORM_KEYS for p in platforms):
        return True
    if merged_sites and all(_is_domestic_domain(s) for s in merged_sites):
        return True
    return False


def _provider_count_for_intensity(intensity: str) -> int:
    return {"quick": 1, "normal": 1, "deep": 2}.get(intensity, 1)


def _ensure_zhipu_not_sole_deep(
    chosen: List[str], available: List[str], max_n: int,
) -> List[str]:
    """deep 模式禁止智谱单源（额度小，必须叠主源）。"""
    if max_n < 2 or len(chosen) != 1 or chosen[0] != "zhipu":
        return chosen
    for partner in ("tavily", "volcengine", "tencent", "bailian"):
        if partner in available:
            return [partner, "zhipu"][:max_n]
    return chosen


def _select_providers(
    intensity: str,
    is_domestic: bool,
    domestic_only: bool,
    plan: Dict[str, Any],
    available: List[str],
    *,
    tavily_primary_available: bool = True,
) -> List[str]:
    """
    按强度 / 地域 / Tavily 主力额度选后端：
    - 海外 + 主力 Tavily 有额度 → Tavily 第一源
    - 海外 + 主力耗尽（走备用 Key）→ 智谱第一源，Tavily 备用
    - deep → 智谱禁止单源
    """
    if not available:
        return []

    max_n = _provider_count_for_intensity(intensity)
    is_deep = intensity == "deep"

    chosen: List[str] = []

    def add(name: str) -> None:
        if name in available and name not in chosen:
            chosen.append(name)

    if is_domestic or domestic_only:
        add("volcengine")
        if is_deep:
            for p in ("tencent", "bailian", "zhipu"):
                add(p)
                if len(chosen) >= max_n:
                    break
        if not chosen:
            for p in ("tencent", "bailian", "zhipu", "tavily"):
                add(p)
                if chosen:
                    break
    elif is_deep:
        if tavily_primary_available:
            add("tavily")
            add("zhipu")
        else:
            add("zhipu")
            add("tavily")
        if len(chosen) < max_n:
            for p in ("tencent", "bailian"):
                add(p)
                if len(chosen) >= max_n:
                    break
    else:
        if tavily_primary_available:
            add("tavily")
        else:
            add("zhipu")
            if not chosen:
                add("tavily")
        if not chosen:
            for p in ("tencent", "bailian", "volcengine"):
                add(p)
                if chosen:
                    break

    chosen = chosen[:max_n]
    if is_deep:
        chosen = _ensure_zhipu_not_sole_deep(chosen, available, max_n)
    return chosen


def _fallback_providers(
    selected: List[str],
    available: List[str],
    is_domestic: bool,
    domestic_only: bool,
    intensity: str = "normal",
    *,
    tavily_primary_available: bool = True,
    max_extra: int = 2,
) -> List[str]:
    """主路由全部失败时，按优先级尝试备用后端。"""
    is_deep = intensity == "deep"
    if is_domestic or domestic_only:
        priority = ("volcengine", "tencent", "bailian", "tavily", "zhipu")
    elif is_deep:
        if tavily_primary_available:
            priority = ("tavily", "zhipu", "tencent", "bailian", "volcengine")
        else:
            priority = ("zhipu", "tavily", "tencent", "bailian", "volcengine")
    elif tavily_primary_available:
        priority = ("tavily", "zhipu", "tencent", "bailian", "volcengine")
    else:
        priority = ("zhipu", "tavily", "tencent", "bailian", "volcengine")
    tried = set(selected)
    fallbacks: List[str] = []
    for name in priority:
        if name in available and name not in tried:
            fallbacks.append(name)
            if len(fallbacks) >= max_extra:
                break
    return fallbacks


def _run_provider(
    provider: str,
    query: str,
    *,
    strategy: str,
    plan: Dict[str, Any],
    time_spec: Dict[str, Any],
    merged_sites: Optional[List[str]],
    exclude_sites: Optional[List[str]],
    auth_level: int,
    eff_topic: str,
    intensity: str,
) -> dict:
    eff_freshness = plan.get("freshness")
    volc_tr = plan.get("volc_time_range")
    t_start = time_spec.get("start")
    t_end = time_spec.get("end")
    count = {"quick": 3, "normal": 5, "deep": 10}.get(intensity, 5)

    if provider == "bailian":
        return _bailian_search(query, strategy, eff_freshness, merged_sites)
    if provider == "tavily":
        return _tavily_search(
            query, eff_freshness, merged_sites, exclude_sites,
            t_start, t_end, eff_topic,
        )
    if provider == "volcengine":
        return _volcengine_search(
            query, count=count, time_range=volc_tr,
            auth_level=auth_level, sites=merged_sites, exclude_sites=exclude_sites,
        )
    if provider == "zhipu":
        return _zhipu_search(query, count=count, freshness=eff_freshness, intensity=intensity)
    if provider == "tencent":
        return _tencent_wsa_search(query)
    return {"success": False, "error": f"unknown provider: {provider}", "provider": provider}


def _provider_needs_post_filter(provider: str, plan: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """返回该 provider 结果是否需要额外后处理及过滤条件。"""
    pf: Dict[str, Any] = {}
    needed = False

    if provider == "bailian":
        # sites 已由 assigned_site_list 原生传入，勿重复滤
        if plan.get("exclude_sites"):
            pf["exclude_sites"] = plan["exclude_sites"]
            needed = True
        if plan.get("start") and plan.get("end"):
            pf["start"] = plan["start"]
            pf["end"] = plan["end"]
            needed = True
        if plan.get("auth_level", 0) > 0:
            pf["auth_level"] = plan["auth_level"]
            needed = True
    elif provider == "tavily":
        if plan.get("start") and plan.get("end"):
            pf["start"] = plan["start"]
            pf["end"] = plan["end"]
            needed = True
    elif provider == "volcengine":
        if plan.get("start") and plan.get("end"):
            pf["start"] = plan["start"]
            pf["end"] = plan["end"]
            needed = True
    elif provider in ("zhipu", "tencent"):
        if plan.get("sites"):
            pf["sites"] = plan["sites"]
            needed = True
        if plan.get("exclude_sites"):
            pf["exclude_sites"] = plan["exclude_sites"]
            needed = True
        if plan.get("start") and plan.get("end"):
            pf["start"] = plan["start"]
            pf["end"] = plan["end"]
            needed = True
        if plan.get("auth_level", 0) > 0:
            pf["auth_level"] = plan["auth_level"]
            needed = True

    return needed, pf


# ============================================================================
# 统一接口
# ============================================================================

def _parse_region(raw: Optional[str]) -> str:
    """region: auto | domestic | overseas（含中英文别名）。"""
    if raw is None or raw == "":
        return "auto"
    r = str(raw).strip().lower()
    if r in ("auto", "default"):
        return "auto"
    if r in ("domestic", "cn", "china", "国内"):
        return "domestic"
    if r in ("overseas", "intl", "international", "global", "abroad", "海外"):
        return "overseas"
    return "auto"


def _resolve_search_region(
    region: str,
    query: str,
    merged_sites: Optional[List[str]],
    platforms: Optional[List[str]],
) -> Dict[str, Any]:
    """解析 region 参数 → 路由用的 domestic 标志 + 有效区域标签。"""
    inferred_domestic = _is_domestic_query(query, merged_sites)
    domestic_only = _is_domestic_only_context(merged_sites, platforms)

    if region == "domestic":
        return {
            "is_domestic": True,
            "domestic_only": domestic_only,
            "region_requested": region,
            "region_effective": "domestic",
            "region_inferred": False,
        }
    if region == "overseas":
        return {
            "is_domestic": False,
            "domestic_only": False,
            "region_requested": region,
            "region_effective": "overseas",
            "region_inferred": False,
        }
    # auto — 由 query / sites / platforms 推断
    effective = "domestic" if (inferred_domestic or domestic_only) else "overseas"
    return {
        "is_domestic": inferred_domestic,
        "domestic_only": domestic_only,
        "region_requested": "auto",
        "region_effective": effective,
        "region_inferred": True,
    }


def _build_retry_hint(
    region_requested: str,
    region_effective: str,
    intensity: str,
    merged: dict,
) -> str:
    """给大模型的多轮搜索建议（写入返回 JSON）。"""
    hints: List[str] = []
    if region_requested == "auto":
        hints.append(
            f"本次 region=auto，系统推断为 {region_effective} 搜索。"
            "若中文 query 在国内源结果不足（如 HuggingFace 评测集、英文论文、海外新闻），"
            "请显式设 region=overseas 再搜一轮。"
        )
    elif region_requested != region_effective:
        hints.append(
            f"已请求 region={region_requested}，实际生效 {region_effective}。"
        )
    else:
        hints.append(f"本次按 region={region_effective} 路由。")

    if intensity != "deep":
        hints.append("需要更全面覆盖时可设 intensity=deep（并行 2 个搜索源）。")

    if region_effective == "domestic":
        hints.append("海外内容不足时可改 region=overseas 重试。")
    else:
        hints.append("国内平台内容不足时可改 region=domestic 或加 platforms。")

    if not merged.get("success") or _is_empty_search_result(merged):
        alt = "overseas" if region_effective == "domestic" else "domestic"
        hints.append(f"本次结果为空或失败，建议换 region={alt} 或调整 query 后再搜。")

    return " ".join(hints)


def search(
    query: str,
    intensity: str = "normal",
    freshness: int = None,
    sites: list = None,
    start_date: str = None,
    end_date: str = None,
    exclude_sites: list = None,
    platforms: list = None,
    auth_level: int = 0,
    topic: str = "general",
    region: str = "auto",
) -> dict:
    """
    联网搜索 - 多服务商并行搜索，合并结果

    Args:
        query: 搜索问题
        intensity: 搜索强度 (quick/normal/deep)
        freshness: 时效筛选天数 (7/30/180/365)；与 start_date/end_date 二选一或组合
        sites: 限定站点/域名列表
        start_date: 起始日期 YYYY-MM-DD（与 end_date 搭配精确窗口，如「昨天+今天」）
        end_date: 结束日期 YYYY-MM-DD
        exclude_sites: 排除域名列表（Tavily/火山原生支持；百炼走后处理）
        platforms: 平台别名，如 xiaohongshu/wechat/weibo — 展开为 sites
        auth_level: 权威度 0=默认 1=高权威（仅火山原生；其他忽略）
        topic: Tavily 话题 general/news/finance
        region: auto=自动推断 | domestic=强制国内源 | overseas=强制海外源

    Returns:
        {"success": True/False, "answer": "...", "sources": [...]}
    """
    strategy_map = {"quick": "turbo", "normal": "max", "deep": "agent"}
    strategy = strategy_map.get(intensity, "max")
    region = _parse_region(region)

    merged_sites = _expand_platforms(sites, platforms)
    time_spec = _resolve_time_filters(freshness, start_date, end_date)
    plan = _build_filter_plan(
        time_spec, merged_sites, exclude_sites, auth_level or 0, topic or "general"
    )

    region_ctx = _resolve_search_region(region, query, merged_sites, platforms)
    is_domestic = region_ctx["is_domestic"]
    domestic_only = region_ctx["domestic_only"]
    region_effective = region_ctx["region_effective"]
    eff_topic = plan.get("topic", "general")
    if eff_topic == "general" and time_spec.get("has_exact_range"):
        t_start = time_spec.get("start")
        t_end = time_spec.get("end")
        span = (t_end - t_start).days + 1 if t_start and t_end else 0
        if span <= 7 and not is_domestic:
            eff_topic = "news"

    available = _available_providers()
    tavily_primary = _is_tavily_primary_available()
    selected = _select_providers(
        intensity, is_domestic, domestic_only, plan, available,
        tavily_primary_available=tavily_primary,
    )
    if not selected:
        return {
            "success": False,
            "error": "无可用搜索密钥（需配置 BAILIAN/TAVILY/WEB_SEARCH/ZHIPU/TENCENT 之一）",
            "alerts": [],
        }

    run_kw = dict(
        strategy=strategy,
        plan=plan,
        time_spec=time_spec,
        merged_sites=merged_sites,
        exclude_sites=exclude_sites,
        auth_level=auth_level or 0,
        eff_topic=eff_topic,
        intensity=intensity,
    )

    results = [_run_provider(p, query, **run_kw) for p in selected]

    # Per-provider post-filter where native API lacks support
    processed = []
    for r in results:
        provider = r.get("provider", "")
        needed, pf = _provider_needs_post_filter(provider, plan)
        if needed and r.get("success"):
            sources = _post_filter_sources(list(r.get("sources") or []), **pf)
            r = dict(r)
            r["sources"] = sources
        processed.append(r)

    merged = _merge_results(processed)

    # 主路由全失败或空结果时自动 fallback（如智谱无 link、Tavily 432）
    fallback_used: List[str] = []
    if not merged.get("success") or _is_empty_search_result(merged):
        if _is_empty_search_result(merged):
            merged = {"success": False, "error": "主源返回空结果", "alerts": merged.get("alerts", [])}
        fallbacks = _fallback_providers(
            selected, available, is_domestic, domestic_only, intensity=intensity,
            tavily_primary_available=tavily_primary,
        )
        if fallbacks:
            fb_results = [_run_provider(p, query, **run_kw) for p in fallbacks]
            fb_processed = []
            for r in fb_results:
                provider = r.get("provider", "")
                needed, pf = _provider_needs_post_filter(provider, plan)
                if needed and r.get("success"):
                    sources = _post_filter_sources(list(r.get("sources") or []), **pf)
                    r = dict(r)
                    r["sources"] = sources
                fb_processed.append(r)
            merged = _merge_results(processed + fb_processed)
            fallback_used = fallbacks

    meta = {
        "routing": {
            "intensity": intensity,
            "providers": selected,
            "domestic": is_domestic,
            "domestic_only": domestic_only,
            "region_requested": region_ctx["region_requested"],
            "region_effective": region_effective,
            "region_inferred": region_ctx["region_inferred"],
            "search_region": region_effective,
            "tavily_primary_available": tavily_primary,
            "effective_topic": eff_topic,
        },
        "params_applied": {
            "region": region_effective,
            "intensity": intensity,
            "freshness": plan.get("freshness"),
            "topic": eff_topic,
            "auth_level": auth_level or 0,
            "platforms": platforms,
            "sites": merged_sites,
        },
    }
    if fallback_used:
        meta["routing"]["fallback_providers"] = fallback_used
    meta["retry_hint"] = _build_retry_hint(
        region_ctx["region_requested"], region_effective, intensity, merged,
    )
    if time_spec.get("has_exact_range"):
        meta["date_range"] = {
            "start": time_spec["start"].isoformat(),
            "end": time_spec["end"].isoformat(),
        }
    if merged_sites:
        meta["sites"] = merged_sites
    if exclude_sites:
        meta["exclude_sites"] = exclude_sites
    if platforms:
        meta["platforms"] = platforms
    if meta:
        merged["filters_applied"] = meta

    return merged


# 海外品牌/话题 — 命中则走海外路由（Tavily/智谱优先）
_OVERSEAS_KEYWORDS: Tuple[str, ...] = (
    # AI 公司 / 模型
    "OpenAI", "Anthropic", "Claude", "ChatGPT", "GPT-4", "GPT-5", "GPT-5.5", "Codex",
    "Gemini", "Google", "DeepMind", "Microsoft", "Azure", "Meta", "Facebook",
    "Amazon", "AWS", "Apple", "Tesla", "NVIDIA", "Intel", "AMD", "Qualcomm",
    "Mistral", "Cohere", "Perplexity", "Llama", "Copilot", "Groq", "xAI", "Grok",
    "Deepgram", "Fish Audio", "ElevenLabs", "Hugging Face", "HuggingFace",
    "LangGraph", "AutoGen", "CrewAI", "Semantic Kernel", "LangChain",
    # 媒体 / 数据源
    "CNBC", "Forbes", "Reuters", "Bloomberg", "TechCrunch", "The Verge",
    "Wall Street Journal", "WSJ", "Reddit", "Hacker News", "Y Combinator",
    "GitHub", "Stack Overflow", "arXiv",
    # 地域 / 市场
    "美国", "美股", "纳斯达克", "NASDAQ", "硅谷", "美元", "USD", "华尔街",
    "United States", "U.S.", "U.K.", "欧盟", "欧洲",
)

# 国内品牌 — 优先于海外关键词（硅基流动/DeepSeek 等含英文但仍走国内）
_DOMESTIC_BRAND_KEYWORDS: Tuple[str, ...] = (
    "DeepSeek", "深度求索", "豆包", "Doubao", "字节跳动", "字节", "火山引擎",
    "硅基流动", "SiliconFlow", "通义", "文心", "混元", "智谱", "Moonshot", "Kimi",
    "腾讯", "阿里", "阿里云", "百度", "华为", "美团", "滴滴", "小红书", "哔哩哔哩",
    "B站", "bilibili", "知乎", "微博", "微信", "抖音", "拼多多", "京东",
)

# 国内语境 — 地理 / 政策 / 民生
_DOMESTIC_CONTEXT_KEYWORDS: Tuple[str, ...] = (
    "中国", "北京", "上海", "广州", "深圳", "政策", "gov.cn", "人民币", "A股",
    "国内", "天气", "省政府", "国务院", "工信部",
)


def _keyword_in_query(keyword: str, query: str) -> bool:
    """ASCII 短词用词边界，避免 'US' 误命中 'Opus'。"""
    if not keyword or not query:
        return False
    if keyword.isascii():
        if len(keyword) <= 3:
            return bool(re.search(
                r"(?<![A-Za-z0-9])" + re.escape(keyword) + r"(?![A-Za-z0-9])",
                query,
                re.I,
            ))
        return keyword.lower() in query.lower()
    return keyword in query


def _is_domestic_query(query: str, sites: list = None) -> bool:
    """判断是否是国内搜索（国内品牌 > 海外品牌 > 国内语境 > 默认国内）。"""
    if sites:
        domestic_domains = (
            ".cn", "gov.cn", "edu.cn", "xiaohongshu.com", "weibo.com",
            "zhihu.com", "mp.weixin.qq.com",
        )
        if all(any(d in s for d in domestic_domains) for s in sites):
            return True

    for kw in _DOMESTIC_BRAND_KEYWORDS:
        if _keyword_in_query(kw, query):
            return True

    for kw in _OVERSEAS_KEYWORDS:
        if _keyword_in_query(kw, query):
            return False

    # 独立 "US"（非 Opus/status 等子串）
    if re.search(r"(?<![A-Za-z])US(?![A-Za-z])", query, re.I):
        return False

    for kw in _DOMESTIC_CONTEXT_KEYWORDS:
        if _keyword_in_query(kw, query):
            return True

    return True


def _merge_results(results: list) -> dict:
    """合并多个服务商的结果"""
    successful = [r for r in results if r.get("success")]
    alerts = [{"provider": r.get("provider"), "error": r.get("error")}
              for r in results if not r.get("success") and r.get("error")]

    if not successful:
        return {"success": False, "error": results[0].get("error", "无搜索结果"), "alerts": alerts}

    answers = [r.get("answer", "") for r in successful if r.get("answer")]
    best_answer = max(answers, key=len) if answers else ""

    all_sources = []
    seen_keys = set()
    for r in successful:
        for s in r.get("sources", []):
            key = _source_dedup_key(s)
            if key and key not in seen_keys:
                seen_keys.add(key)
                all_sources.append(s)

    return {
        "success": True,
        "answer": best_answer,
        "sources": all_sources[:10],
        "provider": [r.get("provider") for r in successful],
        "alerts": alerts,
    }
