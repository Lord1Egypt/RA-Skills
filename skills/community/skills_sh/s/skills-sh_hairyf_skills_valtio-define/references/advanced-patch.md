---
name: advanced-patch
description: Update store state using patch operations
---

# $patch

Update store state with partial updates or functional updates. More efficient than direct mutation when updating multiple properties.

## Object Patch

Update state with a partial object:

```tsx
const store = defineStore({
  state: () => ({ count: 0, name: 'test' }),
})

// Update multiple properties at once
store.$patch({ count: 10, name: 'updated' })
```

**Key Points:**
* Merges properties into existing state
* Only updates specified properties
* Triggers reactivity for changed properties

## Functional Patch

Update state with a function:

```tsx
store.$patch((state) => {
  state.count += 5
  state.name = 'modified'
})
```

**Key Points:**
* Direct access to state object
* Can perform complex updates
* Useful for conditional updates or calculations
* State is mutable within the function

## When to Use

**Use $patch when:**
* Updating multiple properties atomically
* Need to ensure all updates happen together
* Updating from external sources (e.g., API responses)

**Use direct mutation when:**
* Simple single-property updates
* Inside actions (where `this` is already bound)

```tsx
// Inside action - direct mutation is fine
actions: {
  increment() {
    this.count++ // ✅ Direct mutation
  },
  reset() {
    this.count = 0
    this.name = 'reset'
  },
}

// Outside action - prefer $patch
store.$patch({ count: 0, name: 'reset' }) // ✅ Atomic update
```
