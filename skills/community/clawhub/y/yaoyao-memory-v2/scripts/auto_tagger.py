#!/usr/bin/env python3
"""
自动标签模块 - v1.0.0
为记忆自动生成标签

功能：
1. 基于内容分析自动打标签
2. 支持多维度标签（类型/领域/优先级）
3. 智能推荐标签
4. 批量打标签
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import Counter

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"

# 标签词典
TAG_DICTIONARY = {
    "技术": ["代码", "API", "Python", "系统", "架构", "技术", "实现", "配置"],
    "产品": ["功能", "需求", "用户", "体验", "界面", "产品", "设计"],
    "决策": ["决定", "选择", "采用", "决策", "拍板", "敲定"],
    "错误": ["错误", "失败", "bug", "异常", "问题", "修复", "踩坑"],
    "学习": ["学会", "理解", "掌握", "学习", "了解", "熟悉"],
    "项目": ["项目", "开发", "任务", "进度", "里程碑"],
    "用户": ["用户", "偏好", "喜欢", "习惯", "不喜欢"],
    "AI": ["AI", "模型", "LLM", "Claude", "GPT", "Agent"],
    "工具": ["工具", "脚本", "命令", "CLI"],
}

# 重要性关键词
IMPORTANCE_KEYWORDS = {
    "Critical": ["核心", "关键", "致命", "最高"],
    "High": ["重要", "优先", "紧急", "关键"],
    "Low": ["临时", "暂定", "可能", "或许"],
}

class AutoTagger:
    """自动标签器"""
    
    def __init__(self):
        self.memory_dir = MEMORY_DIR
    
    def extract_tags(self, content: str, max_tags: int = 5) -> List[str]:
        """从内容中提取标签"""
        tags = set()
        content_lower = content.lower()
        
        # 匹配词典
        for tag, keywords in TAG_DICTIONARY.items():
            for kw in keywords:
                if kw in content_lower:
                    tags.add(tag)
                    break
        
        # 提取 #标签
        hash_tags = re.findall(r'#(\w+)', content)
        tags.update(hash_tags)
        
        # 提取英文单词标签（3-15字符）
        english_words = re.findall(r'\b([A-Z][a-z]{2,14})\b', content)
        for word in english_words:
            if word.lower() not in {"the", "and", "for", "with", "from", "this", "that"}:
                tags.add(word)
        
        # 限制数量
        return list(tags)[:max_tags]
    
    def detect_importance(self, content: str) -> str:
        """检测重要性等级"""
        for level, keywords in IMPORTANCE_KEYWORDS.items():
            for kw in keywords:
                if kw in content:
                    return level
        return "Normal"
    
    def tag_memory(self, filename: str) -> Dict:
        """为单条记忆打标签"""
        file_path = self.memory_dir / filename
        
        if not file_path.exists():
            return {"filename": filename, "error": "文件不存在"}
        
        try:
            content = file_path.read_text(encoding="utf-8")
            tags = self.extract_tags(content)
            importance = self.detect_importance(content)
            
            return {
                "filename": filename,
                "tags": tags,
                "importance": importance,
                "tag_count": len(tags)
            }
        except Exception as e:
            return {"filename": filename, "error": str(e)}
    
    def tag_all(self) -> List[Dict]:
        """为所有记忆打标签"""
        results = []
        
        for f in self.memory_dir.glob("*.md"):
            if f.name.startswith(".") or "合并版" in f.name:
                continue
            
            result = self.tag_memory(f.name)
            results.append(result)
        
        return results
    
    def apply_tags(self, filename: str, tags: List[str]) -> bool:
        """应用标签到记忆文件"""
        file_path = self.memory_dir / filename
        
        if not file_path.exists():
            return False
        
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # 在文件开头添加标签
            tag_line = " ".join(f"#{t}" for t in tags)
            new_content = f"{tag_line}\n\n{content}"
            
            file_path.write_text(new_content, encoding="utf-8")
            return True
        except:
            return False
    
    def report(self) -> str:
        """生成标签报告"""
        results = self.tag_all()
        
        if not results:
            return "📋 自动标签报告：无记忆数据"
        
        tag_counter = Counter()
        importance_counter = Counter()
        
        for r in results:
            if "error" in r:
                continue
            for tag in r.get("tags", []):
                tag_counter[tag] += 1
            importance_counter[r.get("importance", "Normal")] += 1
        
        lines = [
            "📋 自动标签报告",
            "=" * 40,
            f"总记忆: {len(results)}",
            "",
            "🏷️ 标签分布:",
        ]
        
        for tag, count in tag_counter.most_common(10):
            lines.append(f"  #{tag}: {count}")
        
        lines.extend([
            "",
            "📊 重要性分布:",
        ])
        
        for level, count in importance_counter.items():
            lines.append(f"  {level}: {count}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    tagger = AutoTagger()
    print(tagger.report())
