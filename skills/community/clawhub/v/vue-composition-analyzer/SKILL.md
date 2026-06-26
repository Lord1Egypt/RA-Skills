---
name: vue-composition-analyzer
description: Analyze Vue 3 Composition API usage — audit reactivity patterns, composable design, ref vs reactive choices, computed properties, watcher usage, and component lifecycle hooks. Use when reviewing Vue 3 codebases, migrating from Options API, or enforcing Composition API best practices.
metadata:
  tags: ["vue", "vue3", "composition-api", "reactivity", "frontend", "code-quality"]
---

# Vue Composition API Analyzer

Deep analysis of Vue 3 Composition API usage. Detects anti-patterns in reactivity, composable design, watcher usage, lifecycle hooks, and component structure. Produces actionable findings with severity levels.

Use when: reviewing Vue 3 quality, migrating from Options API, auditing composable architecture, or enforcing Composition API conventions.

## Analysis Steps

### 1. Project Discovery & API Style Census

```bash
cat package.json 2>/dev/null | jq '{vue: .dependencies.vue, nuxt: .dependencies.nuxt, pinia: .dependencies.pinia}'
find . -name "*.vue" -not -path '*/node_modules/*' | wc -l

# Options API components
grep -rl "export default {" --include="*.vue" . 2>/dev/null | while read f; do
  grep -l "data()\|methods:\|computed:" "$f" 2>/dev/null
done | sort -u | head -20

# Script setup (preferred) vs setup()
grep -rl "<script setup" --include="*.vue" . 2>/dev/null | wc -l
grep -rl "setup()" --include="*.vue" . 2>/dev/null | wc -l
```

Classify each component as Options API, `setup()`, or `<script setup>`. Flag mixed-style codebases.

### 2. Reactivity Pattern Audit

```bash
grep -rn "ref(\|reactive(\|shallowRef\|shallowReactive" --include="*.vue" --include="*.ts" . 2>/dev/null | head -30

# Reactivity loss: destructuring reactive without toRefs
grep -rn "const {.*} = .*reactive\|let {.*} = .*reactive" --include="*.vue" --include="*.ts" . 2>/dev/null | head -15

# toRefs usage
grep -rn "toRefs\|toRef(" --include="*.vue" --include="*.ts" . 2>/dev/null | head -15
```

Check for:
- **Reactivity loss**: destructuring `reactive()` without `toRefs()` silently breaks reactivity
- **ref vs reactive confusion**: `ref` for primitives and replaceable objects, `reactive` for stable complex objects
- **Unnecessary reactive**: wrapping a primitive in `reactive({count: 0})` instead of `ref(0)`
- **Missing shallowRef**: large objects that don't need deep reactivity (DOM elements, third-party instances)
- **Double wrapping**: `ref(reactive({...}))` — always a bug

### 3. Computed & Watcher Audit

```bash
grep -rn "computed(" --include="*.vue" --include="*.ts" . 2>/dev/null | head -20

# Side effects in computed
grep -A5 "computed(" --include="*.vue" --include="*.ts" . 2>/dev/null \
  | grep -i "console\.\|fetch(\|emit(\|\.value =" | head -15

# Watchers
grep -rn "watch(\|watchEffect(" --include="*.vue" --include="*.ts" . 2>/dev/null | head -20

# Immediate watchers (often replaceable with watchEffect)
grep -A10 "watch(" --include="*.vue" --include="*.ts" . 2>/dev/null | grep "immediate: true" | head -10

# Deep watchers on large objects
grep -A10 "watch(" --include="*.vue" --include="*.ts" . 2>/dev/null | grep "deep: true" | head -10
```

Flag:
- **Side effects in computed**: computed must be pure derivations, never mutate state or trigger I/O
- **Non-reactive dependencies in computed**: reading `localStorage`/`window` won't trigger re-computation
- **watch + immediate: true**: usually replaceable with `watchEffect()`
- **deep: true on large objects**: performance risk, prefer watching specific nested paths
- **Async watchers without onCleanup**: race conditions on rapid value changes

### 4. Composable Design Review

```bash
find . -name "use*.ts" -o -name "use*.js" -not -path '*/node_modules/*' 2>/dev/null | head -20
find . -path "*/composables/*" -not -name "use*" -not -path '*/node_modules/*' -name "*.ts" 2>/dev/null | head -10

# Composables using component-specific APIs
grep -rn "defineProps\|defineEmits\|useSlots" --include="*.ts" . 2>/dev/null | grep -i "composable\|use" | head -10
```

