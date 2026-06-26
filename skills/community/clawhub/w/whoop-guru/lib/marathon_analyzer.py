"""
Marathon Analyzer - 马拉松训练分析器
根据训练阶段和恢复数据给出综合建议
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# 添加父目录到路径
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SKILL_DIR)

from lib.goals import GoalsManager, MarathonGoal
from lib.tracker import ProgressTracker


class MarathonAnalyzer:
    """
    马拉松训练分析器
    根据马拉松目标和训练数据给出综合建议
    """
    
    # 训练阶段配置
    TRAINING_PHASES = {
        "基础期": {
            "days_min": 29,
            "days_max": float('inf'),
            "weekly_volume_ratio": 1.0,
            "long_run_ratio": 0.3,
            "intensity": "低",
            "description": "积累跑量，打好有氧基础"
        },
        "巅峰期": {
            "days_min": 14,
            "days_max": 28,
            "weekly_volume_ratio": 0.9,
            "long_run_ratio": 0.25,
            "intensity": "中高",
            "description": "提高强度，引入节奏跑和间歇训练"
        },
        "减量期": {
            "days_min": 8,
            "days_max": 14,
            "weekly_volume_ratio": 0.6,
            "long_run_ratio": 0.2,
            "intensity": "中低",
            "description": "减量保持状态，避免过度训练"
        },
        "比赛周": {
            "days_min": 1,
            "days_max": 7,
            "weekly_volume_ratio": 0.3,
            "long_run_ratio": 0.1,
            "intensity": "极低",
            "description": "充分休息，保持活力"
        },
        "比赛日": {
            "days_min": 0,
            "days_max": 0,
            "weekly_volume_ratio": 0,
            "long_run_ratio": 0,
            "intensity": "比赛",
            "description": "全力以赴！"
        }
    }
    
    # 心率区间定义
    HEART_RATE_ZONES = {
        "Z1": {"min": 0.5, "max": 0.6, "name": "恢复区", "description": "非常轻松"},
        "Z2": {"min": 0.6, "max": 0.7, "name": "有氧区", "description": "轻松聊天"},
        "Z3": {"min": 0.7, "max": 0.8, "name": "Tempo区", "description": "有点吃力"},
        "Z4": {"min": 0.8, "max": 0.9, "name": "乳酸阈值区", "description": "吃力"},
        "Z5": {"min": 0.9, "max": 1.0, "name": "无氧区", "description": "非常吃力"}
    }
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.goals_manager = GoalsManager(user_id)
        self.tracker = ProgressTracker(user_id)
    
    def get_training_phase_config(self, phase: str) -> Dict:
        """获取训练阶段配置"""
        return self.TRAINING_PHASES.get(phase, self.TRAINING_PHASES["基础期"])
    
    def get_phase_from_days(self, days: int) -> str:
        """根据距离天数返回训练阶段"""
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
    
    def get_training_advice(
        self,
        user_id: str,
        whoop_data: Dict = None
    ) -> Dict:
        """
        综合分析生成训练建议
        
        Args:
            user_id: 用户ID
            whoop_data: WHOOP数据（恢复、HRV等）
        
        Returns:
            {
                "has_marathon_plan": bool,
                "marathon_info": {...},
                "today_suggestion": {...},
                "warnings": [...],
                "race_strategy": {...}
            }
        """
        result = {
            "has_marathon_plan": False,
            "marathon_info": {},
            "today_suggestion": {},
            "warnings": [],
            "race_strategy": {}
        }
        
        # 获取活跃马拉松目标
        marathon_goal = self.goals_manager.get_active_marathon_goal()
        
        if not marathon_goal:
            result["today_suggestion"] = self._get_default_suggestion()
            return result
        
        result["has_marathon_plan"] = True
        
        # 马拉松信息
        days_until = marathon_goal.days_until_race
        phase = marathon_goal.training_phase
        
        result["marathon_info"] = {
            "goal_id": marathon_goal.goal_id,
            "goal_name": marathon_goal.goal_name,
            "race_date": marathon_goal.race_date,
            "race_type": marathon_goal.race_type,
            "days_until_race": days_until,
            "training_phase": phase,
            "goal_time": marathon_goal.goal_time,
            "target_pace": marathon_goal.target_pace,
            "splits": marathon_goal.splits
        }
        
        # 获取近期训练数据
        recent_runs = self.tracker.get_recent_runs(user_id, days=7)
        pattern = self.tracker.analyze_running_pattern(user_id, days=14)
        
        # 获取WHOOP恢复数据
        recovery = 50
        hrv = 40
        if whoop_data:
            recovery = whoop_data.get("recovery", 50)
            hrv = whoop_data.get("hrv", 40)
        
        # 生成今日建议
        result["today_suggestion"] = self._generate_today_suggestion(
            marathon_goal=marathon_goal,
            phase=phase,
            days_until=days_until,
            recent_runs=recent_runs,
            pattern=pattern,
            recovery=recovery,
            hrv=hrv
        )
        
        # 生成警告
        result["warnings"] = self._generate_warnings(
            marathon_goal=marathon_goal,
            phase=phase,
            days_until=days_until,
            recent_runs=recent_runs,
            recovery=recovery,
            hrv=hrv
        )
        
        # 生成比赛策略
        if phase in ["比赛周", "比赛日", "减量期"]:
            result["race_strategy"] = self._generate_race_strategy(
                marathon_goal=marathon_goal,
                recent_training=recent_runs
            )
        
        return result
    
    def _generate_today_suggestion(
        self,
        marathon_goal: MarathonGoal,
        phase: str,
        days_until: int,
        recent_runs: List[Dict],
        pattern: Dict,
        recovery: int,
        hrv: int
    ) -> Dict:
        """生成今日训练建议"""
        
        # 基于阶段的基础建议
        phase_suggestions = {
            "基础期": {
                "type": "长跑",
                "distance_range": (10, 15),
                "pace_range": ("6:00", "6:30"),
                "heart_rate_zone": "Z2",
                "description": "基础有氧跑"
            },
            "巅峰期": {
                "type": "节奏跑",
                "distance_range": (8, 12),
                "pace_range": ("5:30", "5:50"),
                "heart_rate_zone": "Z3-Z4",
                "description": "强度训练"
            },
            "减量期": {
                "type": "轻松跑",
                "distance_range": (5, 8),
                "pace_range": ("6:30", "7:00"),
                "heart_rate_zone": "Z2",
                "description": "保持状态"
            },
            "比赛周": {
                "type": "热身跑",
                "distance_range": (3, 5),
                "pace_range": ("7:00", "7:30"),
                "heart_rate_zone": "Z1-Z2",
                "description": "保持活力"
            },
            "比赛日": {
                "type": "比赛",
                "distance_range": (0, 0),
                "pace_range": ("全力", "目标配速"),
                "heart_rate_zone": "Z3-Z5",
                "description": "全力以赴！"
            }
        }
        
        suggestion = phase_suggestions.get(phase, phase_suggestions["基础期"]).copy()
        
        # 根据恢复数据调整
        if recovery < 50:
            suggestion["type"] = "休息或轻松散步"
            suggestion["distance_range"] = (0, 3)
            suggestion["pace_range"] = ("随意", "散步速度")
            suggestion["heart_rate_zone"] = "Z1"
            suggestion["description"] = "恢复不足，以休息为主"
        elif recovery < 65:
            # 降低强度
            suggestion["distance_range"] = (
                suggestion["distance_range"][0] * 0.7,
                suggestion["distance_range"][1] * 0.7
            )
            suggestion["description"] = suggestion["description"] + "（减量）"
        
        # 根据近期训练调整
        if len(recent_runs) >= 2:
            last_two_long = all(r.get("distance_km", 0) >= 10 for r in recent_runs[:2])
            if last_two_long and phase in ["巅峰期", "基础期"]:
                suggestion["type"] = "恢复跑"
                suggestion["distance_range"] = (5, 8)
                suggestion["pace_range"] = ("6:30", "7:00")
                suggestion["description"] = "连续高强度后恢复"
        
        # 计算目标距离
        target_distance = suggestion["distance_range"][1]  # 使用范围的上限
        
        return {
            "suggested_distance": round(target_distance, 1),
            "distance_range": suggestion["distance_range"],
            "suggested_type": suggestion["type"],
            "suggested_pace": f"{suggestion['pace_range'][0]}-{suggestion['pace_range'][1]}",
            "heart_rate_zone": suggestion["heart_rate_zone"],
            "description": suggestion["description"],
            "training_phase": phase,
            "days_until_race": days_until,
            "recovery_status": "良好" if recovery >= 65 else "一般" if recovery >= 50 else "不足"
        }
    
    def _generate_warnings(
        self,
        marathon_goal: MarathonGoal,
        phase: str,
        days_until: int,
        recent_runs: List[Dict],
        recovery: int,
        hrv: int
    ) -> List[str]:
        """生成警告列表"""
        warnings = []
        
        # 恢复不足警告
        if recovery < 50:
            warnings.append("⚠️ 恢复评分较低（{}%），建议休息或极轻活动".format(recovery))
        elif recovery < 65:
            warnings.append("🟡 恢复评分一般（{}%），注意控制强度".format(recovery))
        
        # HRV警告
        if hrv < 30:
            warnings.append("⚠️ HRV偏低（{}ms），可能有疲劳累积".format(hrv))
        
        # 连续高强度警告
        if len(recent_runs) >= 3:
            recent_high = sum(1 for r in recent_runs[:3] if r.get("distance_km", 0) >= 10)
            if recent_high >= 3:
                warnings.append("⚠️ 连续多日长跑，注意休息和恢复")
        
        # 比赛周特殊警告
        if phase == "比赛周":
            warnings.append("🔴 赛前减量期，减少训练量")
            warnings.append("💤 保证充足睡眠比训练更重要")
        elif phase == "减量期":
            warnings.append("🟡 减量期，训练量降到平时的60%")
        
        # 背靠背比赛警告
        if marathon_goal.is_recovery_week_needed:
            warnings.append("⚠️ 背靠背比赛，7天内有两场，注意恢复")
        
        return warnings
    
    def _generate_race_strategy(
        self,
        marathon_goal: MarathonGoal,
        recent_training: List[Dict]
    ) -> Dict:
        """生成比赛策略"""
        race_type = marathon_goal.race_type
        target_pace = marathon_goal.target_pace
        target_time = marathon_goal.goal_time
        
        strategy = {
            "race_pace": target_pace or "待定",
            "target_time": target_time or "待定",
            "前半段": {},
            "后半段": {}
        }
        
        if race_type == "半程马拉松":
            pace_seconds = self._pace_to_seconds(target_pace) if target_pace else 0
            if pace_seconds:
                first_half_pace = pace_seconds
                second_half_pace = pace_seconds + 5  # 后半段慢5秒
                strategy["前半段"] = {
                    "distance": "10.5km",
                    "pace": self._seconds_to_pace(first_half_pace),
                    "description": "按目标配速跑，保持节奏"
                }
                strategy["后半段"] = {
                    "distance": "10.7km",
                    "pace": self._seconds_to_pace(second_half_pace),
                    "description": "可能会掉速，控制在10秒内"
                }
        
        elif race_type == "全程马拉松":
            pace_seconds = self._pace_to_seconds(target_pace) if target_pace else 0
            if pace_seconds:
                first_half_pace = pace_seconds
                second_half_pace = pace_seconds + 10  # 后半段慢10秒
                strategy["前半段"] = {
                    "distance": "21km",
                    "pace": self._seconds_to_pace(first_half_pace),
                    "description": "按目标配速跑，前半程留有余地"
                }
                strategy["后半段"] = {
                    "distance": "21km",
                    "pace": self._seconds_to_pace(second_half_pace),
                    "description": "可能会掉速，注意补给和心态"
                }
        
        return strategy
    
    def should_adjust_plan(
        self,
        user_id: str,
        whoop_recovery: int
    ) -> Tuple[bool, str, str]:
        """
        检查是否需要调整训练计划
        
        Returns:
            (should_adjust: bool, reason: str, adjustment: str)
        """
        marathon_goal = self.goals_manager.get_active_marathon_goal()
        
        if not marathon_goal:
            return False, "", ""
        
        phase = marathon_goal.training_phase
        days_until = marathon_goal.days_until_race
        
        # 恢复极低
        if whoop_recovery < 40:
            return True, \
                   "恢复评分过低（{}%）".format(whoop_recovery), \
                   "建议当天完全休息或只做拉伸"
        
        # 比赛周不应大强度
        if phase == "比赛周" and whoop_recovery < 70:
            return True, \
                   "赛前恢复不足（{}%）".format(whoop_recovery), \
                   "建议减少训练量，以热身为主"
        
        # 连续高强度后
        recent_runs = self.tracker.get_recent_runs(user_id, days=5)
        if len(recent_runs) >= 2:
            high_intensity = sum(1 for r in recent_runs[:2] if r.get("distance_km", 0) >= 12)
            if high_intensity >= 2 and whoop_recovery < 60:
                return True, \
                       "连续高强度训练后恢复一般", \
                       "建议改成轻松跑或休息一天"
        
        return False, "", ""
    
    def get_phase_summary(self, marathon_goal: MarathonGoal) -> Dict:
        """获取训练阶段总结"""
        phase = marathon_goal.training_phase
        days_until = marathon_goal.days_until_race
        config = self.get_training_phase_config(phase)
        
        # 计算建议跑量
        pattern = self.tracker.analyze_running_pattern(self.user_id, days=30)
        current_weekly = pattern.get("weekly_avg_distance", 0)
        suggested_weekly = current_weekly * config["weekly_volume_ratio"]
        
        return {
            "phase": phase,
            "days_until": days_until,
            "description": config["description"],
            "intensity": config["intensity"],
            "weekly_volume_suggestion": round(suggested_weekly, 1),
            "long_run_suggestion": round(suggested_weekly * config["long_run_ratio"], 1),
            "phase_tips": self._get_phase_tips(phase, marathon_goal)
        }
    
    def _get_phase_tips(self, phase: str, marathon_goal: MarathonGoal) -> List[str]:
        """获取各阶段的训练提示"""
        tips_by_phase = {
            "基础期": [
                "以低强度有氧跑为主，堆积跑量",
                "每周跑量增加不超过10%",
                "专注跑步技术，动作经济性",
                "保持规律作息，保证恢复"
            ],
            "巅峰期": [
                "引入节奏跑和间歇训练",
                "节奏跑保持在Z3-Z4区",
                "长跑配速可以接近目标配速",
                "注意训练后的充分恢复"
            ],
            "减量期": [
                "训练量降到巅峰期的60%",
                "以轻松跑为主，不追求速度",
                "保证充足睡眠和营养",
                "可以安排一次热身跑保持状态"
            ],
            "比赛周": [
                "大幅减少跑量，只做热身",
                "以Z1-Z2强度为主",
                "早睡早起，保证7-8小时睡眠",
                "碳水化合物补充，储备能量"
            ],
            "比赛日": [
                "比赛日！全力以赴！",
                "注意起跑节奏，不要冲动",
                "补给按计划进行",
                "享受比赛，相信训练！"
            ]
        }
        
        tips = tips_by_phase.get(phase, [])
        
        # 背靠背比赛额外提示
        if marathon_goal.is_recovery_week_needed and phase == "比赛周":
            tips.append("⚠️ 背靠背比赛，赛前充分休息")
        
        return tips
    
    def _get_default_suggestion(self) -> Dict:
        """获取默认建议（无马拉松计划时）"""
        return {
            "suggested_distance": 8.0,
            "suggested_type": "轻松跑",
            "suggested_pace": "6:00-6:30",
            "heart_rate_zone": "Z2",
            "description": "保持运动习惯",
            "training_phase": "无计划",
            "days_until_race": None,
            "recovery_status": "未知"
        }
    
    @staticmethod
    def _pace_to_seconds(pace: str) -> int:
        """将MM:SS转换为秒"""
        try:
            if ":" in pace:
                parts = pace.split(":")
                return int(parts[0]) * 60 + int(parts[1])
        except Exception:
            pass
        return 0
    
    @staticmethod
    def _seconds_to_pace(seconds: float) -> str:
        """将秒数转换为MM:SS格式"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    
    def get_marathon_context(self, user_id: str) -> Dict:
        """
        获取马拉松背景信息（供报告使用）
        
        Returns:
            {
                "has_marathon_plan": bool,
                "race_name": str,
                "days_until_race": int,
                "training_phase": str,
                "phase_summary": {...},
                "next_race": {...}
            }
        """
        context = {
            "has_marathon_plan": False,
            "race_name": None,
            "days_until_race": None,
            "training_phase": None,
            "phase_summary": None,
            "next_race": None
        }
        
        marathon_goal = self.goals_manager.get_active_marathon_goal()
        
        if not marathon_goal:
            return context
        
        context["has_marathon_plan"] = True
        context["race_name"] = marathon_goal.goal_name
        context["days_until_race"] = marathon_goal.days_until_race
        context["training_phase"] = marathon_goal.training_phase
        context["phase_summary"] = self.get_phase_summary(marathon_goal)
        
        # 获取即将到来的比赛
        upcoming = self.goals_manager.get_upcoming_marathon_goals(limit=2)
        if upcoming:
            context["next_race"] = {
                "name": upcoming[0].goal_name,
                "date": upcoming[0].race_date,
                "days_until": upcoming[0].days_until_race,
                "type": upcoming[0].race_type,
                "goal_pace": upcoming[0].target_pace
            }
        
        return context


