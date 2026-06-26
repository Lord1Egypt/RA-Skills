#!/usr/bin/env python3
"""
记忆优先级计算器 - 智能计算记忆优先级

功能：
- 基于多维度计算记忆优先级
- 重要性评估（与用户目标的相关性）
- 实用性评估（使用频率预测）
- 情感权重计算
- 时间衰减模型
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db


class MemoryPriorityCalculator:
    """记忆优先级计算器"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.conn = None
        self._connect()
        
        # 关键词权重配置
        self.importance_keywords = {
            '高权重': ['重要', '关键', '必须', '绝对', '核心', 'critical', 'important', 'key'],
            '中权重': ['应该', '建议', '推荐', '最好', '建议', 'should', 'must'],
            '低权重': ['可能', '也许', '大概', '也许', 'maybe', 'perhaps']
        }
        
        self.utility_keywords = {
            '高实用性': ['登录', '密码', '账号', '配置', '安装', '设置', 'password', 'config'],
            '中实用性': ['方法', '技巧', '教程', '步骤', 'how to', 'tutorial'],
            '低实用性': ['想法', '念头', '构思', 'idea', 'thought']
        }
        
        self.emotion_keywords = {
            '强情感': ['喜欢', '讨厌', '爱', '恨', '想要', '恐惧', 'love', 'hate', 'fear'],
            '中情感': ['觉得', '感觉', '认为', 'think', 'feel'],
            '弱情感': ['关于', '对于', '对于', 'about', 'regarding']
        }
    
    def _connect(self):
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
    
    def calculate_importance_score(self, content: str) -> float:
        """计算重要性得分"""
        if not content:
            return 50.0
        
        score = 50.0  # 基础分
        content_lower = content.lower()
        
        # 关键词加分
        for weight, keywords in self.importance_keywords.items():
            for kw in keywords:
                if kw.lower() in content_lower:
                    if weight == '高权重':
                        score += 15
                    elif weight == '中权重':
                        score += 8
                    else:
                        score += 3
        
        # 句子长度（较长通常更详细）
        if len(content) > 100:
            score += 5
        
        return min(100, max(0, score))
    
    def calculate_utility_score(self, content: str) -> float:
        """计算实用性得分"""
        if not content:
            return 50.0
        
        score = 50.0
        content_lower = content.lower()
        
        for weight, keywords in self.utility_keywords.items():
            for kw in keywords:
                if kw.lower() in content_lower:
                    if weight == '高实用性':
                        score += 20
                    elif weight == '中实用性':
                        score += 10
                    else:
                        score += 5
        
        # 代码/命令检测
        if any(marker in content for marker in ['```', '`', 'python', 'bash', 'npm', 'pip']):
            score += 10
        
        # URL 检测
        if 'http' in content_lower or '://' in content:
            score += 5
        
        return min(100, max(0, score))
    
    def calculate_emotion_score(self, content: str) -> float:
        """计算情感权重得分"""
        if not content:
            return 50.0
        
        score = 50.0
        content_lower = content.lower()
        
        for weight, keywords in self.emotion_keywords.items():
            for kw in keywords:
                if kw.lower() in content_lower:
                    if weight == '强情感':
                        score += 15
                    elif weight == '中情感':
                        score += 8
                    else:
                        score += 3
        
        # 感叹号/问号检测
        if '!' in content:
            score += 5
        if '?' in content:
            score += 3
        
        return min(100, max(0, score))
    
    def calculate_recency_score(self, created_time: str) -> float:
        """计算新鲜度得分"""
        if not created_time:
            return 50.0
        
        try:
            created = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
            now = datetime.now()
            days_old = (now - created).days
            
            # 新记忆高得分，随时间衰减
            if days_old <= 1:
                return 100.0
            elif days_old <= 7:
                return 90.0
            elif days_old <= 30:
                return 80.0 - (days_old - 7) * 0.5
            elif days_old <= 90:
                return 70.0 - (days_old - 30) * 0.2
            else:
                return max(30.0, 60.0 - (days_old - 90) * 0.05)
        except:
            return 50.0
    
    def calculate_type_bonus(self, mem_type: str) -> float:
        """计算类型加成"""
        type_weights = {
            'preference': 15,
            'decision': 20,
            'goal': 25,
            'habit': 10,
            'skill': 20,
            'contact': 15,
            'info': 5,
            'learning': 15
        }
        
        return type_weights.get(mem_type, 0)
    
    def calculate_final_priority(
        self,
        content: str,
        mem_type: str,
        created_time: str,
        existing_priority: int = 50
    ) -> Dict:
        """计算最终优先级"""
        importance = self.calculate_importance_score(content)
        utility = self.calculate_utility_score(content)
        emotion = self.calculate_emotion_score(content)
        recency = self.calculate_recency_score(created_time)
        type_bonus = self.calculate_type_bonus(mem_type)
        
        # 综合计算（加权平均）
        final_score = (
            importance * 0.25 +
            utility * 0.25 +
            emotion * 0.15 +
            recency * 0.20 +
            type_bonus +
            existing_priority * 0.15
        )
        
        final_score = min(100, max(0, final_score))
        
        return {
            'final_priority': round(final_score),
            'breakdown': {
                'importance': round(importance, 1),
                'utility': round(utility, 1),
                'emotion': round(emotion, 1),
                'recency': round(recency, 1),
                'type_bonus': round(type_bonus, 1),
                'existing_weight': round(existing_priority * 0.15, 1)
            },
            'suggested_action': self._get_suggested_action(final_score)
        }
    
    def _get_suggested_action(self, priority: float) -> str:
        """根据优先级建议操作"""
        if priority >= 90:
            return "🔴 立即关注 - 最高优先级"
        elif priority >= 75:
            return "🟠 高优先级 - 尽快处理"
        elif priority >= 60:
            return "🟡 中高优先级 - 值得关注"
        elif priority >= 45:
            return "🟢 中优先级 - 常规记忆"
        else:
            return "⚪ 低优先级 - 可归档"
    
    def analyze_all_memories(self) -> Dict:
        """分析所有记忆的优先级"""
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            ORDER BY created_time DESC
            LIMIT 100
        """)
        
        priorities = []
        for row in cursor.fetchall():
            calc = self.calculate_final_priority(
                row['content'],
                row['type'],
                row['created_time'],
                row['priority'] or 50
            )
            priorities.append({
                'record_id': row['record_id'],
                'content_preview': (row['content'] or '')[:50],
                'type': row['type'],
                'old_priority': row['priority'],
                'new_priority': calc['final_priority'],
                'change': calc['final_priority'] - (row['priority'] or 50),
                'breakdown': calc['breakdown']
            })
        
        # 排序：变化最大的在前
        priorities.sort(key=lambda x: abs(x['change']), reverse=True)
        
        return {
            'total_analyzed': len(priorities),
            'priority_changes': priorities[:20],  # 显示变化最大的20条
            'avg_old_priority': sum(p['old_priority'] or 50 for p in priorities) / len(priorities) if priorities else 0,
            'avg_new_priority': sum(p['new_priority'] for p in priorities) / len(priorities) if priorities else 0
        }
    
    def generate_priority_report(self) -> str:
        """生成优先级报告"""
        lines = ["# 📊 记忆优先级分析报告", ""]
        lines.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        analysis = self.analyze_all_memories()
        
        lines.append(f"## 📈 总体统计")
        lines.append(f"- 分析记忆数：{analysis['total_analyzed']}")
        lines.append(f"- 平均原优先级：{analysis['avg_old_priority']:.1f}")
        lines.append(f"- 平均新优先级：{analysis['avg_new_priority']:.1f}")
        lines.append("")
        
        lines.append("## 🔄 优先级变化（Top 10）")
        for item in analysis['priority_changes'][:10]:
            change_emoji = "📈" if item['change'] > 0 else "📉" if item['change'] < 0 else "➖"
            lines.append(f"{change_emoji} [{item['type']}] {item['content_preview']}...")
            lines.append(f"   {item['old_priority']} → **{item['new_priority']}** (变化: {item['change']:+.0f})")
        
        return "\n".join(lines)
    
    def close(self):
        if self.conn:
            self.conn.close()


def main():
    calc = MemoryPriorityCalculator()
    print(calc.generate_priority_report())
    calc.close()


if __name__ == '__main__':
    main()
