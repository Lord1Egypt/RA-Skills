---
number: 3026
title: TypeScript shows incorrect ref type for setup store properties instead of auto-unwrapped type
category: Help and Questions
created: 2025-08-26
url: "https://github.com/vuejs/pinia/discussions/3026"
upvotes: 1
comments: 1
answered: true
---

# TypeScript shows incorrect ref type for setup store properties instead of auto-unwrapped type

### Reproduction

https://pinia.vuejs.org/core-concepts/#Using-the-store

### Steps to reproduce the bug

  1. Create a Pinia store using setup syntax with defineStore('name', () 
  => {})
  2. Define a ref inside the store: const count = ref(0)
  3. Return the ref from the store: return { count }
  4. Use the store in a Vue component: const store = useChatStore()
  5. Access the property: store.count
  6. Check TypeScript IntelliSense/hover information

### Expected behavior

  - TypeScript should show count: number (auto-unwrapped type)
  - IntelliSense should provide correct type hints for the unwrapped value
  - No TypeScript errors when using the property as a number
  - Type should match runtime behavior

### Actual behavior

...

---

## Accepted Answer

**@posva** [maintainer]:

This was fixed in newer version, upgrade your versions.

Don't open issues that do not follow the guidelines, thank you.