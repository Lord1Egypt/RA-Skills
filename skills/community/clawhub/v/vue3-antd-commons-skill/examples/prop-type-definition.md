# Vue3组件Prop类型定义示例

## 1. 基本Prop类型定义

```typescript
// 1. 基本Prop类型定义
interface ButtonProps {
  // 必选属性
  type: 'primary' | 'default' | 'dashed' | 'link' | 'text'
  
  // 可选属性
  size?: 'small' | 'middle' | 'large'
  
  // 布尔属性
  disabled?: boolean
  loading?: boolean
  ghost?: boolean
  
  // 字符串属性
  href?: string
  target?: '_blank' | '_self' | '_parent' | '_top'
  
  // 数字属性
  duration?: number
  
  // 对象属性
  style?: CSSProperties
  
  // 数组属性
  className?: string | string[]
  
  // 自定义类型属性
  icon?: any
}
```

## 2. 使用withDefaults设置默认值

```typescript
// 2. 使用withDefaults设置默认值
const props = withDefaults(defineProps<ButtonProps>(), {
  type: 'default',
  size: 'middle',
  disabled: false,
  loading: false,
  ghost: false,
  duration: 0.3
})
```

## 3. 复杂对象类型Prop

```typescript
// 3. 复杂对象类型Prop
interface TableProps<T = any> {
  columns: Column<T>[]
  dataSource: T[]
  pagination?: PaginationConfig | false
  rowKey?: string | ((record: T) => string)
  bordered?: boolean
  loading?: boolean
  scroll?: { x?: number | string; y?: number | string }
}

interface Column<T = any> {
  title: string
  dataIndex: string
  key?: string
  render?: (text: any, record: T, index: number) => VNode | string
  width?: number | string
  align?: 'left' | 'center' | 'right'
}
```

## 4. 使用泛型Prop

```typescript
// 4. 使用泛型Prop
const tableProps = defineProps<{
  data: <T>(items: T[]) => T[]
  config: { name: string; value: number }
}>()
```

## 5. 事件类型定义

```typescript
// 5. 事件类型定义
interface ButtonEmits {
  (e: 'click', event: MouseEvent): void
  (e: 'hover', event: MouseEvent): void
  (e: 'focus', event: FocusEvent): void
  (e: 'blur', event: FocusEvent): void
}

const emit = defineEmits<ButtonEmits>()

// 使用示例
const handleClick = (event: MouseEvent) => {
  emit('click', event)
}
```

## 6. 在组件中使用

```vue
// 6. 在组件中使用
<template>
  <button
    :type="type"
    :size="size"
    :disabled="disabled"
    :loading="loading"
    :ghost="ghost"
    :href="href"
    :target="target"
    :style="style"
    :class="className"
    @click="handleClick"
  >
    <slot>{{ type }}</slot>
  </button>
</template>

<script setup lang="ts">
import { defineProps, withDefaults, defineEmits } from 'vue'

// 此处省略Props和Emits的定义（见上方）

const props = withDefaults(defineProps<ButtonProps>(), {
  type: 'default',
  size: 'middle',
  disabled: false,
  loading: false,
  ghost: false,
  duration: 0.3
})

const emit = defineEmits<ButtonEmits>()

const handleClick = (event: MouseEvent) => {
  emit('click', event)
}
</script>
```