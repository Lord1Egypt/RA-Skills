# Fab 悬浮按钮


## 组件概况

Fab（Floating Action Button）悬浮按钮组件是一个固定在屏幕边缘的可交互按钮，支持拖拽移动、多方向展开子菜单、自定义主题色和触发器样式。该组件适用于快速操作入口场景，可放置于屏幕四个角落或四边中点位置，展开时通过过渡动画展示多个子操作按钮，并内置多实例互斥管理机制，确保同一时间仅有一个 Fab 处于展开状态。

## 核心功能描述

- **多位置定位**：支持 8 种位置选项 —— `left-top`、`right-top`、`left-bottom`、`right-bottom`、`left-center`、`right-center`、`top-center`、`bottom-center`
- **四方向展开**：子菜单支持 `top`（上）、`bottom`（下）、`left`（左）、`right`（右）四个方向弹出，弹出方向与位置独立配置
- **拖拽吸附**：开启 `draggable` 后可自由拖动按钮，松手后自动吸附到屏幕左侧或右侧边界
- **可展开模式**：`expandable` 控制点击时是否切换菜单展开/收起状态；关闭后点击仅触发 `click` 事件
- **多实例互斥**：多个 Fab 实例共存时，展开当前实例会自动收起其他实例，通过队列机制管理
- **自定义触发器**：支持通过 `#trigger` 插槽自定义触发按钮外观，替代默认的圆形图标按钮
- **主题类型**：支持 `primary`、`success`、`info`、`warning`、`error`、`default` 共 6 种按钮类型
- **图标切换**：展开与收起状态分别使用 `activeIcon` 和 `inactiveIcon` 图标，默认展开显示 `close`、收起显示 `add`
- **边界保护**：拖拽过程中按钮始终被限制在安全区域内，不会超出屏幕或进入状态栏
- **双 v-model 支持**：通过 `v-model:active` 控制展开状态，支持外部程序化控制
- **CSS 过渡动画**：子菜单展开/收起使用 300ms cubic-bezier 缓动动画，吸附拖动使用 300ms ease 过渡
- **暗色模式支持**：内置 dark 主题样式，自动跟随系统主题切换

## 适用业务场景

- **快捷操作入口**：页面右下角的常用操作集合，如添加、编辑、删除、分享等
- **多功能菜单**：需要展示多个关联操作的场景，如内容创作工具栏（点赞、收藏、投币、分享）
- **全局辅助功能**：悬浮于页面之上的辅助功能入口，如返回顶部、帮助中心、反馈入口
- **拖拽式快捷方式**：用户可自定义按钮位置的场景，如工具面板、快捷键入口
- **自定义触发入口**：使用自定义按钮样式替代默认圆形按钮的场景，如带文字的分享按钮、品牌色按钮

## API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| active | boolean | `false` | 否 | 是否激活（展开子菜单），支持 `v-model:active` |
| type | `'primary' \| 'success' \| 'info' \| 'warning' \| 'error' \| 'default'` | `'primary'` | 否 | 悬浮按钮类型 |
| size | number | `50` | 否 | 悬浮按钮大小，单位为像素（px） |
| position | `'left-top' \| 'right-top' \| 'left-bottom' \| 'right-bottom' \| 'left-center' \| 'right-center' \| 'top-center' \| 'bottom-center'` | `'right-bottom'` | 否 | 悬浮按钮在屏幕上的位置 |
| direction | `'top' \| 'right' \| 'bottom' \| 'left'` | `'top'` | 否 | 子菜单弹出方向 |
| disabled | boolean | `false` | 否 | 是否禁用按钮 |
| inactiveIcon | string | `'add'` | 否 | 按钮未展开时的图标名称 |
| activeIcon | string | `'close'` | 否 | 按钮展开时的图标名称 |
| zIndex | number | `99` | 否 | 自定义悬浮按钮层级 |
| draggable | boolean | `false` | 否 | 是否可拖动 |
| gap | `Record<'top' \| 'right' \| 'bottom' \| 'left', number>` | `{}` | 否 | 悬浮按钮与屏幕边缘的间距（像素），分别控制四边间距 |
| expandable | boolean | `true` | 否 | 点击时是否切换菜单展开/收起状态；关闭后点击仅触发 `click` 事件 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点类名 |

#### position 可选值说明

