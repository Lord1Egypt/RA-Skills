---
name: pnpm-filtering
description: Rich selector syntax for restricting commands to specific workspace packages
---

# pnpm Filtering

Filtering restricts commands to specific subsets of packages. Selectors are specified via `--filter` or `-F`.

## Basic Matching

### By Package Name

```bash
pnpm --filter "@babel/core" test
pnpm --filter "@babel/*" test
pnpm --filter "*core" test
```

Without scope, pnpm picks the first match. If multiple packages share a name, specify scope or filter picks nothing.

### By Directory Glob

```bash
pnpm --filter "./packages/**" build
pnpm --filter "{packages/**}" build
```

## Dependency-based Selectors

### Package and Its Dependencies

Suffix with `...`:

```bash
pnpm --filter foo... test      # foo + all deps
pnpm --filter "@babel/preset-*..." test
```

### Only Dependencies (Exclude Package)

Suffix with `^...`:

```bash
pnpm --filter "foo^..." test   # only foo's deps
```

### Package and Its Dependents

Prefix with `...`:

```bash
pnpm --filter ...foo test      # foo + packages that depend on foo
```

### Only Dependents

Prefix with `...^`:

```bash
pnpm --filter "...^foo" test   # only packages depending on foo
```

### Both Directions

```bash
pnpm --filter "...foo..." build   # deps + foo + dependents
```

## Changed Since Commit/Branch

```bash
pnpm --filter "[origin/master]" test
pnpm --filter "...[origin/master]" test   # changed + dependents
pnpm --filter "[HEAD~5]" lint
```

## Glob + Dependency Operators

```bash
pnpm --filter ...{packages/**} build
pnpm --filter {packages/**}... test
pnpm --filter ...{packages/**}... build
pnpm --filter "{packages/**}[origin/master]" build
pnpm --filter "@babel/*{components/**}" build
```

## Exclusion

Prefix with `!`:

```bash
pnpm --filter=!foo build
pnpm --filter=!./lib test
```

## Multiple Filters

```bash
pnpm --filter ...foo --filter bar --filter baz... test
```

## Flags

### --filter-prod

Like `--filter` but omits `devDependencies` when selecting dependency projects.

### --test-pattern

Detect if modified files are tests. If so, dependents are not included in "changed since" filtering:

```bash
pnpm --filter="...[origin/master]" --test-pattern="test/*" test
```

### --changed-files-ignore-pattern

Ignore changed files by glob when filtering for changed projects:

```bash
pnpm --filter="...[origin/master]" --changed-files-ignore-pattern="**/README.md" run build
```

### --fail-if-no-match

Fail if no packages match. Set `failIfNoMatch: true` in config for permanent behavior.

## Usage Examples

```bash
# Run tests in changed packages and their dependents
pnpm --filter "...[origin/main]" test

# Build only app1 and its deps
pnpm --filter app1... build

# Lint all except internal packages
pnpm --filter=!"@myorg/internal-*" run lint

# Build packages under apps/
pnpm --filter "./apps/**" build
```

<!--
Source references:
- https://pnpm.io/filtering
-->
