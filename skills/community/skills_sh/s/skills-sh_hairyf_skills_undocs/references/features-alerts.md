---
name: undocs-alerts
description: Use alert components (note, tip, important, warning, caution) in markdown
---

# Alert Components

Undocs provides MDC (Markdown Components) for creating alert boxes in your documentation.

## Available Alerts

### Note

Highlights information that users should take into account:

```mdc
::note
Highlights information that users should take into account, even when skimming.
::
```

### Tip

Optional information to help users be more successful:

```mdc
::tip
Optional information to help a user be more successful.
::
```

### Important

Crucial information necessary for users to succeed:

```mdc
::important
Crucial information necessary for users to succeed.
::
```

### Warning

Critical content demanding immediate user attention:

```mdc
::warning{to="/"}
Critical content demanding immediate user attention due to potential risks.
::
```

### Caution

Negative potential consequences of an action:

```mdc
::caution{to="/"}
Negative potential consequences of an action.
::
```

## Props

- `to` (optional): Link destination URL or route path. When provided, the alert becomes clickable.

## Usage Examples

### Simple Alert

```mdc
::note
This is a simple note without any links.
::
```

### Alert with Link

```mdc
::warning{to="/migration-guide"}
Breaking changes in v2.0. Please read the migration guide.
::
```

### Nested Content

Alerts can contain markdown content:

```mdc
::important
This is important information.

- Point 1
- Point 2
- Point 3
::
```

## Key Points

- Alerts use MDC syntax (`::component-name`)
- All alerts support markdown content inside
- `warning` and `caution` can include a `to` prop for navigation
- Alerts are rendered with appropriate colors and icons automatically
- Based on Nuxt UI Prose components

<!--
Source references:
- https://undocs.unjs.io/guide/components/components
-->
