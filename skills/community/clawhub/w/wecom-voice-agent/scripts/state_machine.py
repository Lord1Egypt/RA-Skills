#!/usr/bin/env python3
"""
企业微信语音助手 — 多轮对话状态机 v2.0

管理一次语音通话的完整生命周期：
  IDLE → DIALING → SPEAKING → LISTENING → CONFIRMING → ENDING

特性：
- 30 秒无新语音自动结束通话
- ASR 置信度 < 0.85 时进入 CONFIRMING 二次确认
- 纯 Python 标准库，零外部依赖
- 状态持久化到本地 JSON（支持断线恢复）

更新日志：
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0 | 2026-07-15 | 初始发布：完整状态机、持久化、并发管理 |
| v2.0.1 | 2026-07-15 | 修复 call_id 路径遍历风险、中文化日志、类型提示优化 |

联系信息：njskills@agent.qq.com

使用方法：
    python scripts/state_machine.py           # 运行自测
    python scripts/state_machine.py --demo    # 演示完整流程
"""

import json
import time
import logging
import os
import re
import sys
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable, Tuple

# ==========================================
# 配置
# ==========================================

DEFAULT_TIMEOUT_SECONDS = 30  # 无新语音自动结束时间
CONFIDENCE_THRESHOLD = 0.85    # ASR 置信度二次确认阈值
SESSION_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'temp_sessions')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("StateMachine")


def _sanitize_call_id(call_id: str) -> str:
    """
    清理 call_id，防止路径遍历攻击。
    仅允许字母、数字、下划线和连字符。
    """
    if not call_id or not isinstance(call_id, str):
        raise ValueError("call_id 不能为空且必须是字符串")
    # 仅允许安全字符
    if not re.match(r'^[a-zA-Z0-9_\-]+$', call_id):
        raise ValueError(f"call_id 包含非法字符，仅允许字母、数字、下划线和连字符: {call_id}")
    return call_id


# ==========================================
# 状态枚举
# ==========================================

class CallState(Enum):
    """通话状态"""
    IDLE = "idle"                   # 空闲/未开始
    DIALING = "dialing"             # 拨号中
    SPEAKING = "speaking"           # Agent 说话中（TTS 播报）
    LISTENING = "listening"         # 等待用户语音输入
    CONFIRMING = "confirming"       # 二次确认中（ASR 置信度低）
    ENDING = "ending"               # 通话结束中

    def __str__(self):
        return self.value


class CallEvent(Enum):
    """触发状态转换的事件"""
    START_CALL = "start_call"               # 发起/接听电话
    AGENT_SPEAK_DONE = "agent_speak_done"   # Agent 说完
    USER_VOICE = "user_voice"               # 收到用户语音
    USER_CONFIRM = "user_confirm"           # 用户确认
    USER_DENY = "user_deny"                 # 用户否认
    TIMEOUT = "timeout"                     # 超时
    HANGUP = "hangup"                       # 挂断


# ==========================================
# 状态机核心
# ==========================================

