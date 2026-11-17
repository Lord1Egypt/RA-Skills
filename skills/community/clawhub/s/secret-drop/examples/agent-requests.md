# Example messenger requests

The messages below contain only synthetic links.

## Global OpenClaw provider credential

> Store this as `OPENROUTER_API_KEY` for OpenClaw: `https://eu.pwpush.com/p/example-token/r`

Expected agent action:

```bash
python3 <skill-directory>/scripts/secret-drop ingest \
  "https://eu.pwpush.com/p/example-token/r" \
  --to openclaw-env \
  --name OPENROUTER_API_KEY \
  --json
```

A successful result says `restart_required: true`. Do not claim the running Gateway uses the value until an authorized restart is complete.

## Protected OpenClaw store entry and SecretRef binding

> Store this drop as `ACME_API_KEY`, allow only `api.acme.example`, and bind it to `models.providers.acme.apiKey`: `https://snappwd.io/g/sp-example#example-key`

Expected agent action:

```bash
python3 <skill-directory>/scripts/secret-drop ingest \
  "https://snappwd.io/g/sp-example#example-key" \
  --to openclaw-store \
  --name ACME_API_KEY \
  --store-kind secret \
  --allow-host api.acme.example \
  --config-path models.providers.acme.apiKey \
  --reload \
  --json
```

## Project dotenv

> Put this into `/srv/acme/.env` as `DATABASE_URL`: `https://pwpush.example/p/example-token/r`

For a self-hosted Password Pusher on an unknown domain, select the provider explicitly:

```bash
python3 <skill-directory>/scripts/secret-drop ingest \
  "https://pwpush.example/p/example-token/r" \
  --provider pwpush \
  --to dotenv \
  --path /srv/acme/.env \
  --name DATABASE_URL \
  --json
```

## Outbound secret request from operator

> What is the database password in `/srv/acme/.env`?

Expected agent action:

```bash
python3 <skill-directory>/scripts/secret-drop share \
  --from dotenv \
  --path /srv/acme/.env \
  --name DATABASE_URL \
  --json
```

The agent posts only the resulting one-time URL back to the operator.
