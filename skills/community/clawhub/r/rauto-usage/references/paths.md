# Rauto Paths

Use this file for any "where is data stored?" question.

## Runtime root

```text
~/.rauto/
```

## Default directories

```text
~/.rauto/connections/            # saved connection profiles (*.toml)
~/.rauto/profiles/               # custom profile files (legacy/custom store)
~/.rauto/templates/commands/     # command templates (*.j2, etc.)
~/.rauto/templates/devices/      # custom device profiles (*.toml)
~/.rauto/records/                # recording files (*.jsonl)
~/.rauto/records/by_connection/  # auto history recordings per saved connection
~/.rauto/backups/                # backup archives (*.tar.gz)
```

## Notes

- Local `./templates/` may still be read as fallback for backward compatibility.
- `rauto backup create` defaults to `~/.rauto/backups/rauto-backup-<timestamp>.tar.gz`.
