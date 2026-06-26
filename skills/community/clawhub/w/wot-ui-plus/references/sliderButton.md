# SliderButton 滑块按钮

## 组件概况

SliderButton 滑块按钮组件是一种滑动验证/解锁交互组件，用户通过拖动滑块到指定阈值位置来触发成功状态。该组件提供了丰富的样式自定义选项，支持进度反馈、自动重置、禁用状态等功能，适用于滑动验证、滑动解锁、敏感操作二次确认等场景。组件内部基于触摸事件（touchstart、touchmove、touchend）实现，支持实时进度计算、阈值判定和状态管理。

## 核心功能描述

- **滑动验证交互**：用户拖动滑块至指定阈值位置后自动触发成功状态
- **阈值控制**：通过 `threshold` 属性自定义触发成功的阈值，默认需滑动至最右端
- **自动重置**：通过 `autoReset` 和 `resetDelay` 实现成功后自动回弹到初始位置
- **实时进度反馈**：通过 `change` 事件实时返回滑动进度百分比（0~1）
- **状态文本切换**：通过 `text` 和 `successText` 分别设置默认和成功状态下的提示文本
- **样式自定义**：支持设置宽度、高度、圆角、背景色、轨道颜色、文字颜色等外观属性
- **禁用状态**：通过 `disabled` 属性禁用滑动交互
- **触摸手势优化**：支持多平台触摸事件处理，防止页面滚动穿透
- **层级控制**：通过 `railIndex` 属性设置滑动轨道的 z-index 层级
- **暴露方法**：通过 `init`、`reset`、`handleSuccess` 方法支持程序化控制
- **插槽扩展**：提供 `default` 插槽自定义文本区域，`thumb` 插槽自定义滑块图标
- **跨平台适配**：H5 端支持 hover 效果，小程序端优化触摸体验

## 适用业务场景

- **登录验证**：登录页面中使用滑动验证替代传统图形验证码
- **敏感操作确认**：删除、支付、授权等敏感操作前的二次确认
- **滑动解锁**：应用解锁、屏幕解锁等场景
- **任务确认**：完成任务确认、签到打卡等需要用户主动操作的场景
- **防误触设计**：防止用户误触按钮导致的非预期操作
- **表单提交**：表单提交前的滑动验证，提升操作仪式感

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| text | 默认状态下显示的按钮文字 | string | - | 滑动解锁 | - |
| successText | 验证成功后显示的按钮文字 | string | - | 验证成功 | - |
| width | 组件宽度，支持带单位字符串（如 '300px'）或纯数字（单位 px） | string / number | - | '' | - |
| height | 组件高度，也作为滑块的宽度/高度 | string / number | - | 45 | - |
| round | 组件圆角大小 | string / number | - | 100 | - |
| bgColor | 组件背景颜色 | string | - | #e0e0e0 | - |
| railColor | 滑动轨道背景颜色 | string | - | #4d80f0 | - |
| railIndex | 滑动轨道的 z-index 层级 | string / number | - | '' | - |
| railRadius | 滑动轨道圆角大小 | string / number | - | 100 | - |
| textColor | 默认状态下文字颜色 | string | - | #c2c2c2 | - |
| activeTextColor | 成功状态下文字颜色 | string | - | #ffffff | - |
| fontSize | 文字大小 | string / number | - | 16 | - |
| textBold | 文字是否加粗显示 | boolean | - | false | - |
| threshold | 触发成功的阈值，默认需滑到底部，支持带单位字符串或纯数字 | string / number | - | '' | - |
| autoReset | 成功后是否自动重置 | boolean | - | false | - |
| resetDelay | 自动重置的延迟时间（毫秒） | number | - | 300 | - |
| disabled | 是否禁用滑动 | boolean | - | false | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点类名 | string | - | '' | - |

### Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| change | 滑动过程中触发，返回当前滑动进度百分比（0~1） | percent: number |
| success | 滑动达到阈值触发成功时调用 | - |
| reset | 滑块重置回初始位置时触发 | - |

