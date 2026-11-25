# VPS Audit & Migration

Auditing existing VPS Docker setups and migrating them to strut management.

## Quick Reference

```bash
# Audit a VPS (discover what's running)
strut audit <vps-host> [vps-user] [ssh-key]
strut audit 192.168.1.100 ubuntu
strut audit example-host deploy 2222 <path-to-ssh-key>

# Migration wizard
strut migrate <vps-host> [vps-user] [ssh-port] [ssh-key]           # interactive
strut migrate <vps-host> [vps-user] [ssh-port] [ssh-key] --yes     # automated (phases 1-5)
strut migrate <vps-host> [vps-user] --start-phase 4                # resume

# Generate a stack from an audit
strut audit:generate <stack-name> --from audits/<timestamp>-<host>

# List past audits
strut audit:list
```

## What Gets Audited

Docker containers/volumes/networks/images, nginx config, systemd services, cron jobs, firewall rules (UFW/iptables), SSL certificates, database services, environment variable **key names** (not values — intentional), disk usage, and port usage.

## Audit Output

```
audits/<timestamp>-<host>/
├── REPORT.md                # human-readable full report
├── STACK_SUGGESTIONS.md     # suggested stack groupings
├── containers.jsonl         # container/volume/network/image data
├── nginx/ systemd/ cron/    # discovered configs
├── firewall/ ssl/ databases/
├── secrets/                 # env file key names
└── keys/                    # categorized key discovery + KEYS_MIGRATION.md
```

Review with: `cat audits/<latest>/REPORT.md` and `cat audits/<latest>/STACK_SUGGESTIONS.md`.

## Migration Wizard (8 Phases)

1. **Pre-flight checks** — SSH connectivity, Docker install check, disk space, container count.
2. **Setup strut on VPS** — clones the repo (handles GitHub auth: PAT, SSH key, or deploy key).
3. **Audit** — full discovery (same as `audit`).
4. **Generate stacks** — scaffolds `docker-compose.yml` + `.env.template` per suggested stack.
5. **Pre-cutover backup** — backs up databases from existing containers; writes `ROLLBACK.md`.
6. **Test deployment** *(interactive)* — deploy + health-check each stack.
7. **Cutover** *(interactive)* — stop old containers (not removed), bring up strut stacks, health-check.
8. **Cleanup** *(interactive)* — remove stopped containers, `docker system prune`. Volumes preserved.

Phases 6-8 are intentionally interactive — they require manual validation.

## Stack Generation

```bash
strut audit:generate my-app --from audits/<timestamp>-<host>
```

Generates starting-point files. You must then:
1. Review port mappings.
2. Fill in env var values (audit only captures key names).
3. Map volumes (reuse existing via `external: true` + `name:`).
4. Update health checks and `depends_on`.

### Reusing an Existing Volume

```yaml
volumes:
  postgres-data:
    external: true
    name: oldproject_postgres_data   # existing volume name from the audit
```

## Common Workflows

### Onboard a New VPS

```bash
strut audit 192.168.1.100 ubuntu
cat audits/<latest>/REPORT.md
strut audit:generate my-app --from audits/<latest>
nano stacks/my-app/docker-compose.yml
cp stacks/my-app/.env.template .my-app-prod.env
nano .my-app-prod.env
strut my-app deploy --env my-app-prod
strut my-app health --env my-app-prod
```

### Find Which Env Vars a Container Uses

List variable **names only**. Do not print values: they are secrets and would land in the session transcript. Copy the values into your `.env` file yourself.

```bash
ssh ubuntu@<vps-host>
docker exec <container-name> env | cut -d= -f1 | grep -E '(DATABASE|API|SECRET|SMTP)'
```

## Troubleshooting

### SSH connection fails

```bash
ssh -o ConnectTimeout=10 ubuntu@<vps-host>
ssh-add <path-to-ssh-key>    # the key you already use for this VPS; never print or paste its contents
```

### Docker not found

The wizard offers to install Docker. Manual fallback: install Docker Engine on the VPS by following Docker's official instructions for its distribution (https://docs.docker.com/engine/install/). Do not pipe a downloaded script into a shell on the VPS; if you use a convenience script, download it, read it, then run it.

### Generated stack doesn't work

1. Review TODO comments in the generated `docker-compose.yml`.
2. Confirm all env vars are filled.
3. Verify volume mappings.
4. `strut <stack> logs --follow` and start with one service.

## Rollback

```bash
docker start <old-container-name>                          # restart old containers
docker compose --project-name <stack>-prod down            # stop strut stack
cat backups/pre-migration-<stack>-*/ROLLBACK.md            # recovery instructions
```
