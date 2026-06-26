# UKC API Reference

## Environment variables

| Var | Purpose |
|-----|---------|
| `UKC_TOKEN` | Bearer auth token |
| `UKC_METRO` | Base URL, e.g. `https://api.unikraft.io/v1/metro/fra0` |
| `UKC_USER` | Username / org identifier |
| `UKC_SANDBOX_IMAGE` | Image to use for sandbox instances |

---

## Exec API (on the sandbox)

**Endpoint:** `POST https://<fqdn>/exec`

**Request:**
```json
{ "cmd": "echo hello" }
```
Commands run via `sh -lc <cmd>` (login shell).

**Response 200:**
```json
{ "stdout": "hello\n", "stderr": "", "code": 0 }
```

**Error responses:**

| Status | Body |
|--------|------|
| 400 | `{"error": "invalid json"}` or `{"error": "\"cmd\" must be a string"}` |
| 404 | `{"error": "not found"}` — wrong path/method |
| 500 | `{"error": "<spawn error message>"}` |

---

## SSH access

- **Port:** `2222` (TLS-wrapped — raw TCP will be refused)
- **User:** `root`
- **Key:** `/tmp/<sandbox-name>/id_ed25519` (written by `create-sandbox.sh`)
- Used by the rsync scripts for file sync
- Requires `ProxyCommand="openssl s_client -quiet -connect <fqdn>:2222 2>/dev/null"` to tunnel through TLS
