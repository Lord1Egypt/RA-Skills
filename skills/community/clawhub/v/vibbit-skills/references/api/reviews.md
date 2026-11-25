# Product review APIs

Use the contents to read only the section needed for the current operation. Each section retains its own parameters, authorization, and execution boundaries.

- [Reddit discussions: reddit_reviews](#reddit-reviews)
- [Amazon reviews: amazon_reviews](#amazon-reviews)

<a id="reddit-reviews"></a>

## Reddit discussions: reddit_reviews

Task type: `REDDIT_REVIEW_SEARCH`. Mode: `sync`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/513300737e0)

<a id="reddit-reviews-inputs"></a>

### Inputs

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

<a id="reddit-reviews-call"></a>

### Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" reddit_reviews --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" reddit_reviews --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

Keep links to the actual discussions. Separate quoted opinions from your interpretation and do not claim small samples represent the whole market.

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)

<a id="amazon-reviews"></a>

## Amazon reviews: amazon_reviews

Task type: `AMAZON_REVIEW_SEARCH`. Mode: `unknown`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/513300736e0)

Use actual response fields. If results cannot be interpreted, report query status; an empty response does not establish zero reviews.

<a id="amazon-reviews-inputs"></a>

### Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `url` | url | Yes |
| `domain` | string | No |
| `limit` | integer | No |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "url": "https://www.amazon.com/dp/REPLACE_ASIN",
  "domain": "com",
  "limit": 5
}
~~~

<a id="amazon-reviews-call"></a>

### Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" amazon_reviews --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" amazon_reviews --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

Use a verified product-page URL, not keywords or an invented ASIN. Successful response structure is not fully documented; an empty response does not establish zero reviews.

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)
