#!/usr/bin/env python3
"""
SRS - Security Research System v2.0
安全研究系统 - 含知识库日常review + 持续运行
"""

import os
import json
import time
import subprocess
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import threading

# ==================== 评估指标 ====================

class EvaluationCriteria:
    """评估判定是否进入系统的条件"""
    
    PRIORITY_RULES = {
        "external": {
            "cve_critical": 100,
            "security_incident": 95,
            "compliance_violation": 90,
            "public_disclosure": 85,
        },
        "scheduled": {
            "daily_report": 70,
            "weekly_summary": 65,
            "monthly_review": 60,
        },
        "proactive": {
            "threat_intel": 50,
            "research_opportunity": 45,
            "trend_analysis": 40,
        },
        "internal": {
            "infrastructure": 20,
            "tooling": 15,
            "documentation": 10,
        }
    }
    
    KNOWLEDGE_KEYWORDS = {
        # 高价值安全关键词
        "high": [
            "cve", "vulnerability", "exploit", "0day", "breach",
            "prompt injection", "jailbreak", "bypass",
            "supply chain", "backdoor", "malware"
        ],
        # 中价值关键词
        "medium": [
            "security", "threat", "attack", "risk", "compliance",
            "llm", "agent", "ai security", "mcp"
        ],
        # 低价值关键词
        "low": [
            "tutorial", "how to", "beginner", "introduction"
        ]
    }
    
    @classmethod
    def evaluate_task(cls, task_info: Dict) -> Dict:
        scores = {}
        
        priority_score = cls._evaluate_priority(task_info)
        scores["priority"] = priority_score
        
        relevance_score = cls._evaluate_relevance(task_info)
        scores["relevance"] = relevance_score
        
        time_score = cls._evaluate_timeliness(task_info)
        scores["timeliness"] = time_score
        
        value_score = cls._evaluate_value(task_info)
        scores["value"] = value_score
        
        total = (
            priority_score * 0.25 +
            relevance_score * 0.20 +
            time_score * 0.25 +
            value_score * 0.30
        )
        scores["total"] = total
        scores["admit"] = total >= 60
        
        return scores
    
    @classmethod
    def _evaluate_priority(cls, task_info: Dict) -> float:
        task_type = task_info.get("type", "proactive")
        task_name = task_info.get("name", "").lower()
        
        if task_type == "external":
            return 85
        
        for key, score in cls.PRIORITY_RULES["external"].items():
            if key in task_name:
                return score
        
        if task_type == "scheduled":
            for key, score in cls.PRIORITY_RULES["scheduled"].items():
                if key in task_name:
                    return score
        
        return 30
    
    @classmethod
    def _evaluate_relevance(cls, task_info: Dict) -> float:
        task_text = (task_info.get("name", "") + " " + 
                    task_info.get("description", "")).lower()
        
        for keyword in cls.KNOWLEDGE_KEYWORDS["high"]:
            if keyword in task_text:
                return 100.0
        
        for keyword in cls.KNOWLEDGE_KEYWORDS["medium"]:
            if keyword in task_text:
                return 60.0
        
        return 30.0
    
    @classmethod
    def _evaluate_timeliness(cls, task_info: Dict) -> float:
        urgency = task_info.get("urgency", "medium")
        mapping = {"critical": 100, "high": 80, "medium": 60, "low": 40}
        return mapping.get(urgency, 50)
    
    @classmethod
    def _evaluate_value(cls, task_info: Dict) -> float:
        score = 0
        if task_info.get("external_release"):
            score += 30
        if task_info.get("knowledge_contribution"):
            score += 20
        if task_info.get("risk_mitigation"):
            score += 25
        return score
    
    @classmethod
    def match_role(cls, task_info: Dict) -> str:
        task_text = (task_info.get("name", "") + " " + 
                    task_info.get("description", "")).lower()
        
        mapping = {
            "security_researcher": ["cve", "vulnerability", "threat", "exploit"],
            "domain_researcher": ["research", "analysis", "paper"],
            "knowledge_manager": ["document", "report", "knowledge"],
            "explorer": ["discover", "scan", "trend"],
            "secops": ["incident", "alert", "monitor"],
        }
        
        for role, keywords in mapping.items():
            for keyword in keywords:
                if keyword in task_text:
                    return role
        
        return "security_researcher"

# ==================== 知识库Review ====================

