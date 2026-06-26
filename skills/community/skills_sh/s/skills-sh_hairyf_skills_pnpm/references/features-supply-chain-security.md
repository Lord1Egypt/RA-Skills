---
name: pnpm-supply-chain-security
description: Mitigate supply chain attacks—allowBuilds, blockExoticSubdeps, trustPolicy
---

# pnpm Supply Chain Security

pnpm v10+ mitigates supply-chain risks with several settings.

## Block Risky postinstall Scripts

pnpm v10 **disables** `postinstall` scripts in dependencies by default. Use `allowBuilds` to whitelist trusted packages:

```yaml
# pnpm-workspace.yaml or .npmrc
allowBuilds:
  - '@airbnb/node-memwatch'
  - '@apollo/protobufjs'
```

**Avoid** `dangerouslyAllowAllBuilds: true`. Prefer explicit allow list.

## Block Exotic Transitive Dependencies

```yaml
blockExoticSubdeps: true
```

Prevents transitive deps from using Git repos or direct tarball URLs.

## Delay New Versions

```yaml
minimumReleaseAge: 1440   # minutes (24h)
```

Packages must be published at least this long before installation.

## Trust Policy

```yaml
trustPolicy: no-downgrade
```

Prevents installing if trust level decreased (e.g. previously had provenance, now doesn't).

```yaml
trustPolicyExclude:
  - some-package
trustPolicyIgnoreAfter: 172800   # seconds (2 days) - ignore for older packages
```

## Lockfile

Always commit `pnpm-lock.yaml` to pin versions.

## Best Practices

1. Use `allowBuilds` instead of `dangerouslyAllowAllBuilds`
2. Set `blockExoticSubdeps: true` to restrict exotic sources
3. Consider `minimumReleaseAge: 1440` for 24h delay
4. Enable `trustPolicy: no-downgrade` when using npm provenance
5. Use security tools (Socket, Snyk, Aikido) for monitoring

<!--
Source references:
- https://pnpm.io/supply-chain-security
-->
