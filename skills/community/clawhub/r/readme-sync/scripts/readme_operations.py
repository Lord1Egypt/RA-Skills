#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
README Sync Operations
按需读取和更新 README.md 的工具脚本

用法:

用法:
  python readme_operations.py read <section>       # 读取指定章节
  python readme_operations.py read-all             # 读取整个 README
  python readme_operations.py pending              # 查看待更新条目
  python readme_operations.py add <type> <content> # 添加待更新条目
  python readme_operations.py clear                 # 清空待更新
  python readme_operations.py sync                 # 执行同步（写入 README）
  python readme_operations.py init                 # 初始化 README
  python readme_operations.py diff                 # 查看差异
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

PENDING_FILE = ".readme_pending.json"
README_FILE = "README.md"


def get_project_root():
    """获取项目根目录（向上查找 README.md）"""
    cwd = Path.cwd()
    for path in [cwd] + list(cwd.parents):
        if (path / README_FILE).exists():
            return path
    return cwd


def load_pending():
    """加载待更新条目"""
    pending_file = get_project_root() / PENDING_FILE
    if pending_file.exists():
        with open(pending_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_pending(pending):
    """保存待更新条目"""
    pending_file = get_project_root() / PENDING_FILE
    with open(pending_file, "w", encoding="utf-8") as f:
        json.dump(pending, f, ensure_ascii=False, indent=2)


def extract_section(content, section_name):
    """提取指定章节内容"""
    # 匹配 ## 标题 或 ### 标题（#后面有空格，更精确）
    # 使用 (?:^#{1,3} ) 后面跟非#字符，直到找到section_name
    hash_marks = r"#{1,3}"
    pattern = rf"(?:^({hash_marks}) [^\n]*{re.escape(section_name)}[^\n]*$\n)(.*?)(?=^#{hash_marks} |\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(2).strip()
    return None


def read_section(section_name):
    """读取指定章节"""
    readme_path = get_project_root() / README_FILE
    if not readme_path.exists():
        print(f"README.md not found at {readme_path}")
        print("\n📝 请选择操作：")
        print("  1. 运行 'init' 初始化空 README")
        print("  2. 运行 'scan' 扫描代码生成 README")
        print("  3. 运行 'auto-init' 自动扫描并初始化 README")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    if section_name == "all":
        print(content)
        return

    section_content = extract_section(content, section_name)
    if section_content:
        print(f"## {section_name}\n{section_content}")
    else:
        print(f"❌ Section '{section_name}' not found")
        sys.exit(1)


def show_pending():
    """显示待更新条目"""
    pending = load_pending()
    if not pending:
        print("📝 No pending updates")
        return

    print(f"📝 Pending updates ({len(pending)} items):\n")
    for i, item in enumerate(pending, 1):
        print(f"  {i}. [{item['type']}] {item['content']}")
        if item.get("related"):
            print(f"     📁 {item['related']}")
    print()


def add_pending(item_type, content, related=None):
    """添加待更新条目"""
    pending = load_pending()

    if len(pending) >= 5:
        print("⚠️  Maximum 5 pending items. Run 'sync' or 'clear' first.")

    item = {
        "type": item_type,
        "content": content,
        "related": related,
        "timestamp": datetime.now().isoformat()
    }
    pending.append(item)
    save_pending(pending)
    print(f"✅ Added: [{item_type}] {content}")
    if related:
        print(f"   📁 {related}")


def clear_pending():
    """清空待更新条目"""
    save_pending([])
    print("✅ Pending updates cleared")


def sync_to_readme():
    """将待更新条目同步到 README"""
    pending = load_pending()
    if not pending:
        print("❌ No pending updates to sync")
        return

    readme_path = get_project_root() / README_FILE
    if not readme_path.exists():
        print(f"❌ README.md not found at {readme_path}")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 按类型分组
    changelog_entries = []
    progress_updates = []
    trap_warnings = []

    for item in pending:
        entry = f"| {datetime.now().strftime('%Y-%m-%d')} | {item['content']} | {item.get('related', '')} |"
        if item["type"] == "changelog":
            changelog_entries.append(entry)
        elif item["type"] == "progress":
            progress_updates.append(f"- [x] {item['content']}")
        elif item["type"] == "trap":
            trap_warnings.append(f"- ⚠️  {item['content']}")

    # 更新近期修改记录
    if changelog_entries:
        # 找到 ## 近期修改记录 章节
        pattern = r"(## 近期修改记录\s*<!--.*?-->?\s*\n)([\s\S]*?)(?=\n## |\Z)"
        match = re.search(pattern, content)
        if match:
            existing = match.group(2).strip()
            # 解析现有表格（跳过表头和分隔行）
            header = "| 日期 | 修改内容 | 相关文件/模块 |\n|------|---------|--------------|"
            existing_lines = []
            if existing:
                for line in existing.split("\n"):
                    # 只保留数据行（以 | 开头但不是 |---）
                    if line.startswith("|") and "|" in line and "---" not in line and "日期" not in line:
                        existing_lines.append(line.strip())
            # 合并新条目（在现有条目之前，最多10条）
            all_entries = changelog_entries + existing_lines[:9]
            new_section = "## 近期修改记录\n" + header + "\n" + "\n".join(all_entries) + "\n"
            content = content[:match.start()] + new_section + content[match.end():]

    # 更新进度
    if progress_updates:
        # 找到 ## 当前进度 章节，追加到列表最后
        for update in progress_updates:
            if update not in content:
                pattern = r"(## 当前进度\s*\n)([\s\S]*?)(?=\n## |\Z)"
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    current_content = match.group(2).strip()
                    # 如果最后一行不是空行，先加换行
                    if current_content and not current_content.endswith("\n\n"):
                        if not current_content.endswith("\n"):
                            current_content += "\n"
                    # 追加新条目
                    new_content = current_content + update + "\n"
                    content = content[:match.start(2)] + new_content + content[match.end():]

    # 更新踩坑记录
    if trap_warnings:
        for warning in trap_warnings:
            if warning not in content:
                # 找到踩坑记录章节，追加到最后
                pattern = r"(## 踩坑记录\s*\n)([\s\S]*?)(?=\n## |\Z)"
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    current_content = match.group(2).strip()
                    new_content = current_content + "\n" + warning if current_content else warning
                    content = content[:match.start(2)] + new_content + content[match.end():]

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    # 清空 pending
    save_pending([])

    print("✅ README updated successfully")
    print(f"   📝 {len(changelog_entries)} changelog entries")
    print(f"   ✅ {len(progress_updates)} progress updates")
    print(f"   ⚠️  {len(trap_warnings)} trap warnings")


def init_readme():
    """初始化 README（空白模板）"""
    readme_path = get_project_root() / README_FILE
    if readme_path.exists():
        response = input(f"⚠️  {README_FILE} already exists. Overwrite? (y/N): ")
        if response.lower() != "y":
            print("Cancelled.")
            return

    template_path = Path(__file__).parent.parent / "references" / "readme_template.md"
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    else:
        template = get_default_template()

    # 填充默认项目名
    project_name = get_project_root().name
    template = template.replace("项目名称", project_name)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(template)

    print(f"✅ {README_FILE} initialized at {readme_path}")


def scan_project():
    """扫描项目代码结构，生成 README 内容（不写入文件）"""
    root = get_project_root()

    # 扫描目录结构
    dirs = []
    files = []
    for item in sorted(root.iterdir()):
        if item.name.startswith(".") or item.name in ["node_modules", "__pycache__", "venv", ".git"]:
            continue
        if item.is_dir():
            dirs.append(f"├── {item.name}/")
        else:
            ext = item.suffix.lower()
            files.append(f"├── {item.name}")

    # 扫描主要代码文件（用于推断语言/框架）
    code_files = []
    for ext in [".py", ".js", ".ts", ".java", ".go", ".rs", ".rb", ".php", ".c", ".cpp"]:
        code_files.extend(root.rglob(f"*{ext}"))
    code_files = [f for f in code_files if ".git" not in str(f) and "__pycache__" not in str(f)]
    code_files = code_files[:20]  # 只取前20个

    # 推断语言
    lang_counts = {}
    for f in code_files:
        ext = f.suffix
        lang_counts[ext] = lang_counts.get(ext, 0) + 1

    lang_map = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
        ".java": "Java", ".go": "Go", ".rs": "Rust", ".rb": "Ruby",
        ".php": "PHP", ".c": "C", ".cpp": "C++"
    }

    top_langs = sorted(lang_counts.items(), key=lambda x: -x[1])[:3]
    langs = ", ".join([f"{lang_map.get(ext, ext)}({cnt})" for ext, cnt in top_langs])

    print("# 项目结构扫描结果\n")
    print(f"## 目录\n" + "\n".join(dirs[:10]) if dirs else "## 目录\n（空目录）")
    print(f"\n## 主要文件\n" + "\n".join(files[:15]) if files else "\n## 主要文件\n（空项目）")
    print(f"\n## 推断技术栈\n{langs if langs else '未知（空项目）'}")
    print(f"\n总计：{len(dirs)} 个目录，{len(files)} 个文件，{len(code_files)} 个代码文件")


