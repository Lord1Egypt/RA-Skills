---
title: Test Async Components
impact: MEDIUM
impactDescription: Handle async data in tests
tags: testing, async, suspense
---

## Test Async Components

Test components that fetch data asynchronously using proper async patterns.

**Async component with Suspense:**

```tsx
// components/UserProfile.tsx
async function UserData({ userId }: { userId: string }) {
  const user = await fetchUser(userId)
  return <div>{user.name}</div>
}

export function UserProfile({ userId }: { userId: string }) {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <UserData userId={userId} />
    </Suspense>
  )
}
```

**Testing with mocked data:**

```tsx
// components/UserProfile.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import { UserProfile } from './UserProfile'

// Mock the fetch function
jest.mock('@/lib/api', () => ({
  fetchUser: jest.fn((id) =>
    Promise.resolve({ id, name: 'John Doe', email: 'john@example.com' })
  ),
}))

test('renders user after loading', async () => {
  render(<UserProfile userId="1" />)

  // First shows loading state
  expect(screen.getByText('Loading...')).toBeInTheDocument()

  // Then shows user data
  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument()
  })
})
```

**Testing error states:**

```tsx
import { fetchUser } from '@/lib/api'

test('shows error when fetch fails', async () => {
  // Mock fetch to reject
  (fetchUser as jest.Mock).mockRejectedValueOnce(new Error('Failed'))

  render(
    <ErrorBoundary fallback={<div>Error occurred</div>}>
      <UserProfile userId="1" />
    </ErrorBoundary>
  )

  await waitFor(() => {
    expect(screen.getByText('Error occurred')).toBeInTheDocument()
  })
})
```

**Using MSW for API mocking:**

```tsx
import { rest } from 'msw'
import { setupServer } from 'msw/node'

const server = setupServer(
  rest.get('/api/users/:id', (req, res, ctx) => {
    return res(ctx.json({ id: req.params.id, name: 'John' }))
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```
