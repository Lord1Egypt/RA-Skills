"""
Psychology Literature Search Module (升级版)
心理学文献检索模块

功能:
- 多数据源检索 (Semantic Scholar / OpenAlex / CrossRef)
- 中文文献检索 (通过 OpenAlex 语言过滤)
- 批量导出为表格 (CSV)
- 多种引用格式 (APA / GB/T 7714 国标 / MLA / Chicago)

所有 API 均免费且无需 API key
"""

import urllib.request
import urllib.parse
import json
import csv
from typing import Dict, List, Optional


class LiteratureSearch:
    """心理学文献检索器"""

    SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"
    CROSSREF_API = "https://api.crossref.org/works"
    OPENALEX_API = "https://api.openalex.org/works"

    def __init__(self, email: Optional[str] = None):
        """
        参数:
        -----
        email : str, 可选
            提供邮箱可加入 OpenAlex/CrossRef 的礼貌池(polite pool)，响应更快
        """
        self.email = email
        self.headers = {"User-Agent": "PsychLitSearch/1.0"}

    def _request(self, url: str) -> Optional[Dict]:
        """发送 HTTP 请求并解析 JSON"""
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=20) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as e:
            print(f"请求出错: {e}")
            return None

    # ============ Semantic Scholar 检索 ============

    def search_semantic_scholar(self, query: str, limit: int = 10,
                                year_from: Optional[int] = None) -> List[Dict]:
        """使用 Semantic Scholar 检索文献"""
        fields = "title,authors,year,abstract,citationCount,venue,externalIds,url"
        params = {
            "query": query,
            "limit": min(limit, 100),
            "fields": fields,
        }
        if year_from:
            params["year"] = f"{year_from}-"

        url = f"{self.SEMANTIC_SCHOLAR_API}/paper/search?{urllib.parse.urlencode(params)}"
        data = self._request(url)

        if not data or "data" not in data:
            return []

        results = []
        for paper in data["data"]:
            authors = [a.get("name", "") for a in (paper.get("authors") or [])]
            results.append({
                "标题": paper.get("title", ""),
                "作者": authors[:8],
                "年份": paper.get("year"),
                "期刊": paper.get("venue", ""),
                "被引次数": paper.get("citationCount", 0),
                "摘要": (paper.get("abstract") or "")[:300],
                "DOI": (paper.get("externalIds") or {}).get("DOI", ""),
                "链接": paper.get("url", ""),
                "语言": "",
            })
        return results

    # ============ OpenAlex 检索 ============

    def search_openalex(self, query: str, limit: int = 10,
                       year_from: Optional[int] = None,
                       language: Optional[str] = None) -> List[Dict]:
        """
        使用 OpenAlex 检索文献

        参数:
        -----
        language : str, 可选
            语言过滤，如 'zh'(中文) / 'en'(英文)
        """
        params = {
            "search": query,
            "per-page": min(limit, 50),
            "sort": "cited_by_count:desc",
        }
        filters = []
        if year_from:
            filters.append(f"from_publication_date:{year_from}-01-01")
        if language:
            filters.append(f"language:{language}")
        if filters:
            params["filter"] = ",".join(filters)
        if self.email:
            params["mailto"] = self.email

        url = f"{self.OPENALEX_API}?{urllib.parse.urlencode(params)}"
        data = self._request(url)

        if not data or "results" not in data:
            return []

        results = []
        for work in data["results"]:
            authorships = work.get("authorships", [])
            authors = [a.get("author", {}).get("display_name", "")
                      for a in authorships[:8]]
            primary = work.get("primary_location") or {}
            source = primary.get("source") or {}
            results.append({
                "标题": work.get("title", ""),
                "作者": authors,
                "年份": work.get("publication_year"),
                "期刊": source.get("display_name", ""),
                "被引次数": work.get("cited_by_count", 0),
                "摘要": "",
                "DOI": (work.get("doi") or "").replace("https://doi.org/", ""),
                "链接": work.get("doi", ""),
                "语言": work.get("language", ""),
                "开放获取": work.get("open_access", {}).get("is_oa", False),
            })
        return results

    def search_chinese(self, query: str, limit: int = 10,
                      year_from: Optional[int] = None) -> List[Dict]:
        """
        检索中文文献 (通过 OpenAlex 语言过滤)

        注意: 知网(CNKI)、万方无公开免费 API 且禁止爬取，
        本方法通过 OpenAlex 收录的中文期刊文献(带 DOI)进行检索。

        参数:
        -----
        query : str
            可用中文或英文关键词
        """
        return self.search_openalex(query, limit, year_from, language="zh")

    # ============ CrossRef 检索 ============

    def search_crossref(self, query: str, limit: int = 10) -> List[Dict]:
        """使用 CrossRef 检索文献"""
        params = {
            "query": query,
            "rows": min(limit, 50),
            "sort": "relevance",
        }
        if self.email:
            params["mailto"] = self.email

        url = f"{self.CROSSREF_API}?{urllib.parse.urlencode(params)}"
        data = self._request(url)

        if not data or "message" not in data:
            return []

        results = []
        for item in data["message"].get("items", []):
            authors = []
            for a in item.get("author", [])[:8]:
                name = f"{a.get('given', '')} {a.get('family', '')}".strip()
                authors.append(name)

            title = item.get("title", [""])
            title = title[0] if title else ""

            year = None
            if "published" in item:
                date_parts = item["published"].get("date-parts", [[None]])
                year = date_parts[0][0] if date_parts and date_parts[0] else None

            container = item.get("container-title", [""])
            venue = container[0] if container else ""

            results.append({
                "标题": title,
                "作者": authors,
                "年份": year,
                "期刊": venue,
                "被引次数": item.get("is-referenced-by-count", 0),
                "摘要": "",
                "DOI": item.get("DOI", ""),
                "链接": item.get("URL", ""),
                "语言": item.get("language", ""),
            })
        return results

    # ============ 统一检索入口 ============

    def search(self, query: str, source: str = "semantic_scholar",
              limit: int = 10, year_from: Optional[int] = None) -> List[Dict]:
        """
        统一检索入口

        参数:
        -----
        source : str
            'semantic_scholar' / 'openalex' / 'crossref' / 'chinese'(中文文献)
        """
        if source == "semantic_scholar":
            return self.search_semantic_scholar(query, limit, year_from)
        elif source == "openalex":
            return self.search_openalex(query, limit, year_from)
        elif source == "crossref":
            return self.search_crossref(query, limit)
        elif source == "chinese":
            return self.search_chinese(query, limit, year_from)
        else:
            raise ValueError(f"不支持的数据源: {source}")

    # ============ 表格导出 ============

    def export_to_csv(self, papers: List[Dict], filename: str = "文献列表.csv") -> str:
        """
        将检索结果批量导出为 CSV 表格 (可用 Excel 打开)

        参数:
        -----
        papers : list
            search() 返回的文献列表
        filename : str
            导出文件名

        返回:
        -----
        str : 导出文件的路径
        """
        if not papers:
            print("没有可导出的文献")
            return ""

        columns = ["序号", "标题", "作者", "年份", "期刊", "被引次数", "DOI", "链接"]

        # utf-8-sig 让 Excel 正确识别中文编码
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            for i, paper in enumerate(papers, 1):
                authors = "; ".join(paper.get("作者", []))
                writer.writerow([
                    i,
                    paper.get("标题", ""),
                    authors,
                    paper.get("年份", ""),
                    paper.get("期刊", ""),
                    paper.get("被引次数", ""),
                    paper.get("DOI", ""),
                    paper.get("链接", ""),
                ])
        print(f"✅ 已导出 {len(papers)} 篇文献到: {filename}")
        return filename

    # ============ 引用格式化 ============

    def _format_authors_apa(self, authors: List[str]) -> str:
        """APA 作者格式"""
        if not authors:
            return "无作者"
        if len(authors) == 1:
            return authors[0]
        if len(authors) <= 20:
            return ", ".join(authors[:-1]) + ", & " + authors[-1]
        return ", ".join(authors[:19]) + ", ... " + authors[-1]

    def format_citation(self, paper: Dict, style: str = "apa") -> str:
        """
        生成引用格式

        参数:
        -----
        paper : dict
            单条文献
        style : str
            引用风格: 'apa' / 'gbt7714'(国标) / 'mla' / 'chicago'
        """
        authors = paper.get("作者", [])
        year = paper.get("年份", "n.d.")
        title = paper.get("标题", "")
        venue = paper.get("期刊", "")
        doi = paper.get("DOI", "")

        if style == "apa":
            author_str = self._format_authors_apa(authors)
            citation = f"{author_str} ({year}). {title}. {venue}."
            if doi:
                citation += f" https://doi.org/{doi}"
            return citation

        elif style == "gbt7714":
            # 中国国标 GB/T 7714-2015
            if len(authors) > 3:
                author_str = ", ".join(authors[:3]) + ", 等"
            else:
                author_str = ", ".join(authors)
            citation = f"{author_str}. {title}[J]. {venue}, {year}."
            if doi:
                citation += f" DOI:{doi}."
            return citation

        elif style == "mla":
            if not authors:
                author_str = ""
            elif len(authors) == 1:
                author_str = authors[0]
            else:
                author_str = authors[0] + ", et al."
            citation = f'{author_str}. "{title}." {venue}, {year}.'
            return citation

        elif style == "chicago":
            if not authors:
                author_str = ""
            elif len(authors) == 1:
                author_str = authors[0]
            else:
                author_str = ", ".join(authors[:-1]) + ", and " + authors[-1]
            citation = f'{author_str}. "{title}." {venue} ({year}).'
            if doi:
                citation += f" https://doi.org/{doi}."
            return citation

        else:
            raise ValueError(f"不支持的引用格式: {style}")

    def format_apa(self, paper: Dict) -> str:
        """生成 APA 引用 (兼容旧版接口)"""
        return self.format_citation(paper, style="apa")

    def export_citations(self, papers: List[Dict], style: str = "apa",
                        filename: str = "参考文献.txt") -> str:
        """
        批量导出引用列表为文本文件

        参数:
        -----
        papers : list
            文献列表
        style : str
            引用格式: 'apa' / 'gbt7714' / 'mla' / 'chicago'
        filename : str
            导出文件名
        """
        with open(filename, "w", encoding="utf-8") as f:
            for i, paper in enumerate(papers, 1):
                f.write(f"[{i}] {self.format_citation(paper, style)}\n\n")
        print(f"✅ 已导出 {len(papers)} 条 {style.upper()} 格式引用到: {filename}")
        return filename


