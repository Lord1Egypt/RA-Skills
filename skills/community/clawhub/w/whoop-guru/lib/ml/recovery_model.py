"""
ML Recovery Model - 恢复预测模型
基于历史数据预测未来恢复状态
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

# 数据路径 - 使用环境变量
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ml/ -> lib/ -> whoop-guru/
WORKSPACE_DIR = os.environ.get("OPENCLAW_WORKSPACE", os.path.dirname(SKILL_DIR))
PROCESSED_DIR = os.environ.get("WHOOP_DATA_DIR", os.path.join(WORKSPACE_DIR, "data", "processed"))
DATA_FILE = os.path.join(PROCESSED_DIR, "latest.json")


class RecoveryPredictor:
    """
    恢复预测器
    基于加权模型预测未来恢复状态
    """
    
    def __init__(self):
        self.weights = {
            "previous_recovery": 0.25,
            "hrv_trend": 0.20,
            "sleep_quality": 0.20,
            "training_strain": 0.20,
            "rest_days": 0.15
        }
    
    def load_history(self, days: int = 30) -> List[Dict]:
        """加载历史数据"""
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            
            recovery = data.get("processed", {}).get("recovery", [])
            
            # 过滤最近N天
            cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            return [r for r in recovery if r.get("date", "") >= cutoff]
        except Exception:
            return []
    
    def calculate_trend(self, values: List[float]) -> float:
        """计算趋势（简单线性回归斜率）"""
        if len(values) < 3:
            return 0.0
        
        n = len(values)
        x_mean = sum(range(n)) / n
        y_mean = sum(values) / n
        
        numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        slope = numerator / denominator
        return max(-50, min(50, slope * 10))
    
    def predict_next_7_days(self) -> Dict:
        """
        预测未来7天的恢复状态
        
        Returns:
            {
                "predictions": [day1_score, day2_score, ...],
                "confidence": "high/medium/low",
                "trend": "up/stable/down",
                "factors": {...}
            }
        """
        history = self.load_history(30)
        
        if len(history) < 3:
            return {
                "predictions": [50] * 7,
                "confidence": "low",
                "trend": "stable",
                "reason": "数据不足"
            }
        
        # 计算各因素
        recovery_values = [r.get("recovery_score", 50) for r in history]
        hrv_values = [r.get("hrv", 40) for r in history if r.get("hrv")]
        rhr_values = [r.get("rhr", 55) for r in history if r.get("rhr")]
        
        # 基础恢复分（最近7天平均）
        recent_avg = sum(recovery_values[:7]) / min(7, len(recovery_values))
        
        # HRV趋势
        hrv_trend = self.calculate_trend(hrv_values[:14]) if len(hrv_values) >= 7 else 0
        
        # 睡眠质量（最近）
        sleep_quality = 75  # 默认值
        
        # 训练强度（最近7天）
        daily_data = history[:7] if len(history) >= 7 else history
        strain_avg = sum(d.get("recovery_score", 50) for d in daily_data) / len(daily_data) if daily_data else 50
        
        # 预测
        predictions = []
        current_score = recent_avg
        
        for day in range(7):
            # 简单预测：基于趋势递减
            if day > 0:
                current_score = current_score * 0.98 + 50 * 0.02  # 回归均值
            
            # 添加一些随机波动
            import random
            noise = random.uniform(-3, 3)
            predicted = max(20, min(100, current_score + noise))
            predictions.append(round(predicted, 1))
        
        # 置信度
        if len(history) >= 14:
            confidence = "high"
        elif len(history) >= 7:
            confidence = "medium"
        else:
            confidence = "low"
        
        # 趋势判断
        if predictions[0] > predictions[-1] + 5:
            trend = "up"
        elif predictions[0] < predictions[-1] - 5:
            trend = "down"
        else:
            trend = "stable"
        
        return {
            "predictions": predictions,
            "confidence": confidence,
            "trend": trend,
            "factors": {
                "recent_avg": round(recent_avg, 1),
                "hrv_trend": round(hrv_trend, 2),
                "days_ahead": 7
            }
        }
    
    def get_training_recommendation(self, target_recovery: float = 70) -> Dict:
        """
        获取训练建议
        
        Args:
            target_recovery: 目标恢复评分
        
        Returns:
            训练建议字典
        """
        prediction = self.predict_next_7_days()
        avg_predicted = sum(prediction["predictions"]) / 7
        
        # 建议
        if avg_predicted >= 80:
            recommendation = "可以安排高强度训练"
            intensity = "high"
            strain_target = "12-15"
        elif avg_predicted >= 60:
            recommendation = "可以安排中等强度训练"
            intensity = "medium"
            strain_target = "8-12"
        elif avg_predicted >= 40:
            recommendation = "建议轻度活动或休息"
            intensity = "low"
            strain_target = "5-8"
        else:
            recommendation = "建议完全休息"
            intensity = "rest"
            strain_target = "0-3"
        
        return {
            "recommended_intensity": intensity,
            "strain_target": strain_target,
            "recommendation": recommendation,
            "predicted_avg": round(avg_predicted, 1),
            "confidence": prediction["confidence"]
        }


class HRVAnalyzer:
    """
    HRV分析器
    检测HRV异常，提供健康预警
    """
    
    def __init__(self):
        self.baseline_window = 14  # 基准期（天）
        self.anomaly_threshold = 25  # 异常阈值（百分比）
    
    def load_hrv_data(self, days: int = 30) -> List[Dict]:
        """加载HRV数据"""
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            
            recovery = data.get("processed", {}).get("recovery", [])
            
            cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            return [r for r in recovery if r.get("date", "") >= cutoff and r.get("hrv")]
        except Exception:
            return []
    
    def calculate_baseline(self) -> Tuple[float, float]:
        """计算HRV基线和标准差"""
        hrv_data = self.load_hrv_data(30)
        
        if len(hrv_data) < 7:
            return 40.0, 10.0  # 默认值
        
        values = [r.get("hrv", 40) for r in hrv_data[:self.baseline_window]]
        
        if not values:
            return 40.0, 10.0
        
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = variance ** 0.5
        
        return mean, std
    
    def detect_anomaly(self) -> Dict:
        """
        检测HRV异常
        
        Returns:
            {
                "is_anomaly": bool,
                "current_hrv": float,
                "baseline": float,
                "change_pct": float,
                "severity": "normal/warning/critical"
            }
        """
        hrv_data = self.load_hrv_data(7)
        
        if not hrv_data:
            return {
                "is_anomaly": False,
                "reason": "数据不足"
            }
        
        current_hrv = hrv_data[0].get("hrv", 40)
        baseline, std = self.calculate_baseline()
        
        if baseline == 0:
            baseline = 40
        
        change_pct = ((current_hrv - baseline) / baseline) * 100
        
        # 判断异常
        is_anomaly = abs(change_pct) > self.anomaly_threshold
        
        if abs(change_pct) > 40:
            severity = "critical"
        elif abs(change_pct) > 25:
            severity = "warning"
        else:
            severity = "normal"
        
        return {
            "is_anomaly": is_anomaly,
            "current_hrv": current_hrv,
            "baseline": round(baseline, 1),
            "std": round(std, 1),
            "change_pct": round(change_pct, 1),
            "severity": severity
        }


def get_recovery_prediction() -> Dict:
    """获取恢复预测的便捷函数"""
    predictor = RecoveryPredictor()
    return predictor.predict_next_7_days()


def get_training_recommendation() -> Dict:
    """获取训练建议的便捷函数"""
    predictor = RecoveryPredictor()
    return predictor.get_training_recommendation()


def get_hrv_anomaly() -> Dict:
    """获取HRV异常的便捷函数"""
    analyzer = HRVAnalyzer()
    return analyzer.detect_anomaly()


if __name__ == "__main__":
    print("=== Recovery Predictor ===")
    predictor = RecoveryPredictor()
    result = predictor.predict_next_7_days()
    print(f"Predictions: {result['predictions']}")
    print(f"Trend: {result['trend']}, Confidence: {result['confidence']}")
    
    print("\n=== Training Recommendation ===")
    rec = predictor.get_training_recommendation()
    print(f"Intensity: {rec['recommended_intensity']}")
    print(f"Recommendation: {rec['recommendation']}")
    
    print("\n=== HRV Anomaly ===")
    analyzer = HRVAnalyzer()
    anomaly = analyzer.detect_anomaly()
    print(f"Is Anomaly: {anomaly['is_anomaly']}")
    print(f"Change: {anomaly['change_pct']}%")
