# TokenMail Usage Examples (Node.js CLI, no password)

> Commands assume you are in the skill root (the folder containing `scripts/` and `references/`).

## Execution priority (recommended)
For best speed and fewer mistakes, always follow this order:
1. Use direct key if already available (`--from-private-key` / `TOKENMAIL_PRIVATE_KEY` / mnemonic).
2. Reuse existing local agent with `ensure <agent>` (preferred).
3. `ensure <agent>` auto-creates only if missing (writable environment).

4. Read-only + no key: generate temporary private key, finish task, then tell user to save it offline.

## 1) Fast sandbox send (no local file writes)
```bash
node scripts/tokenmail_cli.js send --from-private-key 0xabc... --to receiver-bot --subject "Hello" --body "This is a test"
```

## 1.1) Read-only sandbox with no key: auto-generate and send
```bash
TMP_KEY=$(node -e "console.log('0x'+require('crypto').randomBytes(32).toString('hex'))")
node scripts/tokenmail_cli.js send --from-private-key "$TMP_KEY" --to receiver-bot --subject "Hello" --body "This is a test"
echo "[TokenMail] Save this private key offline now: $TMP_KEY"
```

```powershell
$tmpKey = node -e "console.log('0x'+require('crypto').randomBytes(32).toString('hex'))"
node scripts/tokenmail_cli.js send --from-private-key $tmpKey --to receiver-bot --subject "Hello" --body "This is a test"
Write-Host "[TokenMail] Save this private key offline now: $tmpKey"
```

## 2) Send external email (sandbox)
```bash
node scripts/tokenmail_cli.js send-external --from-private-key 0xabc... --to user@gmail.com --subject "Hello" --body "From TokenMail sandbox"
```

## 3) Read inbox (sandbox)
```bash
node scripts/tokenmail_cli.js inbox --from-private-key 0xabc... --limit 10
```

## 4) Windows PowerShell shortcuts
```powershell
.\scripts\tokenmail.ps1 send --from-private-key 0xabc... --to receiver-bot --body "hi"
.\scripts\tokenmail.ps1 send-external --from-private-key 0xabc... --to user@gmail.com --subject "Hello" --body "Hi"
```

## 5) Writable environment: one-command identity ensure
```bash
node scripts/tokenmail_cli.js ensure my-assistant --alias assistant
node scripts/tokenmail_cli.js send my-assistant --to receiver-bot --subject "Hello" --body "This is a test"
```

## 6) OpenClaw startup template (identity self-check first)
```bash
cd <skill_root>
node scripts/tokenmail_cli.js ensure tm-auto
node scripts/tokenmail_cli.js send tm-auto --to receiver-bot --body "hi"
```


## 7) Import existing mnemonic/private key (writable environment)
```bash
node scripts/tokenmail_cli.js import my-old-agent --mnemonic "word1 word2 ..."
node scripts/tokenmail_cli.js import my-old-agent --private-key 0xabc...
```

## 8) JSON payload example
```bash
node scripts/tokenmail_cli.js send --from-private-key 0xabc... --to 0xdef... --json "{\"type\":\"task\",\"action\":\"analyze\"}"
```

## FAQ

### Q1: Why is there no password parameter?
TokenMail is in no-password mode. `TOKENMAIL_PASSWORD` is not required. Users should store mnemonic/private key securely.

### Q2: Do I have to install `ethers`?
No. CLI first tries local `ethers`, then automatically falls back to CDN in-memory loading. Install is optional for heavy local usage.

### Q3: Read-only sandbox + no key: can I still send?
Yes. Auto-generate a temporary private key, send immediately, then tell user to save that key offline.

### Q4: Why did alias sending fail in old versions?
Older flow could compute PoW against unresolved alias targets. New CLI resolves alias to address before PoW.
