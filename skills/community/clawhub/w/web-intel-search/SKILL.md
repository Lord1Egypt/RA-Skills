---
name: web-intel-search
description: "Security search & research: OSINT, pentest, bug bounty, CVE/PoC, writeups, cheatsheets, red team, appsec, cloud architecture, debug, labs, blogs."
version: 1.9.0
license: MIT-0
compatibility: Requires internet/web access. Optional CLI tools and API keys unlock advanced modules.
metadata:
  version: 1.9.0
  language: en
  modules: 12
  sources:
    - elementalsouls/Claude-OSINT
    - UseOSINT/Skills
    - jassics/awesome-claude-security (osint plugin)
    - zbailey83/dorking-skill
    - danielrosehill/Claude-Dork
    - ClawHub p0lish/web-recon
    - ClawHub hostilespider/recon-quick
    - ClawHub gpyangyoujun/multi-search-engine
    - ClawHub cineglobe/osint-investigator
    - ClawHub sinndarkblade/deepdive-osint
    - ClawHub djc00p/deep-research-ecc
    - ClawHub ericsantos/perplexity-deep-search
    - ClawHub rogersuperbuilderalpha/academic-research
    - ClawHub guleguleguru/osint-social
    - ClawHub iyeque/unified-web-search
    - ClawHub robbyczgw-cla/web-search-plus
    - erolyan/hack-skills-Cybersecurity (cyberspace search engines)
    - qazbnm456/awesome-web-security
    - rbartoli/agent-skills (osint)
    - ljagiello/ctf-skills (ctf-osint)
---

# Web Intelligence & Security Search

A unified, method-driven playbook for finding information on the internet: general web research,
OSINT, security reconnaissance, threat intelligence, and evidence-grade reporting. Designed to be
tool-agnostic: use built-in web search/fetch when available, add APIs or CLI tools when needed.

**Ethics first.** This skill is for authorized security testing, defensive research, journalism,
due diligence, CTF, and learning. Only search/scan assets you own or have written permission to
test. Respect terms of service, robots.txt, privacy law, and rate limits. Never use discovered
credentials, never download illegal material, and never publish third-party PII.

## Trigger Keywords

Use this skill whenever the request contains any of these - even if the user does not say
"search". The router (Section 0.5) picks the module; the process (Section 1) is mandatory.

**English:** search, research, find, look up, investigate, OSINT, recon, footprint, attack surface,
dork, Google dork, GitHub dork, Shodan, Censys, FOFA, ZoomEye, Hunter, BinaryEdge, Netlas, Quake,
CVE, PoC, exploit, 0day, 1day, n-day, patch diff, vulnerability, advisory, CVSS, KEV, EPSS,
bug bounty, bounty program, scope, HackerOne, Bugcrowd, Intigriti, YesWeHack, Immunefi, Huntr,
writeup, how I found, case study, cheatsheet, payload, wordlist, bypass, WAF, red team, redteam,
adversary emulation, C2, ATT&CK, OPSEC, purple team, appsec, secure code, SAST, DAST, SCA,
code review, secure SDLC, threat model, STRIDE, LLM, GenAI, agentic AI, prompt injection, AIBOM,
supply chain, DFIR, detection engineering, beneficial ownership,
architecture, zero trust, cloud security,
debug, stack trace, crash, reproduce, root cause, fuzzing, lab, CTF, HTB, TryHackMe, PortSwigger,
conference, blog, research, malware, phishing, leak, breach, IOC, exposed, subdomain, certificate,
reverse image, pentest, source list, source ledger, used sources, read but not used, bibliography.

**Tiếng Việt:** tìm kiếm, tra cứu, nghiên cứu, tìm hiểu, điều tra, thu thập thông tin, trinh sát,
bề mặt tấn công, tìm lỗ hổng, săn bug, bug bounty, writeup, kinh nghiệm, PoC, khai thác, cheatsheet,
payload, red team, redteam, debug, gỡ lỗi, appsec, bảo mật ứng dụng, bảo mật AI, LLM, kiến trúc bảo mật, threat model,
cloud security, lab, CTF, blog bảo mật, mã độc, rò rỉ dữ liệu, tìm tài khoản, tìm người, tìm công ty,
tìm tên miền, tìm IP, kiểm tra rò rỉ, tìm ảnh gốc, pentest, danh sách nguồn, nguồn đã dùng,
nguồn đã đọc, link nguồn, nguồn tham khảo.

---

## 0. Operating Principles

1. **Objective before query.** Define the question, the decision it supports, and the acceptable
   confidence level. A search without an objective becomes a rabbit hole.
2. **Passive before active.** Prefer public/indexed data before touching the target. Active probes
   (DNS brute force, port scan, directory fuzzing) require explicit authorization.
3. **Multiple engines, multiple angles.** No single index is complete. Cross-check Google + Bing +
   DuckDuckGo + regional engines, then cyberspace engines for infrastructure.
4. **Triangulate.** A fact is only "confirmed" when backed by 2-3 independent, preferably primary,
   sources. Record the source URL and date for every claim.
5. **Pivot on identifiers.** Every finding is a new seed: domain → IP → ASN → certificate → favicon →
   component → email → username → repository → secret. Search is a graph walk, not a single query.
6. **Timebox.** Use a deliberate budget (e.g., 20% planning, 50% collection, 30% verification and
   reporting). Stop expanding when marginal findings drop.
