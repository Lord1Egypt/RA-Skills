---
name: svelte-component-auditor
description: Audit Svelte and SvelteKit components for performance, accessibility, reactive statement usage, store design, and SSR compatibility. Use when reviewing Svelte codebases, optimizing rendering performance, or enforcing component best practices.
metadata:
  tags: ["svelte", "sveltekit", "frontend", "accessibility", "performance", "code-quality"]
---

# Svelte Component Auditor

Deep audit of Svelte and SvelteKit components. Analyzes reactive declarations, store patterns, accessibility, SSR readiness, and rendering performance. Produces prioritized findings with concrete fixes.

Use when: reviewing a Svelte/SvelteKit project, preparing for production, auditing accessibility, or establishing component quality standards.

## Analysis Steps

### 1. Project Discovery

```bash
cat package.json 2>/dev/null | jq '{svelte: .devDependencies.svelte, sveltekit: .devDependencies["@sveltejs/kit"]}'
cat svelte.config.js 2>/dev/null || cat svelte.config.ts 2>/dev/null
find . -name "*.svelte" -not -path '*/node_modules/*' -not -path '*/.svelte-kit/*' | wc -l
find . -path "*/routes/*" -name "+*" -not -path '*/node_modules/*' 2>/dev/null | sort | head -20
```

Determine: Svelte version (4 vs 5 runes), SvelteKit presence, adapter type, component count, route structure.

### 2. Reactive Statement Audit

```bash
# Reactive declarations ($: label syntax — Svelte 4)
grep -rn '^\s*\$:' --include="*.svelte" . 2>/dev/null | head -25

# Reactive assignments that won't trigger (array mutation)
grep -rn '\$:.*\.push\|\$:.*\.splice\|\$:.*\.sort' --include="*.svelte" . 2>/dev/null | head -15

# Complex reactive chains (>5 per component = smell)
for f in $(find . -name "*.svelte" -not -path '*/node_modules/*' 2>/dev/null); do
  count=$(grep -c '^\s*\$:' "$f" 2>/dev/null)
  if [ "$count" -gt 5 ]; then echo "COMPLEX($count): $f"; fi
done | head -15

# Svelte 5 runes
grep -rn '\$state\|\$derived\|\$effect\|\$props' --include="*.svelte" --include="*.svelte.ts" . 2>/dev/null | head -15
```

Check for:
- **Mutating arrays in reactive declarations**: `$: items.push(x)` won't trigger — must reassign: `items = [...items, x]`
- **Circular reactive dependencies**: cause runtime errors
- **Over-complex reactive chains**: >5 `$:` declarations signals need for store or utility extraction
- **$effect without cleanup**: effects with subscriptions/timers must return a cleanup function

### 3. Store Design Analysis

```bash
grep -rn "writable(\|readable(\|derived(" --include="*.ts" --include="*.js" --include="*.svelte" . 2>/dev/null | grep -v 'venv/' | head -20

# Store subscriptions without unsubscribe (leak in non-component code)
grep -rn "\.subscribe(" --include="*.ts" --include="*.js" . 2>/dev/null | head -15

# Auto-subscription in components ($store)
grep -rn '\$[a-zA-Z]' --include="*.svelte" . 2>/dev/null | grep -v '\$:\|//' | head -15
```

Flag:
- **Store subscriptions in .ts/.js without unsubscribe**: auto-unsubscribe (`$store`) only works in .svelte files
- **Global stores with SSR**: module-scope writable stores cause cross-request data leaks — use context or page data
- **Missing derived stores**: repeated computations across components should be derived
- **Overloaded stores**: single store managing unrelated concerns — split by domain

### 4. Performance Analysis

```bash
# Large components (>200 lines)
for f in $(find . -name "*.svelte" -not -path '*/node_modules/*' 2>/dev/null); do
  lines=$(wc -l < "$f"); if [ "$lines" -gt 200 ]; then echo "LARGE($lines): $f"; fi
done | sort -t'(' -k1.7 -rn | head -10

# Unkeyed each blocks
grep -rn '{#each' --include="*.svelte" . 2>/dev/null | grep -v '(' | head -15

# bind:this overuse
grep -rn "bind:this" --include="*.svelte" . 2>/dev/null | head -15
```

Flag:
- **Unkeyed each blocks**: `{#each items as item}` without key causes full list re-renders on any change
- **Components >300 lines**: decompose into sub-components
- **Excessive bind:this**: direct DOM manipulation bypasses reactivity

### 5. Accessibility Audit

