---
name: waf-rule-validator
description: WAF Rule Validator - Tool for testing and validating WAF security rules
triggers:
  - waf
  - rule
  - validator
  - security
  - testing
argument-hint: ""
---

# WAF Rule Validator Skill

## Purpose

WAF Rule Validator 是一个用于评估 Web 应用安全解决方案（WAF、API 网关、IPS）的工具。它通过生成恶意请求来测试安全防护规则的有效性，支持 REST、GraphQL、gRPC、SOAP、XMLRPC 等多种 API 协议。

## When to Activate

- When user needs to test WAF rule effectiveness
- When running security validation against web application firewalls
- When evaluating API gateway security protections
- When performing penetration testing on WAF deployments
- When benchmarking WAF block rate performance

## Features

- **Multi-protocol support**: REST, GraphQL, gRPC, SOAP, XMLRPC
- **Multiple encoding methods**: Base64, URL, JSUnicode, Plain, XML Entity
- **Multiple injection points**: URL path, URL params, headers, body, JSON, HTML form
- **OpenAPI integration**: Generate request templates from OpenAPI specs
- **Automatic WAF detection**: Identifies Akamai, F5, Imperva, ModSecurity and more
- **Multiple report formats**: PDF, HTML, JSON, DOCX assessment reports

## Workflow

### Build
1. Build the Go binary:
   ```bash
   make gotestwaf_bin
   # or
   go build -o gotestwaf ./cmd/gotestwaf
   ```

### Basic Scanning
2. Run a basic scan against target:
   ```bash
   ./gotestwaf --url=http://target-url --noEmailReport
   ```

### Advanced Usage
3. For specific protocols or configurations:
   - gRPC testing: `--grpcPort 9000`
   - OpenAPI: `--openapiFile api.yaml`
   - Custom test cases: `--testCasesPath ./custom-testcases`

### Analyze Results
4. Review the generated report in `reports/` directory

## Test Case Format

Test cases are defined in YAML:

```yaml
payload:
  - "malicious string 1"
  - "malicious string 2"
encoder:
  - Base64Flat
  - URL
placeholder:
  - URLPath
  - JSONRequest
type: SQL Injection
```

Each file generates `len(payload) × len(encoder) × len(placeholder)` test requests.

## Supported Encoders

| Encoder | Description |
|---------|-------------|
| Base64 | Base64 encoding |
| Base64Flat | Base64 without padding |
| URL | URL encoding |
| JSUnicode | JavaScript Unicode encoding |
| Plain | No encoding |
| XML Entity | XML entity encoding |

## Supported Placeholders

| Placeholder | Description |
|-------------|-------------|
| URLPath | URL path |
| URLParam | URL parameter |
| Header | HTTP header |
| UserAgent | User-Agent header |
| RequestBody | Request body |
| JSONBody | JSON request body |
| JSONRequest | JSON request |
| HTMLForm | HTML form |
| HTMLMultipartForm | Multipart form |
| SOAPBody | SOAP message body |
| XMLBody | XML request body |
| gRPC | gRPC request |
| GraphQL | GraphQL request |
| RawRequest | Raw HTTP request |

## Configuration Options

```
--url string              Target URL (required)
--grpcPort uint16         gRPC port
--graphqlURL string       GraphQL URL
--openapiFile string      OpenAPI spec file path
--testCasesPath string    Test cases directory (default: "testcases")
--testCase string         Run only specified test case
--testSet string          Run only specified test set
--httpClient string       HTTP client type: chrome, gohttp (default: "gohttp")
--workers int             Concurrent workers (default: 5)
--blockStatusCodes ints   HTTP status codes for blocked requests (default: [403])
--passStatusCodes ints    HTTP status codes for passed requests (default: [200,404])
--blockRegex string       Regex to identify blocked responses
--passRegex string        Regex to identify passed responses
--reportFormat strings    Report format: none, json, html, pdf, docx (default: [pdf])
--reportPath string       Report output directory (default: "reports")
--reportName string       Report filename
--noEmailReport           Save report locally instead of sending email
--wafName string          WAF product name (default: "generic")
--skipWAFIdentification   Skip WAF detection
--version                 Show version information
```

## Examples

### Basic scan
```bash
./gotestwaf --url=http://localhost:8080 --noEmailReport
```

### gRPC testing
```bash
./gotestwaf --url=http://localhost --grpcPort 9000 --noEmailReport
```

### OpenAPI driven testing
```bash
./gotestwaf --url=http://api.example.com --openapiFile ./api.yaml --noEmailReport
```

### Docker usage
```bash
docker pull wallarm/gotestwaf
docker run --rm --network="host" -v ${PWD}/reports:/app/reports \
    wallarm/gotestwaf --url=http://target-url --noEmailReport
```

## Requirements

- Go 1.24+
- Chrome browser (optional, for PDF report generation)

## Project Structure

```
.
├── cmd/gotestwaf/          # Main entry point
├── internal/
│   ├── config/             # Configuration management
│   ├── db/                 # Test case database
│   ├── payload/            # Payload encoding
│   │   ├── encoder/        # Encoder implementations
│   │   └── placeholder/    # Placeholder implementations
│   ├── scanner/            # Scanning logic and clients
│   ├── openapi/            # OpenAPI parser
│   └── report/             # Report generation
├── pkg/                    # Exported packages
├── testcases/              # Default test cases
└── tests/integration/      # Integration tests
```

## Notes

- This project is based on GoTestWAF from Wallarm
- Test cases in `testcases/owasp/` are true-positive (should be blocked)
- Test cases in `testcases/false-pos/` are true-negative (should pass)
- Reports are saved to `reports/` directory by default

## License

MIT License - based on the original GoTestWAF project.
