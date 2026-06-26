---
title: Fix Nullish Coalescing Runtime Errors
impact: HIGH
impactDescription: Complex expressions cause runtime errors
tags: gotchas, javascript, operators, runtime
---

## Fix Nullish Coalescing Runtime Errors

Complex expressions using nullish coalescing (`??`) can cause `_variable is not defined` runtime errors in Next.js due to how the code is transpiled.

**Error message:**

```
ReferenceError: _someVariable is not defined
```

**Problematic pattern:**

```tsx
// This can cause runtime errors in Next.js
const value = someObject?.deeply?.nested?.property ?? fallbackFunction()

// Also problematic with complex expressions
const result = (condition ? objectA : objectB)?.value ?? defaultValue
```

**SWC-specific problematic contexts:**

These patterns are especially prone to SWC transpilation issues:

```tsx
// In ternary false branches - SWC mangles this
condition ? value : element.boundElements ?? []

// After function calls - SWC mangles this
getFormValue(...) ?? undefined

// In object property values within conditionals
active: option.active ?? props.value === option.value

// In complex conditional assignments
const elements = isValid ? items : container.elements ?? []
```

**Why this happens:**

The transpilation of nullish coalescing with optional chaining creates intermediate variables. In certain edge cases with complex expressions, these variables may not be properly scoped.

**Solution 1: Use explicit ternary operator**

```tsx
// Before (problematic)
const value = someObject?.deeply?.nested?.property ?? fallbackValue

// After (safe)
const value = someObject?.deeply?.nested?.property !== null &&
              someObject?.deeply?.nested?.property !== undefined
  ? someObject.deeply.nested.property
  : fallbackValue
```

**Solution 2: Use logical OR for falsy fallbacks**

If you only need to handle `null`/`undefined` and the value won't be `0`, `''`, or `false`:

```tsx
// Before
const value = someObject?.property ?? 'default'

// After (if property won't be 0, '', or false)
const value = someObject?.property || 'default'
```

**Solution 3: Break into separate statements**

```tsx
// Before (complex expression)
const value = (condition ? objectA : objectB)?.nested?.prop ?? fallback

// After (clear and safe)
const selectedObject = condition ? objectA : objectB
const nestedValue = selectedObject?.nested?.prop
const value = nestedValue ?? fallback
```

**Solution 4: Use intermediate variables**

```tsx
// Before
const displayName = user?.profile?.displayName ?? user?.username ?? 'Anonymous'

// After
const profileName = user?.profile?.displayName
const username = user?.username
const displayName = profileName ?? username ?? 'Anonymous'
```

**Solution 5: Use `nc()` helper function for files with many occurrences**

When a file has numerous nullish coalescing expressions that need fixing, a helper function reduces repetition:

```tsx
// Define at the top of the file or in a utils module
const nc = <T>(value: T | null | undefined, defaultValue: T): T =>
  value != null ? value : defaultValue;

// Usage examples
const boundElements = nc(element.boundElements, [])
const formValue = nc(getFormValue(field), undefined)
const isActive = nc(option.active, props.value === option.value)
```

This approach:
- Preserves nullish coalescing semantics (only replaces `null`/`undefined`)
- Avoids SWC transpilation issues
- Keeps code readable when many expressions need fixing

**When to watch for this issue:**

- Chained optional access with nullish coalescing: `a?.b?.c ?? d`
- Conditional expressions with optional chaining: `(x ? a : b)?.c ?? d`
- Function calls in nullish coalescing: `obj?.method?.() ?? fallback()`
- Deeply nested object access patterns
- Ternary false branches: `cond ? x : y ?? z`
- Object property values in conditionals

**Search patterns for affected code:**

```bash
# Find potential issues
grep -r "\?\." --include="*.tsx" --include="*.ts" | grep "??"

# Find ternary expressions with nullish coalescing
grep -rE "\? .* : .*\?\?" --include="*.tsx" --include="*.ts"
```