| 值 | 位置描述 |
|---|---------|
| `left-top` | 左上角 |
| `right-top` | 右上角 |
| `left-bottom` | 左下角 |
| `right-bottom` | 右下角 |
| `left-center` | 左侧中点 |
| `right-center` | 右侧中点 |
| `top-center` | 顶部中点 |
| `bottom-center` | 底部中点 |

#### direction 可选值说明

| 值 | 弹出方向描述 |
|---|-------------|
| `top` | 向上弹出（子菜单位于按钮上方） |
| `bottom` | 向下弹出（子菜单位于按钮下方） |
| `left` | 向左弹出（子菜单位于按钮左侧） |
| `right` | 向右弹出（子菜单位于按钮右侧） |

### Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| update:active | `boolean` | 激活状态变化时触发，传入当前激活状态值 |
| click | - | 点击按钮时触发，仅在 `expandable` 为 `false` 或 `disabled` 为 `false` 且非可展开模式时触发 |

### Methods

通过 `ref` 获取组件实例后可调用以下方法：

| 方法名称 | 参数 | 说明 |
|---------|------|------|
| open | - | 展开子菜单（设置 `active` 为 `true`） |
| close | - | 收起子菜单（设置 `active` 为 `false`） |

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 子菜单内容，放置展开后的子操作按钮 |
| trigger | - | 自定义触发器按钮内容，替代默认的圆形图标按钮 |

## 使用示例

### 示例 1：基本用法

展示悬浮按钮在不同主题色和位置下的效果，以及菜单弹出方向的切换。

```vue
<template>
  <view>
    <!-- 基础 Fab，默认右下角位置，向上弹出菜单 -->
    <wd-fab>
      <wd-button type="primary" round custom-class="custom-button">
        <wd-icon name="logo-github-o" size="22px"></wd-icon>
      </wd-button>
      <wd-button type="success" round custom-class="custom-button">
        <wd-icon name="star" size="22px"></wd-icon>
      </wd-button>
      <wd-button type="error" round custom-class="custom-button">
        <wd-icon name="finance" size="22px"></wd-icon>
      </wd-button>
      <wd-button type="warning" round custom-class="custom-button">
        <wd-icon name="good" size="22px"></wd-icon>
      </wd-button>
    </wd-fab>

    <!-- 指定位置为左上角 -->
    <wd-fab position="left-top">
      <wd-button type="primary" round custom-class="custom-button">
        <wd-icon name="add" size="22px"></wd-icon>
      </wd-button>
      <wd-button type="success" round custom-class="custom-button">
        <wd-icon name="edit" size="22px"></wd-icon>
      </wd-button>
    </wd-fab>

    <!-- 指定弹出方向为右侧 -->
    <wd-fab position="right-center" direction="right">
      <wd-button type="primary" round custom-class="custom-button">
        <wd-icon name="setting" size="22px"></wd-icon>
      </wd-button>
      <wd-button type="info" round custom-class="custom-button">
        <wd-icon name="help" size="22px"></wd-icon>
      </wd-button>
    </wd-fab>
  </view>
</template>
<script lang="ts" setup>
</script>
<style lang="scss" scoped>
  :deep(.custom-button) {
    min-width: auto !important;
    box-sizing: border-box;
    width: 32px !important;
    height: 32px !important;
    border-radius: 16px !important;
    margin: 8rpx;
  }
</style>
```

子菜单内容通过默认插槽传入，可放置任意数量的子操作按钮。子按钮建议使用较小的尺寸（如 32px），并通过 `custom-class` 设置统一的样式。`position` 控制主按钮在屏幕中的位置，`direction` 控制子菜单弹出方向，两者可自由组合使用。

### 示例 2：拖拽与禁用

展示悬浮按钮的拖拽吸附功能以及禁用状态。

```vue
<template>
  <view>
    <!-- 可拖动的悬浮按钮，松手后自动吸附到屏幕左右两侧 -->
    <wd-fab draggable>
      <wd-button type="primary" round custom-class="custom-button">
        <wd-icon name="add" size="22px"></wd-icon>
      </wd-button>
      <wd-button type="success" round custom-class="custom-button">
        <wd-icon name="star" size="22px"></wd-icon>
      </wd-button>
      <wd-button type="error" round custom-class="custom-button">
        <wd-icon name="delete" size="22px"></wd-icon>
      </wd-button>
    </wd-fab>

    <!-- 禁用状态的悬浮按钮，无法点击和拖拽 -->
    <wd-fab :disabled="true">
      <wd-button type="info" round custom-class="custom-button">
        <wd-icon name="setting" size="22px"></wd-icon>
      </wd-button>
    </wd-fab>

    <!-- 自定义按钮大小和层级 -->
    <wd-fab :size="60" :z-index="100" position="top-center">
      <wd-button type="warning" round custom-class="custom-button">
        <wd-icon name="warning" size="30px"></wd-icon>
      </wd-button>
    </wd-fab>
  </view>
</template>
<script lang="ts" setup>
</script>
<style lang="scss" scoped>
  :deep(.custom-button) {
    min-width: auto !important;
    box-sizing: border-box;
    width: 32px !important;
    height: 32px !important;
    border-radius: 16px !important;
    margin: 8rpx;
  }
</style>
```

