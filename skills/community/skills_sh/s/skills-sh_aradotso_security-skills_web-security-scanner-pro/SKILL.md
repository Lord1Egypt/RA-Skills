---
name: web-security-scanner-pro
description: Advanced Python web security scanner with 49 modules, evasion engine, CVE database, and WAF bypass for penetration testing
triggers:
  - scan website for vulnerabilities
  - run security audit on web application
  - test for SQL injection and XSS
  - check WordPress security issues
  - bypass WAF and scan protected site
  - detect web server vulnerabilities
  - generate security assessment report
  - perform penetration test on website
---

# Web Security Scanner Pro Skill

> Skill by [ara.so](https://ara.so) — Security Skills collection.

Expert skill for using Web Security Scanner Pro, a comprehensive Python-based web security scanner with 49 modules for vulnerability detection, WAF evasion, and automated security testing.

## What This Project Does

Web Security Scanner Pro (WSA Pro) is an open-source security testing tool that:

- **Scans for 49 vulnerability types** including XSS, SQLi, LFI, RFI, XXE, SSTI, CSRF, command injection
- **Tests CMS platforms** (WordPress with 9 modules, Joomla, Drupal)
- **Detects misconfigurations** in web servers (Apache, Nginx, IIS, LiteSpeed, Tomcat)
- **Identifies vulnerable software** via built-in CVE database (2024-2026)
- **Evades detection** with WAF bypass, user-agent rotation, rate limiting, proxy support
- **Generates professional reports** in HTML, PDF, Markdown, and JSON formats
- **Provides REST API** for automation and CI/CD integration

The scanner includes advanced SQL injection detection (error-based, boolean-blind, time-based blind, UNION-based) and can identify 9 different WAFs (Cloudflare, Sucuri, ModSecurity, etc.).

## Installation

### Prerequisites

```bash
# Requires Python 3.9+
python --version

# Install from GitHub
git clone https://github.com/miladrezanezhad/web-security-scanner-pro.git
cd web-security-scanner-pro
pip install -r requirements.txt
```

### Dependencies

The project requires these key Python packages:
- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing
- `pyyaml` - Configuration
- `jinja2` - Report templates
- `reportlab` - PDF generation
- `flask` - REST API server

## Key Commands

### Basic Usage

```bash
# Interactive mode (menu-driven interface)
python main.py

# Quick scan (4 critical modules)
python main.py quick https://example.com

# Full scan (all 49 modules)
python main.py scan https://example.com

# Specific modules only
python main.py scan https://example.com --modules wordpress,xss,sqli,ssl

# Stealth mode for WAF-protected sites
python main.py scan https://example.com --mode stealth

# Aggressive mode (faster, more detectable)
python main.py scan https://example.com --mode aggressive

# Generate multiple report formats
python main.py scan https://example.com --format html pdf json markdown

# Use proxy
python main.py scan https://example.com --proxy http://127.0.0.1:8080

# Custom rate limiting
python main.py scan https://example.com --delay 2 --timeout 30
```

### Module Categories

```bash
# CMS scanning
python main.py scan https://example.com --modules wordpress,joomla,drupal

# Vulnerability testing
python main.py scan https://example.com --modules xss,sqli,lfi,xxe,ssti,csrf

# Server fingerprinting
python main.py scan https://example.com --modules apache,nginx,php,mysql

# Control panel detection
python main.py scan https://example.com --modules cpanel,directadmin,plesk

# SSL/TLS testing
python main.py scan https://example.com --modules ssl,headers

# API security
python main.py scan https://example.com --modules graphql,rest_api,jwt
```

## Configuration

### config.yaml Structure

```yaml
# Core settings
scanner:
  timeout: 30
  max_retries: 3
  threads: 10
  user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Evasion settings
evasion:
  enabled: true
  user_agent_rotation: true
  random_delay: true
  min_delay: 1
  max_delay: 3
  exponential_backoff: true
  
# Proxy configuration
proxy:
  enabled: false
  http: ""
  https: ""
  socks5: ""
  tor: false
  
# Module configuration
modules:
  enabled:
    - wordpress
    - xss
    - sqli
    - ssl
    - headers
  disabled:
    - aggressive_fuzzing

# Report settings
reporting:
  output_dir: "reports/output"
  default_format: "html"
  include_screenshots: false
  
# CVE database
database:
  auto_update: true
  update_interval: 7  # days
  severity_filter: ["CRITICAL", "HIGH", "MEDIUM"]
```

### Environment Variables

```bash
# Set proxy via environment
export HTTP_PROXY="http://127.0.0.1:8080"
export HTTPS_PROXY="http://127.0.0.1:8080"

# API server configuration
export WSA_API_HOST="0.0.0.0"
export WSA_API_PORT="5000"
export WSA_API_KEY="your-secret-key-here"

# Database credentials (if needed)
export DB_HOST="localhost"
export DB_USER="scanner"
export DB_PASS="${DB_PASSWORD}"
```

## Python API Usage

### Programmatic Scanning

```python
from core.scanner import SecurityScanner
from core.browser import StealthBrowser
from core.evasion import EvasionEngine

# Initialize scanner
scanner = SecurityScanner(
    target="https://example.com",
    modules=["wordpress", "xss", "sqli"],
    mode="stealth"
)

# Configure evasion
scanner.evasion = EvasionEngine(
    user_agent_rotation=True,
    random_delay=True,
    waf_detection=True
)

# Run scan
results = scanner.scan()

# Access findings
for finding in results.get_findings():
    print(f"{finding.severity}: {finding.title}")
    print(f"  Module: {finding.module}")
    print(f"  Description: {finding.description}")
    print(f"  Remediation: {finding.remediation}")
```

### Custom Module Development

```python
from modules.base import BaseModule

class CustomScanModule(BaseModule):
    """Custom security scanning module."""
    
    def __init__(self, browser):
        super().__init__(browser)
        self.name = "custom_scan"
        self.description = "Custom vulnerability detection"
        
    def run(self, target):
        """Execute custom scan logic."""
        findings = []
        
        # Make HTTP request
        response = self.browser.get(target)
        
        # Check for vulnerability
        if self._check_vulnerability(response):
            findings.append({
                "severity": "HIGH",
                "title": "Custom Vulnerability Detected",
                "description": "Found custom security issue",
                "url": target,
                "evidence": response.text[:200],
                "remediation": "Apply custom fix"
            })
            
        return findings
        
    def _check_vulnerability(self, response):
        """Custom vulnerability detection logic."""
        return "vulnerable_pattern" in response.text.lower()

# Register and use custom module
scanner.register_module(CustomScanModule)
```

### Advanced SQL Injection Testing

```python
from modules.vulnerabilities.sqli import SQLInjectionScanner

# Initialize SQLi scanner
sqli_scanner = SQLInjectionScanner(browser)

# Test specific parameter
result = sqli_scanner.test_parameter(
    url="https://example.com/page.php",
    parameter="id",
    value="1"
)

if result.vulnerable:
    print(f"SQLi Type: {result.injection_type}")  # error, boolean, time, union
    print(f"Database: {result.database_type}")    # mysql, postgresql, mssql
    print(f"Payload: {result.payload}")
    print(f"Evidence: {result.evidence}")

# Advanced time-based detection
time_result = sqli_scanner.test_time_based(
    url="https://example.com/search",
    parameter="q",
    delay=5  # seconds
)
```

### WAF Detection and Bypass

```python
from core.evasion import EvasionEngine

evasion = EvasionEngine()

# Detect WAF
waf_info = evasion.detect_waf("https://example.com")
if waf_info["detected"]:
    print(f"WAF Detected: {waf_info['name']}")
    print(f"Confidence: {waf_info['confidence']}")
    
    # Apply WAF-specific bypass techniques
    evasion.apply_bypass_techniques(waf_info['name'])

# Test bypass effectiveness
bypass_success = evasion.test_bypass(
    url="https://example.com",
    payload="<script>alert(1)</script>"
)

# Supported WAFs:
# - Cloudflare
# - Sucuri
# - Wordfence
# - AWS WAF
# - ModSecurity
# - Akamai
# - Imperva
# - F5 BIG-IP
# - Barracuda
```

### Report Generation

```python
from core.reporter import ReportGenerator

# Initialize reporter
reporter = ReportGenerator(scan_results)

# Generate HTML report with charts
html_report = reporter.generate_html(
    output_file="reports/output/scan_report.html",
    include_charts=True,
    include_screenshots=False
)

# Generate PDF report
pdf_report = reporter.generate_pdf(
    output_file="reports/output/scan_report.pdf",
    company_name="Security Corp",
    tester_name="John Doe"
)

# Generate JSON for automation
json_report = reporter.generate_json(
    output_file="reports/output/scan_report.json",
    pretty_print=True
)

# Markdown for GitHub
md_report = reporter.generate_markdown(
    output_file="reports/output/scan_report.md"
)
```

### CVE Database Queries

```python
from core.database import VulnerabilityDatabase

# Initialize CVE database
cve_db = VulnerabilityDatabase()

# Search for WordPress vulnerabilities
wp_vulns = cve_db.search_by_software(
    software="WordPress",
    version="6.4.2"
)

for vuln in wp_vulns:
    print(f"CVE: {vuln.cve_id}")
    print(f"CVSS: {vuln.cvss_score}")
    print(f"Severity: {vuln.severity}")
    print(f"Description: {vuln.description}")

# Search by CVE ID
cve_info = cve_db.get_by_cve("CVE-2024-12345")

# Filter by severity
critical_vulns = cve_db.filter_by_severity("CRITICAL")

# Update database
cve_db.update_database()
```

## REST API Usage

### Start API Server

```bash
# Start REST API server
python -m core.api --host 0.0.0.0 --port 5000

# With authentication
export WSA_API_KEY="your-secret-key"
python -m core.api --host 0.0.0.0 --port 5000 --auth
```

### API Endpoints

```python
import requests

API_BASE = "http://localhost:5000/api/v1"
API_KEY = os.getenv("WSA_API_KEY")
headers = {"X-API-Key": API_KEY}

# Start new scan
response = requests.post(
    f"{API_BASE}/scan",
    headers=headers,
    json={
        "target": "https://example.com",
        "modules": ["wordpress", "xss", "sqli"],
        "mode": "stealth",
        "report_format": ["html", "json"]
    }
)
scan_id = response.json()["scan_id"]

# Check scan status
status = requests.get(
    f"{API_BASE}/scan/{scan_id}/status",
    headers=headers
)
print(status.json())

# Get scan results
results = requests.get(
    f"{API_BASE}/scan/{scan_id}/results",
    headers=headers
)

# Download report
report = requests.get(
    f"{API_BASE}/scan/{scan_id}/report?format=html",
    headers=headers
)

# List available modules
modules = requests.get(
    f"{API_BASE}/modules",
    headers=headers
)

# Get CVE information
cve_info = requests.get(
    f"{API_BASE}/cve/CVE-2024-12345",
    headers=headers
)
```

## Common Patterns

### WordPress Security Audit

```python
from core.scanner import SecurityScanner

# Comprehensive WordPress scan
scanner = SecurityScanner(
    target="https://wordpress-site.com",
    modules=[
        "wordpress_version",
        "wordpress_plugins",
        "wordpress_themes",
        "wordpress_users",
        "wordpress_xmlrpc",
        "wordpress_readme",
        "wordpress_debug",
        "wordpress_directory_listing",
        "wordpress_config_backup"
    ]
)

results = scanner.scan()

# Check for specific WordPress issues
if results.has_finding("wordpress_xmlrpc"):
    print("XML-RPC enabled - potential brute force target")
    
if results.has_finding("wordpress_debug"):
    print("Debug mode enabled - information disclosure")

# Export WordPress-specific report
results.export_wordpress_report("wp_audit.pdf")
```

### Stealth Scanning for Protected Sites

```python
from core.scanner import SecurityScanner
from core.evasion import EvasionEngine

# Configure stealth mode
scanner = SecurityScanner(target="https://protected-site.com")

scanner.evasion.configure({
    "user_agent_rotation": True,
    "random_delay": True,
    "min_delay": 2,
    "max_delay": 5,
    "exponential_backoff": True,
    "detect_waf": True,
    "detect_captcha": True,
    "retry_on_block": True,
    "max_retries": 5
})

# Use proxy/Tor for anonymity
scanner.set_proxy("socks5://127.0.0.1:9050")  # Tor

# Run stealth scan
results = scanner.scan(mode="stealth")

# Check if blocked
if results.was_blocked:
    print(f"Blocked by: {results.blocking_mechanism}")
    print(f"Completed: {results.completion_percentage}%")
```

### Automated CI/CD Integration

```python
#!/usr/bin/env python3
"""CI/CD security scan script."""

import os
import sys
from core.scanner import SecurityScanner

def main():
    target = os.getenv("SCAN_TARGET")
    threshold = os.getenv("SEVERITY_THRESHOLD", "HIGH")
    
    # Run automated scan
    scanner = SecurityScanner(
        target=target,
        modules=["xss", "sqli", "csrf", "headers", "ssl"]
    )
    
    results = scanner.scan()
    
    # Generate JSON report
    results.export_json("scan_results.json")
    
    # Check severity threshold
    critical_count = results.count_by_severity("CRITICAL")
    high_count = results.count_by_severity("HIGH")
    
    if critical_count > 0:
        print(f"FAIL: {critical_count} critical vulnerabilities found")
        sys.exit(1)
    
    if threshold == "HIGH" and high_count > 0:
        print(f"FAIL: {high_count} high-severity vulnerabilities found")
        sys.exit(1)
    
    print("PASS: No critical vulnerabilities detected")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Batch Scanning Multiple Targets

```python
from core.scanner import SecurityScanner
from concurrent.futures import ThreadPoolExecutor
import json

def scan_target(target_info):
    """Scan a single target."""
    target, modules = target_info
    
    scanner = SecurityScanner(
        target=target,
        modules=modules,
        mode="stealth"
    )
    
    results = scanner.scan()
    return {
        "target": target,
        "findings": results.get_findings(),
        "severity_counts": results.get_severity_counts()
    }

# Load targets from file
with open("targets.json") as f:
    targets = json.load(f)

# Scan in parallel
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(scan_target, targets.items()))

