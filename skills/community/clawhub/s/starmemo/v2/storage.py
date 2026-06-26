#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
starmemo v2.0 - 存储层
结构化记忆 + 知识库 + 索引系统
"""
import os
import json
import hashlib
from datetime import datetime, date
from pathlib import Path


class MemoryStorage:
    """分层存储系统"""
    
    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.base_dir = Path(base_dir)
        self.memory_dir = self.base_dir / "memory"
        self.daily_dir = self.memory_dir / "daily"
        self.knowledge_dir = self.memory_dir / "knowledge"
        self.archive_dir = self.memory_dir / "archive"
        
        # 索引文件
        self.daily_index = self.memory_dir / "daily-index.md"
        self.knowledge_index = self.memory_dir / "knowledge-index.md"
        
        self._init_dirs()
        self._hash_cache = set()  # 去重缓存
    
    def _init_dirs(self):
        """初始化目录结构"""
        for d in [self.memory_dir, self.daily_dir, self.knowledge_dir, self.archive_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        # 初始化索引文件
        if not self.daily_index.exists():
            self.daily_index.write_text("# 记忆索引\n\n", encoding="utf-8")
        if not self.knowledge_index.exists():
            self.knowledge_index.write_text("# 知识库索引\n\n", encoding="utf-8")
    
    def today_file(self) -> Path:
        """获取今日记忆文件"""
        return self.daily_dir / f"{date.today()}.md"
    
    # ========== 每日记忆 ==========
    
    def save_daily(self, cause: str, change: str, todo: str = "", topic: str = "") -> bool:
        """
        保存结构化每日记忆
        
        Args:
            cause: 原因/背景
            change: 做了什么/改了什么
            todo: 待办/后续（可选）
            topic: 主题（可选，自动生成）
        
        Returns:
            bool: 是否保存成功
        """
        content = f"{cause}{change}{todo}"
        h = hashlib.md5(content.encode()).hexdigest()[:8]
        if h in self._hash_cache:
            return False
        self._hash_cache.add(h)
        
        # 自动生成主题
        if not topic:
            topic = self._extract_topic(cause) or "日常记录"
        
        # 格式化时间
        ts = datetime.now().strftime("%H:%M")
        
        # 写入记忆
        entry = f"\n## [{ts}] {topic}\n"
        entry += f"- **因**：{cause}\n"
        entry += f"- **改**：{change}\n"
        if todo:
            entry += f"- **待**：{todo}\n"
        
        today_file = self.today_file()
        if not today_file.exists():
            today_file.write_text(f"# 记忆 - {date.today()}\n\n", encoding="utf-8")
        
        with open(today_file, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        
        # 更新索引
        self._update_daily_index(topic, date.today())
        
        return True
    
    def _extract_topic(self, text: str) -> str:
        """从文本提取主题（简单规则）"""
        # 关键词映射
        topic_keywords = {
            "技能": ["技能", "skill", "安装", "配置"],
            "开发": ["开发", "代码", "编程", "实现", "功能"],
            "调试": ["调试", "错误", "问题", "bug", "修复"],
            "学习": ["学习", "了解", "研究", "探索"],
            "决策": ["决定", "选择", "方案", "采用"],
            "任务": ["任务", "待办", "完成", "进度"],
        }
        
        text_lower = text.lower()
        for topic, keywords in topic_keywords.items():
            for kw in keywords:
                if kw in text_lower:
                    return topic
        
        return "日常记录"
    
    def _update_daily_index(self, topic: str, day: date):
        """更新每日记忆索引"""
        index_content = self.daily_index.read_text(encoding="utf-8")
        
        # 检查是否已存在
        entry = f"- {topic} → daily/{day}.md"
        if entry in index_content:
            return
        
        # 添加新条目
        lines = index_content.strip().split("\n")
        
        # 查找或创建日期分区
        date_header = f"## {day.strftime('%Y-%m-%d')}"
        
        if date_header in index_content:
            # 在该日期分区下添加
            new_lines = []
            added = False
            for line in lines:
                new_lines.append(line)
                if line == date_header and not added:
                    new_lines.append(entry)
                    added = True
            index_content = "\n".join(new_lines)
        else:
            # 创建新的日期分区
            index_content = index_content.strip() + f"\n\n{date_header}\n{entry}\n"
        
        self.daily_index.write_text(index_content, encoding="utf-8")
    
    def search_daily(self, keyword: str, limit: int = 5) -> list:
        """搜索每日记忆"""
        results = []
        
        # 从今天开始搜索
        for day in sorted(self.daily_dir.glob("*.md"), reverse=True):
            if len(results) >= limit:
                break
            
            content = day.read_text(encoding="utf-8")
            if keyword.lower() in content.lower():
                # 提取匹配的段落
                for block in content.split("## ["):
                    if keyword.lower() in block.lower():
                        results.append({
                            "file": day.name,
                            "content": "## [" + block[:300]
                        })
                        if len(results) >= limit:
                            break
        
        return results
    
    # ========== 知识库 ==========
    
    def save_knowledge(self, key: str, content: str, source: str = "对话提取"):
        """
        保存知识点到知识库
        
        Args:
            key: 知识点标题
            content: 知识内容
            source: 来源
        """
        # 清理标题作为文件名
        safe_key = "".join(c for c in key if c.isalnum() or c in " -_").strip()
        if not safe_key:
            safe_key = hashlib.md5(key.encode()).hexdigest()[:8]
        
        file_path = self.knowledge_dir / f"{safe_key}.md"
        
        # 写入知识
        entry = f"# {key}\n\n"
        entry += f"> 来源：{source}\n"
        entry += f"> 时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        entry += content
        
        file_path.write_text(entry, encoding="utf-8")
        
        # 更新知识索引
        self._update_knowledge_index(key, safe_key)
        
        return str(file_path)
    
    def _update_knowledge_index(self, key: str, safe_key: str):
        """更新知识库索引"""
        index_content = self.knowledge_index.read_text(encoding="utf-8")
        
        entry = f"- {key} → knowledge/{safe_key}.md"
        if entry in index_content:
            return
        
        index_content = index_content.strip() + f"\n{entry}\n"
        self.knowledge_index.write_text(index_content, encoding="utf-8")
    
    def search_knowledge(self, keyword: str, limit: int = 5) -> list:
        """搜索知识库"""
        results = []
        
        for f in self.knowledge_dir.glob("*.md"):
            if len(results) >= limit:
                break
            
            content = f.read_text(encoding="utf-8")
            if keyword.lower() in content.lower():
                results.append({
                    "file": f.name,
                    "title": f.stem,
                    "content": content[:500]
                })
        
        return results
    
    # ========== 归档 ==========
    
    def rotate(self, archive_days: int = 3):
        """
        归档过期记忆
        
        Args:
            archive_days: 超过多少天归档
        """
        today = date.today()
        
        for f in self.daily_dir.glob("*.md"):
            try:
                day_str = f.stem  # YYYY-MM-DD
                file_date = datetime.strptime(day_str, "%Y-%m-%d").date()
                delta = (today - file_date).days
                
                if delta >= archive_days:
                    # 移动到归档
                    archive_path = self.archive_dir / f.name
                    f.rename(archive_path)
                    print(f"📦 已归档: {f.name}")
            except Exception as e:
                print(f"⚠️ 归档失败 {f.name}: {e}")
    
    # ========== 读取 ==========
    
    def get_today(self) -> str:
        """获取今日记忆"""
        today_file = self.today_file()
        if today_file.exists():
            return today_file.read_text(encoding="utf-8")
        return "今日暂无记忆"
    
    def get_yesterday(self) -> str:
        """获取昨日记忆"""
        yesterday = date.today()
        from datetime import timedelta
        yesterday = yesterday - timedelta(days=1)
        
        y_file = self.daily_dir / f"{yesterday}.md"
        if y_file.exists():
            return y_file.read_text(encoding="utf-8")
        return "昨日暂无记忆"
    
    def list_files(self) -> dict:
        """列出所有记忆文件"""
        result = {
            "daily": [],
            "knowledge": [],
            "archive": []
        }
        
        for f in sorted(self.daily_dir.glob("*.md"), reverse=True):
            result["daily"].append({
                "name": f.name,
                "size": f.stat().st_size
            })
        
        for f in sorted(self.knowledge_dir.glob("*.md")):
            result["knowledge"].append({
                "name": f.name,
                "size": f.stat().st_size
            })
        
        for f in sorted(self.archive_dir.glob("*.md"), reverse=True)[:10]:
            result["archive"].append({
                "name": f.name,
                "size": f.stat().st_size
            })
        
        return result
