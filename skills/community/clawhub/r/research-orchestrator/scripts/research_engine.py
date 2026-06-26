#!/usr/bin/env python3
"""
Deep Research Engine
Multi-source research with web search and academic sources
"""

import json
import os
import sys
import subprocess
from datetime import datetime


class ResearchEngine:
    def __init__(self, workspace=None):
        self.workspace = workspace or os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())
        self.search_cache = {}

    def search_web(self, query, max_results=10):
        """Execute web search using web-search skill or curl"""

        results = []

        # Try web-search skill first
        try:
            # This would be called by the OpenClaw agent
            # For now, return placeholder
            results = {
                "query": query,
                "source": "web-search",
                "results": [],
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"⚠️ Web search failed: {e}")

        return results

    def search_academic(self, query, max_results=5):
        """Search academic sources (arxiv, scholar)"""

        results = []

        # Search arxiv
        arxiv_results = self._search_arxiv(query, max_results)
        results.extend(arxiv_results)

        return {
            "query": query,
            "source": "academic",
            "results": results,
            "timestamp": datetime.now().isoformat(),
        }

    def _search_arxiv(self, query, max_results=5):
        """Search arxiv.org"""

        results = []

        try:
            # Use curl to search arxiv API
            encoded_query = query.replace(" ", "+")
            url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"

            # This would use curl in practice
            # For now, return structure
            results = []
        except Exception as e:
            print(f"⚠️ Arxiv search failed: {e}")

        return results

    def multi_source_search(self, queries, sources=None):
        """Execute search across multiple sources"""

        if sources is None:
            sources = ["web", "academic"]

        all_results = []

        for query in queries:
            query_results = {"query": query, "sources": {}}

            if "web" in sources:
                web_results = self.search_web(query)
                query_results["sources"]["web"] = web_results

            if "academic" in sources:
                try:
                    academic_results = self.search_academic(query)
                    query_results["sources"]["academic"] = academic_results
                except Exception as e:
                    print(f"⚠️ Academic search failed, falling back to web: {e}")
                    # Fallback to web search
                    web_results = self.search_web(query)
                    query_results["sources"]["web"] = web_results

            all_results.append(query_results)

        return all_results

    def extract_findings(self, search_results):
        """Extract key findings from search results"""

        findings = []
        sources = []

        for result_group in search_results:
            query = result_group["query"]

            for source_type, source_results in result_group["sources"].items():
                for item in source_results.get("results", []):
                    finding = {
                        "query": query,
                        "source_type": source_type,
                        "content": item.get("content", ""),
                        "url": item.get("url", ""),
                        "title": item.get("title", ""),
                        "credibility": self._assess_credibility(item),
                        "extracted_at": datetime.now().isoformat(),
                    }
                    findings.append(finding)
                    sources.append(finding["url"])

        return findings, list(set(sources))

    def _assess_credibility(self, source):
        """Assess source credibility"""

        url = source.get("url", "").lower()

        # High credibility domains
        high_credibility = [
            "arxiv.org",
            "nature.com",
            "science.org",
            "ieee.org",
            "gartner.com",
            "idc.com",
            "mckinsey.com",
            "gov",
            "edu",
        ]

        # Medium credibility domains
        medium_credibility = [
            "reuters.com",
            "bloomberg.com",
            "wsj.com",
            "techcrunch.com",
            "wired.com",
        ]

        for domain in high_credibility:
            if domain in url:
                return "high"

        for domain in medium_credibility:
            if domain in url:
                return "medium"

        return "low"

    def generate_search_queries(self, topic, language="en"):
        """Generate diverse search queries for a topic"""

        queries = []

        if language.startswith("zh"):
            queries = [
                f"{topic} 市场规模 2026",
                f"{topic} 发展趋势",
                f"{topic} 行业分析",
                f"{topic} 主要厂商",
                f"{topic} 投资动态",
                f"{topic} 技术趋势",
                f"{topic} 政策环境",
                f"{topic} 风险挑战",
            ]
        else:
            queries = [
                f"{topic} market size 2026",
                f"{topic} industry trends",
                f"{topic} market analysis",
                f"{topic} key players",
                f"{topic} investment trends",
                f"{topic} technology trends",
                f"{topic} regulatory environment",
                f"{topic} challenges risks",
            ]

        return queries

    def research_angle(self, angle_name, queries, sources=None):
        """Research a specific angle with multiple queries"""

        print(f"🔍 Researching: {angle_name}")
        print(f"   Queries: {len(queries)}")

        # Execute multi-source search
        results = self.multi_source_search(queries, sources)

        # Extract findings
        findings, source_urls = self.extract_findings(results)

        print(f"   Findings: {len(findings)}")
        print(f"   Sources: {len(source_urls)}")

        return {
            "angle": angle_name,
            "queries": queries,
            "findings": findings,
            "sources": source_urls,
            "finding_count": len(findings),
            "source_count": len(source_urls),
            "completed_at": datetime.now().isoformat(),
        }

    def save_research_results(self, output_file, research_data):
        """Save research results to file"""

        # Create markdown report
        md_content = f"# {research_data['angle']}\n\n"
        md_content += f"**Queries**: {', '.join(research_data['queries'])}\n\n"
        md_content += f"**Findings**: {research_data['finding_count']}\n\n"
        md_content += f"**Sources**: {research_data['source_count']}\n\n"

        md_content += "## Key Findings\n\n"

        for i, finding in enumerate(research_data["findings"], 1):
            md_content += f"### Finding {i}\n"
            md_content += f"- **Content**: {finding['content'][:200]}...\n"
            md_content += f"- **Source**: {finding['url']}\n"
            md_content += f"- **Credibility**: {finding['credibility']}\n\n"

        md_content += "## Sources\n\n"
        for source in research_data["sources"]:
            md_content += f"- {source}\n"

        # Save markdown
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        # Save JSON data
        json_file = output_file.replace(".md", ".json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(research_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Research saved: {output_file}")
        return output_file


def main():
    """CLI interface"""

    if len(sys.argv) < 2:
        print("Usage: python3 research_engine.py <command> [args]")
        print("Commands:")
        print("  search <query>          - Single search")
        print("  research <topic> [lang] - Full research on topic")
        sys.exit(1)

    command = sys.argv[1]
    engine = ResearchEngine()

    if command == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        results = engine.search_web(query)
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif command == "research":
        topic = sys.argv[2] if len(sys.argv) > 2 else "AI chips"
        lang = sys.argv[3] if len(sys.argv) > 3 else "en"
        queries = engine.generate_search_queries(topic, lang)
        results = engine.multi_source_search(queries)
        findings, sources = engine.extract_findings(results)
        print(
            json.dumps(
                {"findings": findings[:5], "source_count": len(sources)}, indent=2
            )
        )

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
