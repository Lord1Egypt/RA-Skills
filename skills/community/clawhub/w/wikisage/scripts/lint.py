#!/usr/bin/env python3
"""
Wiki Lint 脚本（Karpathy LLM Wiki 模式 · Layer 1 机械扫描）

Layer 1：机械扫描，写报告 + 打印摘要到 stdout
Layer 2：LLM 介入整理（由用户说「整理 wiki」触发，不是这个脚本的事）

用法：
  python3 lint.py                    # 完整 lint
  python3 lint.py --quick            # 轻量 lint（ingest 后触发）
  python3 lint.py --wiki-root /path  # 自定义 wiki 根目录（也可用 $WIKI_ROOT）
  python3 lint.py --summary          # 只打印一行摘要到 stdout（给 cron pipe 用）
  python3 lint.py --no-log           # 不写 log.md（预览模式）

环境变量：
  WIKI_ROOT          wiki markdown 根目录（默认 ~/.openclaw/workspace/wiki）

报告产出：
  $WIKI_ROOT/.lint-history/YYYY-MM-DD.md   # 持久化报告
  stdout                                    # 完整报告或一行摘要（带 --summary）

推送通知？自行在 cron/Task Scheduler 里 pipe：
  python3 lint.py --summary | mail -s 'wiki lint' you@example.com
  python3 lint.py --summary | xargs -I{} openclaw message send --target user:xxx --message {}
  python3 lint.py --summary | curl -X POST -d @- https://hooks.slack.com/services/...
"""

import os
import re
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


def default_wiki_root() -> Path:
    env = os.environ.get("WIKI_ROOT")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".openclaw/workspace/wiki"


# "缺失交叉引用"判定：两个页面如果标题/标签相似度高，但互相没 [[链接]]，可能漏了交叉引用
# 简化版：同目录下的页面，如果页面 A 的正文提到页面 B 的标题（非 [[]] 包裹），算"可能缺交叉引用"
SKIP_MENTION_CHECK_DIRS = {"sources", "raw", ".lint-history"}


def find_all_pages(wiki_dir: Path):
    pages_dir = wiki_dir / "pages"
    if not pages_dir.exists():
        return []
    return sorted(pages_dir.rglob("*.md"))


def extract_title(page_path: Path) -> str:
    """从页面第一行 # 标题 提取标题"""
    try:
        content = page_path.read_text(errors="ignore")
        m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        return m.group(1).strip() if m else page_path.stem
    except Exception:
        return page_path.stem


def extract_links(content: str):
    """提取所有 [[链接]]"""
    return re.findall(r"\[\[([^\]]+)\]\]", content)


def check_index_consistency(wiki_dir: Path):
    issues = []
    index_file = wiki_dir / "index.md"
    if not index_file.exists():
        return [f"❌ index.md 不存在：{index_file}"]

    index_content = index_file.read_text()
    index_links = set(extract_links(index_content))
    actual_pages = {p.stem for p in find_all_pages(wiki_dir)}

    for link in index_links:
        slug = link.replace(" ", "-").lower()
        if link not in actual_pages and slug not in actual_pages:
            issues.append(f"  📋 index.md 有条目但文件不存在：[[{link}]]")

    for page in actual_pages:
        if page not in index_links and page.replace("-", " ") not in index_links:
            issues.append(f"  📋 文件存在但 index.md 未记录：{page}.md")

    return issues


def check_orphan_pages(wiki_dir: Path):
    pages = find_all_pages(wiki_dir)
    if not pages:
        return []
    all_links = set()
    for page in pages:
        content = page.read_text(errors="ignore")
        all_links.update(extract_links(content))
    # index.md 里的链接也算引用
    index_file = wiki_dir / "index.md"
    if index_file.exists():
        all_links.update(extract_links(index_file.read_text()))

    orphans = []
    for page in pages:
        stem = page.stem
        if stem not in all_links and stem.replace("-", " ") not in all_links:
            rel = page.relative_to(wiki_dir)
            orphans.append(f"  - {rel}")
    return orphans


def check_missing_concept_pages(wiki_dir: Path):
    pages = find_all_pages(wiki_dir)
    actual_pages = {p.stem for p in pages}

    link_refs = defaultdict(list)
    for page in pages:
        content = page.read_text(errors="ignore")
        for link in extract_links(content):
            slug = link.replace(" ", "-").lower()
            if link not in actual_pages and slug not in actual_pages:
                link_refs[link].append(page.stem)

    missing = []
    for link, refs in sorted(link_refs.items(), key=lambda x: -len(x[1])):
        missing.append(f"  - [[{link}]] — 被 {len(refs)} 个页面引用（{', '.join(refs[:3])}{'...' if len(refs) > 3 else ''}）")
    return missing


def check_stale_pages(wiki_dir: Path, days: int = 90):
    pages = find_all_pages(wiki_dir)
    stale = []
    cutoff = datetime.now() - timedelta(days=days)
    for page in pages:
        mtime = datetime.fromtimestamp(page.stat().st_mtime)
        if mtime < cutoff:
            rel = page.relative_to(wiki_dir)
            delta = (datetime.now() - mtime).days
            stale.append(f"  - {rel}（{delta} 天未更新）")
    return stale


