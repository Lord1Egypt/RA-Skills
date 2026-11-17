# Approve the current storyboard: confirm_translation

Task type: `VIDEO_VOICE_OVER_TASK`. Mode: `mutation`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/515938897e0)

Requires actual reviewed storyboard context. Omitted sub_task_id confirms the whole batch; CLI requires --all-items explicitly.

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `sub_task_id` | id | No |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "sub_task_id": "2100065567327711232"
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" confirm_translation --task-id task-RETURNED_NUMERIC_ID --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" confirm_translation --task-id task-RETURNED_NUMERIC_ID --input /absolute/path/request.json
~~~

Method: `POST /openapi/v1/tasks/{taskId}/storyboard/confirm`. Send the operation body directly, without task_type/input_info wrappers.



[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)

## Approval scope

Approve the current server storyboard, not supplied storyboard text, translation, or voice settings. Query actual STORYBOARD_REVIEW content first, including associated video and phase; use the user's existing authorization.

For one item, pass its actual sub_task_id. The numeric example above is a placeholder. To approve the batch:

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" confirm_translation --task-id task-RETURNED_NUMERIC_ID --all-items --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" confirm_translation --task-id task-RETURNED_NUMERIC_ID --all-items --wait
~~~

A batch request sends an empty object. Missing sub_task_id implies all items at the service level, so the client requires explicit --all-items and rejects mixing batch and one-item options.

STORYBOARD_REVIEW is required. Approving all participants starts RENDERING and voice/composition work; one-item approval may only save its review status. Repeated approval in RENDERING/COMPLETED is documented as idempotent for this operation, not all POSTs; uncertain writes are still not automatically repeated.

Use the new returned operation record to continue after batch approval. The original creation record's review_mode is not rewritten. RUNNING without review details does not identify a particular stage.

The reference page's generated schema marks sub_task_id required, while its prose permits omission for batch approval. The client follows that documented batch meaning and exact integer encoding. See [translation](translate_video.md).
