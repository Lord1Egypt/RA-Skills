# React Setup

First-time setup for the React skill.

## Step 1: Create Workspace

```bash
mkdir -p ~/react
```

## Step 2: Initialize Memory

Copy `memory-template.md` (in this skill's folder) to `~/Clawic/data/react/memory.md`. Fill in the Stack Decisions table on first use — every later session reads it instead of re-asking.

## Step 3: Verify Setup

The skill is ready when `~/Clawic/data/react/memory.md` exists.

## Project Structure

Feature folders, not type folders (→ SKILL.md, Where Experts Disagree):

```
src/
├── app/                 # Routes (Next.js App Router)
├── features/            # One folder per feature
│   └── [feature]/
│       ├── components/
│       ├── hooks/
│       ├── api/         # Fetchers + query key factory + types
│       └── index.ts     # Public exports — other features import ONLY from here
├── shared/              # Used by 2+ features (move here at second consumer, not before)
│   ├── components/ui/   # Primitives (Button, Input)
│   └── hooks/
└── providers/           # Context providers, QueryClient
```

The `index.ts` barrel is the enforcement point: if a cross-feature import bypasses it, the dependency graph is already tangled.

## Recommended Stack

| Layer | Tool | Why this over alternatives |
|-------|------|----------------------------|
| Framework | Next.js 15 | Server Components + Actions with zero config; pick Vite instead for login-gated SPAs (→ SKILL.md, Where Experts Disagree) |
| Styling | Tailwind CSS | Styles colocated with markup; no naming layer to maintain |
| Components | shadcn/ui | Copied into your repo — you own and edit the code, no library API to fight |
| Server state | TanStack Query | Cache lifecycle, dedupe, devtools; SWR only if you need nothing but GET |
| Client state | Zustand | Selectors without providers; no boilerplate ceremony |
| Forms | React Hook Form + Zod | Uncontrolled inputs (no rerender per keystroke); one Zod schema validates client and server |
| Testing | Vitest + Testing Library | Queries by role/label — tests survive refactors that don't change behavior |

## TypeScript Config

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

`noUncheckedIndexedAccess` is the one teams skip and regret: it makes `array[0]` typed `T | undefined`, surfacing empty-state crashes at compile time (→ SKILL.md, Core Rule 7).

## Common Commands

```bash
# Next.js
npx create-next-app@latest my-app --typescript --tailwind --app

# Vite (SPA)
npm create vite@latest my-app -- --template react-ts

# Add shadcn/ui
npx shadcn@latest init

# Data + state + forms
npm install @tanstack/react-query zustand react-hook-form zod @hookform/resolvers
```
