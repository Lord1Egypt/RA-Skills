#!/usr/bin/env python3
"""
任务发起器 - 主动提出并执行任务
"""
import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from context_analyzer import ContextAnalyzer
from action_suggester import ActionSuggester

class TaskInitiator:
    def __init__(self, base_path=None):
        self.base_path = base_path or Path(__file__).parent.parent.parent
        self.tasks_file = self.base_path / "memory" / "proactive_tasks.json"
        # 确保目录存在
        self.tasks_file.parent.mkdir(parents=True, exist_ok=True)
        
    def propose_tasks(self):
        """主动提出任务"""
        analyzer = ContextAnalyzer(self.base_path)
        suggester = ActionSuggester(self.base_path)
        
        context = analyzer.get_current_context()
        suggestions = suggester.suggest_actions(context)
        
        # 将建议转化为具体任务
        tasks = []
        for suggestion in suggestions:
            task = self._suggestion_to_task(suggestion, context)
            if task:
                tasks.append(task)
        
        return tasks
    
    def _suggestion_to_task(self, suggestion, context):
        """将建议转化为具体任务"""
        task_templates = {
            "morning_startup": {
                "name": "早间检查",
                "steps": [
                    "检查股票持仓状态",
                    "查看小红书昨日数据",
                    "确认今日待办事项"
                ],
                "auto_execute": False
            },
            "trading": {
                "name": "交易监控",
                "steps": [
                    "检查候选股票实时价格",
                    "评估买入/卖出条件",
                    "记录交易决策"
                ],
                "auto_execute": False
            },
            "content": {
                "name": "内容发布",
                "steps": [
                    "检查待发布内容",
                    "完善标题和正文",
                    "生成配图",
                    "选择发布时间（15:00-17:00）"
                ],
                "auto_execute": False
            },
            "routine": {
                "name": "例行检查",
                "steps": [
                    "检查今日完成情况",
                    "记录重要事项",
                    "更新记忆系统"
                ],
                "auto_execute": False
            },
            "task": {
                "name": "任务处理",
                "steps": [
                    "审查待办事项",
                    "按优先级处理"
                ],
                "auto_execute": False
            },
            "learning": {
                "name": "学习优化",
                "steps": [
                    "运行analyze_performance",
                    "提取改进规则",
                    "更新MEMORY.md"
                ],
                "auto_execute": False
            }
        }
        
        task_type = suggestion.get('type', 'routine')
        template = task_templates.get(task_type, task_templates['routine'])
        
        return {
            "id": f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "name": template['name'],
            "priority": suggestion.get('priority', 'medium'),
            "description": suggestion.get('action', ''),
            "steps": template['steps'],
            "auto_execute": template['auto_execute'],
            "status": "proposed"
        }
    
    def save_tasks(self, tasks):
        """保存任务"""
        existing = []
        if self.tasks_file.exists():
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        
        # 合并新任务
        all_tasks = existing + tasks
        
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(all_tasks, f, ensure_ascii=False, indent=2)
    
    def get_pending_tasks(self):
        """获取待处理任务"""
        if not self.tasks_file.exists():
            return []
        
        with open(self.tasks_file, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        
        return [t for t in tasks if t.get('status') == 'proposed']
    
    def mark_completed(self, task_id):
        """标记任务完成"""
        if not self.tasks_file.exists():
            return
        
        with open(self.tasks_file, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        
        for task in tasks:
            if task['id'] == task_id:
                task['status'] = 'completed'
                task['completed_at'] = datetime.now().isoformat()
        
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="任务发起器")
    parser.add_argument("--propose", action="store_true", help="主动提出任务")
    parser.add_argument("--pending", action="store_true", help="查看待处理任务")
    parser.add_argument("--complete", type=str, help="标记任务完成（提供任务ID）")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()
    
    initiator = TaskInitiator()
    
    if args.propose:
        tasks = initiator.propose_tasks()
        if args.json:
            print(json.dumps(tasks, ensure_ascii=False, indent=2))
        else:
            print(f"=== 提出 {len(tasks)} 个任务 ===")
            for task in tasks:
                print(f"\n[{task['priority'].upper()}] {task['name']}")
                print(f"描述: {task['description']}")
                print("步骤:")
                for i, step in enumerate(task['steps'], 1):
                    print(f"  {i}. {step}")
        
        # 保存任务
        initiator.save_tasks(tasks)
        print(f"\n任务已保存到 {initiator.tasks_file}")
    
    elif args.pending:
        tasks = initiator.get_pending_tasks()
        if args.json:
            print(json.dumps(tasks, ensure_ascii=False, indent=2))
        else:
            if tasks:
                print(f"=== {len(tasks)} 个待处理任务 ===")
                for task in tasks:
                    print(f"- [{task['priority'].upper()}] {task['name']}: {task['description']}")
            else:
                print("没有待处理任务")
    
    elif args.complete:
        initiator.mark_completed(args.complete)
        print(f"任务 {args.complete} 已标记为完成")
    
    else:
        # 默认：提出任务
        tasks = initiator.propose_tasks()
        for task in tasks[:3]:  # 只显示前3个
            print(f"[{task['priority'].upper()}] {task['name']}: {task['description']}")
