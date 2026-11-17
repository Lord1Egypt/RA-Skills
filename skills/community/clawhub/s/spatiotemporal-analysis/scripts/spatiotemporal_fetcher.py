#!/usr/bin/env python3
"""
spatiotemporal_fetcher.py · 时空智能分析法数据采集器

设计哲学：
- 数据从源头抓取，本地存储为结构化 JSON
- 不依赖 LLM 训练数据（避免过时）
- 每个数据点都有 source_url + capture_time
- 失败的源自动 fallback 到下一级
- 复用 academic-workflow skill 的学术检索能力

用法:
  python spatiotemporal_fetcher.py --subject "OPC 一人公司" --mode longitudinal
  python spatiotemporal_fetcher.py --subject "Cursor" --mode cross_sectional
  python spatiotemporal_fetcher.py --subject "AGI 设计思维" --mode all
"""

import argparse
import hashlib
import json
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# ---------- 数据模型 ----------

@dataclass
class TimelineEvent:
    """纵向时间线的单个事件"""
    date: str
    event_type: str
    title: str
    description: str
    source_url: str
    source_type: str
    confidence: str  # confirmed/reported/speculated
    capture_time: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CompetitorProfile:
    """横向对比的单个竞品"""
    name: str
    founded: str = ""
    pricing: str = ""
    core_edge: str = ""
    key_weakness: str = ""
    user_praise: List[str] = field(default_factory=list)
    user_complaint: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)


# ---------- 数据源 ----------

class DataSource:
    def fetch(self, query: str) -> List[dict]:
        raise NotImplementedError


class AcademicSource(DataSource):
    """复用 academic-workflow skill 的学术检索"""

    def __init__(self):
        try:
            sys.path.insert(0, '/Users/neocross/.hermes/skills/openclaw-imports/academic-workflow/scripts')
            from research import search_openalex, search_arxiv
            self.search_openalex = search_openalex
            self.search_arxiv = search_arxiv
        except ImportError as e:
            print(f"⚠️ academic-workflow 不可用: {e}")
            self.search_openalex = None
            self.search_arxiv = None

    def fetch(self, query: str) -> List[dict]:
        results = []
        # OpenAlex（无需 API key）
        if self.search_openalex:
            try:
                papers = self.search_openalex(query, max_results=10, sort='date')
                for p in papers:
                    results.append({
                        "title": p.get('title', ''),
                        "year": p.get('publication_year'),
                        "cited_by": p.get('cited_by_count', 0),
                        "doi": p.get('doi', ''),
                        "source_type": "academic_openalex",
                        "url": f"https://doi.org/{p.get('doi', '')}" if p.get('doi') else "",
                    })
            except Exception as e:
                print(f"  OpenAlex 失败: {e}")

        # arXiv（前沿预印本）
        if self.search_arxiv:
            try:
                papers = self.search_arxiv(query, max_results=5)
                for p in papers:
                    results.append({
                        "title": p.get('title', ''),
                        "year": p.get('published', '')[:10],
                        "authors": p.get('authors', []),
                        "url": p.get('entry_id', ''),
                        "source_type": "academic_arxiv",
                    })
            except Exception as e:
                print(f"  arXiv 失败: {e}")
        return results


class WebSource(DataSource):
    """DuckDuckGo 免费搜索"""

    def __init__(self):
        try:
            from duckduckgo_search import DDGS
            self.DDGS = DDGS
        except ImportError:
            print("⚠️ duckduckgo_search 未安装，pip install duckduckgo-search")
            self.DDGS = None

    def fetch(self, query: str) -> List[dict]:
        if not self.DDGS:
            return []
        results = []
        try:
            with self.DDGS() as ddgs:
                for r in ddgs.text(query, max_results=10):
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", ""),
                        "source_type": self._classify(r.get("href", "")),
                        "capture_time": datetime.now().isoformat(),
                    })
        except Exception as e:
            print(f"  DuckDuckGo 失败: {e}")
        return results

    def _classify(self, url: str) -> str:
        if "arxiv.org" in url:
            return "academic_arxiv"
        if "github.com" in url or "huggingface" in url:
            return "repo"
        if "reddit.com" in url or "news.ycombinator" in url:
            return "community"
        if any(d in url for d in ["crunchbase", "pitchbook"]):
            return "financial_db"
        return "news"


