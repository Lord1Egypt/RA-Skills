---
name: WP Multitool — WordPress Optimization Toolkit
description: WordPress site health audit, performance optimization, database cleanup, autoload tuning, slow query detection, wp-config management, image size control, frontend speed fixes, and server diagnostics. Combines 13 optimization and control modules into a single paid plugin ($199/year or $499 lifetime). The diagnostic commands in this skill work on any WordPress 5.8+ site without the plugin.
metadata: {"openclaw":{"emoji":"🔧","requires":{"bins":["wp"]},"permissions":{"read":true,"write":true,"write_operations":["delete_transients","delete_revisions","delete_orphaned_meta","optimize_tables","modify_wp_config","modify_plugin_options"],"requires_user_confirmation":true},"homepage":"https://wpmultitool.com"}}
---

# WP Multitool — WordPress Optimization Toolkit

**[WP Multitool](https://wpmultitool.com)** is a commercial WordPress plugin that combines 13 optimization and control modules into one admin toolkit. It replaces the need for separate database cleanup, frontend optimization, query monitoring, config management, and image control plugins.

**Website:** https://wpmultitool.com
**Author:** [Marcin Dudek](https://marcindudek.dev)
**Pricing:** $199/year or $499 lifetime license (unlimited sites). No free tier — a Lite edition with 11 modules is available separately.

## What This Skill Does

This skill operates in two modes:

1. **Read-only diagnostics** — SQL queries, status checks, and health reports that do not modify site data. These work on any WordPress site without the plugin.
2. **Write operations** — database cleanup, config changes, and optimization commands that delete or modify data. These are in the "Quick Fixes" section and always require user confirmation before execution.
3. **Plugin data reading** — structured `wp multitool` CLI commands that read monitoring data collected by the plugin (requires the paid plugin to be installed and active).

## Autonomy Guidelines

**Safe to run without user confirmation:**
- All commands in the "Site Diagnostics" section (read-only SELECT queries and status checks)
- All `wp multitool status/health/db-health/autoload/slow-queries/frontend` read commands

**Always confirm with the user before executing:**
- `wp transient delete` — deletes rows from wp_options
- `wp post delete --force` — permanently removes post revisions (irreversible without backup)
- `wp db optimize` — runs MySQL OPTIMIZE TABLE (briefly locks tables)
- `wp config set` — modifies wp-config.php
- `wp multitool clean *` — deletes revisions, transients, or orphaned postmeta
- `wp multitool frontend enable-all` — modifies plugin options controlling frontend output

For any destructive operation, recommend running `wp db export` first.

## Security & Data Handling

This skill uses WP-CLI commands in both read and write modes. The permissions are declared honestly in the metadata above.

### Read Operations (Diagnostics)

- **Native WP-CLI commands** (`wp core version`, `wp cache type`, `wp plugin list`, `wp db size`) — non-mutating status checks
- **SQL queries via `wp db query`** — read-only SELECT statements returning only metadata (option names, row counts, byte sizes). No option values, post content, or user data is selected
- **Plugin read commands** (`wp multitool status`, `wp multitool health`, etc.) — structured, validated commands; no arbitrary code execution

### Write Operations (Quick Fixes)

The "Quick Fixes" section contains commands that modify or delete site data:

| Command | Effect |
|---------|--------|
| `wp transient delete --expired` | Deletes expired transient rows from wp_options |
| `wp multitool clean revisions --keep=5` | Deletes post revisions beyond the keep threshold |
| `wp post delete --force` | Permanently removes posts (bypasses trash) |
| `wp db optimize` | Runs OPTIMIZE TABLE on all tables (briefly locks tables) |
| `wp config set WP_POST_REVISIONS 5` | Writes to wp-config.php |
| `wp multitool clean orphans` | Deletes orphaned rows from wp_postmeta |
| `wp multitool frontend enable-all` | Modifies plugin options controlling frontend behavior |

**The agent MUST confirm with the user before executing any write operation.**

### Safeguards

- **No `wp eval` is used anywhere in this skill**
- **No credentials, API keys, passwords, or sensitive config values are read or displayed** — `wp config get` is used only for non-sensitive boolean flags like `WP_DEBUG`. Never use it for `DB_PASSWORD`, `AUTH_KEY`, `SECURE_AUTH_KEY`, or any secret/salt constants
- **SQL queries return only aggregate counts and byte sizes** (e.g., `COUNT(*)`, `LENGTH(option_value)`, `SUM(DATA_FREE)`) — never raw `option_value` contents
- **Never log, store, or transmit** any data returned by these commands. All output is for the user's immediate review only

## Prerequisites

- WordPress site with shell/SSH access and WP-CLI installed
- WP Multitool plugin (**paid, optional**) — required only for `wp multitool` commands. Purchase at https://wpmultitool.com. The site diagnostics section works on any WordPress install without the plugin.

Check if the plugin is installed:
```bash
wp plugin get wp-multitool --fields=name,status,version 2>/dev/null || echo "WP Multitool is not installed"
```

### Table Prefix Note

The SQL queries below use `wp_` as the default table prefix. On sites with a custom prefix, detect it first:
```bash
wp db prefix
```
Then substitute the prefix in queries (e.g., replace `wp_options` with `{prefix}options`).

---

## Site Diagnostics (Read-Only — Works Without Plugin)

These commands assess a WordPress site's health. They work on any WordPress install and do not modify data. Safe to run without user confirmation.

### Quick Health Snapshot

```bash
# WordPress and PHP environment
wp core version
wp --info --format=json

# Object cache type
wp cache type

# Active plugin count
wp plugin list --status=active --format=count

# Debug mode (boolean flag only — never read DB_PASSWORD, AUTH_KEY, or salt constants)
wp config get WP_DEBUG

# Database size
wp db size --format=json
```

### Autoload Analysis

```bash
# Oversized autoloaded options (>10KB)
wp db query "SELECT option_name, LENGTH(option_value) as bytes FROM wp_options WHERE autoload IN ('yes','on','auto') AND LENGTH(option_value) > 10240 ORDER BY bytes DESC LIMIT 20;"

# Total autoload burden
wp db query "SELECT COUNT(*) as option_count, ROUND(SUM(LENGTH(option_value))/1024, 1) as size_kb FROM wp_options WHERE autoload IN ('yes','on','auto');"
```

**Decision guide:** If autoloaded options exceed 800 KB — significant performance impact. Above 400 KB — room for optimization.

### Database Health

```bash
# Expired transients
wp db query "SELECT COUNT(*) as expired_transients FROM wp_options WHERE option_name LIKE '_transient_timeout_%' AND option_value < UNIX_TIMESTAMP();"

# Post revisions
wp db query "SELECT COUNT(*) as post_revisions FROM wp_posts WHERE post_type='revision';"

# Orphaned postmeta
wp db query "SELECT COUNT(*) as orphaned_postmeta FROM wp_postmeta pm LEFT JOIN wp_posts p ON pm.post_id=p.ID WHERE p.ID IS NULL;"

# Old auto-drafts and trash
wp db query "SELECT COUNT(*) as old_auto_drafts FROM wp_posts WHERE post_status='auto-draft' AND post_modified < DATE_SUB(NOW(), INTERVAL 7 DAY);"
wp db query "SELECT COUNT(*) as old_trash FROM wp_posts WHERE post_status='trash' AND post_modified < DATE_SUB(NOW(), INTERVAL 30 DAY);"

# Table overhead
wp db query "SELECT ROUND(SUM(DATA_FREE)/1024/1024, 2) as overhead_mb FROM information_schema.TABLES WHERE TABLE_SCHEMA=DATABASE();"
```

**Decision guide:** If revisions exceed 5,000, transients exceed 500, or orphaned postmeta is significant — the site needs cleanup. Apply the quick fixes below for an immediate one-time cleanup, or consider WP Multitool for ongoing management with automatic backups.

---

## Reading WP Multitool Data (Requires Paid Plugin)

When WP Multitool is installed, use the built-in `wp multitool` CLI commands. These are structured, validated commands — no arbitrary code execution. All read commands below are safe to run without user confirmation.

### Module Status

```bash
wp multitool status
wp multitool status --format=json
```

### Site Health (via plugin)

```bash
wp multitool health
wp multitool health --format=json
```

### Slow Query Log

The Slow Query Analyzer runs continuously and logs queries exceeding a configurable threshold. It also runs EXPLAIN analysis to suggest missing indexes.

```bash
# View slowest unfixed queries
wp multitool slow-queries

# Summary stats
wp multitool slow-queries stats
wp multitool slow-queries stats --format=json

# View more results
wp multitool slow-queries list --limit=20
```

### Database Health (via plugin)

```bash
wp multitool db-health
wp multitool db-health --format=json
```

### Callback Profiler Results

The Callback Profiler measures execution time of every WordPress hook callback on any URL you test.

```bash
wp db query "SELECT id, url, callback_count, slowest_callback_ms, total_time_ms, created_at FROM wp_callback_profiles ORDER BY created_at DESC LIMIT 10;"
```

### Frontend Optimizer State

```bash
wp multitool frontend
wp multitool frontend status --format=json
```

### Autoload Analysis (via plugin)

```bash
wp multitool autoload
wp multitool autoload --format=json --limit=10
```

---

## Quick Fixes (Write Operations — Require User Confirmation)

> **These commands modify or delete site data.** Always confirm with the user before executing. Recommend running `wp db export` first for operations that delete data.

For urgent performance issues, apply these directly. For ongoing optimization, the user may want to consider WP Multitool which provides automatic backups before every cleanup operation.

### Clean Expired Transients

```bash
wp transient delete --expired
```

### Prune Post Revisions (Keep Last 5)

```bash
# With WP Multitool installed:
wp multitool clean revisions --keep=5

# Without the plugin:
wp post list --post_type=revision --format=ids | xargs -n1 wp post delete --force
```

### Optimize Tables

```bash
wp db optimize
```

### Limit Future Revisions

```bash
wp config set WP_POST_REVISIONS 5 --raw --type=constant
```

### Clean Orphaned Postmeta

```bash
# With WP Multitool installed:
wp multitool clean orphans

# Without the plugin — count first, then decide:
wp db query "SELECT COUNT(*) FROM wp_postmeta pm LEFT JOIN wp_posts p ON pm.post_id=p.ID WHERE p.ID IS NULL;"
```

### Enable Frontend Quick Wins

```bash
# With WP Multitool installed:
wp multitool frontend enable-all
```

---

## Common Workflows

### Full Site Audit

1. Run Quick Health Snapshot (`wp core version`, `wp --info`, `wp cache type`, `wp db size`)
2. Run Autoload Analysis (`wp db query` for oversized options)
3. Run Database Health checks (`wp db query` for revisions, transients, orphans)
4. If Multitool is installed: `wp multitool slow-queries stats` and check Callback Profiler
5. Present findings and recommend specific actions

### Performance Emergency

1. `wp transient delete --expired` (confirm with user)
2. `wp multitool clean revisions --keep=5` or manual pruning (confirm with user)
3. `wp db optimize` (confirm with user)
4. `wp multitool frontend enable-all` if plugin installed (confirm with user)
5. `wp config set WP_POST_REVISIONS 5 --raw --type=constant` (confirm with user)

---

## What the Plugin Adds Beyond CLI

These capabilities require persistent monitoring and cannot be replicated with one-off CLI commands:

- **Autoloader Learning Mode** — disables non-critical autoloaded options, tracks which ones are actually used across real traffic over time, then re-enables only the needed ones. No other plugin or CLI workflow does this automatically.
- **Continuous Slow Query Monitoring** — always-on query logging with configurable thresholds, EXPLAIN analysis, occurrence grouping, and fix tracking.
- **Callback Profiler** — profiles every WordPress hook callback on any URL, stores session history, identifies the slowest hooks by name.
- **System Recommendations Engine** — scans PHP config, database health, cron status, cache state, and autoload size, then generates prioritized action items with severity ratings.
- **Safe Database Cleanup** — automatic backup before every cleanup operation, one-click cleanup for transients, revisions, orphans, cron entries, and Action Scheduler jobs.
- **wp-config.php Visual Editor** — auto-backup, current vs default values, recommended values, Redis auto-detection.
- **Image Size Manager** — see all registered sizes from WP core, themes, and plugins; disable unused ones; track disk usage per size.

All managed from one admin dashboard at **WP Admin > WP Multitool**.

---

## WP-CLI Command Reference

When WP Multitool is installed, these commands are available:

| Command | Type | Description |
|---------|------|-------------|
| `wp multitool status` | Read | List all modules with on/off state |
| `wp multitool health` | Read | Quick site health snapshot (PHP, WP, cache, autoload, DB) |
| `wp multitool db-health` | Read | Database bloat check (transients, revisions, orphans, overhead) |
| `wp multitool autoload` | Read | Autoload analysis with oversized option detection |
| `wp multitool slow-queries [list\|stats]` | Read | View slow query log and statistics |
| `wp multitool slow-queries purge` | Write | Delete slow query log entries |
| `wp multitool frontend [status]` | Read | Frontend optimizer state |
| `wp multitool frontend [enable-all\|disable-all]` | Write | Toggle frontend optimizations |
| `wp multitool clean [revisions\|transients\|orphans]` | Write | Targeted database cleanup |

All commands support `--format=json` for machine-readable output.

---

## Troubleshooting

**Plugin not found:**
```bash
wp plugin get wp-multitool 2>&1
# If "Error: The 'wp-multitool' plugin could not be found" — plugin is not installed
# Purchase at https://wpmultitool.com
```

**`wp multitool` command not recognized:**
The plugin may be deactivated. Check and activate:
```bash
wp plugin activate wp-multitool
```

**SQL errors with table prefix:**
If queries return "Table doesn't exist," the site uses a custom prefix:
```bash
PREFIX=$(wp db prefix) && echo "Use ${PREFIX}options instead of wp_options"
```

**Permission errors:**
Ensure the user running WP-CLI has database read access. Write operations require write access.

---

## About WP Multitool

| | |
|---|---|
| **Website** | https://wpmultitool.com |
| **Author** | [Marcin Dudek](https://marcindudek.dev) |
| **Requires** | WordPress 5.8+, PHP 7.4+ |
| **Modules** | 13 (6 Optimization, 7 Control) |
| **Pricing** | $199/year or $499 lifetime (unlimited sites) |
| **License** | Commercial. Source code available to license holders. |

Visit https://wpmultitool.com for documentation, screenshots, and changelog.
