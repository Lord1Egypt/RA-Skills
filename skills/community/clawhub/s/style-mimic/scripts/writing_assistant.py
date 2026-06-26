#!/usr/bin/env python3
"""
style-mimic 写作助手
帮助用户按照社会洞察类文章风格进行写作
"""

import argparse
import json
import os
import random
from pathlib import Path
from typing import Dict, List, Optional

class WritingAssistant:
    def __init__(self, skill_dir: Path):
        self.skill_dir = skill_dir
        self.templates_dir = skill_dir / "templates"
        self.examples_dir = skill_dir / "examples"
        self.references_dir = skill_dir / "references"
        
        # 加载模板
        self.templates = self._load_templates()
        
        # 常用句式库
        self.common_phrases = [
            "你觉得这公平吗？大多数人觉得不公平。但大多数人也觉得没办法。",
            "这篇文章要做三件事：第一... 第二... 第三...",
            "在没有路灯的夜晚... 现在灯亮了，他还攥着不放。",
            "不是... 而是...",
            "过去是... 现在是...",
            "表面上看... 实际上...",
            "短期来看... 长期来看...",
            "从技术层面... 从经济层面... 从社会层面...",
            "一方面... 另一方面...",
            "与其说... 不如说..."
        ]
        
        # 经典引用库
        self.classical_quotes = [
            "《道德经》有云：'道可道，非常道；名可名，非常名。'",
            "孔子曰：'学而不思则罔，思而不学则殆。'",
            "《庄子》云：'吾生也有涯，而知也无涯。'",
            "孟子说：'穷则独善其身，达则兼济天下。'",
            "《孙子兵法》：'知彼知己，百战不殆。'",
            "王阳明：'知行合一。'",
            "鲁迅：'地上本没有路，走的人多了，也便成了路。'",
            "《易经》：'天行健，君子以自强不息。'"
        ]
    
    def _load_templates(self) -> Dict[str, str]:
        """加载所有模板"""
        templates = {}
        if self.templates_dir.exists():
            for template_file in self.templates_dir.glob("*.md"):
                with open(template_file, 'r', encoding='utf-8') as f:
                    templates[template_file.stem] = f.read()
        return templates
    
    def list_templates(self) -> List[str]:
        """列出所有可用模板"""
        return list(self.templates.keys())
    
    def get_template(self, template_name: str) -> Optional[str]:
        """获取指定模板"""
        return self.templates.get(template_name)
    
    def generate_opening(self, topic: str, template_type: str = "analysis") -> str:
        """生成文章开头"""
        openings = {
            "analysis": [
                f"【强烈对比切入】一边是{topic}的蓬勃发展，一边是相关问题的日益凸显。",
                f"【现象切入】最近，{topic}成为热议焦点。表面繁荣背后，隐藏着怎样的结构性矛盾？",
                f"【问题切入】在{topic}日益普及的今天，我们是否真正理解了它的本质影响？"
            ],
            "commentary": [
                f"【热点切入】近期，{topic}引发广泛讨论。各方观点激烈碰撞，真相究竟如何？",
                f"【事件切入】{topic}事件持续发酵，折射出怎样的社会心态和价值冲突？",
                f"【现象切入】{topic}现象背后，是时代变迁的必然，还是发展失衡的警示？"
            ],
            "report": [
                f"【背景说明】随着{topic}的快速发展，相关研究日益重要。本报告旨在系统分析...",
                f"【现状描述】{topic}领域近年来呈现快速增长态势，但也面临诸多挑战...",
                f"【研究目的】本文通过对{topic}的深入研究，试图揭示其内在规律和发展趋势..."
            ]
        }
        
        return random.choice(openings.get(template_type, openings["analysis"]))
    
    def generate_closing(self, topic: str) -> str:
        """生成文章结尾"""
        quote = random.choice(self.classical_quotes)
        
        closings = [
            f"{quote} 古人的智慧，今日依然值得我们深思。",
            f"回到{topic}这个话题，现在我们有了更深入的理解。问题的关键不在于...",
            f"{topic}只是表象，真正考验我们的是...",
            f"在{topic}的讨论中，我们看到的不仅是技术或经济问题，更是..."
        ]
        
        return random.choice(closings)
    
    def suggest_structure(self, topic: str, article_type: str = "analysis") -> List[str]:
        """建议文章结构"""
        structures = {
            "analysis": [
                f"1. 定义核心概念：为{topic}创造准确的新概念",
                f"2. 建立分析框架：从多个维度剖析{topic}",
                f"3. 深入问题本质：揭示{topic}背后的结构性矛盾",
                f"4. 提出解决方案：针对{topic}的务实建议"
            ],
            "commentary": [
                f"1. 现象还原：客观描述{topic}的实际情况",
                f"2. 各方立场：梳理关于{topic}的不同观点",
                f"3. 深度剖析：分析{topic}反映的深层问题",
                f"4. 价值判断：明确对{topic}的基本立场",
                f"5. 建设建议：提出改进{topic}的具体措施"
            ],
            "report": [
                f"1. 现状描述：{topic}的基本情况和数据",
                f"2. 问题诊断：{topic}面临的主要挑战",
                f"3. 原因分析：{topic}问题的多维度原因",
                f"4. 趋势预测：{topic}的未来发展方向",
                f"5. 对策建议：推动{topic}健康发展的策略"
            ]
        }
        
        return structures.get(article_type, structures["analysis"])
    
    def get_common_phrase(self) -> str:
        """获取常用句式"""
        return random.choice(self.common_phrases)
    
    def analyze_style(self, text: str) -> Dict[str, float]:
        """分析文本风格特征（简化版）"""
        # 这里实现一个简化的风格分析
        # 实际应用中可以使用更复杂的NLP技术
        
        analysis = {
            "structure_score": 0.0,  # 结构清晰度
            "logic_score": 0.0,      # 逻辑严密性
            "data_score": 0.0,       # 数据支撑度
            "style_score": 0.0       # 风格匹配度
        }
        
        # 简单分析（实际应使用更复杂的算法）
        lines = text.split('\n')
        words = text.split()
        
        # 检查结构标记
        structure_indicators = ["首先", "其次", "最后", "第一", "第二", "第三", "一方面", "另一方面"]
        for indicator in structure_indicators:
            if indicator in text:
                analysis["structure_score"] += 0.1
        
        # 检查数据引用
        data_indicators = ["%", "数据", "统计", "调查", "研究显示", "据统计"]
        for indicator in data_indicators:
            if indicator in text:
                analysis["data_score"] += 0.15
        
        # 检查逻辑连接词
        logic_indicators = ["因为", "所以", "因此", "然而", "但是", "尽管", "如果", "那么"]
        for indicator in logic_indicators:
            if indicator in text:
                analysis["logic_score"] += 0.1
        
        # 检查风格特征词
        style_indicators = ["框架", "坐标系", "结构性", "本质", "现象", "原因", "解决方案"]
        for indicator in style_indicators:
            if indicator in text:
                analysis["style_score"] += 0.1
        
        # 限制分数在0-1之间
        for key in analysis:
            analysis[key] = min(1.0, analysis[key])
        
        return analysis
    
    def generate_improvement_suggestions(self, analysis: Dict[str, float]) -> List[str]:
        """根据分析结果生成改进建议"""
        suggestions = []
        
        if analysis["structure_score"] < 0.3:
            suggestions.append("建议加强文章结构，使用'第一、第二、第三'或'首先、其次、最后'等结构标记")
        
        if analysis["logic_score"] < 0.3:
            suggestions.append("建议增强逻辑连接，使用'因为...所以...'、'然而...'、'因此...'等逻辑词")
        
        if analysis["data_score"] < 0.3:
            suggestions.append("建议增加数据支撑，引用具体数字、调查结果或研究数据")
        
        if analysis["style_score"] < 0.3:
            suggestions.append("建议强化风格特征，使用'框架分析'、'结构性矛盾'、'本质探讨'等典型表述")
        
        if not suggestions:
            suggestions.append("文章风格基本符合要求，继续保持！")
        
        return suggestions