def auto_init():
    """扫描项目并生成 README"""
    root = get_project_root()
    readme_path = root / README_FILE

    if readme_path.exists():
        response = input(f"⚠️  {README_FILE} already exists. Overwrite? (y/N): ")
        if response.lower() != "y":
            print("Cancelled.")
            return

    # 扫描目录结构
    dirs = []
    files = []
    for item in sorted(root.iterdir()):
        if item.name.startswith(".") or item.name in ["node_modules", "__pycache__", "venv", ".git"]:
            continue
        if item.is_dir():
            dirs.append(f"| `{item.name}/` | 目录 | |")
        else:
            ext = item.suffix.lower()
            files.append(f"| `{item.name}` | 文件 | |")

    # 扫描主要代码文件
    code_files = []
    for ext in [".py", ".js", ".ts", ".java", ".go", ".rs", ".rb", ".php", ".c", ".cpp"]:
        code_files.extend(root.rglob(f"*{ext}"))
    code_files = [f for f in code_files if ".git" not in str(f) and "__pycache__" not in str(f)]
    code_files = code_files[:20]

    # 推断语言
    lang_counts = {}
    for f in code_files:
        ext = f.suffix
        lang_counts[ext] = lang_counts.get(ext, 0) + 1

    lang_map = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
        ".java": "Java", ".go": "Go", ".rs": "Rust", ".rb": "Ruby",
        ".php": "PHP", ".c": "C", ".cpp": "C++"
    }

    top_langs = sorted(lang_counts.items(), key=lambda x: -x[1])[:3]
    tech_stack = "\n".join([f"- {lang_map.get(ext, ext)}：{cnt} 个文件" for ext, cnt in top_langs]) if top_langs else "- 语言：未知"

    project_name = root.name

    content = f"""# {project_name}

## 一句话定位
[项目是干什么的，1-2 行]

## 技术栈
{tech_stack}

## 项目结构
| 名称 | 类型 | 说明 |
|------|------|------|
{chr(10).join(dirs[:15]) if dirs else "| （空目录） | | |"}
{chr(10).join(files[:15]) if files else "| （空项目根目录） | | |"}

## 当前进度
- [ ] 进行中：xxx
- [ ] 计划中：xxx

## API 概览（如适用）
| 接口 | 说明 |
|------|------|
| GET /xxx | xxx |

## 踩坑记录
<!-- 在此记录常见的坑 -->

## 近期修改记录
<!-- 最近 10 条修改，按时间倒序 -->
| 日期 | 修改内容 | 相关文件/模块 |
|------|---------|--------------|
"""

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ README.md auto-generated at {readme_path}")
    print(f"   📁 {len(dirs)} dirs, {len(files)} files scanned")


