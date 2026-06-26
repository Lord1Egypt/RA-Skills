#!/usr/bin/env python3
"""
Secretary Core v2.1 - Adaptive Work Planning
Updates work requirements and plans based on conversation needs
Integrates with Intelligence Officer for continuous improvement
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class WorkRequirement:
    """Work requirement item"""
    id: str
    title: str
    description: str
    priority: str  # high/medium/low
    deadline: Optional[str]
    status: str = "pending"  # pending/in_progress/completed
    created_from: str = "conversation"  # conversation/intelligence/ceo

@dataclass
class WorkPlan:
    """Work plan structure"""
    date: str
    requirements: List[WorkRequirement] = field(default_factory=list)
    last_updated: str = ""
    iteration_count: int = 0

class AdaptiveSecretary:
    """Secretary with adaptive work planning v2.1"""
    
    def __init__(self):
        """Initialize adaptive secretary"""
        self.work_plans = {}
        self.requirements_history = []
        self.ceo_feedback_loop = []
    
    def analyze_conversation(self, conversation: str) -> Dict:
        """
        Analyze conversation to identify work requirements
        
        Args:
            conversation: Conversation text
            
        Returns:
            Identified requirements and priorities
        """
        requirements = []
        
        # Keywords that indicate work requirements
        requirement_keywords = [
            "需要", "想要", "希望", "计划", "安排", "任务",
            "need", "want", "plan", "task", "require"
        ]
        
        # Priority indicators
        priority_keywords = {
            "high": ["紧急", "立即", "马上", "urgent", "immediate"],
            "medium": ["重要", "优先", "important", "priority"],
            "low": ["可以", "有空", "later", "when possible"]
        }
        
        # Extract requirements
        sentences = conversation.split('。')
        for sentence in sentences:
            if any(kw in sentence for kw in requirement_keywords):
                # Determine priority
                priority = "medium"
                for p, keywords in priority_keywords.items():
                    if any(kw in sentence for kw in keywords):
                        priority = p
                        break
                
                requirements.append({
                    "text": sentence.strip(),
                    "priority": priority,
                    "source": "conversation"
                })
        
        return {
            "requirements": requirements,
            "count": len(requirements),
            "priorities": {
                "high": sum(1 for r in requirements if r["priority"] == "high"),
                "medium": sum(1 for r in requirements if r["priority"] == "medium"),
                "low": sum(1 for r in requirements if r["priority"] == "low")
            }
        }
    
    def update_work_plan(self, date: str, new_requirements: List[Dict], source: str = "conversation") -> WorkPlan:
        """
        Update work plan with new requirements
        
        Args:
            date: Plan date (YYYY-MM-DD)
            new_requirements: New requirements to add
            source: Source of requirements (conversation/intelligence/ceo)
            
        Returns:
            Updated work plan
        """
        # Get or create plan
        if date not in self.work_plans:
            self.work_plans[date] = WorkPlan(date=date, last_updated=datetime.now().isoformat())
        
        plan = self.work_plans[date]
        
        # Add new requirements
        for req in new_requirements:
            work_req = WorkRequirement(
                id=f"req-{len(plan.requirements) + 1}",
                title=req.get("title", req.get("text", "New Task"))[:50],
                description=req.get("text", ""),
                priority=req.get("priority", "medium"),
                deadline=req.get("deadline"),
                status="pending",
                created_from=source
            )
            plan.requirements.append(work_req)
            self.requirements_history.append({
                "requirement": work_req,
                "added_at": datetime.now().isoformat(),
                "source": source
            })
        
        # Update metadata
        plan.last_updated = datetime.now().isoformat()
        plan.iteration_count += 1
        
        return plan
    
    def integrate_intelligence_feedback(self, intelligence_report: Dict) -> List[WorkRequirement]:
        """
        Integrate intelligence officer feedback into work plan
        
        Args:
            intelligence_report: Intelligence report from Intelligence Officer
            
        Returns:
            New work requirements based on intelligence
        """
        new_requirements = []
        
        # From R&D recommendations
        for rec in intelligence_report.get("rd_recommendations", [])[:3]:
            if rec.get("priority") == "high":
                new_requirements.append({
                    "title": f"研发：{rec.get('title', 'New R&D')}",
                    "text": rec.get("justification", ""),
                    "priority": "high",
                    "deadline": (datetime.now() + timedelta(weeks=2)).strftime("%Y-%m-%d"),
                    "source": "intelligence"
                })
        
        # From trends
        for trend in intelligence_report.get("hot_trends", [])[:2]:
            if trend.get("relevance") == "high":
                new_requirements.append({
                    "title": f"跟踪趋势：{trend.get('topic', 'New Trend')}",
                    "text": trend.get("action", ""),
                    "priority": "medium",
                    "deadline": (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d"),
                    "source": "intelligence"
                })
        
        return [WorkRequirement(**req) for req in new_requirements if "title" in req]
    
    def get_ceo_optimization_suggestions(self) -> Dict:
        """
        Generate workflow optimization suggestions for CEO
        
        Returns:
            Optimization suggestions based on patterns
        """
        suggestions = []
        
        # Analyze requirement patterns
        if len(self.requirements_history) > 10:
            # Count by source
            sources = {}
            for item in self.requirements_history:
                source = item["source"]
                sources[source] = sources.get(source, 0) + 1
            
            # Identify patterns
            if sources.get("conversation", 0) > sources.get("intelligence", 0) * 2:
                suggestions.append({
                    "type": "process_improvement",
                    "title": "增加情报驱动的需求收集",
                    "justification": "当前需求主要来自对话，建议增加情报搜集官的输入比例",
                    "action": "提高 Intelligence Officer 的使用频率",
                    "expected_impact": "更前瞻性的工作规划"
                })
            
            # Priority distribution
            priorities = {}
            for item in self.requirements_history:
                priority = item["requirement"].priority
                priorities[priority] = priorities.get(priority, 0) + 1
            
            if priorities.get("high", 0) > len(self.requirements_history) * 0.5:
                suggestions.append({
                    "type": "priority_management",
                    "title": "优化优先级管理",
                    "justification": f"高优先级任务占比 {priorities['high']/len(self.requirements_history)*100:.1f}%，可能影响效率",
                    "action": "重新评估优先级标准，减少高优先级任务数量",
                    "expected_impact": "提高团队效率和专注度"
                })
        
        return {
            "suggestions": suggestions,
            "analysis_date": datetime.now().isoformat(),
            "data_points": len(self.requirements_history)
        }
    
    def generate_work_plan_report(self, date: str) -> str:
        """
        Generate work plan report
        
        Args:
            date: Plan date (YYYY-MM-DD)
            
        Returns:
            Formatted report
        """
        if date not in self.work_plans:
            return f"No work plan for {date}"
        
        plan = self.work_plans[date]
        
        report = f"""# 📋 工作计划 - {date}

