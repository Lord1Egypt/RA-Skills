"""
ML预测模块
用于训练效果预测、恢复预测、动态调整
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class RecoveryPredictor:
    """
    恢复预测器
    基于历史数据预测明日恢复状态
    """
    
    def __init__(self, data_dir: str = "data/processed"):
        self.data_dir = data_dir
        self.model_weights = {
            "previous_recovery": 0.3,
            "hrv_trend": 0.25,
            "sleep_quality": 0.2,
            "training_strain": 0.15,
            "rest_days": 0.1
        }
    
    def predict_next_recovery(self, days: int = 7) -> Dict:
        """
        预测未来N天的恢复状态
        
        Args:
            days: 预测天数
        
        Returns:
            预测结果字典
        """
        history = self._load_recent_history(days * 2)
        
        if len(history) < 3:
            return {
                "prediction": 50,
                "confidence": "low",
                "reason": "数据不足"
            }
        
        # 计算加权预测
        weights = self.model_weights
        score = 0
        
        # 基础恢复分
        recent_avg = sum(h.get("recovery_score", 50) for h in history) / len(history)
        score += recent_avg * weights["previous_recovery"]
        
        # HRV趋势
        hrv_trend = self._calculate_trend([h.get("hrv", 40) for h in history])
        score += hrv_trend * weights["hrv_trend"]
        
        # 睡眠质量
        sleep_avg = sum(h.get("sleep_score", 70) for h in history) / len(history)
        score += sleep_avg * weights["sleep_quality"]
        
        # 最近训练强度
        strain_avg = sum(h.get("strain", 10) for h in history) / len(history)
        strain_factor = max(0, 1 - strain_avg / 20)  # 强度越高，恢复越慢
        score += strain_factor * 100 * weights["training_strain"]
        
        # 休息天数
        rest_days = sum(1 for h in history if h.get("strain", 10) < 5)
        score += (rest_days / len(history)) * 100 * weights["rest_days"]
        
        confidence = "high" if len(history) >= 14 else "medium"
        
        return {
            "prediction": round(score, 1),
            "confidence": confidence,
            "factors": {
                "recent_recovery": round(recent_avg, 1),
                "hrv_trend": hrv_trend,
                "sleep_quality": round(sleep_avg, 1),
                "strain_factor": round(strain_factor, 2)
            }
        }
    
    def _load_recent_history(self, days: int) -> List[Dict]:
        """加载最近N天的历史数据"""
        try:
            with open(os.path.join(self.data_dir, "analysis.json"), 'r') as f:
                data = json.load(f)
                recovery_data = data.get("recovery", {})
                # 简化处理，返回模拟数据
                return [
                    {"recovery_score": recovery_data.get("avg_recovery", 50),
                     "hrv": recovery_data.get("avg_hrv", 40),
                     "strain": 10}
                    for _ in range(min(days, 30))
                ]
        except Exception:
            return []
    
    def _calculate_trend(self, values: List[float]) -> float:
        """计算趋势（简单线性回归斜率）"""
        if len(values) < 2:
            return 0
        
        n = len(values)
        x_mean = sum(range(n)) / n
        y_mean = sum(values) / n
        
        numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0
        
        slope = numerator / denominator
        # 归一化到 -50 到 +50
        return max(-50, min(50, slope * 10))


class StrainOptimizer:
    """
    训练强度优化器
    基于恢复状态动态调整训练计划
    """
    
    def __init__(self):
        self.strain_thresholds = {
            "high_recovery": 70,      # 恢复>=70，可以高强度
            "medium_recovery": 50,     # 恢复50-70，中等强度
            "low_recovery": 30,        # 恢复30-50，低强度
            "rest": 0                 # 恢复<30，建议休息
        }
    
    def get_recommended_intensity(self, recovery: float, recent_strain: List[float]) -> Dict:
        """
        获取推荐训练强度
        
        Args:
            recovery: 当前恢复评分 (0-100)
            recent_strain: 最近几天的strain列表
        
        Returns:
            推荐强度配置
        """
        # 检查连续高强度天数
        high_intensity_days = sum(1 for s in recent_strain[-7:] if s >= 12)
        
        if recovery >= self.strain_thresholds["high_recovery"] and high_intensity_days < 3:
            return {
                "intensity": "high",
                "description": "高强度力量训练",
                "strain_target": "12-15",
                "exercises": ["复合动作为主", "大重量低次数"],
                "duration": "60-75分钟",
                "cautions": []
            }
        
        elif recovery >= self.strain_thresholds["medium_recovery"]:
            return {
                "intensity": "medium",
                "description": "中等强度训练",
                "strain_target": "8-12",
                "exercises": ["上肢/下肢分化", "中重量多次数"],
                "duration": "45-60分钟",
                "cautions": ["注意心率控制"]
            }
        
        elif recovery >= self.strain_thresholds["low_recovery"]:
            return {
                "intensity": "low",
                "description": "低强度活动",
                "strain_target": "5-8",
                "exercises": ["慢走", "瑜伽", "拉伸"],
                "duration": "30-45分钟",
                "cautions": ["以恢复为主，不要勉强"]
            }
        
        else:
            return {
                "intensity": "rest",
                "description": "建议休息",
                "strain_target": "0-3",
                "exercises": ["休息", "睡眠", "轻度拉伸"],
                "duration": "-",
                "cautions": ["身体需要恢复", "不要强行训练"]
            }
    
    def should_deload(self, recovery_history: List[float]) -> Tuple[bool, str]:
        """
        判断是否需要减载周
        
        Args:
            recovery_history: 近期恢复评分列表
        
        Returns:
            (是否减载, 原因)
        """
        if len(recovery_history) < 14:
            return False, "数据不足"
        
        recent_avg = sum(recovery_history[-7:]) / 7
        older_avg = sum(recovery_history[-14:-7]) / 7
        
        # 如果最近7天平均恢复比之前7天低10%以上，考虑减载
        if recent_avg < older_avg - 10:
            return True, f"恢复评分下降 ({older_avg:.0f}% → {recent_avg:.0f}%)"
        
        # 如果连续3天恢复低于40%
        low_days = sum(1 for r in recovery_history[-3:] if r < 40)
        if low_days >= 3:
            return True, "连续3天恢复低于40%"
        
        return False, "无需减载"


class ProgressAnalyzer:
    """
    进步分析器
    分析训练效果，判断是否需要调整计划
    """
    
    def __init__(self):
        self.minimum_progression = {
            "strength": 2.5,  # 每周至少增加2.5kg
            "endurance": 5,   # 每周增加5次
            "volume": 5       # 每周增加5%训练量
        }
    
    def analyze_progress(
        self,
        current_stats: Dict,
        previous_stats: Dict,
        weeks: int = 4
    ) -> Dict:
        """
        分析进步情况
        
        Args:
            current_stats: 当前状态
            previous_stats: 4周前状态
            weeks: 间隔周数
        
        Returns:
            分析结果
        """
        progress = {}
        assessments = {}
        
        # 力量进步
        for lift in ["squat", "bench", "deadlift"]:
            current = current_stats.get(f"{lift}_max", 0)
            previous = previous_stats.get(f"{lift}_max", 0)
            if previous > 0:
                change = current - previous
                weekly_change = change / weeks
                progress[lift] = {
                    "change": round(change, 1),
                    "weekly": round(weekly_change, 2),
                    "on_track": weekly_change >= self.minimum_progression["strength"]
                }
                assessments[lift] = "✅ 进步正常" if progress[lift]["on_track"] else "⚠️ 需要调整"
        
        # 训练量进步
        current_volume = current_stats.get("weekly_volume", 0)
        previous_volume = previous_stats.get("weekly_volume", 0)
        if previous_volume > 0:
            volume_change = (current_volume - previous_volume) / previous_volume * 100
            progress["volume"] = {
                "change_pct": round(volume_change, 1),
                "on_track": volume_change >= self.minimum_progression["volume"]
            }
            assessments["volume"] = "✅ 训练量正常" if progress["volume"]["on_track"] else "⚠️ 需要调整"
        
        # 综合判断
        all_on_track = all(
            p.get("on_track", True) 
            for p in progress.values() 
            if isinstance(p, dict)
        )
        
        return {
            "progress": progress,
            "assessments": assessments,
            "recommendation": "继续当前计划" if all_on_track else "建议调整训练计划",
            "plateau_detected": not all_on_track
        }
    
    def suggest_adjustment(self, analysis_result: Dict) -> List[str]:
        """
        根据分析结果给出调整建议
        
        Returns:
            调整建议列表
        """
        suggestions = []
        
        if not analysis_result.get("plateau_detected"):
            return ["保持当前训练计划"]
        
        progress = analysis_result.get("progress", {})
        
        for lift, data in progress.items():
            if isinstance(data, dict) and not data.get("on_track"):
                suggestions.append(f"{lift}: 增加训练频率或改变训练方式")
        
        if not suggestions:
            suggestions.append("尝试新的训练动作或增加训练强度")
        
        return suggestions


# 全局实例
_predictor = None
_optimizer = None
_analyzer = None

def get_recovery_predictor() -> RecoveryPredictor:
    global _predictor
    if _predictor is None:
        _predictor = RecoveryPredictor()
    return _predictor

def get_strain_optimizer() -> StrainOptimizer:
    global _optimizer
    if _optimizer is None:
        _optimizer = StrainOptimizer()
    return _optimizer

def get_progress_analyzer() -> ProgressAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = ProgressAnalyzer()
    return _analyzer
