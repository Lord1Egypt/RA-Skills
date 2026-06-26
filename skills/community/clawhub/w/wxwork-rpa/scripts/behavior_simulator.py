#!/usr/bin/env python3
"""
人类行为模拟增强
包含随机抖动、行为模式、反检测策略
"""

import time
import random
import math
from typing import List, Tuple, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class BehaviorSimulator:
    """人类行为模拟器"""

    def __init__(self):
        self.behavior_patterns = self._load_behavior_patterns()
        self.last_activity_time = time.time()
        self.activity_history = []

    def _load_behavior_patterns(self) -> Dict[str, Any]:
        """加载行为模式"""
        return {
            'slow_typer': {
                'min_delay': 0.1,
                'max_delay': 0.3,
                'error_rate': 0.02,
                'backspace_rate': 0.01
            },
            'fast_typer': {
                'min_delay': 0.05,
                'max_delay': 0.15,
                'error_rate': 0.01,
                'backspace_rate': 0.005
            },
            'careful_typer': {
                'min_delay': 0.15,
                'max_delay': 0.4,
                'error_rate': 0.005,
                'backspace_rate': 0.002
            }
        }

    def get_mouse_trajectory(self, start_x: int, start_y: int,
                             end_x: int, end_y: int,
                             behavior_type: str = 'natural') -> List[Tuple[int, int]]:
        """
        生成模拟人类的鼠标轨迹
        """
        if behavior_type == 'natural':
            return self._natural_mouse_trajectory(start_x, start_y, end_x, end_y)
        elif behavior_type == 'direct':
            return self._direct_mouse_trajectory(start_x, start_y, end_x, end_y)
        elif behavior_type == 'hesitant':
            return self._hesitant_mouse_trajectory(start_x, start_y, end_x, end_y)
        else:
            return self._natural_mouse_trajectory(start_x, start_y, end_x, end_y)

    def _natural_mouse_trajectory(self, start_x: int, start_y: int,
                                  end_x: int, end_y: int) -> List[Tuple[int, int]]:
        """自然鼠标轨迹"""
        points = []

        # 计算距离
        distance = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)

        # 根据距离确定点数
        num_points = max(10, int(distance / 5))

        # 使用改进的贝塞尔曲线
        control_points = self._generate_control_points(start_x, start_y, end_x, end_y)

        for i in range(num_points):
            t = i / (num_points - 1)

            # 计算贝塞尔曲线点
            x, y = self._bezier_point(t, start_x, start_y,
                                      control_points[0], control_points[1],
                                      control_points[2], control_points[3],
                                      end_x, end_y)

            # 添加物理抖动（模拟手部微颤）
            if i > 0 and i < num_points - 1:
                x += random.randint(-2, 2)
                y += random.randint(-2, 2)

            points.append((int(x), int(y)))

        # 在终点附近添加微调（模拟瞄准）
        for _ in range(3):
            adjust_x = end_x + random.randint(-3, 3)
            adjust_y = end_y + random.randint(-3, 3)
            points.append((adjust_x, adjust_y))

        points.append((end_x, end_y))

        return points

    def _generate_control_points(self, start_x: int, start_y: int,
                                 end_x: int, end_y: int) -> Tuple:
        """生成贝塞尔曲线控制点"""
        # 中点
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2

        # 随机偏移量
        offset_x = (end_x - start_x) * random.uniform(0.1, 0.3)
        offset_y = (end_y - start_y) * random.uniform(0.1, 0.3)

        # 控制点1（靠近起点）
        cp1_x = start_x + offset_x * random.uniform(0.3, 0.7)
        cp1_y = start_y + offset_y * random.uniform(0.3, 0.7)

        # 控制点2（靠近终点）
        cp2_x = end_x - offset_x * random.uniform(0.3, 0.7)
        cp2_y = end_y - offset_y * random.uniform(0.3, 0.7)

        return (cp1_x, cp1_y, cp2_x, cp2_y)

    def _bezier_point(self, t: float, *points) -> Tuple[float, float]:
        """计算n阶贝塞尔曲线点"""
        n = len(points) // 2 - 1

        if n == 0:
            return points[0], points[1]

        new_points = []
        for i in range(n):
            x = (1 - t) * points[i * 2] + t * points[(i + 1) * 2]
            y = (1 - t) * points[i * 2 + 1] + t * points[(i + 1) * 2 + 1]
            new_points.extend([x, y])

        return self._bezier_point(t, *new_points)

    def simulate_typing_with_errors(self, text: str, pattern: str = 'natural') -> str:
        """
        模拟带错别字的打字
        返回实际输入的文本
        """
        if pattern == 'natural':
            error_rate = 0.01  # 1%的错误率
            backspace_rate = 0.005  # 0.5%的回退率
        else:
            pattern_config = self.behavior_patterns.get(pattern,
                                                        self.behavior_patterns['slow_typer'])
            error_rate = pattern_config['error_rate']
            backspace_rate = pattern_config['backspace_rate']

        result = []
        i = 0

        while i < len(text):
            char = text[i]

            # 判断是否输入错误
            if random.random() < error_rate:
                # 输入错别字
                typo = self._generate_typo(char)
                result.append(typo)

                # 判断是否立即修正
                if random.random() < 0.7:
                    # 立即修正
                    result.append('\b')  # 退格
                    result.append(char)
                else:
                    # 稍后修正（几个字符后）
                    pass
            else:
                result.append(char)

            # 随机回退（模拟删除重输）
            if random.random() < backspace_rate and len(result) > 1:
                backspace_count = random.randint(1, 3)
                for _ in range(min(backspace_count, len(result))):
                    result.append('\b')

            i += 1

        return ''.join(result)

    def _generate_typo(self, char: str) -> str:
        """生成常见错别字"""
        # 常见中文错别字映射
        chinese_typos = {
            '的': ['得', '地'],
            '在': ['再'],
            '是': ['时'],
            '和': ['或'],
            '了': ['啦', '咯'],
            '吗': ['嘛'],
            '吧': ['把'],
            '这': ['着'],
            '那': ['哪'],
            '他': ['她', '它'],
            '你': ['您'],
            '我': ['偶', '窝'],
        }

        # 常见英文错别字映射
        english_typos = {
            'a': 's', 'b': 'v', 'c': 'x', 'd': 's', 'e': 'r',
            'f': 'g', 'g': 'h', 'h': 'j', 'i': 'o', 'j': 'k',
            'k': 'l', 'l': 'k', 'm': 'n', 'n': 'm', 'o': 'p',
            'p': 'o', 'q': 'w', 'r': 't', 's': 'd', 't': 'r',
            'u': 'i', 'v': 'b', 'w': 'q', 'x': 'c', 'y': 'u',
            'z': 'x'
        }

        if '\u4e00' <= char <= '\u9fff':  # 中文字符
            return random.choice(chinese_typos.get(char, [char]))
        elif char.lower() in english_typos:
            return english_typos[char.lower()]
        else:
            return char

    def add_random_delay(self, base_delay: float = 1.0,
                         variation: float = 0.3) -> float:
        """
        添加随机延迟，模拟人类反应时间
        """
        # 使用正态分布，但限制在合理范围内
        delay = random.normalvariate(base_delay, variation * base_delay)
        delay = max(0.1, min(delay, base_delay * 2))

        # 记录活动时间
        self.last_activity_time = time.time()
        self.activity_history.append({
            'time': datetime.now(),
            'delay': delay,
            'type': 'wait'
        })

        return delay

    def simulate_thinking_time(self, text_length: int = 0) -> float:
        """
        模拟思考时间（根据文本长度）
        """
        if text_length == 0:
            # 随机思考时间
            think_time = random.uniform(0.5, 2.0)
        else:
            # 根据文本长度计算思考时间
            base_time = text_length * 0.1
            think_time = random.uniform(base_time * 0.5, base_time * 1.5)
            think_time = min(think_time, 5.0)  # 最多5秒

        time.sleep(think_time)
        return think_time

    def get_random_behavior_pattern(self) -> str:
        """获取随机行为模式"""
        patterns = list(self.behavior_patterns.keys())
        return random.choice(patterns)