class KnowledgeBaseReviewer:
    """知识库日常Review - 提取安全任务"""
    
    def __init__(self, research_dir: str, todo_file: str):
        self.research_dir = research_dir
        self.todo_file = todo_file
        self.reviewed_file = os.path.join(os.path.dirname(todo_file), ".reviewed.json")
        self._load_reviewed()
        
    def _load_reviewed(self):
        """加载已review的文件"""
        if os.path.exists(self.reviewed_file):
            with open(self.reviewed_file, 'r') as f:
                self.reviewed = json.load(f)
        else:
            self.reviewed = {}
    
    def _save_reviewed(self):
        """保存已review记录"""
        with open(self.reviewed_file, 'w') as f:
            json.dump(self.reviewed, f)
    
    def scan_new_research(self) -> List[Dict]:
        """扫描新的研究成果"""
        new_tasks = []
        
        if not os.path.exists(self.research_dir):
            return new_tasks
        
        for item in os.listdir(self.research_dir):
            item_path = os.path.join(self.research_dir, item)
            
            # 跳过非目录
            if not os.path.isdir(item_path):
                continue
            
            # 检查是否已review (跳过时间检查，首次运行)
            # if item in self.reviewed:
            #     continue
            
            # 扫描目录内容
            files = []
            for root, dirs, filenames in os.walk(item_path):
                for f in filenames:
                    if f.endswith('.md'):
                        files.append(os.path.join(root, f))
            
            if files and len(files) > 0:
                # 提取关键词
                keywords = self._extract_keywords(files)
                
                task = {
                    "name": f"Review: {item}",
                    "description": f"Review {len(files)} files in {item}",
                    "type": "proactive",
                    "source": "knowledge_review",
                    "keywords": keywords,
                    "path": item_path,
                    "file_count": len(files)
                }
                
                # 评估 - 使用简化的评估逻辑
                priority_score = 50  # 提高基础优先级
                relevance_score = 80 if keywords else 40  # 有关键词给更高
                time_score = 70
                value_score = 50
                
                total = (priority_score * 0.25 + relevance_score * 0.20 + 
                        time_score * 0.25 + value_score * 0.30)
                admit = total >= 60
                
                evaluation = {
                    "total": total,
                    "admit": admit,
                    "priority": priority_score,
                    "relevance": relevance_score,
                    "timeliness": time_score,
                    "value": value_score
                }
                
                task["evaluation"] = evaluation
                task["role"] = EvaluationCriteria.match_role(task)
                
                if admit:
                    new_tasks.append(task)
                
                # 标记已review
                self.reviewed[item] = {
                    "time": datetime.now().isoformat(),
                    "file_count": len(files),
                    "admitted": admit
                }
        
        self._save_reviewed()
        return new_tasks
    
    def _extract_keywords(self, files: List[str]) -> List[str]:
        """从文件中提取关键词"""
        keywords = set()
        
        for f in files[:5]:  # 只检查前5个文件
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read().lower()
                    
                for kw in EvaluationCriteria.KNOWLEDGE_KEYWORDS["high"]:
                    if kw in content:
                        keywords.add(kw)
            except:
                pass
        
        return list(keywords)[:10]

# ==================== 待办管理器 ====================

class TodoManager:
    """待办管理 - 添加安全任务"""
    
    def __init__(self, todo_file: str):
        self.todo_file = todo_file
        self._ensure_file()
        
    def _ensure_file(self):
        if not os.path.exists(self.todo_file):
            os.makedirs(os.path.dirname(self.todo_file), exist_ok=True)
            with open(self.todo_file, 'w') as f:
                f.write("# SRS 待办列表\n\n")
    
    def add_task(self, task: Dict) -> bool:
        """添加任务到待办"""
        eval_data = task.get("evaluation", {})
        
        if not eval_data.get("admit", False):
            return False
        
        priority = "P0" if eval_data.get("total", 0) >= 80 else "P1"
        
        entry = f"""
### {priority}: {task['name']}

**评估分数**: {eval_data.get('total', 0):.1f}
**匹配角色**: {task.get('role', 'security_researcher')}
**来源**: 知识库Review
**关键词**: {', '.join(task.get('keywords', []))}

- [ ] {task['description']}
- 来源: {task.get('path', 'N/A')}

"""
        
        with open(self.todo_file, 'a') as f:
            f.write(entry)
        
        return True

# ==================== SRS 主系统 ====================

class SRS:
    """Security Research System - 安全研究系统"""
    
    def __init__(self):
        self.name = "SRS"
        self.version = "2.0"
        
        # 目录配置
        self.base_dir = os.path.expanduser("~/.openclaw/workspace/srs")
        self.research_dir = os.path.expanduser("~/ai-security/research")
        self.todo_file = os.path.expanduser("~/ai-security/TODO.md")
        
        # 组件
        self.reviewer = KnowledgeBaseReviewer(self.research_dir, self.todo_file)
        self.todo = TodoManager(self.todo_file)
        
    def daily_review(self) -> Dict:
        """日常知识库Review"""
        print("📚 开始日常知识库Review...")
        
        new_tasks = self.reviewer.scan_new_research()
        
        added = 0
        for task in new_tasks:
            if self.todo.add_task(task):
                added += 1
                print(f"  ✅ 添加任务: {task['name']} (分数: {task['evaluation']['total']:.1f})")
        
        return {
            "total_scanned": len(new_tasks),
            "tasks_added": added,
            "tasks": new_tasks
        }
    
    def status(self) -> Dict:
        return {
            "name": self.name,
            "version": self.version,
            "research_dir": self.research_dir,
            "todo_file": self.todo_file
        }

# ==================== CLI ====================

def main():
    import sys
    
    srs = SRS()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            print(json.dumps(srs.status(), indent=2, ensure_ascii=False))
            
        elif command == "review" or command == "daily":
            result = srs.daily_review()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif command == "eval" and len(sys.argv) > 2:
            task = {"name": sys.argv[2], "description": sys.argv[2], "type": "external"}
            result = EvaluationCriteria.evaluate_task(task)
            print(json.dumps(result, indent=2))
            
        elif command == "criteria":
            print(json.dumps({
                "priority_rules": EvaluationCriteria.PRIORITY_RULES,
                "keywords": EvaluationCriteria.KNOWLEDGE_KEYWORDS
            }, indent=2, ensure_ascii=False))
            
    else:
        print(f"""
🎯 SRS v{srs.version} - Security Research System

用法:
  srs status              # 查看状态
  srs review              # 日常知识库Review
  srs daily               # 同上
  srs eval '<任务>'       # 评估任务
  srs criteria            # 查看评估标准
        """)

if __name__ == "__main__":
    main()
