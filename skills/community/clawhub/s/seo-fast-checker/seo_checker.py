#!/usr/bin/env python3
"""SEO优化检查器 - 输入网址一键输出SEO诊断报告"""

import argparse
import json
import os
import re
import sys
import textwrap
import time
from collections import Counter
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag


# ── 工具函数 ─────────────────────────────────────────────────────

def fetch_page(url: str, timeout: int = 15) -> tuple[requests.Response, float]:
    """获取页面并记录耗时"""
    start = time.time()
    resp = requests.get(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        },
        timeout=timeout,
        allow_redirects=True,
    )
    elapsed = time.time() - start
    return resp, elapsed


def extract_domain(url: str) -> str:
    return urlparse(url).netloc


def human_size(bytes_: int) -> str:
    if bytes_ < 1024:
        return f"{bytes_} B"
    elif bytes_ < 1024**2:
        return f"{bytes_ / 1024:.1f} KB"
    return f"{bytes_ / (1024**2):.1f} MB"


# ── SEO 检查单元 ─────────────────────────────────────────────────

SeoIssue = dict  # type: {"severity": str, "item": str, "status": str, "detail": str}


def check_title(soup: BeautifulSoup) -> list[SeoIssue]:
    issues = []
    title_tag = soup.find("title")
    if not title_tag or not title_tag.string or not title_tag.string.strip():
        issues.append({"severity": "🔴", "item": "标题标签", "status": "缺失", "detail": "页面没有 <title> 标签，严重影响 SEO"})
    else:
        t = title_tag.string.strip()
        length = len(t)
        if length < 10:
            issues.append({"severity": "🟡", "item": "标题标签", "status": "太短", "detail": f"标题仅 {length} 个字符，建议 10-60 个字符"})
        elif length > 60:
            issues.append({"severity": "🟡", "item": "标题标签", "status": "太长", "detail": f"标题 {length} 个字符，建议不超过 60 个字符（会被截断）"})
        else:
            issues.append({"severity": "🟢", "item": "标题标签", "status": "良好", "detail": f"'{t}' ({length} 字符)"})
    return issues


def check_meta_description(soup: BeautifulSoup) -> list[SeoIssue]:
    issues = []
    meta = soup.find("meta", attrs={"name": "description"})
    if not meta or not meta.get("content", "").strip():
        issues.append({"severity": "🔴", "item": "Meta Description", "status": "缺失", "detail": "没有 meta description，影响搜索结果点击率"})
    else:
        content = meta["content"].strip()
        length = len(content)
        if length < 50:
            issues.append({"severity": "🟡", "item": "Meta Description", "status": "太短", "detail": f"仅 {length} 字符，建议 50-160 字符"})
        elif length > 160:
            issues.append({"severity": "🟡", "item": "Meta Description", "status": "太长", "detail": f"{length} 字符，建议不超过 160 字符"})
        else:
            issues.append({"severity": "🟢", "item": "Meta Description", "status": "良好", "detail": f"'{content[:80]}...' ({length} 字符)"})
    return issues


def check_headings(soup: BeautifulSoup) -> list[SeoIssue]:
    issues = []
    h1_tags = soup.find_all("h1")
    if len(h1_tags) == 0:
        issues.append({"severity": "🔴", "item": "H1 标签", "status": "缺失", "detail": "页面没有 H1 标签，严重影响 SEO 结构"})
    elif len(h1_tags) > 1:
        issues.append({"severity": "🟡", "item": "H1 标签", "status": "过多", "detail": f"页面有 {len(h1_tags)} 个 H1，建议每页仅使用一个 H1"})
    else:
        text = h1_tags[0].get_text(strip=True)
        issues.append({"severity": "🟢", "item": "H1 标签", "status": "良好", "detail": f"'{text[:80]}'"})

    # 检查 heading 层级
    all_headings = []
    for tag_name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        for tag in soup.find_all(tag_name):
            all_headings.append(tag.name)
    issues.append({"severity": "🟢", "item": "Heading 层级", "status": "信息", "detail": f"各层级数量: {', '.join(f'{h}={all_headings.count(h)}' for h in sorted(set(all_headings)))}"})
    return issues


