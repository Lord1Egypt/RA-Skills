---
name: wordpress-wp-cli-internal-api
description: Build, inspect, and extend WP-CLI command code using the documented stable internal API. Use when the task involves custom WP-CLI commands, package bootstraps, command registration, hooks, output helpers, internal execution helpers, or PHP code that calls `WP_CLI::*` or `WP_CLI\\Utils::*`.
metadata: {"openclaw":{"emoji":"⚙️"}}
---

# WordPress WP-CLI Internal API

Use this skill when you are writing WP-CLI itself, not merely operating WordPress through `wp`.

The official internal API reference exposes a stable surface for command registration, logging, hooks, execution, and output formatting. This skill keeps that stable surface close at hand and gives you a quick command skeleton generator.

## Use This Skill For

- building custom WP-CLI commands
- reviewing command classes that call `WP_CLI::add_command()`
- choosing between `WP_CLI::log()`, `success()`, `warning()`, and `error()`
- formatting output with `WP_CLI\Utils\format_items()`
- running one WP-CLI command from another with `WP_CLI::runcommand()`
- using hooks such as `WP_CLI::add_hook()` and `WP_CLI::do_hook()`

## Do Not Use This Skill For

- normal site administration where a stock WP-CLI command already exists
- REST route implementation or review
- plugin business logic that has nothing to do with WP-CLI command entrypoints

## Workflow

### 1. Stay On The Stable Surface

Read [references/stable-internal-api.md](references/stable-internal-api.md).

Start from the officially documented stable methods instead of undocumented internals.

### 2. Render A Command Skeleton

Use:

```bash
scripts/render-command-skeleton.sh --command acme report --class Acme_Report_Command
scripts/render-command-skeleton.sh --command acme report --class Acme_Report_Command --write /tmp/report-command.php
```

This gives you a minimal command class that already uses:

- `WP_CLI::add_command()`
- `WP_CLI::success()`
- `WP_CLI\Utils\get_flag_value()`
- `WP_CLI\Utils\format_items()`

### 3. Choose Output And Error Patterns Deliberately

Read [references/command-patterns.md](references/command-patterns.md).

Default rule:

- human progress: `log()` or `line()`
- successful completion: `success()`
- non-fatal concern: `warning()`
- fatal stop: `error()`

### 4. Prefer Internal Execution Helpers Over Shelling Out

If a command needs to trigger another WP-CLI command, prefer:

- `WP_CLI::runcommand()`
- `WP_CLI::launch_self()`

Reach for generic shell execution only when the task is truly outside WP-CLI.

## Files

- `scripts/render-command-skeleton.sh`: render a minimal custom command class and registration stub
- `references/stable-internal-api.md`: grouped stable API surface from the official WP-CLI internal API docs
- `references/command-patterns.md`: practical command-authoring patterns and guardrails
