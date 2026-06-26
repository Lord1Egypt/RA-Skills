# RootPortal 根门户

  
## 组件概况

RootPortal 根门户组件是一个用于将内容渲染到页面根节点的传送门组件。该组件主要用于解决在复杂层级结构中固定定位（fixed）失效的问题，将内容从当前 DOM 层级中脱离出来，传送到页面根节点下，确保弹窗、遮罩层等固定定位元素能够正确显示在页面最顶层。组件在不同平台采用不同的实现方案：H5 端使用 Teleport 组件，小程序端使用 root-portal，App 端使用 renderjs 实现。

## 核心功能描述

- **跨层级传送**：将组件内容传送到页面根节点，避免复杂 DOM 结构中的层级问题
- **多平台适配**：针对 H5、小程序、App 等不同平台采用最适合的实现方案
- **主题继承**：自动继承父级配置提供者的主题样式，保持视觉一致性
- **虚拟主机**：使用 virtualHost 选项，使组件样式隔离，不影响外部样式
- **全局样式支持**：支持通过 addGlobalClass 添加全局样式类
- **H5 端实现**：使用 Vue 3 的 Teleport 组件将内容传送至 body 标签
- **小程序端实现**：使用原生 root-portal 组件实现内容传送
- **App 端实现**：使用 renderjs 在原生层将元素追加到页面根节点

## 适用业务场景

- **弹窗层级问题**：在嵌套弹窗、模态框等场景中，解决 fixed 定位被父级容器遮挡的问题
- **全屏遮罩**：创建覆盖整个屏幕的遮罩层，确保不受父级 z-index 影响
- **全局提示**：全局消息提示、Toast、通知等需要脱离当前组件层级的场景
- **工具栏固定**：顶部导航、底部工具栏等需要固定在屏幕特定位置的元素
- **复杂布局**：在复杂的嵌套组件结构中，确保某些元素能显示在最顶层

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| - | RootPortal 组件无特殊 props 属性，所有属性会透传给根节点 | - | - | - | - |

### Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| - | RootPortal 组件不触发任何自定义事件 | - |

### Methods

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | RootPortal 组件不对外暴露任何方法 | - | - |

### Slots

| 插槽名 | 说明 |
|--------|------|
| default | 默认插槽，用于放置需要传送到底层的内容 |

## 使用示例

### 示例 1：基础用法

最基本的 RootPortal 使用方式，将内容传送到底层根节点。

```vue
<template>
  <view class="root-portal-demo">
    <demo-block title="基本用法">
      <wd-button type="primary" @click="showBasic = true">显示基本弹窗</wd-button>
      <wd-root-portal v-if="showBasic">
        <view class="basic-modal">
          <view class="basic-modal-content">
            <text class="basic-modal-title">基本弹窗</text>
            <text class="basic-modal-text">这是一个使用 root-portal 的基本弹窗示例</text>
            <wd-button type="primary" @click="showBasic = false">关闭</wd-button>
          </view>
        </view>
      </wd-root-portal>
    </demo-block>
  </view>
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  const showBasic = ref(false)
</script>

<style lang="scss" scoped>
  .root-portal-demo {
    padding: 16px;
  }

  .basic-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }

  .basic-modal-content {
    background-color: #fff;
    padding: 24px;
    border-radius: 12px;
    width: 280px;
    text-align: center;
  }

  .basic-modal-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 12px;
    display: block;
  }

  .basic-modal-text {
    font-size: 14px;
    color: #666;
    margin-bottom: 20px;
    display: block;
  }
</style>
```

该示例展示了 RootPortal 的基本用法。当点击按钮显示弹窗时，弹窗内容通过 RootPortal 传送到了页面根节点，避免了被父级容器的层级所限制，确保弹窗能够正常显示在最顶层。

### 示例 2：嵌套结构中的应用

在复杂嵌套结构中使用 RootPortal 解决层级问题。

