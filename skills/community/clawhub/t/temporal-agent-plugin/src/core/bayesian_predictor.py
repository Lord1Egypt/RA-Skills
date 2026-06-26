import time
import math
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import threading


@dataclass
class BayesianPrior:
    """贝叶斯先验分布参数

    使用 Gamma 分布作为先验：
    - Gamma(alpha, beta) 的均值 = alpha / beta
    - alpha 越大，分布越集中（信心越强）
    - beta 控制分布的尺度
    """
    alpha: float
    beta: float

    @property
    def mean(self) -> float:
        """先验均值"""
        return self.alpha / self.beta if self.beta > 0 else float('inf')

    @property
    def variance(self) -> float:
        """先验方差"""
        return self.alpha / (self.beta ** 2) if self.beta > 0 else float('inf')

    @property
    def std(self) -> float:
        """先验标准差"""
        return math.sqrt(self.variance)


class LightweightTimeoutPredictor:
    """轻量级超时预测器 - 高频低价值场景专用

    特点：
    - 仅使用滑动窗口均值，无贝叶斯计算
    - 延迟目标：<50ms
    - 适用于 cron 每5分钟触发等高频低价值场景
    """

    DEFAULT_WINDOW_SIZE = 10
    DEFAULT_SAFETY_MULTIPLIER = 1.5
    DEFAULT_MIN_TIMEOUT = 5.0
    DEFAULT_MAX_TIMEOUT = 300.0

    def __init__(
        self,
        window_size: int = DEFAULT_WINDOW_SIZE,
        safety_multiplier: float = DEFAULT_SAFETY_MULTIPLIER,
        min_timeout: float = DEFAULT_MIN_TIMEOUT,
        max_timeout: float = DEFAULT_MAX_TIMEOUT
    ):
        self.window_size = window_size
        self.safety_multiplier = safety_multiplier
        self.min_timeout = min_timeout
        self.max_timeout = max_timeout

        self._observations: List[float] = []
        self._lock = threading.RLock()

    def update(self, duration: float):
        """更新观测数据"""
        with self._lock:
            self._observations.append(duration)
            if len(self._observations) > self.window_size:
                self._observations.pop(0)

    def predict_timeout(self) -> float:
        """预测超时时间 - 轻量模式"""
        with self._lock:
            if not self._observations:
                return self.min_timeout

            mean = sum(self._observations) / len(self._observations)
            timeout = mean * self.safety_multiplier
            return max(self.min_timeout, min(timeout, self.max_timeout))

    def get_confidence(self) -> float:
        """获取预测置信度"""
        with self._lock:
            count = len(self._observations)
            if count == 0:
                return 0.0
            return min(count / self.window_size, 1.0)

    def reset(self):
        """重置预测器"""
        with self._lock:
            self._observations.clear()

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._lock:
            if not self._observations:
                return {
                    'mode': 'lightweight',
                    'window_size': self.window_size,
                    'observation_count': 0,
                    'predicted_timeout': self.min_timeout,
                    'confidence': 0.0
                }

            mean = sum(self._observations) / len(self._observations)
            return {
                'mode': 'lightweight',
                'window_size': self.window_size,
                'observation_count': len(self._observations),
                'mean': mean,
                'predicted_timeout': self.predict_timeout(),
                'confidence': self.get_confidence(),
                'recent_values': list(self._observations)
            }


