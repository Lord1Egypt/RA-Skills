#!/usr/bin/env python3
"""
tag_manager.py - 智能标签管理器
自动建议/合并/清理标签
"""
import json
import sqlite3
import re
from collections import Counter
from pathlib import Path
from datetime import datetime


MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
MEMORY_DB = MEMORY_DIR / "memory.db"


class TagManager:
    """标签管理器"""
    
    def __init__(self):
        self.db_path = MEMORY_DB
    
    def _connect(self):
        return sqlite3.connect(self.db_path)
    
    def get_all_tags(self) -> Counter:
        """获取所有标签及出现频次"""
        conn = self._connect()
        cursor = conn.execute("SELECT tags FROM memories WHERE tags IS NOT NULL")
        tags = []
        for row in cursor:
            if row[0]:
                try:
                    tag_list = json.loads(row[0])
                    if isinstance(tag_list, list):
                        tags.extend(tag_list)
                except:
                    pass
        conn.close()
        return Counter(tags)
    
    def get_tag_stats(self) -> dict:
        """获取标签统计"""
        all_tags = self.get_all_tags()
        
        total_memories_with_tags = 0
        conn = self._connect()
        cursor = conn.execute("SELECT COUNT(*) FROM memories WHERE tags IS NOT NULL AND tags != '[]'")
        total_memories_with_tags = cursor.fetchone()[0]
        conn.close()
        
        return {
            "total_tags": len(all_tags),
            "total_tag_usages": sum(all_tags.values()),
            "unique_tags": len(set(all_tags)),
            "avg_tags_per_memory": total_tags / total_memories_with_tags if total_memories_with_tags > 0 else 0,
            "top_tags": all_tags.most_common(20)
        }
    
    def suggest_tags_for_memory(self, content: str) -> list:
        """为记忆内容建议标签"""
        suggestions = []
        
        # 关键词模式
        patterns = {
            "技术": ["python", "代码", "api", "bug", "开发", "编程", "脚本", "编程"],
            "项目": ["项目", "开发", "功能", "模块", "设计", "实现"],
            "学习": ["学习", "研究", "分析", "探索", "理解"],
            "工作": ["工作", "任务", "todo", "计划", "安排"],
            "生活": ["生活", "休息", "运动", "饮食", "睡眠"],
            "健康": ["健康", "身体", "锻炼", "运动"],
            "财务": ["钱", "花销", "支出", "收入", "预算"],
            "人际关系": ["朋友", "家人", "同事", "联系", "社交"],
            "创意": ["想法", "创意", "灵感", "构思", "设计"],
            "问题解决": ["问题", "解决", "修复", "debug", "错误"]
        }
        
        content_lower = content.lower()
        for tag, keywords in patterns.items():
            if any(kw in content_lower for kw in keywords):
                suggestions.append(tag)
        
        return list(set(suggestions))
    
    def add_tag_to_memories(self, tag: str, memory_ids: list = None, type_filter: str = None):
        """为记忆添加标签"""
        conn = self._connect()
        
        if memory_ids:
            placeholders = ",".join("?" * len(memory_ids))
            cursor = conn.execute(f"SELECT id, tags FROM memories WHERE id IN ({placeholders})", memory_ids)
        elif type_filter:
            cursor = conn.execute("SELECT id, tags FROM memories WHERE type = ?", (type_filter,))
        else:
            cursor = conn.execute("SELECT id, tags FROM memories")
        
        updated = 0
        for row in cursor:
            current_tags = []
            if row[1]:
                try:
                    current_tags = json.loads(row[1])
                except:
                    current_tags = []
            
            if tag not in current_tags:
                current_tags.append(tag)
                conn.execute(
                    "UPDATE memories SET tags = ?, updated_at = ? WHERE id = ?",
                    (json.dumps(current_tags), datetime.now().isoformat(), row[0])
                )
                updated += 1
        
        conn.commit()
        conn.close()
        return updated
    
    def remove_tag_from_memories(self, tag: str, memory_ids: list = None):
        """从记忆移除标签"""
        conn = self._connect()
        
        if memory_ids:
            placeholders = ",".join("?" * len(memory_ids))
            cursor = conn.execute(f"SELECT id, tags FROM memories WHERE id IN ({placeholders})", memory_ids)
        else:
            cursor = conn.execute("SELECT id, tags FROM memories WHERE tags IS NOT NULL")
        
        updated = 0
        for row in cursor:
            if row[1]:
                try:
                    current_tags = json.loads(row[1])
                    if tag in current_tags:
                        current_tags.remove(tag)
                        conn.execute(
                            "UPDATE memories SET tags = ?, updated_at = ? WHERE id = ?",
                            (json.dumps(current_tags), datetime.now().isoformat(), row[0])
                        )
                        updated += 1
                except:
                    pass
        
        conn.commit()
        conn.close()
        return updated
    
    def merge_tags(self, source_tag: str, target_tag: str):
        """合并标签（将source_tag合并到target_tag）"""
        # 先添加新标签
        added = self.add_tag_to_memories(target_tag)
        # 再删除旧标签
        removed = self.remove_tag_from_memories(source_tag)
        return {"added": added, "removed": removed}
    
    def cleanup_orphan_tags(self) -> dict:
        """清理孤立标签（删除从未使用的标签定义）"""
        # 这个功能取决于标签存储方式
        return {"cleaned": 0}
    
    def auto_tag_memories(self, type_filter: str = None, dry_run: bool = True) -> dict:
        """自动为记忆添加标签"""
        conn = self._connect()
        
        if type_filter:
            cursor = conn.execute(
                "SELECT id, content, tags FROM memories WHERE type = ?",
                (type_filter,)
            )
        else:
            cursor = conn.execute("SELECT id, content, tags FROM memories")
        
        results = {
            "total": 0,
            "tagged": 0,
            "suggestions": []
        }
        
        for row in cursor:
            results["total"] += 1
            memory_id, content, current_tags = row
            
            # 获取建议标签
            suggestions = self.suggest_tags_for_memory(content)
            
            # 获取当前标签
            existing = []
            if current_tags:
                try:
                    existing = json.loads(current_tags)
                except:
                    existing = []
            
            # 找出新增标签
            new_tags = [t for t in suggestions if t not in existing]
            
            if new_tags and not dry_run:
                all_tags = existing + new_tags
                conn.execute(
                    "UPDATE memories SET tags = ?, updated_at = ? WHERE id = ?",
                    (json.dumps(all_tags), datetime.now().isoformat(), memory_id)
                )
                results["tagged"] += 1
            
            if new_tags:
                results["suggestions"].append({
                    "id": memory_id,
                    "new_tags": new_tags,
                    "preview": content[:50]
                })
        
        conn.commit()
        conn.close()
        return results


