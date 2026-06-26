#!/usr/bin/env python3
"""
空投交互检查清单生成器
为指定项目生成完整的交互任务清单
"""

from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime, timedelta

@dataclass
class Task:
    """单个任务"""
    name: str
    description: str
    frequency: str  # daily, weekly, monthly, one-time
    estimated_time: int  # 分钟
    priority: str  # high, medium, low
    completed: bool = False
    notes: str = ""

@dataclass
class TaskList:
    """任务清单"""
    project_name: str
    phase: str
    tasks: List[Task] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

class InteractionChecklist:
    """交互检查清单生成器"""
    
    # 项目模板库
    PROJECT_TEMPLATES = {
        "monad": {
            "name": "Monad Testnet",
            "phase": "测试网阶段",
            "tasks": [
                Task("配置网络", "添加 Monad Testnet 到钱包", "one-time", 5, "high"),
                Task("领测试币", "从水笼头领取 MON 测试币", "daily", 5, "high"),
                Task("官方桥接", "从 Sepolia 桥接 ETH 到 Monad", "weekly", 15, "high"),
                Task("部署合约", "使用 Remix 部署简单合约", "one-time", 20, "high"),
                Task("Kintsu质押", "在 Kintsu 质押 MON", "weekly", 10, "medium"),
                Task("NadSwap交易", "在 NadSwap 进行 Swap", "weekly", 10, "medium"),
                Task("Curvance借贷", "在 Curvance 存借操作", "weekly", 15, "medium"),
                Task("生态探索", "尝试新的生态项目", "weekly", 20, "low"),
            ]
        },
        "sahara": {
            "name": "Sahara AI",
            "phase": "白名单申请",
            "tasks": [
                Task("白名单申请", "提交白名单申请表", "one-time", 30, "high"),
                Task("Galxe任务", "完成 Galxe 上的社交任务", "weekly", 20, "high"),
                Task("Discord活跃", "参与 Discord 社区讨论", "daily", 10, "medium"),
                Task("Twitter互动", "关注、转发官方推文", "weekly", 10, "medium"),
                Task("测试网准备", "注册测试网账号", "one-time", 15, "medium"),
            ]
        },
        "eclipse": {
            "name": "Eclipse Mainnet",
            "phase": "主网阶段",
            "tasks": [
                Task("跨链桥接", "从 Ethereum 桥接 ETH 到 Eclipse", "one-time", 20, "high"),
                Task("Invariant交易", "在 Invariant DEX 交易", "weekly", 15, "high"),
                Task("添加流动性", "在 Invariant 提供流动性", "monthly", 15, "medium"),
                Task("Titan合约", "在 Titan 开合约仓位", "weekly", 15, "medium"),
                Task("NFT交互", "购买/交易 Eclipse NFT", "monthly", 20, "low"),
            ]
        },
        "polymarket": {
            "name": "Polymarket",
            "phase": "主网使用",
            "tasks": [
                Task("账号注册", "注册并完成 KYC", "one-time", 30, "high"),
                Task("充值USDC", "从 Polygon 充值 USDC", "one-time", 15, "high"),
                Task("参与预测", "选择事件进行预测", "weekly", 20, "high"),
                Task("提供流动性", "为市场提供流动性", "monthly", 20, "medium"),
                Task("活动关注", "关注新事件和活动", "weekly", 10, "low"),
            ]
        },
    }
    
    def generate_checklist(self, project_key: str) -> TaskList:
        """生成指定项目的检查清单"""
        template = self.PROJECT_TEMPLATES.get(project_key.lower())
        
        if not template:
            available = ", ".join(self.PROJECT_TEMPLATES.keys())
            raise ValueError(f"未知项目: {project_key}. 可用项目: {available}")
        
        return TaskList(
            project_name=template["name"],
            phase=template["phase"],
            tasks=[Task(**t.__dict__) for t in template["tasks"]]
        )
    
    def generate_custom_checklist(
        self,
        project_name: str,
        phase: str,
        tasks_data: List[Dict]
    ) -> TaskList:
        """生成自定义检查清单"""
        tasks = [Task(**data) for data in tasks_data]
        
        return TaskList(
            project_name=project_name,
            phase=phase,
            tasks=tasks
        )
    
    def print_checklist(self, checklist: TaskList):
        """打印检查清单"""
        print(f"\n{'='*70}")
        print(f"📋 {checklist.project_name} 交互检查清单")
        print(f"   阶段: {checklist.phase}")
        print(f"   创建时间: {checklist.created_at.strftime('%Y-%m-%d')}")
        print(f"{'='*70}")
        
        # 按优先级分组
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(checklist.tasks, key=lambda t: priority_order.get(t.priority, 3))
        
        # 按频率分组显示
        frequencies = ["one-time", "daily", "weekly", "monthly"]
        frequency_names = {
            "one-time": "🔵 一次性任务",
            "daily": "🟢 每日任务",
            "weekly": "🟡 每周任务",
            "monthly": "🟠 每月任务"
        }
        
        for freq in frequencies:
            tasks_in_freq = [t for t in sorted_tasks if t.frequency == freq]
            if tasks_in_freq:
                print(f"\n{frequency_names[freq]}")
                print("-" * 70)
                
                for i, task in enumerate(tasks_in_freq, 1):
                    status = "✅" if task.completed else "⬜"
                    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
                    
                    print(f"{status} {priority_emoji} {task.name}")
                    print(f"   描述: {task.description}")
                    print(f"   预计时间: {task.estimated_time}分钟")
                    if task.notes:
                        print(f"   备注: {task.notes}")
                    print()
        
        # 统计
        total = len(checklist.tasks)
        completed = sum(1 for t in checklist.tasks if t.completed)
        total_time = sum(t.estimated_time for t in checklist.tasks)
        
        print(f"{'='*70}")
        print(f"📊 统计: {completed}/{total} 任务完成 | 预计总时间: {total_time}分钟")
        print(f"{'='*70}\n")
    
    def generate_schedule(self, checklist: TaskList) -> Dict[str, List[str]]:
        """生成时间安排建议"""
        schedule = {
            "周一": [],
            "周二": [],
            "周三": [],
            "周四": [],
            "周五": [],
            "周六": [],
            "周日": [],
        }
        
        # 分配每周任务
        weekly_tasks = [t for t in checklist.tasks if t.frequency == "weekly"]
        days = list(schedule.keys())
        
        for i, task in enumerate(weekly_tasks):
            day = days[i % 7]
            schedule[day].append(f"{task.name} ({task.estimated_time}min)")
        
        # 每日任务
        daily_tasks = [t for t in checklist.tasks if t.frequency == "daily"]
        for day in schedule:
            for task in daily_tasks:
                schedule[day].insert(0, f"[每日] {task.name} ({task.estimated_time}min)")
        
        return schedule
    
    def print_schedule(self, schedule: Dict[str, List[str]]):
        """打印时间安排"""
        print(f"\n📅 建议时间安排")
        print("=" * 70)
        
        for day, tasks in schedule.items():
            print(f"\n{day}:")
            if tasks:
                for task in tasks:
                    print(f"  • {task}")
            else:
                print("  (休息日)")
        
        print()


def demo():
    """演示"""
    generator = InteractionChecklist()
    
    # Monad 检查清单
    print("\n" + "🎯 " * 20)
    monad_list = generator.generate_checklist("monad")
    generator.print_checklist(monad_list)
    
    # 生成时间安排
    schedule = generator.generate_schedule(monad_list)
    generator.print_schedule(schedule)
    
    # Sahara 检查清单
    print("\n" + "🎯 " * 20)
    sahara_list = generator.generate_checklist("sahara")
    generator.print_checklist(sahara_list)


if __name__ == "__main__":
    demo()
