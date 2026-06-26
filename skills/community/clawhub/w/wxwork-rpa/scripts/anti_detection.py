#!/usr/bin/env python3
"""
反检测策略
包含随机化、模式变化、行为伪装
"""

import time
import random
import hashlib
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AntiDetection:
    """反检测策略管理器"""

    def __init__(self):
        self.behavior_fingerprint = self._generate_behavior_fingerprint()
        self.activity_log = []
        self.last_pattern_change = time.time()
        self.current_pattern = 'slow'

        # 行为模式配置
        self.behavior_patterns = {
            'normal': {
                'mouse_speed': 0.3,
                'typing_speed': 0.5,
                'click_delay': 0.2,
                'scroll_speed': 1.0
            },
            'slow': {
                'mouse_speed': 0.5,
                'typing_speed': 1,
                'click_delay': 0.4,
                'scroll_speed': 0.5
            },
            'fast': {
                'mouse_speed': 0.2,
                'typing_speed': 0.05,
                'click_delay': 0.1,
                'scroll_speed': 2.0
            },
            'random': {
                'mouse_speed': random.uniform(0.2, 0.5),
                'typing_speed': random.uniform(0.05, 0.2),
                'click_delay': random.uniform(0.1, 0.4),
                'scroll_speed': random.uniform(0.5, 2.0)
            }
        }

    def _generate_behavior_fingerprint(self) -> str:
        """生成行为指纹"""
        # 使用多个因素生成唯一指纹
        factors = [
            str(time.time()),
            str(random.random()),
            str(hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8])
        ]

        fingerprint = hashlib.sha256(''.join(factors).encode()).hexdigest()[:16]
        logger.info(f"生成行为指纹: {fingerprint}")
        return fingerprint

    def should_change_pattern(self) -> bool:
        """判断是否需要改变行为模式"""
        current_time = time.time()

        # 每30-60分钟随机改变一次模式
        if current_time - self.last_pattern_change > random.randint(1800, 3600):
            return True

        # 或者根据活动频率决定
        recent_activities = self._get_recent_activities(minutes=5)
        if len(recent_activities) > 50:  # 5分钟内活动超过50次
            return True

        return False

    def get_next_pattern(self) -> str:
        """获取下一个行为模式"""
        patterns = list(self.behavior_patterns.keys())

        # 避免连续使用相同模式
        available_patterns = [p for p in patterns if p != self.current_pattern]

        if not available_patterns:
            available_patterns = patterns

        next_pattern = random.choice(available_patterns)
        self.current_pattern = next_pattern
        self.last_pattern_change = time.time()

        logger.info(f"切换行为模式: {next_pattern}")
        return next_pattern

    def get_pattern_config(self, pattern: Optional[str] = None) -> Dict[str, float]:
        """获取指定模式的配置"""
        if pattern is None:
            pattern = self.current_pattern

        config = self.behavior_patterns.get(pattern, self.behavior_patterns['normal'])

        # 添加微小随机变化
        randomized_config = {}
        for key, value in config.items():
            # ±10%的随机变化
            variation = value * random.uniform(-0.1, 0.1)
            randomized_config[key] = max(0.01, value + variation)

        return randomized_config

    def log_activity(self, activity_type: str, details: Dict[str, Any]):
        """记录活动日志"""
        activity = {
            'timestamp': datetime.now(),
            'type': activity_type,
            'details': details,
            'fingerprint': self.behavior_fingerprint
        }

        self.activity_log.append(activity)

        # 限制日志大小
        if len(self.activity_log) > 1000:
            self.activity_log = self.activity_log[-1000:]

    def _get_recent_activities(self, minutes: int = 5) -> list:
        """获取最近的活动"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [a for a in self.activity_log if a['timestamp'] > cutoff_time]

    def add_random_variation(self, value: float, variation_percent: float = 0.1) -> float:
        """添加随机变化"""
        variation = value * random.uniform(-variation_percent, variation_percent)
        return value + variation

    def simulate_human_imperfections(self):
        """模拟人类的不完美行为"""
        # 随机微小延迟
        tiny_delay = random.uniform(0.01, 0.05)
        time.sleep(tiny_delay)

        # 随机无效操作（概率很低）
        if random.random() < 0.001:
            # 模拟误点击或误操作
            self._simulate_mistake()

    def _simulate_mistake(self):
        """模拟误操作"""
        mistake_type = random.choice(['double_click', 'wrong_click', 'accidental_scroll'])

        if mistake_type == 'double_click':
            # 模拟意外双击
            logger.debug("模拟意外双击")
        elif mistake_type == 'wrong_click':
            # 模拟点错位置
            logger.debug("模拟点错位置")
        elif mistake_type == 'accidental_scroll':
            # 模拟意外滚动
            logger.debug("模拟意外滚动")

    def get_safe_delay(self, base_delay: float) -> float:
        """获取安全的延迟时间（避免规律性）"""
        # 使用随机分布，避免固定间隔
        if base_delay < 0.5:
            # 短延迟使用均匀分布
            delay = random.uniform(base_delay * 0.8, base_delay * 1.2)
        else:
            # 长延迟使用正态分布
            delay = random.normalvariate(base_delay, base_delay * 0.2)

        # 确保最小延迟
        return max(0.1, delay)