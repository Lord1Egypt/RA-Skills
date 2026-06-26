"""
Proactive trigger
Runs via Cron Job to implement calendar events and silence wake-up
"""

import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable, List
from threading import Thread, Event

from .models import UserProfile, Language
from .memory_system import MemorySystem
from .utils.calendar_utils import CalendarUtils
from .config import SILENCE_WAKEUP_HOURS, CRON_CHECK_INTERVAL_SECONDS


class ProactiveTrigger:
    """Proactive trigger core class"""
    
    def __init__(
        self,
        memory_system: MemorySystem,
        message_callback: Optional[Callable[[str, str], None]] = None
    ):
        """
        Args:
            memory_system: Memory system instance
            message_callback: Message callback function (user_id, message) -> None
        """
        self.memory_system = memory_system
        self.message_callback = message_callback
        self._running = False
        self._stop_event = Event()
        self._thread: Optional[Thread] = None
    
    def check_calendar_events(self, user_id: str) -> Optional[str]:
        """
        Condition A: Check calendar events
        If matches holiday/solar term, generate customized greeting
        """
        profile = self.memory_system.load_user_profile(user_id)
        language = profile.language_pref.value
        
        greeting = CalendarUtils.should_trigger_calendar_greeting(language)
        return greeting
    
    def check_silence_wakeup(self, user_id: str) -> Optional[str]:
        """
        Condition B: Silence wake-up
        If last_active_time > 48 hours, generate icebreaker based on memory system
        """
        profile = self.memory_system.load_user_profile(user_id)
        
        # Calculate silence duration
        silence_duration = datetime.now() - profile.last_active_time
        silence_hours = silence_duration.total_seconds() / 3600
        
        if silence_hours < SILENCE_WAKEUP_HOURS:
            return None
        
        # Get memory for generating icebreaker
        memory = self.memory_system.get_memory_for_proactive_message(user_id)
        if not memory:
            # If no memory, use generic greeting (avoid stiff "hello")
            if profile.language_pref == Language.ZH:
                return "最近怎么样？有什么想聊的吗？"
            else:
                return "How have you been? Anything on your mind?"
        
        # Generate context-aware icebreaker based on memory
        return self._generate_icebreaker(memory, profile.language_pref)
    
    def _generate_icebreaker(
        self,
        memory: Dict[str, Any],
        language: Language
    ) -> str:
        """
        Generate icebreaker based on memory
        Prohibits stiff "hello", must combine with context
        """
        entity_type = memory["entity_type"]
        entity_name = memory["entity_name"]
        content = memory["content"]
        
        if language == Language.ZH:
            # 根据实体类型生成不同的破冰语
            if entity_type == "family":
                return f"之前你提到{entity_name}，{content}，现在情况怎么样了？"
            elif entity_type == "health":
                return f"关于{content}，最近感觉好一些了吗？"
            elif entity_type == "work":
                return f"之前说的{content}，后来进展如何？"
            elif entity_type == "date":
                return f"快到{entity_name}了，{content}，准备得怎么样了？"
            else:
                return f"前两天提到的那件事（{content}），后来怎样了？"
        else:
            # English version
            if entity_type == "family":
                return f"You mentioned {entity_name} before - {content}. How is it going now?"
            elif entity_type == "health":
                return f"About {content} - are you feeling better recently?"
            elif entity_type == "work":
                return f"How did {content} turn out?"
            elif entity_type == "date":
                return f"{entity_name} is coming up - {content}. How are the preparations?"
            else:
                return f"You mentioned something about {content} the other day. How did it go?"
    
    def check_and_trigger(self, user_id: str) -> List[str]:
        """
        检查所有触发条件，返回需要发送的消息列表
        """
        messages = []
        
        # 检查日历事件
        calendar_msg = self.check_calendar_events(user_id)
        if calendar_msg:
            messages.append(calendar_msg)
        
        # 检查沉默唤醒
        silence_msg = self.check_silence_wakeup(user_id)
        if silence_msg:
            messages.append(silence_msg)
        
        return messages
    
    def start_cron_job(self, user_ids: list) -> None:
        """
        启动 Cron Job 线程
        定期检查所有用户的触发条件
        """
        if self._running:
            return
        
        self._running = True
        self._stop_event.clear()
        
        def cron_loop():
            while not self._stop_event.is_set():
                try:
                    # 检查所有用户
                    for user_id in user_ids:
                        messages = self.check_and_trigger(user_id)
                        for msg in messages:
                            if self.message_callback:
                                self.message_callback(user_id, msg)
                    
                    # 等待指定间隔
                    self._stop_event.wait(CRON_CHECK_INTERVAL_SECONDS)
                except Exception as e:
                    print(f"Error in cron job: {e}")
                    time.sleep(60)  # 出错后等待1分钟再继续
        
        self._thread = Thread(target=cron_loop, daemon=True)
        self._thread.start()
        print(f"Proactive trigger cron job started (check interval: {CRON_CHECK_INTERVAL_SECONDS}s)")
    
    def stop_cron_job(self) -> None:
        """停止 Cron Job"""
        self._running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        print("Proactive trigger cron job stopped")
    
    def trigger_immediate_check(self, user_id: str) -> List[str]:
        """
        立即触发检查（用于测试或手动触发）
        """
        return self.check_and_trigger(user_id)
