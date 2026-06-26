---
title: Public Folder Works the Same Way
impact: LOW
impactDescription: No changes needed
tags: assets, public, static-files
---

## Public Folder Works the Same Way

The `public/` folder works identically in Next.js and CRA. Files are served from the root URL.

**CRA Pattern (before):**

```
public/
├── favicon.ico
├── logo.png
├── robots.txt
└── manifest.json
```

```tsx
// Referencing public assets
<img src="/logo.png" alt="Logo" />
<link rel="icon" href="/favicon.ico" />
```

**Next.js Pattern (after):**

```
public/
├── favicon.ico
├── logo.png
├── robots.txt
└── manifest.json
```

```tsx
// Same referencing - no changes needed
<img src="/logo.png" alt="Logo" />
```

**Key points:**
- Files in `public/` are served at root path
- No build processing (use as-is)
- `/public` is NOT included in the URL path
- `public/image.png` → accessible at `/image.png`

**Differences from CRA:**
- No `%PUBLIC_URL%` variable needed
- Use absolute paths directly: `/file.ext`

**What to put in public/:**
- Favicons
- robots.txt
- sitemap.xml
- Static documents (PDFs)
- Files that need exact URLs

**What NOT to put in public/:**
- Images that should be optimized (use `next/image`)
- CSS files (import them)
- JavaScript files (import them)
