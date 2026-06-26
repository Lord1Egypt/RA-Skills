# Tour 新手引导


## 组件概况

Tour 新手引导组件是一个用于向用户逐步介绍产品功能的交互式引导工具。该组件通过在页面上高亮显示目标元素并在其附近展示说明文字，帮助新用户快速了解界面布局和功能操作。引导流程支持多步骤切换、自定义蒙版样式、滚动跟随等多种特性，适用于产品首次使用引导、新功能上线提示等场景。

## 核心功能描述

- **多步骤引导**：通过 steps 数组配置引导流程，支持灵活设置每一步的高亮元素和说明文字
- **智能定位**：自动根据目标元素在页面中的位置，动态调整引导提示框的显示位置（上方或下方）
- **高亮蒙版**：使用半透明遮罩覆盖全屏，仅通过 boxShadow 技术高亮目标区域，聚焦用户注意力
- **滚动跟随**：当目标元素被页面顶部或底部遮挡时，自动滚动页面确保元素可见
- **自定义蒙版**：支持修改蒙版颜色、透明度、圆角等样式，满足不同视觉需求
- **富文本内容**：引导内容支持 HTML 标签（如 `<strong>`、`<em>`、`<u>`、`<H1>`、`<code>` 等），通过 rich-text 组件渲染
- **灵活交互**：支持点击蒙版切换下一步、控制当前步骤索引、自定义按钮文字等交互方式
- **完整事件体系**：提供步骤切换、上一步、下一步、完成、跳过、错误等完整的事件回调
- **缺失元素策略**：当目标元素在 DOM 中不存在时，可配置跳过、停止或隐藏引导框的处理策略

## 适用业务场景

- **新用户首次使用**：新用户首次打开应用时，通过逐步引导熟悉核心功能和操作入口
- **新功能上线提示**：产品更新迭代后，引导用户了解新增功能和变更点
- **复杂操作指引**：对于多步骤操作流程，通过引导帮助用户逐步完成
- **功能发现引导**：引导用户探索页面中容易被忽略的隐藏功能或快捷操作
- **培训演示场景**：在企业内部系统或 SaaS 产品中，提供自助式的功能培训引导

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| modelValue | 是否显示引导组件，使用 v-model 绑定 | boolean | - | false | - |
| steps | 引导步骤列表，每个步骤包含 element 选择器、content 内容等信息 | TourStep[] | - | [] | - |
| current | 当前步骤索引，支持 v-model:current 双向绑定 | number | - | 0 | - |
| mask | 是否显示蒙版遮罩层 | boolean | - | true | - |
| maskColor | 蒙版颜色，支持 rgba 格式，与 mask 属性配合使用 | string | - | - | - |
| offset | 引导框与高亮元素之间的间距，单位 px | number | - | 20 | - |
| duration | 动画持续时间，单位毫秒 | number | - | 300 | - |
| borderRadius | 高亮区域的圆角大小，单位 px | number | - | 8 | - |
| padding | 高亮区域的内边距，单位 px | number | - | 8 | - |
| prevText | 上一步按钮文字 | string | - | - | - |
| nextText | 下一步按钮文字 | string | - | - | - |
| skipText | 跳过按钮文字 | string | - | - | - |
| finishText | 完成按钮文字 | string | - | - | - |
| bottomSafetyOffset | 底部安全偏移量，滚动计算时确保元素周围有足够空间 | number | - | 100 | - |
| topSafetyOffset | 顶部安全偏移量，滚动计算时确保元素周围有足够空间 | number | - | 0 | - |
| customNav | 是否使用自定义顶部导航栏 | boolean | - | false | - |
| clickMaskNext | 点击蒙版是否自动进入下一步 | boolean | - | false | - |
| highlightStyle | 高亮区域自定义样式 | CSSProperties | - | {} | - |
| zIndex | 引导组件的层级 | number | - | - | - |
| showTourButtons | 是否显示引导按钮（上一步、下一步、跳过、完成） | boolean | - | true | - |
| scope | 查询作用域，限定选择器范围 | object | - | - | - |
| missingStrategy | 缺失元素处理策略 | string | skip / stop / hide | stop | - |

