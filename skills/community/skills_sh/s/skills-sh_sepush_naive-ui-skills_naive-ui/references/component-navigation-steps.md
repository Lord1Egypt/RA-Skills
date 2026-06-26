---
name: component-navigation-steps
description: Navigation components including Steps, Timeline, Pagination, and Anchor
---

# Navigation & Steps

Components for displaying multi-step processes, timelines, and navigation.

## Steps

### Basic Usage

```vue
<script setup lang="ts">
import { ref } from 'vue'

const current = ref(1)

const steps = [
  { title: 'I am the first', description: 'Description' },
  { title: 'I am the second', description: 'Description' },
  { title: 'I am the third', description: 'Description' }
]
</script>

<template>
  <n-steps :current="current" vertical>
    <n-step
      v-for="(step, index) in steps"
      :key="index"
      :title="step.title"
      :description="step.description"
    />
  </n-steps>
</template>
```

### Horizontal Steps

```vue
<template>
  <n-steps :current="1">
    <n-step title="Account" description="Create account" />
    <n-step title="Profile" description="Set up profile" />
    <n-step title="Complete" description="Done" />
  </n-steps>
</template>
```

### Clickable Steps

```vue
<template>
  <n-steps v-model:current="current" :on-update:current="onUpdateCurrent">
    <n-step title="Step 1" />
    <n-step title="Step 2" />
    <n-step title="Step 3" />
  </n-steps>
</template>
```

### Status

```vue
<template>
  <n-steps :current="2" status="error">
    <n-step title="Done" description="Finished" />
    <n-step title="Error" description="Something wrong" />
    <n-step title="Pending" description="Waiting" />
  </n-steps>
</template>
```

### Icon Steps

```vue
<script setup lang="ts">
import { Person, Airplane, Bag } from '@vicons/ionicons5'
</script>

<template>
  <n-steps :current="1">
    <n-step title="Account" :icon="Person" />
    <n-step title="Shipping" :icon="Airplane" />
    <n-step title="Payment" :icon="Bag" />
  </n-steps>
</template>
```

### Size

```vue
<template>
  <n-space vertical>
    <n-steps :current="1" size="small">
      <n-step title="Small" />
      <n-step title="Step 2" />
    </n-steps>

    <n-steps :current="1" size="medium">
      <n-step title="Medium" />
      <n-step title="Step 2" />
    </n-steps>
  </n-space>
</template>
```

## Timeline

### Basic Usage

```vue
<template>
  <n-timeline>
    <n-timeline-item content="Oops" time="2018-04-03 20:46" />
    <n-timeline-item type="success" title="Success" content="Success content" time="2018-04-03 20:46" />
    <n-timeline-item type="info" title="Info" content="Info content" time="2018-04-03 20:46" />
    <n-timeline-item type="warning" title="Warning" content="Warning content" time="2018-04-03 20:46" />
    <n-timeline-item type="error" title="Error" content="Error content" time="2018-04-03 20:46" />
  </n-timeline>
</template>
```

### Horizontal Timeline

```vue
<template>
  <n-timeline horizontal>
    <n-timeline-item content="Step 1" />
    <n-timeline-item content="Step 2" />
    <n-timeline-item content="Step 3" />
  </n-timeline>
</template>
```

### Custom Icon

```vue
<script setup lang="ts">
import { Checkmark } from '@vicons/ionicons5'
</script>

<template>
  <n-timeline>
    <n-timeline-item :icon="Checkmark" content="Completed" />
  </n-timeline>
</template>
```

### Item Line Type

```vue
<template>
  <n-timeline>
    <n-timeline-item line-type="dashed" content="Dashed line" />
    <n-timeline-item line-type="dotted" content="Dotted line" />
  </n-timeline>
</template>
```

## Pagination

### Basic Usage

```vue
<script setup lang="ts">
const page = ref(1)
const pageSize = ref(10)
const itemCount = ref(100)
</script>

<template>
  <n-pagination
    v-model:page="page"
    v-model:page-size="pageSize"
    :item-count="itemCount"
    show-size-picker
    :page-sizes="[10, 20, 50]"
  />
</template>
```

### Quick Jumper

```vue
<template>
  <n-pagination
    v-model:page="page"
    :page-count="20"
    show-quick-jumper
  />
</template>
```

### Simple Mode

```vue
<template>
  <n-pagination
    v-model:page="page"
    :page-count="20"
    simple
  />
</template>
```

### Disabled

```vue
<template>
  <n-pagination disabled :page-count="10" />
</template>
```

### Slot Customization

