# Conventions

## Purpose

This document defines the coding conventions specific to the z.ai sandbox platform. General best practices (PascalCase, camelCase, standard TypeScript) are not repeated here — they are assumed knowledge.

---

## State Management

Select the state management approach based on the scope and source of the data.

| Need | Solution | Why |
|------|----------|-----|
| Local UI state (toggles, form fields) | `useState` | Scoped to a single component; no shared dependency |
| Shared client state (auth, theme, app-wide flags) | Zustand store in `/stores/` | Avoids prop drilling; provides reactive updates across components |
| Server state / data fetching | TanStack Query | Handles caching, revalidation, and loading states automatically |
| Form state with validation | React Hook Form + Zod | Declarative validation schema; Zod matches TypeScript types |

---

## Import Order

Strict ordering within every file. The authoritative rule is defined in `constraints/code-standards.md`; the expanded specification with examples is below.

```typescript
// 1. React / Next.js
import { useState, useEffect } from 'react';

// 2. External packages
import { z } from 'zod';

// 3. Internal (@/ paths)
import { db } from '@/lib/db';
import { Button } from '@/components/ui/button';

// 4. Relative imports
import { formatDate } from './utils';

// 5. Types (always last, use `import type`)
import type { User } from '@/types';
```

Why: a predictable dependency graph makes code reviews faster and reveals architectural layering violations at a glance.

---

## File Organization

The internal structure of a component file follows this order:

```
1. Imports
2. Types / Interfaces
3. Constants
4. Helper functions
5. Main component
6. Sub-components
7. Export
```

Why: readers encounter dependencies before usage, types before implementations, and the primary export last.

---

## Platform-Specific Rules

| Area | Rule | Severity |
|------|------|----------|
| Styling | Use shadcn/ui components from `src/components/ui/` — do not build UI primitives from scratch | [REQUIRED] |
| Colors | Avoid indigo/blue defaults unless the user explicitly requests them | [RECOMMENDED] |
| TypeScript | Use `unknown` over `any`; use `import type` for type-only imports | [REQUIRED] |
| Server/Client split | Hooks require `'use client'`; server-only logic uses `'use server'`; everything else defaults to server component | [REQUIRED] |
| SDK placement | `z-ai-web-dev-sdk` must only appear in backend/server code, never in client components | [CRITICAL] |
