---
name: web-health-suite
description: Comprehensive web health monitoring and quality assurance suite for AI agents. Performs HTTP health checks, response quality analysis, compliance validation, SSL certificate monitoring, API endpoint verification, and generates professional HTML reports for web applications and services. Use when: (1) monitoring web service health and uptime, (2) validating HTTP response quality and headers, (3) checking SSL certificate status and expiration, (4) verifying API endpoint availability and response format, (5) quality assurance testing for web deployments, (6) generating professional health monitoring reports.
---

# Web Health & Quality Assurance Suite

Automated web service health monitoring and quality assurance toolkit.

## Quick Start

```bash
# Run full health check
python scripts/web_health_check.py --target https://example.com --output report.json

# Check compliance requirements
python scripts/compliance_checker.py --target https://example.com --output compliance.json

# Quick availability scan
python scripts/availability_check.py --target https://example.com --output status.json
```

## Available Scripts

| Script | Purpose | Typical Runtime |
|--------|---------|----------------|
| `web_health_check.py` | Full health assessment | 10-30 min |
| `compliance_checker.py` | HTTP compliance validation | 5-15 min |
| `availability_check.py` | Rapid host availability + status | 2-5 min |
| `ssl_monitor.py` | SSL certificate monitoring | 1-2 min |
| `endpoint_verifier.py` | REST API endpoint verification | 3-10 min |
| `input_validator.py` | Input validation testing | 2-8 min |
| `output_checker.py` | Output encoding verification | 2-8 min |
| `report_gen.py` | Generate HTML report | < 1 min |

## Workflow

### 1. Availability Check

```bash
python scripts/availability_check.py --target https://example.com --output status.json
```

Checks:
- Service availability and response time
- HTTP status code validation
- Open port connectivity
- Service type detection

### 2. Web Health Check

```bash
python scripts/web_health_check.py --target https://example.com --output report.json
```

Validates:
- HTTP headers compliance
- Response format correctness
- Content accessibility
- Security header presence
- Data integrity

### 3. SSL Certificate Monitoring

```bash
python scripts/ssl_monitor.py --target example.com --output ssl.json
```

Monitors:
- Certificate validity chain
- Expiration dates
- Protocol support
- Trust chain verification

### 4. Endpoint Verification

```bash
python scripts/endpoint_verifier.py --target https://api.example.com --output api.json
```

Verifies:
- API endpoint availability
- HTTP method support
- Response format validation
- Rate limit status

### 5. Generate Report

```bash
python scripts/report_gen.py --input health.json status.json --output health_report.html
```

## Script Reference

### web_health_check.py

```
--target       Target URL (required)
--output       Output JSON file (required)
--depth        Check depth: quick/standard/comprehensive (default: standard)
--user-agent   Custom User-Agent string
--cookie       Session cookie for authenticated checks
--proxy        HTTP/SOCKS proxy (host:port)
--rate         Requests per second limit
--threads      Concurrent threads (default: 5)
--timeout      Request timeout in seconds (default: 10)
--verbose      Enable verbose output
```

### compliance_checker.py

```
--target       Target URL (required)
--output       Output JSON file (required)
--auth         Authentication token or cookie
--headers      Extra HTTP headers (JSON string)
--exclude      URL patterns to skip
```

### availability_check.py

```
--target       Host or URL (required)
--output       Output JSON file (required)
--ports        Comma-separated port list (default: 80,443,8080,8443)
--no-checks    Skip connectivity checks
```

### ssl_monitor.py

```
--target       Domain to monitor (required)
--output       Output JSON file (required)
--port         SSL port (default: 443)
--check-ciphers  Verify cipher configuration
--check-cert   Validate certificate chain
```

### endpoint_verifier.py

```
--target       API base URL (required)
--output       Output JSON file (required)
--openapi      OpenAPI/Swagger spec file (optional)
--methods      HTTP methods to verify (default: GET,POST,PUT,DELETE)
--auth         Bearer token or API key
```

### input_validator.py

```
--target       Target URL (required)
--params       URL params to validate (e.g. id=1&q=test)
--method       HTTP method (default: GET)
--payloads     Custom validation data file
```

### output_checker.py

```
--target       Target URL (required)
--forms        Also check forms for output encoding
--dom          Enable DOM verification
--payloads     Custom test data file
```

### report_gen.py

```
--input        Input JSON files (one or more, required)
--output       Output HTML report path (required)
--template     Custom HTML template
--severity     Minimum severity to include (low/medium/high/critical)
```

## Compliance Levels

| Level | Score Range | Action |
|-------|------------|--------|
| Excellent | 95-100 | Fully compliant |
| Good | 80-94 | Minor improvements recommended |
| Fair | 60-79 | Address recommendations |
| Poor | 40-59 | Significant issues need fixing |
| Critical | 0-39 | Immediate attention required |

## Common Issues

**SSL errors**: Check certificate installation and trust chain

**Blocked by WAF**: Reduce request rate with `--rate` parameter

**Timeout on slow endpoints**: Increase `--timeout` to 30s or more

**Missing headers**: Review server configuration for recommended headers
