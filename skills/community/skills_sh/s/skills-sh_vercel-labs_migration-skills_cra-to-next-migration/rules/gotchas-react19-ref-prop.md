---
title: Handle React 19 Ref Prop Changes
impact: HIGH
impactDescription: ref is now a regular prop in React 19
tags: gotchas, react19, ref, forwardRef
---

## Handle React 19 Ref Prop Changes

React 19 changes how refs work: `ref` is now a regular prop, and
`forwardRef` is no longer required for most use cases.

**Error message:**

```
Accessing element.ref was removed in React 19. ref is now a regular prop.
It will be removed from the JSX Element type in a future release.
```

**Example: Radix UI Popover triggering this error**

```tsx
// ColorPicker.tsx - This Radix UI component triggers the warning
import * as Popover from '@radix-ui/react-popover'

function ColorPickerTrigger() {
  return (
    <Popover.Root>
      <Popover.Trigger type="button" className="color-picker__button">
        Select Color
      </Popover.Trigger>
      <Popover.Content>
        {/* color picker content */}
      </Popover.Content>
    </Popover.Root>
  )
}
```

The error points to `Popover.Trigger` because older versions of Radix UI internally access `element.ref` using the deprecated React API. This is not a problem with your code - it's the library's internal implementation.

**Why this happens:**

1. Third-party libraries (like Radix UI, React Hook Form) access `element.ref` directly using the old API
2. Your code uses `forwardRef` when it's no longer needed
3. Custom components haven't been updated for React 19's ref handling

**Solution 1: Update third-party libraries**

Many libraries have released React 19 compatible versions. Update to the latest versions:

```bash
# Update Radix UI primitives (common ones that use refs internally)
npm update @radix-ui/react-popover @radix-ui/react-select @radix-ui/react-dropdown-menu @radix-ui/react-dialog @radix-ui/react-tooltip

# Update React Hook Form
npm update react-hook-form

# Update all dependencies to latest
npm update
```

**Radix UI React 19 compatible versions:**

Versions 1.1.x+ of most Radix UI primitives are React 19 compatible. Example upgrades:

```json
{
  "@radix-ui/react-popover": "1.0.3" -> "1.1.15",
  "@radix-ui/react-tabs": "1.0.2" -> "1.1.13",
  "@radix-ui/react-dialog": "^1.1.0",
  "@radix-ui/react-select": "^2.1.0",
  "@radix-ui/react-dropdown-menu": "^2.1.0",
  "@radix-ui/react-tooltip": "^1.1.0",
  "@radix-ui/react-checkbox": "^1.1.0",
  "@radix-ui/react-radio-group": "^1.2.0"
}
```

Check the library's changelog for React 19 compatibility notes.

**Solution 2: Migrate forwardRef to ref prop (for your own components)**

Before (React 18 and earlier):

```tsx
import { forwardRef } from 'react'

interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ children, onClick }, ref) => {
    return (
      <button ref={ref} onClick={onClick}>
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'
```

After (React 19):

```tsx
interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
  ref?: React.Ref<HTMLButtonElement>
}

function Button({ children, onClick, ref }: ButtonProps) {
  return (
    <button ref={ref} onClick={onClick}>
      {children}
    </button>
  )
}
```

**Solution 3: TypeScript ref typing**

For proper TypeScript support with ref as a regular prop:

```tsx
import { Ref, RefObject } from 'react'

// Option 1: Use React.Ref<T> for flexibility (accepts callback refs and RefObjects)
interface InputProps {
  value: string
  onChange: (value: string) => void
  ref?: Ref<HTMLInputElement>
}

// Option 2: Use RefObject<T> if you only accept object refs
interface InputProps {
  value: string
  onChange: (value: string) => void
  ref?: RefObject<HTMLInputElement>
}

function Input({ value, onChange, ref }: InputProps) {
  return (
    <input
      ref={ref}
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
  )
}
```

**Solution 4: Temporary workaround for incompatible libraries**

If a library hasn't been updated yet, you can suppress the warning temporarily while waiting for updates:

```tsx
// Wrap the problematic component to handle the ref differently
'use client'

import { useRef, useEffect } from 'react'
import { SomeLibraryComponent } from 'some-library'

export function WrappedComponent(props: ComponentProps) {
  const internalRef = useRef<HTMLElement>(null)

  // Pass ref through a different mechanism if needed
  return <SomeLibraryComponent {...props} />
}
```

**Search patterns for affected code:**

```bash
# Find forwardRef usage that can be simplified
grep -r "forwardRef" --include="*.tsx" --include="*.ts"

# Find components receiving ref prop
grep -r "ref\s*=" --include="*.tsx" --include="*.ts"

# Find displayName assignments (often paired with forwardRef)
grep -r "\.displayName\s*=" --include="*.tsx" --include="*.ts"
```

**Migration checklist:**

1. Update all third-party dependencies to their latest versions
2. Search for `forwardRef` in your codebase
3. Convert `forwardRef` components to regular functions with ref as a prop
4. Update TypeScript interfaces to include the ref prop
5. Remove `displayName` assignments (no longer needed without forwardRef)
6. Test that refs are properly forwarded to DOM elements

**Note on backwards compatibility:**

`forwardRef` still works in React 19 but is no longer necessary. You can migrate incrementally - the old pattern won't break, it's just more verbose than needed.

See also: `components-third-party.md` for wrapping third-party client components in Next.js.
