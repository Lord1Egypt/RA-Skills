# xCloud Deployment Paths: Docker vs Native

## Two Paths Available

### Path 1 — xCloud Native (Git Push Deploy)

xCloud natively supports these stacks without Docker:
- **WordPress** — managed WordPress hosting with auto-config
- **Laravel** — PHP-FPM, Composer install, artisan commands
- **PHP** — generic PHP apps (CodeIgniter, Symfony, etc.)
- **Node.js** — npm/yarn install, process management

How it works:
```
git push → xCloud: git pull + composer install (or npm install) + reload
```

Advantages:
- Simpler setup — no Dockerfile needed
- Faster deploys (no image build/pull)
- xCloud manages PHP version, extensions, process manager
- Direct file access via SFTP

When to choose Native:
- Standard single-language app
- Standard database (MySQL/MariaDB only)
- No custom runtime dependencies

### Path 2 — Custom Docker Deploy

Use Docker when:
- App requires non-standard runtime (Python, Go, Rust, Java)
- Multiple services (API + queue worker + Redis)
- Framework requires build step (Next.js, Nuxt.js, NestJS)
- Custom dependencies not available via apt/pecl
- Already containerized (existing docker-compose.yml)

How it works:
```
git push → xCloud: git pull + docker-compose pull + docker-compose up -d
```

Constraints (see xcloud-constraints.md for full list):
- No `build:` in compose — images must be pre-built in public registry
- Single exposed port
- No Caddy/Traefik/nginx-proxy (xCloud handles SSL + reverse proxy)

## Decision Matrix

| Stack | DB Needs | Background Jobs | Recommended Path |
|---|---|---|---|
| WordPress | MySQL only | No | Native |
| Laravel | MySQL only | No | Native |
| Laravel | MySQL + Redis + Queue workers | Yes | Docker |
| PHP generic | MySQL only | No | Native |
| Node.js (Express/Fastify) | Any | No | Native |
| Next.js | Any | No | Docker |
| NestJS | Any | Any | Docker |
| Python (FastAPI/Django) | Any | Any | Docker |
| Go / Rust / Java | Any | Any | Docker |
| Multi-service app | Any | Any | Docker |
