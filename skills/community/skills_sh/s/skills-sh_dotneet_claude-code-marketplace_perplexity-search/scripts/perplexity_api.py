#!/usr/bin/env python3
"""
Perplexity API Client Script

Provides command-line access to Perplexity API for:
- ask: General conversational AI with web search (sonar-pro)
- research: Deep research and analysis (sonar-deep-research)
- reason: Advanced reasoning tasks (sonar-reasoning-pro)
- search: Web search with ranked results
"""

import argparse
import json
import os
import re
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def get_api_key():
    """Get API key from environment variable."""
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        print("Error: PERPLEXITY_API_KEY environment variable is required", file=sys.stderr)
        sys.exit(1)
    return api_key


def get_timeout():
    """Get timeout from environment variable (default: 300 seconds)."""
    timeout_ms = os.environ.get("PERPLEXITY_TIMEOUT_MS", "300000")
    return int(timeout_ms) / 1000


def strip_thinking_tokens(content: str) -> str:
    """Remove <think>...</think> tags from content."""
    return re.sub(r'<think>[\s\S]*?</think>', '', content).strip()


def make_api_request(url: str, body: dict, api_key: str) -> dict:
    """Make a POST request to the Perplexity API."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    request = Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    timeout = get_timeout()

    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else "No response body"
        print(f"API Error: {e.code} {e.reason}\n{error_body}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Network Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except TimeoutError:
        print(f"Timeout Error: Request did not complete within {timeout}s", file=sys.stderr)
        sys.exit(1)


def chat_completion(messages: list, model: str, strip_thinking: bool = False) -> str:
    """
    Perform chat completion using Perplexity API.

    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Model to use (sonar-pro, sonar-deep-research, sonar-reasoning-pro)
        strip_thinking: If True, remove <think>...</think> tags from response

    Returns:
        Response content with citations appended
    """
    api_key = get_api_key()
    url = "https://api.perplexity.ai/chat/completions"

    body = {
        "model": model,
        "messages": messages,
    }

    data = make_api_request(url, body, api_key)

    # Extract message content
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

    # Strip thinking tokens if requested
    if strip_thinking:
        content = strip_thinking_tokens(content)

    # Append citations if available
    citations = data.get("citations", [])
    if citations:
        content += "\n\nCitations:\n"
        for i, citation in enumerate(citations, 1):
            content += f"[{i}] {citation}\n"

    return content


def web_search(query: str, max_results: int = 10, max_tokens_per_page: int = 1024, country: str = None) -> str:
    """
    Perform web search using Perplexity Search API.

    Args:
        query: Search query string
        max_results: Maximum number of results (1-20)
        max_tokens_per_page: Maximum tokens per page (256-2048)
        country: ISO country code for regional results

    Returns:
        Formatted search results
    """
    api_key = get_api_key()
    url = "https://api.perplexity.ai/search"

    body = {
        "query": query,
        "max_results": max_results,
        "max_tokens_per_page": max_tokens_per_page,
    }

    if country:
        body["country"] = country

    data = make_api_request(url, body, api_key)

    # Format results
    results = data.get("results", [])
    if not results:
        return "No search results found."

    output = f"Found {len(results)} search results:\n\n"

    for i, result in enumerate(results, 1):
        output += f"{i}. **{result.get('title', 'No title')}**\n"
        output += f"   URL: {result.get('url', 'N/A')}\n"
        if result.get("snippet"):
            output += f"   {result['snippet']}\n"
        if result.get("date"):
            output += f"   Date: {result['date']}\n"
        output += "\n"

    return output


def cmd_ask(args):
    """Handle 'ask' command."""
    messages = [{"role": "user", "content": args.query}]
    result = chat_completion(messages, "sonar-pro")
    print(result)


def cmd_research(args):
    """Handle 'research' command."""
    messages = [{"role": "user", "content": args.query}]
    result = chat_completion(messages, "sonar-deep-research", args.strip_thinking)
    print(result)


def cmd_reason(args):
    """Handle 'reason' command."""
    messages = [{"role": "user", "content": args.query}]
    result = chat_completion(messages, "sonar-reasoning-pro", args.strip_thinking)
    print(result)


def cmd_search(args):
    """Handle 'search' command."""
    result = web_search(
        args.query,
        max_results=args.max_results,
        max_tokens_per_page=args.max_tokens_per_page,
        country=args.country
    )
    print(result)


def main():
    parser = argparse.ArgumentParser(
        description="Perplexity API Client",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ask command
    ask_parser = subparsers.add_parser("ask", help="General question answering with web search")
    ask_parser.add_argument("query", help="Your question")
    ask_parser.set_defaults(func=cmd_ask)

    # research command
    research_parser = subparsers.add_parser("research", help="Deep research and comprehensive analysis")
    research_parser.add_argument("query", help="Research topic or question")
    research_parser.add_argument("--strip-thinking", action="store_true",
                                  help="Remove <think>...</think> tags from response")
    research_parser.set_defaults(func=cmd_research)

    # reason command
    reason_parser = subparsers.add_parser("reason", help="Advanced reasoning and problem-solving")
    reason_parser.add_argument("query", help="Reasoning task or problem")
    reason_parser.add_argument("--strip-thinking", action="store_true",
                                help="Remove <think>...</think> tags from response")
    reason_parser.set_defaults(func=cmd_reason)

    # search command
    search_parser = subparsers.add_parser("search", help="Web search with ranked results")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--max-results", type=int, default=10,
                               help="Maximum number of results (1-20, default: 10)")
    search_parser.add_argument("--max-tokens-per-page", type=int, default=1024,
                               help="Maximum tokens per page (256-2048, default: 1024)")
    search_parser.add_argument("--country", type=str,
                               help="ISO country code for regional results (e.g., JP, US)")
    search_parser.set_defaults(func=cmd_search)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
