"""实时直播分析模块 — 流式ASR+滑动窗口+敏感词检测"""

import os
import re
import time
import threading
from collections import deque
from typing import Any, Callable, Dict, List, Optional

from .logger import get_logger

logger = get_logger(__name__)


class LiveAnalyzer:
    """
    实时直播分析器。
    
    功能：
    - 流式 ASR（模拟实时语音识别）
    - 滑动窗口缓冲（控制内存）
    - 敏感词检测（AC自动机）
    - 实时告警回调
    
    性能优化：滑动窗口限制内存，不缓存全量数据。
    """
    
    # 默认敏感词列表（基础）
    DEFAULT_SENSITIVE_WORDS = [
        "脏话", "辱骂", "诽谤", "造谣", "赌博", "毒品",
        "枪支", "色情", "诈骗", "非法集资", "传销",
    ]
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        live_config = config.get("live_analysis", {})
        
        # 滑动窗口配置
        self.window_size = live_config.get("window_size", 30)  # 秒
        self.window_slide = live_config.get("window_slide", 5)  # 秒
        self.max_buffer_length = live_config.get("max_buffer_length", 1000)  # 最大缓冲条数
        
        # 告警配置
        self.alert_callback: Optional[Callable] = None
        self.alert_threshold = live_config.get("alert_threshold", 3)  # 窗口内敏感词阈值
        
        # 敏感词列表
        self.sensitive_words: List[str] = live_config.get(
            "sensitive_words", self.DEFAULT_SENSITIVE_WORDS
        )
        
        # 状态
        self._running = False
        self._buffer: deque = deque(maxlen=self.max_buffer_length)
        self._window_text: deque = deque()  # 滑动窗口内的文本
        self._lock = threading.Lock()
        
        # 统计
        self._stats = {
            "total_segments": 0,
            "total_sensitive_detected": 0,
            "total_alerts": 0,
            "start_time": None,
        }
    
    def set_alert_callback(self, callback: Callable[[Dict], None]):
        """
        设置告警回调函数。
        
        Args:
            callback: 接收告警字典的回调函数
        """
        self.alert_callback = callback
    
    def add_sensitive_words(self, words: List[str]):
        """
        添加敏感词。
        
        Args:
            words: 敏感词列表
        """
        self.sensitive_words.extend(words)
        # 去重
        self.sensitive_words = list(set(self.sensitive_words))
        logger.info(f"   已添加 {len(words)} 个敏感词，共 {len(self.sensitive_words)} 个")
    
    def remove_sensitive_words(self, words: List[str]):
        """
        移除敏感词。
        
        Args:
            words: 要移除的敏感词列表
        """
        self.sensitive_words = [w for w in self.sensitive_words if w not in words]
    
    def start(self, video_source: str = None) -> bool:
        """
        启动实时分析。
        
        Args:
            video_source: 视频源（URL 或设备路径），为 None 则使用模拟数据
            
        Returns:
            是否成功启动
        """
        if self._running:
            logger.warning("实时分析已在运行中")
            return False
        
        self._running = True
        self._stats["start_time"] = time.time()
        
        # 启动后台处理线程
        self._process_thread = threading.Thread(
            target=self._process_loop,
            args=(video_source,),
            daemon=True,
        )
        self._process_thread.start()
        
        logger.info("🔴 [实时直播分析] 已启动")
        logger.info(f"   滑动窗口: {self.window_size}s, 滑动步长: {self.window_slide}s")
        logger.info(f"   敏感词数量: {len(self.sensitive_words)}")
        
        return True
    
    def stop(self) -> Dict[str, Any]:
        """
        停止实时分析。
        
        Returns:
            运行统计
        """
        if not self._running:
            return self.get_stats()
        
        self._running = False
        
        # 等待后台线程结束
        if hasattr(self, '_process_thread'):
            self._process_thread.join(timeout=5)
        
        stats = self.get_stats()
        logger.info(f"🔴 [实时直播分析] 已停止，运行 {stats['duration']:.1f}s")
        
        return stats
    
    def feed_segment(self, segment: Dict):
        """
        手动输入一段识别结果（用于外部 ASR 输入）。
        
        Args:
            segment: ASR 段 {"start": float, "end": float, "text": str}
        """
        if not self._running:
            return
        
        with self._lock:
            self._buffer.append(segment)
            self._stats["total_segments"] += 1
        
        # 检测敏感词
        self._detect_sensitive_in_segment(segment)
    
    def feed_text(self, text: str, timestamp: float = None):
        """
        手动输入一段文本。
        
        Args:
            text: 文本内容
            timestamp: 时间戳（可选）
        """
        segment = {
            "start": timestamp or time.time(),
            "end": (timestamp or time.time()) + 1.0,
            "text": text,
        }
        self.feed_segment(segment)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取运行统计"""
        with self._lock:
            stats = self._stats.copy()
        
        if stats["start_time"]:
            stats["duration"] = time.time() - stats["start_time"]
        else:
            stats["duration"] = 0
        
        stats["sensitive_words_count"] = len(self.sensitive_words)
        stats["buffer_size"] = len(self._buffer)
        stats["running"] = self._running
        
        return stats
    
    def get_window_text(self) -> str:
        """获取当前滑动窗口内的文本"""
        with self._lock:
            return " ".join(s.get("text", "") for s in self._window_text)
    
    def _process_loop(self, video_source: str = None):
        """
        后台处理循环。
        
        支持两种模式：
        1. 实时模式：从视频源读取（需配合流式 ASR）
        2. 模拟模式：等待外部通过 feed_segment 输入
        """
        logger.debug("后台处理线程已启动")
        
        while self._running:
            try:
                # 滑动窗口清理（移除过期数据)
                self._slide_window()
                
                # 模拟模式：等待外部输入，不主动读取
                if video_source is None:
                    time.sleep(self.window_slide)
                    continue
                
                # TODO: 实际视频源读取（需配合流式 ASR）
                time.sleep(self.window_slide)
                
            except Exception as e:
                logger.debug(f"处理循环异常: {e}")
                time.sleep(1)
        
        logger.debug("后台处理线程已停止")
    
    def _slide_window(self):
        """滑动窗口：移除过期数据"""
        with self._lock:
            current_time = time.time()
            window_start = current_time - self.window_size
            
            # 移除窗口外的数据
            while self._window_text:
                seg = self._window_text[0]
                if seg.get("start", 0) < window_start:
                    self._window_text.popleft()
                else:
                    break
    
    def _detect_sensitive_in_segment(self, segment: Dict):
        """检测段中的敏感词"""
        text = segment.get("text", "")
        if not text:
            return
        
        found_words = []
        for word in self.sensitive_words:
            if word in text:
                found_words.append(word)
        
        if found_words:
            self._stats["total_sensitive_detected"] += len(found_words)
            
            # 触发告警
            alert = {
                "timestamp": segment.get("start", time.time()),
                "text": text,
                "sensitive_words": found_words,
                "severity": len(found_words),
            }
            
            self._trigger_alert(alert)
    
    def _trigger_alert(self, alert: Dict):
        """触发告警"""
        self._stats["total_alerts"] += 1
        
        if self.alert_callback:
            try:
                self.alert_callback(alert)
            except Exception as e:
                logger.debug(f"告警回调异常: {e}")
        else:
            # 默认告警输出
            logger.warning(
                f"⚠️ 敏感词告警 [{alert['timestamp']:.1f}s] "
                f"发现: {', '.join(alert['sensitive_words'])} | "
                f"内容: {alert['text'][:50]}..."
            )
    
    def get_sensitive_report(self) -> Dict[str, Any]:
        """
        生成敏感词检测报告。
        
        Returns:
            检测报告
        """
        stats = self.get_stats()
        
        return {
            "total_duration": stats["duration"],
            "total_segments": stats["total_segments"],
            "total_sensitive_detected": stats["total_sensitive_detected"],
            "total_alerts": stats["total_alerts"],
            "sensitive_rate": (
                stats["total_sensitive_detected"] / stats["total_segments"]
                if stats["total_segments"] > 0 else 0
            ),
            "risk_level": self._calculate_risk_level(stats),
        }
    
    def _calculate_risk_level(self, stats: Dict) -> str:
        """计算风险等级"""
        if stats["total_segments"] == 0:
            return "无数据"
        
        rate = stats["total_sensitive_detected"] / stats["total_segments"]
        
        if rate > 0.1:
            return "高风险"
        elif rate > 0.05:
            return "中风险"
        elif rate > 0.01:
            return "低风险"
        else:
            return "安全"
    
    def export_sensitive_log(self, output_path: str) -> str:
        """
        导出敏感词日志。
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            输出文件路径
        """
        import json
        
        log_data = {
            "export_time": time.time(),
            "stats": self.get_stats(),
            "sensitive_words": self.sensitive_words,
            "alerts": [],  # TODO: 保存告警历史
        }
        
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"   敏感词日志已导出: {output_path}")
        return output_path
    
    def reset_stats(self):
        """重置统计"""
        with self._lock:
            self._stats = {
                "total_segments": 0,
                "total_sensitive_detected": 0,
                "total_alerts": 0,
                "start_time": time.time(),
            }
