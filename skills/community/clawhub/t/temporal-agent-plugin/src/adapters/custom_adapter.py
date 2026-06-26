from typing import Dict, Any, Optional, Callable

from src.core.temporal_analyzer import TemporalAnalyzer
from src.core.progress_estimator import ProgressEstimator
from src.core.anomaly_detector import AnomalyDetector
from src.core.social_temporal import SocialTemporal
from src.core.causal_predictor import CausalPredictor
from src.core.time_anchor import TimeAnchorInjector

class CustomAdapter:
    """自定义框架适配器
    
    用于与其他自定义AI框架集成
    """
    
    def __init__(self):
        self.temporal_analyzer = TemporalAnalyzer()
        self.progress_estimator = ProgressEstimator()
        self.anomaly_detector = AnomalyDetector()
        self.social_temporal = SocialTemporal()
        self.causal_predictor = CausalPredictor()
        self.time_anchor = TimeAnchorInjector()
    
    def start_timer(self, task_id: str) -> float:
        """开始计时
        
        Args:
            task_id: 任务ID
            
        Returns:
            开始时间戳
        """
        return self.temporal_analyzer.start_timer(task_id)
    
    def stop_timer(self, task_id: str) -> float:
        """停止计时
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务持续时间
        """
        return self.temporal_analyzer.stop_timer(task_id)
    
    def predict_duration(self, task_type: str, complexity: float = 1.0) -> float:
        """预测任务执行时间
        
        Args:
            task_type: 任务类型
            complexity: 复杂度因子
            
        Returns:
            预测的执行时间
        """
        return self.temporal_analyzer.predict_duration(task_type, complexity)
    
    def is_taking_too_long(self, task_id: str, expected_duration: float) -> bool:
        """判断任务是否执行时间过长
        
        Args:
            task_id: 任务ID
            expected_duration: 预期执行时间
            
        Returns:
            是否执行时间过长
        """
        return self.temporal_analyzer.is_taking_too_long(task_id, expected_duration)
    
    def start_task(self, task_id: str, task_type: str, total_steps: int = 100):
        """开始任务
        
        Args:
            task_id: 任务ID
            task_type: 任务类型
            total_steps: 总步骤数
        """
        self.progress_estimator.start_task(task_id, task_type, total_steps)
    
    def update_progress(self, task_id: str, current_step: int, **kwargs):
        """更新任务进度
        
        Args:
            task_id: 任务ID
            current_step: 当前步骤
            **kwargs: 额外信息
        """
        self.progress_estimator.update_progress(task_id, current_step, **kwargs)
    
    def get_progress(self, task_id: str) -> Dict[str, Any]:
        """获取任务进度
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务进度信息
        """
        return self.progress_estimator.get_progress(task_id)
    
    def detect_anomaly(self, event_type: str, duration: float) -> bool:
        """检测异常
        
        Args:
            event_type: 事件类型
            duration: 持续时间
            
        Returns:
            是否异常
        """
        return self.anomaly_detector.is_response_time_abnormal(event_type, duration)
    
    def record_utterance(self, speaker: str, content: str):
        """记录对话
        
        Args:
            speaker: 说话者
            content: 内容
        """
        self.social_temporal.record_utterance(speaker, content)
    
    def should_respond(self) -> bool:
        """判断是否应该回应
        
        Returns:
            是否应该回应
        """
        return self.social_temporal.should_respond()
    
    def is_interruption(self) -> bool:
        """判断是否是打断
        
        Returns:
            是否是打断
        """
        return self.social_temporal.is_interruption()
    
    def predict_latency(self, action: str) -> float:
        """预测动作的延迟
        
        Args:
            action: 动作
            
        Returns:
            预测的延迟
        """
        return self.causal_predictor.predict_latency(action)
    
    def predict_result_time(self, action: str) -> float:
        """预测结果出现的时间
        
        Args:
            action: 动作
            
        Returns:
            预测的结果时间
        """
        return self.causal_predictor.predict_result_time(action)
    
    def register_progress_callback(self, task_id: str, callback: Callable):
        """注册进度回调函数
        
        Args:
            task_id: 任务ID
            callback: 回调函数
        """
        self.progress_estimator.register_progress_callback(task_id, callback)
    
    def clear_history(self):
        """清空所有历史记录
        """
        self.temporal_analyzer.clear_history()
        self.social_temporal.clear_history()
        self.causal_predictor.clear_history()
        self.anomaly_detector.clear_history()
    
    def get_time_context(self, timezone: Optional[str] = None) -> Dict[str, Any]:
        """获取时间上下文
        
        Args:
            timezone: 时区
            
        Returns:
            时间上下文信息
        """
        return self.time_anchor.get_time_context(timezone)
    
    def inject_time_anchor(self, prompt: str, timezone: Optional[str] = None) -> str:
        """注入时间锚点到提示词
        
        Args:
            prompt: 原始提示词
            timezone: 时区
            
        Returns:
            注入时间锚点后的提示词
        """
        return self.time_anchor.inject_time_anchor(prompt, timezone)
    
    def get_current_time(self, timezone: Optional[str] = None) -> str:
        """获取当前时间
        
        Args:
            timezone: 时区
            
        Returns:
            当前时间字符串
        """
        return self.time_anchor.get_time_string(timezone)
    
    def get_relative_time(self, timestamp: float) -> str:
        """获取相对时间
        
        Args:
            timestamp: 时间戳
            
        Returns:
            相对时间描述
        """
        return self.time_anchor.get_relative_time(timestamp)
    
    def format_time_difference(self, seconds: float) -> str:
        """格式化时间差
        
        Args:
            seconds: 时间差（秒）
            
        Returns:
            格式化的时间差
        """
        return self.time_anchor.format_time_difference(seconds)