#!/usr/bin/env python3
"""
OpenClaw 每日资讯推送主控脚本
串联所有采集器，汇总结果，输出 Markdown 报告。
"""

import argparse
import json
import sys
import os
import time
from datetime import datetime, timedelta, timezone

# 确保当前目录在 sys.path 中，以便导入 collectors
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Windows UTF-8 输出支持
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from collectors import bilibili, github_oc, clawhub_oc, xiaohongshu


# ---- 采集器配置 ----
COLLECTORS = [
    {
        "name": "bilibili",
        "display_name": "B站",
        "emoji": "📺",
        "module": bilibili,
    },
    {
        "name": "github",
        "display_name": "GitHub",
        "emoji": "💻",
        "module": github_oc,
    },
    {
        "name": "clawhub",
        "display_name": "ClawHub",
        "emoji": "🔧",
        "module": clawhub_oc,
    },
    {
        "name": "xiaohongshu",
        "display_name": "小红书",
        "emoji": "📱",
        "module": xiaohongshu,
    },
]


def run_collectors(keyword: str, hours: int) -> list:
    """
    依次运行所有采集器，收集结果。
    某个采集器失败不影响其他采集器。

    Returns:
        list: 每个采集器的结果字典列表
    """
    results = []

    for cfg in COLLECTORS:
        name = cfg["name"]
        module = cfg["module"]
        print(f"  ⏳ 正在采集 {cfg['display_name']}...", end=" ", flush=True)

        try:
            start = time.time()
            result = module.collect(keyword=keyword, hours=hours)
            elapsed = time.time() - start

            # 确保 source 字段正确
            if "source" not in result:
                result["source"] = name

            count = result.get("total", len(result.get("items", [])))
            status = "✅"
            if result.get("error"):
                status = "⚠️"
            print(f"{status} {count} 条 ({elapsed:.1f}s)")

            results.append(result)

        except Exception as e:
            print(f"❌ 失败: {e}")
            results.append({
                "source": name,
                "items": [],
                "total": 0,
                "error": str(e),
                "query_time": datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M"),
            })

    return results


def generate_markdown(results: list, keyword: str) -> str:
    """
    将所有采集器的结果合并，生成 Markdown 格式的每日资讯报告。

    Args:
        results: 各采集器返回的结果列表
        keyword: 搜索关键词

    Returns:
        str: Markdown 格式的报告
    """
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    lines = []
    lines.append(f"# 🦞 OpenClaw 每日资讯 ({date_str})")
    lines.append("")
    lines.append(f"> 关键词：`{keyword}` | 生成时间：{time_str}")
    lines.append("")

    total_count = 0

    # 为每个采集器创建对应的章节
    source_config = {
        "bilibili": {"emoji": "📺", "name": "B站"},
        "github": {"emoji": "💻", "name": "GitHub"},
        "clawhub": {"emoji": "🔧", "name": "ClawHub"},
        "xiaohongshu": {"emoji": "📱", "name": "小红书"},
    }

    for result in results:
        source = result.get("source", "unknown")
        items = result.get("items", [])
        count = result.get("total", len(items))
        error = result.get("error")

        # 获取显示配置
        cfg = source_config.get(source, {"emoji": "📄", "name": source})
        emoji = cfg["emoji"]
        display_name = cfg["name"]

        lines.append(f"## {emoji} {display_name} ({count}条)")

        if error and not items:
            lines.append(f"> ⚠️ 采集异常：{error}")
            lines.append("")
            continue

        if error:
            lines.append(f"> ⚠️ 注意：{error}")
            lines.append("")

        if not items:
            lines.append("> 暂无新内容")
            lines.append("")
            continue

        for i, item in enumerate(items, 1):
            title = item.get("title", "无标题")
            url = item.get("url", "#")
            author = item.get("author", "")
            description = item.get("description", "")

            # 根据来源构建不同格式
            if source == "bilibili":
                views = item.get("views", 0)
                views_str = _format_views(views)
                pub_time = item.get("publish_time", "")
                meta_parts = []
                if author:
                    meta_parts.append(f"UP主: {author}")
                if views_str:
                    meta_parts.append(f"{views_str}播放")
                if pub_time:
                    meta_parts.append(pub_time)
                meta = " - ".join(meta_parts) if meta_parts else ""

                lines.append(f"{i}. **[{title}]({url})** - {meta}")

            elif source == "github":
                item_type = item.get("type", "")
                repo = item.get("repo", "")
                type_label = {"pr": "PR", "issue": "issue", "repo": "仓库"}.get(item_type, item_type)
                meta_parts = []
                if author:
                    meta_parts.append(f"@{author}")
                if type_label:
                    meta_parts.append(type_label)
                if repo:
                    meta_parts.append(repo)
                meta = " - ".join(meta_parts)

                lines.append(f"{i}. **[{title}]({url})** - {meta}")

            elif source == "clawhub":
                version = item.get("version", "")
                meta_parts = []
                if author:
                    meta_parts.append(author)
                if version:
                    meta_parts.append(version)
                meta = " - ".join(meta_parts)

                lines.append(f"{i}. **[{title}]({url})** - {meta}")

            elif source == "xiaohongshu":
                pub_time = item.get("publish_time", "")
                meta_parts = []
                if author:
                    meta_parts.append(author)
                if pub_time:
                    meta_parts.append(pub_time)
                meta = " - ".join(meta_parts)

                lines.append(f"{i}. **[{title}]({url})** - {meta}")

            else:
                lines.append(f"{i}. **[{title}]({url})**")

            # 添加描述
            if description:
                # 截断过长的描述
                desc = description[:150]
                if len(description) > 150:
                    desc += "..."
                lines.append(f"   > {desc}")

        total_count += count
        lines.append("")

    # 汇总
    lines.append("---")
    lines.append(f"共 {total_count} 条新增内容 | 生成时间：{now.strftime('%Y-%m-%d %H:%M')}")

    return "\n".join(lines)


