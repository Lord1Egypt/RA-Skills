# Report Definition

This file defines the canonical shape for a saved recurring-report definition.

The goal is stability:
- the user describes the report through conversation
- the agent sharpens the report into locked data sources, UI constraints, and an execution brief
- the agent generates a preview for human approval
- the agent pins the locked subtree and any referenced query files with hashes
- the final approved definition is saved
- OpenClaw cron reuses that saved definition on every recurring run

## Required top-level fields

| Field | Type | Notes |
|---|---|---|
| `schemaVersion` | integer | Contract version for migration and validation |
| `reportId` | string | Stable machine identifier |
| `name` | string | Human-readable report name |
| `purpose` | string | Business purpose and audience |
| `owner` | object | Human or team responsible for the report |
| `status` | string | `draft`, `enabled`, `paused`, or `archived` |
| `schedule` | object | Timezone plus machine-readable trigger and derived summary |
| `delivery` | object | Channel plus explicit target |
| `output` | object | Artifact type and naming rules |
| `dataSources` | array | Locked data sources, queries, or dataset refs |
| `uiDefinition` | object | High-level presentation guidance and must-have constraints |
| `executionPrompt` | string | The sharpened prompt that the cron executes |
| `runtimeGuards` | object | Host-enforced safety rules for runtime AI |

For `enabled` and `paused` reports, also require:
- `preview`
- `approval`
- `integrity`
- `automation`
- `verification`

## Canonical JSON shape

```json
{
  "schemaVersion": 1,
  "reportId": "weekly-sales-summary",
  "name": "Weekly Sales Summary",
  "purpose": "Send sales leadership a Monday morning summary of revenue, volume, and region trends.",
  "owner": {
    "id": "sales-director",
    "displayName": "Sales Director"
  },
  "status": "enabled",
  "schedule": {
    "timezone": "Africa/Casablanca",
    "summary": "Every Monday at 08:00",
    "trigger": {
      "type": "weekly",
      "days": ["MON"],
      "time": "08:00"
    }
  },
  "delivery": {
    "channel": "email",
    "target": {
      "to": ["sales@example.com"],
      "cc": []
    },
    "definition": {
      "subject": "Weekly Sales Summary",
      "bodyTemplate": "Please find attached the weekly sales summary."
    },
    "policy": {
      "allowedDomains": ["example.com"]
    }
  },
  "output": {
    "type": "pdf",
    "filenameTemplate": "Weekly Sales Summary - {{ run_date }}.pdf"
  },
  "dataSources": [
    {
      "id": "weekly-sales",
      "backend": "mssql",
      "purpose": "Primary weekly sales metrics by region and product line.",
      "queryFileSha256": "<sha256-of-sql-file>",
      "definition": {
        "queryFile": "sql/reports/weekly_sales_summary.sql",
        "parameters": {
          "period": "current-week"
        }
      }
    },
    {
      "id": "weekly-exceptions",
      "backend": "mssql",
      "purpose": "Exception cases that must be called out separately.",
      "definition": {
        "query": "SELECT Region, Reason, Amount FROM sales.vw_weekly_exceptions WHERE WeekStart = CAST(GETDATE() AS date);",
        "parameters": {
          "period": "current-week"
        }
      }
    }
  ],
  "uiDefinition": {
    "summary": "Executive PDF with a short narrative, KPI strip, one chart, and one exceptions table.",
    "mustInclude": [
      "Show numeric values directly on the chart.",
      "Mention the approved exclusions explicitly in the narrative.",
      "Keep the report under two pages."
    ],
    "components": [
      {
        "kind": "kpi-strip",
        "title": "Weekly KPIs",
        "instructions": "Include revenue, volume, and average order value."
      },
      {
        "kind": "bar-chart",
        "title": "Revenue by Region",
        "instructions": "Sort descending by revenue and display values on the bars."
      },
      {
        "kind": "table",
        "title": "Top Exceptions",
        "instructions": "Show the 10 largest exceptions with region and reason."
      }
    ],
    "dynamicLayout": false
  },
  "executionPrompt": "Use only the approved data sources in this definition. Do not change the query logic, exclusions, or delivery target. Generate the PDF in French, keep the narrative concise, include the required chart labels and values, and deliver it to the approved email recipients.",
  "runtimeGuards": {
    "treatDataAsUntrusted": true,
    "allowDataDrivenToolCalls": false,
    "allowDataDrivenRecipients": false,
    "enforceApprovedDeliveryTarget": true
  },
  "preview": {
    "artifactRef": "exports/reports/previews/weekly-sales-summary/preview.pdf",
    "summary": "Preview approved by Sales Director on 2026-04-15."
  },
  "approval": {
    "approvedAt": "2026-04-15T14:35:00Z",
    "approvedBy": {
      "id": "sales-director",
      "displayName": "Sales Director"
    },
    "approvedSubtreeSha256": "<sha256-of-locked-subtree>"
  },
  "integrity": {
    "lockedSubtreeSha256": "<sha256-of-locked-subtree>"
  },
  "automation": {
    "platform": "openclaw",
    "kind": "cron",
    "jobId": "cron_weekly_sales_summary",
    "sessionTarget": "isolated"
  },
  "verification": {
    "activationCheckAt": "2026-04-15T14:40:00Z",
    "activationCheckMode": "isolated",
    "environmentFingerprint": "skills:chart-mpl,imap-smtp-mail,pdf-report",
    "verifiedSubtreeSha256": "<sha256-of-locked-subtree>"
  },
  "metadata": {
    "createdAt": "2026-04-15T14:30:00Z",
    "updatedAt": "2026-04-15T14:40:00Z",
    "lastRunAt": null,
    "nextRunAt": null,
    "lastStatus": null,
    "failureReason": null
  }
}
```