7. **Document as you go.** Save queries, URLs, timestamps, screenshots/archives, and raw results.
   Reproducibility is part of the deliverable.
8. **Treat results as claims, not truth.** SEO spam, AI-generated pages, stale indexes, and
   misattributed hosts are common. Verify before reporting.

---

## 0.5 Module Router & Process Contract

This skill is a **router + a mandatory process**. The Universal Search Loop (Section 1) and the
verification/reporting rules (Section 10) always apply. A module only changes the source pack,
query recipes, and output fields - never the process.

### Invocation policy
- Invoke for information-seeking work: find, compare, verify, investigate, learn, monitor.
- Invoke even when the user only supplies a keyword or identifier (e.g., `CVE-2024-3400`,
  `IDOR writeup`, `HackTheBox`, `zero trust AWS`).
- Do not invoke for pure implementation or editing unless research is needed; then scope the skill
  to the research step only.
- If the request asks to attack a real target without authorization, refuse the action and offer
  authorized/defensive alternatives.
- For a trivial, stable fact, one search + one verification is enough; do not over-engineer.

### Router algorithm
1. Parse the request: intent, target type, domain, and explicit keywords.
2. Match the intent against the module table. Select **1 primary** module and **0-2 secondary**
   modules. If ambiguous, ask one clarifying question or run both and label the results.
3. Load the selected pack(s) from `references/modules/`.
4. Execute the Universal Search Loop end-to-end:
   **Frame -> Plan -> Expand -> Collect -> Verify -> Report**.
5. Log every query/dork, source URL, and date.
6. Pass the Process Compliance Gate before answering.
7. If the request spans domains, chain modules in order. Examples:
   - Bug bounty research: M1 -> M2 -> M3 -> M4 -> M9
   - Vulnerability reproduction: M3 -> M11 -> M8 -> M9
   - AppSec/architecture review: M6 -> M7 -> M12
   - Red team preparation: M5 -> M10 -> M9 -> M12

### Module selection table
| User keywords / intent | Primary module | Pack |
|---|---|---|
| bug bounty, bounty program, HackerOne, Bugcrowd, Intigriti, YesWeHack, Immunefi, Huntr, scope, VDP, reward, triage, duplicate, disclosure policy | M1 Bug Bounty | `01-bug-bounty.md` |
| writeup, how I found, case study, kinh nghiệm săn bug, bug story, disclosure, blog post, Medium, dev.to, HackerOne Hacktivity | M2 Writeups & Experience | `02-writeups-experience.md` |
| CVE, PoC, exploit, 0day, 1day, n-day, patch diff, vulnerability research, advisory, CVSS, KEV, EPSS, Exploit-DB, Nuclei template | M3 CVE & PoC | `03-cve-poc-exploit.md` |
| cheatsheet, payload, wordlist, bypass, WAF, one-liner, command, exploitation, privilege escalation, reverse shell | M4 Cheatsheets & Payloads | `04-cheatsheets-payloads.md` |
| red team, redteam, adversary emulation, C2, ATT&CK, OPSEC, initial access, lateral movement, persistence, purple team, DFIR, detection engineering | M5 Red Team | `05-redteam-adversary-emulation.md` |
| appsec, secure code, SAST, DAST, SCA, code review, secure SDLC, threat model, STRIDE, OWASP Top 10, ASVS, LLM, GenAI, supply chain | M6 AppSec & Secure Code | `06-appsec-secure-code.md` |
| architecture, security architecture, zero trust, cloud security, AWS/Azure/GCP security, reference architecture, NIST/CIS, design review, segmentation | M7 Security Architecture | `07-security-architecture-cloud.md` |
| debug, gỡ lỗi, stack trace, crash, reproduce, root cause, fuzzing, gdb, sanitizer, error message, binary analysis | M8 Debugging & Reproduction | `08-debugging-reproduction.md` |
| lab, CTF, training, HTB, TryHackMe, PortSwigger Academy, VulnHub, learn, practice, certification | M9 Labs, CTF & Training | `09-learning-labs-ctf.md` |
| blog, research, conference, DEF CON, Black Hat, BSides, OWASP chapter, X/Twitter, Mastodon, Reddit, Discord, newsletter, YouTube | M10 Community & Research | `10-community-conferences-research.md` |
| vendor advisory, patch, MSRC, security bulletin, release notes, CVE bulletin, PSIRT, changelog | M11 Vendor Advisories | `11-vendor-advisories-patch-diff.md` |
| methodology, PTES, OWASP WSTG, OSSTMM, NIST 800-115, scoping, rules of engagement, report, remediation | M12 Methodology & Reporting | `12-methodology-reporting.md` |
| threat intel, malware, IOC, phishing, leak, breach, dark web (legal sources) | Section 7 + M3/M10 | existing sections |
| person, domain, IP, email, username, image | Section 6 + relevant module | existing sections |

### Routing rules
- **Search, not attack.** This skill finds information. Do not run exploits, brute force, or
  destructive actions from a module. Lab validation only in authorized environments.
- **One primary module.** Secondary modules only when they add a distinct source class.
- **Always verify.** Bug bounty writeups and PoCs are often incomplete, outdated, or wrong. Confirm
  against the vendor advisory, patch, or a lab environment.
