---
name: vikunja
description: Production-oriented Vikunja task/project management skill with deterministic commands and strong validation.
homepage: https://vikunja.io/
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["curl","jq"],"env":["VIKUNJA_URL","VIKUNJA_TOKEN"]}}}
---

# Vikunja (Custom Core)

Production-focused custom Vikunja skill.

## Setup

```bash
export VIKUNJA_URL="https://your-vikunja-host"
export VIKUNJA_TOKEN="<api-or-jwt-token>"
```

Script path:

```bash
{baseDir}/scripts/vikunja.sh
```

## Core task commands

```bash
{baseDir}/scripts/vikunja.sh health
{baseDir}/scripts/vikunja.sh list --project "Inbox" --limit 25
{baseDir}/scripts/vikunja.sh create --project "Inbox" --title "Call vendor" --due "2026-03-15" --priority 4
{baseDir}/scripts/vikunja.sh update --id 123 --title "Updated title" --priority 5 --reminder "2026-03-14"
{baseDir}/scripts/vikunja.sh move --id 123 --project "Ops" --view "Kanban" --bucket "In Progress"
{baseDir}/scripts/vikunja.sh complete --id 123
{baseDir}/scripts/vikunja.sh bulk-update --ids 101,102,103 --priority 3 --done false
```

## Comments

```bash
{baseDir}/scripts/vikunja.sh comments list --task-id 123
{baseDir}/scripts/vikunja.sh comments add --task-id 123 --comment "Initial note"
{baseDir}/scripts/vikunja.sh comments update --task-id 123 --comment-id 9 --comment "Edited note"
{baseDir}/scripts/vikunja.sh comments delete --task-id 123 --comment-id 9
```

## Labels

```bash
# global labels
{baseDir}/scripts/vikunja.sh labels list
{baseDir}/scripts/vikunja.sh labels create --title "blocked" --color "#ff0000"

# task labels
{baseDir}/scripts/vikunja.sh labels list --task-id 123
{baseDir}/scripts/vikunja.sh labels add --task-id 123 --label "blocked"
{baseDir}/scripts/vikunja.sh labels remove --task-id 123 --label-id 4
```

## Assignees

```bash
{baseDir}/scripts/vikunja.sh assignees list --task-id 123
{baseDir}/scripts/vikunja.sh assignees add --task-id 123 --user-id 1
{baseDir}/scripts/vikunja.sh assignees remove --task-id 123 --user-id 1
```

## Views and buckets

```bash
{baseDir}/scripts/vikunja.sh views list --project "Inbox"
{baseDir}/scripts/vikunja.sh views create --project "Inbox" --title "Kanban" --kind kanban

{baseDir}/scripts/vikunja.sh buckets list --project "Inbox" --view "Kanban"
{baseDir}/scripts/vikunja.sh buckets create --project "Inbox" --view "Kanban" --title "In Progress"
```

## Project webhooks

```bash
{baseDir}/scripts/vikunja.sh webhooks list --project "Inbox"
{baseDir}/scripts/vikunja.sh webhooks create --project "Inbox" --target-url "http://localhost:8787/hook" --event task.created --event task.updated
{baseDir}/scripts/vikunja.sh webhooks delete --project "Inbox" --webhook-id 7
```

## Attachments

```bash
{baseDir}/scripts/vikunja.sh attachments list --task-id 123
{baseDir}/scripts/vikunja.sh attachments upload --task-id 123 --file /tmp/proof.pdf
{baseDir}/scripts/vikunja.sh attachments download --task-id 123 --attachment-id 44 --output /tmp/proof-copy.pdf
{baseDir}/scripts/vikunja.sh attachments delete --task-id 123 --attachment-id 44
```

## Relations

```bash
{baseDir}/scripts/vikunja.sh relations add --task-id 123 --other-task-id 456 --kind blocks
{baseDir}/scripts/vikunja.sh relations remove --task-id 123 --other-task-id 456 --kind blocks
```

## Saved filters

```bash
{baseDir}/scripts/vikunja.sh filters list
{baseDir}/scripts/vikunja.sh filters create --title "Today High" --filter 'done = false && priority >= 4 && due_date < now/d + 1d'
{baseDir}/scripts/vikunja.sh filters get --id 3
{baseDir}/scripts/vikunja.sh filters update --id 3 --title "Today Critical"
{baseDir}/scripts/vikunja.sh filters delete --id 3
```

## Notifications + subscriptions

```bash
{baseDir}/scripts/vikunja.sh notifications list
{baseDir}/scripts/vikunja.sh notifications mark --id 8
{baseDir}/scripts/vikunja.sh notifications mark

{baseDir}/scripts/vikunja.sh subscriptions subscribe --entity project --entity-id 12
{baseDir}/scripts/vikunja.sh subscriptions unsubscribe --entity project --entity-id 12
```

## API tokens

```bash
{baseDir}/scripts/vikunja.sh tokens list
{baseDir}/scripts/vikunja.sh tokens create --title "automation" --expires-at "2026-12-31" --permissions-json '{"tasks":["read_all"]}'
{baseDir}/scripts/vikunja.sh tokens delete --token-id 5
```

## Smoke test harness

```bash
# example (optional): source your local env helper file
# source ~/.config/vikunja/.vikunja_skill_env
export VIKUNJA_URL VIKUNJA_TOKEN
{baseDir}/scripts/test-smoke.sh
```
