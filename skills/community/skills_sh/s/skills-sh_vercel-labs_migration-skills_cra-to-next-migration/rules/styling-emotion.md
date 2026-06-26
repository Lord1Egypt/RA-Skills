---
title: Configure Emotion for SSR
impact: HIGH
impactDescription: Prevents flash of unstyled content
tags: styling, emotion, ssr
---

## Configure Emotion for SSR

Emotion requires specific configuration for Next.js App Router to prevent flash of unstyled content.

**CRA Pattern (before):**

```tsx
// Works without config in CRA
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react'

const style = css`
  color: blue;
`

export default function App() {
  return <div css={style}>Content</div>
}
```

**Next.js App Router (after):**

```bash
npm install @emotion/react @emotion/cache @emotion/styled
```

```tsx
// lib/emotion.tsx
'use client'

import { CacheProvider } from '@emotion/react'
import createCache from '@emotion/cache'
import { useServerInsertedHTML } from 'next/navigation'
import { useState } from 'react'

export default function EmotionRegistry({
  children,
}: {
  children: React.ReactNode
}) {
  const [cache] = useState(() => {
    const cache = createCache({ key: 'css' })
    cache.compat = true
    return cache
  })

  useServerInsertedHTML(() => {
    const entries = Object.entries(cache.inserted)
    if (entries.length === 0) return null

    let styles = ''
    let dataEmotionAttribute = cache.key

    entries.forEach(([name, value]) => {
      if (typeof value === 'string') {
        styles += value
        dataEmotionAttribute += ` ${name}`
      }
    })

    return (
      <style
        data-emotion={dataEmotionAttribute}
        dangerouslySetInnerHTML={{ __html: styles }}
      />
    )
  })

  return <CacheProvider value={cache}>{children}</CacheProvider>
}
```

```tsx
// app/layout.tsx
import EmotionRegistry from '@/lib/emotion'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <EmotionRegistry>{children}</EmotionRegistry>
      </body>
    </html>
  )
}
```

**Using Emotion (requires 'use client'):**

```tsx
// components/Box.tsx
'use client'

import styled from '@emotion/styled'

const StyledBox = styled.div`
  padding: 20px;
  background: #f0f0f0;
`

export function Box({ children }) {
  return <StyledBox>{children}</StyledBox>
}
```
