# Operations Reference

## Paths

```powershell
$SkillRoot = Join-Path $HOME '.agents\skills\setup-obsidian-arxiv-daily'
$Installer = Join-Path $SkillRoot 'scripts\install_arxiv_daily.py'
$TaskScript = Join-Path $SkillRoot 'scripts\register_scheduled_task.ps1'
```

Resolve the Vault before using either script:

```powershell
$Vault = (Resolve-Path -LiteralPath 'D:\path\to\Obsidian Vault').Path
```

## Install

Preview a clean installation:

```powershell
python $Installer --vault $Vault --project-name arxiv-daily --dry-run
```

Install:

```powershell
python $Installer --vault $Vault --project-name arxiv-daily
```

Preview an update to an existing project:

```powershell
python $Installer --vault $Vault --project-name arxiv-daily --dry-run --force
```

After explicit overwrite approval, update packaged files:

```powershell
python $Installer --vault $Vault --project-name arxiv-daily --force
```

`--force` copies packaged files only. It does not remove or replace content
under `papers`, `daily`, `archive`, or `logs`.

## Configure

Edit `<vault>\<project-name>\config.yaml`. The default configuration:

```yaml
retention_days: 90
per_field_limit: 10
lookback_days: 7
sort_by: submittedDate
sort_order: descending
summary_enabled: true
summary_provider: deepseek
deepseek_model: deepseek-v4-pro
deepseek_base_url: https://api.deepseek.com
request_timeout_seconds: 60
fields:
  - name: LLM Agent
    query: '"large language model" AND agent'
  - name: RAG
    query: 'retrieval augmented generation OR RAG'
  - name: AI Safety
    query: 'AI safety OR alignment'
```

Preserve the indentation and the `name`/`query` pair for each field. The parser
supports this intentionally small YAML subset; do not add arbitrary nested
YAML.

## DeepSeek Credential

The collector reads `DEEPSEEK_API_KEY` from the process environment. Never put
the value in `config.yaml`, a PowerShell script, task arguments, Markdown, or
logs.

Check presence without revealing the value:

```powershell
if ([string]::IsNullOrWhiteSpace($env:DEEPSEEK_API_KEY)) {
    'DEEPSEEK_API_KEY is not available in this process.'
} else {
    'DEEPSEEK_API_KEY is available.'
}
```

If it is absent, ask the user to configure it through their approved secret or
environment-management method. Installation and tests can continue; production
notes fall back to the original abstract when DeepSeek is unavailable.

## Validate

Run installed unit tests:

```powershell
$Project = Join-Path $Vault 'arxiv-daily'
python -m unittest discover -s (Join-Path $Project 'scripts') -p 'test_*.py'
```

Run a network dry run that writes no project files:

```powershell
& (Join-Path $Project 'scripts\arxiv_daily.ps1') -DryRun -MaxTotal 1
```

Interpret results separately:

- Unit-test failure means the installed program is invalid.
- Dry-run failure can mean network, arXiv, proxy, DNS, or configuration failure.
- Missing DeepSeek credentials do not affect dry-run paper selection because
  summaries are not generated in dry-run mode.

## Schedule

Choose a unique task name per Vault. Preview task registration:

```powershell
& $TaskScript `
  -Vault $Vault `
  -ProjectName 'arxiv-daily' `
  -TaskName 'ObsidianArxivDaily' `
  -At '10:30' `
  -WhatIf
```

If the task name already exists, inspect it before proceeding:

```powershell
$Task = Get-ScheduledTask -TaskName 'ObsidianArxivDaily'
$Info = Get-ScheduledTaskInfo -TaskName 'ObsidianArxivDaily'
$Task.Actions | Format-List Execute,Arguments,WorkingDirectory
$Task.Triggers | Format-List *
$Info | Format-List LastRunTime,LastTaskResult,NextRunTime
```

Register a new task:

```powershell
& $TaskScript `
  -Vault $Vault `
  -ProjectName 'arxiv-daily' `
  -TaskName 'ObsidianArxivDaily' `
  -At '10:30'
```

Only after explicit approval to replace the inspected task:

```powershell
& $TaskScript `
  -Vault $Vault `
  -ProjectName 'arxiv-daily' `
  -TaskName 'ObsidianArxivDaily' `
  -At '10:30' `
  -Force
```

## Verify and Troubleshoot

Inspect the latest log:

```powershell
$LatestLog = Get-ChildItem (Join-Path $Project 'logs') -Filter '*.log' |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
Get-Content -LiteralPath $LatestLog.FullName -Encoding UTF8
```

Expected successful lines:

```text
Run started: fields=<count> existing_ids=<count> max_total=<value>
Run completed: selected=<count> written=<count> archived=<count>
```

Check the daily note and a generated paper with explicit UTF-8 if console
rendering is garbled. Do not assume persisted text is corrupt based only on
PowerShell display.

## Removal Boundary

Before removing an installation, separately confirm:

1. Whether to unregister the exact scheduled task.
2. Whether generated `papers`, `daily`, `archive`, and `logs` must be retained.

Never recursively delete the project as part of an update or troubleshooting
operation.
