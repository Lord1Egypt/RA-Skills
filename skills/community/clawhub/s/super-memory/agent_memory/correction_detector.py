from __future__ import annotations
"""
correction_detector.py - 智能修正检测器
检测记忆中的修正/撤回/更正信息，并自动关联到原始记忆
"""

import re
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class CorrectionDetector:
    """
    智能修正检测器

    结合两种策略检测修正信息：
    1. 信号词检测：明确标记为修正的词语
    2. embedding相似度：高相似度暗示可能是对前文的修正

    修正类型：
    - 完全撤回：整段内容被撤回
    - 部分修正：只修正某个具体点
    - 澄清说明：解释之前的说法
    - 玩笑/虚构：标记为虚构内容
    """

    # 修正信号词（按类型分类）
    CORRECTION_SIGNALS = {
        # 完全撤回
        "full_retract": [
            "上面是我编的",
            "上面是假的",
            "我瞎说的",
            "我瞎编的",
            "不是真的",
            "我乱说的",
            "开个玩笑",
            "我说着玩的",
            "不算数",
            "当我没说",
            "收回刚才说的",
            "上面的话不算",
            "上面是胡说的",
            "纯属虚构",
            "如有雷同纯属巧合",
            "上面不是真的",
        ],
        # 部分修正
        "partial_correct": [
            "不对",
            "不对，应该是",
            "错了",
            "纠正一下",
            "更正",
            "修正一下",
            "其实不是这样",
            "准确地说",
            "严格来说",
            "更正一下",
            "应该是",
            "准确来说",
            "应该是这样",
        ],
        # 澄清说明
        "clarify": [
            "补充一下",
            "补充说明",
            "解释一下",
            "补充",
            "另外",
            "补充信息",
            "补充一下",
        ],
        # 虚构标记
        "fiction": [
            "我编的",
            "编的",
            "虚构的",
            "故事",
            "我瞎编的",
            "编造的故事",
            "不是真实情况",
        ],
    }

    # 情绪检测词（辅助判断）
    EMOTIONAL_CORRECTION = [
        "哈哈",
        "呵呵",
        "笑死",
        "开玩笑",
        "逗你玩",
        "骗你的",
        "故意的",
    ]

    def __init__(self, embedding_store=None):
        """
        初始化修正检测器

        Args:
            embedding_store: 向量存储（用于相似度计算）
        """
        self.embedding_store = embedding_store
        self._flatten_signals()

    def _flatten_signals(self):
        """将分类的信号词展平为列表"""
        self._all_signals = []
        self._signal_map = {}
        for category, signals in self.CORRECTION_SIGNALS.items():
            for signal in signals:
                self._all_signals.append(signal)
                self._signal_map[signal] = category

    def detect_correction_signal(self, text: str) -> Optional[Dict]:
        """
        检测文本中是否包含修正信号词

        Args:
            text: 待检测文本

        Returns:
            包含信号词信息字典，如：
            {
                "has_signal": True,
                "signal": "上面是我编的",
                "category": "full_retract",
                "confidence": 0.9,
                "position": 5  # 信号词在文本中的位置
            }
        """
        text_lower = text.lower()

        # 优先匹配长信号词（更精确）
        sorted_signals = sorted(self._all_signals, key=len, reverse=True)

        for signal in sorted_signals:
            signal_lower = signal.lower()
            if signal_lower in text_lower:
                position = text_lower.find(signal_lower)
                category = self._signal_map.get(signal, "unknown")

                # 根据位置和上下文计算置信度
                confidence = self._calculate_signal_confidence(
                    text, signal, position
                )

                return {
                    "has_signal": True,
                    "signal": signal,
                    "category": category,
                    "confidence": confidence,
                    "position": position,
                }

        return {"has_signal": False, "signal": None, "category": None, "confidence": 0.0, "position": -1}

    def _calculate_signal_confidence(
        self, text: str, signal: str, position: int
    ) -> float:
        """
        根据上下文计算信号词的置信度

        Args:
            text: 完整文本
            signal: 匹配到的信号词
            position: 信号词位置

        Returns:
            置信度 (0.0 - 1.0)
        """
        base_confidence = {
            "full_retract": 0.95,
            "fiction": 0.90,
            "partial_correct": 0.80,
            "clarify": 0.60,
        }

        category = self._signal_map.get(signal, "unknown")
        confidence = base_confidence.get(category, 0.70)

        # 调整因素
        # 1. 信号词在文本末尾，置信度更高
        if position > len(text) * 0.7:
            confidence += 0.05

        # 2. 信号词在文本开头，置信度更高（更明确）
        if position < len(text) * 0.2:
            confidence += 0.05

        # 3. 文本很短，置信度更高（信号更突出）
        if len(text) < 30:
            confidence += 0.10

        # 4. 包含情绪词，置信度更高
        for emotion in self.EMOTIONAL_CORRECTION:
            if emotion in text:
                confidence += 0.05
                break

        return min(confidence, 1.0)

    def detect_similarity_correction(
        self, text: str, previous_memories: List[Dict], threshold: float = 0.75
    ) -> List[Dict]:
        """
        基于embedding相似度检测修正

        Args:
            text: 当前文本
            previous_memories: 前几条记忆列表
            threshold: 相似度阈值，超过则认为可能是修正

        Returns:
            可能被修正的记忆列表，格式：
            [{
                "memory_id": "xxx",
                "similarity": 0.82,
                "content_preview": "...",
            }]
        """
        if not self.embedding_store or not previous_memories:
            return []

        try:
            # 获取当前文本的embedding
            results = self.embedding_store.search(query=text, top_k=5)

            corrections = []
            for item in results:
                if item["score"] >= threshold:
                    # 获取完整记忆内容
                    memory_id = item["memory_id"]
                    # 找到对应的记忆
                    for mem in previous_memories:
                        if mem.get("memory_id") == memory_id:
                            corrections.append({
                                "memory_id": memory_id,
                                "similarity": item["score"],
                                "content_preview": mem.get("content", "")[:100],
                            })
                            break

            return corrections

        except Exception as e:
            logger.warning("correction_detector: %s", e)
            return []

    def smart_detect(
        self,
        new_text: str,
        recent_memories: List[Dict],
        time_window_seconds: int = 300,
    ) -> Dict:
        """
        综合检测：结合信号词 + 相似度 + 时间窗口

        Args:
            new_text: 新文本
            recent_memories: 最近记忆列表（按时间倒序）
            time_window_seconds: 时间窗口（秒），只检测这个时间范围内的记忆

        Returns:
            检测结果字典：
            {
                "is_correction": True/False,
                "confidence": 0.0-1.0,
                "type": "full_retract|partial_correct|similarity|none",
                "target_memories": [...],  # 可能被修正的记忆
                "signal_info": {...},  # 信号词信息
                "suggested_action": "mark_retracted|create_link|ignore",
            }
        """
        result = {
            "is_correction": False,
            "confidence": 0.0,
            "type": "none",
            "target_memories": [],
            "signal_info": None,
            "suggested_action": "ignore",
            "reason": "",
        }

        # 1. 首先检测信号词（最可靠）
        signal_result = self.detect_correction_signal(new_text)
        result["signal_info"] = signal_result

        if signal_result["has_signal"]:
            result["is_correction"] = True
            result["confidence"] = signal_result["confidence"]
            result["type"] = signal_result["category"]
            result["suggested_action"] = self._get_action_for_type(
                signal_result["category"]
            )
            result["reason"] = f"检测到修正信号词: {signal_result['signal']}"

            # 找到时间窗口内的相关记忆作为目标
            result["target_memories"] = self._find_timewindow_memories(
                recent_memories, time_window_seconds
            )

            return result

        # 2. 如果没有信号词，检查embedding相似度
        if self.embedding_store and recent_memories:
            similarity_corrections = self.detect_similarity_correction(
                new_text, recent_memories
            )

            if similarity_corrections:
                # 找到最高相似度的
                best_match = max(
                    similarity_corrections, key=lambda x: x["similarity"]
                )

                # 需要较高置信度才认为是修正
                if best_match["similarity"] >= 0.85:
                    result["is_correction"] = True
                    result["confidence"] = best_match["similarity"] * 0.8  # 降低置信度
                    result["type"] = "similarity"
                    result["target_memories"] = similarity_corrections
                    result["suggested_action"] = "create_link"
                    result["reason"] = f"高相似度检测（{best_match['similarity']:.2f}），可能是修正"

                    return result

        # 3. 检查是否包含情绪修正词（低置信度）
        for emotion in self.EMOTIONAL_CORRECTION:
            if emotion in new_text:
                # 可能是在开玩笑，降低重要性但不标记为修正
                result["reason"] = f"检测到情绪词: {emotion}，可能是玩笑"
                break

        return result

    def _get_action_for_type(self, correction_type: str) -> str:
        """根据修正类型建议行动"""
        action_map = {
            "full_retract": "mark_retracted",  # 标记为已撤回
            "fiction": "mark_retracted",  # 标记为虚构
            "partial_correct": "create_link",  # 创建关联
            "clarify": "create_link",  # 创建关联
        }
        return action_map.get(correction_type, "create_link")

    def _find_timewindow_memories(
        self, memories: List[Dict], time_window: int
    ) -> List[Dict]:
        """找到时间窗口内的记忆"""
        import time

        current_time = time.time()
        time_threshold = current_time - time_window

        recent = []
        for mem in memories:
            mem_time = mem.get("time_ts", 0)
            if mem_time >= time_threshold:
                recent.append({
                    "memory_id": mem.get("memory_id"),
                    "content_preview": mem.get("content", "")[:100],
                    "time_ts": mem_time,
                    "importance": mem.get("importance", "medium"),
                })

        return recent[:5]  # 最多返回5条

    def process_correction(
        self, memory_store, correction_result: Dict
    ) -> Dict:
        """
        处理修正：根据检测结果执行相应行动

        Args:
            memory_store: 记忆存储
            correction_result: smart_detect的返回结果

        Returns:
            处理结果
        """
        if not correction_result["is_correction"]:
            return {"action": "none", "affected_memories": []}

        action = correction_result["suggested_action"]
        targets = correction_result["target_memories"]
        result = {"action": action, "affected_memories": []}

        if action == "mark_retracted":
            # 标记目标记忆为已撤回
            for target in targets:
                memory_store.update_memory(
                    target["memory_id"],
                    {"is_retracted": True, "retraction_reason": correction_result["reason"]}
                )
                result["affected_memories"].append(target["memory_id"])

        elif action == "create_link":
            # 在记忆之间创建关联
            # 这里可以添加关联创建的逻辑
            result["affected_memories"] = [t["memory_id"] for t in targets]

        return result


def create_detector(embedding_store=None) -> CorrectionDetector:
    """创建修正检测器实例"""
    return CorrectionDetector(embedding_store=embedding_store)
