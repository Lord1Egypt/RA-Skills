# Database Backups & Restore

Backup and restore procedures for strut databases (Postgres, Neo4j, MySQL, SQLite).

## Create Backups on VPS

```bash
strut my-stack backup postgres --env prod
strut my-stack backup neo4j --env prod
strut my-stack backup mysql --env prod
strut my-stack backup sqlite --env prod
strut my-stack backup all --env prod        # all enabled targets for the stack
```

## Pull Production Data to Local

```bash
strut my-stack db:pull --env prod                    # pull + restore all
strut my-stack db:pull postgres --env prod           # specific type
strut my-stack db:pull --env prod --download-only     # download, no restore
```

## Push Local Data to Production

```bash
# ⚠️ overwrites production data
strut my-stack db:push postgres --env prod --file backups/postgres-20260303-143022.sql
strut my-stack db:push postgres --env prod --file backups/postgres.sql --dry-run
```

## Restore & Rehearsal

```bash
# Rehearse a restore into a scratch DB, compare vs live, then drop scratch (non-destructive)
strut my-stack restore backups/postgres-20260315.sql --dry-run

# Actual restore (drops and recreates the live DB)
strut my-stack restore backups/postgres-20260315.sql --env prod
```

`--dry-run` never touches the live database — it restores into a temporary scratch DB, reports row-count deltas vs live, and drops the scratch DB.

## Backup Verification

```bash
strut my-stack backup verify backups/postgres-20260315-020000.sql --env prod
strut my-stack backup verify-all --env prod
strut my-stack backup health --env prod            # health scores (0-100)
```

## Retention & Scheduling

Each stack has a `backup.conf` controlling schedules and retention:

```bash
# stacks/<stack>/backup.conf
BACKUP_POSTGRES=true
BACKUP_SCHEDULE_POSTGRES="0 2 * * *"   # 02:00 UTC daily
BACKUP_RETAIN_DAYS=30
BACKUP_RETAIN_COUNT=10
```

```bash
strut my-stack backup schedule install-defaults --env prod
strut my-stack backup schedule list --env prod
strut my-stack backup retention --env prod
```

## Common Scenarios

### Refresh Local Dev

> Production data usually contains customer PII. Pull it only to a machine you control, keep it out of git, and confirm with the user before running `db:pull`. Do not open or print dump contents in the session.

```bash
strut my-stack db:pull --env prod
```

### Recover from a Bad Migration

A down migration can drop tables, indexes or other schema objects, and any data in them is gone for good. Do not run one on production until the user has approved it, having seen the dry run and the backup below.

```bash
strut my-stack backup neo4j --env prod            # back up the database you are about to roll back
strut my-stack backup list neo4j --env prod        # confirm the new backup exists
strut my-stack migrate neo4j --status --env prod  # see which migration is current
strut my-stack migrate neo4j --down 1 --env prod  # only after the user approves
strut my-stack health --env prod
```

Back up the same database that the migration touches (here `neo4j`; use `postgres` for a Postgres migration). A backup of a different database does not protect this one. `db:pull` copies production data to your machine and is not a backup of the VPS.

## Notes

- Databases running inside Docker containers may require `VPS_SUDO=true` in the env file for sudo Docker access.
- SQLite inside a Docker volume needs `BACKUP_SQLITE_USE_DOCKER=true` in `backup.conf`.

## Troubleshooting

```bash
strut my-stack exec "df -h /" --env prod                      # disk space
strut my-stack exec "docker compose exec postgres pg_isready" --env prod
strut my-stack shell --env prod                                # check SSH access
grep -c '^VPS_HOST=' .prod.env                                # 1 if VPS_HOST is set
```
