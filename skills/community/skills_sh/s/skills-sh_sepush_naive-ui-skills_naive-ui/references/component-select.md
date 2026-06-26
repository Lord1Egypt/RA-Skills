---
name: component-select
description: Select with filterable, multiple, tags, async search, and custom rendering
---

# Select Component

## Basic Usage

```vue
<template>
  <n-select
    v-model:value="selected"
    :options="options"
    placeholder="Select option"
    clearable
  />
</template>

<script setup lang="ts">
import type { SelectOption } from 'naive-ui'

const selected = ref<string | null>(null)

const options: SelectOption[] = [
  { label: 'Option 1', value: '1' },
  { label: 'Option 2', value: '2', disabled: true },
  { label: 'Option 3', value: '3' }
]
</script>
```

## Multiple with Tags

```vue
<template>
  <n-select
    v-model:value="selected"
    multiple
    :options="options"
    :max-tag-count="3"
    :max-tag-placeholder="omitted => `+${omitted.length}`"
    clearable
  />
</template>

<script setup lang="ts">
const selected = ref<string[]>([])
</script>
```

## Async Search

```vue
<template>
  <n-select
    v-model:value="selected"
    filterable
    remote
    clearable
    placeholder="Search user..."
    :options="options"
    :loading="loading"
    @search="handleSearch"
  />
</template>

<script setup lang="ts">
import { debounce } from 'lodash-es'
import type { SelectOption } from 'naive-ui'

interface User {
  id: string
  name: string
  email: string
}

const selected = ref<string | null>(null)
const options = ref<SelectOption[]>([])
const loading = ref(false)

const handleSearch = debounce(async (query: string) => {
  if (!query || query.length < 2) {
    options.value = []
    return
  }

  loading.value = true
  try {
    const users = await searchUsers(query)
    options.value = users.map((u: User) => ({
      label: `${u.name} (${u.email})`,
      value: u.id
    }))
  } finally {
    loading.value = false
  }
}, 300)
</script>
```

## Custom Render

```vue
<template>
  <n-select
    v-model:value="selected"
    :options="options"
    :render-label="renderLabel"
    :render-tag="renderTag"
  />
</template>

<script setup lang="ts">
import { h } from 'vue'
import { NIcon, NTag, NTooltip } from 'naive-ui'

const renderLabel = (option) => {
  return h('div', { style: 'display: flex; align-items: center; gap: 8px' }, [
    h(NIcon, null, { default: () => h(option.icon) }),
    h('span', null, option.label),
    option.description && h('small', { style: 'color: #999' }, option.description)
  ])
}

const renderTag = ({ option, handleClose }) => {
  return h(NTag, {
    type: option.type || 'default',
    closable: true,
    onClose: handleClose
  }, { default: () => option.label })
}
</script>
```

## Grouped Options

```vue
<script setup lang="ts">
const groupedOptions = [
  {
    type: 'group',
    label: 'Group 1',
    key: 'group1',
    children: [
      { label: 'Option 1', value: '1' },
      { label: 'Option 2', value: '2' }
    ]
  },
  {
    type: 'group',
    label: 'Group 2',
    key: 'group2',
    children: [
      { label: 'Option 3', value: '3' }
    ]
  }
]
</script>
```

## Create New Options

```vue
<template>
  <n-select
    v-model:value="selected"
    v-model:options="options"
    filterable
    tag
    multiple
    @create="handleCreate"
  />
</template>

<script setup lang="ts">
const selected = ref([])
const options = ref([
  { label: 'Existing', value: 'existing' }
])

const handleCreate = (label) => {
  const newOption = { label, value: label }
  options.value.push(newOption)
  return newOption
}
</script>
```




## Select Tag + Clearable Does Not Remove Created Options

When using `tag` and `clearable`, clearing the value removes the selection but keeps dynamically created options in the dropdown.

**The Problem:**

