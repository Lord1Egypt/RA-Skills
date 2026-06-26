---
title: Reference Assets Without Public Prefix
impact: LOW
impactDescription: Simpler asset URLs
tags: assets, urls, paths
---

## Reference Assets Without Public Prefix

In Next.js, reference files in the `public` folder directly without any prefix or environment variable.

**CRA Pattern (before):**

```tsx
// Using process.env.PUBLIC_URL or %PUBLIC_URL%
<img src={`${process.env.PUBLIC_URL}/images/logo.png`} />

// In HTML
<link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
```

**Next.js Pattern (after):**

```tsx
// Just use absolute path from root
<img src="/images/logo.png" />

// In metadata (app/layout.tsx)
export const metadata = {
  icons: {
    icon: '/favicon.ico',
  },
}
```

**Migration:**

```bash
# Find and replace in your code
# %PUBLIC_URL% -> (empty string)
# process.env.PUBLIC_URL -> (empty string)

# Before
src="%PUBLIC_URL%/images/photo.jpg"
src={`${process.env.PUBLIC_URL}/images/photo.jpg`}

# After
src="/images/photo.jpg"
```

**Examples:**

```tsx
// Images
<img src="/images/banner.jpg" alt="Banner" />

// Downloads
<a href="/files/document.pdf">Download PDF</a>

// Videos
<video src="/videos/intro.mp4" />

// Audio
<audio src="/audio/notification.mp3" />
```

**Note:** For images, prefer using `next/image` component with static imports for optimization benefits.
