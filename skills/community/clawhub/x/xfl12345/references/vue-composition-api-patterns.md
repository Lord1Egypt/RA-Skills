---
name: vue-composition-api-patterns
description: >
  Vue 3 `<script setup>` 常用模式。写、改、审基于 Vue 3 setup 语法糖的组件时触发。
---

# Vue 3 Composition API 常用模式

## 双向绑定与事件

- 父子组件数据双向绑定用 `v-model` + `defineModel`
- 简单事件驱动的数据，用可写计算属性代劳

❌ BAD: 手工绑 :model-value + @update:model-value + 处理函数，不仅啰嗦，还因为需要维护 4 处符号的对接，心智负担重，可读性差

```vue
<script setup lang="ts">
import { useContext } from './context'
import { NameInput } from './component'

const context = useContext()
function onNameInput(name: string) {
  context.setName(name)
}
</script>
<template>
  <NameInput :modelValue="context.name" @update:modelValue="onNameInput" />
</template>
```

✅ GOOD: 可写 computed 桥接源数据，模板里直接 v-model

```vue
<script setup lang="ts">
import { computed } from 'vue'

import { useContext } from './context'
import { NameInput } from './component'

const context = useContext()
// 条理清晰，边界明确。仅用一个符号管住同一对 getter/setter ，
// 阅读不跳跃，可读性强，极大减轻心智负担。同时又能防止符号泛滥、跟踪困难
const name = computed<string>({
  get: () => context.name,
  set: (v) => (context.setName(v)),
})
</script>
<template>
  <NameInput v-model="name" />
</template>
```

## 函数默认指定具体类型

- ✅ `defineModel<T>({ ... })`
- ✅ `defineModel<T>('fieldName', { ... })`
- ✅ `computed<T>(() => '')`
- ✅ `ref<T>()`
- ✅ `reactive<T>({ ... })`

### 例外

函数体内只有一个可变变量并返回它时，为了避免同样的类型写两遍，可省略泛型，改在函数内标注该变量类型：

❌ BAD: 仅返回一个可变变量类型时，重复声明类型。

```typescript
import { computed, ref } from 'vue'

const flag = ref<boolean>(true)
const msg = computed<string | string[]>(() => {
  let result: string | string[] = ''
  if (flag.value) {
    result = ['abc']
  }
  return result
})
```

✅ GOOD: 仅返回一个可变变量类型时，使用类型注解（Type Annotation）直接声明在变量上。

```typescript
import { computed, ref } from 'vue'

const flag = ref<boolean>(true)
const msg = computed(() => {
  let result: string | string[] = ''
  if (flag.value) {
    result = ['abc']
  }
  return result
})
```

## 模板 ref 约定

- template 里写 `ref="xxRef"` 时，必须放在 XML 属性的第一个：
  - ❌ BAD: `<div abc="xxx" def="xxx" ref="xxRef"></div>`
  - ✅ GOOD: `<div ref="xxRef" abc="xxx" def="xxx"></div>`

## Emit 约定

- 变量名统一用 `emit`（全项目一致，防止歧义）
- 在 script 中定义封装函数
- 模板调用封装函数，不 inline `emit()`——封装函数自解释、事件改名只动一处（虽然类型检查 inline 也有，但这不是理由）
- 使用**interface 属性 + 元组语法** `eventName: [arg1: Type, ...]` 而不是函数签名语法 `(e: 'eventName'): void`
- 事件名用 **camelCase**（Vue 自动映射到模板的 kebab-case）

### 示例

```typescript
// types.ts
export interface Emits {
  updateProgress: [value: number]    // 有参数：元组语法
  reset: []                           // 无参数：空元组
}
```

```vue
<script setup lang="ts">
import type { Emits } from './types'

const emit = defineEmits<Emits>()

// 封装函数，提供更好的类型检查和可维护性
function updateProgress(value: number) {
  emit('updateProgress', value)
}

function reset() {
  emit('reset')
}
</script>

<template>
  <!-- ✅ 调用封装函数 -->
  <button @click="updateProgress(50)" />
  <button @click="reset" />

  <!-- ❌ 避免：inline 调用可读性差，事件改名时每个调用点都要改 -->
  <button @click="emit('updateProgress', 50)" />
</template>
```