# Generate summary report
critical_targets = [
    r for r in results 
    if r["severity_counts"].get("CRITICAL", 0) > 0
]

print(f"Scanned {len(results)} targets")
print(f"Critical issues found in {len(critical_targets)} targets")
```

## Troubleshooting

### Connection Issues

```python
from core.scanner import SecurityScanner
from core.browser import StealthBrowser

# Test connectivity
browser = StealthBrowser()
try:
    response = browser.get("https://example.com", timeout=10)
    print(f"Status: {response.status_code}")
except requests.exceptions.Timeout:
    print("Connection timeout - increase timeout value")
except requests.exceptions.ConnectionError:
    print("Connection failed - check network/proxy")
except requests.exceptions.SSLError:
    print("SSL error - certificate validation failed")
    # Disable SSL verification (not recommended for production)
    browser = StealthBrowser(verify_ssl=False)
```

### WAF Blocking

```python
# Detect if you're being blocked
from core.evasion import EvasionEngine

evasion = EvasionEngine()

# Check for blocking indicators
if evasion.is_blocked(response):
    print("Request blocked by WAF")
    
    # Apply bypass techniques
    evasion.increase_stealth_level()
    evasion.set_delay_range(min=3, max=8)
    evasion.enable_proxy_rotation()
    
    # Retry with enhanced evasion
    response = browser.get(url, evasion=evasion)
