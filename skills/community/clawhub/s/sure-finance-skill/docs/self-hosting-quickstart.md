# Self-Hosting Quickstart (Docker)

This quickstart is aligned with Sure's official Docker guide.

> **Security note:** The commands below download compose files from `raw.githubusercontent.com`. Always review downloaded files before running `docker compose up`. This entire document is optional — it applies only when the user explicitly asks to self-host Sure.

## Minimal Setup

```bash
mkdir -p ~/docker-apps/sure
cd ~/docker-apps/sure
curl -o compose.yml https://raw.githubusercontent.com/we-promise/sure/main/compose.example.yml
# Review compose.yml before proceeding
docker compose up -d
```

Sure should be available at:
- http://localhost:3000

## Optional Environment Hardening

```bash
curl -o .env https://raw.githubusercontent.com/we-promise/sure/main/.env.example
```

Recommended values:

```txt
SECRET_KEY_BASE="<generated-secret>"
POSTGRES_PASSWORD="<strong-password>"
```

If serving behind HTTPS reverse proxy, set in compose:

```yaml
RAILS_ASSUME_SSL: "true"
```

## AI Compose Mode

```bash
curl -o compose.ai.yml https://raw.githubusercontent.com/we-promise/sure/main/compose.example.ai.yml
curl -o pipelock.example.yaml https://raw.githubusercontent.com/we-promise/sure/main/pipelock.example.yaml
# Review both files before proceeding
docker compose -f compose.ai.yml up -d
```

With local LLM profile:

```bash
docker compose -f compose.ai.yml --profile ai up -d
```

## Update Procedure

```bash
docker compose pull
docker compose build
docker compose up --no-deps -d web worker
```

## Quick Health Checks

```bash
docker compose ps
curl --silent --show-error --fail http://localhost:3000
```
