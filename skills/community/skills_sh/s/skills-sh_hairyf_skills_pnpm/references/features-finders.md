---
name: pnpm-finders
description: Search dependency graph by package properties (v10.16+)
---

# pnpm Finders

Finders search the dependency graph by any package property, not just name. Define in `.pnpmfile.cjs`, use with `pnpm list` and `pnpm why`.

## Define Finders

```js
// .pnpmfile.cjs
module.exports = {
  finders: {
    react17: (ctx) => {
      return ctx.readManifest().peerDependencies?.react === "^17.0.0"
    }
  }
}
```

Return `true` to include, `false` to skip, or a `string` for extra info.

## Context (ctx)

| Field | Description |
|-------|-------------|
| `name` | Package name |
| `version` | Package version |
| `readManifest()` | Returns `package.json` object |

## Usage

```bash
pnpm why --find-by=react17
pnpm list --find-by=react17
```

## Return Extra Metadata

```js
finders: {
  react17: (ctx) => {
    const manifest = ctx.readManifest()
    if (manifest.peerDependencies?.react === "^17.0.0") {
      return `license: ${manifest.license}`
    }
    return false
  }
}
```

## Example Use Cases

- Find packages with specific license
- Detect minimum Node.js version requirements
- List packages that expose binaries
- Print funding URLs

<!--
Source references:
- https://pnpm.io/finders
- https://pnpm.io/pnpmfile
-->
