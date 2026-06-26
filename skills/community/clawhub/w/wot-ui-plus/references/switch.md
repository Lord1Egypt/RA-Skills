# Switch 开关


## 组件概述

开关组件用于表示两种相互对立的状态，如开/关、启用/禁用等。用户通过点击切换状态，常用于设置项、权限控制等场景。组件支持自定义颜色、尺寸、绑定值类型，并提供改变前拦截钩子。

## 核心功能

- **双向绑定**：通过 `v-model` 实现开关状态的双向绑定
- **自定义值类型**：支持 `boolean`、`string`、`number` 三种绑定值类型，通过 `active-value` 和 `inactive-value` 自定义激活/非激活值
- **颜色定制**：支持自定义激活颜色、非激活颜色和圆点颜色
- **尺寸可调**：通过 `size` 属性控制开关大小
- **禁用状态**：支持禁用交互，视觉上呈现灰色不可操作样式
- **改变前拦截**：通过 `beforeChange` 钩子函数实现异步确认、权限校验等前置逻辑
- **状态校验**：初始化时自动校验绑定值是否在合法范围内，非法值会被重置为 `inactive-value`

## 适用业务场景

- 系统设置中的功能开关（如通知开关、夜间模式）
- 表单中的二元选择项
- 权限控制、状态启用/禁用操作
- 需要二次确认的状态切换（如删除保护、重要设置变更）

## API

### Props

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
|------|------|------|--------|--------|
| model-value / v-model | 绑定值，支持 boolean / string / number | `boolean \| string \| number` | - | `false` |
| disabled | 是否禁用 | `boolean` | - | `false` |
| active-value | 激活时的值 | `boolean \| string \| number` | - | `true` |
| inactive-value | 非激活时的值 | `boolean \| string \| number` | - | `false` |
| active-color | 激活时的背景颜色 | `string` | - | - |
| inactive-color | 非激活时的背景颜色 | `string` | - | - |
| circle-color | 圆点颜色 | `string` | - | - |
| size | 开关大小 | `number \| string` | - | - |
| before-change | 改变前执行的钩子函数，接收 `{ value, resolve }` 参数，调用 `resolve(true)` 确认切换，`resolve(false)` 取消切换 | `SwitchBeforeChange` | - | - |
| custom-style | 自定义根节点样式 | `string` | - | `''` |
| custom-class | 自定义根节点样式类 | `string` | - | `''` |

### Events

| 事件名称 | 说明 | 参数 |
|----------|------|------|
| change | 开关状态变化时触发 | `{ value: boolean \| string \| number }` 切换后的值 |

### Slots

无。

### 类型定义

```typescript
export type SwitchBeforeChangeOption = {
  value: number | string | boolean
  resolve: (pass: boolean) => void
}

export type SwitchBeforeChange = (option: SwitchBeforeChangeOption) => void
```

## 使用示例

### 示例一：基础用法

最简单的开关用法，绑定布尔值。

```vue
<template>
  <wd-switch v-model="checked1" @change="handleChange" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checked1 = ref<boolean>(true)

function handleChange({ value }: any) {
  console.log('开关值变化:', value)
}
</script>
```

### 示例二：自定义激活/非激活值

通过 `active-value` 和 `inactive-value` 自定义开关绑定的值类型和具体值。

```vue
<template>
  <view class="switch-demo">
    <view class="desc">当前值: {{ checked2 }}</view>
    <wd-switch
      v-model="checked2"
      active-value="你好"
      inactive-value="世界"
      @change="handleChange"
    />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checked2 = ref<string>('世界')

function handleChange({ value }: any) {
  console.log('开关值变化:', value)
}
</script>

<style lang="scss" scoped>
.switch-demo {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.desc {
  font-size: 14px;
  color: #333;
}
</style>
```

### 示例三：自定义颜色

使用 `active-color`、`inactive-color` 和 `circle-color` 自定义开关的外观颜色。

```vue
<template>
  <wd-switch
    v-model="checked3"
    active-color="#13ce66"
    inactive-color="#f00"
    circle-color="#333333"
    @change="handleChange"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checked3 = ref<boolean>(true)

function handleChange({ value }: any) {
  console.log('开关值变化:', value)
}
</script>
```

