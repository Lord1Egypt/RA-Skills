#!/usr/bin/env python3
"""
memory_index.py - 扫描记忆目录，自动生成/更新 INDEX.md（支持多用户 + 公共记忆）

用法:
  python scripts/memory_index.py [--base-dir PATH] [--uid UID] [--scope private|shared|all]
"""

import os
import re
import sys
import argparse
from datetime import datetime
from collections import Counter


def count_entries(filepath):
    if not os.path.exists(filepath):
        return 0
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return len(re.findall(r"^## ", content, re.MULTILINE))


def extract_first_summary(filepath):
    if not os.path.exists(filepath):
        return "—"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"\*\*(?:摘要|内容|描述)\*\*[:：]\s*(.+)", content)
    if match:
        return match.group(1)[:60].strip()
    headers = re.findall(r"^## (.+)$", content, re.MULTILINE)
    if headers:
        return "、".join(headers[:3])[:60]
    return "—"


def make_semantic_key(title):
    """
    为条目生成 semantic_key（20字以内的语义摘要）。
    用于向量搜索时作为高权重文本 + 人类快速浏览。
    """
    # 去掉时间前缀 [HH:MM]
    clean = re.sub(r"^\[\d{2}:\d{2}\]\s*", "", title.strip()).strip()
    if len(clean) <= 20:
        return clean
    return clean[:17] + "..."


def parse_sections_for_index(filepath):
    """
    解析文件，返回所有条目的 semantic_key 列表。
    [(section_idx, title, semantic_key, summary), ...]
    """
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    results = []
    parts = re.split(r"(?=^## )", content, flags=re.MULTILINE)
    for idx, part in enumerate(parts):
        part = part.strip()
        if not part or len(part) < 10:
            continue
        lines = part.split("\nfrom typing import List, Dict, Optional, Union, Any, Tuple\n")
        raw_title = lines[0].strip().lstrip("#").strip()
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
        if not body:
            continue
        semantic_key = make_semantic_key(raw_title)
        summary = extract_first_summary_from_body(body)
        results.append((idx, raw_title, semantic_key, summary))
    return results


def extract_first_summary_from_body(body):
    """从 body 中提取摘要"""
    match = re.search(r"\*\*(?:摘要|内容|描述)\*\*[:：]\s*(.+)", body)
    if match:
        return match.group(1)[:60].strip()
    # 取非元数据行
    key_lines = []
    for line in body.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("**"):
            continue
        key_lines.append(stripped)
        if len(key_lines) >= 2:
            break
    return " ".join(key_lines)[:60] if key_lines else body[:40]


