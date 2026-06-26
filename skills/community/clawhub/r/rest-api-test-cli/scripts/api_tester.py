#!/usr/bin/env python3
"""api-tester: REST API testing and validation toolkit.

Usage:
    python3 api_tester.py --url https://api.example.com/users
    python3 api_tester.py --url https://api.example.com/login --method POST --body '{"user":"admin","pass":"secret"}'
    python3 api_tester.py --url https://api.example.com/users --headers '{"Authorization":"Bearer tok123"}' --validate
    python3 api_tester.py --spec openapi.json --test-all
    python3 api_tester.py --url https://api.example.com/slow --benchmark
    python3 api_tester.py --url https://api.example.com/users --report
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
import ssl
from datetime import datetime
from pathlib import Path


def make_request(url, method="GET", headers=None, body=None, timeout=30, follow_redirects=True):
    """Make HTTP request with detailed response capture."""
    req_headers = {
        "User-Agent": "api-tester/1.0",
        "Accept": "application/json, */*",
    }
    if headers:
        req_headers.update(headers)

    data = None
    if body and method in ("POST", "PUT", "PATCH"):
        if isinstance(body, dict):
            data = json.dumps(body).encode("utf-8")
            if "Content-Type" not in req_headers:
                req_headers["Content-Type"] = "application/json"
        elif isinstance(body, str):
            data = body.encode("utf-8")
            if not body.startswith("{") and "Content-Type" not in req_headers:
                req_headers["Content-Type"] = "application/x-www-form-urlencoded"

    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)

    ctx = ssl.create_default_context()
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED

    start = time.time()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            elapsed = time.time() - start
            body_bytes = resp.read()
            content_type = resp.headers.get("Content-Type", "")
            response_body = body_bytes.decode("utf-8") if body_bytes else ""

            result = {
                "success": True,
                "url": url,
                "method": method,
                "status_code": resp.status,
                "reason": resp.reason,
                "headers": dict(resp.headers),
                "response_time_ms": round(elapsed * 1000, 2),
                "response_size_bytes": len(body_bytes),
                "content_type": content_type,
                "body": response_body,
            }

            # Try to parse JSON body
            if "application/json" in content_type:
                try:
                    result["body_json"] = json.loads(response_body)
                except json.JSONDecodeError:
                    result["body_json"] = None
            return result

    except urllib.error.HTTPError as e:
        elapsed = time.time() - start
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        body_json = None
        try:
            body_json = json.loads(body)
        except (json.JSONDecodeError, ValueError):
            pass

        result = {
            "success": False,
            "url": url,
            "method": method,
            "status_code": e.code,
            "reason": str(e.reason) if hasattr(e, 'reason') else "HTTP Error",
            "headers": dict(e.headers) if e.headers else {},
            "response_time_ms": round(elapsed * 1000, 2),
            "response_size_bytes": len(body.encode()),
            "content_type": e.headers.get("Content-Type", "") if e.headers else "",
            "body": body[:10000],
            "body_json": body_json,
            "error": str(e),
        }
        return result

    except urllib.error.URLError as e:
        elapsed = time.time() - start
        return {
            "success": False,
            "url": url,
            "method": method,
            "status_code": 0,
            "reason": str(e.reason) if hasattr(e, 'reason') else str(e),
            "headers": {},
            "response_time_ms": round(elapsed * 1000, 2),
            "response_size_bytes": 0,
            "content_type": "",
            "body": "",
            "error": str(e),
        }

    except Exception as e:
        return {
            "success": False,
            "url": url,
            "method": method,
            "status_code": 0,
            "reason": str(e),
            "headers": {},
            "response_time_ms": 0,
            "response_size_bytes": 0,
            "content_type": "",
            "body": "",
            "error": str(e),
        }


def validate_response(result, expected_status=200, max_time_ms=3000, expected_keys=None):
    """Validate response against expectations."""
    checks = []
    passed = 0
    total = 0

    # Status code check
    total += 1
    if result["status_code"] == expected_status:
        checks.append({"check": "status_code", "expected": expected_status, "actual": result["status_code"], "passed": True})
        passed += 1
    else:
        checks.append({"check": "status_code", "expected": expected_status, "actual": result["status_code"], "passed": False})

    # Response time check
    total += 1
    if result["response_time_ms"] < max_time_ms:
        checks.append({"check": "response_time", "expected": f"<{max_time_ms}ms", "actual": f"{result['response_time_ms']}ms", "passed": True})
        passed += 1
    else:
        checks.append({"check": "response_time", "expected": f"<{max_time_ms}ms", "actual": f"{result['response_time_ms']}ms", "passed": False})

    # Key presence (if body_json exists)
    if expected_keys and result.get("body_json"):
        for key in expected_keys:
            total += 1
            if key in result["body_json"]:
                checks.append({"check": f"key_exists: {key}", "expected": "present", "actual": "found", "passed": True})
                passed += 1
            else:
                checks.append({"check": f"key_exists: {key}", "expected": "present", "actual": "not found", "passed": False})
    elif expected_keys and not result.get("body_json"):
        total += len(expected_keys)
        for key in expected_keys:
            checks.append({"check": f"key_exists: {key}", "expected": "present", "actual": "non-JSON response", "passed": False})

    # Overall
    return {
        "passed": passed,
        "total": total,
        "all_passed": passed == total,
        "checks": checks,
    }


def benchmark_endpoint(url, method="GET", headers=None, body=None, iterations=5):
    """Run multiple requests and report timing statistics."""
    times = []
    successes = 0
    failures = 0

    for i in range(iterations):
        result = make_request(url, method=method, headers=headers, body=body)
        times.append(result["response_time_ms"])
        if result["success"]:
            successes += 1
        else:
            failures += 1

    times.sort()
    avg = sum(times) / len(times)
    return {
        "url": url,
        "method": method,
        "iterations": iterations,
        "successes": successes,
        "failures": failures,
        "min_ms": round(times[0], 2),
        "max_ms": round(times[-1], 2),
        "avg_ms": round(avg, 2),
        "median_ms": round(times[len(times) // 2], 2),
        "all_times": times,
    }


def generate_html_report(results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = ""
    for r in results:
        status_class = "success" if r["success"] else "error"
        code = r["status_code"]
        code_color = "green" if 200 <= code < 300 else ("orange" if 300 <= code < 400 else "red")
        body_preview = ""
        if r["body_json"]:
            body_preview = json.dumps(r["body_json"], indent=2)[:2000]
        elif r["body"]:
            body_preview = r["body"][:1000]
        rows += f"""
        <tr class="{status_class}">
            <td>{r["method"]}</td>
            <td style="max-width:400px;word-break:break-all;">{r["url"]}</td>
            <td style="color:{code_color};font-weight:600;">{code}</td>
            <td>{r["response_time_ms"]}ms</td>
            <td>{r["response_size_bytes"]}B</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>API Test Report</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1100px; margin: 20px auto; padding: 0 20px; background: #f5f5f5; color: #333; }}
