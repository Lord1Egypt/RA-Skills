# Ubuntu Encyclopedia Workflow

## Core stance

Use Ubuntu manpages, official Ubuntu docs, and local observed state together.

Default order:
1. check `.Ubuntu-Encyclopedia/` cache/notes
2. check authoritative Ubuntu sources when needed
3. inspect live environment state
4. answer or act
5. record durable learnings

## When lookup is mandatory

Do a manpage/docs lookup before answering or acting when any of these are true:
- the user asks about Ubuntu command syntax, package behavior, service behavior, or distro-specific admin/troubleshooting steps
- the task involves apt, apt-get, dpkg, snap, systemd, systemctl, journalctl, Netplan, NetworkManager, repository/key management, release upgrades, storage/admin work, or Ubuntu-specific networking
- the task involves a version-sensitive feature or a behavior you are not highly confident about
- the task involves live maintenance/troubleshooting work and the command path or safety boundaries matter

## Source preference

Prefer sources in this order:
1. Ubuntu manpages for command/utility behavior
2. Official Ubuntu documentation for broader workflows and distro guidance

## Cache-first rule

Before fetching docs, check whether the needed material already exists under:
- `.Ubuntu-Encyclopedia/manpages/manpages.ubuntu.com/...`
- `.Ubuntu-Encyclopedia/docs/...`
- `.Ubuntu-Encyclopedia/notes/components/...`
- `.Ubuntu-Encyclopedia/notes/patterns/...`
- `.Ubuntu-Encyclopedia/inventory/...`

If the local cache is good enough, use it.
If not, fetch/check the authoritative source and then cache what you used.

## How to cache docs

Use:
- `scripts/cache_manpage.py` for Ubuntu manpages
- `scripts/cache_doc.py` for broader official Ubuntu docs

Typical usage:

```bash
python3 scripts/cache_manpage.py \
  --url 'https://manpages.ubuntu.com/manpages/noble/en/man8/apt.8.html' \
  --root '<workspace>/.Ubuntu-Encyclopedia'
```

## How to store local knowledge

### Component notes

Use `.Ubuntu-Encyclopedia/notes/components/<component-name>.md` for:
- package/service/component purpose
- access path or host role
- sensitive boundaries
- discovered quirks

### Pattern notes

Use `.Ubuntu-Encyclopedia/notes/patterns/<topic>.md` for:
- recurring maintenance/admin patterns
- repeated gotchas
- safe repair sequences
- environment-specific design conventions

### Inventory files

Use `.Ubuntu-Encyclopedia/inventory/` for:
- deployment/access inventory
- host-role notes
- documentation index

## Distinguish evidence types

When writing notes, label information mentally as one of:
- **Authoritative docs** — from Ubuntu manpages or official Ubuntu docs
- **Observed local state** — from live environment inspection
- **Inference/recommendation** — your judgment based on docs + local state

Do not blur these together.

## High-sensitivity areas

Treat these as high-sensitivity even when you have live access:
- release upgrades
- package repair or forceful package operations
- networking changes
- storage/mount/fstab changes
- boot-impacting changes
- service/security changes that could break access

For these, prefer docs lookup even if you think you remember the command.