- **Never copy-paste payloads blindly.** Understand preconditions, target version, and impact.
- **Cite the module.** In the final output, state which module(s) were used.

### Process Compliance Gate
Before delivering any answer, confirm:
- [ ] Objective, scope, and authorization status stated.
- [ ] Primary/secondary modules selected and named.
- [ ] At least two source classes used (primary + secondary/index) unless the fact is trivial.
- [ ] Exact queries/dorks and dates logged.
- [ ] Claims carry URL + date + confidence (A-D).
- [ ] Source ledger lists every URL used for synthesis and every URL read but excluded, with a
      reason for exclusion.
- [ ] Contradictions and unknowns called out.
- [ ] No unredacted secrets, PII, or illegal content.
- [ ] Output follows the report template (Section 9.3).

If a box cannot be checked, keep searching or state the limitation explicitly.

### Worked routing examples
| Request | Route |
|---|---|
| "Tìm writeup bug bounty về IDOR trên HackerOne" | M2 primary; M1 if scope/program lookup is needed |
| "CVE-2024-3400 có PoC chưa?" | M3 primary; M11 for vendor patch; M8 for lab reproduction |
| "Cheatsheet leo thang đặc quyền Linux" | M4 primary; M9 for lab practice |
| "Thiết kế zero trust cho AWS" | M7 primary; M6 if app threat modeling is included |
| "Debug crash trong binary CTF" | M8 primary; M9 for challenge context |
| "Red team ATT&CK technique cho initial access" | M5 primary; M10 for recent research |
| "So sánh OWASP ASVS và NIST 800-53" | M6 + M7 + M12 |

---

## 1. The Universal Search Loop

Use this loop for any research task, from a simple fact-check to a full attack-surface assessment.

### Phase 1 - Frame
- Restate the objective in one sentence.
- Identify target type(s): person, username, email, phone, domain, IP/CIDR, ASN, organization,
  image, document, malware sample, CVE/product, event, or topic.
- Define scope and constraints: legal authorization, time range, geography, language, depth,
  output format.
- List 3-5 sub-questions that together answer the objective.

### Phase 2 - Plan sources
- **Primary sources:** official records, vendor advisories, registries, raw data, the target itself.
- **Secondary sources:** news, blogs, aggregators, social media, analysis platforms.
- **Indexes:** general search engines, code search, cyberspace scanners, archives, academic indexes.
- Prefer primary sources for facts, secondary for context, aggregators for discovery only.

### Phase 3 - Query expansion
Build a keyword matrix before searching:
- Synonyms and jargon (`breach` / `leak` / `dump`; `CVE` / `vulnerability` / `advisory`)
- Translations (English, Vietnamese, Chinese, Russian as relevant)
- Entity variants: legal name, trade name, abbreviations, typos, old names, subsidiaries
- Identifier variants: domain with/without `www`, punycode, IP, ASN, cert CN/SAN, favicon hash
- File types and platforms likely to host the answer
- Time constraints (`before:` / `after:` / `tbs=qdr:`)

### Phase 4 - Collection
- Start broad, then narrow with operators.
- Run the same intent across 2-4 engines.
- Paginate; the best result is often beyond page 1.
- Deep-fetch promising sources instead of trusting snippets.
- For each hit, extract: URL, title, author, date, key claim, and next pivot.
- Maintain a source ledger from the first click: URL, title, author/date, key claim, and status
  (used for synthesis / read but not used / inaccessible).

### Phase 5 - Verification
- Confirm with an independent source (different owner/domain).
- Check recency and whether the page is archived/altered.
- Look for contradictions and explain them.
- Assign confidence: **Confirmed** (primary + corroboration), **Likely** (2+ independent),
  **Possible** (single source), **Unverified** (lead only).
- Preserve evidence: Wayback/archive.today link, screenshot, raw JSON/HTML.

### Phase 6 - Report
- Lead with the answer, then evidence.
- Separate fact, inference, and speculation explicitly.
- Include the exact queries/dorks used (reproducibility).
- Provide next steps and confidence levels.
- Append the Source Ledger: sources used for synthesis and sources read but not used, each with a
  link and a reason for exclusion.

---

## 2. General Web Search Engines

### 2.1 Engine selection
| Need | Best first choices |
|---|---|
| Broad general web | Google, Bing, Brave |
| Privacy / no tracking | DuckDuckGo, Startpage, Brave, Qwant |
| Independent index | Mojeek, Marginalia, Brave |
| Regional / non-English | Yandex (RU), Baidu/Sogou/360 (CN), Naver (KR), Seznam (CZ) |
| Exact phrase / technical | Google, Bing |
| News / recent | Google News, Bing News, GDELT, NewsAPI |
| Academic | Google Scholar, OpenAlex, Semantic Scholar, arXiv, PubMed |
| Code | GitHub, GitLab, Sourcegraph, grep.app |
| Infrastructure | Shodan, Censys, FOFA, ZoomEye, Netlas, Quake |

