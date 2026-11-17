# Search Engine Operator Cheat Sheets

## Meta indexes
- `github.com/edoardottt/awesome-hacker-search-engines` - categorized index of security search
  engines (DNS, certificates, leaks, code, devices, threat intel, and more).
- `github.com/jivoi/awesome-osint` - broad OSINT category index; use as a fallback when this file
  does not cover a niche target type.
These are routers, not sources: cite the underlying engine or page you actually queried.

## Google

| Operator | Example | Meaning |
|---|---|---|
| `site:` | `site:example.com` | Restrict to site; `site:*.example.com` includes subdomains |
| `inurl:` | `inurl:admin` | Term in URL |
| `allinurl:` | `allinurl:admin login` | All terms in URL (legacy) |
| `intitle:` | `intitle:"index of"` | Term in title |
| `allintitle:` | `allintitle:admin login` | All terms in title (legacy) |
| `intext:` | `intext:"password"` | Term in body |
| `allintext:` | `allintext:user password` | All terms in body (legacy) |
| `filetype:` / `ext:` | `filetype:pdf` | File type |
| `"..."` | `"exact phrase"` | Exact phrase |
| `-` | `-site:wikipedia.org` | Exclude |
| `OR` / `\|` | `pdf OR docx` | Boolean OR |
| `*` | `"admin * login"` | Wildcard |
| `AROUND(n)` | `admin AROUND(3) password` | Terms within n words |
| `before:` / `after:` | `after:2025-01-01` | Date range |
| `numrange:` | `numrange:1000-5000` | Numeric range |
| `related:` | `related:example.com` | Similar sites |
| `cache:` | `cache:example.com` | Cached page (often unreliable) |
| `source:` | `source:reuters` | Google News source |
| `imagesize:` | `imagesize:1920x1080` | Image dimensions |
| `loc:` | `loc:vn` | Location (news) |

Time filter URL param: `&tbs=qdr:h` (hour), `qdr:d`, `qdr:w`, `qdr:m`, `qdr:y`.
Safe search: `&safe=off|active`. Language: `&hl=vi`. Country: `&gl=vn`.

## Bing

```
site:example.com
filetype:pdf
intitle:"index of"
inbody:"password"
inurl:admin
ip:203.0.113.10
language:vi
loc:vn
contains:pdf
ext:sql
"exact phrase"
-word
OR
```
Time filter: `&filters=ex1%3a%22ez5_18262_18269%22` (varies; use UI or API).

## DuckDuckGo

- Common Google operators mostly work.
- Bangs: `!g` Google, `!gh` GitHub, `!so` Stack Overflow, `!w` Wikipedia, `!yt` YouTube,
  `!sh` Shodan, `!vt` VirusTotal, `!wayback` Wayback Machine.
- HTML endpoint: `https://duckduckgo.com/html/?q=<query>`.
- Lite endpoint: `https://lite.duckduckgo.com/lite/?q=<query>`.

## Yandex

```
site:example.com
host:example.com
title:"admin"
url:login
mime:pdf
date:20250101..20251231
"exact phrase"
```
Strong for reverse image search (`https://yandex.com/images/`), regional content, and faces.

## Chinese web search

- **Baidu** (`baidu.com`) - Chinese-language results; supports `site:`, `intitle:`, `inurl:`,
  `filetype:`. Expect SEO spam and clones; verify the primary source.
- **Sogou** (`sogou.com`) - Chinese results; WeChat article search at `weixin.sogou.com`.
- **360 Search** (`so.com`) - Chinese results; supports `site:`, `intitle:`, `filetype:`.
- **Bing China** (`cn.bing.com`) - Bing results with China-localized indexing.
- Search in Chinese (简化字) and local product names; translate the CVE/product first. Do not treat
  search snippets as evidence; open the original page and check dates, authorship, and provenance.

## GitHub Code Search

```
in:name              repo name
in:description       repo description
in:readme            README content
in:topics            topics
in:file              file content
in:path              file path
repo:owner/name      specific repo
org:name             organization
user:name            user
language:python      language
path:.env            path filter
filename:.npmrc      filename
extension:sql        extension
size:>1000           size (KB)
stars:>100           stars
fork:true|false      include forks
archived:true|false  archived
is:public            visibility
created:>2024-01-01  creation date
pushed:>2025-01-01   last push
topic:security       topic
```
Examples:
```
org:target filename:.env
org:target "AKIA"
filename:.git-credentials
path:.github/workflows "secrets."
"BEGIN RSA PRIVATE KEY" org:target
extension:sql "INSERT INTO" org:target
```

## Shodan

