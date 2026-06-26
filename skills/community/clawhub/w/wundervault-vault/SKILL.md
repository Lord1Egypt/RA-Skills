---
name: wundervault-vault
description: Read passwords, API keys, and credentials from a Wundervault zero-knowledge, multi-agent vault, and run authorized shell commands with secrets injected — without exposing them in chat. Requires a Wundervault account — request early access at wundervault.com.
---

# Wundervault Vault

Wundervault is an encrypted, self-hosted secret vault that exposes secrets to agents via MCP tools. Secrets never appear in chat — they are decrypted server-side and injected directly into commands or written to config files. **The plaintext of a secret is never returned to the agent.**

## Check Setup First

Always call `vault_entries_list` before doing anything vault-related. Use the result to determine where the user is in setup:

| Result | What it means | What to do |
|--------|--------------|------------|
| Returns a list of entries | Vault is connected and ready | Proceed |
| Returns empty list | Connected but no secrets yet | Tell the user to add secrets at wundervault.com |
| Returns auth/credentials error | MCP server installed but not onboarded | Walk through onboarding (see below) |
| Tool not available | MCP server not wired to this agent | Walk through setup (see INSTALL.md) |

### First-run onboarding

If the vault tools are missing or credentials are invalid, tell the user:

> "Wundervault isn't set up yet. Here's how to get started:
> 1. Request access via the [contact form](https://wundervault.com/contact)
> 2. Once approved, set up your account and onboard your agent at wundervault.com
> 3. Verify the MCP server package using the checksums at [wundervault.com/install](https://wundervault.com/install)
> 4. Come back and I'll verify the connection"

Do not attempt to use any vault tools until `vault_entries_list` succeeds.

## Tools

### `vault_entries_list`
List all vault entries available to this agent. Returns entry IDs and names only — no secret values.

```
vault_entries_list()
→ [{ id: "abc123", name: "ResendApiKey", tier: "full" }, ...]
```

Use this first to get the entry ID before calling any other tool.

### `vault_entry_get`
Retrieve and burn a secret. The secret is decrypted server-side and **never returned to the agent** — you will receive a burn confirmation only.

```
vault_entry_get(entry_id: "abc123", purpose: "confirm secret exists")
→ "✅ Secret retrieved and burned."
```

Use this only to confirm a secret exists or to acknowledge retrieval. To actually use a secret in a command or file, use `vault_exec` or `vault_entry_inject_env` instead.

### `vault_exec`
Execute a shell command with a vault secret injected as an environment variable — the secret is never exposed in chat or logs.

```
vault_exec(entry_id: "abc123", purpose: "publish package", command: "npm publish --access public")
```

**Two tiers:**
- **Tier 1** (standard): runs immediately
- **Tier 2** (restricted): Tier 2 access is controlled server-side — the user enables it from the wundervault.com dashboard

Shell escape sequences (`$()`, backticks, `bash -c`, `eval`) and file-writing redirects (`>`, `>>`, `tee`) are hard-blocked before the secret is decrypted. To put a secret into a file, use `vault_entry_inject_env` — do not redirect it with the shell. (These blocks are a guardrail, not a sandbox; the real protection is that plaintext is never returned to you.)

**Remote execution via SSH:** Pass `remote_host` to run the command on a remote machine. The secret is injected inside the remote shell via SSH stdin — no `AcceptEnv`/`SendEnv` config required on the remote host. Use `ssh_key_entry_id` to load the SSH key from the vault itself.

```
vault_exec(
  entry_id: "abc123",
  purpose: "check subscribers on prod",
  command: "curl -s -u \"admin:$DB_PASSWORD\" http://localhost:9000/api/subscribers",
  inject_as: { env_key: "DB_PASSWORD" },
  remote_host: { host: "192.168.1.50", user: "opc", ssh_key_entry_id: "ssh-key-entry-id" }
)
```

**Remote command with only an SSH key (no secret injected):** `entry_id` is optional. To run a command on a remote host using just a vaulted SSH key — without injecting any secret as an env var — omit `entry_id` and pass `remote_host.ssh_key_entry_id`.

```
vault_exec(
  purpose: "restart the service on prod",
  command: "sudo systemctl restart wundervault",
  remote_host: { host: "prod.example.com", user: "opc", ssh_key_entry_id: "ssh-key-entry-id" }
)
```

### `vault_entry_inject_env`
Write a secret directly into an environment file (`.env`) as an environment variable, without it passing through chat.

**Disabled by default.** To use this tool, enable it in Settings > Agent Capabilities at wundervault.com. You can disable it again at any time.

```
vault_entry_inject_env(
  entry_id: "abc123",
  purpose: "inject API key into app config",
  file_path: "/home/user/app/.env",
  env_key: "RESEND_API_KEY"
)
```

Note: `file_path` and `env_key` are the correct parameter names.

**Why you'd enable it:** Writing secrets directly to `.env` files is the standard way to configure apps, containers, and deploy pipelines. Without this tool, you'd need to paste secrets manually — exposing them in your terminal or chat history. `vault_entry_inject_env` lets agents wire up credentials automatically while keeping plaintext out of the conversation entirely.

**Risks to understand before enabling:**
- An agent can write a secret to any `.env` path it can reach — including paths outside your project directory
- If an agent is compromised or acting on a malicious prompt, it could inject credentials into unexpected locations
- Written secrets are no longer burn-on-read — they persist on disk in the target file
- File permissions on the `.env` are your responsibility; the tool writes the value but does not set restrictive permissions automatically

### `vault_rsync`
Sync a local directory to a remote host via rsync over SSH, with the SSH key fetched from the vault. The key is written to a temp file for the transfer duration and deleted immediately after.

```
vault_rsync(
  ssh_key_entry_id: "ssh-key-entry-id",
  purpose: "deploy static files to prod",
  local_path: "/home/user/app/dist/",
  remote_user: "opc",
  remote_host: "prod.example.com",
  remote_path: "/var/www/html"
)
```

### `vault_entry_forget`
Discard a vault entry reference from context. Does not delete the vault entry.

```
vault_entry_forget(entry_id: "abc123")
→ ✔️ Reference discarded.
```

## Common Patterns

**Run a command with a secret (Tier 1):**
```
1. vault_entries_list() → find entry ID for the secret you need
2. vault_exec(entry_id: "abc123", purpose: "...", command: "...")
```

**Run a command with a Tier 2 entry (deploy, publish, infrastructure change):**
```
1. vault_entries_list() → find entry ID
2. vault_exec(entry_id: "abc123", purpose: "...", command: "...")
```
Note: Tier 2 entries require the user to enable access from the wundervault.com dashboard before use.

**Write a secret to a config file:**
```
1. vault_entries_list() → find entry ID
2. vault_entry_inject_env(entry_id: "abc123", purpose: "...", file_path: "/app/.env", env_key: "MY_KEY")
```

**Deploy files to a remote server:**
```
1. vault_entries_list() → find SSH key entry ID
2. vault_rsync(ssh_key_entry_id: "...", local_path: "./dist/", remote_user: "opc", remote_host: "prod.example.com", remote_path: "/var/www/html")
```


## Multi-Agent Setup

Wundervault is designed for multi-agent environments. Each agent gets its own scoped identity and token — they are fully isolated from each other at the daemon level.

- Each agent authenticates with its own token file (`~/.wundervault/agents/{AgentName}.token`)
- Agents can only access entries they have been explicitly granted
- The vault owner controls which agents exist and what they can reach from the wundervault.com dashboard
- Agents cannot see each other's tokens, identities, or access scopes
- Audit logs are per-agent, so you can trace exactly which agent accessed which secret and when

This makes Wundervault suitable for setups where multiple specialized agents (a coding agent, a deploy agent, a partner agent, etc.) share infrastructure but must not share credentials.

## Security Notes

- Secrets are end-to-end encrypted; plaintext is never returned to the agent
- The onboarding script verifies its own ed25519 signature on startup and exits if the check fails. Pipe mode (`curl ... | python3`) is hard-blocked — the script detects it and refuses to run. Pinned version, SHA-256 checksum, and public key are at [wundervault.com/install](https://wundervault.com/install).
- Agents never hold credentials directly — only a scoped token is stored locally. The local daemon manages the actual credentials and exposes them only through its controlled interface, enforcing tier checks and audit logging on every request. Compromise of an agent token does not grant direct access to vault credentials.
- `vault_exec` and `vault_rsync` are the correct tools for using secrets — not `vault_entry_get`
- Tier 2 entries are configured by the vault owner; agents cannot escalate a Tier 1 entry
- Tier 2 access is enabled server-side by the user via the wundervault.com dashboard
- The `inject_as` override lets you specify which env var name receives the secret if the vault entry has no exec_config set

## More Info

- npm: `@wundervault/mcp-server`
- Vault UI: [wundervault.com](https://wundervault.com)
