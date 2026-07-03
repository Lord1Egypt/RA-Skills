---
name: custompage-delete
description: A custom page delete skill based on the "Tradebee Website Builder" Open API. It is used to move one or more custom pages to the recycle bin under a specified site language.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# custompage-delete

## Overview

Use the Tradebee Website Builder Open API to move one or more custom pages to the recycle bin.

## Input Parameters

### `language` (string, **Required**)

Exact site language code to delete from.

### `id_list` (array, **Required**)

Custom page ID list, up to 100 items.

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact custom page delete request after seeing the final language and custom page IDs.

## Usage Example

```json
{
  "language": "en",
  "id_list": [23, 24],
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: move custom pages 23 and 24 to the recycle bin in language en."
  }
}
```