class BayesianTimeoutPredictor:
    """基于贝叶斯更新的超时预测器 - 完整模式

    解决冷启动问题：
    1. 冷启动时使用保守先验（高估超时时间）
    2. 每次任务完成后，将实际耗时写入记忆，更新后验分布
    3. 随着数据积累，预测逐渐收敛到真实值

    使用 Gamma-Poisson 共轭先验模型：
    - 先验：Gamma(alpha_0, beta_0)
    - 似然：观测数据服从 Gamma 分布
    - 后验：Gamma(alpha_0 + n, beta_0 + sum(observations))
    """

    DEFAULT_CONSERVATIVE_PRIOR = BayesianPrior(alpha=2.0, beta=0.05)

    TASK_TYPE_PRIORS: Dict[str, BayesianPrior] = {
        'api_call': BayesianPrior(alpha=2.0, beta=0.1),
        'file_operation': BayesianPrior(alpha=2.0, beta=0.03),
        'network_request': BayesianPrior(alpha=2.0, beta=0.05),
        'computation': BayesianPrior(alpha=2.0, beta=0.02),
        'io_operation': BayesianPrior(alpha=2.0, beta=0.025),
    }

    def __init__(
        self,
        prior: Optional[BayesianPrior] = None,
        task_type: str = "default",
        safety_multiplier: float = 2.0,
        min_timeout: float = 5.0,
        max_timeout: float = 3600.0
    ):
        self.task_type = task_type
        self.prior = prior or self.TASK_TYPE_PRIORS.get(task_type, self.DEFAULT_CONSERVATIVE_PRIOR)
        self.safety_multiplier = safety_multiplier
        self.min_timeout = min_timeout
        self.max_timeout = max_timeout

        self.posterior_alpha = self.prior.alpha
        self.posterior_beta = self.prior.beta

        self.observations: List[float] = []
        self.observation_count = 0

        self._lock = threading.RLock()

    def update(self, duration: float):
        """更新后验分布"""
        with self._lock:
            self.observations.append(duration)
            self.observation_count += 1

            self.posterior_alpha = self.prior.alpha + self.observation_count
            self.posterior_beta = self.prior.beta + sum(self.observations)

    def predict_timeout(self) -> float:
        """预测超时时间"""
        with self._lock:
            posterior_mean = self.posterior_alpha / self.posterior_beta
            timeout = posterior_mean * self.safety_multiplier
            return max(self.min_timeout, min(timeout, self.max_timeout))

    def get_confidence(self) -> float:
        """获取预测置信度"""
        if self.observation_count == 0:
            return 0.0

        k = 0.5
        confidence = 1.0 / (1.0 + math.exp(-k * (self.observation_count - 5)))
        return min(confidence, 1.0)

    def get_posterior_stats(self) -> Dict[str, Any]:
        """获取后验分布统计信息"""
        with self._lock:
            posterior_mean = self.posterior_alpha / self.posterior_beta
            posterior_var = self.posterior_alpha / (self.posterior_beta ** 2)
            posterior_std = math.sqrt(posterior_var)

            return {
                'task_type': self.task_type,
                'observation_count': self.observation_count,
                'prior_mean': self.prior.mean,
                'prior_std': self.prior.std,
                'posterior_mean': posterior_mean,
                'posterior_std': posterior_std,
                'predicted_timeout': self.predict_timeout(),
                'confidence': self.get_confidence(),
                'observations': list(self.observations[-10:])
            }

    def reset(self, prior: Optional[BayesianPrior] = None):
        """重置预测器"""
        with self._lock:
            if prior:
                self.prior = prior
            self.posterior_alpha = self.prior.alpha
            self.posterior_beta = self.prior.beta
            self.observations.clear()
            self.observation_count = 0

    def get_calibration_data(self) -> Dict[str, Any]:
        """获取校准数据"""
        with self._lock:
            if len(self.observations) < 2:
                return {
                    'calibrated': False,
                    'observation_count': self.observation_count,
                    'message': '观测数据不足，无法校准'
                }

            errors = []
            for i in range(1, len(self.observations)):
                temp_alpha = self.prior.alpha + i
                temp_beta = self.prior.beta + sum(self.observations[:i])
                predicted = (temp_alpha / temp_beta) * self.safety_multiplier
                actual = self.observations[i]
                error = abs(predicted - actual) / actual if actual > 0 else 0
                errors.append(error)

            mean_error = sum(errors) / len(errors) if errors else 0

            return {
                'calibrated': self.observation_count >= 5,
                'observation_count': self.observation_count,
                'mean_relative_error': mean_error,
                'converged': mean_error < 0.3,
                'observations': list(self.observations[-10:])
            }


