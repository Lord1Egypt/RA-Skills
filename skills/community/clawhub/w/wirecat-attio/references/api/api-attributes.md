<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Attributes

## `attio api attributes-create [options]`

- What: Create an attribute
- Call: `POST /v2/{target}/{identifier}/attributes`, effect: write
- Sign-in: oauth2
- Body: `PostV2ByTargetByIdentifierAttributesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--target <value>` | yes | target |
| `--identifier <value>` | yes | identifier |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api attributes-get [options]`

- What: Get an attribute
- Call: `GET /v2/{target}/{identifier}/attributes/{attribute}`, effect: read
- Sign-in: oauth2

| Flag | Required | What |
|---|---|---|
| `--target <value>` | yes | target |
| `--identifier <value>` | yes | identifier |
| `--attribute <value>` | yes | attribute |

## `attio api attributes-list [options]`

- What: List attributes
- Call: `GET /v2/{target}/{identifier}/attributes`, effect: read
- Sign-in: oauth2
- Pages: offset: send `offset` (query), raised by the items read so far; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--target <value>` | yes | target |
| `--identifier <value>` | yes | identifier |
| `--limit <value>` | no | limit |
| `--offset <value>` | no | offset |
| `--show-archived <value>` | no | show\_archived |
| `--all` | no | read every page, as the API pages it |

## `attio api attributes-options-create [options]`

- What: Create a select option
- Call: `POST /v2/{target}/{identifier}/attributes/{attribute}/options`, effect: write
- Sign-in: oauth2
- Body: `PostV2ByTargetByIdentifierAttributesByAttributeOptionsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--target <value>` | yes | target |
| `--identifier <value>` | yes | identifier |
| `--attribute <value>` | yes | attribute |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api attributes-options-list [options]`

- What: List select options
- Call: `GET /v2/{target}/{identifier}/attributes/{attribute}/options`, effect: read
- Sign-in: oauth2

| Flag | Required | What |
|---|---|---|
| `--target <value>` | yes | target |
| `--identifier <value>` | yes | identifier |
| `--attribute <value>` | yes | attribute |
| `--show-archived <value>` | no | show\_archived |

## `attio api attributes-options-update [options]`

- What: Update a select option
- Call: `PATCH /v2/{target}/{identifier}/attributes/{attribute}/options/{option}`, effect: write
- Sign-in: oauth2
- Body: `PatchV2ByTargetByIdentifierAttributesByAttributeOptionsByOptionRequest`, required

| Flag | Required | What |
|---|---|---|
| `--target <value>` | yes | target |
| `--identifier <value>` | yes | identifier |
| `--attribute <value>` | yes | attribute |
| `--option <value>` | yes | option |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api attributes-statuses-create [options]`

- What: Create a status
- Call: `POST /v2/{target}/{identifier}/attributes/{attribute}/statuses`, effect: write
- Sign-in: oauth2
- Body: `PostV2ByTargetByIdentifierAttributesByAttributeStatusesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--target <value>` | yes | target |
| `--identifier <value>` | yes | identifier |
| `--attribute <value>` | yes | attribute |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api attributes-statuses-list [options]`

- What: List statuses
- Call: `GET /v2/{target}/{identifier}/attributes/{attribute}/statuses`, effect: read
- Sign-in: oauth2

| Flag | Required | What |
|---|---|---|
| `--target <value>` | yes | target |
| `--identifier <value>` | yes | identifier |
| `--attribute <value>` | yes | attribute |
| `--show-archived <value>` | no | show\_archived |

## `attio api attributes-statuses-update [options]`

- What: Update a status
- Call: `PATCH /v2/{target}/{identifier}/attributes/{attribute}/statuses/{status}`, effect: write
- Sign-in: oauth2
- Body: `PatchV2ByTargetByIdentifierAttributesByAttributeStatusesByStatusRequest`, required

| Flag | Required | What |
|---|---|---|
| `--target <value>` | yes | target |
| `--identifier <value>` | yes | identifier |
| `--attribute <value>` | yes | attribute |
| `--status <value>` | yes | status |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api attributes-update [options]`

- What: Update an attribute
- Call: `PATCH /v2/{target}/{identifier}/attributes/{attribute}`, effect: write
- Sign-in: oauth2
- Body: `PatchV2ByTargetByIdentifierAttributesByAttributeRequest`, required

| Flag | Required | What |
|---|---|---|
| `--target <value>` | yes | target |
| `--identifier <value>` | yes | identifier |
| `--attribute <value>` | yes | attribute |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