### Methods

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| init | 重新初始化组件尺寸，在布局变化后调用 | - | void |
| reset | 手动重置滑块到初始位置，清除成功状态 | - | void |
| handleSuccess | 手动触发成功状态 | - | void |

### Slots

| 插槽名 | 说明 |
|--------|------|
| default | 自定义提示文字区域，替代默认的 text/successText 文本 |
| thumb | 自定义滑块图标，默认使用 `wd-icon` 双箭头图标（`double-right`） |

## 使用示例

### 示例 1：基础用法

展示滑动验证组件的基本使用方式，拖动滑块至最右端触发成功。

```vue
<template>
  <view class="wd-page">
    <demo-block title="基础用法">
      <view class="wd-demo-area">
        <wd-slider-button :text="'滑动解锁'" @success="onSliderSuccess" @reset="onSliderReset" />
      </view>
    </demo-block>
  </view>
</template>

<script lang="ts" setup>
  // 滑动成功
  const onSliderSuccess = () => {
    uni.showToast({
      title: '滑动验证成功！',
      icon: 'success'
    })
  }

  // 滑块重置
  const onSliderReset = () => {
    console.log('滑动按钮已重置')
  }
</script>

<style lang="scss">
  .wd-demo-area {
    padding: 20px 0;
  }
</style>
```

默认情况下，滑块需要拖动到最右端才能触发成功状态。成功时会触发 `success` 事件，重置回初始位置时会触发 `reset` 事件。组件内部会自动计算容器宽度和阈值，确保准确的触发判断。

### 示例 2：自定义样式

自定义滑块按钮的外观样式，包括颜色、尺寸、文字等。

```vue
<template>
  <view class="wd-page">
    <demo-block title="自定义样式">
      <view class="wd-demo-area">
        <wd-slider-button
          :text="sliderData.text"
          :successText="sliderData.successText"
          :bgColor="sliderData.bgColor"
          :railColor="sliderData.railColor"
          :height="45"
          textColor="#ffffff"
          :textBold="true"
          railIndex="10"
          threshold="150"
          autoReset
          @reset="onCustomSuccess"
        />
      </view>
    </demo-block>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  // 滑块数据接口定义
  interface SliderData {
    text: string
    successText: string
    bgColor: string
    railColor: string
  }

  // 响应式数据
  const sliderData = ref<SliderData>({
    text: '开始出发',
    successText: '开始出发',
    bgColor: 'rgb(230, 27, 47)',
    railColor: 'rgba(230, 27, 47, 0.85)'
  })

  // 自定义样式 - 滑动成功回调
  const onCustomSuccess = () => {
    sliderData.value = {
      text: '接到乘客',
      successText: '接到乘客',
      bgColor: 'rgb(47, 230, 117)',
      railColor: 'rgba(47, 230, 117, 0.85)'
    }
  }
</script>

<style lang="scss">
  .wd-demo-area {
    padding: 20px 0;
  }
</style>
```

该示例展示了丰富的样式自定义功能：
- `height`：设置组件高度为 45px，同时滑块宽度也为 45px
- `textColor` 和 `textBold`：设置白色文字并加粗
- `railIndex`：设置轨道 z-index 层级为 10
- `threshold`：设置触发阈值为 150px，滑动 150px 即可触发成功
- `autoReset`：开启自动重置，成功后自动回弹
- `bgColor` 和 `railColor`：自定义背景色和轨道颜色

### 示例 3：禁用状态

展示组件的禁用状态，适用于条件不满足时禁止操作。

```vue
<template>
  <view class="wd-page">
    <demo-block title="禁用状态">
      <view class="wd-demo-area">
        <wd-slider-button :text="'已禁用'" :width="300" :height="50" :disabled="true" />
      </view>
    </demo-block>
  </view>
</template>

<script lang="ts" setup>
</script>

<style lang="scss">
  .wd-demo-area {
    padding: 20px 0;
  }
</style>
```

当 `disabled` 属性设置为 `true` 时，滑块无法拖动，触摸事件会被阻止。视觉上呈现为禁用效果，适用于条件未满足时防止用户操作。

