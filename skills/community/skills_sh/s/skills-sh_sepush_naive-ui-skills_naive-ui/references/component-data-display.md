---
name: component-data-display
description: Data display components including Image, List, Descriptions, Calendar, and Time
---

# Data Display Components

Components for displaying various types of data.

## Image

### Basic Usage

```vue
<template>
  <n-image
    width="100"
    src="https://example.com/image.jpg"
  />
</template>
```

### Fallback

```vue
<template>
  <n-image
    src="https://broken-link.jpg"
    fallback-src="https://placeholder.com/100"
  />
</template>
```

### Preview

```vue
<template>
  <n-image-group show-toolbar-tooltip>
    <n-space>
      <n-image
        v-for="url in imageUrls"
        :key="url"
        width="100"
        height="100"
        :src="url"
      />
    </n-space>
  </n-image-group>
</template>
```

### Custom Preview Toolbar

```vue
<template>
  <n-image
    src="https://example.com/image.jpg"
    @download="handleDownload"
  >
    <template #toolbar>
      <n-space>
        <n-button @click="rotateLeft">Rotate Left</n-button>
        <n-button @click="rotateRight">Rotate Right</n-button>
      </n-space>
    </template>
  </n-image>
</template>
```

### Object Fit

```vue
<template>
  <n-space>
    <n-image
      width="100"
      height="100"
      src="https://example.com/wide.jpg"
      object-fit="fill"
    />
    <n-image
      width="100"
      height="100"
      src="https://example.com/wide.jpg"
      object-fit="contain"
    />
    <n-image
      width="100"
      height="100"
      src="https://example.com/wide.jpg"
      object-fit="cover"
    />
  </n-space>
</template>
```

### Lazy Loading

```vue
<template>
  <n-image
    lazy
    src="https://example.com/large-image.jpg"
    placeholder="https://example.com/placeholder.jpg"
  />
</template>
```

### Image with Overlay

```vue
<template>
  <n-image src="https://example.com/image.jpg">
    <template #overlay>
      <div class="overlay-content">
        <n-button type="primary">View Details</n-button>
      </div>
    </template>
  </n-image>
</template>

<style>
.overlay-content {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 0.3s;
}
.n-image:hover .overlay-content {
  opacity: 1;
}
</style>
```

## List

### Basic List

```vue
<template>
  <n-list>
    <n-list-item>
      <n-thing title="Item 1" description="Description 1" />
    </n-list-item>
    <n-list-item>
      <n-thing title="Item 2" description="Description 2" />
    </n-list-item>
  </n-list>
</template>
```

### Bordered List

```vue
<template>
  <n-list bordered>
    <n-list-item v-for="i in 5" :key="i">
      <n-thing :title="'Item ' + i" />
    </n-list-item>
  </n-list>
</template>
```

### Clickable Items

```vue
<template>
  <n-list hoverable clickable>
    <n-list-item
      v-for="item in items"
      :key="item.id"
      @click="handleSelect(item)"
    >
      <n-thing :title="item.title" />
    </n-list-item>
  </n-list>
</template>
```

### List with Actions

```vue
<template>
  <n-list>
    <n-list-item>
      <n-thing title="Item">
        <template #description>Description</template>
      </n-thing>
      <template #suffix>
        <n-button text>
          <template #icon>
            <n-icon :component="EditIcon" />
          </template>
        </n-button>
        <n-button text type="error">
          <template #icon>
            <n-icon :component="TrashIcon" />
          </template>
        </n-button>
      </template>
    </n-list-item>
  </n-list>
</template>
```

### Virtual List

```vue
<template>
  <n-list>
    <n-virtual-list
      :items="items"
      :item-size="56"
      style="max-height: 400px"
    >
      <template #default="{ item }">
        <n-list-item>
          <n-thing :title="item.title" />
        </n-list-item>
      </template>
    </n-virtual-list>
  </n-list>
</template>
```

## Descriptions

### Basic Usage

```vue
<template>
  <n-descriptions label-placement="top" title="User Info">
    <n-descriptions-item label="Name">John Doe</n-descriptions-item>
    <n-descriptions-item label="Email">john@example.com</n-descriptions-item>
    <n-descriptions-item label="Phone">+1 234 567 890</n-descriptions-item>
  </n-descriptions>
</template>
```