Filters:
```
port:                     hostname:                 net:
org:                      asn:                      isp:
country:                  city:                     geo:
os:                       product:                  version:
http.title:               http.html:                http.status:
http.favicon.hash:        http.component:           http.headers.server:
ssl:                      ssl.cert.subject.CN:      ssl.cert.issuer.CN:
vuln:                     has_vuln:                 tag:
device:                   uptime:                   before: / after:
```
Examples:
```
org:"Example Inc"
ssl:"example.com"
http.favicon.hash:-1234567890
http.title:"Login" country:VN
product:"Elasticsearch" port:9200
port:27017 -country:US
vuln:CVE-2024-3400
```
CLI:
```bash
shodan init $SHODAN_API_KEY
shodan search --fields ip_str,port,org,product 'org:"Example Inc"' --limit 100
shodan count 'ssl:"example.com"'
shodan host 203.0.113.10
shodan download out.json.gz 'org:"Example Inc"'
shodan parse --fields ip_str,port,product out.json.gz
shodan stats --facets port:100 org:"Example Inc"
```
InternetDB: `curl https://internetdb.shodan.io/203.0.113.10`

## Censys (CenQL)

```
host.services.port: 443
host.services.service_name: HTTP
host.services.transport_protocol: TCP
host.services.tls.certificates.leaf_data.subject.organization: "Example Inc"
host.services.tls.certificates.leaf_data.names: example.com
autonomous_system.asn: 12345
autonomous_system.organization: "Example Inc"
services.http.response.status_code: 200
web.hostname: example.com
cert.names: example.com
cert.parsed.subject.organization: "Example Inc"
```
Logic: `and`, `or`, `not`, parentheses, comparison operators.
CLI:
```bash
censys search 'services.tls.certificates.leaf_data.names: example.com' --index hosts
censys view 203.0.113.10
```
API: `https://search.censys.io/api/v2/hosts/search?q=...` (basic auth).

## FOFA

```
domain="example.com"
host="example.com"
ip="203.0.113.0/24"
port="443"
protocol="https"
app="Apache"
title="后台管理"
body="phpinfo"
header="thinkphp"
cert="example.com"
cert.subject="Example Inc"
cert.issuer="Let's Encrypt"
server="nginx"
icon_hash="123456789"
fid="..."
http_status="200"
os="Windows"
country="VN"
region="Hanoi"
city="Hanoi"
```
Logic: `&&`, `||`, `!=`, parentheses.
Example: `domain="example.com" && port="443" && title="login"`.
API: `https://fofa.info/api/v1/search/all?key=KEY&qbase64=<base64(query)>`.
CLI: `fofa -q 'domain="example.com" && port="80"' -o results.csv`.

## ZoomEye

```
app:nginx
app.version:1.24
port:443
service:http
device:router
title:"admin"
header:"thinkphp"
body:"Welcome"
ip:203.0.113.10
cidr:203.0.113.0/24
domain:example.com
subdomain:dev.example.com
country:VN
city:Hanoi
ssl:"example.com"
ssl.cert:"Example Inc"
iconhash:123456789
filehash:...
```
API: `https://api.zoomeye.org/host/search?query=...` (API key header).

## Hunter (鹰图)

```
domain="example.com"
ip="203.0.113.0/24"
web.title="login"
web.body="admin"
web.icon="hash"
cert="example.com"
port="443"
protocol="https"
app="nginx"
os="Linux"
region="Beijing"
is_domain=true
```
API: `https://hunter.qianxin.com/openApi/search`.

## BinaryEdge

```
ip:203.0.113.10
port:443
domain:example.com
country:VN
product:nginx
tag:...
type:...
```
API: `https://api.binaryedge.io/v2/query/search?query=...`.

## Netlas

```
domain:example.com
host:example.com
ip:203.0.113.10
port:443
cert.subject.organization:"Example Inc"
http.title:"admin"
```
API: `https://app.netlas.io/api/responses/`.

## Quake (360)

```
title:"admin"
body:"phpinfo"
cert:"example.com"
ip:"203.0.113.10"
port:"443"
app:"nginx"
service:"http"
domain:"example.com"
region:"Beijing"
isp:"China Telecom"
```
API: `https://quake.360.net/api/v3/search/quake_service`.

## GreyNoise

```
ip:203.0.113.10
classification:malicious
classification:benign
tags:...
asn:12345
organization:"Example Inc"
```
API: `https://api.greynoise.io/v3/community/<ip>`.

## VirusTotal

```
domain:example.com
ip:203.0.113.10
file:<sha256>
url:https://example.com/path
```
API: `https://www.virustotal.com/api/v3/{domains,ip_addresses,files,urls}/{id}`.

## Wayback Machine CDX

```
https://web.archive.org/cdx/search/cdx?url=example.com/*&output=json&fl=timestamp,original,statuscode,mimetype&collapse=urlkey&limit=1000
https://web.archive.org/cdx/search/cdx?url=example.com&from=2024&to=2025&output=json
```

## Common Crawl Index

```
https://index.commoncrawl.org/CC-MAIN-2025-30-index?url=example.com/*&output=json
```

## Certificate Transparency

```
https://crt.sh/?q=%25.example.com&output=json
https://crt.sh/?q=example.com&exclude=expired
```

## CISA KEV / EPSS / NVD

```
https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
https://api.first.org/data/v1/epss?cve=CVE-2024-3400
https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-3400
https://api.osv.dev/v1/query
```
