---
name: component-menu
description: Menu navigation component with recursive rendering and router integration
---

# Menu & Navigation

Navigation components including Menu, Dropdown, Breadcrumb, and Tabs.

## Menu

### Basic Usage

```vue
<script setup lang="ts">
import type { MenuOption } from 'naive-ui'
import { h, ref } from 'vue'
import { RouterLink } from 'vue-router'

const menuOptions: MenuOption[] = [
  {
    label: 'Dashboard',
    key: 'dashboard',
    icon: renderIcon(DashboardIcon)
  },
  {
    label: 'Users',
    key: 'users',
    icon: renderIcon(PeopleIcon),
    children: [
      { label: 'All Users', key: 'users-list' },
      { label: 'Roles', key: 'users-roles' }
    ]
  },
  {
    label: 'Settings',
    key: 'settings',
    icon: renderIcon(SettingsIcon),
    children: [
      {
        label: 'General',
        key: 'settings-general',
        children: [
          { label: 'Site', key: 'settings-general-site' },
          { label: 'Email', key: 'settings-general-email' }
        ]
      },
      { label: 'Security', key: 'settings-security' }
    ]
  }
]

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const activeKey = ref<string>('dashboard')
const collapsed = ref(false)
</script>

<template>
  <n-menu
    v-model:value="activeKey"
    :collapsed="collapsed"
    :collapsed-width="64"
    :options="menuOptions"
    @update:value="handleMenuSelect"
  />
</template>
```

### Router Integration

```vue
<script setup lang="ts">
import type { MenuOption } from 'naive-ui'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()

const menuOptions: MenuOption[] = [
  {
    label: () => h(RouterLink, { to: '/' }, { default: () => 'Home' }),
    key: 'home',
    icon: renderIcon(HomeIcon)
  },
  {
    label: () => h(RouterLink, { to: '/about' }, { default: () => 'About' }),
    key: 'about',
    icon: renderIcon(InfoIcon)
  },
  {
    label: 'Products',
    key: 'products',
    icon: renderIcon(CartIcon),
    children: [
      {
        label: () => h(RouterLink, { to: '/products' }, { default: () => 'All Products' }),
        key: 'products-list'
      },
      {
        label: () => h(RouterLink, { to: '/products/categories' }, { default: () => 'Categories' }),
        key: 'products-categories'
      }
    ]
  }
]

// Auto-select based on route
const activeKey = computed(() => {
  return route.name as string || 'home'
})
</script>
```

### Accordion Mode

```vue
<template>
  <n-menu
    :options="menuOptions"
    accordion
    :default-expanded-keys="['users']"
  />
</template>
```

### Collapsed Menu

```vue
<template>
  <n-layout has-sider>
    <n-layout-sider
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="240"
      :collapsed="collapsed"
      show-trigger
      @collapse="collapsed = true"
      @expand="collapsed = false"
    >
      <n-menu
        :collapsed="collapsed"
        :collapsed-width="64"
        :collapsed-icon-size="22"
        :options="menuOptions"
      />
    </n-layout-sider>
    <n-layout-content>
      Content
    </n-layout-content>
  </n-layout>
</template>
```

## Dropdown

### Basic Usage

```vue
<script setup lang="ts">
import type { DropdownOption } from 'naive-ui'

const options: DropdownOption[] = [
  {
    label: 'Edit',
    key: 'edit',
    icon: renderIcon(EditIcon)
  },
  {
    label: 'Delete',
    key: 'delete',
    icon: renderIcon(TrashIcon),
    type: 'error'
  },
  {
    type: 'divider',
    key: 'd1'
  },
  {
    label: 'More',
    key: 'more',
    children: [
      { label: 'Copy', key: 'copy' },
      { label: 'Move', key: 'move' }
    ]
  }
]

const handleSelect = (key: string) => {
  switch (key) {
    case 'edit':
      handleEdit()
      break
    case 'delete':
      handleDelete()
      break
  }
}
</script>

<template>
  <n-dropdown :options="options" @select="handleSelect">
    <n-button>Actions</n-button>
  </n-dropdown>
</template>
```

### Trigger on Right Click

```vue
<template>
  <n-dropdown :options="options" trigger="contextmenu">
    <div class="context-menu-area">
      Right click here
    </div>
  </n-dropdown>
</template>

<style>
.context-menu-area {
  height: 200px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
```

## Breadcrumb

### Basic Usage

```vue
<script setup lang="ts">
const breadcrumbOptions = [
  { label: 'Home', to: '/' },
  { label: 'Products', to: '/products' },
  { label: 'Category', to: '/products/category' },
  { label: 'Item Detail' }
]
</script>

<template>
  <n-breadcrumb>
    <n-breadcrumb-item
      v-for="item in breadcrumbOptions"
      :key="item.label"
      :href="item.to"
    >
      {{ item.label }}
    </n-breadcrumb-item>
  </n-breadcrumb>
</template>
```

### With Router

```vue
<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const breadcrumbs = computed(() => {
  const matched = route.matched
  return matched.map(route => ({
    label: route.meta?.title || route.name,
    to: route.path
  }))
})

const handleClick = (path: string) => {
  router.push(path)
}
</script>

<template>
  <n-breadcrumb>
    <n-breadcrumb-item
      v-for="(item, index) in breadcrumbs"
      :key="index"
      :clickable="!!item.to"
      @click="item.to && handleClick(item.to)"
    >
      {{ item.label }}
    </n-breadcrumb-item>
  </n-breadcrumb>
</template>
```

