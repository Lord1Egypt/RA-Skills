#!/usr/bin/env python3
"""
Telnyx Embeddings - Semantic Search

Search any Telnyx Storage bucket using natural language.
Query embedding is handled server-side — only TELNYX_API_KEY required.
No OpenAI or Google API keys needed.

Usage:
  ./search.py "what are the project requirements?"
  ./search.py "meeting notes" --bucket my-bucket --num 10
  ./search.py "API limits" --json
  ./search.py "deployment" --timeout 45
"""

import os
import sys
import json
import urllib.request
import urllib.error
import time
import argparse


# Default configuration
DEFAULT_CONFIG = {
    "bucket": "openclaw-main",
    "region": "us-central-1",
    "default_num_docs": 5,
}


def load_config():
    """Load configuration from file or defaults"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                user_config = json.load(f)
                return {**DEFAULT_CONFIG, **user_config}
        except (json.JSONDecodeError, IOError):
            pass
    return DEFAULT_CONFIG


def load_credentials():
    """Load Telnyx API key from environment or .env file

    Returns:
        str: The Telnyx API key

    Raises:
        SystemExit: If no API key found
    """
    # Check environment first
    if os.environ.get("TELNYX_API_KEY"):
        return os.environ["TELNYX_API_KEY"]

    # Check for .env file in skill directory
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("TELNYX_API_KEY="):
                    return line.split("=", 1)[1].strip('"').strip("'")

    print("ERROR: No Telnyx API key found", file=sys.stderr)
    print("Set TELNYX_API_KEY environment variable or create .env file with:", file=sys.stderr)
    print("  TELNYX_API_KEY=your-api-key", file=sys.stderr)
    sys.exit(1)


def parse_telnyx_error(error_body):
    """Parse Telnyx API error response for better error messages

    Args:
        error_body (str): Raw error response body

    Returns:
        str: Human-readable error message
    """
    try:
        error_data = json.loads(error_body)
        if "errors" in error_data and error_data["errors"]:
            error = error_data["errors"][0]
            code = error.get("code", "unknown")
            detail = error.get("detail", "No details provided")
            return "%s: %s" % (code, detail)
        elif "message" in error_data:
            return error_data["message"]
        else:
            return error_body.strip()
    except (json.JSONDecodeError, KeyError):
        return error_body.strip()


def normalize_response(response_data):
    """Normalize API response format for consistent handling

    Args:
        response_data (dict): Raw API response

    Returns:
        dict: Normalized response with consistent field names
    """
    if "data" in response_data and isinstance(response_data["data"], list):
        normalized_data = []
        for doc in response_data["data"]:
            normalized_doc = {
                "content": doc.get("document_chunk", doc.get("content", "")),
                "source": doc.get("metadata", {}).get("filename", doc.get("file_name", "unknown")),
                "certainty": doc.get("metadata", {}).get("certainty", doc.get("certainty", 0)),
                "distance": doc.get("distance", 0),
            }
            normalized_data.append(normalized_doc)

        return {"data": normalized_data}

    return response_data


def similarity_search(query, num_docs=5, bucket_name=None, timeout=30, max_retries=3):
    """Search using Telnyx similarity search API with retry logic

    Args:
        query (str): Search query text
        num_docs (int): Number of documents to return
        bucket_name (str): Override bucket name from config
        timeout (int): Request timeout in seconds
        max_retries (int): Maximum retry attempts

    Returns:
        dict: API response with search results or error info
    """
    config = load_config()
    api_key = load_credentials()

    bucket = bucket_name or config["bucket"]

    url = "https://api.telnyx.com/v2/ai/embeddings/similarity-search"

    payload = json.dumps({
        "bucket_name": bucket,
        "query": query,
        "num_docs": num_docs,
    }).encode()

    headers = {
        "Authorization": "Bearer %s" % api_key,
        "Content-Type": "application/json",
        "User-Agent": "openclaw-telnyx-embeddings/1.0",
    }

    for attempt in range(max_retries):
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                response_data = json.loads(response.read().decode())
                return normalize_response(response_data)

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")

            # Don't retry on auth/client errors
            if e.code in [401, 403, 404]:
                return {
                    "error": "HTTP %d" % e.code,
                    "details": parse_telnyx_error(error_body),
                }

            # Retry on 5xx errors
            if attempt < max_retries - 1 and e.code >= 500:
                backoff = 2 ** attempt  # 1, 2, 4 seconds
                time.sleep(backoff)
                continue
            else:
                return {
                    "error": "HTTP %d" % e.code,
                    "details": parse_telnyx_error(error_body),
                }

        except (urllib.error.URLError, OSError) as e:
            if attempt < max_retries - 1:
                backoff = 2 ** attempt
                time.sleep(backoff)
                continue
            else:
                return {"error": "Network error: %s" % str(e)}

        except Exception as e:
            return {"error": "Unexpected error: %s" % str(e)}

    return {"error": "Max retries exceeded"}


def format_results(results, max_content_chars=500):
    """Format search results for display

    Args:
        results (dict): Search results from API
        max_content_chars (int): Maximum characters to display per result

    Returns:
        str: Formatted results string
    """
    if "error" in results:
        return "Error: %s\n%s" % (results["error"], results.get("details", ""))

    if "data" not in results or not results["data"]:
        return "No results found."

    output = []
    for i, doc in enumerate(results["data"], 1):
        certainty = doc.get("certainty", 0)
        filename = doc.get("source", "unknown")
        content = doc.get("content", "")

        display_content = content[:max_content_chars]

        # Certainty indicator
        if certainty >= 0.9:
            conf = "[HIGH]"
        elif certainty >= 0.85:
            conf = "[MED]"
        else:
            conf = "[LOW]"

        output.append("--- Result %d %s (certainty: %.3f) ---" % (i, conf, certainty))
        output.append("Source: %s" % filename)
        output.append("")
        output.append(display_content)
        if len(content) > max_content_chars:
            output.append("...[truncated]")
        output.append("")

    return "\n".join(output)


def search(query, num_docs=5, bucket_name=None, output_json=False, timeout=30):
    """Main search function

    Args:
        query (str): Search query
        num_docs (int): Number of results to return
        bucket_name (str): Override bucket name
        output_json (bool): Return JSON instead of formatted text
        timeout (int): Request timeout in seconds

    Returns:
        str: Formatted results or JSON string
    """
    results = similarity_search(query, num_docs, bucket_name, timeout)

    if output_json:
        return json.dumps(results, indent=2)
    else:
        return format_results(results)


def main():
    parser = argparse.ArgumentParser(
        description="Semantic search using Telnyx AI embeddings"
    )
    parser.add_argument("query", nargs="*", help="Search query")
    parser.add_argument("--num", "-n", type=int, default=None, help="Number of results")
    parser.add_argument("--bucket", "-b", help="Bucket name to search")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--full", "-f", action="store_true", help="Show full content (no truncation)")
    parser.add_argument("--timeout", "-t", type=int, default=30, help="Request timeout in seconds")

    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        sys.exit(1)

    query = " ".join(args.query)
    config = load_config()
    num_docs = args.num or config.get("default_num_docs", 5)

    if not args.json:
        bucket_info = " (bucket: %s)" % args.bucket if args.bucket else ""
        print("\nSearching: \"%s\"%s\n" % (query, bucket_info))

    results = search(
        query=query,
        num_docs=num_docs,
        bucket_name=args.bucket,
        output_json=args.json,
        timeout=args.timeout,
    )

    print(results)


if __name__ == "__main__":
    main()
