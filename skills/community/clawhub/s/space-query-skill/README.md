# Space Query Skill

Build search queries for network asset discovery (空间测绘) platforms.

## Supported Platforms

| Platform | Best For | Website |
|----------|---------|--------|
| FOFA | Global coverage, detailed protocol data | [fofa.info](https://fofa.info) |
| Quake (鹰图) | China-focused, threat intelligence | [quake.360.net](https://quake.360.net) |
| ZoomEye | Detailed service fingerprints | [zoomeye.org](https://zoomeye.org) |
| Shodan | International IoT devices, vulnerability correlation | [shodan.io](https://shodan.io) |

## Installation

### Claude Code
```bash
# Clone the repository
git clone https://github.com/gandli/space-query-skill.git ~/.claude/skills/space-query-skill
```

### Claude Code Plugin
```bash
/plugin marketplace add gandli/space-query-skill
/plugin install space-query-skill@gandli
```

### Other
```bash
# Using skills CLI (recommended)
npx skills add gandli/space-query-skill
```

## Usage

Describe what you want to find:

```
Find all Redis servers exposed in China
Search for Apache Log4j vulnerabilities
Look for login pages on government websites
Find expired SSL certificates on banks
Search for CVE-2021-44228 affected hosts
```

The skill will generate queries for the appropriate platform(s).

## Features

- Multi-platform query syntax support
- CVE/vulnerability search queries
- Platform-specific field mappings
- Query pattern templates
- Operator precedence handling

## Examples

### Exposed Database
```
FOFA:   port="6379" && product="Redis" && country="CN"
Quake:  port:6379 AND app:Redis AND country:China
Shodan: port:6379 product:Redis country:CN
```

### Login Pages
```
FOFA:   (title="登录" || title="admin") && country="CN"
Shodan: title:"login page" country:CN
```

### CVE/Vulnerability
```
Shodan: product:Apache vuln:CVE-2021-44228
FOFA:   product="Apache" && body="log4j"
Quake:  app:Apache AND tag:CVE-2021-44228
```

## License

MIT