**最后更新：** {plan.last_updated}  
**迭代次数：** {plan.iteration_count}  
**总任务数：** {len(plan.requirements)}

---

## 📊 任务分布

| 优先级 | 数量 | 占比 |
|--------|------|------|
"""
        
        # Count by priority
        priority_counts = {}
        for req in plan.requirements:
            priority_counts[req.priority] = priority_counts.get(req.priority, 0) + 1
        
        for priority in ["high", "medium", "low"]:
            count = priority_counts.get(priority, 0)
            percentage = count / len(plan.requirements) * 100 if plan.requirements else 0
            report += f"| {priority} | {count} | {percentage:.1f}% |\n"
        
        report += """
---

## 📝 任务列表

"""
        
        # Group by priority
        for priority in ["high", "medium", "low"]:
            priority_reqs = [r for r in plan.requirements if r.priority == priority]
            if priority_reqs:
                report += f"""### {priority.upper()} Priority

"""
                for req in priority_reqs:
                    status_emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(req.status, "⏳")
                    source_emoji = {"conversation": "💬", "intelligence": "🕵️", "ceo": "👔"}.get(req.created_from, "💬")
                    report += f"{status_emoji} {source_emoji} **{req.title}** (截止：{req.deadline or '未定'})\n"
                    report += f"   - {req.description[:100]}...\n\n"
        
        report += """---

## 📈 来源分析

"""
        # Count by source
        source_counts = {}
        for req in plan.requirements:
            source_counts[req.created_from] = source_counts.get(req.created_from, 0) + 1
        
        for source, count in source_counts.items():
            source_emoji = {"conversation": "💬 对话", "intelligence": "🕵️ 情报", "ceo": "👔 CEO"}.get(source, source)
            report += f"- {source_emoji}: {count} 任务\n"
        
        report += f"""
---

**生成时间：** {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""
        
        return report

# Main execution for testing
def main():
    """Test adaptive secretary"""
    secretary = AdaptiveSecretary()
    
    # Simulate conversation
    conversation = "我需要立即准备明天的会议材料，另外希望下周能完成竞品分析报告，有空的时候整理一下文档。"
    
    # Analyze conversation
    analysis = secretary.analyze_conversation(conversation)
    print(f"📊 Conversation Analysis: {analysis['count']} requirements found")
    
    # Update work plan
    today = datetime.now().strftime("%Y-%m-%d")
    new_reqs = [
        {"title": "Prepare meeting materials", "text": "准备明天会议材料", "priority": "high", "deadline": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")},
        {"title": "Competitor analysis", "text": "完成竞品分析报告", "priority": "medium", "deadline": (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d")}
    ]
    
    plan = secretary.update_work_plan(today, new_reqs, source="conversation")
    print(f"✅ Work plan updated: {len(plan.requirements)} tasks")
    
    # Generate report
    report = secretary.generate_work_plan_report(today)
    print("\n" + report)

if __name__ == "__main__":
    main()
