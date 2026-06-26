---
title: Configure Cypress for Next.js
impact: LOW
impactDescription: E2E testing setup
tags: testing, cypress, e2e
---

## Configure Cypress for Next.js

Configure Cypress for end-to-end testing of your Next.js application.

**Installation:**

```bash
npm install -D cypress
```

**Cypress configuration:**

```js
// cypress.config.js
const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    supportFile: 'cypress/support/e2e.js',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
  },
})
```

**Package.json scripts:**

```json
{
  "scripts": {
    "cypress": "cypress open",
    "cypress:headless": "cypress run",
    "e2e": "start-server-and-test 'next dev' http://localhost:3000 cypress",
    "e2e:headless": "start-server-and-test 'next start' http://localhost:3000 cypress:headless"
  }
}
```

**Example E2E test:**

```tsx
// cypress/e2e/navigation.cy.ts
describe('Navigation', () => {
  it('navigates to about page', () => {
    cy.visit('/')
    cy.get('a[href="/about"]').click()
    cy.url().should('include', '/about')
    cy.get('h1').should('contain', 'About')
  })
})

describe('Search', () => {
  it('searches for products', () => {
    cy.visit('/')
    cy.get('input[placeholder="Search..."]').type('react')
    cy.get('button[type="submit"]').click()
    cy.url().should('include', '/search?q=react')
    cy.get('[data-testid="results"]').should('exist')
  })
})
```

**Testing with authentication:**

```tsx
// cypress/support/commands.ts
Cypress.Commands.add('login', (email, password) => {
  cy.session([email, password], () => {
    cy.visit('/login')
    cy.get('input[name="email"]').type(email)
    cy.get('input[name="password"]').type(password)
    cy.get('button[type="submit"]').click()
    cy.url().should('include', '/dashboard')
  })
})

// cypress/e2e/dashboard.cy.ts
describe('Dashboard', () => {
  beforeEach(() => {
    cy.login('user@example.com', 'password')
  })

  it('shows user dashboard', () => {
    cy.visit('/dashboard')
    cy.get('h1').should('contain', 'Dashboard')
  })
})
```
