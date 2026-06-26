# Overlay 遮罩层


## 组件概况

Overlay 遮罩层组件是一个用于覆盖在页面上的半透明黑色背景层，通常用于在用户交互过程中屏蔽底层内容的操作，同时支持通过插槽在遮罩层上嵌入自定义内容（如弹窗、提示框等）。该组件基于 wd-transition 实现淡入淡出的过渡动画效果，支持层级控制、滚动锁定等特性，适用于需要临时聚焦用户注意力的交互场景。

## 核心功能描述

- **半透明遮罩**：组件渲染为固定定位的全屏遮罩层，使用深色半透明背景（`rgba(0, 0, 0, 0.7)`），有效阻断用户对底层内容的操作
- **过渡动画**：内部基于 wd-transition 组件实现 fade 淡入淡出动画，可通过 duration 属性自定义动画时长
- **层级控制**：通过 zIndex 属性控制遮罩层在页面中的堆叠顺序，确保遮罩层正确覆盖目标内容
- **滚动锁定**：在 H5 平台支持通过 lockScroll 属性锁定背景滚动，锁定时蒙层里的内容也将无法滚动
- **点击事件**：支持监听遮罩层的点击事件，便于用户点击遮罩关闭弹窗等交互
- **内容嵌入**：通过默认插槽可在遮罩层上方嵌入任意自定义内容，如弹窗卡片、加载提示等

## 适用业务场景

- **弹窗背景遮罩**：作为 Dialog、Popup 等弹窗组件的底层遮罩，阻止用户操作弹窗外的内容
- **加载状态**：在页面加载数据时显示遮罩层配合加载提示，防止用户重复提交操作
- **操作引导**：在新手引导流程中使用遮罩层聚焦用户注意力到特定操作区域
- **图片预览**：在图片浏览场景中作为全屏预览的黑色背景层
- **表单确认**：在重要操作前弹出确认遮罩，确保用户明确操作意图

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| show | boolean | false | 否 | 是否展示遮罩层，通过 v-model 或 :show 双向控制显示/隐藏状态 |
| duration | number / object / boolean | 300 | 否 | 动画时长，单位为毫秒，支持传入数字、对象或布尔值（传递给 wd-transition 组件） |
| lockScroll | boolean | true | 否 | 是否锁定背景滚动，在 H5 平台生效，锁定时蒙层里的内容也将无法滚动 |
| zIndex | number | 10 | 否 | 遮罩层的层级堆叠顺序，值越大越靠前显示 |
| customStyle | string | '' | 否 | 自定义组件根元素的内联样式 |
| customClass | string | '' | 否 | 自定义组件根元素的样式类名 |

### Events

| 事件名称 | 回调参数 | 触发时机 |
| --- | --- | --- |
| click | - | 点击遮罩层时触发 |

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 用于在遮罩层上方嵌入自定义内容，如弹窗卡片、加载指示器等 |

### Methods

当前源码中未通过 `defineExpose` 暴露实例方法。

### 外部样式类

| 类名 | 说明 |
| --- | --- |
| wd-overlay | 遮罩层根节点样式类，可用于全局样式覆盖 |

## 使用示例

### 示例 1：基础用法

效果说明：展示遮罩层的基础使用方式，点击按钮显示遮罩层，点击遮罩层本身关闭。

```vue
<template>
  <wd-button type="primary" @click="show = true">显示遮罩层</wd-button>
  <wd-overlay :show="show" @click="show = false" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)
</script>

<style scoped lang="scss">
/* 本示例无需额外样式。 */
</style>
```

### 示例 2：嵌入自定义内容

效果说明：在遮罩层上嵌入一个居中的白色卡片容器，卡片内部包含开关控件和可滚动内容区域。点击遮罩层关闭，卡片内部区域使用 `@click.stop` 阻止事件冒泡避免误关闭。

