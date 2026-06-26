# PasswordInput 密码输入框


## 组件概况

PasswordInput 密码输入框组件是一个用于安全密码输入的展示型组件，提供格子化的密码输入框外观，支持掩码/明文切换、自定义长度、格子间距控制、错误提示等功能。该组件本身不处理输入逻辑，需要搭配数字键盘（如 NumberKeyboard）使用，通过 `v-model` 双向绑定输入值。适用于支付密码、安全码、登录密码等需要安全输入的场景。

## 核心功能描述

- **掩码/明文切换**：通过 `mask` 属性控制是否隐藏密码内容（圆点掩码 vs 明文展示）
- **自定义长度**：通过 `length` 属性设置密码位数，默认为 6 位
- **格子间距**：通过 `gutter` 属性设置格子之间的间距，支持 `px`、`em` 等单位
- **错误提示**：通过 `error-info` 属性显示错误信息，优先级高于普通 `info` 提示
- **信息提示**：通过 `info` 属性在输入框下方显示提示信息
- **聚焦光标**：通过 `focused` 属性控制是否显示输入光标，光标出现在已输入内容的下一位
- **双向绑定**：支持 `v-model` 绑定密码值
- **点击聚焦**：点击密码输入框区域会触发 `focus` 事件，可用于联动弹出数字键盘

## 适用业务场景

- **支付密码输入**：搭配 NumberKeyboard 使用，6 位数字支付密码，掩码展示
- **登录密码输入**：明文/掩码切换，支持自定义长度
- **安全码验证**：如 CVV 码、动态口令等短密码输入
- **密码重置**：带错误提示的新密码设置，输入格式错误时显示错误信息
- **两步验证**：二次安全验证场景的密码输入

## API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | string | '' | 否 | 绑定的值，支持 v-model 双向绑定 |
| mask | boolean | true | 否 | 是否隐藏密码内容（掩码模式） |
| length | number | 6 | 否 | 密码格子最大长度 |
| gutter | `string \| number` | 0 | 否 | 输入框格子之间的间距，如 20px、2em，默认单位为 px |
| focused | boolean | true | 否 | 是否已聚焦，聚焦时会显示光标 |
| info | string | '' | 否 | 输入框下方文字提示 |
| errorInfo | string | '' | 否 | 输入框下方错误提示（优先级高于 info） |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点类名 |

### Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| focus | (event: Event) | 点击密码输入框区域时触发，返回原生触摸事件对象 |

### Methods

组件不对外暴露任何方法。

### Slots

组件不对外暴露任何插槽。

## 使用示例

### 示例 1：基本用法

展示默认的 6 位密码输入框，搭配数字键盘使用。

```vue
<template>
  <view>
    <wd-password-input
      v-model="value"
      :focused="visible"
      @focus="visible = true"
    />

    <wd-number-keyboard
      v-model:visible="visible"
      v-model="value"
      :maxlength="6"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const value = ref<string>('')
  const visible = ref<boolean>(true)
</script>
```

PasswordInput 负责展示密码输入框的外观（掩码圆点、光标、格子），NumberKeyboard 负责数字输入。点击 PasswordInput 区域触发 `focus` 事件弹出键盘。`mask` 默认为 `true`，输入内容以圆点掩码展示。`length` 默认为 6，展示 6 个密码格子。

### 示例 2：自定义长度

设置自定义的密码位数，如 4 位安全码。

```vue
<template>
  <view>
    <wd-password-input
      v-model="value"
      :length="4"
      :focused="visible"
      @focus="showKeyboard"
    />

    <wd-number-keyboard
      v-model:visible="visible"
      v-model="value"
      :maxlength="4"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const value = ref<string>('')
  const visible = ref<boolean>(false)

  function showKeyboard() {
    visible.value = true
  }
</script>
```

通过 `length` 属性设置密码格子的数量，设置为 4 时显示 4 个格子。注意 `NumberKeyboard` 的 `maxlength` 需与 `length` 保持一致，确保键盘输入长度与显示格子匹配。

### 示例 3：设置格子间距

调整密码格子之间的间距，改变视觉布局效果。

```vue
<template>
  <view>
    <wd-password-input
      v-model="value"
      :gutter="10"
      :focused="visible"
      @focus="visible = true"
    />

    <wd-number-keyboard
      v-model:visible="visible"
      v-model="value"
      :maxlength="6"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const value = ref<string>('')
  const visible = ref<boolean>(false)
</script>
```

通过 `gutter` 属性设置格子之间的间距。默认值为 0，格子之间无间距紧密排列。设置为 `10`（默认单位 px）后，每个格子之间有 10px 的间隔。支持自定义单位，如 `'2em'`、`'20px'` 等。

### 示例 4：明文展示

将密码掩码关闭，以明文形式展示输入的字符。

```vue
<template>
  <view>
    <wd-password-input
      v-model="value"
      :mask="false"
      :focused="visible"
      @focus="visible = true"
    />

    <wd-number-keyboard
      v-model:visible="visible"
      v-model="value"
      :maxlength="6"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const value = ref<string>('')
  const visible = ref<boolean>(false)
</script>
```

