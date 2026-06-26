"""
Dynamic Planner - 动态训练计划调整
根据恢复状态动态调整训练计划
"""

import os
import json
from datetime import datetime, timedelta
from lib.tz import today_str
from typing import Dict, List, Optional

# 数据路径 - 使用环境变量
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # lib/ -> whoop-guru/
WORKSPACE_DIR = os.environ.get("OPENCLAW_WORKSPACE", os.path.dirname(os.path.dirname(SKILL_DIR)))  # whoop-guru/ -> skill/ -> workspace
PROCESSED_DIR = os.environ.get("WHOOP_DATA_DIR", os.path.join(WORKSPACE_DIR, "data", "processed"))
DATA_FILE = os.path.join(PROCESSED_DIR, "latest.json")


class DynamicPlanner:
    """
    动态训练计划调整器
    
    根据以下因素动态调整：
    - 当前恢复状态
    - 近期训练负荷
    - 睡眠质量
    - HRV趋势
    """
    
    # 强度阈值
    THRESHOLDS = {
        "high_recovery": 75,
        "medium_recovery": 55,
        "low_recovery": 35,
    }
    
    # 高强度阈值
    STRAIN_THRESHOLD = 12
    
    def __init__(self):
        self.deload_weeks = 4  # 减载周期
    
    def load_latest_data(self) -> Dict:
        """加载最新数据"""
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def get_current_status(self) -> Dict:
        """获取当前状态"""
        data = self.load_latest_data()
        
        recovery = data.get("processed", {}).get("recovery", [])
        sleep = data.get("processed", {}).get("sleep", [])
        daily_summary = data.get("daily_summary", {})
        
        current_recovery = recovery[0].get("recovery_score", 50) if recovery else 50
        current_hrv = recovery[0].get("hrv", 40) if recovery else 40
        
        # 获取今日strain从cycles
        cycles = daily_summary.get("cycles", [])
        today_strain = cycles[0].get("strain", 0) if cycles else 0
        
        # 计算本周训练天数从workouts
        workouts = daily_summary.get("workouts", [])
        training_days = len(workouts)
        today_has_training = len([w for w in workouts if w.get("date", "").startswith(today_str())]) > 0 if workouts else False
        
        # 计算睡眠债务
        sleep_debt = 0
        if len(sleep) >= 7:
            total_sleep = sum(s.get("total_in_bed_hours", 0) for s in sleep[-7:])
            sleep_debt = max(0, 7 * 8 - total_sleep)
        
        return {
            "recovery": current_recovery,
            "hrv": current_hrv,
            "today_strain": today_strain,
            "today_has_training": today_has_training,
            "training_days_this_week": training_days,
            "sleep_debt": sleep_debt,
        }
    
    def get_recommended_intensity(self) -> Dict:
        """
        获取推荐训练强度
        
        Returns:
            {
                "intensity": "high/medium/low/rest",
                "description": str,
                "strain_target": str,
                "reason": str
            }
        """
        status = self.get_current_status()
        
        recovery = status["recovery"]
        today_strain = status["today_strain"]
        training_days = status["training_days_this_week"]
        sleep_debt = status["sleep_debt"]
        
        # 特殊情况：今日已训练
        if status["today_has_training"] and today_strain >= 10:
            return {
                "intensity": "rest",
                "description": "今日已完成训练",
                "strain_target": "0",
                "reason": f"今日strain已达{today_strain}，身体得到刺激"
            }
        
        # 根据恢复状态判断
        if recovery >= self.THRESHOLDS["high_recovery"]:
            if training_days < 5:
                return {
                    "intensity": "high",
                    "description": "高强度训练",
                    "strain_target": "12-15",
                    "reason": f"恢复{recovery}%良好，可进行高强度训练"
                }
            else:
                return {
                    "intensity": "medium",
                    "description": "中等强度训练",
                    "strain_target": "8-12",
                    "reason": "本周训练较频繁，建议中等强度"
                }
        
        elif recovery >= self.THRESHOLDS["medium_recovery"]:
            return {
                "intensity": "medium",
                "description": "中等强度训练",
                "strain_target": "8-12",
                "reason": f"恢复{recovery}%一般，适合中等强度"
            }
        
        elif recovery >= self.THRESHOLDS["low_recovery"]:
            return {
                "intensity": "low",
                "description": "轻度活动",
                "strain_target": "5-8",
                "reason": f"恢复{recovery}%偏低，建议轻度活动"
            }
        
        else:
            return {
                "intensity": "rest",
                "description": "完全休息",
                "strain_target": "0-3",
                "reason": f"恢复{recovery}%较差，建议休息"
            }
    
    def should_deload(self) -> Dict:
        """
        判断是否需要减载周
        
        Returns:
            {
                "should_deload": bool,
                "reason": str,
                "deload_type": "active/rest/passive"
            }
        """
        data = self.load_latest_data()
        recovery = data.get("processed", {}).get("recovery", [])
        
        if len(recovery) < 14:
            return {
                "should_deload": False,
                "reason": "数据不足"
            }
        
        # 最近7天 vs 前7天
        recent_7 = [r.get("recovery_score", 50) for r in recovery[:7]]
        older_7 = [r.get("recovery_score", 50) for r in recovery[7:14]]
        
        recent_avg = sum(recent_7) / 7
        older_avg = sum(older_7) / 7
        
        # 判断减载
        if recent_avg < older_avg - 10:
            return {
                "should_deload": True,
                "reason": f"恢复评分下降 ({older_avg:.0f}% → {recent_avg:.0f}%)",
                "deload_type": "active"
            }
        
        # 连续3天低恢复
        low_days = sum(1 for r in recent_7 if r < 40)
        if low_days >= 3:
            return {
                "should_deload": True,
                "reason": f"连续{low_days}天恢复低于40%",
                "deload_type": "passive"
            }
        
        return {
            "should_deload": False,
            "reason": "恢复状态良好，无需减载"
        }
    
    def get_adjusted_plan(self, base_plan: Dict) -> Dict:
        """
        调整基础训练计划
        
        Args:
            base_plan: 基础计划字典
        
        Returns:
            调整后的计划
        """
        recommendation = self.get_recommended_intensity()
        deload = self.should_deload()
        
        adjusted = base_plan.copy()
        adjusted["adjustments"] = []
        
        # 应用强度调整
        if recommendation["intensity"] == "rest":
            adjusted["plan_type"] = "休息日"
            adjusted["adjustments"].append("根据当前恢复状态，建议休息")
        elif recommendation["intensity"] == "low":
            adjusted["plan_type"] = "轻度活动"
            adjusted["strain_target"] = "5-8"
            adjusted["adjustments"].append("恢复偏低，降低强度")
        elif recommendation["intensity"] == "medium":
            adjusted["plan_type"] = "中等强度"
            adjusted["strain_target"] = "8-12"
            adjusted["adjustments"].append("中等强度训练")
        
        # 应用减载
        if deload["should_deload"]:
            adjusted["deload"] = True
            adjusted["deload_type"] = deload["deload_type"]
            adjusted["adjustments"].append(f"减载周: {deload['reason']}")
        
        return adjusted


def get_dynamic_recommendation() -> Dict:
    """获取动态训练建议"""
    planner = DynamicPlanner()
    return planner.get_recommended_intensity()


def check_deload() -> Dict:
    """检查是否需要减载"""
    planner = DynamicPlanner()
    return planner.should_deload()


if __name__ == "__main__":
    print("=== Dynamic Planner ===")
    planner = DynamicPlanner()
    
    print("\n--- Current Status ---")
    status = planner.get_current_status()
    print(f"Recovery: {status['recovery']}%")
    print(f"HRV: {status['hrv']}ms")
    print(f"Today Strain: {status['today_strain']}")
    print(f"Training Days: {status['training_days_this_week']}")
    
    print("\n--- Recommendation ---")
    rec = planner.get_recommended_intensity()
    print(f"Intensity: {rec['intensity']}")
    print(f"Description: {rec['description']}")
    print(f"Reason: {rec['reason']}")
    
    print("\n--- Deload Check ---")
    deload = planner.should_deload()
    print(f"Should Deload: {deload['should_deload']}")
    print(f"Reason: {deload['reason']}")
