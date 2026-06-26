---
title: Use Server Actions for Mutations
impact: HIGH
impactDescription: New pattern for form submissions
tags: data-fetching, server-actions, mutations, forms
---

## Use Server Actions for Mutations

CRA handles form submissions with client-side fetch. Next.js Server Actions provide a simpler pattern for mutations.

**CRA Pattern (before):**

```tsx
// src/components/ContactForm.tsx
import { useState } from 'react'

export default function ContactForm() {
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    const formData = new FormData(e.target)
    const res = await fetch('/api/contact', {
      method: 'POST',
      body: JSON.stringify(Object.fromEntries(formData)),
      headers: { 'Content-Type': 'application/json' },
    })

    if (res.ok) {
      alert('Message sent!')
    }
    setLoading(false)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" required />
      <textarea name="message" required />
      <button disabled={loading}>Send</button>
    </form>
  )
}
```

**Next.js Server Action (after):**

```tsx
// app/contact/page.tsx
async function submitContact(formData: FormData) {
  'use server'

  const email = formData.get('email')
  const message = formData.get('message')

  await db.contacts.create({ email, message })
  // Optionally revalidate cache
  revalidatePath('/contacts')
}

export default function ContactPage() {
  return (
    <form action={submitContact}>
      <input name="email" type="email" required />
      <textarea name="message" required />
      <button type="submit">Send</button>
    </form>
  )
}
```

**With client-side pending state:**

```tsx
'use client'

import { useFormStatus } from 'react-dom'

function SubmitButton() {
  const { pending } = useFormStatus()
  return <button disabled={pending}>{pending ? 'Sending...' : 'Send'}</button>
}

export default function ContactForm({ action }) {
  return (
    <form action={action}>
      <input name="email" type="email" required />
      <SubmitButton />
    </form>
  )
}
```

**Benefits:**
- No API route needed for simple mutations
- Progressive enhancement (works without JS)
- Type-safe with TypeScript
- Automatic revalidation integration
