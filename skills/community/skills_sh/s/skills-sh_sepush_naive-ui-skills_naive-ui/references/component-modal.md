---
name: component-modal
description: Modal and Dialog with form validation, draggable, focus management, and async close
---

# Modal & Dialog

## Basic Modal

> **Prerequisite:** If you want to create a modal using `useModal`, you need to wrap the calling component inside `n-modal-provider` and use `useModal` to get the API.

```vue
<template>
  <n-button @click="show = true">Open</n-button>
  <n-modal v-model:show="show" title="Modal" preset="card">
    Content
  </n-modal>
</template>

<script setup lang="ts">
const show = ref(false)
</script>
```

## Form Modal

```vue
<template>
  <n-button @click="openModal">Add User</n-button>

  <n-modal
    v-model:show="showModal"
    preset="card"
    title="Add User"
    style="width: 500px"
    :mask-closable="false"
    @after-leave="resetForm"
  >
    <n-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-placement="left"
      label-width="80"
    >
      <n-form-item path="name" label="Name">
        <n-input v-model:value="form.name" />
      </n-form-item>
      <n-form-item path="email" label="Email">
        <n-input v-model:value="form.email" />
      </n-form-item>
    </n-form>

    <template #footer>
      <n-space justify="end">
        <n-button @click="showModal = false">Cancel</n-button>
        <n-button
          type="primary"
          :loading="submitting"
          @click="handleSubmit"
        >
          Submit
        </n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import type { FormInst, FormRules } from 'naive-ui'

const showModal = ref(false)
const submitting = ref(false)
const formRef = ref<FormInst | null>(null)
const form = ref({
  name: '',
  email: ''
})

const rules: FormRules = {
  name: { required: true, message: 'Name is required' },
  email: { required: true, type: 'email', message: 'Invalid email' }
}

const openModal = () => {
  showModal.value = true
}

const resetForm = () => {
  form.value = { name: '', email: '' }
  formRef.value?.restoreValidation()
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    submitting.value = true
    await createUser(form.value)
    message.success('Created')
    showModal.value = false
  } finally {
    submitting.value = false
  }
}
</script>
```

## Dialog (Preset)

> **Prerequisite:** If you want to use dialog, you need to wrap the calling component inside `n-dialog-provider` and use `useDialog` to get the API.

```vue
<script setup lang="ts">
const dialog = useDialog()

const confirmDelete = () => {
  dialog.warning({
    title: 'Confirm Delete',
    content: 'Are you sure you want to delete this?',
    positiveText: 'Delete',
    negativeText: 'Cancel',
    onPositiveClick: async () => {
      await deleteItem()
      message.success('Deleted')
    }
  })
}

const showError = () => {
  dialog.error({
    title: 'Error',
    content: 'Something went wrong',
    positiveText: 'OK'
  })
}
</script>
```

## Draggable Modal

```vue
<template>
  <n-modal
    v-model:show="show"
    preset="card"
    title="Draggable"
    draggable
  >
    Content that can be dragged by the header
  </n-modal>
</template>
```
