---
name: component-display
description: Display components including Badge, Tag, Avatar, Progress, and Statistic
---

# Display Components

Components for displaying data, status, and statistics.

## Badge

### Basic Usage

```vue
<template>
  <n-badge :value="5">
    <n-avatar src="https://example.com/avatar.jpg" />
  </n-badge>
</template>
```

### Badge Types

```vue
<template>
  <n-space>
    <n-badge :value="20" :max="15">
      <n-button>Messages</n-button>
    </n-badge>

    <n-badge dot>
      <n-icon size="24" :component="NotificationsOutline" />
    </n-badge>

    <n-badge processing>
      <n-icon size="24" :component="NotificationsOutline" />
    </n-badge>
  </n-space>
</template>
```

### Badge with Text

```vue
<template>
  <n-badge value="NEW">
    <n-button>Updates</n-button>
  </n-badge>
</template>
```

### Offset

```vue
<template>
  <n-badge :value="10" :offset="[10, 10]">
    <n-avatar size="large" />
  </n-badge>
</template>
```

## Tag

### Basic Usage

```vue
<template>
  <n-space>
    <n-tag>Default</n-tag>
    <n-tag type="primary">Primary</n-tag>
    <n-tag type="info">Info</n-tag>
    <n-tag type="success">Success</n-tag>
    <n-tag type="warning">Warning</n-tag>
    <n-tag type="error">Error</n-tag>
  </n-space>
</template>
```

### Closable Tags

```vue
<script setup lang="ts">
import { ref } from 'vue'

const tags = ref([
  { label: 'Vue', value: 'vue' },
  { label: 'React', value: 'react' },
  { label: 'Angular', value: 'angular' }
])

const removeTag = (value: string) => {
  const index = tags.value.findIndex(tag => tag.value === value)
  if (index > -1) {
    tags.value.splice(index, 1)
  }
}
</script>

<template>
  <n-space>
    <n-tag
      v-for="tag in tags"
      :key="tag.value"
      closable
      @close="removeTag(tag.value)"
    >
      {{ tag.label }}
    </n-tag>
  </n-space>
</template>
```

### Tag Sizes

```vue
<template>
  <n-space>
    <n-tag size="small">Small</n-tag>
    <n-tag size="medium">Medium</n-tag>
    <n-tag size="large">Large</n-tag>
  </n-space>
</template>
```

### Round Tags

```vue
<template>
  <n-tag round>Round Tag</n-tag>
  <n-tag round type="primary">Round Primary</n-tag>
</template>
```

### Checkable Tags

```vue
<script setup lang="ts">
const checked = ref(false)
</script>

<template>
  <n-tag v-model:checked="checked" checkable>
    Checkable Tag
  </n-tag>
</template>
```

## Avatar

### Basic Usage

```vue
<template>
  <n-space>
    <n-avatar src="https://example.com/avatar.jpg" />
    <n-avatar round src="https://example.com/avatar.jpg" />
  </n-space>
</template>
```

### Avatar Sizes

```vue
<template>
  <n-space align="center">
    <n-avatar size="small" src="..." />
    <n-avatar size="medium" src="..." />
    <n-avatar size="large" src="..." />
    <n-avatar :size="48" src="..." />
  </n-space>
</template>
```

### Fallback

```vue
<template>
  <n-avatar
    src="https://broken-link.jpg"
    fallback-src="https://default-avatar.jpg"
  />
</template>
```

### With Object Fit

```vue
<template>
  <n-avatar
    src="https://example.com/image.jpg"
    object-fit="cover"
    style="width: 100px; height: 100px"
  />
</template>
```

### Avatar Group

```vue
<template>
  <n-avatar-group :options="avatarOptions" :size="40" :max="3">
    <template #avatar="{ option: { src } }">
      <n-avatar :src="src" />
    </template>
    <template #rest="{ options: restOptions, rest }">
      <n-avatar>+{{ rest }}</n-avatar>
    </template>
  </n-avatar-group>
</template>
```

## Progress

### Basic Progress

```vue
<template>
  <n-progress type="line" :percentage="60" />
  <n-progress type="circle" :percentage="60" />
</template>
```

### Progress Types

```vue
<template>
  <n-space vertical>
    <n-progress type="line" :percentage="30" />
    <n-progress type="line" status="info" :percentage="50" />
    <n-progress type="line" status="success" :percentage="70" />
    <n-progress type="line" status="warning" :percentage="80" />
    <n-progress type="line" status="error" :percentage="90" />
  </n-space>
</template>
```

