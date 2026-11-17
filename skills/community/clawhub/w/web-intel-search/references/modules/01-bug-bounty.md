# M1 - Bug Bounty Programs, Scope & Disclosure

**Purpose:** Find bounty programs, verify scope and rules, understand rewards/triage, and locate
the correct disclosure channel before any research or testing.

**Triggers:** bug bounty, bounty program, HackerOne, Bugcrowd, Intigriti, YesWeHack, Immunefi,
Huntr, Open Bug Bounty, Synack, Cobalt, scope, in-scope, out-of-scope, VDP, reward, triage,
duplicate, disclosure policy, safe harbor, rules of engagement, private program, 补天, 漏洞盒子,
火线, SRC.

**Process contract:** Always run the Universal Search Loop (Section 1) and the Process Compliance
Gate (Section 0.5). This module supplies sources and queries only.

---

## Primary sources

### Platforms
| Platform | Focus | Program search |
|---|---|---|
| HackerOne | General, large programs | `hackerone.com/directory/programs` |
| Bugcrowd | General, managed programs | `bugcrowd.com/programs` |
| Intigriti | Europe-heavy | `intigriti.com/programs` |
| YesWeHack | Europe/Asia | `yeswehack.com/programs` |
| Immunefi | Web3 / smart contracts | `immunefi.com/bug-bounty/` |
| Huntr | AI/ML and open source | `huntr.com/bounties` |
| Open Bug Bounty | Coordinated VDP | `openbugbounty.org` |
| Synack | Vetted/private | `synack.com` |
| Cobalt | Pentest-as-a-service | `cobalt.io` |
| HackenProof | Web3 | `hackenproof.com` |
| Sherlock / Code4rena / Cantina | Audit contests | platform sites |
| 补天 (Butian) | China SRC and vulnerability platform | `butian.net` |
| 漏洞盒子 (Vulbox) | China crowdsourced security | `vulbox.com` |
| 火线 (Huoxian) | China security community and SRC | `huoxian.cn` |

Chinese SRCs may require real-name verification, local-law compliance, and program-specific
authorization. Follow the published scope; do not test without permission.

### Scope and policy sources
- The program page itself (scope, exclusions, reward table, SLA, safe harbor).
- `/.well-known/security.txt` and `/security.txt` on the target domain.
- `responsible disclosure`, `security policy`, `vulnerability disclosure policy` pages.
- **FireBounty** (`firebounty.com`) - aggregated VDP and bug-bounty policy index (176k+ entries,
  includes security.txt).
- `arkadiyt/bounty-targets-data` (GitHub) - machine-readable scopes for major platforms.
- Program changelog and hacktivity/crowdstream for prior disclosures.

---

## Query recipes

```text
# Find the program
site:hackerone.com "example.com"
site:bugcrowd.com "example.com"
site:intigriti.com "example.com"
site:yeswehack.com "example.com"
site:immunefi.com "example"
site:huntr.com "example"
site:firebounty.com "example.com"
site:butian.net "SRC"
site:vulbox.com "SRC"
site:huoxian.cn "SRC"

# Find disclosure policy / security contact
site:example.com "responsible disclosure"
site:example.com "vulnerability disclosure"
site:example.com "security.txt"
site:example.com inurl:security
site:example.com intext:"safe harbor"
"example.com" "bug bounty" -site:example.com
"example.com" "VDP" OR "vulnerability disclosure program"

# Find prior reports / duplicates
site:hackerone.com/hacktivity "example.com"
site:bugcrowd.com/crowdstream "example.com"
"example.com" "disclosed" "report"

# Scope aggregation
github.com/arkadiyt/bounty-targets-data
"example.com" "out of scope"
"example.com" "in scope" "wildcard"
```

---

## Workflow

1. **Identify the program owner.** Is it public, private/invite-only, a VDP, or a self-hosted
   policy? Record the canonical URL.
2. **Read scope precisely.** List in-scope domains, apps, APIs, mobile apps, IP ranges, and
   explicitly excluded assets. Note wildcard rules and third-party exclusions.
3. **Read the rules.** Test accounts, rate limits, prohibited techniques (DoS, social engineering,
   physical), data handling, disclosure timeline, safe harbor language.
4. **Check rewards and triage.** Reward range, severity mapping, first-response SLA, duplicate
   policy, out-of-scope bug classes (e.g., self-XSS, missing headers).
5. **Check prior disclosures.** Hacktivity/CrowdStream and public writeups to avoid duplicates.
6. **Verify program status.** Last updated, paused programs, ownership changes, acquired companies.
7. **Record the program brief** (see output contract) before moving to M2/M3/M4.

---

## What to extract

| Field | Example |
|---|---|
| Program | `Example Inc` on HackerOne |
| URL | `https://hackerone.com/example` |
| Type | Public bounty / VDP / private invite |
| In scope | `*.example.com`, `api.example.com`, iOS/Android apps |
| Out of scope | `status.example.com`, third-party SaaS, marketing sites |
| Rules | No DoS, no social engineering, test accounts required |
| Rewards | $500 - $10,000; Critical $10k |
| SLA | First response 2 business days |
| Disclosure | 90 days coordinated |
| Prior reports | 12 disclosed; check for IDOR/SSRF duplicates |
| Notes | Program paused on 2026-09-01 |

---

## Pitfalls

- Testing an asset that looks in scope but is owned by a third party.
- Assuming a wildcard covers acquired companies or cloud-hosted services.
- Ignoring program updates and exclusions added after the last writeup.
- Reporting duplicates already disclosed in Hacktivity.
- Violating safe harbor by using out-of-scope techniques.
- Confusing a VDP (no reward, legal protection) with a paid bounty.

---

## Ethics

- Only test assets explicitly in scope, with the program's rules as the authorization.
- Respect rate limits, privacy, and data-minimization requirements.
- Report privately through the program channel; never publish before the disclosure deadline.
- Stop and ask the program when scope is ambiguous.

---

## Output contract

```
module:        M1 Bug Bounty
objective:     identify program + scope + rules for <target>
authorization: program policy (public bounty/VDP)
sources_used:  program URL, security.txt, scope data, prior reports, mapped to the claim it supports
sources_read:  URLs opened but excluded, with reason (off-scope, stale, duplicate, low confidence, inaccessible, discovery only)
findings:      scope table, rules, rewards, SLA, exclusions, confidence
pivots:        M2 writeups, M3 CVEs, M4 cheatsheets, M9 labs
caveats:       scope changes, private assets, program status
```