### 2.2 Core operators (Google-style; most work on Bing/Brave with small differences)
```
site:example.com                 restrict to domain (site:*.example.com for subdomains)
inurl:admin                     term in URL
intitle:"index of"              term in title
intext:"password"               term in body
filetype:pdf                    file type (ext: is an alias)
"exact phrase"                  exact match
-word / -site:example.com       exclude
OR / |                          boolean OR
*                               wildcard
AROUND(3)                       proximity (Google)
before:2024-01-01 after:2023-01-01   date range
numrange:1000-5000              numeric range
related:example.com             similar sites
cache:example.com               cached copy (often unreliable)
source:reuters                  news source (Google News)
```
Time filters: Google `&tbs=qdr:h|d|w|m|y` (hour/day/week/month/year); Bing `&filters=ex1:"ez5_..."`.

**Bing specifics:** `inbody:`, `ip:`, `language:`, `loc:`, `contains:`, `site:`, `filetype:`.
**Yandex specifics:** strong for reverse image, regional content, and some operator behavior that
differs from Google; supports `site:`, `host:`, `mime:`, `title:`, `url:`, `date:`.
**DuckDuckGo:** supports common operators and `!bang` shortcuts (`!gh`, `!so`, `!w`, `!yt`, `!g`).

### 2.3 Search APIs and automation
- **Google Programmable Search (CSE)** - 100 free queries/day, then paid.
- **SerpAPI / Serper / SearchAPI** - SERP scraping APIs, multi-engine.
- **Brave Search API** - independent index, generous developer tier.
- **Bing Web Search API** - being retired in some tiers; check current availability.
- **Tavily** - agent-oriented search + extraction.
- **Exa** - neural/semantic search and similar-page discovery.
- **Perplexity API (sonar / sonar-reasoning / sonar-deep-research)** - cited answers.
- **SearXNG** - self-hosted metasearch across dozens of engines; best for privacy and no key.
- **Firecrawl / Crawl4AI** - crawl and extract page content for agents.
- **GDELT / NewsAPI / Common Crawl** - news and web-scale datasets.

Rule: prefer APIs over scraping; obey quotas and ToS; cache responses; deduplicate by canonical URL.

### 2.4 Search quality heuristics
- Add `site:` early to cut noise; add `-site:` to remove known junk domains.
- Keep queries to 2-4 operators; stacking more usually reduces recall.
- Quote multi-word phrases; unquoted words are ANDed by most engines.
- Search in the target's language; translate key terms and product names.
- Use file-type targeting for documents (`filetype:pdf/xlsx/csv/sql/env`).
- Use date operators for incidents, breaches, and vulnerabilities.
- Search exact error strings and unique code fragments; they identify software precisely.
- Check spelling variants, old product names, and vendor renames.

---

## 3. Security & Cyberspace Search Engines

These index hosts and services, not page text. Use them for asset discovery, fingerprinting,
certificate pivoting, and finding exposed services.

### 3.1 Shodan
Filters: `port:`, `hostname:`, `net:`, `org:`, `asn:`, `country:`, `city:`, `geo:`, `os:`,
`product:`, `version:`, `http.title:`, `http.html:`, `http.status:`, `http.favicon.hash:`,
`http.component:`, `ssl:`, `ssl.cert.subject.CN:`, `ssl.cert.issuer.CN:`, `vuln:`, `has_vuln:`,
`tag:`, `device:`, `isp:`, `uptime:`, `before:`, `after:`, `-` (exclude), `"..."`.
- CLI: `shodan init KEY`, `shodan search`, `shodan count`, `shodan host`, `shodan download`,
  `shodan parse`, `shodan stats`.
- Free IP summary: `https://internetdb.shodan.io/<ip>` (ports, hostnames, vulns, tags).
- High-value pivots: `org:"Target"`, `ssl:"target.com"`, `http.favicon.hash:<hash>`,
  `http.title:"Login"`, `port:27017/9200/6379/11211`, `product:"Elastic"`, `vuln:CVE-...`.

### 3.2 Censys
CenQL examples:
```
host.services.port: 443
host.services.service_name: HTTP
autonomous_system.organization: "Target Inc"
autonomous_system.asn: 12345
host.services.tls.certificates.leaf_data.subject.organization: "Target Inc"
host.services.tls.certificates.leaf_data.names: target.com
cert.names: target.com
services.http.response.status_code: 200
web.hostname: target.com
```
- Certificate data is Censys's strength: pivot from a cert to every host presenting it.
- Search hosts, web properties, and certificates separately; combine with `and`, `or`, `not`.
- API/CLI: `censys search`, `censys view`; mind index names and version differences.

### 3.3 FOFA
Syntax: `domain=`, `host=`, `ip=`, `port=`, `protocol=`, `app=`, `title=`, `body=`, `header=`,
`cert=`, `cert.subject=`, `cert.issuer=`, `server=`, `icon_hash=`, `fid=`, `http_status=`,
`os=`, `country=`, `region=`, `city=`.
- Logic: `&&`, `||`, `!=`, parentheses. Example: `domain="example.com" && port="443"`.
- Strong Web-fingerprint and China/APAC coverage. Pivot via `cert=` and `icon_hash=`.

### 3.4 ZoomEye
Fields: `app:`, `app.version:`, `port:`, `service:`, `device:`, `title:`, `header:`, `body:`,
`ip:`, `cidr:`, `domain:`, `subdomain:`, `country:`, `city:`, `ssl:`, `ssl.cert.`,
`iconhash:`, `filehash:`.
- Good for network devices and global coverage; supports historical data on paid tiers.

