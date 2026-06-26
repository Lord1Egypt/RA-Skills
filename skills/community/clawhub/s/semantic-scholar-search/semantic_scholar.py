#!/usr/bin/env python3
"""
Semantic Scholar Search - Free academic paper search tool

Based on Semantic Scholar API v2
https://api.semanticscholar.org/
"""

import requests
import json
import sys
from typing import Dict, Any, List, Optional


class SemanticScholarSearch:
    """Semantic Scholar API wrapper."""

    def __init__(self):
        self.base_url = "https://api.semanticscholar.org/graph/v1"
        self.headers = {"Accept": "application/json"}

    def search_papers(
        self,
        query: str,
        limit: int = 10,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        sort_by: str = "relevance"
    ) -> List[Dict[str, Any]]:
        """
        Search for academic papers.

        Args:
            query: Search query string
            limit: Maximum number of results (default: 10)
            year_min: Minimum publication year
            year_max: Maximum publication year
            sort_by: Sort order - 'relevance' or 'citationCount'

        Returns:
            List of paper dictionaries
        """
        endpoint = f"{self.base_url}/paper/search"

        params = {
            "query": query,
            "limit": min(limit, 100),  # API max is 100
            "fields": "title,authors,year,citationCount,abstract,venue,url,tldr"
        }

        if year_min:
            params["year"] = f"{year_min}-"
        if year_max:
            if "year" in params:
                params["year"] = f"{year_min}-{year_max}" if year_min else f"-{year_max}"
            else:
                params["year"] = f"-{year_max}"

        if sort_by == "citationCount":
            params["sort"] = "citationCount:desc"

        try:
            response = requests.get(endpoint, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            papers = []
            for item in data.get("data", []):
                paper = {
                    "title": item.get("title", "No title"),
                    "authors": [a.get("name", "Unknown") for a in item.get("authors", [])],
                    "year": item.get("year", "Unknown"),
                    "citationCount": item.get("citationCount", 0),
                    "venue": item.get("venue", "Unknown"),
                    "url": item.get("url", ""),
                    "abstract": item.get("abstract", ""),
                    "tldr": item.get("tldr", {}).get("text", "") if item.get("tldr") else ""
                }
                papers.append(paper)

            return papers

        except requests.RequestException as e:
            return [{"error": f"Request failed: {str(e)}"}]
        except Exception as e:
            return [{"error": f"Error: {str(e)}"}]

    def get_author(self, author_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for authors.

        Args:
            author_name: Author name to search
            limit: Maximum number of results

        Returns:
            List of author dictionaries
        """
        endpoint = f"{self.base_url}/author/search"

        params = {
            "query": author_name,
            "limit": limit,
            "fields": "name,affiliation,citationCount,paperCount,url"
        }

        try:
            response = requests.get(endpoint, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            authors = []
            for item in data.get("data", []):
                author = {
                    "name": item.get("name", "Unknown"),
                    "affiliation": item.get("affiliation", "Unknown"),
                    "citationCount": item.get("citationCount", 0),
                    "paperCount": item.get("paperCount", 0),
                    "url": item.get("url", "")
                }
                authors.append(author)

            return authors

        except requests.RequestException as e:
            return [{"error": f"Request failed: {str(e)}"}]

    def get_paper_details(self, paper_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific paper.

        Args:
            paper_id: Semantic Scholar paper ID

        Returns:
            Paper details dictionary
        """
        endpoint = f"{self.base_url}/paper/{paper_id}"

        params = {
            "fields": "title,authors,year,citationCount,abstract,venue,url,references,citations,tldr"
        }

        try:
            response = requests.get(endpoint, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            return {
                "title": data.get("title", "No title"),
                "authors": [a.get("name", "Unknown") for a in data.get("authors", [])],
                "year": data.get("year", "Unknown"),
                "citationCount": data.get("citationCount", 0),
                "venue": data.get("venue", "Unknown"),
                "url": data.get("url", ""),
                "abstract": data.get("abstract", ""),
                "tldr": data.get("tldr", {}).get("text", "") if data.get("tldr") else "",
                "references": len(data.get("references", [])),
                "citations": len(data.get("citations", []))
            }

        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}


class OutputHandler:
    """Handle output formatting."""

    @staticmethod
    def print_papers(papers: List[Dict[str, Any]]) -> None:
        """Print papers in a readable format."""
        if not papers:
            print("[ERROR] No papers found")
            return

        if "error" in papers[0]:
            print(f"[ERROR] {papers[0]['error']}")
            return

        print(f"\nFound {len(papers)} papers:\n")

        for i, paper in enumerate(papers, 1):
            print(f"{'='*60}")
            print(f"[{i}] {paper.get('title', 'No title')}")
            print(f"Authors: {', '.join(paper.get('authors', ['Unknown']))}")
            print(f"Year: {paper.get('year', 'Unknown')} | Citations: {paper.get('citationCount', 0)}")
            print(f"Venue: {paper.get('venue', 'Unknown')}")

            # 优先显示 TLDR（简短摘要）
            tldr = paper.get('tldr', '')
            abstract = paper.get('abstract', '')
            if tldr:
                print(f"Abstract: {tldr}")
            elif abstract:
                # 截断长摘要
                if len(abstract) > 300:
                    abstract = abstract[:300] + "..."
                print(f"Abstract: {abstract}")

            url = paper.get('url', '')
            if url:
                print(f"URL: {url}")
            print()

        print(f"{'='*60}")

    @staticmethod
    def print_authors(authors: List[Dict[str, Any]]) -> None:
        """Print authors in a readable format."""
        if not authors:
            print("[ERROR] No authors found")
            return

        if "error" in authors[0]:
            print(f"[ERROR] {authors[0]['error']}")
            return

        print(f"\nFound {len(authors)} authors:\n")

        for i, author in enumerate(authors, 1):
            print(f"{'='*60}")
            print(f"[{i}] {author.get('name', 'Unknown')}")
            print(f"Affiliation: {author.get('affiliation', 'Unknown')}")
            print(f"Total Citations: {author.get('citationCount', 0)} | Papers: {author.get('paperCount', 0)}")
            url = author.get('url', '')
            if url:
                print(f"URL: {url}")
            print()

        print(f"{'='*60}")


def main():
    """Main entry point."""
    # Set UTF-8 encoding for Windows
    import os
    if os.name == 'nt':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

    if len(sys.argv) < 2:
        print("用法：python semantic_scholar.py <搜索词> [年份] [排序方式]")
        print("示例：")
        print("  python semantic_scholar.py \"machine learning\"")
        print("  python semantic_scholar.py \"deep learning\" 2020 citationCount")
        print("  python semantic_scholar.py --author \"Yann LeCun\"")
        sys.exit(1)

    searcher = SemanticScholarSearch()
    output = OutputHandler()

    # 检查是否是作者搜索
    if sys.argv[1] == "--author":
        if len(sys.argv) < 3:
            print("[ERROR] Please provide author name")
            sys.exit(1)
        author_name = sys.argv[2]
        authors = searcher.get_author(author_name)
        output.print_authors(authors)
        return

    # 论文搜索
    query = sys.argv[1]
    year_min = None
    sort_by = "relevance"

    # 解析年份参数
    if len(sys.argv) >= 3:
        try:
            year_min = int(sys.argv[2])
        except ValueError:
            if sys.argv[2] in ["citationCount", "citation"]:
                sort_by = "citationCount"

    # 解析排序参数
    if len(sys.argv) >= 4:
        if sys.argv[3] in ["citationCount", "citation"]:
            sort_by = "citationCount"

    papers = searcher.search_papers(query, limit=10, year_min=year_min, sort_by=sort_by)
    output.print_papers(papers)


if __name__ == "__main__":
    main()