设置 `draggable` 为 `true` 后，用户可以通过触摸拖动改变按钮位置，松手时按钮会根据其中心点与屏幕中心点的关系自动吸附到左侧或右侧边缘。`disabled` 为 `true` 时按钮不可点击也不可拖拽。`size` 属性控制主按钮的宽高（像素），`zIndex` 控制层级。

### 示例 3：自定义触发器

使用 `#trigger` 插槽自定义触发按钮的外观，替代默认的圆形图标按钮。

```vue
<template>
  <view>
    <!-- 自定义触发器，使用带文字的矩形按钮 -->
    <wd-fab position="left-bottom" :draggable="false" :expandable="false">
      <template #trigger>
        <wd-button icon="share" type="error" @click="handleShare">
          分享给朋友
        </wd-button>
      </template>
    </wd-fab>

    <!-- 自定义触发器，圆形图标按钮但使用不同图标 -->
    <wd-fab position="right-top" inactive-icon="more" active-icon="close">
      <template #trigger>
        <wd-button type="success" round custom-class="custom-trigger">
          <wd-icon name="menu" size="24px"></wd-icon>
        </wd-button>
      </template>
      <wd-button type="primary" round custom-class="custom-button">
        <wd-icon name="edit" size="22px"></wd-icon>
      </wd-button>
      <wd-button type="warning" round custom-class="custom-button">
        <wd-icon name="delete" size="22px"></wd-icon>
      </wd-button>
    </wd-fab>
  </view>
</template>
<script lang="ts" setup>
  function handleShare() {
    console.log('分享给朋友')
  }
</script>
<style lang="scss" scoped>
  :deep(.custom-trigger) {
    min-width: auto !important;
    box-sizing: border-box;
    width: 50px !important;
    height: 50px !important;
    border-radius: 25px !important;
  }
  :deep(.custom-button) {
    min-width: auto !important;
    box-sizing: border-box;
    width: 32px !important;
    height: 32px !important;
    border-radius: 16px !important;
    margin: 8rpx;
  }
</style>
```

通过 `#trigger` 插槽可以完全自定义主按钮的外观。当使用自定义触发器时，`type`、`size`、`inactiveIcon`、`activeIcon` 等属性不会应用到触发器上，需要自行在插槽内容中设置。设置 `expandable` 为 `false` 时，点击触发器不会切换展开/收起状态，仅触发 `click` 事件。

### 示例 4：外部控制展开状态

通过 `v-model:active` 和组件方法实现外部程序化控制展开/收起。

```vue
<template>
  <view>
    <!-- 通过外部按钮控制 Fab 展开/收起 -->
    <wd-button type="primary" round @click="toggleFab">
      {{ active ? '收起菜单' : '展开菜单' }}
    </wd-button>

    <wd-button type="success" round @click="fabRef?.open()">
      程序化展开
    </wd-button>

    <wd-button type="error" round @click="fabRef?.close()">
      程序化收起
    </wd-button>

    <wd-fab ref="fabRef" v-model:active="active">
      <wd-button type="primary" round custom-class="custom-button">
        <wd-icon name="add" size="22px"></wd-icon>
      </wd-button>
      <wd-button type="success" round custom-class="custom-button">
        <wd-icon name="star" size="22px"></wd-icon>
      </wd-button>
      <wd-button type="warning" round custom-class="custom-button">
        <wd-icon name="good" size="22px"></wd-icon>
      </wd-button>
    </wd-fab>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import type { FabInstance } from '@/uni_modules/wot-ui-plus/components/wd-fab/types'

  const active = ref<boolean>(false)
  const fabRef = ref<FabInstance>()

  function toggleFab() {
    active.value = !active.value
  }
</script>
<style lang="scss" scoped>
  :deep(.custom-button) {
    min-width: auto !important;
    box-sizing: border-box;
    width: 32px !important;
    height: 32px !important;
    border-radius: 16px !important;
    margin: 8rpx;
  }
</style>
```

