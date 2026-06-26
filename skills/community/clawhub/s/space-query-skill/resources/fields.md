# Field Reference

Detailed field mappings for each platform.

## FOFA (fofa.info)

### Basic Fields
| Field | Description | Example |
|-------|-------------|---------|
| ip | IPv4 address | `ip="1.1.1.1"` |
| ip="220.181.111.1/24" | IPv4 C段 | |
| port | Port number | `port="6379"` |
| domain | Root domain | `domain="qq.com"` |
| host | Hostname | `host=".fofa.info"` |
| server | Server type | `server="Microsoft-IIS/10"` |
| asn | ASN number | `asn="19551"` |
| org | Organization | `org="LLC Baxet"` |

### Website Fields (type="subdomain")
| Field | Description | Example |
|-------|-------------|---------|
| title | Website title | `title="beijing"` |
| header | HTTP header | `header="elastic"` |
| body | HTML body | `body="网络空间测绘"` |
| js_name | JS filename | `js_name="js/jquery.js"` |
| js_md5 | JS hash | `js_md5="82a..."` |
| status_code | HTTP status | `status_code="200"` |
| icon_hash | Icon hash | `icon_hash="-247388890"` |

### Product/Component
| Field | Description | Example |
|-------|-------------|---------|
| product | Product name | `product="NGINX"` |
| product.version | Version | `product.version="1.6.10"` |
| app | FOFA rule | `app="Microsoft-Exchange"` |
| category | Category | `category="服务"` |

### Certificate
| Field | Description | Example |
|-------|-------------|---------|
| cert | Certificate | `cert="baidu"` |
| cert.domain | Cert domain | `cert.domain="huawei.com"` |
| cert.subject | Subject | `cert.subject="Oracle Corporation"` |
| cert.issuer | Issuer | `cert.issuer="DigiCert"` |
| cert.is_valid | Valid cert | `cert.is_valid=true` |
| cert.is_expired | Expired cert | `cert.is_expired=true` |
| cert.is_match | Cert matches domain | `cert.is_match=true` |

### Location
| Field | Description | Example |
|-------|-------------|---------|
| country | Country | `country="CN"` or `country="中国"` |
| region | Region/state | `region="Zhejiang"` |
| city | City | `city="Hangzhou"` |

### Time
| Field | Description | Example |
|-------|-------------|---------|
| after | Updated after | `after="2023-01-01"` |
| before | Updated before | `before="2023-12-01"` |

### Operators
- `=` exact match, `= ""` for empty
- `==` perfect match, `== ""` for exists-but-empty
- `!=` not equal, `!= ""` for not-empty
- `*=` fuzzy match
- `&&` AND, `||` OR

---

## Quake (quake.360.net)

### Basic Fields
| Field | Description | Example |
|-------|-------------|---------|
| ip | IP address | `ip:1.2.3.4` |
| port | Port | `port:80` |
| domain | Domain | `domain:example.com` |
| country | Country | `country:China` |
| city | City | `city:Beijing` |
| protocol | Protocol | `protocol:http` |

### Special Fields
| Field | Description | Example |
|-------|-------------|---------|
| app | Application | `app:Apache` |
| tag | Tag | `tag:weblogic` |
| device | Device type | `device:Router` |
| os | OS | `os:Windows` |
| header | HTTP header | `header:Server` |
| keyword | Full-text | `keyword:login` |

### Operators
- `AND` / `&&` - AND
- `OR` / `||` - OR
- `NOT` / `!` - NOT
- `*` wildcard (multi), `?` single
- `()` grouping

---

## ZoomEye (zoomeye.org)

ZoomEye uses a "dork" based search system.

### Basic Fields
| Field | Description | Example |
|-------|-------------|---------|
| ip | IP address | `ip:1.2.3.4` |
| port | Port | `port:80` |
| country | Country code | `country:cn` |
| city | City | `city:beijing` |
| app | Application | `app:apache` |
| service | Service type | `service:http` |
| os | Operating system | `os:windows` |
| device | Device type | `device:router` |
| component | Component | `component:jquery` |
| version | Version | `version:1.18.0` |

### CLI/SDK Usage
```bash
# ZoomEye CLI
zoomeye search "telnet"
zoomeye search "country=cn" -facets product -pagesize 10

# ZoomEye SDK (Python)
from zoomeye.sdk import ZoomEye
zm = ZoomEye(api_key="your-api-key")
zm.search('app:apache')
```

