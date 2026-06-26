# Slider 滑块

## 组件概况

Slider 滑块组件由 `wd-slider` 和 `wd-slider-button` 两个子组件组成，分别适用于不同的交互场景。`wd-slider` 提供传统的数值选择滑块，支持单滑块和双滑块（范围选择）模式，用户通过拖动手势在指定范围内精确选择数值。`wd-slider-button` 提供滑动验证/解锁交互，用户拖动滑块至指定阈值后触发成功状态，适用于安全验证、滑动解锁等场景。两个组件均支持丰富的样式自定义、禁用状态和触摸手势优化，满足各类数值选择和验证交互需求。

## 核心功能描述

### wd-slider 传统数值滑块

- **单滑块模式**：通过 `v-model` 绑定 `number` 类型值，用于选择范围内的单个数值
- **双滑块模式（范围选择）**：通过 `v-model` 绑定 `number[]` 数组，用于选择数值区间
- **自定义范围**：通过 `min` 和 `max` 属性设置取值范围，默认 0~100
- **步长控制**：通过 `step` 属性设置步进值，拖动时自动对齐到最近的步长倍数
- **标签显示**：默认显示最小值、最大值和当前滑块值标签，可通过 `hideMinMax` 和 `hideLabel` 隐藏
- **颜色自定义**：通过 `activeColor` 和 `inactiveColor` 分别设置激活和未激活轨道的背景色
- **禁用状态**：通过 `disabled` 属性禁用滑块交互
- **拖动事件**：提供 `dragstart`、`dragmove`、`dragend` 完整的拖动生命周期事件
- **暴露方法**：通过 `initSlider` 方法支持手动重新初始化轨道尺寸

### wd-slider-button 滑动验证按钮

- **滑动验证交互**：用户拖动滑块至阈值位置后触发成功状态
- **阈值控制**：通过 `threshold` 属性自定义触发阈值，默认需滑动至最右端
- **自动重置**：通过 `autoReset` 和 `resetDelay` 实现成功后自动回弹重置
- **进度反馈**：通过 `change` 事件实时返回滑动进度百分比（0~1）
- **状态文本**：通过 `text` 和 `successText` 分别设置默认和成功状态下的提示文本
- **样式自定义**：支持设置宽度、高度、圆角、背景色、轨道颜色等外观属性
- **禁用状态**：通过 `disabled` 属性禁用滑动交互
- **暴露方法**：通过 `reset`、`handleSuccess`、`init` 方法支持程序化控制
- **插槽扩展**：提供 `default` 插槽自定义文本区域，`thumb` 插槽自定义滑块图标

## 适用业务场景

- **数值选择**：音量调节、亮度调节、价格范围筛选、数量选择等需要精确数值选择的场景
- **区间筛选**：价格区间、时间范围、年龄范围等双端范围选择场景
- **滑动验证/解锁**：登录滑动验证、敏感操作二次确认、滑动解锁等安全验证场景
- **进度交互**：需要用户主动拖动完成的操作，如确认同意、验证身份等
- **表单控件**：作为表单内的数值输入控件，替代传统输入框提升操作效率

## wd-slider API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | `number \| number[]` | `0` | 否 | 滑块的值，绑定数组时为双滑块模式 |
| min | `number` | `0` | 否 | 滑块最小值 |
| max | `number` | `100` | 否 | 滑块最大值 |
| step | `number` | `1` | 否 | 步进值，必须大于 0 |
| hideMinMax | `boolean` | `false` | 否 | 是否隐藏两端的最小/最大值标签 |
| hideLabel | `boolean` | `false` | 否 | 是否隐藏滑块上方的当前值标签 |
| disabled | `boolean` | `false` | 否 | 是否禁用滑块 |
| activeColor | `string` | `''` | 否 | 进度条激活部分的背景颜色 |
| inactiveColor | `string` | `'#e5e5e5'` | 否 | 进度条未激活部分的背景颜色 |
| customMinClass | `string` | `''` | 否 | 自定义最小值标签的样式类名 |
| customMaxClass | `string` | `''` | 否 | 自定义最大值标签的样式类名 |
| customStyle | `string` | `''` | 否 | 自定义根节点样式 |
| customClass | `string` | `''` | 否 | 自定义根节点类名 |

### Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| update:modelValue | `value: number \| number[]` | 滑块值变化时触发，用于 `v-model` 双向绑定 |
| dragstart | `{ value: number \| number[] }` | 开始拖动滑块时触发 |
| dragmove | `{ value: number \| number[] }` | 拖动滑块过程中持续触发 |
| dragend | `{ value: number \| number[] }` | 结束拖动滑块时触发 |

### Methods

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| initSlider | - | `void` | 重新初始化滑块轨道宽度和位置，适用于动态布局变化后调用 |

### Slots

组件不对外暴露任何插槽。

## wd-slider-button API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| text | `string` | `'滑动解锁'` | 否 | 默认状态下显示的按钮文字 |
| successText | `string` | `'验证成功'` | 否 | 验证成功后显示的按钮文字 |
| width | `string \| number` | `''` | 否 | 组件宽度，支持带单位字符串（如 `'300px'`）或纯数字（单位 px） |
| height | `string \| number` | `45` | 否 | 组件高度，也作为滑块的宽度/高度 |
| round | `string \| number` | `100` | 否 | 组件圆角大小 |
| bgColor | `string` | `'#e0e0e0'` | 否 | 组件背景颜色 |
| railColor | `string` | `'#4d80f0'` | 否 | 滑动轨道背景颜色 |
| railIndex | `string \| number` | `''` | 否 | 滑动轨道的 z-index 层级 |
| railRadius | `string \| number` | `100` | 否 | 滑动轨道圆角大小 |
| textColor | `string` | `'#c2c2c2'` | 否 | 默认状态下文字颜色 |
| activeTextColor | `string` | `'#ffffff'` | 否 | 成功状态下文字颜色 |
| fontSize | `string \| number` | `16` | 否 | 文字大小 |
| textBold | `boolean` | `false` | 否 | 文字是否加粗显示 |
| threshold | `string \| number` | `''` | 否 | 触发成功的阈值，默认需滑到底部，支持带单位字符串或纯数字 |
| autoReset | `boolean` | `false` | 否 | 成功后是否自动重置 |
| resetDelay | `number` | `300` | 否 | 自动重置的延迟时间（毫秒） |
| disabled | `boolean` | `false` | 否 | 是否禁用滑动 |
| customStyle | `string` | `''` | 否 | 自定义根节点样式 |
| customClass | `string` | `''` | 否 | 自定义根节点类名 |

### Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| change | `percent: number` | 滑动过程中触发，返回当前滑动进度百分比（0~1） |
| success | - | 滑动达到阈值触发成功时调用 |
| reset | - | 滑块重置回初始位置时触发 |

### Methods

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| init | - | `void` | 重新初始化组件尺寸，在布局变化后调用 |
| reset | - | `void` | 手动重置滑块到初始位置，清除成功状态 |
| handleSuccess | - | `void` | 手动触发成功状态 |

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 自定义提示文字区域，替代默认的 text/successText 文本 |
| thumb | - | 自定义滑块图标，默认使用 `wd-icon` 双箭头图标 |

## 使用示例

### 示例 1：基础用法（wd-slider）

展示滑块的基本使用方式，默认范围 0~100，步进值为 1。

```vue
<template>
  <view>
    <wd-slider v-model="value" />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const value = ref<number>(30)
</script>
```

`v-model` 绑定的值为 `number` 类型时，为单滑块模式。拖动滑块会实时更新绑定值，并在滑块上方显示当前数值。

### 示例 2：指定选择范围（wd-slider）

通过 `min` 和 `max` 属性自定义滑块的取值范围。

```vue
<template>
  <view>
    <!-- 负数范围：-10 ~ 10 -->
    <wd-slider v-model="negativeValue" :min="-10" :max="10" />

    <!-- 自定义范围：160 ~ 280 -->
    <wd-slider v-model="heightValue" :min="160" :max="280" :step="30" />

    <!-- 小范围：5 ~ 50 -->
    <wd-slider v-model="smallRangeValue" :min="5" :max="50" />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const negativeValue = ref<number>(0)
  const heightValue = ref<number>(190)
  const smallRangeValue = ref<number>(20)
</script>
```

`min` 和 `max` 可以设置为任意数值（包括负数）。`step` 属性控制拖动时的步进值，每次变化对齐到 `min + n * step` 的倍数。

### 示例 3：双滑块范围选择（wd-slider）

通过绑定数组启用双滑块模式，用于选择数值区间。

```vue
<template>
  <view>
    <wd-slider v-model="rangeValue" :min="10" :max="80" />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  // 绑定数组启用双滑块模式
  const rangeValue = ref<number[]>([20, 40])
</script>
```