### 3.5 Other engines
- **Hunter (鹰图)** - `domain=`, `ip=`, `web.title=`, `web.body=`, `web.icon=`, `cert=`,
  `port=`, `protocol=`, `app=`; strong Chinese web assets.
- **BinaryEdge** - `ip:`, `port:`, `domain:`, `country:`, `product:`, `tag:`, `type:`.
- **Netlas** - query DSL over hosts, domains, certificates; favicon and cert pivots.
- **Quake (360)** - `title:`, `body:`, `cert:`, `ip:`, `port:`, `app:`, `service:`, `domain:`,
  `region:`, `isp:`.
- **Criminal IP** - exposure scoring, filters for open services, CVEs, phishing.
- **GreyNoise** - classify IPs as benign scanner noise vs targeted activity; RIOT for known
  business services. Query examples: `classification:malicious`, `tags:...`, `ip:...`.
- **LeakIX** - exposed services, leaks, and misconfigurations with HTTP/plugin filters.
- **Onyphe** - passive DNS, certificates, and infrastructure datasets.
- **VirusTotal** - `domain:`, `ip:`, `file:`, `url:`, relations and passive DNS.

### 3.6 Infrastructure pivot playbook
1. **Domain → DNS**: A/AAAA/MX/NS/TXT/CNAME/SOA; SPF/DMARC/DKIM reveal vendors.
2. **Domain → certificates**: crt.sh, Cert Spotter, Censys certs, `ssl:` in Shodan/FOFA.
3. **Domain → subdomains**: passive DNS (SecurityTrails, VirusTotal), CT logs, subfinder/amass.
4. **IP → ASN/org**: BGP.he.net, RIPEstat, ipinfo; then `org:` / `asn:` in cyberspace engines.
5. **IP → neighbors**: same /24, same ASN, same certificate, same favicon.
6. **Favicon → hosts**: compute MurmurHash3 of the favicon and search `http.favicon.hash`.
7. **Component → hosts**: `app:`, `product:`, `http.component:` for the same tech stack.
8. **Email → domain → accounts**: format patterns, HIBP, Gravatar, account-discovery tools.
9. **Repository → secrets → cloud assets**: GitHub dorks, then cloud provider enumeration (authorized).
10. **Archive → deleted assets**: Wayback CDX and archive.today for removed pages/subdomains.

Always validate attribution: shared hosting, CDNs, and cloud IPs often produce false positives.

---

## 4. Dorking: Google, GitHub, and Paste Sites

Dorking is structured search using operators to surface content that was never meant to be indexed.
Use it for exposure discovery and attack-surface mapping. Full library: `references/dorks.md`.

### 4.1 High-value Google dork categories
- **Open directories:** `intitle:"index of" site:target.com`
- **Sensitive documents:** `site:target.com filetype:pdf|xlsx|csv|docx|sql|env|bak`
- **Login/admin panels:** `site:target.com inurl:admin|login|dashboard|wp-admin`
- **Exposed configs/secrets:** `filetype:env "DB_PASSWORD"`, `filetype:pem "PRIVATE KEY"`
- **Cloud storage:** `site:s3.amazonaws.com "target"`, `site:storage.googleapis.com`,
  `site:blob.core.windows.net`
- **Cameras/IoT:** `intitle:"Live View" inurl:axis-cgi`, `inurl:ViewerFrame?Mode=`
- **Paste/leak sites:** `site:pastebin.com "target.com"`, `site:rentry.co`, `site:ghostbin`
- **Code/CI leakage:** `site:github.com "target.com" password`, `filetype:yml "secrets"`
- **Error/vuln signals:** `intext:"SQL syntax"`, `intitle:"phpinfo()"`, `inurl:server-status`
- **Employee/contact intel:** `site:linkedin.com/in "Target Inc"`, `"@target.com" filetype:xlsx`

Build dorks incrementally (domain → file type → keyword → negation). Verify results manually;
indexes are often stale and hits can belong to third parties.

### 4.2 GitHub and code search
Qualifiers: `in:name`, `in:description`, `in:readme`, `in:topics`, `in:file`, `in:path`,
`repo:owner/name`, `org:`, `user:`, `language:`, `path:`, `filename:`, `extension:`, `size:`,
`stars:`, `fork:`, `archived:`, `is:public`, `created:`, `pushed:`, `topic:`.
Examples:
```
org:target filename:.env
"AKIA" org:target
filename:.npmrc _auth
filename:.git-credentials
path:.github/workflows "secrets."
"BEGIN RSA PRIVATE KEY" org:target
extension:sql "INSERT INTO" org:target
```
Also search GitLab, Gitee, Sourcegraph, grep.app, and package registries (npm, PyPI, RubyGems,
Docker Hub) for leaked keys and internal hostnames. Tools: `gh search code`, GitDorker, gitleaks,
trufflehog, Gitrob, and `secret_scan.py`-style local scanners.

### 4.3 Secret discovery
Look for provider-specific prefixes and high-entropy strings. A regex catalog is in
`references/secrets.md`. Workflow:
1. Collect candidate files (code search, JS bundles, configs, backups, CI logs).
2. Run regex + entropy scans; deduplicate by hash.
3. **Validate read-only** only where the provider supports safe identity checks, and only on
   authorized engagements. Never use a secret to access data.
4. Report location, type, exposure window, and remediation; redact the value in reports.

---

## 5. OSINT by Target Type

