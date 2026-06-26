# Output Format

Understanding winguictl command output formats.

## Content Boundary Markers

Snapshot and find commands wrap output with boundary markers:

```
--- WINGUICTL_CONTENT nonce=<nonce> ---
[output content]
--- END_WINGUICTL_CONTENT nonce=<nonce> ---
```

**Verify nonce matches** before trusting captured content.

## Element Format

```
- "Element Text" [attribute1="value1" attribute2="value2" relative_rect=(x,y widthxheight)]
```

## Coordinate Attributes

| Attribute | Description |
|-----------|-------------|
| `relative_rect` | Window-relative coordinates (origin: window top-left) |
| `absolute_rect` | Screen-absolute coordinates (origin: screen top-left) |

**Note**: Coordinate type is indicated by attribute name prefix, not generic `rect` field.

## Common Attributes

| Attribute | Description |
|-----------|-------------|
| `text` | Element text/content (in quotes) |
| `control_type` | UIA or Win32 control type |
| `class` | Window class name |
| `hwnd` | Win32 control handle |
| `automation_id` | UIA automation ID |
| `runtime_id` | UIA runtime ID |
| `visible` | Whether element is visible |
| `enabled` | Whether element is enabled |
| `confidence` | Match confidence (0-1) for OCR/image |
| `supported_actions` | Comma-separated UIA actions |
| `toggle_state` | Toggle state: 0=off, 1=on, 2=indeterminate |
| `is_expanded` | Expanded state: 0=collapsed, 1=expanded |
| `is_selected` | Selected state: 0=no, 1=yes |
| `state` | Window state: "minimized", "maximized" |
| `foreground` | Foreground window: "true" |
| `pid` | Process ID |
| `process` | Process name |
| `parent_id` | Parent window handle |

## JSON Output

Action and window commands output JSON:

```json
{
  "ok": true,
  "code": "OK",
  "message": "click executed",
  "data": {
    "window_id": "12345",
    "window_title": "Window Title"
  }
}
```

## Result Codes

| Code | Description |
|------|-------------|
| `OK` | Operation succeeded |
| `FAILED` | Operation failed |
| `VALIDATION_ERROR` | Invalid input parameters |
| `ERROR` | Unexpected error |
| `DRY_RUN` | Preview mode (no action taken) |
