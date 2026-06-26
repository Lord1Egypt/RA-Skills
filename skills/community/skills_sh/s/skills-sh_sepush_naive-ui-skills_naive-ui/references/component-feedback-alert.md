---
name: component-feedback-alert
description: Feedback components including Alert, Skeleton, LoadingBar, Spin, and Popconfirm
---

# Feedback Components

Components for displaying feedback, loading states, and confirmations.

## Alert

### Basic Usage

```vue
<template>
  <n-space vertical>
    <n-alert title="Default" type="default">
      Default alert content
    </n-alert>
    <n-alert title="Info" type="info">
      Info alert content
    </n-alert>
    <n-alert title="Success" type="success">
      Success alert content
    </n-alert>
    <n-alert title="Warning" type="warning">
      Warning alert content
    </n-alert>
    <n-alert title="Error" type="error">
      Error alert content
    </n-alert>
  </n-space>
</template>
```

### Closable

```vue
<template>
  <n-alert title="Closable" closable @close="handleClose">
    You can close this alert
  </n-alert>
</template>
```

### No Icon

```vue
<template>
  <n-alert :show-icon="false" title="No Icon">
    Alert without icon
  </n-alert>
</template>
```

### Borderless

```vue
<template>
  <n-alert title="Borderless" :bordered="false">
    Alert without border
  </n-alert>
</template>
```

### Custom Icon

```vue
<script setup lang="ts">
import { Happy } from '@vicons/ionicons5'
</script>

<template>
  <n-alert :icon="Happy" title="Custom Icon">
    Alert with custom icon
  </n-alert>
</template>
```

### Description

```vue
<template>
  <n-alert title="With Description" type="info">
    <template #header>Alert Title</template>
    Detailed description content goes here. You can provide more context.
  </n-alert>
</template>
```

## Skeleton

### Basic Usage

```vue
<template>
  <n-skeleton text :repeat="3" />
  <n-skeleton style="width: 60%; margin-top: 12px" />
</template>
```

### Skeleton Types

```vue
<template>
  <n-space vertical>
    <n-skeleton style="width: 200px; height: 200px" />
    <n-skeleton circle style="width: 100px; height: 100px" />
    <n-skeleton round style="width: 200px; height: 40px" />
  </n-space>
</template>
```

### Animated

```vue
<template>
  <n-skeleton animated />
</template>
```

### Size

```vue
<template>
  <n-space vertical>
    <n-skeleton text size="small" />
    <n-skeleton text size="medium" />
    <n-skeleton text size="large" />
  </n-space>
</template>
```

### Complex Skeleton

```vue
<template>
  <n-space vertical>
    <n-space>
      <n-skeleton circle style="width: 48px; height: 48px" />
      <n-space vertical>
        <n-skeleton text style="width: 150px" />
        <n-skeleton text style="width: 100px" />
      </n-space>
    </n-space>
    <n-skeleton text :repeat="2" />
    <n-skeleton style="width: 60%; height: 200px" />
  </n-space>
</template>
```

## Loading Bar

### Basic Usage

```vue
<script setup lang="ts">
import { useLoadingBar } from 'naive-ui'

const loadingBar = useLoadingBar()

const startLoading = () => {
  loadingBar.start()
}

const finishLoading = () => {
  loadingBar.finish()
}

const errorLoading = () => {
  loadingBar.error()
}
</script>

<template>
  <n-space>
    <n-button @click="startLoading">Start</n-button>
    <n-button @click="finishLoading">Finish</n-button>
    <n-button @click="errorLoading">Error</n-button>
  </n-space>
</template>
```

### With Router

```vue
<script setup lang="ts">
import { useLoadingBar } from 'naive-ui'
import { useRouter } from 'vue-router'

const loadingBar = useLoadingBar()
const router = useRouter()

router.beforeEach(() => {
  loadingBar.start()
})

router.afterEach(() => {
  loadingBar.finish()
})
</script>
```

## Spin

### Basic Usage

```vue
<template>
  <n-spin :show="loading">
    <n-card title="Card">
      Content that will be covered when spinning
    </n-card>
  </n-spin>
</template>
```

### Spin Sizes

```vue
<template>
  <n-space>
    <n-spin size="small" />
    <n-spin size="medium" />
    <n-spin size="large" />
  </n-space>
</template>
```

### Custom Icon

```vue
<script setup lang="ts">
import { LogoApple } from '@vicons/ionicons5'
</script>

<template>
  <n-spin>
    <template #icon>
      <n-icon :component="LogoApple" />
    </template>
    Loading...
  </n-spin>
</template>
```

### Description

```vue
<template>
  <n-spin :show="loading" description="Loading...">
    <n-card>
      Content
    </n-card>
  </n-spin>
</template>
```

