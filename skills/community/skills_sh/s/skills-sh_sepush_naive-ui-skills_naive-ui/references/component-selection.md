---
name: component-selection
description: Selection components including Radio, Checkbox, Switch, Slider, and Rate
---

# Selection Components

Components for selecting options and toggling states.

## Radio

### Basic Usage

```vue
<script setup lang="ts">
import { ref } from 'vue'

const value = ref('apple')
</script>

<template>
  <n-radio-group v-model:value="value" name="fruit">
    <n-space>
      <n-radio value="apple">Apple</n-radio>
      <n-radio value="banana">Banana</n-radio>
      <n-radio value="orange">Orange</n-radio>
    </n-space>
  </n-radio-group>
</template>
```

### Radio Button

```vue
<template>
  <n-radio-group v-model:value="value">
    <n-radio-button value="daily">Daily</n-radio-button>
    <n-radio-button value="weekly">Weekly</n-radio-button>
    <n-radio-button value="monthly">Monthly</n-radio-button>
  </n-radio-group>
</template>
```

### Radio Group Options

```vue
<script setup lang="ts">
import type { RadioGroupProps } from 'naive-ui'

const options: RadioGroupProps['options'] = [
  { value: 'beijing', label: 'Beijing' },
  { value: 'shanghai', label: 'Shanghai' },
  { value: 'guangzhou', label: 'Guangzhou', disabled: true }
]

const value = ref('beijing')
</script>

<template>
  <n-radio-group v-model:value="value" :options="options" />
</template>
```

### Sizes

```vue
<template>
  <n-space vertical>
    <n-radio-group v-model:value="value" size="small">
      <n-radio-button value="a">Small</n-radio-button>
      <n-radio-button value="b">Small</n-radio-button>
    </n-radio-group>

    <n-radio-group v-model:value="value" size="medium">
      <n-radio-button value="a">Medium</n-radio-button>
      <n-radio-button value="b">Medium</n-radio-button>
    </n-radio-group>

    <n-radio-group v-model:value="value" size="large">
      <n-radio-button value="a">Large</n-radio-button>
      <n-radio-button value="b">Large</n-radio-button>
    </n-radio-group>
  </n-space>
</template>
```

## Checkbox

### Basic Usage

```vue
<script setup lang="ts">
const checked = ref(false)
</script>

<template>
  <n-checkbox v-model:checked="checked">
    I agree to the terms
  </n-checkbox>
</template>
```

### Checkbox Group

```vue
<script setup lang="ts">
const value = ref<string[]>(['apple'])

const options = [
  { value: 'apple', label: 'Apple' },
  { value: 'banana', label: 'Banana' },
  { value: 'orange', label: 'Orange' }
]
</script>

<template>
  <n-checkbox-group v-model:value="value" :options="options" />
</template>
```

### Indeterminate State

```vue
<script setup lang="ts">
const allChecked = ref(false)
const indeterminate = ref(false)
const value = ref<string[]>([])

const options = ['Apple', 'Banana', 'Orange']

const handleUpdateAll = (checked: boolean) => {
  value.value = checked ? [...options] : []
  indeterminate.value = false
}

watch(value, (val) => {
  if (val.length === 0) {
    allChecked.value = false
    indeterminate.value = false
  } else if (val.length === options.length) {
    allChecked.value = true
    indeterminate.value = false
  } else {
    indeterminate.value = true
  }
})
</script>

<template>
  <n-space vertical>
    <n-checkbox
      v-model:checked="allChecked"
      :indeterminate="indeterminate"
      @update:checked="handleUpdateAll"
    >
      Select All
    </n-checkbox>
    <n-divider />
    <n-checkbox-group v-model:value="value">
      <n-space>
        <n-checkbox v-for="opt in options" :key="opt" :value="opt">
          {{ opt }}
        </n-checkbox>
      </n-space>
    </n-checkbox-group>
  </n-space>
</template>
```

### Grid Layout

```vue
<template>
  <n-checkbox-group v-model:value="value">
    <n-grid :y-gap="8" :cols="2">
      <n-gi v-for="i in 6" :key="i">
        <n-checkbox :value="String(i)">
          Option {{ i }}
        </n-checkbox>
      </n-gi>
    </n-grid>
  </n-checkbox-group>
</template>
```

## Switch

### Basic Usage

```vue
<script setup lang="ts">
const active = ref(false)
</script>

<template>
  <n-switch v-model:value="active" />
</template>
```

### With Text/Round

```vue
<template>
  <n-space>
    <n-switch v-model:value="value" round />
    <n-switch v-model:value="value" :round="false" />
  </n-space>
</template>
```

### Custom Content

```vue
<template>
  <n-switch v-model:value="value" size="large">
    <template #checked>ON</template>
    <template #unchecked>OFF</template>
  </n-switch>
</template>
```

