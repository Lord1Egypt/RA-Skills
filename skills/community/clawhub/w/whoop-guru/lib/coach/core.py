"""
教练核心模块
整合WHOOP数据和Prompt模板，提供AI教练功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.prompts.training import get_training_prompt
from lib.user_profile import UserProfile, get_user_profile, save_user_profile


class WhoopData:
    """WHOOP数据获取包装"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.data_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            "data", "processed"
        )
    
    def get_latest_recovery(self) -> dict:
        """获取最新恢复数据"""
        import json
        try:
            with open(os.path.join(self.data_dir, "latest.json"), 'r') as f:
                data = json.load(f)
                if 'processed' in data and 'recovery' in data['processed']:
                    records = data['processed']['recovery']
                    if records:
                        return records[0]
            with open(os.path.join(self.data_dir, "analysis.json"), 'r') as f:
                data = json.load(f)
                return data.get('recovery', {})
        except Exception:
            return {"recovery_score": 50}
    
    def get_latest_sleep(self) -> dict:
        """获取最新睡眠数据"""
        import json
        try:
            with open(os.path.join(self.data_dir, "analysis.json"), 'r') as f:
                data = json.load(f)
                return data.get('sleep', {})
        except Exception:
            return {}
    
    def get_current_strain(self) -> dict:
        """获取当前训练负荷"""
        import json
        try:
            with open(os.path.join(self.data_dir, "analysis.json"), 'r') as f:
                data = json.load(f)
                return data.get('training', {})
        except Exception:
            return {"avg_strain": 10}
    
    def get_30day_data(self) -> dict:
        """获取30天数据摘要"""
        import json
        try:
            with open(os.path.join(self.data_dir, "analysis.json"), 'r') as f:
                data = json.load(f)
                result = {}
                result['avg_recovery'] = data.get('recovery', {}).get('avg_recovery', 50)
                result['avg_hrv'] = data.get('recovery', {}).get('avg_hrv', 40)
                result['avg_rhr'] = data.get('recovery', {}).get('avg_rhr', 55)
                result['sleep_debt'] = data.get('sleep', {}).get('sleep_debt', 0)
                result['training_days'] = data.get('training', {}).get('workout_count', 0)
                result['hrv_trend'] = data.get('recovery', {}).get('trend', 'stable')
                result['sleep_quality'] = data.get('sleep', {}).get('quality', 'normal')
                return result
        except Exception:
            return {"avg_recovery": 50}
    
    def get_90day_summary(self) -> dict:
        """获取90天数据摘要"""
        return self.get_30day_data()


