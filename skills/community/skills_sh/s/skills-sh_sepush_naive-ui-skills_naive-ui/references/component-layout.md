---
name: component-layout
description: Layout system including Layout, Grid, Flex, Space, Card, and Divider
---

# Layout System

Layout components for structuring your application interface.

## Layout

> **Warning:** If you need to use `n-drawer-content`, you should keep `n-drawer`'s `native-scrollbar` prop as `true`.

### Basic Layout

```vue
<template>
  <n-layout>
    <n-layout-header bordered style="height: 64px; padding: 24px">
      Header
    </n-layout-header>
    <n-layout-content style="padding: 24px; min-height: 400px">
      Content
    </n-layout-content>
    <n-layout-footer bordered style="padding: 24px">
      Footer
    </n-layout-footer>
  </n-layout>
</template>
```

### Layout with Sider

```vue
<template>
  <n-layout style="height: 100vh">
    <n-layout-header bordered>Header</n-layout-header>
    <n-layout has-sider>
      <n-layout-sider bordered content-style="padding: 24px">
        Sider
      </n-layout-sider>
      <n-layout-content content-style="padding: 24px">
        Content
      </n-layout-content>
    </n-layout>
    <n-layout-footer bordered>Footer</n-layout-footer>
  </n-layout>
</template>
```

### Collapsible Sider

```vue
<script setup lang="ts">
const collapsed = ref(false)
</script>

<template>
  <n-layout has-sider>
    <n-layout-sider
      collapse-mode="width"
      :collapsed-width="64"
      :width="240"
      :collapsed="collapsed"
      show-trigger
      @collapse="collapsed = true"
      @expand="collapsed = false"
    >
      <n-menu :collapsed="collapsed" :options="menuOptions" />
    </n-layout-sider>
    <n-layout-content>Content</n-layout-content>
  </n-layout>
</template>
```

## Grid

> **Warning:** Due to technical limitation, `n-grid-item` can't be encapsulated in another component.
> 
> **Warning:** The `n-legacy-grid` component is deprecated. In most cases you should use `n-grid` instead.

### Basic Grid

```vue
<template>
  <n-grid :cols="3" :x-gap="12" :y-gap="8">
    <n-grid-item>
      <div class="light-green">1</div>
    </n-grid-item>
    <n-grid-item>
      <div class="green">2</div>
    </n-grid-item>
    <n-grid-item>
      <div class="light-green">3</div>
    </n-grid-item>
  </n-grid>
</template>

<style>
.light-green { background: #e8f5e9; padding: 16px; }
.green { background: #c8e6c9; padding: 16px; }
</style>
```

### Responsive Grid

```vue
<template>
  <n-grid
    cols="1 s:2 m:3 l:4 xl:5"
    responsive="screen"
    :x-gap="16"
    :y-gap="16"
  >
    <n-grid-item v-for="i in 10" :key="i">
      <n-card>{{ i }}</n-card>
    </n-grid-item>
  </n-grid>
</template>
```

### Grid Span

```vue
<template>
  <n-grid :cols="4" :x-gap="12">
    <n-grid-item :span="2">
      <div class="light-green">Span 2</div>
    </n-grid-item>
    <n-grid-item>
      <div class="green">Span 1</div>
    </n-grid-item>
    <n-grid-item>
      <div class="light-green">Span 1</div>
    </n-grid-item>
    <n-grid-item :span="3">
      <div class="green">Span 3</div>
    </n-grid-item>
    <n-grid-item>
      <div class="light-green">Span 1</div>
    </n-grid-item>
  </n-grid>
</template>
```

### Offset

```vue
<template>
  <n-grid :cols="4" :x-gap="12">
    <n-grid-item :span="2">
      <div class="light-green">Content</div>
    </n-grid-item>
    <n-grid-item :span="2" :offset="2">
      <div class="green">Offset 2</div>
    </n-grid-item>
  </n-grid>
</template>
```

## Flex

```vue
<template>
  <n-flex vertical>
    <n-flex justify="space-between" align="center">
      <n-text>Left aligned</n-text>
      <n-space>
        <n-button>Action 1</n-button>
        <n-button>Action 2</n-button>
      </n-space>
    </n-flex>

    <n-flex :size="[16, 16]" wrap>
      <n-tag v-for="i in 10" :key="i">Tag {{ i }}</n-tag>
    </n-flex>
  </n-flex>
</template>
```

## Space

### Basic Usage

```vue
<template>
  <n-space>
    <n-button>Button 1</n-button>
    <n-button>Button 2</n-button>
    <n-button>Button 3</n-button>
  </n-space>
</template>
```

### Vertical Space

```vue
<template>
  <n-space vertical size="large">
    <n-input placeholder="Input 1" />
    <n-input placeholder="Input 2" />
    <n-input placeholder="Input 3" />
  </n-space>
</template>
```

### Alignments

```vue
<template>
  <n-space align="start" style="height: 100px; background: #f5f5f5">
    <n-button size="small">Small</n-button>
    <n-button size="large">Large</n-button>
    <div style="height: 80px; background: #ccc">Fixed height</div>
  </n-space>
</template>
```

