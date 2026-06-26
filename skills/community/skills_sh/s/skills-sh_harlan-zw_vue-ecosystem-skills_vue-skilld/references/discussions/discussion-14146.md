---
number: 14146
title: Status of `#=` v-slot shorthand for default slot
category: General Discussions
created: 2025-11-28
url: "https://github.com/orgs/vuejs/discussions/14146"
upvotes: 2
comments: 1
answered: false
---

# Status of `#=` v-slot shorthand for default slot

Recently I learned that Vue supports even shorter syntax of `v-slot` directive for default slot: simply `#` instead of `#default` (playground):

```vue
<template>
  <Comp #="{foo}">{{ foo }}</Comp>
  <Comp>
    <template #="{foo}">{{ foo }}</template>
  </Comp>
</template>
```

However, I have not found any official information about this feature, so I wo...

---

## Top Comments

**@andreww2012**:

Wow, it looks like `:=` and `@=` shorthands for `v-bind="` and `v-on="` respectively are also supported. It would be awesome to see them documented too 