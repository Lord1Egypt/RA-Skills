# Video material import APIs

Use the contents to read only the section needed for the current operation. Each section retains its own parameters, authorization, and execution boundaries.

- [Import video materials: import_material_videos](#import-material-videos)
- [Query a material import: get_material_import](#get-material-import)

<a id="import-material-videos"></a>

## Import video materials: import_material_videos

[API reference](https://vibbit.apifox.cn/526975082e0): POST `/openapi/v1/materials:importFromUrls` with a native JSON object. Do not use `/tasks`, task_type or input_info.

<a id="import-material-videos-input-and-execution"></a>

### Input and execution

```json
{
  "items": [{"url": "https://example.com/source.mp4", "name": "Product-showcase-v1.mp4"}],
  "auto_ingest": false
}
```

Send 1–20 items; deployment limits may be smaller. Each item accepts only a required url and optional nonblank name. Use a server-accessible HTTP(S) video URL of at most 4096 characters without embedded credentials. Preserve signed query parameters and never change a URL extension based on the display name.

Optional collection_name is the full name of an existing, uniquely matched group and applies to the whole batch. Submit different groups separately. Omit it when unspecified; do not invent a group, send whitespace or claim a new group was created. There is no group-list or group-create command.

The client defaults auto_ingest to false for storage only. Explicitly use true when content search or analysis is needed. The service itself defaults omission to true, so the client sends its choice explicitly. Tags, categories, product binding and collection_id are not creation fields.

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" import_material_videos --input /absolute/path/import.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" import_material_videos --input /absolute/path/import.json --submission-id SAVED_IMPORT_ID --wait
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" resume --submission-id SAVED_IMPORT_ID
```

For a local video, first use [upload_info --file](upload_info.md), save the actual credential-free upload receipt and object_url privately, then build this request. Import an external video URL or confirmed unregistered new output directly without uploading it again. Seedance generation is registered by the service: do not import it again even when no material ID was returned; follow [material resources](../resources/materials.md). The import service resolves platform share links; do not pay for a separate parsing call first. Uploading a reference alone does not request library storage. Follow [material resources](../resources/materials.md) for intent rules.

<a id="import-material-videos-completion-and-recovery"></a>

### Completion and recovery

Save the original import task_id without adding or removing a task- prefix. Use [get_material_import](#get-material-import) or resume the original journal; ordinary generation-task status/wait ID rules do not apply.

The CLI maps status to PENDING/RUNNING/COMPLETED/FAILED and preserves the service's import_status, including SUCCESS/PARTIAL_SUCCESS/FAILED. Each successful item must have status IMPORTED and a real material_id. material_ids contains successful IDs only. artifacts is empty because importing does not generate another video.

Keep successful items and failure reasons on partial success; do not import the entire batch again. Repeating a URL in a new request creates another import. Keep the same --submission-id or --state for one intent. Never automatically repeat POST after uncertainty: query a saved task ID or preserve the journal and investigate acceptance when no ID exists. Journals store hashes and identifiers, not upload credentials or complete request URLs; retain resumable input/upload receipts separately in private production records.

Imported media and analysis have separate outcomes. Preserve imported material IDs even if analysis fails; do not regenerate or reimport to pretend to retry analysis. Independent analysis triggers, image/audio registration, manual tags/categories, product binding and changing an existing material's group are not provided by these commands.

The service downloads supported video-extension URLs directly without link-parsing credits. Share URLs, extensionless URLs and m3u8 use link parsing under existing billing. Storage and analysis are not thereby established as free.

<a id="get-material-import"></a>

## Query a material import: get_material_import

[API reference](https://vibbit.apifox.cn/526977708e0): GET `/openapi/v1/material-import-tasks/{taskId}`. This is read-only and never creates another task. Input:

```json
{"import_task_id": "2100065567327711232"}
```

Use the actual returned import ID, not this example. No request body or mandatory task- prefix is used.

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" get_material_import --input /absolute/path/import-task.json
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" get_material_import --input /absolute/path/import-task.json --wait
```

Omit --wait for one query. --wait polls import completion in 50-second windows, at least 5 seconds apart. Continue the original task or resume its original import journal after a window expires, following [task lifecycle](../runtime/task-lifecycle.md) without repeated continuation confirmation. --state and --submission-id do not apply to this read-only command; use resume for an existing journal.

| import_status | Meaning |
| --- | --- |
| PENDING / RUNNING | Queued or importing |
| SUCCESS | All imported; CLI status is COMPLETED |
| PARTIAL_SUCCESS | Some imported; CLI status is COMPLETED, partial_failure=true and exit code 5 |
| FAILED | All failed; CLI ok=false and status=FAILED, preserving item failures |

result.items contains index, source_url, status, available material_id/name/analysis_status, warnings and failure details. WAITING_PERMIT means waiting for processing capacity, not proven insufficient credits. Accept unfamiliar failure codes and show actual failure_reason.

--wait waits for import completion only. If auto_ingest=true and downstream work needs analysis, continue read-only queries of each item's analysis_status. Only COMPLETED with actual analysis content supports content retrieval. Stop on FAILED/CANCELLED. With auto_ingest=false do not wait for analysis to start by itself. Report imported and analyzing separately; never create a second import just because analysis is pending.
