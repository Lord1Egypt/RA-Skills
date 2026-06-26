---
number: 6207
title: SSR teleports don't work with Suspense
type: other
state: open
created: 2022-06-30
url: "https://github.com/vuejs/core/issues/6207"
reactions: 28
comments: 0
labels: "[scope: suspense, scope: teleport, scope: ssr]"
---

# SSR teleports don't work with Suspense

### Vue version

3.2.37

### Link to minimal reproduction

https://stackblitz.com/edit/github-kqkhhq

### Steps to reproduce

The following code is sufficient to reproduce the bug:
```vue
<Teleport to="#async">
  <Suspense>
    <SomeAsyncComponent />
  </Suspense>
</Teleport>
```

In the reproduction sandbox, you can see that on _client-side_ this behaves correctly (and would hydrate HTML that rendered correctly), and also that this behaves fine on SSR with a sync component.

Note that the same behaviour is displayed if suspense is lifted higher (some nodes higher than teleport) or is nested deeper within the teleport.

### What is expected?

It's expected that the async component will render into the teleport on SSR.

### What is actually happening?

Instead, all that is rendered is the teleport anchor.

### System Info

```shell
Stackblitz.
```


### Any additional comments?

_No response_