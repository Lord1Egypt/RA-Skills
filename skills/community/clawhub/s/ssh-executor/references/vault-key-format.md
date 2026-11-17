# SSH Key Format in Vaultwarden

## Expected Format

The `ssh-keys.sh` script expects SSH keys stored as **custom fields**, not in the notes field.

| Field | Content | Format |
|-------|---------|--------|
| `ssh_private_key` | Private key | base64-encoded |
| `ssh_public_key` | Public key (optional) | base64-encoded |

## How Keys Should Be Stored

Always use `ssh-keys.sh store <name> <path>` to store a key:

```bash
ssh-keys.sh store prod-server ~/.ssh/id_ed25519_prod
```

This creates a vault item named `ssh-prod-server` with proper fields:
- `ssh_private_key` (base64 of the private key)
- `ssh_public_key` (base64 of the .pub file, if exists)

## When Keys Are in Notes

If a key was stored manually (e.g., via Vaultwarden UI, pasted into Secure Notes),
it won't be found by `ssh-keys.sh restore`. Two options:

1. **Re-store properly** (recommended):
   ```bash
   # ⚠️  WARNING: Writing private key to disk — use /dev/shm (RAM-backed)
   #    to avoid persistence on physical storage. Verify cleanup after.
   vault-resolver get ssh-id-rsa/notes > /dev/shm/key
   chmod 600 /dev/shm/key
   # Re-store in correct format (key loaded into vault, never exposed in chat)
   ssh-keys.sh store id-rsa /dev/shm/key
   shred -u /dev/shm/key
   ```

2. **Resolve via notes fallback** (if vault-resolver has the patch):
   ```bash
   vault-resolver get ssh-id-rsa/notes
   ```

## Resolution Flow

When `ssh-run.sh --vault-key <name>` is called:

1. `ssh-run-native.sh` → `ssh-keys.sh restore <name>`
2. `ssh-keys.sh` calls `vault-resolver resolve` with key `ssh-<name>/ssh_private_key`
3. vault-resolver looks for a custom field named `ssh_private_key`
4. If not found and fallback is active, checks other fields then `notes`

## Troubleshooting

If restore says "not found":
```bash
# List all vault items matching ssh
vault-resolver resolve  # with JSON: {"ids":["ssh-*/ssh_private_key"]}

# Check what fields the item actually has
# Use vault-resolver get with field name known to exist
```