```

### Module Errors

```python
from core.scanner import SecurityScanner

scanner = SecurityScanner(target="https://example.com")

# Handle module failures gracefully
scanner.configure({
    "continue_on_error": True,
    "log_errors": True,
    "error_log_file": "scan_errors.log"
})

results = scanner.scan()

# Check which modules failed
if results.has_errors():
    for error in results.get_errors():
        print(f"Module: {error.module}")
        print(f"Error: {error.message}")
        print(f"Traceback: {error.traceback}")
```

### Rate Limiting

```python
# Configure rate limiting to avoid detection
from core.scanner import SecurityScanner

scanner = SecurityScanner(target="https://example.com")

scanner.configure({
    "requests_per_second": 2,
    "concurrent_requests": 5,
    "delay_between_requests": 1.5,
    "randomize_delay": True,
    "respect_robots_txt": True
})
```

### Memory and Performance

```python
# Optimize for large scans
scanner = SecurityScanner(
    target="https://example.com",
    cache_responses=True,
    max_cache_size=1000,
    stream_responses=True,
    compression=True
)

# Monitor memory usage
import psutil
process = psutil.Process()
print(f"Memory: {process.memory_info().rss / 1024 / 1024:.2f} MB")
```

## Legal and Ethical Guidelines

**CRITICAL**: Only scan targets you own or have explicit written authorization to test.

```python
# Add authorization check to your scans
def verify_authorization(target):
    """Verify you have permission to scan."""
    print(f"⚠️  You are about to scan: {target}")
    print("Do you have written authorization to test this target? (yes/no)")
    
    response = input().lower()
    if response != "yes":
        print("Scan aborted. Obtain authorization before testing.")
        sys.exit(1)

# Use before scanning
verify_authorization("https://example.com")
scanner.scan()
```

This skill covers the essential usage patterns for Web Security Scanner Pro. Always ensure you have proper authorization before scanning any target and comply with all applicable laws and regulations.
