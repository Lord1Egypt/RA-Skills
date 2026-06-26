import time
from typing import Dict, Any, List, Optional, Callable
from collections import deque
import threading
import psutil
from datetime import datetime

# 检查依赖项
try:
    import numpy as np
except ImportError:
    raise ImportError("请安装numpy: pip install numpy")

try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


class SmartTimeoutPredictor:
    """智能超时预测器

    基于机器学习的超时预测，解决V1.0固定阈值判断的僵化问题。
    """

    def __init__(self, use_ml: bool = True, min_samples_for_ml: int = 10):
        self.use_ml = use_ml and HAS_SKLEARN
        self.min_samples_for_ml = min_samples_for_ml

        self.task_histories: Dict[str, deque] = {}
        self.ml_model: Optional[RandomForestRegressor] = None
        self.scaler = StandardScaler() if self.use_ml else None
        self._lock = threading.RLock()

        self._time_of_day_cache = None
        self._time_of_day_cache_time = 0

    def _get_time_of_day_factor(self) -> float:
        """获取时间段因子"""
        now = datetime.now()
        hour = now.hour

        if 2 <= hour < 6:
            return 0.8
        elif 6 <= hour < 9:
            return 1.0
        elif 9 <= hour < 12:
            return 1.1
        elif 12 <= hour < 14:
            return 0.9
        elif 14 <= hour < 18:
            return 1.1
        elif 18 <= hour < 22:
            return 1.2
        else:
            return 0.8

    def _get_system_load_factor(self) -> float:
        """获取系统负载因子"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_percent = psutil.virtual_memory().percent

            load_score = (cpu_percent / 100 + memory_percent / 100) / 2
            return 0.5 + load_score * 1.5
        except Exception:
            return 1.0

    def _extract_features(self, task_type: str) -> np.ndarray:
        """提取预测特征"""
        history = self.task_histories.get(task_type, deque(maxlen=100))

        if len(history) == 0:
            mean_duration = 30.0
            std_duration = 10.0
            sample_count = 0
        else:
            durations = list(history)
            mean_duration = np.mean(durations)
            std_duration = np.std(durations) if len(durations) > 1 else mean_duration * 0.3
            sample_count = len(durations)

        system_load = self._get_system_load_factor()
        time_of_day = self._get_time_of_day_factor()
        sample_factor = min(sample_count / self.min_samples_for_ml, 1.0)

        features = np.array([
            mean_duration,
            std_duration,
            system_load,
            time_of_day,
            sample_factor
        ])

        return features

    def record_duration(self, task_type: str, duration: float):
        """记录任务执行时长"""
        with self._lock:
            if task_type not in self.task_histories:
                self.task_histories[task_type] = deque(maxlen=100)
            self.task_histories[task_type].append(duration)

            if self.use_ml and len(self.task_histories[task_type]) >= self.min_samples_for_ml:
                self._train_model()

    def _train_model(self):
        """训练ML模型"""
        if not self.use_ml or not HAS_SKLEARN:
            return

        all_features = []
        all_targets = []

        for task_type, history in self.task_histories.items():
            if len(history) < self.min_samples_for_ml:
                continue

            durations = list(history)
            for i in range(len(durations)):
                features = self._extract_features_at_point(task_type, i)
                target = durations[i]
                all_features.append(features)
                all_targets.append(target)

        if len(all_features) < self.min_samples_for_ml:
            return

        X = np.array(all_features)
        y = np.array(all_targets)

        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)

        self.ml_model = RandomForestRegressor(n_estimators=10, max_depth=5, random_state=42)
        self.ml_model.fit(X_scaled, y)

    def _extract_features_at_point(self, task_type: str, point_index: int) -> np.ndarray:
        """在特定时间点提取特征"""
        history = list(self.task_histories[task_type])
        past_durations = history[:point_index] if point_index > 0 else [30.0]

        mean_duration = np.mean(past_durations)
        std_duration = np.std(past_durations) if len(past_durations) > 1 else mean_duration * 0.3

        system_load = self._get_system_load_factor()
        time_of_day = self._get_time_of_day_factor()
        sample_factor = min(len(past_durations) / self.min_samples_for_ml, 1.0)

        return np.array([
            mean_duration,
            std_duration,
            system_load,
            time_of_day,
            sample_factor
        ])

    def predict_timeout(self, task_type: str) -> float:
        """预测超时阈值"""
        with self._lock:
            history = self.task_histories.get(task_type, deque(maxlen=100))

            if len(history) < 3:
                return self._fallback_baseline_prediction(task_type)

            if self.use_ml and self.ml_model is not None:
                return self._ml_prediction(task_type)
            else:
                return self._statistical_prediction(history)

    def _ml_prediction(self, task_type: str) -> float:
        """基于ML模型的预测"""
        features = self._extract_features(task_type).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        predicted_duration = self.ml_model.predict(features_scaled)[0]

        base_timeout = predicted_duration * 1.5
        return max(base_timeout, 5.0)

    def _statistical_prediction(self, history: deque) -> float:
        """基于统计的预测"""
        durations = list(history)
        mean_duration = np.mean(durations)
        std_duration = np.std(durations)

        system_load = self._get_system_load_factor()
        time_of_day = self._get_time_of_day_factor()

        predicted_duration = mean_duration * system_load * time_of_day
        timeout = predicted_duration + 2 * std_duration

        return max(timeout, 5.0)

    def _fallback_baseline_prediction(self, task_type: str) -> float:
        """后备基线预测"""
        default_baselines = {
            'api_call': 30.0,
            'file_operation': 60.0,
            'network_request': 45.0,
            'computation': 120.0,
            'io_operation': 90.0,
        }

        baseline = default_baselines.get(task_type, 60.0)
        system_load = self._get_system_load_factor()
        time_of_day = self._get_time_of_day_factor()

        return baseline * system_load * time_of_day

    def get_prediction_confidence(self, task_type: str) -> float:
        """获取预测置信度"""
        with self._lock:
            history = self.task_histories.get(task_type, deque(maxlen=100))

            if len(history) == 0:
                return 0.0

            if self.use_ml and self.ml_model is not None and len(history) >= self.min_samples_for_ml:
                return min(len(history) / (self.min_samples_for_ml * 3), 1.0)
            else:
                if len(history) < 3:
                    return 0.0
                return min(len(history) / 20, 0.8)

    def adjust_timeout_realtime(self, task_type: str, elapsed: float, predicted_total: float) -> float:
        """实时调整超时阈值"""
        if elapsed == 0:
            return predicted_total

        progress_rate = elapsed / predicted_total if predicted_total > 0 else 1.0

        if progress_rate < 0.5:
            buffer = 2.0
        elif progress_rate < 0.8:
            buffer = 1.5
        else:
            buffer = 1.2

        history = self.task_histories.get(task_type, deque(maxlen=100))
        if len(history) > 0:
            recent_mean = np.mean(list(history)[-5:])
            if elapsed > recent_mean * 3:
                buffer = max(buffer, 2.5)

        return predicted_total * buffer

    def get_task_statistics(self, task_type: str) -> Dict[str, Any]:
        """获取任务统计信息"""
        with self._lock:
            history = self.task_histories.get(task_type, deque(maxlen=100))

            if len(history) == 0:
                return {
                    'count': 0,
                    'mean': 0.0,
                    'std': 0.0,
                    'min': 0.0,
                    'max': 0.0,
                    'predicted_timeout': 0.0,
                    'confidence': 0.0,
                    'uses_ml': self.use_ml and self.ml_model is not None
                }

            durations = list(history)
            return {
                'count': len(durations),
                'mean': np.mean(durations),
                'std': np.std(durations),
                'min': np.min(durations),
                'max': np.max(durations),
                'median': np.median(durations),
                'predicted_timeout': self.predict_timeout(task_type),
                'confidence': self.get_prediction_confidence(task_type),
                'uses_ml': self.use_ml and self.ml_model is not None
            }