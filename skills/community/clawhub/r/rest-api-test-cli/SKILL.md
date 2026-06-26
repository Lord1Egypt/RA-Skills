---
name: api-tester
description: "REST API testing and validation toolkit. Send requests, validate responses, benchmark performance, generate HTML reports. Use when the user wants to: (1) Test a REST API endpoint, (2) Validate API responses against expectations, (3) Benchmark API endpoint performance, (4) Test all endpoints from an OpenAPI/Swagger spec, (5) Generate API test reports, (6) Debug HTTP responses including status codes, headers, and bodies."
---

# API Tester

Test, validate, and benchmark REST APIs with a single command. No external dependencies — uses only Python standard library.

## Quick start

```bash
# Test a single endpoint
python3 skills/api-tester/scripts/api_tester.py --url https://api.github.com/repos/openclaw/openclaw

# POST with JSON body
python3 skills/api-tester/scripts/api_tester.py \
  --url https://jsonplaceholder.typicode.com/posts \
  --method POST \
  --body '{"title":"test","body":"hello","userId":1}'

# Test with custom headers
python3 skills/api-tester/scripts/api_tester.py \
  --url https://api.example.com/secure \
  --headers '{"Authorization":"Bearer token123"}'
```

## Common commands

| Command | Action |
|---------|--------|
| `--url URL` | Target API endpoint (required) |
| `--method GET\|POST\|PUT\|DELETE\|PATCH` | HTTP method |
| `--headers '{"K":"V"}'` | Custom headers as JSON |
| `--body '{"key":"value"}'` | Request JSON body |
| `--body-file path.json` | Read body from file |
| `--verbose` | Show response body |
| `--validate` | Validate status code + response time |
| `--expected-status 201` | Expected HTTP status (default: 200) |
| `--validate-keys id name email` | Expected JSON keys in response |
| `--benchmark` | Run multiple iterations |
| `--iterations 10` | Benchmark iterations (default: 5) |
| `--max-time 5000` | Max acceptable time in ms (default: 3000) |
| `--timeout 60` | Request timeout (default: 30) |
| `--report` | Generate HTML test report |
| `--output report.html` | Save report to path |
| `--spec openapi.json --test-all` | Test all endpoints from spec |

## Validation

Validate API responses automatically:

```bash
python3 skills/api-tester/scripts/api_tester.py \
  --url https://jsonplaceholder.typicode.com/posts/1 \
  --validate --validate-keys userId id title body
```

Output:
```
Validation: ✅ PASS
  3/3 checks passed
  ✅ status_code: expected=200, actual=200
  ✅ response_time: expected=<3000ms, actual=234ms
  ✅ key_exists: userId: expected=present, actual=found
```

## Benchmarking

Test endpoint performance over multiple iterations:

```bash
python3 skills/api-tester/scripts/api_tester.py \
  --url https://jsonplaceholder.typicode.com/posts \
  --benchmark --iterations 10
```

Output:
```
Benchmark: GET https://jsonplaceholder.typicode.com/posts
  Iterations: 10
  Min:    142ms
  Max:    312ms
  Avg:    198ms
  Median: 189ms
  Success: 10/10
```

## HTML Reports

Generate a styled HTML report for sharing:

```bash
python3 skills/api-tester/scripts/api_tester.py \
  --url https://jsonplaceholder.typicode.com/posts/1 \
  --verbose --report
# Creates: api-test-report-20260510-133000.html
```

## Testing from OpenAPI Spec

Test all endpoints defined in an OpenAPI/Swagger specification:

```bash
python3 skills/api-tester/scripts/api_tester.py \
  --spec openapi.json \
  --test-all
```

## Requirements

- **Python 3.6+** (no pip install needed)
- Uses only `urllib` from standard library
- Works on Linux, macOS, Windows
- No external API calls
