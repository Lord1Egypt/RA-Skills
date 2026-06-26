# Custom Domains for Cloudflare Workers

## Prerequisites

- Domain must be added to your Cloudflare account (nameservers pointing to CF)
- Domain must be proxied (orange cloud icon in DNS settings)
- `CLOUDFLARE_API_TOKEN` with DNS and Workers permissions

## Method 1: Custom Domains API (Recommended)

The `setup-domain.sh` script automates this. Under the hood it uses the Workers Custom Domains API:

```bash
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/domains" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "app.example.com",
    "zone_id": "{zone_id}",
    "service": "my-worker",
    "environment": "production"
  }'
```

This method:
- Automatically creates the required DNS records
- Handles SSL certificate provisioning
- Sets up the route from domain to worker
- Works for apex domains and subdomains

## Method 2: Routes in wrangler.toml

Add routes directly in your wrangler config. Requires the zone ID.

```toml
# Single route
[[routes]]
pattern = "example.com/*"
zone_id = "your-zone-id-here"

# Subdomain
[[routes]]
pattern = "app.example.com/*"
zone_id = "your-zone-id-here"

# Multiple routes
[[routes]]
pattern = "example.com/*"
zone_id = "abc123"

[[routes]]
pattern = "www.example.com/*"
zone_id = "abc123"
```

**Finding your zone ID**: Dashboard → select domain → Overview → right sidebar → Zone ID.

**Important**: You still need a DNS record pointing to the domain. Create a proxied A record to `192.0.2.1` (dummy IP, CF intercepts it) or a proxied AAAA record to `100::`.

```bash
# Create DNS record via API
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "A",
    "name": "app.example.com",
    "content": "192.0.2.1",
    "proxied": true
  }'
```

## Method 3: Cloudflare Dashboard

1. Go to Workers & Pages → your worker
2. Click Settings → Domains & Routes
3. Click "Add Custom Domain"
4. Enter your domain (e.g., `app.example.com`)
5. CF creates DNS records and provisions SSL automatically

## DNS Record Types

| Scenario | Record Type | Name | Content | Proxied |
|----------|------------|------|---------|---------|
| Apex domain | A | `@` | `192.0.2.1` | Yes (orange) |
| Subdomain | CNAME | `app` | `your-worker.your-subdomain.workers.dev` | Yes (orange) |
| Alternative | AAAA | `@` or subdomain | `100::` | Yes (orange) |

**Key point**: The actual IP/target doesn't matter for proxied records — Cloudflare intercepts the traffic and routes it to your worker. The `192.0.2.1` address is a documentation-reserved IP used as a dummy target.

## SSL / TLS

- **Automatic**: Cloudflare provisions and renews SSL certificates automatically
- **No action needed**: When you add a custom domain, SSL is handled
- **Verification**: Takes 1-15 minutes for certificate issuance
- **Check status**: Dashboard → SSL/TLS → Edge Certificates

### SSL Modes

Set the SSL mode in Dashboard → SSL/TLS:

| Mode | Description |
|------|-------------|
| **Full (strict)** | Recommended. End-to-end encryption with validated certificate |
| **Full** | End-to-end encryption, doesn't validate origin cert |
| **Flexible** | Encrypts browser→CF only. Avoid for Workers (no origin server) |

For Workers, **Full (strict)** is recommended since CF handles both sides.

## Subdomains

```bash
# Root domain
bash scripts/setup-domain.sh my-worker example.com

# Subdomain
bash scripts/setup-domain.sh my-worker app.example.com

# Wildcard (requires Enterprise or Advanced Certificate Manager)
# Not available via Workers Custom Domains — use routes instead
```

## Multiple Domains

A single worker can serve multiple domains:

```toml
[[routes]]
pattern = "example.com/*"
zone_id = "zone1"

[[routes]]
pattern = "example.org/*"
zone_id = "zone2"
```

In your worker code, use `request.url` or the `Host` header to serve different content per domain.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| DNS_PROBE_FINISHED_NXDOMAIN | DNS not propagated | Wait 1-5 min, check DNS with `dig` |
| SSL pending | Certificate provisioning | Wait up to 15 min, check Dashboard → SSL |
| ERR_TOO_MANY_REDIRECTS | Redirect loop | Set SSL mode to "Full (strict)" |
| 522 Connection timed out | Domain not proxied | Enable orange cloud in DNS settings |
| 1000 DNS points to prohibited IP | Bad DNS record | Use `192.0.2.1` (A) or `100::` (AAAA) |
| Custom domain conflict | Already assigned | Remove from previous worker first |

## Removing a Custom Domain

```bash
# Via API
curl -X DELETE "https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/domains/{domain_id}" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

Or via Dashboard: Workers → your worker → Settings → Domains & Routes → Remove.