### TourStep 数据结构

| 属性名 | 说明 | 类型 | 可选值 | 默认值 |
|--------|------|------|--------|--------|
| element | 需要高亮的元素选择器（CSS 选择器，如 `#step1`、`.target`） | string | - | - |
| content | 引导文字内容，支持 HTML 标签 | string | - | - |
| padding | 覆盖当前步骤的高亮区域内边距 | number | - | 继承全局 padding |
| offset | 覆盖当前步骤的提示与高亮间距 | number | - | 继承全局 offset |
| placement | 强制设置提示框位置 | string | auto / top / bottom | auto |

### Events

| 事件名 | 回调参数 | 触发时机 |
|--------|----------|----------|
| change | `{ current: number }` | 步骤切换时触发 |
| prev | `{ prevCurrent: number, current: number, total: number, isElementInTop: boolean }` | 点击上一步按钮时触发 |
| next | `{ prevCurrent: number, current: number, total: number, isElementInTop: boolean }` | 点击下一步按钮时触发 |
| finish | `{ current: number, total: number }` | 引导完成时触发（到达最后一步并点击完成） |
| skip | `{ current: number, total: number }` | 用户点击跳过按钮时触发 |
| error | `{ message: string, element: string }` | 引导过程中出现错误时触发（如找不到目标元素） |

### Slots

| 插槽名 | 作用域参数 | 使用场景 |
|--------|------------|----------|
| highlight | `{ elementInfo: CSSProperties }` | 自定义高亮区域样式，替代默认的高亮框 |
| content | - | 自定义引导内容区域，替代默认的 rich-text 展示 |
| prev | - | 自定义上一步按钮 |
| next | - | 自定义下一步按钮 |
| skip | - | 自定义跳过按钮 |
| finish | - | 自定义完成按钮 |

### Methods

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| handlePrev | - | void | 切换到上一步 |
| handleNext | - | void | 切换到下一步 |
| handleFinish | - | void | 完成引导并关闭 |
| handleSkip | - | void | 跳过引导并关闭 |

## 使用示例

### 示例 1：基本用法

效果说明：最简单的引导使用方式。通过 v-model 控制引导的显示与隐藏，配置 steps 数组定义引导步骤，包含目标元素选择器和说明文字。引导完成后自动关闭并触发 finish 事件。

```vue
<template>
  <view class="tour-step" id="step1">
    <text>这是引导的第一步</text>
  </view>

  <view class="tour-step" id="step2">
    <text>这是引导的第二步</text>
  </view>

  <view class="tour-step" id="step3">
    <text>这是引导的第三步</text>
  </view>

  <wd-button type="primary" @click="startTour">开始引导</wd-button>

  <wd-tour
    v-model="showTour"
    :steps="steps"
    @finish="handleFinish"
    @skip="handleSkip"
    @change="handleChange"
  ></wd-tour>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { TourChangeDetail } from '@/uni_modules/wot-ui-plus/components/wd-tour/types'

const showTour = ref(false)

const steps = [
  {
    element: '#step1',
    content: '欢迎使用引导组件，这是第一步的说明'
  },
  {
    element: '#step2',
    content: '这是第二步，展示了另一个功能点'
  },
  {
    element: '#step3',
    content: '这是最后一步，完成引导流程'
  }
]

function startTour() {
  showTour.value = true
}

function handleFinish() {
  console.log('引导完成')
}

function handleSkip() {
  console.log('引导跳过')
}

function handleChange({ current }: TourChangeDetail) {
  console.log('当前步骤:', current)
}
</script>

<style lang="scss" scoped>
.tour-step {
  padding: 20px;
  margin: 20px auto;
  width: fit-content;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  background-color: #f8f8f8;
  min-width: 250px;
}
</style>
```

### 示例 2：自定义蒙版样式

