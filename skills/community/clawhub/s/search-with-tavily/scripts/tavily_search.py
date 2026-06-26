#!/usr/bin/env python3
"""
Tavily Search CLI Tool
Web search using Tavily API - optimized for AI agents and RAG applications.

Usage:
    tavily_search.py search "your query" [--max-results 5]
    tavily_search.py qna "your question"
    tavily_search.py context "your query" [--max-tokens 4000]
"""

import os
import sys
import json
import argparse
from typing import Optional, List, Dict, Any

# Try to import tavily
try:
    from tavily import TavilyClient
    from tavily.exceptions import TavilyError, RateLimitError, InvalidAPIKeyError
except ImportError:
    print("Error: tavily-python package not installed.", file=sys.stderr)
    print("Install with: pip install tavily-python", file=sys.stderr)
    sys.exit(1)


def get_api_key() -> str:
    """Get Tavily API key from environment variable."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("Error: TAVILY_API_KEY environment variable not set.", file=sys.stderr)
        print("Set it with: export TAVILY_API_KEY='tvly-your-key'", file=sys.stderr)
        sys.exit(1)
    return api_key


def create_client() -> TavilyClient:
    """Create and return TavilyClient instance."""
    api_key = get_api_key()
    return TavilyClient(api_key=api_key)


def handle_error(error: Exception) -> None:
    """Handle Tavily errors gracefully."""
    if isinstance(error, InvalidAPIKeyError):
        print("Error: Invalid API key. Check your TAVILY_API_KEY.", file=sys.stderr)
    elif isinstance(error, RateLimitError):
        print("Error: Rate limit exceeded. Please wait before retrying.", file=sys.stderr)
    elif isinstance(error, TavilyError):
        print(f"Error: Tavily API error - {error}", file=sys.stderr)
    else:
        print(f"Error: {error}", file=sys.stderr)
    sys.exit(1)


def search_command(args: argparse.Namespace) -> None:
    """Execute search command."""
    try:
        client = create_client()
        
        response = client.search(
            query=args.query,
            max_results=args.max_results,
            search_depth=args.search_depth,
            include_answer=args.include_answer,
            include_raw_content=args.include_raw_content,
            time_range=args.time_range,
            topic=args.topic,
            include_domains=args.include_domains or [],
            exclude_domains=args.exclude_domains or []
        )
        
        # Output as JSON for easy parsing
        print(json.dumps(response, indent=2, ensure_ascii=False))
        
    except Exception as e:
        handle_error(e)


def qna_command(args: argparse.Namespace) -> None:
    """Execute Q&A command."""
    try:
        client = create_client()
        
        answer = client.qna_search(
            query=args.query,
            search_depth=args.search_depth,
            max_results=args.max_results
        )
        
        # Output answer as plain text
        print(answer)
        
    except Exception as e:
        handle_error(e)


def context_command(args: argparse.Namespace) -> None:
    """Execute context retrieval command (for RAG)."""
    try:
        client = create_client()
        
        context = client.get_search_context(
            query=args.query,
            max_tokens=args.max_tokens,
            max_results=args.max_results,
            search_depth=args.search_depth
        )
        
        # Output context as plain text
        print(context)
        
    except Exception as e:
        handle_error(e)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Tavily Search CLI - Web search for AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s search "latest AI news" --max-results 10
    %(prog)s qna "Who won the 2024 election?"
    %(prog)s context "climate change effects" --max-tokens 2000

Environment:
    TAVILY_API_KEY    Required. Your Tavily API key.
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Perform web search")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--max-results", type=int, default=5, help="Number of results (1-20)")
    search_parser.add_argument("--search-depth", choices=["basic", "comprehensive"], default="basic", help="Search depth")
    search_parser.add_argument("--include-answer", action="store_true", help="Include AI-generated answer")
    search_parser.add_argument("--include-raw-content", action="store_true", help="Include full page content")
    search_parser.add_argument("--time-range", choices=["day", "week", "month", "year"], help="Time filter")
    search_parser.add_argument("--topic", choices=["general", "news"], default="general", help="Search topic")
    search_parser.add_argument("--include-domains", nargs="+", help="Include specific domains")
    search_parser.add_argument("--exclude-domains", nargs="+", help="Exclude specific domains")
    
    # Q&A command
    qna_parser = subparsers.add_parser("qna", help="Get direct answers to questions")
    qna_parser.add_argument("query", help="Question to answer")
    qna_parser.add_argument("--max-results", type=int, default=5, help="Number of sources")
    qna_parser.add_argument("--search-depth", choices=["basic", "comprehensive"], default="basic", help="Search depth")
    
    # Context command
    context_parser = subparsers.add_parser("context", help="Get context for RAG applications")
    context_parser.add_argument("query", help="Query to search")
    context_parser.add_argument("--max-tokens", type=int, default=4000, help="Maximum context tokens")
    context_parser.add_argument("--max-results", type=int, default=5, help="Number of sources")
    context_parser.add_argument("--search-depth", choices=["basic", "comprehensive"], default="comprehensive", help="Search depth")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    commands = {
        "search": search_command,
        "qna": qna_command,
        "context": context_command
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
