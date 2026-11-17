# M4 - Cheatsheets, Payloads & Quick References

**Purpose:** Locate authoritative cheatsheets, payload libraries, wordlists, command references,
and bypass techniques for a given platform or vulnerability class. Verify against official docs and
test only in authorized labs.

**Triggers:** cheatsheet, cheat sheet, payload, wordlist, bypass, WAF bypass, one-liner, command,
exploitation, privilege escalation, reverse shell, SQL injection payload, XSS payload, SSTI,
LFI, SSRF, Active Directory, Linux privesc, Windows privesc.

**Process contract:** Always run the Universal Search Loop (Section 1) and the Process Compliance
Gate (Section 0.5). This module supplies sources and queries only.

---

## Primary sources

### Canonical libraries
| Source | Coverage |
|---|---|
| **PayloadsAllTheThings** (`github.com/swisskyrepo/PayloadsAllTheThings`) | Web, injection, bypass, privesc |
| **HackTricks** (`book.hacktricks.xyz`) | Pentest techniques, cloud, AD, OS |
| **HackTricks Cloud** | AWS/Azure/GCP/K8s |
| **Internal All The Things** (`github.com/swisskyrepo/InternalAllTheThings`) | Internal/AD |
| **OWASP Cheat Sheet Series** (`cheatsheetseries.owasp.org`) | Defensive secure coding |
| **OWASP WSTG** | Test cases and methodology |
| **PortSwigger Web Security Academy** | Labs + technique explanations |
| **GTFOBins** (`gtfobins.github.io`) | Linux binary abuse |
| **LOLBAS** (`lolbas-project.github.io`) | Windows binary abuse |
| **WADComs** (`wadcoms.github.io`) | AD command reference |
| **RevShells** (`revshells.com`) | Reverse shell generator |
| **SecLists** (`github.com/danielmiessler/SecLists`) | Wordlists |
| **Nuclei templates** | Detection/exploitation templates |
| **MITRE ATT&CK** | Technique mapping |

### Official documentation (verify before trusting a cheatsheet)
- Vendor docs for the exact product/version.
- Language/framework security docs (Django, Rails, Spring, Express, etc.).
- Database docs for SQL syntax and functions.
- Cloud provider docs for IAM and metadata behavior.
- Man pages and `--help` for CLI tools.

---

## Query recipes

```text
# Canonical cheatsheets
site:github.com/swisskyrepo/PayloadsAllTheThings "SSRF"
site:book.hacktricks.xyz "privilege escalation" linux
site:cheatsheetseries.owasp.org "SQL injection"
site:gtfobins.github.io "sudo"
site:lolbas-project.github.io "certutil"
site:wadcoms.github.io "kerberoasting"

# Technique-specific
"cheatsheet" "Active Directory" "Kerberoasting"
"payload" "SSTI" "Jinja2"
"WAF bypass" "SQL injection" cheatsheet
"reverse shell" "one-liner" cheatsheet
"Linux privilege escalation" checklist
"Windows privilege escalation" checklist
"GraphQL" "introspection" cheatsheet
"JWT" "none algorithm" payload

# Wordlists
site:github.com/danielmiessler/SecLists "raft"
"wordlist" "directory" "API"
"payload list" "XSS" github

# Verify against official docs
site:docs.djangoproject.com "security"
site:docs.spring.io "security"
site:developer.mozilla.org "Content-Security-Policy"
```

---

## Workflow

1. **Define technique + platform + version.** "Kerberoasting on Windows Server 2019" is actionable;
   "AD cheatsheet" is not.
2. **Find 2-3 canonical sources.** Prefer maintained repos with recent commits and references.
3. **Cross-check official documentation.** Cheatsheets simplify; versions and defaults differ.
4. **Extract the minimal command/payload template** and its prerequisites.
5. **Identify side effects and detection.** Will it crash, modify data, trigger alerts, or persist?
6. **Test only in an authorized lab (M9).** Snapshot first; isolate the network.
7. **Record source + date + version.** Note any deviations you needed.
8. **Prefer detection/defense guidance** when the goal is defensive.

---

## What to extract

| Field | Example |
|---|---|
| Technique | Kerberoasting |
| Platform | AD / Windows Server 2019 |
| Prerequisites | domain user, SPN account, RC4 enabled |
| Command template | `GetUserSPNs.py ...` (lab only) |
| Side effects | event 4769, possible lockout |
| Detection | Sigma rule, SIEM query |
| Source | URL + commit/date |
| Confidence | B (two sources + official docs) |

---

## Pitfalls

- **Destructive commands.** Some cheatsheets include `rm -rf`, fork bombs, or DoS snippets.
- **Version drift.** Flags and defaults change between tool versions.
- **Obfuscated/malicious repos.** Typosquats and fake cheatsheets can ship malware.
- **WAF/EDR evasion ethics.** Bypass techniques are dual-use; use only in authorized tests.
- **Copy-paste errors.** Quotes, escaping, and shell differences break commands.
- **Outdated techniques.** Defenses improve; verify the technique still works.
- **Licensing.** Some wordlists/payloads have usage restrictions.

---

## Ethics

- Use only in authorized labs or engagements.
- Do not run destructive or persistence techniques on production.
- Do not publish step-by-step weaponization for real targets.
- Prefer defensive equivalents (detection rules, secure configuration).
- Cite sources and respect licenses.

---

## Output contract

```
module:        M4 Cheatsheets
objective:     find validated reference for <technique/platform>
authorization: lab / authorized engagement
sources_used:  canonical repos + official docs + date, mapped to the claim it supports
sources_read:  URLs opened but excluded, with reason (off-scope, stale, duplicate, low confidence, inaccessible, discovery only)
findings:      prerequisites, template, side effects, detection
pivots:        M9 lab, M5 red team, M6 secure code
caveats:       version drift, destructive steps removed, confidence
```
