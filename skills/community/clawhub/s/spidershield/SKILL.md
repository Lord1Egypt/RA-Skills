# SpiderShield Security Scanner

Security scanning and trust scoring for OpenClaw skills. 6 commands covering
the full security lifecycle: trust lookup, malware scan, config audit,
auto-fix, rug pull detection, and bulk scanning.

**4,000+ skills pre-scanned. Precision 93%+ (improving). 0.1s trust score lookup.**

---

## Setup

The `/spidershield check` command works immediately — no installation needed.
It queries the SpiderRating Trust API (public, no key required).

For local scanning commands (scan, audit-config, fix, pin, scan-all),
install the scanner:

```bash
pip install spidershield
```

---

## Commands

### /spidershield check <author/skill>

Check the Trust Score for a published skill. Queries the SpiderRating Trust
Registry (4,000+ pre-scanned skills) and returns score, grade, capabilities,
ecosystem ranking, and VirusTotal comparison.

**Examples**:
```
/spidershield check spclaudehome/web-search-pro
/spidershield check alice/my-skill
```

**Output**:
```
SpiderRating Skill Trust Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Skill:      spclaudehome/web-search-pro
  Score:      7.2 / 10   Grade: B
  Verdict:    ✅ SAFE
  Precision:  93%+ (improving)

  📦 Capabilities:
    🌐 Browser  📦 Installs Deps  🔗 Webhook

  🔍 Security: 0 critical · 0 high · 1 medium · 0 low
    [HIGH] No sandbox — Agent can execute arbitrary shell commands

  📊 Ecosystem: #142 / 4,037 skills (Top 4%)
    Breakdown: Description 6.5 · Security 8.0 · Metadata 5.5
    Downloads: 5,000  Active installs: 42

  💡 Rated B (7.2/10) — safe to install.
  🔗 https://spiderrating.com/servers/spclaudehome__web-search-pro
```

**Implementation**: calls `scripts/check.sh $1`

---

### /spidershield scan <path>

Scan a single skill for malicious patterns using 24 detection rules.
Detects credential theft, prompt injection, crypto wallet access,
obfuscated payloads, and more.

**Examples**:
```
/spidershield scan ./my-skill/
/spidershield scan ./my-skill/SKILL.md
```

**Output**:
```
SAFE — my-skill
```
or
```
MALICIOUS — evil-skill
  • Reads ~/.ssh/id_rsa and sends to external webhook
  • Base64-encoded shell command detected
```

**Implementation**: calls `scripts/scan.sh $1`

---

### /spidershield audit-config [--skills] [--verify]

Audit your OpenClaw installation for insecure settings.
Checks 10 configuration items including gateway binding, auth strength,
sandbox mode, and file permissions.

**Options**:
- `--skills` — Also scan all installed skills for malware
- `--verify` — Also verify pinned skills for tampering

**Examples**:
```
/spidershield audit-config
/spidershield audit-config --skills --verify
```

**Implementation**: calls `scripts/audit-config.sh`

---

### /spidershield fix [--dry-run]

Scan OpenClaw config and auto-fix insecure settings.
Shows before/after score change.

**Options**:
- `--dry-run` — Preview what would be fixed without making changes

**Examples**:
```
/spidershield fix --dry-run
/spidershield fix
```

**Output**:
```
Score: 5.2/10 -> 8.1/10
Fixed: gateway binding, auth strength, sandbox mode
```

**Implementation**: calls `scripts/fix.sh`

---

### /spidershield pin add|verify|list|remove [path]

Pin skill content hashes to detect rug pull attacks — when a skill
is silently modified after installation (supply chain attack).

**Subcommands**:
- `pin add <path>` — Record current content hash
- `pin verify [path]` — Check if any pinned skills were modified
- `pin list` — Show all pinned skills
- `pin remove <name>` — Remove a pin

**Examples**:
```
/spidershield pin add ~/.openclaw/skills/web-search-pro/
/spidershield pin verify
/spidershield pin list
```

**Output**:
```
OK web-search-pro
TAMPERED evil-skill
  - Content hash changed since pin (possible rug pull)

Results: 12 OK, 1 TAMPERED, 0 UNKNOWN
```

**Implementation**: calls `scripts/pin.sh $1 $2`

---

### /spidershield scan-all

Scan ALL installed OpenClaw skills for malicious patterns in one command.
Equivalent to `/spidershield audit-config --skills`.

**Example**:
```
/spidershield scan-all
```

**Implementation**: calls `scripts/scan-all.sh`

---

## Privacy

- `/check`: sends only `author/skill` slug to SpiderRating API
- `/scan`, `/audit-config`, `/fix`, `/pin`, `/scan-all`: run **entirely locally** — no data leaves your machine
- SpiderRating never stores your code, credentials, or session data

---

## Links

- Trust Registry: https://spiderrating.com
- Source: https://github.com/teehooai/spidershield
- Issues: https://github.com/teehooai/spidershield/issues
