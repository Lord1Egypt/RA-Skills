# React Best Practices

Comprehensive performance optimization guide for React and Next.js applications from Vercel Engineering. Contains 57 rules across 8 categories, prioritized by impact.

## What's Inside

- Eliminating request waterfalls (CRITICAL) — parallel fetching, deferred await, Suspense boundaries
- Bundle size optimization (CRITICAL) — barrel imports, dynamic imports, deferred third-party libs
- Server-side performance (HIGH) — auth in Server Actions, React.cache(), LRU caching, RSC serialization
- Client-side data fetching (MEDIUM-HIGH) — SWR deduplication, event listeners, localStorage
- Re-render optimization (MEDIUM) — derived state, functional setState, lazy initialization, transitions
- Rendering performance (MEDIUM) — content-visibility, static JSX hoisting, hydration fixes
- JavaScript performance (LOW-MEDIUM) — Set/Map lookups, combined iterations, early returns
- Advanced patterns (LOW) — event handler refs, app initialization, useEffectEvent

## When to Use

- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Refactoring React/Next.js applications
- Optimizing bundle size or load times
- Debugging slow renders or waterfalls

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/frontend/react-best-practices
```

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install react-best-practices
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/frontend/react-best-practices .cursor/skills/react-best-practices
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/frontend/react-best-practices ~/.cursor/skills/react-best-practices
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/frontend/react-best-practices .claude/skills/react-best-practices
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/frontend/react-best-practices ~/.claude/skills/react-best-practices
```

## Related Skills

- `react-performance` — Condensed performance patterns with quick decision guide
- `nextjs` — Next.js App Router patterns and conventions

---

Part of the [Frontend](..) skill category.
