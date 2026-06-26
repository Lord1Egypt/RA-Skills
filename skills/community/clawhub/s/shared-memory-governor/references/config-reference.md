# shared-memory-governor configuration spec

This document explains the JSON configuration used by the `shared-memory-governor` skill.

Use this file as the reference source for:
- configuration review
- field lookup
- status reporting
- maintenance
- schedule consistency checks

## Config file path

Default config file path:

```text
<workspace-parent>/shared-memory/shared-memory.config.json
```

For the current default OpenClaw workspace layout, this resolves to:

```text
/root/.openclaw/shared-memory/shared-memory.config.json
```

Config-related commands may explicitly pass a config path.

Non-config commands in v1 use the active/default config location and do not take `--config`.

If the config location changes, use `init` or `update-config` to apply the change.

---

## Top-level structure

Recommended top-level blocks:

```json
{
  "version": 1,
  "maintainer": {},
  "paths": {},
  "schedules": {},
  "participants": {},
  "attachment": {},
  "sharing": {},
  "readOrder": {},
  "sourcePriority": [],
  "extraction": {},
  "maintenance": {},
  "reporting": {},
  "syncLog": {},
  "language": "en"
}
```

---

## `version`

### Type
`number`

### Purpose
Configuration schema version.

### Recommended value
```json
"version": 1
```

---

## `maintainer`

Defines the maintainer identity for the shared-memory system.

### Example

```json
"maintainer": {
  "agentId": "main"
}
```

### Fields

#### `maintainer.agentId`
- Type: `string`
- Meaning: the primary maintainer agent for coordinated shared-memory review

---

## `paths`

Defines shared-memory filesystem locations.

### Example

```json
"paths": {
  "sharedRoot": "<workspace-parent>/shared-memory",
  "sharedFiles": {
    "user": "shared-user.md",
    "memory": "shared-memory.md",
    "rules": "shared-rules.md"
  },
  "syncLogDir": "shared-sync-log",
  "archiveDir": "archived"
}
```

### Fields

#### `paths.sharedRoot`
- Type: `string`
- Meaning: absolute root directory for the shared-memory system
- Default intent in v1: use a `shared-memory/` directory under the OpenClaw workspace parent directory (that is, as a sibling of `workspace/`)
- In the default local layout, this resolves to:
  ```text
  /root/.openclaw/shared-memory
  ```
- Used by:
  - `init`
  - `run-shared-scan`
  - `run-shared-maintenance`
  - `show-status`
  - `show-sync-logs`
  - `prune-sync-logs`

#### `paths.sharedFiles.user`
- Type: `string`
- Meaning: filename for user-level shared memory

#### `paths.sharedFiles.memory`
- Type: `string`
- Meaning: filename for durable world/project/environment facts

#### `paths.sharedFiles.rules`
- Type: `string`
- Meaning: filename for shared-memory governance rules

#### `paths.syncLogDir`
- Type: `string`
- Meaning: shared-layer log directory under `sharedRoot`

#### `paths.archiveDir`
- Type: `string`
- Meaning: archive directory under `sharedRoot`
- Default detach behavior archives `SHARED_ATTACH.md` under:
  ```text
  <sharedRoot>/<archiveDir>/<agent>/
  ```

---

## `schedules`

Defines recommended schedule settings and is the source of truth for schedule consistency checks.

### Example

```json
"schedules": {
  "timezone": "Asia/Shanghai",
  "privateMaintenance": {
    "enabled": true,
    "every": "72h",
    "time": "12:00",
    "recommended": true
  },
  "sharedScan": {
    "enabled": true,
    "every": "6d",
    "time": "12:30",
    "recommended": true
  },
  "sharedMaintenance": {
    "enabled": true,
    "every": "12d",
    "time": "13:00",
    "recommended": true
  }
}
```

### Fields

#### `schedules.timezone`
- Type: `string`
- Meaning: timezone used by schedule interpretation and consistency checks

#### `schedules.privateMaintenance`
- Meaning: per-agent private long-term memory maintenance schedule
- Prepared by: `attach <agent>`
- Preserved after: `detach <agent>`, `unregister <agent>`

#### `schedules.sharedScan`
- Meaning: shared scan schedule
- Prepared by: `init`

#### `schedules.sharedMaintenance`
- Meaning: shared maintenance schedule
- Prepared by: `init`

### Common nested fields

#### `enabled`
- Type: `boolean`
- Meaning: whether the schedule should be active

#### `every`
- Type: `string`
- Meaning: recurrence interval, e.g. `72h`, `6d`, `12d`

#### `time`
- Type: `string`
- Meaning: preferred scheduled time, e.g. `12:00`

