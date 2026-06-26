---
title: Mock Next.js Modules
impact: MEDIUM
impactDescription: Common Next.js mocks
tags: testing, mocking, jest
---

## Mock Next.js Modules

Common patterns for mocking Next.js specific modules in tests.

**Mock next/navigation:**

```tsx
// __mocks__/next/navigation.ts
export const useRouter = jest.fn(() => ({
  push: jest.fn(),
  replace: jest.fn(),
  back: jest.fn(),
  forward: jest.fn(),
  refresh: jest.fn(),
  prefetch: jest.fn(),
}))

export const usePathname = jest.fn(() => '/')
export const useSearchParams = jest.fn(() => new URLSearchParams())
export const useParams = jest.fn(() => ({}))
export const redirect = jest.fn()
export const notFound = jest.fn()
```

**Mock next/image:**

```tsx
// __mocks__/next/image.tsx
const MockImage = ({ src, alt, ...props }: any) => {
  return <img src={src} alt={alt} {...props} />
}

export default MockImage
```

**Mock next/headers:**

```tsx
// __mocks__/next/headers.ts
export const cookies = jest.fn(() => ({
  get: jest.fn(),
  set: jest.fn(),
  delete: jest.fn(),
}))

export const headers = jest.fn(() => new Headers())
```

**Mock next/link:**

```tsx
// __mocks__/next/link.tsx
const MockLink = ({ children, href, ...props }: any) => {
  return <a href={href} {...props}>{children}</a>
}

export default MockLink
```

**Using mocks in tests:**

```tsx
// components/Nav.test.tsx
jest.mock('next/navigation')
jest.mock('next/image')
jest.mock('next/link')

import { useRouter } from 'next/navigation'

beforeEach(() => {
  ;(useRouter as jest.Mock).mockReturnValue({
    push: jest.fn(),
    pathname: '/home',
  })
})

test('navigation works', () => {
  // Test with mocked router
})
```

**Setup file for global mocks:**

```js
// jest.setup.js
jest.mock('next/navigation')
jest.mock('next/image')
```
