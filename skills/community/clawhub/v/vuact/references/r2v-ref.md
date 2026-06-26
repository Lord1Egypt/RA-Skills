# r2v Component Ref

r2v lets you get a React component ref from the Vue side, so you can call methods exposed by the React component or access its properties.

**Use cases**:
- Call public methods on React components
- Access instance properties on React components
- Implement imperative control from parent to child

## React Function Components

For React function components, use `forwardRef` and `useImperativeHandle` to expose methods:

```tsx
import { forwardRef, useImperativeHandle, useState } from 'react';

export default forwardRef(function FunctionComponent(_, ref) {
  const [count, setCount] = useState(0);
  
  // Expose methods to the parent via useImperativeHandle
  useImperativeHandle(ref, () => ({
    incCount() {
      setCount((c) => c + 1);
    },
  }));
  
  return <div>{count}</div>;
});
```

**Key points**:
1. Wrap the function component with `forwardRef`
2. Define the methods exposed to the parent with `useImperativeHandle`

## React Class Components

For React class components, all public methods are exposed automatically with no extra configuration:

```tsx
import { Component } from 'react';

export default class ClassComponent extends Component {
  state = { count: 0 };
  
  incCount() {
    this.setState({ count: this.state.count + 1 });
  }
  
  render() {
    return <div>{this.state.count}</div>;
  }
}
```

## Vue Usage

Use a ref in Vue to access a React component instance:

```vue
<script setup lang="ts">
import { shallowRef } from 'vue';
import { r2v } from 'vuact';
import FunctionComponent from './function-component';
import ClassComponent from './class-component';

const VFunctionComponent = r2v(FunctionComponent);
const VClassComponent = r2v(ClassComponent);

// Store component references with shallowRef
const functionComponentRef = shallowRef<InstanceType<typeof VFunctionComponent>>();
const classComponentRef = shallowRef<InstanceType<typeof VClassComponent>>();

function incCount() {
  // Access the React component instance via ref.value?.instance
  functionComponentRef.value?.instance?.incCount();
  classComponentRef.value?.instance?.incCount();
}
</script>

<template>
  <div>
    <button @click="incCount">incCount</button>
    <VFunctionComponent ref="functionComponentRef" />
    <VClassComponent ref="classComponentRef" />
  </div>
</template>
```

**Key points**:
1. Use `shallowRef` or `ref` to store component references
2. Access the React component instance via `ref.value?.instance`
3. Then you can call the methods exposed by the React component
