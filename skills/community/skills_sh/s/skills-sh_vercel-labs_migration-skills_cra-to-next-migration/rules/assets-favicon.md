---
title: Place Favicon in App Directory
impact: LOW
impactDescription: New favicon convention
tags: assets, favicon, metadata
---

## Place Favicon in App Directory

Next.js App Router supports placing favicon files directly in the `app` directory for automatic handling.

**CRA Pattern (before):**

```
public/
└── favicon.ico

<!-- public/index.html -->
<link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
```

**Next.js Pattern (after):**

```
app/
├── favicon.ico      # Automatically used
├── icon.png         # Alternative format
├── apple-icon.png   # Apple touch icon
└── layout.tsx
```

No configuration needed - Next.js detects and uses these automatically.

**Supported favicon files:**

| File | Purpose |
|------|---------|
| `favicon.ico` | Default favicon |
| `icon.png` | Modern browsers |
| `icon.svg` | SVG favicon |
| `apple-icon.png` | Apple devices |

**Multiple sizes (icon.tsx):**

```tsx
// app/icon.tsx
import { ImageResponse } from 'next/og'

export const size = { width: 32, height: 32 }
export const contentType = 'image/png'

export default function Icon() {
  return new ImageResponse(
    <div
      style={{
        fontSize: 24,
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'black',
        color: 'white',
      }}
    >
      A
    </div>,
    { ...size }
  )
}
```

**Or via metadata:**

```tsx
// app/layout.tsx
export const metadata = {
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-icon.png',
  },
}
```
