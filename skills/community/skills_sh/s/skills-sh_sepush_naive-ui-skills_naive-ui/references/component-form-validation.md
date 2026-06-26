---
name: component-form-validation
description: Naive UI documentation for Form Validation
---

# Form Validation

## Basic Validation

```vue
<template>
  <n-form ref="formRef" :model="formValue" :rules="rules">
    <n-form-item path="name" label="Name">
      <n-input v-model:value="formValue.name" />
    </n-form-item>
    <n-form-item path="email" label="Email">
      <n-input v-model:value="formValue.email" />
    </n-form-item>
    <n-button @click="handleValidate">Submit</n-button>
  </n-form>
</template>

<script setup lang="ts">
import type { FormInst, FormRules } from 'naive-ui'

const formRef = ref<FormInst | null>(null)
const formValue = ref({
  name: '',
  email: ''
})

const rules: FormRules = {
  name: {
    required: true,
    message: 'Please input name',
    trigger: ['blur', 'input']
  },
  email: {
    required: true,
    type: 'email',
    message: 'Please input valid email',
    trigger: ['blur']
  }
}

const handleValidate = async () => {
  try {
    await formRef.value?.validate()
    message.success('Valid!')
  } catch (errors) {
    console.error(errors)
  }
}
</script>
```

## Array Field Validation

```vue
<script setup lang="ts">
const formValue = ref({
  items: [
    { name: '', quantity: 1 },
    { name: '', quantity: 1 }
  ]
})

const rules = {
  items: {
    type: 'array',
    validator(rule, value) {
      if (!Array.isArray(value) || value.length === 0) {
        return new Error('At least one item required')
      }
      for (let i = 0; i < value.length; i++) {
        if (!value[i].name?.trim()) {
          return new Error(`Item ${i + 1} name is required`)
        }
        if (value[i].quantity <= 0) {
          return new Error(`Item ${i + 1} quantity must be > 0`)
        }
      }
      return true
    }
  }
}
</script>
```

## Dynamic Form Validation

```vue
<template>
  <n-form ref="formRef" :model="form" :rules="rules">
    <div v-for="(field, index) in form.fields" :key="index">
      <n-form-item
        :path="`fields[${index}].value`"
        :rule="dynamicRule"
      >
        <n-input v-model:value="field.value" />
        <n-button @click="removeField(index)">Remove</n-button>
      </n-form-item>
    </div>
    <n-button @click="addField">Add Field</n-button>
  </n-form>
</template>

<script setup lang="ts">
const form = ref({
  fields: [{ value: '' }]
})

const dynamicRule = {
  required: true,
  message: 'This field is required'
}

const addField = () => {
  form.value.fields.push({ value: '' })
}

const removeField = (index) => {
  form.value.fields.splice(index, 1)
}
</script>
```

## Nested Form Validation

```vue
<template>
  <n-form :model="form" :rules="rules">
    <n-card title="Basic Info">
      <n-form-item path="basic.name" label="Name">
        <n-input v-model:value="form.basic.name" />
      </n-form-item>
    </n-card>
    <n-card title="Address">
      <n-form-item path="address.street" label="Street">
        <n-input v-model:value="form.address.street" />
      </n-form-item>
    </n-card>
  </n-form>
</template>

<script setup lang="ts">
const form = ref({
  basic: { name: '' },
  address: { street: '' }
})

const rules = {
  basic: {
    name: { required: true }
  },
  address: {
    street: { required: true }
  }
}
</script>
```

## Partial Validation

```ts
// Validate single field
await formRef.value?.validate(['name'])

// Validate multiple specific fields
await formRef.value?.validate(['name', 'email'])

// Validate with callback
await formRef.value?.validate(
  (errors) => {
    if (!errors) {
      console.log('Valid!')
    }
  },
  (rule) => rule.key === 'name'  // Filter rules
)
```

## Async Validation

```ts
const rules = {
  username: {
    required: true,
    validator(rule, value) {
      return new Promise((resolve, reject) => {
        checkUsernameExists(value).then(exists => {
          if (exists) {
            reject(new Error('Username already taken'))
          } else {
            resolve()
          }
        })
      })
    },
    trigger: ['blur']
  }
}
```

## Custom Validation

```ts
const rules = {
  password: {
    required: true,
    validator(rule, value) {
      if (!value) {
        return new Error('Password is required')
      }
      if (value.length < 8) {
        return new Error('Password must be at least 8 characters')
      }
      if (!/[A-Z]/.test(value)) {
        return new Error('Password must contain uppercase letter')
      }
      return true
    }
  },
  confirmPassword: {
    required: true,
    validator(rule, value) {
      if (value !== formValue.value.password) {
        return new Error('Passwords do not match')
      }
      return true
    }
  }
}
```


