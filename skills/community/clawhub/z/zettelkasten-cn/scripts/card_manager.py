#!/usr/bin/env python3
"""
Zettelkasten Card Manager - 卢曼卡片学习法核心脚本
处理四级笔记的全生命周期操作，并与 Agent 记忆系统关联
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# 配置 - 支持环境变量覆盖
CARDS_DIR = Path(os.environ.get("ZETTELKASTEN_CARDS_DIR", "~/Desktop/cardsdata")).expanduser()
MEMORY_DIR = Path(os.environ.get("ZETTELKASTEN_MEMORY_DIR", "~/.openclaw/workspace/memory")).expanduser()
WORKSPACE_DIR = Path(os.environ.get("ZETTELKASTEN_WORKSPACE_DIR", "~/.openclaw/workspace")).expanduser()
TEMPLATES_DIR = Path(__file__).parent.parent / "assets" / "templates"

NOTE_TYPES = {
    "fleeting": "inbox",
    "literature": "lit", 
    "permanent": "zettel",
    "project": "project",
    "map": "map"
}

# 永久笔记子分类
PERMANENT_CATEGORIES = {
    "身心": "身心",
    "学习": "学习",
    "投资": "投资",
    "家庭": "家庭",
    "事业": "事业",
    "社交": "社交",
    "物品": "物品",
    "爱好": "爱好",
    "体验": "体验"
}

def get_today_id() -> str:
    """生成今日 ID 前缀"""
    return datetime.now().strftime("%Y%m%d")

def get_next_sequence() -> str:
    """获取当日下一个序号"""
    today = get_today_id()
    existing = list(CARDS_DIR.rglob(f"{today}-*.md"))
    
    if not existing:
        return f"{today}-0001"
    
    # 提取序号
    numbers = []
    for f in existing:
        match = re.search(rf"{today}-(\d{{4}})", f.name)
        if match:
            numbers.append(int(match.group(1)))
    
    next_num = max(numbers) + 1 if numbers else 1
    return f"{today}-{next_num:04d}"

def generate_id() -> str:
    """生成唯一 ID"""
    return get_next_sequence()

def load_template(template_name: str) -> str:
    """加载模板文件"""
    template_path = TEMPLATES_DIR / f"{template_name}.md"
    if template_path.exists():
        return template_path.read_text(encoding='utf-8')
    return ""

def render_template(template: str, data: Dict[str, Any]) -> str:
    """渲染模板"""
    result = template
    for key, value in data.items():
        placeholder = "{{" + key + "}}"
        if isinstance(value, list):
            value = json.dumps(value) if value else "[]"
        elif value is None:
            value = ""
        result = result.replace(placeholder, str(value))
    return result

def create_note(note_type: str, title: str, content: str = "", **kwargs) -> Dict[str, Any]:
    """
    创建新笔记
    
    Args:
        note_type: 笔记类型 (fleeting/literature/permanent/project/map)
        title: 笔记标题
        content: 笔记内容
        **kwargs: 额外字段，permanent 类型可传入 category 参数指定分类
    
    Returns:
        创建的笔记信息
    """
    note_id = generate_id()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 确定存储目录
    folder = NOTE_TYPES.get(note_type, "inbox")
    
    # 永久笔记支持子分类
    if note_type == "permanent":
        category = kwargs.get("category", "")
        if category and category in PERMANENT_CATEGORIES:
            folder_path = CARDS_DIR / folder / category
        else:
            folder_path = CARDS_DIR / folder
    else:
        folder_path = CARDS_DIR / folder
    
    folder_path.mkdir(parents=True, exist_ok=True)
    
    # 构建文件名
    slug = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-').lower()[:30]
    filename = f"{note_id}-{slug}.md" if slug else f"{note_id}.md"
    filepath = folder_path / filename
    
    # 准备模板数据
    template_data = {
        "id": note_id,
        "created": now,
        "modified": now,
        "title": title,
        "content": content or "（待补充内容）",
        "summary": kwargs.get("summary", ""),
        "tags": json.dumps(kwargs.get("tags", [])),
        "links": json.dumps(kwargs.get("links", [])),
        "backlinks": json.dumps(kwargs.get("backlinks", [])),
        "memory_refs": json.dumps(kwargs.get("memory_refs", [])),
        "source": kwargs.get("source", ""),
        "source_type": kwargs.get("source_type", ""),
        "source_title": kwargs.get("source_title", ""),
        "author": kwargs.get("author", ""),
        "url": kwargs.get("url", ""),
        "thoughts": kwargs.get("thoughts", ""),
        "zettel_links": json.dumps(kwargs.get("zettel_links", [])),
        "lit_links": json.dumps(kwargs.get("lit_links", [])),
        "up_links": json.dumps(kwargs.get("up_links", [])),
        "down_links": json.dumps(kwargs.get("down_links", [])),
        "peer_links": json.dumps(kwargs.get("peer_links", [])),
        "quote": kwargs.get("quote", ""),
        "goal": kwargs.get("goal", ""),
        "tasks": kwargs.get("tasks", "- [ ] "),
        "progress": kwargs.get("progress", ""),
        "review": kwargs.get("review", ""),
        "status": kwargs.get("status", "active"),
        "deadline": kwargs.get("deadline", ""),
        "slug": kwargs.get("slug", ""),
        "description": kwargs.get("description", ""),
        "core_concepts": kwargs.get("core_concepts", ""),
        "sub_topics": kwargs.get("sub_topics", ""),
        "related_maps": kwargs.get("related_maps", ""),
        "recent_updates": kwargs.get("recent_updates", ""),
        "updated": now,
        "memory_ref": kwargs.get("memory_ref", "")
    }
    
    # 加载并渲染模板
    template = load_template(note_type)
    rendered = render_template(template, template_data)
    
    # 写入文件
    filepath.write_text(rendered, encoding='utf-8')
    
    # 记录操作
    log_operation("create", {
        "id": note_id,
        "type": note_type,
        "title": title,
        "path": str(filepath)
    })
    
    return {
        "id": note_id,
        "type": note_type,
        "title": title,
        "path": str(filepath),
        "created": now
    }

def read_note(note_id: str) -> Optional[Dict[str, Any]]:
    """读取笔记"""
    # 搜索所有目录
    for folder in NOTE_TYPES.values():
        folder_path = CARDS_DIR / folder
        if not folder_path.exists():
            continue
        
        for f in folder_path.glob(f"{note_id}*.md"):
            if note_id in f.name:
                content = f.read_text(encoding='utf-8')
                return {
                    "id": note_id,
                    "path": str(f),
                    "content": content,
                    "folder": folder
                }
    return None

def update_note(note_id: str, **updates) -> bool:
    """更新笔记"""
    note = read_note(note_id)
    if not note:
        return False
    
    content = note["content"]
    filepath = Path(note["path"])
    
    # 更新 frontmatter
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 简单替换 frontmatter 字段
    for key, value in updates.items():
        if key == "content":
            # 替换正文内容（在 --- 之后）
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[0] + "---" + parts[1] + "---\n" + value
        else:
            # 替换 frontmatter 字段
            pattern = rf"({key}:).*$"
            replacement = rf"\1 {value}"
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # 更新 modified 时间
    content = re.sub(r"(modified:).*$", rf"\1 {now}", content, flags=re.MULTILINE)
    
    filepath.write_text(content, encoding='utf-8')
    return True

def log_operation(op_type: str, details: Dict[str, Any]) -> str:
    """记录操作到撤销历史"""
    try:
        import subprocess
        import json
        
        cmd = [
            "python3",
            str(Path(__file__).parent / "undo_manager.py"),
            "log",
            op_type,
            "--details",
            json.dumps(details, ensure_ascii=False)
        ]
        subprocess.run(cmd, capture_output=True)
    except:
        pass  # 记录失败不影响主操作
    return ""

def delete_note(note_id: str) -> bool:
    """删除笔记"""
    note = read_note(note_id)
    if not note:
        return False
    
    filepath = Path(note["path"])
    
    # 移动到回收站而不是直接删除
    trash_dir = CARDS_DIR / ".system" / "trash"
    trash_dir.mkdir(parents=True, exist_ok=True)
    
    new_path = trash_dir / filepath.name
    
    # 记录操作
    log_operation("delete", {
        "id": note_id,
        "title": note.get("title", ""),
        "original_path": str(filepath),
        "trash_path": str(new_path)
    })
    
    filepath.rename(new_path)
    return True

def search_notes(query: str, note_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """搜索笔记"""
    results = []
    
    folders = [NOTE_TYPES[note_type]] if note_type else NOTE_TYPES.values()
    
    for folder in folders:
        folder_path = CARDS_DIR / folder
        if not folder_path.exists():
            continue
        
        for f in folder_path.glob("*.md"):
            content = f.read_text(encoding='utf-8').lower()
            if query.lower() in content or query.lower() in f.name.lower():
                # 提取标题
                title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
                title = title_match.group(1) if title_match else f.stem
                
                # 提取 ID
                id_match = re.search(r"^id: (.+)$", content, re.MULTILINE)
                note_id = id_match.group(1) if id_match else f.stem[:12]
                
                results.append({
                    "id": note_id,
                    "title": title,
                    "path": str(f),
                    "folder": folder,
                    "preview": content[:200] + "..." if len(content) > 200 else content
                })
    
    return results

def list_notes(note_type: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """列出笔记"""
    results = []
    
    folders = [NOTE_TYPES[note_type]] if note_type else NOTE_TYPES.values()
    
    for folder in folders:
        folder_path = CARDS_DIR / folder
        if not folder_path.exists():
            continue
        
        files = sorted(folder_path.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
        
        for f in files[:limit]:
            content = f.read_text(encoding='utf-8')
            
            # 提取标题
            title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
            title = title_match.group(1) if title_match else f.stem
            
            # 提取 ID
            id_match = re.search(r"^id: (.+)$", content, re.MULTILINE)
            note_id = id_match.group(1) if id_match else f.stem[:12]
            
            # 提取创建时间
            created_match = re.search(r"^created: (.+)$", content, re.MULTILINE)
            created = created_match.group(1) if created_match else ""
            
            results.append({
                "id": note_id,
                "title": title,
                "folder": folder,
                "created": created,
                "path": str(f)
            })
    
    return results

def link_notes(from_id: str, to_id: str, link_type: str = "related") -> bool:
    """在两个笔记之间建立链接"""
    from_note = read_note(from_id)
    to_note = read_note(to_id)
    
    if not from_note or not to_note:
        return False
    
    # 读取当前链接
    from_content = from_note["content"]
    
    # 提取现有 links
    links_match = re.search(r"^links: (.+)$", from_content, re.MULTILINE)
    if links_match:
        try:
            links = json.loads(links_match.group(1))
        except:
            links = []
    else:
        links = []
    
    # 添加新链接
    link_entry = {"id": to_id, "type": link_type}
    if link_entry not in links:
        links.append(link_entry)
    
    # 更新笔记
    return update_note(from_id, links=json.dumps(links))

def add_memory_ref(note_id: str, memory_date: str, context: str = "") -> bool:
    """添加记忆引用到笔记"""
    note = read_note(note_id)
    if not note:
        return False
    
    content = note["content"]
    
    # 提取现有 memory_refs
    refs_match = re.search(r"^memory_refs: (.+)$", content, re.MULTILINE)
    if refs_match:
        try:
            refs = json.loads(refs_match.group(1))
        except:
            refs = []
    else:
        refs = []
    
    # 添加新引用
    ref_entry = {"date": memory_date, "context": context}
    if ref_entry not in refs:
        refs.append(ref_entry)
    
    return update_note(note_id, memory_refs=json.dumps(refs))

def get_note_by_memory(memory_date: str) -> List[Dict[str, Any]]:
    """查找关联到特定记忆的笔记"""
    results = []
    
    for folder in NOTE_TYPES.values():
        folder_path = CARDS_DIR / folder
        if not folder_path.exists():
            continue
        
        for f in folder_path.glob("*.md"):
            content = f.read_text(encoding='utf-8')
            
            # 检查是否引用该记忆
            if f"memory_refs:" in content and memory_date in content:
                title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
                title = title_match.group(1) if title_match else f.stem
                
                id_match = re.search(r"^id: (.+)$", content, re.MULTILINE)
                note_id = id_match.group(1) if id_match else f.stem[:12]
                
                results.append({
                    "id": note_id,
                    "title": title,
                    "path": str(f),
                    "folder": folder
                })
    
    return results

def convert_fleeting_to_permanent(fleeting_id: str, **kwargs) -> Optional[Dict[str, Any]]:
    """将闪念笔记转化为永久笔记"""
    fleeting = read_note(fleeting_id)
    if not fleeting or fleeting["folder"] != "inbox":
        return None
    
    # 读取内容
    content = fleeting["content"]
    
    # 提取标题
    title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Untitled"
    
    # 提取正文（去掉 frontmatter）
    parts = content.split("---", 2)
    if len(parts) >= 3:
        body = parts[2].strip()
    else:
        body = content
    
    # 创建永久笔记
    result = create_note(
        "permanent",
        title=kwargs.get("title", title),
        content=kwargs.get("content", body),
        summary=kwargs.get("summary", ""),
        tags=kwargs.get("tags", []),
        memory_refs=kwargs.get("memory_refs", [datetime.now().strftime("%Y-%m-%d")]),
        **kwargs
    )
    
    # 可选：归档原闪念笔记
    if kwargs.get("archive_original", True):
        archive_dir = CARDS_DIR / ".system" / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        old_path = Path(fleeting["path"])
        new_path = archive_dir / old_path.name
        old_path.rename(new_path)
    
    return result

def main():
    parser = argparse.ArgumentParser(description="卢曼卡片学习法管理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # create 命令
    create_parser = subparsers.add_parser("create", help="创建新笔记")
    create_parser.add_argument("type", choices=NOTE_TYPES.keys(), help="笔记类型")
    create_parser.add_argument("title", help="笔记标题")
    create_parser.add_argument("--content", "-c", default="", help="笔记内容")
    create_parser.add_argument("--tags", "-t", help="标签，逗号分隔")
    create_parser.add_argument("--source", "-s", help="来源")
    create_parser.add_argument("--memory", "-m", help="关联的记忆日期 (YYYY-MM-DD)")
    create_parser.add_argument("--category", choices=list(PERMANENT_CATEGORIES.keys()), help="永久笔记分类（仅 permanent 类型）")
    
    # read 命令
    read_parser = subparsers.add_parser("read", help="读取笔记")
    read_parser.add_argument("id", help="笔记ID")
    
    # update 命令
    update_parser = subparsers.add_parser("update", help="更新笔记")
    update_parser.add_argument("id", help="笔记ID")
    update_parser.add_argument("--content", "-c", help="新内容")
    update_parser.add_argument("--title", "-t", help="新标题")
    
    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除笔记")
    delete_parser.add_argument("id", help="笔记ID")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索笔记")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.add_argument("--type", choices=NOTE_TYPES.keys(), help="限定笔记类型")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出笔记")
    list_parser.add_argument("--type", choices=NOTE_TYPES.keys(), help="限定笔记类型")
    list_parser.add_argument("--limit", "-n", type=int, default=20, help="数量限制")
    
    # link 命令
    link_parser = subparsers.add_parser("link", help="链接笔记")
    link_parser.add_argument("from_id", help="源笔记ID")
    link_parser.add_argument("to_id", help="目标笔记ID")
    link_parser.add_argument("--type", default="related", help="链接类型")
    
    # memory 命令
    memory_parser = subparsers.add_parser("memory", help="管理记忆关联")
    memory_subparsers = memory_parser.add_subparsers(dest="memory_command")
    
    mem_add = memory_subparsers.add_parser("add", help="添加记忆引用")
    mem_add.add_argument("note_id", help="笔记ID")
    mem_add.add_argument("date", help="记忆日期 (YYYY-MM-DD)")
    mem_add.add_argument("--context", "-c", default="", help="上下文描述")
    
    mem_find = memory_subparsers.add_parser("find", help="查找关联记忆的笔记")
    mem_find.add_argument("date", help="记忆日期")
    
    # convert 命令
    convert_parser = subparsers.add_parser("convert", help="转化笔记类型")
    convert_parser.add_argument("id", help="闪念笔记ID")
    convert_parser.add_argument("--title", "-t", help="新标题")
    convert_parser.add_argument("--summary", "-s", help="核心观点")
    convert_parser.add_argument("--category", choices=list(PERMANENT_CATEGORIES.keys()), help="永久笔记分类")
    convert_parser.add_argument("--keep", action="store_true", help="保留原笔记")
    
    args = parser.parse_args()
    
    if args.command == "create":
        tags = args.tags.split(",") if args.tags else []
        memory_refs = [args.memory] if args.memory else []
        
        # 构建 kwargs
        kwargs = {
            "tags": tags,
            "source": args.source,
            "memory_refs": memory_refs
        }
        
        # 添加分类（如果是永久笔记）
        if args.type == "permanent" and args.category:
            kwargs["category"] = args.category
        
        result = create_note(
            args.type,
            args.title,
            args.content,
            **kwargs
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "read":
        result = read_note(args.id)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"笔记 {args.id} 未找到", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "update":
        updates = {}
        if args.content:
            updates["content"] = args.content
        if args.title:
            updates["title"] = args.title
        
        if update_note(args.id, **updates):
            print(f"笔记 {args.id} 已更新")
        else:
            print(f"笔记 {args.id} 未找到", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "delete":
        if delete_note(args.id):
            print(f"笔记 {args.id} 已移至回收站")
        else:
            print(f"笔记 {args.id} 未找到", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "search":
        results = search_notes(args.query, args.type)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.command == "list":
        results = list_notes(args.type, args.limit)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.command == "link":
        if link_notes(args.from_id, args.to_id, args.type):
            print(f"已创建链接: {args.from_id} -> {args.to_id}")
        else:
            print("链接创建失败", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "memory":
        if args.memory_command == "add":
            if add_memory_ref(args.note_id, args.date, args.context):
                print(f"已为 {args.note_id} 添加记忆引用 {args.date}")
            else:
                print("添加失败", file=sys.stderr)
                sys.exit(1)
        
        elif args.memory_command == "find":
            results = get_note_by_memory(args.date)
            print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.command == "convert":
        kwargs = {
            "title": args.title,
            "summary": args.summary,
            "archive_original": not args.keep
        }
        if args.category:
            kwargs["category"] = args.category
        
        result = convert_fleeting_to_permanent(args.id, **kwargs)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("转化失败", file=sys.stderr)
            sys.exit(1)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
