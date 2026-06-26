---
title: Test Server Components
impact: HIGH
impactDescription: New testing patterns for RSC
tags: testing, server-components, rsc
---

## Test Server Components

Server Components require different testing approaches since they're async and run on the server.

**Server Component:**

```tsx
// app/users/page.tsx
export default async function UsersPage() {
  const users = await fetchUsers()
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

**Testing approach 1: Test as async function**

```tsx
// app/users/page.test.tsx
import UsersPage from './page'

// Mock the fetch function
jest.mock('./api', () => ({
  fetchUsers: jest.fn(() => Promise.resolve([
    { id: 1, name: 'John' },
    { id: 2, name: 'Jane' },
  ])),
}))

test('renders users', async () => {
  // Server components are async functions
  const result = await UsersPage()

  // Result is JSX, can check structure
  expect(result.type).toBe('ul')
  expect(result.props.children).toHaveLength(2)
})
```

**Testing approach 2: Render to string**

```tsx
import { renderToString } from 'react-dom/server'
import UsersPage from './page'

test('renders users to HTML', async () => {
  const Component = await UsersPage()
  const html = renderToString(Component)

  expect(html).toContain('John')
  expect(html).toContain('Jane')
})
```

**Testing approach 3: Use experimental RSC testing (Next.js)**

```tsx
// Using @testing-library/react with experimental support
import { render, screen } from '@testing-library/react'

// This requires experimental setup
test('renders users', async () => {
  render(await UsersPage())
  expect(screen.getByText('John')).toBeInTheDocument()
})
```

**Best practice: Extract logic for easier testing**

```tsx
// lib/users.ts - Pure functions, easy to test
export async function getUsers() {
  const users = await fetchUsers()
  return users.filter(u => u.active)
}

// lib/users.test.ts
test('filters active users', async () => {
  const users = await getUsers()
  expect(users.every(u => u.active)).toBe(true)
})
```
