---
number: 14350
title: defineModel default value is NOT reactive, buts that's odd
category: Help/Questions
created: 2026-01-22
url: "https://github.com/orgs/vuejs/discussions/14350"
upvotes: 2
comments: 1
answered: false
---

# defineModel default value is NOT reactive, buts that's odd

So I have a component, where I need to use the v-model in a scenario and one I don't.

```typescript
const state = defineModel<CustomerLookupState>('lookup', {
    default: () =>({
        phone_number: '',
        birthday: null,
        location_id: null,
    }),
});
```

And then in my component, I bind the `state` to some form component.

In scenario 1, where I bind the v-model to my component, everything is working fine.

In scenario 2, I don't need to bind the v-model, I want to use the defineModel and need the default value.

As per https://github.com/vuejs/core/issues/10009, it states I should wrap it in `reactive`. That works.

This feels weird, because of the use-case that you can use defineModel as a "standalone" ref, but if I define a default value, the defi...

---

## Top Comments

**@sunnypatell**:

@yooouuri this is by design. `defineModel` compiles to `useModel()` in `packages/runtime-core/src/helpers/useModel.ts`, which uses `customRef` internally. the default value gets stored in a plain `localValue` variable, not a reactive proxy.

when you do `state.value.phone_number = 'x'`, you're mutating a property on a plain object. the `customRef`'s `set()` is never called (you're not replacing `state.value`, just mutating a nested property), so no reactivity triggers.

...