## Field rules

### `reportId`

- Use lowercase letters, digits, hyphens, or underscores.
- Keep it stable across updates.
- Do not derive it from volatile details like the current date.

### `schemaVersion`

- Use `1` for this package.
- Bump it only when the definition contract changes in a way that requires migration logic.

### `status`

Allowed values:
- `draft`
- `enabled`
- `paused`
- `archived`

Recommended lifecycle:
- use `draft` before approval
- switch to `enabled` only after approval, integrity refresh, activation check, save, and cron creation
- use `paused` for temporary suspension after a report has already been approved and wired
- use `archived` when the user explicitly retires the report

### `schedule`

The schedule must contain:
- `timezone`
- `summary`
- `trigger`

The `trigger` object is the source of truth.
The `summary` value must be derived from the trigger, not independently authored.

Supported trigger shapes in this package:
- `hourly`: `trigger.type = "hourly"`, optional `intervalHours`, optional `minute`
- `daily`: `trigger.type = "daily"`, required `time`
- `weekly`: `trigger.type = "weekly"`, required `days[]`, required `time`
- `monthly`: `trigger.type = "monthly"`, required `dayOfMonth`, required `time`

Canonical summary forms:
- hourly: `Every hour at minute 00` or `Every 4 hours at minute 15`
- daily: `Every day at 08:00`
- weekly: `Every Monday at 08:00`
- monthly: `Day 1 of every month at 08:00`

Time values must use `HH:MM` 24-hour format.
Timezone values must use valid IANA names such as `Africa/Casablanca` or `Europe/Paris`.

### `delivery`

The delivery target must be explicit. Examples:
- email recipients
- target conversation id
- destination folder
- webhook endpoint alias

Do not leave delivery implicit or "same as last time".

Supported delivery channels in this package:
- `email`: `target.to[]` or `target.contact`
- `conversation`: `target.conversationId` or `target.threadId`
- `thread`: `target.threadId` or `target.conversationId`
- `webhook`: `target.endpointAlias` or `target.url`
- `folder`: `target.path`

