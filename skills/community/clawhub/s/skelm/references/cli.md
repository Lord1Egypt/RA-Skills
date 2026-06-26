# CLI Reference

Source of truth is `skelm --help`. This file mirrors the current output.

## Global usage

```
skelm run <workflow.mts|workflow.ts> [flags]
skelm list [--json]
skelm describe <workflow> [--json | --format mermaid]
skelm history [--workflow <id>] [--last <n>] [--run <id>] [--events] [--json]
skelm workspace <list|show|clean> [args]
skelm gateway <start|stop|pause|resume|reload|status|install|uninstall> [flags]
skelm audit query [flags]
skelm secrets <get|set|list> [args]
skelm debug <breakpoints|add|remove|runs|release> [args]
skelm sessions <list|prune> [--expired] [--older-than-ms <ms>] [--json]
skelm schedule <add|list|stop|fire> [args]
skelm acp serve
skelm init [<dir>] [--force]
skelm --version
skelm --help
```

## `skelm run`

```
skelm run <workflow.mts|workflow.ts> [flags]

  --input <json>          Input JSON (single argument)
  --input-file <path>     Input from a file
  --input-stdin           Read input JSON from stdin
  --events <fmt>          human (default) | json | none
```

stdout receives the workflow's final output as JSON. stderr receives human progress lines.

## `skelm list`

```
skelm list [--json]
```

Lists all discovered pipeline files. Respects `registries.workflows.glob` in `skelm.config.mts`.

## `skelm describe`

```
skelm describe <workflow> [--json | --format mermaid]

  --json                  Write the workflow graph as JSON
  --format <fmt>          human (default) | mermaid
```

## `skelm history`

```
skelm history [flags]

  --workflow <id>         Filter runs by workflow id
  --last <n>              Limit results (default: 20)
  --run <id>              Show one run in detail
  --events                When used with --run, write persisted events to stderr
  --json                  Write history output as JSON
```

## `skelm workspace`

```
skelm workspace list [--json]
skelm workspace show <workflow-id> <name> [--json]
skelm workspace clean <workflow-id> <name> --force
```

## `skelm gateway`

```
skelm gateway start --foreground         Run the gateway in this process
skelm gateway status [--json]            Show running pid / url / state
skelm gateway stop                       SIGTERM the running gateway
skelm gateway reload                     SIGHUP the running gateway (hot-reload config)
skelm gateway install   --systemd        Write ~/.config/systemd/user/skelm-gateway.service
skelm gateway uninstall --systemd        Remove the systemd unit file
```

`pause` and `resume` require the HTTP control surface: `POST /gateway/pause` or `/gateway/resume`.

## `skelm audit`

```
skelm audit query [--run <runId>] [--actor <name>] [--action <type>]
                  [--since <ISO8601>] [--until <ISO8601>] [--limit <n>] [--json]
```

Queries the tamper-evident audit log written by the gateway.

## `skelm secrets`

```
skelm secrets list [--json]
skelm secrets get <name> [--json]
skelm secrets set <name> --value <value> [--json]
```

## `skelm schedule`

```
skelm schedule list [--json]
skelm schedule add <workflow-id> [--id <id>] [--json]
  --cron <expr>           Cron expression (e.g. '*/5 * * * *')
  --every-ms <ms>         Interval in milliseconds
  --webhook <path>        Webhook path (e.g. /my-hook)
  --at <iso8601>          Fire once at a specific time
  --input <json>          Input JSON passed to the workflow run
  --overlap skip|queue|cancel  Overlap policy (default: skip)
skelm schedule stop <id> [--json]
skelm schedule fire <id> [--json]
```

## `skelm debug`

```
skelm debug breakpoints [--json]    List active step-id breakpoints
skelm debug add <stepId>            Add a breakpoint at a step id
skelm debug remove <stepId>         Remove a breakpoint
skelm debug runs [--json]           List runs paused at a breakpoint
skelm debug release <runId>         Release a paused run
```

## `skelm sessions`

```
skelm sessions list [--json]
skelm sessions prune [--expired] [--older-than-ms <ms>] [--json]
```

## `skelm approvals`

```
skelm approvals list [--json]
skelm approvals approve <id> [--reason <text>] [--approver <name>] [--json]
skelm approvals deny    <id> [--reason <text>] [--approver <name>] [--json]
```

## `skelm init`

```
skelm init [<dir>] [--force]
```

Scaffolds a new project under `<dir>` (defaults to `.`). Creates `package.json`, `tsconfig.json`, `skelm.config.mts`, `workflows/hello.workflow.mts`, `.gitignore`, and `README.md`. `--force` allows init into a non-empty directory.

`skelm init` forces `"type": "module"` in the merged `package.json` so Node's native loader handles `.mts` files regardless of what `npm init` wrote.

## `skelm validate`

```
skelm validate <pipeline.mts|pipeline.ts> [--json]
```

Static check that the pipeline imports cleanly and its declared schemas/steps are well-formed. No runtime side effects.

## `skelm logs`

```
skelm logs [--lines <n>] [--since <iso>] [--level <lvl>] [--filter <s>] [--json]
```

Streams structured logs from a running gateway.

## Exit codes

| Code | Meaning                    |
|------|----------------------------|
| 0    | ok                         |
| 1    | CLI error                  |
| 2    | schema validation failure  |
| 3    | run failed (step error)    |
| 4    | cancelled                  |
| 5    | wait timeout               |
| 6    | permission denied          |
| 7    | step timeout               |
