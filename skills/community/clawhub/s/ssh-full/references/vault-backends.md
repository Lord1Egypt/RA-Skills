# Vault Backend Integration

This skill supports **any** credential vault via the `VAULT_RESOLVER_BIN` environment variable. The backend must accept a JSON request on stdin and return a JSON response on stdout.

## API Contract

### Input (stdin)
```json
{
  "ids": ["item-name/field-name", ...]
}
```

### Output (stdout)
```json
{
  "values": {
    "item-name/field-name": "<base64-encoded value>",
    ...
  }
}
```

### Exit codes
- `0`: success
- Non-zero: failure (skill will handle gracefully)

## Built-in Backends

### vault-resolver (Hermes Agent default)

Zero-config on Hermes Agent. Wraps Vaultwarden's API directly.

```bash
# Auto-detected — no setup needed
ssh-run.sh --host my-server --vault-key my-key -- 'uptime'
```

Key naming convention: `ssh-<name>/ssh_private_key` (base64), `ssh-<name>/ssh_password` (plain text), `sudo-<name>/sudo_password` (plain text).

## Custom Backend Wrappers

### Bitwarden CLI (`bw`)

```bash
export VAULT_RESOLVER_BIN="bw"

# Requires bw CLI + session:
bw login
export BW_SESSION=$(bw unlock --raw)
```

The skill calls `bw` directly — ensure your items follow the naming convention or adapt with a wrapper.

### 1Password CLI (`op`)

```bash
export VAULT_RESOLVER_BIN="op"

# Requires op CLI + signin:
op signin
```

### HashiCorp Vault

```bash
# Wrapper script at /usr/local/bin/vault-wrapper:
cat > /usr/local/bin/vault-wrapper << 'SCRIPT'
#!/usr/bin/env bash
# Reads JSON from stdin, resolves vault paths, outputs JSON to stdout
python3 - << 'PY'
import json, subprocess, sys, os

req = json.load(sys.stdin)
result = {"values": {}}

for id_str in req.get("ids", []):
    # Map ssh-executor naming to Vault paths
    # ssh-mykey/ssh_private_key → secret/ssh/mykey
    parts = id_str.split("/")
    item, field = parts[0], parts[1]
    
    # Remove prefix
    if item.startswith("ssh-"):
        name = item[4:]
        vault_path = f"secret/ssh/{name}"
    elif item.startswith("sudo-"):
        name = item[5:]
        vault_path = f"secret/sudo/{name}"
    else:
        vault_path = f"secret/{item}"
    
    try:
        p = subprocess.run(
            ["vault", "kv", "get", "-field=" + field, vault_path],
            capture_output=True, text=True, timeout=10
        )
        if p.returncode == 0:
            result["values"][id_str] = p.stdout.strip()
    except Exception:
        pass

print(json.dumps(result))
PY
SCRIPT
chmod +x /usr/local/bin/vault-wrapper

export VAULT_RESOLVER_BIN="/usr/local/bin/vault-wrapper"
```

## No Vault (Key Files Only)

If you don't use a vault, skip `--vault-key` entirely:

```bash
# Direct key file
ssh-run.sh --host my-server --user ubuntu --key ~/.ssh/id_rsa -- 'uptime'

# Environment variable
# ⚠️  WARNING: env vars can leak via shell history, /proc, crash reports, and child processes.
#    Prefer vault-based auth (--ssh-pass-vault) for production. Use env vars only in ephemeral CI.
SSH_PASS="<your-password>" ssh-run.sh --host my-server --user ubuntu -- 'uptime'

# Interactive prompt
ssh-run.sh --host my-server --user ubuntu --ssh-pass-ask -- 'uptime'
# → LLM will ask the user, then retry with SSH_PASS
```

## Testing Your Backend

```bash
# Test that your backend works:
echo '{"ids": ["ssh-test/ssh_private_key"]}' | $VAULT_RESOLVER_BIN resolve

# Expected output: {"values": {"ssh-test/ssh_private_key": "<base64>"}}
```
