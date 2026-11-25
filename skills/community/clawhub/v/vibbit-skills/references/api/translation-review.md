# Translation editing and confirmation APIs

Use the contents to read only the section needed for the current operation. Each section retains its own parameters, authorization, and execution boundaries.

- [Save translated text: update_translation](#update-translation)
- [Approve the current storyboard: confirm_translation](#confirm-translation)

<a id="update-translation"></a>

## Save translated text: update_translation

Task type: `VIDEO_VOICE_OVER_TASK`. Mode: `mutation`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/515712723e0)

Requires real review context. Saves text only and clears previous audio/render checkpoints; never approves review.

<a id="update-translation-inputs"></a>

### Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `sub_task_id` | id | Yes |
| `target_language` | string | Yes |
| `segments` | objects | Yes |
| `confirmed` | boolean | No |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "sub_task_id": "2100065567327711232",
  "target_language": "en",
  "segments": [
    {
      "from": 0,
      "to": 2.4,
      "translated_text": "Hello."
    }
  ]
}
~~~

<a id="update-translation-call"></a>

### Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" update_translation --task-id task-RETURNED_NUMERIC_ID --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" update_translation --task-id task-RETURNED_NUMERIC_ID --input /absolute/path/request.json
~~~

Method: `PUT /openapi/v1/tasks/{taskId}/translation`. Send the operation body directly, without task_type/input_info wrappers.



[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)

<a id="update-translation-review-requirements"></a>

### Review requirements

Query the original task first and obtain actual review content in TRANSLATION_REVIEW or STORYBOARD_REVIEW. Do not infer a review stage from RUNNING or invent IDs. Follow existing user authorization.

Example IDs are placeholders. Parent IDs must be complete task-<digits>; sub_task_id must be a positive long belonging to that parent. target_language must be selected for that video, nonempty, and at most 32 characters.

segments must contain 1-1000 objects with from >= 0, to > from (seconds), and nonempty translated_text. Optional fields: id (stable ASR segment ID), source_text, confidence, speaker_id, confirmed, audio_url, audio_duration, over_duration, audio_group_id, audio_fingerprint, lip_sync, lip_sync_video_url. Historical lip_sync_video_url is not a delivered-media replacement field. Provide only real existing values; do not invent confidence/speakers or add historical audio fields unnecessarily.

Saving clears old audio, group/fingerprint, and render checkpoints. Top-level confirmed is compatibility-only: service saves false and client rejects true. Segment confirmed does not approve review. This operation neither starts rendering nor changes templates.

Each mutation has a separate new journal. Uncertain PUT responses must not be replayed; resume queries the parent without proving the edit succeeded. Verify actual task state. After a definite save, query review/phase again before [storyboard approval](#confirm-translation). See [translation inputs](translate_video.md).

<a id="confirm-translation"></a>

## Approve the current storyboard: confirm_translation

Task type: `VIDEO_VOICE_OVER_TASK`. Mode: `mutation`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/515938897e0)

Requires actual reviewed storyboard context. Omitted sub_task_id confirms the whole batch; CLI requires --all-items explicitly.

<a id="confirm-translation-inputs"></a>

### Inputs

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

<a id="confirm-translation-call"></a>

### Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" confirm_translation --task-id task-RETURNED_NUMERIC_ID --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" confirm_translation --task-id task-RETURNED_NUMERIC_ID --input /absolute/path/request.json
~~~

Method: `POST /openapi/v1/tasks/{taskId}/storyboard/confirm`. Send the operation body directly, without task_type/input_info wrappers.



[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)

<a id="confirm-translation-approval-scope"></a>

### Approval scope

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
