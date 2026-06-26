---
number: 2901
title: "Pinia module causing [500] internal server error after upgrading to Nuxt version to 3.15.x"
category: Help and Questions
created: 2025-01-29
url: "https://github.com/vuejs/pinia/discussions/2901"
upvotes: 1
comments: 1
answered: true
---

# Pinia module causing [500] internal server error after upgrading to Nuxt version to 3.15.x

### Reproduction

https://stackblitz.com/edit/github-6p4rt1bq

### Steps to reproduce the bug

No specific steps required as when the app starts I am getting `500
internal server error`. 
In the console I am getting twice
```zsh
[nuxt] [request error] [unhandled] [500] [🍍]: "getActivePinia()" was called but there was no active Pinia. Are you trying to use a store before calling "app.use(pinia)"?
See https://pinia.vuejs.org/core-concepts/outside-component-usage.html for help.
This will fail in production.
```

### Expected behavior


It shouldn't produce any errors as I am using just a plain starter template with `npx nuxi@latest init <my-app>` and a store file from the pinia documentation example:
```ts
export const useCounterStore = defineStore("counter", () => {
    const count = ref(0)
    const name = ref("Eduardo")
    const doubleCount = computed(() => count.value * 2)
    function increment() {
        count.value++
    }

...

---

## Accepted Answer

**@posva** [maintainer]:

You are using a regular script instead of a setup one:

```vue
<script lang="ts" setup>
const store = useCounterStore();
</script>
```

The issue you are falling is in the link mentioned in the warning, https://pinia.vuejs.org/core-concepts/outside-component-usage.html