## Card

### Basic Card

```vue
<template>
  <n-card title="Card Title">
    Card content
  </n-card>
</template>
```

### Card with Header Extra

```vue
<template>
  <n-card title="Users">
    <template #header-extra>
      <n-button text>
        <template #icon>
          <n-icon :component="RefreshIcon" />
        </template>
        Refresh
      </n-button>
    </template>
    Card content
  </n-card>
</template>
```

### Card with Actions

```vue
<template>
  <n-card title="Post Title" hoverable>
    <p>Card content here...</p>
    <template #action>
      <n-space>
        <n-button>Cancel</n-button>
        <n-button type="primary">Submit</n-button>
      </n-space>
    </template>
    <template #footer>
      #tag1 #tag2
    </template>
  </n-card>
</template>
```

### Segmented Card

```vue
<template>
  <n-card :segmented="{
    content: true,
    footer: 'soft'
  }">
    <template #header>
      Custom Header
    </template>
    Content with segmented style
    <template #footer>
      Footer content
    </template>
  </n-card>
</template>
```

### Card Sizes

```vue
<template>
  <n-space>
    <n-card title="Small" size="small" style="width: 200px">
      Small card
    </n-card>
    <n-card title="Medium" size="medium" style="width: 200px">
      Medium card (default)
    </n-card>
    <n-card title="Large" size="large" style="width: 200px">
      Large card
    </n-card>
    <n-card title="Huge" size="huge" style="width: 200px">
      Huge card
    </n-card>
  </n-space>
</template>
```

## Divider

### Horizontal Divider

```vue
<template>
  <div>
    <p>Content above</p>
    <n-divider />
    <p>Content below</p>
  </div>
</template>
```

### Divider with Title

```vue
<template>
  <n-divider title-placement="left">Left Title</n-divider>
  <n-divider title-placement="center">Center Title</n-divider>
  <n-divider title-placement="right">Right Title</n-divider>
</template>
```

### Vertical Divider

```vue
<template>
  <n-space>
    <span>Text</span>
    <n-divider vertical />
    <n-a>Link</n-a>
    <n-divider vertical />
    <n-a>Link</n-a>
  </n-space>
</template>
```

### Dashed Divider

```vue
<template>
  <n-divider dashed>
    Dashed Style
  </n-divider>
</template>
```

## Common Layout Patterns

### Dashboard Grid

```vue
<template>
  <n-grid cols="1 s:2 m:4" :x-gap="16" :y-gap="16">
    <n-grid-item>
      <n-card title="Total Users">
        <n-statistic tabular-nums>
          <n-number-animation ref="numberAnimationInstRef" :from="0" :to="12039" />
        </n-statistic>
      </n-card>
    </n-grid-item>
    <n-grid-item>
      <n-card title="Active">
        <n-statistic tabular-nums>
          <n-number-animation :from="0" :to="4282" />
        </n-statistic>
      </n-card>
    </n-grid-item>
    <n-grid-item>
      <n-card title="Orders">
        <n-statistic tabular-nums>
          <n-number-animation :from="0" :to="892" />
        </n-statistic>
      </n-card>
    </n-grid-item>
    <n-grid-item>
      <n-card title="Revenue">
        <n-statistic tabular-nums prefix="$">
          <n-number-animation :from="0" :to="28492" />
        </n-statistic>
      </n-card>
    </n-grid-item>
  </n-grid>
</template>
```

### Form Layout

```vue
<template>
  <n-card title="User Information">
    <n-grid cols="1 m:2" :x-gap="24">
      <n-grid-item>
        <n-form-item label="First Name">
          <n-input v-model:value="form.firstName" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item label="Last Name">
          <n-input v-model:value="form.lastName" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item span="2">
        <n-form-item label="Address">
          <n-input v-model:value="form.address" type="textarea" />
        </n-form-item>
      </n-grid-item>
    </n-grid>
  </n-card>
</template>
```

### List with Cards

```vue
<template>
  <n-grid cols="1 s:2 m:3" :x-gap="16" :y-gap="16">
    <n-grid-item v-for="item in items" :key="item.id">
      <n-card hoverable @click="selectItem(item)">
        <template #cover>
          <img :src="item.image" style="height: 200px; object-fit: cover">
        </template>
        <h3>{{ item.title }}</h3>
        <p style="color: #666">{{ item.description }}</p>
        <template #action>
          <n-space>
            <n-button size="small">Edit</n-button>
            <n-button size="small" type="error">Delete</n-button>
          </n-space>
        </template>
      </n-card>
    </n-grid-item>
  </n-grid>
</template>
```

## Key Types

```ts
import type {
  LayoutProps,
  LayoutInst,
  GridProps,
  GridItemProps,
  FlexProps,
  SpaceProps,
  CardProps,
  CardInst,
  DividerProps
} from 'naive-ui'
```

## Responsive Breakpoints

| Name | Breakpoint | Width |
|------|------------|-------|
| `cols` | Default | < 640px |
| `s:` | Small | >= 640px |
| `m:` | Medium | >= 1024px |
| `l:` | Large | >= 1280px |
| `xl:` | Extra Large | >= 1536px |


