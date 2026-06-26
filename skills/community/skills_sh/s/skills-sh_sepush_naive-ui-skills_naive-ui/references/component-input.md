---
name: component-input
description: Input and InputNumber component usage, validation triggers, and precision handling
---

# Input & InputNumber

Text input components with various features including validation, formatting, and number handling.

## Input

### Basic Usage

```vue
<script setup lang="ts">
import { ref } from 'vue'

const value = ref('')
</script>

<template>
  <n-input v-model:value="value" placeholder="Enter text" />
</template>
```

### Input Types

```vue
<template>
  <n-space vertical>
    <n-input type="text" placeholder="Text input" />
    <n-input type="password" placeholder="Password input" show-password-on="mousedown" />
    <n-input type="textarea" placeholder="Textarea" :rows="3" />
  </n-space>
</template>
```

### Input with Icons

```vue
<script setup lang="ts">
import { Search, Person } from '@vicons/ionicons5'
</script>

<template>
  <n-space vertical>
    <n-input placeholder="Search">
      <template #prefix>
        <n-icon :component="Search" />
      </template>
    </n-input>
    <n-input placeholder="Username">
      <template #suffix>
        <n-icon :component="Person" />
      </template>
    </n-input>
  </n-space>
</template>
```

### Clearable Input

```vue
<template>
  <n-input v-model:value="value" clearable placeholder="Can be cleared" />
</template>
```

### Input Sizes

```vue
<template>
  <n-space vertical>
    <n-input size="small" placeholder="Small" />
    <n-input size="medium" placeholder="Medium (default)" />
    <n-input size="large" placeholder="Large" />
  </n-space>
</template>
```

### Character Count

```vue
<template>
  <n-input
    v-model:value="value"
    type="textarea"
    maxlength="100"
    show-count
    clearable
  />
</template>
```

### Autosizing Textarea

```vue
<template>
  <n-input
    v-model:value="value"
    type="textarea"
    :autosize="{
      minRows: 3,
      maxRows: 5
    }"
  />
</template>
```

## InputNumber

### Basic Usage

```vue
<script setup lang="ts">
import { ref } from 'vue'

const value = ref(0)
</script>

<template>
  <n-input-number v-model:value="value" />
</template>
```

### Min / Max

```vue
<template>
  <n-input-number v-model:value="value" :min="0" :max="100" />
</template>
```

### Step

```vue
<template>
  <n-input-number v-model:value="value" :step="10" />
</template>
```

### Precision

```vue
<template>
  
  <n-input-number v-model:value="value" :precision="2" />
</template>
```

### Custom Formatter

```vue
<script setup lang="ts">
const value = ref(1000)

const format = (value: number | null): string => {
  if (value === null) return ''
  return `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const parse = (input: string): number | null => {
  const nums = input.replace(/[^\d.]/g, '').trim()
  return nums ? Number(nums) : null
}
</script>

<template>
  <n-input-number
    v-model:value="value"
    :format="format"
    :parse="parse"
    :min="0"
    :precision="2"
  />
</template>
```

### Button Placement

```vue
<template>
  <n-space>
    <n-input-number v-model:value="value" button-placement="both" />
    <n-input-number v-model:value="value" button-placement="right" />
  </n-space>
</template>
```

## Form Validation Patterns

### Basic Validation

```vue
<script setup lang="ts">
import type { FormInst, FormRules } from 'naive-ui'

const formRef = ref<FormInst | null>(null)
const formValue = ref({
  name: '',
  age: null as number | null
})

const rules: FormRules = {
  name: {
    required: true,
    message: 'Please input name',
    trigger: ['blur', 'input']
  },
  age: {
    type: 'number',
    required: true,
    message: 'Please input age',
    trigger: ['blur', 'change']
  }
}

const handleValidate = () => {
  formRef.value?.validate((errors) => {
    if (!errors) {
      console.log('Valid')
    }
  })
}
</script>

<template>
  <n-form ref="formRef" :model="formValue" :rules="rules">
    <n-form-item label="Name" path="name">
      <n-input v-model:value="formValue.name" />
    </n-form-item>
    <n-form-item label="Age" path="age">
      <n-input-number v-model:value="formValue.age" />
    </n-form-item>
  </n-form>
</template>
```

### Warning: Important: InputNumber with Precision/Format

When using `precision` or `format` props, `trigger: ['input']` may not work correctly.

**Problem:**
```vue

<n-form-item path="amount" :rule="{ trigger: ['input'] }">
  <n-input-number v-model:value="amount" :precision="2" />
</n-form-item>
```

**Solution:**
```vue
<script setup lang="ts">
const rules: FormRules = {
  amount: {
    required: true,
    type: 'number',
    // Use blur trigger or manual validation
    trigger: ['blur']
  }
}
</script>

<template>
  <n-form-item path="amount" :rule="rules.amount">
    <n-input-number v-model:value="amount" :precision="2" />
  </n-form-item>
  <n-button @click="validate">Validate</n-button>
</template>
```

### Async Validation

```vue
<script setup lang="ts">
const checkUsername = async (rule: FormItemRule, value: string) => {
  if (!value) return new Error('Please input username')

  // Simulate API call
  const exists = await api.checkUsernameExists(value)
  if (exists) {
    return new Error('Username already exists')
  }
  return true
}

const rules: FormRules = {
  username: {
    required: true,
    validator: checkUsername,
    trigger: 'blur'
  }
}
</script>
```

### Dynamic Validation

```vue
<script setup lang="ts">
const formValue = ref({
  type: 'individual' as 'individual' | 'company',
  name: '',
  companyCode: ''
})

const rules = computed<FormRules>(() => ({
  name: {
    required: true,
    message: 'Name is required'
  },
  companyCode: {
    required: formValue.value.type === 'company',
    message: 'Company code is required for companies'
  }
}))
</script>
```

## Common Patterns

### Search Input with Debounce

```vue
<script setup lang="ts">
import { ref, watch } from 'vue'
import { debounce } from 'lodash-es'

const search = ref('')
const results = ref([])

const searchApi = debounce(async (query: string) => {
  if (!query) {
    results.value = []
    return
  }
  results.value = await api.search(query)
}, 300)

watch(search, searchApi)
</script>

<template>
  <n-input
    v-model:value="search"
    placeholder="Search..."
    clearable
  >
    <template #prefix>
      <n-icon :component="Search" />
    </template>
  </n-input>
</template>
```

### Number Range

```vue
<script setup lang="ts">
const min = ref<number | null>(null)
const max = ref<number | null>(null)

const validateRange = () => {
  if (min.value !== null && max.value !== null && min.value > max.value) {
    message.error('Min cannot be greater than max')
  }
}
</script>

<template>
  <n-space>
    <n-input-number
      v-model:value="min"
      placeholder="Min"
      @blur="validateRange"
    />
    <span>-</span>
    <n-input-number
      v-model:value="max"
      placeholder="Max"
      @blur="validateRange"
    />
  </n-space>
</template>
```

### Controlled Input

```vue
<script setup lang="ts">
const value = ref('')

const handleUpdate = (val: string) => {
  // Filter or transform input
  value.value = val.replace(/[^\d]/g, '') // Only allow digits
}
</script>

<template>
  <n-input
    :value="value"
    @update:value="handleUpdate"
    placeholder="Numbers only"
  />
</template>
```

## Key Types

```ts
import type {
  InputProps,
  InputInst,
  InputNumberProps,
  InputNumberInst
} from 'naive-ui'
```