Target-specific source packs live in `references/osint-targets.md`: domain/website,
IP/ASN/network, email, username/person, phone, image/video/geolocation, company/organization,
deep/dark web, research records, cryptocurrency, and flights/ships/physical. Pick the target type, load the pack, and apply the
same verification, privacy, and authorization rules.

---

## 6. Threat Intelligence & Vulnerability Search

### 6.1 Vulnerabilities and exploits
- **NVD** - `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-...` (API, rate-limited).
- **CVE.org / MITRE** - authoritative CVE records.
- **CISA KEV** - exploited-in-the-wild catalog, JSON feed; prioritize these.
- **EPSS** - probability of exploitation (`https://api.first.org/data/v1/epss?cve=...`).
- **OSV.dev** - open-source package vulnerabilities (API).
- **GitHub Security Advisories** - ecosystem advisories and patched versions.
- **Vulners / VulnCheck / CVEDetails / OpenCVE** - enrichment and search.
- **Exploit-DB** (`searchsploit`), Metasploit modules, Packet Storm, Rapid7 DB, AttackerKB.
- **Vendor advisories** - Microsoft MSRC, Cisco, Fortinet, Ivanti, VMware, Atlassian, etc.
- Search pattern: product + version + "advisory" / "CVE" / "exploit" / "patch"; check dates.

### 6.2 Malware, phishing, and IOCs
- **VirusTotal** - multi-engine files/URLs/domains/IPs, relations, passive DNS.
- **MalwareBazaar, URLhaus, ThreatFox, Feodo Tracker** - abuse.ch feeds.
- **Hybrid Analysis, Any.run, Joe Sandbox, Triage, CAPE** - dynamic analysis.
- **URLScan.io** - page snapshots, DOM, requests, infrastructure.
- **PhishTank, OpenPhish** - phishing feeds.
- **AlienVault OTX, MISP** - community threat intel and IOC sharing.
- **AbuseIPDB, GreyNoise, Spamhaus, Talos** - IP/domain reputation.
- **MITRE ATT&CK, CAPEC, CWE, D3FEND** - adversary techniques and weakness taxonomy.
- Hash lookups: VT, MalwareBazaar, ThreatFox, Malshare; never upload sensitive files publicly.

### 6.3 Detection and research
- Sigma rules, YARA rules, Suricata/Snort rules, Atomic Red Team.
- Vendor research blogs: Unit 42, Mandiant, CrowdStrike, Talos, Microsoft MSTIC, Google TAG,
  SANS ISC, Krebs, BleepingComputer, The Record, Dark Reading.
- Academic: arXiv (cs.CR), IEEE S&P, USENIX Security, NDSS, CCS; Google Scholar for follow-ups.
- Standards: NIST SP 800-61/115/137, ISO 27001/27035, OWASP Top 10/ASVS/WSTG, CIS Benchmarks.

### 6.4 Vulnerability research workflow
1. Identify product, version, and deployment (banner, headers, JS, changelog).
2. Map to CPE and query NVD/OSV/GitHub advisories.
3. Check KEV and EPSS to prioritize.
4. Find public PoC/exploit; read the patch diff when possible.
5. Verify applicability (version range, configuration, mitigations).
6. Document evidence and safe reproduction steps; never exploit outside scope.

---

## 7. Deep Research (non-security)

For market, technology, policy, or academic research, use a structured deep-research workflow:

1. **Clarify** the decision, audience, and required depth.
2. **Plan** 3-5 sub-questions and a source map (primary, secondary, data).
3. **Collect** 15-30 sources via multiple engines; prefer recent and primary.
4. **Deep-read** 3-5 key sources with full-page fetch.
5. **Extract** claims, numbers, dates, definitions, and disagreements into a matrix.
6. **Triangulate** and rate confidence; note what is unknown.
7. **Synthesize** a cited report: answer first, then evidence, caveats, and next steps.
8. **Archive** links and snapshots; include a bibliography.

Academic sources: OpenAlex (250M+ works, no key), Semantic Scholar, Crossref, arXiv, PubMed,
Google Scholar, JSTOR/ResearchGate (access permitting). For papers: DOI → citations → related work
→ authors' other papers. Prefer peer-reviewed sources for claims; preprints are leads.

---

## 8. Automation and Tooling

Full commands in `references/tooling.md`. Core patterns:

### 8.1 Lightweight agent loop
```
for query in queries:
    results = web_search(query, num=10-20)
    urls = dedupe(canonicalize(results))
    for url in top(urls):
        page = web_fetch(url)
        extract entities, dates, claims, pivots
    save(query, results, pages, timestamp)
    sleep(1-2s)  # respect rate limits
```

### 8.2 CLI toolkit (install only what you need)
- Recon: subfinder, amass, assetfinder, dnsx, httpx, naabu, nuclei, katana, gau, waybackurls,
  bbot, theHarvester, recon-ng, spiderfoot.
- Search: `shodan`, `censys`, `gh` (GitHub CLI), `searchsploit`.
- Identity: sherlock, maigret, holehe, PhoneInfoga.
- Media: exiftool, ffmpeg, imagemagick.
- Secrets: gitleaks, trufflehog, GitDorker.
- Scraping: curl + jq, Playwright, Firecrawl, Crawl4AI.

