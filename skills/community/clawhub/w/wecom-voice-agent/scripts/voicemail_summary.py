#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
voicemail_summary.py — 语音留言摘要系统（v1.0）

功能：接收语音留言（voicemail），自动转录 → 生成结构化摘要 → 推送通知
复用能力：call_record_subsystem.MinutesExtractor（纪要提取）+ 关键词分析

依赖：纯 Python 标准库（零外部依赖）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-08-17)
"""

import os
import re
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any

from call_record_subsystem import MinutesExtractor

logger = logging.getLogger(__name__)


# ==========================================
# 配置
# ==========================================

# 摘要输出目录
VOICEMAIL_SUMMARY_DIR = os.path.join(os.path.expanduser("~"), ".wecom_voice", "voicemail")

# 摘要类型标记
VOICEMAIL_TYPE_INQUIRY = "inquiry"       # 咨询类
VOICEMAIL_TYPE_COMPLAINT = "complaint"   # 投诉类
VOICEMAIL_TYPE_ORDER = "order"           # 订单类
VOICEMAIL_TYPE_URGENT = "urgent"         # 紧急类
VOICEMAIL_TYPE_OTHER = "other"           # 其他


# ==========================================
# 语音留言摘要器
# ==========================================

class VoicemailSummarizer:
    """
    语音留言摘要器
    
    处理流程：
    1. 接收原始语音留言（文本/音频路径）
    2. 预处理 → 提取结构化信息
    3. 生成摘要（意图 + 关键信息 + 紧急度）
    4. 输出可读格式
    
    使用方式：
        summarizer = VoicemailSummarizer()
        result = summarizer.process_voicemail("vm_001", "13800138000", "帮我查订单状态")
        print(result["summary"])
    """

    # 紧急关键词
    URGENT_KEYWORDS = [
        "紧急", "马上", "立刻", "立即", "赶快", "急诊",
        "报警", "失火", "漏水", "漏电", "危险", "救命",
        "urgent", "asap", "immediately", "emergency"
    ]

    # 意图分类词典
    INTENT_PATTERNS = {
        VOICEMAIL_TYPE_INQUIRY: [
            "咨询", "问", "查询", "查一下", "了解", "怎么样", "如何",
            "多少钱", "什么时候", "几点", "哪里", "哪个", "能不能"
        ],
        VOICEMAIL_TYPE_COMPLAINT: [
            "投诉", "不满意", "退货", "退款", "差劲", "差评", "骗",
            "假货", "服务态度", "不专业", "态度差", "投诉你们"
        ],
        VOICEMAIL_TYPE_ORDER: [
            "订单", "下单", "买了", "付款", "发货", "物流", "快递",
            "签收", "到哪了", "什么时候到", "催单"
        ],
    }

    def __init__(self):
        self.minutes_extractor = MinutesExtractor()

    def process_voicemail(self, vm_id: str, caller: str,
                          content: str, source: str = "text") -> Dict:
        """
        处理语音留言，生成结构化摘要
        
        Args:
            vm_id: 留言唯一标识
            caller: 来电号码/用户ID
            content: 留言内容（文本或 ASR 转写结果）
            source: 来源类型（text/audio）
            
        Returns:
            dict: 包含 summary / priority / intent / keywords / action_needed
        """
        if not content or not content.strip():
            return self._empty_result(vm_id, caller)

        # 提取结构化信息（复用纪要能力）
        turns = [{"role": "user", "content": content}]
        minutes = self.minutes_extractor.extract(turns, intent="voicemail")

        # 意图分类
        intent = self._classify_intent(content)

        # 紧急度评估
        urgency = self._assess_urgency(content)

        # 生成摘要
        summary = self._generate_summary(content, minutes, intent, urgency)

        # 构建结果
        result = {
            "vm_id": vm_id,
            "caller": caller,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "intent": intent,
            "urgency": urgency,
            "keywords": minutes.keywords,
            "decisions": minutes.decisions,
            "todos": minutes.todos,
            "summary": summary,
            "action_needed": urgency in ("high", "critical") or intent == VOICEMAIL_TYPE_COMPLAINT,
            "sentiment": minutes.sentiment,
            "source": source,
            "raw_content": content[:200],  # 保留原始内容前200字符
        }

        logger.info(f"语音留言摘要生成完成: vm_id={vm_id}, intent={intent}, urgency={urgency}")
        return result

    def process_audio_voicemail(self, vm_id: str, caller: str,
                                audio_path: str, asr_text: str = "") -> Dict:
        """
        处理音频语音留言
        
        Args:
            vm_id: 留言唯一标识
            caller: 来电号码
            audio_path: 音频文件路径
            asr_text: ASR 转写结果（为空时仅返回元数据）
        """
        if not asr_text:
            return {
                "vm_id": vm_id,
                "caller": caller,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "intent": "unknown",
                "urgency": "unknown",
                "keywords": [],
                "summary": f"[音频留言] 来自 {caller}，待转录",
                "action_needed": False,
                "sentiment": "neutral",
                "source": "audio",
                "audio_path": audio_path,
                "raw_content": "",
            }

        result = self.process_voicemail(vm_id, caller, asr_text, source="audio")
        result["audio_path"] = audio_path
        return result

    def batch_process(self, voicemails: List[Dict]) -> List[Dict]:
        """
        批量处理多条语音留言
        
        Args:
            voicemails: 留言列表，每项包含 vm_id, caller, content
            
        Returns:
            list: 摘要结果列表
        """
        results = []
        for vm in voicemails:
            try:
                result = self.process_voicemail(
                    vm_id=vm.get("vm_id", ""),
                    caller=vm.get("caller", ""),
                    content=vm.get("content", ""),
                    source=vm.get("source", "text"),
                )
                results.append(result)
            except Exception as e:
                logger.warning(f"批量处理失败: {e}")
                results.append({
                    "vm_id": vm.get("vm_id", "unknown"),
                    "error": str(e),
                    "summary": f"[处理失败] {e}",
                })
        return results

    def render_summary(self, result: Dict) -> str:
        """
        渲染摘要为可读格式
        """
        lines = [
            "📮 语音留言摘要",
            "=" * 40,
            f"留言ID: {result.get('vm_id', 'N/A')}",
            f"来电: {result.get('caller', 'N/A')}",
            f"时间: {result.get('timestamp', 'N/A')}",
            f"意图: {self._intent_label(result.get('intent', 'other'))}",
            f"紧急度: {self._urgency_label(result.get('urgency', 'low'))}",
            f"情感: {self._sentiment_label(result.get('sentiment', 'neutral'))}",
            "",
        ]

        # 摘要正文
        lines.append("📋 摘要:")
        lines.append(f"  {result.get('summary', '无摘要')}")

        # 关键信息
        keywords = result.get("keywords", [])
        if keywords:
            lines.append(f"\n🔑 关键词: {', '.join(keywords)}")

        todos = result.get("todos", [])
        if todos:
            lines.append("\n📝 待办:")
            for t in todos[:3]:
                lines.append(f"  - {t}")

        # 行动建议
        if result.get("action_needed"):
            lines.append("\n⚠️ 需人工跟进")

        lines.append("=" * 40)
        return "\n".join(lines)

    # === 内部方法 ===

    def _empty_result(self, vm_id: str, caller: str) -> Dict:
        return {
            "vm_id": vm_id,
            "caller": caller,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "intent": "unknown",
            "urgency": "low",
            "keywords": [],
            "summary": "[空留言]",
            "action_needed": False,
            "sentiment": "neutral",
            "raw_content": "",
        }

    def _classify_intent(self, text: str) -> str:
        """基于关键词的意图分类"""
        text_lower = text.lower()
        scores = {}
        for intent, keywords in self.INTENT_PATTERNS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[intent] = score
        if not scores:
            return VOICEMAIL_TYPE_OTHER
        return max(scores, key=scores.get)

    def _assess_urgency(self, text: str) -> str:
        """评估紧急度"""
        text_lower = text.lower()
        urgent_count = sum(1 for kw in self.URGENT_KEYWORDS if kw in text_lower)
        if urgent_count >= 3:
            return "critical"
        elif urgent_count >= 1:
            return "high"
        # 投诉类默认中等紧急
        if self._classify_intent(text) == VOICEMAIL_TYPE_COMPLAINT:
            return "medium"
        return "low"

    def _generate_summary(self, content: str, minutes, intent: str, urgency: str) -> str:
        """生成单句摘要"""
        parts = []
        intent_desc = {
            VOICEMAIL_TYPE_INQUIRY: "咨询",
            VOICEMAIL_TYPE_COMPLAINT: "投诉",
            VOICEMAIL_TYPE_ORDER: "订单相关",
            VOICEMAIL_TYPE_URGENT: "紧急事项",
            VOICEMAIL_TYPE_OTHER: "一般留言",
        }
        parts.append(f"[{intent_desc.get(intent, '留言')}]")
        if minutes.decisions:
            parts.append(f"关键决策: {minutes.decisions[0][:30]}")
        if minutes.keywords:
            parts.append(f"关键词: {', '.join(minutes.keywords[:3])}")
        if urgency in ("high", "critical"):
            parts.append("⚠️需优先处理")
        # 兜底：用原文前50字
        if len(parts) <= 1:
            parts.append(content[:50] + ("..." if len(content) > 50 else ""))
        return " | ".join(parts)

    def _intent_label(self, intent: str) -> str:
        labels = {
            VOICEMAIL_TYPE_INQUIRY: "咨询",
            VOICEMAIL_TYPE_COMPLAINT: "投诉",
            VOICEMAIL_TYPE_ORDER: "订单",
            VOICEMAIL_TYPE_URGENT: "紧急",
            VOICEMAIL_TYPE_OTHER: "其他",
        }
        return labels.get(intent, intent)

    def _urgency_label(self, urgency: str) -> str:
        labels = {
            "critical": "🔴 极紧急",
            "high": "🟠 紧急",
            "medium": "🟡 中等",
            "low": "🟢 一般",
        }
        return labels.get(urgency, urgency)

    def _sentiment_label(self, sentiment: str) -> str:
        labels = {
            "positive": "😊 积极",
            "neutral": "😐 中性",
            "negative": "😟 消极",
        }
        return labels.get(sentiment, sentiment)


# ==========================================
# 便捷函数
# ==========================================

def summarize_voicemail(vm_id: str, caller: str, content: str) -> Dict:
    """便捷函数：生成语音留言摘要"""
    summarizer = VoicemailSummarizer()
    return summarizer.process_voicemail(vm_id, caller, content)


def batch_summarize(voicemails: List[Dict]) -> List[Dict]:
    """便捷函数：批量处理语音留言"""
    summarizer = VoicemailSummarizer()
    return summarizer.batch_process(voicemails)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行语音留言摘要自测"""
    print("=" * 60)
    print("语音留言摘要系统 — 自测模式")
    print("=" * 60)

    summarizer = VoicemailSummarizer()

    # 测试 1: 咨询类留言
    print("\n[测试 1] 咨询类留言")
    result = summarizer.process_voicemail(
        "vm_test_001", "13800138000",
        "你好，我想咨询一下你们的产品价格，最新款多少钱？"
    )
    assert result["intent"] == VOICEMAIL_TYPE_INQUIRY
    assert result["action_needed"] is False
    print(f"  意图: {result['intent']}, 紧急度: {result['urgency']}")
    print("✅ 咨询类留言通过")

    # 测试 2: 投诉类留言
    print("\n[测试 2] 投诉类留言")
    result = summarizer.process_voicemail(
        "vm_test_002", "13900139000",
        "你们的服务太差了！我要投诉，产品质量有问题，要求退货退款！"
    )
    assert result["intent"] == VOICEMAIL_TYPE_COMPLAINT
    assert result["urgency"] == "medium"
    print(f"  意图: {result['intent']}, 紧急度: {result['urgency']}")
    print("✅ 投诉类留言通过")

    # 测试 3: 紧急留言
    print("\n[测试 3] 紧急留言")
    result = summarizer.process_voicemail(
        "vm_test_003", "13700137000",
        "紧急求助！马上要开会了，投影仪坏了，立刻派人来修！"
    )
    assert result["urgency"] in ("high", "critical")
    assert result["action_needed"] is True
    print(f"  意图: {result['intent']}, 紧急度: {result['urgency']}")
    print("✅ 紧急留言通过")

    # 测试 4: 空留言
    print("\n[测试 4] 空留言处理")
    result = summarizer.process_voicemail("vm_test_004", "13600136000", "")
    assert result["summary"] == "[空留言]"
    print("✅ 空留言处理通过")

    # 测试 5: 音频留言（有 ASR）
    print("\n[测试 5] 音频留言（有 ASR）")
    result = summarizer.process_audio_voicemail(
        "vm_test_005", "13500135000",
        "/tmp/test_audio.wav", "订单什么时候发货？"
    )
    assert result["intent"] == VOICEMAIL_TYPE_ORDER
    assert result["audio_path"] == "/tmp/test_audio.wav"
    print(f"  意图: {result['intent']}, 路径: {result['audio_path']}")
    print("✅ 音频留言通过")

    # 测试 6: 音频留言（无 ASR）
    print("\n[测试 6] 音频留言（无 ASR）")
    result = summarizer.process_audio_voicemail(
        "vm_test_006", "13400134000", "/tmp/test_audio2.wav"
    )
    assert "待转录" in result["summary"]
    print("✅ 无 ASR 音频留言通过")

    # 测试 7: 批量处理
    print("\n[测试 7] 批量处理")
    voicemails = [
        {"vm_id": "vm_batch_001", "caller": "13300133000", "content": "查订单"},
        {"vm_id": "vm_batch_002", "caller": "13200132000", "content": "投诉服务态度"},
        {"vm_id": "vm_batch_003", "caller": "13100131000", "content": ""},
    ]
    results = summarizer.batch_process(voicemails)
    assert len(results) == 3
    assert results[0]["intent"] == VOICEMAIL_TYPE_ORDER
    assert results[1]["intent"] == VOICEMAIL_TYPE_COMPLAINT
    print(f"  批量处理 {len(results)} 条完成")
    print("✅ 批量处理通过")

    # 测试 8: 渲染摘要
    print("\n[测试 8] 渲染摘要输出")
    result = summarizer.process_voicemail(
        "vm_test_008", "13000130000",
        "我买的手机屏幕碎了，才买一周，要求换货，否则投诉到底！"
    )
    rendered = summarizer.render_summary(result)
    assert "📮 语音留言摘要" in rendered
    assert "需人工跟进" in rendered
    print(rendered)
    print("✅ 渲染摘要输出通过")

    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_self_test()
