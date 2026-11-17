# M10 - Community, Conferences, Blogs & Research Tracking

**Purpose:** Find and track credible security research, blogs, conference talks, researchers,
newsletters, and community discussions. Build a repeatable monitoring workflow instead of relying
on random links.

**Triggers:** blog, blogger, personal blog, research, conference, DEF CON, Black Hat, BSides,
OWASP chapter, X/Twitter, Mastodon, Bluesky, Reddit, Discord, newsletter, mailing list, YouTube,
podcast, security news, researcher, "who is working on", "latest research", "follow",
Chinese-language, 中文, 先知, 安全客, FreeBuf, 看雪, 安全内参.

**Process contract:** Always run the Universal Search Loop (Section 1) and the Process Compliance
Gate (Section 0.5). This module supplies sources and queries only.

---

## Primary sources

### Conferences
- **DEF CON** (`defcon.org`), **Black Hat** (`blackhat.com`), **BSides** (local sites).
- **OWASP Global AppSec**, **OWASP chapters**.
- **RSA Conference**, **SANS** events.
- **InfoconDB** (`infocondb.org`) - searchable index of security conferences and talks.
- **media.ccc.de** - CCC Congress, camp, and related talk archive (video and audio).
- **Nullcon**, **HITB**, **Pwn2Own**, **CanSecWest**, **OffensiveCon**, **REcon**, **BlueHat**.
- **CTF competitions** (see M9).

### Research labs and blogs
| Source | Focus |
|---|---|
| **PortSwigger Research** | Web exploitation, Burp |
| **Google Project Zero** | 0-days, exploitation |
| **Google TAG** | Threat actors |
| **Microsoft MSTIC** | Threat intelligence |
| **Unit 42 (Palo Alto)** | Threat research |
| **Mandiant** | Incident response, APTs |
| **CrowdStrike** | Adversary intelligence |
| **Cisco Talos** | Malware, vulnerabilities |
| **Recorded Future** | Threat intelligence |
| **SentinelLabs** | Malware, adversaries |
| **Volexity** | Incident response |
| **ESET / Kaspersky GReAT** | Malware research |
| **SANS ISC** | Daily handler diaries |
| **Krebs on Security** | Investigations |
| **BleepingComputer / The Record / Dark Reading / SecurityWeek** | News |
| **Assetnote** | Web research |
| **SpecterOps** | AD/red team, attack paths |
| **TrustedSec** | Offensive security, red team |
| **Bishop Fox** | Offensive security, appsec |
| **Zero Day Initiative** | Vulnerability research and disclosure |
| **ProjectDiscovery** | Recon and bug-bounty tooling |
| **Individual researcher blogs** | Global and Chinese-language researchers; see below |

### Individual researcher blogs
Global:
- **Orange Tsai** (`blog.orange.tw`) - web/AppSec exploitation, bug bounty.
- **Sam Curry** (`samcurry.net`) - web, automotive, and Web3 bug bounty.
- **James Kettle** (`jameskettle.com`) - HTTP desync and web research portfolio; primary
  publications are usually on PortSwigger Research.
- **EdOverflow** (`edoverflow.com`) - web security, security.txt, bug bounty.
- **0xdf** (`0xdf.gitlab.io`) - HTB/CTF, Active Directory, malware analysis.
- **Gynvael Coldwind** (`gynvael.coldwind.pl`) - reverse engineering, CTF, low-level security.
- **harmj0y** (`blog.harmj0y.net`) - Active Directory and red-team research.
- **ADSecurity** (`adsecurity.org`) - Active Directory/Entra ID security.

Chinese-language:
- **倾旋** (`payloads.online`) - red team, Active Directory, internal pentest.
- **离别歌 / phith0n** (`leavesongs.com`) - AppSec, Java/Python, vulnerability research.
- **素十八** (`su18.org`) - Java security and code audit.
- **K0rz3n** (`k0rz3n.com`) - web/Java security and vulnerability analysis.
- **TeamsSix** (`teamssix.com`) - cloud security and red team.
- **Nuclear'Atk** (`lcx.cc`) - exploit and red-team research lab.

Last link check: 2026-10-20. Dates on homepages are not publication guarantees; verify the post
author/date before citing. LiveOverflow, IppSec, NahamSec, and STÖK remain under YouTube because
video is their primary active channel. Several older high-signal blogs are archives; use them only
when the historical technique is still relevant.

### Social and community
- **X/Twitter** infosec lists; **Mastodon** `infosec.exchange`; **Bluesky**.
- **Reddit**: `r/netsec`, `r/bugbounty`, `r/AskNetsec`, `r/redteamsec`, `r/ReverseEngineering`,
  `r/malware`, `r/blueteamsec`.
- **Discord/Slack**: vendor and community servers (Bugcrowd, HackerOne, ProjectDiscovery, OWASP).
- **LinkedIn** for researchers and vendors.
- **YouTube**: LiveOverflow, IppSec, John Hammond, STÖK, NahamSec, The Cyber Mentor, PwnFunction,
  InsiderPhD, Critical Thinking.
- **Podcasts**: Darknet Diaries, Security Now, Risky Business, Critical Thinking.

### Newsletters and aggregators
- tl;dr sec, Risky Business, Unsupervised Learning, SANS NewsBites, Infosec Weekly,
  Sector035 Week in OSINT (`sector035.nl`), Detection Engineering Weekly
  (`detectionengineering.net`), Bug Bounty Reports Explained, PortSwigger Daily Swig archive.
- Hacker News, Lobsters (filtered).
- CISA advisories, vendor PSIRT RSS.