Evaluate:
- **Naming**: composables must start with `use` prefix
- **Single responsibility**: one concern per composable
- **Return type**: should return refs (not raw values) so consumers maintain reactivity
- **Side effect cleanup**: event listeners, timers, subscriptions must clean up via `onUnmounted`
- **Testability**: composables should be testable outside components

### 5. Lifecycle & Resource Leaks

```bash
# onMounted without matching onUnmounted
for f in $(grep -rl "onMounted" --include="*.vue" . 2>/dev/null); do
  if ! grep -q "onUnmounted\|onBeforeUnmount" "$f"; then
    echo "MISSING_CLEANUP: $f"
  fi
done | head -15

# addEventListener without removeEventListener
grep -l "addEventListener" --include="*.vue" --include="*.ts" . 2>/dev/null | while read f; do
  if ! grep -q "removeEventListener" "$f"; then echo "LISTENER_LEAK: $f"; fi
done | head -15

# setInterval without clearInterval
grep -l "setInterval" --include="*.vue" . 2>/dev/null | while read f; do
  if ! grep -q "clearInterval" "$f"; then echo "INTERVAL_LEAK: $f"; fi
done | head -10
```

### 6. Props & Dependency Injection

```bash
grep -rn "defineProps" --include="*.vue" . 2>/dev/null | head -15
grep -A5 "defineProps(\[" --include="*.vue" . 2>/dev/null | head -15
grep -rn "provide(\|inject(" --include="*.vue" --include="*.ts" . 2>/dev/null | head -15
```

Flag:
- **Array-style defineProps**: `defineProps(['foo'])` has no type safety; use object or TypeScript generic syntax
- **Untyped provide/inject**: use `InjectionKey<T>` for type safety
- **Prop mutation**: directly modifying props (Vue warns at runtime, static analysis catches earlier)

## Output Template

```markdown
# Vue Composition API Analysis — [Project Name]

## Summary
- Components: N | Script setup: N% | Options API remaining: N
- Critical: N | Warnings: N

## API Style Migration
| Style | Count | Files |
|-------|-------|-------|
| `<script setup>` | N | — |
| `setup()` function | N | file1.vue |
| Options API | N | legacy1.vue |

## Critical Findings
### [C1] Reactivity Loss — destructuring reactive without toRefs
- **File**: src/components/UserForm.vue:24
- **Code**: `const { name, email } = userState`
- **Fix**: `const { name, email } = toRefs(userState)`

### [C2] Side Effect in Computed
- **File**: src/composables/useCart.ts:45
- **Fix**: Move localStorage write to a watcher

## Warnings
### [W1] Missing Cleanup — addEventListener in onMounted, no onUnmounted
### [W2] Deep Watcher on 1000+ item array — watch specific properties instead

## Composable Health
| Composable | Issues |
|-----------|--------|
| useAuth | Returns raw values instead of refs |
| useCart | No cleanup for event subscription |

## Recommendations
1. Convert N Options API components to `<script setup>`
2. Add `InjectionKey<T>` types to provide/inject pairs
3. Replace `watch(..., { immediate: true })` with `watchEffect()` in N places
4. Add `onUnmounted` cleanup to N components with resource subscriptions
```

## Anti-Pattern Quick Reference

| Anti-Pattern | Severity | Description |
|-------------|----------|-------------|
| Destructure reactive | Critical | Breaks reactivity silently |
| Side effects in computed | Critical | Non-deterministic, SSR-incompatible |
| ref(reactive(...)) | Critical | Double-wrapping, confusing unwrap |
| Missing watcher cleanup | High | Memory leaks, race conditions |
| Deep watch large objects | Medium | Performance degradation |
| watch + immediate | Low | Prefer watchEffect |
| Array-style defineProps | Low | No type safety or defaults |

## Tips

- Use Vue DevTools "Performance" tab to visualize reactive dependency chains
- Run `npx vue-tsc --noEmit` to type-check all SFC files including template expressions
- Consider `effectScope()` in composables that create many watchers/effects for batch cleanup
- Nuxt 3: check `useAsyncData`/`useFetch` for proper key usage and deduplication
