# Reddit discussions: reddit_reviews

Task type: `REDDIT_REVIEW_SEARCH`. Mode: `sync`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/513300737e0)

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `query` | string | Yes |
| `limit` | integer | No |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "query": "portable projector",
  "limit": 5
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" reddit_reviews --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" reddit_reviews --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

Keep links to the actual discussions. Separate quoted opinions from your interpretation and do not claim small samples represent the whole market.

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)
