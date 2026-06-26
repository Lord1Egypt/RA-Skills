#!/usr/bin/env python3
"""
Tiered Recall - 记忆加载器
按层级加载记忆，支持深度回忆
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional


def load_memory_md(workspace: Path) -> str:
    """加载 MEMORY.md"""
    memory_file = workspace / "MEMORY.md"
    if not memory_file.exists():
        return ""
    
    content = memory_file.read_text(encoding="utf-8")
    lines = content.split("\n")
    
    # 返回前100行（核心记忆）
    return "\n".join(lines[:100])


def load_recent_logs(memory_dir: Path, days: int = 2) -> dict[str, str]:
    """加载最近N天的日志"""
    logs = {}
    
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        filename = f"{date.strftime('%Y-%m-%d')}.md"
        filepath = memory_dir / filename
        
        if filepath.exists():
            logs[filename] = filepath.read_text(encoding="utf-8")
    
    return logs


def load_active_projects(output_dir: Path) -> list[dict]:
    """加载活跃项目清单"""
    projects_file = output_dir / "projects.json"
    
    if not projects_file.exists():
        return []
    
    with open(projects_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data.get("active", [])


def load_index(output_dir: Path) -> dict:
    """加载记忆索引"""
    index_file = output_dir / "index.json"
    
    if not index_file.exists():
        return {}
    
    with open(index_file, "r", encoding="utf-8") as f:
        return json.load(f)


def estimate_tokens(text: str) -> int:
    """估算文本的token数（粗略：中文1字≈1token，英文1词≈1token）"""
    # 简单估算：字符数 / 2
    return len(text) // 2


def load_by_topic(index: dict, topic: str, memory_dir: Path) -> list[dict]:
    """按主题加载记忆"""
    results = []
    
    if topic not in index.get("topics", {}):
        return results
    
    for entry in index["topics"][topic]:
        # 兼容新旧格式
        if "f" in entry:
            filepath = memory_dir / entry["f"]
            lines_str = entry["l"]
            title = entry.get("t", "")
            summary = entry.get("s", "")  # 极致摘要
        else:
            filepath = memory_dir / entry["file"]
            lines_str = entry["lines"]
            title = entry.get("section", "")
            summary = entry.get("summary", "")
        
        if not filepath.exists():
            continue
        
        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")
        
        start, end = map(int, lines_str.split("-"))
        section_content = "\n".join(lines[start-1:end])
        
        results.append({
            "file": filepath.name,
            "title": title,
            "summary": summary,
            "content": section_content,
        })
    
    return results


def load_by_project(project_name: str, output_dir: Path, memory_dir: Path, index: dict) -> dict:
    """按项目加载相关记忆"""
    result = {
        "project": project_name,
        "entries": [],
        "files": [],
    }
    
    # 从索引中找相关主题
    for topic, entries in index.get("topics", {}).items():
        if project_name in topic or topic in project_name:
            for entry in entries:
                # 兼容新旧格式
                if "f" in entry:
                    filepath = memory_dir / entry["f"]
                    lines_str = entry["l"]
                    title = entry.get("t", "")
                    summary = entry.get("s", "")
                else:
                    filepath = memory_dir / entry["file"]
                    lines_str = entry["lines"]
                    title = entry.get("section", "")
                    summary = entry.get("summary", "")
                
                if filepath.exists():
                    content = filepath.read_text(encoding="utf-8")
                    lines = content.split("\n")
                    start, end = map(int, lines_str.split("-"))
                    
                    result["entries"].append({
                        "date": filepath.name.replace(".md", ""),
                        "title": title,
                        "summary": summary,
                        "content": "\n".join(lines[start-1:end]),
                    })
    
    # 加载项目文件
    projects = load_active_projects(output_dir)
    for p in projects:
        if p["name"] == project_name:
            result["project_info"] = p
            
            # 尝试加载关键文件
            workspace = memory_dir.parent
            project_path = workspace / p.get("path", "")
            if project_path.exists():
                for key_file in p.get("keyFiles", []):
                    key_filepath = project_path / key_file
                    if key_filepath.exists() and key_filepath.is_file():
                        try:
                            content = key_filepath.read_text(encoding="utf-8")
                            result["files"].append({
                                "path": str(key_filepath.relative_to(workspace)),
                                "size": len(content),
                                "preview": content[:500] + "..." if len(content) > 500 else content,
                            })
                        except Exception:
                            pass
            break
    
    return result


def format_output(
    memory_md: str,
    recent_logs: dict[str, str],
    active_projects: list[dict],
    index: dict,
) -> str:
    """格式化输出"""
    output = []
    
    # L0: 核心记忆
    if memory_md:
        lines = memory_md.split("\n")
        output.append("## 🔴 L0 核心记忆 (MEMORY.md)")
        output.append(f"Token估算: ~{estimate_tokens(memory_md)}")
        output.append("```markdown")
        output.append(memory_md[:2000])  # 截断到2000字符
        if len(memory_md) > 2000:
            output.append("... (已截断)")
        output.append("```")
        output.append("")
    
    # L1: 近期日志
    if recent_logs:
        output.append("## 🟠 L1 近期日志")
        total_tokens = sum(estimate_tokens(log) for log in recent_logs.values())
        output.append(f"文件: {', '.join(recent_logs.keys())}")
        output.append(f"Token估算: ~{total_tokens}")
        output.append("")
        
        for filename, content in recent_logs.items():
            lines = content.split("\n")
            # 只显示前50行
            output.append(f"### {filename}")
            output.append("```markdown")
            output.append("\n".join(lines[:50]))
            if len(lines) > 50:
                output.append(f"... (共{len(lines)}行，已截断)")
            output.append("```")
            output.append("")
    
    # L2: 活跃项目
    if active_projects:
        output.append("## 🟡 L2 活跃项目")
        output.append(f"项目数: {len(active_projects)}")
        output.append("")
        
        for p in active_projects:
            output.append(f"- **{p['name']}**")
            output.append(f"  - 路径: {p['path']}")
            output.append(f"  - 最近提及: {p['lastMentioned']}")
            output.append(f"  - 提及次数: {p['mentionCount']}")
        output.append("")
    
    # L3: 记忆索引
    if index:
        output.append("## 🟢 L3 记忆索引")
        output.append(f"更新时间: {index.get('lastUpdated', 'N/A')}")
        output.append(f"主题数: {len(index.get('topics', {}))}")
        output.append("")
        
        topics = index.get("topics", {})
        for topic, entries in list(topics.items())[:5]:  # 只显示前5个主题
            output.append(f"- {topic}: {len(entries)}条记录")
    
    total = sum(estimate_tokens(line) for line in output)
    output.insert(0, f"# 🧠 分层回忆输出")
    output.insert(1, f"总Token估算: ~{total}")
    output.insert(2, "")
    
    return "\n".join(output)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Tiered Recall 记忆加载器")
    parser.add_argument("--deep", action="store_true", help="深度加载（突破token限制）")
    parser.add_argument("--project", type=str, help="加载指定项目的记忆")
    parser.add_argument("--topic", type=str, help="加载指定主题的记忆")
    parser.add_argument("--days", type=int, default=2, help="加载最近N天的日志")
    parser.add_argument("--workspace", type=str, help="指定工作区路径")
    args = parser.parse_args()
    
    # 路径设置
    if args.workspace:
        workspace = Path(args.workspace)
    else:
        # 从脚本位置向上找到包含MEMORY.md的目录
        current = Path(__file__).resolve()
        while current.parent != current:
            if (current / "MEMORY.md").exists():
                workspace = current
                break
            current = current.parent
        else:
            # 默认使用脚本所在位置的上上上级
            workspace = Path(__file__).parent.parent.parent
    
    memory_dir = workspace / "memory"
    output_dir = workspace / ".tiered-recall"
    
    print("🧠 Tiered Recall - 记忆加载器")
    print("=" * 40)
    
    # 检查索引是否存在
    if not output_dir.exists():
        print("⚠️ 索引不存在，请先运行 build-index.py")
        return
    
    # 加载索引
    index = load_index(output_dir)
    
    # 特殊加载模式
    if args.project:
        print(f"\n📂 加载项目: {args.project}")
        result = load_by_project(args.project, output_dir, memory_dir, index)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    if args.topic:
        print(f"\n🔍 加载主题: {args.topic}")
        results = load_by_topic(index, args.topic, memory_dir)
        for r in results:
            title = r.get('title', '')
            summary = r.get('summary', '')
            if title and summary:
                print(f"\n### {r['file']} - {title} 【{summary}】")
            elif title:
                print(f"\n### {r['file']} - {title}")
            else:
                print(f"\n### {r['file']}")
            print(r['content'][:500])
        return
    
    # 默认分层加载
    print("\n📚 分层加载...")
    
    # L0
    print("  L0: 核心记忆...")
    memory_md = load_memory_md(workspace)
    
    # L1
    print(f"  L1: 最近{args.days}天日志...")
    recent_logs = load_recent_logs(memory_dir, args.days)
    
    # L2
    print("  L2: 活跃项目...")
    active_projects = load_active_projects(output_dir)
    
    # L3
    print("  L3: 记忆索引...")
    index = load_index(output_dir)
    
    # 输出
    print("\n" + "=" * 40)
    print(format_output(memory_md, recent_logs, active_projects, index))


if __name__ == "__main__":
    main()