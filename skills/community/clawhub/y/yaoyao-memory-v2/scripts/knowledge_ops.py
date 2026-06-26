#!/usr/bin/env python3
"""知识运营系统
参考 xiaoyi-claw-omega-final 的知识治理体系
"""
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Set
from pathlib import Path
from enum import Enum

class KnowledgeLevel(Enum):
    """知识等级"""
    CORE = "core"           # 核心知识（永久保留）
    IMPORTANT = "important"  # 重要知识（30天+）
    NORMAL = "normal"       # 普通知识（7-30天）
    TEMPORARY = "temporary"  # 临时知识（<7天）

class KnowledgeCategory(Enum):
    """知识分类"""
    USER = "user"           # 用户相关
    TECHNICAL = "technical"  # 技术相关
    PRODUCT = "product"      # 产品相关
    PROJECT = "project"      # 项目相关
    DECISION = "decision"   # 决策相关
    ERROR = "error"          # 错误/教训
    LEARNING = "learning"   # 学习相关

class KnowledgeEntry:
    """知识条目"""
    
    def __init__(
        self,
        title: str,
        content: str,
        category: KnowledgeCategory,
        level: KnowledgeLevel = KnowledgeLevel.NORMAL,
        tags: Optional[Set[str]] = None,
        source: str = "memory"
    ):
        self.id = self._generate_id(title)
        self.title = title
        self.content = content
        self.category = category
        self.level = level
        self.tags = tags or set()
        self.source = source
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.access_count = 0
        self.last_accessed = None
        self.confidence = 1.0  # 置信度 0-1
    
    def _generate_id(self, title: str) -> str:
        """生成唯一ID"""
        import hashlib
        return hashlib.md5(f"{title}{datetime.now().isoformat()}".encode()).hexdigest()[:12]
    
    def access(self):
        """记录访问"""
        self.access_count += 1
        self.last_accessed = datetime.now().isoformat()
    
    def update_content(self, content: str):
        """更新内容"""
        self.content = content
        self.updated_at = datetime.now().isoformat()
    
    def promote(self):
        """提升知识等级"""
        if self.level == KnowledgeLevel.TEMPORARY:
            self.level = KnowledgeLevel.NORMAL
        elif self.level == KnowledgeLevel.NORMAL:
            self.level = KnowledgeLevel.IMPORTANT
        elif self.level == KnowledgeLevel.IMPORTANT:
            self.level = KnowledgeLevel.CORE
        self.updated_at = datetime.now().isoformat()
    
    def demote(self):
        """降低知识等级"""
        if self.level == KnowledgeLevel.CORE:
            self.level = KnowledgeLevel.IMPORTANT
        elif self.level == KnowledgeLevel.IMPORTANT:
            self.level = KnowledgeLevel.NORMAL
        elif self.level == KnowledgeLevel.NORMAL:
            self.level = KnowledgeLevel.TEMPORARY
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category.value,
            "level": self.level.value,
            "tags": list(self.tags),
            "source": self.source,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed,
            "confidence": self.confidence
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "KnowledgeEntry":
        entry = cls(
            title=data["title"],
            content=data["content"],
            category=KnowledgeCategory(data["category"]),
            level=KnowledgeLevel(data["level"]),
            tags=set(data.get("tags", [])),
            source=data.get("source", "memory")
        )
        entry.id = data["id"]
        entry.created_at = data["created_at"]
        entry.updated_at = data["updated_at"]
        entry.access_count = data.get("access_count", 0)
        entry.last_accessed = data.get("last_accessed")
        entry.confidence = data.get("confidence", 1.0)
        return entry


