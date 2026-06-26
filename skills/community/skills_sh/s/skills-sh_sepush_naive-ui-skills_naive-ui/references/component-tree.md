---
name: component-tree
description: Tree and TreeSelect with async loading, checkable, controlled state, and large dataset handling
---

# Tree & TreeSelect

## Async Loading Tree

```vue
<template>
  <n-tree
    :data="treeData"
    :load-data="handleLoadData"
    remote
    checkable
    selectable
    @update:checked-keys="handleCheck"
  />
</template>

<script setup lang="ts">
import type { TreeOption } from 'naive-ui'

const treeData = ref<TreeOption[]>([
  {
    label: 'Parent',
    key: 'parent',
    isLeaf: false
  }
])

const handleLoadData = async (node: TreeOption) => {
  const children = await fetchChildren(node.key as string)
  node.children = children
}

const handleCheck = (keys: Array<string | number>) => {
  console.log('Checked:', keys)
}
</script>
```

## Controlled Tree

```vue
<template>
  <n-space>
    <n-button @click="expandAll">Expand All</n-button>
    <n-button @click="collapseAll">Collapse All</n-button>
    <n-button @click="checkAll">Check All</n-button>
  </n-space>

  <n-tree
    :data="data"
    checkable
    :expanded-keys="expandedKeys"
    :checked-keys="checkedKeys"
    :selected-keys="selectedKeys"
    @update:expanded-keys="keys => expandedKeys = keys"
    @update:checked-keys="keys => checkedKeys = keys"
  />
</template>

<script setup lang="ts">
import type { TreeOption } from 'naive-ui'

const expandedKeys = ref<Array<string | number>>([])
const checkedKeys = ref<Array<string | number>>([])
const selectedKeys = ref<Array<string | number>>([])

const data = ref<TreeOption[]>([])

const expandAll = () => {
  expandedKeys.value = getAllKeys(data.value)
}

const collapseAll = () => {
  expandedKeys.value = []
}

const getAllKeys = (nodes: TreeOption[]): Array<string | number> => {
  const keys: Array<string | number> = []
  const traverse = (items: TreeOption[]) => {
    items.forEach(item => {
      keys.push(item.key as string | number)
      if (item.children) {
        traverse(item.children as TreeOption[])
      }
    })
  }
  traverse(nodes)
  return keys
}
</script>
```

## TreeSelect

```vue
<template>
  <n-tree-select
    v-model:value="selected"
    :options="options"
    checkable
    clearable
    :expand-on-click="false"
  />
</template>

<script setup lang="ts">
import type { TreeOption } from 'naive-ui'

const selected = ref<string | null>(null)

const options: TreeOption[] = [
  {
    label: 'Parent',
    key: 'parent',
    children: [
      { label: 'Child 1', key: 'child1' },
      { label: 'Child 2', key: 'child2' }
    ]
  }
]
</script>
```

## Virtual Scroll Tree

```vue
<template>
  <n-tree
    :data="largeData"
    virtual-scroll
    :height="400"
    :item-size="30"
    checkable
  />
</template>
```