### Chinese-language sources
- **先知社区** (`xz.aliyun.com`) - Alibaba Cloud security community; web, cloud, red-team research.
- **奇安信攻防社区** (`forum.butian.net`) - offensive security, vulnerability research, SRC notes.
- **安全KER / 安全客** (`anquanke.com`) - security news, vulnerability analysis, courses.
- **FreeBuf** (`freebuf.com`) - Chinese security industry portal and community articles.
- **看雪** (`bbs.kanxue.com`) - reverse engineering, malware, mobile, IoT, and software security.
- **安全脉搏** (`secpulse.com`), **嘶吼** (`4hou.com`), **安全内参** (`secrss.com`) - technical
  and industry aggregators; 安全内参 is policy/decision-maker focused.
- **SecWiki** (`sec-wiki.com`) - Chinese security news/tool index; **T00ls** (`t00ls.com`) -
  long-running forum and directory (login may be required).
- **Seebug** (`seebug.org`) - vulnerability/PoC platform (see M3); **Gitee** (`gitee.com`) and
  **GitCode** (`gitcode.com`) - Chinese code hosting/mirrors for security tools and PoCs.
- Vendor labs: **Tencent Xuanwu** (`xlab.tencent.com`), **Tencent Keen Lab**
  (`keenlab.tencent.com`), **QiAnXin Red Raindrop** (`ti.qianxin.com/blog`).
- Several Chinese sites return 403/405 to automated clients or require JavaScript/login. Use a
  browser, follow site terms and robots rules, and verify translations against the primary source.

---

## Query recipes

```text
# Research by topic
site:portswigger.net/research "SSRF"
site:googleprojectzero.blogspot.com "exploit"
site:unit42.paloaltonetworks.com "campaign"
site:mandiant.com/resources/blog "APT"
site:talosintelligence.com "vulnerability"
site:isc.sans.edu "diary" "CVE"

# Conference material
"DEF CON" "slides" 2025
site:blackhat.com "briefings" "2025"
site:infocondb.org "DEF CON"
site:media.ccc.de "security"
"BSides" "talk" "slides"
"OWASP" "global appsec" "talk"

# Community discussion
site:reddit.com/r/netsec "CVE"
site:reddit.com/r/bugbounty "methodology"
site:news.ycombinator.com "security"
"infosec.exchange" "research"

# Chinese-language sources
site:xz.aliyun.com "SSRF"
site:forum.butian.net "反序列化"
site:anquanke.com "CVE-2024-3400"
site:freebuf.com "漏洞"
site:bbs.kanxue.com "逆向"
site:secpulse.com "内网渗透"
site:secrss.com "政策"
site:sec-wiki.com "工具"
site:t00ls.com "红队"
site:gitee.com "security"

# Researchers
"researcher name" "CVE" "writeup"
"security researcher" "blog" "bug bounty"
"follow" "infosec" "list"
site:blog.orange.tw "SSRF"
site:samcurry.net "bug bounty"
site:payloads.online "内网"
site:leavesongs.com "反序列化"

# News and tracking
"security newsletter" "weekly"
"Detection Engineering Weekly" "detection engineering"
"threat intelligence" "weekly roundup"
"CISA" "advisory" "2025"
```

---

## Workflow

1. **Define the monitoring scope.** Topics, vendors, threat actors, bug classes, regions.
2. **Build a source list.** 10-20 high-signal sources; avoid duplication and low-quality
   aggregators.
3. **Use RSS/Atom and alerts.** Feedly/Inoreader, Google Alerts, GitHub watch, vendor RSS.
4. **Verify every claim.** Cross-check with the vendor advisory, primary research, or a second
   independent source.
5. **Extract structured notes.** Author, date, venue, claim, technique, IOCs, detection, links.
6. **Track researchers and labs**, not just articles.
7. **Review weekly.** Deduplicate, archive, and update the source list.
8. **Convert into action.** Add detections, test in labs, update threat models.

---

## What to extract

| Field | Example |
|---|---|
| Source | PortSwigger Research |
| Author/date | James Kettle, 2025-08 |
| Topic | HTTP request smuggling |
| Claim | new desync primitive |
| Evidence | paper + talk + lab |
| IOCs/detections | request patterns, rules |
| Confidence | B (research + independent corroboration) |
| Follow-ups | read paper, test in lab, update WAF |

---

## Pitfalls

- **Hype and marketing.** Vendor blogs may exaggerate impact.
- **Unverified claims.** Social posts are leads, not evidence.
- **Embargoes.** Respect conference and disclosure embargoes.
- **Paywalls.** Do not republish paywalled content.
- **Echo chambers.** Follow sources with different perspectives.
- **Alert fatigue.** Too many feeds reduce signal; curate aggressively.
- **Stale sources.** Check last update and relevance.

---

## Ethics

- Cite authors and link original sources.
- Respect embargoes, licenses, and paywalls.
- Do not amplify unverified IOCs or fear, uncertainty, and doubt.
- Protect sources and victims; avoid publishing PII.
- Correct errors publicly when you make them.

---

## Output contract

```
module:        M10 Community
objective:     track <topic> across credible sources
authorization: public sources
sources_used:  N sources with URL + date + author, mapped to the claim it supports
sources_read:  URLs opened but excluded, with reason (off-scope, stale, duplicate, low confidence, inaccessible, discovery only)
findings:      claims, techniques, IOCs, detections, confidence
pivots:        M2 writeups, M3 CVE, M5 red team, M12 report
caveats:       hype, unverified claims, embargoes
```
