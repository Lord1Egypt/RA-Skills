---
name: space-query-skill
description: |
  Build search queries for network asset discovery platforms (space测绘). Use when users want to find network assets, discover attack surfaces, investigate vulnerabilities (CVE), or search for specific services/servers/websites.
  Triggers on: 空间测绘, FOFA, 鹰图, ZoomEye, Shodan, CVE, 漏洞, asset discovery, network search, or similar queries.
license: MIT
---

# Space Query Skill

Multi-platform query builder for FOFA, Quake, ZoomEye, and Shodan.

## Quick Start

1. **Detect platform** — Use specified platform or ask user
2. **Analyze intent** — What to find, where, attributes, exclusions
3. **Build query** — Apply correct syntax for the platform
4. **Present result** — Use the output format below

## Platform Selection

| Platform | Best For | Syntax Style |
|----------|----------|--------------|
| FOFA | Global coverage, protocol details | `field="value"` |
| Quake (鹰图) | China data, threat intel | `field:value` |
| ZoomEye | Service fingerprints | `field:value` |
| Shodan | IoT,漏洞关联 | `field:value` |

## Core Patterns

### Pattern 1: Exposed Service
```
FOFA:   product="Redis" && port="6379" && country="CN"
Quake:  app:Redis AND port:6379 AND country:China
Shodan: product:Redis port:6379 country:CN
```

### Pattern 2: Login Page
```
FOFA:   (title="登录" || title="admin" || title="后台") && country="CN"
Quake:  (keyword:登录 OR keyword:admin) AND country:China
Shodan: title:"login" country:CN
```

### Pattern 3: File Upload
```
FOFA:   (body="plupload" || body="webuploader" || title="上传") && country="CN"
Shodan: http.html:"type=\"file\"" country:CN
```

### Pattern 4: SSL Certificate Issue
```
FOFA:   cert.is_expired=true && country="CN"
Shodan: ssl.cert.expired:true country:CN
```

### Pattern 5: CVE/Vulnerability Search

**Critical**: Always extract features from CVE info and use platform-specific product identifiers.

#### CVE Query Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: WebSearch for official queries                    │
│  Search: "[Platform] CVE-XXXX-XXXX" or "[CVE] + FOFA"  │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: Find official source                               │
│  - Platform blog (en.fofa.info, quake.360.net/blog)     │
│  - Security sites (securityonline.info, nvd.nist.gov)     │
│  - GitHub PoC repos often contain platform queries         │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: Extract platform-specific product ID               │
│  - FOFA uses app="product-name"                            │
│  - Quake uses app:product-name                             │
│  - Shodan uses product:product-name                        │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 4: Build query                                       │
└─────────────────────────────────────────────────────────────┘
```

#### How to Find Official Sources

**When given a CVE, ALWAYS use WebSearch first:**

```bash
# Search for platform-specific queries
web_search: "CVE-2024-38819 FOFA query"
web_search: "CVE-2024-38819 fofa.info"
web_search: "CVE-2024-38819 Quake 360"
web_search: "CVE-2024-38819 PoC github"

# Search for official platform announcements
web_search: "site:en.fofa.info CVE-2024-38819"
web_search: "site:quake.360.net CVE"
```

**Official Sources to Check:**
| Source | URL | What to Find |
|--------|-----|--------------|
| FOFA Blog | en.fofa.info | Official queries with exact app IDs |
| Quake Blog | quake.360.net/blog | Threat intel announcements |
| NVD | nvd.nist.gov | CVE details, affected products |
| SecurityOnline | securityonline.info | PoC with platform queries |
| GitHub | github.com | PoC exploits often include FOFA/Quake queries |

#### Example - CVE-2024-38819

**Step 1: WebSearch**
```
Search: "CVE-2024-38819 FOFA"
Result: en.fofa.info shows "app="vmware-Spring-Framework""
```

**Step 2: Official Query Found**
```
FOFA: app="vmware-Spring-Framework"  (25k+ results)
```

**Step 3: Cross-platform translation**
```
FOFA:   app="vmware-Spring-Framework"
Shodan: product:"Spring Framework"
Quake:  app:Spring
ZoomEye: app:spring
```

#### Wrong vs Correct Approach

**Wrong (lazy):**
```
body="CVE-2024-38819"     ❌ CVE ID in body, no results
product="Spring"           ❌ Wrong product ID for most platforms
```

**Correct (official product ID):**
```
app="vmware-Spring-Framework"  ✅ FOFA official query
```

#### Verified CVE Query Table

| CVE | Affects | FOFA | Shodan | Quake |
|-----|---------|------|--------|-------|
| CVE-2024-38819 | Spring Framework | `app="vmware-Spring-Framework"` | `product:"Spring Framework"` | `app:Spring` |
| CVE-2021-44228 | Apache Log4j | `app="Apache-log4j2"` | `product:log4j` | `app:log4j` |
| CVE-2019-0708 | Windows RDP | `app="Microsoft-RDP"` | `vuln:CVE-2019-0708` | `app:RDP` |
| CVE-2022-22965 | Spring4Shell | `app="vmware-Spring-Framework"` | `product:Spring` | `app:Spring` |

**Rule**: When you find an official query from a trusted source (platform blog, security site, verified PoC), use that exact query.

## Operator Precedence

```
() > == > = > != > && > ||
```

**Rule**: Always wrap multiple OR conditions with `()`.

## Output Format

Present queries using this structure:

```markdown
## Query

**Platform:** [Platform]
```
[Query Here]
```

### Explanation
- **Target:** What this finds
- **Fields:** Main fields used
- **Logic:** AND/OR relationship

### Suggestions
- Additional filters to consider
- Known limitations
- Alternative approaches
```

## Field Reference

See `resources/fields.md` for complete field lists per platform.

## Important Notes

1. **Parentheses** — `(A || B) && C` not `A || B && C`
2. **Platform syntax differs** — FOFA uses `="` while others use `:`
3. **Chinese chars** — `country="中国"` works in FOFA, prefer English elsewhere
4. **Time filtering** — `after`/`before` in FOFA/Quake

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No results | Add `status_code="200"` or remove strict filters |
| Too many results | Add country, time, or product filters |
| Wrong syntax | Check platform in reference files |
