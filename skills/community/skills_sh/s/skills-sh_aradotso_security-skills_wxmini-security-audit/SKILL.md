---
name: wxmini-security-audit
description: Automated WeChat mini-program security auditing framework using Claude Code Agent Teams with 7 specialized agents for comprehensive static analysis
triggers:
  - audit this WeChat mini program
  - analyze this wxapkg directory for security issues
  - scan this mini program for vulnerabilities
  - perform security audit on WeChat app
  - check this WeChat mini program for sensitive data leaks
  - review this wxapkg for API security issues
  - run wxmini security analysis on this directory
  - decompile and audit this WeChat mini program
---

# wxmini-security-audit

> Skill by [ara.so](https://ara.so) — Security Skills collection.

Automated security auditing framework for WeChat mini-programs using Claude Code Agent Teams. Orchestrates 7 specialized agents to perform comprehensive static analysis covering sensitive information leakage, API endpoint extraction, cryptographic analysis, and vulnerability detection across seven security dimensions.

## What It Does

- **Multi-Agent Orchestration**: Coordinates 7 specialized agents (decompiler, secret scanner, endpoint miner, crypto analyzer, vulnerability analyzer, custom analyzer, reporter)
- **Dual-Layer Architecture**: Python regex scripts ensure 100% rule coverage, LLM agents provide intelligent analysis with context awareness
- **Parallel Phase 2 Execution**: Runs 4 analysis agents simultaneously to minimize audit time
- **User Intent Parsing**: Automatically triggers deep custom analysis when specific endpoints/parameters are mentioned
- **Pure Static Analysis**: Zero network requests, no attack code generation, fully local processing
- **Comprehensive Reporting**: Generates both summary reports and detailed documentation with structured data exports

## Architecture

The framework operates in sequential phases:

1. **Phase 0**: User intent parsing (extracts target path, creates output directory, parses requirements)
2. **Phase 1**: Decompilation (unveilr.exe processes wxapkg files, generates file inventory)
3. **Phase 1.5**: Script pre-scanning (Python regex extracts raw endpoints and secrets)
4. **Phase 2**: Parallel analysis (4 agents run simultaneously: SecretScanner, EndpointMiner, CryptoAnalyzer, VulnAnalyzer)
5. **Phase 2.5**: Custom analysis (triggered only when user specifies particular endpoints/parameters)
6. **Phase 3**: Report generation (aggregates findings into structured reports)

## Installation

### Prerequisites

- Claude Code CLI environment with Agent Teams/Skill support
- Python 3.x (standard library only, no external dependencies)
- Windows platform (current version requires unveilr.exe)
- unveilr.exe binary (WeChat mini-program decompiler)

### Setup

Clone the repository into your Claude Code Skills directory:

```bash
git clone https://github.com/sssmmmwww/wxmini-security-audit.git
cd wxmini-security-audit
```

Obtain `unveilr.exe` from the [unveilr project](https://github.com/nicholaschan23/unveilr) and place it in the `tools/` directory:

```
wxmini-security-audit/
├── SKILL.md
├── agents/
│   ├── agent-01-decompiler.md
│   ├── agent-02-secret-scanner.md
│   ├── agent-03-endpoint-miner.md
│   ├── agent-04-crypto-analyzer.md
│   ├── agent-05-vuln-analyzer.md
│   ├── agent-06-reporter.md
│   └── agent-07-custom-analyzer.md
└── tools/
    ├── unveilr.exe          # Place here
    └── scripts/
        ├── endpoint_extractor.py
        └── secret_scanner.py
```

## Usage

### Basic Audit

Trigger the audit by providing a mini-program directory path:

```
Audit this WeChat mini program D:\wechat\miniapp\wxapkg_files
```

```
Analyze this mini program for security issues C:\miniprogram\target
```

### Focused Analysis

Specify particular concerns to trigger Phase 2.5 custom analysis:

```
Audit this mini program D:\wxapp, focus on the /api/user/login endpoint
```

```
Scan D:\wxapp for vulnerabilities, particularly payment security and privilege escalation
```

### With External Tool Integration

Provide context from intercepting proxies:

```
Analyze this mini program D:\wxapp, Burp Suite captured the /api/pay endpoint with a tamperable amount parameter
```

### Output Structure

After completion, find results in `wxaudit-output/`:

```
wxaudit-output/
├── security_report.md          # Primary findings, risk assessment, remediation
├── api_endpoints_full.md       # Complete endpoint inventory
├── secrets_full.md             # All sensitive findings including false positives
├── findings.json               # Structured summary data
├── domains.txt                 # Extracted domain list
├── endpoints_fuzz.txt          # Fuzzing-ready endpoint list
├── file_inventory.json         # Decompiled file asset manifest
├── raw_endpoints.json          # Regex extraction raw results
├── raw_secrets.json            # Secret scanner raw results
├── secrets_report.json         # Intelligent secret analysis
├── api_endpoints.json          # Intelligent API analysis
├── crypto_analysis.json        # Cryptographic assessment
├── vuln_analysis.json          # Vulnerability findings
└── custom_analysis.json        # Custom requirement analysis (conditional)
```

## Python Script Layer

### Endpoint Extraction Script

Located at `tools/scripts/endpoint_extractor.py`, this script provides 100% rule coverage for API endpoint detection:

```python
import re
import json
import os

def extract_endpoints(source_dir):
    """
    Extract API endpoints from decompiled mini-program files.
    Returns: List of dicts with {pattern, file, line, context}
    """
    endpoints = []
    patterns = [
        r'https?://[^\s\'"]+',                    # Full URLs
        r'wx\.request\s*\(\s*\{[^}]+url\s*:\s*[\'"]([^\'"]+)',
        r'url\s*:\s*[\'"]([^\'"]+)[\'"]',         # Generic URL assignments
        r'/api/[a-zA-Z0-9/_-]+',                  # API path fragments
        r'baseURL\s*:\s*[\'"]([^\'"]+)[\'"]',     # Base URL configs
    ]
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if not file.endswith(('.js', '.json')):
                continue
            
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        for pattern in patterns:
                            for match in re.finditer(pattern, line):
                                endpoints.append({
                                    'pattern': pattern,
                                    'value': match.group(0),
                                    'file': filepath,
                                    'line': line_num,
                                    'context': line.strip()
                                })
            except Exception as e:
                continue
    
    return endpoints

if __name__ == '__main__':
    import sys
    source_dir = sys.argv[1]
    output_file = sys.argv[2]
    
    results = extract_endpoints(source_dir)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
```

### Secret Scanner Script

Located at `tools/scripts/secret_scanner.py`:

```python
import re
import json
import os

SECRET_PATTERNS = {
    'api_key': r'(?i)(api[_-]?key|apikey|key)\s*[:=]\s*[\'"]([a-zA-Z0-9_\-]{16,})[\'"]',
    'access_token': r'(?i)(access[_-]?token|accesstoken)\s*[:=]\s*[\'"]([a-zA-Z0-9_\-\.]{20,})[\'"]',
    'secret': r'(?i)(secret|app[_-]?secret)\s*[:=]\s*[\'"]([a-zA-Z0-9_\-]{16,})[\'"]',
    'password': r'(?i)(password|passwd|pwd)\s*[:=]\s*[\'"](.{6,})[\'"]',
    'private_key': r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----',
    'ip_internal': r'\b(?:10|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b',
    'phone': r'(?<![0-9])(1[3-9]\d{9})(?![0-9])',
    'id_card': r'[1-6]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]',
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'debug_flag': r'(?i)(debug|test|dev)[_-]?(mode|flag|env)\s*[:=]\s*(true|1|yes)',
}

def scan_secrets(source_dir):
    """
    Scan for sensitive information in source files.
    Returns: List of findings with {type, value, file, line, context}
    """
    findings = []
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if not file.endswith(('.js', '.json', '.xml')):
                continue
            
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        for secret_type, pattern in SECRET_PATTERNS.items():
                            for match in re.finditer(pattern, line):
                                findings.append({
                                    'type': secret_type,
                                    'value': match.group(0),
                                    'file': filepath,
                                    'line': line_num,
                                    'context': line.strip(),
                                    'severity': classify_severity(secret_type)
                                })
            except Exception as e:
                continue
    
    return findings

def classify_severity(secret_type):
    """Assign severity based on secret type."""
    critical = ['private_key', 'secret', 'api_key']
    high = ['access_token', 'password']
    medium = ['ip_internal', 'debug_flag']
    
    if secret_type in critical:
        return 'CRITICAL'
    elif secret_type in high:
        return 'HIGH'
    elif secret_type in medium:
        return 'MEDIUM'
    return 'LOW'

if __name__ == '__main__':
    import sys
    source_dir = sys.argv[1]
    output_file = sys.argv[2]
    
    results = scan_secrets(source_dir)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
```

## Agent Configuration

### Agent 02: SecretScanner

Receives `raw_secrets.json` from the script layer and performs intelligent filtering:

```markdown
# Role
You are a security analyst specializing in sensitive information leakage detection.

# Input
- file_inventory.json (file asset manifest)
- raw_secrets.json (script extraction results)

# Task
1. Load raw_secrets.json
2. Filter false positives:
   - Placeholder values (e.g., "YOUR_API_KEY", "example.com")
   - Comments and documentation
   - Test/demo code markers
3. Classify real findings by severity
4. Generate contextual risk assessment

# Output Format
secrets_report.json:
{
  "valid_findings": [
    {
      "type": "api_key",
      "value": "[REDACTED]",
      "file": "pages/user/login.js",
      "line": 42,
      "severity": "CRITICAL",
      "reasoning": "Hardcoded API key in production login flow",
      "recommendation": "Move to secure backend configuration"
    }
  ],
  "false_positives": [...],
  "summary": {
    "total_raw": 156,
    "valid": 23,
    "critical": 3,
    "high": 8,
    "medium": 12
  }
}
```

### Agent 03: EndpointMiner

Correlates endpoint fragments with BaseURL configurations:

```markdown
# Role
API endpoint extraction and intelligent correlation specialist.

# Input
- file_inventory.json
- raw_endpoints.json (script results)

# Task
1. Group endpoints by BaseURL
2. Reconstruct complete API URLs from fragments
3. Identify request methods from wx.request contexts
4. Map endpoints to source files
5. Flag suspicious patterns (internal IPs, non-HTTPS, hardcoded credentials in URLs)

# Output Format
api_endpoints.json:
{
  "domains": ["https://api.example.com", "https://backend.example.com"],
  "endpoints": [
    {
      "method": "POST",
      "url": "https://api.example.com/api/user/login",
      "base": "https://api.example.com",
      "path": "/api/user/login",
      "source_file": "utils/request.js",
      "line": 15,
      "params": ["username", "password"],
      "security_notes": ["Uses HTTPS", "No credential exposure"]
    }
  ]
}
```

### Agent 05: VulnAnalyzer

Performs vulnerability analysis across seven dimensions:

```markdown
# Vulnerability Analysis Dimensions

1. **Authentication & Authorization**
   - Token storage in localStorage
   - Session management flaws
   - Missing authentication checks

2. **Data Security**
   - Sensitive data in logs
   - Unencrypted storage
   - PII exposure

3. **Injection Vulnerabilities**
   - SQL injection vectors
   - XSS potential
   - Command injection

4. **Privilege Escalation**
   - Role-based access control bypasses
   - User ID manipulation risks

5. **Payment Security**
   - Amount tampering potential
   - Order verification gaps

6. **Information Leakage**
   - Error messages exposing internals
   - Debug mode in production
   - Version disclosure

7. **Configuration Security**
   - Insecure default settings
   - Missing security headers
   - Weak encryption algorithms

# Output Format
vuln_analysis.json with findings categorized by dimension and severity.
```

## Common Patterns

### Pattern 1: Basic Directory Audit

```
User: Audit this WeChat mini program D:\projects\wxapp
Agent: [Executes full 6-phase pipeline]
Output: wxaudit-output/ with 14 files
```

### Pattern 2: Targeted Endpoint Analysis

```
User: Analyze D:\wxapp, focus on /api/payment/submit
Agent: [Triggers Phase 2.5 CustomAnalyzer]
Output: Includes custom_analysis.json with deep dive on payment endpoint
```

### Pattern 3: Integration with Burp Suite

```
User: Audit D:\wxapp, Burp found /api/user/profile returns other users' data when changing uid parameter
Agent: [Correlates with extracted endpoints, flags in vuln_analysis.json under "Privilege Escalation"]
```

## Troubleshooting

### Issue: "unveilr.exe not found"

**Solution**: Download unveilr.exe and place in `tools/` directory:

```bash
# Verify placement
ls tools/unveilr.exe
# Should show: tools/unveilr.exe
```

### Issue: "No endpoints found in raw_endpoints.json"

**Cause**: Source directory contains only compiled wxapkg files, not decompiled JS.

**Solution**: Ensure Phase 1 (agent-01-decompiler) completes successfully. Check `file_inventory.json` for .js files:

```bash
cat wxaudit-output/file_inventory.json | grep ".js"
```

### Issue: "High false positive rate in secrets_full.md"

**Expected**: The dual-layer architecture intentionally preserves all script findings. Agent-02 filters these in `secrets_report.json`.

**Check**: Review `secrets_report.json` for filtered valid findings:

```bash
cat wxaudit-output/secrets_report.json | jq '.summary'
```

### Issue: "Custom analysis not triggered"

**Cause**: User prompt did not specify particular endpoints/parameters.

**Solution**: Explicitly mention target areas:

```
Analyze D:\wxapp, investigate the /api/order/create endpoint and its amount parameter
```

### Issue: "Script execution errors in Phase 1.5"

**Debug**: Check Python script output directly:

```bash
python tools/scripts/endpoint_extractor.py D:\decompiled_output wxaudit-output/raw_endpoints.json
python tools/scripts/secret_scanner.py D:\decompiled_output wxaudit-output/raw_secrets.json
```

## Security Constraints

This framework adheres to strict ethical boundaries:

1. **No Network Activity**: All analysis is local; no validation of extracted secrets/tokens
2. **No Attack Code**: Does not generate PoC exploits or automated attack scripts
3. **Minimal Permissions**: Read-only access to source directory, write-only to output directory
4. **Data Privacy**: No telemetry, no external uploads, all processing remains local

## Environment Variables

No environment variables required. All configuration is embedded in agent prompt files under `agents/`.

To customize agent behavior, edit the respective `.md` files:

```bash
# Example: Adjust SecretScanner sensitivity
vim agents/agent-02-secret-scanner.md
# Modify the false positive filtering rules section
```

## Advanced Usage

### Custom Vulnerability Rules

Extend `agent-05-vuln-analyzer.md` with project-specific patterns:

```markdown
# Custom Rules (add to agent-05-vuln-analyzer.md)

8. **Business Logic Flaws**
   - Check for discount code stacking vulnerabilities
   - Verify coupon expiration enforcement
   - Validate inventory deduction timing
```

### Integration with CI/CD

Run as part of security pipeline:

```bash
# Example GitLab CI job
security_audit:
  script:
    - claude-code execute-skill wxmini-security-audit "Audit ./decompiled_app"
    - cat wxaudit-output/findings.json | jq '.summary.critical' | grep -q '^0$' || exit 1
```

### Bulk Analysis

Process multiple mini-programs:

```bash
for dir in ./mini-programs/*/; do
  claude-code execute-skill wxmini-security-audit "Audit $dir"
  mv wxaudit-output "results/$(basename $dir)-audit"
done
```
