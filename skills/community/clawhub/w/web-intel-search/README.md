# web-intel-search

A router-driven web intelligence and security research skill for OpenClaw, Claude Code, Codex,
Cursor, and other Agent Skills-compatible agents. It finds information, selects the right domain
module, and enforces a strict search + verification process.

**Not an attack tool.** It is a search and research playbook for authorized security work,
defensive research, bug bounty, appsec, architecture, learning, and journalism.

## What it does

- Routes a request to 1 primary + 0-2 secondary modules based on keywords and intent.
- Always runs the Universal Search Loop: Frame -> Plan -> Expand -> Collect -> Verify -> Report.
- Enforces a Process Compliance Gate before answering: scope, sources, queries, confidence,
  contradictions, and redaction.
- Ends every answer with a Source Ledger: links used for synthesis plus links read but not used,
  each with a reason for exclusion.
- Ships 12 domain packs and 6 core reference files.

## Modules

| # | Module | Use when the user asks about |
|---|---|---|
| M1 | Bug Bounty | Programs, scope, platforms, VDP, rewards, triage, disclosure |
| M2 | Writeups & Experience | Bug stories, case studies, "how I found", lessons learned |
| M3 | CVE & PoC | CVE records, affected versions, PoCs, exploits, patch diffs, KEV/EPSS |
| M4 | Cheatsheets & Payloads | Payloads, wordlists, commands, bypasses, privesc references |
| M5 | Red Team | ATT&CK, adversary emulation, C2 docs, OPSEC, purple team |
| M6 | AppSec & Secure Code | SAST/DAST/SCA, code review, secure SDLC, threat modeling, LLM/GenAI |
| M7 | Security Architecture | Zero trust, cloud security, reference architectures, controls |
| M8 | Debugging & Reproduction | Stack traces, crashes, root cause, fuzzing, lab reproduction |
| M9 | Labs, CTF & Training | PortSwigger, HTB, TryHackMe, VulnHub, certifications |
| M10 | Community & Research | Blogs, conferences, researchers, newsletters, social |
| M11 | Vendor Advisories | PSIRT bulletins, patches, changelogs, fixed versions |
| M12 | Methodology & Reporting | PTES, OWASP WSTG, scoping, RoE, reports, retests |

## Core references

- `references/engines.md` - operator cheat sheets and API endpoints.
- `references/dorks.md` - categorized Google/GitHub/Shodan/cloud/paste dorks.
- `references/secrets.md` - secret regex catalog and safe validation notes.
- `references/tooling.md` - CLI, APIs, automation, and safety checklist.
- `references/quick-recipes.md` - copy-paste query recipes and safety notes.
- `references/osint-targets.md` - target-specific OSINT source packs and meta-hubs.

## Install

### OpenClaw / ClawHub

```bash
# from ClawHub after publishing
openclaw skills install @<owner>/web-intel-search

# or copy a local checkout into your OpenClaw skills directory
cp -r web-intel-search ~/.openclaw/skills/
```

### Claude Code

```bash
cp -r web-intel-search ~/.claude/skills/
```

### opencode

```bash
mkdir -p ~/.config/opencode/skill
cp -r web-intel-search ~/.config/opencode/skill/
```

### Other agents

Copy the folder into your agent's skills directory. The entry point is `SKILL.md`; supporting
files are resolved relative to the skill directory.

## Publish to ClawHub

```bash
npm i -g clawhub
clawhub login
clawhub skill publish ./web-intel-search --dry-run
clawhub skill publish ./web-intel-search \
  --slug web-intel-search \
  --name "Web Intel Search" \
  --version 1.9.0 \
  --tags "security,osint,search,bug-bounty,red-team,appsec,architecture" \
  --changelog "v1.9.0: individual researcher blogs for pentest, red team, and bug bounty across global and Chinese-language sources, plus active team blogs"
```

Before publishing, review the skill and its files. ClawHub runs automated security scans; keep
the content defensive and free of secrets.

## Usage examples

```text
"Tìm writeup bug bounty IDOR trên HackerOne"           -> M2 (+M1)
"CVE-2024-3400 có PoC chưa, affected versions nào?"   -> M3 (+M11)
"Cheatsheet leo thang đặc quyền Linux"                 -> M4 (+M9)
"Thiết kế zero trust cho AWS"                          -> M7 (+M6)
"Debug crash trong binary CTF"                         -> M8 (+M9)
"Red team technique cho initial access"                -> M5 (+M10)
"So sánh OWASP ASVS và NIST 800-53"                    -> M6 + M7 + M12
```

Every response should state the module used, the queries run, the sources (URL + date), the
confidence grade, and the caveats. It must also include two source lists: links used for synthesis
and links read but not used (with the exclusion reason).

## Output contract

```text
module:          M# <name>
objective:       one sentence
authorization:   authorized / lab / public-only / unknown
queries:         exact queries and dorks used
sources_used:    URL + title + date + claim supported
sources_read:    URL + title + date + reason read but not used
findings:        claim + evidence + confidence (A-D)
pivots:          next identifiers or sources to check
caveats:         gaps, contradictions, stale/unsupported claims
```

If no source was read but excluded, write `None` explicitly. Discovery-only pages belong under
`sources_read` with reason `discovery only`; do not hide them.

## Process guarantee

The skill does not allow a module to bypass the process. The router selects sources and recipes;
the Universal Search Loop and the Process Compliance Gate remain mandatory. The gate fails if the
Source Ledger omits either used sources or read-but-not-used sources. This keeps results
reproducible and prevents "search and dump" answers.

## Safety

- Authorized testing, labs, and public-source research only.
- No credential use, no destructive actions, no exploit execution against third parties.
- Redact secrets and PII; respect disclosure timelines and terms of service.
- Verify third-party skills and tools before installing them.

## License

MIT-0 (ClawHub default). See `LICENSE`.
