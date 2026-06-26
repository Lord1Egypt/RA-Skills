# Vault Auth Methods

## Token (default)

Already set up during `vault.js setup`. Token stored in `~/.openclaw/vault.json`.

Renew before expiry:
```bash
node vault.js token-renew
```

---

## AppRole

Better for services — role_id is non-secret, secret_id is short-lived.

**Get a token via AppRole:**
```bash
curl -s -X POST https://vault.example.com:8200/v1/auth/approle/login \
  -d '{"role_id":"<role_id>","secret_id":"<secret_id>"}' | \
  node -e "const d=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')); console.log(d.auth.client_token)"
```

Then update config:
```json
{ "auth": { "method": "token", "token": "hvs.xxx-from-approle" } }
```

---

## Kubernetes

For pods running on OVH/lab — authenticates via the pod's service account JWT.

```bash
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
curl -s -X POST https://vault.example.com:8200/v1/auth/kubernetes/login \
  -d "{\"role\":\"my-role\",\"jwt\":\"$TOKEN\"}" | \
  node -e "const d=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')); console.log(d.auth.client_token)"
```

Requires Vault Kubernetes auth backend to be configured with the cluster's CA and API server.

---

## Rotating a token

1. Create a new token in Vault UI or via API
2. Run `vault.js setup` and paste the new token (existing address/mount kept)
3. Old token can be revoked: `curl -X POST -H "X-Vault-Token: <old>" https://.../v1/auth/token/revoke-self`
