---
name: eve-local-dev-loop
description: Local Docker Compose development loop for Eve-compatible apps, with handoff to staging deploys.
---

# Eve Local Dev Loop (Docker Compose)

Use this skill to run and test the app locally with Docker Compose, then hand off to Eve for staging deploys.

## Preconditions

- A `compose.yaml` or `docker-compose.yml` exists in the repo.
- The Eve manifest (`.eve/manifest.yaml`) reflects the same services and ports.

## Local Run

```bash
# Start local services (DB + migrations)
docker compose up -d

# Start API in dev mode (hot reload)
cd apps/api && npm run dev

# Start web in dev mode (Vite dev server with /api proxy)
cd apps/web && npm run dev

# View DB logs
docker compose logs -f

# Reset DB (drop + recreate + migrate)
docker compose down -v && docker compose up -d
```

## Recommended docker-compose.yml

Use the Eve-migrate image locally for migration parity with staging:

```yaml
services:
  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: myapp
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d myapp"]
      interval: 5s
      timeout: 5s
      retries: 5

  migrate:
    image: ghcr.io/eve-horizon/eve-migrate:latest
    environment:
      DATABASE_URL: postgres://app:app@db:5432/myapp
    volumes:
      - ./db/migrations:/migrations:ro
    depends_on:
      db:
        condition: service_healthy

volumes:
  pgdata:
```

**Why eve-migrate?** The same runner executes in both local and staging, giving migration parity. It tracks applied migrations in `schema_migrations` (idempotent, checksummed, transactional). Plain SQL files with timestamp prefixes: `20260312000000_initial_schema.sql`.

Run migrations manually after adding a new file:
```bash
docker compose run --rm migrate
```

## Keep Compose and Manifest in Sync

- Match service names and exposed ports between Compose and the Eve manifest.
- The Compose `db` service mirrors the manifest's managed DB. Locally it's a container; in staging, Eve provisions it.
- The Compose `migrate` service mirrors the manifest's `migrate` job. Both use eve-migrate and mount `db/migrations/`.
- If a service is public in production, set `x-eve.ingress.public: true` in the manifest.
- Use `${secret.KEY}` in the manifest and keep local values in `.eve/dev-secrets.yaml`.

## Local Environment Variables

- Create `.env` for the API (e.g., `DATABASE_URL=postgresql://app:app@localhost:5432/myapp`).
- Prefer `.env` for Compose and `.eve/dev-secrets.yaml` for manifest interpolation.
- Never commit secrets; keep `.eve/dev-secrets.yaml` in `.gitignore`.
- For the Vite dev server, configure a proxy in `vite.config.ts` to forward `/api` to `http://localhost:3000` (matching the nginx proxy pattern in production).

## Promote to Staging

```bash
# Ensure profile and auth are set
eve profile use staging
eve auth status

# Set required secrets
eve secrets set API_KEY "value" --project proj_xxx

# Deploy to staging (requires --ref with 40-char SHA or a ref resolved against --repo-dir)
eve env deploy staging --ref main --repo-dir .

# If the environment has a pipeline configured, this triggers the pipeline.
# Use --direct to bypass pipeline and deploy directly:
eve env deploy staging --ref main --repo-dir . --direct
```

Track the deploy job:

```bash
eve job list --phase active
eve job follow <job-id>
eve job result <job-id>
```

## If Local Works but Staging Fails

- Re-check manifest parity with Compose.
- Verify secrets exist in Eve (`eve secrets list`).
- Use `eve job diagnose <job-id>` for failure details.