### Column Layout

```vue
<template>
  <n-descriptions :columns="3" bordered>
    <n-descriptions-item label="Name">John Doe</n-descriptions-item>
    <n-descriptions-item label="Age">32</n-descriptions-item>
    <n-descriptions-item label="City">New York</n-descriptions-item>
    <n-descriptions-item label="Address" :span="2">
      123 Main St, New York, NY 10001
    </n-descriptions-item>
    <n-descriptions-item label="Status">
      <n-tag type="success">Active</n-tag>
    </n-descriptions-item>
  </n-descriptions>
</template>
```

### Size Variants

```vue
<template>
  <n-space vertical>
    <n-descriptions size="small" title="Small">
      <n-descriptions-item label="Name">John</n-descriptions-item>
    </n-descriptions>
    <n-descriptions size="medium" title="Medium">
      <n-descriptions-item label="Name">John</n-descriptions-item>
    </n-descriptions>
    <n-descriptions size="large" title="Large">
      <n-descriptions-item label="Name">John</n-descriptions-item>
    </n-descriptions>
  </n-space>
</template>
```

### Dynamic Data

```vue
<script setup lang="ts">
const userInfo = {
  name: 'John Doe',
  email: 'john@example.com',
  department: 'Engineering',
  role: 'Senior Developer',
  status: 'Active',
  joinDate: '2020-01-15'
}

const items = [
  { label: 'Name', key: 'name' },
  { label: 'Email', key: 'email' },
  { label: 'Department', key: 'department' },
  { label: 'Role', key: 'role' },
  { label: 'Status', key: 'status', render: (val: string) => h(NTag, { type: 'success' }, val) },
  { label: 'Join Date', key: 'joinDate' }
]
</script>

<template>
  <n-descriptions bordered label-placement="left" :column="2">
    <n-descriptions-item
      v-for="item in items"
      :key="item.key"
      :label="item.label"
    >
      <template v-if="item.render">
        <component :is="item.render(userInfo[item.key])" />
      </template>
      <template v-else>
        {{ userInfo[item.key] }}
      </template>
    </n-descriptions-item>
  </n-descriptions>
</template>
```

## Calendar

### Basic Usage

```vue
<script setup lang="ts">
import { ref } from 'vue'

const value = ref(Date.now())
</script>

<template>
  <n-calendar v-model:value="value">
    <template #header="{ year, month }">
      <div>{{ year }} - {{ month }}</div>
    </template>
    <template #default="{ year, month, date }">
      <div>{{ date }}</div>
    </template>
  </n-calendar>
</template>
```

### With Events

```vue
<script setup lang="ts">
const events = ref([
  { date: '2024-01-15', title: 'Meeting' },
  { date: '2024-01-20', title: 'Deadline' }
])

const isEventDay = (ts: number) => {
  const date = new Date(ts).toISOString().split('T')[0]
  return events.value.some(e => e.date === date)
}
</script>

<template>
  <n-calendar v-model:value="value">
    <template #default="{ year, month, date }">
      <div :class="{ 'has-event': isEventDay(date) }">
        {{ new Date(date).getDate() }}
      </div>
    </template>
  </n-calendar>
</template>

<style>
.has-event {
  color: #18a058;
  font-weight: bold;
}
</style>
```

## Time

### Basic Usage

```vue
<template>
  <n-time :time="Date.now()" />
</template>
```

### Time Types

```vue
<template>
  <n-space vertical>
    <n-time :time="time" type="date" />
    <n-time :time="time" type="datetime" />
    <n-time :time="time" type="relative" />
  </n-space>
</template>
```

### Format

```vue
<template>
  <n-time
    :time="time"
    format="yyyy-MM-dd HH:mm:ss"
  />
</template>
```

### Relative Time

```vue
<template>
  <n-space vertical>
    <n-time :time="Date.now() - 60000" type="relative" />
    <n-time :time="Date.now() - 3600000" type="relative" />
    <n-time :time="Date.now() - 86400000" type="relative" />
  </n-space>
</template>
```

## Countdown

