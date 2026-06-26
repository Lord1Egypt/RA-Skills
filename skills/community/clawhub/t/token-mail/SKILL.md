---
name: tokenmail
description: TokenMail skill for AI agent email communication using a Node.js CLI (no Python cryptography dependency). Optimized for sandbox usage with no mandatory npm install and no mandatory local file writes.
---

# TokenMail Skill (Node.js, no password, sandbox-friendly)

## When to use this skill
Use this skill when:
- The user wants Agent-to-Agent messaging or external email sending (Gmail/Outlook/etc.)
- Python crypto dependencies are unavailable or unreliable
- The environment is sandboxed (limited file writes, npm install blocked)
- Brand must stay unified as `TokenMail`

## Hard constraints
- Use `scripts/tokenmail_cli.js` as the primary entry
- Do **not** require `TOKENMAIL_PASSWORD` or `--password`
- `ethers` installation is **optional** (CDN in-memory fallback is supported)
- Prioritize user speed and task completion

## Command entry
```bash
node scripts/tokenmail_cli.js <command> [options]
```

Windows shortcuts:
- PowerShell: `scripts\tokenmail.ps1`
- CMD: `scripts\tokenmail.cmd`

## Required execution policy (critical)
For `send` / `send-external` / `inbox` / `alias`, follow this exact order:

1. **Direct key first (fastest)**
   - If `--from-private-key`, `TOKENMAIL_PRIVATE_KEY`, `--from-mnemonic`, or `TOKENMAIL_MNEMONIC` is available, execute immediately.

2. **Reuse existing agent before creating anything**
   - Use `ensure <agent>` (preferred) to reuse existing identity automatically.

3. **Only then auto-create (writable env only)**
   - `ensure <agent>` will auto-create only when missing.


4. **Read-only + no key (last resort)**
   - Auto-generate a temporary private key and continue the task.
   - After success, explicitly tell user to save it offline immediately.
   - If runtime crypto RNG is unavailable, ask user for existing mnemonic/private key.

## Important guardrail
Do **not** create a new account before checking existing identities.

## Recommended templates

### Bash: one-command identity ensure
```bash
node scripts/tokenmail_cli.js ensure tm-auto --alias tmauto
node scripts/tokenmail_cli.js send tm-auto --to receiver-bot --subject "Hello" --body "Hi"
```

### PowerShell: one-command identity ensure
```powershell
node scripts/tokenmail_cli.js ensure tm-auto --alias tmauto
node scripts/tokenmail_cli.js send tm-auto --to receiver-bot --subject "Hello" --body "Hi"
```


### Read-only + no key: temporary key fallback
```bash
TMP_KEY=$(node -e "console.log('0x'+require('crypto').randomBytes(32).toString('hex'))")
node scripts/tokenmail_cli.js send --from-private-key "$TMP_KEY" --to receiver-bot --subject "Hello" --body "Hi"
echo "[TokenMail] Temporary private key (save offline now): $TMP_KEY"
```

```powershell
$tmpKey = node -e "console.log('0x'+require('crypto').randomBytes(32).toString('hex'))"
node scripts/tokenmail_cli.js send --from-private-key $tmpKey --to receiver-bot --subject "Hello" --body "Hi"
Write-Host "[TokenMail] Temporary private key (save offline now): $tmpKey"
```

## Performance and install strategy
- `ethers` is **not required** for normal usage.
- Do **not** run `npm install` by default.
- For one-off/sandbox tasks, prefer `--from-private-key` for fastest execution.
- Optional optimization for heavy local usage:
  - `cd scripts && npm i --omit=dev ethers`

## Supported commands
- `create <name> [--alias <alias>] [--mnemonic "..."] [--private-key 0x...]`
- `ensure <name> [--alias <alias>] [--mnemonic "..."] [--private-key 0x...]`
- `import <name> --mnemonic "..."` or `--private-key 0x...`

- `list`
- `send [agent] --to <recipient> [--subject] [--body] [--json] [--from-private-key] [--from-mnemonic]`
- `send-external [agent] --to <email> --subject <s> --body <b> [--html] [--no-sign] [--from-private-key] [--from-mnemonic]`
- `inbox [agent] [--limit <n>] [--from-private-key] [--from-mnemonic]`
- `alias [agent] <alias> [--from-private-key] [--from-mnemonic]`
- `export <agent> [--output <file>]`
- `delete <agent> --force`

Global options:
- `--api-url <url>`
- `--keystore <dir>` (needed only for local keystore mode)

## References
- `references/api_reference.md`
- `references/examples.md`
- `scripts/tokenmail_cli.js`
- `scripts/tokenmail.ps1`
- `scripts/tokenmail.cmd`