class AdaptiveTimeoutPredictor:
    """自适应超时预测器 - 根据场景自动选择轻量/完整模式

    设计原则：
    - 高频低价值场景（cron每5分钟） → 轻量模式（<50ms延迟）
    - 关键路径场景 → 完整贝叶斯模式（<500ms延迟）

    自动切换逻辑：
    - 累计调用次数 < threshold → 完整模式（收集数据）
    - 累计调用次数 >= threshold + 置信度达标 → 切换到轻量模式
    - 检测到异常波动 → 自动切回完整模式重新校准
    """

    DEFAULT_SWITCH_THRESHOLD = 20
    DEFAULT_CONFIDENCE_THRESHOLD = 0.8

    def __init__(
        self,
        task_type: str = "default",
        switch_threshold: int = DEFAULT_SWITCH_THRESHOLD,
        confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
        lightweight_window_size: int = 10,
        bayesian_safety_multiplier: float = 2.0,
        lightweight_safety_multiplier: float = 1.5
    ):
        self.task_type = task_type
        self.switch_threshold = switch_threshold
        self.confidence_threshold = confidence_threshold

        self._lightweight = LightweightTimeoutPredictor(
            window_size=lightweight_window_size,
            safety_multiplier=lightweight_safety_multiplier
        )
        self._bayesian = BayesianTimeoutPredictor(
            task_type=task_type,
            safety_multiplier=bayesian_safety_multiplier
        )

        self._mode = "bayesian"
        self._call_count = 0
        self._last_prediction_time = 0.0
        self._lock = threading.RLock()

    @property
    def mode(self) -> str:
        """当前模式"""
        with self._lock:
            return self._mode

    def predict_timeout(self) -> float:
        """预测超时时间 - 自动选择模式"""
        start_time = time.time()

        with self._lock:
            self._call_count += 1

            if self._mode == "lightweight":
                result = self._lightweight.predict_timeout()
            else:
                result = self._bayesian.predict_timeout()

            self._last_prediction_time = (time.time() - start_time) * 1000
            return result

    def update(self, duration: float):
        """更新观测数据 - 双模式同时更新"""
        with self._lock:
            self._lightweight.update(duration)
            self._bayesian.update(duration)
            self._check_mode_switch()

    def _check_mode_switch(self):
        """检查是否需要切换模式"""
        if self._mode == "lightweight":
            lightweight_conf = self._lightweight.get_confidence()
            if lightweight_conf < 0.5:
                self._mode = "bayesian"
                return

        if self._mode == "bayesian":
            bayesian_conf = self._bayesian.get_confidence()
            call_count_ok = self._call_count >= self.switch_threshold
            confidence_ok = bayesian_conf >= self.confidence_threshold

            if call_count_ok and confidence_ok:
                recent_std = self._get_recent_std()
                if recent_std < bayesian_conf * 0.5:
                    self._mode = "lightweight"

    def _get_recent_std(self) -> float:
        """获取近期观测标准差"""
        obs = self._bayesian.observations
        if len(obs) < 3:
            return float('inf')

        recent = obs[-self.switch_threshold:]
        mean = sum(recent) / len(recent)
        variance = sum((x - mean) ** 2 for x in recent) / len(recent)
        return math.sqrt(variance)

    def get_confidence(self) -> float:
        """获取当前模式预测置信度"""
        with self._lock:
            if self._mode == "lightweight":
                return self._lightweight.get_confidence()
            return self._bayesian.get_confidence()

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._lock:
            return {
                'task_type': self.task_type,
                'current_mode': self._mode,
                'call_count': self._call_count,
                'switch_threshold': self.switch_threshold,
                'confidence_threshold': self.confidence_threshold,
                'last_prediction_time_ms': self._last_prediction_time,
                'lightweight': self._lightweight.get_stats(),
                'bayesian': self._bayesian.get_posterior_stats(),
                'predicted_timeout': self.predict_timeout(),
                'confidence': self.get_confidence()
            }

    def reset(self, mode: Optional[str] = None):
        """重置预测器"""
        with self._lock:
            if mode:
                self._mode = mode
            else:
                self._mode = "bayesian"
            self._call_count = 0
            self._lightweight.reset()
            self._bayesian.reset()

    def force_mode(self, mode: str):
        """强制切换模式"""
        with self._lock:
            if mode in ("lightweight", "bayesian"):
                self._mode = mode


class BayesianTimeoutManager:
    """贝叶斯超时预测管理器 - 扩展支持自适应模式"""

    def __init__(self, safety_multiplier: float = 2.0, use_adaptive: bool = True):
        self.safety_multiplier = safety_multiplier
        self.use_adaptive = use_adaptive
        self.predictors: Dict[str, AdaptiveTimeoutPredictor] = {}
        self._lock = threading.Lock()

    def get_predictor(self, task_type: str) -> AdaptiveTimeoutPredictor:
        """获取或创建任务类型的预测器"""
        with self._lock:
            if task_type not in self.predictors:
                self.predictors[task_type] = AdaptiveTimeoutPredictor(
                    task_type=task_type,
                    bayesian_safety_multiplier=self.safety_multiplier
                )
            return self.predictors[task_type]

    def record_duration(self, task_type: str, duration: float):
        """记录任务执行时长并更新预测"""
        predictor = self.get_predictor(task_type)
        predictor.update(duration)

    def predict_timeout(self, task_type: str) -> float:
        """预测超时时间"""
        predictor = self.get_predictor(task_type)
        return predictor.predict_timeout()

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """获取所有任务类型的统计信息"""
        with self._lock:
            return {
                task_type: predictor.get_stats()
                for task_type, predictor in self.predictors.items()
            }

    def force_mode(self, task_type: str, mode: str):
        """强制切换指定任务类型的预测模式"""
        predictor = self.get_predictor(task_type)
        predictor.force_mode(mode)
