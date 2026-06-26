"""
M2-C: 情感散文与小说分析模块
评估: 情感表达、文笔水平、叙事结构、创意性、共鸣度
"""

from typing import Dict, List
import re


class CreativeAnalyzer:
    """
    情感散文与创意写作分析器

    设计原则:
    1. 形式分析优先于内容分析
    2. 不泄露具体情节
    3. 聚焦情感曲线和写作技巧
    """

    EMOTION_WORDS = [
        "温暖", "感动", "悲伤", "喜悦", "思念", "爱", "希望", "梦想",
        "回忆", "勇气", "坚强", "心疼", "幸福", "痛苦", "孤独",
        "失落", "期待", "怀念", "感激", "释然", "愤怒", "恐惧"
    ]

    POSITIVE_EMOTION = {"温暖", "感动", "喜悦", "希望", "梦想", "幸福", "勇气", "坚强", "感激", "释然"}
    NEGATIVE_EMOTION = {"悲伤", "痛苦", "孤独", "失落", "恐惧", "愤怒", "心疼", "怀念"}

    METAPHOR_KEYWORDS = ["像", "如同", "仿佛", "犹如", "好像", "如", "似的"]

    def __init__(self):
        self.dimension_weights = {
            "emotion_expression": 0.30,
            "writing_style": 0.25,
            "narrative_structure": 0.20,
            "creativity": 0.15,
            "resonance": 0.10
        }

    def analyze(self, title: str, content: str, article_type: str = "essay") -> Dict:
        """
        分析情感/散文文章

        Args:
            title: 文章标题
            content: 文章内容
            article_type: essay | novel (简化版novel调用NovelAnalyzer)

        Returns:
            维度得分字典 + 详细分析
        """
        scores = {}

        # 1. 情感表达 (30%)
        scores["emotion_expression"] = self._calc_emotion_expression(content)

        # 2. 文笔水平 (25%)
        scores["writing_style"] = self._calc_writing_style(content)

        # 3. 叙事结构 (20%)
        scores["narrative_structure"] = self._calc_narrative_structure(content)

        # 4. 创意性 (15%)
        scores["creativity"] = self._calc_creativity(content)

        # 5. 共鸣度 (10%)
        scores["resonance"] = self._calc_resonance(content)

        return {
            "dimension_scores": scores,
            "weights": self.dimension_weights,
            "emotional_curve": self._analyze_emotional_curve(content),
            "genre_specific": self._analyze_genre_specific(content, article_type),
            "indicators": {
                "emotion_word_count": sum(content.count(w) for w in self.EMOTION_WORDS),
                "metaphor_count": sum(content.count(m) for m in self.METAPHOR_KEYWORDS),
                "paragraph_count": len([p for p in content.split("\n\n") if p.strip()]),
                "first_person_usage": content.count("我") + content.count("我们"),
                "dialogue_ratio": self._calc_dialogue_ratio(content)
            },
            "spoiler_warnings": [],
            "strengths": self._identify_strengths(scores),
            "improvements": self._identify_improvements(content, scores)
        }

    def _calc_emotion_expression(self, content: str) -> float:
        """计算情感表达得分"""
        emotion_count = sum(content.count(w) for w in self.EMOTION_WORDS)
        text_length = len(content)

        # 情感词密度
        emotion_density = emotion_count / (text_length / 500)

        # 情感多样性
        present_emotions = [w for w in self.EMOTION_WORDS if w in content]
        emotion_diversity = min(1.0, len(present_emotions) / 5)

        score = emotion_density * 8 + emotion_diversity * 30
        return min(100, max(20, score))

    def _calc_writing_style(self, content: str) -> float:
        """计算文笔水平得分"""
        # 修辞手法使用
        metaphor_count = sum(content.count(m) for m in self.METAPHOR_KEYWORDS)
        metaphor_score = min(40, metaphor_count * 6)

        # 句式变化
        sentence_lengths = self._get_sentence_lengths(content)
        if len(sentence_lengths) >= 3:
            variance = self._calc_variance(sentence_lengths)
            sentence_variety = min(30, variance * 0.5)
        else:
            sentence_variety = 20

        # 标点使用多样性
        puncts = set(content) & set("，。！？；：、""''")
        punctuation_score = min(30, len(punts) * 8)

        return metaphor_score + sentence_variety + punctuation_score

    def _calc_narrative_structure(self, content: str) -> float:
        """计算叙事结构得分"""
        paragraphs = [p for p in content.split("\n\n") if p.strip()]
        paragraph_count = len(paragraphs)

        # 场景转换标记
        scene_markers = content.count("\n\n") + content.count("——") + content.count("...")

        # 时间/空间过渡词
        transition_words = ["那时", "后来", "如今", "于是", "接着", "最后", "最初"]
        transition_count = sum(content.count(w) for w in transition_words)

        structure_score = paragraph_count * 2 + scene_markers * 5 + transition_count * 4
        return min(100, structure_score)

    def _calc_creativity(self, content: str) -> float:
        """计算创意性得分"""
        words = content.split()

        # 词汇独特性
        if words:
            unique_ratio = len(set(words)) / len(words)
            uniqueness = unique_ratio * 50
        else:
            uniqueness = 30

        # 比喻的新颖程度 (简化版)
        metaphor_count = sum(content.count(m) for m in self.METAPHOR_KEYWORDS)

        # 罕见表达检测
        rare_expressions = ["蓦然", "氤氲", "婆娑", "涟漪", "斑驳", "蹉跎", "缱绻"]
        rare_count = sum(content.count(e) for e in rare_expressions)

        creativity = uniqueness + metaphor_count * 3 + rare_count * 10
        return min(100, creativity)

    def _calc_resonance(self, content: str) -> float:
        """计算共鸣度得分"""
        # 第一人称使用
        first_person = content.count("我") + content.count("我们")

        # 对话比例
        dialogue_ratio = self._calc_dialogue_ratio(content)

        # 情感强度词
        strong_emotions = ["永远", "一直", "深刻", "强烈", "刻骨铭心", "撕心裂肺"]
        strong_count = sum(content.count(e) for e in strong_emotions)

        resonance = first_person * 1.5 + dialogue_ratio * 200 + strong_count * 5
        return min(100, 30 + resonance)

    def _analyze_emotional_curve(self, content: str) -> Dict:
        """
        分析情感曲线

        Returns:
            曲线类型、起始情感、结束情感、高潮位置
        """
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

        if len(paragraphs) < 2:
            return {
                "arc_type": "plateau",
                "description": "情感平稳",
                "start_emotion": "平静",
                "end_emotion": "平静",
                "peak_position": 0.5
            }

        # 简化: 统计每段的情感词密度
        paragraph_emotions = []
        for p in paragraphs:
            emotion_count = sum(p.count(w) for w in self.EMOTION_WORDS)
            paragraph_emotions.append(emotion_count)

        if not paragraph_emotions:
            return {
                "arc_type": "plateau",
                "description": "情感平稳",
                "start_emotion": "平静",
                "end_emotion": "平静",
                "peak_position": 0.5
            }

        first_half_avg = sum(paragraph_emotions[:len(paragraphs)//2]) / max(len(paragraphs)//2, 1)
        second_half_avg = sum(paragraph_emotions[len(paragraphs)//2:]) / max(len(paragraphs) - len(paragraphs)//2, 1)

        # 找高潮位置
        peak_idx = paragraph_emotions.index(max(paragraph_emotions)) if paragraph_emotions else 0
        peak_position = (peak_idx + 1) / len(paragraphs)

        # 判断曲线类型
        if second_half_avg > first_half_avg * 1.3:
            arc_type = "rising"
            description = "情感逐渐升华"
        elif second_half_avg < first_half_avg * 0.7:
            arc_type = "falling"
            description = "情感缓缓沉淀"
        elif peak_position < 0.4:
            arc_type = "a_shape"
            description = "先扬后抑"
        elif peak_position > 0.7:
            arc_type = "v_shape"
            description = "先抑后扬"
        else:
            arc_type = "plateau"
            description = "情感平稳"

        # 判断起始/结束情感
        start_emotion = "积极" if first_half_avg > 1 else "平静"
        end_emotion = "积极" if second_half_avg > 1 else "平静"

        return {
            "arc_type": arc_type,
            "description": description,
            "start_emotion": start_emotion,
            "end_emotion": end_emotion,
            "peak_position": round(peak_position, 2)
        }

    def _analyze_genre_specific(self, content: str, article_type: str) -> Dict:
        """体裁特定分析"""
        if article_type == "novel":
            # 简化版小说分析
            return self._basic_novel_analysis(content)
        else:
            # 散文特定分析
            return self._prose_specific_analysis(content)

    def _prose_specific_analysis(self, content: str) -> Dict:
        """散文特定分析"""
        return {
            "imagery_density": self._calc_imagery_density(content),
            "contemplative_depth": self._calc_contemplative_depth(content),
            "personal_voice_strength": self._calc_personal_voice(content)
        }

    def _basic_novel_analysis(self, content: str) -> Dict:
        """简化版小说分析 (详细版见 NovelAnalyzer)"""
        return {
            "dialogue_ratio": self._calc_dialogue_ratio(content),
            "scene_transitions": content.count("\n\n"),
            "narrative_pacing": "平稳" if len(content) < 5000 else "有节奏变化"
        }

    def _calc_dialogue_ratio(self, content: str) -> float:
        """计算对话比例"""
        quote_count = content.count('"') + content.count('"') + content.count('"')
        return quote_count / max(len(content), 1) * 100

    def _calc_imagery_density(self, content: str) -> float:
        """计算意象密度"""
        imagery_words = ["阳光", "月光", "星空", "风", "雨", "雪", "花", "树",
                        "山", "水", "云", "鸟", "叶", "海", "河", "梦", "影"]
        count = sum(content.count(w) for w in imagery_words)
        return min(100, count * 8)

    def _calc_contemplative_depth(self, content: str) -> float:
        """计算思辨深度"""
        reflection_markers = ["思考", "感悟", "明白", "理解", "认识", "体会",
                            "发现", "懂得", "领悟", "省悟"]
        count = sum(content.count(m) for m in reflection_markers)
        return min(100, 30 + count * 12)

    def _calc_personal_voice(self, content: str) -> float:
        """计算个人声音强度"""
        first_person = content.count("我")
        memory_markers = ["记得", "小时候", "曾经", "那时", "往事"]
        memory_count = sum(content.count(m) for m in memory_markers)

        return min(100, first_person * 2 + memory_count * 8)

    def _get_sentence_lengths(self, content: str) -> List[int]:
        """获取句子长度列表"""
        sentences = re.split(r"[.!?。！？]", content)
        return [len(s.strip()) for s in sentences if s.strip()]

    def _calc_variance(self, values: List[float]) -> float:
        """计算方差"""
        if not values:
            return 0
        mean = sum(values) / len(values)
        return sum((v - mean) ** 2 for v in values) / len(values)

    def _identify_strengths(self, scores: Dict) -> List[str]:
        """识别优点"""
        strengths = []
        if scores["emotion_expression"] >= 70:
            strengths.append("情感表达真挚细腻")
        if scores["writing_style"] >= 70:
            strengths.append("文笔优美，修辞手法丰富")
        if scores["narrative_structure"] >= 70:
            strengths.append("结构安排有致")
        if scores["creativity"] >= 70:
            strengths.append("有独特的表达和视角")
        if scores["resonance"] >= 70:
            strengths.append("能引起读者共鸣")
        return strengths

    def _identify_improvements(self, content: str, scores: Dict) -> List[str]:
        """识别改进建议"""
        improvements = []
        if scores["emotion_expression"] < 50:
            improvements.append("可加强情感表达，增加情感词密度")
        if scores["writing_style"] < 50:
            improvements.append("可增加更多修辞手法，丰富句式")
        if scores["narrative_structure"] < 50:
            improvements.append("建议加强段落之间的过渡")
        if scores["creativity"] < 50:
            improvements.append("可尝试更独特的表达方式")
        if self._calc_dialogue_ratio(content) < 2:
            improvements.append("可适当增加对话，增强互动感")
        return improvements


if __name__ == "__main__":
    analyzer = CreativeAnalyzer()

    test_cases = [
        ("秋日随想", "秋风起，落叶黄。站在老槐树下，我想起了远方的母亲..."),
        ("那一年夏天", "阳光、蝉鸣、还有那个再也回不去的童年..."),
    ]

    for title, content in test_cases:
        result = analyzer.analyze(title, content)
        print(f"\n【{title}】")
        for dim, score in result["dimension_scores"].items():
            print(f"  {dim}: {score:.1f}")
        print(f"  情感曲线: {result['emotional_curve']['arc_type']} - {result['emotional_curve']['description']}")