效果说明：通过 maskColor、borderRadius、padding、offset 等属性自定义蒙版的外观样式。可以设置蒙版颜色为任意颜色值（包括 rgba），调整高亮区域的圆角大小、内边距以及与引导框之间的间距。同时支持自定义按钮文字，实现完全个性化的引导体验。

```vue
<template>
  <view class="tour-step" id="maskStep1">
    <text>自定义蒙版示例步骤一</text>
  </view>

  <view class="tour-step" id="maskStep2">
    <text>自定义蒙版示例步骤二</text>
  </view>

  <wd-button type="primary" @click="startCustomMaskTour">自定义蒙版引导</wd-button>

  <wd-tour
    v-model="showCustomMask"
    :steps="customMaskSteps"
    mask
    mask-color="rgba(255, 0, 0, 0.6)"
    :border-radius="15"
    :padding="10"
    :offset="40"
    next-text="下一步"
    prev-text="上一步"
    skip-text="跳过"
    finish-text="完成"
    @finish="handleFinish"
    @skip="handleSkip"
  ></wd-tour>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const showCustomMask = ref(false)

const customMaskSteps = [
  {
    element: '#maskStep1',
    content: '这是<strong>自定义蒙版</strong>示例，使用了<strong>红色半透明</strong>蒙版'
  },
  {
    element: '#maskStep2',
    content: '蒙版颜色设置为<code>rgba(255, 0, 0, 0.6)</code>'
  }
]

function startCustomMaskTour() {
  showCustomMask.value = true
}

function handleFinish() {
  console.log('引导完成')
}

function handleSkip() {
  console.log('引导跳过')
}
</script>

<style lang="scss" scoped>
.tour-step {
  padding: 20px;
  margin: 20px auto;
  width: fit-content;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  background-color: #f8f8f8;
  min-width: 250px;
}
</style>
```

### 示例 3：点击蒙版继续 / 无蒙版模式

效果说明：演示两种不同的交互模式。第一种通过 clickMaskNext 属性实现点击蒙版自动进入下一步，适合快速浏览式引导；第二种通过 mask="false" 关闭蒙版显示，仅高亮目标元素，适用于需要保持页面其他内容可见性的场景。

```vue
<template>
  <view class="tour-step" id="maskNextStep1">
    <text>点击蒙版下一步 - 步骤一</text>
  </view>

  <view class="tour-step" id="noMaskStep1">
    <text>无蒙版模式 - 步骤一</text>
  </view>

  <view class="button-group">
    <wd-button type="primary" @click="startMaskNextTour">点击蒙版继续</wd-button>
    <wd-button type="primary" @click="startNoMaskTour">关闭蒙版</wd-button>
  </view>

  <!-- 点击蒙版自动下一步 -->
  <wd-tour
    v-model="showMaskNext"
    :steps="maskNextSteps"
    :click-mask-next="true"
    @finish="handleFinish"
    @skip="handleSkip"
  ></wd-tour>

  <!-- 不显示蒙版 -->
  <wd-tour
    v-model="showNoMask"
    :steps="noMaskSteps"
    :mask="false"
    @finish="handleFinish"
    @skip="handleSkip"
  ></wd-tour>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const showMaskNext = ref(false)
const showNoMask = ref(false)

const maskNextSteps = [
  {
    element: '#maskNextStep1',
    content: '点击蒙版任意位置即可进入下一步'
  }
]

const noMaskSteps = [
  {
    element: '#noMaskStep1',
    content: '这是<strong>无蒙版</strong>引导模式，只高亮目标元素'
  }
]

function startMaskNextTour() {
  showMaskNext.value = true
}

function startNoMaskTour() {
  showNoMask.value = true
}

function handleFinish() {
  console.log('引导完成')
}

function handleSkip() {
  console.log('引导跳过')
}
</script>

<style lang="scss" scoped>
.tour-step {
  padding: 20px;
  margin: 20px auto;
  width: fit-content;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  background-color: #f8f8f8;
  min-width: 250px;
}

.button-group {
  display: flex;
  gap: 10px;
  padding: 10px 0;
}
</style>
```