设置 `:mask="false"` 关闭掩码，输入的数字以明文形式展示在格子中。适用于需要用户确认输入内容的场景（如首次设置密码时的确认）。`mask` 默认为 `true`，掩码模式下已输入的位置显示圆点。

### 示例 5：提示信息与错误提示

在密码输入框下方显示普通提示和错误提示。

```vue
<template>
  <view>
    <wd-password-input
      v-model="value"
      info="密码为 6 位数字"
      :error-info="errorInfo"
      :focused="visible"
      @focus="visible = true"
    />

    <wd-number-keyboard
      v-model:visible="visible"
      v-model="value"
      :maxlength="6"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref, watch } from 'vue'

  const value = ref<string>('')
  const visible = ref<boolean>(false)
  const errorInfo = ref<string>('')

  // 监听输入值，验证密码格式
  watch(value, (newVal) => {
    if (newVal.length === 6 && newVal !== '123456') {
      errorInfo.value = '密码错误'
    } else {
      errorInfo.value = ''
    }
  })
</script>
```

`info` 属性显示普通提示文字（如 "密码为 6 位数字"）。`error-info` 显示错误提示，当 `error-info` 有值时，会优先显示并覆盖 `info` 内容，同时文字颜色变为红色。当 `error-info` 为空字符串时，回退显示 `info` 内容。可在 `watch` 中监听输入值进行实时验证。

### 示例 6：多场景组合

展示多种属性的组合使用方式。

```vue
<template>
  <view>
    <!-- 4 位密码 + 间距 -->
    <wd-password-input
      v-model="value1"
      :length="4"
      :gutter="8"
      :focused="visible1"
      @focus="visible1 = true"
    />
    <wd-number-keyboard
      v-model:visible="visible1"
      v-model="value1"
      :maxlength="4"
    />

    <!-- 6 位密码 + 明文 + 提示 -->
    <wd-password-input
      v-model="value2"
      :mask="false"
      :length="6"
      info="请输入 6 位支付密码"
      :focused="visible2"
      @focus="visible2 = true"
    />
    <wd-number-keyboard
      v-model:visible="visible2"
      v-model="value2"
      :maxlength="6"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const value1 = ref<string>('')
  const value2 = ref<string>('')
  const visible1 = ref<boolean>(false)
  const visible2 = ref<boolean>(false)
</script>
```

通过组合不同属性，实现不同的展示效果：`length` + `gutter` 控制格子数量和间距，`mask="false"` + `info` 实现明文输入加提示。每个 PasswordInput 搭配独立的 NumberKeyboard 实例，通过各自的 `visible` 状态控制键盘显隐。

## 注意事项

1. **PasswordInput 是纯展示组件**：PasswordInput 不处理任何输入逻辑，所有输入操作需通过外部键盘（如 NumberKeyboard）的 `v-model` 传入值。组件内部通过 `v-for="(_, index) in length"` 渲染对应数量的格子
2. **点击聚焦机制**：PasswordInput 使用 `@touchstart` 触发 `focus` 事件，用户点击组件区域时会向外发出 `focus` 事件，可用于联动弹出数字键盘
3. **光标显示逻辑**：当 `focused` 为 `true` 且当前格子索引等于已输入内容长度时，显示闪烁光标（`wd-password-input__cursor`），光标出现在下一个空位
4. **掩码实现方式**：掩码模式 (`mask=true`) 下，通过 `wd-password-input__mask` 遮罩层实现圆点效果。当 `mask && modelValue[index]` 为真时，遮罩层 `visibility` 设为 `visible`；明文模式 (`mask=false`) 下遮罩层隐藏，直接渲染字符文本
5. **errorInfo 优先级高于 info**：当 `errorInfo` 有值（非空字符串）时，输入框下方显示 `errorInfo` 内容并添加 `is-error` 样式类（红色文字）；只有 `errorInfo` 为空时才显示 `info` 内容
6. **gutter 支持多种单位**：`gutter` 属性值为 `numeric` 类型，可直接传数字（默认 px），也可传带单位的字符串（如 `'2em'`、`'20px'`）。默认值为 0，格子紧密排列
7. **focused 默认值为 true**：`focused` 属性默认为 `true`，组件挂载时即显示光标。如需键盘未弹出时隐藏光标，应将其绑定为键盘的显隐状态
8. **length 控制格子数量**：`length` 决定渲染多少个密码格子。输入值长度超过 `length` 时，超出的字符不会显示在格子中（因为 `v-for` 只遍历 `length` 次）
9. **搭配自定义键盘**：推荐搭配 NumberKeyboard 使用，形成完整的密码输入交互。PasswordInput 展示输入状态，NumberKeyboard 处理输入逻辑，通过 `v-model` 双向绑定同步数据
10. **无预置键盘功能**：与 CodeInput 不同，PasswordInput 不包含原生 input 元素，完全依赖外部输入。如果需要隐藏系统键盘，请配合 CodeInput 的 `disabled-keyboard` 属性或直接使用 NumberKeyboard