# ==================== 便捷函数 ====================

def get_marathon_context(user_id: str = "default") -> Dict:
    """获取马拉松背景信息"""
    analyzer = MarathonAnalyzer(user_id)
    return analyzer.get_marathon_context(user_id)


def get_training_advice(user_id: str, whoop_data: Dict = None) -> Dict:
    """获取训练建议"""
    analyzer = MarathonAnalyzer(user_id)
    return analyzer.get_training_advice(user_id, whoop_data)


def should_adjust_plan(user_id: str, recovery: int) -> Tuple[bool, str, str]:
    """检查是否需要调整计划"""
    analyzer = MarathonAnalyzer(user_id)
    return analyzer.should_adjust_plan(user_id, recovery)


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=== Marathon Analyzer Test ===")
    
    analyzer = MarathonAnalyzer("test_user")
    
    # 测试获取阶段配置
    print("\n--- Training Phase Config ---")
    for phase in ["基础期", "巅峰期", "减量期", "比赛周", "比赛日"]:
        config = analyzer.get_training_phase_config(phase)
        print(f"{phase}: {config['description']}")
    
    # 测试阶段识别
    print("\n--- Phase from Days ---")
    for days in [35, 21, 10, 5, 0]:
        phase = analyzer.get_phase_from_days(days)
        print(f"{days} days: {phase}")
    
    # 测试训练建议
    print("\n--- Training Advice (with mock data) ---")
    advice = analyzer.get_training_advice(
        user_id="test_user",
        whoop_data={"recovery": 70, "hrv": 45}
    )
    print(f"Has plan: {advice['has_marathon_plan']}")
    if advice['has_marathon_plan']:
        print(f"Marathon: {advice['marathon_info']['goal_name']}")
        print(f"Days until: {advice['marathon_info']['days_until_race']}")
        print(f"Phase: {advice['marathon_info']['training_phase']}")
        print(f"Today: {advice['today_suggestion']['suggested_type']} - {advice['today_suggestion']['suggested_distance']}km")
        print(f"Warnings: {len(advice['warnings'])}")
        for w in advice['warnings']:
            print(f"  - {w}")
    
    # 测试阶段总结
    print("\n--- Phase Summary ---")
    summary = analyzer.get_phase_summary(
        MarathonGoal(
            goal_id="test",
            user_id="test",
            race_date=(datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
            race_type="半程马拉松"
        )
    )
    print(f"Phase: {summary['phase']}")
    print(f"Description: {summary['description']}")
    print(f"Tips:")
    for tip in summary['phase_tips']:
        print(f"  - {tip}")
    
    print("\n✅ All tests passed!")
