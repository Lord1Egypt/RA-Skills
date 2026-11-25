---
name: wundervault-vault
description: Use the owner's API keys, SSH keys, wallets, signing keys and authenticator codes without ever holding them. The Wundervault helper app on this computer makes web calls, SSH commands and git pushes, x402 payments and signatures for you, makes new keys straight into the owner's vault, and runs scheduled jobs the owner approved. No tool returns a secret. Free account at wundervault.com.
---

# Wundervault Vault

Wundervault keeps the owner's secrets in the **helper app** on this computer, running under its
own operating-system account. You ask the helper app for work, "call this API", "deploy to this
server", "pay this 402", and it does it with the secret and gives you the result with the secret
removed. **No tool ever returns a secret's value**, and you should never ask for one.

The owner's vault is encrypted in their browser; Wundervault's server stores it but cannot
read it. Secrets the owner marks "ask me first" wait for their approval, with their passkey.

Site: [wundervault.com](https://wundervault.com) · Releases: [@wundervault1 on X](https://x.com/wundervault1) ·
Source: [github.com/wundervault/wundervault-mcp](https://github.com/wundervault/wundervault-mcp)

## Check setup first

Always call `vault_entries_list` before anything vault-related:

| Result | What it means | What to do |
|--------|--------------|------------|
| A list of entries | Connected and ready | Proceed |
| An empty list | Connected, no secrets given to you yet | Ask the owner to give you a secret in their vault at wundervault.com |
| "wundervault-agent is not running for agent '…'" | The helper app isn't installed here, or you aren't enrolled | Walk the owner through INSTALL.md |
| "WUNDERVAULT_AGENT_NAME is not set" | The MCP config lacks your agent name | Add the `env` block (INSTALL.md) |
| "…held by another MCP instance … that cannot share it" | An older copy of the vault tool runs for this agent | Ask the owner to update or close it |
| Tool not available | The MCP server isn't connected to you | Walk through INSTALL.md |

Installing and pairing the helper app needs the owner: administrator commands, and a
confirmation in their vault. You can't do that for them, by design; don't try to work around it.
Once the owner gives you a claim code, you can enrol yourself and add the MCP settings
(INSTALL.md step 3).

## Tools

| Tool | What it does |
|------|--------------|
| `vault_call` | Calls a web service with a secret attached; returns the answer with the secret removed. |
| `vault_new_key` | Makes a new key at a service and puts it straight into the owner's vault. You never see it. |
| `vault_save_secret` | Saves a secret you already have (a file, a command's output) into the vault without reading it into the chat. |
| `vault_send_secret` | Puts vault secrets into a Cloudflare Worker's encrypted settings. The owner approves the list once. |
| `vault_ssh_exec` | Runs a command on an approved server, or rsyncs files to it. The key signs the login and never leaves the helper app. |
| `vault_git` | git push, pull, fetch, clone or ls-remote over SSH with a vaulted key (Linux and macOS). |
| `vault_2fa_code` | The current authenticator-app code for a sign-in. Never the setup key. |
| `vault_pay` | Pays an x402 "402 Payment Required" in USDC on Base or Solana, inside the owner's limits. |
| `vault_sign` | Signs data with a signing key. The owner approves every signature. |
| `vault_job_request` | Asks the owner for a scheduled job (a backup, a sync) that the helper app runs on a server. |
| `vault_job_status`, `vault_jobs`, `vault_job_run_now` | Follow a job request, list your jobs, ask for one run now. |
| `vault_done` | Says you've finished, so admin access can end. |
| `vault_entries_list` | The secrets you may use and what kind each is. Never values. |

Full arguments for every tool: [wundervault.com/mcp](https://wundervault.com/mcp).

### `vault_call` — web services

```
vault_call(
  entry_id: "abc123",
  purpose: "send the weekly report email",
  request: {
    origin: { scheme: "https", host: "api.resend.com", port: 443 },
    method: "POST", path: "/emails",
    body: { from: "…", to: ["…"], subject: "…", html: "…" }
  }
)
```

- The helper app attaches the secret the way the owner set for it (a header, a query parameter,
  a username and password, or part of the web address), and you can't set the header that
  carries the secret yourself. For a key saved without a way, you may propose one with `send_as`;
  the owner approves it once per address.
- `headers` may carry your own headers (user agent, API version). A string `body` is sent as
  written: set its content type in `headers`.
- Keys marked "stamped" (AWS, X, exchanges) never travel: add `request.stamp` describing how the
  service signs requests, and the helper app signs each one. For X and other OAuth 1.0a services
  it is just `{"builtin": "oauth1"}`. The owner approves each new recipe once.
- HTTPS only, real certificate checks, no redirects followed. Private network addresses are
  refused unless the owner allowed one for that secret.
- Or run an operation the owner defined: `operation_id` + `args` instead of `request`.

### `vault_new_key` and `vault_save_secret` — putting keys in the vault

`vault_new_key` makes a key at a service (Resend, Cloudflare, SendGrid, OpenAI, Twilio,
OpenRouter) using a secret allowed to create keys, and sends it straight to the owner's vault.
You get the key's id and name at the service, never the key. With `replaces_entry_id` it
rotates a secret you already have.

`vault_save_secret` saves something you already hold, `from_file`, `from_command` (no shell,
standard output only) or `value`, with `pick` for one `.env` line or JSON field. You get the
name, source and length, never the value.

Either way the new secret waits in the owner's vault until they save it with their passkey and
choose which agents may use it.

### `vault_ssh_exec` and `vault_git` — servers and repositories

```
vault_ssh_exec(
  entry_id: "ssh-key-id",
  destination: "opc@prod.example.com",
  purpose: "restart the app after deploy",
  remote_argv: ["sudo", "systemctl", "restart", "app"]
)

vault_git(
  entry_id: "ssh-key-id", purpose: "push the release branch",
  subcommand: "push", repo_dir: "/home/me/site", remote: "origin", refspecs: ["release"]
)
```

The host must be an approved server for that key (a new one asks the owner on first use);
naming another host inside the command doesn't change where it connects. `remote_argv` runs
without a shell. `rsync_args` instead of a command copies files; every host:path is checked.
`vault_git` checks every address git would use; SSH remotes only, no `--force`.

**Admin keys.** A server can have an everyday key (looking: code, health, logs) and an admin key
(changes: deploys, settings, containers). Use the everyday key for anything that only reads. The
admin key works only while the owner allows admin access, for 5, 15 or 60 minutes, with their
passkey; without it you get `ADMIN_ACCESS_REQUIRED` and the owner is asked. Call again once
they've allowed it, and call `vault_done` when you've finished. Connections close when admin
access ends.

### `vault_job_request` — scheduled jobs

Ask for a job the helper app runs on its own: an exact `argv` (no shell) on a server, with an
everyday SSH key, `daily` at a time or `every` N hours, plus `why` for the owner. Add `file` for a
job whose output is a file to keep, such as a backup. Nothing runs until the owner approves the
exact command on the vault's Jobs page; changing anything is a new request. Then follow it with
`vault_job_status`, list jobs with `vault_jobs`, and ask for an extra run with
`vault_job_run_now` (at most once per 10 minutes per job). You never see a job's output.

### `vault_pay` — x402 payments

When a service answers `402 Payment Required`:

```
vault_pay(entry_id: "wallet-id", payment_required: "<the PAYMENT-REQUIRED header>",
          purpose: "buy one search result from <service>")
→ the header to send when you retry the same request
```

USDC on Base and Solana (and their test networks). Inside the owner's rules (payees they
trust, a daily limit, networks they allow) the helper app signs at once. Anything else waits for
the owner; if they haven't answered, call again with the same payment to keep waiting.

### `vault_sign` — signatures

```
vault_sign(entry_id: "signing-key-id", data: "…", encoding: "utf8",
           purpose: "sign the release manifest")
→ the signature (base64), the public key and the algorithm
```

The owner approves every signature and sees what you're signing (in full when it is text up
to 64 KB). At most 256 KB.

### `vault_2fa_code` — authenticator codes

`vault_2fa_code(entry_id, purpose)` returns the current code and how long it stays valid.
Authenticator-app codes only: not text-message or email codes, not passkeys.

## "Ask me first" secrets

A call with an "ask me first" secret waits until the owner approves that destination, method and
path, once or for a short window. While it waits, nothing has been sent. Don't treat the wait
as an error: wait, or call again with the same request to keep waiting. A different
destination asks the owner again.

## How to behave

- State a real `purpose`. It is kept in the helper app's log on this computer, and the owner
  sees it when asked to approve.
- A claim code from the owner is fine to accept: it isn't a secret, works once, only through the
  helper app on this computer, for 15 minutes. Pipe it into `wundervault-agent --enrol`
  (`printf '%s\n' 'WV-…' | wundervault-agent --enrol`); never pass it as an argument, and don't
  repeat it back.
- Never ask for or accept a secret's value or a setup link. A setup link is a credential; the
  owner types it at the helper app's own prompt. If you already hold a secret, save it with
  `vault_save_secret` instead of pasting it anywhere.
- Never open a Wundervault account, for yourself or for the owner, and never add a passkey or
  hold recovery codes. Those steps are the owner's, on their own device: a passkey is what
  answers "ask me first", so one you held would mean approving your own requests. If the owner
  has no account yet, send them to [wundervault.com](https://wundervault.com) and wait.
- If an older guide tells you to use `vault_exec`, `vault_entry_get`, `vault_entry_inject_env`
  or `vault_rsync`: those were version 1 and are gone. Use the tools above.

## Several agents on one computer

Each agent has its own name and token (`~/.wundervault/agents/<name>.token`), is given its own
secrets, and every use is logged per agent in the helper app's log on this computer. For
"run without asking" secrets, where a secret went and why stays on this computer; Wundervault
never sees it.

That is bookkeeping, not a wall between agents. Agents that run under the same user account
can read each other's token files, so any of them can use another's access to the helper app.
To keep a low-trust agent away from production secrets, run it under a different user account,
or on another computer.

## Security notes

- The helper app runs as its own account; you run as the owner. You can't read its files or its
  memory. Its socket serves operations, not secrets.
- Every request the helper app makes to Wundervault is signed with a key the owner confirmed
  when pairing, so a copied credential alone gets nothing.
- The helper app and the browser encryption are open source:
  [wundervault-mcp](https://github.com/wundervault/wundervault-mcp) and
  [wundervault-crypto](https://github.com/wundervault/wundervault-crypto). The encryption claim
  is verifiable on your own network: [wundervault.com/verify](https://wundervault.com/verify).
- Every known limit: [wundervault.com/limitations](https://wundervault.com/limitations).

## More

- npm: `@wundervault/mcp-server` (version 2)
- Tool reference: [wundervault.com/mcp](https://wundervault.com/mcp)
- Vault: [wundervault.com](https://wundervault.com)
- What's new: [wundervault.com/changelog](https://wundervault.com/changelog)
- Releases and security notes: [@wundervault1 on X](https://x.com/wundervault1)
