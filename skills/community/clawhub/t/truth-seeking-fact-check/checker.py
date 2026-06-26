#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Truth (求真) v1.3 - 核心核查引擎
功能：事实核查逻辑、评分计算、置信度解释
"""

from typing import Dict, List, Optional, Tuple
from datasource import DataSourceManager


class ProblemItem:
    """问题句子项"""
    
    def __init__(self, sentence: str, position: int, reason: str, score: float):
        self.sentence = sentence
        self.position = position
        self.reason = reason
        self.score = score
    
    def to_dict(self) -> Dict:
        return {
            "sentence": self.sentence,
            "position": self.position,
            "reason": self.reason,
            "score": self.score
        }


class ConfidenceExplain:
    """置信度解释"""
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.dimension_scores = {
            "来源匹配度": 0.0,
            "逻辑一致性": 0.0,
            "常识符合度": 0.0,
            "信息明确性": 0.0
        }
        # 默认权重，可用户配置
        self.default_weights = {
            "来源匹配度": 0.4,
            "逻辑一致性": 0.25,
            "常识符合度": 0.25,
            "信息明确性": 0.1
        }
        self.weights = weights if weights is not None else self.default_weights
        # 移除未启用的维度（用户配置可关闭某些维度
        for dim in list(self.weights.keys()):
            if dim not in self.dimension_scores:
                del self.weights[dim]
        self.overall_explanation = ""
        # 元认知：对本次结果的自我置信度（0-100%
        self.meta_confidence = 0.0
    
    def set_score(self, dimension: str, score: float):
        """设置维度得分，0-10分"""
        if dimension in self.dimension_scores:
            self.dimension_scores[dimension] = max(0, min(10, score))
    
    def calculate_meta_confidence(self):
        """计算元认知置信度：基于得分分布和问题数量计算"""
        # 元认知置信度计算逻辑：
        # 1. 维度得分越分散，置信度越低；越集中，置信度越高
        # 2. 问题越多，置信度适当降低
        # 3. 来源匹配度越高，置信度越高
        if "来源匹配度" not in self.weights:
            # 关闭了来源匹配，置信度降低
            base = 50.0
        else:
            base = self.dimension_scores["来源匹配度"] * 8  # 来源匹配占比大
        
        # 计算得分方差
        scores = [s for s in self.dimension_scores.values() if s > 0]
        if len(scores) < 2:
            var = 0
        else:
            mean = sum(scores) / len(scores)
            var = sum((s - mean)**2 for s in scores) / len(scores)
        
        # 方差越大，置信度越低
        var_penalty = min(20, var * 5)
        self.meta_confidence = max(0, min(100, base - var_penalty))
        self.meta_confidence = round(self.meta_confidence, 1)
    
    def get_overall_score(self) -> float:
        """计算加权总分"""
        total = 0.0
        weight_sum = 0.0
        for dim, weight in self.weights.items():
            if dim in self.dimension_scores:
                total += self.dimension_scores[dim] * weight
                weight_sum += weight
        if weight_sum == 0:
            return 5.0
        return round(total / weight_sum, 1)
    
    def to_dict(self) -> Dict:
        return {
            "dimension_scores": self.dimension_scores,
            "weights": self.weights,
            "meta_confidence": self.meta_confidence,
            "overall_explanation": self.overall_explanation
        }


class CheckResult:
    """核查结果"""
    
    def __init__(self, text: str, sentences: List[str], weights: Optional[Dict[str, float]] = None):
        self.text_length = len(text)
        self.credibility_score = 0.0
        self.problematic_sentences: List[ProblemItem] = []
        self.suggestions: List[str] = []
        self.confidence_explanation = ConfidenceExplain(weights)
        self.conclusion = ""
        # 元认知：模型对本次结论自我置信度（0-100%
        self.meta_confidence = 0.0
    
    def add_problem(self, sentence: str, position: int, reason: str, score: float):
        """添加问题句子"""
        self.problematic_sentences.append(ProblemItem(sentence, position, reason, score))
    
    def add_suggestion(self, suggestion: str):
        """添加改进建议"""
        self.suggestions.append(suggestion)
    
    def calculate_final_score(self):
        """计算最终得分"""
        self.credibility_score = self.confidence_explanation.get_overall_score()
        # 根据问题句子调整
        if self.problematic_sentences:
            penalty = len(self.problematic_sentences) * 0.5
            self.credibility_score = max(0, self.credibility_score - penalty)
        self.credibility_score = round(self.credibility_score, 1)
        # 计算元认知置信度
        self.confidence_explanation.calculate_meta_confidence()
        self.meta_confidence = self.confidence_explanation.meta_confidence
    
    def generate_conclusion(self):
        """生成总体结论"""
        score = self.credibility_score
        if score >= 8:
            self.conclusion = "整体可信度高，未发现明显不实内容"
        elif score >= 6:
            self.conclusion = "整体可信度中等，存在少量可能不实内容，请参考标注"
        elif score >= 4:
            self.conclusion = "整体可信度较低，存在多处可能不实内容，建议交叉验证"
        else:
            self.conclusion = "整体可信度低，存在严重不实嫌疑，不建议采信"
        # 添加元认知置信度说明
        if self.meta_confidence >= 80:
            self.conclusion += f"（模型对该结论置信度高：{self.meta_confidence}%）"
        elif self.meta_confidence >= 50:
            self.conclusion += f"（模型对该结论置信度中等：{self.meta_confidence}%）"
        else:
            self.conclusion += f"（模型对该结论置信度较低：{self.meta_confidence}%，建议更多交叉验证）"
    
    def to_dict(self) -> Dict:
        return {
            "text_length": self.text_length,
            "credibility_score": self.credibility_score,
            "problematic_sentences": [p.to_dict() for p in self.problematic_sentences],
            "suggestions": self.suggestions,
            "confidence_explanation": self.confidence_explanation.to_dict(),
            "meta_confidence": self.meta_confidence,
            "conclusion": self.conclusion
        }


class FactChecker:
    """事实核查引擎"""
    
    def __init__(self, datasource: DataSourceManager):
        self.datasource = datasource
    
    def check(self, text: str, sentences: List[str], weights: Optional[Dict[str, float]] = None) -> CheckResult:
        """执行事实核查，支持自定义维度权重"""
        result = CheckResult(text, sentences, weights)
        explain = result.confidence_explanation
        
        # 初始化维度得分默认5分
        for dim in explain.dimension_scores:
            explain.set_score(dim, 5.0)
        
        # 逐句核查
        for idx, sentence in enumerate(sentences):
            self._check_sentence(sentence, idx, result, explain)
        
        # 检查逻辑一致性
        self._check_logical_consistency(sentences, result, explain)
        
        # 检查信息明确性
        self._check_clarity(text, sentences, result, explain)
        
        # 计算最终得分和结论
        result.calculate_final_score()
        result.generate_conclusion()
        
        # 生成解释
        self._generate_explanation(result)
        
        return result
    
    def _check_sentence(self, sentence: str, position: int, result: CheckResult, explain: ConfidenceExplain):
        """单句核查"""
        # 数据源搜索
        search_results = self.datasource.get_search_results(sentence)
        
        if search_results is None:
            # 无数据源，不扣分，但提示
            result.add_suggestion("当前未配置事实数据源，核查结果仅供参考")
            return
        
        if len(search_results) == 0:
            # 没找到任何相关结果，可能是幻觉
            result.add_problem(sentence, position, "未搜索到相关公开信息支撑该说法", 3.0)
            explain.set_score("来源匹配度", explain.dimension_scores["来源匹配度"] - 1)
            result.add_suggestion(f"句子「{sentence[:30]}...」未找到公开信息支撑，建议核实")
            return
        
        # 简单匹配：检查句子关键词是否出现在搜索结果摘要中
        # 更复杂算法可以后续迭代优化
        keywords = [w for w in sentence.split() if len(w) > 2]
        match_count = 0
        for kw in keywords:
            for res in search_results:
                if kw in res.get("snippet", "") or kw in res.get("title", ""):
                    match_count += 1
                    break
        
        if len(keywords) > 0:
            match_ratio = match_count / len(keywords)
            score = 10 * match_ratio
            explain.set_score("来源匹配度", score)
            
            if match_ratio < 0.3:
                result.add_problem(sentence, position, f"关键词匹配度低 ({match_ratio:.1%})，与公开信息不一致", score)
    
    def _check_logical_consistency(self, sentences: List[str], result: CheckResult, explain: ConfidenceExplain):
        """检查逻辑一致性，简单版本检测矛盾"""
        # TODO: 更复杂的矛盾检测可以后续优化
        # 这里只做简单的数字冲突检测占位
        score = 8.0
        explain.set_score("逻辑一致性", score)
    
    def _check_clarity(self, text: str, sentences: List[str], result: CheckResult, explain: ConfidenceExplain):
        """检查信息明确性，检测模糊表述"""
        vague_words = ["可能", "大概", "也许", "据说", "听说", "有人说", "很多人"]
        vague_count = 0
        for word in vague_words:
            vague_count += text.count(word)
        
        if vague_count == 0:
            score = 10.0
        elif vague_count <= 2:
            score = 7.0
        else:
            score = 4.0
            result.add_suggestion("文本存在较多模糊表述，建议增加具体信息提升可信度")
        
        explain.set_score("信息明确性", score)
    
    def _check_common_sense(self, sentence: str, result: CheckResult, explain: ConfidenceExplain):
        """常识符合度检查，占位，可扩展"""
        # 简单实现，可以后续加入常识库
        explain.set_score("常识符合度", 8.0)
    
    def _generate_explanation(self, result: CheckResult):
        """生成总体解释文本"""
        explain = result.confidence_explanation
        dims = explain.dimension_scores
        text = f"本次核查在各维度得分："
        for dim, score in dims.items():
            text += f"{dim} {score:.1f}分，"
        text += f"最终加权得分为{result.credibility_score:.1f}分。"
        text += f"模型对本次核查结论的元认知置信度为{result.meta_confidence:.1f}%。"
        text += f"共发现{len(result.problematic_sentences)}处可能存在问题的内容。"
        explain.overall_explanation = text
