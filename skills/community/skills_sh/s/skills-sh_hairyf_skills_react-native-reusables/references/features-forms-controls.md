---
name: features-forms-controls
description: Form controls — Label, Input, Select, Checkbox, RadioGroup; compound components and primitives
---

# Form Controls & Compound Components

React Native Reusables provides form-style components built on RN Primitives: Label, Input, Textarea, Select, Checkbox, RadioGroup. They follow the same compound-component pattern as shadcn/ui and require the matching `@rn-primitives/*` dependency when added manually.

## Usage

**Label + Input:** Use `Label` with `nativeID` and link via `aria-labelledby` / `accessibilityLabelledBy` for accessibility. Style with `className` on both:

```tsx
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

<View>
  <Label nativeID="email" className="text-sm font-medium">Email</Label>
  <Input className="mt-2" accessibilityLabelledBy="email" />
</View>
```

**Select:** Compound component: `Select`, `SelectTrigger`, `SelectValue`, `SelectContent`, `SelectGroup`, `SelectLabel`, `SelectItem`. Add with `npx react-native-reusables add select` (installs `@rn-primitives/select`). Use `SelectContent` with `contentInsets` for safe area.

**Checkbox / RadioGroup:** Add with `add checkbox` or `add radio-group`. Use with `Label` and optional `Text` for description. Controlled usage via `checked` / `onCheckedChange` (checkbox) or `value` / `onValueChange` (radio group).

**Installation:** Prefer CLI: `npx react-native-reusables add input label select checkbox radio-group`. Manual: install the primitive (e.g. `npx expo install @rn-primitives/select`), then copy the component from the registry (Nativewind or Uniwind variant) and fix import paths.

## Key Points

- Each form component has a corresponding RN Primitives package; CLI installs it automatically.
- Use `Text` from `@/components/ui/text` (and `TextClassContext` where needed) so label/description text inherits styles correctly.
- Overlay parts (SelectContent, DialogContent) require a root `PortalHost`; see [features-overlays-portals](references/features-overlays-portals.md).

<!--
Source references:
- https://github.com/founded-labs/react-native-reusables (apps/docs/content/docs/components/input.mdx, select.mdx, checkbox.mdx, label.mdx, radio-group.mdx)
- https://reactnativereusables.com/docs/components/input
- https://reactnativereusables.com/docs/components/select
-->