### 示例 4：自定义阈值与自动重置

配置自定义触发阈值，并在成功后自动回弹。

```vue
<template>
  <view class="wd-page">
    <demo-block title="自定义阈值">
      <view class="wd-demo-area">
        <!-- 滑动一半即可触发 -->
        <wd-slider-button
          text="滑动一半即可解锁"
          :threshold="150"
          :width="300"
          @success="onHalfThresholdSuccess"
        />

        <!-- 自动重置 -->
        <wd-slider-button
          text="自动重置验证"
          :auto-reset="true"
          :reset-delay="500"
          @success="onAutoResetSuccess"
          @reset="onAutoReset"
        />

        <!-- 小阈值，更容易触发 -->
        <wd-slider-button
          text="轻触即可"
          :threshold="50"
          :height="40"
          @success="onEasySuccess"
        />
      </view>
    </demo-block>
  </view>
</template>

<script lang="ts" setup>
  const onHalfThresholdSuccess = () => {
    console.log('滑动一半验证成功')
  }

  const onAutoResetSuccess = () => {
    console.log('验证成功，500ms后自动重置')
  }

  const onAutoReset = () => {
    console.log('滑块已自动重置')
  }

  const onEasySuccess = () => {
    console.log('轻触验证成功')
  }
</script>

<style lang="scss">
  .wd-demo-area {
    padding: 20px 0;
  }
</style>
```

`threshold` 属性用于设置触发成功所需的滑动距离（单位为 px），默认为空字符串，表示需要滑到最右端。可以设置为较小的值降低触发难度，适用于快速验证场景。

### 示例 5：实时进度反馈

监听滑动过程中的进度变化。

```vue
<template>
  <view class="wd-page">
    <demo-block title="实时进度">
      <view class="wd-demo-area">
        <wd-slider-button
          text="滑动验证"
          @change="onChange"
          @success="onProgressSuccess"
        />
        <view class="progress-display">
          <view class="progress-bar" :style="{ width: `${progress * 100}%` }"></view>
          <text class="progress-text">滑动进度: {{ (progress * 100).toFixed(0) }}%</text>
        </view>
      </view>
    </demo-block>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const progress = ref<number>(0)

  const onChange = (percent: number) => {
    progress.value = percent
  }

  const onProgressSuccess = () => {
    console.log('验证成功')
    progress.value = 1
  }
</script>

<style lang="scss">
  .wd-demo-area {
    padding: 20px 0;
  }

  .progress-display {
    margin-top: 10px;
    height: 20px;
    background-color: #f5f5f5;
    border-radius: 10px;
    overflow: hidden;
    position: relative;
  }

  .progress-bar {
    height: 100%;
    background-color: #4d80f0;
    transition: width 0.1s ease;
  }

  .progress-text {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    font-size: 12px;
    color: #333;
  }
</style>
```

`change` 事件在滑动过程中持续触发，返回 0~1 之间的进度百分比。可用于实现进度条显示、动态颜色变化、声音反馈等效果。

### 示例 6：自定义滑块图标和文字

通过插槽自定义滑块区域的内容和提示文字。

```vue
<template>
  <view class="wd-page">
    <demo-block title="自定义图标和文字">
      <view class="wd-demo-area">
        <!-- 自定义滑块图标 -->
        <wd-slider-button text="请滑动解锁">
          <template #thumb>
            <view class="custom-thumb">
              <wd-icon name="arrow-right" color="#ffffff" size="24"></wd-icon>
            </view>
          </template>
        </wd-slider-button>

        <!-- 自定义文字区域 -->
        <wd-slider-button>
          <template #default>
            <view class="custom-text">
              <wd-icon name="lock" size="16"></wd-icon>
              <text>拖动滑块完成验证</text>
            </view>
          </template>
        </wd-slider-button>
      </view>
    </demo-block>
  </view>
</template>

<script lang="ts" setup>
</script>

<style lang="scss">
  .wd-demo-area {
    padding: 20px 0;
  }

  .custom-thumb {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #ffffff;
    border-radius: 100px;
  }

  .custom-text {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    color: #c2c2c2;
    font-size: 16px;
  }
</style>
```

