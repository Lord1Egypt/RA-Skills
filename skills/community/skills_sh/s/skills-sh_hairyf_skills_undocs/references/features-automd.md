---
name: undocs-automd
description: Integrate automd for automatic documentation updates
---

# Automd Integration

Undocs supports integration with [automd](https://automd.unjs.io) for automatic documentation updates.

## Enable Automd

Enable automd in your configuration:

```yaml
# .config/docs.yaml
automd: true
```

## Automd Features

### File Includes

Include partial files:

```markdown
<!-- automd:file src="../.partials/warn.md" -->
```

### Contributors

Automatically update contributor lists:

```markdown
<!-- automd:contributors license=MIT author="pi0,atinux" -->
```

### JSDoc References

Generate configuration references from TypeScript schema:

```markdown
<!-- automd:jsdocs src="../../schema/config.schema.ts" -->
```

This generates formatted reference tables from JSDoc comments.

### Package Information

Update package information:

```markdown
<!-- automd:with-automd -->
```

## Automd Configuration

Automd configuration is loaded from your docs directory:

```typescript
const config = await automd.loadConfig(docsConfig.dir, docsConfig.automd);
```

## Transform Process

1. **Before Parse**: Files with `<!-- automd:` comments are transformed
2. **Transform**: Automd processes the content
3. **Save**: Updated content is written back to the file
4. **Meta**: Frontmatter is updated with `automd: true`

## Frontmatter Marking

Files processed by automd are marked in frontmatter:

```yaml
---
automd: true
---
```

## Error Handling

If automd encounters issues:

- Warnings are logged to console
- Original content is preserved
- Transform is skipped for that file

## Use Cases

### Keep Documentation Updated

```markdown
<!-- automd:file src="../.partials/warn.md" -->
> [!IMPORTANT]
> This feature is experimental.
```

### Auto-generate API References

```markdown
<!-- automd:jsdocs src="../../src/config.ts" -->
```

### Update Contributors

```markdown
<!-- automd:contributors license=MIT -->
```

## Key Points

- Enable with `automd: true` in config
- Supports file includes, contributors, and JSDoc references
- Transforms happen before markdown parsing
- Updated content is saved back to files
- Files are marked with `automd: true` in frontmatter
- Errors are logged but don't break the build

<!--
Source references:
- https://automd.unjs.io
- https://github.com/unjs/undocs/blob/main/app/modules/content/hooks.ts
-->
