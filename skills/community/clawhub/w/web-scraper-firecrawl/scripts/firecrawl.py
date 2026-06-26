#!/usr/bin/env python3
"""
Firecrawl CLI - Web scraping and content extraction tool

Usage:
    firecrawl scrape URL [options]
    firecrawl crawl URL [options]
    firecrawl map URL [options]
    firecrawl batch FILE [options]
    firecrawl extract URL --schema SCHEMA
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional

# API Configuration
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"


def make_api_request(endpoint: str, data: dict = None, method: str = "POST") -> dict:
    """Make API request to Firecrawl."""
    if not FIRECRAWL_API_KEY:
        print("Error: FIRECRAWL_API_KEY not set")
        print("Get your API key at: https://firecrawl.dev")
        sys.exit(1)
    
    url = f"{FIRECRAWL_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "GET":
            req = urllib.request.Request(url, headers=headers, method="GET")
        else:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode() if data else None,
                headers=headers,
                method=method
            )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"API Error: {e.code} {e.reason}")
        try:
            error_body = json.loads(e.read().decode())
            print(f"Details: {error_body}")
        except:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def poll_job(job_id: str, endpoint: str = "/scrape") -> dict:
    """Poll async job until complete."""
    print(f"Processing... (job: {job_id[:16]}...)")
    
    while True:
        result = make_api_request(f"{endpoint}/{job_id}", method="GET")
        status = result.get("status", "")
        
        if status == "completed":
            return result
        elif status == "failed":
            print(f"Job failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
        elif status == "cancelled":
            print("Job was cancelled")
            sys.exit(1)
        
        # Progress indicator
        print(".", end="", flush=True)
        time.sleep(2)


def scrape(args):
    """Scrape a single URL."""
    print(f"🔍 Scraping: {args.url}")
    
    payload = {
        "url": args.url,
        "formats": args.formats.split(",") if args.formats else ["markdown"],
    }
    
    if args.only_main_content:
        payload["onlyMainContent"] = True
    if args.wait_for:
        payload["waitFor"] = args.wait_for
    if args.timeout:
        payload["timeout"] = args.timeout
    
    result = make_api_request("/scrape", payload)
    
    if result.get("success"):
        data = result.get("data", {})
        
        # Output based on format
        if "markdown" in payload["formats"] and data.get("markdown"):
            print("\n" + "=" * 60)
            print("MARKDOWN CONTENT:")
            print("=" * 60)
            print(data["markdown"][:5000])  # Limit output
            if len(data["markdown"]) > 5000:
                print(f"\n... ({len(data['markdown'])} characters total)")
        
        if "html" in payload["formats"] and data.get("html"):
            print("\n" + "=" * 60)
            print("HTML CONTENT:")
            print("=" * 60)
            print(data["html"][:3000])
        
        # Metadata
        print("\n" + "=" * 60)
        print("METADATA:")
        print("=" * 60)
        metadata = data.get("metadata", {})
        print(f"  Title: {metadata.get('title', 'N/A')}")
        print(f"  Description: {metadata.get('description', 'N/A')[:100]}...")
        print(f"  Source URL: {metadata.get('sourceURL', 'N/A')}")
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Saved to: {args.output}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


def crawl(args):
    """Crawl a website."""
    print(f"🕷️  Crawling: {args.url}")
    print(f"   Limit: {args.limit} pages")
    
    payload = {
        "url": args.url,
        "limit": args.limit,
    }
    
    if args.max_depth:
        payload["maxDepth"] = args.max_depth
    if args.include:
        payload["includePaths"] = args.include.split(",")
    if args.exclude:
        payload["excludePaths"] = args.exclude.split(",")
    if args.formats:
        payload["scrapeOptions"] = {"formats": args.formats.split(",")}
    
    result = make_api_request("/crawl", payload)
    
    if result.get("success"):
        job_id = result.get("id")
        crawl_result = poll_job(job_id, "/crawl")
        
        pages = crawl_result.get("data", [])
        print(f"\n✅ Crawled {len(pages)} pages")
        
        # Summary
        for i, page in enumerate(pages[:10], 1):
            print(f"  {i}. {page.get('metadata', {}).get('sourceURL', 'N/A')}")
        if len(pages) > 10:
            print(f"  ... and {len(pages) - 10} more")
        
        # Save to directory
        if args.output:
            os.makedirs(args.output, exist_ok=True)
            for i, page in enumerate(pages):
                url = page.get('metadata', {}).get('sourceURL', f'page_{i}')
                filename = f"page_{i:03d}_{urlparse(url).netloc.replace('.', '_')}.md"
                filepath = os.path.join(args.output, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# {page.get('metadata', {}).get('title', 'Untitled')}\n\n")
                    f.write(f"Source: {url}\n\n")
                    f.write(page.get('markdown', ''))
            
            print(f"\n💾 Saved to: {args.output}/")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


def map_urls(args):
    """Map/discover URLs from a site."""
    print(f"🗺️  Mapping: {args.url}")
    
    payload = {"url": args.url}
    if args.search:
        payload["search"] = args.search
    if args.limit:
        payload["limit"] = args.limit
    
    result = make_api_request("/map", payload)
    
    if result.get("success"):
        links = result.get("data", [])
        print(f"\n✅ Found {len(links)} URLs")
        
        for i, link in enumerate(links[:20], 1):
            print(f"  {i}. {link}")
        if len(links) > 20:
            print(f"  ... and {len(links) - 20} more")
        
        # Save URL list
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                for link in links:
                    f.write(link + '\n')
            print(f"\n💾 Saved to: {args.output}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


def batch_scrape(args):
    """Batch scrape URLs from file."""
    # Read URLs from file
    with open(args.file, 'r') as f:
        content = f.read()
        try:
            urls = json.loads(content)
        except:
            urls = [line.strip() for line in content.split('\n') if line.strip()]
    
    print(f"📦 Batch scraping {len(urls)} URLs")
    
    payload = {
        "urls": urls,
        "formats": args.formats.split(",") if args.formats else ["markdown"],
    }
    
    result = make_api_request("/batch/scrape", payload)
    
    if result.get("success"):
        print("✅ Batch job started")
        # Note: Batch jobs are async, would need job tracking
        print(f"Job ID: {result.get('id', 'N/A')}")
        print("Check status at: https://firecrawl.dev/app")


def extract(args):
    """Extract structured data using schema."""
    print(f"📊 Extracting from: {args.url}")
    
    # Parse schema
    if os.path.exists(args.schema):
        with open(args.schema, 'r') as f:
            schema = json.load(f)
    else:
        schema = json.loads(args.schema)
    
    payload = {
        "url": args.url,
        "prompt": args.prompt if args.prompt else "Extract the requested information",
        "schema": schema
    }
    
    result = make_api_request("/extract", payload)
    
    if result.get("success"):
        data = result.get("data", {})
        print("\n✅ Extraction complete:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Saved to: {args.output}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


def main():
    parser = argparse.ArgumentParser(
        description="Firecrawl CLI - Web scraping tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  firecrawl scrape https://example.com
  firecrawl crawl https://docs.python.org --limit 50
  firecrawl map https://blog.example.com --search "tutorial"
  firecrawl extract https://example.com/product --schema '{"name":"h1"}'
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Scrape
    scrape_cmd = subparsers.add_parser("scrape", help="Scrape a single URL")
    scrape_cmd.add_argument("url", help="URL to scrape")
    scrape_cmd.add_argument("--formats", default="markdown", help="Output formats: markdown,html,links")
    scrape_cmd.add_argument("--only-main-content", action="store_true", help="Extract only main content")
    scrape_cmd.add_argument("--wait-for", type=int, help="Wait milliseconds for JS rendering")
    scrape_cmd.add_argument("--timeout", type=int, help="Request timeout in ms")
    scrape_cmd.add_argument("-o", "--output", help="Save output to file")
    
    # Crawl
    crawl_cmd = subparsers.add_parser("crawl", help="Crawl a website")
    crawl_cmd.add_argument("url", help="Starting URL")
    crawl_cmd.add_argument("--limit", type=int, default=10, help="Max pages to crawl")
    crawl_cmd.add_argument("--max-depth", type=int, help="Max crawl depth")
    crawl_cmd.add_argument("--include", help="Include patterns (comma-separated)")
    crawl_cmd.add_argument("--exclude", help="Exclude patterns (comma-separated)")
    crawl_cmd.add_argument("--formats", help="Output formats")
    crawl_cmd.add_argument("-o", "--output", help="Output directory")
    
    # Map
    map_cmd = subparsers.add_parser("map", help="Map/discover URLs")
    map_cmd.add_argument("url", help="Site URL")
    map_cmd.add_argument("--search", help="Search term to filter URLs")
    map_cmd.add_argument("--limit", type=int, help="Max URLs to return")
    map_cmd.add_argument("-o", "--output", help="Save URL list to file")
    
    # Batch
    batch_cmd = subparsers.add_parser("batch", help="Batch scrape URLs")
    batch_cmd.add_argument("file", help="File containing URLs (txt or json)")
    batch_cmd.add_argument("--formats", default="markdown", help="Output formats")
    batch_cmd.add_argument("--concurrency", type=int, default=5, help="Concurrent requests")
    batch_cmd.add_argument("-o", "--output", help="Output directory")
    
    # Extract
    extract_cmd = subparsers.add_parser("extract", help="Extract structured data")
    extract_cmd.add_argument("url", help="URL to extract from")
    extract_cmd.add_argument("--schema", required=True, help="JSON schema or schema file")
    extract_cmd.add_argument("--prompt", help="Extraction prompt")
    extract_cmd.add_argument("-o", "--output", help="Save to JSON file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Route commands
    commands = {
        "scrape": scrape,
        "crawl": crawl,
        "map": map_urls,
        "batch": batch_scrape,
        "extract": extract,
    }
    
    if args.command in commands:
        commands[args.command](args)


if __name__ == "__main__":
    main()