def get_default_template():
    """获取默认模板"""
    return """# 项目名称

## 一句话定位
[项目是干什么的，1-2 行]

## 技术栈
- 语言/框架：xxx
- 数据库：xxx
- 其他关键依赖：xxx

## 项目结构
```
├── src/           # 源代码
├── tests/         # 测试
└── docs/          # 文档
```

## 当前进度
- [ ] 进行中：xxx
- [ ] 计划中：xxx

## API 概览（如适用）
| 接口 | 说明 |
|------|------|
| GET /xxx | xxx |

## 踩坑记录
<!-- 在此记录常见的坑 -->

## 近期修改记录
<!-- 最近 10 条修改，按时间倒序 -->
| 日期 | 修改内容 | 相关文件/模块 |
|------|---------|--------------|
"""


def main():
    # Windows 终端编码处理
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="README Sync Operations")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # read 命令
    read_parser = subparsers.add_parser("read", help="Read a section")
    read_parser.add_argument("section", nargs="?", default="all", help="Section name (or 'all')")

    # pending 命令
    subparsers.add_parser("pending", help="Show pending updates")

    # add 命令
    add_parser = subparsers.add_parser("add", help="Add pending update")
    add_parser.add_argument("type", choices=["changelog", "progress", "trap"], help="Update type")
    add_parser.add_argument("content", help="Update content")
    add_parser.add_argument("--related", "-r", help="Related file/module")

    # clear 命令
    subparsers.add_parser("clear", help="Clear pending updates")

    # sync 命令
    subparsers.add_parser("sync", help="Sync pending updates to README")

    # init 命令
    subparsers.add_parser("init", help="Initialize README from template")

    # scan 命令
    subparsers.add_parser("scan", help="Scan project structure (preview only, no file write)")

    # auto-init 命令
    subparsers.add_parser("auto-init", help="Scan project and generate README automatically")

    # diff 命令
    subparsers.add_parser("diff", help="Show pending changes vs current README")

    args = parser.parse_args()

    if args.command == "read":
        read_section(args.section)
    elif args.command == "pending":
        show_pending()
    elif args.command == "add":
        add_pending(args.type, args.content, args.related)
    elif args.command == "clear":
        clear_pending()
    elif args.command == "sync":
        sync_to_readme()
    elif args.command == "init":
        init_readme()
    elif args.command == "scan":
        scan_project()
    elif args.command == "auto-init":
        auto_init()
    elif args.command == "diff":
        show_pending()
        print("Run 'sync' to apply these changes to README")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