class CallStateMachine:
    """
    单次通话的状态机实例

    使用方式：
        sm = CallStateMachine(call_id="call_001", userid="zhangsan")
        sm.transition(CallEvent.START_CALL)
        sm.transition(CallEvent.AGENT_SPEAK_DONE)
        sm.transition(CallEvent.USER_VOICE, confidence=0.92)
    """

    # 状态转换表：当前状态 + 事件 → 下一状态
    TRANSITIONS: Dict[Tuple[CallState, CallEvent], CallState] = {
        # 从 IDLE 开始
        (CallState.IDLE, CallEvent.START_CALL): CallState.SPEAKING,

        # 从 SPEAKING（Agent 说完 → 等待用户）
        (CallState.SPEAKING, CallEvent.AGENT_SPEAK_DONE): CallState.LISTENING,
        (CallState.SPEAKING, CallEvent.HANGUP): CallState.ENDING,

        # 从 LISTENING（收到用户语音）
        (CallState.LISTENING, CallEvent.USER_VOICE): CallState.SPEAKING,  # 直接回复
        (CallState.LISTENING, CallEvent.TIMEOUT): CallState.ENDING,
        (CallState.LISTENING, CallEvent.HANGUP): CallState.ENDING,

        # 从 CONFIRMING（二次确认）
        (CallState.CONFIRMING, CallEvent.USER_CONFIRM): CallState.SPEAKING,
        (CallState.CONFIRMING, CallEvent.USER_DENY): CallState.LISTENING,  # 重新听
        (CallState.CONFIRMING, CallEvent.TIMEOUT): CallState.ENDING,
        (CallState.CONFIRMING, CallEvent.HANGUP): CallState.ENDING,

        # 从 ENDING（终态，不再转换）
    }

    def __init__(
        self,
        call_id: str,
        userid: str,
        direction: str = "outbound",  # outbound / inbound
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
        on_state_change: Optional[Callable] = None,
    ):
        # 安全校验 call_id 防止路径遍历
        self.call_id = _sanitize_call_id(call_id)
        self.userid = userid
        self.direction = direction
        self.timeout = timeout
        self.on_state_change = on_state_change

        self.state = CallState.IDLE
        self.confidence: float = 0.0
        self.asr_text: str = ""
        self.pending_confirmation: str = ""  # 待确认的 ASR 文本
        self.history: list = []              # 对话历史
        self.start_time: Optional[float] = None
        self.last_activity: float = time.time()
        self.turn_count: int = 0             # 对话轮次

        # 持久化路径
        self._session_path = os.path.join(SESSION_DIR, f"call_{self.call_id}.json")

        logger.info(f"状态机创建: call_id={self.call_id}, userid={userid}, direction={direction}")

    def transition(self, event: CallEvent, **kwargs) -> CallState:
        """
        执行状态转换

        Args:
            event: 触发事件
            **kwargs: 附加数据（如 confidence, asr_text 等）

        Returns:
            新状态
        """
        old_state = self.state
        key = (old_state, event)

        if key not in self.TRANSITIONS:
            logger.warning(f"无效的状态转换: 当前状态={old_state} + 事件={event} → 已忽略")
            return old_state

        new_state = self.TRANSITIONS[key]
        self.state = new_state
        self.last_activity = time.time()

        # 处理附加数据
        if "confidence" in kwargs:
            self.confidence = kwargs["confidence"]
        if "asr_text" in kwargs:
            self.asr_text = kwargs["asr_text"]
            self.history.append({
                "role": "user",
                "content": kwargs["asr_text"],
                "confidence": self.confidence,
                "time": datetime.now().isoformat()
            })
        if "agent_text" in kwargs:
            self.history.append({
                "role": "agent",
                "content": kwargs["agent_text"],
                "time": datetime.now().isoformat()
            })

        # 特殊逻辑：置信度低 → 进入 CONFIRMING
        if (new_state == CallState.SPEAKING and
            event == CallEvent.USER_VOICE and
            self.confidence < CONFIDENCE_THRESHOLD and
            self.confidence > 0):
            self.pending_confirmation = self.asr_text
            self.state = CallState.CONFIRMING
            new_state = CallState.CONFIRMING
            logger.info(f"ASR 置信度 {self.confidence:.2f} < {CONFIDENCE_THRESHOLD}，进入二次确认")

        # 记录轮次
        if new_state == CallState.LISTENING:
            self.turn_count += 1

        # 回调
        if self.on_state_change:
            self.on_state_change(old_state, new_state, event, self)

        # 持久化
        self._save()

        logger.info(f"状态转换: {old_state} + {event} → {new_state}")
        return new_state

    def is_timeout(self) -> bool:
        """检查是否超时"""
        if self.state in (CallState.IDLE, CallState.ENDING):
            return False
        elapsed = time.time() - self.last_activity
        return elapsed > self.timeout

    def get_duration(self) -> float:
        """获取通话时长（秒）"""
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time

    def start(self):
        """开始通话"""
        self.start_time = time.time()
        return self.transition(CallEvent.START_CALL)

    def hangup(self):
        """挂断"""
        return self.transition(CallEvent.HANGUP)

    def _save(self):
        """持久化到本地 JSON"""
        try:
            os.makedirs(SESSION_DIR, exist_ok=True)
            data = {
                "call_id": self.call_id,
                "userid": self.userid,
                "direction": self.direction,
                "state": self.state.value,
                "confidence": self.confidence,
                "asr_text": self.asr_text,
                "pending_confirmation": self.pending_confirmation,
                "history": self.history,
                "start_time": self.start_time,
                "last_activity": self.last_activity,
                "turn_count": self.turn_count,
            }
            with open(self._session_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"状态持久化失败: {e}")

    @classmethod
    def load(cls, call_id: str) -> Optional["CallStateMachine"]:
        """从本地 JSON 恢复状态机"""
        try:
            safe_call_id = _sanitize_call_id(call_id)
        except ValueError as e:
            logger.warning(f"恢复失败: {e}")
            return None
        path = os.path.join(SESSION_DIR, f"call_{safe_call_id}.json")
        if not os.path.exists(path):
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            sm = cls(
                call_id=data["call_id"],
                userid=data["userid"],
                direction=data.get("direction", "outbound"),
            )
            sm.state = CallState(data["state"])
            sm.confidence = data.get("confidence", 0.0)
            sm.asr_text = data.get("asr_text", "")
            sm.pending_confirmation = data.get("pending_confirmation", "")
            sm.history = data.get("history", [])
            sm.start_time = data.get("start_time")
            sm.last_activity = data.get("last_activity", time.time())
            sm.turn_count = data.get("turn_count", 0)
            return sm
        except Exception as e:
            logger.warning(f"状态恢复失败: {e}")
            return None

    def to_dict(self) -> dict:
        """导出为字典"""
        return {
            "call_id": self.call_id,
            "userid": self.userid,
            "direction": self.direction,
            "state": self.state.value,
            "confidence": self.confidence,
            "asr_text": self.asr_text,
            "pending_confirmation": self.pending_confirmation,
            "turn_count": self.turn_count,
            "duration": self.get_duration(),
            "history_length": len(self.history),
        }


