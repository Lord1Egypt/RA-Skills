#!/usr/bin/env python3
"""
Tavily Search CLI for OpenClaw
Command-line interface for Tavily search operations
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from tavily_api import TavilyClient, format_results_as_markdown, format_results_numbered, TavilySearchResponse

def get_date_range_for_daily_summary() -> tuple[str, str]:
    """Get date range from yesterday 9:10 to today 9:10 (for daily summary task)"""
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    # Yesterday starting at 9:10
    start_date = yesterday.strftime("%Y-%m-%d")
    # Today ending at 9:10
    end_date = today.strftime("%Y-%m-%d")

    return start_date, end_date

def main():
    parser = argparse.ArgumentParser(description="Tavily Search CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Basic search command
    search_parser = subparsers.add_parser("search", help="Search the web")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--max-results", type=int, default=5, help="Maximum results (1-10)")
    search_parser.add_argument("--search-depth", choices=["basic", "deep"], default="basic", help="Search depth")
    search_parser.add_argument("--topic", choices=["general", "news"], default="general", help="Search topic")
    search_parser.add_argument("--days", type=int, help="Time range in days back from today")
    search_parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    search_parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")
    search_parser.add_argument("--format", choices=["markdown", "numbered", "json"], default="markdown", help="Output format")

    # Answer command
    answer_parser = subparsers.add_parser("answer", help="Get direct answer with citations")
    answer_parser.add_argument("query", help="Question to answer")
    answer_parser.add_argument("--max-results", type=int, default=5, help="Maximum results")
    answer_parser.add_argument("--search-depth", choices=["basic", "deep"], default="basic")
    answer_parser.add_argument("--format", choices=["markdown", "numbered", "json"], default="markdown")

    # Date range command (for daily summary)
    date_range_parser = subparsers.add_parser("date-range", help="Search within date range")
    date_range_parser.add_argument("query", help="Search query")
    date_range_parser.add_argument("--start-date", required=True, help="Start date (YYYY-MM-DD)")
    date_range_parser.add_argument("--end-date", required=True, help="End date (YYYY-MM-DD)")
    date_range_parser.add_argument("--max-results", type=int, default=5, help="Maximum results")
    date_range_parser.add_argument("--search-depth", choices=["basic", "deep"], default="basic")
    date_range_parser.add_argument("--topic", choices=["general", "news"], default="news")
    date_range_parser.add_argument("--format", choices=["markdown", "numbered", "json"], default="numbered")

    # Daily summary command (pre-configured for 9:10 previous day to 9:10 today)
    daily_parser = subparsers.add_parser("daily-summary", help="Daily summary search (yesterday 9:10 to today 9:10)")
    daily_parser.add_argument("query", help="Search query")
    daily_parser.add_argument("--max-results", type=int, default=5, help="Maximum results")
    daily_parser.add_argument("--search-depth", choices=["basic", "deep"], default="basic")
    daily_parser.add_argument("--topic", choices=["general", "news"], default="news")
    daily_parser.add_argument("--format", choices=["markdown", "numbered", "json"], default="numbered")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract content from URLs")
    extract_parser.add_argument("urls", nargs="+", help="URLs to extract")

    args = parser.parse_args()

    try:
        client = TavilyClient()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.command == "search":
        resp = client.search(
            query=args.query,
            max_results=args.max_results,
            search_depth=args.search_depth,
            topic=args.topic,
            days=args.days,
            start_date=args.start_date,
            end_date=args.end_date,
            include_answer=False
        )
        if args.format == "markdown":
            print(format_results_as_markdown(resp))
        elif args.format == "numbered":
            print(format_results_numbered(resp))
        else:
            print(json.dumps({
                "query": resp.query,
                "answer": resp.answer,
                "response_time": resp.response_time,
                "results": [
                    {"title": r.title, "url": r.url, "content": r.content, "score": r.score}
                    for r in resp.results
                ]
            }, indent=2, ensure_ascii=False))

    elif args.command == "answer":
        resp = client.answer(
            query=args.query,
            max_results=args.max_results,
            search_depth=args.search_depth
        )
        if args.format == "markdown":
            print(format_results_as_markdown(resp))
        elif args.format == "numbered":
            print(format_results_numbered(resp))
        else:
            print(json.dumps({
                "query": resp.query,
                "answer": resp.answer,
                "response_time": resp.response_time,
                "results": [
                    {"title": r.title, "url": r.url, "content": r.content, "score": r.score}
                    for r in resp.results
                ]
            }, indent=2, ensure_ascii=False))

    elif args.command == "date-range":
        resp = client.search_date_range(
            query=args.query,
            start_date=args.start_date,
            end_date=args.end_date,
            max_results=args.max_results,
            search_depth=args.search_depth,
            topic=args.topic
        )
        if args.format == "markdown":
            print(format_results_as_markdown(resp))
        elif args.format == "numbered":
            print(format_results_numbered(resp))
        else:
            print(json.dumps({
                "query": resp.query,
                "response_time": resp.response_time,
                "results": [
                    {"title": r.title, "url": r.url, "content": r.content, "score": r.score}
                    for r in resp.results
                ]
            }, indent=2, ensure_ascii=False))

    elif args.command == "daily-summary":
        start_date, end_date = get_date_range_for_daily_summary()
        resp = client.search_date_range(
            query=args.query,
            start_date=start_date,
            end_date=end_date,
            max_results=args.max_results,
            search_depth=args.search_depth,
            topic=args.topic
        )
        # Daily summary defaults to numbered format which matches the user's requirement
        print(format_results_numbered(resp))

    elif args.command == "extract":
        result = client.extract(urls=args.urls)
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