```vue
<template>
  <n-countdown
    :duration="86400000"
    :active="active"
    @finish="handleFinish"
  />
</template>
```

### With Render

```vue
<template>
  <n-countdown :duration="5000000" :render="renderCountdown" />
</template>

<script setup>
const renderCountdown = ({ hours, minutes, seconds }) => {
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
}
</script>
```

## Number Animation

```vue
<template>
  <n-statistic label="Active Users">
    <n-number-animation
      ref="numberAnimationInstRef"
      :from="0"
      :to="12039"
      :active="true"
      :duration="2000"
      :precision="0"
    />
  </n-statistic>
</template>
```

## Common Patterns

### User Profile Card

```vue
<template>
  <n-card>
    <n-space align="start">
      <n-avatar :size="80" :src="user.avatar" />
      <n-space vertical>
        <n-h3>{{ user.name }}</n-h3>
        <n-text depth="3">{{ user.email }}</n-text>
        <n-space>
          <n-tag v-for="role in user.roles" :key="role">{{ role }}</n-tag>
        </n-space>
      </n-space>
    </n-space>

    <n-divider />

    <n-descriptions :columns="2" size="small">
      <n-descriptions-item label="Department">
        {{ user.department }}
      </n-descriptions-item>
      <n-descriptions-item label="Join Date">
        <n-time :time="user.joinDate" type="date" />
      </n-descriptions-item>
      <n-descriptions-item label="Status">
        <n-tag :type="user.active ? 'success' : 'error'">
          {{ user.active ? 'Active' : 'Inactive' }}
        </n-tag>
      </n-descriptions-item>
      <n-descriptions-item label="Last Active">
        <n-time :time="user.lastActive" type="relative" />
      </n-descriptions-item>
    </n-descriptions>
  </n-card>
</template>
```

### Gallery Grid

```vue
<template>
  <n-grid :cols="3" :x-gap="12" :y-gap="12">
    <n-grid-item v-for="image in images" :key="image.id">
      <n-image
        :src="image.url"
        :alt="image.title"
        object-fit="cover"
        style="width: 100%; height: 200px; border-radius: 8px"
        @click="openPreview(image)"
      />
    </n-grid-item>
  </n-grid>
</template>
```

### Activity Feed

```vue
<template>
  <n-list>
    <n-list-item v-for="activity in activities" :key="activity.id">
      <n-thing>
        <template #avatar>
          <n-avatar :src="activity.user.avatar" />
        </template>
        <template #header>
          {{ activity.user.name }}
          <n-text depth="3">{{ activity.action }}</n-text>
          {{ activity.target }}
        </template>
        <template #description>
          <n-time :time="activity.timestamp" type="relative" />
        </template>
      </n-thing>
    </n-list-item>
  </n-list>
</template>
```

## Code & Log (Highlighting)

> **Warning:** Due to package size, Naive UI doesn't include `highlight.js`. If you want to use the `<n-code>` or `<n-log>` components, make sure you have set `highlight.js` before using them. Importing `highlight.js` on demand is recommended to significantly reduce bundle size.

### Code Component Setup

```vue
<script setup lang="ts">
import hljs from 'highlight.js/lib/core'
import typescript from 'highlight.js/lib/languages/typescript'

hljs.registerLanguage('typescript', typescript)
</script>

<template>
  <n-code :hljs="hljs" code="const a = 1;" language="typescript" />
</template>
```

### Log Component Setup

```vue
<script setup lang="ts">
import hljs from 'highlight.js/lib/core'

// Define your custom or standard languages
hljs.registerLanguage('naive-log', (hljs) => ({ /* ... */ }))
</script>

<template>
  <n-log :hljs="hljs" :log="logContent" language="naive-log" />
</template>
```

## Equation (KaTeX)

> **Warning:** Due to package size, Naive UI doesn't include katex. If you want to use Equation, make sure you have setup katex before using it. You can import katex styles in your HTML file: `<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.8/katex.min.css">`

## Key Types

```ts
import type {
  ImageProps,
  ImageGroupProps,
  ListProps,
  ListItemProps,
  DescriptionsProps,
  CalendarProps,
  TimeProps,
  CountdownProps,
  NumberAnimationProps
} from 'naive-ui'
```


