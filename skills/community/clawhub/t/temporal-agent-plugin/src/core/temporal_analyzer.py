import time
import datetime
from typing import Dict, Any, List, Optional

# 检查依赖项
try:
    import pandas as pd
    import numpy as np
except ImportError:
    raise ImportError("请安装pandas和numpy: pip install pandas numpy")

from .time_anchor import TimeAnchorInjector
from .smart_timeout_predictor import SmartTimeoutPredictor
from .bayesian_predictor import BayesianTimeoutManager
from .anomaly_detector import AnomalyDetector
from .social_temporal import SocialTemporal

class TemporalAnalyzer:
    """时序分析引擎
    
    负责处理和分析时间相关的数据，为智能体提供时间感知能力
    V2.1增强：
    - 集成时间锚点功能
    - 集成智能超时预测
    - 增强预测算法
    """
    
    def __init__(self):
        self.start_times = {}
        self.end_times = {}
        self.durations = {}
        self.context_history = []
        
        # 集成时间锚点
        self.time_anchor = TimeAnchorInjector()
        
        # 集成智能超时预测
        self.smart_timeout = SmartTimeoutPredictor()
        
        # 集成贝叶斯超时预测
        self.bayesian_manager = BayesianTimeoutManager()
        
        # 集成异常检测
        self.anomaly_detector = AnomalyDetector()
        
        # 集成社交时序理解
        self.social_temporal = SocialTemporal()
    
    def start_timer(self, task_id: str, task_type: str = 'general', expected_duration: float = 60.0, dependencies: Optional[List[str]] = None) -> float:
        """开始计时
        
        Args:
            task_id: 任务ID
            task_type: 任务类型
            expected_duration: 预期执行时间
            dependencies: 依赖任务ID列表
            
        Returns:
            开始时间戳
        """
        start_time = time.time()
        self.start_times[task_id] = start_time
        
        # 注册任务到异常检测模块
        self.anomaly_detector.register_task(
            task_id=task_id,
            task_type=task_type,
            expected_duration=expected_duration,
            dependencies=dependencies
        )
        
        return start_time
    
    def stop_timer(self, task_id: str) -> float:
        """停止计时
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务持续时间
        """
        if task_id in self.start_times:
            end_time = time.time()
            duration = end_time - self.start_times[task_id]
            self.end_times[task_id] = end_time
            self.durations[task_id] = duration
            
            # 提取任务类型
            task_type = task_id.split('_')[0] if '_' in task_id else 'general'
            
            # 记录到智能超时预测器
            self.smart_timeout.record_duration(task_type, duration)
            
            # 记录到贝叶斯超时预测器
            self.bayesian_manager.record_duration(task_type, duration)
            
            # 记录到历史
            self.context_history.append({
                'task_id': task_id,
                'task_type': task_type,
                'start_time': self.start_times[task_id],
                'end_time': end_time,
                'duration': duration,
                'timestamp': time.time(),
                'time_context': self.time_anchor.get_time_context()
            })
            
            # 注销任务
            self.anomaly_detector.unregister_task(task_id)
            
            return duration
        return 0.0
    
    def get_elapsed_time(self, task_id: str) -> float:
        """获取已用时间
        
        Args:
            task_id: 任务ID
            
        Returns:
            已用时间
        """
        if task_id in self.start_times:
            return time.time() - self.start_times[task_id]
        return 0.0
    
    def get_average_duration(self, task_type: str) -> float:
        """获取任务类型的平均执行时间
        
        Args:
            task_type: 任务类型
            
        Returns:
            平均执行时间
        """
        relevant_durations = []
        for entry in self.context_history:
            if entry.get('task_type') == task_type:
                relevant_durations.append(entry['duration'])
        
        if relevant_durations:
            return np.mean(relevant_durations)
        return 0.0
    
    def predict_duration(self, task_type: str, complexity: float = 1.0) -> float:
        """预测任务执行时间
        
        Args:
            task_type: 任务类型
            complexity: 复杂度因子
            
        Returns:
            预测的执行时间
        """
        # 1. 使用贝叶斯预测器（优先）
        bayesian_prediction = self.bayesian_manager.predict_timeout(task_type)
        if bayesian_prediction > 0:
            return bayesian_prediction * complexity
        
        # 2. 使用智能超时预测器
        timeout_prediction = self.smart_timeout.predict_timeout(task_type)
        if timeout_prediction > 0:
            return timeout_prediction * complexity
        
        # 3. 回退到传统预测
        avg_duration = self.get_average_duration(task_type)
        if avg_duration > 0:
            return avg_duration * complexity
        
        # 4. 默认预测值
        default_durations = {
            'download': 5.0,      # 下载
            'analysis': 30.0,     # 分析
            'code_generation': 10.0,  # 代码生成
            'api_call': 1.0,      # API调用
            'file_operation': 2.0,    # 文件操作
        }
        
        return default_durations.get(task_type, 5.0) * complexity
    
    def is_taking_too_long(self, task_id: str, expected_duration: float, threshold: float = 1.5) -> bool:
        """判断任务是否执行时间过长
        
        Args:
            task_id: 任务ID
            expected_duration: 预期执行时间
            threshold: 阈值因子
            
        Returns:
            是否执行时间过长
        """
        elapsed = self.get_elapsed_time(task_id)
        
        # 提取任务类型
        task_type = task_id.split('_')[0] if '_' in task_id else 'general'
        
        # 使用智能超时预测进行实时调整
        adjusted_timeout = self.smart_timeout.adjust_timeout_realtime(
            task_type, elapsed, expected_duration
        )
        
        return elapsed > adjusted_timeout
    
    def add_context(self, context: Dict[str, Any]):
        """添加上下文信息
        
        Args:
            context: 上下文信息
        """
        context['timestamp'] = time.time()
        context['time_context'] = self.time_anchor.get_time_context()
        self.context_history.append(context)
    
    def get_recent_context(self, time_window: float = 300.0) -> List[Dict[str, Any]]:
        """获取最近的上下文信息
        
        Args:
            time_window: 时间窗口（秒）
            
        Returns:
            最近的上下文信息
        """
        cutoff_time = time.time() - time_window
        return [entry for entry in self.context_history if entry['timestamp'] >= cutoff_time]
    
    def clear_history(self):
        """清空历史记录
        """
        self.context_history = []
    
    def export_history(self) -> pd.DataFrame:
        """导出历史记录为DataFrame
        
        Returns:
            历史记录DataFrame
        """
        return pd.DataFrame(self.context_history)
    
    def get_time_context(self, timezone: Optional[str] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        """获取时间上下文
        
        Args:
            timezone: 时区
            session_id: 会话ID
            
        Returns:
            时间上下文信息
        """
        return self.time_anchor.get_time_context(timezone, session_id)
    
    def inject_time_anchor(self, prompt: str, timezone: Optional[str] = None, session_id: Optional[str] = None) -> str:
        """注入时间锚点到提示词
        
        Args:
            prompt: 原始提示词
            timezone: 时区
            session_id: 会话ID
            
        Returns:
            注入时间锚点后的提示词
        """
        return self.time_anchor.inject_time_anchor(prompt, timezone, session_id)
    
    def create_session(self, session_id: str, timezone: str = 'Asia/Shanghai'):
        """创建会话时间上下文
        
        Args:
            session_id: 会话ID
            timezone: 时区
        """
        return self.time_anchor.create_session(session_id, timezone)
    
    def get_task_statistics(self, task_type: str) -> Dict[str, Any]:
        """获取任务统计信息
        
        Args:
            task_type: 任务类型
            
        Returns:
            任务统计信息
        """
        return self.smart_timeout.get_task_statistics(task_type)
    
    def get_prediction_confidence(self, task_type: str) -> float:
        """获取预测置信度
        
        Args:
            task_type: 任务类型
            
        Returns:
            预测置信度
        """
        # 优先使用贝叶斯预测器的置信度
        predictor = self.bayesian_manager.get_predictor(task_type)
        return predictor.get_confidence()
    
    def get_bayesian_stats(self, task_type: str) -> Dict[str, Any]:
        """获取贝叶斯预测器统计信息
        
        Args:
            task_type: 任务类型
            
        Returns:
            贝叶斯预测器统计信息
        """
        predictor = self.bayesian_manager.get_predictor(task_type)
        return predictor.get_posterior_stats()
    
    def get_all_bayesian_stats(self) -> Dict[str, Dict[str, Any]]:
        """获取所有任务类型的贝叶斯预测器统计信息
        
        Returns:
            所有任务类型的贝叶斯预测器统计信息
        """
        return self.bayesian_manager.get_all_stats()
    
    def get_calibration_report(self) -> Dict[str, Dict[str, Any]]:
        """获取校准报告
        
        Returns:
            校准报告
        """
        return self.bayesian_manager.get_calibration_report()
    
    def update_task_progress(self, task_id: str, progress: float):
        """更新任务进度
        
        Args:
            task_id: 任务ID
            progress: 进度 0.0 ~ 1.0
        """
        self.anomaly_detector.update_progress(task_id, progress)
    
    def detect_task_anomaly(self, task_id: str) -> Dict[str, Any]:
        """检测任务异常
        
        Args:
            task_id: 任务ID
            
        Returns:
            异常检测结果
        """
        return self.anomaly_detector.detect_blockage(task_id)
    
    def mark_dependency_blocked(self, task_id: str, blocked_by: str):
        """标记任务被依赖阻塞
        
        Args:
            task_id: 任务ID
            blocked_by: 阻塞它的任务ID
        """
        self.anomaly_detector.mark_dependency_blocked(task_id, blocked_by)
    
    def record_external_failure(self, task_id: str):
        """记录外部失败
        
        Args:
            task_id: 任务ID
        """
        self.anomaly_detector.record_external_failure(task_id)
    
    def clear_external_failures(self, task_id: str):
        """清除外部失败计数
        
        Args:
            task_id: 任务ID
        """
        self.anomaly_detector.clear_external_failures(task_id)
    
    def get_all_abnormal_events(self) -> List[Dict[str, Any]]:
        """获取所有异常事件
        
        Returns:
            异常事件列表
        """
        return self.anomaly_detector.get_abnormal_events()
    
    def get_all_blockages(self) -> List[Dict[str, Any]]:
        """获取所有阻塞任务
        
        Returns:
            阻塞任务列表
        """
        return self.anomaly_detector.get_all_blockages()
    
    def on_anomaly(self, callback):
        """注册异常回调
        
        Args:
            callback: 回调函数
        """
        self.anomaly_detector.on('on_anomaly', callback)
    
    def record_utterance(self, speaker: str, content: str, timestamp: Optional[float] = None):
        """记录对话
        
        Args:
            speaker: 说话者
            content: 内容
            timestamp: 时间戳
        """
        self.social_temporal.record_utterance(speaker, content, timestamp)
    
    def get_pause_duration(self) -> float:
        """获取当前停顿时间
        
        Returns:
            停顿时间
        """
        return self.social_temporal.get_pause_duration()
    
    def get_pause_type(self, duration: Optional[float] = None) -> str:
        """获取停顿类型
        
        Args:
            duration: 停顿时间
            
        Returns:
            停顿类型
        """
        return self.social_temporal.get_pause_type(duration)
    
    def should_respond(self) -> bool:
        """判断是否应该回应
        
        Returns:
            是否应该回应
        """
        return self.social_temporal.should_respond()
    
    def is_interruption(self, timestamp: Optional[float] = None) -> bool:
        """判断是否是打断
        
        Args:
            timestamp: 时间戳
            
        Returns:
            是否是打断
        """
        return self.social_temporal.is_interruption(timestamp)
    
    def get_context_timeliness(self, context_timestamp: float) -> str:
        """获取上下文时效性
        
        Args:
            context_timestamp: 上下文时间戳
            
        Returns:
            时效性
        """
        return self.social_temporal.get_context_timeliness(context_timestamp)
    
    def get_conversation_flow(self) -> List[Dict[str, Any]]:
        """获取对话流程
        
        Returns:
            对话流程
        """
        return self.social_temporal.get_conversation_flow()
    
    def clear_conversation_history(self):
        """清空对话历史
        """
        self.social_temporal.clear_history()
    
    def set_pause_thresholds(self, short: float, medium: float, long: float):
        """设置停顿阈值
        
        Args:
            short: 短停顿阈值
            medium: 中等停顿阈值
            long: 长停顿阈值
        """
        self.social_temporal.set_pause_thresholds(short, medium, long)