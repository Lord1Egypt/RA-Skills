# InputNumber 数字输入框


数字输入框允许用户通过点击加减按钮或直接键盘输入来调整数值，是数量控制、金额调整等场景中最常用的交互组件之一。

## 组件概况

InputNumber 组件是一个功能丰富的数字输入框，支持加减按钮步进、数值范围限制、小数精度控制、严格步进模式、长按连续增减、异步变更拦截等功能。组件同时保留了原生输入框的灵活性，可与表单系统无缝集成。

### 核心功能描述

- **加减步进**：通过点击加减按钮按设定的 step 值递增/递减
- **范围限制**：支持最小值（min）和最大值（max）边界控制
- **精度控制**：通过 precision 属性控制小数位数
- **严格步进**：stepStrictly 模式下，值始终为 step 的整数倍，越界时自动调整到最近的合法步进值
- **长按手势**：开启 longPress 后，长按加减按钮可连续增减，600ms 后触发，随后每 250ms 执行一次
- **异步变更拦截**：beforeChange 回调支持返回 Promise，可在数值变化前进行异步校验或确认
- **更新模式控制**：immediateChange 控制输入时是否实时更新 v-model，关闭时仅在失焦或按钮点击时更新
- **空值支持**：allowNull 允许输入框为空，配合 placeholder 实现"不限"等场景
- **无输入框模式**：withoutInput 隐藏输入框，仅保留加减按钮
- **按钮独立控制**：disableMinus / disablePlus 可分别禁用减号/加号按钮
- **初始化修正控制**：updateOnInit 控制初始化时是否自动修正 v-model 为合法值

### 适用业务场景

- 购物车商品数量增减
- 订单中规格数量的调整
- 价格/金额的微调输入
- 需要严格步进值的参数配置（如每次增加固定间隔）
- 支持"不限"选项的数量输入

---

## API

### Props

| 参数 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|------|------|------|--------|--------|----------|
| modelValue / v-model | 绑定值 | number \| string | - | - | - |
| min | 最小值 | number | - | 1 | - |
| max | 最大值 | number | - | Number.MAX_SAFE_INTEGER | - |
| step | 步进值 | number | - | 1 | - |
| stepStrictly | 是否严格按照步进值递增或递减 | boolean | - | false | - |
| precision | 数值精度（小数位数） | number \| string | - | 0 | - |
| disabled | 是否禁用整个组件 | boolean | - | false | - |
| disableInput | 是否禁用输入框（仅可点击按钮） | boolean | - | false | - |
| disableMinus | 是否禁用减号按钮 | boolean | - | false | - |
| disablePlus | 是否禁用加号按钮 | boolean | - | false | - |
| withoutInput | 是否不显示输入框 | boolean | - | false | - |
| inputWidth | 输入框宽度 | number \| string | - | 36 | - |
| allowNull | 是否允许为空 | boolean | - | false | - |
| placeholder | 输入框占位符 | string | - | '' | - |
| adjustPosition | 键盘弹起时，是否自动上推页面 | boolean | - | true | - |
| beforeChange | 输入值变化前的回调函数，返回 `false` 可阻止输入，支持返回 `Promise` | Function | - | - | - |
| longPress | 是否开启长按加减手势 | boolean | - | false | - |
| immediateChange | 是否立即响应输入变化，false 时仅在失焦和按钮点击时更新 | boolean | - | true | - |
| updateOnInit | 是否在初始化时更新 v-model 为修正后的值 | boolean | - | true | - |
| inputType | 输入框类型 | string | number / digit | digit | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点类名 | string | - | '' | - |

### Events

| 事件名 | 说明 | 回调参数 | 最低版本 |
|--------|------|----------|----------|
| update:modelValue | 绑定值变化时触发 | 当前数值（number \| string） | - |
| change | 数值变化时触发 | { value: 当前数值 } | - |
| focus | 输入框聚焦时触发 | 原生 focus 事件 detail | - |
| blur | 输入框失焦时触发 | { value: 当前输入值 } | - |

### Methods

通过组件 ref 可调用以下方法：

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | 本组件未暴露外部可调用的方法 | - | - |

### Slots

| 插槽名 | 说明 | 最低版本 |
|--------|------|----------|
| - | 本组件不支持插槽 | - |

---

## 使用示例

### 示例一：基本用法

最基础的数字输入框，支持加减按钮和直接输入。