当 `v-model` 绑定值为 `number[]` 数组时，自动启用双滑块模式，数组第一个元素为左侧滑块值，第二个元素为右侧滑块值。组件会自动保证左侧值小于等于右侧值。

### 示例 4：隐藏标签与禁用状态（wd-slider）

控制标签显示和禁用交互。

```vue
<template>
  <view>
    <!-- 隐藏两端最大最小值标签 -->
    <wd-slider v-model="value1" hide-min-max :step="10" />

    <!-- 隐藏滑块上方当前值标签 -->
    <wd-slider v-model="value2" hide-label />

    <!-- 禁用状态 -->
    <wd-slider v-model="value3" disabled />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const value1 = ref<number>(50)
  const value2 = ref<number>(30)
  const value3 = ref<number>(70)
</script>
```

`hide-min-max` 隐藏轨道两端的数值标签，适合界面空间有限或数值范围已通过其他方式展示的场景。`disabled` 状态下滑块不可拖动，视觉上呈现为半透明禁用效果。

### 示例 5：自定义颜色（wd-slider）

自定义滑块轨道和进度条的颜色。

```vue
<template>
  <view>
    <!-- 自定义激活颜色 -->
    <wd-slider v-model="value1" active-color="#34d19d" />

    <!-- 自定义未激活颜色 -->
    <wd-slider v-model="value2" inactive-color="#f0f0f0" />

    <!-- 同时自定义激活和未激活颜色 -->
    <wd-slider v-model="value3" active-color="#fa4350" inactive-color="#ffe5e7" />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const value1 = ref<number>(40)
  const value2 = ref<number>(60)
  const value3 = ref<number>(80)
</script>
```

`activeColor` 控制已拖动部分（进度条）的背景色，`inactiveColor` 控制未拖动部分（轨道）的背景色。

### 示例 6：监听拖动事件（wd-slider）

监听滑块拖动的完整生命周期。

```vue
<template>
  <view>
    <wd-slider
      v-model="value"
      @dragstart="onDragStart"
      @dragmove="onDragMove"
      @dragend="onDragEnd"
    />
    <view class="event-log">
      <text>{{ logText }}</text>
    </view>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const value = ref<number>(50)
  const logText = ref<string>('')

  function onDragStart(event: { value: number | number[] }) {
    logText.value = `拖动开始: ${event.value}`
  }

  function onDragMove(event: { value: number | number[] }) {
    logText.value = `拖动中: ${event.value}`
  }

  function onDragEnd(event: { value: number | number[] }) {
    logText.value = `拖动结束: ${event.value}`
  }
</script>
```

三个拖动事件按顺序触发：`dragstart`（按下时） -> `dragmove`（持续拖动中） -> `dragend`（松开时）。事件参数中的 `value` 在单滑块模式下为 `number`，双滑块模式下为 `number[]`。

### 示例 7：滑动解锁（wd-slider-button）

展示滑动验证/解锁功能的基本用法。

```vue
<template>
  <view>
    <wd-slider-button @success="onSuccess" @reset="onReset" />
  </view>
</template>
<script lang="ts" setup>
  function onSuccess() {
    console.log('验证成功')
  }

  function onReset() {
    console.log('已重置')
  }
</script>
```

默认文本为"滑动解锁"，成功后显示"验证成功"。用户需要将滑块拖动到最右端才能触发成功。

### 示例 8：自定义样式与阈值（wd-slider-button）

自定义滑动验证组件的外观和触发条件。

```vue
<template>
  <view>
    <!-- 自定义尺寸和颜色 -->
    <wd-slider-button
      text="向右滑动验证"
      :width="320"
      :height="50"
      bg-color="#f5f5f5"
      rail-color="#4D80F0"
      text-color="#999999"
      active-text-color="#ffffff"
      @success="onSuccess"
    />

    <!-- 自定义阈值（滑动一半即可触发） -->
    <wd-slider-button
      text="滑动到一半即可"
      :threshold="'50%'"
      @success="onSuccess"
    />
  </view>
</template>
<script lang="ts" setup>
  function onSuccess() {
    console.log('验证成功')
  }
</script>
```

通过 `threshold` 属性可以自定义触发阈值，默认需要滑到最右端，可以设置为 `50%` 或其他像素值降低触发难度。

### 示例 9：自动重置（wd-slider-button）

设置成功后自动回弹重置。

