---
name: undocs-content-transformation
description: Automatic content transformations in undocs markdown
---

# Content Transformations

Undocs automatically transforms markdown content to enhance documentation writing experience.

## GitHub Notes

GitHub-flavored markdown blockquotes are automatically converted to alert components:

```markdown
> [!NOTE]
> Highlights information that users should take into account, even when skimming.
```

Becomes:

```mdc
::note
Highlights information that users should take into account, even when skimming.
::
```

### Supported Types

- `> [!NOTE]` → `::note`
- `> [!TIP]` → `::tip`
- `> [!IMPORTANT]` → `::important`
- `> [!WARNING]` → `::warning`
- `> [!CAUTION]` → `::caution`

## Auto Code Groups

Consecutive code blocks are automatically grouped into tabs:

````markdown
```json [package.json]
{
  "scripts": {
    "dev": "undocs dev"
  }
}
```

```ts [server/api/hello.get.ts]
export default defineEventHandler(() => {
  return { hello: "world" };
});
```
````

These are automatically converted to a code group component with tabs.

## Steps

Numbered lists with content are automatically converted to step components:

```markdown
1. Install Package

   ::note
   Steps only work with numbered lists.
   ::

   :pm-install{name="undocs"}

2. Run development server

   :pm-run{script="dev"}

3. Done ✅
```

**Important:** Steps only work with numbered lists that have content inside at least one item. The list cannot be a child of another component, and content within a Markdown list needs at least 2 tabs of indentation to be considered as a child of the list.

## Config References

Markdown formatted configuration references are automatically styled:

```markdown
### `$schema`

- **Type**: `string`

### `automd`

- **Type**: `boolean`

Enable integration with https://automd.unjs.io
```

This creates a formatted reference table automatically.

**Tip:** Use [automd:jsdocs](https://automd.unjs.io/generators/jsdocs) to reference schema files directly:

```markdown
<!-- automd:jsdocs src="../../schema/config.schema.ts" -->
```

## Key Points

- Transformations happen automatically during markdown processing
- GitHub notes are converted to MDC alert components
- Consecutive code blocks become code groups
- Numbered lists with content become step components
- Config references are automatically formatted
- All transformations preserve original markdown structure

<!--
Source references:
- https://undocs.unjs.io/guide/components/content-transformation
-->
