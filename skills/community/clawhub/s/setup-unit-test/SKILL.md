---
name: setup-unit-test
description: >
  One-click initialization of an AI-driven unit testing environment for frontend projects (supports React/Vue/pure TypeScript/Next.js).
  Automatically detects project framework, installs Vitest + Testing Library + MSW, generates config files,
  and injects Claude Code custom commands for cross-project reuse.

  Trigger scenarios:
  (1) Need to initialize unit testing in a new or existing project.
  (2) User says "initialize unit tests", "configure test environment", or "setup unit test".
  (3) Need to enable /gen-unit-test and other AI test generation commands in the project.
  (4) Need a single command to set up test configurations across multiple tech stacks (React/Vue/Next.js/TS).
---

## Security & Permissions Statement

This skill performs the following privileged operations to automate test environment configuration:
- **File System**: Reads `package.json` and writes config files (`vitest.config.ts`, `.claude/commands/*.md`).
- **Shell Execution**: Runs `npm/yarn/pnpm` commands to install dependencies, and runs `git` commands to detect staged files.
- **Git Hooks**: Initializes Husky and modifies `.husky/pre-commit` to automate the testing workflow.

**All scripts run locally and will not transmit project data to external servers (unless explicitly sent to Claude via a command invocation).**

---

# Initialize Unit Testing Environment

One-click setup of a production-grade unit testing solution for any frontend project. Detect environment → Install enhanced plugins → Auto alias resolution → AI command injection.

## Workflow

### Step 1: Detect Project Environment

Run the detection script to identify project details:

```bash
node <skill-dir>/scripts/detect-framework.mjs <project-dir>
```

Returns JSON containing: `os`, `framework`, `isNext`, `typescript`, `hasTsConfig`, `packageManager`, `hasGit`, `hasVitest`, etc.

### Step 2: Install Enhanced Dependencies

Install dev dependencies (`-D`) using the corresponding package manager. Skip already-installed dependencies.

**Core Toolchain**:
- `vitest`
- `@vitest/ui` (visual test interface)
- `@vitest/coverage-v8` (code coverage)
- `jsdom` (browser environment simulation)
- `msw` (API network request mocking)
- `vitest-tsconfig-paths` (auto-resolve path aliases from tsconfig.json)

**Additional for React/Next.js projects**:
- `@testing-library/react`
- `@testing-library/jest-dom`
- `@testing-library/user-event`
- `@vitejs/plugin-react`

**Additional for Vue projects**:
- `@testing-library/vue`
- `@testing-library/jest-dom`
- `@testing-library/user-event`
- `@vitejs/plugin-vue`

### Step 3: Generate Smart Config Files

#### vitest.config.ts

Uses the `tsconfigPaths()` plugin for "zero-config alias resolution".

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import vue from '@vitejs/plugin-vue'
import tsconfigPaths from 'vitest-tsconfig-paths'

export default defineConfig({
  plugins: [
    tsconfigPaths(),
    // react(), // Enable for React/Next.js projects
    // vue(),   // Enable for Vue projects
  ],
  test: {
    globals: true,
    environment: 'jsdom',
    include: ['tests/unit/**/*.test.{ts,tsx}'],
    setupFiles: ['./tests/unit/setup/index.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json-summary'],
      include: ['src/**/*.{ts,tsx,vue}'],
      exclude: ['src/**/*.stories.*', 'src/**/*.d.ts'],
      thresholds: { statements: 70, branches: 70, functions: 70, lines: 70 },
    },
    // Additional config for Next.js server component mocking can be added here
  },
})
```

#### tests/unit/setup/index.ts

```typescript
import '@testing-library/jest-dom/vitest'
import { afterAll, afterEach, beforeAll, vi } from 'vitest'
import { server } from './msw-server'

// Global Mock example (e.g., Next.js Router)
// vi.mock('next/navigation', () => ({ useRouter: () => ({ push: vi.fn() }) }))

beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

### Step 4: Inject AI Commands (Cross-Project Reuse)

Write prompt templates to the project's `.claude/commands/`:
- `gen-unit-test.md`: Core test generation instructions.
- `fix-test.md`: Automated failure repair instructions.

### Step 5: Automation Integration (Git Hooks)

#### 5.1 Install Husky & lint-staged
#### 5.2 Copy `check-missing-tests.mjs`
#### 5.3 Write `.husky/pre-commit` (dual-layer guard)
- **Layer 1**: `vitest related --run` (only run tests affected by the current changes).
- **Layer 2**: When `AUTO_GEN_TEST=1`, detect missing tests and invoke Claude Code to auto-generate them.

### Step 6: Verification & Summary Output

```
Initialization complete:
- Framework:       [detection result] (Next.js compatible)
- Alias resolution: Enabled (vitest-tsconfig-paths)
- Visual UI:       Enabled (npm run test:ui)
- Coverage threshold: 70% (manually adjustable in vitest.config.ts)
- AI automation:   Injected /gen-unit-test and /fix-test commands
- Auto-generation: Disabled by default, enable via export AUTO_GEN_TEST=1
```

## Resource Files

- `scripts/detect-framework.mjs` — Environment detection script (with OS and Next.js detection)
- `scripts/check-missing-tests.mjs` — Cross-platform path-compatible test checking script
- `references/gen-unit-test-prompt.md`
- `references/fix-test-prompt.md`
