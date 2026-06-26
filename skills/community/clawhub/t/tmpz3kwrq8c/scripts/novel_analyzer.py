"""
M2-N: 小说分析模块 (无剧透版)
评估: 情节结构、人物塑造、叙事技巧、文风特点
核心原则: 不泄露关键情节
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import re


class SpoilerLevel(Enum):
    """剧透风险等级"""
    SAFE = "safe"       # 无剧透风险
    LOW = "low"        # 低风险
    MEDIUM = "medium"  # 中风险
    HIGH = "high"      # 高风险


@dataclass
class SpoilerWarning:
    """剧透警告"""
    dimension: str
    risk_level: SpoilerLevel
    message: str
    safe_summary: str


class NovelAnalyzer:
    """
    小说分析器 (无剧透版)

    核心原则:
    1. 形式分析优先于内容分析
    2. 关键情节只描述类型/位置，不描述具体内容
    3. 人物分析只描述塑造手法，不揭示命运
    4. 用户可配置剧透容忍度
    """

    STRUCTURE_TYPES = [
        "三幕式", "英雄之旅", "倒叙结构", "平行叙事",
        "环形结构", "碎片式", "渐进式", "套盒结构"
    ]

    CLIMAX_TYPES = [
        "action", "emotional", "revelation", "combined"
    ]

    def __init__(self, spoiler_tolerance: SpoilerLevel = SpoilerLevel.LOW):
        self.spoiler_tolerance = spoiler_tolerance
        self.dimension_weights = {
            "plot_structure": 0.25,
            "character_craft": 0.25,
            "narrative_technique": 0.20,
            "style_features": 0.15,
            "world_building": 0.15
        }

    def analyze(self, title: str, content: str, genre_hint: str = None) -> Dict:
        """
        分析小说质量 (无剧透)

        Returns:
            维度评分 + 结构分析 + 剧透警告
        """
        word_count = len(content)
        genre = genre_hint or self._detect_genre(content)

        scores = {}

        # 1. 情节结构 (25%)
        scores["plot_structure"] = self._calc_plot_structure(content)

        # 2. 人物塑造 (25%)
        scores["character_craft"] = self._calc_character_craft(content)

        # 3. 叙事技巧 (20%)
        scores["narrative_technique"] = self._calc_narrative_technique(content)

        # 4. 文风特点 (15%)
        scores["style_features"] = self._calc_style_features(content)

        # 5. 世界观构建 (15%) - 简化版
        scores["world_building"] = self._calc_world_building(content)

        # 剧透风险评估
        spoiler_warnings = self._assess_spoiler_risk(scores)

        # 过滤高风险内容 (根据容忍度)
        safe_result = self._filter_spoilers(scores, spoiler_warnings)

        return {
            "dimension_scores": safe_result["scores"],
            "weights": self.dimension_weights,
            "overall_score": sum(
                safe_result["scores"][d] * self.dimension_weights[d]
                for d in self.dimension_weights
            ),
            "genre": genre,
            "word_count": word_count,
            "plot_analysis": self._analyze_plot_structure_only(content),
            "character_profiles": self._analyze_characters_only(content),
            "spoiler_warnings": [
                {"dimension": w.dimension, "risk": w.risk_level.value, "message": w.message}
                for w in spoiler_warnings
            ],
            "spoiler_free_summary": self._generate_spoiler_free_summary(safe_result["scores"]),
            "reader_experience": self._predict_reader_experience(content, scores)
        }

    def _detect_genre(self, content: str) -> str:
        """检测小说类型"""
        genre_markers = {
            "玄幻": ["修炼", "灵气", "境界", "宗门", "飞升"],
            "科幻": ["飞船", "星球", "科技", "未来", "人工智能"],
            "悬疑": ["线索", "真相", "推理", "嫌疑", "案件"],
            "言情": ["爱情", "心动", "相守", "思念", "甜蜜"],
            "武侠": ["江湖", "武功", "侠客", "门派", "剑法"],
            "历史": ["朝代", "皇帝", "征战", "权谋", "江山"]
        }

        for genre, markers in genre_markers.items():
            if sum(content.count(m) for m in markers) >= 3:
                return genre
        return "文学小说"

    def _calc_plot_structure(self, content: str) -> float:
        """计算情节结构得分"""
        paragraphs = [p for p in content.split("\n\n") if p.strip()]
        paragraph_count = len(paragraphs)

        # 结构标记
        act_markers = ["开始", "接着", "然后", "最后", "与此同时", "没想到"]
        act_count = sum(content.count(m) for m in act_markers)

        # 场景转换
        scene_breaks = content.count("\n\n")

        # 悬念设置 (问号密度)
        question_density = content.count("?") + content.count("？")
        question_score = min(20, question_density * 3)

        structure = paragraph_count * 1.5 + act_count * 5 + scene_breaks * 3 + question_score
        return min(100, structure)

    def _calc_character_craft(self, content: str) -> float:
        """计算人物塑造得分"""
        # 对话比例 (人物塑造的重要手段)
        dialogue_ratio = (content.count('"') + content.count('"') + content.count('"')) / max(len(content), 1) * 100

        # 心理描写
        psychology_markers = ["想", "觉得", "知道", "明白", "记得", "仿佛"]
        psycho_count = sum(content.count(m) for m in psychology_markers)

        # 人物动作/神态
        action_markers = ["走", "看", "说", "笑", "哭", "站", "坐"]
        action_count = sum(content.count(m) for m in action_markers)

        craft = dialogue_ratio * 2 + psycho_count * 3 + action_count * 2
        return min(100, 30 + craft)

    def _calc_narrative_technique(self, content: str) -> float:
        """计算叙事技巧得分"""
        # 叙事视角标记
        first_person = content.count("我") / max(len(content), 1) * 100
        third_person = content.count("他") + content.count("她")

        # 时间处理 (时间词密度)
        time_markers = ["那年", "后来", "如今", "曾经", "当时", "此刻"]
        time_count = sum(content.count(m) for m in time_markers)

        # 回忆/倒叙标记
        flashback_markers = ["记得", "想起", "回忆", "往事", "曾经"]
        flashback_count = sum(content.count(m) for m in flashback_markers)

        technique = first_person * 3 + time_count * 5 + flashback_count * 8
        return min(100, 40 + technique)

    def _calc_style_features(self, content: str) -> float:
        """计算文风特点得分"""
        sentences = re.split(r"[.!?。！？]", content)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 50

        # 句子长度变化
        sentence_lengths = [len(s) for s in sentences]
        variance = self._calc_variance(sentence_lengths)
        variety_score = min(30, variance * 0.3)

        # 修辞密度
        metaphors = ["像", "如同", "仿佛", "如", "似的"]
        metaphor_count = sum(content.count(m) for m in metaphors)

        # 描写密度 (形容词+副词)
        descriptive_density = len(re.findall(r"[的地得]|[很非常特别极其]", content))

        style = variety_score + metaphor_count * 5 + descriptive_density * 0.5
        return min(100, 40 + style)

    def _calc_world_building(self, content: str) -> float:
        """计算世界观构建得分 (简化版)"""
        # 环境描写密度
        setting_markers = ["窗外", "屋里", "街道", "城市", "乡村", "天空", "大地"]
        setting_count = sum(content.count(m) for m in setting_markers)

        # 专有名词密度 (假设世界构建丰富会有更多专有名词)
        proper_nouns = len(re.findall(r"[《【](.{2,6})[】》]", content))

        world = setting_count * 3 + proper_nouns * 8
        return min(100, 30 + world)

    def _analyze_plot_structure_only(self, content: str) -> Dict:
        """
        分析情节结构 (不泄露具体情节)

        只返回结构类型和比例，不描述具体事件
        """
        paragraphs = [p for p in content.split("\n\n") if p.strip()]
        total_len = len(content)

        if len(paragraphs) < 3:
            return {"structure_type": "简单直叙", "act_ratios": {}}

        # 简化: 假设三幕式
        act1_len = sum(len(p) for p in paragraphs[:len(paragraphs)//3])
        act2_len = sum(len(p) for p in paragraphs[len(paragraphs)//3:2*len(paragraphs)//3])
        act3_len = sum(len(p) for p in paragraphs[2*len(paragraphs)//3:])

        total = max(act1_len + act2_len + act3_len, 1)

        return {
            "structure_type": "三幕式",
            "act_ratios": {
                "setup": round(act1_len / total, 2),
                "confrontation": round(act2_len / total, 2),
                "resolution": round(act3_len / total, 2)
            },
            "pacing": self._assess_pacing(paragraphs)
        }

    def _analyze_characters_only(self, content: str) -> List[Dict]:
        """
        分析人物 (不泄露命运)

        只描述塑造手法和角色类型，不描述具体变化
        """
        characters = []

        # 简化: 识别主要人物视角
        first_person_count = content.count("我")
        if first_person_count > 10:
            characters.append({
                "role": "protagonist",
                "perspective": "第一人称",
                "arc_type": "dynamic",  # 不描述具体弧光
                "voice_strength": "强烈"
            })

        # 配角检测 (对话中的其他人)
        dialogue_count = content.count('"') // 2
        if dialogue_count > 5:
            characters.append({
                "role": "supporting",
                "count": min(dialogue_count // 3, 5),
                "voice_type": "对话驱动"
            })

        return characters if characters else [{"role": "unknown", "note": "需要更多内容分析"}]

    def _assess_spoiler_risk(self, scores: Dict) -> List[SpoilerWarning]:
        """评估剧透风险"""
        warnings = []

        # 情感高潮分析 - 中等风险
        warnings.append(SpoilerWarning(
            dimension="emotional_curve",
            risk_level=SpoilerLevel.MEDIUM,
            message="情感高潮分析可能涉及关键情节暗示",
            safe_summary="情感曲线为拱形/线性/波动型"
        ))

        # 人物命运 - 高风险
        warnings.append(SpoilerWarning(
            dimension="character_arc",
            risk_level=SpoilerLevel.HIGH,
            message="人物命运分析可能揭示结局",
            safe_summary="人物弧光类型为静态/动态/反讽"
        ))

        # 情节转折 - 高风险
        warnings.append(SpoilerWarning(
            dimension="plot_twist",
            risk_level=SpoilerLevel.HIGH,
            message="情节转折分析可能泄露关键事件",
            safe_summary="转折点位置在全文的30%/50%/70%处"
        ))

        return warnings

    def _filter_spoilers(self, scores: Dict, warnings: List[SpoilerWarning]) -> Dict:
        """根据剧透容忍度过滤内容"""
        if self.spoiler_tolerance == SpoilerLevel.HIGH:
            return {"scores": scores, "filtered_dims": []}

        filtered_dims = []
        safe_scores = scores.copy()

        for w in warnings:
            if w.risk_level.value >= self.spoiler_tolerance.value:
                # 降低该维度权重或用安全描述替代
                if w.dimension in safe_scores:
                    safe_scores[w.dimension] *= 0.8  # 降低分数
                filtered_dims.append(w.dimension)

        return {"scores": safe_scores, "filtered_dims": filtered_dims}

    def _generate_spoiler_free_summary(self, scores: Dict) -> Dict:
        """生成无剧透摘要"""
        top_dims = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

        return {
            "key_strengths": [
                f"{dim}表现优秀" for dim, score in top_dims if score >= 70
            ],
            "reading_difficulty": "适中",
            "target_audience": "文学爱好者",
            "expected_experience": "情感沉浸 + 思考"
        }

    def _predict_reader_experience(self, content: str, scores: Dict) -> Dict:
        """预测读者体验"""
        word_count = len(content)

        if word_count < 1000:
            time_estimate = "5-10分钟"
        elif word_count < 5000:
            time_estimate = "15-30分钟"
        else:
            time_estimate = "1小时以上"

        return {
            "reading_time": time_estimate,
            "emotional_journey": "平静 → 投入 → 回味",
            "difficulty": "适中" if scores["style_features"] > 60 else "较高"
        }

    def _assess_pacing(self, paragraphs: List[str]) -> str:
        """评估节奏"""
        if len(paragraphs) < 5:
            return "紧凑"

        avg_len = sum(len(p) for p in paragraphs) / len(paragraphs)

        if avg_len > 200:
            return "舒缓"
        elif avg_len > 100:
            return "适中"
        else:
            return "紧凑"

    def _calc_variance(self, values: List[float]) -> float:
        if not values:
            return 0
        mean = sum(values) / len(values)
        return sum((v - mean) ** 2 for v in values) / len(values)


if __name__ == "__main__":
    analyzer = NovelAnalyzer(spoiler_tolerance=SpoilerLevel.LOW)

    test_content = """
    那是一个冬天的傍晚，雪纷纷扬扬地落下来。他站在车站里，等待着最后一班车。

    "你真的要走吗？"她问。

    他没有回答，只是看着窗外的雪花，想起了很多年前的那个夏天。那时候他们还年轻，以为时间还很长。

    后来，他终于明白，有些告别是不需要说再见的。
    """

    result = analyzer.analyze("等待", test_content)

    print("小说分析结果:")
    print(f"  类型: {result['genre']}")
    print(f"  总分: {result['overall_score']:.1f}")
    print(f"  情节结构: {result['dimension_scores']['plot_structure']:.1f}")
    print(f"  人物塑造: {result['dimension_scores']['character_craft']:.1f}")
    print(f"  剧透警告数: {len(result['spoiler_warnings'])}")
