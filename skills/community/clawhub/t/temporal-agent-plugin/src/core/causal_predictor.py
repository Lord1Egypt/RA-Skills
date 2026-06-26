import time
from typing import Dict, Any, List, Optional, Callable

# 检查依赖项
try:
    import numpy as np
except ImportError:
    raise ImportError("请安装numpy: pip install numpy")

class CausalPredictor:
    """因果预测模型
    
    负责预测动作和结果之间的时间关系，实现精准控制
    """
    
    def __init__(self):
        self.action_history = []
        self.latency_history = {}
    
    def record_action(self, action: str, timestamp: Optional[float] = None):
        """记录动作
        
        Args:
            action: 动作
            timestamp: 时间戳
        """
        if timestamp is None:
            timestamp = time.time()
        
        self.action_history.append({
            'action': action,
            'timestamp': timestamp,
            'result': None,
            'latency': None
        })
    
    def record_result(self, action: str, result: Any, timestamp: Optional[float] = None):
        """记录结果
        
        Args:
            action: 动作
            result: 结果
            timestamp: 时间戳
        """
        if timestamp is None:
            timestamp = time.time()
        
        # 找到最近的相同动作
        for i in reversed(range(len(self.action_history))):
            if self.action_history[i]['action'] == action and self.action_history[i]['result'] is None:
                # 计算延迟
                latency = timestamp - self.action_history[i]['timestamp']
                self.action_history[i]['result'] = result
                self.action_history[i]['latency'] = latency
                
                # 记录到延迟历史
                if action not in self.latency_history:
                    self.latency_history[action] = []
                self.latency_history[action].append(latency)
                
                break
    
    def predict_latency(self, action: str) -> float:
        """预测动作的延迟
        
        Args:
            action: 动作
            
        Returns:
            预测的延迟
        """
        if action in self.latency_history and self.latency_history[action]:
            # 使用历史延迟的平均值
            return np.mean(self.latency_history[action])
        
        # 默认延迟值
        default_latencies = {
            'mouse_click': 0.1,      # 鼠标点击
            'key_press': 0.05,       # 按键
            'api_call': 1.0,         # API调用
            'file_operation': 0.5,   # 文件操作
            'network_request': 0.8,  # 网络请求
        }
        
        return default_latencies.get(action, 0.5)
    
    def predict_result_time(self, action: str) -> float:
        """预测结果出现的时间
        
        Args:
            action: 动作
            
        Returns:
            预测的结果时间
        """
        latency = self.predict_latency(action)
        return time.time() + latency
    
    def get_latency_statistics(self, action: str) -> Dict[str, float]:
        """获取动作的延迟统计信息
        
        Args:
            action: 动作
            
        Returns:
            延迟统计信息
        """
        if action in self.latency_history and self.latency_history[action]:
            latencies = self.latency_history[action]
            return {
                'mean': np.mean(latencies),
                'std': np.std(latencies),
                'min': np.min(latencies),
                'max': np.max(latencies),
                'count': len(latencies)
            }
        
        return {
            'mean': 0.0,
            'std': 0.0,
            'min': 0.0,
            'max': 0.0,
            'count': 0
        }
    
    def get_recent_actions(self, time_window: float = 60.0) -> List[Dict[str, Any]]:
        """获取最近的动作
        
        Args:
            time_window: 时间窗口（秒）
            
        Returns:
            最近的动作
        """
        cutoff_time = time.time() - time_window
        return [action for action in self.action_history if action['timestamp'] >= cutoff_time]
    
    def clear_history(self):
        """清空历史记录
        """
        self.action_history = []
        self.latency_history = {}
    
    def export_history(self) -> List[Dict[str, Any]]:
        """导出历史记录
        
        Returns:
            历史记录
        """
        return self.action_history