### 示例四：自定义尺寸

通过 `size` 属性设置不同大小的开关。

```vue
<template>
  <view class="switch-sizes">
    <wd-switch v-model="checked4" :size="24" @change="handleChange" />
    <wd-switch v-model="checked4" @change="handleChange" />
    <wd-switch v-model="checked4" :size="34" @change="handleChange" />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checked4 = ref<boolean>(true)

function handleChange({ value }: any) {
  console.log('开关值变化:', value)
}
</script>

<style lang="scss" scoped>
.switch-sizes {
  display: flex;
  align-items: center;
  gap: 16px;
}
</style>
```

### 示例五：禁用状态

开关在禁用状态下无法切换，分为选中禁用和非选中禁用两种情况。

```vue
<template>
  <view class="switch-disabled">
    <view class="item">
      <text class="label">选中禁用</text>
      <wd-switch v-model="checked5" disabled />
    </view>
    <view class="item">
      <text class="label">非选中禁用</text>
      <wd-switch v-model="checked6" disabled />
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checked5 = ref<boolean>(true)
const checked6 = ref<boolean>(false)
</script>

<style lang="scss" scoped>
.switch-disabled {
  .item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 0;
    
    .label {
      font-size: 14px;
      color: #333;
    }
  }
}
</style>
```

### 示例六：改变前拦截（before-change）

使用 `before-change` 钩子在状态切换前进行二次确认，用户确认后才执行切换。

```vue
<template>
  <view>
    <wd-message-box />
    <wd-switch
      v-model="checked7"
      :before-change="beforeChange"
      @change="handleChange"
    />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useMessage } from '@/uni_modules/wot-ui-plus'
import type { SwitchBeforeChange } from '@/uni_modules/wot-ui-plus/components/wd-switch/types'

const checked7 = ref<boolean>(false)
const message = useMessage()

const beforeChange: SwitchBeforeChange = ({ value, resolve }) => {
  message
    .confirm('是否切换开关?')
    .then(() => {
      resolve(true)
    })
    .catch(() => {
      resolve(false)
    })
}

function handleChange({ value }: any) {
  console.log('开关值变化:', value)
}
</script>
```

## 注意事项

1. **绑定值类型**：`v-model` 绑定的值类型可以是 `boolean`、`string`、`number`，但必须与 `active-value` 和 `inactive-value` 的类型保持一致，否则可能导致状态判断异常。

2. **默认值对应关系**：默认情况下，`active-value` 为 `true`，`inactive-value` 为 `false`。如果自定义了这两个属性，需要确保 `v-model` 的初始值是其中之一。

3. **非法值处理**：组件在 `onBeforeMount` 阶段会检查 `modelValue` 是否在 `[activeValue, inactiveValue]` 范围内。如果不在，会自动将值重置为 `inactiveValue` 并触发 `change` 事件。

4. **before-change 钩子**：该钩子函数是异步的，必须调用 `resolve(true)` 或 `resolve(false)` 来决定是否继续切换。如果未调用 `resolve`，开关状态将保持不变。此功能适用于需要用户确认、网络请求校验等场景。

5. **禁用状态**：当 `disabled` 为 `true` 时，点击开关不会触发任何状态变化和事件。组件根节点会添加 `is-disabled` 样式类。

6. **颜色与圆点阴影**：当设置了 `active-color` 或 `inactive-color` 时，圆点的 `box-shadow` 会被移除（设置为 `none`）。如果同时设置了 `circle-color`，圆点背景色会使用 `circle-color` 的值。

7. **尺寸单位**：`size` 属性支持数字和字符串类型。当传入数字时，组件内部会通过 `addUnit` 方法自动添加 `px` 单位；传入字符串时原样使用。

8. **状态样式类**：组件根节点会根据状态动态添加样式类：`is-checked`（激活状态）和 `is-disabled`（禁用状态），可用于外部样式定制。

9. **点击交互**：整个开关区域（包括背景和圆点）都是可点击的，点击后触发 `switchValue` 方法进行状态切换。

10. **虚拟主机**：组件启用了 `virtualHost: true`，样式隔离配置为 `styleIsolation: 'shared'` 和 `addGlobalClass: true`，确保在小程序环境中样式可以正常穿透。