通过 `v-model:active` 实现双向绑定，外部可通过修改绑定值控制展开/收起状态。也可通过 `ref` 获取组件实例后调用 `open()` 和 `close()` 方法。当 Fab 被激活展开时，会自动收起页面中其他处于展开状态的 Fab 实例。

### 示例 5：配置边缘间距与图标切换

通过 `gap` 属性设置按钮与屏幕边缘的间距，以及自定义展开/收起图标。

```vue
<template>
  <view>
    <!-- 自定义四周边距，避免与底部 TabBar 重叠 -->
    <wd-fab :gap="{ bottom: 80, right: 20 }" inactive-icon="add" active-icon="close">
      <wd-button type="primary" round custom-class="custom-button">
        <wd-icon name="add" size="22px"></wd-icon>
      </wd-button>
      <wd-button type="success" round custom-class="custom-button">
        <wd-icon name="edit" size="22px"></wd-icon>
      </wd-button>
      <wd-button type="error" round custom-class="custom-button">
        <wd-icon name="delete" size="22px"></wd-icon>
      </wd-button>
    </wd-fab>

    <!-- 左侧居中，向下弹出 -->
    <wd-fab position="left-center" direction="bottom" :gap="{ left: 20 }" inactive-icon="menu" active-icon="close">
      <wd-button type="info" round custom-class="custom-button">
        <wd-icon name="setting" size="22px"></wd-icon>
      </wd-button>
      <wd-button type="warning" round custom-class="custom-button">
        <wd-icon name="help" size="22px"></wd-icon>
      </wd-button>
    </wd-fab>
  </view>
</template>
<script lang="ts" setup>
</script>
<style lang="scss" scoped>
  :deep(.custom-button) {
    min-width: auto !important;
    box-sizing: border-box;
    width: 32px !important;
    height: 32px !important;
    border-radius: 16px !important;
    margin: 8rpx;
  }
</style>
```

`gap` 属性接受一个对象，可分别设置 `top`、`right`、`bottom`、`left` 四个方向的间距（单位 px），默认各边均为 15px。在页面底部有 TabBar 或导航栏的场景中，建议增大对应方向的间距以避免按钮被遮挡。`inactiveIcon` 和 `activeIcon` 用于设置收起和展开状态下按钮上显示的图标。

## 注意事项

1. **多实例互斥管理**：页面中同时存在多个 Fab 组件时，展开其中一个会自动收起其他已展开的 Fab，这是通过内部队列机制实现的。如需关闭所有 Fab，可调用 `useQueue().closeOutside()` 方法
2. **拖拽吸附逻辑**：开启 `draggable` 后，按钮拖拽结束时会以按钮中心点与屏幕中心点的 x 坐标比较结果来决定吸附到左侧或右侧，吸附过程带有 300ms ease 过渡动画
3. **expandable 与 click 事件的关系**：`expandable` 为 `true`（默认值）时，点击按钮会切换展开/收起状态，不会触发 `click` 事件；`expandable` 为 `false` 时，点击按钮会触发 `click` 事件，不切换展开状态
4. **自定义触发器的属性隔离**：使用 `#trigger` 插槽时，主组件的 `type`、`size`、`inactiveIcon`、`activeIcon` 属性不会应用到触发器按钮上，需要在插槽内容中自行设置样式和图标
5. **边界保护机制**：拖拽过程中按钮位置受 `gap` 定义的边界约束，确保按钮不会移出屏幕可视区域。顶部边界在 H5 环境下会自动加上 `windowTop` 值（安全区域高度）
6. **子菜单弹出方向独立于位置**：`direction`（弹出方向）与 `position`（按钮位置）是两个独立的属性，例如可以将按钮放在 `right-bottom`（右下角），同时设置 `direction="left"`（向左弹出）
7. **size 属性的作用范围**：`size` 属性仅控制主触发器按钮的宽高（单位 px），不影响子菜单中按钮的尺寸。图标大小默认为 `size / 2`
8. **初始化延迟**：组件挂载后使用 `requestAnimationFrame` 异步获取按钮尺寸和初始化位置，初始化完成前按钮不可见（通过 `visibility: hidden` 隐藏），以避免位置跳闪
9. **暗色模式自动适配**：组件已内置暗色主题样式，会自动跟随系统主题切换，无需额外配置