def check_keyword_density(soup: BeautifulSoup, url: str) -> list[SeoIssue]:
    issues = []
    text = soup.get_text(separator=" ", strip=True)
    # 从 URL 和标题推断核心关键词
    path = urlparse(url).path.strip("/").replace("-", " ").replace("_", " ")
    words = re.findall(r"\w+", text.lower())
    # 过滤非中文/太短的词
    filtered = [w for w in words if len(w) > 2]
    total = len(filtered)
    if total == 0:
        return issues
    counter = Counter(filtered)
    top_keywords = counter.most_common(10)
    details = "; ".join(f"'{kw}'={freq}次({freq/total*100:.1f}%)" for kw, freq in top_keywords[:5])
    issues.append({"severity": "🟢", "item": "关键词密度", "status": "信息", "detail": f"总词数: {total}，Top5: {details}"})
    return issues


def check_images_alt(soup: BeautifulSoup) -> list[SeoIssue]:
    issues = []
    imgs = soup.find_all("img")
    total = len(imgs)
    missing_alt = 0
    for img in imgs:
        if not img.get("alt") or not img["alt"].strip():
            missing_alt += 1

    if total == 0:
        issues.append({"severity": "🟢", "item": "图片 Alt 属性", "status": "无图片", "detail": "页面未包含图片"})
    else:
        ratio = missing_alt / total * 100
        if missing_alt == 0:
            issues.append({"severity": "🟢", "item": "图片 Alt 属性", "status": "良好", "detail": f"所有 {total} 张图片都有 alt 属性"})
        elif ratio < 30:
            issues.append({"severity": "🟡", "item": "图片 Alt 属性", "status": "部分缺失", "detail": f"{total} 张图片中 {missing_alt} 张缺少 alt ({ratio:.0f}%)"})
        else:
            issues.append({"severity": "🔴", "item": "图片 Alt 属性", "status": "严重缺失", "detail": f"{total} 张图片中 {missing_alt} 张缺少 alt ({ratio:.0f}%)"})
    return issues


def check_canonical(soup: BeautifulSoup, url: str) -> list[SeoIssue]:
    issues = []
    link = soup.find("link", rel="canonical")
    if link and link.get("href"):
        issues.append({"severity": "🟢", "item": "Canonical URL", "status": "已设置", "detail": f"{link['href']}"})
    else:
        issues.append({"severity": "🟡", "item": "Canonical URL", "status": "未设置", "detail": "没有 canonical 标签，可能有重复内容问题"})
    return issues


def check_meta_viewport(soup: BeautifulSoup) -> list[SeoIssue]:
    issues = []
    vp = soup.find("meta", attrs={"name": "viewport"})
    if vp:
        issues.append({"severity": "🟢", "item": "移动端适配", "status": "已设置", "detail": f"viewport: {vp.get('content', '')}"})
    else:
        issues.append({"severity": "🔴", "item": "移动端适配", "status": "缺失", "detail": "没有 viewport meta 标签，移动端体验差"})
    return issues


def check_og_tags(soup: BeautifulSoup) -> list[SeoIssue]:
    issues = []
    og_tags = soup.find_all("meta", attrs={"property": re.compile(r"^og:")})
    twitter_tags = soup.find_all("meta", attrs={"name": re.compile(r"^twitter:")})
    if og_tags:
        details = "; ".join(f"{t.get('property')}={t.get('content', '')[:30]}" for t in og_tags[:4])
        issues.append({"severity": "🟢", "item": "Open Graph", "status": "已设置", "detail": details})
    else:
        issues.append({"severity": "🟡", "item": "Open Graph", "status": "未设置", "detail": "没有 og 标签，社交分享效果差"})

    if twitter_tags:
        issues.append({"severity": "🟢", "item": "Twitter Card", "status": "已设置", "detail": f"{len(twitter_tags)} 个标签"})
    else:
        issues.append({"severity": "🟡", "item": "Twitter Card", "status": "未设置", "detail": "没有 twitter card 标签"})
    return issues


