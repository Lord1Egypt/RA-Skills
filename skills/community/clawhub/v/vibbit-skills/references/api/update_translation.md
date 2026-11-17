# Save translated text: update_translation

Task type: `VIDEO_VOICE_OVER_TASK`. Mode: `mutation`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/515712723e0)

Requires real review context. Saves text only and clears previous audio/render checkpoints; never approves review.

## Inputs

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

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" update_translation --task-id task-RETURNED_NUMERIC_ID --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" update_translation --task-id task-RETURNED_NUMERIC_ID --input /absolute/path/request.json
~~~

Method: `PUT /openapi/v1/tasks/{taskId}/translation`. Send the operation body directly, without task_type/input_info wrappers.



[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)

## Review requirements

Query the original task first and obtain actual review content in TRANSLATION_REVIEW or STORYBOARD_REVIEW. Do not infer a review stage from RUNNING or invent IDs. Follow existing user authorization.

Example IDs are placeholders. Parent IDs must be complete task-<digits>; sub_task_id must be a positive long belonging to that parent. target_language must be selected for that video, nonempty, and at most 32 characters.

segments must contain 1-1000 objects with from >= 0, to > from (seconds), and nonempty translated_text. Optional fields: id (stable ASR segment ID), source_text, confidence, speaker_id, confirmed, audio_url, audio_duration, over_duration, audio_group_id, audio_fingerprint. Provide only real existing values; do not invent confidence/speakers or add historical audio fields unnecessarily.

Saving clears old audio, group/fingerprint, and render checkpoints. Top-level confirmed is compatibility-only: service saves false and client rejects true. Segment confirmed does not approve review. This operation neither starts rendering nor changes templates.

Each mutation has a separate new journal. Uncertain PUT responses must not be replayed; resume queries the parent without proving the edit succeeded. Verify actual task state. After a definite save, query review/phase again before [storyboard approval](confirm_translation.md). See [translation inputs](translate_video.md).
