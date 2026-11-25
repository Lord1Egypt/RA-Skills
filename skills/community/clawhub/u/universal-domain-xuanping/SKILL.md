---
name: universal-domain-xuanping
slug: universal-domain-xuanping
version: 1.2.3
displayName: Universal Domain Risk & Xuan-Ping Review
summary: Enter any domain, get an 8-dimension red/amber/green read-only risk report with compliance-publicity evidence and region-first ICP judgment, plus a deterministic I-Ching hexagram "Xuan-Ping" Easter egg
description: |-
  Universal read-only risk assessment for any domain / web asset (8 dimensions, red/amber/green) with a deterministic I-Ching "Xuan-Ping" divination Easter egg. Enter any domain; a pure external black-box scan covers DNS / TLS / HTTP security headers / subdomains / sensitive content / whois registration age / compliance-publicity evidence (filing numbers, privacy/terms/disclaimer keywords, Set-Cookie, HTTP-to-HTTPS enforcement) and a suspected hosting-region hint, producing a structured report. Includes registration age, explicit data-credibility notes for market value and traffic, and a 64-hexagram reading (pure entertainment, never part of the conclusions).
  Works for EVERY domain: all conclusions are driven by collected evidence; if evidence collection fails, the dimension degrades to "pending verification". It never fabricates facts, never infers server geography or filing (ICP) obligations. On ICP: judge server region first -- overseas hosting usually has no ICP obligation and an absent filing number is normal (not a risk, no urging); never flag amber just because a number is missing. Trigger when a user says "scan/assess this domain", "domain risk review", "check this site's security", "check webpage compliance", "how old is this domain", "cast a hexagram for this domain", or "universal domain risk & xuan-ping review".
  Read-only: no panel login, no credentials, no configuration changes. Risk hints only, no legal opinion. Missing data is stated as missing, never invented.
tags: [domain, security, risk-assessment, dns, tls, whois, compliance, i-ching]
license: MIT
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Universal Domain Risk & Xuan-Ping Review

> A read-only, evidence-driven risk assessment for **any domain**. 8 red/amber/green dimensions, all computed from live evidence, plus a deterministic "Xuan-Ping" (I-Ching hexagram) Easter egg at the end. Evidence first, procedure first, red lines held — but no alarmism, always an actionable path.

## When to use

- "Scan / assess this domain", "give this domain a risk review", "check this site's security"
- "How old is this domain", "are its security headers complete", "any exposed subdomains"
- "Check this webpage's compliance / filing disclosure" (compliance-publicity evidence, read-only)
- "Cast a hexagram for this domain" (divination alone is also supported, as an Easter egg)

## Three iron rules (non-negotiable)

1. **Read-only evidence**: pure external black box; no panel login, no credentials, no configuration changes. If data can't be collected, mark it "needs manual check / pending" — never fabricate.
2. **Hints, not legal opinions**: compliance items (ICP filing / privacy) give **rules only**; any determination belongs to regulators / licensed counsel. Never infer the server's physical location, never decide whether a specific site "has / has no filing obligation". **Judge region first**: overseas hosting usually has no ICP obligation, so an absent filing number is normal -- never a risk, never urged.
3. **Never fill in absent data**: no authoritative source for market value → "no figure given"; traffic cannot be measured externally → "pending owner-supplied data", never a fabricated 0 or estimate. **The hexagram is an Easter egg, never part of the conclusions, never a decision basis.**

## Universality contract (core of v1.1, extended in v1.2)

> This skill faces **every domain**, not one particular site. "Regression tests passed" ≠ "universal". Six hard constraints:

