"""
Goals Module - 目标追踪系统
管理用户健身目标设定和进度追踪
包括马拉松训练目标管理
"""

import os
import json
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field

# 路径设置
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOALS_DIR = os.path.join(SKILL_DIR, "data", "profiles")


@dataclass
class Goal:
    """基础目标数据类"""
    goal_id: str
    user_id: str
    goal_type: str  # 增肌/减脂/力量/体能/马拉松训练
    target: float
    current: float
    unit: str  # kg/次/%/场/km
    deadline: str
    created_at: str
    updated_at: str
    completed: bool = False
    completed_at: str = ""


@dataclass
class MarathonGoal:
    """马拉松目标数据类"""
    goal_id: str
    user_id: str
    goal_type: str = "马拉松训练"
    goal_name: str = ""  # 如"北京半马"
    race_date: str = ""  # YYYY-MM-DD
    race_type: str = "半程马拉松"  # 半程马拉松/全程马拉松
    goal_time: str = ""  # HH:MM:SS
    target_pace: str = ""  # MM:SS（每公里）
    splits: Dict[str, str] = field(default_factory=dict)  # {"前半马": "5:40", "后半马": "5:45"}
    current: float = 0  # 完成的训练次数
    target: float = 1  # 目标场次
    unit: str = "场"
    status: str = "active"  # active/completed/cancelled
    created_at: str = ""
    updated_at: str = ""
    notes: str = ""  # 备注
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()
    
    @property
    def days_until_race(self) -> int:
        """计算距离比赛还有多少天"""
        try:
            race_date_obj = datetime.strptime(self.race_date, "%Y-%m-%d").date()
            today = datetime.now().date()
            return (race_date_obj - today).days
        except Exception:
            return 0
    
    @property
    def training_phase(self) -> str:
        """根据距离比赛天数返回训练阶段"""
        days = self.days_until_race
        
        if days < 0:
            return "已结束"
        elif days == 0:
            return "比赛日"
        elif days <= 7:
            return "比赛周"
        elif days <= 14:
            return "减量期"
        elif days <= 28:
            return "巅峰期"
        else:
            return "基础期"
    
    @property
    def is_recovery_week_needed(self) -> bool:
        """针对背靠背比赛，是否需要恢复周"""
        # 如果距离比赛小于7天且是全程马拉松，可能需要恢复周
        if self.race_type == "全程马拉松" and self.days_until_race <= 7:
            return True
        return False
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MarathonGoal':
        """从字典创建"""
        return cls(**data)