## Tabs

> **Warning:** `n-tabs` will extract the default tab value from its default slot, triggering a Vue slot warning in certain situations. To avoid seeing the warning, explicitly provide a `default-value` prop on the component.

### Basic Usage

```vue
<script setup lang="ts">
import type { TabsInst } from 'naive-ui'

const tabsRef = ref<TabsInst | null>(null)
const activeTab = ref('users')

const panes = [
  { name: 'users', tab: 'Users', component: UserList },
  { name: 'roles', tab: 'Roles', component: RoleList },
  { name: 'permissions', tab: 'Permissions', component: PermissionList }
]

const addTab = () => {
  panes.push({ name: 'new', tab: 'New Tab', component: NewComponent })
}

const removeTab = (name: string) => {
  const index = panes.findIndex(p => p.name === name)
  if (index > -1) {
    panes.splice(index, 1)
  }
}
</script>

<template>
  <n-tabs
    v-model:value="activeTab"
    type="card"
    closable
    @close="removeTab"
  >
    <n-tab-pane
      v-for="pane in panes"
      :key="pane.name"
      :name="pane.name"
      :tab="pane.tab"
    >
      <component :is="pane.component" />
    </n-tab-pane>
  </n-tabs>
  <n-button @click="addTab">Add Tab</n-button>
</template>
```

### Dynamic Tabs

```vue
<script setup lang="ts">
interface TabItem {
  key: string
  label: string
  component: Component
  props?: Record<string, any>
}

const tabs = ref<TabItem[]>([
  { key: 'home', label: 'Home', component: HomeView }
])
const activeKey = ref('home')

const openTab = (item: TabItem) => {
  // Check if tab already exists
  const existing = tabs.value.find(t => t.key === item.key)
  if (!existing) {
    tabs.value.push(item)
  }
  activeKey.value = item.key
}

const closeTab = (key: string) => {
  const index = tabs.value.findIndex(t => t.key === key)
  if (index > -1) {
    tabs.value.splice(index, 1)
    // Switch to another tab if closing active
    if (activeKey.value === key && tabs.value.length > 0) {
      activeKey.value = tabs.value[Math.min(index, tabs.value.length - 1)].key
    }
  }
}
</script>

<template>
  <n-tabs
    v-model:value="activeKey"
    type="card"
    closable
    @close="closeTab"
  >
    <n-tab-pane
      v-for="tab in tabs"
      :key="tab.key"
      :name="tab.key"
      :tab="tab.label"
    >
      <component :is="tab.component" v-bind="tab.props" />
    </n-tab-pane>
  </n-tabs>
</template>
```

## PageHeader

```vue
<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const handleBack = () => {
  router.back()
}
</script>

<template>
  <n-page-header
    title="User Details"
    subtitle="User ID: 12345"
    @back="handleBack"
  >
    <template #avatar>
      <n-avatar src="https://example.com/avatar.png" />
    </template>
    <template #extra>
      <n-space>
        <n-button>Edit</n-button>
        <n-button type="error">Delete</n-button>
      </n-space>
    </template>
    <template #footer>
      <n-breadcrumb>
        <n-breadcrumb-item>Home</n-breadcrumb-item>
        <n-breadcrumb-item>Users</n-breadcrumb-item>
        <n-breadcrumb-item>Details</n-breadcrumb-item>
      </n-breadcrumb>
    </template>
  </n-page-header>
</template>
```

## Layout Patterns

### Admin Layout

```vue
<template>
  <n-layout style="height: 100vh">
    <n-layout-header bordered style="height: 64px; padding: 0 24px">
      <n-space align="center" justify="space-between" style="height: 100%">
        <div class="logo">Admin</div>
        <n-space>
          <n-badge :value="5">
            <n-button quaternary circle>
              <n-icon :component="NotificationsIcon" />
            </n-button>
          </n-badge>
          <n-dropdown :options="userOptions">
            <n-button quaternary>
              <n-avatar size="small" src="/avatar.png" />
              Admin
            </n-button>
          </n-dropdown>
        </n-space>
      </n-space>
    </n-layout-header>

    <n-layout has-sider style="height: calc(100vh - 64px)">
      <n-layout-sider
        bordered
        collapse-mode="width"
        :collapsed-width="64"
        :width="240"
        :native-scrollbar="false"
      >
        <n-menu :options="menuOptions" />
      </n-layout-sider>

      <n-layout-content style="padding: 24px">
        <n-breadcrumb style="margin-bottom: 16px">
          <n-breadcrumb-item>Home</n-breadcrumb-item>
          <n-breadcrumb-item>Dashboard</n-breadcrumb-item>
        </n-breadcrumb>
        <router-view />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>
```

## Key Types

```ts
import type {
  MenuOption,
  MenuInst,
  DropdownOption,
  DropdownGroupOption,
  TabsInst,
  TabPaneProps
} from 'naive-ui'
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Menu not highlighting | Key mismatch | Ensure menu key matches route name |
| Dropdown not closing | Manual control needed | Use `show` prop with `on-clickoutside` |
| Tabs content not updating | Component caching | Use `:key` on component or disable keep-alive |
| Breadcrumb not reflecting route | Static data | Use `route.matched` for dynamic breadcrumbs |


