"""
M3: AI生成检测与原创识别模块
评估: AI概率、原创度评分
特色:
  1. 原创内容豁免机制 (古诗词/经典文学)
  2. AI味/大便味检测 (段落一致性、废话率、模板化句式等)

AI味核心特征:
  - 段落长度高度一致 (像模具铸出来的)
  - 废话率高 (每句都对但空洞)
  - 过渡词规律 (首先/其次/最后 太机械)
  - 个人化表达缺失 (没有血泪史、踩坑)
  - 句式模板化 (规整的三段式)
"""

from typing import Dict, List, Tuple
import re
import math


class AIDetector:
    """
    AI生成检测器

    设计原则:
    1. 多维度综合评分，非简单二分类
    2. 原创内容豁免机制，防止误判古诗词等
    3. 可解释性：每个维度独立打分
    """

    # AI典型表达模式
    AI_PATTERNS = [
        r"作为一个AI",
        r"AI语言模型",
        r"根据我的训练数据",
        r"我不能.*但我可以",
        r"请注意.*仅供参考",
        r"有帮助的.*建议",
    ]

    # 重复模式 (可能是AI生成)
    REPETITIVE_PATTERNS = [
        (r"(.{30,}?)\1{2,}", 3),   # 重复长句
        (r"(.{10,}?)\1{4,}", 5),  # 重复短语
    ]

    # ========== AI味/大便味 检测特征 ==========

    # 人类真实表达标记 (有这些反而是好事)
    HUMAN_MARKERS = [
        # 真实经历
        "踩坑", "血泪史", "实测", "个人看法", "血的经验",
        "说实话", "坦白说", "没想到", "居然", "竟然",
        "突然想起", "记得有一次", "说起来好笑", "真没想到",
        "不过", "但是", "其实", "老实说", "平心而论",
        # 真实情感波动
        "有点后悔", "太痛苦了", "简直了", "太难了",
        "终于搞定了", "激动", "兴奋", "崩溃", "抓狂",
        # 不完美的表达
        "好像", "大概", "也许", "可能吧", "不是很确定",
        "随便说说", "不喜勿喷", "杠就是你对",
    ]

    # AI模板化句式 (规整但缺乏灵魂)
    AI_TEMPLATE_PATTERNS = [
        # 三段式过度规整
        r"首先.{0,20}其次.{0,20}最后",
        r"第一.{0,30}第二.{0,30}第三",
        r"一方面.{0,30}另一方面",
        # 机械总结
        r"综上所述",
        r"总而言之",
        r"简而言之",
        r"总的来说",
        r"通过以上",
        # 泛化的正确废话
        r"具有.*特点",
        r"可以.*实现",
        r"能够.*帮助",
        r"对于.*具有.*意义",
        r"在.*方面.*起到.*作用",
        # 规律过渡词
        r"因此.{0,10}因此",
        r"所以.{0,10}所以",
        r"首先.{1,5}其次.{1,5}然后",
    ]

    # AI高频过渡词 (使用太规律说明是AI)
    AI_TRANSITION_WORDS = [
        "首先", "其次", "最后", "因此", "所以", "然而",
        "与此同时", "综上所述", "总而言之", "值得注意的是",
        "毫无疑问", "不言而喻", "众所周知", "无可否认"
    ]

    def __init__(self):
        self.dimension_weights = {
            "text_statistics": 0.10,
            "perplexity": 0.15,
            "vocabulary_richness": 0.10,
            "style_consistency": 0.10,
            "semantic_coherence": 0.05,
            "special_patterns": 0.10,
            # 新增 AI味检测维度
            "paragraph_uniformity": 0.15,   # 段落一致性
            "bullshit_ratio": 0.10,          # 废话率
            "template_patterns": 0.10,      # 模板化程度
            "human_markers": 0.05,           # 人类真实表达
        }

    def detect(self, content: str) -> Dict:
        """
        检测AI生成概率和原创性

        Returns:
            {
                "ai_probability": float (0-1),
                "is_ai_generated": bool,
                "originality_score": int (0-100),
                "confidence_label": str,
                "ai_flavor_score": int (0-100),  # AI味/大便味评分
                "dimensions": {...}
            }
        """
        text_len = len(content)

        # 检测豁免类型 (古诗词等)
        exemption = self._detect_exemption(content)
        exemption_type = exemption["type"]
        exemption_confidence = exemption["confidence"]

        # 各维度评分
        dim_scores = {}

        # D1: 文本统计特征
        dim_scores["text_statistics"] = self._calc_text_statistics(content)

        # D2: 困惑度 (简化版)
        dim_scores["perplexity"] = self._calc_perplexity_score(content)

        # D3: 词汇丰富度
        dim_scores["vocabulary_richness"] = self._calc_vocabulary_richness(content)

        # D4: 风格一致性
        dim_scores["style_consistency"] = self._calc_style_consistency(content)

        # D5: 语义连贯性
        dim_scores["semantic_coherence"] = self._calc_semantic_coherence(content)

        # D6: 特殊模式 (豁免检测)
        dim_scores["special_patterns"] = self._calc_special_patterns_score(content, exemption)

        # ========== 新增: AI味/大便味检测 ==========

        # D7: 段落一致性 (AI文章段落长度高度一致)
        dim_scores["paragraph_uniformity"] = self._calc_paragraph_uniformity(content)

        # D8: 废话率 (每句都对但空洞)
        dim_scores["bullshit_ratio"] = self._calc_bullshit_ratio(content)

        # D9: 模板化程度 (三段式、过度规整)
        dim_scores["template_patterns"] = self._calc_template_patterns_score(content)

        # D10: 人类真实表达标记
        dim_scores["human_markers"] = self._calc_human_markers_score(content)

        # 计算加权总分
        weighted_score = sum(
            dim_scores[d] * self.dimension_weights[d]
            for d in self.dimension_weights
        )

        # 应用豁免机制
        if exemption_type:
            boost = self._get_exemption_boost(exemption_type)
            weighted_score = min(100, weighted_score * boost)

        ai_probability = 1 - (weighted_score / 100)
        originality_score = int(weighted_score)

        # AI味/大便味评分 (越高越像AI)
        ai_flavor_score = self._calc_ai_flavor_score(dim_scores)

        # 判断是否为AI生成
        is_ai_generated = ai_probability > 0.6

        # 置信度标签
        confidence_label = self._get_confidence_label(weighted_score, exemption_type)

        return {
            "ai_probability": round(ai_probability, 2),
            "is_ai_generated": is_ai_generated,
            "originality_score": originality_score,
            "ai_flavor_score": ai_flavor_score,
            "ai_flavor_level": self._get_ai_flavor_level(ai_flavor_score),
            "confidence_label": confidence_label,
            "exemption_type": exemption_type,
            "exemption_confidence": exemption_confidence,
            "dimensions": {k: {"score": round(v, 1)} for k, v in dim_scores.items()},
            "weights": self.dimension_weights,
            "analysis": self._generate_analysis(dim_scores, exemption),
            "ai_flavor_warnings": self._generate_ai_flavor_warnings(dim_scores),
        }

    def _detect_exemption(self, content: str) -> Dict:
        """
        检测是否属于豁免类型 (古诗词等)
        """
        # 古诗词检测
        poetry_result = self._detect_poetry(content)
        if poetry_result["is_poetry"]:
            return {"type": "classical_poetry", "confidence": poetry_result["confidence"]}

        # 经典文学检测
        lit_result = self._detect_classic_literature(content)
        if lit_result["is_classic"]:
            return {"type": "classic_literature", "confidence": lit_result["confidence"]}

        return {"type": None, "confidence": 0}

    def _detect_poetry(self, content: str) -> Dict:
        """检测是否为古诗词"""
        lines = [l.strip() for l in content.split("\n") if l.strip()]

        if len(lines) < 2:
            return {"is_poetry": False, "confidence": 0}

        # 检查每行字数 (五言/七言)
        char_counts = [len(l) for l in lines if len(l) < 20]
        if not char_counts:
            return {"is_poetry": False, "confidence": 0}

        # 押韵检测 (简单版：尾字相同或相近)
        rhyme_chars = [l[-1] if l else "" for l in lines if l]
        rhyme_match = len(set(rhyme_chars)) <= max(2, len(rhyme_chars) // 2)

        # 五言/七言格式
        is_wuzyan = all(c in [5, 7] for c in char_counts if 3 <= c <= 10)

        # 计算置信度
        confidence = 0
        if is_wuzyan:
            confidence += 0.4
        if rhyme_match:
            confidence += 0.3
        if 4 <= len(lines) <= 8:
            confidence += 0.2

        # 意象词密度
        imagery_words = ["月", "风", "花", "雪", "鸟", "云", "山", "水", "日", "星"]
        imagery_count = sum(content.count(w) for w in imagery_words)
        if imagery_count >= len(lines):
            confidence += 0.1

        return {"is_poetry": confidence >= 0.5, "confidence": min(1.0, confidence)}

    def _detect_classic_literature(self, content: str) -> Dict:
        """检测是否为经典文学作品"""
        sentences = re.split(r"[.!?。！？]", content)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return {"is_classic": False, "confidence": 0}

        avg_sentence_len = sum(len(s) for s in sentences) / len(sentences)

        # 长句比例 (经典文学通常句子较长)
        long_sentence_ratio = sum(1 for s in sentences if len(s) > 30) / len(sentences)

        # 复合句指标 (顿号、关联词)
        compound_indicators = content.count("，") + content.count("；")
        compound_ratio = compound_indicators / max(len(content), 1) * 100

        confidence = 0
        if avg_sentence_len > 35:
            confidence += 0.3
        if long_sentence_ratio > 0.4:
            confidence += 0.3
        if compound_ratio > 5:
            confidence += 0.2

        return {"is_classic": confidence >= 0.6, "confidence": min(1.0, confidence)}

    def _get_exemption_boost(self, exemption_type: str) -> float:
        """获取豁免类型的分数加成"""
        boosts = {
            "classical_poetry": 1.3,
            "classic_literature": 1.25
        }
        return boosts.get(exemption_type, 1.0)

    def _calc_text_statistics(self, content: str) -> float:
        """D1: 文本统计特征"""
        sentences = re.split(r"[.!?。！？]", content)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 50

        sentence_lengths = [len(s) for s in sentences]
        variance = self._calc_variance(sentence_lengths)

        # AI特征: 句子长度方差小
        # 正常人类写作方差较大
        variance_score = max(0, 100 - variance * 0.5)

        # 标点多样性
        puncts = set(content) & set(".,!?;:'\"()[]{}，。！？；：""''")
        punctuation_score = min(100, len(puncts) * 15)

        return (variance_score * 0.6 + punctuation_score * 0.4)

    def _calc_perplexity_score(self, content: str) -> float:
        """
        D2: 困惑度评分 (简化版)

        简化实现：通过句子长度均匀度和词汇重复率模拟困惑度
        真实实现需要使用 n-gram 语言模型
        """
        sentences = re.split(r"[.!?。！？]", content)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) < 3:
            return 70

        # 句子长度均匀度
        sentence_lengths = [len(s) for s in sentences]
        variance = self._calc_variance(sentence_lengths)

        # 方差过小 = 可能AI (分数降低)
        variance_penalty = min(30, variance * 0.3)

        # 词汇重复率
        words = content.split()
        if words:
            unique_ratio = len(set(words)) / len(words)
            repetition_score = unique_ratio * 60
        else:
            repetition_score = 50

        return max(20, 100 - variance_penalty + repetition_score - 40)

    def _calc_vocabulary_richness(self, content: str) -> float:
        """D3: 词汇丰富度"""
        words = content.split()
        if not words:
            return 50

        # Type-Token Ratio
        ttr = len(set(words)) / len(words)

        # 罕见词汇 (长词比例)
        long_words = sum(1 for w in words if len(w) > 6)
        long_word_ratio = long_words / len(words)

        score = ttr * 50 + long_word_ratio * 50
        return min(100, score)

    def _calc_style_consistency(self, content: str) -> float:
        """D4: 风格一致性分析"""
        # 句子开头词分析
        sentences = re.split(r"[.!?。！？]", content)
        sentences = [s.strip() for s in sentences if s.strip()][:10]

        if not sentences:
            return 70

        opening_words = []
        for s in sentences:
            words = s.split()
            if words:
                opening_words.append(words[0])

        # 开头词重复率 (AI倾向于用相同的开头)
        if len(opening_words) > 1:
            unique_opening_ratio = len(set(opening_words)) / len(opening_words)
            opening_score = unique_opening_ratio * 60
        else:
            opening_score = 50

        # 过渡词使用规律
        transitions = ["然而", "但是", "因此", "所以", "并且", "同时"]
        transition_count = sum(content.count(t) for t in transitions)
        transition_density = transition_count / max(len(content) / 500, 1)

        # 过渡词过多或过少都可能是AI特征
        transition_score = 100 - abs(transition_density - 3) * 20

        return (opening_score * 0.5 + max(0, transition_score) * 0.5)

    def _calc_semantic_coherence(self, content: str) -> float:
        """D5: 语义连贯性"""
        sentences = re.split(r"[.!?。！？]", content)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) < 2:
            return 80

        # 代词密度 (人称代词通常表示良好指代)
        pronouns = ["我", "你", "他", "她", "它", "我们", "他们", "她们"]
        pronoun_count = sum(content.count(p) for p in pronouns)

        # 逻辑连接词
        connectors = ["因为", "所以", "如果", "虽然", "但是", "而且", "或者"]
        connector_count = sum(content.count(c) for c in connectors)

        semantic_score = min(100, pronoun_count * 2 + connector_count * 5)
        return semantic_score if semantic_score > 30 else 60

    def _calc_special_patterns_score(self, content: str, exemption: Dict) -> float:
        """D6: 特殊模式评分 (豁免检测)"""
        if exemption["type"] == "classical_poetry":
            return 95
        elif exemption["type"] == "classic_literature":
            return 90

        # AI典型表达检测
        ai_pattern_score = 100
        for pattern in self.AI_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                ai_pattern_score -= 20

        # 重复模式检测
        for pattern, weight in self.REPETITIVE_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                ai_pattern_score -= weight * len(matches)

        return max(0, ai_pattern_score)

    def _calc_variance(self, values: list) -> float:
        """计算方差"""
        if not values:
            return 0
        mean = sum(values) / len(values)
        return sum((v - mean) ** 2 for v in values) / len(values)

    def _get_confidence_label(self, score: float, exemption_type: str) -> str:
        """获取置信度标签"""
        if exemption_type:
            return "高度可信原创"

        if score >= 85:
            return "高度可信原创"
        elif score >= 70:
            return "可能是原创"
        elif score >= 50:
            return "无法确定"
        elif score >= 30:
            return "中度疑似AI"
        else:
            return "高度疑似AI"

    def _generate_analysis(self, dim_scores: Dict, exemption: Dict) -> str:
        """生成分析说明"""
        if exemption["type"]:
            exemption_names = {
                "classical_poetry": "古诗词",
                "classic_literature": "经典文学作品"
            }
            return f"检测为{exemption_names.get(exemption['type'], '原创')}格式，应用原创性豁免规则"

        concerns = []
        if dim_scores["text_statistics"] < 50:
            concerns.append("句子长度过于均匀")
        if dim_scores["perplexity"] < 50:
            concerns.append("语言过于流畅")
        if dim_scores["vocabulary_richness"] < 50:
            concerns.append("词汇丰富度偏低")

        if concerns:
            return "可能的AI特征: " + "、".join(concerns)
        return "未检测到明显的AI生成特征"

    # ========== 新增: AI味/大便味检测实现 ==========

    def _calc_paragraph_uniformity(self, content: str) -> float:
        """
        D7: 段落一致性检测

        AI生成的文章段落长度高度一致，像模具铸出来的。
        真正的好文章段落有长有短，自然波动。
        """
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

        if len(paragraphs) < 3:
            return 70  # 段落太少无法判断

        para_lengths = [len(p) for p in paragraphs]

        # 计算段落长度方差
        variance = self._calc_variance(para_lengths)
        mean_length = sum(para_lengths) / len(para_lengths)

        # 方差系数 (CV = std/mean) - 越小越一致，越像AI
        if mean_length > 0:
            std_dev = math.sqrt(variance)
            cv = std_dev / mean_length
        else:
            cv = 0

        # CV < 0.3 说明段落长度高度一致 = AI味
        # CV > 0.5 说明段落长度变化大 = 人类写作
        if cv < 0.2:
            uniformity_score = 20  # 高度一致，AI味浓
        elif cv < 0.3:
            uniformity_score = 40
        elif cv < 0.4:
            uniformity_score = 60
        elif cv < 0.5:
            uniformity_score = 80
        else:
            uniformity_score = 95  # 变化大，人类写作

        # 额外检查：段落平均长度是否都接近
        close_to_mean_count = sum(1 for l in para_lengths if abs(l - mean_length) < mean_length * 0.2)
        if close_to_mean_count / len(para_lengths) > 0.7:
            uniformity_score = min(uniformity_score, 30)  # 大多数段落长度接近 = AI味

        return uniformity_score

    def _calc_bullshit_ratio(self, content: str) -> float:
        """
        D8: 废话率检测

        AI写的每句话都"正确"但空洞，没有实质信息。
        检测方法：
        1. 统计泛化表达（如"具有重要意义"）
        2. 统计无实质内容的填充句
        3. 计算信息量密度
        """
        # 废话模式
        BULLSHIT_PATTERNS = [
            r"具有重要意义",
            r"起到关键作用",
            r"对于.*具有.*意义",
            r"在.*方面.*作用",
            r"是一个.*问题",
            r"需要.*考虑",
            r"可以.*实现",
            r"能够.*帮助",
            r"目的是.*为了",
            r"主要是.*因为",
            r"涉及到.*方面",
            r"这种情况.*发生",
            r"相关.*研究.*表明",
            r"根据.*显示",
            r"从.*角度来看",
            r"总的来说",
            r"一般而言",
            r"通常情况下",
        ]

        sentences = re.split(r"[.!?。！？]", content)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 50

        bullshit_count = 0
        for sentence in sentences:
            for pattern in BULLSHIT_PATTERNS:
                if re.search(pattern, sentence):
                    bullshit_count += 1
                    break

            # 超短无意义句子
            if len(sentence) < 15:
                bullshit_count += 0.5

        bullshit_ratio = bullshit_count / len(sentences)

        # 废话率越高 = AI味越重
        if bullshit_ratio > 0.5:
            return 15
        elif bullshit_ratio > 0.4:
            return 30
        elif bullshit_ratio > 0.3:
            return 50
        elif bullshit_ratio > 0.2:
            return 70
        elif bullshit_ratio > 0.1:
            return 85
        else:
            return 95  # 废话少，说明有实质内容

    def _calc_template_patterns_score(self, content: str) -> float:
        """
        D9: 模板化程度检测

        AI倾向于使用规整的模板：
        - "首先/其次/最后" 三段式
        - "综上所述/总而言之" 机械总结
        - 规律的使用过渡词
        """
        template_score = 100  # 初始100分，越低越AI

        # 检测模板化句式
        template_matches = 0
        for pattern in self.AI_TEMPLATE_PATTERNS:
            matches = re.findall(pattern, content)
            template_matches += len(matches)

        # 模板化句式越多，分数越低
        if template_matches >= 5:
            template_score = 15
        elif template_matches >= 4:
            template_score = 30
        elif template_matches >= 3:
            template_score = 50
        elif template_matches >= 2:
            template_score = 70
        elif template_matches >= 1:
            template_score = 85

        # 检测过渡词规律性
        transition_analysis = self._analyze_transition_pattern(content)
        if transition_analysis["is_too_regular"]:
            template_score = template_score * 0.6  # 降低分数

        return max(0, template_score)

    def _analyze_transition_pattern(self, content: str) -> Dict:
        """
        分析过渡词使用规律性

        AI倾向于规律使用过渡词，而人类写作过渡词使用更自然。
        """
        # 统计AI高频过渡词
        ai_transition_count = sum(content.count(w) for w in self.AI_TRANSITION_WORDS)

        # 计算过渡词之间的间距
        transition_positions = []
        for word in self.AI_TRANSITION_WORDS:
            pos = 0
            while True:
                pos = content.find(word, pos)
                if pos == -1:
                    break
                transition_positions.append(pos)
                pos += 1

        if len(transition_positions) < 3:
            return {"is_too_regular": False, "reason": "过渡词太少"}

        # 计算间距方差
        spacings = [transition_positions[i+1] - transition_positions[i]
                   for i in range(len(transition_positions)-1)]

        if len(spacings) < 2:
            return {"is_too_regular": False, "reason": "间距无法计算"}

        spacing_variance = self._calc_variance(spacings)
        avg_spacing = sum(spacings) / len(spacings)

        # 间距方差小 = 规律使用 = AI
        if avg_spacing > 0:
            cv = math.sqrt(spacing_variance) / avg_spacing
            if cv < 0.5 and len(transition_positions) >= 4:
                return {
                    "is_too_regular": True,
                    "reason": f"过渡词间距过于规律 (CV={cv:.2f})",
                    "transition_count": ai_transition_count
                }

        return {"is_too_regular": False, "reason": "过渡词使用自然"}

    def _calc_human_markers_score(self, content: str) -> float:
        """
        D10: 人类真实表达标记

        人类写作会有真实的生活痕迹：
        - 踩坑经验
        - 情感波动
        - 不确定的表达
        - 个人化的叙述

        AI写作缺乏这些personal voice。
        """
        human_marker_count = sum(content.count(marker) for marker in self.HUMAN_MARKERS)

        # 计算人类标记密度
        text_length = len(content)
        density = human_marker_count / (text_length / 500)  # 每500字的标记数

        if density >= 5:
            return 95  # 标记丰富，人类写作
        elif density >= 3:
            return 80
        elif density >= 2:
            return 65
        elif density >= 1:
            return 50
        elif density >= 0.5:
            return 35
        else:
            return 20  # 几乎没有人类标记，AI味浓

    def _calc_ai_flavor_score(self, dim_scores: Dict) -> int:
        """
        计算AI味/大便味综合评分 (0-100)

        越高说明AI味越重。
        """
        # AI味维度：段落一致性、废话率、模板化
        # 这些维度得分越高(原创性越高)，AI味越低，需要反转
        ai_flavor_dimensions = {
            "paragraph_uniformity": dim_scores.get("paragraph_uniformity", 50),
            "bullshit_ratio": dim_scores.get("bullshit_ratio", 50),
            "template_patterns": dim_scores.get("template_patterns", 50),
        }

        # 人类标记维度：得分越高AI味越低
        human_dimensions = {
            "human_markers": dim_scores.get("human_markers", 50),
        }

        # AI味得分 = 加权平均（反转AI味维度）
        ai_score = sum(
            (100 - score)
            for dim, score in ai_flavor_dimensions.items()
        ) / len(ai_flavor_dimensions)

        # 人类得分
        human_score = sum(
            score * 0.05  # 人类标记权重较小
            for score in human_dimensions.values()
        )

        final_ai_flavor = min(100, max(0, ai_score * 0.9 + (100 - human_score) * 0.1))

        return int(final_ai_flavor)

    def _get_ai_flavor_level(self, score: int) -> str:
        """获取AI味等级"""
        if score < 20:
            return "人类写作 (几乎无AI味)"
        elif score < 40:
            return "轻度疑似AI"
        elif score < 60:
            return "中度疑似AI"
        elif score < 80:
            return "高度疑似AI"
        else:
            return "极强AI味 (大便味)"

    def _generate_ai_flavor_warnings(self, dim_scores: Dict) -> List[str]:
        """生成AI味警告列表"""
        warnings = []

        if dim_scores.get("paragraph_uniformity", 50) < 40:
            warnings.append(f"段落长度高度一致，AI味特征明显 (一致性: {dim_scores['paragraph_uniformity']:.0f})")

        if dim_scores.get("bullshit_ratio", 50) < 40:
            warnings.append(f"废话率较高，内容空洞 (废话率指标: {dim_scores['bullshit_ratio']:.0f})")

        if dim_scores.get("template_patterns", 50) < 50:
            warnings.append(f"使用模板化句式，缺乏个性 (模板化: {dim_scores['template_patterns']:.0f})")

        if dim_scores.get("human_markers", 50) < 40:
            warnings.append(f"缺少人类真实表达痕迹，没有personal voice (人类标记: {dim_scores['human_markers']:.0f})")

        return warnings


