---
name: Traefik
description: Avoid common Traefik mistakes — router priority, TLS configuration, Docker labels syntax, and middleware ordering.
metadata: {"clawdbot":{"emoji":"🔀","os":["linux","darwin","win32"]}}
---

## Router Basics
- Router must have `rule` AND `service` — missing either = not working
- Rule priority: longer rules win by default — explicit `priority` to override
- `Host()` is case-insensitive — `Host(\`example.com\`)` matches Example.com
- Multiple hosts: `Host(\`a.com\`) || Host(\`b.com\`)` — OR logic

## Docker Labels Syntax
- Labels on container, not compose service level — `deploy.labels` for Swarm
- Backticks for rules in Docker Compose — `Host(\`example.com\`)` with escaping
- Enable per-container: `traefik.enable=true` — if `exposedByDefault=false`
- Service name auto-generated from container — or set explicitly with `traefik.http.services.myservice.loadbalancer.server.port=80`

## TLS and Certificates
- EntryPoint `websecure` needs TLS config — otherwise plain HTTP on 443
- Let's Encrypt: `certificatesResolvers.myresolver.acme.email` required — registration fails without
- HTTP challenge needs port 80 open — DNS challenge for wildcard or closed 80
- `tls=true` on router activates TLS — `tls.certresolver=myresolver` for auto-cert
- Staging ACME for testing — `caServer` to staging URL, avoids rate limits

## EntryPoints
- Define in static config — `--entrypoints.web.address=:80`
- Redirect HTTP to HTTPS at entrypoint level — cleaner than per-router middleware
- Router binds to entrypoint with `entryPoints=web,websecure` — comma-separated list

## Middlewares
- Chain order matters — first middleware wraps all following
- Middleware defined once, used by many routers — `middlewares=auth,compress`
- Common: `stripPrefix`, `redirectScheme`, `basicAuth`, `rateLimit`
- BasicAuth: use `htpasswd` format — escape `$` in Docker Compose with `$$`

## Service Configuration
- `loadbalancer.server.port` when container exposes multiple — Traefik can't guess
- Health check: `healthcheck.path=/health` — removes unhealthy from rotation
- Sticky sessions: `loadbalancer.sticky.cookie.name=srv_id` — for stateful apps

## Common Mistakes
- Router without entryPoint — defaults may not be what you expect
- Forgetting `traefik.docker.network` with multiple networks — Traefik picks wrong one
- ACME storage not persisted — certificates regenerated, hits rate limit
- Dashboard exposed without auth — `api.insecure=true` is dangerous in production
- PathPrefix without StripPrefix — backend receives full path, may 404
- Services on different ports — each needs explicit port label

## File Provider
- `watch=true` for hot reload — otherwise restart Traefik on changes
- Can coexist with Docker provider — useful for external services
- Define routers, services, middlewares in YAML — same concepts as labels

## Debugging
- `--log.level=DEBUG` for troubleshooting — verbose but helpful
- Dashboard shows routers, services, middlewares — verify configuration
- `--api.insecure=true` for local dev only — secure with auth in production