def _format_views(views) -> str:
    """格式化播放量数字"""
    if not views:
        return ""
    try:
        views = int(views)
    except (ValueError, TypeError):
        return str(views)

    if views >= 10000:
        return f"{views / 10000:.1f}万"
    elif views >= 1000:
        return f"{views / 1000:.1f}千"
    return str(views)


def generate_json(results: list, keyword: str) -> dict:
    """生成 JSON 格式的报告"""
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)

    total = sum(r.get("total", len(r.get("items", []))) for r in results)

    return {
        "date": now.strftime("%Y-%m-%d"),
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "keyword": keyword,
        "total": total,
        "sources": results,
    }


def save_report(markdown: str, output_path: str):
    """保存 Markdown 报告到文件"""
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"\n📄 Markdown 报告已保存: {output_path}")


def save_json_report(data: dict, output_path: str):
    """保存 JSON 报告到文件"""
    json_path = output_path.rsplit(".", 1)[0] + ".json"

    output_dir = os.path.dirname(json_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"📊 JSON 报告已保存: {json_path}")


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw 每日资讯推送 - 汇总多平台动态，生成 Markdown 报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--keyword", "-k",
        default="OpenClaw",
        help="搜索关键词 (默认: OpenClaw)",
    )
    parser.add_argument(
        "--hours", "-H",
        type=int,
        default=24,
        help="回溯小时数 (默认: 24)",
    )
    parser.add_argument(
        "--output", "-o",
        default="daily_report.md",
        help="输出文件路径 (默认: daily_report.md)",
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="同时输出 JSON 格式",
    )

    args = parser.parse_args()

    print(f"🦞 OpenClaw 每日资讯采集器")
    print(f"   关键词: {args.keyword}")
    print(f"   时间范围: 最近 {args.hours} 小时")
    print(f"   输出: {args.output}")
    print()

    # 运行所有采集器
    results = run_collectors(args.keyword, args.hours)

    # 生成 Markdown 报告
    print()
    markdown = generate_markdown(results, args.keyword)

    # 保存文件
    save_report(markdown, args.output)

    # 可选：保存 JSON
    if args.json:
        json_data = generate_json(results, args.keyword)
        save_json_report(json_data, args.output)

    # 打印摘要
    total = sum(r.get("total", len(r.get("items", []))) for r in results)
    errors = [r for r in results if r.get("error") and not r.get("items")]
    print(f"\n✅ 完成！共采集 {total} 条内容")
    if errors:
        print(f"⚠️  {len(errors)} 个采集器出现异常")

    # 同时输出到 stdout（方便管道使用）
    print("\n" + "=" * 60)
    print(markdown)

    return 0


if __name__ == "__main__":
    sys.exit(main())