if __name__ == "__main__":
    detector = AIDetector()

    test_cases = [
        # 古诗 - 应该豁免
        ("床前明月光，疑是地上霜。举头望明月，低头思故乡。", "古诗"),

        # 典型AI味文章 - 三段式、废话率高、段落一致
        ("""
        首先，人工智能技术在现代社会中具有重要意义。
        其次，人工智能可以应用于多个领域，如医疗、金融、教育等。
        最后，人工智能的发展需要考虑伦理和法律问题。

        综上所述，人工智能技术对于推动社会进步具有重要作用。
        因此，我们应该积极拥抱这一技术变革。
        所以，企业应该加大在人工智能领域的投入。
        """, "典型AI味文章"),

        # 真实人类写作 - 有血泪史、情感波动、段落长度不一
        ("""
        说实话，之前踩坑踩怕了。

        记得有一次半夜爬起来排查bug，结果发现是个低级错误——少了个分号。那一刻真的崩溃，血泪史啊血泪史。

        后来学乖了，每次上线前都要检查三遍。不过说实话，这种经历才是真正的成长。

        没想到代码review的时候竟然被夸了！激动！
        """, "真实人类写作"),

        # 模板化AI文章
        ("""
        Python是一种高级编程语言，它具有简洁易学的特点，被广泛应用于Web开发、数据科学、人工智能等领域。

        首先，Python拥有丰富的库和框架。
        其次，Python的语法简洁明了。
        最后，Python具有强大的社区支持。

        总的来说，Python是一门非常优秀的编程语言。
        因此，对于初学者来说，Python是一个很好的选择。
        所以，建议大家好好学习Python。
        """, "模板化AI文章"),
    ]

    for text, label in test_cases:
        result = detector.detect(text)
        print(f"\n{'='*50}")
        print(f"【{label}】")
        print(f"{'='*50}")
        print(f"  AI概率: {result['ai_probability']:.0%}")
        print(f"  原创评分: {result['originality_score']}/100")
        print(f"  AI味评分: {result['ai_flavor_score']}/100 ({result['ai_flavor_level']})")
        print(f"  结论: {result['confidence_label']}")

        if result.get('ai_flavor_warnings'):
            print(f"  AI味警告:")
            for w in result['ai_flavor_warnings']:
                print(f"    - {w}")

        print(f"\n  各维度得分:")
        for dim, info in result['dimensions'].items():
            dim_names = {
                "text_statistics": "文本统计",
                "perplexity": "困惑度",
                "vocabulary_richness": "词汇丰富",
                "style_consistency": "风格一致",
                "semantic_coherence": "语义连贯",
                "special_patterns": "特殊模式",
                "paragraph_uniformity": "段落一致",
                "bullshit_ratio": "废话率",
                "template_patterns": "模板化",
                "human_markers": "人类标记",
            }
            name = dim_names.get(dim, dim)
            print(f"    {name}: {info['score']:.0f}")
