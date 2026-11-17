"""scripts/github.py - GitHub 源（官方 REST API，B2）。

产品原生检索域：用户「拿你查工具 / 库 / 开源代码」时，由 connector 路由到此，
打官方 api.github.com/search/repositories（标准 HTTPS，**无 TLS 指纹军备竞赛**，干净）。

限流应对（反爬轻量版）：token 首选调用方注入的 github_token（调用方注入，见 search(github_token=)），
其次回落 env GITHUB_TOKEN（逗号分隔，开箱即用兜底）轮换；读 X-RateLimit-Reset / Retry-After 退避；
无 token 时**提醒用户可配置提额**，若调用方注入 web_fetch 则兜底抓 github 搜索页，否则返回空 + warning。
库内自包含、零第三方依赖、不强制任何 key。
"""

import json
import os
import urllib.error as _uerr
import urllib.request as _ureq
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import quote as _urlencode
from urllib.request import Request as _Request


def _get_tokens(github_token: Optional[Any] = None) -> List[str]:
    """解析 GitHub token 来源：首选调用方注入的 github_token，其次 env GITHUB_TOKEN（开箱即用兜底）。

    由调用方提供：调用方想用自己的 token 直接传 github_token=...（字符串或列表/元组）；不传则回落 env；
    再无则返 [] → 上层走 web_fetch 兜底。库不强制任何 key。
    """
    if github_token:
        if isinstance(github_token, (list, tuple)):
            return [str(t).strip() for t in github_token if str(t).strip()]
        return [t.strip() for t in str(github_token).split(",") if t.strip()]
    raw = os.environ.get("GITHUB_TOKEN", "")
    return [t.strip() for t in raw.split(",") if t.strip()]


def _api_get(url: str, token: Optional[str]) -> Tuple[int, Optional[dict], Dict[str, str]]:
    """单次 API 调用。返回 (status, parsed|None, headers)。"""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Signal-Search/1.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"token {token}"
    req = _Request(url, headers=headers)
    try:
        with _ureq.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8", "replace")
            return resp.getcode(), json.loads(body), dict(resp.headers)
    except _uerr.HTTPError as e:
        return e.code, None, dict(e.headers)
    except Exception:
        return 0, None, {}


def _build_docs(data: dict) -> List[Dict[str, Any]]:
    docs: List[Dict[str, Any]] = []
    for it in (data.get("items") or [])[:10]:
        name = it.get("full_name") or ""
        desc = it.get("description") or ""
        stars = it.get("stargazers_count") or 0
        lang = it.get("language") or ""
        url = it.get("html_url") or ""
        docs.append(
            {
                "url": url,
                "text": f"{name}\n{desc}\n⭐{stars}  {lang}",
                "engine": "github",
                "source_type": "github",
                "landing_resolved": True,
                "repo": name,
                "stars": stars,
                # D3 结构化引用字段（导出 BibTeX 时优先用 key / repo，纯 web 源退化为 URL）
                "citation": {
                    "key": f"github-{name.replace('/', '-')}",
                    "repo": name,
                    "stars": stars,
                    "source": "github-api",
                },
            }
        )
    return docs


def search(
    query: str,
    cfg: Dict[str, Any] = None,
    web_fetch: Optional[Callable] = None,
    github_token: Optional[Any] = None,
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """GitHub 源搜索。返回 (docs, warnings)。

    - github_token：可选注入（字符串或列表），调用方注入；提供则用此 token 打官方 API，优选于 env GITHUB_TOKEN。
    - 多 token 轮换（注入的多个或 env 的逗号分隔）；限流(403/429)轮换下一个 token。
    - 无 token：**提醒用户可配置 GITHUB_TOKEN 提额**；若 web_fetch 注入则兜底抓 github 搜索页。
    """
    warnings: List[str] = []
    q = (query or "").strip()
    if not q:
        return [], []

    tokens = _get_tokens(github_token)
    url = (
        "https://api.github.com/search/repositories?q=" + _urlencode(q) + "&per_page=10&sort=stars"
    )

    docs: List[Dict[str, Any]] = []
    rate_limited = False
    attempts = (tokens + [None]) if tokens else [None]
    for i, tok in enumerate(attempts):
        status, data, hdrs = _api_get(url, tok)
        if status == 200 and data:
            docs = _build_docs(data)
            break
        if status in (429, 403):
            # 还有别的 token 可轮换则继续，否则记限流退出
            if tok is not None and i < len(attempts) - 1:
                continue
            rate_limited = True
            reset = (hdrs or {}).get("X-RateLimit-Reset")
            if reset:
                warnings.append(
                    f"GitHub API 限流(HTTP {status})，重置时间 {reset}；配置 GITHUB_TOKEN 可提升限额"
                )
            break

    if docs:
        return docs, warnings

    # 无结果：提醒 + web_fetch 兜底
    if not tokens:
        warnings.append(
            "未配置 GITHUB_TOKEN，GitHub 搜索限频严格（代码 10 / 仓库 30 次每分钟）；"
            "配置后仓库搜索可达 30 次/分钟。配置方式：环境变量 GITHUB_TOKEN=ghp_xxx"
        )
    if web_fetch:
        try:
            page_url = "https://github.com/search?q=" + _urlencode(q) + "&type=repositories"
            html = web_fetch(page_url)
            if html:
                return [
                    {
                        "url": page_url,
                        "text": str(html),
                        "engine": "github",
                        "source_type": "github",
                        "landing_resolved": True,
                        "citation": {"key": "github-search", "source": "github-web"},
                    }
                ], warnings
        except Exception:
            pass
    if rate_limited:
        warnings.append("GitHub API 限流且无可用 token 轮换，未注入 web_fetch 兜底，返回空结果")
    return [], warnings