def main():
    import sys
    
    print("🏷️ 智能标签管理器")
    print("=" * 40)
    
    manager = TagManager()
    
    if len(sys.argv) < 2:
        print("""用法:
    tag_manager.py stats              # 标签统计
    tag_manager.py suggest <内容>     # 建议标签
    tag_manager.py add <标签> [ids]   # 添加标签
    tag_manager.py remove <标签> [ids]# 移除标签
    tag_manager.py merge <源> <目标>  # 合并标签
    tag_manager.py auto_tag [类型]    # 自动标签(仅预览)
    tag_manager.py auto_tag_apply     # 自动标签(执行)""")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "stats":
        stats = manager.get_tag_stats()
        print(f"\n📊 标签统计:")
        print(f"   总标签数: {stats['total_tags']}")
        print(f"   独立标签: {stats['unique_tags']}")
        print(f"   平均每条记忆: {stats['avg_tags_per_memory']:.1f} 个标签")
        print(f"\n🏷️ Top 10 标签:")
        for tag, count in stats["top_tags"][:10]:
            print(f"   {tag}: {count}")
    
    elif cmd == "suggest":
        if len(sys.argv) < 3:
            print("❌ 请提供内容")
            return
        content = sys.argv[2]
        suggestions = manager.suggest_tags_for_memory(content)
        print(f"建议标签: {', '.join(suggestions) if suggestions else '无建议'}")
    
    elif cmd == "add":
        if len(sys.argv) < 3:
            print("❌ 请指定标签")
            return
        tag = sys.argv[2]
        ids = sys.argv[3].split(",") if len(sys.argv) > 3 else None
        count = manager.add_tag_to_memories(tag, ids)
        print(f"✅ 已为 {count} 条记忆添加标签 '{tag}'")
    
    elif cmd == "remove":
        if len(sys.argv) < 3:
            print("❌ 请指定标签")
            return
        tag = sys.argv[2]
        ids = sys.argv[3].split(",") if len(sys.argv) > 3 else None
        count = manager.remove_tag_from_memories(tag, ids)
        print(f"✅ 已从 {count} 条记忆移除标签 '{tag}'")
    
    elif cmd == "merge":
        if len(sys.argv) < 4:
            print("❌ 请指定源标签和目标标签")
            return
        result = manager.merge_tags(sys.argv[2], sys.argv[3])
        print(f"✅ 合并完成: 添加 {result['added']}, 移除 {result['removed']}")
    
    elif cmd == "auto_tag":
        type_filter = sys.argv[2] if len(sys.argv) > 2 else None
        results = manager.auto_tag_memories(type_filter, dry_run=True)
        print(f"\n📋 自动标签预览 ({results['total']} 条记忆):")
        for s in results["suggestions"][:10]:
            print(f"   [{s['id']}] +{', '.join(s['new_tags'])}")
            print(f"       {s['preview']}...")
        print(f"\n✅ 可为 {results['tagged']} 条记忆添加标签")
    
    elif cmd == "auto_tag_apply":
        results = manager.auto_tag_memories(dry_run=False)
        print(f"✅ 已为 {results['tagged']} 条记忆添加标签")


if __name__ == "__main__":
    main()
