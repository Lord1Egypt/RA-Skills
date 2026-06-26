---
title: Update Jest Configuration
impact: MEDIUM
impactDescription: Test setup changes
tags: testing, jest, configuration
---

## Update Jest Configuration

CRA includes Jest configuration. Next.js requires explicit setup.

**CRA Pattern (before):**

```json
// package.json - built-in config
{
  "scripts": {
    "test": "react-scripts test"
  }
}
```

**Next.js Pattern (after):**

```bash
npm install -D jest jest-environment-jsdom @testing-library/react @testing-library/jest-dom
```

```js
// jest.config.js
const nextJest = require('next/jest')

const createJestConfig = nextJest({
  // Provide the path to your Next.js app
  dir: './',
})

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
}

module.exports = createJestConfig(customJestConfig)
```

```js
// jest.setup.js
import '@testing-library/jest-dom'
```

```json
// package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch"
  }
}
```

**TypeScript support:**

```js
// jest.config.js
const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
  transform: {
    '^.+\\.(ts|tsx)$': ['ts-jest', { tsconfig: 'tsconfig.jest.json' }],
  },
}
```

```json
// tsconfig.jest.json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "jsx": "react-jsx"
  }
}
```
