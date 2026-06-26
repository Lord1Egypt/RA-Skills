#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将“新浪微博”的微博正文解析结果回填到飞书多维表字段「内容解析」。

筛选逻辑：
- 来源渠道 == "新浪微博"
- 内容解析 为空时才回填（可用 ONLY_EMPTY=0 强制覆盖）

解析逻辑：
- 从记录字段中读取微博原文URL（优先字段名：获取原文URL，其次原文 URL/原文URL/原文url 等）
- 提取 weiboId
- 调用：https://m.weibo.cn/statuses/show?id={weiboId}
- 取返回数据中的 data.text，并去掉尖括号内容（近似去 HTML 标签）
- 截断到 MAX_CHARS（默认 100）
"""

import json
import os
import re
import sys
import time
from html import unescape
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


APP_ID = os.getenv("APP_ID", "").strip()
APP_SECRET = os.getenv("APP_SECRET", "").strip()
BITABLE_URL = os.getenv("BITABLE_URL", "").strip()

# 业务字段名（以你们多维表实际为准；脚本也会做候选字段兜底）
SOURCE_CHANNEL_FIELD = os.getenv("SOURCE_CHANNEL_FIELD", "来源渠道").strip()  # 字段名
CONTENT_ANALYSIS_FIELD = os.getenv("CONTENT_ANALYSIS_FIELD", "内容解析").strip()  # 字段名

# 你提到的“获取原文URL”（可能也有人用“原文 URL”）
WEIBO_ORIGINAL_URL_CANDIDATES = [
    os.getenv("WEIBO_ORIGINAL_URL_FIELD", "").strip() or "",  # 用户可显式指定
    "获取原文URL",
    "原文 URL",
    "原文URL",
    "原文url",
]
WEIBO_ORIGINAL_URL_CANDIDATES = [x for x in WEIBO_ORIGINAL_URL_CANDIDATES if x]

SOURCE_CHANNEL_VALUE = os.getenv("SOURCE_CHANNEL_VALUE", "新浪微博").strip()

ONLY_EMPTY = os.getenv("ONLY_EMPTY", "1").strip().lower() in ("1", "true", "yes")
MAX_CHARS = int(os.getenv("MAX_CHARS", "100"))
LIMIT = int(os.getenv("LIMIT", "50"))  # 本次最多处理多少条匹配记录
PAGE_SIZE = int(os.getenv("PAGE_SIZE", "500"))
WORKERS = int(os.getenv("WORKERS", "3"))

WEIBO_REQUEST_TIMEOUT = int(os.getenv("WEIBO_REQUEST_TIMEOUT", "15"))
WEIBO_MAX_RETRIES = int(os.getenv("WEIBO_MAX_RETRIES", "2"))


def _safe_text(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        if not v:
            return ""
        v = v[0]
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False)
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


def get_session() -> requests.Session:
    s = requests.Session()
    return s


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


def pick_first_field(fields: Dict[str, Any], candidates: List[str]) -> str:
    for c in candidates:
        if c in fields:
            v = _safe_text(fields.get(c))
            if v:
                return v
    return ""


def extract_weibo_id(url: str) -> Optional[str]:
    if not url:
        return None

    patterns = [
        # https://weibo.com/7976115583/QwgTm2OVI
        re.compile(r"weibo\.com\/\d+\/([a-zA-Z0-9]+)"),
        # https://m.weibo.cn/status/xxxxx
        re.compile(r"m\.weibo\.cn\/status\/([a-zA-Z0-9]+)"),
        # 带参数的情况
        re.compile(r"weibo\.com\/\d+\/([a-zA-Z0-9]+)\?"),
    ]
    for pat in patterns:
        m = pat.search(url)
        if m:
            return m.group(1)

    # fallback: 最后一段（不含 '?'）
    parts = [p for p in url.split("/") if p]
    if not parts:
        return None
    last = parts[-1]
    if last and "?" not in last:
        return last
    return None


_HTML_TAG_RE = re.compile(r"<[^>]*>")


def strip_html_like(text: str) -> str:
    # 微博返回 text 往往包含尖括号包装的信息，这里用正则去掉
    t = unescape(text or "")
    t = _HTML_TAG_RE.sub("", t)
    # 收敛连续空白
    t = re.sub(r"\s+", " ", t).strip()
    return t


def fetch_weibo_text(weibo_id: str) -> str:
    api_url = f"https://m.weibo.cn/statuses/show?id={weibo_id}"

    last_err: Optional[Exception] = None
    for attempt in range(WEIBO_MAX_RETRIES + 1):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
                "Referer": "https://m.weibo.cn/",
                "X-Requested-With": "XMLHttpRequest",
            }
            resp = get_session().get(api_url, headers=headers, timeout=WEIBO_REQUEST_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            if data.get("ok") != 1:
                raise RuntimeError(f"Weibo API error: {data}")
            obj = data.get("data") or {}
            text = obj.get("text") or ""
            # 有些长文接口可能在 longText 出现（尽量兜底）
            if not text and isinstance(obj.get("longText"), str):
                text = obj.get("longText")
            return strip_html_like(text)
        except Exception as e:
            last_err = e
            # 退避一点点，避免瞬时限流
            time.sleep(0.8 * (2 ** attempt))
    if last_err:
        raise last_err
    return ""


def fetch_records(token: str) -> List[Dict[str, Any]]:
    if not BITABLE_URL:
        raise RuntimeError("请设置环境变量 BITABLE_URL（飞书多维表链接）")
    app_token, table_id = parse_bitable_url(BITABLE_URL)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    headers = {"Authorization": f"Bearer {token}"}
    params: Dict[str, Any] = {"page_size": PAGE_SIZE}

    result: List[Dict[str, Any]] = []
    page_token: Optional[str] = None
    while True:
        if page_token:
            params["page_token"] = page_token
        resp = get_session().get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"获取记录失败: {data}")

        obj = data.get("data") or {}
        items = obj.get("items") or []
        result.extend(items)

        page_token = obj.get("page_token")
        has_more = obj.get("has_more")
        if not has_more or not page_token:
            break
        if len(result) >= LIMIT:
            # 这里直接按 LIMIT 限制，避免拉太多
            result = result[:LIMIT]
            break
    return result


def batch_update_records(token: str, updates: List[Dict[str, Any]]) -> None:
    if not updates:
        return
    if not BITABLE_URL:
        raise RuntimeError("BITABLE_URL 未初始化")
    app_token, table_id = parse_bitable_url(BITABLE_URL)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"records": updates}
    resp = get_session().post(
        url,
        headers=headers,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"批量更新失败: {data}")


def build_content_value(body: str) -> str:
    body = strip_html_like(body)
    if MAX_CHARS > 0 and len(body) > MAX_CHARS:
        return body[: MAX_CHARS - 1] + "…"
    return body


def main() -> None:
    if not BITABLE_URL:
        raise RuntimeError("请设置环境变量 BITABLE_URL（飞书多维表链接）")

    token = get_tenant_access_token()
    print(f"获取飞书 token 成功")

    records = fetch_records(token)
    print(f"共拉取 {len(records)} 条记录（含分页，已按 LIMIT 限制）")

    # 1) 先在本地筛选出需要的微博记录
    targets: List[Dict[str, Any]] = []
    for rec in records:
        fields = rec.get("fields") or {}
        channel = _safe_text(fields.get(SOURCE_CHANNEL_FIELD))
        if channel != SOURCE_CHANNEL_VALUE:
            continue

        existing = _safe_text(fields.get(CONTENT_ANALYSIS_FIELD))
        if ONLY_EMPTY and existing:
            continue

        weibo_url = pick_first_field(fields, WEIBO_ORIGINAL_URL_CANDIDATES)
        if not weibo_url:
            continue

        record_id = rec.get("record_id")
        if not record_id:
            continue

        targets.append(
            {
                "record_id": record_id,
                "weibo_url": weibo_url,
            }
        )

    print(f"筛选到需要回填的记录：{len(targets)} 条（来源渠道={SOURCE_CHANNEL_VALUE}）")
    if not targets:
        return

    # 2) 并发抓取微博正文
    updates: List[Dict[str, Any]] = []
    errors: List[Tuple[str, str]] = []  # (record_id, err)

    def _task(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        record_id = item["record_id"]
        weibo_url = item["weibo_url"]
        weibo_id = extract_weibo_id(weibo_url)
        if not weibo_id:
            raise RuntimeError(f"无法从微博 URL 提取 weiboId: {weibo_url}")
        body = fetch_weibo_text(weibo_id)
        if not body:
            # 微博正文为空时也不强写，避免覆盖成空
            return None
        content_val = build_content_value(body)
        return {"record_id": record_id, "fields": {CONTENT_ANALYSIS_FIELD: content_val}}

    with ThreadPoolExecutor(max_workers=max(1, WORKERS)) as ex:
        fut_to_item = {ex.submit(_task, t): t for t in targets}
        completed = 0
        total = len(fut_to_item)
        for fut in as_completed(fut_to_item):
            completed += 1
            item = fut_to_item[fut]
            rid = item["record_id"]
            try:
                u = fut.result()
                if u:
                    updates.append(u)
                print(f"  [{completed}/{total}] record_id={rid} ok")
            except Exception as e:
                errors.append((rid, str(e)))
                print(f"  [{completed}/{total}] record_id={rid} err: {e}")

    # 3) 批量回填（分片）
    if updates:
        chunk_size = 50
        for i in range(0, len(updates), chunk_size):
            batch_update_records(token, updates[i : i + chunk_size])
            print(f"已回填 {min(i + chunk_size, len(updates))}/{len(updates)} 条")

    if errors:
        print("\n以下记录回填失败（仅输出前 10 条）：")
        for rid, msg in errors[:10]:
            print(f"- record_id={rid}: {msg}")

    print(f"\n完成：成功回填 {len(updates)} 条，失败 {len(errors)} 条")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"执行失败: {e}", file=sys.stderr)
        sys.exit(1)

