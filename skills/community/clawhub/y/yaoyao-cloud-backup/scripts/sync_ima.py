#!/usr/bin/env python3
"""
龙虾记忆系统 - IMA 同步脚本
将重要记忆同步到 IMA 知识库
"""

import argparse
import sys
sys.path.insert(0, str(__file__).rsplit("/", 1)[0])
try:
    from audit import log
except:
    def log(*args, **kwargs): pass
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_ima_credentials():
    """加载 IMA 凭证"""
    # 优先从环境变量
    client_id = os.environ.get("IMA_OPENAPI_CLIENTID")
    api_key = os.environ.get("IMA_OPENAPI_APIKEY")
    
    # 其次从配置文件
    if not client_id or not api_key:
        config_dir = Path.home() / ".config" / "ima"
        if config_dir.exists():
            client_id_file = config_dir / "client_id"
            api_key_file = config_dir / "api_key"
            if client_id_file.exists():
                client_id = client_id_file.read_text().strip()
            if api_key_file.exists():
                api_key = api_key_file.read_text().strip()
    
    return client_id, api_key


def ima_api(path: str, body: dict, client_id: str, api_key: str) -> dict:
    """调用 IMA API"""
    import urllib.request
    import urllib.error
    
    url = f"https://ima.qq.com/{path}"
    headers = {
        "ima-openapi-clientid": client_id,
        "ima-openapi-apikey": api_key,
        "Content-Type": "application/json",
    }
    
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            # 兼容两种返回格式：code 或 retcode
            if "code" in result and "retcode" not in result:
                result["retcode"] = result["code"]
            return result
    except urllib.error.HTTPError as e:
        return {"retcode": e.code, "errmsg": str(e)}


def search_knowledge_base(query: str, client_id: str, api_key: str) -> list:
    """搜索知识库"""
    result = ima_api(
        "openapi/wiki/v1/search_knowledge_base",
        {"query": query, "cursor": "", "limit": 20},
        client_id,
        api_key
    )
    
    if result.get("retcode") == 0:
        return result.get("data", {}).get("infos", [])
    return []


def create_note(title: str, content: str, client_id: str, api_key: str, folder_id: str = None) -> dict:
    """创建笔记"""
    body = {
        "content_format": 1,  # Markdown
        "content": content,
    }
    if folder_id:
        body["folder_id"] = folder_id
    
    result = ima_api("openapi/note/v1/import_doc", body, client_id, api_key)
    return result


def extract_sync_content(workspace: Path, sync_type: str) -> list:
    """从 MEMORY.md 和每日记忆文件提取需要同步的内容"""
    items = []
    
    if sync_type == "decision":
        # 提取决策 - 从 MEMORY.md 和每日文件
        import re
        patterns = [
            r"###\s*\[(\d{4}-\d{2}-\d{2})\][^\n]*决策[^\n]*\n([\s\S]*?)(?=\n###|\n##|\Z)",
            r"###\s*(\d{4}-\d{2}-\d{2})[^\n]*决策[^\n]*\n([\s\S]*?)(?=\n###|\n##|\Z)",
            r"##\s*决策[^\n]*\n([\s\S]*?)(?=\n##|\Z)",
        ]
        
        all_content = {}
        
        # 1. 从每日记忆文件收集
        memory_dir = workspace / "memory"
        if memory_dir.exists():
            for day_file in sorted(memory_dir.glob("2026-*.md")):
                date_str = day_file.stem
                content = day_file.read_text(encoding="utf-8")
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        if len(match) == 2:
                            date, text = match
                        else:
                            date = date_str
                            text = match[0] if isinstance(match, tuple) else match
                        key = f"decision-{date}"
                        if key not in all_content:
                            all_content[key] = {
                                "title": f"决策记录 - {date}",
                                "content": f"# 决策记录 ({date})\n\n{text.strip()}",
                                "date": date,
                            }
        
        # 2. 从 MEMORY.md 收集
        memory_md = workspace / "MEMORY.md"
        if memory_md.exists():
            content = memory_md.read_text(encoding="utf-8")
            for pattern in patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if len(match) == 2:
                        date, text = match
                    else:
                        date = datetime.now().strftime("%Y-%m-%d")
                        text = match[0] if isinstance(match, tuple) else match
                    key = f"decision-{date}"
                    if key not in all_content:
                        all_content[key] = {
                            "title": f"决策记录 - {date}",
                            "content": f"# 决策记录 ({date})\n\n{text.strip()}",
                            "date": date,
                        }
        
        items = list(all_content.values())
    
    elif sync_type == "error":
        # 提取错误教训
        import re
        patterns = [
            r"###\s*\[(\d{4}-\d{2}-\d{2})\][^\n]*错误[^\n]*\n([\s\S]*?)(?=\n###|\n##|\Z)",
            r"###\s*(\d{4}-\d{2}-\d{2})[^\n]*错误[^\n]*\n([\s\S]*?)(?=\n###|\n##|\Z)",
            r"##\s*错误[^\n]*\n([\s\S]*?)(?=\n##|\Z)",
        ]
        
        all_content = {}
        
        # 从每日文件收集
        memory_dir = workspace / "memory"
        if memory_dir.exists():
            for day_file in sorted(memory_dir.glob("2026-*.md")):
                date_str = day_file.stem
                content = day_file.read_text(encoding="utf-8")
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        if len(match) == 2:
                            date, text = match
                        else:
                            date = date_str
                            text = match[0] if isinstance(match, tuple) else match
                        key = f"error-{date}"
                        if key not in all_content:
                            all_content[key] = {
                                "title": f"错误教训 - {date}",
                                "content": f"# 错误教训 ({date})\n\n{text.strip()}",
                                "date": date,
                            }
        
        items = list(all_content.values())
    
    elif sync_type == "all":
        # 合并 MEMORY.md 和每日记忆文件
        all_items = []
        
        # 1. 每日记忆文件（按日期排序）
        memory_dir = workspace / "memory"
        if memory_dir.exists():
            for day_file in sorted(memory_dir.glob("2026-*.md")):
                date_str = day_file.stem
                content = day_file.read_text(encoding="utf-8")
                all_items.append({
                    "title": f"每日记忆 - {date_str}",
                    "content": content,
                    "date": date_str,
                })
        
        # 2. MEMORY.md 长期记忆（放在最后）
        memory_md = workspace / "MEMORY.md"
        if memory_md.exists():
            content = memory_md.read_text(encoding="utf-8")
            all_items.append({
                "title": f"长期记忆 - {datetime.now().strftime('%Y-%m-%d')}",
                "content": content,
                "date": datetime.now().strftime("%Y-%m-%d"),
            })
        
        items = all_items
    
    return items