```vue
<template>
  <n-pagination v-model:page="page" :page-count="20">
    <template #prefix="{ itemCount, startIndex, endIndex }">
      Showing {{ startIndex }} to {{ endIndex }} of {{ itemCount }} items
    </template>
    <template #suffix>
      items per page
    </template>
  </n-pagination>
</template>
```

## Anchor

### Basic Usage

```vue
<template>
  <n-anchor affix>
    <n-anchor-link title="Basic" href="#basic" />
    <n-anchor-link title="API" href="#api">
      <n-anchor-link title="Props" href="#props" />
      <n-anchor-link title="Events" href="#events" />
    </n-anchor-link>
  </n-anchor>
</template>
```

### Scroll Container

```vue
<script setup lang="ts">
const scrollContainer = ref<HTMLElement | null>(null)
</script>

<template>
  <div ref="scrollContainer" style="height: 300px; overflow: auto">
    <n-anchor :get-container="() => scrollContainer">
      <n-anchor-link title="Section 1" href="#section1" />
      <n-anchor-link title="Section 2" href="#section2" />
    </n-anchor>

    <div id="section1">Section 1 content...</div>
    <div id="section2">Section 2 content...</div>
  </div>
</template>
```

### Offset

```vue
<template>
  <n-anchor :offset-top="64">
    <n-anchor-link title="Section" href="#section" />
  </n-anchor>
</template>
```

## Anchor (Back to Top)

```vue
<template>
  <n-back-top :right="40" :bottom="40">
    <n-button circle>
      <template #icon>
        <n-icon :component="ArrowUp" />
      </template>
    </n-button>
  </n-back-top>
</template>
```

### Visibility Height

```vue
<template>
  <n-back-top :visibility-height="300">
    Back to top after scrolling 300px
  </n-back-top>
</template>
```

## Common Patterns

### Multi-step Form

```vue
<script setup lang="ts">
const currentStep = ref(0)
const formData = ref({
  account: {},
  personal: {},
  payment: {}
})

const steps = [
  { title: 'Account', key: 'account' },
  { title: 'Personal', key: 'personal' },
  { title: 'Payment', key: 'payment' },
  { title: 'Review', key: 'review' }
]

const nextStep = () => {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}
</script>

<template>
  <n-card>
    <n-steps :current="currentStep" :status="currentStatus">
      <n-step
        v-for="step in steps"
        :key="step.key"
        :title="step.title"
      />
    </n-steps>

    <div style="margin: 24px 0">
      <account-form v-if="currentStep === 0" v-model="formData.account" />
      <personal-form v-if="currentStep === 1" v-model="formData.personal" />
      <payment-form v-if="currentStep === 2" v-model="formData.payment" />
      <review-form v-if="currentStep === 3" :data="formData" />
    </div>

    <n-space justify="end">
      <n-button v-if="currentStep > 0" @click="prevStep">
        Previous
      </n-button>
      <n-button
        v-if="currentStep < steps.length - 1"
        type="primary"
        @click="nextStep"
      >
        Next
      </n-button>
      <n-button
        v-else
        type="primary"
        @click="submit"
      >
        Submit
      </n-button>
    </n-space>
  </n-card>
</template>
```

### Order Tracking

```vue
<template>
  <n-timeline>
    <n-timeline-item
      v-for="(event, index) in orderHistory"
      :key="index"
      :type="event.type"
      :title="event.title"
      :content="event.description"
      :time="event.timestamp"
    />
  </n-timeline>
</template>
```

### Table with Pagination

```vue
<script setup lang="ts">
const loading = ref(false)
const data = ref([])
const pagination = reactive({
  page: 1,
  pageSize: 10,
  itemCount: 0,
  showSizePicker: true,
  pageSizes: [10, 20, 50],
  onChange: (page: number) => {
    pagination.page = page
    fetchData()
  },
  onUpdatePageSize: (pageSize: number) => {
    pagination.pageSize = pageSize
    pagination.page = 1
    fetchData()
  }
})

const fetchData = async () => {
  loading.value = true
  const result = await api.getList({
    page: pagination.page,
    pageSize: pagination.pageSize
  })
  data.value = result.data
  pagination.itemCount = result.total
  loading.value = false
}
</script>

<template>
  <n-data-table
    :columns="columns"
    :data="data"
    :loading="loading"
    :pagination="pagination"
    remote
  />
</template>
```

## Key Types

```ts
import type {
  StepsProps,
  StepProps,
  TimelineProps,
  TimelineItemProps,
  PaginationProps,
  AnchorProps,
  AnchorLinkProps,
  BackTopProps
} from 'naive-ui'
```


