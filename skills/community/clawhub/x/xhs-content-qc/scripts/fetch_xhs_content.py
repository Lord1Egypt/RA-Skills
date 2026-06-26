from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import subprocess
import sys
from typing import Any


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def _strip_tags(html: str) -> str:
    # 简单去标签：用于“尽量拿到可读文本”，不追求 100% 准确。
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _extract_meta(html: str, prop: str) -> str | None:
    # property="og:title" content="..."
    m = re.search(
        rf'property=["\']{re.escape(prop)}["\']\s+content=["\']([^"\']+)["\']',
        html,
        flags=re.I,
    )
    if m:
        return m.group(1).strip()
    # name="description" content="..."
    m2 = re.search(
        rf'name=["\']{re.escape(prop)}["\']\s+content=["\']([^"\']+)["\']',
        html,
        flags=re.I,
    )
    if m2:
        return m2.group(1).strip()
    return None


def _extract_title(html: str) -> str | None:
    for meta_prop in ("og:title", "twitter:title"):
        v = _extract_meta(html, meta_prop)
        if v:
            return v
    m = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.I | re.S)
    if m:
        return html_lib.unescape(m.group(1)).strip()
    return None


def _extract_hashtags(text: str, max_tags: int) -> list[str]:
    # 仅做启发式：匹配 # + 1~30 个字母数字或中文字符（不含空格）
    tags = re.findall(r"#[A-Za-z0-9_\u4e00-\u9fff]{1,30}", text)
    # 去重保持顺序
    seen: set[str] = set()
    out: list[str] = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            out.append(t)
        if len(out) >= max_tags:
            break
    return out


def _extract_ats(text: str, max_ats: int) -> list[str]:
    # 允许英文账号中间有一个空格（如 @BUBBLE TREE达人体验官）
    # 不保证完全准确，但能覆盖常见“@英文 + 可跟中文后缀”的形式。
    ats = re.findall(
        r"@[A-Za-z0-9_]+(?:\s+[A-Za-z0-9_]+)?(?:[A-Za-z0-9_\u4e00-\u9fff]{0,20})",
        text,
    )
    seen: set[str] = set()
    out: list[str] = []
    for a in ats:
        if a not in seen:
            seen.add(a)
            out.append(a)
        if len(out) >= max_ats:
            break
    return out


def fetch_html_with_curl(url: str, *, timeout_s: int, user_agent: str) -> tuple[int | None, str | None, str]:
    # 返回 (http_code, effective_url, html)
    marker_code = "__HTTP_CODE__:"
    marker_url = "__URL_EFFECTIVE__:"
    cmd = [
        "curl",
        "-sL",
        "-A",
        user_agent,
        "--max-redirs",
        "5",
        "--connect-timeout",
        str(timeout_s),
        url,
        "-w",
        f"\n{marker_code}%{{http_code}}\n{marker_url}%{{url_effective}}\n",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
    out = proc.stdout or ""

    http_code: int | None = None
    effective_url: str | None = None

    idx = out.rfind(marker_code)
    if idx != -1:
        html = out[:idx].rstrip()
        m_code = re.search(rf'{re.escape(marker_code)}(\d+)', out)
        if m_code:
            http_code = int(m_code.group(1))
        m_url = re.search(rf'{re.escape(marker_url)}(.+)', out)
        if m_url:
            effective_url = m_url.group(1).strip()
        return http_code, effective_url, html

    # 如果没找到 marker，仍返回 stdout 作为 html
    return None, None, out


def main() -> None:
    parser = argparse.ArgumentParser(description="尽量抓取小红书链接可读内容（标题/话题/@/文本预览）")
    parser.add_argument("--url", required=True, help="小红书笔记链接（xiaohongshu.com/explore/... 或 xhslink.com/...）")
    parser.add_argument("--timeout-s", type=int, default=15)
    parser.add_argument("--max-chars", type=int, default=20000)
    parser.add_argument("--max-tags", type=int, default=80)
    parser.add_argument("--max-ats", type=int, default=20)
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    args = parser.parse_args()

    url: str = args.url
    http_code: int | None = None
    effective_url: str | None = None
    html: str

    # 这里优先 curl：在部分环境里 httpx 可能触发 403；curl 更贴近 skill 里使用的 GET。
    http_code, effective_url, html = fetch_html_with_curl(
        url, timeout_s=args.timeout_s, user_agent=args.user_agent
    )

    title = _extract_title(html) if html else None
    desc = _extract_meta(html, "og:description") or _extract_meta(html, "description")

    text = _strip_tags(html) if html else ""
    if args.max_chars > 0:
        text_preview = text[: args.max_chars]
    else:
        text_preview = text

    hashtags = _extract_hashtags(text, args.max_tags) if text else []
    ats = _extract_ats(text, args.max_ats) if text else []

    result: dict[str, Any] = {
        "url": url,
        "http_status": http_code,
        "final_url": effective_url,
        "title": title,
        "description": desc,
        "hashtags": hashtags,
        "ats": ats,
        "text_preview": text_preview,
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

