# Digital-human listing: list_digital_humans

Task type: `QUERY_DIGITAL_HUMAN_LIST`. Mode: `sync`; actual behavior and account access depend on the response.

Query directly; resource counts, IDs, and access scope come from the current account response.

The [public contract](https://vibbit.apifox.cn/517439849e0) defines no creation timestamp, sort/pagination input, or voice-preview field. Do not send guessed parameters. Follow [digital humans](../resources/digital-humans.md) for complete display and binding a selection to its original record.

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| None | Empty object | - |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" list_digital_humans --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" list_digital_humans --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

Directly query avatars for the current account; no --allow-legacy is required. Preserve returned id, name, avatar, voice, and cover fields. A voice field is not proof of a standalone TTS voice ID. Cover previews appear separately in previews[]; see [image previews](../runtime/media-preview.md). Do not submit these presentation fields back to the API.

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)
