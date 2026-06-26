---
number: 14154
title: 组件二封时原组件事件应该如何定义可以兼顾类型和便捷性？
category: Help/Questions
created: 2025-12-01
url: "https://github.com/orgs/vuejs/discussions/14154"
upvotes: 1
comments: 1
answered: true
---

# 组件二封时原组件事件应该如何定义可以兼顾类型和便捷性？

```html
<script setup lang="ts">
import type { InputPropsPublic, InputEmits } from 'element-plus'

defineProps<{} & InputPropsPublic>()

// 使用 defineEmits 后，事件会跟 props 一样被组件自身消费掉，无法在 $attrs 里面获取，
// 这里除了 emits 一个一个重新抛出外还有别的比较便捷吗？
const emits = defineEmits<InputEmits>()
</script>

<template>
  <ElInput v-bind="{ ...$props, ...$attrs }" />
</template>
```

---

## Accepted Answer

覆蓋原本事件：

```vue
<script lang="ts" setup>
import type { ComponentProps } from 'vue-component-type-helpers';
import { XTextField } from '@x/ui'; 

type TextFieldProps = ComponentProps<typeof XTextField>;

interface Props extends /* @vue-ignore */ Omit<TextFieldProps, 'onClick'> { // Exclude a specific event from a component.
  // my props
}

defineOptions({
  inheritAttrs: false,
});

const props = defineProps<Props>();
const emit = defineEmits<(evt: 'click', payload: MouseEvent) => void>(); // Emit an event with the same name as the original event, but change the operation to your own.

function onMyClick() {
  // You can now modify the original event; it will still use the same name as the original.
  emit('click', /* ... */);
}
</script>

<template>
  <XTextField v-bind="$attrs" @click="onMyClick()" /> 
</template>
```