```vue
<template>
  <wd-button type="primary" @click="show = true">嵌入内容</wd-button>

  <wd-overlay :show="show" @click="show = false">
    <view class="wrapper">
      <view class="content" @click.stop="">
        <view class="scroll">
          <view class="block" v-for="i in 10" :key="i" @click.stop="">{{ i }}</view>
        </view>
      </view>
    </view>
  </wd-overlay>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)
</script>

<style scoped lang="scss">
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.content {
  background-color: #fff;
  border-radius: 12px;
}

.scroll {
  height: 50vh;
  overflow-y: auto;
  width: 300px;
}

.block {
  width: 100%;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
```

### 示例 3：控制滚动锁定

效果说明：通过 lockScroll 属性控制是否锁定背景滚动。当 lockScroll 为 true 时，遮罩层及内部内容均无法滚动；为 false 时，内部内容可以正常滚动。此功能仅在 H5 平台生效。

```vue
<template>
  <wd-button type="primary" @click="show = true">锁定滚动演示</wd-button>

  <wd-overlay :show="show" @click="show = false" :lock-scroll="lockScroll">
    <view class="wrapper">
      <view class="content" @click.stop="">
        <view class="control-panel">
          <text>是否锁定滚动：</text>
          <wd-switch v-model="lockScroll" size="22px" />
        </view>
        <view class="scroll">
          <view class="block" v-for="i in 20" :key="i" @click.stop="">{{ i }}</view>
        </view>
      </view>
    </view>
  </wd-overlay>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)
const lockScroll = ref<boolean>(true)
</script>

<style scoped lang="scss">
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.content {
  background-color: #fff;
  border-radius: 12px;
  padding: 16px;
}

.control-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.scroll {
  height: 40vh;
  overflow-y: auto;
  width: 280px;
}

.block {
  width: 100%;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #f0f0f0;
}
</style>
```

### 示例 4：自定义层级与样式

效果说明：通过 zIndex 和 customStyle 属性自定义遮罩层的层级和背景透明度，适用于需要叠加多个遮罩层或调整遮罩深浅的场景。

```vue
<template>
  <wd-button type="primary" @click="show = true">半透明遮罩</wd-button>

  <wd-overlay
    :show="show"
    @click="show = false"
    :z-index="100"
    custom-style="background: rgba(0, 0, 0, 0.3);"
  >
    <view class="custom-content">
      <text class="custom-text">这是一个半透明遮罩</text>
    </view>
  </wd-overlay>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)
</script>

<style scoped lang="scss">
.custom-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.custom-text {
  color: #fff;
  font-size: 18px;
}
</style>
```

## 注意事项

1. **show 属性控制**：遮罩层的显示/隐藏完全由 show 属性控制，默认值为 false（隐藏）。请通过响应式变量绑定并在需要时切换其值。

2. **滚动锁定平台限制**：lockScroll 属性仅在 H5 平台生效（通过 `useLockScroll` composable 实现）。在小程序和 App 平台该属性不会产生效果，需通过其他方式（如 page-meta 组件）实现滚动锁定。

3. **点击事件冒泡处理**：当在遮罩层插槽中嵌入内容时，若希望点击内部内容不触发遮罩关闭，请在内部容器上使用 `@click.stop` 阻止事件冒泡。

4. **zIndex 层级规划**：默认 zIndex 为 10。若页面中存在其他浮层组件（如弹窗、下拉菜单等），请合理分配 zIndex 值确保遮罩层显示在正确层级。建议弹窗类组件的 zIndex 不低于 1000。

5. **全屏固定定位**：遮罩层使用 position: fixed 定位覆盖整个视口（left: 0; top: 0; right: 0; bottom: 0），无需额外设置宽高。

6. **过渡动画时长**：duration 属性传递给内部的 wd-transition 组件，默认值为 300 毫秒。可传入数字统一设置进入/退出时长，或传入对象分别控制，具体参考 Transition 组件文档。

7. **暗色主题适配**：组件内置暗色主题样式，在 `.wot-theme-dark` 容器下会自动切换为对应的深色遮罩背景。

8. **插槽内容定位**：嵌入遮罩层的内容默认位于遮罩上方（z-index 关系），建议通过 flex 布局或绝对定位自行控制内容位置。

9. **虚拟主机配置**：组件内部配置了 `virtualHost: true`，这意味着在小程序平台组件的根节点样式会直接生效，无需考虑额外的包装元素影响。
