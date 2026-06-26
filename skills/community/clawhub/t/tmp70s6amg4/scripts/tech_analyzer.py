"""
M2-T: 技术文章分析模块
评估: 技术深度、结构清晰度、实用性、原创性、可读性
"""

from typing import Dict
import re


class TechAnalyzer:
    """技术文章质量分析器"""

    TECH_TERMS = [
        "实现", "架构", "设计", "模块", "接口", "数据", "处理",
        "算法", "性能", "优化", "配置", "部署", "测试", "调试",
        "函数", "类", "对象", "变量", "方法", "调用", "返回",
        "数据库", "SQL", "API", "HTTP", "网络", "协议", "安全"
    ]

    ORIGINALITY_INDICATORS = [
        "实测", "踩坑", "经验", "总结", "原创", "个人看法",
        "实践证明", "经过验证", "血泪史", "心得"
    ]

    PLAGIARISM_INDICATORS = [
        "转载", "来源", "transfer", "from", "摘录", "整理自",
        "翻译自", "according to", "转载自"
    ]

    def __init__(self):
        self.dimension_weights = {
            "technical_depth": 0.30,
            "structure": 0.25,
            "practicality": 0.20,
            "originality": 0.15,
            "readability": 0.10
        }

    def analyze(self, title: str, content: str) -> Dict:
        """
        分析技术文章质量

        Returns:
            维度得分字典 + 详细分析
        """
        text = f"{title} {content}"
        scores = {}

        # 1. 技术深度 (30%)
        scores["technical_depth"] = self._calc_technical_depth(content)

        # 2. 结构清晰度 (25%)
        scores["structure"] = self._calc_structure_score(content)

        # 3. 实用性 (20%)
        scores["practicality"] = self._calc_practicality(content)

        # 4. 原创性 (15%)
        scores["originality"] = self._calc_originality(content, text)

        # 5. 可读性 (10%)
        scores["readability"] = self._calc_readability(content)

        return {
            "dimension_scores": scores,
            "weights": self.dimension_weights,
            "indicators": {
                "code_blocks": content.count("```"),
                "heading_count": len(re.findall(r"\n#{1,4}\s", content)),
                "term_density": self._calc_term_density(content),
                "paragraph_count": len([p for p in content.split("\n\n") if p.strip()]),
                "step_indicators": self._count_steps(content),
                "originality_score": scores["originality"],
                "avg_sentence_length": self._avg_sentence_length(content)
            },
            "issues": self._identify_issues(content, scores),
            "strengths": self._identify_strengths(content, scores)
        }

    def _calc_technical_depth(self, content: str) -> float:
        """计算技术深度得分"""
        term_density = self._calc_term_density(content)
        paragraph_count = len([p for p in content.split("\n\n") if p.strip()])
        code_blocks = content.count("```")

        depth = term_density * 15 + paragraph_count * 1.5 + code_blocks * 8
        return min(100, max(20, depth))

    def _calc_structure_score(self, content: str) -> float:
        """计算结构清晰度得分"""
        heading_count = len(re.findall(r"\n#{1,4}\s", content))
        list_items = len(re.findall(r"^\s*[-*+]\s|\d+\.", content, re.MULTILINE))
        code_blocks = content.count("```")

        structure = 50 + heading_count * 5 + list_items * 3 + code_blocks * 5
        return min(100, structure)

    def _calc_practicality(self, content: str) -> float:
        """计算实用性得分"""
        step_indicators = self._count_steps(content)
        code_blocks = content.count("```")
        command_indicators = content.count("$ ") + content.count(">>> ")

        practicality = 40 + step_indicators * 8 + code_blocks * 6 + command_indicators * 5
        return min(100, practicality)

    def _calc_originality(self, content: str, text: str) -> float:
        """计算原创性得分"""
        originality_indicators = sum(
            text.count(indicator) for indicator in self.ORIGINALITY_INDICATORS
        )
        plagiarism_indicators = sum(
            content.count(indicator) for indicator in self.PLAGIARISM_INDICATORS
        )

        plagiarism_penalty = plagiarism_indicators * 15
        originality_bonus = originality_indicators * 8

        unique_ratio = len(set(content)) / max(len(content), 1)
        uniqueness = unique_ratio * 40

        score = 55 + originality_bonus + uniqueness - plagiarism_penalty
        return min(100, max(0, score))

    def _calc_readability(self, content: str) -> float:
        """计算可读性得分"""
        avg_len = self._avg_sentence_length(content)
        punctuation_diversity = self._calc_punctuation_diversity(content)

        readability = 100 - abs(avg_len - 18) * 2 + punctuation_diversity * 10
        return min(100, max(0, readability))

    def _calc_term_density(self, content: str) -> float:
        """计算技术术语密度"""
        text_len = len(content)
        if text_len == 0:
            return 0
        term_count = sum(content.count(t) for t in self.TECH_TERMS)
        return term_count / (text_len / 1000)

    def _count_steps(self, content: str) -> int:
        """统计步骤指示器数量"""
        patterns = [
            r"第一步|第二步|第三步|第四步",
            r"步骤\d+",
            r"\d+\.\s+[先然后再]",
            r"首先|其次|最后",
            r"step\s*\d+|Step\s*\d+"
        ]
        return sum(len(re.findall(p, content, re.IGNORECASE)) for p in patterns)

    def _avg_sentence_length(self, content: str) -> float:
        """计算平均句子长度"""
        sentences = re.split(r"[.!?。！？]", content)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return 0
        return sum(len(s) for s in sentences) / len(sentences)

    def _calc_punctuation_diversity(self, content: str) -> float:
        """计算标点多样性"""
        puncts = ".,!?;:'\"-()[]{}"
        unique_puncts = sum(1 for p in puncts if p in content)
        return unique_puncts / len(puncts) * 100

    def _identify_issues(self, content: str, scores: Dict) -> list:
        """识别文章问题"""
        issues = []
        if scores["structure"] < 50:
            issues.append("结构不够清晰，建议增加标题层级和列表")
        if scores["practicality"] < 50:
            issues.append("缺少实际可操作的步骤或代码示例")
        if scores["originality"] < 50:
            issues.append("原创性有待提升，建议增加个人经验总结")
        if self._avg_sentence_length(content) > 40:
            issues.append("句子过长，建议适当拆分提高可读性")
        if content.count("```") == 0:
            issues.append("建议增加代码示例辅助理解")
        return issues

    def _identify_strengths(self, content: str, scores: Dict) -> list:
        """识别文章优点"""
        strengths = []
        if scores["technical_depth"] >= 70:
            strengths.append("技术内容深入，有原理分析")
        if scores["structure"] >= 70:
            strengths.append("结构清晰，层次分明")
        if scores["practicality"] >= 70:
            strengths.append("包含可复用的代码或步骤")
        if scores["originality"] >= 70:
            strengths.append("有原创观点和实战经验")
        return strengths


if __name__ == "__main__":
    analyzer = TechAnalyzer()

    test_content = """
    # Python异步编程实战

    ## 什么是异步编程

    异步编程是一种并发编程模式，相比传统的同步编程...

    ## 核心技术: async/await

    Python 3.5 引入了 async/await 关键字...

    ```python
    async def fetch_data(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
    ```

    ## 步骤指南

    1. 首先安装 aiohttp
    2. 然后创建异步函数
    3. 最后使用 asyncio.run() 运行
    """

    result = analyzer.analyze("Python异步编程实战", test_content)
    print("技术文章分析结果:")
    for dim, score in result["dimension_scores"].items():
        print(f"  {dim}: {score:.1f}")