def main():
    parser = argparse.ArgumentParser(description="style-mimic 写作助手")
    parser.add_argument("--topic", help="文章主题")
    parser.add_argument("--type", choices=["analysis", "commentary", "report"], 
                       default="analysis", help="文章类型")
    parser.add_argument("--action", choices=["opening", "closing", "structure", 
                                           "phrase", "analyze", "suggest"],
                       default="structure", help="执行的操作")
    parser.add_argument("--text", help="需要分析的文本（用于analyze操作）")
    parser.add_argument("--list-templates", action="store_true", 
                       help="列出所有可用模板")
    
    args = parser.parse_args()
    
    # 初始化助手
    skill_dir = Path(__file__).parent.parent
    assistant = WritingAssistant(skill_dir)
    
    if args.list_templates:
        print("可用模板:")
        for template in assistant.list_templates():
            print(f"  - {template}")
        return
    
    if args.action == "opening" and args.topic:
        opening = assistant.generate_opening(args.topic, args.type)
        print("文章开头建议:")
        print(opening)
    
    elif args.action == "closing" and args.topic:
        closing = assistant.generate_closing(args.topic)
        print("文章结尾建议:")
        print(closing)
    
    elif args.action == "structure" and args.topic:
        structure = assistant.suggest_structure(args.topic, args.type)
        print("文章结构建议:")
        for item in structure:
            print(f"  • {item}")
    
    elif args.action == "phrase":
        phrase = assistant.get_common_phrase()
        print("常用句式:")
        print(phrase)
    
    elif args.action == "analyze" and args.text:
        analysis = assistant.analyze_style(args.text)
        print("风格分析结果:")
        for key, value in analysis.items():
            print(f"  {key}: {value:.2f}")
    
    elif args.action == "suggest" and args.text:
        analysis = assistant.analyze_style(args.text)
        suggestions = assistant.generate_improvement_suggestions(analysis)
        print("改进建议:")
        for suggestion in suggestions:
            print(f"  • {suggestion}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()