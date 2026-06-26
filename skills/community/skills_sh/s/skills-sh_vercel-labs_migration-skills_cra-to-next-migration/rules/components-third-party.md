---
title: Wrap Third-Party Client Components
impact: MEDIUM
impactDescription: Handle external library components
tags: components, third-party, libraries
---

## Wrap Third-Party Client Components

Many third-party libraries export Client Components that need `'use client'`. Create wrapper components to use them in Server Components.

**CRA Pattern (before):**

```tsx
// Direct import works - everything is client
import { Carousel } from 'some-carousel-library'
import { DatePicker } from 'some-datepicker'

export default function Page() {
  return (
    <div>
      <Carousel items={items} />
      <DatePicker onChange={handleChange} />
    </div>
  )
}
```

**Next.js Pattern (after):**

```tsx
// components/Carousel.tsx
'use client'

// Re-export with 'use client' directive
export { Carousel } from 'some-carousel-library'

// Or create a wrapper with custom props
import { Carousel as BaseCarousel } from 'some-carousel-library'

export function Carousel(props) {
  return <BaseCarousel {...props} />
}
```

```tsx
// app/page.tsx (Server Component)
import { Carousel } from '@/components/Carousel'

export default async function Page() {
  const items = await fetchItems()

  return (
    <div>
      <Carousel items={items} />
    </div>
  )
}
```

**Pattern for multiple components:**

```tsx
// components/ui/index.tsx
'use client'

// Re-export all client components from one file
export { Carousel } from 'some-carousel-library'
export { DatePicker } from 'some-datepicker'
export { Select, Dropdown } from 'some-ui-library'
```

**Check if library supports Server Components:**

Some modern libraries export separate client/server entry points:

```tsx
// Some libraries have RSC support
import { ServerSafeComponent } from 'modern-library' // Works in Server Components
import { ClientComponent } from 'modern-library/client' // Needs 'use client'
```

Always check the library's documentation for Next.js App Router compatibility.

## React 19 Compatibility

Next.js 16+ uses React 19, which changes how refs are forwarded to components. Many third-party libraries may show warnings or errors until they're updated.

**Common warnings:**

```
Warning: Function components cannot be given refs. Attempts to access
this ref will fail. Did you mean to use React.forwardRef()?
```

```
Accessing element.ref was removed in React 19. ref is now a regular prop.
It will be removed from the JSX Element type in a future release.
```

The second error occurs when library code internally accesses `element.ref` using React's deprecated API. This is common with Radix UI components like `Popover.Trigger`, `Select.Trigger`, etc. See `gotchas-react19-ref-prop.md` for detailed solutions.

**Affected libraries (check for updates):**

- Radix UI primitives
- Headless UI
- Reach UI
- React Aria
- Downshift
- React Select
- Older versions of Material UI

**Solution 1: Update to React 19 compatible versions**

```bash
# Check for updates
npm outdated

# Update specific packages
npm update @radix-ui/react-dialog @radix-ui/react-dropdown-menu
```

Most actively maintained libraries have released React 19 compatible versions.

**Solution 2: Temporary wrapper to suppress warnings**

If updates aren't available yet, create a wrapper component:

```tsx
'use client'

import { forwardRef } from 'react'
import { Dialog as RadixDialog } from '@radix-ui/react-dialog'

// Wrapper that properly forwards refs
export const Dialog = forwardRef<HTMLDivElement, React.ComponentProps<typeof RadixDialog>>(
  (props, ref) => {
    return <RadixDialog {...props} ref={ref} />
  }
)
Dialog.displayName = 'Dialog'
```

**Solution 3: Use legacy ref pattern**

For components that don't support ref forwarding:

```tsx
'use client'

import { useRef, useEffect } from 'react'
import { SomeComponent } from 'legacy-library'

function Wrapper() {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Access the DOM through the container if needed
    const element = containerRef.current?.querySelector('.target-element')
  }, [])

  return (
    <div ref={containerRef}>
      <SomeComponent />
    </div>
  )
}
```

**Check library compatibility:**

Before starting migration, audit your dependencies:

```bash
# List all dependencies
npm ls --depth=0

# Check each UI library's GitHub issues/releases for React 19 support
```

Most popular libraries have React 19 compatibility in their latest versions. Prioritize updating these dependencies early in the migration process.

See also: `gotchas-dynamic-imports.md` for code splitting with next/dynamic.