class KnowledgeBase:
    """知识库"""
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or (Path.home() / ".openclaw" / "workspace" / "memory" / "knowledge_base.json")
        self.entries: Dict[str, KnowledgeEntry] = {}
        self.load()
    
    def load(self):
        """从磁盘加载"""
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                self.entries = {
                    eid: KnowledgeEntry.from_dict(e)
                    for eid, e in data.get("entries", {}).items()
                }
            except Exception as ex:
                print(f"加载知识库失败: {ex}")
                self.entries = {}
    
    def save(self):
        """保存到磁盘"""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "entries": {eid: e.to_dict() for eid, e in self.entries.items()}
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def add(self, entry: KnowledgeEntry) -> str:
        """添加知识条目"""
        self.entries[entry.id] = entry
        self.save()
        return entry.id
    
    def get(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """获取知识条目"""
        entry = self.entries.get(entry_id)
        if entry:
            entry.access()
            self.save()
        return entry
    
    def search(self, query: str, category: Optional[KnowledgeCategory] = None,
                level: Optional[KnowledgeLevel] = None) -> List[KnowledgeEntry]:
        """搜索知识"""
        results = []
        query_lower = query.lower()
        
        for entry in self.entries.values():
            # 分类过滤
            if category and entry.category != category:
                continue
            
            # 等级过滤
            if level and entry.level != level:
                continue
            
            # 关键词匹配
            if (query_lower in entry.title.lower() or 
                query_lower in entry.content.lower() or
                any(query_lower in tag.lower() for tag in entry.tags)):
                results.append(entry)
        
        # 按访问次数和置信度排序
        results.sort(key=lambda e: (e.access_count, e.confidence), reverse=True)
        return results
    
    def get_by_category(self, category: KnowledgeCategory) -> List[KnowledgeEntry]:
        """按分类获取"""
        return [e for e in self.entries.values() if e.category == category]
    
    def get_by_level(self, level: KnowledgeLevel) -> List[KnowledgeEntry]:
        """按等级获取"""
        return [e for e in self.entries.values() if e.level == level]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        by_category = {}
        by_level = {}
        
        for entry in self.entries.values():
            cat = entry.category.value
            lvl = entry.level.value
            by_category[cat] = by_category.get(cat, 0) + 1
            by_level[lvl] = by_level.get(lvl, 0) + 1
        
        return {
            "total": len(self.entries),
            "by_category": by_category,
            "by_level": by_level,
            "total_access": sum(e.access_count for e in self.entries.values())
        }
    
    def format_report(self) -> str:
        """格式化报告"""
        stats = self.get_stats()
        
        report = "📚 知识库报告\n"
        report += "=" * 40 + "\n\n"
        
        report += f"📊 总条目: {stats['total']}\n"
        report += f"📈 总访问: {stats['total_access']}\n\n"
        
        report += "📁 按分类:\n"
        for cat, count in stats["by_category"].items():
            report += f"  • {cat}: {count}\n"
        
        report += "\n📊 按等级:\n"
        for lvl, count in stats["by_level"].items():
            report += f"  • {lvl}: {count}\n"
        
        return report


class KnowledgeOperations:
    """知识运营操作"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
    
    def auto_classify(self, text: str) -> KnowledgeCategory:
        """自动分类"""
        text_lower = text.lower()
        
        # 分类关键词
        category_keywords = {
            KnowledgeCategory.USER: ["用户", "偏好", "习惯", "喜欢", "不喜欢", "user", "preference"],
            KnowledgeCategory.TECHNICAL: ["技术", "架构", "代码", "api", "系统", "technical", "code"],
            KnowledgeCategory.PRODUCT: ["产品", "功能", "设计", "ui", "ux", "product", "feature"],
            KnowledgeCategory.PROJECT: ["项目", "里程碑", "进度", "project", "milestone"],
            KnowledgeCategory.DECISION: ["决策", "决定", "采用", "选择", "decision", "choose"],
            KnowledgeCategory.ERROR: ["错误", "bug", "问题", "失败", "error", "bug", "issue"],
            KnowledgeCategory.LEARNING: ["学习", "掌握", "了解", "learning", "study"],
        }
        
        for cat, keywords in category_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return cat
        
        return KnowledgeCategory.NORMAL
    
    def auto_tag(self, text: str) -> Set[str]:
        """自动打标签"""
        tags = set()
        
        # 提取 #标签
        tags.update(re.findall(r'#(\w+)', text))
        
        # 提取 @人名
        tags.update(re.findall(r'@(\w+)', text))
        
        # 提取时间表达式
        time_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # 2026-04-07
            r'\d{4}/\d{2}/\d{2}',  # 2026/04/07
        ]
        for pattern in time_patterns:
            tags.update(re.findall(pattern, text))
        
        return tags
    
    def promote_if_important(self, entry_id: str, threshold: int = 5) -> bool:
        """如果访问次数足够多则提升等级"""
        entry = self.kb.get(entry_id)
        if not entry:
            return False
        
        if entry.access_count >= threshold:
            entry.promote()
            self.kb.save()
            return True
        return False


if __name__ == "__main__":
    # 测试
    print("=== 知识库测试 ===")
    
    kb = KnowledgeBase()
    
    # 添加知识条目
    entry1 = KnowledgeEntry(
        title="用户偏好中文",
        content="用户喜欢使用中文交流",
        category=KnowledgeCategory.USER,
        level=KnowledgeLevel.NORMAL,
        tags={"用户", "偏好"}
    )
    kb.add(entry1)
    
    entry2 = KnowledgeEntry(
        title="技术架构决策",
        content="采用四层记忆架构",
        category=KnowledgeCategory.DECISION,
        level=KnowledgeLevel.IMPORTANT,
        tags={"架构", "决策"}
    )
    kb.add(entry2)
    
    print(f"添加了 {len(kb.entries)} 条知识")
    
    # 搜索
    results = kb.search("用户")
    print(f"\n搜索'用户'找到 {len(results)} 条:")
    for r in results:
        print(f"  - {r.title} ({r.category.value})")
    
    # 报告
    print("\n" + kb.format_report())
    
    # 知识运营
    ops = KnowledgeOperations(kb)
    category = ops.auto_classify("用户喜欢使用中文")
    print(f"\n自动分类: {category.value}")
    
    tags = ops.auto_tag("用户偏好 #中文 @摇摇")
    print(f"自动标签: {tags}")
