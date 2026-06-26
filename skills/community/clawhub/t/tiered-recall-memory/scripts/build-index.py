#!/usr/bin/env python3
"""
Tiered Recall - 记忆索引生成器
扫描 memory/ 目录，提取主题和关键词，生成 index.json
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# 项目关键词模式
PROJECT_PATTERNS = [
    {"name": "合成天选打工人", "pattern": r"(合成天选打工人|天选打工人|游戏|merge-worker)", "path": "games/merge-worker/", "keyFiles": ["index.html"]},
    {"name": "搞钱特战队", "pattern": r"(搞钱特战队|赚钱|变现|商业模式)", "path": "products/AI-Guide/"},
    {"name": "OpenClaw变现", "pattern": r"(OpenClaw变现|安装服务|咨询服务)", "path": "products/"},
    {"name": "team-collab", "pattern": r"(team-collab|团队协作)", "path": "skills/team-collab/"},
    {"name": "tiered-recall", "pattern": r"(分层回忆|tiered-recall)", "path": "skills/tiered-recall/"},
]

# 主题分类关键词
TOPIC_KEYWORDS = {
    "游戏开发": ["游戏", "版本", "Bug", "修复", "功能", "v2.", "关卡", "合成"],
    "搞钱特战队": ["搞钱", "赚钱", "变现", "商业模式", "定价", "收入", "产品"],
    "OpenClaw": ["OpenClaw", "安装", "部署", "Gateway", "配置"],
    "团队协作": ["团队", "子代理", "spawn", "会议", "投票"],
    "记忆系统": ["记忆", "MEMORY", "日志", "反思", "回忆"],
    "健康提醒": ["健康", "喝水", "运动", "护肤", "HealthGuardian"],
    "软著申请": ["软著", "著作权", "版权", "源代码"],
    "抖音小游戏": ["抖音", "小游戏", "tt.", "SDK"],
}


def extract_sections(content: str) -> list[dict]:
    """提取Markdown文件的章节"""
    sections = []
    lines = content.split("\n")
    
    current_section = None
    start_line = 0
    
    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            if current_section:
                current_section["end_line"] = i - 1
                sections.append(current_section)
            
            current_section = {
                "title": line[3:].strip(),
                "start_line": i,
                "content_lines": [],
            }
        elif current_section:
            current_section["content_lines"].append(line)
    
    if current_section:
        current_section["end_line"] = len(lines)
        sections.append(current_section)
    
    return sections


def classify_topic(text: str) -> list[str]:
    """根据内容分类主题"""
    topics = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text.lower():
                topics.append(topic)
                break
    return topics


def summarize_section(lines: list[str], max_length: int = 10) -> str:
    """生成极致摘要（10字以内，用于区分同标题条目）"""
    # 提取第一个有意义的行
    for line in lines[:10]:
        line = line.strip()
        # 跳过空行、表格、分隔线、代码块
        if not line or line.startswith("|") or line.startswith("---") or line.startswith("```") or line.startswith("#"):
            continue
        # 提取关键词：去掉常见前缀
        for prefix in ["- ", "* ", "1. ", "2. ", "3. ", "### ", "**", "【", "（"]:
            if line.startswith(prefix):
                line = line[len(prefix):]
        # 截取前10个有效字符
        return line[:max_length].replace("**", "").replace("【", "").replace("】", "")
    return ""


def build_index(memory_dir: Path, output_dir: Path):
    """构建记忆索引（精简版，只保留定位信息）"""
    index = {
        "v": "1.0.1",  # 版本（缩写）
        "t": datetime.now().isoformat(),  # 时间（缩写）
        "topics": defaultdict(list),
    }
    
    # 扫描所有日志文件
    log_files = sorted(memory_dir.glob("*.md"), key=lambda x: x.name, reverse=True)
    
    for file in log_files:
        try:
            content = file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"⚠️ 读取失败: {file.name} - {e}")
            continue
        
        # 提取章节
        sections = extract_sections(content)
        
        for section in sections:
            # 分类主题
            topics = classify_topic(section["title"] + " " + " ".join(section["content_lines"][:5]))
            
            for topic in topics:
                # 索引格式：文件名+行号+标题+极致摘要（10字内）
                summary = summarize_section(section["content_lines"])
                index["topics"][topic].append({
                    "f": file.name,  # 文件名
                    "l": f"{section['start_line']}-{section['end_line']}",  # 行号
                    "t": section["title"][:50],  # 章节标题（限制50字符）
                    "s": summary,  # 极致摘要（10字内）
                })
    
    # 转换 defaultdict 为普通 dict
    index["topics"] = dict(index["topics"])
    
    # 保存索引（紧凑格式）
    output_dir.mkdir(parents=True, exist_ok=True)
    index_file = output_dir / "index.json"
    
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(',', ':'))
    
    print(f"✅ 索引已生成: {index_file}")
    print(f"   - 主题数: {len(index['topics'])}")
    
    for topic, entries in index["topics"].items():
        print(f"   - {topic}: {len(entries)} 条")
    
    return index


def detect_active_projects(memory_dir: Path, output_dir: Path, days: int = 7):
    """检测活跃项目"""
    from datetime import datetime, timedelta
    
    projects = {}
    cutoff = datetime.now() - timedelta(days=days)
    
    log_files = sorted(memory_dir.glob("*.md"), key=lambda x: x.name, reverse=True)
    
    for file in log_files:
        try:
            file_date = datetime.strptime(file.stem, "%Y-%m-%d")
        except ValueError:
            continue
        
        if file_date < cutoff:
            continue
        
        try:
            content = file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"⚠️ 读取失败: {file.name} - {e}")
            continue
        
        for pattern in PROJECT_PATTERNS:
            if re.search(pattern["pattern"], content, re.IGNORECASE):
                project_name = pattern["name"]
                if project_name not in projects:
                    projects[project_name] = {
                        "name": project_name,
                        "path": pattern.get("path", ""),
                        "keyFiles": pattern.get("keyFiles", []),
                        "lastMentioned": file.stem,
                        "mentionCount": 0,
                    }
                projects[project_name]["mentionCount"] += 1
    
    # 按提及次数排序
    sorted_projects = sorted(projects.values(), key=lambda x: x["mentionCount"], reverse=True)
    
    # 保存项目清单
    output_dir.mkdir(parents=True, exist_ok=True)
    projects_file = output_dir / "projects.json"
    
    output = {
        "version": "1.0.0",
        "lastUpdated": datetime.now().isoformat(),
        "recentDays": days,
        "active": sorted_projects,
    }
    
    with open(projects_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 活跃项目已更新: {projects_file}")
    for p in sorted_projects:
        print(f"   - {p['name']}: {p['mentionCount']}次提及 (最近: {p['lastMentioned']})")
    
    return sorted_projects


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Tiered Recall 索引生成器")
    parser.add_argument("--clean", action="store_true", help="清理旧索引后重建")
    parser.add_argument("--days", type=int, default=7, help="检测活跃项目的天数范围")
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
    
    print("🧠 Tiered Recall - 索引生成器")
    print("=" * 40)
    print(f"工作区: {workspace}")
    print(f"记忆目录: {memory_dir}")
    print(f"输出目录: {output_dir}")
    print()
    
    # 检查记忆目录
    if not memory_dir.exists():
        print(f"⚠️ 记忆目录不存在: {memory_dir}")
        memory_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ 已创建: {memory_dir}")
    
    # 清理旧索引
    if args.clean and output_dir.exists():
        import shutil
        shutil.rmtree(output_dir)
        print("🗑️ 已清理旧索引")
    
    # 构建索引
    print("\n📚 构建记忆索引...")
    build_index(memory_dir, output_dir)
    
    # 检测活跃项目
    print(f"\n🔍 检测活跃项目（最近{args.days}天）...")
    detect_active_projects(memory_dir, output_dir, args.days)
    
    print("\n✅ 完成！")


if __name__ == "__main__":
    main()