### Wrapped Spin

```vue
<template>
  <div style="display: flex">
    <n-spin :show="loading" style="width: 100%">
      <n-table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in data" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.value }}</td>
          </tr>
        </tbody>
      </n-table>
    </n-spin>
  </div>
</template>
```

## Popconfirm

### Basic Usage

```vue
<template>
  <n-popconfirm @positive-click="handlePositiveClick">
    <template #trigger>
      <n-button>Delete</n-button>
    </template>
    Are you sure you want to delete this?
  </n-popconfirm>
</template>
```

### Custom Text

```vue
<template>
  <n-popconfirm
    positive-text="Confirm"
    negative-text="Cancel"
    @positive-click="handleConfirm"
  >
    <template #trigger>
      <n-button type="error">Delete</n-button>
    </template>
    <template #icon>
      <n-icon :component="TrashIcon" color="red" />
    </template>
    This action cannot be undone.
  </n-popconfirm>
</template>
```

### Show/Hide

```vue
<script setup lang="ts">
const show = ref(false)

const handleConfirm = () => {
  show.value = false
  deleteItem()
}
</script>

<template>
  <n-popconfirm v-model:show="show" @positive-click="handleConfirm">
    <template #trigger>
      <n-button @click="show = true">Delete</n-button>
    </template>
    Confirm deletion?
  </n-popconfirm>
</template>
```

## Loading States

### Button Loading

```vue
<template>
  <n-button :loading="loading" @click="handleClick">
    Submit
  </n-button>
</template>
```

### Input Loading

```vue
<template>
  <n-input v-model:value="value" loading placeholder="Loading..." />
</template>
```

### Select Loading

```vue
<template>
  <n-select v-model:value="value" :loading="loading" :options="options" />
</template>
```

## Common Patterns

### Page Loading

```vue
<script setup lang="ts">
const loading = ref(true)
const data = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    data.value = await fetchData()
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <n-spin :show="loading" size="large" style="min-height: 300px">
    <div v-if="data">
      <n-h1>{{ data.title }}</n-h1>
      <n-p>{{ data.content }}</n-p>
    </div>
  </n-spin>
</template>
```

### Skeleton Screen

```vue
<template>
  <div v-if="loading">
    <n-skeleton style="width: 100%; height: 200px" />
    <n-skeleton text size="large" style="margin-top: 12px" />
    <n-skeleton text :repeat="3" />
  </div>
  <div v-else>
    <img :src="imageUrl" style="width: 100%; height: 200px; object-fit: cover">
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
  </div>
</template>
```

### List with Loading

```vue
<template>
  <n-list>
    <n-list-item v-for="item in items" :key="item.id">
      <n-thing :title="item.title">
        <template #description>{{ item.description }}</template>
      </n-thing>
    </n-list-item>
    <template #footer>
      <n-spin v-if="loadingMore" size="small">
        <template #description>
          Loading more...
        </template>
      </n-spin>
      <n-button v-else text @click="loadMore">Load More</n-button>
    </template>
  </n-list>
</template>
```

### Operation Confirmation

```vue
<template>
  <n-space>
    <n-popconfirm @positive-click="handleDelete">
      <template #trigger>
        <n-button type="error">Delete</n-button>
      </template>
      Are you sure to delete this item?
    </n-popconfirm>

    <n-popconfirm
      :show-icon="false"
      @positive-click="handlePublish"
    >
      <template #trigger>
        <n-button type="primary">Publish</n-button>
      </template>
      <template #action>
        <n-button size="small" @click="handleSaveAsDraft">
          Save as Draft
        </n-button>
        <n-button size="small" type="primary" @click="handlePublishNow">
          Publish Now
        </n-button>
      </template>
      Publish this article?
    </n-popconfirm>
  </n-space>
</template>
```

### Alert Banner

```vue
<template>
  <n-alert
    v-if="showBanner"
    title="System Maintenance"
    type="warning"
    closable
    @close="showBanner = false"
  >
    System will be down for maintenance on Sunday 2:00 AM - 4:00 AM.
  </n-alert>
</template>
```

### Form Submission

```vue
<script setup lang="ts">
const submitting = ref(false)

const handleSubmit = async () => {
  submitting.value = true
  try {
    await submitForm(formData.value)
    message.success('Submitted successfully')
  } catch (error) {
    message.error('Submission failed')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <n-spin :show="submitting">
    <n-form>
      
      <n-button type="primary" @click="handleSubmit">
        Submit
      </n-button>
    </n-form>
    <template #description>
      Submitting...
    </template>
  </n-spin>
</template>
```

## Key Types

```ts
import type {
  AlertProps,
  SkeletonProps,
  SpinProps,
  PopconfirmProps,
  LoadingBarProviderInst
} from 'naive-ui'
```


