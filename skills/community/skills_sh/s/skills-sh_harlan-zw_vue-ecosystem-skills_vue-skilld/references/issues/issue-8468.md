---
number: 8468
title: @vue/compiler-sfc cannot build  components that use generic discriminated union props
type: other
state: open
created: 2023-05-31
url: "https://github.com/vuejs/core/issues/8468"
reactions: 12
comments: 7
labels: "[scope: compiler, scope: script-setup]"
---

# @vue/compiler-sfc cannot build  components that use generic discriminated union props

### Vue version

3.3.4

### Link to minimal reproduction

https://github.com/justin-schroeder/generics-discriminated-union-reproduction

### Steps to reproduce

Any component with generics, where the generics extend a discriminated union cannot be compiled by `@vue/compiler-sfc` — however, they work just fine with Volar.

```jsx
// Input.vue
<script setup lang="ts" generic="P extends Inputs">
import type { Inputs } from '../props.ts'

defineProps<P>()
</script>
```


```ts
// props.ts
type Text = { type: 'text', value: string }
type Number = { type: 'number', value: number }

export type Inputs = Text | Number
```


### What is expected?

Typed prop unions work both in both Volar and build time.

### What is actually happening?

The following error is thrown:

```
[vite] Internal server error: [@vue/compiler-sfc] Unresolvable type reference or unsupported built-in utility type

/src/components/Input.vue
2  |  import type { Inputs } from '../props.ts'
3  |  
4  |  const props = defineProps<P>()
   |                            ^
5  |  </script>
```


Full reproduction repository here: https://github.com/justin-schroeder/generics-discriminated-union-reproduction

### System Info

```shell
System:
    OS: macOS 13.1
    CPU: (10) arm64 Apple M1 Pro
    Memory: 63.72 MB / 16.00 GB
    Shell: 5.8.1 - /bin/zsh
  Binaries:
    Node: 18.14.2 - /usr/local/bin/node
    Yarn: 1.22.18 - ~/.yarn/bin/yarn
    npm: 9.5.0 - /usr/local/bin/npm
  Browsers:
    Brave Browser: 113.1.51.118
    Chrome: 113.0.5672.126
    Edge: 113.0.1774.57
    Firefox: 111.0.1
    Safari: 16.2
  npmPackages:
    vue: 3.3.4 => 3.3.4
```
```


### Any additional comments?

_No response_