---
name: website-scan
description: Comprehensive website analysis and scanning tool. Analyzes IP (IPv4/IPv6), DNS records, WHOIS data, website content (including Schema.org JSON-LD, robots.txt, llms.txt, sitemap.xml), SEO metrics, and third-party data (Google index). Supports deep scanning with Playwright for client-side rendered pages. Generates detailed technical reports.
---

# Website Scanner

Comprehensive website analysis tool that scans domains and generates detailed technical reports.

## When to Use

Use this skill when you need to:
- Analyze a website's technical infrastructure (IP, DNS, WHOIS)
- Audit website content and SEO
- Extract structured data (Schema.org JSON-LD)
- Check robots.txt, llms.txt, sitemap.xml
- Perform deep scanning of multiple pages
- Generate comprehensive website reports

## Prerequisites

### Required System Tools
- `dig` - DNS lookup utility
- `whois` - WHOIS query tool

### Python Dependencies
```bash
pip install requests beautifulsoup4 aiohttp
```

### Optional (for deep scanning)
- Playwright (for JavaScript-rendered pages)
```bash
pip install playwright
playwright install chromium
```

## Usage

### Basic Scan
```bash
python3 scripts/scan.py example.com
```

### Deep Scan (follow sitemap)
```bash
python3 scripts/scan.py example.com --deep --max-pages 10
```

### Save Reports
```bash
python3 scripts/scan.py example.com --output report.json --markdown report.md
```

## Features

### 1. Network Analysis
- **IP Resolution**: IPv4 and IPv6 addresses
- **Geolocation**: Server location, ASN, organization
- **DNS Records**: A, AAAA, MX, NS, TXT, CNAME, SOA
- **WHOIS Data**: Registrar, creation/expiration dates, status

### 2. Content Analysis
- **Homepage Metadata**: Title, description, viewport, charset
- **Heading Structure**: H1-H6 distribution
- **Links**: Internal vs external count
- **Images**: Alt text coverage
- **Scripts/Styles**: Resource count

### 3. Structured Data
- **Schema.org JSON-LD**: Extract all structured data schemas
- **Open Graph**: Meta tag analysis
- **Twitter Cards**: Social media metadata

### 4. SEO Analysis
- **SEO Score**: 0-100 rating
- **Issues**: Missing tags, optimization problems
- **Recommendations**: Actionable improvements

### 5. Crawler Files
- **robots.txt**: Fetch and parse
- **llms.txt**: AI/LLM instructions
- **sitemap.xml**: Parse URL structure

### 6. Third-Party Data
- **Google Index**: Check indexed pages (approximate)
- **Server Detection**: Technology stack identification

### 7. Deep Scanning
- Follow sitemap URLs
- Analyze multiple pages
- Client-side rendering support (with Playwright)

## Output Format

### Console Output
Human-readable markdown report with:
- IP and network information
- DNS record summary
- WHOIS details
- Content statistics
- SEO score and issues
- Third-party metrics

### JSON Export
```json
{
  "scan_info": {
    "url": "https://example.com",
    "domain": "example.com",
    "scan_date": "2026-04-02T10:00:00"
  },
  "ip_info": { ... },
  "dns_info": { ... },
  "whois_info": { ... },
  "content_analysis": { ... },
  "seo": { ... },
  ...
}
```

### Markdown Export
Formatted report suitable for documentation or sharing.

## Examples

### Example 1: Quick Scan
```bash
python3 scripts/scan.py hugogu.cn
```

Output includes:
- IP addresses and location
- DNS configuration
- WHOIS registration info
- Homepage SEO analysis

### Example 2: Full Audit
```bash
python3 scripts/scan.py hugogu.cn --deep --max-pages 20 \
  --output audit.json --markdown audit.md
```

Performs comprehensive analysis including:
- All network information
- Deep page crawling
- SEO audit
- Structured data extraction
- Full report export

## Limitations

1. **Rate Limiting**: Some queries (WHOIS, DNS) may be rate-limited
2. **JavaScript Rendering**: Basic scan doesn't execute JS (use --deep with Playwright)
3. **Third-Party APIs**: Traffic estimation requires paid API keys
4. **Google Index**: Approximate only (scrapes search results)

## Troubleshooting

### "dig command not found"
```bash
# Ubuntu/Debian
sudo apt-get install dnsutils

# macOS
brew install bind

# CentOS/RHEL
sudo yum install bind-utils
```

### "whois command not found"
```bash
# Ubuntu/Debian
sudo apt-get install whois

# macOS
brew install whois
```

### DNS Resolution Fails
Check if domain is accessible:
```bash
nslookup example.com
dig example.com
```

## Architecture

```
┌─────────────────┐
│ WebsiteScanner  │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    │         │          │          │
┌───▼───┐ ┌──▼────┐ ┌───▼───┐ ┌───▼────┐
│ IP    │ │ DNS   │ │ WHOIS │ │ Content│
│Analyzer│ │Analyzer│ │Analyzer│ │Analyzer│
└───────┘ └───────┘ └───────┘ └───────┘
                                   │
                          ┌────────┼────────┐
                          │        │        │
                      ┌───▼───┐ ┌─▼────┐ ┌─▼────┐
                      │ SEO   │ │ JSON │ │ Deep │
                      │Analyzer│ │ -LD  │ │ Scan │
                      └───────┘ └──────┘ └──────┘
```

## Integration with OpenClaw

This skill can be invoked from OpenClaw to:
1. Scan competitor websites
2. Audit your own sites
3. Research domain infrastructure
4. Generate technical documentation

Example OpenClaw workflow:
```
User: "Scan hugogu.cn and tell me about its infrastructure"
→ Run scanner
→ Analyze results
→ Generate summary
```