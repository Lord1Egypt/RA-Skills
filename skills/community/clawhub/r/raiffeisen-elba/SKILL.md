---
name: "raiffeisen-elba"
description: "Automate Raiffeisen ELBA online banking: login/logout, list accounts, and fetch transactions via Playwright."
summary: "Raiffeisen ELBA banking automation: login, accounts, transactions."
version: "1.5.3"
homepage: "https://github.com/odrobnik/raiffeisen-elba-skill"
metadata:
  openclaw:
    emoji: "🏦"
    requires:
      bins: ["python3"]
      python: ["requests", "playwright"]
---

# Raiffeisen ELBA Banking Automation

Fetch current account balances, securities depot positions, and transactions for all account types in JSON format. Uses Playwright to automate Raiffeisen ELBA online banking.

## ⚠️ Security & 2FA Flow

This skill requires explicit 2FA approval on the user's mobile device (pushTAN).

1. **Start the Login Process:** Start the login using the OpenClaw `process` tool with the `exec` command or run it as a background job via the `exec` tool.
2. **Tell the user to approve:** You MUST stop executing further commands and inform the user of the pushTAN code (e.g., `ELBA PUSHTAN CODE: XXXX`). Do not loop polling the process without telling the user what to do. Use `sessions_yield` to wait for the user to confirm approval.
3. **Wait for approval:** Only resume the automation flow after the user confirms approval. If the login process exits with a timeout (usually 60-300 seconds), ask the user if they are ready before restarting the login.
4. **Ephemeral Bearer Token:** After successful 2FA, the token is cached locally (`0600`).
5. **Always Logout:** Run `logout` after completing operations to clear the session.

## Setup & Configuration

See [SETUP.md](SETUP.md) for prerequisites and configuration.

- **Profiles:** Credentials live in `<WORKSPACE_ROOT>/raiffeisen-elba/config.json`. If it has a `profiles` object, each key is a profile name; check which profiles exist when it is ambiguous which login the user means.
- **Profile Argument:** If multiple profiles exist, pass `--profile <name>` to all ELBA commands. The argument must match the key in `config.json`.

## Commands

**Entry point:** `python3 {baseDir}/scripts/elba.py`

```bash
# Authenticate (requires pushTAN approval)
python3 {baseDir}/scripts/elba.py [--profile <name>] login

# List all accounts
python3 {baseDir}/scripts/elba.py [--profile <name>] accounts [--json]

# Download transactions (--json prints to stdout; --out <file> writes a file instead)
# Important: If the account ID/IBAN fails, check the exact ID string output by the `accounts` command. Some accounts have an internal ID rather than a pure IBAN.
python3 {baseDir}/scripts/elba.py [--profile <name>] transactions --account <id|iban> --from YYYY-MM-DD --until YYYY-MM-DD [--json]

# Fetch depot portfolio positions
python3 {baseDir}/scripts/elba.py [--profile <name>] portfolio --depot-id <id> [--json]

# Clear session and cached token
python3 {baseDir}/scripts/elba.py [--profile <name>] logout
```

## Recommended Workflow

1. Check `config.json` for the profile name if more than one login is configured.
2. Run the `login` process using the `exec` and `process` tools to read the generated pushTAN code.
3. Inform the user to approve the pushTAN on their device and wait for their confirmation.
4. Once logged in, run `accounts --json` to get the list of accounts and exact account IDs.
5. Run `transactions --account <exact-id-from-step-4> --from YYYY-MM-DD --until YYYY-MM-DD --json` and redirect the output to a JSON file (e.g. `> /tmp/elba_tx.json`). Progress messages go to stderr, so the file contains only JSON.
6. Run `logout` to clear the session.
