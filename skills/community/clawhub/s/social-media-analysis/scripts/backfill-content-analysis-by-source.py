#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从飞书多维表批量读取记录，按「来源渠道」解析「原文URL」并回填「内容解析」。

覆盖渠道（默认）：
- 抖音APP
- 酷安APP
- 今日头条
- 快手APP
- 小红书APP

回填策略：
- 默认 ONLY_EMPTY=1：仅当「内容解析」为空时回填

回填内容：
- 使用与 scripts/build-content-analysis.js 基本一致的规则生成「100字以内内容解析」
- 解析来源优先：平台可直接从 URL 抓取的文字摘要（如 meta/描述/抖音 desc）
- 抓取失败不会覆盖现有「内容解析」
"""

import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

import requests


# ------------------ 飞书配置 ------------------
APP_ID = os.getenv("APP_ID", "").strip()
APP_SECRET = os.getenv("APP_SECRET", "").strip()
BITABLE_URL = os.getenv("BITABLE_URL", "").strip()

# ------------------ 业务字段（按实际多维表字段名可改） ------------------
SOURCE_CHANNEL_FIELD = os.getenv("SOURCE_CHANNEL_FIELD", "来源渠道").strip()
CONTENT_ANALYSIS_FIELD = os.getenv("CONTENT_ANALYSIS_FIELD", "内容解析").strip()

# 用户提到“获取原文URL”，但项目里通常叫“原文 URL”
ORIGINAL_URL_CANDIDATES = [
    x.strip()
    for x in [
        os.getenv("WEIBO_ORIGINAL_URL_FIELD", "").strip(),  # 用户可指定一个自定义字段名
        "获取原文URL",
        "原文 URL",
        "原文URL",
        "原文url",
        "doc_url",
    ]
    if x.strip()
]

# ------------------ 渠道过滤 ------------------
DEFAULT_CHANNELS = ["抖音APP", "酷安APP", "今日头条", "快手APP", "小红书APP"]
SOURCE_CHANNELS = [
    x.strip()
    for x in os.getenv("SOURCE_CHANNELS", ",".join(DEFAULT_CHANNELS)).split(",")
    if x.strip()
]
SOURCE_CHANNELS_SET = set(SOURCE_CHANNELS)

SOURCE_CHANNEL_VALUE_TO_PLATFORM = {
    "抖音APP": ("抖音", "视频"),
    "酷安APP": ("酷安", "未知"),
    "今日头条": ("今日头条", "图文"),
    "快手APP": ("快手", "视频"),
    "小红书APP": ("小红书", "图文"),
}

# ------------------ 行为参数 ------------------
ONLY_EMPTY = os.getenv("ONLY_EMPTY", "1").strip().lower() in ("1", "true", "yes")
MAX_TARGETS = int(os.getenv("LIMIT", "50"))
FETCH_PAGE_SIZE = int(os.getenv("PAGE_SIZE", "200"))
WORKERS = int(os.getenv("WORKERS", "4"))
MAX_CHARS = int(os.getenv("MAX_CHARS", "100"))

# 抓取相关
HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", "15"))
RETRY_TIMES = int(os.getenv("HTTP_RETRY_TIMES", "1"))  # 失败重试次数（不建议太高）

SESSION: Optional[requests.Session] = None


def get_session() -> requests.Session:
    global SESSION
    if SESSION is None:
        SESSION = requests.Session()
    return SESSION


def _safe_text(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        if not v:
            return ""
        v = v[0]
    if isinstance(v, dict):
        try:
            return json.dumps(v, ensure_ascii=False)
        except Exception:
            return str(v)
    return str(v).strip()


def parse_bitable_url(url: str) -> Tuple[str, str]:
    parsed = urlparse(url)
    app_token = ""
    parts = [p for p in parsed.path.split("/") if p]
    for i, p in enumerate(parts):
        if p == "base" and i + 1 < len(parts):
            app_token = parts[i + 1]
            break
    qs = parse_qs(parsed.query)
    table_id = qs.get("table", [None])[0]
    if not app_token or not table_id:
        raise RuntimeError(f"BITABLE_URL 解析失败: {url}")
    return app_token, table_id


def get_tenant_access_token() -> str:
    if not APP_ID or not APP_SECRET:
        raise RuntimeError("请设置环境变量 APP_ID / APP_SECRET")
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    resp = get_session().post(url, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"获取 tenant_access_token 失败: {data}")
    return data["tenant_access_token"]


def fetch_targets(token: str) -> List[Dict[str, Any]]:
    if not BITABLE_URL:
        raise RuntimeError("请设置环境变量 BITABLE_URL（飞书多维表链接）")

    app_token, table_id = parse_bitable_url(BITABLE_URL)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    headers = {"Authorization": f"Bearer {token}"}
    params: Dict[str, Any] = {"page_size": min(500, FETCH_PAGE_SIZE)}

    targets: List[Dict[str, Any]] = []
    page_token: Optional[str] = None

    while True:
        if page_token:
            params["page_token"] = page_token
        resp = get_session().get(url, headers=headers, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"获取记录失败: {data}")

        obj = data.get("data") or {}
        items = obj.get("items") or []
        for rec in items:
            fields = rec.get("fields") or {}
            ch = _safe_text(fields.get(SOURCE_CHANNEL_FIELD))
            if ch not in SOURCE_CHANNELS_SET:
                continue

            existing = _safe_text(fields.get(CONTENT_ANALYSIS_FIELD))
            if ONLY_EMPTY and existing:
                continue

            original_url = ""
            for cand in ORIGINAL_URL_CANDIDATES:
                if cand in fields:
                    original_url = _safe_text(fields.get(cand))
                    if original_url:
                        break
            if not original_url:
                continue

            record_id = rec.get("record_id")
            if not record_id:
                continue

            targets.append(
                {
                    "record_id": record_id,
                    "source_channel": ch,
                    "original_url": original_url,
                }
            )
            if len(targets) >= MAX_TARGETS:
                return targets

        page_token = obj.get("page_token")
        has_more = obj.get("has_more")
        if not has_more or not page_token:
            break

    return targets


def batch_update_records(token: str, updates: List[Dict[str, Any]]) -> None:
    if not updates:
        return
    if not BITABLE_URL:
        raise RuntimeError("BITABLE_URL 未初始化")
    app_token, table_id = parse_bitable_url(BITABLE_URL)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"records": updates}
    resp = get_session().post(url, headers=headers, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"批量更新失败: {data}")


# ------------------ 解析与分析：统一规则 ------------------
BRAND_KWS = ["小米", "小爱", "小爱同学", "Xiaomi", "Mi", "Redmi"]
SPLIT_RE = re.compile(r"[。！？!?；;\n]")
HTML_TAG_RE = re.compile(r"<[^>]*>")
URL_RE = re.compile(r"https?:\/\/\S+")
WS_RE = re.compile(r"\s+")


def normalize_text(input_text: Any) -> str:
    text = str(input_text or "")
    text = HTML_TAG_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = WS_RE.sub(" ", text)
    return text.strip()


def split_sentences(text: str) -> List[str]:
    t = normalize_text(text)
    return [s.strip() for s in SPLIT_RE.split(t) if s.strip()]


def truncate_by_chars(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    if max_chars <= 1:
        return "…"
    return text[: max_chars - 1] + "…"


def pick_top_sentence(sentences: List[str], keywords: List[str]) -> str:
    if not sentences:
        return ""
    best = sentences[0]
    best_score = -1.0
    for s in sentences:
        score = 0.0
        lower = s.lower()
        for kw in keywords:
            if kw.lower() in lower:
                score += 2
        if 12 <= len(s) <= 60:
            score += 1
        # 复刻 JS 的“字符类”正则行为（允许出现任一关键词字符即可加分）
        if re.search(r"[发布|体验|测评|开箱|对比|评测|升级|更新|功能]", s):
            score += 1
        if score > best_score:
            best_score = score
            best = s
    return best


def build_content_analysis(title: str, text: str, platform: str, media_type: str, visual: str, max_chars: int = 100) -> str:
    title_text = normalize_text(title)
    body_text = normalize_text(text)
    visual_text = normalize_text(visual)

    sents = split_sentences(f"{title_text}。{body_text}".strip("。"))
    core = pick_top_sentence(sents, BRAND_KWS) or title_text or body_text
    visual_core = pick_top_sentence(split_sentences(visual_text), BRAND_KWS)

    has_brand = any(kw in title_text or kw in body_text or kw in visual_text for kw in BRAND_KWS)
    has_visual = len(visual_text) > 0

    if has_brand:
        analysis = f"该内容与小米/小爱相关，核心信息：{core}"
        if has_visual:
            analysis += f"；画面显示：{visual_core or truncate_by_chars(visual_text, 28)}"
    elif has_visual:
        analysis = f"该内容未明显提及小米/小爱，核心信息：{core or '文本信息有限'}；画面显示：{visual_core or truncate_by_chars(visual_text, 28)}"
    else:
        analysis = f"该内容核心信息：{core or '文本信息有限，建议补充原文或媒体素材后复核'}"

    return truncate_by_chars(analysis, max_chars)


# ------------------ 文本抽取（按平台） ------------------
UA_COMMON = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def _strip_html_like(s: str) -> str:
    t = unescape(s or "")
    t = HTML_TAG_RE.sub("", t)
    t = WS_RE.sub(" ", t).strip()
    return t


def http_get_text(url: str) -> str:
    headers = {"User-Agent": UA_COMMON, "Accept": "text/html,application/json,*/*"}
    last_err: Optional[Exception] = None
    for attempt in range(RETRY_TIMES + 1):
        try:
            resp = get_session().get(url, headers=headers, timeout=HTTP_TIMEOUT, allow_redirects=True)
            resp.raise_for_status()
            return resp.text or ""
        except Exception as e:
            last_err = e
            time.sleep(0.6 * (2 ** attempt))
    if last_err:
        raise last_err
    return ""


def extract_meta_description(html: str) -> Tuple[str, str]:
    # og:title
    def _meta_content(pattern: str) -> str:
        m = re.search(pattern, html, flags=re.IGNORECASE)
        if not m:
            return ""
        return _strip_html_like(m.group(1))

    title = _meta_content(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']')
    if not title:
        title = _meta_content(r"<meta[^>]+name=['\"]title['\"][^>]+content=['\"]([^'\"]+)['\"]")
    if not title:
        m = re.search(r"<title>([^<]+)</title>", html, flags=re.IGNORECASE)
        if m:
            title = _strip_html_like(m.group(1))

    desc = _meta_content(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']')
    if not desc:
        desc = _meta_content(r"<meta[^>]+name=['\"]description['\"][^>]+content=['\"]([^'\"]+)['\"]")

    # JSON-LD fallback
    if not desc:
        for m in re.finditer(r"<script[^>]+type=['\"]application/ld\+json['\"][^>]*>([\s\S]*?)</script>", html, flags=re.IGNORECASE):
            raw = m.group(1).strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
                if isinstance(obj, dict):
                    desc = _strip_html_like(obj.get("description", "") or "")
                    title = title or _strip_html_like(obj.get("name", "") or obj.get("headline", "") or "")
                    if desc:
                        break
            except Exception:
                continue

    return title, desc


def extract_douyin_desc_from_url(url: str) -> Tuple[str, str]:
    """
    复刻 scripts/parse-douyin-video.js 的逻辑（但只取 desc 文本，不下载视频）。
    返回 (title, text)
    """
    # 1) 从 URL 抽取 modal_id / awemeId
    aweme_id = ""
    m = re.search(r"modal_id=([0-9]+)", url)
    if m:
        aweme_id = m.group(1)
    else:
        m = re.search(r"video/([^/?]+)", url)
        if m:
            aweme_id = m.group(1)
        else:
            m = re.search(r"note/([^/?]+)", url)
            if m:
                aweme_id = m.group(1)

    if not aweme_id:
        raise RuntimeError(f"无法从抖音 URL 中提取视频ID: {url}")

    request_url = f"https://www.douyin.com/jingxuan?modal_id={aweme_id}"
    headers = {
        "User-Agent": UA_COMMON,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://www.douyin.com/",
        "Connection": "keep-alive",
    }

    resp = get_session().get(request_url, headers=headers, timeout=HTTP_TIMEOUT, allow_redirects=True)
    resp.raise_for_status()
    html_content = resp.text or ""

    # 复刻 JS 的提取：在 HTML 中找 JSON 字符串片段（playAddr/searchProps/app）
    pattern = re.compile(r'"([^"]*?(?:playAddr|searchProps|app)[^"]*?)"', flags=re.DOTALL)
    matches = pattern.findall(html_content)
    target_match = ""
    for m in matches:
        if "playAddr" in m and "searchProps" in m and "app" in m:
            target_match = m
            break
    if not target_match:
        raise RuntimeError("未找到包含视频数据的 JSON 片段")

    # decodeURIComponent
    from urllib.parse import unquote

    decoded_json = unquote(target_match)
    video_data_json = json.loads(decoded_json)
    video_detail = ((video_data_json or {}).get("app") or {}).get("videoDetail") or {}
    desc = video_detail.get("desc") or ""
    return desc, desc


def extract_weibo_body(weibo_url: str) -> Tuple[str, str]:
    # 如果你只要多渠道，不传 weibo，这个也可忽略；先保留稳定实现
    # 抽 weiboId
    m = re.search(r"weibo\.com/\d+/([a-zA-Z0-9]+)", weibo_url)
    if not m:
        m = re.search(r"m\.weibo\.cn/status/([a-zA-Z0-9]+)", weibo_url)
    if not m:
        m = re.search(r"weibo\.com/\d+/([a-zA-Z0-9]+)\?", weibo_url)
    if not m:
        # fallback: 最后一段
        parts = [p for p in weibo_url.split("/") if p]
        if parts:
            last = parts[-1]
            if "?" not in last:
                m = re.match(r"(.+)", last)
    if not m:
        raise RuntimeError(f"无法从微博 URL 提取 weiboId: {weibo_url}")
    weibo_id = m.group(1)

    api_url = f"https://m.weibo.cn/statuses/show?id={weibo_id}"
    headers = {
        "User-Agent": UA_COMMON,
        "Referer": "https://m.weibo.cn/",
        "X-Requested-With": "XMLHttpRequest",
    }
    resp = get_session().get(api_url, headers=headers, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    if data.get("ok") != 1:
        raise RuntimeError(f"Weibo API error: {data}")
    obj = data.get("data") or {}
    text = obj.get("text") or ""
    if not text and isinstance(obj.get("longText"), str):
        text = obj.get("longText")
    return "", _strip_html_like(text)


def extract_by_channel(source_channel: str, original_url: str) -> Tuple[str, str, str, str, str]:
    """
    返回：
    - title
    - text（正文/摘要）
    - visual（可选：用于 build-content-analysis 的画面证据）
    - platform（用于 evidence）
    - media_type（用于 evidence）
    """
    platform, media_type = SOURCE_CHANNEL_VALUE_TO_PLATFORM.get(source_channel, (source_channel, "未知"))

    # 优先按渠道抓取
    if source_channel == "抖音APP":
        title, text = extract_douyin_desc_from_url(original_url)
        visual = ""
        return title or "", text or "", visual, platform, media_type

    # 其他渠道：meta/json-ld best effort
    html = http_get_text(original_url)
    title, desc = extract_meta_description(html)
    visual = ""
    # 简单兜底：如果只拿到 title，visual 也可以提供一定信息
    if not desc and title:
        visual = f"标题：{title}"

    # 特殊：如果酷安/快手 URL 返回的是 JSON/渲染失败页面，desc 可能为空
    # 这里不强行写空内容交由上层判断
    return title or "", desc or "", visual, platform, media_type


def build_analysis_for_record(source_channel: str, original_url: str) -> str:
    title, text, visual, platform, media_type = extract_by_channel(source_channel, original_url)
    # 只要 text/title 非空就尽量产出解析；否则直接返回空（由上层决定是否跳过写回）
    if not title and not text:
        return ""
    return build_content_analysis(
        title=title,
        text=text,
        platform=platform,
        media_type=media_type,
        visual=visual,
        max_chars=MAX_CHARS,
    )


def main() -> None:
    if not BITABLE_URL:
        raise RuntimeError("请设置环境变量 BITABLE_URL（飞书多维表链接）")

    token = get_tenant_access_token()
    print(f"获取飞书 token 成功")

    targets = fetch_targets(token)
    print(f"筛选到需要处理的记录：{len(targets)} 条（渠道：{', '.join(SOURCE_CHANNELS)})")
    if not targets:
        return

    updates: List[Dict[str, Any]] = []
    errors: List[Tuple[str, str]] = []

    def _task(t: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        record_id = t["record_id"]
        ch = t["source_channel"]
        url = t["original_url"]
        content_val = build_analysis_for_record(ch, url)
        if not content_val:
            return None
        return {"record_id": record_id, "fields": {CONTENT_ANALYSIS_FIELD: content_val}}

    with ThreadPoolExecutor(max_workers=max(1, WORKERS)) as ex:
        fut_to_t = {ex.submit(_task, t): t for t in targets}
        done = 0
        total = len(fut_to_t)
        for fut in as_completed(fut_to_t):
            done += 1
            t = fut_to_t[fut]
            rid = t["record_id"]
            try:
                u = fut.result()
                if u:
                    updates.append(u)
                print(f"  [{done}/{total}] record_id={rid} ok")
            except Exception as e:
                errors.append((rid, str(e)))
                print(f"  [{done}/{total}] record_id={rid} err: {e}")

    if updates:
        chunk_size = 50
        for i in range(0, len(updates), chunk_size):
            batch_update_records(token, updates[i : i + chunk_size])
            print(f"已回填 {min(i + chunk_size, len(updates))}/{len(updates)} 条")

    if errors:
        print("\n回填失败（前 10 条）：")
        for rid, msg in errors[:10]:
            print(f"- record_id={rid}: {msg}")
        print(f"失败总数：{len(errors)}")

    print(f"\n完成：成功回填 {len(updates)} 条，失败 {len(errors)} 条")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"执行失败: {e}")
        raise

