---
title: Test Client Components
impact: MEDIUM
impactDescription: Standard RTL patterns with mocks
tags: testing, client-components, rtl
---

## Test Client Components

Client Components are tested similarly to CRA components, but may need Next.js mocks.

**Client Component:**

```tsx
// components/SearchForm.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export function SearchForm() {
  const [query, setQuery] = useState('')
  const router = useRouter()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    router.push(`/search?q=${encodeURIComponent(query)}`)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
      <button type="submit">Search</button>
    </form>
  )
}
```

**Test file:**

```tsx
// components/SearchForm.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { SearchForm } from './SearchForm'

// Mock next/navigation
const mockPush = jest.fn()
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
    replace: jest.fn(),
    back: jest.fn(),
  }),
  usePathname: () => '/',
  useSearchParams: () => new URLSearchParams(),
}))

describe('SearchForm', () => {
  beforeEach(() => {
    mockPush.mockClear()
  })

  test('renders search input', () => {
    render(<SearchForm />)
    expect(screen.getByPlaceholderText('Search...')).toBeInTheDocument()
  })

  test('navigates on submit', async () => {
    const user = userEvent.setup()
    render(<SearchForm />)

    await user.type(screen.getByPlaceholderText('Search...'), 'react')
    await user.click(screen.getByRole('button', { name: /search/i }))

    expect(mockPush).toHaveBeenCalledWith('/search?q=react')
  })
})
```
