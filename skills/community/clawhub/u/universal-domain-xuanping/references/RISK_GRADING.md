# Risk Grading Criteria (Universal Domain Risk & Xuan-Ping Review)

> RAG framework criteria. Evidence first, procedure first, red lines held - but no alarmism, always an actionable path.

## RAG definitions

| Rating | Meaning | Action |
|---|---|---|
| 🔴 Red | Legal red line / irreversible major loss | Escalate to the owner immediately; do not alter or conceal |
| 🟡 Amber | Risk mitigable, or evidence incomplete | List actionable paths for the business owner to decide |
| 🟢 Green | No major risk found | Issue after review |
| ⚪ Hint | Rule note, NOT a risk rating | Owner verifies; black box makes no substantive conclusion |

## Per-dimension criteria

1. **Domain resolution**: A record exists and redirects are proper -> green; cannot obtain -> amber.
2. **TLS certificate**: >14 days remaining, proper CA, SAN covers the base -> green; <=14 days or read failure -> amber.
3. **HTTP security headers**: HSTS / CSP / X-Content-Type-Options all present -> green; core missing -> amber. x-frame-options / x-xss-protection are bonus items.
4. **Subdomain exposure**: no 404/530/unreachable external references -> green; dangling references or anomalous subdomains -> amber (ledger to clean).
5. **Sensitive content**: no private-key / password leak -> green; suspected leak -> red (verify now). Public emails are logged only, NOT red.
6. **Compliance (filing/privacy/Cookie/HTTPS)**: page-only read-only evidence + rule hint, no legal opinion, no inference of server location or filing obligation; judge region first (U4) so an absent filing number is NOT a risk. Permanent ⚪ hint, excluded from RAG scoring.
7. **Registration age**: state the fact (date + years) only; no risk rating.
8. **Market value / traffic**: data unavailable, amber "pending", **never a fake figure**.

## Filing (ICP) notes

- The ICP filing obligation is triggered by the **server being physically in mainland China**; an overseas server needs no MIIT ICP filing. The `.cn` suffix does not change this rule.
- **Judge region first (U4)**: a `hosting` suspected-region hint comes from CDN ranges ("suspected" only, NOT proof of origin). Overseas / suspected overseas CDN edge -> usually no obligation -> an absent filing number is **normal, not a risk, no urging**; mainland -> owner verifies; region unknown -> neutral self-check. **Never flag amber or urge just because a page has no filing number.**
- Beware **misattribution** when looking up a filing number: a lookup site may display its own, not the target's. If not found, mark "not found / needs manual check", never guess the number.
- Exceptions: moving the server back to the mainland or using a CDN with mainland nodes re-triggers the obligation; news / medical / finance / education qualifications are not waived by overseas hosting.

## Change-the-ledger-not-the-history

- Conclusion updates are appended as "Update U1/U2..."; the original is kept, never overwritten.
- When the current run differs from history (headers added, certificate renewed), this run is authoritative; annotate the difference, never force alignment to old values.

## Divination boundary

- The Xuan-Ping (I-Ching) hexagram is a deterministic hash-mapped Easter egg, pure entertainment.
- Not in the conclusion table, not in the formal assessment, not a decision basis.
- Listed separately at the end of the report with a fixed disclaimer.

---

## Update U2 | Universalization refactor (2026-11-22, v1.1)

> Trigger: a universality review noted "after publishing, this skill must produce conclusions for EVERY domain, not just one site".
> v1.0 passed regression tests but the report layer hard-coded several site-specific facts; reconstructed after a 4-domain matrix test.
> **This section overrides the criteria above; the original is kept per "change the ledger, not the history".**

### U2.1 Withdrawn old conclusions (v1.0 defects, fixed)

| Old criterion / implementation | Problem | v1.1 handling |
|---|---|---|
| Item 6 "overseas hosting -> no ICP obligation -> green" | Asserted a specific site's "overseas hosting / no obligation" with no geography probe, emitted for every domain = **fabrication** | Compliance is now a permanent ⚪ hint: rules only, **no decision** on any site's filing obligation |
| Item 5 "no email leak -> green / leak -> red" | A public homepage email is a common contact; flagging it red = false positive | Emails **logged only, not red**; private-key header -> red; password/key words -> amber "suspected, pending" |
| Item 7 "registration age not rated" | No status when whois unavailable, easily misread as verified | Missing -> amber "pending, verify in registrar panel" |
| "Irreversible risk: DNS/TLS/resolution all normal" hard-coded | Claimed normal while all evidence failed = **self-contradiction** | Generated from `evidence` actual state; incomplete -> "cannot rule out irreversible risk" |
| "Certificate auto-renewed by CDN" hard-coded | Inference for non-CDN sites | Conditional hint only when `cdn_hint` hits |
| Red-flag count `s[0]=='red'` (unpack error) | **Red flags never counted** | Fixed to count by rating state |

