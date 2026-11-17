# Frontend Test Environment Setup

## React

```bash
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom jsdom
npm install --save-dev msw  # API mocking
npm install --save-dev @testing-library/user-event  # Realistic user interaction
```

```javascript
// vitest.config.ts
export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
  },
});

// src/test/setup.ts
import '@testing-library/jest-dom';
import { server } from './mocks/server';
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## Vue

```bash
npm install --save-dev vitest @vue/test-utils jsdom
npm install --save-dev msw
```

## Svelte

```bash
npm install --save-dev vitest @testing-library/svelte jsdom
```

## Next.js

Special considerations:
- SSR: `next-router-mock` for routing in tests
- API Routes: test with supertest directly
- Component tests: same as React (jsdom + Testing Library)

## Component Test Structure

```
ComponentName.test.tsx
├── Rendering: Given props, renders correct DOM structure
├── Interaction: User events → state change → correct render
├── Boundary: Empty data, error state, loading state
└── Accessibility: Keyboard navigation, role attributes
```

## API Mock Strategy

- **Unit/Component tests**: MSW intercepts at network level
- **Integration tests**: vitest + testcontainers or real backend service
- **E2E tests**: Real backend (can be staging), via webapp-testing or Agent Browser

## Test Environment Notes

- `jsdom`: Pure JS DOM implementation, fast, no rendering
- `happy-dom`: Faster than jsdom, fewer features
- Neither renders CSS or executes layout — visual regression needs real browser (Playwright)

## Static Asset Mocking

```javascript
// vitest.config.ts — mock images, CSS, fonts
// These don't affect component logic
// Use moduleNameMapper or vi.mock()
```

## E2E Testing

Browser-based E2E is handled by:
- `webapp-testing` skill: Playwright scripts with server lifecycle
- `Agent Browser` skill: agent-browser CLI for interactive automation

This skill determines whether E2E is needed and generates the interaction test plan (see `references/interaction-test-plan.md`). Those skills execute the plan.