def check_robots(soup: BeautifulSoup) -> list[SeoIssue]:
    issues = []
    meta_robots = soup.find("meta", attrs={"name": "robots"})
    if meta_robots:
        content = meta_robots.get("content", "")
        issues.append({"severity": "🟡", "item": "Robots Meta", "status": "已设置", "detail": f"robots: {content}"})
    else:
        issues.append({"severity": "🟢", "item": "Robots Meta", "status": "未设置", "detail": "没有 robots meta（默认允许索引）"})
    return issues


def check_json_ld(soup: BeautifulSoup) -> list[SeoIssue]:
    issues = []
    scripts = soup.find_all("script", type="application/ld+json")
    if scripts:
        issues.append({"severity": "🟢", "item": "结构化数据(JSON-LD)", "status": "已设置", "detail": f"发现 {len(scripts)} 个结构化数据块"})
    else:
        issues.append({"severity": "🟡", "item": "结构化数据(JSON-LD)", "status": "未设置", "detail": "没有 JSON-LD 结构化数据，错失富媒体搜索结果机会"})
    return issues


def check_page_speed(resp: requests.Response, elapsed: float) -> list[SeoIssue]:
    issues = []
    size = len(resp.content)
    issues.append({"severity": "🟢", "item": "页面加载时间", "status": "信息", "detail": f"{elapsed:.2f}s (从服务器获取)"})
    if size > 500 * 1024:
        issues.append({"severity": "🔴", "item": "页面大小", "status": "过大", "detail": f"{human_size(size)}，建议控制在 300KB 以内"})
    elif size > 300 * 1024:
        issues.append({"severity": "🟡", "item": "页面大小", "status": "较大", "detail": f"{human_size(size)}，建议优化"})
    else:
        issues.append({"severity": "🟢", "item": "页面大小", "status": "良好", "detail": f"{human_size(size)}"})
    return issues


def check_links(soup: BeautifulSoup, base_url: str) -> list[SeoIssue]:
    issues = []
    links = soup.find_all("a", href=True)
    internal = 0
    external = 0
    broken = 0
    domain = extract_domain(base_url)
    for a in links:
        href = a["href"].strip()
        if href.startswith("#") or href.startswith("javascript:"):
            continue
        full_url = urljoin(base_url, href)
        if extract_domain(full_url) == domain:
            internal += 1
        else:
            external += 1
    issues.append({"severity": "🟢", "item": "链接统计", "status": "信息", "detail": f"内部链接: {internal} 个，外部链接: {external} 个"})
    return issues


# ── AI 增强分析 ─────────────────────────────────────────────────

def ai_analysis(url: str, raw_html: str) -> str:
    """调用 AI 进行增强分析"""
    try:
        from openai import OpenAI
    except ImportError:
        return "错误: 需要安装 openai 库。运行: pip install openai"

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "错误: 请设置环境变量 OPENAI_API_KEY"

    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=api_key)

    # 提取前 5000 字符进行 AI 分析
    text = BeautifulSoup(raw_html, "html.parser").get_text(separator=" ", strip=True)[:5000]

    prompt = textwrap.dedent(f"""\
        你是一位 SEO 专家。请对以下网页内容进行 SEO 分析，给出具体的优化建议。

        URL: {url}

        页面内容（前5000字符）：
        {text}

        请以 Markdown 格式输出分析报告，包含以下内容：
        1. 内容质量评估（原创性、价值性、相关性）
        2. 关键词策略建议（推荐的核心关键词）
        3. 内容优化建议（标题改进、内容补充方向）
        4. 用户体验建议（可读性、结构、CTA等）
        5. 优先级排序（哪些改进最紧急）

        注意：输出不要太长，但要具体可执行。
    """)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一位资深的 SEO 优化专家，精通百度 SEO 和 Google SEO。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
    )
    return resp.choices[0].message.content or ""