Safety floor enforced by the validator:
- email addresses must be syntactically valid
- `bcc` is not allowed in this package
- email delivery must include a subject
- `conversation` and `thread` delivery must include `delivery.definition.messageTemplate`
- webhook URLs must use HTTPS and must not target localhost or private/link-local/loopback/reserved IPs
- folder paths must not contain parent-directory traversal

`delivery.policy.allowedDomains[]` is optional. When present, it must be non-empty and every email recipient must match it.
`delivery.definition.bodyTemplate` is optional in this package.
`delivery.definition.messageTemplate` is the caption sent alongside the artifact on `conversation` and `thread` channels. It must identify the report to the reader (for example: `"Rapport Top 5 clients CA TTC 2026 — {{ run_date }}"`). Without it, cron runs would drop a bare file into the chat.

For `conversation` and `thread` channels, default `target.conversationId` (or `threadId`) to the conversation where the user framed the request. Only target a different conversation after explicit user confirmation — silently re-targeting is a cross-delivery leak.

### `output`

The output object defines the report artifact, for example:
- `text`
- `pdf`
- `excel`
- `image`
- `markdown`

If the artifact name matters, store a deterministic `filenameTemplate`.
Prefer a human-readable filename — recipients see it in their inbox or chat (for example: `"Weekly Sales Summary - {{ run_date }}.pdf"`). Spaces are fine; avoid characters that break URLs or shells such as `/`, `\`, `:`, `?`, `*`, `"`, `<`, `>`, `|`.
If `reportId` or `name` already contains a year, omit the year from `filenameTemplate` to avoid duplication such as `Weekly Sales Summary 2026 - 2026-04-17.pdf`.
Do not over-model output-specific mechanics in the definition unless the user explicitly needs fixed structure.

### `dataSources`

The `dataSources` array captures the locked business data contract.

Each entry must contain:
- `id`
- `backend`
- `purpose`
- `definition`

Do not store a vague business request in place of real data logic.
The `definition` value must be an object, not a scalar or free-form note.

Recommended deterministic keys include:
- `query`
- `queryFile`
- `storedProcedure`
- `datasetRef`
- `sourceRef`
- `pipelineRef`
- `jobRef`
- `fileRef`
- `apiRequestRef`

Optional companion fields may include:
- `parameters`

Rules:
- when `queryFile` is used, also store `queryFileSha256` on the same data-source object
- referenced query files must exist at validation time
- `parameters`, when present, must be an object
- prefer parameterized queries or stored procedures over interpolated inline SQL where possible

### `uiDefinition`

The `uiDefinition` object captures the high-level presentation contract.

Required:
- `summary`

Recommended companion fields:
- `mustInclude`
- `constraints`
- `components`
- `dynamicLayout`

Keep `uiDefinition` concise. Capture must-haves such as:
- chart type intent
- whether labels or values must be visible
- required sections
- ordering or top-N rules
- totals, percentages, or formatting constraints
- whether layout can be dynamic

`uiDefinition` is guidance for runtime AI, not a deterministic renderer schema.
Do not pretend it guarantees exact pixel-perfect output.

### `executionPrompt`

The `executionPrompt` is the sharpened runtime brief for the OpenClaw cron.

It should:
- tell runtime AI to use only the approved data sources
- preserve the approved exclusions and business rules
- preserve the approved delivery target
- describe the final output expectations clearly

It should not:
- ask runtime AI to rediscover the data logic
- depend on the preview artifact as runtime input
- contain volatile run-specific facts that belong in data or metadata

### `runtimeGuards`

`runtimeGuards` captures the minimum runtime safety contract for recurring reports.

Required values in this package:
- `treatDataAsUntrusted = true`
- `allowDataDrivenToolCalls = false`
- `allowDataDrivenRecipients = false`
- `enforceApprovedDeliveryTarget = true`

Host automation should enforce these rules outside the prompt itself.

