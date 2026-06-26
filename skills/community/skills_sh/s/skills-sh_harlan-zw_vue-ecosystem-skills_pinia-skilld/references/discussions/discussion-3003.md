---
number: 3003
title: Pinia plugins not working inside tests
category: Help and Questions
created: 2025-07-09
url: "https://github.com/vuejs/pinia/discussions/3003"
upvotes: 1
comments: 2
answered: true
---

# Pinia plugins not working inside tests

Even the most basic plugin fails in a test environment:

```
it('tests', async () => {
  const foo = vi.fn();

  const pinia = createPinia();
  pinia.use(({ store }) => foo(store.$id));
  setActivePinia(pinia);

  const useTestStore = defineStore('store', { state: () => ({ foo: 1 }) });
  const store = useTestStore();

  expect(foo).toHaveBeenCalled();
});

```

Here is a minimal reproduction: https://stackblitz.com/edit/github-ofdqvmtu?file=test.test.ts

---

## Accepted Answer

```javascript
import { it, expect, vi } from 'vitest';
import { createPinia, setActivePinia, defineStore } from 'pinia';
import { createApp, defineComponent, h, KeepAlive } from 'vue';

it('tests', async () => {
  const foo = vi.fn();

  const pinia = createPinia().use(({ store }) => foo(store.$id));
  setActivePinia(pinia);

  createApp(defineComponent(() => () => h(KeepAlive, {}))).use(pinia); // this is needed for the store to work

  const useTestStore = defineStore('store', { state: () => ({ foo: 1 }) });
  const store = useTestStore();

  expect(foo).toHaveBeenCalled();
});
```