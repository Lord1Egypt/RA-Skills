---
name: react-component-auditor
description: Audit React components for performance, accessibility, hook correctness, prop design, and re-render optimization — identify memo opportunities and state management issues.
metadata:
  tags: ["react", "performance", "accessibility", "frontend", "hooks"]
---

# React Component Auditor

Audit React components for performance bottlenecks, accessibility issues, hook correctness, prop design problems, and unnecessary re-renders. Identifies memo opportunities, stale closure bugs, and state management anti-patterns.

## Usage

```
"Audit my React components for performance"
"Check for unnecessary re-renders"
"Review hook usage in my components"
"Audit accessibility of my React app"
```

## How It Works

### 1. Component Discovery

```bash
find src -name "*.tsx" -o -name "*.jsx" | head -30
grep -rn "export.*function\|export default\|React.FC\|React.memo" src/components/ | head -30
```

### 2. Performance Analysis

**Re-render detection:**
- Components without `React.memo` that receive object/array props
- Inline function props causing child re-renders
- Missing `useCallback` on event handlers passed as props
- Missing `useMemo` on expensive computations
- Context providers that trigger wide re-render trees
- State in wrong component (lifting too high)

**Bundle impact:**
- Large component files (>300 lines — should split)
- Heavy imports not code-split (chart libraries, editors)
- Barrel file re-exports causing tree-shaking failures

### 3. Hook Correctness

- `useEffect` with missing dependencies (stale closure bugs)
- `useEffect` with too many dependencies (runs too often)
- `useEffect` without cleanup (memory leaks on timers, subscriptions)
- `useState` for derived state (should be computed)
- Custom hooks not following rules of hooks
- `useRef` for values that should be `useState` (no re-render)

### 4. Accessibility Audit

- Interactive elements without keyboard support
- Missing `aria-label` on icon buttons
- Images without `alt` text
- Form inputs without associated labels
- Color contrast issues in conditional styling
- Focus management in modals and dialogs
- Missing skip navigation links

### 5. Prop Design

- Too many props (>7 suggests component should split)
- Boolean props with confusing negation (`isNotVisible`)
- Required props that have obvious defaults
- Children pattern vs render props vs composition
- Prop drilling (>3 levels deep)

### 6. State Management

- Local state that should be global (shared across routes)
- Global state that should be local (only used in one component)
- Redundant state (derivable from other state)
- Syncing state between components (use single source of truth)

## Output

```
## React Component Audit

**Components:** 45 | **Custom Hooks:** 12

### 🔴 Critical (3)
1. **Stale closure in useEffect** — UserProfile.tsx:34
   `userId` in dependency array but `fetchUser` captures stale `token`
   → Add `token` to deps or use `useCallback` for `fetchUser`

2. **Context re-render storm** — AppProvider.tsx
   Single context with 12 values — any change re-renders all consumers
   → Split into AuthContext, ThemeContext, UserContext

3. **Missing keyboard support** — DropdownMenu.tsx
   Custom dropdown has no keyboard navigation (Enter, Escape, Arrow keys)
   → Add onKeyDown handler with aria-expanded

### 🟡 Improvements (5)
4. 8 components could benefit from React.memo (receive stable parents)
5. Inline arrow functions in 12 onClick handlers
6. 3 useEffects with empty cleanup (timer, subscription leaks)
7. DashboardPage has 23 props — split into sub-components
8. Form inputs missing htmlFor/id label association in 5 forms

### ✅ Good Practices
- Custom hooks for data fetching with loading/error states
- Proper Suspense boundaries with fallbacks
- Error boundaries on route level
- Consistent component file structure
```
