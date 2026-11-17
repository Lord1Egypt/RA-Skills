# M2 - Bug Bounty Writeups, Case Studies & Field Experience

**Purpose:** Find high-quality writeups, disclosed reports, case studies, and practitioner
experience for a vulnerability class, technology, or target. Extract reproducible methodology
and lessons - not just payloads.

**Triggers:** writeup, how I found, case study, bug story, kinh nghiệm săn bug, disclosure,
HackerOne Hacktivity, Bugcrowd CrowdStream, Medium, dev.to, InfoSec Write-ups, Pentester Land,
"bug bounty journey", "lessons learned", "methodology".

**Process contract:** Always run the Universal Search Loop (Section 1) and the Process Compliance
Gate (Section 0.5). This module supplies sources and queries only.

---

## Primary sources

### Disclosed report feeds
- **HackerOne Hacktivity** - `hackerone.com/hacktivity` (filter by program, severity, disclosure).
- **Bugcrowd CrowdStream** - `bugcrowd.com/crowdstream`.
- **Intigriti writeups/blog** - `intigriti.com/blog`.
- **YesWeHack blog** - `yeswehack.com/blog`.
- **Pentester Land** - `pentester.land/writeups` (curated list).
- **InfoSec Write-ups** - `infosecwriteups.com`.
- **GitHub writeup repos** - search `bug bounty writeups`, `ctf-writeups`, `hackerone-reports`.

### Practitioner blogs and channels
- **Bug bounty/web:** Orange Tsai (`blog.orange.tw`), Sam Curry (`samcurry.net`), James Kettle
  (`jameskettle.com`), EdOverflow (`edoverflow.com`), 0xdf (`0xdf.gitlab.io`).
- **Red team/AD:** harmj0y (`blog.harmj0y.net`), ADSecurity (`adsecurity.org`).
- **Chinese-language:** 倾旋 (`payloads.online`), 离别歌/phith0n (`leavesongs.com`), 素十八
  (`su18.org`), K0rz3n (`k0rz3n.com`), TeamsSix (`teamssix.com`), Nuclear'Atk (`lcx.cc`).
- Team blogs: PortSwigger Research, Project Zero, Assetnote, SpecterOps, TrustedSec, Bishop Fox,
  Zero Day Initiative, ProjectDiscovery, and vendor labs; M10 has the full list and caveats.
- YouTube: STÖK, NahamSec, InsiderPhD, Critical Thinking, IppSec, LiveOverflow, John Hammond.
- Conference talks (DEF CON, Black Hat, BSides, OWASP) with slides/recordings.
- Reddit `r/bugbounty`, `r/netsec`; X/Twitter and Mastodon threads.

### Aggregators and datasets
- `github.com/EdOverflow/bugbounty-cheatsheet` (methodology and resources).
- `github.com/devanshbatham/Awesome-Bugbounty-Writeups` (writeups grouped by bug class).
- `github.com/securitycipher/daily-bugbounty-writeups` (daily curated writeup feed).
- `github.com/arkadiyt/bounty-targets-data` (scope data; see M1).
- HackerOne disclosed report exports and public "top reports" lists.
- "Bug Bounty Reports Explained" style channels/newsletters.

---

## Query recipes

```text
# By vulnerability class
site:medium.com "bug bounty" "IDOR"
site:infosecwriteups.com "SSRF"
site:hackerone.com/hacktivity "IDOR"
"how I found" "IDOR" "bug bounty"
"SSRF" "writeup" "bounty"

# By technology / target
"Spring Boot" "Actuator" "bug bounty" writeup
"Next.js" "SSRF" "writeup"
"GraphQL" "IDOR" "bug bounty"
"example.com" writeup -site:example.com

# By report ID / CVE
"HackerOne report" "1234567"
"CVE-2024-3400" writeup
"disclosed" "report" "critical"

# Methodology and experience
"bug bounty methodology" 2025
"how to hunt" "IDOR" "recon"
"lessons learned" "bug bounty"
"my first bug bounty" "writeup"
"duplicate" "bug bounty" lessons
"triage" "bug bounty" experience

# GitHub collections
site:github.com "bug-bounty-writeups"
site:github.com "hackerone" "writeups"
site:github.com "pentest" "writeups" "CVE"
```

---

## Workflow

1. **Define the research question.** Bug class + technology + constraint (e.g., "IDOR in
   GraphQL APIs with UUIDs").
2. **Collect 5-10 writeups** from different authors and years. Prefer disclosed reports with
   enough detail and a clear root cause.
3. **Extract a structured card per writeup:** target type, vuln class, root cause, prerequisites,
   discovery path, payload concept, impact, fix, references.
4. **Compare across writeups.** Identify patterns, common preconditions, and what changed over time
   (framework fixes, WAF behavior, new features).
5. **Separate signal from luck.** Note whether the find depended on a specific feature, misconfig,
   or business logic.
6. **Map to your authorized target.** Check whether the preconditions exist; do not test without
   scope.
7. **Validate in a lab (M9)** before claiming reproducibility.
8. **Write a synthesis**, not a copy: patterns, decision tree, detection ideas, references.

---

## What to extract

| Field | Example |
|---|---|
| Writeup | "IDOR in GraphQL node interface" |
| Author / date | researcher, 2025-08 |
| Target type | SaaS B2B, GraphQL API |
| Root cause | missing object-level authorization on `node(id:)` |
| Prerequisites | authenticated user, predictable IDs, no tenant check |
| Discovery path | recon -> schema introspection -> query mutation |
| Impact | read other tenants' invoices |
| Fix | per-object authorization + tests |
| Confidence | B (multiple corroborating writeups) |
| Source | URL + archive link |

---

## Pitfalls

- **Survivorship bias:** published writeups over-represent successful, interesting bugs.
- **Outdated techniques:** framework patches and WAF changes invalidate old payloads.
- **Redacted details:** disclosed reports often hide the exact request/response.
- **Version/config mismatch:** the same code may be safe in a different deployment.
- **Hype and marketing:** "critical" claims may not match real impact.
- **Copy-paste risk:** running someone else's payload on an unauthorized target is illegal.

---

## Ethics

- Respect disclosure timelines and program rules.
- Do not name unresolved targets or expose user data.
- Redact tokens, PII, and internal hostnames.
- Cite the original author and link the source.
- Use writeups to learn and defend, not to attack out-of-scope systems.

---

## Output contract

```
module:        M2 Writeups
objective:     extract methodology for <bug class/tech>
authorization: public sources only / program scope if testing
sources_used:  N writeups with URL + date + author, mapped to the claim it supports
sources_read:  URLs opened but excluded, with reason (off-scope, stale, duplicate, low confidence, inaccessible, discovery only)
findings:      patterns, preconditions, payload concepts, impact, fixes
pivots:        M1 scope, M3 CVE, M4 cheatsheet, M9 lab
caveats:       outdated/redacted/lucky findings; confidence level
```