# ============ 使用示例 ============

if __name__ == "__main__":
    searcher = LiteratureSearch(email="your_email@example.com")

    # 1. 检索英文文献
    print("=== 英文检索: social cognition ===\n")
    papers = searcher.search("social cognition gaze", limit=5, year_from=2020)
    for i, p in enumerate(papers, 1):
        print(f"{i}. {p['标题']} ({p['年份']})")

    # 2. 检索中文文献
    print("\n=== 中文检索: 社会认知 ===\n")
    cn_papers = searcher.search("社会认知 注意", source="chinese", limit=5)
    for i, p in enumerate(cn_papers, 1):
        print(f"{i}. {p['标题']} ({p['年份']})")

    # 3. 导出为表格
    searcher.export_to_csv(papers, "文献列表.csv")

    # 4. 生成不同格式引用
    if papers:
        print("\n=== 引用格式对比 ===")
        print("APA:    ", searcher.format_citation(papers[0], "apa"))
        print("国标:    ", searcher.format_citation(papers[0], "gbt7714"))
        print("MLA:    ", searcher.format_citation(papers[0], "mla"))
        print("Chicago:", searcher.format_citation(papers[0], "chicago"))

    # 5. 批量导出引用
    searcher.export_citations(papers, style="gbt7714", filename="参考文献_国标.txt")
