"""
Tavily API Client for OpenClaw
Implements all Tavily Search API endpoints
"""

import os
import json
import requests
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass
from datetime import date

@dataclass
class TavilySearchResult:
    title: str
    url: str
    content: str
    score: float
    raw_content: Optional[str] = None

@dataclass
class TavilySearchResponse:
    query: str
    results: List[TavilySearchResult]
    answer: Optional[str] = None
    response_time: float = 0.0

class TavilyClient:
    BASE_URL = "https://api.tavily.com"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Tavily client with API key"""
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError(
                "TAVILY_API_KEY environment variable not set. "
                "Get your API key at https://tavily.com/ and set it with:\n"
                "export TAVILY_API_KEY=your_api_key_here"
            )

    def search(
        self,
        query: str,
        max_results: int = 5,
        search_depth: str = "basic",
        topic: str = "general",
        days: Optional[int] = None,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        include_answer: bool = False,
        include_raw_content: bool = False,
        include_images: bool = False,
        domain_filter: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
    ) -> TavilySearchResponse:
        """
        Perform a search with Tavily Search API

        Parameters:
            query: Search query
            max_results: Maximum number of results to return (default: 5, max: 10)
            search_depth: "basic" or "deep" (default: "basic")
                - basic: Faster, good for most use cases
                - deep: More thorough, slower but better quality
            topic: "general" or "news" (default: "general")
                - general: Best for general purpose search
                - news: Optimized for recent news and current events
            days: Time range in days back from current date
            start_date: Start date for range (YYYY-MM-DD)
            end_date: End date for range (YYYY-MM-DD)
            include_answer: Include AI-generated answer (default: False)
            include_raw_content: Include raw content from pages (default: False)
            include_images: Include images from search (default: False)
            domain_filter: List of domains to include only
            exclude_domains: List of domains to exclude

        Returns:
            TavilySearchResponse with results and optional answer
        """
        endpoint = f"{self.BASE_URL}/search"

        # Convert date objects to strings
        if isinstance(start_date, date):
            start_date = start_date.strftime("%Y-%m-%d")
        if isinstance(end_date, date):
            end_date = end_date.strftime("%Y-%m-%d")

        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": min(max_results, 10),
            "search_depth": search_depth,
            "topic": topic,
            "include_answer": include_answer,
            "include_raw_content": include_raw_content,
            "include_images": include_images,
        }

        if days is not None:
            payload["days"] = days
        if start_date is not None:
            payload["start_date"] = start_date
        if end_date is not None:
            payload["end_date"] = end_date
        if domain_filter is not None:
            payload["domain"] = domain_filter
        if exclude_domains is not None:
            payload["exclude_domains"] = exclude_domains

        response = requests.post(endpoint, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        results = []
        for r in data.get("results", []):
            result = TavilySearchResult(
                title=r.get("title", ""),
                url=r.get("url", ""),
                content=r.get("content", ""),
                score=r.get("score", 0.0),
                raw_content=r.get("raw_content")
            )
            results.append(result)

        return TavilySearchResponse(
            query=query,
            results=results,
            answer=data.get("answer"),
            response_time=data.get("response_time", 0.0)
        )

    def answer(
        self,
        query: str,
        max_results: int = 5,
        search_depth: str = "basic",
    ) -> TavilySearchResponse:
        """
        Get a direct answer with citations (Q&A mode)

        Parameters:
            query: Question to answer
            max_results: Maximum number of results
            search_depth: "basic" or "deep"

        Returns:
            TavilySearchResponse with answer and cited results
        """
        return self.search(
            query=query,
            max_results=max_results,
            search_depth=search_depth,
            include_answer=True
        )

    def extract(
        self,
        urls: List[str],
        include_images: bool = False,
    ) -> Dict[str, Any]:
        """
        Extract clean content from URLs

        Parameters:
            urls: List of URLs to extract
            include_images: Whether to include images

        Returns:
            Dictionary with extracted content results
        """
        endpoint = f"{self.BASE_URL}/extract"

        payload = {
            "api_key": self.api_key,
            "urls": urls,
            "include_images": include_images,
        }

        response = requests.post(endpoint, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()

    def search_date_range(
        self,
        query: str,
        start_date: Union[str, date],
        end_date: Union[str, date],
        max_results: int = 5,
        search_depth: str = "basic",
        topic: str = "news",
    ) -> TavilySearchResponse:
        """
        Search within a specific date range

        Parameters:
            query: Search query
            start_date: Start date (YYYY-MM-DD or date object)
            end_date: End date (YYYY-MM-DD or date object)
            max_results: Maximum results
            search_depth: "basic" or "deep"
            topic: "general" or "news"

        Returns:
            TavilySearchResponse
        """
        return self.search(
            query=query,
            max_results=max_results,
            search_depth=search_depth,
            topic=topic,
            start_date=start_date,
            end_date=end_date
        )

def format_results_as_markdown(response: TavilySearchResponse) -> str:
    """Format search results as markdown for easy reading"""
    output = []

    if response.answer:
        output.append(f"**Answer:** {response.answer}\n")

    output.append(f"**Results ({len(response.results)}) in {response.response_time:.2f}s:**\n")

    for i, result in enumerate(response.results, 1):
        output.append(f"{i}. **[{result.title}]({result.url})**")
        output.append(f"   {result.content}\n")

    return "\n".join(output)

def format_results_numbered(response: TavilySearchResponse) -> str:
    """Format as numbered list with event简介 + link (as requested by daily summary)"""
    output = []

    for i, result in enumerate(response.results, 1):
        content = result.content.strip().replace("\n", " ")
        if len(content) > 200:
            content = content[:197] + "..."
        output.append(f"{i}. {content} - {result.url}")

    return "\n".join(output)

if __name__ == "__main__":
    # Simple test
    import sys
    if len(sys.argv) > 1:
        client = TavilyClient()
        resp = client.search(sys.argv[1], max_results=5, days=7)
        print(format_results_as_markdown(resp))