```vue
<template>
  <view>
    <wd-slider-button
      text="请滑动验证"
      :auto-reset="true"
      :reset-delay="500"
      @success="onSuccess"
      @reset="onReset"
    />
  </view>
</template>
<script lang="ts" setup>
  function onSuccess() {
    console.log('验证成功，500ms后自动重置')
  }

  function onReset() {
    console.log('已自动重置')
  }
</script>
```

启用 `autoReset` 后，触发成功状态后会在 `resetDelay` 毫秒后自动回弹到初始位置并清除成功状态，适用于需要重复验证的场景。

### 示例 10：程序化控制（wd-slider-button）

通过 ref 调用组件方法进行程序化控制。

```vue
<template>
  <view>
    <wd-slider-button
      ref="sliderButtonRef"
      text="请滑动验证"
      @success="onSuccess"
    />

    <wd-button @click="handleReset">手动重置</wd-button>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const sliderButtonRef = ref<any>(null)

  function onSuccess() {
    console.log('验证成功')
  }

  function handleReset() {
    sliderButtonRef.value?.reset()
  }
</script>
```

通过 `ref` 获取组件实例后，可以调用 `reset()` 手动重置滑块、`handleSuccess()` 手动触发成功状态、`init()` 重新初始化组件尺寸。

### 示例 11：监听滑动进度（wd-slider-button）

实时获取滑动进度百分比。

```vue
<template>
  <view>
    <wd-slider-button
      text="请滑动验证"
      @change="onChange"
      @success="onSuccess"
    />
    <view class="progress-display">
      <text>滑动进度: {{ (progress * 100).toFixed(0) }}%</text>
    </view>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const progress = ref<number>(0)

  function onChange(percent: number) {
    progress.value = percent
  }

  function onSuccess() {
    console.log('验证成功')
  }
</script>
```

`change` 事件在滑动过程中持续触发，返回 0~1 之间的进度百分比值。可用于实现进度条显示、动态颜色变化等效果。

### 示例 12：自定义滑块图标（wd-slider-button）

通过插槽自定义滑块区域的内容。

```vue
<template>
  <view>
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
</template>
<script lang="ts" setup>
</script>
```

`thumb` 插槽替换默认的滑块图标，`default` 插槽替换默认的提示文字区域。通过插槽可以实现更灵活的自定义效果。

## 注意事项

1. **双滑块模式自动校正**：当 `v-model` 绑定数组且左侧值大于右侧值时，组件会自动交换两个值的位置，确保左侧值始终小于等于右侧值
2. **step 必须大于 0**：如果 `step` 设置为小于等于 0 的值，组件会输出警告并自动回退到步进值为 1
3. **值范围自动约束**：所有传入的值都会被自动约束在 `min` 和 `max` 范围内，超出范围的值会被截断
4. **精度处理**：组件内部使用 `toFixed(10)` 处理浮点数精度问题，确保步进计算不会出现精度丢失
5. **布局变化后需重新初始化**：当滑块容器尺寸发生动态变化（如窗口大小改变、动画过渡结束）时，需手动调用 `initSlider()`（wd-slider）或 `init()`（wd-slider-button）方法重新计算轨道尺寸
6. **wd-slider-button 默认需要滑到底部**：不设置 `threshold` 时，必须将滑块拖动到组件最右端才能触发成功，`threshold` 的默认计算为 `容器宽度 - 滑块宽度`
7. **成功状态阻止继续拖动**：wd-slider-button 进入成功状态后，滑块不可继续拖动，除非调用 `reset()` 方法清除成功状态
8. **禁用状态阻止所有交互**：两个组件的 `disabled` 属性为 `true` 时，所有触摸事件均不会响应
9. **wd-slider-button 的 threshold 支持单位**：`threshold` 属性支持纯数字（单位 px）或带单位的字符串（如 `'50%'`），设置为 `0` 或空字符串时使用默认计算方式
10. **wd-slider 的 modelValue 变化监听**：当外部修改 `modelValue` 时，组件会重新计算初始值并自动对齐到最近的步长倍数
11. **自定义样式扩展**：通过 `customStyle` 和 `customClass` 属性可以对两个组件进行样式扩展，如添加阴影、修改边距等
12. **wd-slider 的双滑块模式由绑定值类型自动判断**：无需额外的 `isRange` 属性，只需将 `v-model` 绑定为 `number[]` 数组即可自动切换为双滑块模式
