# Recover: Re-issue the Certificate

Applies when the app has a domain and its certificate is expired, near expiry, or the HTTPS
handshake fails. Re-issuing reuses the `qwencloud-deploy` HTTPS flow (DNS-01 via Cloud Assistant).

## Confirmation gate

- Target: certificate for `<domain>` on ECS `<ecs-id>` in `<region>`.
- Action: re-issue via certbot (DNS-01), then reload Nginx.
- Interruption: none for issuance; Nginx reload is near-zero.
- Version change: none (app code unchanged).
- New cost: none.
- Verification: `curl -sI https://<domain>/` returns 2xx/3xx and the new expiry is ~90 days out.
- If it fails: report the failing step and stop; the old cert stays in place until replaced.

Decline → change nothing.

## Execute (reuse the deploy HTTPS flow)

Run steps 2–5 of `qwencloud-deploy` HTTPS setup (`deploy/reference/https/https_setup.md`): launch
certbot with the self-polling DNS-01 auth-hook, create the `_acme-challenge` TXT, configure/reload
Nginx, then clean up the TXT. Idempotent — certbot skips when the cert is still valid > 7 days.

## Verify

```bash
curl -sI https://<domain>/ | head -1
openssl x509 -enddate -noout -in /etc/qwencloud/certbot/config/live/<domain>/fullchain.pem
```

Then update `.qwencloud-deploy` (`outputs.domain` / `outputs.cert_path`) and record the audit
entry (`workflow.md`). Redact tokens from any evidence.
