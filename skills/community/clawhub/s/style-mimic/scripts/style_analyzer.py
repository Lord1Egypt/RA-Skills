#!/usr/bin/env python3
"""
style-mimic 风格检测工具
分析文本是否符合社会洞察类文章风格
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple

class StyleAnalyzer:
    def __init__(self):
        # 风格特征词库
        self.style_features = {
            "structural_thinking": [
                "框架", "坐标系", "模型", "结构", "体系", "系统",
                "维度", "层面", "角度", "视角", "范式"
            ],
            "concept_innovation": [
                "新概念", "重新定义", "本质是", "实际上是", "本质上",
                "重新理解", "新范式", "新思维", "新视角"
            ],
            "binary_opposition": [
                "不是...而是...", "表面...实际...", "理想...现实...",
                "形式...实质...", "短期...长期...", "局部...整体..."
            ],
            "progressive_argument": [
                "首先", "其次", "最后", "第一", "第二", "第三",
                "一方面", "另一方面", "不仅如此", "更进一步"
            ],
            "data_support": [
                "数据", "统计", "调查", "研究", "显示", "表明",
                "%", "比例", "增长率", "市场规模", "用户规模"
            ],
            "case_reference": [
                "例如", "比如", "典型案例", "具体来说", "以...为例",
                "案例", "实例", "实际情况"
            ],
            "classical_quotation": [
                "《", "》", "曰", "云", "有云", "说道", "曾说",
                "古人", "经典", "名言", "格言"
            ],
            "critical_tone": [
                "问题", "矛盾", "困境", "挑战", "危机", "弊端",
                "不足", "缺陷", "局限性", "需要改进"
            ],
            "constructive_suggestion": [
                "建议", "方案", "对策", "措施", "方法", "路径",
                "策略", "改进", "优化", "提升", "解决"
            ]
        }
        
        # 优秀句式模式
        self.excellent_patterns = [
            r"你觉得[\u4e00-\u9fa5]+吗？",
            r"这篇文章要做[\u4e00-\u9fa5]+件事",
            r"不是[\u4e00-\u9fa5]+而是[\u4e00-\u9fa5]+",
            r"过去是[\u4e00-\u9fa5]+现在是[\u4e00-\u9fa5]+",
            r"表面上看[\u4e00-\u9fa5]+实际上[\u4e00-\u9fa5]+",
            r"从[\u4e00-\u9fa5]+层面看[\u4e00-\u9fa5]+",
            r"短期[\u4e00-\u9fa5]+长期[\u4e00-\u9fa5]+"
        ]
    
    def analyze_text(self, text: str) -> Dict[str, Dict]:
        """全面分析文本风格"""
        results = {
            "feature_scores": {},
            "pattern_matches": [],
            "overall_score": 0.0,
            "strengths": [],
            "weaknesses": []
        }
        
        # 分析每个风格特征
        total_features = 0
        matched_features = 0
        
        for feature_name, keywords in self.style_features.items():
            score = self._calculate_feature_score(text, keywords)
            results["feature_scores"][feature_name] = score
            
            if score > 0:
                matched_features += 1
            total_features += 1
        
        # 检查优秀句式
        for pattern in self.excellent_patterns:
            matches = re.findall(pattern, text)
            if matches:
                results["pattern_matches"].extend(matches)
        
        # 计算总体分数
        feature_score = matched_features / total_features if total_features > 0 else 0
        pattern_score = min(1.0, len(results["pattern_matches"]) / 5)  # 最多5个优秀句式
        results["overall_score"] = (feature_score * 0.7 + pattern_score * 0.3)
        
        # 识别优点和不足
        results["strengths"] = self._identify_strengths(results["feature_scores"])
        results["weaknesses"] = self._identify_weaknesses(results["feature_scores"])
        
        return results
    
    def _calculate_feature_score(self, text: str, keywords: List[str]) -> float:
        """计算单个特征的得分"""
        if not keywords:
            return 0.0
        
        matches = 0
        for keyword in keywords:
            if keyword in text:
                matches += 1
        
        return min(1.0, matches / len(keywords))
    
    def _identify_strengths(self, feature_scores: Dict[str, float]) -> List[str]:
        """识别优点"""
        strengths = []
        feature_names = {
            "structural_thinking": "结构化思维",
            "concept_innovation": "概念创新",
            "binary_opposition": "二元对立分析",
            "progressive_argument": "递进论证",
            "data_support": "数据支撑",
            "case_reference": "案例引用",
            "classical_quotation": "经典引用",
            "critical_tone": "批判性思维",
            "constructive_suggestion": "建设性建议"
        }
        
        for feature, score in feature_scores.items():
            if score >= 0.5:  # 得分超过0.5认为是优点
                strengths.append(feature_names.get(feature, feature))
        
        return strengths
    
    def _identify_weaknesses(self, feature_scores: Dict[str, float]) -> List[str]:
        """识别不足"""
        weaknesses = []
        feature_names = {
            "structural_thinking": "结构化思维",
            "concept_innovation": "概念创新",
            "binary_opposition": "二元对立分析",
            "progressive_argument": "递进论证",
            "data_support": "数据支撑",
            "case_reference": "案例引用",
            "classical_quotation": "经典引用",
            "critical_tone": "批判性思维",
            "constructive_suggestion": "建设性建议"
        }
        
        for feature, score in feature_scores.items():
            if score < 0.2:  # 得分低于0.2认为是不足
                weaknesses.append(feature_names.get(feature, feature))
        
        return weaknesses
    
    def generate_detailed_report(self, analysis_results: Dict[str, Dict]) -> str:
        """生成详细分析报告"""
        report = []
        report.append("=" * 60)
        report.append("style-mimic 风格分析报告")
        report.append("=" * 60)
        
        # 总体评分
        overall_score = analysis_results["overall_score"]
        report.append(f"\n📊 总体评分: {overall_score:.2f}/1.0")
        
        if overall_score >= 0.7:
            report.append("   ✅ 优秀：文章风格高度符合社会洞察类特征")
        elif overall_score >= 0.5:
            report.append("   👍 良好：文章风格基本符合要求")
        elif overall_score >= 0.3:
            report.append("   ⚠️  一般：部分风格特征需要加强")
        else:
            report.append("   ❌ 待改进：需要大幅提升风格匹配度")
        
        # 特征得分
        report.append("\n🔍 特征分析:")
        for feature, score in analysis_results["feature_scores"].items():
            feature_name = {
                "structural_thinking": "结构化思维",
                "concept_innovation": "概念创新", 
                "binary_opposition": "二元对立",
                "progressive_argument": "递进论证",
                "data_support": "数据支撑",
                "case_reference": "案例引用",
                "classical_quotation": "经典引用",
                "critical_tone": "批判性思维",
                "constructive_suggestion": "建设性建议"
            }.get(feature, feature)
            
            bar = "█" * int(score * 20) + " " * (20 - int(score * 20))
            report.append(f"   {feature_name:15s} [{bar}] {score:.2f}")
        
        # 优秀句式匹配
        if analysis_results["pattern_matches"]:
            report.append(f"\n💎 优秀句式匹配 ({len(analysis_results['pattern_matches'])}个):")
            for i, pattern in enumerate(analysis_results["pattern_matches"][:5], 1):
                report.append(f"   {i}. {pattern}")
        
        # 优点
        if analysis_results["strengths"]:
            report.append(f"\n✅ 优点 ({len(analysis_results['strengths'])}个):")
            for strength in analysis_results["strengths"]:
                report.append(f"   • {strength}")
        
        # 不足
        if analysis_results["weaknesses"]:
            report.append(f"\n⚠️  待改进 ({len(analysis_results['weaknesses'])}个):")
            for weakness in analysis_results["weaknesses"]:
                report.append(f"   • {weakness}")
        
        # 改进建议
        report.append("\n💡 改进建议:")
        if analysis_results["weaknesses"]:
            for weakness in analysis_results["weaknesses"]:
                suggestion = self._get_suggestion_for_weakness(weakness)
                report.append(f"   • {suggestion}")
        else:
            report.append("   • 继续保持现有风格，可尝试更多创新表达")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)
    
    def _get_suggestion_for_weakness(self, weakness: str) -> str:
        """根据不足提供具体建议"""
        suggestions = {
            "结构化思维": "尝试使用'框架分析'、'多维度视角'、'系统思考'等表述",
            "概念创新": "创造新概念来准确定义现象，如'知识肥胖症'、'信息过载症'",
            "二元对立分析": "使用'不是...而是...'、'表面...实际...'等对比句式",
            "递进论证": "使用'首先、其次、最后'或'第一、第二、第三'等结构标记",
            "数据支撑": "引用具体数据，如'70%的用户...'、'市场规模达到...'",
            "案例引用": "添加具体案例，如'以张伟为例...'、'典型案例是...'",
            "经典引用": "适当引用古籍名言，如'《道德经》有云...'、'孔子曰...'",
            "批判性思维": "直指问题核心，如'问题的关键在于...'、'结构性矛盾在于...'",
            "建设性建议": "提出具体解决方案，分'短期、中期、长期'建议"
        }
        
        return suggestions.get(weakness, f"加强{weakness}方面的表达")

def main():
    parser = argparse.ArgumentParser(description="style-mimic 风格检测工具")
    parser.add_argument("--text", help="需要分析的文本")
    parser.add_argument("--file", help="包含文本的文件路径")
    parser.add_argument("--output", choices=["brief", "detailed"], 
                       default="detailed", help="输出格式")
    
    args = parser.parse_args()
    
    # 获取文本
    text = ""
    if args.text:
        text = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"错误：文件 '{args.file}' 不存在")
            return
    else:
        parser.print_help()
        return
    
    if not text.strip():
        print("错误：文本内容为空")
        return
    
    # 分析文本
    analyzer = StyleAnalyzer()
    results = analyzer.analyze_text(text)
    
    # 输出结果
    if args.output == "brief":
        print(f"风格匹配度: {results['overall_score']:.2f}/1.0")
        print(f"优点: {', '.join(results['strengths']) if results['strengths'] else '无'}")
        print(f"不足: {', '.join(results['weaknesses']) if results['weaknesses'] else '无'}")
    else:
        report = analyzer.generate_detailed_report(results)
        print(report)

if __name__ == "__main__":
    main()