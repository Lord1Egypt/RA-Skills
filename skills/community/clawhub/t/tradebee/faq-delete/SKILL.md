---
name: faq-delete
description: A FAQ deletion skill based on the "Tradebee Website Builder" Open API. It is used to move one or more FAQs under a specified site language to the recycle bin and supports batch deletion by FAQ ID list.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# faq-delete

## Overview

Use the Tradebee Website Builder Open API to move one or more FAQs to the recycle bin.

Supports batch deletion of FAQ IDs under a specified language. Deleted FAQs are moved to the recycle bin and can be restored there if deleted by mistake.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `language` (string, **Required**)

Enabled site language.

> Must be selected manually from the list returned by `languages-get`. AI inference or automatic generation is not allowed.

---

### `id_list` (array of integers, **Required**)

FAQ ID list, up to 100 items. Matching FAQs will be moved to the recycle bin.

### `confirmation` (object, **Required**)

Explicit user approval for this high-impact action.

| Field      | Type    | Description |
|------------|---------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language and exact FAQ IDs to be moved to the recycle bin. |
| `summary`  | string  | Restates the language and exact FAQ IDs shown to the user before execution. |

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
| `success` | array | Successfully recycled items  |
| `fail`    | array | Failed deletion items        |

### `data.success[]`

| Field | Type    | Description     |
|-------|---------|-----------------|
| `id`  | integer | FAQ ID          |
| `msg` | string  | Success message |

### `data.fail[]`

| Field | Type    | Description     |
|-------|---------|-----------------|
| `id`  | integer | FAQ ID          |
| `msg` | string  | Failure message |

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
    "summary": "Confirmed by user: move FAQs 18468028, 18467384, and 18466967 to the recycle bin in language en."
  },
  "id_list": [
    18468028,
    18467384,
    18466967
  ]
}
```

## Notes

1. This delete action moves FAQs to the recycle bin instead of permanently removing them.
2. If a FAQ is deleted by mistake, it can be restored from the recycle bin.

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
