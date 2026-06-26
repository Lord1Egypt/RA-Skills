"""
报告生成模块
"""

import json
from datetime import datetime
from typing import Dict


class ReportGenerator:
    """分析报告生成器"""

    def generate(
        self,
        title: str,
        article_type: str,
        type_confidence: float,
        overall_score: int,
        grade: str,
        reading_advice: Dict,
        dimension_scores: Dict,
        ai_detection: Dict,
        analysis_details: Dict
    ) -> Dict:
        """
        生成完整分析报告

        Returns:
            报告字典 (JSON格式)
        """
        report_id = f"taster_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        return {
            "report_id": report_id,
            "title": title,
            "type": article_type,
            "type_confidence": type_confidence,
            "overall_score": overall_score,
            "grade": grade,
            "reading_advice": reading_advice,
            "dimension_scores": dimension_scores,
            "ai_detection": ai_detection,
            "detailed_analysis": analysis_details,
            "timestamp": datetime.now().isoformat() + "Z"
        }

    def to_markdown(self, report: Dict) -> str:
        """生成 Markdown 格式报告"""
        verdict = report['reading_advice']['verdict']
        grade = report['grade']
        score = report['overall_score']

        # 等级emoji
        grade_emoji = {
            "A+": "💎", "A": "⭐", "B+": "👍", "B": "👌",
            "C": "🤔", "D": "👎"
        }.get(grade, "📄")

        md = f"""# 文章品鉴报告

## 基本信息

- **标题**: {report['title']}
- **类型**: {self._type_name(report['type'])} (置信度: {report['type_confidence']:.0%})
- **评分**: {score}分 ({grade}) {grade_emoji}
- **分析时间**: {report['timestamp']}

---

## 综合评价

### {verdict}

**目标读者**: {report['reading_advice']['target_audience']}
**预计阅读时间**: {report['reading_advice']['time_estimation']}

---

## 维度评分

| 维度 | 得分 | 权重 |
|------|------|------|
"""
        for dim, info in report['dimension_scores'].items():
            dim_name = self._dim_name(dim)
            score_bar = self._score_bar(info['score'])
            md += f"| {dim_name} | {score_bar} {info['score']:.0f} | {info.get('weight', 0):.0%} |\n"

        md += f"""
---

## AI检测结果

"""

        ai_result = report['ai_detection']
        ai_level = ai_result.get('confidence_label', '未知')

        if ai_result.get('exemption_type'):
            exemption_name = {
                'classical_poetry': '古诗词',
                'classic_literature': '经典文学'
            }.get(ai_result['exemption_type'], '原创')
            md += f"- **豁免类型**: {exemption_name} (置信度: {ai_result.get('exemption_confidence', 0):.0%})\n"
        else:
            md += f"- **AI生成概率**: {ai_result['ai_probability']:.0%}\n"

        md += f"""- **结论**: {ai_level}
- **原创评分**: {ai_result.get('originality_score', 'N/A')}/100

"""

        # 阅读建议
        md += """## 阅读建议

**核心价值:**
"""
        for benefit in report['reading_advice'].get('key_benefits', []):
            md += f"- {benefit}\n"

        md += """
**适合阅读场景:**
"""
        for moment in report['reading_advice'].get('suitable_moments', []):
            md += f"- {moment}\n"

        # 详细分析 (如果有)
        if report.get('detailed_analysis'):
            details = report['detailed_analysis']

            # 情感曲线
            if 'emotional_curve' in details:
                curve = details['emotional_curve']
                md += f"""
---

## 情感曲线分析

- **曲线类型**: {curve.get('arc_type', '未知')}
- **描述**: {curve.get('description', '无')}
- **高潮位置**: 全文{int(curve.get('peak_position', 0.5) * 100)}%处
"""

            # 优点/改进
            if 'strengths' in details and details['strengths']:
                md += """
---

## 文章优点

"""
                for s in details['strengths']:
                    md += f"- {s}\n"

            if 'improvements' in details and details['improvements']:
                md += """
---

## 改进建议

"""
                for i in details['improvements']:
                    md += f"- {i}\n"

        md += """

---

*由 Article Taster 自动生成*
"""
        return md

    def _type_name(self, type_code: str) -> str:
        names = {
            "technical_article": "技术文章",
            "essay": "情感散文",
            "novel": "小说",
            "other": "其他文章"
        }
        return names.get(type_code, type_code)

    def _dim_name(self, dim_code: str) -> str:
        names = {
            "technical_depth": "技术深度",
            "structure": "结构清晰度",
            "practicality": "实用性",
            "originality": "原创性",
            "readability": "可读性",
            "emotion_expression": "情感表达",
            "writing_style": "文笔水平",
            "narrative_structure": "叙事结构",
            "creativity": "创意性",
            "resonance": "共鸣度",
            "plot_structure": "情节结构",
            "character_craft": "人物塑造",
            "narrative_technique": "叙事技巧",
            "style_features": "文风特点",
            "world_building": "世界观构建",
            "content_depth": "内容深度",
            "accuracy": "准确性",
            "depth": "深度",
            "learning_value": "学习价值",
            "information_density": "信息密度"
        }
        return names.get(dim_code, dim_code)

    def _score_bar(self, score: float, length: int = 10) -> str:
        """生成评分条"""
        filled = int(score / 10)
        empty = length - filled
        return "█" * filled + "░" * empty

    def to_json_string(self, report: Dict, indent: int = 2) -> str:
        """生成格式化的JSON字符串"""
        return json.dumps(report, indent=indent, ensure_ascii=False)


if __name__ == "__main__":
    # 测试报告生成
    generator = ReportGenerator()

    sample_report = {
        "report_id": "taster_test",
        "title": "测试文章",
        "type": "technical_article",
        "type_confidence": 0.85,
        "overall_score": 82,
        "grade": "A",
        "reading_advice": {
            "verdict": "强烈推荐！内容扎实，适合认真阅读",
            "target_audience": "初中级开发者",
            "time_estimation": "10分钟",
            "key_benefits": ["深入浅出的架构设计", "实操性强"],
            "suitable_moments": ["专注阅读", "深度学习"]
        },
        "dimension_scores": {
            "technical_depth": {"score": 85, "weight": 0.30},
            "structure": {"score": 80, "weight": 0.25},
            "practicality": {"score": 82, "weight": 0.20},
            "originality": {"score": 78, "weight": 0.15},
            "readability": {"score": 80, "weight": 0.10}
        },
        "ai_detection": {
            "ai_probability": 0.15,
            "is_ai_generated": False,
            "confidence_label": "高度可信原创",
            "originality_score": 85,
            "exemption_type": None
        },
        "detailed_analysis": {
            "strengths": ["技术深度好", "有代码示例"],
            "improvements": ["可以增加更多实战案例"]
        },
        "timestamp": "2026-04-08T10:00:00Z"
    }

    print(generator.to_markdown(sample_report))
