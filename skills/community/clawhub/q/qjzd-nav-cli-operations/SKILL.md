---
name: qjzd-nav-cli-operations
version: 1.0.0
description: Use when managing QJZD Nav backups, restore, and site settings including uploading background images, logos, and favicons.
references:
  - ../qjzd-nav-cli
  - ../qjzd-nav-cli-auth
metadata:
  openclaw:
    category: developer-tools
    requires:
      bins: ["qjzd-nav"]
    cliHelp: "qjzd-nav backup --help && qjzd-nav settings --help"
---

# QJZD Nav CLI Operations

Use this skill for `qjzd-nav backup` and `qjzd-nav settings`.

If auth may not be ready, check `qjzd-nav auth current` first or load `qjzd-nav-cli-auth`.

## Commands

```bash
qjzd-nav backup --help
qjzd-nav settings --help
```

## Backups

List backups:

```bash
qjzd-nav backup list
qjzd-nav backup list --json
```

Export backup (JSON format):

```bash
qjzd-nav backup export
qjzd-nav backup export --output ./backup.json
qjzd-nav backup export --json
```

Export backup with assets (ZIP format):

```bash
qjzd-nav backup export-zip
qjzd-nav backup export-zip --output ./backup.zip
```

Download a backup file:

```bash
qjzd-nav backup download --filename "qjzd-nav-backup-2024-01-01.json" --output ./download.json
```

Delete a backup:

```bash
qjzd-nav backup delete --filename "qjzd-nav-backup-2024-01-01.json"
```

Import backup (JSON only):

```bash
qjzd-nav backup import --file ./backup.json
```

## Settings

Get current settings:

```bash
qjzd-nav settings get
qjzd-nav settings get --json
```

Update settings:

```bash
qjzd-nav settings update --site-title "My Nav" --site-subtitle "Links"
qjzd-nav settings update --logo-icon "i-lucide-star"
qjzd-nav settings update --background-overlay 50
qjzd-nav settings update --show-shortcut-hints --show-edit-button
```

Upload file (background, logo, or favicon):

```bash
# Upload and set as background image (default overlay: 20%)
qjzd-nav settings upload --type background --file ./bg.jpg

# Upload and set as logo
qjzd-nav settings upload --type logo --file ./logo.png

# Upload and set as favicon
qjzd-nav settings upload --type favicon --file ./favicon.ico
```

Supported file types:

- Background: PNG, JPG, WEBP
- Logo: PNG, JPG, SVG, ICO
- Favicon: PNG, SVG, ICO

## Settings Fields

| Field                    | Type    | Description                                           |
| ------------------------ | ------- | ----------------------------------------------------- |
| `--site-title`           | string  | Site title                                            |
| `--site-subtitle`        | string  | Site subtitle                                         |
| `--logo-icon`            | string  | Lucide icon class (e.g., `i-lucide-compass`)          |
| `--logo-image`           | string  | Logo image URL                                        |
| `--favicon`              | string  | Favicon URL                                           |
| `--background-image`     | string  | Background image URL                                  |
| `--background-overlay`   | number  | Background overlay 0-100 (default: 20 when uploading) |
| `--show-shortcut-hints`  | boolean | Show keyboard shortcut hints                          |
| `--sidebar-collapsed`    | boolean | Sidebar default collapsed state                       |
| `--show-edit-button`     | boolean | Show edit button                                      |
| `--show-settings-button` | boolean | Show settings button                                  |

## Rules

- `backup import` only supports JSON format, not ZIP.
- When uploading background, `--background-overlay` defaults to 20%.
- Use `--json` for automation and scripts.
- Backup files are stored on the server with a maximum of 100 backups.