def check_ima_enabled(workspace: Path) -> bool:
    """检查 IMA 是否已启用"""
    state_file = workspace / "memory" / "heartbeat-state.json"
    if state_file.exists():
        state = json.loads(state_file.read_text(encoding="utf-8"))
        return state.get("imaEnabled", False)
    return False


def update_sync_time(workspace: Path):
    """更新最后同步时间"""
    state_file = workspace / "memory" / "heartbeat-state.json"
    if state_file.exists():
        state = json.loads(state_file.read_text(encoding="utf-8"))
        state["lastChecks"]["imaSync"] = datetime.now().isoformat()
        state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="同步记忆到 IMA 知识库")
    parser.add_argument("--workspace", default="~/.openclaw/workspace", help="工作空间路径")
    parser.add_argument("--type", choices=["decision", "error", "all"], default="all", help="同步类型")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不执行")
    parser.add_argument("--enable", action="store_true", help="启用 IMA 自动同步")
    parser.add_argument("--disable", action="store_true", help="禁用 IMA 自动同步")
    args = parser.parse_args()
    
    workspace = Path(args.workspace).expanduser()
    
    # 处理启用/禁用
    if args.enable or args.disable:
        state_file = workspace / "memory" / "heartbeat-state.json"
        if not state_file.exists():
            print("❌ 请先运行初始化: python3 scripts/init_memory.py")
            sys.exit(1)
        
        state = json.loads(state_file.read_text(encoding="utf-8"))
        state["imaEnabled"] = args.enable
        state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
        
        if args.enable:
            print("✅ IMA 自动同步已启用")
            print("   心跳维护时会自动同步重要记忆到云端")
        else:
            print("ℹ️  IMA 自动同步已禁用")
            print("   可手动同步: python3 scripts/sync_ima.py")
        return
    
    # 检查凭证
    client_id, api_key = load_ima_credentials()
    if not client_id or not api_key:
        print("❌ 缺少 IMA 凭证，请先配置:")
        print("   运行: python3 scripts/init_memory.py --ima-setup")
        sys.exit(1)
    
    # 检查是否启用
    if not check_ima_enabled(workspace):
        print("⚠️  IMA 自动同步未启用")
        print("   启用: python3 scripts/sync_ima.py --enable")
        print("   或继续手动同步...")
        print("")
    
    memory_md = workspace / "MEMORY.md"
    
    if not memory_md.exists():
        print(f"❌ MEMORY.md 不存在: {memory_md}")
        sys.exit(1)
    
    print(f"🔍 提取 {args.type} 类型内容...")
    items = extract_sync_content(workspace, args.type)
    
    if not items:
        print("✅ 没有需要同步的内容")
        return
    
    print(f"   找到 {len(items)} 条内容:\n")
    for item in items:
        print(f"   📄 {item['title']}")
    
    if args.dry_run:
        print("\n[DRY RUN] 预览完成，未执行同步")
        return
    
    print("\n🚀 同步到 IMA...")
    
    success_count = 0
    for item in items:
        result = create_note(item["title"], item["content"], client_id, api_key)
        if result.get("retcode") == 0:
            # IMA API 返回 note_id，不是 doc_id
            doc_id = result.get("data", {}).get("note_id") or result.get("data", {}).get("doc_id", "unknown")
            print(f"   ✅ {item['title']} → doc_id: {doc_id}")
            success_count += 1
        else:
            print(f"   ❌ {item['title']}: {result.get('errmsg', 'unknown error')}")
    
    # 更新同步时间
    if success_count > 0:
        update_sync_time(workspace)
    
    print(f"\n✅ 同步完成: {success_count}/{len(items)} 成功")


if __name__ == "__main__":
    main()
