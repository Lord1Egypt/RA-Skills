---
name: best-practices-troubleshooting
description: doctor, --log-level all, common issues (PortalHost, aliases, dependencies)
---

# Troubleshooting & Debugging

Use the CLI `doctor` command to validate setup. When something fails, run with verbose logging to gather details for bug reports or local fixes.

## Usage

**doctor:** Check project setup and get actionable fixes:

```bash
npx react-native-reusables doctor [options]
# -c, --cwd <cwd>   working directory
# -s, --summary      summary only
# -y, --yes          skip confirmation
```

**Verbose logging:** Prepend `--log-level all` to any command to get full logs (useful when filing issues or debugging):

```bash
npx react-native-reusables --log-level all doctor
npx react-native-reusables --log-level all add button
```

**Common issues:**

- **Overlays not showing** — Ensure `PortalHost` is mounted at the app root. Without it, Dialog, Popover, SelectContent, etc. may not render or may be clipped.
- **Path aliases** — Components use `@/components/ui/*`. Configure `@/` in `tsconfig.json` and your bundler (e.g. Expo/Metro) so imports resolve. Run `doctor` to verify.
- **Missing dependencies** — If you added components manually, install the required `@rn-primitives/*` packages (e.g. `@rn-primitives/dialog`, `@rn-primitives/select`). CLI `add` does this automatically.
- **Text / Icon not found** — Ensure `Text` and `Icon` from `@/components/ui/text` and `@/components/ui/icon` are present; many components depend on them. Add with `add text icon` if missing.
- **Styling (Nativewind/Uniwind)** — Ensure global CSS and theme are set up per [core-installation](references/core-installation.md) and [core-customization](references/core-customization.md); run `doctor` to catch misconfig.

## Key Points

- Run `doctor` after init or when adding components manually; fix any reported issues before assuming a bug.
- When reporting bugs, include output of `npx react-native-reusables --log-level all doctor` (and the failing command) so maintainers can reproduce.

<!--
Source references:
- https://github.com/founded-labs/react-native-reusables (apps/docs/content/docs/cli.mdx)
- https://reactnativereusables.com/docs/cli
-->