def extract_tags(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return re.findall(r"#(\w[\w-]*)", content)


def extract_todos(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    todos = re.findall(r"^- \[ \] (.+)$", content, re.MULTILINE)
    return [(os.path.basename(filepath).replace(".md", ""), t) for t in todos]


def _get_first_semantic_key(filepath):
    """提取文件第一条记录的 semantic key"""
    if not filepath or not os.path.exists(filepath):
        return "—"
    try:
        sections = parse_sections_for_index(filepath)
        if sections:
            return sections[0][2]  # semantic_key
    except Exception:
        pass
    return "—"

def scan_dir(dir_path, pattern, max_files=30):
    """扫描目录，返回文件摘要列表"""
    results = []
    if not os.path.exists(dir_path):
        return results
    for fname in sorted(os.listdir(dir_path), reverse=True)[:max_files]:
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(dir_path, fname)
        key = pattern.format(fname=fname.replace(".md", ""))
        results.append({
            "key": key,
            "_filepath": fpath,  # 用于提取 semantic key
            "entries": count_entries(fpath),
            "summary": extract_first_summary(fpath),
            "tags": extract_tags(fpath),
            "todos": extract_todos(fpath),
        })
    return results


def build_user_index(base_dir, uid):
    """构建单个用户的 INDEX.md"""
    user_dir = os.path.join(base_dir, "users", uid)
    daily_dir = os.path.join(user_dir, "daily")
    weekly_dir = os.path.join(user_dir, "weekly")
    permanent_dir = os.path.join(user_dir, "permanent")
    habits_path = os.path.join(user_dir, "HABITS.md")

    all_tags = Counter()
    all_todos = []
    now = datetime.now()

    # L1
    l1_data = scan_dir(daily_dir, "{fname}", max_files=30)
    for item in l1_data:
        all_tags.update(item["tags"])
        all_todos.extend(item["todos"])

    # L2
    l2_data = scan_dir(weekly_dir, "{fname}", max_files=12)
    for item in l2_data:
        all_tags.update(item["tags"])

    # L3
    l3_categories = ["decisions", "tech-stack", "projects", "people", "knowledge", "lessons", "preferences"]
    l3_rows = []
    for cat in l3_categories:
        fpath = os.path.join(permanent_dir, f"{cat}.md")
        if os.path.exists(fpath):
            mtime = datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%Y-%m-%d")
            entries = count_entries(fpath)
            summary = extract_first_summary(fpath)
            tags = extract_tags(fpath)
            all_tags.update(tags)
            l3_rows.append((cat, entries, summary[:50], mtime))

    # HABITS
    habits_count = count_entries(habits_path)

    total_l1 = len(l1_data)
    total_l2 = len(l2_data)
    total_l3 = sum(r[1] for r in l3_rows)

    content = f"""# Memory Index ({uid})
_最后更新: {now.strftime('%Y-%m-%d %H:%M')}_

## 快速摘要
| 层级 | 文件数 | 条目数 | 最近更新 |
|------|--------|--------|----------|
| L1 临时 | {total_l1} | {sum(e['entries'] for e in l1_data)} | {l1_data[0]['key'] if l1_data else '—'} |
| L2 长期 | {total_l2} | {sum(e['entries'] for e in l2_data)} | {l2_data[0]['key'] if l2_data else '—'} |
| L3 永久 | {len(l3_rows)} | {total_l3} | — |
| 习惯 | 1 | {habits_count} | — |

"""

    # 未完成任务
    if all_todos:
        content += "## 未完成任务追踪\n"
        for date_str, todo in all_todos[:20]:
            content += f"- [ ] {todo} _(来自 {date_str})_\n"
        content += "\n"
    else:
        content += "## 未完成任务追踪\n_暂无未完成任务_ ✅\n\n"

    # L1 - 增强版：每条记忆的 semantic key
    content += "## L1 临时记忆索引\n"
    if l1_data:
        content += "| 日期 | 条目 | Semantic Key | 标签 | 条目数 |\n"
        content += "|------|------|--------------|------|--------|\n"
        for item in l1_data[:15]:
            tag_str = " ".join(f"#{t}" for t in item["tags"][:4])
            # 从文件内容提取第一条 semantic key
            sk = _get_first_semantic_key(item.get("_filepath"))
            content += f"| {item['key']} | {item['summary'][:30]} | {sk} | {tag_str} | {item['entries']} |\n"
    else:
        content += "_暂无记录_\n"
    content += "\n"

    # L2
    content += "## L2 长期记忆索引\n"
    if l2_data:
        content += "| 周次 | 主要内容 | Semantic Key | 条目数 |\n"
        content += "|------|----------|--------------|--------|\n"
        for item in l2_data:
            sk = _get_first_semantic_key(item.get("_filepath"))
            content += f"| {item['key']} | {item['summary'][:35]} | {sk} | {item['entries']} |\n"
    else:
        content += "_暂无记录_\n"
    content += "\n"

    # L3 - 增强版
    content += "## L3 永久记忆索引\n"
    content += "| 分类 | 条目 | Semantic Key | 摘要 | 更新日期 |\n"
    content += "|------|------|--------------|------|----------|\n"
    if l3_rows:
        for cat, entries, summary, mtime in l3_rows:
            sk = _get_first_semantic_key(
                os.path.join(permanent_dir, f"{cat}.md")
            )
            content += f"| {cat} | {entries} | {sk} | {summary} | {mtime} |\n"
    else:
        content += "_暂无记录_\n"
    content += "\n"

    # 热门标签
    if all_tags:
        tags_str = " ".join(f"#{t}({c})" for t, c in all_tags.most_common(20))
        content += f"## 热门标签\n{tags_str}\n\n"

    content += """## 搜索提示
- 按日期: 查看 `users/{uid}/daily/YYYY-MM-DD.md`
- 按主题: 使用标签 `#tag`
- 按决策: 查看 `users/{uid}/permanent/decisions.md`
- 按技术: 查看 `users/{uid}/permanent/tech-stack.md`
- 按习惯: 查看 `users/{uid}/HABITS.md`
""".replace("{uid}", uid)

    return content


def build_shared_index(base_dir):
    """构建公共 INDEX.md"""
    shared_dir = os.path.join(base_dir, "shared")
    daily_dir = os.path.join(shared_dir, "daily")
    weekly_dir = os.path.join(shared_dir, "weekly")
    permanent_dir = os.path.join(shared_dir, "permanent")

    all_tags = Counter()
    now = datetime.now()

    # shared daily
    sd_data = scan_dir(daily_dir, "{fname}", max_files=14)
    for item in sd_data:
        all_tags.update(item["tags"])

    # shared weekly
    sw_data = scan_dir(weekly_dir, "{fname}", max_files=12)
    for item in sw_data:
        all_tags.update(item["tags"])

    # shared L3
    shared_l3_cats = ["decisions", "tech-stack", "projects", "knowledge"]
    l3_rows = []
    for cat in shared_l3_cats:
        fpath = os.path.join(permanent_dir, f"{cat}.md")
        if os.path.exists(fpath):
            mtime = datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%Y-%m-%d")
            entries = count_entries(fpath)
            summary = extract_first_summary(fpath)
            tags = extract_tags(fpath)
            all_tags.update(tags)
            l3_rows.append((cat, entries, summary[:50], mtime))

    content = f"""# Shared Memory Index
_最后更新: {now.strftime('%Y-%m-%d %H:%M')}_

## 快速摘要
| 层级 | 文件数 | 条目数 | 最近更新 |
|------|--------|--------|----------|
| 公共临时 | {len(sd_data)} | {sum(e['entries'] for e in sd_data)} | {sd_data[0]['key'] if sd_data else '—'} |
| 公共周报 | {len(sw_data)} | {sum(e['entries'] for e in sw_data)} | {sw_data[0]['key'] if sw_data else '—'} |
| 公共永久 | {len(l3_rows)} | {sum(r[1] for r in l3_rows)} | — |

"""

    # 公共 L1 - 增强版
    content += "## 公共临时记忆\n"
    if sd_data:
        content += "| 日期 | 条目 | Semantic Key | 标签 |\n"
        content += "|------|------|--------------|------|\n"
        for item in sd_data[:10]:
            tag_str = " ".join(f"#{t}" for t in item["tags"][:4])
            sk = _get_first_semantic_key(item.get("_filepath"))
            content += f"| {item['key']} | {item['summary'][:35]} | {sk} | {tag_str} |\n"
    else:
        content += "_暂无记录_\n"
    content += "\n"

    # 公共 L2
    content += "## 公共周报\n"
    if sw_data:
        content += "| 周次 | 主要内容 | 条目数 |\n"
        content += "|------|----------|--------|\n"
        for item in sw_data:
            content += f"| {item['key']} | {item['summary'][:50]} | {item['entries']} |\n"
    else:
        content += "_暂无记录_\n"
    content += "\n"

    # 公共 L3 - 增强版
    content += "## 公共永久记忆索引\n"
    content += "| 分类 | 条目 | Semantic Key | 摘要 | 更新日期 |\n"
    content += "|------|------|--------------|------|----------|\n"
    if l3_rows:
        for cat, entries, summary, mtime in l3_rows:
            sk = _get_first_semantic_key(
                os.path.join(permanent_dir, f"{cat}.md")
            )
            content += f"| {cat} | {entries} | {sk} | {summary} | {mtime} |\n"
    else:
        content += "_暂无记录_\n"
    content += "\n"

    if all_tags:
        tags_str = " ".join(f"#{t}({c})" for t, c in all_tags.most_common(15))
        content += f"## 公共热门标签\n{tags_str}\n\n"

    content += """## 搜索提示
- 团队当日进展: `shared/daily/YYYY-MM-DD.md`
- 团队周报: `shared/weekly/YYYY-WNN.md`
- 公共决策: `shared/permanent/decisions.md`
- 项目信息: `shared/permanent/projects.md`
"""

    return content


def main():
    parser = argparse.ArgumentParser(description="生成/更新记忆索引")
    parser.add_argument("--base-dir", default=".", help="记忆仓库根目录")
    parser.add_argument("--uid", help="用户ID（默认: MEMORY_USER_ID 或 'default'）")
    parser.add_argument("--scope", default="all", choices=["private", "shared", "all"],
                        help="索引范围")
    args = parser.parse_args()

    # 安全检查：确保 base_dir 在预期范围内
    base_dir = os.path.abspath(args.base_dir)
    # 禁止访问系统关键路径
    forbidden = {"/", "C:\\", "/home", "/Users", "/System"}
    if any(base_dir.startswith(p) for p in forbidden):
        print(f"❌ 禁止访问系统路径: {base_dir}")
        sys.exit(1)
    uid = args.uid or os.environ.get("MEMORY_USER_ID", "default")

    print(f"\n🔍 记忆索引构建")
    print(f"📁 仓库: {base_dir}")
    print(f"👤 用户: {uid}\n")

    # 私人索引
    if args.scope in ("private", "all"):
        user_dir = os.path.join(base_dir, "users", uid)
        if os.path.exists(user_dir):
            content = build_user_index(base_dir, uid)
            index_path = os.path.join(user_dir, "INDEX.md")
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ 个人索引已更新: users/{uid}/INDEX.md")
        else:
            print(f"⚠️  用户目录不存在: users/{uid}/")

    # 公共索引
    if args.scope in ("shared", "all"):
        shared_dir = os.path.join(base_dir, "shared")
        if os.path.exists(shared_dir):
            content = build_shared_index(base_dir)
            index_path = os.path.join(shared_dir, "INDEX.md")
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ 公共索引已更新: shared/INDEX.md")
        else:
            print(f"⚠️  公共目录不存在: shared/")


if __name__ == "__main__":
    main()
