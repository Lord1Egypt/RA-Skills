---
title: Upgrade Dependencies for React 19 Compatibility
impact: CRITICAL
impactDescription: Many packages require major version bumps
tags: dependencies, react19, upgrade, compatibility
---

## Upgrade Dependencies for React 19 Compatibility

Next.js 14+ with React 19 requires major version upgrades for several common packages. These packages will fail or show warnings if not upgraded.

**Required dependency upgrades:**

| Package | CRA Version | Next.js (React 19) Version |
|---------|-------------|---------------------------|
| `react-redux` | ^8.x | ^9.0.0 |
| `@reduxjs/toolkit` | ^1.x | ^2.0.0 |
| `react-router-dom` | ^6.x | Remove (use Next.js routing) |
| `react-tailwindcss-datepicker` | ^1.x | ^2.0.0 |
| `eslint` | ^8.x | ^9.0.0 |

**Check for React 19 compatibility before migrating:**

```bash
# Check for packages that may need updates
npm ls react
npm outdated
```

**Common compatibility issues:**

1. **Redux Toolkit v2** - Removes object notation for `extraReducers` (see state-redux rule)
2. **react-redux v9** - Requires RTK v2, new hook typing patterns
3. **ESLint v9** - Flat config format, many plugins need updates
4. **Date pickers** - Most React date picker libraries needed React 19 updates

**Upgrade strategy:**

```bash
# Upgrade Redux ecosystem together
npm install @reduxjs/toolkit@^2.0.0 react-redux@^9.0.0

# Check peer dependency warnings
npm install 2>&1 | grep "peer dep"
```

**Finding React 19 compatible versions:**

Check the package's GitHub releases or npm page for React 19 support. Look for:
- Release notes mentioning "React 19"
- `peerDependencies` allowing `react: "^19.0.0"`
