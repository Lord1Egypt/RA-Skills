# Web Collection Learning Guide

This file is an offline routing and recovery summary for the agent. The online documents are the source of truth for user-facing instructions and QA:

- Quick start / first-time use / UI operation guide: https://vcn5grhrq8y0.feishu.cn/wiki/MoXrwwUN7iiUFkk8eWycs9JqntA?from=from_copylink
- QA / troubleshooting guide: https://vcn5grhrq8y0.feishu.cn/wiki/F83hw2w6Xi7EOFkIScrccrQYnnd?from=from_copylink

When a user asks how to use the paid plugin, how to configure it for the first time, where to click, or how access works, read or point them to the quick-start guide. When a user asks about errors, export failures, missing data, connector status, local/cloud behavior, or common questions, read or point them to the QA guide. Use the rest of this file only to keep execution safe when online docs are unavailable or when running the bundled scripts.

Use one unified rule set:

1. Never ask for configuration that is already present in environment variables.
2. Local and cloud share the same recommended defaults and overall collection flow.
3. Cloud only adds two extra required values: `id` and `token`.
4. Local mode may only call `scripts/collect_and_export_loop.sh`.
5. Cloud mode may only call `scripts/cloud_dispatch_loop.sh`.
6. Deduplication fields are resolved by the connector/plugin, never by this skill.
7. Personal bitable export must remain `exportMode=personal`; deduplication is what makes the new plugin choose its smart personal export internally.

## Asking Rules

Ask only for user-facing defaults that are still missing after checking:

- `defaultExportMode`
- `defaultMaxItems`
- `defaultFetchDetail`
- `defaultDetailSpeed`
- `defaultDeduplicationEnabled`
- `defaultDeduplicationStrategy`
- `defaultCloudDeviceId` in cloud mode only
- `defaultCloudToken` in cloud mode only

Do not ask for:

- deduplication field or any field-selection input
- `WEB_COLLECTION_CONNECTION_MODE`
- `WEB_COLLECTION_BRIDGE_URL`
- `WEB_COLLECTION_CLOUD_BASE_URL`
- `WEB_COLLECTION_CLOUD_DEVICE_ID` when already present
- `WEB_COLLECTION_CLOUD_TOKEN` when already present
- `WEB_COLLECTION_BRIDGE_CMD`

## Shared Flow

1. Run `scripts/preflight_check.sh`
2. Persist any user-provided defaults if this turn supplies them
3. Ask only for missing user-facing values
4. Build the payload
5. Dispatch through the mode-specific script only

## Deduplication Defaults

- Default to enabled.
- Default strategy is `keepOld` (保留原始数据).
- For bitable/personal export, include only `enabled` and `strategy`.
- For CSV export, do not attach deduplication settings.
- Do not send `personalSmart` as a connector export mode.

## Smart Export Failure Handling

When `bitable` export fails but collection already succeeded:

1. Say collection completed and the failure happened during export to the original bitable table.
2. Do not reduce the whole run to a generic failure message like `HTTP 500` or `Failed to fetch`.
3. Explain likely causes in user-facing language:
   - target table does not exist
   - target table fields do not match this dataset
   - export service had a temporary error
4. Then ask exactly one follow-up choice:
   - `新建表继续导出`
   - `导出为CSV`

Recommended prompt:

```text
采集已经完成，失败发生在导出到原多维表格这一步。

原表导出失败通常有几种原因：
- 原目标表不存在
- 原目标表字段结构与本次数据不一致
- 导出服务临时异常

为了避免这次结果丢失，我现在可以继续帮你导出。你可以选择：

- 新建表继续导出：在当前多维表格中创建一个新的数据表后继续导出
- 导出为CSV：直接把这次结果保存成 CSV 文件

[[quick_replies: 新建表继续导出, 导出为CSV]]
```

Behavior notes:

- If the failed run has a connector `taskId`, use `scripts/reexport_task.sh` to reuse the cached task records. Do not run a new collection.
- If the user chooses `导出为CSV`, call `scripts/reexport_task.sh --task-id "<taskId>" --export-target csv`.
- If the user chooses `新建表继续导出`, call `scripts/reexport_task.sh --task-id "<taskId>" --export-target bitable --new-table`.
- Say explicitly that this reuses the previous task's cached records.
- If no task id is available, say the skill cannot guarantee a no-recollect retry and ask before starting any new collection.
