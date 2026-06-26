---
name: component-form
description: Form layouts, validation patterns, dynamic forms, and nested forms
---

# Form Component

> **💡 Important**: If you need to set `required` for a form item whose value is of type `number` (like when using `n-input-number`), you **MUST** specify `type: 'number'` in the rule object. Otherwise, the validation will fail or trigger incorrectly.

## Inline Form

```vue
<template>
  <n-form inline :model="form" :rules="rules">
    <n-form-item path="name" label="Name">
      <n-input v-model:value="form.name" />
    </n-form-item>
    <n-form-item path="status" label="Status">
      <n-select v-model:value="form.status" :options="statusOptions" />
    </n-form-item>
    <n-form-item>
      <n-button type="primary" @click="search">Search</n-button>
    </n-form-item>
  </n-form>
</template>
```

## Grid Layout Form

```vue
<template>
  <n-form :model="form" :rules="rules">
    <n-grid :cols="2" :x-gap="24">
      <n-form-item-gi path="firstName" label="First Name">
        <n-input v-model:value="form.firstName" />
      </n-form-item-gi>
      <n-form-item-gi path="lastName" label="Last Name">
        <n-input v-model:value="form.lastName" />
      </n-form-item-gi>
    </n-grid>
  </n-form>
</template>
```

## Dynamic Form Fields

```vue
<template>
  <n-form ref="formRef" :model="form" :rules="rules">
    <n-divider>Items</n-divider>

    <div v-for="(item, index) in form.items" :key="index">
      <n-space align="start">
        <n-form-item
          :path="`items[${index}].name`"
          :rule="{ required: true, message: 'Required' }"
        >
          <n-input v-model:value="item.name" placeholder="Item name" />
        </n-form-item>

        <n-form-item
          :path="`items[${index}].quantity`"
          :rule="{ type: 'number', min: 1 }"
        >
          <n-input-number v-model:value="item.quantity" :min="1" />
        </n-form-item>

        <n-button
          circle
          type="error"
          @click="removeItem(index)"
          :disabled="form.items.length <= 1"
        >
          <n-icon><close-icon /></n-icon>
        </n-button>
      </n-space>
    </div>

    <n-button dashed block @click="addItem">
      + Add Item
    </n-button>
  </n-form>
</template>

<script setup lang="ts">
interface FormItem {
  name: string
  quantity: number
}

interface Form {
  items: FormItem[]
}

const form = ref<Form>({
  items: [{ name: '', quantity: 1 }]
})

const addItem = () => {
  form.value.items.push({ name: '', quantity: 1 })
}

const removeItem = (index: number) => {
  form.value.items.splice(index, 1)
}
</script>
```

## Form with Async Submit

```vue
<template>
  <n-form ref="formRef" :model="form" :rules="rules">
    <n-form-item path="name" label="Name">
      <n-input v-model:value="form.name" />
    </n-form-item>
    <n-form-item>
      <n-button
        type="primary"
        :loading="submitting"
        @click="handleSubmit"
      >
        Submit
      </n-button>
    </n-form-item>
  </n-form>
</template>

<script setup lang="ts">
import type { FormInst, FormRules } from 'naive-ui'

const formRef = ref<FormInst | null>(null)
const submitting = ref(false)
const form = ref({ name: '' })

const rules: FormRules = {
  name: { required: true, message: 'Name is required' }
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    submitting.value = true
    await submitApi(form.value)
    message.success('Success')
  } catch (e) {
    // Handle error
  } finally {
    submitting.value = false
  }
}
</script>
const form = ref({ name: '' })

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    submitting.value = true
    await submitApi(form.value)
    message.success('Success')
  } catch (e) {
    // Handle error
  } finally {
    submitting.value = false
  }
}
</script>
```


