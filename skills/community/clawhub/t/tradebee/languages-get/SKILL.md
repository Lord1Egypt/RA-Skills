---
name: languages-get
description: A language list retrieval skill based on the "Tradebee Website Builder" Open API. It is used to obtain the list of enabled site languages and provide the dependency data source for the `language` parameter used by other skills.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# languages-get

## Overview

Use the "Tradebee Website Builder" Open API to retrieve the list of currently enabled languages for the site. This skill can be used to:

- Retrieve platform-supported languages
- Provide selectable values for the `language` parameter
- Support AI Agent dropdown linkage
- Support OpenClaw Skill dependency injection
- Support chained Workflow calls

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

## Output Structure

### Top-Level Fields

| Field  | Type           | Description                            |
|--------|----------------|----------------------------------------|
| status | boolean        | Request status, `true` for success / `false` for failure |
| msg    | string         | Response message                       |
| data   | object \| null | Response data, `null` on failure       |

### `data.list[]` (array of objects)

Each language record contains the following fields:

| Field    | Type   | Description                              |
|----------|--------|------------------------------------------|
| language | string | Site language code identifier (for API use) |
| name     | string | Language name (for display)              |

## Usage Example

### Query

```json
{
}
```

---

## Notes

1. Configure `BEE_API_KEY` in the environment before using this skill. Never provide API keys in tool inputs, prompts, examples, logs, or chat text.

---

## Applicable Scenarios

- Retrieve currently enabled language sites
- Language filtering