#### `recommended`
- Type: `boolean`
- Meaning: whether the value is a recommended default rather than a mandatory requirement

---

## `participants`

Defines participation membership.

### Example

```json
"participants": {
  "registeredAgents": [],
  "includeSubagents": true,
  "subagentsReadShared": true,
  "subagentsWriteShared": false,
  "subagentContributionMode": "relay-to-maintainer"
}
```

### Fields

#### `participants.registeredAgents`
- Type: `array[string]`
- Meaning: the registered participant list
- Important: this is not the attached list
- Used by:
  - `register <agent>`
  - `unregister <agent>`
  - shared scan scope
  - shared maintenance scope

#### `participants.includeSubagents`
- Type: `boolean`
- Meaning: whether subagents may participate as readers/contributors under policy

#### `participants.subagentsReadShared`
- Type: `boolean`
- Meaning: whether subagents may read shared memory

#### `participants.subagentsWriteShared`
- Type: `boolean`
- Meaning: whether subagents may directly write primary shared-memory files
- Recommended v1 value: `false`

#### `participants.subagentContributionMode`
- Type: `string`
- Meaning: how subagent-discovered candidates are handled
- Recommended v1 value:
  ```json
  "relay-to-maintainer"
  ```

---

## `attachment`

Defines local attachment policy.

### Example

```json
"attachment": {
  "required": true,
  "mode": "explicit",
  "localGuideFile": "SHARED_ATTACH.md",
  "primaryEntrypoint": "AGENTS.md"
}
```

### Fields

#### `attachment.required`
- Type: `boolean`
- Meaning: whether local guidance is required for shared-memory reading

#### `attachment.mode`
- Type: `string`
- Meaning: attachment mode
- Recommended v1 value:
  ```json
  "explicit"
  ```

#### `attachment.localGuideFile`
- Type: `string`
- Meaning: local guidance filename
- Recommended v1 value:
  ```json
  "SHARED_ATTACH.md"
  ```

#### `attachment.primaryEntrypoint`
- Type: `string`
- Meaning: local file used as the primary startup guidance entrypoint
- Recommended v1 value:
  ```json
  "AGENTS.md"
  ```

---

## `sharing`

Defines hard boundary switches for prohibited sharing categories.

### Example

```json
"sharing": {
  "shareAssistantIdentityContext": false,
  "shareAssistantPersonaContext": false,
  "shareAssistantToneContext": false,
  "sharePrivateProjectContext": false,
  "shareTemporaryTaskState": false,
  "sharePlaintextSecrets": false
}
```

### Purpose
This block exists to encode non-shareable hard boundaries.

It should not duplicate every positive sharing rule already expressed by:
- file responsibilities
- content policy
- `sourcePriority`
- narrative rules in `SKILL.md`

### Fields

#### `shareAssistantIdentityContext`
- Type: `boolean`
- Recommended v1 value: `false`
- Meaning: whether assistant-specific identity context may be shared

#### `shareAssistantPersonaContext`
- Type: `boolean`
- Recommended v1 value: `false`
- Meaning: whether assistant-specific style framing may be shared

#### `shareAssistantToneContext`
- Type: `boolean`
- Recommended v1 value: `false`
- Meaning: whether assistant tone/style identity may be shared

#### `sharePrivateProjectContext`
- Type: `boolean`
- Recommended v1 value: `false`
- Meaning: whether agent-private project-only context may be shared

#### `shareTemporaryTaskState`
- Type: `boolean`
- Recommended v1 value: `false`
- Meaning: whether temporary task state may be shared

#### `sharePlaintextSecrets`
- Type: `boolean`
- Recommended v1 value: `false`
- Meaning: whether plaintext secrets may be shared

---

## `readOrder`

Defines long-term memory read precedence.

### Example

```json
"readOrder": {
  "privateFirst": true,
  "sharedSecond": true,
  "sharedCannotOverrideIdentityContext": true
}
```

### Fields

#### `readOrder.privateFirst`
- Type: `boolean`
- Meaning: read private memory first

#### `readOrder.sharedSecond`
- Type: `boolean`
- Meaning: read shared memory second

#### `readOrder.sharedCannotOverrideIdentityContext`
- Type: `boolean`
- Meaning: shared memory remains supplemental and cannot override assistant-specific identity context

---

## `sourcePriority`

Defines upstream source order for shared promotion.

### Example

```json
"sourcePriority": [
  "MEMORY.md",
  "USER.md"
]
```

### Purpose
This block defines which upstream sources shared scan should prioritize.

It is intentionally separate from `extraction` because it defines source order, not merely extraction behavior details.

