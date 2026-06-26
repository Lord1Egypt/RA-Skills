---
name: undocs-read-more
description: Create links to other pages using the read-more component
---

# Read More Component

The `read-more` component creates styled links to other pages or external URLs.

## Basic Usage

### Internal Link

```mdc
:read-more{to="/guide"}
```

Creates a link to an internal route.

### External Link

```mdc
:read-more{to="https://unjs.io" title="UnJS Website"}
```

Creates a link to an external URL with a custom title.

## Props

- `to` (required): Destination URL or route path
- `title` (optional): Custom title text. If not provided, the URL is used (protocol is hidden)

## Usage Examples

### Link to Guide

```mdc
:read-more{to="/guide/getting-started"}
```

### External Link with Title

```mdc
:read-more{to="https://github.com/unjs/undocs" title="View on GitHub"}
```

### Link to Configuration

```mdc
Learn more about configuration:

:read-more{to="/config"}
```

## Key Points

- Creates visually distinct links for better UX
- Automatically handles internal vs external links
- Protocol is hidden from title when not specified
- Useful for cross-referencing documentation pages
- Styled consistently with the undocs theme

<!--
Source references:
- https://undocs.unjs.io/guide/components/components
-->
