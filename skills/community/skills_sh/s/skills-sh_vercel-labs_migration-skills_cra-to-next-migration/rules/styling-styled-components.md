---
title: Configure styled-components for SSR
impact: HIGH
impactDescription: Prevents flash of unstyled content
tags: styling, styled-components, ssr
---

## Configure styled-components for SSR

styled-components requires specific configuration to work with Next.js Server-Side Rendering.

**CRA Pattern (before):**

```tsx
// Works without config in CRA
import styled from 'styled-components'

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`

export default function App() {
  return <Container>Content</Container>
}
```

**Next.js App Router (after):**

```bash
npm install styled-components
```

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  compiler: {
    styledComponents: true,
  },
}

module.exports = nextConfig
```

```tsx
// lib/registry.tsx
'use client'

import React, { useState } from 'react'
import { useServerInsertedHTML } from 'next/navigation'
import { ServerStyleSheet, StyleSheetManager } from 'styled-components'

export default function StyledComponentsRegistry({
  children,
}: {
  children: React.ReactNode
}) {
  const [styledComponentsStyleSheet] = useState(() => new ServerStyleSheet())

  useServerInsertedHTML(() => {
    const styles = styledComponentsStyleSheet.getStyleElement()
    styledComponentsStyleSheet.instance.clearTag()
    return <>{styles}</>
  })

  if (typeof window !== 'undefined') return <>{children}</>

  return (
    <StyleSheetManager sheet={styledComponentsStyleSheet.instance}>
      {children}
    </StyleSheetManager>
  )
}
```

```tsx
// app/layout.tsx
import StyledComponentsRegistry from './lib/registry'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <StyledComponentsRegistry>{children}</StyledComponentsRegistry>
      </body>
    </html>
  )
}
```

**Using styled-components (requires 'use client'):**

```tsx
// components/Button.tsx
'use client'

import styled from 'styled-components'

const StyledButton = styled.button`
  background: blue;
  color: white;
`

export function Button() {
  return <StyledButton>Click me</StyledButton>
}
```
