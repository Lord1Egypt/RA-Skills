#!/usr/bin/env python3
"""
上下文分析器 - 理解当前状态和环境
"""
import json
import os
from datetime import datetime, time
from pathlib import Path

class ContextAnalyzer:
    def __init__(self, base_path=None):
        self.base_path = base_path or Path(__file__).parent.parent.parent
        self.memory_path = self.base_path / "memory"
        self.learning_path = self.memory_path / "learning"
        
    def get_current_context(self):
        """获取当前上下文"""
        context = {
            "timestamp": datetime.now().isoformat(),
            "time_slot": self._get_time_slot(),
            "day_of_week": datetime.now().strftime("%A"),
            "is_weekday": datetime.now().weekday() < 5,
            "pending_tasks": self._get_pending_tasks(),
            "recent_interactions": self._get_recent_interactions(),
            "active_projects": self._get_active_projects(),
            "market_status": self._get_market_status(),
            "content_status": self._get_content_status()
        }
        return context
    
    def _get_time_slot(self):
        """获取当前时间段"""
        now = datetime.now().time()
        if time(6, 0) <= now < time(9, 0):
            return "morning_startup"
        elif time(9, 0) <= now < time(11, 30):
            return "morning_trading"
        elif time(11, 30) <= now < time(13, 0):
            return "lunch_break"
        elif time(13, 0) <= now < time(15, 0):
            return "afternoon_trading"
        elif time(15, 0) <= now < time(17, 0):
            return "content_publish_window"
        elif time(17, 0) <= now < time(22, 0):
            return "evening_routine"
        else:
            return "night_quiet"
    
    def _get_pending_tasks(self):
        """获取待完成任务"""
        tasks = []
        memory_file = self.memory_path / "MEMORY.md"
        if memory_file.exists():
            content = memory_file.read_text(encoding="utf-8")
            # 简单提取待办事项
            import re
            todos = re.findall(r'- \[ \] (.+)', content)
            tasks.extend(todos)
        return tasks
    
    def _get_recent_interactions(self):
        """获取最近交互记录"""
        interactions_file = self.learning_path / "interactions.json"
        if interactions_file.exists():
            with open(interactions_file, 'r', encoding='utf-8') as f:
                interactions = json.load(f)
                return interactions[-5:] if interactions else []
        return []
    
    def _get_active_projects(self):
        """获取活跃项目"""
        projects = []
        # 检查小红书项目
        xhs_strategy = self.memory_path.parent / "planning" / "xiaohongshu-strategy.md"
        if xhs_strategy.exists():
            projects.append({
                "name": "小红书自我养活",
                "status": "active",
                "priority": "high"
            })
        # 检查股票项目
        instreet_info = self.memory_path / "MEMORY.md"
        if instreet_info.exists():
            projects.append({
                "name": "InStreet竞技场",
                "status": "active",
                "priority": "medium"
            })
        return projects
    
    def _get_market_status(self):
        """获取市场状态"""
        now = datetime.now()
        weekday = now.weekday()
        current_time = now.time()
        
        if weekday >= 5:  # 周末
            return {"status": "closed", "reason": "weekend"}
        
        if time(9, 30) <= current_time <= time(11, 30):
            return {"status": "morning_session"}
        elif time(13, 0) <= current_time <= time(15, 0):
            return {"status": "afternoon_session"}
        else:
            return {"status": "closed", "reason": "outside_trading_hours"}
    
    def _get_content_status(self):
        """获取内容发布状态"""
        content_dir = self.base_path / "content"
        if not content_dir.exists():
            return {"pending_posts": 0, "last_post": None}
        
        # 检查待发布内容
        pending = list(content_dir.glob("xiaohongshu_post*.md"))
        
        # 检查最近发布记录
        memory_file = self.memory_path / "MEMORY.md"
        last_post = None
        if memory_file.exists():
            content = memory_file.read_text(encoding="utf-8")
            import re
            match = re.search(r'第二篇.*?(\d{4}-\d{2}-\d{2})', content)
            if match:
                last_post = match.group(1)
        
        return {
            "pending_posts": len(pending),
            "last_post": last_post
        }
    
    def analyze(self):
        """分析并返回上下文摘要"""
        context = self.get_current_context()
        
        summary = {
            "time_context": f"当前是{context['time_slot']}时段，{context['day_of_week']}",
            "market": context['market_status'],
            "tasks": f"待完成任务: {len(context['pending_tasks'])}个",
            "projects": [p['name'] for p in context['active_projects']],
            "content": context['content_status'],
            "recent_learning": len(context['recent_interactions'])
        }
        
        return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="上下文分析器")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()
    
    analyzer = ContextAnalyzer()
    if args.json:
        print(json.dumps(analyzer.get_current_context(), ensure_ascii=False, indent=2))
    else:
        summary = analyzer.analyze()
        print("=== 上下文分析 ===")
        for key, value in summary.items():
            print(f"{key}: {value}")