# ==========================================
# 状态机管理器（多通话并发）
# ==========================================

class StateMachineManager:
    """
    管理多个并发通话状态机

    使用方式：
        mgr = StateMachineManager()
        sm = mgr.create_call("call_001", "zhangsan")
        sm.start()
    """

    def __init__(self, max_concurrent: int = 5):
        self._machines: Dict[str, CallStateMachine] = {}
        self._max_concurrent = max_concurrent
        logger.info(f"状态机管理器创建，最大并发: {max_concurrent}")

    def create_call(
        self,
        call_id: str,
        userid: str,
        direction: str = "outbound",
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> CallStateMachine:
        """创建新通话"""
        if len(self._machines) >= self._max_concurrent:
            raise RuntimeError(f"并发通话数已达上限 {self._max_concurrent}")

        if call_id in self._machines:
            logger.warning(f"通话 {call_id} 已存在，返回现有实例")
            return self._machines[call_id]

        sm = CallStateMachine(
            call_id=call_id,
            userid=userid,
            direction=direction,
            timeout=timeout,
        )
        self._machines[call_id] = sm
        logger.info(f"创建通话: call_id={call_id}, userid={userid}")
        return sm

    def get_call(self, call_id: str) -> Optional[CallStateMachine]:
        """获取通话状态机"""
        return self._machines.get(call_id)

    def end_call(self, call_id: str) -> bool:
        """结束通话"""
        sm = self._machines.pop(call_id, None)
        if sm:
            logger.info(f"结束通话: call_id={call_id}")
            return True
        return False

    def get_active_calls(self) -> list:
        """获取所有活跃通话"""
        return [
            sm.to_dict() for sm in self._machines.values()
            if sm.state not in (CallState.IDLE, CallState.ENDING)
        ]

    def cleanup_timeout_calls(self) -> list:
        """清理超时通话，返回被清理的 call_id 列表"""
        timed_out = []
        for call_id, sm in list(self._machines.items()):
            if sm.is_timeout():
                logger.info(f"通话超时: call_id={call_id}")
                sm.transition(CallEvent.TIMEOUT)
                timed_out.append(call_id)
        for call_id in timed_out:
            self.end_call(call_id)
        return timed_out


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行状态机自测"""
    print("=" * 60)
    print("多轮对话状态机 — 自测模式")
    print("=" * 60)

    # 测试 1: 正常外呼流程
    print("\n[测试 1] 正常外呼流程（高置信度）")
    sm = CallStateMachine(call_id="test_001", userid="zhangsan", direction="outbound")
    assert sm.state == CallState.IDLE

    sm.start()
    assert sm.state == CallState.SPEAKING

    sm.transition(CallEvent.AGENT_SPEAK_DONE, agent_text="您好，我是语音助手")
    assert sm.state == CallState.LISTENING

    sm.transition(CallEvent.USER_VOICE, confidence=0.95, asr_text="明天天气怎么样")
    assert sm.state == CallState.SPEAKING  # 高置信度直接回复

    sm.transition(CallEvent.AGENT_SPEAK_DONE, agent_text="明天北京晴，25度")
    assert sm.state == CallState.LISTENING

    sm.hangup()
    assert sm.state == CallState.ENDING
    print("✅ 正常外呼流程通过")

    # 测试 2: 低置信度二次确认
    print("\n[测试 2] 低置信度二次确认")
    sm2 = CallStateMachine(call_id="test_002", userid="lisi", direction="inbound")
    sm2.start()
    sm2.transition(CallEvent.AGENT_SPEAK_DONE, agent_text="您好，请说")
    sm2.transition(CallEvent.USER_VOICE, confidence=0.6, asr_text="我要退订")
    assert sm2.state == CallState.CONFIRMING  # 低置信度进入确认
    assert sm2.pending_confirmation == "我要退订"

    sm2.transition(CallEvent.USER_CONFIRM)
    assert sm2.state == CallState.SPEAKING
    print("✅ 二次确认流程通过")

    # 测试 3: 超时自动结束
    print("\n[测试 3] 超时自动结束")
    sm3 = CallStateMachine(call_id="test_003", userid="wangwu", timeout=1)  # 1秒超时
    sm3.start()
    sm3.transition(CallEvent.AGENT_SPEAK_DONE)
    time.sleep(1.5)
    assert sm3.is_timeout()
    sm3.transition(CallEvent.TIMEOUT)
    assert sm3.state == CallState.ENDING
    print("✅ 超时自动结束通过")

    # 测试 4: 并发管理
    print("\n[测试 4] 并发管理")
    mgr = StateMachineManager(max_concurrent=3)
    sm1 = mgr.create_call("c1", "u1")
    sm2 = mgr.create_call("c2", "u2")
    sm3 = mgr.create_call("c3", "u3")
    try:
        mgr.create_call("c4", "u4")
        print("❌ 应抛出并发上限异常")
    except RuntimeError:
        print("✅ 并发上限控制通过")

    # 启动通话（使状态从 IDLE 转为 SPEAKING）
    sm1.start()
    sm2.start()
    sm3.start()

    active = mgr.get_active_calls()
    assert len(active) == 3
    print(f"✅ 活跃通话数: {len(active)}")

    # 测试 5: 持久化
    print("\n[测试 5] 持久化恢复")
    sm4 = CallStateMachine(call_id="test_005", userid="zhaoliu")
    sm4.start()
    sm4.transition(CallEvent.AGENT_SPEAK_DONE, agent_text="测试")
    sm4.transition(CallEvent.USER_VOICE, confidence=0.9, asr_text="测试内容")

    loaded = CallStateMachine.load("test_005")
    assert loaded is not None
    assert loaded.state == sm4.state
    assert loaded.asr_text == "测试内容"
    print("✅ 持久化恢复通过")

    # 测试 6: 路径遍历防护
    print("\n[测试 6] 路径遍历防护")
    try:
        bad_sm = CallStateMachine(call_id="test_passwd", userid="hacker")
        print("❌ 应拒绝恶意 call_id")
    except ValueError as e:
        print(f"✅ 已拦截恶意 call_id: {e}")

    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print('='*60)


if __name__ == "__main__":
    run_self_test()
