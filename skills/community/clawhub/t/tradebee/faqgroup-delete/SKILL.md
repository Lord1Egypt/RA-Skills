---
name: faqgroup-delete
description: A FAQ group deletion skill based on the "Tradebee Website Builder" Open API. It is used to batch delete one or more FAQ groups under a specified site language and returns separate success and failure ID lists.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# faqgroup-delete

## Overview

Use the Tradebee Website Builder Open API to delete one or more FAQ groups.

Supports batch deletion of FAQ group IDs under a specified language and returns separate success and failure item lists.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `language` (string, **Required**)

Enabled site language.

> Must be selected manually from the list returned by `languages-get`. AI inference or automatic generation is not allowed.

---

### `id_list` (array of integers, **Required**)

FAQ group ID list, up to 100 items.

### `confirmation` (object, **Required**)

Explicit user approval for this high-impact action.

| Field      | Type    | Description |
|------------|---------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language and exact FAQ group IDs to delete. |
| `summary`  | string  | Restates the language and exact FAQ group IDs shown to the user before execution. |

---

## Output Structure

### Top-Level Structure

| Field  | Type         | Description      |
|--------|--------------|------------------|
| status | boolean      | Request status   |
| msg    | string       | Response message |
| data   | object/null  | Returned data    |

### `data`

| Field     | Type  | Description                  |
|-----------|-------|------------------------------|
| `success` | array | Successfully deleted items   |
| `fail`    | array | Failed deletion items        |

### `data.success[]`

| Field | Type    | Description          |
|-------|---------|----------------------|
| `id`  | integer | FAQ group ID         |
| `msg` | string  | Success message      |

### `data.fail[]`

| Field | Type    | Description          |
|-------|---------|----------------------|
| `id`  | integer | FAQ group ID         |
| `msg` | string  | Failure message      |

---

## Dependencies

| Parameter | Dependency skill | Field source    | Mode   |
|-----------|------------------|-----------------|--------|
| language  | languages-get    | list[].language | select |

---

## Usage Example

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: delete FAQ groups 18468028, 18467384, and 18466967 in language en."
  },
  "id_list": [
    18468028,
    18467384,
    18466967
  ]
}
```

## Notes

1. If a FAQ group still contains FAQs, the API can return failures for those group IDs.
2. Review `data.fail[]` instead of assuming every requested ID was deleted.

## Response Example

```json
{
  "status": true,
  "msg": "Deleted successfully",
  "data": {
    "success": [
      {
        "id": 18468028,
        "msg": "Deleted"
      }
    ],
    "fail": []
  }
}
```
