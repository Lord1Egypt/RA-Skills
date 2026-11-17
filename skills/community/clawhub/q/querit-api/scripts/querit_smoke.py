#!/usr/bin/env python3
"""Smoke-test a Querit API key against /v1/search and /v1/contents.

Standard library only - nothing to install. Reads the key from QUERIT_API_KEY and
never prints it.

Examples:
    python3 querit_smoke.py --search "what does salesforce do"
    python3 querit_smoke.py --search "openclaw skills" --need-content --count 5
    python3 querit_smoke.py --contents https://example.com https://www.python.org
    python3 querit_smoke.py --search "quantum computing" --raw

Exit codes:
    0  request succeeded and the response matched the documented shape
    1  request failed (auth, rate limit, network, timeout, HTTP error)
    2  usage error (bad arguments, missing key)
"""

import argparse
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.request

SEARCH_URL = "https://api.querit.ai/v1/search"
CONTENTS_URL = "https://api.querit.ai/v1/contents"
MAX_CONTENTS_URLS = 10

HINTS = {
    401: "Key rejected. Check the header is 'Bearer <key>' and that the key is active.",
    403: "Forbidden - usually a per-endpoint subscription, not a bad key. A key valid "
         "for /v1/search does not automatically cover /v1/contents; read error_msg.",
    404: "Endpoint not found. Verify the URL path (/v1/search, /v1/contents).",
    422: "Request body rejected. Check parameter names and types.",
    429: "Rate limited. QPS is plan-dependent - throttle, then retry with backoff.",
}


def fail(message, code=1):
    print(f"FAIL: {message}", file=sys.stderr)
    return code


def read_key():
    key = os.environ.get("QUERIT_API_KEY", "").strip()
    if not key:
        print(
            "QUERIT_API_KEY is not set.\n"
            "  export QUERIT_API_KEY='<your key>'\n"
            "  Create a key on the Querit platform: https://www.querit.ai",
            file=sys.stderr,
        )
        return None
    return key


def post_json(url, payload, key, timeout):
    """POST JSON and return (status, body_or_none, raw_text, elapsed_ms)."""
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, method="POST")
    request.add_header("Authorization", f"Bearer {key}")
    request.add_header("Content-Type", "application/json")
    request.add_header("Accept", "application/json")

    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.getcode()
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        # An HTTP error still carries a body, and Querit puts error_msg in it.
        status = exc.code
        raw = exc.read().decode("utf-8", errors="replace")
    except socket.timeout:
        # Read timeouts surface here rather than as URLError, and on Python 3.9
        # socket.timeout is not a TimeoutError subclass.
        elapsed = (time.monotonic() - started) * 1000
        raise RuntimeError(
            f"client timeout after {elapsed:.0f} ms - raise --timeout and retry"
        )
    except urllib.error.URLError as exc:
        elapsed = (time.monotonic() - started) * 1000
        raise RuntimeError(f"network error after {elapsed:.0f} ms: {exc.reason}")
    except OSError as exc:
        elapsed = (time.monotonic() - started) * 1000
        raise RuntimeError(f"transport error after {elapsed:.0f} ms: {exc}")

    elapsed = (time.monotonic() - started) * 1000
    try:
        body = json.loads(raw)
    except json.JSONDecodeError:
        body = None
    return status, body, raw, elapsed


def report_transport(label, status, body, raw, elapsed):
    """Print the common envelope. Returns True when the call looks usable."""
    print(f"{label}")
    print(f"  http status  : {status}")
    print(f"  latency      : {elapsed:.0f} ms")

    if body is None:
        preview = raw[:300].replace("\n", " ")
        print(f"  body         : not JSON - {preview!r}")
        return False

    if "search_id" in body:
        print(f"  search_id    : {body.get('search_id')}  (quote this to support)")
    if body.get("took") is not None:
        print(f"  server took  : {body.get('took')}")
    if body.get("searchTime") is not None:
        print(f"  crawl time   : {body.get('searchTime')} s")

    error_code = body.get("error_code")
    if error_code is not None and error_code != 200:
        print(f"  error_code   : {error_code}")
        print(f"  error_msg    : {body.get('error_msg')}")

    if status != 200:
        hint = HINTS.get(status)
        if hint:
            print(f"  hint         : {hint}")
        return False
    return True