def check_missing_confidence(wiki_dir: Path):
    """
    检查每个页面 frontmatter 里是否有 `置信度:` 字段。
    旧页面可以没有，但新写/更新的应该补。入库未标会让 Query 时无法判断来源可信度。
    跟 lint 过的其他检查保持一致，返回 markdown list 条目。
    """
    pages = find_all_pages(wiki_dir)
    missing = []
    tag_pat = re.compile(r"^\*\*置信度：\*\*", re.MULTILINE)
    for page in pages:
        # sources/ 和 raw/ 子目录的摘要页可先跳过（内容是摘抄，置信度一律看作 EXTRACTED）
        if any(seg in page.parts for seg in SKIP_MENTION_CHECK_DIRS):
            continue
        try:
            head = page.read_text(errors="replace")[:1024]
        except OSError:
            continue
        if not tag_pat.search(head):
            rel = page.relative_to(wiki_dir)
            missing.append(f"  - {rel}")
    return missing


def check_missing_cross_refs(wiki_dir: Path):
    """
    检查可能缺失的交叉引用：
    页面 A 的正文里提到了页面 B 的完整标题（纯文本，非 [[]]），
    但 A 的「相关页面」章节没有 [[B]] 链接 → 可能漏了交叉引用
    """
    pages = find_all_pages(wiki_dir)
    # 建 title → path 映射
    title_to_page = {}
    page_to_title = {}
    for p in pages:
        # 跳过 sources/raw 下的页面（它们本来就是摘要，不适合做概念枢纽）
        rel = p.relative_to(wiki_dir)
        if any(part in SKIP_MENTION_CHECK_DIRS for part in rel.parts):
            continue
        title = extract_title(p)
        # 标题太短（< 4 字符）会误报，跳过
        if len(title) < 4:
            continue
        title_to_page[title] = p
        page_to_title[p] = title

    suggestions = []
    for page, title in page_to_title.items():
        content = page.read_text(errors="ignore")
        # 把本页面已有的 [[链接]] 全去掉，剩下的才是"纯文本提到"
        stripped = re.sub(r"\[\[[^\]]+\]\]", "", content)
        existing_links = set(extract_links(content))
        existing_links_normalized = {l.lower() for l in existing_links}

        for other_title, other_page in title_to_page.items():
            if other_page == page:
                continue
            # 本页正文提到了 other_title（纯文本）
            if other_title in stripped:
                # 但 [[链接]] 里没包含 other_page.stem 或 other_title
                if (other_page.stem not in existing_links_normalized
                        and other_title.lower() not in existing_links_normalized):
                    rel = page.relative_to(wiki_dir)
                    suggestions.append(f"  - {rel} 提到了「{other_title}」但没建立 [[{other_page.stem}]] 链接")

    # 去重（一个页面可能提到多次同一个别人，只报一次）
    return sorted(set(suggestions))[:30]  # 限制 30 条防爆


def write_report_file(wiki_dir: Path, report_md: str, now_date: str) -> Path:
    """报告写到 wiki/.lint-history/YYYY-MM-DD.md（持久化）"""
    history_dir = wiki_dir / ".lint-history"
    history_dir.mkdir(exist_ok=True)
    report_file = history_dir / f"{now_date}.md"
    report_file.write_text(report_md)
    return report_file


def build_summary(wiki_dir: Path, now_date: str, stats: dict) -> str:
    """构造一行报警摘要，用于 --summary / 外部推送 pipe。"""
    total_issues = (
        stats.get("index_issues", 0)
        + stats.get("orphans", 0)
        + stats.get("missing_concepts", 0)
        + stats.get("missing_cross_refs", 0)
        + stats.get("stale", 0)
        + stats.get("missing_confidence", 0)
    )
    report_path = f"{wiki_dir}/.lint-history/{now_date}.md"
    if total_issues == 0:
        return f"📚 Wiki Lint: ✅ 0 issues | report: {report_path}"
    return (
        f"📚 Wiki Lint: {total_issues} issues "
        f"(index:{stats.get('index_issues', 0)} "
        f"orphans:{stats.get('orphans', 0)} "
        f"missing-concepts:{stats.get('missing_concepts', 0)} "
        f"missing-xref:{stats.get('missing_cross_refs', 0)} "
        f"stale:{stats.get('stale', 0)} "
        f"no-confidence:{stats.get('missing_confidence', 0)}) "
        f"| report: {report_path}"
    )


