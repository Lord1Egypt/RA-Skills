---
name: component-datepicker
description: DatePicker with ranges, shortcuts, formatting, and timezone handling
---

# DatePicker

## Basic Date Picker

```vue
<template>
  <n-date-picker v-model:value="timestamp" type="date" />
</template>

<script setup lang="ts">
const timestamp = ref<number>(Date.now())
</script>
```

## Date Range

```vue
<template>
  <n-date-picker
    v-model:value="range"
    type="datetimerange"
    clearable
    :shortcuts="shortcuts"
  />
</template>

<script setup lang="ts">
import type { Shortcuts } from 'naive-ui/es/date-picker/src/interface'

const range = ref<[number, number]>([Date.now(), Date.now() + 86400000])

const shortcuts: Shortcuts = {
  'Today': () => [Date.now(), Date.now()],
  'This Week': () => {
    const now = new Date()
    const start = new Date(now.getFullYear(), now.getMonth(), now.getDate() - now.getDay())
    return [start.getTime(), Date.now()]
  },
  'This Month': () => {
    const now = new Date()
    const start = new Date(now.getFullYear(), now.getMonth(), 1)
    return [start.getTime(), Date.now()]
  }
}
</script>
```

## Formatted Value

```vue
<template>
  <n-date-picker
    v-model:formatted-value="dateString"
    value-format="yyyy-MM-dd"
    type="date"
    clearable
  />
</template>

<script setup lang="ts">
// Use null, not empty string
const dateString = ref<string | null>(null)
</script>
```

## Disabled Dates

```vue
<template>
  <n-date-picker
    v-model:value="date"
    :is-date-disabled="isDateDisabled"
    :is-time-disabled="isTimeDisabled"
  />
</template>

<script setup lang="ts">
import type { IsDateDisabled, IsTimeDisabled } from 'naive-ui/es/date-picker/src/interface'

const date = ref<number>(Date.now())

const isDateDisabled: IsDateDisabled = (timestamp: number) => {
  // Disable future dates
  return timestamp > Date.now()
}

const isTimeDisabled: IsTimeDisabled = (ts: number, type: 'hour' | 'minute' | 'second', range: 'start' | 'end') => {
  // Disable times before 9am and after 6pm
  const hour = new Date(ts).getHours()
  return hour < 9 || hour > 18
}
</script>
```




## DatePicker Empty String Value Throws Error

Setting `formatted-value` to empty string causes errors. DatePicker expects `null` for empty values, not empty string.

**Incorrect (throws error):**

```vue
<template>
  <n-date-picker
    v-model:formatted-value="dateValue"
    value-format="yyyy-MM-dd"
  />
</template>

<script setup lang="ts">
// Incorrect: Empty string causes error
const dateValue = ref('')
</script>
```

**Correct (use null):**

```vue
<template>
  <n-date-picker
    v-model:formatted-value="dateValue"
    value-format="yyyy-MM-dd"
    clearable
  />
</template>

<script setup lang="ts">
// Correct: Use null for empty
const dateValue = ref<string | null>(null)
</script>
```

**Why:**

DatePicker internally parses the formatted value. An empty string `''` fails parsing, while `null` is explicitly handled as "no value".

**Clearing the value:**

```vue
<script setup lang="ts">
const dateValue = ref<string | null>('2024-01-01')

// Clear properly
const clearDate = () => {
  dateValue.value = null // Correct: Correct
  // dateValue.value = '' // Incorrect: Wrong - causes error
}
</script>
```

**TypeScript Best Practice:**

```ts
// Use union type to enforce correct usage
const dateValue = ref<string | null>(null)

// Or with range
const dateRange = ref<[string, string] | null>(null)
```

**Alternative (use value instead of formatted-value):**

```vue
<template>
  <n-date-picker
    v-model:value="timestamp"
    type="date"
    clearable
  />
</template>

<script setup lang="ts">
// Timestamp can be null
const timestamp = ref<number | null>(null)
</script>
```
