"""金句提取器 — 本地三信号评分：句长/语义完整度/关键词密度"""

import re
from typing import Any, Dict, List, Optional

from ..logger import get_logger

logger = get_logger(__name__)


# 信号权重（总和 = 1.0）
SIGNAL_WEIGHTS = {
    "sentence_length": 0.25,
    "semantic_completeness": 0.45,
    "keyword_density": 0.30,
}

# 中文关键词词典（规则/决策/判断/结论/方法/经验类）
KEYWORD_PATTERNS = [
    r"关键", r"核心", r"本质", r"原则", r"方法", r"技巧",
    r"经验", r"教训", r"总结", r"结论", r"观点", r"建议",
    r"记住", r"注意", r"必须", r"应该", r"一定", r"绝对",
    r"首先", r"其次", r"最后", r"总之", r"归根结底", r"最重要",
    r"发现", r"意识到", r"认识到", r"证明", r"说明", r"意味着",
    r"秘诀", r"真相", r"规律", r"逻辑", r"思维", r"框架",
]

# 句末标点
SENTENCE_END = r"[。！？；.!?;]"


class HighlightExtractor:
    """
    金句提取器 — 纯本地评分，无API依赖。
    
    三信号评分模型：
    1. 句长信号（15-80字最佳，过短/过长扣分）
    2. 语义完整度（是否包含主谓宾/完整意思单元）
    3. 关键词密度（命中关键词模式的频次）
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.highlight_config = config.get("highlight", {})
        self.min_length = self.highlight_config.get("min_length", 15)
        self.max_length = self.highlight_config.get("max_length", 80)
        self.top_n = self.highlight_config.get("top_n", 10)

    def extract(
        self,
        segments: List[Dict[str, Any]],
        min_confidence: float = 0.5,
    ) -> Dict[str, Any]:
        """
        从语音段中提取金句。
        
        Args:
            segments: whisper 识别结果中的语音段列表
            min_confidence: 最低置信度阈值（0-1）
            
        Returns:
            {
                "highlights": [
                    {
                        "text": "完整金句文本",
                        "start": 12.5,
                        "end": 18.3,
                        "confidence": 0.82,
                        "scores": {...},
                        "reasons": [...],
                    }
                ],
                "total_candidates": 15,
                "total_extracted": 8,
            }
        """
        if not segments:
            return {"highlights": [], "total_candidates": 0, "total_extracted": 0}

        # 切分完整句
        candidates = self._split_to_sentences(segments)

        if not candidates:
            return {"highlights": [], "total_candidates": 0, "total_extracted": 0}

        # 逐句评分
        scored = []
        for candidate in candidates:
            result = self._score_sentence(candidate)
            if result["confidence"] >= min_confidence:
                scored.append(result)

        # 按置信度排序，取 top_n
        scored.sort(key=lambda x: x["confidence"], reverse=True)
        highlights = scored[: self.top_n]

        logger.info(
            f"金句提取完成: {len(highlights)}/{len(candidates)} 条 "
            f"(置信度 ≥ {min_confidence})"
        )

        return {
            "highlights": highlights,
            "total_candidates": len(candidates),
            "total_extracted": len(highlights),
        }

    def _split_to_sentences(
        self,
        segments: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """将语音段切分为完整句"""
        sentences = []
        current_text = ""
        current_start = None

        for seg in segments:
            text = seg.get("text", "").strip()
            if not text:
                continue

            if current_start is None:
                current_start = seg.get("start", 0)

            current_text += text

            # 检查是否句末
            if re.search(SENTENCE_END, text):
                # 清理句末标点
                clean_text = re.sub(r"\s+", "", current_text).strip()
                if len(clean_text) >= self.min_length:
                    sentences.append({
                        "text": clean_text,
                        "start": current_start,
                        "end": seg.get("end", 0),
                    })
                current_text = ""
                current_start = None

        # 处理末尾未完结的文本
        if current_text and len(current_text.strip()) >= self.min_length:
            sentences.append({
                "text": re.sub(r"\s+", "", current_text).strip(),
                "start": current_start or 0,
                "end": segments[-1].get("end", 0) if segments else 0,
            })

        return sentences

    def _score_sentence(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """对单句进行三信号评分"""
        text = candidate["text"]
        reasons = []

        # 信号1: 句长评分
        length_score = self._score_length(text)

        # 信号2: 语义完整度
        semantic_score, semantic_reasons = self._score_semantic(text)
        reasons.extend(semantic_reasons)

        # 信号3: 关键词密度
        keyword_score, keyword_reasons = self._score_keywords(text)
        reasons.extend(keyword_reasons)

        # 加权总分
        confidence = (
            length_score * SIGNAL_WEIGHTS["sentence_length"]
            + semantic_score * SIGNAL_WEIGHTS["semantic_completeness"]
            + keyword_score * SIGNAL_WEIGHTS["keyword_density"]
        )

        # 归一化到 0-1
        confidence = min(max(confidence, 0.0), 1.0)

        if length_score >= 0.8:
            reasons.append(f"句长适中（{len(text)}字）")
        if keyword_score >= 0.6:
            reasons.append("含关键词")

        return {
            "text": text,
            "start": candidate["start"],
            "end": candidate["end"],
            "confidence": round(confidence, 2),
            "scores": {
                "length": round(length_score, 2),
                "semantic": round(semantic_score, 2),
                "keyword": round(keyword_score, 2),
            },
            "reasons": reasons[:3],  # 最多3个理由
        }

    def _score_length(self, text: str) -> float:
        """句长评分 — 15-80字最佳"""
        length = len(text)
        if length < self.min_length:
            return length / self.min_length * 0.3
        elif length <= 40:
            return 0.7 + 0.3 * (length - self.min_length) / (40 - self.min_length)
        elif length <= self.max_length:
            return 1.0
        else:
            # 过长递减
            return max(0.3, 1.0 - (length - self.max_length) / 100)

    def _score_semantic(self, text: str) -> tuple:
        """语义完整度评分"""
        score = 0.5
        reasons = []

        # 包含动词（中文动词常见模式）
        verb_patterns = [
            r"是", r"有", r"在", r"做", r"说", r"看", r"想", r"知道",
            r"认为", r"觉得", r"希望", r"需要", r"必须", r"应该",
            r"能", r"会", r"可以", r"去", r"来", r"给", r"到", r"用",
        ]
        for vp in verb_patterns:
            if vp in text:
                score += 0.1
                break

        # 包含主语相关词（我/你/他/我们/他们/大家/人）
        subject_words = ["我", "你", "他", "她", "我们", "你们", "他们", "大家", "人", "这", "那"]
        for sw in subject_words:
            if sw in text:
                score += 0.1
                break

        # 包含总结/判断词（说明/证明/反映/表明/意味着）
        judgment_words = ["说明", "证明", "反映", "表明", "意味着", "显示", "代表"]
        for jw in judgment_words:
            if jw in text:
                score += 0.15
                reasons.append("含判断词")
                break

        # 含数字（具体化表达更有信息量）
        if re.search(r"\d+", text):
            score += 0.05

        # 含引号（引用/强调）
        if '"' in text or '"' in text or '"' in text:
            score += 0.05
            reasons.append("含引用/强调")

        return min(score, 1.0), reasons

    def _score_keywords(self, text: str) -> tuple:
        """关键词密度评分"""
        if not text:
            return 0.0, []

        hit_count = 0
        matched_keywords = []

        for pattern in KEYWORD_PATTERNS:
            if re.search(pattern, text):
                hit_count += 1
                matched_keywords.append(pattern)

        if hit_count == 0:
            return 0.0, []

        # 每命中1个 +0.3，最多1.0
        score = min(hit_count * 0.3, 1.0)
        reasons = [f"命中关键词: {', '.join(matched_keywords[:3])}"]

        return score, reasons
