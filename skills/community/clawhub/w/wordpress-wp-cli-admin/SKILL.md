---
name: wordpress-wp-cli-admin
description: Operate WordPress installs through WP-CLI for inspection, core maintenance, plugin and theme management, users, options, content, media, cron, database tasks, and multisite-aware administration. Use when shell, SSH, or node-local access exists and the task should be done with `wp` instead of the REST API or custom WP-CLI package development.
metadata: {"openclaw":{"emoji":"🛠️"}}
---

# WordPress WP-CLI Admin

Use this skill when a WordPress task belongs in `wp`, not `/wp-json`.

The point of this skill is not to memorize every command. The point is to get to the right command family, attach the right global flags, inspect the target install first, and avoid reckless write operations.

## Use This Skill For

- checking whether a target install is healthy and reachable with `wp`
- plugin and theme management
- users, roles, comments, posts, pages, terms, and media operations
- options, transients, rewrites, cron, and cache-related site work
- core version, update, checksum, and maintenance tasks
- database export, import, and search-replace work
- multisite-aware administration when `--url` matters

## Do Not Use This Skill For

- REST-only integrations where the caller has HTTP access but not shell access
- building custom WP-CLI commands or packages
- blind destructive operations without a read-first pass or backup path

## Workflow

### 1. Inspect The Install First

Start with:

```bash
scripts/inspect-install.sh --path /srv/www/site
scripts/inspect-install.sh --path /srv/www/site --url https://example.com
```

This checks that `wp` exists, confirms the path looks like a WordPress install, and prints useful status for core, URLs, plugins, and themes.

If you need the live command tree:

```bash
scripts/list-commands.sh
scripts/list-commands.sh --group plugin
```

### 2. Choose The Right Command Family

Read [references/command-families.md](references/command-families.md).

Default mapping:

- core health or updates: `core`
- installed code: `plugin`, `theme`, `language`
- content and taxonomy: `post`, `page`, `comment`, `term`, `category`, `tag`
- accounts and permissions: `user`, `role`, `cap`, `super-admin`
- config and runtime: `option`, `transient`, `cron`, `rewrite`, `cache`
- database and migration: `db`, `search-replace`
- multisite: `site`, `network`, `super-admin`

### 3. Attach The Right Global Flags

Read [references/global-flags-and-safety.md](references/global-flags-and-safety.md).

Common flags:

- `--path=<path>`
- `--url=<url>`
- `--user=<login>`
- `--ssh=<target>`
- `--http=<url>`
- `--skip-plugins`
- `--skip-themes`
- `--debug`
- `--quiet`
- `--format=json`

### 4. Prefer Read-First Commands

Examples:

```bash
wp plugin list --format=table
wp theme list --format=table
wp option get home
wp core version
wp cron event list
```

Only then move to write operations such as `plugin update`, `search-replace`, `option update`, or `db import`.

### 5. Treat High-Risk Operations As Change Windows

Before destructive work:

- export the database
- use `search-replace --dry-run` when available
- verify the target URL in multisite
- avoid running broad updates without confirming versions and dependencies

## Files

- `scripts/inspect-install.sh`: inspect a target WordPress path with WP-CLI
- `scripts/list-commands.sh`: print `wp help` or `wp help <group>` for live command discovery
- `references/command-families.md`: command family cheat sheet for common WordPress admin tasks
- `references/global-flags-and-safety.md`: global arg patterns, remote execution, and destructive-operation rules
