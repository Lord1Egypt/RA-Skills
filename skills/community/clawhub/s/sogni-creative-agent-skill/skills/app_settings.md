---
name: app_settings
description: Toggle user-visible app preferences such as the safe-content filter.
always_loaded: false
tool_names:
  - set_content_filter
---

# App settings

Read/write controls over user-visible app preferences (currently the safe-content filter). Kept narrow on purpose — a settings change is a deliberate user action, not something the LLM should chain into a creative workflow without an explicit ask.

## Tools

- `set_content_filter` — toggle the safe-content filter on / off.

## Constraints

- Only invoke when the user has explicitly asked to change a setting.