```vue
<template>
  <view>
    <!-- 基础用法 -->
    <wd-input-number v-model="value1" @change="handleChange" />

    <!-- 设置步长 -->
    <wd-input-number v-model="value2" :step="2" @change="handleChange" />

    <!-- 限制最大最小值 -->
    <wd-input-number v-model="value3" :min="3" :max="10" @change="handleChange" />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(1)
const value2 = ref<number>(1)
const value3 = ref<number>(1)

function handleChange({ value }: { value: number | string }) {
  console.log('当前值：', value)
}
</script>
```

### 示例二：小数精度与严格步进

支持小数精度控制和严格步进模式，适用于金额、规格等需要精确数值的场景。

```vue
<template>
  <view>
    <!-- 设置小数精度 -->
    <wd-input-number
      v-model="value1"
      :precision="1"
      :step="0.1"
      @change="handleChange"
    />

    <!-- 输入严格为步数的倍数 -->
    <wd-input-number
      v-model="value2"
      step-strictly
      :step="2"
      @change="handleChange"
    />

    <!-- 严格步进 + 边界限制 -->
    <view class="strict-bounds-demo">
      <view class="demo-description">
        值：{{ value3 }}（步进值2，最小值3，最大值15，严格步进模式）
      </view>
      <wd-input-number
        v-model="value3"
        step-strictly
        :step="2"
        :min="3"
        :max="15"
        @change="handleChange"
      />
      <view class="demo-note">
        尝试输入各种值：
        <br />
        - 输入1 -> 自动调整为4（>=3的最小2的倍数）
        <br />
        - 输入5 -> 自动调整为4（最接近的2的倍数）
        <br />
        - 输入17 -> 自动调整为14（<=15的最大2的倍数）
      </view>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<string>('1.2')
const value2 = ref<number>(1)
const value3 = ref<number>(4)

function handleChange({ value }: { value: number | string }) {
  console.log('当前值：', value)
}
</script>

<style lang="scss" scoped>
.strict-bounds-demo {
  .demo-description {
    font-size: 14px;
    color: #333;
    margin-bottom: 8px;
    font-weight: 500;
  }

  .demo-note {
    font-size: 12px;
    color: #999;
    margin-top: 12px;
    line-height: 1.4;
    padding: 8px;
    background: #f5f5f5;
    border-radius: 4px;
  }

  .wd-input-number {
    margin-bottom: 16px;
  }
}
</style>
```

### 示例三：禁用状态与无输入框模式

多种禁用方式以及隐藏输入框的纯按钮模式。

```vue
<template>
  <view>
    <!-- 完全禁用 -->
    <wd-input-number v-model="value1" disabled @change="handleChange" />

    <!-- 仅禁用输入框（只能通过按钮操作） -->
    <wd-input-number v-model="value2" disable-input @change="handleChange" />

    <!-- 仅禁用减号按钮 -->
    <wd-input-number v-model="value3" disable-minus @change="handleChange" />

    <!-- 仅禁用加号按钮 -->
    <wd-input-number v-model="value4" disable-plus @change="handleChange" />

    <!-- 无输入框模式，仅显示加减按钮 -->
    <view class="flex">
      <view>数量：{{ value5 }}</view>
      <wd-input-number v-model="value5" without-input @change="handleChange" />
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(2)
const value2 = ref<number>(1)
const value3 = ref<number>(1)
const value4 = ref<number>(1)
const value5 = ref<number>(1)

function handleChange({ value }: { value: number | string }) {
  console.log('当前值：', value)
}
</script>

<style lang="scss" scoped>
.flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
```

### 示例四：空值支持与长按加减

支持输入框为空以及长按连续增减的交互体验。

```vue
<template>
  <view>
    <!-- 允许空值，并设置 placeholder -->
    <wd-input-number
      v-model="value1"
      allow-null
      placeholder="不限"
      input-width="70px"
      @change="handleChange"
    />

    <!-- 非允许空值但可临时删除 -->
    <view class="temp-empty-demo">
      <view class="demo-description">
        值：{{ value2 }}（可以删除为空，但失焦时会自动修正为最小值）
      </view>
      <wd-input-number
        v-model="value2"
        :allow-null="false"
        :min="1"
        @change="handleChange"
      />
      <view class="demo-note">
        尝试删除输入框中的所有内容，然后点击其他地方失焦，会自动修正为最小值1
      </view>
    </view>

    <!-- 长按加减按钮连续增减 -->
    <wd-input-number v-model="value3" long-press @change="handleChange" />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<string>('')
const value2 = ref<number>(1)
const value3 = ref<number>(1)

function handleChange({ value }: { value: number | string }) {
  console.log('当前值：', value)
}
</script>

<style lang="scss" scoped>
.temp-empty-demo {
  .demo-description {
    font-size: 14px;
    color: #333;
    margin-bottom: 8px;
    font-weight: 500;
  }

  .demo-note {
    font-size: 12px;
    color: #999;
    margin-top: 12px;
    line-height: 1.4;
    padding: 8px;
    background: #f5f5f5;
    border-radius: 4px;
  }

  .wd-input-number {
    margin-bottom: 16px;
  }
}
</style>
```

