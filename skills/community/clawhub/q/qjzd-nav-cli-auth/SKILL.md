---
name: qjzd-nav-cli-auth
version: 1.0.0
description: Use when working with QJZD Nav CLI login, bearer token auth, profile setup, profile switching, current profile inspection, or fixing missing keyring credentials.
references:
  - ../qjzd-nav-cli
metadata:
  openclaw:
    category: developer-tools
    requires:
      bins: ["qjzd-nav"]
    cliHelp: "qjzd-nav auth --help"
---

# QJZD Nav CLI Auth

Use this skill for `qjzd-nav auth` and `qjzd-nav auth profile`.

If authentication is not set up yet, do this first before running `link`, `category`, `tag`, `backup`, or `settings` commands.

## Commands

```bash
qjzd-nav auth --help
qjzd-nav auth login --help
qjzd-nav auth profile --help
```

Main workflows:

- `qjzd-nav auth login`
- `qjzd-nav auth current`
- `qjzd-nav auth profile list`
- `qjzd-nav auth profile current`
- `qjzd-nav auth profile get <name>`
- `qjzd-nav auth profile use <name>`
- `qjzd-nav auth profile delete <name>`
- `qjzd-nav auth profile doctor`

## Common Flows

Login with password (uses RSA encryption):

```bash
qjzd-nav auth login \
  --profile default \
  --url https://nav.qjzd.online \
  --password <password>
```

Note: The password is encrypted with the server's public key before being sent.

Inspect and switch profiles:

```bash
qjzd-nav auth current
qjzd-nav auth profile list
qjzd-nav auth profile use production
qjzd-nav auth profile get default --json
```

Diagnose broken credentials:

```bash
qjzd-nav auth profile doctor
qjzd-nav auth profile delete production --force
```

## Rules

- In non-interactive mode, `qjzd-nav auth login` requires `--profile`, `--url`, and `--password`.
- Use `--json` when another tool needs structured output.
- `profile delete` is destructive; use `--force` in non-interactive mode.
- Profile metadata lives in config, but secrets live in the system keyring.
- The CLI uses RSA encryption for password authentication.

## Routing

- Use `qjzd-nav-cli-content` for links, categories, and tags.
- Use `qjzd-nav-cli-operations` for backups, restore, and settings.