### Circle Progress

```vue
<template>
  <n-space>
    <n-progress type="circle" :percentage="75" />
    <n-progress type="circle" :percentage="75" status="success" />
    <n-progress type="circle" :percentage="75" status="warning" />
    <n-progress type="circle" :percentage="75" status="error" />
  </n-space>
</template>
```

### Dashboard Progress

```vue
<template>
  <n-progress type="dashboard" :percentage="60" gap-degree="120" />
</template>
```

### Multiple Progress

```vue
<template>
  <n-progress
    type="line"
    :percentage="[30, 20, 10]"
    :color="['#2080f0', '#18a058', '#f0a020']"
  />
</template>
```

### Processing State

```vue
<template>
  <n-progress
    type="line"
    :percentage="60"
    processing
    :show-indicator="false"
  />
</template>
```

## Statistic

### Basic Usage

```vue
<template>
  <n-statistic label="Active Users" :value="93" />
</template>
```

### With Prefix/Suffix

```vue
<template>
  <n-space>
    <n-statistic label="Revenue" :value="12890">
      <template #prefix>$</template>
    </n-statistic>

    <n-statistic label="Growth" :value="15.4">
      <template #suffix>%</template>
    </n-statistic>
  </n-space>
</template>
```

### Trend

```vue
<template>
  <n-space>
    <n-statistic label="Sales" :value="12890" trend="up">
      <template #suffix>%</template>
    </n-statistic>

    <n-statistic label="Returns" :value="12" trend="down" />
  </n-space>
</template>
```

### Number Animation

```vue
<script setup lang="ts">
import { ref } from 'vue'

const active = ref(false)

const activate = () => {
  active.value = true
}
</script>

<template>
  <n-statistic tabular-nums>
    <n-number-animation
      ref="numberAnimationInstRef"
      :from="0"
      :to="12039"
      :active="active"
      :duration="2000"
    />
  </n-statistic>
  <n-button @click="activate">Start</n-button>
</template>
```

## Countdown

```vue
<template>
  <n-countdown
    :duration="86400000"
    :active="true"
  />
</template>
```

## Result

```vue
<template>
  <n-result
    status="success"
    title="Operation Successful"
    description="Your changes have been saved successfully."
  >
    <template #footer>
      <n-button>Back Home</n-button>
    </template>
  </n-result>
</template>
```

### Result Types

```vue
<template>
  <n-space vertical>
    <n-result status="info" title="Information" />
    <n-result status="success" title="Success" />
    <n-result status="warning" title="Warning" />
    <n-result status="error" title="Error" />
    <n-result status="404" title="Not Found" />
    <n-result status="403" title="Forbidden" />
    <n-result status="500" title="Server Error" />
  </n-space>
</template>
```

## Empty

```vue
<template>
  <n-empty description="No data available">
    <template #extra>
      <n-button size="small">Create New</n-button>
    </template>
  </n-empty>
</template>
```

## Common Patterns

### Dashboard Stats

```vue
<template>
  <n-grid cols="1 s:2 m:4" :x-gap="16">
    <n-grid-item>
      <n-card>
        <n-statistic label="Total Sales" tabular-nums>
          <template #prefix>$</template>
          <n-number-animation :from="0" :to="28492" />
        </n-statistic>
        <n-tag size="small" type="success" style="margin-top: 8px">
          +12.5% vs last month
        </n-tag>
      </n-card>
    </n-grid-item>
  </n-grid>
</template>
```

### User List with Avatars

```vue
<template>
  <n-list>
    <n-list-item v-for="user in users" :key="user.id">
      <n-thing>
        <template #avatar>
          <n-badge :value="user.unread" :max="99">
            <n-avatar :src="user.avatar" />
          </n-badge>
        </template>
        <template #header>{{ user.name }}</template>
        <template #description>{{ user.email }}</template>
        <template #header-extra>
          <n-tag v-if="user.online" type="success" size="small">
            Online
          </n-tag>
        </template>
      </n-thing>
    </n-list-item>
  </n-list>
</template>
```

## Key Types

```ts
import type {
  BadgeProps,
  TagProps,
  AvatarProps,
  ProgressProps,
  StatisticProps,
  CountdownProps,
  ResultProps,
  EmptyProps
} from 'naive-ui'
```