class GoalsManager:
    """
    目标管理器
    管理用户的健身目标（包括马拉松训练目标）
    """
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.goals_file = os.path.join(GOALS_DIR, f"goals_{user_id}.json")
        self.marathon_goals_file = os.path.join(GOALS_DIR, f"marathon_goals_{user_id}.json")
        os.makedirs(GOALS_DIR, exist_ok=True)
    
    # ==================== 基础目标 CRUD ====================
    
    def _load_goals(self) -> List[Dict]:
        """加载基础目标"""
        if not os.path.exists(self.goals_file):
            return []
        try:
            with open(self.goals_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    
    def _save_goals(self, goals: List[Dict]) -> bool:
        """保存基础目标"""
        try:
            with open(self.goals_file, 'w', encoding='utf-8') as f:
                json.dump(goals, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def create_goal(
        self,
        goal_type: str,
        target: float,
        current: float,
        unit: str,
        deadline: str
    ) -> Goal:
        """创建新目标"""
        goal = Goal(
            goal_id=f"goal_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            user_id=self.user_id,
            goal_type=goal_type,
            target=target,
            current=current,
            unit=unit,
            deadline=deadline,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        goals = self._load_goals()
        goals.append(asdict(goal))
        self._save_goals(goals)
        
        return goal
    
    def get_active_goals(self) -> List[Goal]:
        """获取活跃基础目标"""
        goals = self._load_goals()
        return [Goal(**g) for g in goals if not g.get("completed", False)]
    
    def get_completed_goals(self) -> List[Goal]:
        """获取已完成基础目标"""
        goals = self._load_goals()
        return [Goal(**g) for g in goals if g.get("completed", False)]
    
    def update_progress(self, goal_id: str, current: float) -> bool:
        """更新目标进度"""
        goals = self._load_goals()
        
        for goal in goals:
            if goal["goal_id"] == goal_id:
                goal["current"] = current
                goal["updated_at"] = datetime.now().isoformat()
                
                if current >= goal["target"]:
                    goal["completed"] = True
                    goal["completed_at"] = datetime.now().isoformat()
                
                return self._save_goals(goals)
        
        return False
    
    def mark_completed(self, goal_id: str) -> bool:
        """标记目标完成"""
        goals = self._load_goals()
        
        for goal in goals:
            if goal["goal_id"] == goal_id:
                goal["completed"] = True
                goal["completed_at"] = datetime.now().isoformat()
                goal["updated_at"] = datetime.now().isoformat()
                return self._save_goals(goals)
        
        return False
    
    def delete_goal(self, goal_id: str) -> bool:
        """删除目标"""
        goals = self._load_goals()
        original_len = len(goals)
        goals = [g for g in goals if g["goal_id"] != goal_id]
        
        if len(goals) < original_len:
            return self._save_goals(goals)
        return False
    
    def get_goal_progress(self, goal: Goal) -> Dict:
        """计算目标进度"""
        if goal.target == 0:
            progress = 0
        else:
            progress = (goal.current / goal.target) * 100
        
        remaining = max(0, goal.target - goal.current)
        
        days_left = 0
        try:
            deadline = datetime.strptime(goal.deadline, "%Y-%m-%d")
            days_left = (deadline - datetime.now()).days
        except Exception:
            pass
        
        on_track = goal.completed
        if days_left > 0 and not goal.completed:
            total_days = (datetime.strptime(goal.deadline, "%Y-%m-%d") - 
                         datetime.strptime(goal.created_at[:10], "%Y-%m-%d")).days
            elapsed = total_days - days_left
            if total_days > 0:
                expected_progress = (elapsed / total_days) * 100
                on_track = progress >= expected_progress * 0.9
        
        return {
            "progress": round(min(100, progress), 1),
            "remaining": round(remaining, 1),
            "days_left": days_left,
            "on_track": on_track,
            "completed": goal.completed
        }
    
    # ==================== 马拉松目标 CRUD ====================
    
    def _load_marathon_goals(self) -> List[Dict]:
        """加载马拉松目标"""
        if not os.path.exists(self.marathon_goals_file):
            return []
        try:
            with open(self.marathon_goals_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    
    def _save_marathon_goals(self, goals: List[Dict]) -> bool:
        """保存马拉松目标"""
        try:
            with open(self.marathon_goals_file, 'w', encoding='utf-8') as f:
                json.dump(goals, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def create_marathon_goal(
        self,
        race_name: str,
        race_date: str,
        goal_time: str = None,
        race_type: str = "半程马拉松",
        target_pace: str = None,
        splits: Dict[str, str] = None,
        notes: str = ""
    ) -> MarathonGoal:
        """
        创建马拉松训练目标
        
        Args:
            race_name: 比赛名称（如"北京半马"）
            race_date: 比赛日期（YYYY-MM-DD）
            goal_time: 目标时间（HH:MM:SS），如"02:00:00"
            race_type: 比赛类型（半程马拉松/全程马拉松）
            target_pace: 目标配速（MM:SS），如"5:40"
            splits: 分段策略，如{"前半马": "5:40", "后半马": "5:45"}
            notes: 备注
        
        Returns:
            创建的MarathonGoal对象
        """
        # 计算目标配速
        if goal_time:
            # 根据目标时间反推配速
            if race_type == "半程马拉松":
                total_seconds = self._time_to_seconds(goal_time)
                pace_seconds = total_seconds / 21.0975
                target_pace = self._seconds_to_pace(pace_seconds)
            elif race_type == "全程马拉松":
                total_seconds = self._time_to_seconds(goal_time)
                pace_seconds = total_seconds / 42.195
                target_pace = self._seconds_to_pace(pace_seconds)
        
        # 计算分段配速
        if splits is None:
            if race_type == "半程马拉松" and target_pace:
                splits = {
                    "前半马": target_pace,
                    "后半马": self._add_seconds_to_pace(target_pace, 5)  # 后半马慢5秒
                }
            elif race_type == "全程马拉松" and target_pace:
                splits = {
                    "前21km": target_pace,
                    "后21km": self._add_seconds_to_pace(target_pace, 5)  # 后半马慢5秒
                }
        
        marathon_goal = MarathonGoal(
            goal_id=f"marathon_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            user_id=self.user_id,
            goal_type="马拉松训练",
            goal_name=race_name,
            race_date=race_date,
            race_type=race_type,
            goal_time=goal_time or "",
            target_pace=target_pace or "",
            splits=splits or {},
            current=0,
            target=1,
            unit="场",
            status="active",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            notes=notes
        )
        
        goals = self._load_marathon_goals()
        goals.append(marathon_goal.to_dict())
        self._save_marathon_goals(goals)
        
        return marathon_goal
    
    def get_marathon_goals(self) -> List[MarathonGoal]:
        """获取所有马拉松目标"""
        goals = self._load_marathon_goals()
        return [MarathonGoal.from_dict(g) for g in goals]
    
    def get_active_marathon_goals(self) -> List[MarathonGoal]:
        """获取活跃的马拉松目标"""
        goals = self._load_marathon_goals()
        return [MarathonGoal.from_dict(g) for g in goals 
                if g.get("status", "active") == "active"]
    
    def get_active_marathon_goal(self) -> Optional[MarathonGoal]:
        """获取最近的一场马拉松目标（按日期排序）"""
        active_goals = self.get_active_marathon_goals()
        if not active_goals:
            return None
        
        # 按日期排序，返回最近的
        active_goals.sort(key=lambda x: x.race_date)
        return active_goals[0]
    
    def get_upcoming_marathon_goals(self, limit: int = 2) -> List[MarathonGoal]:
        """获取即将到来的马拉松目标"""
        active = self.get_active_marathon_goals()
        # 过滤出未来7天内的
        upcoming = [g for g in active if g.days_until_race >= 0]
        upcoming.sort(key=lambda x: x.race_date)
        return upcoming[:limit]
    
    def get_days_until_race(self, goal_id: str) -> int:
        """计算距离比赛还有多少天"""
        goals = self._load_marathon_goals()
        for g in goals:
            if g["goal_id"] == goal_id:
                try:
                    race_date = datetime.strptime(g["race_date"], "%Y-%m-%d").date()
                    today = datetime.now().date()
                    return (race_date - today).days
                except Exception:
                    return 0
        return 0
    
    def get_training_phase(self, goal_id: str = None) -> str:
        """根据距离比赛天数返回训练阶段"""
        if goal_id is None:
            goal = self.get_active_marathon_goal()
            if goal is None:
                return "无计划"
            return goal.training_phase
        
        goals = self._load_marathon_goals()
        for g in goals:
            if g["goal_id"] == goal_id:
                try:
                    race_date = datetime.strptime(g["race_date"], "%Y-%m-%d").date()
                    today = datetime.now().date()
                    days = (race_date - today).days
                    
                    if days < 0:
                        return "已结束"
                    elif days == 0:
                        return "比赛日"
                    elif days <= 7:
                        return "比赛周"
                    elif days <= 14:
                        return "减量期"
                    elif days <= 28:
                        return "巅峰期"
                    else:
                        return "基础期"
                except Exception:
                    return "未知"
        return "未找到"
    
    def get_recovery_week_warning(self, goal_id: str = None) -> bool:
        """检查是否需要提醒恢复周（背靠背比赛）"""
        if goal_id is None:
            goal = self.get_active_marathon_goal()
            if goal is None:
                return False
            return goal.is_recovery_week_needed
        
        goals = self._load_marathon_goals()
        for g in goals:
            if g["goal_id"] == goal_id:
                if g.get("race_type") == "全程马拉松":
                    try:
                        race_date = datetime.strptime(g["race_date"], "%Y-%m-%d").date()
                        today = datetime.now().date()
                        days = (race_date - today).days
                        return days <= 7
                    except Exception:
                        pass
        return False
    
    def calculate_suggested_weekly_volume(self, goal_id: str = None) -> Dict:
        """根据训练阶段计算建议周跑量"""
        if goal_id is None:
            goal = self.get_active_marathon_goal()
            if goal is None:
                return {"suggested_km": 0, "phase": "无计划"}
            phase = goal.training_phase
        else:
            phase = self.get_training_phase(goal_id)
        
        # 根据阶段建议跑量
        phase_config = {
            "基础期": {"weekly_km": 50, "long_run_km": 15, "intensity": "低"},
            "巅峰期": {"weekly_km": 60, "long_run_km": 18, "intensity": "中"},
            "减量期": {"weekly_km": 35, "long_run_km": 10, "intensity": "低"},
            "比赛周": {"weekly_km": 15, "long_run_km": 5, "intensity": "极低"},
            "比赛日": {"weekly_km": 0, "long_run_km": 0, "intensity": "比赛"},
        }
        
        config = phase_config.get(phase, phase_config["基础期"])
        config["phase"] = phase
        return config
    
    def update_marathon_goal(self, goal_id: str, **kwargs) -> bool:
        """更新马拉松目标"""
        goals = self._load_marathon_goals()
        
        for i, goal in enumerate(goals):
            if goal["goal_id"] == goal_id:
                for key, value in kwargs.items():
                    if key in goal:
                        goal[key] = value
                goal["updated_at"] = datetime.now().isoformat()
                return self._save_marathon_goals(goals)
        
        return False
    
    def delete_marathon_goal(self, goal_id: str) -> bool:
        """删除马拉松目标"""
        goals = self._load_marathon_goals()
        original_len = len(goals)
        goals = [g for g in goals if g["goal_id"] != goal_id]
        
        if len(goals) < original_len:
            return self._save_marathon_goals(goals)
        return False
    
    def mark_marathon_completed(self, goal_id: str) -> bool:
        """标记马拉松目标完成"""
        return self.update_marathon_goal(goal_id, status="completed")
    
    # ==================== 辅助方法 ====================
    
    @staticmethod
    def _time_to_seconds(time_str: str) -> int:
        """将HH:MM:SS转换为秒"""
        try:
            parts = time_str.split(":")
            if len(parts) == 3:
                h, m, s = parts
                return int(h) * 3600 + int(m) * 60 + int(s)
            elif len(parts) == 2:
                m, s = parts
                return int(m) * 60 + int(s)
        except Exception:
            pass
        return 0
    
    @staticmethod
    def _seconds_to_pace(seconds: float) -> str:
        """将秒数转换为MM:SS格式"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    
    @staticmethod
    def _add_seconds_to_pace(pace: str, add_seconds: int) -> str:
        """给配速增加秒数"""
        try:
            parts = pace.split(":")
            total_seconds = int(parts[0]) * 60 + int(parts[1]) + add_seconds
            return GoalsManager._seconds_to_pace(total_seconds)
        except Exception:
            return pace
    
    # ==================== 报告生成 ====================
    
    def generate_report(self) -> Dict:
        """生成综合目标报告"""
        active = self.get_active_goals()
        completed = self.get_completed_goals()
        marathon_goals = self.get_marathon_goals()
        active_marathon = self.get_active_marathon_goals()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "basic_goals": {
                "active_count": len(active),
                "completed_count": len(completed),
                "active_goals": []
            },
            "marathon_goals": {
                "active_count": len(active_marathon),
                "total_count": len(marathon_goals),
                "active_goals": []
            },
            "summary": ""
        }
        
        # 基础目标
        for goal in active[:5]:
            progress = self.get_goal_progress(goal)
            report["basic_goals"]["active_goals"].append({
                "goal_type": goal.goal_type,
                "current": goal.current,
                "target": goal.target,
                "unit": goal.unit,
                "deadline": goal.deadline,
                **progress
            })
        
        # 马拉松目标
        for goal in active_marathon[:3]:
            report["marathon_goals"]["active_goals"].append({
                "goal_id": goal.goal_id,
                "goal_name": goal.goal_name,
                "race_date": goal.race_date,
                "race_type": goal.race_type,
                "days_until_race": goal.days_until_race,
                "training_phase": goal.training_phase,
                "goal_time": goal.goal_time,
                "target_pace": goal.target_pace
            })
        
        # 总结
        if active_marathon:
            next_race = self.get_active_marathon_goal()
            if next_race:
                report["summary"] = f"下一场比赛：{next_race.goal_name}（{next_race.days_until_race}天后）"
        else:
            report["summary"] = "暂无马拉松计划"
        
        return report


# ==================== 便捷函数 ====================

def create_goal(user_id: str, goal_type: str, target: float, current: float, 
                unit: str, deadline: str) -> Goal:
    """创建基础目标"""
    manager = GoalsManager(user_id)
    return manager.create_goal(goal_type, target, current, unit, deadline)


def create_marathon_goal(
    user_id: str,
    race_name: str,
    race_date: str,
    goal_time: str = None,
    race_type: str = "半程马拉松",
    target_pace: str = None,
    splits: Dict[str, str] = None,
    notes: str = ""
) -> MarathonGoal:
    """创建马拉松目标"""
    manager = GoalsManager(user_id)
    return manager.create_marathon_goal(
        race_name=race_name,
        race_date=race_date,
        goal_time=goal_time,
        race_type=race_type,
        target_pace=target_pace,
        splits=splits,
        notes=notes
    )


def get_goals_report(user_id: str = "default") -> Dict:
    """获取综合目标报告"""
    manager = GoalsManager(user_id)
    return manager.generate_report()


def get_marathon_goals(user_id: str = "default") -> List[MarathonGoal]:
    """获取马拉松目标列表"""
    manager = GoalsManager(user_id)
    return manager.get_marathon_goals()


def get_active_marathon_goal(user_id: str = "default") -> Optional[MarathonGoal]:
    """获取最近的马拉松目标"""
    manager = GoalsManager(user_id)
    return manager.get_active_marathon_goal()


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=== Goals Manager Test ===")
    
    user_id = "test_user"
    manager = GoalsManager(user_id)
    
    # 测试基础目标
    print("\n--- Create Basic Goal ---")
    goal = manager.create_goal(
        goal_type="增肌",
        target=80,
        current=75,
        unit="kg",
        deadline="2026-07-29"
    )
    print(f"Created: {goal.goal_type} {goal.current} → {goal.target} {goal.unit}")
    
    # 测试马拉松目标
    print("\n--- Create Marathon Goal ---")
    marathon = manager.create_marathon_goal(
        race_name="北京半马",
        race_date="2026-04-12",
        goal_time="02:00:00",
        race_type="半程马拉松"
    )
    print(f"Created: {marathon.goal_name}")
    print(f"  Race date: {marathon.race_date}")
    print(f"  Days until race: {marathon.days_until_race}")
    print(f"  Training phase: {marathon.training_phase}")
    print(f"  Target pace: {marathon.target_pace}")
    print(f"  Splits: {marathon.splits}")
    
    # 创建第二个马拉松目标
    print("\n--- Create Second Marathon Goal ---")
    marathon2 = manager.create_marathon_goal(
        race_name="通州全马",
        race_date="2026-04-19",
        goal_time="04:45:00",
        race_type="全程马拉松"
    )
    print(f"Created: {marathon2.goal_name}")
    print(f"  Days until race: {marathon2.days_until_race}")
    print(f"  Training phase: {marathon2.training_phase}")
    print(f"  Needs recovery week: {marathon2.is_recovery_week_needed}")
    
    # 获取报告
    print("\n--- Goals Report ---")
    report = manager.generate_report()
    print(f"Basic goals: {report['basic_goals']['active_count']} active")
    print(f"Marathon goals: {report['marathon_goals']['active_count']} active")
    print(f"Summary: {report['summary']}")
    
    # 测试训练阶段建议
    print("\n--- Suggested Weekly Volume ---")
    for phase in ["基础期", "巅峰期", "减量期", "比赛周", "比赛日"]:
        manager.update_marathon_goal(marathon.goal_id, race_date="2026-05-01")
        suggestion = manager.calculate_suggested_weekly_volume()
        print(f"  {phase}: {suggestion['weekly_km']}km/week, intensity: {suggestion['intensity']}")
        break
    
    # 清理测试数据
    print("\n--- Cleanup ---")
    manager.delete_goal(goal.goal_id)
    manager.delete_marathon_goal(marathon.goal_id)
    manager.delete_marathon_goal(marathon2.goal_id)
    print("Test data cleaned up")