### 示例 4：自定义高亮区域和引导内容

效果说明：通过插槽实现完全自定义的高亮区域样式和引导内容展示。highlight 插槽接收 elementInfo 参数（包含高亮元素的位置、尺寸等信息），可以自定义任何高亮效果（如虚线边框、半透明背景等）。content 插槽允许替换默认的 rich-text 内容为任意自定义组件布局。

```vue
<template>
  <view class="tour-step" id="customStep1">
    <text>自定义高亮 - 步骤一</text>
  </view>

  <view class="tour-step" id="customStep2">
    <text>自定义高亮 - 步骤二</text>
  </view>

  <wd-button type="primary" @click="startCustomHighlight">自定义高亮区域</wd-button>

  <wd-tour
    v-model="showCustomHighlight"
    :steps="customHighlightSteps"
    :padding="10"
    @finish="handleFinish"
    @skip="handleSkip"
    @change="handleChange"
  >
    <template #highlight="{ elementInfo }">
      <view
        class="custom-highlight"
        :style="`${objToStyle(elementInfo)};${objToStyle(customHighlightStyle)}`"
      ></view>
    </template>

    <template #content>
      <view class="custom-content">
        <wd-icon name="help-circle-filled" size="22px"></wd-icon>
        <text class="custom-text">自定义引导内容区域</text>
      </view>
    </template>

    <template #next>
      <view class="custom-button custom-next">继续</view>
    </template>

    <template #finish>
      <view class="custom-button custom-finish">完成</view>
    </template>
  </wd-tour>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { objToStyle } from '@/uni_modules/wot-ui-plus/components/common/util'
import type { TourChangeDetail } from '@/uni_modules/wot-ui-plus/components/wd-tour/types'

const showCustomHighlight = ref(false)

const customHighlightSteps = [
  {
    element: '#customStep1',
    content: '这是<strong>自定义高亮区域</strong>示例'
  },
  {
    element: '#customStep2',
    content: '使用了<em>红色虚线边框</em>和<code>半透明背景</code>'
  }
]

// 自定义高亮样式
const customHighlightStyle = {
  border: '2px dashed #ff0000',
  borderRadius: '8px',
  background: 'rgba(255, 0, 0, 0.1)',
  boxSizing: 'border-box'
}

function startCustomHighlight() {
  showCustomHighlight.value = true
}

function handleFinish() {
  console.log('引导完成')
}

function handleSkip() {
  console.log('引导跳过')
}

function handleChange({ current }: TourChangeDetail) {
  console.log('当前步骤:', current)
}
</script>

<style lang="scss" scoped>
.tour-step {
  padding: 20px;
  margin: 20px auto;
  width: fit-content;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  background-color: #f8f8f8;
  min-width: 250px;
}

.custom-highlight {
  position: fixed;
  box-sizing: border-box;
  transition: all 0.3s ease-in-out;
}

.custom-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
}

.custom-text {
  font-size: 14px;
  color: #333;
}

.custom-button {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;

  &.custom-next {
    background-color: #34d19d;
    color: #fff;
  }

  &.custom-finish {
    background-color: #34d19d;
    color: #fff;
  }
}
</style>
```

### 示例 5：控制当前步骤

效果说明：通过 v-model:current 实现对外部控制当前引导步骤的支持。可以在引导开始前设置起始步骤，或在引导过程中动态跳转至指定步骤。适用于需要跳过部分引导步骤或从特定步骤开始的场景。

