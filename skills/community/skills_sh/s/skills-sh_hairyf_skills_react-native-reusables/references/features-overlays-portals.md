---
name: features-overlays-portals
description: PortalHost requirement, overlay components (Dialog, Popover, Select), contentInsets
---

# Overlays & Portals

Overlay components (Dialog, Popover, Select content, Dropdown, etc.) render through React Native's portal system. A **PortalHost** must be mounted at the root of the app for these to display correctly; otherwise overlay content may not appear or may be clipped.

## Usage

**PortalHost at root:** Place exactly one `PortalHost` high in the tree (e.g. in the root layout or app wrapper):

```tsx
import { PortalHost } from "@rn-primitives/portal";

export default function RootLayout() {
  return (
    <>
      <YourAppContent />
      <PortalHost />
    </>
  );
}
```

**Overlay components:** Dialog, Popover, SelectContent, DropdownMenuContent, and similar components render their content into the portal. Import from `@/components/ui/<component>` after adding via CLI.

**SelectContent insets:** For Select (and similar dropdowns), pass `contentInsets` so the content respects safe area or keyboard. Often used with `useSafeAreaInsets()` or a fixed inset object:

```tsx
import { useSafeAreaInsets } from "react-native-safe-area-context";

const contentInsets = useSafeAreaInsets();

<Select>
  <SelectTrigger className="w-[180px]">
    <SelectValue placeholder="Select..." />
  </SelectTrigger>
  <SelectContent insets={contentInsets} className="w-[180px]">
    <SelectItem label="Option" value="opt">Option</SelectItem>
  </SelectContent>
</Select>
```

**Dependencies:** Overlay primitives require the corresponding `@rn-primitives/*` package (e.g. `@rn-primitives/dialog`, `@rn-primitives/select`). The CLI `add` command installs them; for manual setup, install the primitive then copy the UI component.

## Key Points

- Without a root `PortalHost`, overlay content may not show or may be mispositioned. Add it once at app root.
- Use `contentInsets` (or safe area insets) on SelectContent and similar so content is not hidden by notches or keyboard.
- Components link to [RN Primitives](https://rnprimitives.com) docs and API; refer there for full prop lists.

<!--
Source references:
- https://github.com/founded-labs/react-native-reusables (apps/docs/content/docs/components/dialog.mdx, select.mdx)
- https://reactnativereusables.com/docs/components/dialog
- https://reactnativereusables.com/docs/components/select
-->
