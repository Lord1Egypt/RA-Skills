# Secrets & Key Rotation

Rotating credentials for a strut stack — SSH keys, API keys, database passwords, GitHub secrets, and environment variables.

## Key Types

| Category | Where stored | CLI prefix | Affects |
|---|---|---|---|
| SSH keys | VPS `authorized_keys` + `keys/ssh-keys.json` | `keys ssh:*` | VPS access, CI/CD |
| API keys | `.env` + `keys/api-keys.json` | `keys api:*` | External consumers |
| Database passwords | `.env` + live DB | `keys db:rotate` | All services |
| GitHub secrets | GitHub repo secrets | `keys github:*` | CI/CD pipelines |
| Env var secrets | `.env` file | `keys env:*` | All services |

The `keys/` directory stores metadata only (fingerprints, masked values, dates) — never actual secrets.

## Secrets Sync (env files)

```bash
strut my-stack secrets push --env prod       # upload .env to VPS (mode 600)
strut my-stack secrets pull --env prod        # download .env from VPS
strut my-stack secrets diff --env prod        # compare local vs remote key names (masked)
strut my-stack secrets validate --env prod    # check required_vars coverage
strut my-stack secrets hydrate --env prod     # populate .env from template + providers
strut my-stack secrets set KEY --env prod      # set a single secret (value via stdin)
```

## Full Stack Rotation

Work through in order — DB password changes require a redeploy, so batch them.

### 1. Back up current state

```bash
strut my-stack keys env:backup --env prod
strut my-stack backup all --env prod
```

### 2. Rotate SSH keys

```bash
strut my-stack keys ssh:rotate <username> --env prod
strut my-stack keys ssh:audit --env prod
strut my-stack keys github:rotate-vps-key --repos "YOUR_ORG/repo-a,YOUR_ORG/repo-b"
```

### 3. Rotate database passwords

```bash
strut my-stack keys db:rotate postgres --env prod
strut my-stack keys db:rotate neo4j --env prod
strut my-stack deploy --env prod       # redeploy so services pick up new passwords
strut my-stack health --env prod
```

### 4. Rotate env var secrets

```bash
strut my-stack keys env:rotate --env prod                    # auto-rotatable secrets
strut my-stack secrets set THIRD_PARTY_API_KEY --env prod   # rotate in provider first; the value is read from stdin, never put it on the command line
```

### 5. Rotate API keys

```bash
strut my-stack keys api:list
strut my-stack keys api:rotate <key-name>
```

### 6. Final verification

```bash
strut my-stack keys env:validate --env prod
strut my-stack keys env:diff --local .prod.env --remote --env prod
strut my-stack health --env prod --json
strut my-stack keys ssh:audit --env prod
```

## Rotation Schedule (suggested)

| Secret type | Interval | Also rotate on |
|---|---|---|
| SSH keys | 90 days | Team member departure |
| GitHub PAT | 90 days | Expiry warning |
| Database passwords | 90 days | Suspected breach |
| API keys | 90 days | Consumer offboarding |
| Third-party keys | Per provider | Suspected exposure |

## Troubleshooting

### Services down after rotation

```bash
strut my-stack logs --tail 100 --env prod
# Most common: services didn't pick up the new DB password → redeploy
strut my-stack deploy --env prod
```

### Rotation failed mid-process

```bash
ls .prod.env.backup-*
cp .prod.env.backup-YYYYMMDD-HHMMSS .prod.env
strut my-stack deploy --env prod
```