### 8.3 API hygiene
- Store keys in environment variables or a secret manager, never in the skill/repo.
- Cache results; deduplicate; log query + timestamp + engine.
- Handle 403/429 with exponential backoff; rotate sessions only where ToS permits.
- Pin tool versions; avoid `curl | bash` installs; verify checksums.

### 8.4 When to use which
| Task | Tooling |
|---|---|
| Quick fact / current event | web search + 2 fetches |
| Deep report | 3-5 sub-questions, 15-30 sources, synthesis |
| Attack surface | subfinder + httpx + nuclei + Shodan/FOFA |
| Leak hunting | GitHub code search + gitleaks + HIBP |
| IOC triage | VirusTotal + OTX + URLhaus + GreyNoise |
| Person/username | WhatsMyName/Sherlock + manual social verification |
| Image origin | Yandex/Lens/TinEye + exiftool + geolocation |

---

## 9. Verification, Confidence, and Reporting

### 9.1 Evidence grading
| Grade | Meaning | Basis |
|---|---|---|
| A - Confirmed | Directly observed in a primary source | Official record, raw data, target response |
| B - Likely | 2+ independent reliable sources agree | Corroborated reporting/telemetry |
| C - Possible | One credible source or indirect evidence | Single report, inference from artifact |
| D - Unverified | Lead only | Social post, unconfirmed index hit |

### 9.2 Common false positives
- Shared hosting/CDN IPs and cloud ranges.
- Stale search indexes and archived pages.
- Misattributed organization names in scanners.
- Homonyms (people, companies) and typo-squats.
- Honeypots and fake services; banners can lie.
- AI-generated/spam pages designed to rank for queries.

### 9.3 Report template
```markdown
# <Title>
## Executive summary (answer first)
## Scope & authorization
## Methodology (engines, tools, date range)
## Key findings (severity, evidence, confidence)
## Timeline / attack path (if applicable)
## Indicators (IOCs) and pivots
## Risks and impact
## Recommendations / remediation
## Sources used for synthesis
| # | Source | URL | Date | Claim supported |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |

## Sources read but not used
| # | Source | URL | Date | Reason excluded |
|---|---|---|---|---|
| 1 | ... | ... | ... | off-scope / stale / duplicate / low confidence / contradicted / inaccessible / discovery only |

## Appendix: queries, dorks, raw evidence
```

### 9.4 Severity
- Security findings: CVSS v3.1/v4.0 + EPSS + KEV status; or Critical/High/Medium/Low/Info.
- Business/research findings: impact × likelihood, with explicit assumptions.
- Always state what would change the conclusion.

### 9.5 Source ledger (mandatory)
Every answer includes a **Source Ledger** with two separate lists. Do not merge them.
- **Used for synthesis** - each source that directly supports, contradicts, or shapes a claim in
  the answer. Format: `title - URL - published/updated date - accessed date - claim supported`.
- **Read but not used** - each source you opened or deep-read but excluded. Format:
  `title - URL - date - reason`, where reason is one of: off-scope, stale, duplicate, lower quality,
  contradicted, inaccessible/paywalled, spam/malicious, discovery only, could not verify.

Rules:
- If a source was used only to find other sources, list it under "read but not used" as
  "discovery only" so the user can still see the research path.
- Do not list search-result pages as sources; list the destination URL. Keep the exact query in the
  methodology/appendix.
- If no source was read but excluded, write "None" explicitly.
- Redact tokens, PII, and sensitive query parameters; note the redaction.
- Build the ledger during research, not from memory at the end.

---

## 10. OPSEC and Skill Supply-Chain Safety

### 10.1 Research OPSEC
- Passive-first; avoid alerting the target until authorized.
- Separate identity/browser/VM for investigations; don't use personal accounts.
- VPN/Tor only where legal and appropriate; note that some sources block them.
- Don't log into target services; don't reuse passwords; don't upload sensitive files.
- Minimize collected PII; set retention limits; encrypt at rest.

### 10.2 Verify before installing any third-party skill
The ClawHavoc incident (1,184 malicious skills on ClawHub) and Snyk's ToxicSkills research
(~36.8% of skills with flaws) show that skill registries are an attack surface. Before installing:
- Read the full `SKILL.md` and every script; look for prompt injection, hidden instructions,
  `curl | bash`, base64/obfuscation, credential access, or unexpected network calls.
- Check publisher identity, download velocity, version history, and security audit.
- Scan with a skill vetter (e.g., Skill Vetter, agentscanner) and static analysis.
- Pin versions; install in a sandbox without secrets; restrict network and filesystem access.
- Prefer official or well-known publishers; re-review on every update.

---

## 11. Quick Reference: Query Recipes

Copy-paste starting points live in `references/quick-recipes.md` (exact errors, exposed documents,
admin panels, subdomains, repo secrets, Shodan/Censys/FOFA pivots, breach search, CVE enrichment,
reverse image, username spread). Adapt every recipe to the target and verify against a primary source.

---

## 12. Anti-Patterns

- Searching only one engine and declaring "not found".
- Trusting snippets without opening the source.
- Treating scanner attribution as ground truth.
- Running active scans without written authorization.
- Using discovered credentials "just to check".
- Publishing PII or unredacted secrets.
- Installing unvetted skills/tools that exfiltrate data.
- Reporting without dates, URLs, or confidence levels.
- Listing only used sources and hiding sources that were read but rejected; show both with reasons.
- Providing a bibliography without mapping each source to the claim it supports.
- Expanding scope endlessly instead of answering the question.