def run_lint(wiki_dir: Path, quick: bool = False, write_log: bool = True, summary_only: bool = False):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    now_date = datetime.now().strftime("%Y-%m-%d")
    report_lines = [f"# Wiki Lint 报告 — {wiki_dir} — {now}\n"]

    print(f"🔍 Lint: {wiki_dir} ({'轻量模式' if quick else '完整模式'})")

    # 1. index.md 一致性
    index_issues = check_index_consistency(wiki_dir)
    report_lines.append("## 📋 index.md 一致性")
    if index_issues:
        report_lines.extend(index_issues)
    else:
        report_lines.append("  ✅ 无问题")
    report_lines.append("")

    # 统计数据
    stats = {"index_issues": len(index_issues)}

    if not quick:
        # 2. 孤儿页面
        orphans = check_orphan_pages(wiki_dir)
        stats["orphans"] = len(orphans)
        report_lines.append(f"## ⚠️ 孤儿页面（{len(orphans)} 个）")
        report_lines.extend(orphans if orphans else ["  ✅ 无孤儿页面"])
        report_lines.append("")

        # 3. 缺失概念页
        missing = check_missing_concept_pages(wiki_dir)
        stats["missing_concepts"] = len(missing)
        report_lines.append(f"## 🔗 缺失概念页（{len(missing)} 个）")
        report_lines.extend(missing if missing else ["  ✅ 无缺失概念页"])
        report_lines.append("")

        # 4. 缺失交叉引用
        cross_refs = check_missing_cross_refs(wiki_dir)
        stats["missing_cross_refs"] = len(cross_refs)
        report_lines.append(f"## 🔀 可能缺失的交叉引用（{len(cross_refs)} 个）")
        report_lines.append("  _规则：页面 A 正文提到页面 B 的标题但没有 [[B]] 链接_")
        report_lines.extend(cross_refs if cross_refs else ["  ✅ 无"])
        report_lines.append("")

        # 5. 过时内容
        stale = check_stale_pages(wiki_dir)
        stats["stale"] = len(stale)
        report_lines.append(f"## 📅 过时页面（{len(stale)} 个，超过 90 天）")
        report_lines.extend(stale if stale else ["  ✅ 无过时页面"])
        report_lines.append("")

        # 5.5 缺置信度标签
        no_conf = check_missing_confidence(wiki_dir)
        stats["missing_confidence"] = len(no_conf)
        report_lines.append(f"## 🏷️ 缺置信度标签（{len(no_conf)} 个）")
        report_lines.append("  _规则：页面 frontmatter 应有 `**置信度：**` 字段（EXTRACTED/INFERRED/AMBIGUOUS/UNVERIFIED）_")
        report_lines.extend(no_conf if no_conf else ["  ✅ 全部页面都有置信度标签"])
        report_lines.append("")

        # 6. 矛盾内容 / 空白点 → 需要 LLM（Layer 2）
        report_lines.append("## 💡 需要 LLM 判断（Layer 2）")
        report_lines.append("  - 矛盾内容（同一事实在多页描述不一致）")
        report_lines.append("  - 过时说法（新来源推翻旧说法）")
        report_lines.append("  - 数据空白（可以上网搜的主题）")
        report_lines.append("  → 在对话里说「整理 wiki」触发 LLM 逐项处理")
        report_lines.append("")

    report = "\n".join(report_lines)
    if not summary_only:
        print(report)

    # 写报告文件
    report_file = write_report_file(wiki_dir, report, now_date)
    if not summary_only:
        print(f"\n📄 报告已保存：{report_file.relative_to(wiki_dir)}")

    # 追加 log.md
    if write_log:
        log_file = wiki_dir / "log.md"
        mode = "快速" if quick else "完整"
        with open(log_file, "a") as f:
            f.write(f"\n## [{now_date}] lint | {mode} lint\n\n")
            f.write(f"- 模式：{mode}\n")
            f.write(f"- 报告：`.lint-history/{now_date}.md`\n")
            if not quick:
                f.write(f"- 孤儿页面：{stats['orphans']} 个\n")
                f.write(f"- 缺失概念页：{stats['missing_concepts']} 个\n")
                f.write(f"- 缺失交叉引用：{stats['missing_cross_refs']} 个\n")
                f.write(f"- 过时页面：{stats['stale']} 个\n")
                f.write(f"- 缺置信度标签：{stats['missing_confidence']} 个\n")
            f.write("\n")

    # --summary: 只打一行到 stdout，供外部 pipe
    if summary_only:
        print(build_summary(wiki_dir, now_date, stats))

    return report, stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="轻量模式（只查 index.md）")
    parser.add_argument("--wiki-root", default=None, help="wiki 根目录（默认 $WIKI_ROOT 或 ~/.openclaw/workspace/wiki）")
    parser.add_argument("--summary", action="store_true", help="只打印一行摘要到 stdout（供 cron/Scheduler pipe 到邮件/聊天/webhook）")
    parser.add_argument("--no-log", action="store_true", help="不追加 log.md（预览模式）")
    args = parser.parse_args()

    wiki_dir = Path(args.wiki_root).expanduser() if args.wiki_root else default_wiki_root()
    if not wiki_dir.exists():
        print(f"❌ wiki 目录不存在：{wiki_dir}", file=sys.stderr)
        print(f"   提示：设置 $WIKI_ROOT 或用 --wiki-root 指定", file=sys.stderr)
        sys.exit(2)

    run_lint(
        wiki_dir=wiki_dir,
        quick=args.quick,
        write_log=not args.no_log,
        summary_only=args.summary,
    )