### `preview`

`preview` is optional while the report is still in `draft`, and required for `enabled` or `paused`.

Required field:
- `artifactRef` — path to the generated preview file (PDF, image, etc.) that was actually shown to the approver. The file must exist on disk at validation time.

Optional metadata:
- `summary` — short human note about the approval step (who approved, when).

A preview is an artifact, not a narrative. A text-only preview record does not satisfy this contract — the validator will reject `preview` without a real file on disk.
The preview is for human approval, not for runtime execution.

### `approval`

`approval` is required for `enabled` or `paused`.

Minimum fields:
- `approvedAt`
- `approvedBy`
- `approvedSubtreeSha256`

`approvedBy` must contain at least `id` or `displayName`.
`approvedSubtreeSha256` must match `integrity.lockedSubtreeSha256`.

### `integrity`

`integrity` is required for `enabled` or `paused`.

Minimum fields:
- `lockedSubtreeSha256`

The locked subtree hash is computed over the canonical JSON for:
- `schedule`
- `delivery`
- `output`
- `dataSources`
- `uiDefinition`
- `executionPrompt`
- `runtimeGuards`

This hash exists to detect silent tampering after approval.
It provides tamper evidence inside the definition file, not a cryptographic signature from an external trust system.
It intentionally covers the locked runtime contract, not descriptive fields such as `owner` or `purpose`.
The canonical byte representation used by this package is the Python validator's `json.dumps(..., ensure_ascii=True, sort_keys=True, separators=(",", ":"))`.
Non-Python consumers should either call the same validator or reproduce that exact byte contract before recomputing hashes.

### `automation`

`automation` is optional until the cron is created.

Once the cron exists, store OpenClaw metadata here:
- `platform = "openclaw"`
- `kind = "cron"`
- `jobId`
- `sessionTarget`

Prefer `sessionTarget = "isolated"` for recurring reports unless the host agent has a specific reason to use another mode.

### `verification`

`verification` is required for `enabled` or `paused`.

Minimum fields:
- `activationCheckAt`
- `activationCheckMode`
- `environmentFingerprint`
- `verifiedSubtreeSha256`

`activationCheckMode` must match `automation.sessionTarget`.
`environmentFingerprint` must use the canonical format `skills:<name>[,<name>...]`, sorted lexicographically and without duplicates.
`verifiedSubtreeSha256` must match `integrity.lockedSubtreeSha256`.

Use `verification` to record that the approved definition was exercised in the same runtime mode that the cron will use.
The current fingerprint tracks skill names only. It proves that the same named skills were present, not that exact skill versions or behaviors were identical.
The host runner should recompute the environment fingerprint and all referenced hashes on every cron run and fail closed on mismatch.

## Storage convention

Use a private configuration path for persisted report definitions, for example:
- `config/scheduled-reports/<reportId>.json`

Keep preview artifacts in a private path, for example:
- `exports/reports/previews/<reportId>/`

Do not store persisted report definitions under conversational `memory/` paths.
Do not commit sensitive definitions or previews to shared repositories without explicit approval and access controls.

## Validation command

Validate a definition before activation:

```bash
python3 skills/scheduled-reports/scripts/validate_report_definition.py \
  --input config/scheduled-reports/weekly-sales-summary.json
```

The validator checks:
- required fields
- allowed status values
- supported trigger types and machine-readable schedule details
- canonical schedule summaries
- valid IANA timezone names
- allowed delivery channels and safe delivery targets
- non-empty output type
- structured locked data sources
- query-file existence and hash matches when `queryFile` is used
- structured high-level UI definition
- required runtime guard values
- non-empty execution prompt
- optional OpenClaw automation metadata when present
- canonical environment fingerprint shape
- approval and verification hashes bound to the locked-subtree hash
- required approval, integrity, automation, preview, and verification metadata for `enabled` and `paused`
- integrity hash match for the locked subtree
