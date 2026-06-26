---
name: react-native-reusables-installation
description: How to install React Native Reusables (CLI init vs manual setup) and add components.
---

# Installation

## Create project (CLI)

Scaffold a new Expo project:

```bash
npx react-native-reusables init
```

Options: `-c, --cwd <cwd>`, `-t, --template <template>`. Templates include `minimal`, `minimal-uniwind`, `clerk-auth`.

## Add components

After init (or after manual setup), add components by name:

```bash
npx react-native-reusables add button
npx react-native-reusables add input dialog
npx react-native-reusables add -a   # all components
```

Options: `-y` skip confirmation, `-o` overwrite existing files, `-p, --path <path>`.

Import from your configured aliases:

```tsx
import { Button } from '@/components/ui/button';
import { Text } from '@/components/ui/text';

export default function Screen() {
  return (
    <Button>
      <Text>Click me</Text>
    </Button>
  );
}
```

## Manual setup (existing project)

If you are not using `init`, you must:

1. **Nativewind:** Follow [Nativewind installation](https://www.nativewind.dev/docs/getting-started/installation). Set `inlineRem: 16` in `metro.config.js` for `withNativeWind`.
2. **Dependencies:**
   ```bash
   npx expo install tailwindcss-animate class-variance-authority clsx tailwind-merge @rn-primitives/portal
   ```
3. **PortalHost:** Render `<PortalHost />` from `@rn-primitives/portal` in the root layout as the last child of your providers (required for Dialog, DropdownMenu, Tooltip, Popover, etc.).
4. **Path aliases:** Configure in `tsconfig.json`, e.g. `"@/*": ["./*"]`.
5. **Styles:** Add CSS variables to `global.css` (`:root` and `.dark:root`), map them in `tailwind.config.js`, and mirror in `lib/theme.ts` (including `NAV_THEME` for React Navigation).
6. **cn helper:** Add `lib/utils.ts` with `cn` using `clsx` and `tailwind-merge`.
7. **components.json:** Create so the CLI knows paths (see [customization](core-customization.md)).

Run `npx react-native-reusables doctor` to verify setup.

## Key Points

- Use **init** for new projects; use manual steps when adding to an existing Expo + Nativewind app.
- **PortalHost** is required for any overlay component (dialog, dropdown, tooltip, popover).
- Keep `global.css`, `tailwind.config`, and `theme.ts` in sync when changing theme variables.

<!--
Source references:
- https://github.com/founded-labs/react-native-reusables (docs: installation/index.mdx, installation/manual.mdx)
- https://reactnativereusables.com/docs/installation
-->