### Recommended v1 meaning
1. read `MEMORY.md` first for durable long-term candidates
2. then read `USER.md` for stable user preferences and user-level constraints

### Notes
- Do not treat raw daily memory as a normal source in v1
- This source order works together with the pipeline:
  ```text
  daily memory → private long-term memory → shared scan → shared memory layer
  ```

---

## `extraction`

Defines extraction behavior details.

### Example

```json
"extraction": {
  "allowDailyMemoryFallback": false,
  "skipMarkedEntries": true,
  "reextractIfUpdated": true,
  "extractionMarker": {
    "enabled": true,
    "format": "> Status: Extracted to shared memory ({date})"
  }
}
```

### Fields

#### `extraction.allowDailyMemoryFallback`
- Type: `boolean`
- Recommended v1 value: `false`
- Meaning: whether shared scan may fall back to raw daily memory when preferred sources are insufficient
- Recommended interpretation in v1:
  - keep this `false`
  - require promotion to come from distilled long-term memory sources

#### `extraction.skipMarkedEntries`
- Type: `boolean`
- Meaning: skip entries already marked as extracted

#### `extraction.reextractIfUpdated`
- Type: `boolean`
- Meaning: allow re-promotion when a previously extracted local entry has materially changed

#### `extraction.extractionMarker.enabled`
- Type: `boolean`
- Meaning: whether extraction markers are used

#### `extraction.extractionMarker.format`
- Type: `string`
- Meaning: extraction marker format
- Recommended v1 value:
  ```json
  "> Status: Extracted to shared memory ({date})"
  ```

---

## `maintenance`

Defines what shared maintenance is allowed to do.

### Example

```json
"maintenance": {
  "deduplicateSharedMemory": true,
  "mergeSimilarEntries": false,
  "pruneOutdatedSharedEntries": true,
  "markLocalExtractedEntries": true,
  "modifyLocalMemoryDirectly": false
}
```

### Fields

#### `maintenance.deduplicateSharedMemory`
- Type: `boolean`
- Meaning: allow deduplication in shared memory

#### `maintenance.mergeSimilarEntries`
- Type: `boolean`
- Meaning: allow safe merging of similar shared entries

#### `maintenance.pruneOutdatedSharedEntries`
- Type: `boolean`
- Meaning: allow pruning outdated shared entries

#### `maintenance.markLocalExtractedEntries`
- Type: `boolean`
- Meaning: allow only minimal appended extraction markers on local source entries
- In v1, this means:
  - append extraction markers only
  - do not restructure local content

#### `maintenance.modifyLocalMemoryDirectly`
- Type: `boolean`
- Recommended v1 value: `false`
- Meaning: whether shared maintenance may directly rewrite local long-term memory body content
- In v1, `false` means:
  - do not rewrite
  - do not restructure
  - do not delete local body content

### Important clarification
These two fields are not contradictory:

- `markLocalExtractedEntries: true`
- `modifyLocalMemoryDirectly: false`

This means:
- marker append is allowed
- direct body rewrite/restructure/delete is not allowed

---

## `reporting`

Defines reporting behavior.

### Example

```json
"reporting": {
  "mode": "log-and-report",
  "target": "current-chat",
  "includeSummary": true,
  "includeSkippedReasons": true
}
```

### Fields

#### `reporting.mode`
- Type: `string`
- Meaning: reporting mode for operational tasks

#### `reporting.target`
- Type: `string`
- Meaning: report destination target

#### `reporting.includeSummary`
- Type: `boolean`
- Meaning: include high-level summaries in reports

#### `reporting.includeSkippedReasons`
- Type: `boolean`
- Meaning: include skipped-reason summaries in reports

---

## `syncLog`

Defines shared-layer log behavior.

### Example

```json
"syncLog": {
  "enabled": true,
  "retainDays": 180,
  "fileNaming": "{date}_{time}_{type}.md"
}
```

### Fields

#### `syncLog.enabled`
- Type: `boolean`
- Meaning: whether shared-layer sync logs are written

#### `syncLog.retainDays`
- Type: `number`
- Meaning: retention period for shared-layer logs

#### `syncLog.fileNaming`
- Type: `string`
- Meaning: naming pattern for shared scan and maintenance logs

### Scope rule
`show-sync-logs` and `prune-sync-logs` apply only to the shared-layer log directory and not to agent-private maintenance logs.

---

## `language`

Defines the default storage language.

### Example

```json
"language": "en"
```

### Meaning
Use a single default storage language for:
- shared-memory files
- `SHARED_ATTACH.md`
- extraction markers
- default examples stored by the skill

### Current policy
- final skill storage examples: English
- review drafts and discussion: may be Chinese

---

## Config-related commands

