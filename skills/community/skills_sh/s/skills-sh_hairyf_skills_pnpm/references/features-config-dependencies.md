---
name: pnpm-config-dependencies
description: Share hooks, catalogs, patches across projects via config packages
---

# pnpm Config Dependencies

Config dependencies centralize configuration (hooks, catalogs, patches, overrides) across repositories. They install **before** regular dependencies.

## Setup

```bash
pnpm add --config @myorg/pnpm-configs
```

Adds to `pnpm-workspace.yaml`:

```yaml
configDependencies:
  '@myorg/pnpm-configs': "1.0.0+sha512-..."
```

## Constraints

- Config dependencies **cannot** have their own dependencies
- **Cannot** define lifecycle scripts (preinstall, postinstall, etc.)

## Use Cases

### Load Hooks from Config Package

```js
// .pnpmfile.cjs
const { readPackage } = require('.pnpm-config/@myorg/pnpm-configs')

module.exports = {
  hooks: { readPackage }
}
```

### Load Allow List for Builds

```yaml
# pnpm-workspace.yaml
configDependencies:
  '@myorg/trusted-deps': 0.1.0+sha512-...
onlyBuiltDependenciesFile: node_modules/.pnpm-config/@myorg/trusted-deps/allow.json
```

### Add Catalogs via updateConfig

```js
// @myorg/pnpm-plugin-my-catalogs/pnpmfile.cjs
module.exports = {
  hooks: {
    updateConfig(config) {
      config.catalogs.default ??= {}
      config.catalogs.default['is-odd'] = '1.0.0'
      return config
    }
  }
}
```

After `pnpm add --config @myorg/pnpm-plugin-my-catalogs`:

```bash
pnpm add is-odd@catalog:
```

### Reference Patches in Config Package

```yaml
configDependencies:
  my-patches: "1.0.0+sha512-..."
patchedDependencies:
  react: "node_modules/.pnpm-config/my-patches/react.patch"
```

## Auto-load pnpmfile

Packages matching `pnpm-plugin-*` or `@*/pnpm-plugin-*` automatically load their `pnpmfile.cjs`.

<!--
Source references:
- https://pnpm.io/config-dependencies
-->