h1, h2 {{ color: #333; border-bottom: 2px solid #ddd; padding-bottom: 8px; }}
table {{ width: 100%; border-collapse: collapse; margin: 12px 0; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #eee; }}
th {{ background: #f0f0f0; font-weight: 600; }}
tr.success td {{ background: #f0fff0; }}
tr.error td {{ background: #fff0f0; }}
pre {{ background: #f8f8f8; padding: 12px; border-radius: 4px; overflow-x: auto; font-size: 13px; }}
code {{ font-size: 13px; }}
.footer {{ margin-top: 30px; color: #888; font-size: 12px; text-align: center; }}
.summary {{ display: flex; gap: 16px; margin: 16px 0; }}
.summary-item {{ background: white; border-radius: 6px; padding: 12px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); flex: 1; text-align: center; }}
.summary-num {{ font-size: 24px; font-weight: 700; display: block; }}
</style>
</head>
<body>
<h1>API Test Report</h1>
<p>Generated: {timestamp} | Results: {len(results)} endpoints</p>

<div class="summary">
    <div class="summary-item"><span class="summary-num">{sum(1 for r in results if r['success'])}</span> Success</div>
    <div class="summary-item"><span class="summary-num">{sum(1 for r in results if not r['success'])}</span> Failed</div>
    <div class="summary-item"><span class="summary-num">{round(sum(r['response_time_ms'] for r in results if r['response_time_ms'] > 0) / max(len([r for r in results if r['response_time_ms'] > 0]), 1), 1)}ms</span> Avg Response</div>
</div>

<h2>Results</h2>
<table>
<tr><th>Method</th><th>URL</th><th>Status</th><th>Time</th><th>Size</th></tr>
{rows}
</table>

<h2>Response Details</h2>
{''.join(f'<h3>{r["method"]} {r["url"]}</h3><pre><code>{json.dumps(r.get("body_json") or r.get("body",""), indent=2)[:2000]}</code></pre>' for r in results if r.get("body_json") or r.get("body"))}

<p class="footer">api-tester v1.0.0</p>
</body>
</html>"""
    return html


def print_result(result, verbose=False):
    """Print a single API test result."""
    icon = "✅" if result["success"] and 200 <= result["status_code"] < 400 else "❌"
    print(f"\n{icon}  {result['method']} {result['url']}")
    print(f"   Status: {result['status_code']} ({result['reason']})")
    print(f"   Time:   {result['response_time_ms']}ms")
    print(f"   Size:   {result['response_size_bytes']}B")

    if verbose and result.get("body_json"):
        print(f"\n   Body (JSON):")
        print(f"   {json.dumps(result['body_json'], indent=2)[:2000]}")
    elif verbose and result.get("body"):
        print(f"\n   Body:")
        print(f"   {result['body'][:500]}")


def try_parse_header(headers_str):
    """Parse header string. Supports JSON string or key:value pairs."""
    if not headers_str:
        return {}
    headers_str = headers_str.strip()
    if headers_str.startswith("{"):
        try:
            return json.loads(headers_str)
        except json.JSONDecodeError:
            pass
    # Try key:value pairs separated by newlines or commas
    result = {}
    for line in headers_str.replace(",", "\n").split("\n"):
        line = line.strip()
        if ":" in line:
            k, v = line.split(":", 1)
            result[k.strip()] = v.strip()
    return result


def main():
    parser = argparse.ArgumentParser(description="REST API Testing Toolkit")
    parser.add_argument("--url", "-u", help="Target URL")
    parser.add_argument("--method", "-X", default="GET", choices=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
    parser.add_argument("--headers", "-H", help='Request headers as JSON or "Key: Value" pairs')
    parser.add_argument("--body", "-d", help="Request body (string or JSON file path)")
    parser.add_argument("--body-file", help="Read body from file")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")
    parser.add_argument("--expected-status", type=int, default=200, help="Expected status code")
    parser.add_argument("--validate", action="store_true", help="Validate response against defaults")
    parser.add_argument("--validate-keys", nargs="*", help="Expected JSON keys in response")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmark (multiple iterations)")
    parser.add_argument("--iterations", type=int, default=5, help="Benchmark iterations")
    parser.add_argument("--report", "-r", action="store_true", help="Generate HTML report")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Detailed output")
    parser.add_argument("--spec", help="OpenAPI/Swagger spec file path (experimental)")
    parser.add_argument("--test-all", action="store_true", help="Test all endpoints from spec (requires --spec)")
    parser.add_argument("--max-time", type=int, default=3000, help="Max acceptable response time in ms")
    args = parser.parse_args()

    # Parse headers
    headers = try_parse_header(args.headers)

    # Parse body
    body = args.body
    if args.body_file:
        try:
            with open(args.body_file) as f:
                body = f.read()
        except FileNotFoundError:
            print(f"Error: body file not found: {args.body_file}")
            sys.exit(1)

    # Try to parse body as JSON dict
    body_dict = None
    if body:
        try:
            body_dict = json.loads(body) if isinstance(body, str) else body
        except (json.JSONDecodeError, TypeError):
            pass

    all_results = []

    if args.spec and args.test_all:
        # Test from spec file
        try:
            with open(args.spec) as f:
                spec = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading spec: {e}")
            sys.exit(1)

        base_url = args.url or ""
        paths = spec.get("paths", {})
        total = 0
        tested = 0
        for path, methods in paths.items():
            for method in methods:
                if method.upper() in ("GET", "POST", "PUT", "DELETE", "PATCH"):
                    total += 1
                    if args.test_all:
                        tested += 1
                        full_url = base_url + path
                        print(f"  [{tested}/{total}] {method.upper()} {full_url}")
                        result = make_request(full_url, method=method.upper(), headers=headers, timeout=args.timeout)
                        all_results.append(result)
                        print(f"    → {result['status_code']} ({result['response_time_ms']}ms)")
        print(f"\nTested {tested} endpoints from spec.")

    elif args.url:
        if args.benchmark:
            result = benchmark_endpoint(args.url, method=args.method, headers=headers, body=body_dict or body, iterations=args.iterations)
            print(f"\nBenchmark: {args.method} {args.url}")
            print(f"  Iterations: {result['iterations']}")
            print(f"  Min:    {result['min_ms']}ms")
            print(f"  Max:    {result['max_ms']}ms")
            print(f"  Avg:    {result['avg_ms']}ms")
            print(f"  Median: {result['median_ms']}ms")
            print(f"  Success: {result['successes']}/{result['iterations']}")
            all_results.append(result)
        else:
            result = make_request(args.url, method=args.method, headers=headers, body=body_dict or body, timeout=args.timeout)
            all_results.append(result)
            print_result(result, verbose=args.verbose)

            if args.validate:
                validation = validate_response(result, expected_status=args.expected_status, max_time_ms=args.max_time, expected_keys=args.validate_keys)
                print(f"\nValidation: {'✅ PASS' if validation['all_passed'] else '❌ FAIL'}")
                print(f"  {validation['passed']}/{validation['total']} checks passed")
                for check in validation["checks"]:
                    icon = "✅" if check["passed"] else "❌"
                    print(f"  {icon} {check['check']}: expected={check['expected']}, actual={check['actual']}")

        if args.report:
            html = generate_html_report(all_results)
            output_path = args.output or f"api-test-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"
            with open(output_path, "w") as f:
                f.write(html)
            print(f"\nReport saved: {output_path}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