class CoachCore:
    """
    AI教练核心
    负责整合数据和Prompt，生成个性化方案
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.profile = get_user_profile(user_id)
        self.whoop = WhoopData(user_id)
    
    def generate_daily_plan(self) -> str:
        """生成今日训练计划"""
        recovery = self.whoop.get_latest_recovery()
        sleep = self.whoop.get_latest_sleep()
        strain = self.whoop.get_current_strain()
        
        recovery_status = recovery.get('recovery_score', 50)
        
        if recovery_status >= 80:
            body_status = "优秀，可以进行高强度训练"
            recommended_type = "力量训练（胸/背/腿）"
            intensity = "高强度"
        elif recovery_status >= 60:
            body_status = "良好，可以进行中等强度训练"
            recommended_type = "上肢或下肢训练"
            intensity = "中等强度"
        elif recovery_status >= 40:
            body_status = "一般，建议轻度活动"
            recommended_type = "慢走或瑜伽"
            intensity = "低强度"
        else:
            body_status = "较差，建议休息或完全恢复"
            recommended_type = "休息或轻度拉伸"
            intensity = "极低强度"
        
        sleep_debt = sleep.get('sleep_debt', 0) if sleep else 0
        
        data = {
            "recovery": recovery_status,
            "recent_strain": strain.get('avg_strain', 10),
            "sleep_debt": sleep_debt,
            "goal": self.profile.goal if self.profile else "增肌",
            "available_time": self.profile.available_time if self.profile else 60,
            "body_status": body_status,
            "recommended_type": recommended_type,
            "intensity": intensity,
            "exercises": self._get_exercises_by_type(recommended_type),
            "sets_reps": self._get_sets_reps(intensity),
            "cautions": self._get_cautions(recovery_status, sleep_debt)
        }
        
        return get_training_prompt("daily", data)
    
    def generate_16_week_plan(self) -> str:
        """生成16周计划"""
        if not self.profile:
            return "请先设置用户档案"
        
        whoop_summary = self.whoop.get_90day_summary()
        
        data = {
            "experience": self.profile.experience_years,
            "body_type": f"体重{self.profile.body_weight}kg" if self.profile.body_weight else "未知",
            "goal": self.profile.goal,
            "avg_recovery": whoop_summary.get('avg_recovery', 50),
            "compliance": 80,
            "sleep_score": whoop_summary.get('avg_sleep_quality', 70),
            "max_strain": whoop_summary.get('max_strain', 15)
        }
        
        return get_training_prompt("16week", data)
    
    def generate_plateau_break(self, event: str, max_weight: float) -> str:
        """生成平台期突破计划"""
        whoop_data = self.whoop.get_30day_data()
        
        data = {
            "event": event,
            "max_weight": max_weight,
            "body_weight": self.profile.body_weight if self.profile else 70,
            "goal_weight": self.profile.target_weight if self.profile else 75,
            "recovery": whoop_data.get('avg_recovery', 50),
            "training_frequency": whoop_data.get('training_days', 4),
            "hrv_trend": whoop_data.get('hrv_trend', 'stable'),
            "sleep_quality": whoop_data.get('sleep_quality', 'normal')
        }
        
        return get_training_prompt("plateau", data)
    
    def generate_weakpoint_plan(self, weak_point: str, strong_point: str) -> str:
        """生成弱项诊断计划"""
        data = {
            "weak_point": weak_point,
            "strong_point": strong_point,
            "related_metric": weak_point,
            "hr_recovery_time": "正常",
            "hrv_change": "正常",
            "fatigue_level": "moderate"
        }
        
        return get_training_prompt("weakpoint", data)
    
    def generate_recovery_plan(self) -> str:
        """生成恢复优化计划"""
        whoop_summary = self.whoop.get_30day_data()
        
        data = {
            "days_per_week": self.profile.days_per_week if self.profile else 4,
            "avg_recovery": whoop_summary.get('avg_recovery', 50),
            "avg_hrv": whoop_summary.get('avg_hrv', 40),
            "avg_rhr": whoop_summary.get('avg_rhr', 55),
            "sleep_debt": whoop_summary.get('sleep_debt', 0)
        }
        
        return get_training_prompt("recovery", data)
    
    def generate_injury_plan(self, injury_area: str, injury_movement: str) -> str:
        """生成伤病预防计划"""
        whoop_data = self.whoop.get_30day_data()
        
        data = {
            "injury_area": injury_area,
            "injury_movement": injury_movement,
            "hr_recovery_change": whoop_data.get('hr_recovery_change', 0),
            "related_training": whoop_data.get('related_training', 0),
            "recovery_trend": whoop_data.get('recovery_trend', 'stable')
        }
        
        return get_training_prompt("injury", data)
    
    def generate_tracking_framework(self) -> str:
        """生成追踪框架"""
        whoop_data = self.whoop.get_30day_data()
        
        data = {
            "body_weight": self.profile.body_weight if self.profile else 70,
            "squat": self.profile.max_squat if self.profile else 100,
            "bench": self.profile.max_bench if self.profile else 80,
            "frequency": whoop_data.get('training_days', 4)
        }
        
        return get_training_prompt("tracking", data)
    
    def _get_exercises_by_type(self, training_type: str) -> str:
        """根据训练类型返回动作"""
        exercises = {
            "力量训练（胸/背/腿）": "卧推、上斜哑铃卧推、高位下拉、硬拉、深蹲",
            "上肢或下肢训练": "卧推、臂屈伸、深蹲、腿举",
            "慢走或瑜伽": "慢走30分钟，全身拉伸",
            "休息或轻度拉伸": "全身拉伸、泡沫轴放松"
        }
        return exercises.get(training_type, "待定")
    
    def _get_sets_reps(self, intensity: str) -> str:
        """根据强度返回组数次数"""
        sets_reps = {
            "高强度": "4-5组 x 6-8次",
            "中等强度": "3-4组 x 8-12次",
            "低强度": "2-3组 x 12-15次",
            "极低强度": "1-2组 x 15-20次"
        }
        return sets_reps.get(intensity, "待定")
    
    def _get_cautions(self, recovery: float, sleep_debt: float) -> str:
        """获取注意事项"""
        cautions = []
        if recovery < 40:
            cautions.append("⚠️ 恢复较低，注意监控身体状态")
        if sleep_debt > 20:
            cautions.append("⚠️ 睡眠债务较重，建议增加睡眠时间")
        if not cautions:
            cautions.append("✅ 状态良好，按计划执行")
        return " | ".join(cautions)


def get_coach(user_id: str) -> CoachCore:
    """获取教练实例"""
    return CoachCore(user_id)
