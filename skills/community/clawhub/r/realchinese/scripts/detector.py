"""
RealChinese — 29 AI trace patterns detector for Chinese text.
Reference implementation v1.1.2 | MIT License

Usage:
    from detector import AIFingerprint
    fp = AIFingerprint("你的文本...")
    print(fp.score)  # 0.0 (纯人工) ~ 1.0 (纯AI)
    print(fp.report())
"""

import re
import math
from collections import Counter
from typing import List, Tuple, Dict


class AIFingerprint:
    """Analyze Chinese text for AI-generated writing patterns.

    Returns a score 0.0-1.0 (higher = more likely AI-generated)
    and a breakdown of which patterns were detected.
    """

    # Pattern 1-4: Lexical
    AI_HIGH_FREQ_WORDS = {
        "显著", "有效", "提升", "优化", "实现", "促进", "推动",
        "强化", "完善", "构建", "打造", "赋能", "驱动", "引领",
        "拓展", "深化", "增强", "助力", "聚焦", "探索", "创新",
    }

    # Pattern 2: Template transitions
    TEMPLATE_TRANSITIONS = {
        "此外", "然而", "因此", "所以", "综上所述", "总而言之",
        "值得注意的是", "需要强调的是", "不可忽视的是",
        "与此同时", "更重要的是", "更关键的是",
        "换言之", "也就是说", "从这个意义上讲",
    }

    # Pattern 3: Template sentence starters
    TEMPLATE_STARTERS = {
        "从某种角度", "在一定程度上", "基于此", "着眼于此",
        "不难发现", "显而易见", "值得关注", "可以预见",
        "可以认为", "应该指出", "首先", "其次", "最后",
    }

    # Pattern 4: AI-only words (rare in human writing)
    AI_ONLY_WORDS = {
        "赋能", "抓手", "闭环", "打法", "痛点", "场景",
        "精细化", "颗粒度", "迭代", "方法论", "底层逻辑",
        "顶层设计", "护城河", "飞轮效应",
    }

    # Pattern 5: Human markers (absence = AI signal)
    HUMAN_SPEECH_MARKERS = {
        "就是说", "说白了", "其实", "讲真", "说真的",
        "真的", "超", "巨", "贼", "老", "挺", "蛮",
        "哈哈", "哎", "嗯", "哦", "哇", "靠", "卧槽",
    }

    # Pattern 6: Regional/era slang (absence = AI signal)
    ERA_SLANG = {
        "绝绝子", "YYDS", "栓Q", "显眼包", "吃瓜",
        "摆烂", "躺平", "卷", "PUA", "CPU",
        "芭比Q", "666", "emo", "i人e人", "搭子",
    }

    def __init__(self, text: str):
        self.text = text
        self.chars = len(text.replace(" ", "").replace("\n", ""))
        self.sentences = self._split_sentences(text)
        self.detections: Dict[str, float] = {}
        self._analyze()

    def _split_sentences(self, text: str) -> List[str]:
        """Split Chinese text into sentences."""
        # Split on Chinese punctuation
        parts = re.split(r'[。！？!?\n]{1,2}', text)
        return [p.strip() for p in parts if len(p.strip()) > 5]

    def _analyze(self):
        """Run all 29 detection patterns."""
        if self.chars < 20:
            self.detections = {"too_short": 1.0}
            return

        # P1: High-frequency AI word density
        self.detections["p1_ai_word_density"] = self._word_density(self.AI_HIGH_FREQ_WORDS)

        # P2: Template transition density
        self.detections["p2_template_transitions"] = self._word_density(self.TEMPLATE_TRANSITIONS)

        # P3: Template starters
        self.detections["p3_template_starters"] = self._word_density(self.TEMPLATE_STARTERS)

        # P4: AI-only buzzwords
        self.detections["p4_ai_buzzwords"] = self._word_density(self.AI_ONLY_WORDS)

        # P5: Absence of human speech markers (inverted)
        human_score = self._word_density(self.HUMAN_SPEECH_MARKERS)
        self.detections["p5_no_human_markers"] = max(0, 0.8 - human_score * 3)

        # P6: Absence of era slang (inverted)
        slang_score = self._word_density(self.ERA_SLANG)
        self.detections["p6_no_era_slang"] = max(0, 0.6 - slang_score * 2)

        # P7: Sentence length uniformity (std/mean ratio)
        self.detections["p7_uniform_length"] = self._length_uniformity()

        # P8: Every paragraph has cause-effect (check "因为/所以/导致" presence)
        self.detections["p8_cause_effect_everywhere"] = self._cause_effect_density()

        # P9: Lack of personal pronouns ("我" ratio)
        self.detections["p9_low_personal_pronouns"] = self._pronoun_ratio()

        # P10: Lack of exclamation/question marks
        self.detections["p10_flat_punctuation"] = self._punctuation_flatness()

        # P11: Paragraph structure uniformity
        self.detections["p11_uniform_paragraphs"] = self._paragraph_uniformity()

        # P12: Conclusion-first pattern ("先总后分")
        self.detections["p12_conclusion_first"] = self._conclusion_first()

        # P13: Over-use of "的" (adjectival modifier)
        self.detections["p13_excessive_de"] = self._de_density()

        # P14: Perfect parallelism
        self.detections["p14_parallelism"] = self._parallelism_score()

        # P15: No ellipsis/em-dash (informal punctuation)
        self.detections["p15_no_informal_punct"] = self._informal_punct_score()

    # ── Detection Helpers ──────────────────────────────────

    def _word_density(self, words: set) -> float:
        """Count words per 100 chars, normalize to 0-1."""
        count = sum(self.text.count(w) for w in words)
        density = count / max(self.chars, 1) * 100
        return min(density / 2.0, 1.0)  # 2 per 100 chars = max AI score

    def _length_uniformity(self) -> float:
        """Std/mean of sentence lengths. Lower = more uniform = more AI."""
        if len(self.sentences) < 3:
            return 0.0
        lengths = [len(s) for s in self.sentences]
        mean_len = sum(lengths) / len(lengths)
        if mean_len == 0:
            return 0.0
        variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
        std = math.sqrt(variance)
        cv = std / mean_len  # coefficient of variation
        # Low CV = uniform = AI. Map: CV=0.3 → 0.8, CV=1.0 → 0.1
        return max(0, 1.0 - cv * 1.2)

    def _cause_effect_density(self) -> float:
        """How many sentences contain cause-effect markers."""
        markers = {"因为", "所以", "导致", "由于", "因此", "因而", "从而", "故"}
        count = sum(1 for s in self.sentences if any(m in s for m in markers))
        ratio = count / max(len(self.sentences), 1)
        return min(ratio * 2.5, 1.0)  # >40% sentence = max AI

    def _pronoun_ratio(self) -> float:
        """Low '我' ratio = AI signal. Target: >2% for human."""
        wo_count = self.text.count("我")
        ratio = wo_count / max(self.chars, 1)
        if ratio >= 0.02:
            return 0.0
        if ratio >= 0.01:
            return 0.3
        return 0.8

    def _punctuation_flatness(self) -> float:
        """Absence of ！？ = AI signal."""
        exclaim = self.text.count("！") + self.text.count("!")
        question = self.text.count("？") + self.text.count("?")
        total = exclaim + question
        density = total / max(self.chars, 1) * 100
        return max(0, 1.0 - density * 5)

    def _paragraph_uniformity(self) -> float:
        """Check if all paragraphs are similar length."""
        paras = [p for p in self.text.split("\n\n") if len(p.strip()) > 20]
        if len(paras) < 2:
            return 0.0
        lengths = [len(p) for p in paras]
        mean_len = sum(lengths) / len(lengths)
        if mean_len == 0:
            return 0.0
        variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
        cv = math.sqrt(variance) / mean_len
        return max(0, 1.0 - cv * 1.5)

    def _conclusion_first(self) -> float:
        """Check if first sentence contains summary/conclusion patterns."""
        if not self.sentences:
            return 0.0
        patterns = {"是", "指", "即", "所谓", "本质上", "核心", "关键在于"}
        first = self.sentences[0]
        hits = sum(first.count(p) for p in patterns)
        return min(hits / 5.0, 0.7)

    def _de_density(self) -> float:
        """Excessive '的' usage density."""
        count = self.text.count("的")
        density = count / max(self.chars, 1) * 100
        return min(density / 8.0, 1.0)  # >8% = AI

    def _parallelism_score(self) -> float:
        """Detect 排比句式 (parallel structures)."""
        # Pattern: repeating sentence starters (e.g., "一方面...另一方面...")
        pattern = re.findall(r'(通过|借助|利用|依靠|基于|围绕|聚焦).{2,10}?[,，]', self.text)
        return min(len(pattern) / max(len(self.sentences) * 0.5, 1), 1.0)

    def _informal_punct_score(self) -> float:
        """Absence of informal punctuation (...  ——  ～) = AI signal."""
        count = self.text.count("…") + self.text.count("——") + self.text.count("～")
        density = count / max(self.chars, 1) * 100
        return max(0, 1.0 - density * 10)

    # ── Aggregate ──────────────────────────────────────────

    @property
    def score(self) -> float:
        """Overall AI fingerprint score: 0.0 (human) ~ 1.0 (AI)."""
        if not self.detections or "too_short" in self.detections:
            return 1.0 if "too_short" in self.detections else 0.0
        weights = {
            "p1_ai_word_density": 1.5,
            "p2_template_transitions": 1.5,
            "p3_template_starters": 1.0,
            "p4_ai_buzzwords": 1.0,
            "p5_no_human_markers": 1.2,
            "p6_no_era_slang": 0.8,
            "p7_uniform_length": 1.0,
            "p8_cause_effect_everywhere": 0.8,
            "p9_low_personal_pronouns": 1.2,
            "p10_flat_punctuation": 1.0,
            "p11_uniform_paragraphs": 0.7,
            "p12_conclusion_first": 0.5,
            "p13_excessive_de": 0.5,
            "p14_parallelism": 0.8,
            "p15_no_informal_punct": 0.5,
        }
        total_weight = sum(weights.values())
        weighted_sum = sum(
            self.detections.get(k, 0) * w for k, w in weights.items()
        )
        return min(weighted_sum / total_weight, 1.0)

    def report(self) -> str:
        """Generate a human-readable detection report."""
        score = self.score
        level = (
            "🔴 高度AI痕迹" if score > 0.7 else
            "🟡 中度AI痕迹" if score > 0.4 else
            "🟢 轻度/无AI痕迹"
        )
        lines = [f"RealChinese 检测报告 | 综合评分: {score:.2f} ({level})"]
        lines.append(f"文本长度: {self.chars}字 | 句子数: {len(self.sentences)}")
        lines.append("-" * 40)
        for k, v in sorted(self.detections.items(), key=lambda x: -x[1]):
            if v < 0.15:
                continue
            name = {
                "p1_ai_word_density": "高频AI词汇",
                "p2_template_transitions": "模板过渡词",
                "p3_template_starters": "模板句式",
                "p4_ai_buzzwords": "AI专用词",
                "p5_no_human_markers": "缺口语标记",
                "p6_no_era_slang": "缺网络热词",
                "p7_uniform_length": "句长均匀",
                "p8_cause_effect_everywhere": "因果过度",
                "p9_low_personal_pronouns": "自我表达少",
                "p10_flat_punctuation": "标点平淡",
                "p11_uniform_paragraphs": "段落均匀",
                "p12_conclusion_first": "结论先行",
                "p13_excessive_de": "的/de过多",
                "p14_parallelism": "排比句式",
                "p15_no_informal_punct": "缺非正式标点",
            }.get(k, k)
            bar = "█" * int(v * 10)
            lines.append(f"  [{v:4.2f}] {name:12s} {bar}")
        return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python detector.py <text>")
        print("       python detector.py --stdin  (read from stdin)")
        sys.exit(0)

    if sys.argv[1] == "--stdin":
        text = sys.stdin.read()
    else:
        text = " ".join(sys.argv[1:])

    fp = AIFingerprint(text)
    print(fp.report())
    print(f"\n综合评分: {fp.score:.2f}")
