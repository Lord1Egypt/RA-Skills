#!/usr/bin/env python3
"""
Telnyx Embeddings - Direct Text Embedding

Generate embedding vectors for text using Telnyx AI.
Returns raw vectors for use in custom applications.

Usage:
  ./embed.py "text to embed"
  ./embed.py --file input.txt
  echo "text" | ./embed.py --stdin
  ./embed.py "text" --json
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
    if os.environ.get("TELNYX_API_KEY"):
        return os.environ["TELNYX_API_KEY"]

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
    """Parse Telnyx API error response"""
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


def list_models(timeout=10):
    """List available embedding models from Telnyx API

    Returns:
        list: Model names, or None on error
    """
    api_key = load_credentials()
    url = "https://api.telnyx.com/v2/ai/openai/embeddings/models"
    headers = {
        "Authorization": "Bearer %s" % api_key,
        "Content-Type": "application/json",
        "User-Agent": "openclaw-telnyx-embeddings/1.0",
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode())
            return data.get("models", [])
    except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
        print("ERROR: Could not fetch models: %s" % e, file=sys.stderr)
        return None


def embed_text(text, model=None, timeout=30, max_retries=3):
    """Generate embedding vector for text using Telnyx AI

    Args:
        text (str): Text to embed
        model (str): Model name (optional — uses API default if not specified)
        timeout (int): Request timeout in seconds
        max_retries (int): Maximum retry attempts

    Returns:
        dict: Response with embedding vector or error info
    """
    api_key = load_credentials()

    url = "https://api.telnyx.com/v2/ai/openai/embeddings"

    payload_dict = {"input": text, "model": model or "thenlper/gte-large"}

    payload = json.dumps(payload_dict).encode()

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
                return normalize_embedding_response(response_data)

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")

            if e.code in [401, 403]:
                return {
                    "error": "HTTP %d" % e.code,
                    "details": parse_telnyx_error(error_body),
                }

            if e.code in [404, 422]:
                return {
                    "error": "HTTP %d" % e.code,
                    "details": parse_telnyx_error(error_body),
                }

            if attempt < max_retries - 1 and e.code >= 500:
                backoff = 2 ** attempt
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


def normalize_embedding_response(response_data):
    """Normalize embedding API response

    Expected format (OpenAI-compatible):
    {
        "data": [{"embedding": [0.1, 0.2, ...], "index": 0}],
        "model": "...",
        "usage": {"prompt_tokens": N, "total_tokens": N}
    }

    Args:
        response_data (dict): Raw API response

    Returns:
        dict: Normalized response
    """
    # Handle OpenAI-compatible format
    if "data" in response_data and isinstance(response_data["data"], list):
        embeddings = []
        for item in response_data["data"]:
            embedding = item.get("embedding", item.get("values", []))
            embeddings.append({
                "embedding": embedding,
                "index": item.get("index", len(embeddings)),
                "dimensions": len(embedding),
            })

        result = {"data": embeddings}

        if "model" in response_data:
            result["model"] = response_data["model"]
        if "usage" in response_data:
            result["usage"] = response_data["usage"]

        return result

    # Handle direct vector response
    if "embedding" in response_data:
        embedding = response_data["embedding"]
        return {
            "data": [{
                "embedding": embedding,
                "index": 0,
                "dimensions": len(embedding),
            }],
            "model": response_data.get("model", "unknown"),
        }

    # Unknown format — return as-is
    return response_data


def format_embedding(result):
    """Format embedding result for display

    Args:
        result (dict): Embedding result

    Returns:
        str: Formatted output
    """
    if "error" in result:
        lines = ["ERROR: %s" % result["error"]]
        if "details" in result:
            lines.append("  %s" % result["details"])
        return "\n".join(lines)

    if "data" not in result or not result["data"]:
        return "No embedding returned."

    lines = []
    for item in result["data"]:
        dims = item.get("dimensions", 0)
        embedding = item.get("embedding", [])

        lines.append("Dimensions: %d" % dims)

        if "model" in result:
            lines.append("Model: %s" % result["model"])

        if "usage" in result:
            usage = result["usage"]
            lines.append("Tokens: %s" % usage.get("total_tokens", "?"))

        # Show first/last few values as preview
        if len(embedding) > 8:
            preview = embedding[:4] + ["..."] + embedding[-4:]
        else:
            preview = embedding

        lines.append("Vector: [%s]" % ", ".join(str(v) for v in preview))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate embedding vectors using Telnyx AI"
    )
    parser.add_argument("text", nargs="*", help="Text to embed")
    parser.add_argument("--file", help="Read text from file")
    parser.add_argument("--stdin", action="store_true", help="Read text from stdin")
    parser.add_argument("--model", "-m", help="Embedding model name (default: thenlper/gte-large)")
    parser.add_argument("--list-models", action="store_true", help="List available embedding models")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--timeout", "-t", type=int, default=30, help="Request timeout in seconds")

    args = parser.parse_args()

    if args.list_models:
        models = list_models(timeout=args.timeout)
        if models is None:
            sys.exit(1)
        print("\nAvailable models:")
        for m in models:
            default = " (default)" if m == "thenlper/gte-large" else ""
            print("  %s%s" % (m, default))
        sys.exit(0)

    # Get text from one of the input sources
    text = None
    if args.file:
        try:
            with open(args.file, "r") as f:
                text = f.read().strip()
        except IOError as e:
            print("ERROR: Could not read file: %s" % e, file=sys.stderr)
            sys.exit(1)
    elif args.stdin or (not args.text and not sys.stdin.isatty()):
        text = sys.stdin.read().strip()
    elif args.text:
        text = " ".join(args.text)

    if not text:
        parser.print_help()
        print("\nProvide text as an argument, via --file, or piped via --stdin.")
        sys.exit(1)

    if not args.json:
        preview = text[:80] + "..." if len(text) > 80 else text
        print("\nEmbedding: \"%s\"\n" % preview)

    result = embed_text(text, model=args.model, timeout=args.timeout)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_embedding(result))


if __name__ == "__main__":
    main()
