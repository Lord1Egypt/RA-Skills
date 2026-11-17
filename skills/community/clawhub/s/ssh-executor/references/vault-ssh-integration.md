# Vaultwarden + SSH Agent Integration

## Why

Private keys are the most sensitive credential for SSH. Keeping them in files on disk is
convenient but risky — any process or compromise on the host has access. Moving keys to
Vaultwarden and loading them into the in-memory SSH agent on demand:

- **Encryption at rest:** Keys are AES-256-CBC + HMAC encrypted in Vaultwarden.
- **No persistent key files:** The private key is decoded to a temp file, loaded into the
  agent, and immediately wiped. No key material lingers on disk.
- **Controlled access:** OpenClaw's vault-resolver authenticates via API key + master
  password. SSH never sees vault credentials.
- **Audit trail:** Every key retrieval is logged to `vault-audit.jsonl` with timestamp.

## Architecture

```
┌──────────────┐     vault-resolver      ┌──────────────┐
│  Vaultwarden  │ ◄───────stdin/stdout─── │  ssh-keys.sh  │
│  (encrypted)  │                         │  (retrieve)   │
└──────────────┘                         └──────┬───────┘
                                                 │
                                          tempfile (wiped)
                                                 │
                                          ┌──────▼───────┐
                                          │  ssh-agent    │
                                          │  (in-memory)   │
                                          └──────┬───────┘
                                                 │
                                          ┌──────▼───────┐
                                          │  ssh-run.sh   │
                                          │  (exec cmd)   │
                                          └──────────────┘
```

## Key lifecycle

### 1. First-time store

```bash
# Start with a local private key
ssh-keys.sh store prod-server ~/.ssh/id_rsa_prod
```

This base64-encodes the file and writes it to Vaultwarden as item `ssh-prod-server`
with fields `ssh_private_key` (base64) and `ssh_public_key` (base64, if `.pub` exists).

**After storing, you can safely delete the local file:**
```bash
rm ~/.ssh/id_rsa_prod ~/.ssh/id_rsa_prod.pub
```

### 2. Restore on demand

```bash
ssh-keys.sh restore prod-server
```

This:
1. Retrieves the base64 blob from Vaultwarden
2. Decodes to a temp file (`chmod 600`, auto-cleaned)
3. Validates it's a real SSH key (`ssh-keygen -l`)
4. Loads it into the SSH agent via `ssh-add`
5. Wipes the temp file

The key stays in the agent until the agent process terminates or you run `ssh-add -D`.

### 3. Use with ssh-run.sh

```bash
scripts/ssh-run.sh --host my-server --vault-key prod-server -- 'hostname && uptime'
```

The `--vault-key` flag automatically calls `ssh-keys.sh restore` before connecting.

### 4. See what's loaded

```bash
scripts/ssh-keys.sh agent-status
```

## Security considerations

- **The SSH agent stays running** for the container's lifetime. This means the key is
  usable for the duration of the session. If you need to cycle keys between connections
  or shut down the agent after use, add `ssh-add -D` to your cleanup.
- **Multiple keys:** The agent can hold multiple keys simultaneously. Keys are matched
  by the server's `~/.ssh/authorized_keys` or by SSH config's `IdentityFile` directive.
- **Vault credentials vs SSH credentials:** vault-resolver authenticates to Vaultwarden
  independently. SSH never receives or uses vault credentials. This separation means
  that even a compromised SSH server cannot leak vault access.
- **No key material in logs:** The `ssh-run.sh` output intentionally omits key paths,
  and `ssh-keys.sh` never prints decoded key content.
- **Who can access:** vault-resolver is protected by caller token authentication within
  the container. Only processes with the correct `VAULT_CALLER_TOKEN` can resolve secrets.

## SSH config integration

You can combine vault keys with SSH config to get per-host key resolution:

```ssh-config
Host prod-*
  User deploy
  IdentityFile ~/.ssh/id_placeholder  # Agent will provide the actual key
  IdentityAgent $SSH_AUTH_SOCK
```

Instead of identity files, `--vault-key` injects the key into the agent, and SSH's
agent forwarding picks it up during key exchange.

## Complete workflow example

```bash
# 1. Store the key once
ssh-keys.sh store prod-app ~/.ssh/id_ed25519_prod

# 2. Remove local copy (optional but recommended)
rm ~/.ssh/id_ed25519_prod ~/.ssh/id_ed25519_prod.pub

# 3. Connect and run commands
ssh-run.sh --host prod-app --vault-key prod-app -- 'df -h'
ssh-run.sh --host prod-app --vault-key prod-app --confirm-dangerous -- \
  'journalctl -u myapp -n 50 --no-pager'

# 4. Check agent state
ssh-keys.sh agent-status
```
