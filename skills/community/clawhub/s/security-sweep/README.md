# Security Sweep for OpenClaw

A comprehensive security scanner for OpenClaw skills and plugins. Scans for hardcoded secrets, dangerous exec patterns, dependency vulnerabilities, network egress, and shell injection surfaces.

When secrets are found, they can be **auto-encrypted to Notion** — never stored in plain text.

---

## Features

- 🔍 **Secret Detection** — Scans for API keys, tokens, passwords, credentials hardcoded in skill files
- 🐚 **Exec Pattern Analysis** — Finds dangerous `exec()`, `spawn()`, `eval()`, and shell injection surfaces
- 📦 **NPM Audit** — Checks for vulnerable dependencies in skills with `package.json`
- 🌐 **Network Egress** — Reports unexpected outbound connections
- 🔒 **Auto-Encrypt to Notion** — Encrypts found secrets to your Notion secrets store (AES-256-GCM)
- 🚀 **CI-Ready** — Exit codes and structured output for use in GitHub Actions

---

## Quick Start

```bash
# Scan all skills
bash scripts/full-scan.sh \
  --builtin "$(brew --prefix)/Cellar/openclaw-cli/2026.3.13/libexec/lib/node_modules/openclaw/skills" \
  --workspace "$HOME/.openclaw/workspace/skills" \
  --output ~/security-sweep-report.txt

# Quick scan (fast patterns only)
bash scripts/quick-scan.sh --dir ~/.openclaw/workspace/skills
```

---

## Reports

Reports are saved to the output file you specify. Each finding includes:
- File path
- Risk level (CRITICAL / HIGH / MEDIUM / LOW / INFO)
- Recommended action

Sample output:
```
━━━ WORKSPACE SKILLS Summary ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔴 CRITICAL: 0
  🟠 HIGH:     0
  🟡 MEDIUM:   0
  🟢 LOW:      0
  ℹ️  INFO:     3

━━━ Findings ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ℹ️  NETWORK: skill/example/public/js/api.js
  ℹ️  NETWORK: skill/example/src/index.js
```

---

## Risk Levels

| Level | Description | Example |
|-------|-------------|---------|
| 🔴 CRITICAL | Hardcoded secret or unsafe eval | `const key = "sk-123..."` |
| 🟠 HIGH | Dangerous exec without sanitization | `exec(userInput)` |
| 🟡 MEDIUM | Shell injection surface or npm audit failure | `bash -c "${var}"` |
| 🟢 LOW | Overly broad file permissions | `chmod 777` |
| ℹ️ INFO | Expected network egress documented | External API call |

---

## ⚠️ Warning: `--encrypt-found` Requires a Secure Private Skillbase

The `--encrypt-found` flag is powerful but **assumes your private skill directory is already secure**. It encrypts found secrets to Notion before removal — but:

- **If your private skills already contain real secrets, those secrets are already exposed** — the scan is read-only and doesn't cause leaks
- **If your Notion is compromised, encrypted blobs are useless without the master password** — but the attacker gets the ciphertext
- **The encryption protects secrets at rest in Notion** — it does NOT protect secrets in transit or in your shell history

**You should NOT use `--encrypt-found` if:**
- Your private skillbase may contain uncommitted work-in-progress with real credentials
- You haven't set up the Notion secrets store yet
- You're scanning a third-party skill you don't control

**Always review the findings before any auto-encryption** — the flag is off by default for this reason.

> **⚠️ CRITICAL:** The master password is the only way to decrypt your secrets. **Forget it and the secrets are permanently unrecoverable** — AES-256-GCM with PBKDF2 (100k iterations) is intentionally slow and cannot be brute-forced. Store it in a password manager.

## Auto-Encrypt to Notion

When `--encrypt-found` is used and `NOTION_MASTER_PASSWORD` is set, found secrets are encrypted to your Notion secrets store before being removed.

```bash
export NOTION_MASTER_PASSWORD="your-master-password"
bash scripts/full-scan.sh --encrypt-found [options]
```

Requires `notion-secrets.js` in `~/.openclaw/scripts/`. See `references/notion-encryption.md` for setup.

---

## Before Publishing

Run a full scan and confirm:
- [ ] 0 CRITICAL findings
- [ ] 0 HIGH findings
- [ ] All npm audits pass
- [ ] No secrets anywhere in the codebase
- [ ] All network egress is expected and documented

---

## GitHub Actions Integration

```yaml
- name: Security Sweep
  run: |
    bash scripts/full-scan.sh \
      --builtin "./skills" \
      --output "./security-report.txt"
    # Fail on CRITICAL or HIGH
    grep -qE "🔴|🟠" ./security-report.txt && exit 1
```

---

## License

MIT — free to use, modify, and distribute.