```vue
<template>
  <view class="nested-demo">
    <view class="container">
      <view class="section">
        <view class="sub-section">
          <wd-button type="primary" @click="showNestedModal = true">在嵌套结构中显示弹窗</wd-button>
          
          <!-- 这里模拟一个复杂的嵌套结构 -->
          <view class="complex-wrapper" style="position: relative; z-index: 1;">
            <view class="nested-content">
              <p>这是一个复杂的嵌套结构</p>
              <p>内部有多个设置了 z-index 的元素</p>
              <p>普通的 fixed 定位可能会被遮挡</p>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 使用 RootPortal 确保弹窗显示在最顶层 -->
    <wd-root-portal v-if="showNestedModal">
      <view class="nested-modal-overlay" @click="showNestedModal = false">
        <view class="nested-modal-content" @click.stop>
          <h3>嵌套结构弹窗</h3>
          <p>即使在复杂的嵌套结构中，也能正确显示在最顶层</p>
          <wd-button type="primary" @click="showNestedModal = false">关闭</wd-button>
        </view>
      </view>
    </wd-root-portal>
  </view>
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  const showNestedModal = ref(false)
</script>

<style lang="scss" scoped>
  .nested-demo {
    padding: 16px;
  }

  .container {
    border: 1px solid #ccc;
    padding: 20px;
  }

  .section {
    background: #f5f5f5;
    padding: 15px;
  }

  .sub-section {
    background: #e5e5e5;
    padding: 10px;
  }

  .complex-wrapper {
    background: #d5d5d5;
    padding: 10px;
    margin-top: 10px;
  }

  .nested-content {
    background: white;
    padding: 10px;
  }

  .nested-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
  }

  .nested-modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    text-align: center;
    max-width: 300px;
  }

  .nested-modal-content h3 {
    margin-top: 0;
  }
</style>
```

该示例演示了在复杂嵌套结构中使用 RootPortal 的重要性。如果没有 RootPortal，弹窗可能会被嵌套结构中的其他设置了 z-index 的元素遮挡。通过 RootPortal，弹窗内容被传送到底层，确保能够正确显示在最顶层。

### 示例 3：配合其他组件使用

与其他组件（如 Popup、Overlay）配合使用，解决层级问题。

```vue
<template>
  <view class="combo-demo">
    <wd-cell-group>
      <wd-cell title="配合 Popup 使用" is-link @click="showPopup = true" />
      <wd-cell title="配合 Overlay 使用" is-link @click="showOverlay = true" />
    </wd-cell-group>

    <!-- 使用 RootPortal 的 Popup -->
    <wd-root-portal>
      <wd-popup v-model="showPopup" position="center" custom-style="width: 80%; padding: 20px;">
        <view class="popup-content">
          <h3>使用 RootPortal 的弹窗</h3>
          <p>即使在复杂层级中也能正常显示</p>
          <wd-button type="primary" @click="showPopup = false">关闭</wd-button>
        </view>
      </wd-popup>
    </wd-root-portal>

    <!-- 使用 RootPortal 的 Overlay -->
    <wd-root-portal>
      <wd-overlay v-model="showOverlay" @click="showOverlay = false">
        <view class="overlay-content" @click.stop>
          <h3>使用 RootPortal 的遮罩层</h3>
          <p>确保遮罩层处于最高层级</p>
          <wd-button type="primary" @click="showOverlay = false">关闭</wd-button>
        </view>
      </wd-overlay>
    </wd-root-portal>
  </view>
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  const showPopup = ref(false)
  const showOverlay = ref(false)
</script>

<style lang="scss" scoped>
  .combo-demo {
    padding: 16px;
  }

  .popup-content,
  .overlay-content {
    text-align: center;
    padding: 20px;

    h3 {
      margin-top: 0;
    }

    p {
      margin: 15px 0;
    }
  }
</style>
```

该示例展示了 RootPortal 如何与其他组件配合使用。在嵌套较深的组件结构中，Popup 或 Overlay 可能会受到父级 z-index 的限制，通过 RootPortal 可以确保它们始终显示在正确的层级。

## 注意事项

1. **平台差异**：RootPortal 在不同平台采用不同的实现机制，H5 使用 Teleport，小程序使用 root-portal，App 使用 renderjs，开发者无需关心具体实现。

2. **条件渲染**：建议配合 v-if 使用，避免不必要的 DOM 节点占用内存，只有在需要时才创建传送的内容。

3. **样式隔离**：由于内容被传送到页面根节点，需要注意样式的全局影响，避免污染其他组件的样式。

4. **事件冒泡**：传送后的内容在 DOM 结构上脱离了原来的位置，需要注意事件冒泡的影响。

5. **z-index 管理**：虽然 RootPortal 解决了层级问题，但仍需合理设置 z-index 值，避免与其他全局元素冲突。

6. **性能考虑**：频繁创建和销毁 RootPortal 内容可能会影响性能，应避免不必要的重渲染。

7. **App 端特殊处理**：在 App 端使用 renderjs 实现，元素会被直接追加到 uni-app 或 body 元素下，确保其处于最顶层。

8. **主题继承**：组件会自动继承父级配置提供者的主题样式，保持视觉一致性。

9. **无障碍访问**：传送后的内容在语义上仍然与原始位置关联，但 DOM 位置发生变化，可能影响无障碍访问，需要适当处理。

10. **调试困难**：由于 DOM 结构的变化，调试时可能难以定位传送后的元素，建议使用浏览器开发者工具的组件检查功能。