### `init [--config <path>] [--shared-root <path>]`
Use for initial setup.

Behavior:
- may create missing config file
- requires writable parent directory
- requires confirmation before overwriting existing config
- requires confirmation before reinitializing an already populated shared root

If both `--config` and `--shared-root` are passed, the initialized config and structure should use that provided `sharedRoot`.

### `show-config [--config <path>]`
Display current config contents.

### `validate-config [--config <path>]`
Validate config structure, required fields, and internal consistency.

### `update-config [--config <path>]`
Apply manually edited config changes after validation.

In v1:
- user edits the JSON file manually
- then runs `update-config`
- the skill validates and applies changes

If schedule definitions are inconsistent with the updated config, report the mismatch.

Do not automatically rewrite all schedules in v1.

---

## Schedule consistency checks

Schedule consistency checks must use the current JSON config as the source of truth.

Every schedule-related field present in JSON must be checked with no omissions.

At minimum, consistency checks should cover:
- `enabled`
- `timezone`
- `every`
- `time`
- task type
- config path
- `sharedRoot` if passed through task parameters
- any other schedule-related JSON-defined fields

### Where checks happen

#### Shared scan checks
Check all participating agents' private maintenance schedule state for:
- existence
- enabled state
- consistency with current JSON config

#### Shared maintenance checks
Check shared scan and shared maintenance schedule state for:
- existence
- enabled state
- consistency with current JSON config

#### Repair attachment checks
Check the target agent's private maintenance schedule state for:
- existence
- enabled state
- consistency with current JSON config

---

## Status display requirements

`show-status` must use list format.

Display at least:
- Shared root
- Active config path
- Last shared scan
- Next shared scan
- Last shared maintenance
- Next shared maintenance

For each agent, display:
- agent name
- `registerStatus`
- `attachStatus`
- `privateMaintenanceLastRun`
- `privateMaintenanceNextRun`

Interpretation:
- `registerStatus` = membership state
- `attachStatus` = local guidance readiness state

Incomplete local attachment must be displayed as `detached`.

---

## Recommended full config example

```json
{
  "version": 1,
  "maintainer": {
    "agentId": "main"
  },
  "paths": {
    "sharedRoot": "<workspace-parent>/shared-memory",
    "sharedFiles": {
      "user": "shared-user.md",
      "memory": "shared-memory.md",
      "rules": "shared-rules.md"
    },
    "syncLogDir": "shared-sync-log",
    "archiveDir": "archived"
  },
  "schedules": {
    "timezone": "Asia/Shanghai",
    "privateMaintenance": {
      "enabled": true,
      "every": "72h",
      "time": "12:00",
      "recommended": true
    },
    "sharedScan": {
      "enabled": false,
      "every": "6d",
      "time": "12:30",
      "recommended": true
    },
    "sharedMaintenance": {
      "enabled": false,
      "every": "12d",
      "time": "13:00",
      "recommended": true
    }
  },
  "participants": {
    "registeredAgents": [],
    "includeSubagents": true,
    "subagentsReadShared": true,
    "subagentsWriteShared": false,
    "subagentContributionMode": "relay-to-maintainer"
  },
  "attachment": {
    "required": true,
    "mode": "explicit",
    "localGuideFile": "SHARED_ATTACH.md",
    "primaryEntrypoint": "AGENTS.md"
  },
  "sharing": {
    "shareAssistantIdentityContext": false,
    "shareAssistantPersonaContext": false,
    "shareAssistantToneContext": false,
    "sharePrivateProjectContext": false,
    "shareTemporaryTaskState": false,
    "sharePlaintextSecrets": false
  },
  "readOrder": {
    "privateFirst": true,
    "sharedSecond": true,
    "sharedCannotOverrideIdentityContext": true
  },
  "sourcePriority": [
    "MEMORY.md",
    "USER.md"
  ],
  "extraction": {
    "allowDailyMemoryFallback": false,
    "skipMarkedEntries": true,
    "reextractIfUpdated": true,
    "extractionMarker": {
      "enabled": true,
      "format": "> Status: Extracted to shared memory ({date})"
    }
  },
  "maintenance": {
    "deduplicateSharedMemory": true,
    "mergeSimilarEntries": true,
    "pruneOutdatedSharedEntries": true,
    "markLocalExtractedEntries": true,
    "modifyLocalMemoryDirectly": false
  },
  "reporting": {
    "mode": "log-and-report",
    "target": "current-chat",
    "includeSummary": true,
    "includeSkippedReasons": true
  },
  "syncLog": {
    "enabled": true,
    "retainDays": 180,
    "fileNaming": "{date}_{time}_{type}.md"
  },
  "language": "en"
}
```
