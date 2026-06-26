# Required Tools

## Core (required)

| Tool | Package | Purpose |
|------|---------|---------|
| curl | curl | HTTP requests, header checks, CORS testing |
| dig | dnsutils | DNS lookups |
| jq | jq | JSON processing |
| nmap | nmap | Port scanning |

## Scanning (install as needed)

| Tool | Install | Purpose |
|------|---------|---------|
| whatweb | `apt install whatweb` | Technology fingerprinting |
| wafw00f | `pip install wafw00f` | WAF detection |
| subfinder | [GitHub releases](https://github.com/projectdiscovery/subfinder) | Subdomain enumeration |
| gobuster | `apt install gobuster` | Directory bruteforce |
| ffuf | [GitHub releases](https://github.com/ffuf/ffuf) | Fast web fuzzer |
| nikto | `apt install nikto` | Vulnerability scanner |
| wpscan | `gem install wpscan` | WordPress scanner |
| nuclei | [GitHub releases](https://github.com/projectdiscovery/nuclei) | Template-based vuln scan |
| testssl | `apt install testssl.sh` | SSL/TLS analysis |
| titus | [GitHub](https://github.com/AidenPearce369/titus) | Secrets detection (459 rules) |
| httpx | [GitHub releases](https://github.com/projectdiscovery/httpx) | HTTP probing |

## Screenshot (one of)

| Tool | Install | Purpose |
|------|---------|---------|
| cutycapt | `apt install cutycapt` | Lightweight screenshot capture |
| chromium | `apt install chromium` | Headless browser screenshot |

## Optional

| Tool | Purpose |
|------|---------|
| amass | Advanced subdomain enum |
| waybackurls | Wayback Machine URL extraction |
| Shodan CLI | Infrastructure intel (or use `SHODAN_API_KEY` env var) |

Scripts gracefully skip missing tools — install what you need.