# ── 报告渲染 ────────────────────────────────────────────────────

def generate_report(url: str, issues: list[SeoIssue], ai_text: str | None = None) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    severity_order = {"🔴": 0, "🟡": 1, "🟢": 2}

    critical = [i for i in issues if i["severity"] == "🔴"]
    warning = [i for i in issues if i["severity"] == "🟡"]
    passed = [i for i in issues if i["severity"] == "🟢"]

    lines = [
        f"# SEO 诊断报告",
        f"",
        f"**URL**: {url}",
        f"**检测时间**: {now}",
        f"",
        f"---",
        f"",
        f"## 总览",
        f"",
        f"| 严重问题 🔴 | 建议优化 🟡 | 良好 🟢 |",
        f"|-----------|------------|--------|",
        f"| {len(critical)} | {len(warning)} | {len(passed)} |",
        f"",
        f"---",
        f"",
    ]

    if critical:
        lines.append("## 🔴 严重问题（必须修复）")
        lines.append("")
        for i in critical:
            lines.append(f"### {i['item']}")
            lines.append(f"- **状态**: {i['status']}")
            lines.append(f"- **详情**: {i['detail']}")
            lines.append("")

    if warning:
        lines.append("## 🟡 建议优化")
        lines.append("")
        for i in warning:
            lines.append(f"### {i['item']}")
            lines.append(f"- **状态**: {i['status']}")
            lines.append(f"- **详情**: {i['detail']}")
            lines.append("")

    lines.append("## 🟢 良好项")
    lines.append("")
    for i in passed:
        lines.append(f"- **{i['item']}**: {i['detail']}")
    lines.append("")

    if ai_text:
        lines.append("---")
        lines.append("")
        lines.append("## 🤖 AI 增强分析")
        lines.append("")
        lines.append(ai_text)
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*报告由 SEO Checker 自动生成*")

    return "\n".join(lines)


# ── 主入口 ───────────────────────────────────────────────────────

def analyze_url(url: str, use_ai: bool = False) -> str:
    """分析单个 URL 并返回报告"""
    # 确保 URL 有协议
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print(f"正在分析: {url} ...", file=sys.stderr)

    try:
        resp, elapsed = fetch_page(url)
    except requests.exceptions.RequestException as e:
        return f"# SEO 诊断报告\n\n**URL**: {url}\n\n**错误**: 无法访问页面 - {e}\n"

    soup = BeautifulSoup(resp.text, "html.parser")

    issues: list[SeoIssue] = []
    issues.extend(check_title(soup))
    issues.extend(check_meta_description(soup))
    issues.extend(check_headings(soup))
    issues.extend(check_keyword_density(soup, url))
    issues.extend(check_images_alt(soup))
    issues.extend(check_canonical(soup, url))
    issues.extend(check_meta_viewport(soup))
    issues.extend(check_og_tags(soup))
    issues.extend(check_robots(soup))
    issues.extend(check_json_ld(soup))
    issues.extend(check_page_speed(resp, elapsed))
    issues.extend(check_links(soup, url))

    ai_text = None
    if use_ai:
        print("正在调用 AI 进行增强分析...", file=sys.stderr)
        ai_text = ai_analysis(url, resp.text)

    return generate_report(url, issues, ai_text)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="SEO优化检查器 — 输入网址一键输出SEO诊断报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("urls", nargs="+", help="要检查的网址（支持多个）")
    parser.add_argument("--output", "-o", type=str, default=None, help="输出文件路径")
    parser.add_argument("--ai", action="store_true", help="启用 AI 增强分析（需 OPENAI_API_KEY）")

    args = parser.parse_args()

    reports = []
    for url in args.urls:
        report = analyze_url(url, args.ai)
        reports.append(report)

    full = "\n\n".join(reports)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(full)
        print(f"报告已保存至: {args.output}", file=sys.stderr)
    else:
        print(full)


if __name__ == "__main__":
    main()
