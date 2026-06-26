---
name: undocs-nuxt-ui-prose
description: Use Nuxt UI Prose components in undocs markdown files
---

# Nuxt UI Prose Components

Undocs is built on Nuxt UI, which provides a rich set of Prose components for markdown content.

## Available Components

All Nuxt UI Prose components are available in your markdown files. See the [Nuxt UI Typography documentation](https://ui4.nuxt.com/docs/typography) for the complete list.

## Common Prose Components

### Code Groups

Group multiple code blocks with tabs:

````markdown
```json [package.json]
{
  "name": "example"
}
```

```ts [config.ts]
export default {}
```
````

### Tabs

Create tabbed content:

```markdown
::tabs
  ::div
  ---
  label: Preview
  ---
  Content here
  ::
  ::div
  ---
  label: Code
  ---
  Code here
  ::
::
```

### Alerts

Use alert components (also available as MDC):

```markdown
::note
This is a note.
::
```

## MDC Syntax

Undocs uses MDC (Markdown Components) syntax:

```markdown
::component-name{prop="value"}
Content
::
```

## Custom Components

You can use custom Vue components in markdown:

```markdown
::my-custom-component{title="Hello"}
Content
::
```

## Typography

Nuxt UI Prose provides enhanced typography:

- Better heading styles
- Improved code blocks
- Enhanced lists
- Better blockquotes
- Improved tables

## Code Highlighting

Code blocks are highlighted using Shiki:

- Multiple themes (github-dark, github-light)
- Language detection
- Syntax highlighting
- Line numbers support

## Key Points

- All Nuxt UI Prose components are available
- Use MDC syntax for components
- Code groups are automatically created from consecutive code blocks
- Enhanced typography is applied automatically
- Shiki is used for code highlighting
- Custom Vue components can be used

<!--
Source references:
- https://ui4.nuxt.com/docs/typography
- https://content.nuxt.com/guide/writing/mdc
-->
