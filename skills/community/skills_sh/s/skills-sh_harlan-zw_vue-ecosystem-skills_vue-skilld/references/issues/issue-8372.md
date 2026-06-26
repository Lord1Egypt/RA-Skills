---
number: 8372
title: Inherit attributes with generic components causes type error
type: other
state: closed
created: 2023-05-19
url: "https://github.com/vuejs/core/issues/8372"
reactions: 29
comments: 5
labels: "[scope: types]"
---

# Inherit attributes with generic components causes type error

### Vue version

3.3.4

### Link to minimal reproduction

https://stackblitz.com/edit/vitejs-vite-nwkbil?file=package.json,src%2Fcomponents%2FListGeneric.vue,src%2FApp.vue,src%2Fcomponents%2FList.vue

### Steps to reproduce

1. Open a new Terminal after successful setup of dependencies
2. Type and run `npm run typecheck` into the terminal
3. See an error in App.vue file

### What is expected?

There is no error occurred

### What is actually happening?

```
TS2345: Argument of type '{ dataCy: string; "data-cy": string; modelValue: "modelValue"; "onUpdate:modelValue": any; }' is not assignable to parameter of type '{ modelValue: "modelValue"; sameModel?: string | undefined; } & VNodeProps & AllowedComponentProps & ComponentCustomProps'.
  Object literal may only specify known properties, and 'dataCy' does not exist in type '{ modelValue: "modelValue"; sameModel?: string | undefined; } & VNodeProps & AllowedComponentProps & ComponentCustomProps'.
  ```

### System Info

_No response_

### Any additional comments?

_No response_