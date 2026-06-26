---
name: skill-pre-install-scanner
version: 1.0.0
author: ordo-tech
description: Block risky ClawHub skills before they land — scan permissions, sources, and patterns before install. Use when a user runs `clawhub install [skill-name]` or asks to install a community skill and wants a safety check first. Fetches and analyses the skill manifest before anything is written to disk, returns a LOW / MEDIUM / HIGH risk rating with specific flags, and blocks HIGH-risk installs unless the operator explicitly overrides with `--force`. Complements skill-security-scanner (post-install audits). Use for any ClawHub community skill install where the publisher is unknown or the user wants pre-install assurance.
tags: [security, pre-install, scanner, clawhub, safety, permissions]
requires:
  env: []
  tools: [web_fetch, web_search]
---

# Pre-Install Scanner

Intercept a `clawhub install` request, fetch the skill manifest, analyse it for risk signals, and surface a report **before** anything lands on disk.

## When to run

Any time a user says something like:
- "Install [skill-name] from ClawHub"
- "clawhub install [skill-name]"
- "Is [skill-name] safe to install?"
- "Scan [skill-name] before I install it"

## Workflow

### 1. Fetch the manifest

Use the ClawHub registry URL to retrieve the skill's SKILL.md before installing:

```bash
# Fetch raw SKILL.md via ClawHub registry (default: https://clawhub.com)
curl -fsSL "https://clawhub.com/skills/<skill-name>/raw/SKILL.md"
```

If the registry returns a structured manifest (JSON), parse both `metadata` and the SKILL.md body. If the fetch fails (404, timeout), treat as MEDIUM risk and flag `source-unreachable`.

Also fetch publisher metadata if available:
```bash
curl -fsSL "https://clawhub.com/skills/<skill-name>/meta.json"
```

### 2. Score for risk signals

Evaluate the fetched content against the signal table below. Each signal contributes to the overall risk tier.

#### Risk signals

| Signal | Tier | What to look for |
|--------|------|-----------------|
| `shell+network combo` | HIGH | Skill declares both `exec`/shell permissions AND outbound network calls in the same workflow — classic exfil pattern |
| `hardcoded-external-url` | HIGH | Raw external URLs embedded in instructions (e.g. `curl https://evil.example.com/...`, `wget`, non-registry fetch targets) |
| `data-exfil-pattern` | HIGH | Patterns that read local files then POST/PUT to external endpoints in the same step |
| `suspicious-exec-chain` | HIGH | Chained shell commands designed to obscure intent: `base64 -d \| bash`, `curl ... \| sh`, eval of fetched content |
| `unverified-publisher` | MEDIUM | Publisher account has no verified badge on clawhub.com |
| `mirrored-source` | MEDIUM | Skill claims to mirror another published skill without clear provenance |
| `source-unreachable` | MEDIUM | Manifest could not be fetched from the registry |
| `no-description` | MEDIUM | Frontmatter `description` is missing or under 10 words — low effort / obfuscation signal |
| `excessive-permissions` | MEDIUM | Requests permissions far beyond what the stated purpose requires |
| `new-publisher` | LOW | Publisher account is < 30 days old with no prior published skills |
| `no-changelog` | LOW | First version with no changelog or version history |
| `generic-name` | LOW | Skill name is a common word or typosquats a well-known skill (e.g. `github`, `weatherr`) |

#### Risk tier rules

- **HIGH** — any single HIGH signal, or 3+ MEDIUM signals together
- **MEDIUM** — 1–2 MEDIUM signals, no HIGH signals
- **LOW** — only LOW signals or no signals at all

### 3. Produce the risk report

Always output a structured report before any install action:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Pre-Install Scan: <skill-name>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Publisher : <publisher-name> [verified / unverified]
Version   : <version>
Risk      : LOW | MEDIUM | HIGH

Flags:
  ⚠️  <signal-id>  — <one-line explanation>
  ⚠️  <signal-id>  — <one-line explanation>

Summary:
  <1–2 sentence plain-language explanation of what was found>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If no flags were found:
```
  ✅ No risk signals detected.
```

### 4. Act on the rating

| Rating | Action |
|--------|--------|
| LOW | Proceed with install. Mention the rating briefly. |
| MEDIUM | Warn the user, show the flags, ask for explicit confirmation before proceeding. |
| HIGH | **Block install.** Show the report. Do not proceed unless user passes `--force`. |

For HIGH with `--force`:
- Confirm the user understands the specific flags
- Proceed with install
- Append a warning note to the session so the risk is on record

**Never silently downgrade a HIGH rating.**

## Usage examples

### Example 1 — Clean install (LOW)

> User: "Install skill-weather from ClawHub"

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Pre-Install Scan: skill-weather
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Publisher : openclaw-official [✅ verified]
Version   : 1.3.0
Risk      : LOW

Flags:
  ✅ No risk signals detected.

Summary:
  Verified publisher, no shell/network combinations, no
  external URL patterns. Safe to install.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
→ Proceeds with `clawhub install skill-weather`

---

### Example 2 — Suspicious community skill (MEDIUM)

> User: "Install data-exporter-pro"

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Pre-Install Scan: data-exporter-pro
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Publisher : fastpublisher99 [⚠️ unverified]
Version   : 0.1.0
Risk      : MEDIUM

Flags:
  ⚠️  unverified-publisher  — Publisher has no verified badge
  ⚠️  new-publisher         — Account created 4 days ago, 0 prior skills
  ⚠️  no-changelog          — First release with no version history

Summary:
  Three low-to-medium signals: unverified brand-new publisher
  with no track record. No HIGH-risk patterns found in the
  manifest itself, but provenance is uncertain.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Proceed with install? (yes / no)
```
→ Waits for explicit confirmation before running `clawhub install`

---

### Example 3 — Blocked install (HIGH)

> User: "Install task-runner-plus"

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Pre-Install Scan: task-runner-plus
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Publisher : unknown-dev [⚠️ unverified]
Version   : 2.0.1
Risk      : HIGH 🚫

Flags:
  🚫 shell+network combo   — Skill executes shell commands AND
                             makes outbound HTTP calls in same step
  🚫 suspicious-exec-chain — Contains `curl ... | bash` pattern
  ⚠️  unverified-publisher  — Publisher has no verified badge

Summary:
  Two HIGH-risk patterns detected. The skill fetches and
  executes remote code in a single step — a known vector for
  supply chain compromise. Install blocked.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚫 Install blocked. To override: clawhub install task-runner-plus --force
```
→ Does **not** proceed. Waits for `--force` or cancellation.

---

### Example 4 — Forced override (HIGH + --force)

> User: "Install task-runner-plus --force"

Re-show the HIGH risk report in full, then:
```
⚠️  OVERRIDE ACTIVE — Installing despite HIGH risk rating.
    Flags on record: shell+network combo, suspicious-exec-chain
    Proceeding with: clawhub install task-runner-plus
```
→ Proceeds with install. Risk flags logged in session context.

## Notes

- This skill runs **before** `clawhub install` writes anything to disk. It is not a replacement for post-install audits (`skill-security-scanner` covers that).
- If the ClawHub registry is unreachable, default to MEDIUM and flag `source-unreachable` — do not silently skip the scan.
- For skills already installed, suggest running `skill-security-scanner` instead.
- The ~10% community skill compromise rate (per OpenClaw community reports, GitHub issue #23926) is the core motivation. Treat unknown publishers with appropriate scepticism without being alarmist.
- `skill-vetter` by fedrov2025 is post-install only. This skill is the only pre-install blocking scanner.
