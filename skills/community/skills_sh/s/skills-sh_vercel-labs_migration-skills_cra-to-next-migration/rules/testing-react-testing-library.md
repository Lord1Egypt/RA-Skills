---
title: RTL Works the Same
impact: LOW
impactDescription: Minimal changes needed
tags: testing, rtl, react-testing-library
---

## RTL Works the Same

React Testing Library works the same way in Next.js for Client Components.

**CRA Pattern (before):**

```tsx
// src/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

test('renders button and handles click', () => {
  const handleClick = jest.fn()
  render(<Button onClick={handleClick}>Click me</Button>)

  const button = screen.getByRole('button', { name: /click me/i })
  expect(button).toBeInTheDocument()

  fireEvent.click(button)
  expect(handleClick).toHaveBeenCalledTimes(1)
})
```

**Next.js Pattern (after):**

```tsx
// components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

test('renders button and handles click', () => {
  const handleClick = jest.fn()
  render(<Button onClick={handleClick}>Click me</Button>)

  const button = screen.getByRole('button', { name: /click me/i })
  expect(button).toBeInTheDocument()

  fireEvent.click(button)
  expect(handleClick).toHaveBeenCalledTimes(1)
})
```

**Testing components with next/navigation:**

```tsx
// components/NavButton.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { NavButton } from './NavButton'

// Mock next/navigation
jest.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: jest.fn(),
      replace: jest.fn(),
      back: jest.fn(),
    }
  },
  usePathname() {
    return '/'
  },
}))

test('navigates on click', async () => {
  const { useRouter } = require('next/navigation')
  render(<NavButton href="/about">About</NavButton>)

  await userEvent.click(screen.getByRole('button'))
  expect(useRouter().push).toHaveBeenCalledWith('/about')
})
```