class GitHubSource(DataSource):
    """GitHub 抓取（需 gh CLI）"""

    def fetch(self, query: str) -> List[dict]:
        import subprocess
        results = []
        try:
            r = subprocess.run(
                ["gh", "search", "repos", query, "--limit", "10",
                 "--json", "name,description,url,stargazersCount,createdAt,updatedAt"],
                capture_output=True, text=True, timeout=30
            )
            if r.returncode == 0:
                for item in json.loads(r.stdout):
                    results.append({
                        "name": item["name"],
                        "url": item["url"],
                        "description": item.get("description", ""),
                        "stars": item.get("stargazersCount", 0),
                        "created": item.get("createdAt", ""),
                        "updated": item.get("updatedAt", ""),
                        "source_type": "github",
                    })
        except Exception as e:
            print(f"  GitHub 失败: {e}")
        return results


class CacheSource(DataSource):
    """本地 7 天缓存"""

    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _key(self, query: str) -> str:
        return hashlib.md5(query.encode()).hexdigest()[:12]

    def fetch(self, query: str) -> List[dict]:
        f = self.cache_dir / f"{self._key(query)}.json"
        if f.exists():
            age_days = (time.time() - f.stat().st_mtime) / 86400
            if age_days < 7:
                return json.loads(f.read_text())
        return []

    def save(self, query: str, results: list):
        f = self.cache_dir / f"{self._key(query)}.json"
        f.write_text(json.dumps(results, ensure_ascii=False, indent=2))


# ---------- 主调度 ----------

class HengzongFetcher:
    def __init__(self, cache_dir: str = "~/.hermes/spatiotemporal-cache"):
        self.cache = CacheSource(cache_dir)
        self.sources = [
            AcademicSource(),
            WebSource(),
            GitHubSource(),
        ]

    def fetch(self, query: str, use_cache: bool = True) -> List[dict]:
        """多源 fallback"""
        if use_cache:
            cached = self.cache.fetch(query)
            if cached:
                return cached

        all_results = []
        for source in self.sources:
            try:
                results = source.fetch(query)
                all_results.extend(results)
                if len(all_results) >= 10:
                    break
            except Exception as e:
                print(f"⚠️ {type(source).__name__} 失败: {e}")
                continue

        if all_results:
            self.cache.save(query, all_results)
        return all_results

    def fetch_longitudinal(self, subject: str) -> dict:
        """纵向：拉时间线（按时间排序）"""
        queries = [
            f"{subject} history origin founding",
            f"{subject} funding investment series",
            f"{subject} launch release timeline",
            f"{subject} founder team leadership",
        ]
        results = {}
        for q in queries:
            results[q] = self.fetch(q)
        return results

    def fetch_cross_sectional(self, subject: str) -> dict:
        """横向：拉竞品/替代方案"""
        queries = [
            f"{subject} vs alternatives competitors",
            f"{subject} comparison review",
            f"best {subject} 2026",
        ]
        results = {}
        for q in queries:
            results[q] = self.fetch(q)
        return results


# ---------- CLI ----------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="时空智能分析法 · 数据采集器")
    parser.add_argument("--subject", required=True, help="研究对象")
    parser.add_argument("--mode", choices=["longitudinal", "cross_sectional", "all"],
                        default="all")
    parser.add_argument("--cache-dir", default="~/.hermes/spatiotemporal-cache")
    parser.add_argument("--no-cache", action="store_true")

    args = parser.parse_args()

    fetcher = HengzongFetcher(cache_dir=args.cache_dir)

    print(f"📅 研究对象: {args.subject}")
    print(f"📦 缓存: {args.cache_dir} (TTL 7 天)")
    print()

    if args.mode in ("longitudinal", "all"):
        print("📜 拉纵向时间线...")
        long = fetcher.fetch_longitudinal(args.subject)
        total = sum(len(v) for v in long.values())
        print(f"  ✅ 共 {total} 条原始数据，{len(long)} 个查询")

    if args.mode in ("cross_sectional", "all"):
        print("🔍 拉横向对比...")
        cross = fetcher.fetch_cross_sectional(args.subject)
        total = sum(len(v) for v in cross.values())
        print(f"  ✅ 共 {total} 条原始数据，{len(cross)} 个查询")

    print()
    print("💡 下一步：把原始数据交给 spatiotemporal 子 agent 提取结构化事件/竞品。")
