---
name: component-virtual-list
description: Virtual scrolling patterns for large data sets using VirtualList component
---

# Virtual List

Use `n-virtual-list` for rendering large lists efficiently by only rendering visible items.

## Basic Usage

```vue
<script setup lang="ts">
import { ref } from 'v ue'

interface Item {
  key: number
  value: string
}

const items = ref<Item[]>(
  Array.from({ length: 10000 }, (_, i) => ({
    key: i,
    value: `Item ${i}`
  }))
)
</script>

<template>
  <n-virtual-list
    :items="items"
    :item-size="42"
    style="max-height: 400px"
  >
    <template #default="{ item }">
      <div class="list-item">
        {{ item.value }}
      </div>
    </template>
  </n-virtual-list>
</template>

<style>
.list-item {
  height: 42px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  border-bottom: 1px solid #eee;
}
</style>
```

## With DataTable

```vue
<template>
  <n-data-table
    :columns="columns"
    :data="data"
    :scroll-x="1000"
    virtual-scroll
    :max-height="400"
  />
</template>
```

## With Select

```vue
<template>
  <n-select
    v-model:value="selected"
    :options="options"
    :virtual-scroll="true"
    :fallback-option="false"
  />
</template>
```

## With Tree

```vue
<template>
  <n-tree
    :data="treeData"
    virtual-scroll
    :height="400"
    :item-size="32"
  />
</template>
```

## Dynamic Item Height

```vue
<script setup lang="ts">
const getItemHeight = (item: Item, index: number) => {
  // Return different heights based on content
  return item.isExpanded ? 80 : 40
}
</script>

<template>
  <n-virtual-list
    :items="items"
    :item-size="getItemHeight"
    style="max-height: 400px"
  >
    <template #default="{ item, index }">
      <div :style="{ height: getItemHeight(item, index) + 'px' }">
        {{ item.value }}
      </div>
    </template>
  </n-virtual-list>
</template>
```

## Key Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `items` | `Array` | `[]` | List of items to render |
| `item-size` | `number \| Function` | `0` | Height of each item (px) or function |
| `key-field` | `string` | `'key'` | Unique key field in items |
| `visible-items` | `number` | - | Number of visible items (auto-calculated if not set) |


