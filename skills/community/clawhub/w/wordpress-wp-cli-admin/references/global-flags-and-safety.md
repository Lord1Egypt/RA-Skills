# Global Flags And Safety

Primary docs:

- WP-CLI global parameters: <https://developer.wordpress.org/cli/commands/#global-parameters>

## Core Global Flags

Most WordPress admin automation depends on a small set of flags:

- `--path=<path>`: target WordPress install path
- `--url=<url>`: target site in multisite or URL-sensitive contexts
- `--user=<login>`: execute command as a specific WordPress user
- `--ssh=<target>`: execute remotely over SSH
- `--http=<url>`: execute over a remote HTTP transport when supported
- `--skip-plugins`: avoid plugin side effects during diagnosis
- `--skip-themes`: avoid theme side effects during diagnosis
- `--skip-packages`: avoid custom package loading during diagnosis
- `--require=<file>`: preload PHP bootstrap files
- `--exec=<php-code>`: inject small setup code
- `--debug`: expand troubleshooting output
- `--quiet`: suppress noise in automation

## Safe Inspection Pattern

For diagnosis:

```bash
wp --path=/srv/www/site --skip-plugins --skip-themes core version
wp --path=/srv/www/site plugin list --format=table
wp --path=/srv/www/site option get home
```

## High-Risk Commands

Treat these as change-window operations:

- `db import`
- `db reset`
- `search-replace`
- `plugin update --all`
- `theme update --all`
- `core update`
- bulk user or content deletes

## Safer Defaults

- export before import or replace
- prefer `--format=json` for machine parsing
- use `search-replace --dry-run` before live replacement
- confirm `--url` on multisite before changing data
- use `--skip-plugins` and `--skip-themes` during diagnosis when front-end code may break CLI bootstrap

## Remote Rules

For remote execution:

- prefer `--ssh` when shell access exists
- use `--http` only when the target environment is deliberately exposing a remote runner
- keep credentials and SSH keys out of skill folders
