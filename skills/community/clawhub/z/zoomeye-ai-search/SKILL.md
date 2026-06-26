---
name: zoomeye-ai-search
description: ZoomEye AI cyberspace search engine CLI. Use when searching global network assets, querying ZoomEye data, building ZoomEye AI dork queries, or conducting security research (asset discovery, vulnerability impact assessment, Bug Bounty, CVE correlation). CLI command: zoomeyeai, package: zoomeyeai, domain: zoomeye.ai.
---

# ZoomEye AI — Cyberspace Search

Search global network assets via the `zoomeyeai` CLI at https://www.zoomeye.ai.

> **Key features:** Supports `vul.cve`, `is_bugbounty`, `bugbounty.source`, `is_changed`, `is_new` fields.

## When to Use

### Triggers (MUST load this skill)

- Searching global/overseas network assets
- Building dork queries for ZoomEye international
- Searching assets affected by a CVE
- Bug Bounty asset discovery and filtering
- Searching for assets added or changed in the last 7 days
- User mentions "zoomeyeai", "zoomeye.ai", "ZoomEye AI", "ZoomEye international"

### Skip

- Purely theoretical discussion, no execution needed
- User asks about Shodan, Censys, or other search engines

### Syntax-only mode

If the user only wants natural language → dork conversion ("how do I search for...", "write me the syntax for..."), skip environment checks and execution. Go directly to [Workflow → Step 1](#1-natural-language--dork-conversion) and output the dork.

## Prerequisites

### Step 1: Check Environment

Always verify the environment before executing any search:

```bash
# Check if installed
which zoomeyeai && zoomeyeai --version

# Check if token is configured
zoomeyeai info
```

### Step 2: Guide the User Based on Results

**If `zoomeyeai` is not installed:**

```bash
pip3 install zoomeyeai
```

**If `zoomeyeai info` returns an auth error (token not configured):**

1. Tell the user they need a ZoomEye AI API-KEY:
   > To use ZoomEye international search, you need an API-KEY:
   > 1. Go to https://www.zoomeye.ai/profile and log in
   > 2. Find your API-KEY in your profile
   > 3. Send me the key and I'll initialize it for you

2. Once the user provides the key:
   ```bash
   zoomeyeai init -apikey "<APIKEY>"
   ```

3. Verify:
   ```bash
   zoomeyeai info
   ```
   Confirm the response shows user info and quota, then proceed.

**If `zoomeyeai info` returns normally:**

Environment is ready. Proceed to workflow.

## CLI Commands

```bash
zoomeyeai -h                        # Help
zoomeyeai --version                 # Version
zoomeyeai init -apikey "<KEY>"      # Initialize token
zoomeyeai info                      # Account info & quota
zoomeyeai search "<dork>" [options] # Core search command
```

> Note: No `clear` command.

### Search Options

| Option | Description |
|--------|-------------|
| `-page <n>` | Page number, default 1, sorted by update time |
| `-pagesize <n>` | Results per page, default 10, max 10000 |
| `-sub_type {v4,v6,web,all}` | Data type. `v4`=IPv4 devices (default), `v6`=IPv6, `web`=websites/domains, `all`=everything |
| `-facets <items>` | Aggregate stats, comma-separated. Supports: `product`, `device`, `service`, `os`, `port`, `country`, `subdivisions`, `city` |
| `-fields <fields>` | Return fields, comma-separated. Default: `ip,port,domain,update_time` |
| `-figure {pie,hist}` | Data visualization. Requires `-facets` |

### Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| Auth failure / `login required` | Token not configured | Run `zoomeyeai init -apikey "<APIKEY>"` |
| `rate limit exceeded` / empty results | Quota exhausted or rate limited | Wait and retry, or check quota → `zoomeyeai info` |
| Command timeout | Network issue or slow API | Retry once; if still failing, tell user to check network |

## Search Syntax

### Basic Rules

- Search is **case-insensitive** (except `==` exact match)
- Search strings are **word-segmented** for matching
- Wrap string values in quotes: `"Cisco System"` or `'Cisco System'`
- Escape internal quotes with `\`: `"a\"b"`
- Escape parentheses with `\`: `portinfo\(\)`

### Logical Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Fuzzy match (contains keyword) | `title="knownsec"` |
| `==` | Exact match (case-sensitive, can search empty values) | `title=="knownsec"` |
| `\|\|` | OR | `service="ssh" \|\| service="http"` |
| `&&` | AND | `device="router" && after="2020-01-01"` |
| `!=` | NOT | `country="US" && subdivisions!="new york"` |
| `()` | Grouping / precedence | `(country="US" && port!=80) \|\| (country="US" && title!="404 Not Found")` |
| `*` | Wildcard / fuzzy | `title="google*"` |

### Search Field Reference

#### Device & Service Fingerprints

| Field | Description | Common Values |
|-------|-------------|---------------|
| `app` | Application/product fingerprint | `"Cisco ASA SSL VPN"`, `"GitLab"`, `"phpMyAdmin"` |
| `service` | Service protocol | `"ssh"`, `"http"`, `"ftp"`, `"telnet"`, `"mysql"`, `"redis"`, `"rdp"`, `"smb"` |
| `device` | Device type | `"router"`, `"switch"`, `"storage-misc"`, `"firewall"`, `"webcam"` |
| `os` | Operating system | `"RouterOS"`, `"Linux"`, `"Windows"`, `"IOS"`, `"JUNOS"` |
| `title` | HTML title | `"admin"`, `"login"`, `"Cisco"` |
| `industry` | Industry type | `"government"`, `"technology"`, `"energy"`, `"finance"`, `"manufacturing"` |
| `product` | Component/product name | `"Cisco"`, `"Apache"`, `"Nginx"` |
| `protocol` | Transport protocol | `"TCP"`, `"UDP"`, `"TCP6"`, `"SCTP"` |
| `is_honeypot` | Honeypot filter | `"True"` / `"False"` |

#### IP, Domain & Organization

| Field | Description | Example |
|-------|-------------|---------|
| `ip` | IP address (v4/v6) | `ip="8.8.8.8"`, `ip="2600:3c00::f03c:91ff:fefc:574a"` |
| `cidr` | CIDR range | `cidr="52.2.254.36/24"` (/24=C, /16=B, /8=A) |
| `org` | Organization name | `org="Stanford University"` |
| `isp` | ISP name | `isp="China Mobile"` |
| `asn` | AS number | `asn=42893` |
| `port` | Port number | `port=80` (single port only) |
| `hostname` | Hostname | `hostname="google.com"` |
| `domain` | Domain/subdomain | `domain="baidu.com"` |

#### Geolocation (English)

| Field | Description | Example |
|-------|-------------|---------|
| `country` | Country (abbreviation or full name) | `"US"`, `"United States"`, `"JP"` |
| `subdivisions` | State/province (English) | `"california"`, `"new york"`, `"tokyo"` |
| `city` | City (English) | `"san francisco"`, `"london"` |

#### SSL/TLS Certificates

| Field | Description | Example |
|-------|-------------|---------|
| `ssl` | Certificate content contains (use for product/company search) | `ssl="google"` |
| `ssl.cert.fingerprint` | SHA1 fingerprint | `ssl.cert.fingerprint="F3C98F223D82CC41CF83D94671CCC6C69873FABF"` |
| `ssl.chain_count` | Cert chain count | `ssl.chain_count=3` |
| `ssl.cert.alg` | Signature algorithm | `ssl.cert.alg="SHA256-RSA"` |
| `ssl.cert.issuer.cn` | Issuer CN | `ssl.cert.issuer.cn="pbx.wildix.com"` |
| `ssl.cert.subject.cn` | Subject CN | `ssl.cert.subject.cn="example.com"` |
| `ssl.cert.pubkey.rsa.bits` | RSA public key bits | `ssl.cert.pubkey.rsa.bits=2048` |
| `ssl.cert.pubkey.ecdsa.bits` | ECDSA public key bits | `ssl.cert.pubkey.ecdsa.bits=256` |
| `ssl.cert.pubkey.type` | Public key type | `ssl.cert.pubkey.type="RSA"` |
| `ssl.cert.serial` | Certificate serial | `ssl.cert.serial="18460192207935675900910674501"` |
| `ssl.cipher.bits` | Cipher bits | `ssl.cipher.bits="128"` |
| `ssl.cipher.name` | Cipher suite name | `ssl.cipher.name="TLS_AES_128_GCM_SHA256"` |
| `ssl.cipher.version` | Cipher suite version | `ssl.cipher.version="TLSv1.3"` |
| `ssl.version` | SSL/TLS version | `ssl.version="TLSv1.3"` |
| `ssl.jarm` | JARM fingerprint | `ssl.jarm="29d29d15d29d29d00029d29d29d29dea0f89a2e5fb09e4d8e099befed92cfa"` |
| `ssl.ja3s` | JA3S fingerprint | `ssl.ja3s=45094d08156d110d8ee97b204143db14` |

#### HTTP Headers & Body

| Field | Description | Example |
|-------|-------------|---------|
| `http.header` | HTTP response headers contain | `http.header="http"` |
| `http.header_hash` | Response header MD5 | `http.header_hash="27f9973fe57298c3b63919259877a84d"` |
| `http.header.server` | Server header value | `http.header.server="Nginx"` |
| `http.header.version` | Server version | `http.header.version="1.2"` |
| `http.header.status_code` | HTTP status code | `"200"`, `"302"`, `"404"`, `"500"` |
| `http.body` | HTML body contains | `http.body="document"` |
| `http.body_hash` | HTML body MD5 | `http.body_hash="84a18166fde3ee7e7c974b8d1e7e21b4"` |

#### Protocol Banners, Hashes & Time

| Field | Description | Example |
|-------|-------------|---------|
| `banner` | Non-HTTP protocol banner | `banner="FTP"` |
| `iconhash` | Favicon hash (MD5 or mmh3) | `iconhash="f3418a443e7d841097c714d69ec4bcb8"`, `iconhash="1941681276"` |
| `filehash` | Uploaded file hash | `filehash="0b5ce08db7fb8fffe4e14d05588d49d9"` |
| `dig` | DNS dig result | `dig="baidu.com 220.181.38.148"` |
| `after` | Updated after | `after="2020-01-01"` (must combine with other filters) |
| `before` | Updated before | `before="2020-01-01"` (must combine with other filters) |

#### Additional Fields

The following fields are available:

| Field | Description | Example |
|-------|-------------|---------|
| `vul.cve` | Search by CVE ID | `vul.cve="CVE-2021-44228"` |
| `is_bugbounty` | Bug Bounty program assets | `is_bugbounty=true` |
| `bugbounty.source` | Bug Bounty data source | `bugbounty.source="hackerone"`, `"bugcrowd"`, `"intigriti"`, `"yeswehack"`, `"openbugbounty"`, `"all"` |
| `is_changed` | Asset changed within 7 days (new + updated) | `is_changed=true` |
| `is_new` | Newly discovered within 7 days | `is_new=true` |

## Workflow (AI Decision Tree)

Once the environment is verified, follow these steps:

### 1. Natural Language → Dork Conversion

#### Geolocation Keywords

| User says | Field | Conversion |
|-----------|-------|-------------|
| "US", "United States", "America" | `country` | `country="US"` |
| "Japan", "JP" | `country` | `country="JP"` |
| "Germany", "DE" | `country` | `country="DE"` |
| "California", "CA" | `subdivisions` | `subdivisions="california"` |
| "New York", "NY" | `city` or `subdivisions` | `city="new york"` |
| Any English city/state name | `city` / `subdivisions` | `city="london"` |

#### Port/Service Keywords

| User says | Field | Conversion |
|-----------|-------|-------------|
| "port XX", "open port XX" | `port` | `port=80` |
| "SSH", "SSH service" | `service` | `service="ssh"` |
| "HTTP", "web", "website" | `service` | `service="http"` |
| "database", "MySQL", "Redis", "MongoDB" | `service` | `service="mysql"` |
| "RDP", "remote desktop" | `service` or `port` | `service="rdp"` |

#### Device/OS Keywords

| User says | Field | Conversion |
|-----------|-------|-------------|
| "router" | `device` | `device="router"` |
| "switch" | `device` | `device="switch"` |
| "webcam", "camera" | `device` | `device="webcam"` |
| "Linux", "Linux server" | `os` | `os="Linux"` |
| "Windows", "Windows server" | `os` | `os="Windows"` |
| "Cisco" | `app` | `app="Cisco"` |

#### Additional Keywords

| User says | Field | Conversion |
|-----------|-------|-------------|
| "CVE-2021-44228", "Log4j vulnerability", "impact of CVE" | `vul.cve` | `vul.cve="CVE-2021-44228"` |
| "Bug Bounty assets", "bounty program" | `is_bugbounty` | `is_bugbounty=true` |
| "HackerOne assets", "Bugcrowd's" | `bugbounty.source` | `bugbounty.source="hackerone"` |
| "new in last 7 days", "recently discovered", "new assets" | `is_new` | `is_new=true` |
| "changed in last 7 days", "recently updated" | `is_changed` | `is_changed=true` |
| "all Bug Bounty sources" | `bugbounty.source` | `bugbounty.source="all"` |

#### Conversion Examples

| Natural Language | Dork |
|-----------------|------|
| "SSH services in the US" | `country="US" && service="ssh"` |
| "Log4j vulnerability affected assets globally" | `vul.cve="CVE-2021-44228"` |
| "Nginx servers on HackerOne" | `bugbounty.source="hackerone" && http.header.server="Nginx"` |
| "Redis services discovered in the last 7 days" | `service="redis" && is_new=true` |
| "Routers in Japan, exclude honeypots" | `country="JP" && device="router" && is_honeypot!="True"` |
| "Changed GitLab assets in Bug Bounty" | `is_bugbounty=true && is_changed=true && app="GitLab"` |
| "Windows RDP in Germany" | `country="DE" && service="rdp" && os="Windows"` |
| "Assets with port 3389 open, recently changed" | `port=3389 && is_changed=true` |
| "Admin panels in California" | `(title="admin" \|\| title="login") && subdivisions="california"` |
| "Let's Encrypt certs on US assets" | `ssl.cert.issuer.cn="Let's Encrypt" && country="US"` |

### 2. Build the Dork

Combine fields with operators:

- **Narrow down** → `&&`: `country="US" && service="redis" && os="Linux"`
- **Broaden** → `||`: `port=80 || port=443 || port=8080`
- **Exclude** → `!=`: `country="US" && subdivisions!="california"`
- **Complex logic** → `()`: `(country="US" && port!=80) || (country="JP" && title!="404 Not Found")`

### 3. Choose sub_type

| Scenario | sub_type |
|----------|----------|
| IoT, servers, cameras, ICS, IPv4 assets | `v4` (default) |
| IPv6 assets | `v6` |
| Websites, web apps, domains | `web` |
| Unsure, need everything | `all` |

### 4. Execution Strategy (Quota Optimization)

Follow "probe → verify → export":

```bash
# Step 1: Small probe to confirm dork syntax and results
zoomeyeai search "<dork>" -pagesize 10

# Step 2: Check data distribution with facets (pagesize=1 saves quota)
zoomeyeai search "<dork>" -facets country,service,os -pagesize 1

# Step 3: Bulk retrieval
zoomeyeai search "<dork>" -pagesize 1000
```

### 5. Shell Quoting Rules

| Scenario | Outer Quote | Example |
|----------|------------|---------|
| Dork with `field="value"` only, no single quotes | **Single quotes** | `zoomeyeai search 'country="US" && service="ssh"'` |
| Dork contains single quote character | **Double quotes** | `zoomeyeai search "title='Cisco System'"` |
| Dork contains `&&`, `\|\|` shell special chars | **Single quotes** (safest) | `zoomeyeai search 'service="ssh" \|\| service="http"'` |

**Key rule: prefer single quotes as the outer wrapper.** Only switch to double quotes when the dork itself contains single quote characters.

## Common Search Scenarios

### CVE Vulnerability Impact Assessment

```bash
# Global distribution of a CVE
zoomeyeai search 'vul.cve="CVE-2021-44228"' -facets country -pagesize 1

# CVE + specific product version
zoomeyeai search 'vul.cve="CVE-2021-44228" && app="Log4j"' -pagesize 100
```

### Bug Bounty Asset Discovery

```bash
# Bug Bounty assets from a specific platform
zoomeyeai search 'is_bugbounty=true && bugbounty.source="hackerone"' -pagesize 10

# Specific product in Bug Bounty
zoomeyeai search 'is_bugbounty=true && app="GitLab"' -pagesize 10

# HTTP services across all Bug Bounty platforms
zoomeyeai search 'is_bugbounty=true && bugbounty.source="all" && service="http"' -pagesize 10
```

### New & Changed Asset Monitoring

```bash
# SSH services discovered in last 7 days
zoomeyeai search 'service="ssh" && is_new=true' -pagesize 10

# Web assets changed in last 7 days
zoomeyeai search 'service="http" && is_changed=true' -facets country -pagesize 1

# Newly discovered assets affected by a CVE
zoomeyeai search 'vul.cve="CVE-2024-1234" && is_new=true' -pagesize 100
```

### Global Exposure Discovery

```bash
# Exposed database services in a country
zoomeyeai search 'country="US" && (service="redis" || service="mysql" || service="mongodb")' -pagesize 10

# Assets of an organization
zoomeyeai search 'org="Stanford University"' -pagesize 100

# Global RDP services, excluding honeypots
zoomeyeai search 'service="rdp" && is_honeypot!="True"' -pagesize 10
```

### Web Application Identification

```bash
# Web servers by Server header
zoomeyeai search 'http.header.server="nginx" && country="US"' -sub_type web -pagesize 10

# Admin panels by title
zoomeyeai search '(title="admin" || title="login") && country="JP"' -sub_type web -pagesize 10

# Specific apps by body content
zoomeyeai search 'http.body="phpMyAdmin"' -sub_type web -pagesize 10
```

### SSL Certificate & Fingerprint

```bash
# Assets linked to a company's certificate
zoomeyeai search 'ssl="google"' -pagesize 10

# Let's Encrypt issued certificates
zoomeyeai search "ssl.cert.issuer.cn=\"Let's Encrypt\" && country=\"US\"" -pagesize 10

# JARM fingerprint search
zoomeyeai search 'ssl.jarm="29d29d15d29d29d00029d29d29d29dea0f89a2e5fb09e4d8e099befed92cfa"' -pagesize 10
```

### Subnet & IP Scanning

```bash
zoomeyeai search 'cidr="52.2.254.36/24"' -pagesize 100
zoomeyeai search 'cidr="52.2.254.36/16" && service="http"' -pagesize 100
```

## SDK Usage

```python
from zoomeyeai.sdk import ZoomEye

zm = ZoomEye(api_key="your-api-key")

# Account info & quota
zm.userinfo()
# Returns: {"email": "", "username": "", "quota": {"plan": "", "end_date": "", "points": "", "zoomeye_points": ""}}

# Search
result = zm.search(
    dork='country=us',
    qbase64='',                  # Base64-encoded query (alternative to dork)
    page=1,
    pagesize=20,                 # SDK default is 20
    sub_type='all',              # v4 / v6 / web / all
    fields='ip,port,domain,os,app,title',
    facets='country,service'
)
```

## Notes

| Item | Detail |
|------|--------|
| Quota | Each search consumes quota. Use `-pagesize 1` + `-facets` first, then bulk retrieve |
| Geolocation | Use English names, e.g. `country="United States"` or `country="US"` |
| `-save` | Not available. Export data manually or use SDK |
| `before`/`after` | Cannot be used alone; must combine with other filters |
| Shell quoting | Always wrap the dork in quotes. Prefer single quotes |
