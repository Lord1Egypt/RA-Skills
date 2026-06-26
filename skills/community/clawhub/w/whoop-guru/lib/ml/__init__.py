"""
ML Module - 机器学习预测和动态调整
包含：
- recovery_model.py: 恢复预测模型
- predictor.py: 兼容旧接口
"""

from lib.ml.recovery_model import (
    RecoveryPredictor,
    HRVAnalyzer,
    get_recovery_prediction,
    get_training_recommendation,
    get_hrv_anomaly,
)

__all__ = [
    'RecoveryPredictor',
    'HRVAnalyzer',
    'get_recovery_prediction',
    'get_training_recommendation',
    'get_hrv_anomaly',
]