```bash
# Images without alt
grep -rn '<img' --include="*.svelte" . 2>/dev/null | grep -v 'alt=' | head -15

# Click handlers on non-interactive elements
grep -rn 'on:click' --include="*.svelte" . 2>/dev/null \
  | grep '<div\|<span\|<li\|<p' | head -15

# Form inputs without labels
grep -rn '<input' --include="*.svelte" . 2>/dev/null \
  | grep -v 'aria-label\|id=.*label\|type="hidden"\|type="submit"' | head -15

# Focus management
grep -rn 'focus()\|tabindex\|aria-live\|aria-expanded' --include="*.svelte" . 2>/dev/null | head -10
```

Flag with WCAG reference:
- **Images without alt**: WCAG 1.1.1 — all `<img>` must have alt (empty for decorative)
- **Click on non-interactive elements**: WCAG 4.1.2 — use `<button>` or add `role="button"` + `tabindex="0"` + keyboard handler
- **Inputs without labels**: WCAG 1.3.1 — every form control needs an accessible name
- **No aria-live regions**: WCAG 4.1.3 — dynamic status messages need `aria-live="polite"`

### 6. SSR Compatibility

```bash
# Browser-only APIs used outside onMount
grep -rn 'window\.\|document\.\|localStorage\|sessionStorage\|navigator\.' \
  --include="*.svelte" --include="*.ts" . 2>/dev/null \
  | grep -v 'node_modules\|\.svelte-kit\|onMount\|onDestroy\|browser' | head -15

# $app/environment browser guard
grep -rn "import.*browser.*\$app" --include="*.svelte" --include="*.ts" . 2>/dev/null | head -10

# Data fetching in components instead of load functions
grep -rn "fetch(" --include="*.svelte" . 2>/dev/null | grep -v 'node_modules' | head -10

# Private env leaked to client
grep -rn '\$env/static/private\|\$env/dynamic/private' --include="*.svelte" . 2>/dev/null | head -5
```

Flag:
- **Browser APIs outside lifecycle hooks**: `window`, `document`, `localStorage` at top level crash SSR
- **Missing `browser` guard**: import `{ browser }` from `$app/environment` to guard browser-only code
- **Cross-request state pollution**: module-level mutable state shared across SSR requests
- **Private env in client code**: `$env/static/private` imported in .svelte files leaks secrets
- **Fetching in components**: SvelteKit load functions provide streaming, caching, and SSR — component fetch loses these

### 7. Component API Surface

```bash
grep -rn 'export let ' --include="*.svelte" . 2>/dev/null | head -15
grep -rn 'export let [a-zA-Z]*;$' --include="*.svelte" . 2>/dev/null | head -10
grep -rn "createEventDispatcher\|setContext\|getContext" --include="*.svelte" . 2>/dev/null | head -15
grep -rn '\$\$props\|\$\$restProps' --include="*.svelte" . 2>/dev/null | head -10
```

Flag:
- **Props without defaults**: no compile-time enforcement that callers provide them
- **$$props/$$restProps overuse**: bypasses Svelte's prop tracking, prevents tree-shaking
- **Missing slot fallback content**: `<slot>fallback</slot>` provides better DX
- **Untyped context**: `setContext`/`getContext` should use typed keys

## Output Template

```markdown
# Svelte Component Audit — [Project Name]

## Summary
- Components: N | Svelte: 4.x/5.x | SvelteKit: yes/no
- Critical: N | Warnings: N | A11y violations: N

## Critical Findings
### [C1] SSR Crash — `window.innerWidth` at top level
- **File**: src/routes/dashboard/+page.svelte:8
- **Fix**: Move inside `onMount(() => { ... })`

### [C2] Cross-Request State Leak
- **File**: src/lib/stores/user.ts:3 — module-scope writable
- **Fix**: Initialize in load functions or context API

## Accessibility Violations
| Rule | Count | Severity | Files |
|------|-------|----------|-------|
| img-alt-missing | N | Critical | file1, file2 |
| click-on-div | N | High | file3 |
| input-no-label | N | High | file4 |

## Performance Issues
| Issue | File | Fix |
|-------|------|-----|
| Unkeyed each block | List.svelte:24 | Add `(item.id)` key |
| 450-line component | Dashboard.svelte | Split into sub-components |

## Recommendations
1. Fix N SSR-breaking browser API usages
2. Add keys to N each blocks
3. Resolve N accessibility violations
4. Move N module-scope stores to context/load for SSR safety
5. Add `+error.svelte` at route group levels
```

## Tips

- Run `npx svelte-check` for type errors, a11y warnings, and unused CSS
- Use `@sveltejs/enhanced-img` for automatic image optimization in SvelteKit
- Enable `compilerOptions.runes: true` in svelte.config.js to start Svelte 5 migration
- Use `{#key expression}` to force-recreate a component when data changes
- Test SSR locally with `adapter-node` before deploying to catch browser API issues