### Loading State

```vue
<template>
  <n-switch v-model:value="value" :loading="loading" />
</template>
```

### Value Mapping

```vue
<script setup lang="ts">
// Map checked/unchecked to custom values
const value = ref('active')
</script>

<template>
  <n-switch
    v-model:value="value"
    checked-value="active"
    unchecked-value="inactive"
  />
</template>
```

## Slider

### Basic Usage

```vue
<script setup lang="ts">
const value = ref(50)
</script>

<template>
  <n-slider v-model:value="value" :step="10" />
</template>
```

### Range Slider

```vue
<script setup lang="ts">
const range = ref([20, 80])
</script>

<template>
  <n-slider v-model:value="range" range :step="1" />
</template>
```

### Marks

```vue
<script setup lang="ts">
const marks = {
  0: '0°C',
  20: '20°C',
  40: '40°C',
  60: '60°C',
  80: '80°C',
  100: '100°C'
}
</script>

<template>
  <n-slider v-model:value="value" :marks="marks" />
</template>
```

### Vertical

```vue
<template>
  <n-slider v-model:value="value" vertical style="height: 200px" />
</template>
```

### Disabled/Tooltip

```vue
<template>
  <n-slider v-model:value="value" disabled />
  <n-slider v-model:value="value" :tooltip="false" />
</template>
```

## Rate

### Basic Usage

```vue
<script setup lang="ts">
const value = ref(3)
</script>

<template>
  <n-rate v-model:value="value" />
</template>
```

### Custom Icon

```vue
<script setup lang="ts">
import { Heart } from '@vicons/ionicons5'
</script>

<template>
  <n-rate>
    <n-icon :component="Heart" />
  </n-rate>
</template>
```

### Half Star

```vue
<template>
  <n-rate v-model:value="value" allow-half />
</template>
```

### Readonly

```vue
<template>
  <n-rate readonly :default-value="4" />
</template>
```

### Custom Count

```vue
<template>
  <n-rate v-model:value="value" :count="10" />
</template>
```

### Size & Color

```vue
<template>
  <n-space vertical>
    <n-rate size="small" />
    <n-rate size="medium" />
    <n-rate size="large" />
    <n-rate color="#ffb347" />
  </n-space>
</template>
```

## Color Picker

```vue
<script setup lang="ts">
const color = ref('#2080F0FF')
</script>

<template>
  <n-color-picker v-model:value="color" />
</template>
```

### Alpha Channel

```vue
<template>
  <n-color-picker v-model:value="color" :show-alpha="false" />
</template>
```

### Modes

```vue
<template>
  <n-color-picker
    v-model:value="color"
    :modes="['hex', 'rgb', 'hsl']"
  />
</template>
```

## Transfer

> **Warning:** The `n-legacy-transfer` component is deprecated. It won't receive new features and will be removed in the next major version. It's recommended to use the new `n-transfer` component.

## Common Patterns

### Settings Form

```vue
<template>
  <n-form>
    <n-form-item label="Notifications">
      <n-switch v-model:value="settings.notifications" />
    </n-form-item>

    <n-form-item label="Theme">
      <n-radio-group v-model:value="settings.theme">
        <n-radio-button value="light">Light</n-radio-button>
        <n-radio-button value="dark">Dark</n-radio-button>
        <n-radio-button value="auto">Auto</n-radio-button>
      </n-radio-group>
    </n-form-item>

    <n-form-item label="Languages">
      <n-checkbox-group v-model:value="settings.languages">
        <n-space>
          <n-checkbox value="en">English</n-checkbox>
          <n-checkbox value="zh">Chinese</n-checkbox>
          <n-checkbox value="ja">Japanese</n-checkbox>
        </n-space>
      </n-checkbox-group>
    </n-form-item>

    <n-form-item label="Volume">
      <n-slider v-model:value="settings.volume" :step="1" />
    </n-form-item>
  </n-form>
</template>
```

### Product Rating

```vue
<template>
  <n-card title="Product Reviews">
    <n-space align="center">
      <span style="font-size: 48px; font-weight: bold">4.5</span>
      <n-space vertical>
        <n-rate readonly allow-half :default-value="4.5" />
        <n-text depth="3">Based on 128 reviews</n-text>
      </n-space>
    </n-space>

    <n-divider />

    <n-space vertical>
      <n-slider
        v-model:value="ratingFilter"
        range
        :marks="{1: '1★', 3: '3★', 5: '5★'}"
        :min="1"
        :max="5"
        :step="1"
      />
    </n-space>
  </n-card>
</template>
```

## Key Types

```ts
import type {
  RadioProps,
  RadioGroupProps,
  CheckboxProps,
  CheckboxGroupProps,
  SwitchProps,
  SliderProps,
  RateProps,
  ColorPickerProps
} from 'naive-ui'
```


