import time
import threading
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@dataclass
class SessionTimeContext:
    """会话时间上下文"""
    session_id: str
    start_time: float
    last_sync_time: float
    time_offset: float = 0.0
    timezone: str = 'Asia/Shanghai'


class TimeAnchorInjector:
    """增强版时间锚点注入器

    解决"不知道现在是何时"的问题，为AI提供当前时间感知能力
    V2.0增强：
    - 会话级时间管理
    - 高频时间同步
    - 时间漂移检测
    - 多语言时间格式支持
    """

    def __init__(self):
        import pytz
        from geopy.geocoders import Nominatim
        self.geolocator = Nominatim(user_agent="temporal_agent")
        self.default_timezone = pytz.timezone('Asia/Shanghai')  # 默认东八区
        self.session_contexts: Dict[str, SessionTimeContext] = {}
        self._lock = threading.Lock()
        self._sync_interval = 1.0  # 1秒同步一次
        self._max_time_drift = 0.5  # 最大允许时间漂移（秒）

    def create_session(self, session_id: str, timezone: str = 'Asia/Shanghai') -> SessionTimeContext:
        """创建会话时间上下文

        Args:
            session_id: 会话ID
            timezone: 时区

        Returns:
            会话时间上下文
        """
        with self._lock:
            context = SessionTimeContext(
                session_id=session_id,
                start_time=time.time(),
                last_sync_time=time.time(),
                timezone=timezone
            )
            self.session_contexts[session_id] = context
            return context

    def get_session_context(self, session_id: str) -> Optional[SessionTimeContext]:
        """获取会话时间上下文

        Args:
            session_id: 会话ID

        Returns:
            会话时间上下文，如果不存在返回None
        """
        with self._lock:
            return self.session_contexts.get(session_id)

    def remove_session(self, session_id: str):
        """移除会话时间上下文

        Args:
            session_id: 会话ID
        """
        with self._lock:
            if session_id in self.session_contexts:
                del self.session_contexts[session_id]

    def get_current_timestamp(self, session_id: Optional[str] = None) -> float:
        """获取当前时间戳

        Args:
            session_id: 会话ID，用于会话级时间管理

        Returns:
            当前时间戳
        """
        if session_id:
            context = self.get_session_context(session_id)
            if context:
                current_time = time.time()
                # 检查时间漂移
                time_since_sync = current_time - context.last_sync_time
                if time_since_sync > self._sync_interval:
                    # 重新同步
                    context.last_sync_time = current_time
                    context.time_offset = 0  # 重置偏移
                return current_time + context.time_offset
        return time.time()

    def get_current_time(self, timezone: Optional[str] = None, session_id: Optional[str] = None) -> datetime:
        """获取当前时间

        Args:
            timezone: 时区，如 'Asia/Shanghai'
            session_id: 会话ID，用于会话级时间管理

        Returns:
            当前时间
        """
        import pytz
        if timezone:
            tz = pytz.timezone(timezone)
        else:
            tz = self.default_timezone

        timestamp = self.get_current_timestamp(session_id)
        return datetime.fromtimestamp(timestamp, tz)

    def get_time_string(self, timezone: Optional[str] = None, format: str = "%Y-%m-%d %H:%M:%S", session_id: Optional[str] = None) -> str:
        """获取当前时间字符串

        Args:
            timezone: 时区
            format: 时间格式
            session_id: 会话ID，用于会话级时间管理

        Returns:
            当前时间字符串
        """
        current_time = self.get_current_time(timezone, session_id)
        return current_time.strftime(format)

    def get_time_context(self, timezone: Optional[str] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        """获取时间上下文

        Args:
            timezone: 时区
            session_id: 会话ID，用于会话级时间管理

        Returns:
            时间上下文信息
        """
        current_time = self.get_current_time(timezone, session_id)

        return {
            'current_time': current_time.strftime("%Y-%m-%d %H:%M:%S"),
            'current_date': current_time.strftime("%Y-%m-%d"),
            'current_time_only': current_time.strftime("%H:%M:%S"),
            'day_of_week': current_time.strftime("%A"),
            'day_of_week_chinese': self._get_day_of_week_chinese(current_time.weekday()),
            'month': current_time.strftime("%B"),
            'month_chinese': self._get_month_chinese(current_time.month),
            'year': current_time.year,
            'timestamp': self.get_current_timestamp(session_id),
            'timezone': str(current_time.tzinfo),
            'is_weekend': current_time.weekday() in [5, 6],
            'is_morning': 6 <= current_time.hour < 12,
            'is_afternoon': 12 <= current_time.hour < 18,
            'is_evening': 18 <= current_time.hour < 22,
            'is_night': current_time.hour >= 22 or current_time.hour < 6,
            'time_since_epoch': int(self.get_current_timestamp(session_id)),
            'iso_format': current_time.isoformat(),
            'relative_time': self._get_relative_time(current_time)
        }

    def inject_time_anchor(self, prompt: str, timezone: Optional[str] = None, session_id: Optional[str] = None) -> str:
        """注入时间锚点到提示词

        Args:
            prompt: 原始提示词
            timezone: 时区
            session_id: 会话ID，用于会话级时间管理

        Returns:
            注入时间锚点后的提示词
        """
        time_context = self.get_time_context(timezone, session_id)

        # 替换动态变量
        injected_prompt = prompt
        for key, value in time_context.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in injected_prompt:
                injected_prompt = injected_prompt.replace(placeholder, str(value))

        # 强制注入当前时间（确保时间信息总是最新）
        if "{{current_time}}" in injected_prompt:
            injected_prompt = injected_prompt.replace("{{current_time}}", time_context['current_time'])

        # 注入时间锚点头部（确保智能体总是看到最新时间）
        time_anchor_header = f"\n[时间锚点] 当前时间：{time_context['current_time']} | 时区：{time_context['timezone']} | 星期：{time_context['day_of_week_chinese']}\n"
        if "[时间锚点]" not in injected_prompt:
            injected_prompt = time_anchor_header + injected_prompt

        return injected_prompt

    def get_timezone_by_location(self, location: str) -> Optional[str]:
        """根据地理位置获取时区

        Args:
            location: 地理位置，如 "惠州"

        Returns:
            时区字符串
        """
        try:
            location_info = self.geolocator.geocode(location)
            if location_info:
                # 这里简化处理，实际应该根据经纬度查询时区
                # 对于中国城市，统一返回东八区
                if '中国' in location or 'China' in location:
                    return 'Asia/Shanghai'
                return 'Asia/Shanghai'  # 默认返回东八区
        except Exception:
            pass
        return None

    def _get_day_of_week_chinese(self, weekday: int) -> str:
        """获取星期的中文表示

        Args:
            weekday: 星期几（0-6，0表示周一）

        Returns:
            星期的中文表示
        """
        days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return days[weekday]

    def _get_month_chinese(self, month: int) -> str:
        """获取月份的中文表示

        Args:
            month: 月份（1-12）

        Returns:
            月份的中文表示
        """
        months = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
        return months[month - 1]

    def _get_relative_time(self, current_time: datetime) -> str:
        """获取相对时间描述

        Args:
            current_time: 当前时间

        Returns:
            相对时间描述
        """
        hour = current_time.hour
        if 6 <= hour < 9:
            return "早晨"
        elif 9 <= hour < 12:
            return "上午"
        elif 12 <= hour < 14:
            return "中午"
        elif 14 <= hour < 18:
            return "下午"
        elif 18 <= hour < 22:
            return "晚上"
        else:
            return "深夜"

    def get_relative_time(self, timestamp: float) -> str:
        """获取相对时间

        Args:
            timestamp: 时间戳

        Returns:
            相对时间描述
        """
        now = time.time()
        diff = now - timestamp
        
        if diff < 60:
            return f"{int(diff)}秒前"
        elif diff < 3600:
            minutes = int(diff // 60)
            return f"{minutes}分钟前"
        elif diff < 86400:
            hours = int(diff // 3600)
            return f"{hours}小时前"
        else:
            days = int(diff // 86400)
            return f"{days}天前"

    def format_time_difference(self, seconds: float) -> str:
        """格式化时间差

        Args:
            seconds: 时间差（秒）

        Returns:
            格式化后的时间差
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        parts = []
        if hours > 0:
            parts.append(f"{hours}小时")
        if minutes > 0:
            parts.append(f"{minutes}分钟")
        if secs > 0 or not parts:
            parts.append(f"{secs}秒")

        return "".join(parts)

    def sync_time(self, session_id: str, reference_time: float):
        """同步时间

        Args:
            session_id: 会话ID
            reference_time: 参考时间戳
        """
        with self._lock:
            context = self.get_session_context(session_id)
            if context:
                current_time = time.time()
                context.time_offset = reference_time - current_time
                context.last_sync_time = current_time

    def get_time_drift(self, session_id: str) -> float:
        """获取时间漂移

        Args:
            session_id: 会话ID

        Returns:
            时间漂移（秒）
        """
        context = self.get_session_context(session_id)
        if context:
            return abs(context.time_offset)
        return 0.0

    def is_time_drift_excessive(self, session_id: str) -> bool:
        """判断时间漂移是否过大

        Args:
            session_id: 会话ID

        Returns:
            是否时间漂移过大
        """
        return self.get_time_drift(session_id) > self._max_time_drift

    def get_all_sessions(self) -> List[SessionTimeContext]:
        """获取所有会话

        Returns:
            会话列表
        """
        with self._lock:
            return list(self.session_contexts.values())

    def clear_all_sessions(self):
        """清除所有会话"""
        with self._lock:
            self.session_contexts.clear()