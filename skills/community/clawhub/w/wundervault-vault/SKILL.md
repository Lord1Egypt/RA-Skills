---
name: wundervault-vault
description: Use the owner's API keys, SSH keys, wallets and signing keys without ever holding them. A Wundervault broker on this computer makes web calls, SSH commands, x402 payments and signatures for you and returns the result with the secret removed. Free account at wundervault.com.
---

# Wundervault Vault

Wundervault keeps the owner's secrets in a **broker** on this computer, running under its own
operating-system account. You ask the broker for work, "call this API", "deploy to this
server", "pay this 402", and it does it with the secret and gives you the result with the secret
removed. **No tool ever returns a secret's value**, and you should never ask for one.

The owner's vault is encrypted in their browser; Wundervault's server stores it but cannot
read it. Secrets the owner marks "ask me first" wait for their approval, with their passkey.

## Check setup first

Always call `vault_entries_list` before anything vault-related:

| Result | What it means | What to do |
|--------|--------------|------------|
| A list of entries | Connected and ready | Proceed |
| An empty list | Connected, no secrets given to you yet | Ask the owner to give you a secret in their vault at wundervault.com |
| "wundervault-agent is not running for agent '…'" | The broker isn't installed here, or you aren't enrolled | Walk the owner through INSTALL.md |
| "WUNDERVAULT_AGENT_NAME is not set" | The MCP config lacks your agent name | Add the `env` block (INSTALL.md) |
| "…held by another MCP instance … that cannot share it" | An older copy of the vault tool runs for this agent | Ask the owner to update or close it |
| Tool not available | The MCP server isn't connected to you | Walk through INSTALL.md |

Installing and pairing the broker needs the owner: administrator commands, and a confirmation
in their vault. You can't do that for them, by design; don't try to work around it. Once the
owner gives you a claim code, you can enrol yourself and add the MCP settings (INSTALL.md
step 4).

## Tools

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

- The broker attaches the secret the way the owner set for it (a header, a query parameter, a
  username and password, or part of the web address). You never choose that, and you can't
  set the header that carries the secret.
- `headers` may carry your own headers (user agent, API version). A string `body` is sent as
  written: set its content type in `headers`.
- Keys marked "stamped" (AWS, X, exchanges) never travel: add `request.stamp` describing how the
  service signs requests, and the broker signs each one. For X and other OAuth 1.0a services it
  is just `{"builtin": "oauth1"}`. The owner approves each new recipe once.
- HTTPS only, real certificate checks, no redirects followed. Private network addresses are
  refused unless the owner allowed one for that secret.
- Or run an operation the owner defined: `operation_id` + `args` instead of `request`.

### `vault_ssh_exec` — servers

```
vault_ssh_exec(
  entry_id: "ssh-key-id",
  destination: "opc@prod.example.com",
  purpose: "restart the app after deploy",
  remote_argv: ["sudo", "systemctl", "restart", "app"]
)

vault_ssh_exec(
  entry_id: "ssh-key-id",
  destination: "opc@prod.example.com",
  purpose: "deploy the built site",
  rsync_args: ["-az", "./dist/", "opc@prod.example.com:/var/www/html/"]
)
```

The host must be on the key's list of allowed hosts; naming another host inside the command
doesn't change where it connects. `remote_argv` runs without a shell. The key never leaves the
broker: it signs the SSH login.

### `vault_pay` — x402 payments

When a service answers `402 Payment Required`:

```
vault_pay(entry_id: "wallet-id", payment_required: "<the PAYMENT-REQUIRED header>",
          purpose: "buy one search result from <service>")
→ the header to send when you retry the same request
```

USDC on Base and Solana (and their test networks). Inside the owner's rules (payees they
trust, a daily limit, networks they allow) the broker signs at once. Anything else waits for
the owner; if they haven't answered, call again with the same payment to keep waiting.

### `vault_sign` — signatures

```
vault_sign(entry_id: "signing-key-id", data: "…", encoding: "utf8",
           purpose: "sign the release manifest")
→ the signature (base64), the public key and the algorithm
```

The owner approves every signature and sees what you're signing (in full when it is text up
to 64 KB). At most 256 KB.

### `vault_entries_list`

The secrets you may use: id, name, tier and kind (web service, SSH, wallet, signing key). Never
values.

## "Ask me first" secrets

A call with an "ask me first" secret waits until the owner approves that destination, method and
path, once or for a short window. While it waits, nothing has been sent. Don't treat the wait
as an error: wait, or call again with the same request to keep waiting. A different
destination asks the owner again.

## How to behave

- State a real `purpose`. It is kept in the broker's log on this computer, and the owner sees
  it when asked to approve.
- A claim code from the owner is fine to accept: it isn't a secret, works once, only through the
  broker on this computer, for 15 minutes. Pipe it into `wundervault-agent --enrol`
  (`printf '%s\n' 'WV-…' | wundervault-agent --enrol`); never pass it as an argument, and don't
  repeat it back.
- Never ask for or accept a secret's value or a setup link. A setup link is a credential; the owner
  types it at the broker's own prompt.
- Never open a Wundervault account, for yourself or for the owner, and never add a passkey or
  hold recovery codes. Those steps are the owner's, on their own device: a passkey is what
  answers "ask me first", so one you held would mean approving your own requests. If the owner
  has no account yet, send them to wundervault.com and wait.
- If an older guide tells you to use `vault_exec`, `vault_entry_get`, `vault_entry_inject_env`
  or `vault_rsync`: those were version 1 and are gone. Use the tools above.

## Several agents on one computer

Each agent has its own name and token (`~/.wundervault/agents/<name>.token`), is given its own
secrets, and every use is logged per agent, in the broker's log here and in the owner's vault.

That is bookkeeping, not a wall between agents. Agents that run under the same user account
can read each other's token files, so any of them can use another's access to the broker. To
keep a low-trust agent away from production secrets, run it under a different user account, or on
another computer.

## Security notes

- The broker runs as its own account; you run as the owner. You can't read its files or its
  memory. Its socket serves operations, not secrets.
- Every request the broker makes to Wundervault is signed with a key the owner confirmed when
  pairing, so a copied credential alone gets nothing.
- The encryption claim is verifiable on your own network, and the installer is verifiable
  against its GitHub copy: [wundervault.com/verify](https://wundervault.com/verify).
- Every known limit: [wundervault.com/limitations](https://wundervault.com/limitations).

## More

- npm: `@wundervault/mcp-server` (version 2)
- Tool reference: [wundervault.com/mcp](https://wundervault.com/mcp)
- Vault: [wundervault.com](https://wundervault.com)