`thumb` 插槽替换默认的滑块图标，`default` 插槽替换默认的提示文字区域。通过插槽可以实现更灵活的自定义效果。

### 示例 7：程序化控制

通过 ref 调用组件方法进行程序化控制。

```vue
<template>
  <view class="wd-page">
    <demo-block title="程序化控制">
      <view class="wd-demo-area">
        <wd-slider-button
          ref="sliderButtonRef"
          text="请滑动验证"
          @success="onSuccess"
        />

        <view class="control-buttons">
          <wd-button @click="handleReset">手动重置</wd-button>
          <wd-button type="success" @click="handleSuccess">触发成功</wd-button>
          <wd-button type="warning" @click="handleInit">重新初始化</wd-button>
        </view>
      </view>
    </demo-block>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const sliderButtonRef = ref<any>(null)

  const onSuccess = () => {
    console.log('验证成功')
  }

  const handleReset = () => {
    sliderButtonRef.value?.reset()
  }

  const handleSuccess = () => {
    sliderButtonRef.value?.handleSuccess()
  }

  const handleInit = () => {
    sliderButtonRef.value?.init()
  }
</script>

<style lang="scss">
  .wd-demo-area {
    padding: 20px 0;
  }

  .control-buttons {
    display: flex;
    gap: 10px;
    margin-top: 15px;
  }
</style>
```

通过 `ref` 获取组件实例后，可以调用：
- `reset()`：手动重置滑块到初始位置，清除成功状态
- `handleSuccess()`：手动触发成功状态，滑块滑到最右端
- `init()`：重新初始化组件尺寸，在容器大小变化后调用

## 注意事项

1. **阈值计算**：当 `threshold` 为空字符串时，组件会自动计算阈值为容器宽度减去滑块宽度（即 `areaWidth - thumbWidth`），这意味着需要滑动到最右端才能触发成功。

2. **进度计算**：`change` 事件返回的进度是基于阈值计算的，公式为 `thumbX / thresholdX`。当阈值为 0 时，进度始终为 0。

3. **成功状态阻止**：进入成功状态后，滑块无法继续拖动，必须通过 `reset()` 方法清除成功状态后才能重新使用。

4. **自动重置机制**：开启 `autoReset` 后，触发成功状态后会设置 `thumbX` 为容器宽度（`areaWidth`），然后在 `resetDelay` 毫秒后调用 `reset()` 回弹到初始位置。

5. **触摸体验优化**：组件在触摸开始时记录指尖相对滑块左侧的偏移量（`dragOffsetX`），避免拖动时滑块跳动。计算公式为：`nextX = touch.clientX - areaLeft - dragOffsetX`。

6. **过渡动画控制**：使用 `useTransition` 状态控制过渡动画的启用时机。拖动过程中禁用过渡动画以确保实时响应，拖动结束时启用过渡动画实现平滑回弹。

7. **组件尺寸**：`height` 属性同时控制组件高度和滑块宽度/高度，滑块默认为正方形，与组件高度一致。

8. **布局变化后重新初始化**：当容器尺寸发生动态变化（如页面切换、屏幕旋转等）时，需手动调用 `init()` 方法重新计算容器尺寸。

9. **H5 端 hover 效果**：H5 端滑块在 hover 时会放大 1.05 倍（`transform: scale(1.05)`），增强交互反馈。小程序端会禁用点击高亮（`-webkit-tap-highlight-color: transparent`）。

10. **z-index 层级**：滑块的 z-index 固定为 1000，轨道的 z-index 通过 `railIndex` 属性自定义，默认为 1。确保滑块始终在轨道上方。

11. **文本层级**：提示文字的 z-index 为 5，低于滑块和轨道，确保不影响触摸操作。同时设置 `user-select: none` 和 `pointer-events: none` 防止文本选择和点击。

12. **圆角适配**：`round` 属性控制组件整体圆角，`railRadius` 控制轨道圆角，两者可独立设置。建议使用相同的值以获得更好的视觉效果。