### Important Notes
- Uses API key authentication (free tier available)
- Supports facets for aggregated statistics
- Website data requires different search mode
- Reference: [github.com/knownsec/ZoomEye-python](https://github.com/knownsec/ZoomEye-python)

---

## Shodan (shodan.io)

### Filters
| Filter | Description | Example |
|--------|-------------|---------|
| country | Country code | `country:CN` |
| city | City | `city:Beijing` |
| geo | Coordinates | `geo:39.9,116.4,50km` |
| org | Organization | `org:"China Telecom"` |
| isp | ISP | `isp:"China Unicom"` |
| asn | ASN | `asn:45090` |
| hostname | Hostname | `hostname:.edu.cn` |
| net | Network | `net:192.168.0.0/24` |
| port | Port | `port:22` |

### Product/Service
| Filter | Description | Example |
|--------|-------------|---------|
| product | Product | `product:nginx` |
| version | Version | `version:1.18.0` |
| os | OS | `os:"Windows 7"` |
| device | Device | `device:webcam` |
| vuln | Vulnerability | `vuln:CVE-2021-44228` |

### Operators
- `AND` / `OR` / `NOT` (or `!`)
- `"phrase"` exact phrase
- `()` grouping

---

## Common Use Cases

### Find Databases
| Platform | Query |
|----------|-------|
| FOFA | `port="6379" && product="Redis" && country="CN"` |
| Quake | `port:6379 AND app:Redis AND country:China` |
| ZoomEye | `port:6379 AND app:redis` |
| Shodan | `port:6379 product:Redis` |

### Find Login Pages
| Platform | Query |
|----------|-------|
| FOFA | `(title="登录" \|\| title="admin") && country="CN"` |
| Quake | `(keyword:登录 OR keyword:admin) AND country:China` |
| ZoomEye | `title:登录 OR title:admin` |
| Shodan | `title:"login" country:CN` |

### Find Webcams
| Platform | Query |
|----------|-------|
| FOFA | `product="海康威视" && country="CN"` |
| Quake | `app:海康威视 AND country:China` |
| Shodan | `device:webcam country:CN` |

### Find Vulnerable Services
| Platform | Query |
|----------|-------|
| FOFA | `product="Apache" && product.version="2.4.49"` |
| Quake | `app:Apache AND ver:2.4.49` |
| Shodan | `product:Apache version:2.4.49 vuln:CVE-2021-44228` |

---

## CVE Vulnerability Search

### Platform Support

| Platform | CVE Support | Example |
|----------|------------|---------|
| Shodan | Full CVE tags | `vuln:CVE-2021-44228` |
| Quake | Tag-based | `tag:CVE-2021-44228` |
| FOFA | Body/content search | `body="log4j"` |
| ZoomEye | Partial | `vuln:CVE-2021-44228` |

### Common CVE Queries

| CVE | Affected | FOFA | Shodan | Quake |
|-----|---------|------|--------|-------|
| CVE-2026-33032 | Nginx UI | `app="nginx-ui"` | `product:"Nginx UI"` | `app:nginx-ui` |
| CVE-2024-38819 | Spring Framework | `app="vmware-Spring-Framework"` | `product:"Spring Framework"` | `app:Spring` |
| CVE-2021-44228 | Apache Log4j | `app="Apache-log4j2"` | `vuln:CVE-2021-44228` | `app:log4j` |
| CVE-2019-0708 | Windows RDP | `app="Microsoft-RDP"` | `vuln:CVE-2019-0708` | `app:RDP` |
| CVE-2022-22965 | Spring4Shell | `app="vmware-Spring-Framework"` | `product:Spring` | `app:Spring` |
| CVE-2021-26855 | MS Exchange | `app="Microsoft-Exchange"` | `vuln:CVE-2021-26855` | `app:Exchange` |

### Vulnerability Search Tips

1. **Shodan** has the best CVE support - use `vuln:CVE-YYYY-NNNNN`
2. **FOFA** often requires searching for vulnerability signatures in body/header
3. **Quake** uses tags for known CVEs
4. **ZoomEye** supports some CVE searches
5. Always combine with product/service filters for accuracy