### U2.2 New: failed-evidence degradation (highest priority)

- Any dimension with failed evidence -> degrade to "pending / undetermined", never an affirmative "normal / none found / no risk / no obligation".
- If the summary has incomplete evidence items, it must **first state "this report does not constitute a complete conclusion"**; never gloss over as all-green.
- Subdomains are a finite enumeration: not listed != absent; whois is a third-party API: not found != no record.

### U2.3 New: CDN / geography only as "suspected" hints

- CDN attribution is **data-driven** from A records vs public IP ranges, worded fixed as "**suspected** CDN edge, NOT proof of origin location".
- Hitting a CDN range does **not** infer the server's physical location; no hit does **not** conclude "not CDN".
- Edge / resolved IPs cannot confirm origin location -> filing obligation always left to "owner verifies hosting panel"; black box does not decide.

### U2.4 Universality contract (6 hard constraints)

1. Conclusion text contains no domain-specific facts (concrete IPs, CDN names, geography; suffix written as `.{tld}` variable).
2. All facts come from `scan.json`; the report layer is pure rendering, zero built-in conclusions.
3. Failed evidence degrades (see U2.2).
4. CDN / geography only as suspected hints (see U2.3).
5. Finite enumeration != exhaustive; third-party API != authoritative ledger.
6. New ⚪ hint marker: compliance is a permanent hint, excluded from RAG risk scoring.

### U2.5 Regression matrix (must pass before publishing)

| Type | Sample | Check |
|---|---|---|
| `.cn` + CDN edge | a CDN-fronted site | CDN hint driven by IP ranges; registration age normal |
| `.com` non-CDN | example.com | No hard-coded Cloudflare/overseas wording; `Creation Date` / Unix timestamp parses |
| Large domestic portal | a major portal | No invented "no ICP obligation"; many subdomains, no false positives |
| Non-existent domain | a random .cn | All dimensions degrade to "pending", summary states incomplete, no "all normal" |

> All four pass: no banned hard-coded strings, compliance sections all contain "no decision", hexagram determinism verified.
> Also fixed whois integer-timestamp parsing (`api.whois.vu` returns Unix seconds for gTLDs; v1.0 threw `AttributeError` and falsely degraded).


## Update U3 | Compliance-publicity read-only evidence (2026-11-23, v1.2)

- The compliance dimension upgraded from pure rule-hint to "read-only page evidence + rule hint": added ICP / public-security filing-number regex, privacy-policy / terms / disclaimer keyword groups, Set-Cookie, and HTTP->HTTPS enforcement checks.
- All are **permanent ⚪ hints, excluded from RAG scoring**; only page "present / absent" facts are reported; absence != violation / no filing obligation; no legal opinion.
- The HTTP->HTTPS probe must check the **actual service host** (final_url netloc), never the input bare domain (a bare domain may redirect to https while the www host does not -- opposite conclusions).
- Supersedes the old item 6 wording "overseas hosting -> no ICP obligation -> green" for rating purposes; original text kept per "change the ledger, not the history".

## Update U4 | Region-first ICP correction (2026-11-23, v1.2.1)

- Trigger: "ICP must be judged by whether the server is domestic or overseas; never flag amber just because ICP is absent."
- Added a `hosting` suspected-region hint (from matched CDN ranges, always "suspected", NOT proof of origin). Judgment order: **region first, then number**.
- Overseas / suspected overseas CDN edge -> usually no ICP obligation -> an absent page number is normal, **not a risk, not urged, no action item**; mainland -> owner verifies; region unknown -> neutral self-check.
- Removed the unconditional "no page filing number -> please verify whether filed" urging row; a missing number alone is never an amber rating or an actionable item.
- Original text of earlier items kept per "change the ledger, not the history".