---

## 13. Domain Modules

Each module is a self-contained source pack. Load only the modules selected by the router.
Every module follows the same contract: purpose, triggers, primary sources, query recipes,
workflow, output, pitfalls, ethics.

| Module | File | What it answers |
|---|---|---|
| M1 Bug Bounty | `references/modules/01-bug-bounty.md` | Programs, scope, disclosure policy, platforms, triage, rewards |
| M2 Writeups | `references/modules/02-writeups-experience.md` | Real-world bug stories, methodology, lessons learned |
| M3 CVE & PoC | `references/modules/03-cve-poc-exploit.md` | Vulnerability records, PoCs, exploits, patch diffs, exploitation status |
| M4 Cheatsheets | `references/modules/04-cheatsheets-payloads.md` | Payloads, commands, wordlists, bypass techniques, quick references |
| M5 Red Team | `references/modules/05-redteam-adversary-emulation.md` | Adversary emulation, ATT&CK, C2, OPSEC, purple team |
| M6 AppSec | `references/modules/06-appsec-secure-code.md` | Secure code, SAST/DAST/SCA, code review, threat modeling, LLM/GenAI |
| M7 Architecture | `references/modules/07-security-architecture-cloud.md` | Zero trust, cloud security, reference architectures, controls |
| M8 Debugging | `references/modules/08-debugging-reproduction.md` | Crash triage, debugging, fuzzing, root cause, reproduction |
| M9 Labs/CTF | `references/modules/09-learning-labs-ctf.md` | Practice platforms, challenges, certifications |
| M10 Community | `references/modules/10-community-conferences-research.md` | Blogs, conferences, researchers, newsletters, social |
| M11 Advisories | `references/modules/11-vendor-advisories-patch-diff.md` | Vendor patches, bulletins, changelogs, PSIRT |
| M12 Methodology | `references/modules/12-methodology-reporting.md` | Frameworks, scoping, RoE, reporting, remediation |

**Module chaining:** M1 -> M2 -> M3 -> M4 -> M9 is the classic bug-bounty research chain.
M6 -> M7 -> M12 is the appsec/architecture review chain. M3 -> M11 -> M8 is the vulnerability
reproduction chain.

**Module output contract.** Every module run must return:
```
module:            M# <name>
objective:         one sentence
authorization:     authorized / lab / public-only / unknown
queries:           exact queries and dorks used
sources_used:      exact URL + title + date + claim supported
sources_read:      exact URL + title + date + reason read but not used
findings:          claim + evidence + confidence (A-D)
pivots:            next identifiers or sources to check
caveats:           gaps, contradictions, stale/unsupported claims
```

---

## 14. References

All reference paths are relative to this skill directory; in OpenClaw resolve them as
`{baseDir}/references/...`.

- `references/engines.md` - operator cheat sheets and API endpoints (Google, Bing, GitHub,
  Shodan, Censys, FOFA, ZoomEye, Hunter, BinaryEdge, Netlas, Quake).
- `references/dorks.md` - categorized Google/GitHub/Shodan/cloud/paste dork library.
- `references/secrets.md` - secret regex catalog and validation notes.
- `references/tooling.md` - CLI commands, install hints, and automation snippets.
- `references/quick-recipes.md` - copy-paste query recipes and safety notes.
- `references/osint-targets.md` - target-specific OSINT source packs and meta-hubs.
- `references/modules/` - the 12 domain modules listed in Section 13.

Source skills/repos synthesized:
Claude-OSINT (elementalsouls), UseOSINT/Skills (28 OSINT skills), awesome-claude-security
(jassics), dorking-skill (zbailey83), Claude-Dork (danielrosehill), ClawHub: web-recon (p0lish),
recon-quick (hostilespider), multi-search-engine (gpyangyoujun), osint-investigator (cineglobe),
deepdive-osint (sinndarkblade), deep-research (djc00p / ANVEAI / samber),
perplexity-deep-search (ericsantos), academic-research (rogersuperbuilderalpha),
osint-social (guleguleguru), unified-web-search (iyeque), web-search-plus (robbyczgw-cla),
hack-skills-Cybersecurity (erolyan), awesome-web-security (qazbnm456), agent-skills osint
(rbartoli), ctf-osint (ljagiello).

Module source packs additionally draw from: HackerOne Hacktivity, Bugcrowd CrowdStream,
Intigriti, YesWeHack, Immunefi, Huntr, arkadiyt/bounty-targets-data, Pentester Land,
InfoSec Write-ups, PayloadsAllTheThings, HackTricks, Internal All The Things, OWASP
WSTG/ASVS/Cheat Sheets, PortSwigger Web Security Academy and Research, NVD, CVE.org,
CISA KEV, EPSS, OSV, GitHub Advisories, Exploit-DB, Packet Storm, nomi-sec/PoC-in-GitHub,
trickest/cve, ARPSyndicate/cvemon, Nuclei templates, MITRE ATT&CK, Atomic Red Team, Red Team
Notes, GTFOBins, LOLBAS, Sigma, Semgrep, CodeQL, Snyk, NIST, CIS, AWS/Azure/GCP security
documentation, and the vendor PSIRT/advisory pages listed in M11.
