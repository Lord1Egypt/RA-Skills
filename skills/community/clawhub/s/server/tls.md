# TLS Termination — Wiring, Reload, and Expiry

Where HTTPS is terminated, how the serving process picks up a new certificate, and how expiry stops being a surprise. Obtaining certificates, ACME challenge types, and chain debugging belong to the `ssl` skill; this file is the server side of the same story.

**Before touching a certificate**, read `~/Clawic/data/domains/domains.md` for what already exists — registrar expiry, certificate expiry, who issues it — and `## Due` in `~/Clawic/data/server/memory.md` for when it was last checked. Issuing a second certificate for a name that already has one burns rate limit and leaves two renewal timers fighting.

**Contents:** [Terminate Once](#terminate-once) · [The Reload Hook Is the Whole Job](#the-reload-hook-is-the-whole-job) · [Verify the Served Certificate](#verify-the-served-certificate) · [Expiry Is a Cadence](#expiry-is-a-cadence) · [File Layout and Permissions](#file-layout-and-permissions) · [Configuration Worth Setting](#configuration-worth-setting) · [HSTS](#hsts) · [Wildcards and SANs](#wildcards-and-sans) · [Internal and Machine-to-Machine TLS](#internal-and-machine-to-machine-tls) · [mTLS](#mtls) · [Renewal Failure Modes](#renewal-failure-modes) · [Write It Down](#write-it-down)

## Terminate Once

Every hop that terminates TLS is a hop that holds a private key and can misconfigure a cipher. Pick one:

| Topology | Where the key lives | Note |
|---|---|---|
| CDN → origin over TLS ("full strict") | CDN and origin | The origin certificate can be a long-lived one issued by the CDN; the public one is the CDN's problem |
| CDN → origin plaintext | CDN only | Only acceptable when the origin is unreachable from the internet; otherwise the "HTTPS site" serves plaintext to anyone who finds the IP |
| Proxy on the box | The box | The default for a self-managed server; automatic ACME makes it unattended |
| App terminates directly | The app process | Only for a single Go/Rust binary with no proxy; you lose the reload story and the shared cert cache |

TLS between proxy and a local upstream on loopback buys nothing and costs a handshake per connection. Across machines on a shared network, it buys real protection — and needs the upstream's certificate to be verifiable, not `insecure_skip_verify`, which is TLS theatre.

## The Reload Hook Is the Whole Job

Renewal writes a new file. The running process still holds the old certificate in memory and will serve it until it is told otherwise — for the remaining days of validity, and then past expiry.

```
# certbot: runs only when a renewal actually happened
certbot renew --deploy-hook "systemctl reload nginx"
```

- The hook belongs to the **renewal**, not to a separate cron line, so it fires exactly when there is something new to load and never otherwise.
- `--deploy-hook` runs after a successful renewal; `--post-hook` runs after every attempt. Use deploy for reloads.
- With `--standalone` you also need `--pre-hook`/`--post-hook` to stop and start the proxy around port 80 — `--webroot` or a proxy-native ACME integration avoids the downtime entirely.
- Caddy and Traefik renew and reload internally; there is no hook to write and no cron to forget. That is the strongest practical argument for them (`stack.md`).
- A certificate consumed by more than one process (proxy plus a mail or database service) needs each one reloaded in the hook. The one nobody remembers is the one that breaks.
- Test the whole path with a dry run before trusting it: `certbot renew --dry-run` exercises issuance and hooks against the staging environment.

## Verify the Served Certificate

The file on disk is not evidence. Ask the running server:

```
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer
```

`-servername` is mandatory on any box serving more than one site: without SNI you get the default vhost's certificate and conclude the wrong thing. Compare the `notAfter` from the wire with the file's — a difference of days is a missing reload, and it is the single most common TLS incident on a self-managed server.

Check the chain too: `openssl s_client -showcerts` should present the leaf plus intermediates. Browsers often paper over a missing intermediate using cached issuers, so "works in my browser, fails in curl and on Android" is a chain problem, not a client problem — serve `fullchain.pem`, never `cert.pem`.

## Expiry Is a Cadence

- Let's Encrypt certificates last 90 days and renew at 30 days remaining; automation retries daily, so a renewal has a month of failed attempts before anyone is inconvenienced — which is exactly why nobody notices it failing.
- Expiry notification emails are no longer something to rely on. The check has to be yours: a monthly sweep entry in `## Due` that reads the *served* expiry for every hostname in `domains.md`, not the files on disk.
- Track the **registrar expiry separately** from the certificate expiry. They fail identically from the outside and only one of them has a renewal daemon.
- Rate limits punish retry loops: repeated identical requests hit a duplicate-certificate limit, and repeated failed validations hit their own. Use the staging environment while fixing anything, and verify current limits at the issuer before a bulk migration.

## File Layout and Permissions

| File | Contents | Mode |
|---|---|---|
| `fullchain.pem` | Leaf + intermediates — this is what the proxy serves | 0644 |
| `privkey.pem` | Private key | 0600, owned by root; the proxy reads it as root at startup and drops privileges |
| `chain.pem` | Intermediates only — for OCSP stapling in older configs | 0644 |
| `cert.pem` | Leaf only — serving this is the missing-chain bug | — |

certbot's `live/` paths are symlinks into `archive/`; reference the `live/` path in config so renewal is transparent, and never copy the file elsewhere — a copied certificate is a certificate that stops renewing.

A private key never leaves the box, never goes into a repository, never goes into `~/Clawic/data/`. What gets written there is the path and the expiry (`memory-template.md`).

## Configuration Worth Setting

- **Protocols**: TLS 1.2 and 1.3 only. TLS 1.0/1.1 are deprecated and their presence is an audit finding, not a compatibility win.
- **Ciphers**: take the current recommended set from a maintained generator rather than a hand-written list — a copied cipher string from a blog post ages into a vulnerability.
- **`ssl_session_cache shared:SSL:10m`** (nginx): roughly 40,000 sessions; resumption removes a full handshake for returning visitors.
- **OCSP stapling**: `ssl_stapling on` with a resolver, or let an automatic proxy handle it. Without stapling the client makes its own OCSP call and a slow responder becomes your latency.
- **`ssl_prefer_server_ciphers off`** with TLS 1.3 — client preference is the modern default.
- Redirect HTTP to HTTPS with a 301 on a dedicated `listen 80` server block that also leaves `/.well-known/acme-challenge/` reachable, or HTTP-01 renewal breaks the moment the redirect is added.

## HSTS

`Strict-Transport-Security: max-age=31536000; includeSubDomains` tells browsers to refuse plaintext for a year. It is the right default *after* HTTPS works everywhere, and it is close to irreversible: a browser that saw the header keeps enforcing it until the max-age expires, whatever you serve afterwards.

Order of operations: ship HTTPS, verify every subdomain (including the ones you forgot — internal tools, staging, an old mail interface), then a short `max-age=300`, then raise it. `preload` is a separate, slower-to-undo commitment: submission is quick, removal takes months of browser release cycles.

## Wildcards and SANs

- A wildcard (`*.example.com`) requires DNS-01 validation, which means the issuing process holds a DNS provider API token. That token is a secret: it lives in the environment or a credential file with tight permissions, referenced as `env:CF_API_TOKEN` in anything written down.
- `*.example.com` does **not** cover `example.com` itself, and does not cover `a.b.example.com` — one level only. Both are routine outages after a migration.
- SAN certificates (several explicit names on one certificate) are simpler to reason about for a handful of hosts and avoid the DNS token entirely. Prefer them below roughly ten names.
- One certificate covering every site on the box means one renewal failure takes down every site. Per-site certificates fail independently, which is worth the extra renewals.

## Internal and Machine-to-Machine TLS

For service-to-service traffic on a private network, a private CA (or the platform's built-in issuer) beats public certificates: no rate limits, no public DNS requirement, and the trust store is yours. The cost is distributing the CA bundle to every client and rotating it — which is real work, so only take it on when the network is genuinely untrusted or a compliance regime requires it.

Never disable verification to make it work. `insecure_skip_verify`, `curl -k`, and `verify=False` turn TLS into obfuscation, and they are permanent: nobody comes back to remove them.

## mTLS

Client certificates verify at the terminating hop and nowhere else. If TLS terminates at a CDN, mTLS has to be configured *there* — forwarding the client certificate as a header downstream carries a claim, not proof, and that header must then be stripped from untrusted input at the edge or anyone can forge an identity.

On nginx: `ssl_client_certificate <ca.pem>; ssl_verify_client on;` and pass `$ssl_client_s_dn` to the app. Revocation needs a CRL or OCSP that is actually maintained — an mTLS setup without a revocation story cannot remove a compromised client.

## Renewal Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| Renewed on disk, browser sees old | No reload hook | Deploy hook that reloads every consumer |
| Renewal fails, HTTP-01 | The HTTPS redirect swallows `/.well-known/acme-challenge/`, or port 80 is closed | Exempt the challenge path before the redirect; keep 80 open |
| Renewal fails, DNS-01 | Provider token expired or rotated | Re-issue the token; store the pointer, never the value |
| Works for the apex, fails for a subdomain | The subdomain is not in the certificate, or its DNS points elsewhere | Check the SAN list against `domains.md` |
| Certificate valid, browser still warns | Missing intermediate — serving `cert.pem` instead of `fullchain.pem` | Serve the full chain and re-verify from the wire |
| Renewal succeeded but the site is down | Reload ran against a config with an unrelated syntax error | Validate config in the hook before reloading (`nginx -t && systemctl reload nginx`) |
| Everything expires on the same day | One certificate for every site | Split per site; stagger issuance |

## Write It Down

After wiring or renewing: update the certificate columns of `~/Clawic/data/domains/domains.md` (issuer, expiry, where it terminates), the vhost column of `## Services`, and the expiry sweep row in `## Due` (`memory-template.md`). A certificate incident — expired, wrong chain, missing reload — goes to `incidents/<year>.md` with the *real* cause; the second entry with the same cause means the runbook belongs in `artifacts/`. Never write key material, ACME account keys, or DNS provider tokens: pointers only (`env:CF_API_TOKEN`, `file:/etc/letsencrypt/live/example.com/privkey.pem`).
