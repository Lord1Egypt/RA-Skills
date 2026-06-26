# `.Ubuntu-Encyclopedia/` Cache Layout

Use this directory as the workspace-local data root for the skill.

## Directory tree

```text
.Ubuntu-Encyclopedia/
  manpages/
    manpages.ubuntu.com/
      ... cached Ubuntu manpages ...
  docs/
      ... cached official Ubuntu docs pages ...
  notes/
    components/
      ... per-component notes ...
    patterns/
      ... reusable Ubuntu notes ...
  inventory/
    access.md
    topology.md
    doc-index.md
```

## Placement rules

### `manpages/`
Store cached copies of Ubuntu manpages here.

Mirror the official path as much as practical.
Example:

```text
https://manpages.ubuntu.com/manpages/noble/en/man8/apt.8.html
->
.Ubuntu-Encyclopedia/manpages/manpages.ubuntu.com/manpages/noble/en/man8/apt.8.md
```

### `docs/`
Store cached copies of broader official Ubuntu docs here.

### `notes/components/`
Store environment-specific component notes here.

Suggested filenames:
- `apt.md`
- `systemd.md`
- `networking.md`
- `storage.md`
- `release-upgrades.md`

### `notes/patterns/`
Store reusable operational notes here.

Examples:
- `apt-repair.md`
- `service-troubleshooting.md`
- `netplan-gotchas.md`
- `journalctl-patterns.md`

### `inventory/`
Store environment-wide inventories here.

Suggested files:
- `access.md`
- `topology.md`
- `doc-index.md`

## Cache philosophy

Do not mirror the whole source set eagerly.
Cache only the pages you actually consulted and expect to be useful later.