```vue
<template>
  <view class="tour-step" id="controlStep1">
    <text>控制当前步骤 - 步骤一</text>
  </view>

  <view class="tour-step" id="controlStep2">
    <text>控制当前步骤 - 步骤二</text>
  </view>

  <view class="tour-step" id="controlStep3">
    <text>控制当前步骤 - 步骤三</text>
  </view>

  <view class="tour-step" id="controlStep4">
    <text>控制当前步骤 - 步骤四</text>
  </view>

  <wd-button-group>
    <wd-button type="primary" @click="startFromBeginning">从头开始引导</wd-button>
    <wd-button type="primary" @click="startFromThird">从第三步开始引导</wd-button>
  </wd-button-group>

  <wd-tour
    v-model="showControlTour"
    :steps="controlSteps"
    v-model:current="currentStep"
    :padding="10"
    @finish="handleFinish"
    @skip="handleSkip"
    @change="handleChange"
  ></wd-tour>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { TourChangeDetail } from '@/uni_modules/wot-ui-plus/components/wd-tour/types'

const showControlTour = ref(false)
const currentStep = ref(0)

const controlSteps = [
  {
    element: '#controlStep1',
    content: '第一步：了解基本功能'
  },
  {
    element: '#controlStep2',
    content: '第二步：探索更多功能'
  },
  {
    element: '#controlStep3',
    content: '第三步：深入了解功能'
  },
  {
    element: '#controlStep4',
    content: '第四步：完成引导'
  }
]

function startFromBeginning() {
  currentStep.value = 0
  showControlTour.value = true
}

function startFromThird() {
  currentStep.value = 2
  showControlTour.value = true
}

function handleFinish() {
  showControlTour.value = false
  console.log('引导完成')
}

function handleSkip() {
  showControlTour.value = false
  console.log('引导跳过')
}

function handleChange({ current }: TourChangeDetail) {
  console.log('当前步骤:', current)
}
</script>

<style lang="scss" scoped>
.tour-step {
  padding: 20px;
  margin: 20px auto;
  width: fit-content;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  background-color: #f8f8f8;
  min-width: 250px;
}
</style>
```

## 注意事项

1. **目标元素选择器**：steps 数组中的 element 字段为 CSS 选择器字符串（如 `#id`、`.class`），确保在页面中存在对应的 DOM 元素。如果选择器无法匹配到元素，将根据 missingStrategy 策略处理（默认 stop 为停止引导）。

2. **引导显示时机**：建议在页面 DOM 渲染完成后再开启引导（设置 modelValue 为 true）。如果目标元素是动态渲染的，可使用 nextTick 确保元素已挂载再启动引导。

3. **滚动位置管理**：组件内部通过 uni.pageScrollTo 实现自动滚动。当页面内容较长、目标元素需要滚动才能可见时，组件会自动计算滚动距离。可通过 bottomSafetyOffset 和 topSafetyOffset 调整滚动安全区域。

4. **自定义导航栏适配**：如果页面使用了自定义导航栏，请设置 customNav 属性为 true。此时组件会通过 uni.getMenuButtonBoundingClientRect() 获取导航栏位置信息，确保引导提示框正确定位。也可通过 topSafetyOffset 手动指定顶部偏移量。

5. **缺失元素策略**：missingStrategy 支持三种值：
   - `skip`：跳过当前步骤，直接进入下一步
   - `stop`：停止引导（默认行为）
   - `hide`：隐藏当前步骤的引导提示框

6. **查询作用域限制**：在小程序平台中，选择器可能无法跨越组件边界查找元素。可通过 scope 属性传入组件实例，限定选择器的查询范围。

7. **富文本内容渲染**：content 字段通过 rich-text 组件渲染，支持常见的 HTML 标签（如 `<strong>`、`<em>`、`<u>`、`<H1>`、`<code>` 等）。避免使用不安全的 HTML 内容。

8. **引导按钮显示控制**：通过 showTourButtons 属性可隐藏所有引导按钮，适用于仅通过点击蒙版或自定义交互完成引导的场景。

9. **层级管理**：引导组件默认使用较高的 zIndex 值确保覆盖页面其他内容。若页面中存在其他高浮层组件，请通过 zIndex 属性合理分配层级关系。

10. **动画过渡**：组件内置了平滑的动画过渡效果（默认 300ms），高亮区域和引导框在步骤切换时会平滑过渡到新位置。可通过 duration 属性调整动画时长。
