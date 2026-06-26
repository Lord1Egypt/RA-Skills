# Sticky 粘性定位


## 组件概况

Sticky 粘性定位组件由 `wd-sticky` 和 `wd-sticky-box` 两个关联组件组成。`wd-sticky` 用于实现元素的粘性定位效果，当页面滚动到指定位置时，元素会固定在视口顶部。`wd-sticky-box` 是一个容器组件，用于包裹 `wd-sticky`，限制吸顶元素的活动范围，使其仅在容器边界内吸顶。该组件通过 IntersectionObserver API 实现滚动监听，适用于需要固定在页面顶部的导航栏、筛选条件、操作按钮等场景。

## 核心功能描述

- **基础吸顶**：将 `wd-sticky` 包裹需要吸顶的内容，滚动到页面顶部时自动固定定位，滚动回原位置时恢复文档流
- **吸顶距离控制**：通过 `offset-top` 属性设置元素距离视口顶部的偏移距离，实现吸顶后与顶部留白
- **容器范围限制**：将 `wd-sticky` 放置在 `wd-sticky-box` 内部，吸顶元素仅在容器范围内生效，离开容器后自动恢复为绝对定位
- **动态内容适配**：内置 `wd-resize` 监听子组件尺寸变化，当内容高度或宽度动态改变时自动重新计算吸顶位置
- **层级控制**：通过 `z-index` 属性控制吸顶元素的堆叠层级，确保在页面滚动时不被其他元素遮挡
- **H5 端导航栏适配**：H5 端自动识别并适配 44px 导航栏高度，确保吸顶元素位于导航栏下边沿
- **动态插入支持**：组件支持在运行时动态插入内容，插入后自动重新建立滚动监听

## 适用业务场景

- **列表页筛选栏**：在商品列表、数据列表等长页面中，筛选条件和排序控件需要始终保持在顶部可视区域，方便用户随时切换筛选条件
- **文章/详情页目录导航**：在长文章或产品详情页面中，目录导航需要在滚动时固定在顶部，帮助用户快速定位到不同章节
- **多 Tab 切换头部**：包含多个 Tab 标签页的内容区域，Tab 导航在滚动时吸顶，保持导航可见性
- **表单操作栏**：在长表单页面中，提交按钮和重要操作信息在滚动到一定位置后固定在顶部，提升操作便捷性

## API

### wd-sticky Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| offsetTop | number | 0 | 否 | 吸顶距离，元素距离视口顶部多少像素时触发吸顶 |
| zIndex | number | 1 | 否 | 吸顶元素的层级堆叠顺序，值越大越靠前 |
| customStyle | string | '' | 否 | 自定义组件根元素样式 |
| customClass | string | '' | 否 | 自定义组件根元素类名 |

### wd-sticky Events

当前源码中未通过 `defineEmits` 派发自定义事件。

### wd-sticky Methods

通过 `defineExpose` 暴露以下方法：

| 方法名称 | 参数 | 说明 |
| --- | --- | --- |
| setPosition | boxLeaved: boolean, position: string, top: number | 手动设置吸顶位置状态，供 wd-sticky-box 内部调用 |

### wd-sticky Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 用于放置需要吸顶的内容，支持任意自定义内容 |

### wd-sticky-box Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| customStyle | string | '' | 否 | 自定义容器根元素样式 |
| customClass | string | '' | 否 | 自定义容器根元素类名 |

### wd-sticky-box Events

当前源码中未通过 `defineEmits` 派发自定义事件。

### wd-sticky-box Methods

当前源码中未通过 `defineExpose` 暴露实例方法。内部通过 provide/inject 机制与 `wd-sticky` 子组件通信。

### wd-sticky-box Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 用于包裹 `wd-sticky` 组件及其内容，定义吸顶元素的活动容器范围 |

## 使用示例

### 示例 1：基础吸顶

效果说明：将按钮包裹在 `wd-sticky` 中，页面滚动时按钮会在到达视口顶部时自动吸顶固定，向下滚动回原始位置后恢复文档流。

```vue
<template>
  <view style="height: 250vh">
    <view class="demo-block">
      <wd-sticky>
        <wd-button type="success">基础吸顶</wd-button>
      </wd-sticky>
    </view>
  </view>
</template>

<script setup lang="ts">
/* 本示例无需额外逻辑。 */
</script>

<style scoped lang="scss">
.demo-block {
  padding: 15px 0;
}
</style>
```

### 示例 2：设置吸顶距离

效果说明：通过 `offset-top` 属性设置吸顶距离为 50px，元素吸顶后距离视口顶部保留 50px 的间距，适用于顶部有导航栏或搜索框需要避让的场景。