def run_search(args, key):
    payload = {
        "query": args.search,
        "count": args.count,
        "needContent": args.need_content,
    }
    filters = {}
    if args.language:
        filters["languages"] = {"include": [args.language]}
    if args.site:
        filters["sites"] = {"include": [args.site]}
    if filters:
        payload["filters"] = filters
    if args.chunks_per_doc:
        payload["chunksPerDoc"] = args.chunks_per_doc

    status, body, raw, elapsed = post_json(SEARCH_URL, payload, key, args.timeout)

    print(f"request      : POST /v1/search  {json.dumps(payload, ensure_ascii=False)}")
    ok = report_transport("response", status, body, raw, elapsed)
    if not ok:
        return 1

    if args.raw:
        print(json.dumps(body, indent=2, ensure_ascii=False))
        return 0

    results = body.get("results", {}).get("result")
    if results is None:
        print("  shape        : missing results.result - response does not match the "
              "documented contract")
        return 1

    executed = body.get("query_context", {}).get("query")
    print(f"  query echoed : {executed!r}")
    print(f"  results      : {len(results)}")

    if not results:
        print("  note         : zero results. Re-check the filters in the request "
              "before treating this as a relevance problem.")
        return 0

    with_text = 0
    for index, item in enumerate(results, start=1):
        sentences = item.get("sentence") or []
        if sentences:
            with_text += 1
        print(f"  [{index}] {item.get('title') or '(no title)'}")
        print(f"      url      : {item.get('url')}")
        print(f"      site     : {item.get('site_name')}   age: {item.get('page_age')}")
        snippet = (item.get("snippet") or "").replace("\n", " ")
        print(f"      snippet  : {snippet[:160]}")
        if sentences:
            first = sentences[0].replace("\n", " ")
            print(f"      text     : {len(sentences)} sentences, first: {first[:120]}")
        elif args.need_content:
            print("      text     : no sentence field (page text unavailable - "
                  "expected for some results)")

    if args.need_content:
        print(f"  text coverage: {with_text}/{len(results)} results carried page text")
        if with_text == 0:
            print("  note         : zero coverage across all results usually means the "
                  "account does not have the page-text option enabled.")
        elif with_text < len(results):
            print("  note         : partial coverage is normal. If every result needs "
                  "text, follow up with /v1/contents on the missing URLs.")
    return 0


def run_contents(args, key):
    urls = args.contents
    if len(urls) > MAX_CONTENTS_URLS:
        return fail(
            f"/v1/contents accepts at most {MAX_CONTENTS_URLS} URLs per call, "
            f"got {len(urls)}",
            2,
        )

    payload = {
        "urls": urls,
        "format": args.format,
        "crawlTimeout": args.crawl_timeout,
        "extrasMeta": True,
    }
    if args.timeout <= args.crawl_timeout:
        print(
            f"warning      : client timeout ({args.timeout}s) is not above "
            f"crawlTimeout ({args.crawl_timeout}s); the client may abort a request "
            f"the server would have finished",
            file=sys.stderr,
        )

    status, body, raw, elapsed = post_json(CONTENTS_URL, payload, key, args.timeout)

    print(f"request      : POST /v1/contents  {len(urls)} url(s), "
          f"format={args.format}, crawlTimeout={args.crawl_timeout}s")
    ok = report_transport("response", status, body, raw, elapsed)
    if not ok:
        return 1

    if args.raw:
        print(json.dumps(body, indent=2, ensure_ascii=False))
        return 0

    results = body.get("results")
    if results is None:
        print("  shape        : missing results - response does not match the "
              "documented contract")
        return 1

    # results and statuses are joined by id, never by position.
    status_by_id = {s.get("id"): s.get("status") for s in body.get("statuses", [])}
    succeeded, seen = 0, set()

    for index, item in enumerate(results, start=1):
        url = item.get("url")
        seen.add(url)
        crawl_status = status_by_id.get(item.get("id"), "unknown")
        content = item.get("content") or ""
        meta = item.get("extrasMeta") or {}
        if crawl_status == "success":
            succeeded += 1
        print(f"  [{index}] {url}")
        print(f"      status   : {crawl_status}")
        print(f"      content  : {len(content)} chars")
        print(f"      title    : {meta.get('title')}")
        print(f"      published: {meta.get('publishTime')}   site: {meta.get('siteName')}")
        if content:
            head = content[:160].replace("\n", " ")
            print(f"      preview  : {head}")

    missing = [u for u in urls if u not in seen]
    for url in missing:
        print(f"  [--] {url}\n      status   : absent from results")

    print(f"  crawl result : {succeeded}/{len(urls)} succeeded")
    if succeeded < len(urls):
        print("  note         : partial success is normal. Raise --crawl-timeout for "
              "slow pages; treat non-success as a fetch failure, not a blank page.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Verify a Querit API key and inspect real responses.",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--search", metavar="QUERY", help="run a /v1/search call")
    mode.add_argument("--contents", nargs="+", metavar="URL",
                      help="run a /v1/contents call on 1-10 URLs")

    parser.add_argument("--count", type=int, default=5,
                        help="search result count (default 5; capped at 10 or 20 by account)")
    parser.add_argument("--need-content", action="store_true",
                        help="request page text with search results")
    parser.add_argument("--chunks-per-doc", type=int,
                        help="summary chunks per document (most accounts are capped at 1)")
    parser.add_argument("--language", help="language filter value, e.g. english")
    parser.add_argument("--site", help="restrict search to a single site")
    parser.add_argument("--format", default="markdown",
                        choices=["text", "markdown", "html"],
                        help="contents output format (default markdown)")
    parser.add_argument("--crawl-timeout", type=int, default=10,
                        help="server-side crawl timeout in seconds, 1-60 (default 10)")
    parser.add_argument("--timeout", type=int, default=30,
                        help="client socket timeout in seconds (default 30)")
    parser.add_argument("--raw", action="store_true",
                        help="print the raw JSON response instead of a summary")

    args = parser.parse_args(argv)

    if args.count < 1:
        return fail("--count must be at least 1", 2)
    if not 1 <= args.crawl_timeout <= 60:
        return fail("--crawl-timeout must be between 1 and 60", 2)

    key = read_key()
    if not key:
        return 2

    try:
        if args.search:
            return run_search(args, key)
        return run_contents(args, key)
    except RuntimeError as exc:
        return fail(str(exc))
    except KeyboardInterrupt:
        return fail("interrupted")


if __name__ == "__main__":
    sys.exit(main())