| # | Constraint | Counterexample (v1.0 bug, fixed) |
|---|---|---|
| 1 | Conclusion text must contain **no domain-specific facts** (concrete IPs, CDN names, server geography, suffix) | ~~"A record is a Cloudflare overseas edge IP, server overseas → no ICP obligation"~~ emitted for every domain = fabrication |
| 2 | **Failed evidence degrades** to "pending / undetermined", never "normal / none found / no obligation" | ~~"Irreversible risk: DNS/TLS/resolution all normal"~~ while all failed = self-contradiction |
| 3 | CDN / geography only as **data-driven "suspected"** hints (from public IP ranges), never assert origin location | Edge IP ≠ origin; hitting a CDN range yields no hosting conclusion |
| 4 | All facts come from `scan.json`; the report layer is pure rendering, no built-in conclusions | Every conclusion computed from JSON |
| 5 | **Finite enumeration ≠ exhaustive**: unlisted subdomains must say "does not imply absence"; whois is a third-party API, the registrar panel is authoritative | Never treat "not found" as "no asset / no record" |
| 6 | An email is a common contact channel, **not a leak**; only a private-key header is red; password/key words are "suspected, pending" | Flagging a public homepage email as red = false positive |
| 7 | (v1.2) Compliance-publicity reports page "present / absent" facts only; **absence != violation / no filing obligation** | Asserting "no number on page -> obligation / violation" from a black box |
| 8 | (v1.2.1/U4) **Judge ICP by server region first**: overseas / suspected overseas CDN edge -> no obligation -> **absent number is normal, not a risk, no urging**; mainland -> owner verifies; unknown -> neutral self-check. **Never flag amber / urge just because a number is missing** | ~~"No ICP number on page -> please verify whether filed" (unconditional urging)~~ urges regardless of server region = false-alarm pressure |

**A 4th marker ⚪ Hint**: the compliance dimension is permanently a ⚪ "rule hint, owner to verify" item, excluded from red/amber/green risk scoring — avoiding any substantive compliance conclusion from a black box.

## Standard workflow (3 steps)

```bash
SK=./scripts

# 1. Read-only evidence scan (DNS/TLS/HTTP headers/subdomains/content/whois/compliance-publicity; output includes evidence flags + hosting hint)
python3 $SK/scan_domain.py <domain> > /tmp/scan.json

# 2. Xuan-Ping divination (Easter egg, deterministic)
python3 $SK/divination.py <domain> > /tmp/div.json

# 3. Generate the 8-dimension report (RAG + degradation + hexagram Easter egg)
python3 $SK/gen_report.py /tmp/scan.json /tmp/div.json ./<domain>_risk_report.md
```

Then present the report, briefly summarizing the RAG conclusion and the one hexagram. **If any evidence item is incomplete, you must explicitly state "this report does not constitute a complete conclusion"** — never gloss it over as all-green / normal.

## The 8 dimensions

| # | Dimension | Data source | Rating (with degradation) |
|---|---|---|---|
| 1 | Domain & resolution | socket A/AAAA + redirect | Normal green; failed → amber pending |
| 2 | TLS certificate | ssl subject/SAN/days left | >14 days green, nearing expiry amber; no 443 → amber "undetermined" |
| 3 | HTTP security headers | requests response headers | Core present green; core missing amber; failed → amber |
| 4 | Subdomain exposure | generic common-name enumeration + HTTP probe | No 404/530 green; base fails → "untested" amber |
| 5 | Sensitive content | homepage scan for private keys/passwords/emails/links | Private-key header red; password words amber pending; emails logged only |
| 6 | Compliance (filing/privacy/Cookie/HTTPS) | **page-only evidence + rules, no inference** | ⚪ permanent hint; reports present/absent facts; absence != obligation/violation, excluded from RAG |
| 7 | Registration age | whois structured fields first + multi-format fallback | If found, show years; else → amber pending |
| 8 | Market value / traffic | no authoritative external source | amber pending, no figures |

> **Compliance note (U4 region-first)**: An ICP filing obligation is triggered by the **server being physically in mainland China**; the domain suffix does not change that rule. Edge / resolved IPs cannot prove the origin's physical location, so this skill uses a `hosting` **suspected-region hint** from CDN ranges ("suspected" only, NOT proof of origin). **Judgment order: determine region first, then check for a number -- overseas / suspected overseas CDN edge usually has no ICP obligation, so an absent number is normal, NOT a risk, no urging, no action item; mainland -> owner verifies; region unknown -> neutral self-check. Never flag amber or urge just because the page has no filing number.** When looking up a number, beware **misattribution** (a lookup site may display its own filing number, not the target's); if not found, mark "not found / needs manual check" and **never guess the number**. Exceptions: moving back to the mainland or using a CDN with mainland nodes re-triggers the obligation; special-industry qualifications are not waived by overseas hosting.