```vue
<template>
  <view style="height: 250vh">
    <view class="demo-block">
      <wd-sticky :offset-top="50">
        <wd-button>吸顶距离 50px</wd-button>
      </wd-sticky>
    </view>
  </view>
</template>

<script setup lang="ts">
/* 本示例无需额外逻辑。 */
</script>

<style scoped lang="scss">
.demo-block {
  padding: 15px 0;
}
</style>
```

### 示例 3：相对容器吸顶

效果说明：将 `wd-sticky` 放置在 `wd-sticky-box` 容器内，吸顶元素仅在容器范围内生效。当滚动到容器底部边界时，元素会从固定定位切换为绝对定位，跟随容器一起滚动出视口。

```vue
<template>
  <view style="height: 250vh">
    <view class="demo-block">
      <wd-sticky-box>
        <view class="custom-container">
          <wd-sticky>
            <wd-button type="warning">相对容器吸顶</wd-button>
          </wd-sticky>
        </view>
      </wd-sticky-box>
    </view>
  </view>
</template>

<script setup lang="ts">
/* 本示例无需额外逻辑。 */
</script>

<style scoped lang="scss">
.demo-block {
  padding: 15px 0;
}

.custom-container {
  height: 120px;
  width: 100vw;
  background-color: #ffffff;
}
</style>
```

### 示例 4：容器吸顶 + 自定义吸顶距离

效果说明：结合 `wd-sticky-box` 和 `offset-top` 属性，在容器范围内吸顶的同时距离视口顶部保留 150px 间距，适用于页面头部存在多个固定元素的复杂场景。

```vue
<template>
  <view style="height: 250vh">
    <view class="demo-block">
      <wd-sticky-box>
        <view class="custom-container">
          <wd-sticky :offset-top="150">
            <wd-button type="warning">容器吸顶 + 150px 间距</wd-button>
          </wd-sticky>
        </view>
      </wd-sticky-box>
    </view>
  </view>
</template>

<script setup lang="ts">
/* 本示例无需额外逻辑。 */
</script>

<style scoped lang="scss">
.demo-block {
  padding: 15px 0;
}

.custom-container {
  height: 120px;
  width: 100vw;
  background-color: #ffffff;
}
</style>
```

### 示例 5：动态插入内容

效果说明：通过条件渲染控制 `wd-sticky` 内部内容的显示与隐藏，内容动态插入后组件会自动重新计算尺寸并建立滚动监听，无需手动处理。

```vue
<template>
  <view style="height: 250vh">
    <view class="demo-block">
      <wd-button type="info" plain @click="handleInsert">点击插入</wd-button>
      <wd-sticky>
        <wd-button type="error" v-if="show">动态生成的内容</wd-button>
      </wd-sticky>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)

function handleInsert() {
  show.value = true
}
</script>

<style scoped lang="scss">
.demo-block {
  padding: 15px 0;
}
</style>
```

## 注意事项

- **wd-sticky 必须搭配 wd-resize**：`wd-sticky` 内部依赖 `wd-resize` 组件监听内容尺寸变化，请确保在使用时不要移除或替换该内部依赖。
- **wd-sticky-box 与 wd-sticky 配对使用**：`wd-sticky-box` 需要通过 provide/inject 机制与内部的 `wd-sticky` 子组件通信实现容器范围吸顶，因此 `wd-sticky` 必须作为 `wd-sticky-box` 的直接后代或嵌套后代使用。
- **容器高度限制**：`wd-sticky` 内容的高度不应大于或等于 `wd-sticky-box` 容器的高度，否则吸顶逻辑无意义，组件会强制将定位设为 absolute。
- **IntersectionObserver 兼容性**：组件使用 `uni.createIntersectionObserver` 实现滚动监听，在不同平台（H5、小程序、App）的 IntersectionObserver API 行为可能存在差异，建议在目标平台进行充分测试。
- **H5 端导航栏适配**：H5 端会自动增加 44px 导航栏高度的偏移计算，包括吸顶位置计算和元素边界查询。其他端不受影响。
- **动态内容重算**：当 `wd-sticky` 或 `wd-sticky-box` 内部内容尺寸发生变化时，组件会自动清除旧的 IntersectionObserver 并重新创建，确保吸顶位置计算的准确性。
- **zIndex 层级建议**：`wd-sticky` 默认 zIndex 为 1，若页面中存在其他固定定位元素，请根据实际层级关系调高该值确保吸顶元素不被遮挡。
- **fixed 定位特性**：吸顶状态下元素使用 fixed 定位，会从文档流中脱离。`wd-sticky` 的根元素会保持相对定位并占据原始空间，避免页面出现布局跳动。
- **多平台 position 判断差异**：H5 和 APP-PLUS 端在判断吸顶触发条件时使用严格小于比较（`<`），其他端使用小于等于比较（`<=``），这是为了适配各平台渲染引擎的细微差异。
