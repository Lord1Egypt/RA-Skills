"""
Marathon Extensions for GoalsManager
Marathon training goal support
"""

import os
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field


@dataclass
class MarathonGoal:
    """马拉松目标数据类"""
    goal_id: str
    user_id: str
    goal_type: str = "马拉松训练"
    goal_name: str = ""
    race_date: str = ""
    race_type: str = "半程马拉松"
    goal_time: str = ""
    target_pace: str = ""
    splits: dict = field(default_factory=dict)
    current: float = 0
    target: float = 1
    unit: str = "场"
    status: str = "active"
    created_at: str = ""
    updated_at: str = ""
    notes: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()
    
    @property
    def days_until_race(self) -> int:
        try:
            race_date_obj = datetime.strptime(self.race_date, "%Y-%m-%d").date()
            today = datetime.now().date()
            return (race_date_obj - today).days
        except Exception:
            return 0
    
    @property
    def training_phase(self) -> str:
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
        if self.race_type == "全程马拉松" and self.days_until_race <= 7:
            return True
        return False
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MarathonGoal':
        return cls(**data)


def _time_to_seconds(time_str: str) -> int:
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


def _seconds_to_pace(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def _add_seconds_to_pace(pace: str, add_seconds: int) -> str:
    try:
        parts = pace.split(":")
        total_seconds = int(parts[0]) * 60 + int(parts[1]) + add_seconds
        return _seconds_to_pace(total_seconds)
    except Exception:
        return pace


class MarathonGoalsManager:
    """马拉松目标管理器扩展"""
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.goals_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "profiles"
        )
        os.makedirs(self.goals_dir, exist_ok=True)
        self.goals_file = os.path.join(self.goals_dir, f"marathon_goals_{user_id}.json")
    
    def _load_goals(self) -> list:
        if not os.path.exists(self.goals_file):
            return []
        try:
            with open(self.goals_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    
    def _save_goals(self, goals: list) -> bool:
        try:
            with open(self.goals_file, 'w', encoding='utf-8') as f:
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
        splits: dict = None,
        notes: str = ""
    ) -> MarathonGoal:
        """创建马拉松训练目标"""
        # 计算目标配速
        if goal_time:
            total_seconds = _time_to_seconds(goal_time)
            if race_type == "半程马拉松":
                pace_seconds = total_seconds / 21.0975
                target_pace = _seconds_to_pace(pace_seconds)
            elif race_type == "全程马拉松":
                pace_seconds = total_seconds / 42.195
                target_pace = _seconds_to_pace(pace_seconds)
        
        # 计算分段配速
        if splits is None and target_pace:
            if race_type == "半程马拉松":
                splits = {
                    "前半马": target_pace,
                    "后半马": _add_seconds_to_pace(target_pace, 5)
                }
            elif race_type == "全程马拉松":
                splits = {
                    "前21km": target_pace,
                    "后21km": _add_seconds_to_pace(target_pace, 5)
                }
        
        goal = MarathonGoal(
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
        
        goals = self._load_goals()
        goals.append(goal.to_dict())
        self._save_goals(goals)
        
        return goal
    
    def get_marathon_goals(self) -> list:
        goals = self._load_goals()
        return [MarathonGoal.from_dict(g) for g in goals]
    
    def get_active_marathon_goals(self) -> list:
        goals = self._load_goals()
        return [MarathonGoal.from_dict(g) for g in goals if g.get("status", "active") == "active"]
    
    def get_active_marathon_goal(self) -> MarathonGoal:
        active = self.get_active_marathon_goals()
        if not active:
            return None
        active.sort(key=lambda x: x.race_date)
        return active[0]
    
    def get_upcoming_marathon_goals(self, limit: int = 2) -> list:
        active = self.get_active_marathon_goals()
        upcoming = [g for g in active if g.days_until_race >= 0]
        upcoming.sort(key=lambda x: x.race_date)
        return upcoming[:limit]
    
    def update_marathon_goal(self, goal_id: str, **kwargs) -> bool:
        goals = self._load_goals()
        for i, goal in enumerate(goals):
            if goal["goal_id"] == goal_id:
                for key, value in kwargs.items():
                    if key in goal:
                        goal[key] = value
                goal["updated_at"] = datetime.now().isoformat()
                return self._save_goals(goals)
        return False
    
    def delete_marathon_goal(self, goal_id: str) -> bool:
        goals = self._load_goals()
        original_len = len(goals)
        goals = [g for g in goals if g["goal_id"] != goal_id]
        if len(goals) < original_len:
            return self._save_goals(goals)
        return False
    
    def mark_marathon_completed(self, goal_id: str) -> bool:
        return self.update_marathon_goal(goal_id, status="completed")
    
    def generate_report(self) -> dict:
        active = self.get_active_marathon_goals()
        all_goals = self.get_marathon_goals()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "active_count": len(active),
            "total_count": len(all_goals),
            "active_goals": []
        }
        
        for goal in active[:5]:
            report["active_goals"].append({
                "goal_id": goal.goal_id,
                "goal_name": goal.goal_name,
                "race_date": goal.race_date,
                "race_type": goal.race_type,
                "days_until_race": goal.days_until_race,
                "training_phase": goal.training_phase,
                "goal_time": goal.goal_time,
                "target_pace": goal.target_pace
            })
        
        return report
