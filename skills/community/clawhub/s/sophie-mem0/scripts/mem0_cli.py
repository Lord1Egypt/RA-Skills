#!/usr/bin/env python3
"""
Sophie Mem0 - 智能记忆系统 CLI

提供以下功能：
- 添加记忆 (add)
- 搜索记忆 (search)
- 获取所有记忆 (list)
- 删除记忆 (delete)
- 健康检查 (health)
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Optional

# 配置文件路径
CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/mem0_config.json")


def load_config() -> dict:
    """加载配置文件"""
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ 配置文件不存在: {CONFIG_PATH}")
        print("请先创建配置文件，参考 SKILL.md")
        sys.exit(1)
    
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def create_memory_client(config: dict):
    """创建内存客户端"""
    try:
        from mem0.memory.main import Memory
        return Memory.from_config(config)
    except ImportError:
        print("❌ mem0ai 未安装")
        print("请运行: pip install mem0ai")
        sys.exit(1)


def cmd_add(client, args):
    """添加记忆"""
    if not args.text:
        print("❌ 请提供记忆内容: --text '要记住的内容'")
        sys.exit(1)
    
    user_id = args.user or "sophie"
    
    try:
        result = client.add(
            messages=args.text,
            user_id=user_id,
            metadata=args.metadata
        )
        
        # 尝试从结果中提取ID
        memory_id = "unknown"
        if isinstance(result, dict):
            # 新版API返回格式
            if "id" in result:
                memory_id = result["id"]
            elif "memory_id" in result:
                memory_id = result["memory_id"]
            # 尝试从metadata中获取
            elif "metadata" in result and result["metadata"]:
                memory_id = result["metadata"].get("id", "unknown")
        
        print(f"✅ 已记住：{args.text}")
        print(f"   记忆ID: {memory_id}")
        print(f"   用户: {user_id}")
        print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ 添加记忆失败: {e}")
        sys.exit(1)


def cmd_search(client, args):
    """搜索记忆"""
    if not args.query:
        print("❌ 请提供搜索查询: --query '搜索内容'")
        sys.exit(1)
    
    user_id = args.user or "sophie"
    
    try:
        results = client.search(
            query=args.query,
            user_id=user_id,
            limit=args.limit or 5
        )
        
        if not results.get("results"):
            print(f"🔍 没有找到与「{args.query}」相关的记忆")
            return
        
        result_list = results["results"]
        print(f"🔍 找到 {len(result_list)} 条相关记忆：\n")
        
        for i, r in enumerate(result_list, 1):
            score = r.get("score", 0) * 100
            memory = r.get("memory", "")
            mem_id = r.get("id", "unknown")
            created = r.get("created_at", "unknown")
            
            print(f"{i}. {memory}")
            print(f"   相关度: {score:.1f}%")
            print(f"   ID: {mem_id}")
            print(f"   添加于: {created[:19] if created else 'unknown'}")
            print()
        
    except Exception as e:
        print(f"❌ 搜索失败: {e}")
        sys.exit(1)


def cmd_list(client, args):
    """列出所有记忆"""
    user_id = args.user or "sophie"
    
    try:
        all_memories = client.get_all(user_id=user_id)
        
        # 兼容新旧API格式
        memories = all_memories.get("memories") or all_memories.get("results") or []
        
        if not memories:
            print("📭 还没有任何记忆")
            return
        print(f"📚 共 {len(memories)} 条记忆：\n")
        
        for i, m in enumerate(memories, 1):
            memory = m.get("memory", "")
            mem_id = m.get("id", "unknown")
            created = m.get("created_at", "unknown")
            
            print(f"{i}. {memory}")
            print(f"   ID: {mem_id}")
            print(f"   添加于: {created[:19] if created else 'unknown'}")
            print()
        
    except Exception as e:
        print(f"❌ 获取记忆列表失败: {e}")
        sys.exit(1)


def cmd_delete(client, args):
    """删除记忆"""
    if not args.memory_id:
        print("❌ 请提供记忆ID: --memory-id 'xxx-xxx'")
        sys.exit(1)
    
    user_id = args.user or "sophie"
    
    try:
        client.delete(memory_id=args.memory_id, user_id=user_id)
        print(f"✅ 已删除记忆: {args.memory_id}")
        
    except Exception as e:
        print(f"❌ 删除记忆失败: {e}")
        sys.exit(1)


def cmd_health(args):
    """健康检查"""
    print("🏥 Sophie Mem0 健康检查\n")
    
    checks = []
    
    # 1. 检查配置文件
    try:
        config = load_config()
        checks.append(("配置文件", True, "OK"))
    except Exception as e:
        checks.append(("配置文件", False, str(e)))
    
    # 2. 检查 Qdrant 连接
    try:
        import requests
        resp = requests.get("http://localhost:6333/readyz", timeout=5)
        if resp.status_code == 200:
            checks.append(("Qdrant", True, "OK"))
        else:
            checks.append(("Qdrant", False, f"Status: {resp.status_code}"))
    except Exception as e:
        checks.append(("Qdrant", False, str(e)))
    
    # 3. 检查 mem0ai
    try:
        from mem0 import __version__
        checks.append(("mem0ai", True, f"v{__version__}"))
    except Exception as e:
        checks.append(("mem0ai", False, "未安装"))
    
    # 4. 检查 API Key
    try:
        config = load_config()
        api_key = config.get("llm", {}).get("config", {}).get("api_key", "")
        if api_key and len(api_key) > 10:
            checks.append(("API Key", True, f"已配置 ({api_key[:8]}...)"))
        else:
            checks.append(("API Key", False, "未配置"))
    except Exception as e:
        checks.append(("API Key", False, str(e)))
    
    # 输出结果
    all_ok = True
    for name, ok, detail in checks:
        status = "✅" if ok else "❌"
        print(f"{status} {name}: {detail}")
        if not ok:
            all_ok = False
    
    print()
    if all_ok:
        print("✅ 所有检查通过，记忆系统运行正常！")
    else:
        print("⚠️ 部分检查失败，请查看上述错误")
    
    sys.exit(0 if all_ok else 1)


def main():
    parser = argparse.ArgumentParser(
        description="Sophie Mem0 - 智能记忆系统",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="添加新记忆")
    add_parser.add_argument("--text", "-t", required=True, help="记忆内容")
    add_parser.add_argument("--user", "-u", default="sophie", help="用户ID")
    add_parser.add_argument("--metadata", "-m", help="元数据 (JSON格式)")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索记忆")
    search_parser.add_argument("--query", "-q", required=True, help="搜索查询")
    search_parser.add_argument("--user", "-u", default="sophie", help="用户ID")
    search_parser.add_argument("--limit", "-l", type=int, default=5, help="返回结果数量")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有记忆")
    list_parser.add_argument("--user", "-u", default="sophie", help="用户ID")
    
    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除记忆")
    delete_parser.add_argument("--memory-id", "-i", required=True, help="记忆ID")
    delete_parser.add_argument("--user", "-u", default="sophie", help="用户ID")
    
    # health 命令
    health_parser = subparsers.add_parser("health", help="健康检查")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "health":
        cmd_health(args)
        return
    
    # 加载配置并创建客户端
    config = load_config()
    client = create_memory_client(config)
    
    # 执行命令
    if args.command == "add":
        cmd_add(client, args)
    elif args.command == "search":
        cmd_search(client, args)
    elif args.command == "list":
        cmd_list(client, args)
    elif args.command == "delete":
        cmd_delete(client, args)


if __name__ == "__main__":
    main()
