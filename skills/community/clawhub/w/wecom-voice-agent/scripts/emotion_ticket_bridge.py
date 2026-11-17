#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emotion_ticket_bridge.py — 情感到工单直连桥接（v2.7）

功能：
1. 监听 emotion_analyzer（v2.2）的 5 类情感识别结果
2. 强负面（愤怒 score ≥ 0.75 或 连续 2 轮焦虑 score ≥ 0.70）时
   直连 ticket_manager（v2.3）自动建单 + 优先级提升 + 主管通知
3. 无需独立触发，属既有能力的链路打通

依赖：纯 Python 标准库（import emotion_analyzer + ticket_manager）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-09-02)
"""

import os
import json
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

# ==========================================
# 配置
# ==========================================

# 强负面阈值
ANGRY_THRESHOLD = 0.75
ANXIOUS_THRESHOLD = 0.70
# 连续焦虑轮次触发
CONSECUTIVE_ANXIOUS_ROUNDS = 2
# 主管通知 webhook（可选）
SUPERVISOR_WEBHOOK = os.environ.get("SUPERVISOR_WEBHOOK", "")
# 通知方式：webhook / wecom / log
NOTIFY_METHOD = os.environ.get("NOTIFY_METHOD", "log")


# ==========================================
# 情感到工单桥接器
# ==========================================

class EmotionTicketBridge:
    """
    情感到工单直连桥接器

    使用方式：
        bridge = EmotionTicketBridge()
        
        # 分析情感并自动触发工单
        result = bridge.process_emotion("用户文本", session_id="call_001", userid="user_123")
        # result: {"triggered": True, "ticket_id": "TK...", "emotion": "angry", ...}
    """

    def __init__(self, angry_threshold: float = ANGRY_THRESHOLD,
                 anxious_threshold: float = ANXIOUS_THRESHOLD,
                 consecutive_anxious_rounds: int = CONSECUTIVE_ANXIOUS_ROUNDS):
        self.angry_threshold = angry_threshold
        self.anxious_threshold = anxious_threshold
        self.consecutive_anxious_rounds = consecutive_anxious_rounds
        self._session_history: Dict[str, List[Dict]] = {}  # session_id → 情感历史

    def process_emotion(self, text: str, session_id: str = "", userid: str = "",
                        call_id: str = "") -> Dict[str, Any]:
        """
        分析情感并自动触发工单（如满足条件）

        Args:
            text: 用户文本
            session_id: 会话 ID
            userid: 用户 ID
            call_id: 通话 ID

        Returns:
            dict: {
                "triggered": bool,
                "emotion": str,
                "confidence": float,
                "ticket_id": str or None,
                "priority_boosted": bool,
                "supervisor_notified": bool,
                "action_taken": str
            }
        """
        # 延迟导入避免循环依赖
        try:
            from emotion_analyzer import EmotionAnalyzer, Emotion
            self._Emotion = Emotion
        except ImportError:
            logger.warning("emotion_analyzer 未找到，跳过情感分析")
            return {"triggered": False, "emotion": "unknown", "action_taken": "analyzer_unavailable"}

        # 情感分析
        analyzer = EmotionAnalyzer()
        result = analyzer.analyze(text)
        emotion = result.get("emotion")
        confidence = result.get("confidence", 0.0)
        scores = result.get("scores", {})

        # 判断是否强负面（在记录当前轮之前判断，这样当前轮不计入历史）
        is_strong_negative = self._is_strong_negative(emotion, confidence, scores, session_id)

        # 记录历史（当前轮计入历史，供下次判断使用）
        if session_id:
            self._record_emotion(session_id, emotion, confidence, scores)

        if not is_strong_negative:
            return {
                "triggered": False,
                "emotion": emotion.value if hasattr(emotion, 'value') else str(emotion),
                "confidence": confidence,
                "ticket_id": None,
                "priority_boosted": False,
                "supervisor_notified": False,
                "action_taken": "no_action",
            }

        # 触发直连：建单 + 升级 + 通知
        ticket = self._create_ticket(text, emotion, confidence, session_id, userid, call_id)
        priority_boosted = self._boost_priority(ticket)
        supervisor_notified = self._notify_supervisor(ticket, emotion, confidence, userid)

        return {
            "triggered": True,
            "emotion": emotion.value if hasattr(emotion, 'value') else str(emotion),
            "confidence": confidence,
            "ticket_id": ticket.get("id") if ticket else None,
            "priority_boosted": priority_boosted,
            "supervisor_notified": supervisor_notified,
            "action_taken": "ticket_created_and_escalated",
        }

    def _is_strong_negative(self, emotion, confidence: float, scores: Dict, session_id: str) -> bool:
        """
        判断是否为强负面情感

        条件：
        1. 愤怒 score ≥ 0.75
        2. 连续 2 轮焦虑 score ≥ 0.70
        """
        try:
            from emotion_analyzer import Emotion
        except ImportError:
            return False

        # 条件 1：愤怒
        if emotion == Emotion.ANGRY and confidence >= self.angry_threshold:
            return True

        # 条件 2：连续焦虑（含当前轮）
        if emotion == Emotion.ANXIOUS and confidence >= self.anxious_threshold:
            history = self._session_history.get(session_id, [])
            # 统计历史中连续焦虑轮次
            consecutive = 0
            for record in reversed(history):
                if record.get("emotion") == Emotion.ANXIOUS and record.get("confidence", 0) >= self.anxious_threshold:
                    consecutive += 1
                else:
                    break
            # 含当前轮：consecutive(历史) + 1(当前) >= rounds
            if consecutive + 1 >= self.consecutive_anxious_rounds:
                return True

        return False

    def _record_emotion(self, session_id: str, emotion, confidence: float, scores: Dict):
        """记录情感历史"""
        if session_id not in self._session_history:
            self._session_history[session_id] = []

        self._session_history[session_id].append({
            "emotion": emotion,
            "confidence": confidence,
            "scores": scores,
            "timestamp": datetime.now().isoformat(),
        })

        # 只保留最近 10 轮
        if len(self._session_history[session_id]) > 10:
            self._session_history[session_id] = self._session_history[session_id][-10:]

    def _create_ticket(self, text: str, emotion, confidence: float,
                       session_id: str, userid: str, call_id: str) -> Optional[Dict]:
        """创建工单"""
        try:
            from ticket_manager import TicketManager
        except ImportError:
            logger.warning("ticket_manager 未找到，无法创建工单")
            return None

        manager = TicketManager()
        emotion_tag = emotion.value if hasattr(emotion, 'value') else str(emotion)

        ticket = manager.auto_create_ticket(
            text=text,
            created_by="emotion_bridge",
            session_id=session_id or call_id,
            emotion_tag=emotion_tag,
            source="emotion_auto",
        )

        logger.info(f"情感直连建单: {ticket.get('id')}, 情感: {emotion_tag}, 用户: {userid}")
        return ticket

    def _boost_priority(self, ticket: Optional[Dict]) -> bool:
        """提升工单优先级"""
        if not ticket:
            return False

        ticket_id = ticket.get("id")
        if not ticket_id:
            return False

        try:
            from ticket_manager import TicketManager
            manager = TicketManager()
        except ImportError:
            return False

        # 直接更新优先级字段
        try:
            with sqlite3.connect(manager.db_path) as conn:
                conn.execute("""
                    UPDATE tickets SET priority = 'high', updated_at = ?
                    WHERE id = ? AND priority != 'high'
                """, (datetime.now().isoformat(), ticket_id))
                conn.commit()
            logger.info(f"工单 {ticket_id} 优先级提升为 HIGH")
            return True
        except Exception as e:
            logger.warning(f"优先级提升失败: {e}")
            return False

    def _notify_supervisor(self, ticket: Optional[Dict], emotion, confidence: float, userid: str) -> bool:
        """通知主管"""
        if not ticket:
            return False

        message = self._build_notification_message(ticket, emotion, confidence, userid)

        if NOTIFY_METHOD == "webhook" and SUPERVISOR_WEBHOOK:
            return self._send_webhook(message)
        elif NOTIFY_METHOD == "wecom":
            return self._send_wecom(message)
        else:
            # 默认：记录日志
            logger.warning(f"[主管通知] {message}")
            return True

    def _build_notification_message(self, ticket: Dict, emotion, confidence: float, userid: str) -> str:
        """构建通知消息"""
        emotion_text = emotion.value if hasattr(emotion, 'value') else str(emotion)
        return (
            f"⚠️ 强负面情感工单告警\n"
            f"工单号: {ticket.get('id', '未知')}\n"
            f"用户: {userid}\n"
            f"情感: {emotion_text} (置信度: {confidence:.2f})\n"
            f"标题: {ticket.get('title', '未知')}\n"
            f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"请尽快处理！"
        )

    def _send_webhook(self, message: str) -> bool:
        """发送 webhook 通知"""
        try:
            from urllib.request import Request, urlopen
            import ssl

            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            payload = json.dumps({"text": message}).encode("utf-8")
            req = Request(SUPERVISOR_WEBHOOK, data=payload, headers={"Content-Type": "application/json"})
            resp = urlopen(req, timeout=5, context=ctx)
            return resp.status == 200
        except Exception as e:
            logger.warning(f"webhook 通知失败: {e}")
            return False

    def _send_wecom(self, message: str) -> bool:
        """发送企业微信通知"""
        # 企微通知需要配置 webhook，此处为占位
        logger.info(f"[企微通知] {message}")
        return True

    def reset_session(self, session_id: str):
        """重置会话历史"""
        if session_id in self._session_history:
            del self._session_history[session_id]


# ==========================================
# 便捷函数
# ==========================================

_bridge_instance: Optional[EmotionTicketBridge] = None


def get_bridge() -> EmotionTicketBridge:
    """获取单例"""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = EmotionTicketBridge()
    return _bridge_instance


def process_emotion(text: str, session_id: str = "", userid: str = "",
                    call_id: str = "") -> Dict[str, Any]:
    """便捷函数：分析情感并自动触发"""
    return get_bridge().process_emotion(text, session_id, userid, call_id)


def is_strong_negative(text: str, session_id: str = "") -> bool:
    """便捷函数：判断是否为强负面（不触发建单）"""
    bridge = get_bridge()
    try:
        from emotion_analyzer import EmotionAnalyzer, Emotion
        analyzer = EmotionAnalyzer()
        result = analyzer.analyze(text)
        emotion = result.get("emotion")
        confidence = result.get("confidence", 0.0)
        scores = result.get("scores", {})
        return bridge._is_strong_negative(emotion, confidence, scores, session_id)
    except ImportError:
        return False


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行情感到工单桥接自测"""
    print("=" * 60)
    print("emotion_ticket_bridge.py — 自测模式")
    print("=" * 60)

    bridge = EmotionTicketBridge()

    # 测试 1: 愤怒情感触发
    print("\n[测试 1] 愤怒情感触发")
    result = bridge.process_emotion(
        "你们这是什么破服务！太差了！我要投诉！",
        session_id="test_call_001",
        userid="user_123",
    )
    print(f"  触发: {result['triggered']}")
    print(f"  情感: {result['emotion']}")
    print(f"  工单: {result['ticket_id']}")
    print(f"  优先级提升: {result['priority_boosted']}")
    print(f"  主管通知: {result['supervisor_notified']}")
    assert result["triggered"] is True
    assert result["emotion"] == "angry"
    assert result["ticket_id"] is not None
    assert result["priority_boosted"] is True
    print("✅ 愤怒触发通过")

    # 测试 2: 连续焦虑触发
    print("\n[测试 2] 连续焦虑触发")
    bridge2 = EmotionTicketBridge()
    # 第一轮焦虑
    r1 = bridge2.process_emotion(
        "我很着急，赶紧帮我处理一下",
        session_id="test_call_002",
        userid="user_456",
    )
    print(f"  第一轮焦虑 触发: {r1['triggered']}")
    assert r1["triggered"] is False  # 第一轮不触发

    # 第二轮焦虑
    r2 = bridge2.process_emotion(
        "怎么还没处理？我真的很急！快点！",
        session_id="test_call_002",
        userid="user_456",
    )
    print(f"  第二轮焦虑 触发: {r2['triggered']}")
    print(f"  情感: {r2['emotion']}")
    assert r2["triggered"] is True
    assert r2["emotion"] == "anxious"
    print("✅ 连续焦虑触发通过")

    # 测试 3: 中性情感不触发
    print("\n[测试 3] 中性情感不触发")
    result3 = bridge.process_emotion(
        "好的，谢谢，我知道了",
        session_id="test_call_003",
        userid="user_789",
    )
    print(f"  触发: {result3['triggered']}")
    assert result3["triggered"] is False
    print("✅ 中性不触发通过")

    # 测试 4: 满意情感不触发
    print("\n[测试 4] 满意情感不触发")
    result4 = bridge.process_emotion(
        "太棒了，服务很好，谢谢！",
        session_id="test_call_004",
        userid="user_abc",
    )
    print(f"  触发: {result4['triggered']}")
    assert result4["triggered"] is False
    print("✅ 满意不触发通过")

    # 测试 5: 便捷函数
    print("\n[测试 5] 便捷函数")
    result5 = process_emotion("垃圾服务！骗人的！", session_id="test_call_005")
    print(f"  便捷函数触发: {result5['triggered']}")
    assert result5["triggered"] is True
    print("✅ 便捷函数通过")

    # 测试 6: is_strong_negative 不触发建单
    print("\n[测试 6] is_strong_negative 判断")
    is_neg = is_strong_negative("太差了！投诉！")
    print(f"  强负面: {is_neg}")
    assert is_neg is True
    is_neg2 = is_strong_negative("好的谢谢")
    print(f"  非强负面: {is_neg2}")
    assert is_neg2 is False
    print("✅ 判断函数通过")

    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_self_test()
