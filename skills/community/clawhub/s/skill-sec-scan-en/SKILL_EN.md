# 🔒 Skill Security Scanner

**Enterprise-Grade Skill Security Scanner**

Automatically detect security risks in ClawHub / GitHub / local Skills. Supports JavaScript, TypeScript, Python, Shell files with threat intelligence-driven static analysis.

---

## 🎯 Core Features

| Feature | Description |
|---------|-------------|
| **Multi-File Detection** | Supports `.js`, `.ts`, `.py`, `.sh` |
| **Threat Classification** | 4 Major Categories: EXFIL, INJECTION, OBFUSCATION, TROJAN |
| **Detection Rules** | 57 refined detection rules covering 60+ dangerous patterns |
| **Smart Scoring** | 100-point scoring system for quantified risk levels |
| **Whitelist** | User-defined trusted Skills |

---

## 🛡️ Threat Classification

| Category | Code | Risks |
|----------|------|-------|
| **Data Exfiltration** | EXFIL | credential-access, vault-access, private-key, api-key, network-backdoor, http-server, network-request, http-client, database-access, config-write, wallet-access, port-listening, proxy-tor, git-operation, file-download |
| **Injection Attack** | INJECTION | remote-script, cmd-execution, npx-exec, dynamic-exec, prompt-injection, jailbreak, dynamic-import, backtick-injection, system-probing, shell-injection, crypto-operation |
| **Trojan/Backdoor** | TROJAN | destructive-delete, credential-read, process-kill, persistent-timer, postinstall-risk, archive-exploit, arbitrary-write, deserialize |
| **Code Obfuscation** | OBFUSCATION | base64, env-trigger, hidden-exec, persistent-shell, obfuscated-package |

---

## 📊 Detection Rules (57 Total)

| Category | Rules | Sample Rules |
|----------|-------|--------------|
| INJECTION | 19 | cmd-execution, npx-exec, dynamic-exec, prompt-injection, jailbreak |
| EXFIL | 18 | credential-access, vault-access, private-key, network-backdoor |
| TROJAN | 14 | destructive-delete, process-kill, shell-injection, persistent-timer |
| OBFUSCATION | 6 | base64, env-trigger, hidden-exec, persistent-shell |

---

## ⚡ Quick Start

### Single Scan

```bash
./scripts/scan.sh https://clawhub.ai/owner/skill-name
./scripts/scan.sh ~/.openclaw/workspace/skills/skill-name
```

### Batch Scan

```bash
./scripts/scan-all.sh
```

---

## Trigger Methods

### Scan Detection

| Trigger | Description |
|---------|-------------|
| `scan [URL/name]` | Scan a skill for security |
| `check security of [skill]` | Check if skill is safe |
| `detect [skill]` | Detect security issues |

### Risk Inquiry

| Trigger | Description |
|---------|-------------|
| `is [skill] risky?` | Ask about risk level |
| `is [skill] safe?` | Ask if skill is safe |
| `does [skill] have issues?` | Ask about problems |

---

## Report Output Format

### Standard Template

```
🔒 **Skill Security Report**
════════════════════════════════════════════════════════════════════

**Skill Name:** <name>
**Scanned Files:** <N>
**Issues Found:** <N>

📊 Score: ✅/⚠️/🚫 <score>/100 — <status>

🔍 **Checklist:** All threat categories scanned

| File Type | Status |
|-----------|--------|
| JavaScript (.js) | ✅/➖ None |
| TypeScript (.ts) | ✅/➖ None |
| Python (.py) | ✅/➖ None |
| Shell (.sh) | ✅/➖ None |

**🛡️ Detection Rules (57 total):**
- **EXFIL (18):** credential-access, vault-access, private-key...
- **INJECTION (19):** remote-script, cmd-execution...
- **TROJAN (14):** destructive-delete, process-kill...
- **OBFUSCATION (6):** base64, env-trigger...

📊 **Results:** Found <N> issues (if any)
- 🔴 critical: <N>
- 🟠 high: <N>
- 🟡 medium: <N>

---

**⚠️ Issue Details:** (if any)

| # | Category | Rule | Level | File |
|:---:|----------|------|-------|------|
| 1 | <Cat> | <rule> | <level> | <file> |

---

**Explanation:**
- <rule> — <explanation>

---

✅/⚠️/🚫 **Conclusion:** <verdict>

════════════════════════════════════════════════════════════════════
```

### Scoring

| Score | Status | Conclusion |
|-------|--------|------------|
| 80-100 | ✅ Safe | Recommended |
| 30-79 | ⚠️ Suspicious | Use with caution |
| 0-29 | 🚫 Dangerous | Not recommended |

---

## 🤖 Agent Behavior Guide

After batch scan, Agent should prompt user for individual scans:

```
✅ Passed: 14
🚫 Attention needed: 5

⚠️ Risky skills:
• crypto-wallet (score: 0)
• solana-wallet (score: 0)
• litcoin (score: 30)

💡 Run individual scan for full report:
   "scan crypto-wallet"
   "check litcoin"
```

---

## Supported File Types

| Type | Extension | Status |
|------|-----------|--------|
| JavaScript | `.js` | ✅ |
| TypeScript | `.ts` | ✅ |
| Python | `.py` | ✅ |
| Shell | `.sh` | ✅ |

---

## Version History

### v1.0.0 (2026-03-18)
- Initial release
- 57 detection rules
- 4 threat categories
- Markdown report format
- Whitelist support
- Batch scanning
