# Code Standards

This document defines the mandatory coding standards for all source files produced in the z.ai sandbox. These rules exist to ensure code is composable, testable, and maintainable across sessions and contributors.

---

## Function Standards [REQUIRED]

These constraints apply to every function, method, and async function in the codebase.

| Rule | Why |
|------|-----|
| Single responsibility — each function does exactly one thing | Composable, testable functions that can be reused without side effects |
| Maximum 50 lines per function | Cognitive load management; long functions correlate with hidden bugs and resist testing |
| Named constants over magic numbers | `if (retries < MAX_RETRIES)` communicates intent; raw values require readers to guess the meaning |
| Error handling in every fallible function | Silent failures produce incorrect state that is expensive to diagnose later |

## File Standards [REQUIRED]

These constraints apply to every `.ts` and `.tsx` file.

| Rule | Why |
|------|-----|
| Named exports by default; default exports only for page components (`page.tsx`, `layout.tsx`) | Named imports survive refactors; default exports break when files are renamed |
| Co-located types for single-file use, shared `types.ts` for cross-file use | Keeps type definitions discoverable without duplicating them across the codebase |
| No circular imports (if A imports B, B must not import A) | Circular dependencies cause unpredictable initialization order and runtime errors |

## Import Order [REQUIRED]

Strict ordering within every file. See `knowledge/universal/conventions.md` for the full specification with examples.

```
React / Next.js  →  External packages  →  Internal (@/ paths)  →  Relative imports  →  Types (import type)
```

Why: a predictable dependency graph makes code reviews faster and reveals architectural layering violations at a glance.

## Code Quality Standards

The following patterns are classified by severity. Each entry explains what the pattern is, why it matters, and what to use instead.

### [CRITICAL] — Platform-breaking

| Pattern | Why It Matters | Preferred Alternative |
|---------|---------------|----------------------|
| Silent try-catch (empty catch block) | Swallows errors entirely, hiding data corruption or failed operations | Log the error and handle it, or re-throw with context |

### [REQUIRED] — Quality standard

| Pattern | Why It Matters | Preferred Alternative |
|---------|---------------|----------------------|
| `console.log` / `console.warn` in production code | Pollutes the console, leaks internal data, no structured output | Use a logging utility or remove after debugging |
| `any` type | Bypasses the type system entirely, defeating the purpose of TypeScript | Use `unknown` and narrow with type guards — see `constraints/type-safety.md` |
| Callback nesting deeper than 3 levels | Creates unreadable control flow that is difficult to reason about and test | Flatten with async/await or extract named functions |
| Copy-pasted logic blocks | Drift between copies creates subtle behavioral differences | Extract to a shared function, parameterize differences |
| Commented-out code blocks | Clutters the file and creates ambiguity about whether code is needed | Delete it; version control preserves the history |
| TODO comments without a ticket reference | Creates untrackable debt that is never resolved | Reference a ticket number or convert to an actionable issue |
| Hardcoded strings that should be constants | Values become inconsistent when changed in one place but not others | Define as named constants at module or config level |
| Boolean parameters in function signatures | `true`/`false` at call sites conveys no meaning without reading the signature | Use an options object, an enum, or split into two functions |

### [RECOMMENDED] — Best practice

| Pattern | Why It Matters | Preferred Alternative |
|---------|---------------|----------------------|
| Deeply nested ternary expressions | Hard to parse visually and easy to misread the branching logic | Extract to a named variable or use early returns |
| Large component files (> 300 lines) | Signals that the component handles too many concerns | Split into smaller components and co-located helpers |
| Inline styles in JSX | Makes theming inconsistent and prevents CSS-level optimizations | Use Tailwind utility classes or shadcn/ui component props |
