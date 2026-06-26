---
title: Return Proper Response Types
impact: MEDIUM
impactDescription: Different response formats
tags: api, response, content-type
---

## Return Proper Response Types

Return different response types from Route Handlers based on your needs.

**Express/CRA Backend (before):**

```js
// JSON response
res.json({ data: 'value' })

// Text response
res.send('Hello')

// File download
res.download('/path/to/file.pdf')

// Redirect
res.redirect('/new-path')

// Status codes
res.status(404).json({ error: 'Not found' })
```

**Next.js Route Handler (after):**

```tsx
import { NextResponse } from 'next/server'

// JSON response
export async function GET() {
  return NextResponse.json({ data: 'value' })
}

// JSON with status code
export async function GET() {
  return NextResponse.json(
    { error: 'Not found' },
    { status: 404 }
  )
}

// Text response
export async function GET() {
  return new NextResponse('Hello World', {
    headers: { 'Content-Type': 'text/plain' },
  })
}

// HTML response
export async function GET() {
  return new NextResponse('<h1>Hello</h1>', {
    headers: { 'Content-Type': 'text/html' },
  })
}

// Redirect
export async function GET() {
  return NextResponse.redirect(new URL('/new-path', request.url))
}

// File/stream response
export async function GET() {
  const file = await fs.readFile('/path/to/file.pdf')
  return new NextResponse(file, {
    headers: {
      'Content-Type': 'application/pdf',
      'Content-Disposition': 'attachment; filename="file.pdf"',
    },
  })
}

// No content
export async function DELETE() {
  await deleteResource()
  return new NextResponse(null, { status: 204 })
}
```
