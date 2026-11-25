# Domain & SSL Configuration

Configuring custom domains and SSL/TLS certificates for strut stacks.

> The `sudo` commands below run **on the VPS** (via `strut <stack> shell` or `exec`) and change certificates or firewall state. Show the exact command to the user and wait for their go-ahead before running any of them. The read-only ones (`journalctl`, `ls`, `ufw status`, `certbot renew --dry-run`) are safe to run to diagnose.

## Quick Reference

```bash
# Configure domain with SSL (recommended)
strut my-stack domain example.com admin@example.com --env prod

# HTTP only (no SSL)
strut my-stack domain example.com admin@example.com --skip-ssl --env prod
```

## Prerequisites

### 1. DNS A Record

Point the domain at your VPS IP:

```
api.example.com  A  <VPS_IP>  TTL=300
```

Verify: `dig +short api.example.com` should return the VPS IP.

### 2. Firewall — Ports 80 + 443

Your cloud provider's firewall must allow inbound TCP on 80 and 443. (Most common cause of cert failures.)

### 3. Stack Deployed with nginx Running

```bash
strut my-stack deploy --env prod
strut my-stack status --env prod    # confirm nginx is up
```

## What the `domain` Command Does

1. Validates DNS resolves to the correct IP.
2. Generates a production nginx reverse-proxy config.
3. Obtains a Let's Encrypt certificate via certbot (webroot validation).
4. Configures HTTPS with an HTTP→HTTPS redirect.
5. Adds security headers (HSTS, X-Frame-Options, etc.).
6. Sets up an auto-renewal cron.

## Certificate Details

- Provider: Let's Encrypt (90-day validity, auto-renewed when <30 days remain).
- Method: webroot validation (no downtime).
- TLS 1.2 and 1.3 only, strong ciphers.

```bash
sudo certbot renew --dry-run    # test renewal
```

## Multiple Domains

Run the `domain` command once per domain:

```bash
strut my-stack domain api.example.com admin@example.com --env prod
strut my-stack domain app.example.com admin@example.com --env prod
```

## Wildcard Certificates

The automated flow uses webroot (no wildcard support). For wildcards, use DNS validation manually:

```bash
sudo certbot certonly --manual --preferred-challenges dns -d "*.example.com"
# then copy certs into the nginx volume
```

## Troubleshooting

### DNS not resolving

```bash
dig +short example.com    # empty → wait for propagation (5-60 min) or fix DNS
```

### Port 80/443 not accessible

```bash
curl -I http://example.com    # test from outside the VPS
sudo ufw status               # check VPS firewall
docker ps | grep nginx        # nginx running?
```

### Certificate obtainment failed

```bash
sudo journalctl -u certbot
# Common causes: port 80 blocked by cloud firewall, wrong DNS, or LE rate limit
```

### HTTPS not working after setup

```bash
strut my-stack logs nginx --follow --env prod
sudo ls -la /etc/letsencrypt/live/example.com/
strut my-stack exec "docker compose exec nginx nginx -t" --env prod
strut my-stack exec "docker compose exec nginx nginx -s reload" --env prod
```

Test your config at https://www.ssllabs.com/ssltest/.

## Security Features (Auto-Configured)

- HSTS (1 year, includeSubDomains)
- TLS 1.2+ only, no weak ciphers
- X-Frame-Options, X-Content-Type-Options headers
- HTTP→HTTPS redirect for all traffic
