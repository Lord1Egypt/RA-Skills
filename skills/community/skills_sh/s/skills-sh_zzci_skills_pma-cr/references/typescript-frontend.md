# TypeScript Frontend Review Pack

Apply this pack to React, Next.js, Vite, and browser-facing TypeScript UI code.

## Focus Areas

### Hooks and render correctness

- Missing hook dependencies that create stale closures are real bugs.
- State updates during render are usually correctness bugs.
- Reading or mutating `ref.current` during render is suspicious unless it follows an allowed lazy-init pattern.
- Effects should synchronize with external systems, not replace normal render derivation.

### Async UI state

- New fetch or mutation flows need loading, error, and empty-state handling where user-visible.
- Prevent duplicate submits for non-idempotent actions.
- Watch optimistic UI for rollback and error recovery gaps.
- Ensure async work is cancelled or ignored on stale responses where race conditions matter.

### Identity and memoization

- Unstable list keys are a bug if items can reorder, insert, or delete.
- Do not demand `useMemo` or `useCallback` by default; only flag them when there is direct evidence of incorrectness or severe churn.

### Dead code and stale UI flows

- Look for components, routes, loaders, or hooks that are no longer referenced by the current route tree or app shell.
- Watch for feature-flagged UI branches that are permanently disabled but still carry fetches, side effects, or auth assumptions.
- Beware of false positives in file-system routers, dynamic imports, and code-splitting boundaries.

### Next.js and server/client boundaries

- Client-only APIs must not leak into server-only code paths.
- Sensitive server data should not be serialized into client props or actions without need.
- For Server Actions, review origin restrictions and request size limits when the deployment model needs proxies or trusted cross-origins.

### Accessibility and forms

- Interactive controls need correct semantics, labels, and focus behavior.
- Missing `type="button"` inside forms can create accidental submissions.
- Error states should be exposed in a way users can perceive and recover from.

## High-Signal Findings

Report issues such as:

- stale closure due to missing dependencies
- mutation triggered from render
- race between request responses causing wrong UI state
- reorderable list keyed by index
- broken form submit semantics
- server-only secret or privileged data crossing into client code
- orphan route component or dead UI flow preserved after a refactor

## Usually Skip

- requests to add `useMemo` everywhere
- blanket component splitting advice
- style-only JSX preferences
- broad "too many props" complaints without a concrete bug or maintainability break
- components that only look unused because they are loaded by framework routing or dynamic import conventions

## Source Notes

- React Hooks lint docs: https://react.dev/reference/eslint-plugin-react-hooks
- React `exhaustive-deps`: https://react.dev/reference/eslint-plugin-react-hooks/lints/exhaustive-deps
- React refs lint: https://react.dev/reference/eslint-plugin-react-hooks/lints/refs
- Next.js data security guide: https://nextjs.org/docs/app/guides/data-security
- Next.js `serverActions` config: https://nextjs.org/docs/app/api-reference/config/next-config-js/serverActions
- TypeScript `noUnusedLocals`: https://www.typescriptlang.org/tsconfig/noUnusedLocals.html
- TypeScript `allowUnreachableCode`: https://www.typescriptlang.org/tsconfig/allowUnreachableCode.html
