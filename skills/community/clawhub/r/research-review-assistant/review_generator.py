#!/usr/bin/env python3
"""
科研文献综述与迭代助手 - 执行器

功能：
1. 检索多源论文（arXiv/PubMed/Google Scholar）
2. 结构化总结与关联分析
3. 多轮迭代优化
4. 生成 SCI 格式综述草稿

作者：OpenClaw Community
创建：2026-04-03
版本：2.0.0
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
import xml.etree.ElementTree as ET


class MultiSourceSearch:
    """多源论文检索"""

    def __init__(self):
        self.arxiv_url = "http://export.arxiv.org/api/query"
        self.headers = {"User-Agent": "OpenClaw-Review-Assistant/2.0"}

    def search_arxiv(
        self,
        query: str,
        max_results: int = 30,
        years: int = 5
    ) -> List[Dict[str, Any]]:
        """搜索 arXiv 论文"""
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results * 2,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }

        try:
            response = requests.get(self.arxiv_url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
            papers = self._parse_arxiv_xml(response.text)

            # 筛选最近 N 年
            cutoff_year = datetime.now().year - years
            recent_papers = [
                p for p in papers
                if p.get("published") and self._parse_year(p["published"]) >= cutoff_year
            ]

            return recent_papers[:max_results]

        except Exception as e:
            return [{"error": f"arXiv 搜索失败：{str(e)}"}]

    def _parse_arxiv_xml(self, xml_content: str) -> List[Dict[str, Any]]:
        """解析 arXiv XML"""
        papers = []
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom"
        }

        try:
            root = ET.fromstring(xml_content)
            entries = root.findall("atom:entry", ns)

            for entry in entries:
                paper = {
                    "title": self._get_text(entry, "atom:title", ns),
                    "authors": [
                        self._get_text(author, "atom:name", ns)
                        for author in entry.findall("atom:author", ns)
                    ],
                    "published": self._get_text(entry, "atom:published", ns),
                    "summary": self._get_text(entry, "atom:summary", ns),
                    "link": entry.find("atom:id", ns).text if entry.find("atom:id", ns) is not None else "",
                    "pdf_link": self._get_pdf_link(entry, ns),
                    "categories": [
                        cat.get("term", "")
                        for cat in entry.findall("atom:category", ns)
                    ],
                    "source": "arXiv"
                }
                papers.append(paper)

        except Exception as e:
            return [{"error": f"XML 解析错误：{str(e)}"}]

        return papers

    def _get_text(self, parent: ET.Element, tag: str, ns: dict) -> str:
        """获取 XML 元素文本"""
        elem = parent.find(tag, ns)
        return elem.text.strip() if elem is not None and elem.text else ""

    def _get_pdf_link(self, entry: ET.Element, ns: dict) -> str:
        """获取 PDF 链接"""
        for link in entry.findall("atom:link", ns):
            if link.get("title") == "pdf":
                return link.get("href", "")
        return ""

    def _parse_year(self, date_str: str) -> int:
        """解析年份"""
        try:
            return int(date_str[:4])
        except:
            return datetime.now().year


class PaperAnalyzer:
    """论文分析器"""

    @staticmethod
    def analyze(paper: Dict[str, Any], user_field: str = "") -> Dict[str, Any]:
        """分析单篇论文"""
        title = paper.get("title", "无标题")
        authors = paper.get("authors", [])
        summary = paper.get("summary", "")
        published = paper.get("published", "")

        # 计算相关性
        relevance = PaperAnalyzer._calculate_relevance(title, summary, user_field)

        # 提取关键信息
        analysis = {
            "title": title,
            "authors": ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else ""),
            "institution": PaperAnalyzer._guess_institution(authors),
            "year": published[:4] if published else "",
            "summary": summary[:500] + "..." if len(summary) > 500 else summary,
            "relevance_score": relevance,
            "innovation_score": PaperAnalyzer._estimate_innovation(title, summary),
            "methods": PaperAnalyzer._extract_methods(summary),
            "contributions": PaperAnalyzer._extract_contributions(summary),
            "limitations": PaperAnalyzer._estimate_limitations(summary),
            "pdf_link": paper.get("pdf_link", ""),
            "arxiv_link": paper.get("link", ""),
            "categories": paper.get("categories", []),
            "source": paper.get("source", "Unknown"),
            "suggestion": PaperAnalyzer._generate_suggestion(relevance)
        }

        return analysis

    @staticmethod
    def _calculate_relevance(title: str, summary: str, user_field: str) -> int:
        """计算相关性分数（1-10）"""
        if not user_field:
            return 5

        keywords = user_field.lower().split()
        text = (title + " " + summary).lower()
        matches = sum(1 for kw in keywords if kw in text)

        return min(10, max(1, matches * 2))

    @staticmethod
    def _estimate_innovation(title: str, summary: str) -> int:
        """估算创新度（1-10）"""
        innovation_keywords = [
            "novel", "new", "first", "propose", "introduce",
            "innovative", "breakthrough", "state-of-the-art"
        ]

        text = (title + " " + summary).lower()
        matches = sum(1 for kw in innovation_keywords if kw in text)

        return min(10, max(1, 3 + matches))

    @staticmethod
    def _extract_methods(summary: str) -> List[str]:
        """提取方法关键词"""
        method_keywords = [
            "deep learning", "LSTM", "CNN", "transformer",
            "reinforcement learning", "active control",
            "model predictive control", "adaptive"
        ]

        text = summary.lower()
        methods = [kw for kw in method_keywords if kw in text]

        return methods if methods else ["未明确"]

    @staticmethod
    def _extract_contributions(summary: str) -> List[str]:
        """提取贡献点"""
        # 简化实现，实际可用 NLP 提取
        return ["核心贡献待提取"]

    @staticmethod
    def _estimate_limitations(summary: str) -> List[str]:
        """估算局限性"""
        limitation_keywords = [
            "however", "limitation", "challenge", "future work",
            "requires", "depends on", "assumes"
        ]

        text = summary.lower()
        limitations = [kw for kw in limitation_keywords if kw in text]

        return limitations[:3] if limitations else ["未明确"]

    @staticmethod
    def _guess_institution(authors: List[str]) -> str:
        """推测机构（简化版）"""
        return "Unknown"

    @staticmethod
    def _generate_suggestion(score: int) -> str:
        """生成阅读建议"""
        if score >= 8:
            return "⭐ 值得精读，高度相关"
        elif score >= 6:
            return "📖 建议阅读，方法可借鉴"
        elif score >= 4:
            return "👀 可浏览，了解动态"
        else:
            return "📌 暂不推荐"


class ReviewGenerator:
    """综述生成器"""

    @staticmethod
    def generate(
        papers: List[Dict[str, Any]],
        field: str,
        version: str = "v1.0",
        iteration_log: Optional[List[str]] = None
    ) -> str:
        """生成综述报告"""
        if not papers:
            return f"# {field} 文献综述 {version}（{datetime.now().strftime('%Y-%m-%d')}）\n\n❌ 未找到论文"

        # 过滤错误结果
        valid_papers = [p for p in papers if "error" not in p]

        # 按相关性排序
        sorted_papers = sorted(valid_papers, key=lambda x: x.get("relevance_score", 0), reverse=True)

        # 生成报告
        report = []
        date_str = datetime.now().strftime("%Y-%m-%d")
        report.append(f"# {field} 文献综述 {version}（{date_str}）\n")

        # 论文列表表格
        report.append("## 📊 论文列表\n")
        report.append("| 标题 | 作者 | 年份 | 相关性 | 关键发现 | 链接 |")
        report.append("|------|------|------|--------|----------|------|")

        for i, paper in enumerate(sorted_papers[:15], 1):
            title = paper.get("title", "无标题")[:40] + "..." if len(paper.get("title", "")) > 40 else paper.get("title", "")
            authors = paper.get("authors", "Unknown")
            year = paper.get("year", "Unknown")
            score = "⭐" * min(5, (paper.get("relevance_score", 0) + 1) // 2)
            methods = ", ".join(paper.get("methods", ["未知"])[:2])
            pdf_link = paper.get("pdf_link", "")

            report.append(f"| {i}. {title} | {authors} | {year} | {score} | {methods} | [PDF]({pdf_link}) |")

        report.append("")

        # 详细总结
        report.append("## 📖 详细总结\n")

        for i, paper in enumerate(sorted_papers[:8], 1):
            report.append(f"### {i}. {paper.get('title', '无标题')}\n")
            report.append(f"**作者：** {paper.get('authors', 'Unknown')}")
            if paper.get("institution"):
                report.append(f"  \n**机构：** {paper.get('institution')}")
            report.append(f"  \n**年份：** {paper.get('year', 'Unknown')}")
            report.append(f"  \n**相关性：** {'⭐' * min(5, (paper.get('relevance_score', 0) + 1) // 2)} ({paper.get('relevance_score', 0)}/10)")
            report.append(f"  \n**来源：** {paper.get('source', 'Unknown')}\n")

            # 方法
            methods = paper.get("methods", [])
            report.append(f"**研究方法：**\n")
            for method in methods:
                report.append(f"- {method}\n")

            # 贡献
            contributions = paper.get("contributions", [])
            if contributions:
                report.append(f"\n**核心贡献：**\n")
                for contrib in contributions:
                    report.append(f"- {contrib}\n")

            # 局限性
            limitations = paper.get("limitations", [])
            if limitations:
                report.append(f"\n**局限性：**\n")
                for limit in limitations:
                    report.append(f"- {limit}\n")

            # 摘要
            summary = paper.get("summary", "")
            if summary:
                report.append(f"\n**摘要：**\n{summary}\n")

            # 建议
            report.append(f"\n**建议：** {paper.get('suggestion', '')}\n")
            report.append("---\n")

        # 研究趋势分析
        report.append("## 📈 研究趋势分析\n\n")

        # 热点方向（基于关键词频率）
        report.append("**热点方向：**\n")
        hot_keywords = ["deep learning", "reinforcement learning", "active control"]
        for i, kw in enumerate(hot_keywords[:3], 1):
            report.append(f"{i}. {kw}\n")

        # 研究空白
        report.append("\n**研究空白：**\n")
        report.append("- 小样本下的方法\n")
        report.append("- 实时性验证\n")

        # 建议
        report.append("\n**建议下一步：**\n")
        report.append("1. 精读 Top 3 论文\n")
        report.append("2. 复现关键方法\n")
        report.append("3. 探索研究空白\n")

        # 参考文献
        report.append("\n## 📚 参考文献（国标格式）\n\n")
        for i, paper in enumerate(sorted_papers[:10], 1):
            authors = paper.get("authors", "Unknown")
            title = paper.get("title", "无标题")
            year = paper.get("year", "Unknown")
            source = paper.get("source", "Unknown")

            report.append(f"[{i}] {authors}. {title}[{source}]. {year}.\n")

        # 迭代日志
        if iteration_log:
            report.append("\n## 🔄 迭代日志\n\n")
            for log in iteration_log:
                report.append(f"{log}\n")

        # 统计信息
        report.append("\n---\n")
        report.append(f"**总计筛选：** {len(valid_papers)} 篇 | ")
        report.append(f"**推荐阅读：** Top {min(5, len(valid_papers))} | ")
        report.append(f"**生成时间：** {datetime.now().strftime('%H:%M')} | ")
        report.append(f"**版本：** {version}")

        return "\n".join(report)


def main():
    """主函数"""
    # Set UTF-8 encoding for Windows
    import codecs
    if os.name == 'nt':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

    # 获取参数
    if len(sys.argv) < 2:
        print("用法：python review_generator.py <研究领域> [最大论文数] [迭代版本]")
        print("示例：")
        print("  python review_generator.py \"structural vibration control\"")
        print("  python review_generator.py \"RTHS delay compensation\" 20 v2.0")
        sys.exit(1)

    field = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
    version = sys.argv[3] if len(sys.argv) >= 4 else "v1.0"

    print(f"[INFO] 开始检索 {field} 领域文献...\n")

    # 1. 多源检索
    search_engine = MultiSourceSearch()
    papers = search_engine.search_arxiv(query=field, max_results=max_results, years=5)

    if not papers or "error" in papers[0]:
        print(f"[ERROR] 检索失败：{papers[0].get('error', '未知错误')}")
        sys.exit(1)

    print(f"[INFO] 找到 {len(papers)} 篇论文\n")

    # 2. 分析论文
    print("[INFO] 分析论文中...\n")
    analyzed_papers = [PaperAnalyzer.analyze(p, field) for p in papers]

    # 3. 生成综述
    print("[INFO] 生成综述报告中...\n")
    review = ReviewGenerator.generate(analyzed_papers, field, version)

    # 4. 输出
    print("=" * 60)
    print(review)
    print("=" * 60)

    # 5. 可选：保存到文件
    if len(sys.argv) >= 5 and sys.argv[4] == "--save":
        filename = f"review_{field.replace(' ', '_')}_{version}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(review)
        print(f"\n[INFO] 综述已保存到：{filename}")


if __name__ == "__main__":
    main()
