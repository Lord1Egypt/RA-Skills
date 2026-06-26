---
name: qjzd-nav-cli
version: 1.0.0
description: Use when the task involves QJZD Nav CLI, including managing links, categories, tags, backups, settings, or authentication.
references:
  - ../qjzd-nav-cli-auth
  - ../qjzd-nav-cli-content
  - ../qjzd-nav-cli-operations
metadata:
  openclaw:
    category: developer-tools
    requires:
      bins: ["qjzd-nav"]
    cliHelp: "qjzd-nav --help"
---

# QJZD Nav CLI

This is the routing skill for the QJZD Nav CLI skill set.

If the request only says "use QJZD Nav CLI" or mixes multiple areas, start here, then jump to the domain skill that matches the task.

## Skill Map

- `qjzd-nav-cli-auth`: login, profile setup, profile switching, keyring and credential repair
- `qjzd-nav-cli-content`: links, categories, and tags management
- `qjzd-nav-cli-operations`: backup, restore, and settings management

## Fast Routing

Use these commands to identify the right area:

```bash
qjzd-nav --help
qjzd-nav auth --help
qjzd-nav link --help
qjzd-nav category --help
qjzd-nav tag --help
qjzd-nav backup --help
qjzd-nav settings --help
qjzd-nav completion --help
```

## Shell Completion

Generate and install shell completion scripts:

```bash
# Bash
eval "$(qjzd-nav completion bash)"

# Zsh
eval "$(qjzd-nav completion zsh)"
```

After enabling completion, press <kbd>Tab</kbd> to complete commands:

```bash
qjzd-nav <TAB>
qjzd-nav auth <TAB>
qjzd-nav link <TAB>
```

## Shared Defaults

- Prefer an authenticated profile unless the task is public.
- Use `--profile <name>` when the environment matters.
- Use `--json` for automation.
- Use `--force` carefully for destructive non-interactive operations.

## Top-Level Areas

- `auth` - Authentication and profile management
- `link` - Link CRUD operations
- `category` - Category CRUD operations
- `tag` - Tag CRUD operations
- `backup` - Backup and restore operations
- `settings` - Site settings management

## Config And Secrets

Profile metadata is stored in:

- `$QJZD_NAV_CLI_CONFIG_DIR/config.json` if `QJZD_NAV_CLI_CONFIG_DIR` is set
- otherwise `$XDG_CONFIG_HOME/qjzd-nav/config.json`
- otherwise `$HOME/.config/qjzd-nav/config.json`

Credentials are stored in the system keyring via `@napi-rs/keyring`.
