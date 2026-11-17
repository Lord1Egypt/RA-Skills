# Hardening a Live Service

Reducing what an attacker reaches after the first thing goes wrong. Machine-level hardening — SSH, firewall policy, users, kernel — belongs to `vps` and `linux`; this file is the service that listens.

**Before a hardening pass**, read `## Services` in `~/Clawic/data/server/memory.md` (or `services.md` if `## Boxes` points there): the listen address column tells you in one look which services are reachable from outside, and that is the whole first half of this file.

**Contents:** [The Exposure Sweep](#the-exposure-sweep) · [Run As Nobody Useful](#run-as-nobody-useful) · [systemd Sandboxing](#systemd-sandboxing) · [Getting Secrets to a Process](#getting-secrets-to-a-process) · [The Docker Firewall Trap](#the-docker-firewall-trap) · [Security Headers](#security-headers) · [Abuse Controls](#abuse-controls) · [Admin Interfaces](#admin-interfaces) · [Dependency and Image Freshness](#dependency-and-image-freshness) · [If Something Leaked](#if-something-leaked) · [Baseline Checklist](#baseline-checklist) · [Write It Down](#write-it-down)

## The Exposure Sweep

Four commands, from the box, in this order. Most findings come from the first one.

1. `ss -tlnp` — every listener. Anything on `0.0.0.0` that is not the proxy is a finding: databases, admin UIs, metrics endpoints, message brokers, the app itself.
2. `iptables -S` / `nft list ruleset` — the rules actually in force, including the ones a container runtime inserted (below). `ufw status` is a summary of one tool's intentions, not the kernel's state.
3. From another machine: a port scan of the public IP. What answers from outside is the only exposure that counts, and it regularly differs from what the firewall config implies.
4. `find / -name '.env' -o -name '*.pem' -o -name 'id_*' 2>/dev/null` under the web roots — a secret inside a served directory is a download, not a secret (`static.md`).

An app bound to `0.0.0.0:8080` behind a proxy is reachable directly on 8080: TLS bypassed, forwarded-header trust bypassed, rate limits bypassed, and auth done at the proxy bypassed entirely. Bind loopback or a Unix socket (SKILL.md Rule 7).

## Run As Nobody Useful

- One dedicated system user per service, no login shell, no home directory it can write to except what it needs. Two services sharing a user means one compromise reads the other's environment and files.
- Never run the app as root to reach port 80. `AmbientCapabilities=CAP_NET_BIND_SERVICE` grants exactly that one ability, or — better — the proxy owns 80/443 and the app lives on a high port.
- The service user should not own its own code. Code owned by root and readable by the service user means a compromised process cannot rewrite the application it is running.
- Writable paths are enumerated, not assumed: uploads, cache, logs, a socket directory. Everything else read-only (below).
- `DynamicUser=yes` in systemd allocates a transient user with no persistent identity — excellent for stateless services, wrong for anything owning files across restarts.

## systemd Sandboxing

Cheap, and each line removes a class of post-compromise move:

```ini
NoNewPrivileges=yes
ProtectSystem=strict          # entire filesystem read-only...
ReadWritePaths=/srv/api/shared/uploads /run/api
ProtectHome=yes
PrivateTmp=yes                # its own /tmp; no cross-service tmp attacks
PrivateDevices=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
RestrictSUIDSGID=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes    # breaks JIT runtimes — omit for Node/JVM/PyPy
SystemCallFilter=@system-service
```

`systemd-analyze security <unit>` scores exposure from 0 to 10 and lists what is missing; going from the default (~9.5, "UNSAFE") to under 4 is usually a handful of lines and no behavior change. Add them incrementally and restart between: `ProtectSystem=strict` without the right `ReadWritePaths` fails at the first write, which is a five-minute fix, and `MemoryDenyWriteExecute` breaks any JIT, which is a confusing crash if you add ten directives at once.

Containers give a comparable boundary differently: `read_only: true`, `cap_drop: [ALL]`, `no-new-privileges:true`, a non-root `user:`, and tmpfs for scratch (`containers.md`).

## Getting Secrets to a Process

| Method | Verdict |
|---|---|
| Environment file, mode 0640, owned `root:<service>` | The workable default |
| `Environment=` in the unit | No — unit files are world-readable and values appear in `systemctl show` |
| Secret in the repository or the image | No, ever. It is now in every layer, every clone, every backup |
| Secret in a proxy config or a compose file committed to git | Same problem, one directory over |
| systemd `LoadCredential=` | Best available on a plain box: the value is a file readable only by that unit, never in the environment |
| A secret manager the user already runs | Best when it exists; the app fetches at startup and never persists |
| Mounted file the app reads at startup | Fine, and easier to rotate than an environment variable |

Environment variables are readable by the process's own user via `/proc/<pid>/environ` and can leak into crash reports, `ps` output for child processes, and debug endpoints. That is an argument for dedicated users and for files over environment, not for giving up.

Rotation is part of the design: a secret nobody can rotate without downtime never gets rotated. Support two valid values during a rotation window wherever the protocol allows it.

**Nothing under `~/Clawic/data/` ever receives a secret value** — not a `.env` the user pastes, not a connection string in a runbook, not a token in a "config that finally worked". The pointer goes where the value would be (`memory-template.md`).

## The Docker Firewall Trap

Publishing a container port writes rules into the runtime's own chain, which is evaluated **before** the ufw rules. `docker run -p 5432:5432` on a box where `ufw status` says "deny incoming" publishes Postgres to the internet, and ufw reports everything is fine. Databases have been found and drained this way within hours of a box coming online.

Three fixes, in order:

1. Publish to loopback explicitly: `127.0.0.1:5432:5432`. Nothing outside the box can reach it, whatever the firewall thinks.
2. Do not publish at all — services on the same Docker network reach each other by name without any host port (`containers.md`).
3. If a port must be public, let the proxy be the only published container and route internally.

Verify from another machine, never from the box: the loopback test passes in every configuration and proves nothing.

## Security Headers

Set at the proxy so every app on the box inherits them:

| Header | Value | Effect |
|---|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | No plaintext for a year — after HTTPS works everywhere (`tls.md`) |
| `X-Content-Type-Options` | `nosniff` | Stops the browser guessing a content type and executing an upload |
| `X-Frame-Options` / CSP `frame-ancestors` | `DENY` or an allowlist | Clickjacking; `frame-ancestors` supersedes the old header |
| `Content-Security-Policy` | Application-specific | The only header that stops injected script from executing; the only one that requires real work |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Stops full URLs (with tokens in query strings) leaking to third parties |
| `Permissions-Policy` | Deny what the app does not use | Camera, microphone, geolocation off by default |

CSP is done in report-only mode first (`Content-Security-Policy-Report-Only`), for long enough to see real traffic, then enforced. Shipping a strict policy straight to production breaks analytics, embeds, and inline handlers on the first afternoon and gets switched off wholesale.

`add_header` in nginx **replaces** the inherited set within a `location` block: adding one header in a location silently drops every header defined at the server level. Use `always` and re-declare, or set them in one place only.

Remove the version banner (`server_tokens off;`, `expose_php=Off`) — minor, but free.

## Abuse Controls

- Rate limit by real client IP at the proxy — which requires forwarded-header handling to be correct first, or the limit applies to the CDN and takes everyone down together (`proxy.md`).
- Different limits for different routes: login and password-reset endpoints need something aggressive (a handful per minute), a read API needs generous. One global limit is either useless or hostile.
- `limit_conn` caps concurrent connections per IP and is the cheap defence against slow-loris style connection hoarding; combine with short `client_header_timeout` and `client_body_timeout`.
- Fail2ban-style blocking works off log patterns and is only as good as the logged client IP — same prerequisite.
- Bot floods that saturate the network cannot be solved on the box: that is a CDN or provider-level problem, and the honest answer is to say so rather than tune nginx into a corner.

## Admin Interfaces

Every self-hosted app ships one, and it is the most common way a home or small-business server is taken:

- Never expose an admin panel to the internet if a VPN or SSH tunnel is available. "Behind a strong password" is a race against a scanner that already knows the default path.
- Change every default credential before the service is reachable, not after — scanners find new hosts in minutes, not days.
- Put a second factor in front of what has none: proxy-level basic auth, mTLS, an IP allowlist, or an authentication proxy. Two weak locks in series beat one.
- Keep management ports off the public interface: databases, message brokers, metrics endpoints, container dashboards, and the container socket most of all. Exposing the Docker socket over TCP, or mounting it into a container that does not need it, is equivalent to handing over root.

## Dependency and Image Freshness

- Unattended security updates on for the OS, with a known reboot policy — a box that installs kernel updates and never reboots is running the old kernel indefinitely.
- Base images pinned by digest and rebuilt on a cadence: pinning without rebuilding is how a two-year-old vulnerable base ships to production forever (`containers.md`).
- Application dependencies scanned on a schedule, not only at release. The vulnerability arrives after your last deploy.
- The cadence belongs in `## Due`, or it does not happen (`maintenance.md`).

## If Something Leaked

Order matters — revoke before investigating, because investigation takes hours and the credential is being used now.

1. **Revoke or rotate the credential.** Not "change it soon". If it is a certificate key, reissue and revoke.
2. **Cut the access path**: disable the exposed port, take the service off the public interface, or stop it.
3. **Then** work out the blast radius: what that credential could reach, and what it did reach — access logs, database audit, provider activity log.
4. Rotate everything the compromised process could read: its environment file, its keys, the tokens of services it talks to.
5. Assume persistence if the process was reachable as root: new users, authorized keys, cron entries, systemd units, container images.
6. Record it in `incidents/<year>.md` with the real cause; if a secret ever lived in a file under `~/Clawic/data/`, delete it there and replace it with a pointer.

A leaked secret in git history survives a later commit that removes it; rotation is the only fix, and rewriting history is cleanup, not remediation.

## Baseline Checklist

| Check | Passing looks like |
|---|---|
| Listeners | Only the proxy on `0.0.0.0`; everything else loopback or socket |
| Service users | One dedicated non-login user per service, not owning its own code |
| Sandbox | `systemd-analyze security` under ~4 for each network-facing unit |
| Secrets | Nothing in units, images, or the repository; environment file 0640 or a credential store |
| Container ports | Published to `127.0.0.1` or not published; container socket never exposed |
| TLS | HTTPS everywhere, HSTS set, renewal reloads the serving process (`tls.md`) |
| Headers | The table above set once, at the proxy, and verified with a live request |
| Rate limits | Per-route, on the real client IP, with 429 as the response |
| Admin surfaces | Not on the public internet, defaults changed, second factor in front |
| Updates | Unattended security updates on, reboot policy known, image rebuild cadence in `## Due` |
| Backups | Exist, are off-box, and a restore has been timed (`maintenance.md`) |
| Uploads | Not executable, not served from the app's origin without validation |

## Write It Down

After a hardening pass: update the listen-address column of `## Services` for anything you moved to loopback, add the update and rebuild cadences to `## Due`, and put the sandbox stanza that took real effort into `~/Clawic/data/server/artifacts/working-unit-<service>.md` with the reason for each directive (`memory-template.md`). A leak or exposure goes in `incidents/<year>.md`. Write paths, ports and variable *names*; never a key, a token, or the contents of an environment file.
