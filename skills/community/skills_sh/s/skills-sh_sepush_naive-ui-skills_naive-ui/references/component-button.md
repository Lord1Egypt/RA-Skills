---
name: component-button
description: Button component with variants, loading states, and icon integration
---

# Button

Button component with multiple types, sizes, states, and icon support.

## Basic Usage

```vue
<template>
  <n-space>
    <n-button>Default</n-button>
    <n-button type="tertiary">Tertiary</n-button>
    <n-button type="primary">Primary</n-button>
    <n-button type="info">Info</n-button>
    <n-button type="success">Success</n-button>
    <n-button type="warning">Warning</n-button>
    <n-button type="error">Error</n-button>
  </n-space>
</template>
```

## Button Types

### Default

```vue
<template>
  <n-button>Default Button</n-button>
</template>
```

### Primary

```vue
<template>
  <n-button type="primary">Primary</n-button>
</template>
```

### Dashed

```vue
<template>
  <n-button dashed>Dashed Button</n-button>
</template>
```

### Ghost

```vue
<template>
  <div style="background: #000; padding: 20px">
    <n-button ghost>Ghost Button</n-button>
    <n-button ghost type="primary">Primary Ghost</n-button>
  </div>
</template>
```

### Text

```vue
<template>
  <n-button text>Text Button</n-button>
  <n-button text tag="a" href="https://example.com">
    Link Button
  </n-button>
</template>
```

## Sizes

```vue
<template>
  <n-space align="baseline">
    <n-button size="tiny">Tiny</n-button>
    <n-button size="small">Small</n-button>
    <n-button size="medium">Medium</n-button>
    <n-button size="large">Large</n-button>
  </n-space>
</template>
```

## Icon Buttons

### With Icon Component

```vue
<script setup lang="ts">
import { CashOutline as CashIcon } from '@vicons/ionicons5'
</script>

<template>
  <n-space>
    <n-button>
      <template #icon>
        <n-icon :component="CashIcon" />
      </template>
      With Icon
    </n-button>

    <n-button circle>
      <template #icon>
        <n-icon :component="CashIcon" />
      </template>
    </n-button>

    <n-button text circle>
      <template #icon>
        <n-icon :component="CashIcon" />
      </template>
    </n-button>
  </n-space>
</template>
```

### Icon Position

```vue
<template>
  <n-space>
    <n-button>
      <template #icon>
        <n-icon :component="ArrowForwardIcon" />
      </template>
      Icon Left
    </n-button>

    <n-button>
      Icon Right
      <template #icon>
        <n-icon :component="ArrowForwardIcon" />
      </template>
    </n-button>
  </n-space>
</template>
```

## Loading State

```vue
<script setup lang="ts">
import { ref } from 'vue'

const loading = ref(false)

const handleClick = async () => {
  loading.value = true
  try {
    await someAsyncOperation()
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <n-space>
    <n-button :loading="loading" @click="handleClick">
      Click to Load
    </n-button>

    <n-button :loading="loading" type="primary">
      Loading...
    </n-button>

    <n-button :loading="loading" circle>
      <template #icon>
        <n-icon :component="RefreshIcon" />
      </template>
    </n-button>
  </n-space>
</template>
```

## Disabled State

```vue
<template>
  <n-space>
    <n-button disabled>Disabled</n-button>
    <n-button type="primary" disabled>Primary Disabled</n-button>
    <n-button text disabled>Text Disabled</n-button>
  </n-space>
</template>
```

## Block Button

```vue
<template>
  <n-button block type="primary">Full Width Button</n-button>
</template>
```

## Button Group

```vue
<template>
  <n-button-group>
    <n-button>Left</n-button>
    <n-button>Middle</n-button>
    <n-button>Right</n-button>
  </n-button-group>

  <n-button-group vertical>
    <n-button>Top</n-button>
    <n-button>Middle</n-button>
    <n-button>Bottom</n-button>
  </n-button-group>
</template>
```

## Color Customization

```vue
<template>
  <n-space>
    <n-button color="#8a2be2">Custom Color</n-button>
    <n-button color="#ff69b4" text-color="#000">Custom Text Color</n-button>
    <n-button text-color="#ff69b4" type="primary">Custom Text on Primary</n-button>
  </n-space>
</template>
```

## Async Click Handling

```vue
<script setup lang="ts">
const handleAsyncClick = async () => {
  await new Promise(resolve => setTimeout(resolve, 2000))
  console.log('Async operation completed')
}
</script>

<template>
  
  <n-button @click="handleAsyncClick">
    Auto Loading on Async
  </n-button>
</template>
```

## Router Integration

