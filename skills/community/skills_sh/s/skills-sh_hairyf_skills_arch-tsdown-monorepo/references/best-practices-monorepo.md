---
name: best-practices-monorepo
description: Catalogs, workspace deps, and release practices
---

# Best Practices (Monorepo)

## Use pnpm Catalogs for Versions

- Put shared devDependency versions in **pnpm-workspace.yaml** under **catalogs** (e.g. `cli`, `testing`, `types`, `inlined`).
- In each package, reference them as `catalog:cli`, `catalog:testing`, etc., instead of hardcoding versions.
- Benefits: single place to upgrade tsdown, vitest, typescript, eslint; consistent versions across all packages.

## Prefer workspace:* for Internal Deps

- Use `"@scope/other-pkg": "workspace:*"` for dependencies between workspace packages.
- pnpm resolves them to the local package; at publish time they are replaced with the published version range (e.g. same version).
- Avoid using `link:` or file paths for workspace packages; `workspace:*` is the standard and works with publish.

## Keep Root private: true

- Root `package.json` should have `"private": true` so it is never published.
- Only packages under `packages/*` that have a `name` and no `private: true` are publishable.

## Exports: Source in Dev, dist in Publish

- In each package, **exports** point to source (e.g. `".": "./src/index.ts"`) for fast iteration and correct types when developing in the monorepo.
- Use **publishConfig.exports** to point to **dist/** (e.g. `".": "./dist/index.mjs"`) so published consumers get the built output and types.
- tsdown’s **exports.devExports** and **exports.enabled** align with this pattern.

## One-Time Publish, Then Trusted Publisher

- Publish each package to npm **once** manually so the package name exists.
- Then connect each package to GitHub via npm’s Trusted Publisher (package access page).
- For all later releases, use **pnpm run release** (bumpp) and push the tag; let CI publish. Do not store npm tokens in CI; use OIDC.

## Build Order

- Root script `pnpm -r run build` runs each package’s `build` in dependency order when using pnpm (packages that depend on others get built after their deps). So `utils` builds before `core` if core depends on utils.

## Lint and Typecheck the Whole Repo

- Run **lint** and **typecheck** from root (`nr lint`, `nr typecheck`) so the entire workspace is checked. CI does this in the lint job before the heavier test matrix.

<!--
Source references:
- https://github.com/hairyf/starter-monorepo
- https://pnpm.io/catalogs
- https://github.com/e18e/ecosystem-issues/issues/201
-->
