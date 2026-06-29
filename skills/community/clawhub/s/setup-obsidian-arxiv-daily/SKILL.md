---
name: setup-obsidian-arxiv-daily
description: Use when installing, migrating, updating, validating, troubleshooting, or scheduling an automated arXiv paper digest inside an Obsidian Vault on Windows.
---

# Setup Obsidian arXiv Daily

## Overview

Deploy the packaged arXiv collector into a confirmed Obsidian Vault, validate
the installation, and optionally register a Windows daily task. Preserve
generated notes and keep credentials outside project files.

## Core Workflow

1. Resolve the target Vault to an absolute path and confirm it exists.
2. Inspect whether `<vault>\<project-name>` already exists.
3. Run `scripts/install_arxiv_daily.py` with `--dry-run`.
4. For an existing project, explain that `--force` updates packaged files while
   preserving `papers`, `daily`, `archive`, and `logs`. Obtain explicit approval
   before using `--force`.
5. Install and edit only the requested values in the generated `config.yaml`.
6. Run the installed unit tests.
7. Run the installed PowerShell wrapper with `-DryRun -MaxTotal 1`.
8. Register a scheduled task only if the user requested scheduling.
9. Verify exact paths, test counts, task state, next run time, and recent logs.

Read [operations.md](references/operations.md) for exact commands and
configuration details.

## Safety Rules

- Never copy historical papers, daily notes, archives, logs, or caches from
  another Vault.
- Never write, print, log, or embed `DEEPSEEK_API_KEY`. Verify only whether it
  is present in the execution environment.
- Do not overwrite an existing project without explicit approval.
- Do not replace an existing scheduled task without confirming its exact task
  name, action path, target Vault, and receiving explicit approval for `-Force`.
- Use `-WhatIf` when validating task registration.
- Treat network dry-run failure separately from installation failure: unit tests
  must still run without network access.
- Do not claim success until the fresh installed-copy tests and requested task
  inspection have completed.

## Configuration Boundaries

Change only keys requested by the user:

- `retention_days`
- `per_field_limit`
- `lookback_days`
- `sort_by`
- `sort_order`
- `summary_enabled`
- `summary_provider`
- `deepseek_model`
- `deepseek_base_url`
- `request_timeout_seconds`
- `fields`

Keep `deepseek_base_url` on `https://api.deepseek.com`; the collector rejects
other hosts. Dataview is required only for rendering `dashboard.md`, not for
collection or Markdown generation.

## Bundled Resources

- `scripts/install_arxiv_daily.py`: bounded preview/install/update utility.
- `scripts/register_scheduled_task.ps1`: guarded Windows task registration.
- `assets/arxiv-daily/`: tested collector, wrapper, tests, configuration,
  dashboard, and templates.
- `tests/`: installer and task-registration regression tests.
