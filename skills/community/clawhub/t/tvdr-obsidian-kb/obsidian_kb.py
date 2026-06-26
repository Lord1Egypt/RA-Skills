#!/usr/bin/env python3
"""
Obsidian知识库管理工具
支持创建笔记、语义搜索、笔记管理等操作
"""

import urllib.request
import urllib.parse
import json
import sys
import os
from datetime import datetime

class ObsidianKB:
    """Obsidian知识库API客户端"""
    
    def __init__(self, api_url="http://192.168.18.15:5000"):
        self.api_url = api_url.rstrip('/')
        self.session_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def health_check(self):
        """检查服务健康状态"""
        try:
            req = urllib.request.Request(f"{self.api_url}/health")
            with urllib.request.urlopen(req) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            return f"❌ 健康检查失败: {e}"
    
    def create_note(self, title, content, tags=None, folder=None):
        """创建新笔记"""
        try:
            data = {
                "title": title,
                "content": content,
                "tags": tags or []
            }
            if folder:
                data["folder"] = folder
            
            json_data = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(
                f"{self.api_url}/api/note",
                data=json_data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("status", "success"), result.get("message", ""), result.get("file", "")
                
        except Exception as e:
            return "error", f"创建笔记失败: {e}", ""
    
    def search_notes(self, query, limit=10):
        """语义搜索笔记"""
        try:
            data = {"query": query}
            if limit:
                data["limit"] = limit
            
            json_data = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(
                f"{self.api_url}/api/search",
                data=json_data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
                
        except Exception as e:
            return {"status": "error", "message": f"搜索失败: {e}"}
    
    def get_note(self, filename):
        """获取单个笔记"""
        try:
            req = urllib.request.Request(f"{self.api_url}/api/note?file={urllib.parse.quote(filename)}")
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return {"status": "error", "message": f"获取笔记失败: {e}"}
    
    def list_notes(self):
        """列出所有笔记"""
        try:
            req = urllib.request.Request(f"{self.api_url}/api/notes")
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return {"status": "error", "message": f"列出笔记失败: {e}"}
    
    def get_stats(self):
        """获取统计信息"""
        try:
            req = urllib.request.Request(f"{self.api_url}/api/stats")
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return {"status": "error", "message": f"获取统计信息失败: {e}"}
    
    def rebuild_index(self):
        """重建索引"""
        try:
            req = urllib.request.Request(
                f"{self.api_url}/api/build",
                method='POST'
            )
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return {"status": "error", "message": f"重建索引失败: {e}"}


def create_note_cli():
    """命令行创建笔记"""
    if len(sys.argv) < 3:
        print("❌ 用法: python obsidian_kb.py create \"标题\" \"内容\" [tags...] [folder]")
        return
    
    title = sys.argv[2]
    content = sys.argv[3]
    tags = sys.argv[4:-1] if len(sys.argv) > 4 else []
    folder = sys.argv[-1] if len(sys.argv) > 5 else None
    
    kb = ObsidianKB()
    status, message, file = kb.create_note(title, content, tags, folder)
    print(f"状态: {status}")
    print(f"消息: {message}")
    if file:
        print(f"文件: {file}")


def search_notes_cli():
    """命令行搜索笔记"""
    if len(sys.argv) < 3:
        print("❌ 用法: python obsidian_kb.py search \"查询内容\" [limit]")
        return
    
    query = sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    kb = ObsidianKB()
    results = kb.search_notes(query, limit)
    
    print(f"🔍 搜索结果: {query}")
    print("=" * 50)
    
    if results.get("status") == "success":
        for i, result in enumerate(results.get("results", [])):
            print(f"\n📄 {i+1}. {result.get('title', 'Unknown')}")
            print(f"📁 文件: {result.get('file', 'Unknown')}")
            print(f"🔗 相似度: {result.get('similarity', 0):.3f}")
            print(f"📝 内容预览:")
            content = result.get('content', '')[:200]
            print(f"   {content}...")
    else:
        print(f"❌ 搜索失败: {results.get('message')}")


def health_check_cli():
    """命令行健康检查"""
    kb = ObsidianKB()
    result = kb.health_check()
    print(f"健康检查: {result}")


def list_notes_cli():
    """命令行列出笔记"""
    kb = ObsidianKB()
    notes = kb.list_notes()
    
    if notes.get("status") == "success":
        print(f"📚 总计: {len(notes.get('notes', []))} 篇笔记")
        print("=" * 50)
        for note in notes.get('notes', [])[:20]:  # 只显示前20个
            print(f"📄 {note}")
        if len(notes.get('notes', [])) > 20:
            print(f"... 还有 {len(notes.get('notes', [])) - 20} 篇笔记")
    else:
        print(f"❌ 获取笔记列表失败: {notes.get('message')}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("🔍 Obsidian知识库管理工具")
        print("=" * 30)
        print("用法:")
        print("  python obsidian_kb.py health           # 健康检查")
        print("  python obsidian_kb.py create 标题 内容 [tags...] [folder]")
        print("  python obsidian_kb.py search 查询 [limit]")
        print("  python obsidian_kb.py list            # 列出笔记")
        print("  python obsidian_kb.py stats            # 统计信息")
        return
    
    command = sys.argv[1].lower()
    kb = ObsidianKB()
    
    if command == "health":
        health_check_cli()
    elif command == "create":
        create_note_cli()
    elif command == "search":
        search_notes_cli()
    elif command == "list":
        list_notes_cli()
    elif command == "stats":
        stats = kb.get_stats()
        if stats.get("status") == "success":
            print(f"📊 统计信息:")
            print(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            print(f"❌ 获取统计信息失败: {stats.get('message')}")
    else:
        print(f"❌ 未知命令: {command}")


if __name__ == "__main__":
    main()