```vue
<template>
  <n-select
    v-model:value="selectedValue"
    v-model:options="options"
    filterable
    tag
    clearable
  />
</template>

<script setup lang="ts">
import type { SelectOption } from 'naive-ui'

const selectedValue = ref<string | null>(null)

const options = ref<SelectOption[]>([
  { label: 'Option 1', value: '1' },
  { label: 'Option 2', value: '2' }
])

// User creates new option: "New Option"
// Then clicks clear
// Incorrect: Value is cleared but "New Option" still appears in dropdown
</script>
```

**Solution: Handle clear event to reset options**

```vue
<template>
  <n-select
    v-model:value="selectedValue"
    v-model:options="currentOptions"
    filterable
    tag
    clearable
    @clear="handleClear"
  />
</template>

<script setup lang="ts">
import type { SelectOption } from 'naive-ui'

const selectedValue = ref<string | null>(null)

// Original options (never modified)
const originalOptions: SelectOption[] = [
  { label: 'Option 1', value: '1' },
  { label: 'Option 2', value: '2' }
]

// Working copy
const currentOptions = ref<SelectOption[]>([...originalOptions])

const handleClear = () => {
  // Correct: Reset to original options, removing temporary ones
  currentOptions.value = [...originalOptions]
}
</script>
```

**Alternative: Track and clean temporary options**

```vue
<script setup lang="ts">
import type { SelectOption } from 'naive-ui'

const selectedValue = ref<string | null>(null)
const options = ref<SelectOption[]>([...originalOptions])
const temporaryOptions = ref<Set<string>>(new Set())

const handleCreate = (label: string): SelectOption => {
  const newOption = { label, value: label }
  temporaryOptions.value.add(label)
  return newOption
}

const handleClear = () => {
  // Remove temporary options
  options.value = options.value.filter(
    opt => !temporaryOptions.value.has(opt.label as string)
  )
  temporaryOptions.value.clear()
}
</script>
```

**Alternative: Use controlled mode without v-model:options**

```vue
<template>
  <n-select
    v-model:value="selectedValue"
    :options="allOptions"
    filterable
    tag
    clearable
    @create="handleCreate"
    @clear="handleClear"
  />
</template>

<script setup lang="ts">
const selectedValue = ref<string | null>(null)

const baseOptions = [
  { label: 'Option 1', value: '1' },
  { label: 'Option 2', value: '2' }
]

const createdOptions = ref<SelectOption[]>([])

const allOptions = computed(() => [
  ...baseOptions,
  ...createdOptions.value
])

const handleCreate = (label: string) => {
  const newOption = { label, value: label }
  createdOptions.value.push(newOption)
  return newOption
}

const handleClear = () => {
  createdOptions.value = []
}
</script>
```

**Note:**

This is expected behavior - clear removes the value, not the options. If you want to clean up temporary options, you need to handle it manually.


## Programmatically Close Select Dropdown

Need to close select dropdown after custom action (e.g., selecting in a custom render, or after external trigger).

**The Problem:**

```vue
<template>
  <n-select
    v-model:value="selected"
    :options="options"
    :render-label="renderLabel"
  />
</template>

<script setup lang="ts">
// User asks: "How to programmatically close the dropdown menu?"
// There's no `close()` method exposed directly
</script>
```

**Solution: Use blur() method**

```vue
<template>
  <n-select
    ref="selectRef"
    v-model:value="selected"
    :options="options"
    @update:value="handleValueUpdate"
  />
</template>

<script setup lang="ts">
import type { SelectInst } from 'naive-ui'

const selectRef = ref<SelectInst | null>(null)

const handleValueUpdate = () => {
  // Close dropdown by blurring
  selectRef.value?.blur() // Correct: Works!
}

// Or close programmatically from external action
const closeDropdown = () => {
  selectRef.value?.blur()
}
</script>
```

**Alternative: Control with focus state**

```vue
<template>
  <n-select
    v-model:value="selected"
    :options="options"
    :menu-props="{ onClickoutside: handleClickOutside }"
  />
</template>

<script setup lang="ts">
const handleClickOutside = () => {
  // Handle click outside
}
</script>
```

**Note:**

- `blur()` is the recommended way to close dropdown
- There's no `close()` or `open()` method exposed
- For opening, use `focus()` method

## Related

- [Select Component Guide](../../naive-ui/references/component-select.md)
