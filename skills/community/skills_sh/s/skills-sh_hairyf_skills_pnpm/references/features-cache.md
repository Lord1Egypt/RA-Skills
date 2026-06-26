---
name: features-cache
description: pnpm cache commands for viewing and managing package metadata cache
---

# pnpm Cache

:::warning
Cache commands are experimental.
:::

pnpm caches package metadata and tarballs. Use these commands to inspect or clear the cache.

## Commands

```bash
# List cached packages (supports glob filter)
pnpm cache list

# List configured registries
pnpm cache list-registries

# Delete packages from cache
pnpm cache delete <pkg>...

# View cache contents/details
pnpm cache view
```

## Store vs Cache

- **Store** (`pnpm store`): Content-addressable package files (hard-linked). See [core-store](core-store.md).
- **Cache**: Downloaded tarballs and metadata before they are extracted to the store.

## Configuration

Cache location can be configured in `.npmrc`:

```ini
cache-dir=~/.pnpm-store/cache
```

## Key Points

- Use `cache delete` to free space or fix corrupted cached packages
- `cache list` helps debug what's in the cache
- Store commands (`pnpm store prune`, etc.) are for the content store, not the cache

<!--
Source references:
- https://pnpm.io/cli/cache
- https://pnpm.io/cli/cache-list
- https://pnpm.io/cli/cache-delete
-->