```vue
<template>
  <n-space>
    <n-button tag="router-link" to="/home">
      Go Home
    </n-button>

    <n-button tag="a" href="https://example.com" target="_blank">
      External Link
    </n-button>
  </n-space>
</template>
```

## Common Patterns

### Form Actions

```vue
<template>
  <n-space justify="end">
    <n-button @click="resetForm">Reset</n-button>
    <n-button type="primary" @click="submitForm" :loading="submitting">
      Submit
    </n-button>
  </n-space>
</template>
```

### Confirmation Button

```vue
<script setup lang="ts">
import { useDialog } from 'naive-ui'

const dialog = useDialog()

const handleDelete = () => {
  dialog.warning({
    title: 'Confirm Delete',
    content: 'Are you sure you want to delete this item?',
    positiveText: 'Delete',
    negativeText: 'Cancel',
    onPositiveClick: () => {
      deleteItem()
    }
  })
}
</script>

<template>
  <n-button type="error" @click="handleDelete">
    Delete
  </n-button>
</template>
```

### Copy to Clipboard

```vue
<script setup lang="ts">
import { useMessage } from 'naive-ui'

const message = useMessage()

const copyToClipboard = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text)
    message.success('Copied to clipboard')
  } catch (err) {
    message.error('Failed to copy')
  }
}
</script>

<template>
  <n-button text @click="copyToClipboard('Some text')">
    <template #icon>
      <n-icon :component="CopyIcon" />
    </template>
    Copy
  </n-button>
</template>
```

## Key Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | `'default' \| 'primary' \| 'info' \| 'success' \| 'warning' \| 'error'` | `'default'` | Button type |
| `size` | `'tiny' \| 'small' \| 'medium' \| 'large'` | `'medium'` | Button size |
| `dashed` | `boolean` | `false` | Dashed style |
| `ghost` | `boolean` | `false` | Ghost style |
| `text` | `boolean` | `false` | Text style |
| `circle` | `boolean` | `false` | Circle shape |
| `round` | `boolean` | `false` | Rounded corners |
| `loading` | `boolean` | `false` | Loading state |
| `disabled` | `boolean` | `false` | Disabled state |
| `block` | `boolean` | `false` | Full width |
| `tag` | `string` | `'button'` | HTML tag or component |

## Key Types

```ts
import type {
  ButtonProps,
  ButtonInst,
  ButtonGroupProps
} from 'naive-ui'
```

## Async Button Click Errors Not Caught by errorHandler

Vue's `app.config.errorHandler` doesn't catch errors in async button handlers because the error occurs in a promise that Vue doesn't track.

**Incorrect (error not caught by errorHandler):**

```vue
<template>
  <n-button type="primary" @click="login">Login</n-button>
</template>

<script setup lang="ts">
async function login(): Promise<void> {
  await loginForm.value?.validate()
  await authService.login(user.value)  // Incorrect: Error here not caught
  await router.push('/dashboard')
}
</script>
```

**Correct Solution 1: Explicit try-catch**

```vue
<template>
  <n-button
    type="primary"
    :loading="loading"
    @click="handleLogin"
  >
    Login
  </n-button>
</template>

<script setup lang="ts">
const message = useMessage()
const loading = ref(false)

async function handleLogin(): Promise<void> {
  loading.value = true
  try {
    await loginForm.value?.validate()
    await authService.login(user.value)
    await router.push('/dashboard')
  } catch (error: any) {
    // Correct: Explicit error handling
    message.error(error.message || 'Login failed')
  } finally {
    loading.value = false
  }
}
</script>
```

**Correct Solution 2: Wrap in synchronous handler**

```vue
<template>
  <n-button @click="() => login().catch(handleError)">
    Login
  </n-button>
</template>

<script setup lang="ts">
async function login(): Promise<void> {
  await loginForm.value?.validate()
  await authService.login(user.value)
}

function handleError(error: any) {
  message.error(error.message)
}
</script>
```

**Correct Solution 3: Use global error boundary**

```vue
<script setup lang="ts">
import { onErrorCaptured } from 'vue'

onErrorCaptured((err, instance, info) => {
  console.error('Error captured:', err)
  message.error('An error occurred')
  return false // Stop propagation
})
</script>
```

**Best Practice:**

Always handle async errors explicitly in button handlers. Don't rely on global errorHandler for async operations.

```vue
<script setup lang="ts">
// Good pattern: Always wrap async handlers
const handleAsyncAction = async () => {
  try {
    await someAsyncOperation()
  } catch (e) {
    // Handle or report error
    message.error('Operation failed')
    console.error(e)
  }
}
</script>
```