### 示例五：异步变更与非立即更新模式

通过 beforeChange 实现异步校验，以及通过 immediateChange 控制更新时机。

```vue
<template>
  <view>
    <!-- 异步变更 -->
    <wd-input-number v-model="value1" :before-change="beforeChange" />

    <!-- 立即更新模式（默认）与非立即更新模式对比 -->
    <view class="immediate-demo">
      <view class="demo-title">立即更新模式（默认）- 值：{{ value2 }}</view>
      <wd-input-number
        v-model="value2"
        :immediate-change="true"
        @change="handleChange"
      />
      <view class="demo-title">非立即更新模式 - 值：{{ value3 }}</view>
      <wd-input-number
        v-model="value3"
        :immediate-change="false"
        @change="handleChange"
      />
      <view class="demo-note">
        在输入框中输入内容时，上方的值会立即更新，下方的值仅在失焦或点击按钮时更新
      </view>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { InputNumberBeforeChange } from '@/uni_modules/wot-ui-plus/components/wd-input-number/types'

const value1 = ref<number>(1)
const value2 = ref<number>(1)
const value3 = ref<number>(1)

function handleChange({ value }: { value: number | string }) {
  console.log('当前值：', value)
}

const beforeChange: InputNumberBeforeChange = (value) => {
  console.log('正在更新到：', value)
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log('更新完成')
      resolve(true)
    }, 500)
  })
}
</script>

<style lang="scss" scoped>
.immediate-demo {
  .demo-title {
    font-size: 14px;
    color: #333;
    margin-bottom: 8px;
    font-weight: 500;
  }

  .demo-note {
    font-size: 12px;
    color: #999;
    margin-top: 12px;
    line-height: 1.4;
    padding: 8px;
    background: #f5f5f5;
    border-radius: 4px;
  }

  .wd-input-number {
    margin-bottom: 16px;
  }
}
</style>
```

---

## 注意事项

1. **modelValue 必填**：`modelValue` 为必需属性，必须通过 v-model 绑定一个初始值。

2. **严格步进模式下的边界处理**：当 `stepStrictly` 为 `true` 时，组件会将超出边界的值调整到最近的合法步进值。例如步进值为 2、最小值为 3、最大值为 15 时，输入 1 会被调整为 4（>=3 的最小 2 的倍数），输入 17 会被调整为 14（<=15 的最大 2 的倍数）。

3. **精度与步进的关系**：`precision` 控制小数位数，当需要小数步进时（如 0.1），需要同时设置 `:precision="1"` 和 `:step="0.1"`，否则输入的小数可能被截断。

4. **allowNull 空值行为**：当 `allowNull` 为 `true` 时，用户可以清空输入框，此时 v-model 的值变为空字符串 `''`；当 `allowNull` 为 `false` 时，用户虽然可以临时删除内容，但在失焦时会自动修正为 `min` 值。

5. **immediateChange 更新时机**：默认为 `true`，即每次输入都会实时更新 v-model。设置为 `false` 时，仅在输入框失焦或点击加减按钮时才更新 v-model，适用于需要在失焦后统一校验的场景。

6. **beforeChange 异步拦截**：`beforeChange` 回调函数接收新值作为参数，可返回布尔值或 `Promise<boolean>`。返回 `false` 或 `Promise.resolve(false)` 时，将阻止数值变化。

7. **长按手势时间**：开启 `longPress` 后，长按 600ms 触发第一次步进，之后每 250ms 触发一次。松手即停止。

8. **updateOnInit 初始化修正**：默认为 `true`，初始化时会自动将 v-model 修正为合法的数值。设置为 `false` 时，不会修改原始绑定值，但仍会进行显示格式化。

9. **输入框类型**：`inputType` 默认为 `digit`（整数键盘），如需支持小数输入，请设置为 `number`。同时组件会根据 `precision` 自动设置 `input-mode` 为 `decimal` 或 `numeric`。

10. **自定义样式**：使用 `customStyle` 属性时，样式值应为字符串形式的内联样式，如 `"margin: 10px;"`。使用 `customClass` 属性可添加自定义 CSS 类名。
