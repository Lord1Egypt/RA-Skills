#!/usr/bin/env python3
"""
科研文献每日推送技能执行器

功能：
1. 检索 arXiv 最新论文
2. 生成结构化总结
3. 推送通知

作者：OpenClaw Community
创建：2026-04-03
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import xml.etree.ElementTree as ET


class ArxivSearch:
    """arXiv API 搜索封装"""

    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"
        self.headers = {"User-Agent": "OpenClaw-Research-Push/1.0"}

    def search(
        self,
        query: str,
        max_results: int = 10,
        days: int = 2,
        sort_by: str = "submittedDate"
    ) -> List[Dict[str, Any]]:
        """
        搜索 arXiv 论文

        Args:
            query: 搜索关键词
            max_results: 最大结果数
            days: 最近 N 天
            sort_by: 排序方式

        Returns:
            论文列表
        """
        # 构建搜索查询
        search_query = f"all:{query}"

        # 计算日期范围（arXiv API 不支持直接日期过滤，需要获取后筛选）
        params = {
            "search_query": search_query,
            "start": 0,
            "max_results": max_results * 2,  # 多获取一些用于筛选
            "sortBy": sort_by,
            "sortOrder": "descending"
        }

        try:
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()

            # 解析 XML 响应
            papers = self._parse_response(response.text)

            # 筛选最近 N 天的论文
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_papers = [
                p for p in papers
                if p.get("published") and self._parse_date(p["published"]) >= cutoff_date
            ]

            return recent_papers[:max_results]

        except requests.RequestException as e:
            return [{"error": f"搜索失败：{str(e)}"}]
        except Exception as e:
            return [{"error": f"错误：{str(e)}"}]

    def _parse_response(self, xml_content: str) -> List[Dict[str, Any]]:
        """解析 arXiv XML 响应"""
        papers = []
        ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

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
                    "updated": self._get_text(entry, "atom:updated", ns),
                    "summary": self._get_text(entry, "atom:summary", ns),
                    "link": entry.find("atom:id", ns).text if entry.find("atom:id", ns) is not None else "",
                    "pdf_link": self._get_pdf_link(entry, ns),
                    "categories": [
                        cat.get("term", "")
                        for cat in entry.findall("atom:category", ns)
                    ]
                }
                papers.append(paper)

        except ET.ParseError as e:
            return [{"error": f"XML 解析错误：{str(e)}"}]

        return papers

    def _get_text(self, parent: ET.Element, tag: str, ns: dict) -> str:
        """获取 XML 元素文本"""
        elem = parent.find(tag, ns)
        return elem.text.strip() if elem is not None and elem.text else ""

    def _get_pdf_link(self, entry: ET.Element, ns: dict) -> str:
        """获取 PDF 下载链接"""
        for link in entry.findall("atom:link", ns):
            if link.get("title") == "pdf":
                return link.get("href", "")
        return ""

    def _parse_date(self, date_str: str) -> datetime:
        """解析 ISO 8601 日期"""
        try:
            # arXiv 日期格式：2026-04-02T12:34:56Z
            return datetime.strptime(date_str[:19], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return datetime.now()


class PaperAnalyzer:
    """论文分析器"""

    @staticmethod
    def analyze(paper: Dict[str, Any], user_field: str = "") -> Dict[str, Any]:
        """
        分析单篇论文

        Args:
            paper: 论文信息
            user_field: 用户研究领域

        Returns:
            分析结果
        """
        # 提取关键信息
        title = paper.get("title", "无标题")
        authors = paper.get("authors", [])
        summary = paper.get("summary", "")
        published = paper.get("published", "")

        # 简单的相关性评分（基于关键词匹配）
        relevance_score = PaperAnalyzer._calculate_relevance(title, summary, user_field)

        # 生成分析结果
        analysis = {
            "title": title,
            "authors": ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else ""),
            "institution": PaperAnalyzer._extract_institution(authors),  # 简化处理
            "published": published[:10] if published else "",
            "summary": summary[:500] + "..." if len(summary) > 500 else summary,
            "relevance_score": relevance_score,
            "innovation_score": PaperAnalyzer._estimate_innovation(title, summary),
            "pdf_link": paper.get("pdf_link", ""),
            "arxiv_link": paper.get("link", ""),
            "categories": paper.get("categories", []),
            "suggestion": PaperAnalyzer._generate_suggestion(relevance_score)
        }

        return analysis

    @staticmethod
    def _calculate_relevance(title: str, summary: str, user_field: str) -> int:
        """计算相关性分数（1-10）"""
        if not user_field:
            return 5  # 默认中等相关

        # 简单的关键词匹配
        keywords = user_field.lower().split()
        text = (title + " " + summary).lower()

        matches = sum(1 for kw in keywords if kw in text)
        score = min(10, max(1, matches * 2))

        return score

    @staticmethod
    def _estimate_innovation(title: str, summary: str) -> int:
        """估算创新度（1-10）"""
        # 检测创新关键词
        innovation_keywords = [
            "novel", "new", "first", "propose", "introduce",
            "innovative", "breakthrough", "state-of-the-art"
        ]

        text = (title + " " + summary).lower()
        matches = sum(1 for kw in innovation_keywords if kw in text)

        return min(10, max(1, 3 + matches))

    @staticmethod
    def _extract_institution(authors: List[str]) -> str:
        """提取机构信息（简化版）"""
        # 实际实现需要更复杂的作者 - 机构映射
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


class ReportGenerator:
    """报告生成器"""

    @staticmethod
    def generate(
        papers: List[Dict[str, Any]],
        field: str,
        date: Optional[str] = None
    ) -> str:
        """
        生成推送报告

        Args:
            papers: 论文分析结果列表
            field: 研究领域
            date: 日期字符串

        Returns:
            Markdown 格式报告
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        # 过滤错误结果
        valid_papers = [p for p in papers if "error" not in p]

        if not valid_papers:
            return f"# 📚 今日 {field} 文献早报（{date}）\n\n❌ 未找到最新论文"

        # 按相关性排序
        sorted_papers = sorted(valid_papers, key=lambda x: x.get("relevance_score", 0), reverse=True)

        # 生成报告
        report = []
        report.append(f"# 📚 今日 {field} 文献早报（{date}）\n")

        # 论文列表表格
        report.append("## 📊 论文列表\n")
        report.append("| 标题 | 作者 | 相关性 | 链接 |")
        report.append("|------|------|--------|------|")

        for i, paper in enumerate(sorted_papers[:10], 1):
            title = paper.get("title", "无标题")[:50] + "..." if len(paper.get("title", "")) > 50 else paper.get("title", "")
            authors = paper.get("authors", "Unknown")
            score = "⭐" * min(5, (paper.get("relevance_score", 0) + 1) // 2)
            pdf_link = paper.get("pdf_link", "")

            report.append(f"| {i}. {title} | {authors} | {score} | [PDF]({pdf_link}) |")

        report.append("")

        # 详细总结
        report.append("## 📖 详细总结\n")

        for i, paper in enumerate(sorted_papers[:5], 1):
            report.append(f"### {i}. {paper.get('title', '无标题')}\n")
            report.append(f"**作者：** {paper.get('authors', 'Unknown')}")
            if paper.get("institution"):
                report.append(f"  \n**机构：** {paper.get('institution')}")
            report.append(f"  \n**相关性：** {'⭐' * min(5, (paper.get('relevance_score', 0) + 1) // 2)} ({paper.get('relevance_score', 0)}/10)")
            report.append(f"  \n**发表：** {paper.get('published', 'Unknown')}\n")

            # 核心创新点（从摘要提取）
            summary = paper.get("summary", "")
            if summary:
                report.append(f"**核心内容：**\n{summary}\n")

            # 建议
            report.append(f"**建议：** {paper.get('suggestion', '')}\n")
            report.append("---\n")

        # 推荐阅读 Top 3
        report.append("## 📌 推荐阅读 Top 3\n\n")
        for i, paper in enumerate(sorted_papers[:3], 1):
            score_desc = ""
            if paper.get("relevance_score", 0) >= 8:
                score_desc = "高度相关，创新性强"
            elif paper.get("relevance_score", 0) >= 6:
                score_desc = "方法可借鉴"
            else:
                score_desc = "综述性好"

            report.append(f"{i}. **{paper.get('title', '无标题')}** - {score_desc}\n")

        # 统计信息
        report.append("---\n")
        report.append(f"**总计筛选：** {len(valid_papers)} 篇 | ")
        report.append(f"**推荐阅读：** Top {min(3, len(valid_papers))} | ")
        report.append(f"**生成时间：** {datetime.now().strftime('%H:%M')}")

        return "\n".join(report)


def main():
    """主函数"""
    # Set UTF-8 encoding for Windows
    import os
    import codecs
    if os.name == 'nt':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

    # 获取参数
    if len(sys.argv) < 2:
        print("用法：python research_push.py <研究领域> [最大论文数]")
        print("示例：")
        print("  python research_push.py \"structural vibration control\"")
        print("  python research_push.py \"RTHS\" 5")
        sys.exit(1)

    field = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

    print("[INFO] Starting paper search...")

    # 1. 搜索论文
    search_engine = ArxivSearch()
    papers = search_engine.search(query=field, max_results=max_results, days=2)

    if not papers or "error" in papers[0]:
        print(f"[ERROR] Search failed: {papers[0].get('error', 'Unknown error')}")
        sys.exit(1)

    print(f"[INFO] Found {len(papers)} papers\n")

    # 2. 分析论文
    print("[INFO] Analyzing papers...\n")
    analyzed_papers = [PaperAnalyzer.analyze(p, field) for p in papers]

    # 3. 生成报告
    print("[INFO] Generating report...\n")
    report = ReportGenerator.generate(analyzed_papers, field)

    # 4. 输出
    print("=" * 60)
    print(report)
    print("=" * 60)

    # 5. 可选：保存到文件
    if len(sys.argv) >= 4 and sys.argv[3] == "--save":
        filename = f"research_push_{datetime.now().strftime('%Y%m%d')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n[INFO] Report saved to: {filename}")


if __name__ == "__main__":
    main()
