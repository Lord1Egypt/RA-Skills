#!/usr/bin/env python3
"""
行动建议器 - 根据上下文预测需求并生成建议
"""
import json
from datetime import datetime, time
from pathlib import Path

class ActionSuggester:
    def __init__(self, base_path=None):
        self.base_path = base_path or Path(__file__).parent.parent.parent
        
    def suggest_actions(self, context=None):
        """根据上下文生成行动建议"""
        if context is None:
            from context_analyzer import ContextAnalyzer
            analyzer = ContextAnalyzer(self.base_path)
            context = analyzer.get_current_context()
        
        suggestions = []
        time_slot = context.get('time_slot', '')
        market_status = context.get('market_status', {})
        content_status = context.get('content_status', {})
        
        # 1. 时间触发型建议
        time_suggestions = self._time_based_suggestions(time_slot)
        suggestions.extend(time_suggestions)
        
        # 2. 市场状态建议
        market_suggestions = self._market_based_suggestions(market_status)
        suggestions.extend(market_suggestions)
        
        # 3. 内容发布建议
        content_suggestions = self._content_based_suggestions(content_status)
        suggestions.extend(content_suggestions)
        
        # 4. 待办任务建议
        pending_tasks = context.get('pending_tasks', [])
        if pending_tasks:
            suggestions.append({
                "type": "task",
                "priority": "medium",
                "action": f"有{len(pending_tasks)}个待完成任务",
                "suggestion": "检查并处理待办事项"
            })
        
        # 5. 学习优化建议
        recent_interactions = context.get('recent_interactions', [])
        if len(recent_interactions) > 3:
            suggestions.append({
                "type": "learning",
                "priority": "low",
                "action": "近期交互记录较多",
                "suggestion": "可以运行analyze_performance分析表现"
            })
        
        # 按优先级排序
        priority_order = {"high": 0, "medium": 1, "low": 2}
        suggestions.sort(key=lambda x: priority_order.get(x['priority'], 2))
        
        return suggestions
    
    def _time_based_suggestions(self, time_slot):
        """基于时间的建议"""
        suggestions = []
        
        if time_slot == "morning_startup":
            suggestions.append({
                "type": "routine",
                "priority": "high",
                "action": "早间启动检查",
                "suggestion": "检查股票持仓、小红书数据、今日计划"
            })
        
        elif time_slot == "morning_trading":
            suggestions.append({
                "type": "trading",
                "priority": "high",
                "action": "早盘交易时段",
                "suggestion": "观察候选股票，等待买入机会"
            })
        
        elif time_slot == "afternoon_trading":
            suggestions.append({
                "type": "trading",
                "priority": "high",
                "action": "尾盘交易时段",
                "suggestion": "评估今日持仓，决定是否操作"
            })
        
        elif time_slot == "content_publish_window":
            suggestions.append({
                "type": "content",
                "priority": "high",
                "action": "下午内容发布窗口",
                "suggestion": "检查待发布内容，准备发布小红书笔记"
            })
        
        elif time_slot == "evening_routine":
            suggestions.append({
                "type": "routine",
                "priority": "medium",
                "action": "晚间例行检查",
                "suggestion": "检查今日数据，记录交易日志"
            })
        
        return suggestions
    
    def _market_based_suggestions(self, market_status):
        """基于市场状态的建议"""
        suggestions = []
        status = market_status.get('status', 'closed')
        
        if status == "morning_session":
            suggestions.append({
                "type": "trading",
                "priority": "high",
                "action": "早盘进行中",
                "suggestion": "检查广安爱众等候选股表现"
            })
        
        elif status == "afternoon_session":
            suggestions.append({
                "type": "trading",
                "priority": "high",
                "action": "尾盘进行中",
                "suggestion": "评估持仓，准备收盘操作"
            })
        
        return suggestions
    
    def _content_based_suggestions(self, content_status):
        """基于内容状态的建议"""
        suggestions = []
        pending = content_status.get('pending_posts', 0)
        
        if pending > 0:
            suggestions.append({
                "type": "content",
                "priority": "high",
                "action": f"有{pending}篇待发布内容",
                "suggestion": "完善内容并选择合适时间发布"
            })
        
        return suggestions
    
    def get_next_action(self):
        """获取下一个最重要的行动"""
        suggestions = self.suggest_actions()
        if suggestions:
            return suggestions[0]
        return None


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="行动建议器")
    parser.add_argument("--next", action="store_true", help="只显示下一个建议行动")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()
    
    suggester = ActionSuggester()
    
    if args.next:
        action = suggester.get_next_action()
        if action:
            if args.json:
                print(json.dumps(action, ensure_ascii=False))
            else:
                print(f"\n[{action['priority'].upper()}] {action['action']}")
                print(f"Suggestion: {action['suggestion']}")
        else:
            print("暂无待处理事项")
    else:
        suggestions = suggester.suggest_actions()
        if args.json:
            print(json.dumps(suggestions, ensure_ascii=False, indent=2))
        else:
            print("=== 行动建议 ===")
            for i, s in enumerate(suggestions, 1):
                print(f"{i}. [{s['priority'].upper()}] {s['action']}")
                print(f"   建议: {s['suggestion']}")