## Xuan-Ping divination (Easter egg)

- **Method**: normalize the domain (strip www / lowercase) → SHA256 → King Wen 64-hexagram order + moving line. Deterministic, same domain → same hexagram, non-random, works for any domain.
- **Output**: hexagram number + name + hexagram text + moving line + a one-line playful reading.
- **Boundary**: pure entertainment, listed separately at the end of the report; **not in the conclusion table, not in the formal assessment, not a decision basis**. A fixed disclaimer is embedded in the script.

## Data sources & degradation

| Data | Primary | On failure |
|---|---|---|
| A/AAAA | python socket | `ok=false`, mark "resolution evidence failed", never fabricate |
| CDN attribution | public IP-range comparison ("suspected" only) | No hit → blank, **never conclude "not CDN"** |
| Compliance-publicity | homepage read-only regex + keywords + response headers | Page not retrieved → all items 'not evidenced', no inference |
| Hosting region (U4) | matched CDN range → "suspected" region hint | No hit / unregistered → "Unknown", no geography inference |
| TLS | python ssl | `ok=false`, mark "certificate not obtained / undetermined" |
| Security headers | requests | `ok=false`, mark "evidence failed" |
| Subdomains | generic common-name enumeration | Unresolvable ones skipped, never "does not exist" |
| whois | api.whois.vu: structured fields + multi-format fallback (incl. Unix timestamps) | `ok=false`, mark "verify in registrar panel" |
| Market value | no authoritative source | no figure, suggest third-party self-check |
| Traffic | no external source | mark "owner to supply from panel" |

## Regression matrix (universality baseline)

> One passing case does not prove universality. Before publishing, cover at least these types and check "no fabricated facts / no self-contradiction / failed evidence correctly degrades":

| Type | Sample | Focus |
|---|---|---|
| `.cn` + CDN edge | a CDN-fronted site | CDN hint driven by IP ranges, not hard-coded; registration age normal |
| `.com` non-CDN | example.com | No hard-coded "Cloudflare/overseas" wording; whois `Creation Date` parses |
| Large domestic portal | a major portal | No invented "no ICP obligation"; many subdomains, no false positives |
| Non-existent domain | a random non-existent .cn | All dimensions degrade to "pending", summary states the conclusion is incomplete, no "all normal" |
| Overseas CDN / no ICP number | a CDN-fronted domain with no filing number | Compliance text must say "overseas hosting usually has no ICP obligation, absent number is normal, not a risk, no urging"; **actionable paths must NOT contain 'verify whether filed / urging'** |

Each domain's hexagram must be deterministic and identical across runs. Site state changes over time (headers / certificate days) — the current run is authoritative; annotate differences, never force alignment to historical values.

## Files

- `scripts/scan_domain.py`: read-only evidence scanner (generic; output includes `evidence` / `cdn_hint` / `hosting` (U4 region hint) / `compliance` / `http_https`)
- `scripts/divination.py`: Xuan-Ping divination (generic, deterministic)
- `scripts/gen_report.py`: 8-dimension RAG report generator (pure data-driven, zero hard-coded conclusions)
- `references/RISK_GRADING.md`: RAG rating criteria and universality contract

## Boundaries & discipline

- Pure external black-box read-only evidence; no panel login, no credentials, no configuration changes.
- Failed evidence always degrades to "pending / undetermined", never filled with "normal / no risk / no obligation".
- Compliance section is page-publicity evidence plus a rule hint, not a legal opinion; never infer server physical location or filing obligations; "not detected on page" != "violation / no obligation".
- No market-value figure, no fabricated traffic; the hexagram is an Easter egg, not part of the conclusions, not a decision basis.
