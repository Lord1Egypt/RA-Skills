# Input 输入框


输入框允许用户通过键盘或手写输入文本内容，是表单和数据录入场景中最基础的交互组件之一。

## 组件概况

Input 组件是一个高度可定制的输入框组件，支持多种输入类型（文本、数字、身份证、手机号等）、密码模式、清空按钮、字数限制、前后置图标等功能。组件内置了与表单校验系统的集成能力，可与 `wd-form` 组件配合使用实现完整的表单验证流程。

### 核心功能描述

- **多种输入类型**：支持 text、number、digit、idcard、safe-password、nickname、tel 等类型
- **密码模式**：内置密码显示/隐藏切换功能
- **清空控制**：支持始终显示或聚焦时显示清空按钮，可控制清空后是否自动聚焦
- **字数限制与统计**：支持最大长度限制及实时字数统计显示
- **图标插槽**：支持前后置图标，支持图标插槽自定义
- **标签对齐**：支持左侧标题、标签宽度自定义、必填标记位置控制
- **表单集成**：原生支持 wd-form 表单校验，显示错误提示信息
- **样式定制**：支持边框类型切换（边框/下划线/无边框）、尺寸切换、右对齐等
- **键盘控制**：支持键盘右下角按钮文字自定义、光标位置控制、键盘距离控制等
- **合成事件**：支持忽略或处理文本合成系统事件（composition event）

### 适用业务场景

- 用户注册/登录表单中的账号密码输入
- 搜索框输入
- 金额、数量等数字输入
- 手机号、身份证号等特定格式输入
- 需要字数限制的评论、备注输入

---

## API

### Props

| 参数 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|------|------|------|--------|--------|----------|
| modelValue / v-model | 绑定值 | string \| number | - | '' | - |
| type | 输入框类型 | string | text / number / digit / idcard / safe-password / nickname / tel | text | - |
| placeholder | 占位文本 | string | - | 请输入... | - |
| placeholderStyle | 原生属性，指定 placeholder 的样式，目前仅支持 color、font-size 和 font-weight | string | - | - | - |
| placeholderClass | 原生属性，指定 placeholder 的样式类 | string | - | '' | - |
| disabled | 是否禁用 | boolean | - | false | - |
| readonly | 是否只读 | boolean | - | false | - |
| clearable | 是否显示清空按钮 | boolean | - | false | - |
| clearTrigger | 清空按钮显示时机 | string | always / focus | always | - |
| focusWhenClear | 点击清空按钮时是否自动聚焦 | boolean | - | true | - |
| showPassword | 是否显示为密码框 | boolean | - | false | - |
| showWordLimit | 是否显示字数限制 | boolean | - | false | - |
| maxlength | 最大输入长度 | number | - | -1 | - |
| label | 左侧标题 | string | - | - | - |
| labelWidth | 左侧标题宽度 | string | - | '' | - |
| size | 输入框大小 | string | large | - | - |
| error | 是否显示错误状态 | boolean | - | false | - |
| center | 标题和输入框是否垂直居中 | boolean | - | false | - |
| alignRight | 输入框内容是否靠右展示 | boolean | - | false | - |
| required | 是否必填 | boolean | - | false | - |
| markerSide | 必填标记位置 | string | before / after | before | - |
| prefixIcon | 前置图标名称 | string | - | - | - |
| suffixIcon | 后置图标名称 | string | - | - | - |
| noBorder | 非 cell 类型下是否隐藏下划线 | boolean | - | false | - |
| inputBorder | 边框类型 | string | border / underline / none | underline | - |
| prop | 表单域 model 字段名，用于表单校验 | string | - | - | - |
| rules | 表单验证规则 | FormItemRule[] | - | [] | - |
| focus | 是否获取焦点 | boolean | - | false | - |
| confirmType | 键盘右下角按钮文字 | string | send / search / next / go / done | done | - |
| confirmHold | 点击键盘右下角按钮时是否保持键盘不收起 | boolean | - | false | - |
| cursorSpacing | 光标与键盘的距离 | number | - | 0 | - |
| cursor | focus 时的光标位置 | number | - | -1 | - |
| selectionStart | 光标起始位置 | number | - | -1 | - |
| selectionEnd | 光标结束位置 | number | - | -1 | - |
| adjustPosition | 键盘弹起时是否自动上推页面 | boolean | - | true | - |
| holdKeyboard | focus 时点击页面不收起键盘 | boolean | - | false | - |
| alwaysEmbed | 微信小程序：强制 input 处于同层状态 | boolean | - | false | - |
| ignoreCompositionEvent | 是否忽略文本合成系统事件 | boolean | - | true | - |
| inputmode | 编辑元素时可能输入的数据类型提示 | string | none / text / decimal / numeric / tel / search / email / url | text | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点类名 | string | - | '' | - |
| customInputClass | 自定义输入框类名 | string | - | '' | - |
| customLabelClass | 自定义标签类名 | string | - | '' | - |

### Events

| 事件名 | 说明 | 回调参数 | 最低版本 |
|--------|------|----------|----------|
| update:modelValue | 绑定值变化时触发 | 输入框当前值 | - |
| input | 输入时触发 | 原生 input 事件 detail | - |
| focus | 聚焦时触发 | 原生 focus 事件 detail | - |
| blur | 失焦时触发 | { value: 当前值 } | - |
| confirm | 点击键盘完成按钮时触发 | 原生 confirm 事件 detail | - |
| keyboardheightchange | 键盘高度变化时触发 | 原生 keyboardheightchange 事件 detail | - |
| clear | 点击清空按钮时触发 | - | - |
| click | 点击组件时触发 | MouseEvent | - |
| clickprefixicon | 点击前置图标时触发 | - | - |
| clicksuffixicon | 点击后置图标时触发 | - | - |

### Slots

| 插槽名 | 说明 | 最低版本 |
|--------|------|----------|
| prefix | 前置图标插槽，覆盖 prefixIcon 属性 | - |
| suffix | 后置图标插槽，覆盖 suffixIcon 属性 | - |
| label | 标题插槽，覆盖 label 属性 | - |

---

## 使用示例

### 示例一：基本用法

最基础的输入框，支持双向绑定和输入事件监听。

```vue
<template>
  <view>
    <wd-input v-model="value" placeholder="请输入内容" @input="handleInput" />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref<string>('')

function handleInput(event: any) {
  console.log('输入内容：', event)
}
</script>
```

### 示例二：带清空按钮和密码模式

适用于需要频繁输入和清除的场景，如搜索框、登录表单等。

```vue
<template>
  <view>
    <!-- 带清空按钮的输入框 -->
    <wd-input v-model="searchValue" placeholder="搜索商品" clearable />

    <!-- 密码输入框，支持显示/隐藏密码 -->
    <wd-input
      v-model="password"
      placeholder="请输入密码"
      clearable
      show-password
      type="text"
    />

    <!-- 聚焦时才显示清空按钮 -->
    <wd-input
      v-model="focusValue"
      placeholder="聚焦时显示清空按钮"
      clearable
      clear-trigger="focus"
    />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const searchValue = ref<string>('')
const password = ref<string>('')
const focusValue = ref<string>('')
</script>
```

### 示例三：带前后置图标和字数限制

适用于需要视觉提示和长度限制的场景，如手机号输入、验证码输入等。

```vue
<template>
  <view>
    <!-- 带前后置图标的输入框 -->
    <wd-input
      v-model="phone"
      placeholder="请输入手机号"
      prefix-icon="phone"
      suffix-icon="arrow-down"
      clearable
      type="tel"
    />

    <!-- 带字数统计的输入框 -->
    <wd-input
      v-model="content"
      placeholder="请输入内容，最多50个字符"
      :maxlength="50"
      show-word-limit
    />

    <!-- 自定义输入区域组合 -->
    <wd-input
      v-model="price"
      placeholder="请输入价格"
      no-border
      custom-style="display: inline-block; width: 70px; vertical-align: middle;"
    />
    <text style="display: inline-block; vertical-align: middle; font-size: 14px; line-height: 24px;">元</text>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const phone = ref<string>('')
const content = ref<string>('')
const price = ref<string>('')
</script>
```

### 示例四：Cell 组合用法

与 `wd-cell-group` 配合使用，适用于表单页面布局。

```vue
<template>
  <view>
    <wd-cell-group border>
      <!-- 基础输入 -->
      <wd-input
        v-model="form.name"
        label="姓名"
        placeholder="请输入姓名"
        clearable
      />

      <!-- 必填输入 -->
      <wd-input
        v-model="form.phone"
        label="手机号"
        placeholder="请输入手机号"
        required
        type="tel"
      />

      <!-- 带插槽的输入 -->
      <wd-input
        v-model="form.code"
        label="验证码"
        placeholder="请输入验证码"
        clearable
      >
        <template #suffix>
          <wd-button size="small" custom-class="button">获取验证码</wd-button>
        </template>
      </wd-input>

      <!-- 大尺寸输入 -->
      <wd-input
        v-model="form.email"
        label="邮箱"
        placeholder="请输入邮箱"
        size="large"
        clearable
      />
    </wd-cell-group>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const form = ref({
  name: '',
  phone: '',
  code: '',
  email: ''
})
</script>
```

### 示例五：数字类型和边框样式

控制输入数据类型和视觉表现。

```vue
<template>
  <view>
    <!-- 数字类型输入 -->
    <wd-input
      v-model="age"
      placeholder="请输入年龄"
      type="number"
    />

    <!-- 带边框样式 -->
    <wd-input
      v-model="name"
      placeholder="带完整边框"
      input-border="border"
      prefix-icon="user"
      suffix-icon="arrow-right"
    />

    <!-- 禁用状态 -->
    <wd-input
      v-model="disabledValue"
      placeholder="禁用状态"
      disabled
    />

    <!-- 只读状态 -->
    <wd-input
      v-model="readonlyValue"
      placeholder="只读状态"
      readonly
    />

    <!-- 错误状态 -->
    <wd-input
      v-model="errorValue"
      placeholder="错误状态"
      error
    />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const age = ref<number | ''>('')
const name = ref<string>('')
const disabledValue = ref<string>('禁用内容')
const readonlyValue = ref<string>('只读内容')
const errorValue = ref<string>('错误内容')
</script>
```

---

## 注意事项

1. **maxlength 设置**：当设置 `show-word-limit` 为 `true` 时，必须同时设置 `maxlength` 属性，否则字数统计不会显示。

2. **清空按钮触发时机**：`clearTrigger` 属性默认为 `always`，即输入框有值时始终显示清空按钮。设置为 `focus` 时，只有在输入框聚焦且有值时才会显示清空按钮。

3. **清空后聚焦行为**：默认情况下，点击清空按钮后会自动重新聚焦输入框。如果不需要此行为，可设置 `focus-when-clear` 为 `false`。

4. **密码模式**：使用 `show-password` 时，`type` 建议设置为 `text`，因为密码显示/隐藏切换是通过控制原生 `password` 属性实现的。

5. **只读与禁用区别**：
   - `disabled` 状态下输入框完全不可交互，不显示清空按钮和字数统计
   - `readonly` 状态下输入框仅不可编辑，但仍可选择和复制内容

6. **数字类型限制**：`type="number"` 在部分平台可能允许输入小数点，如果需要严格的整数输入，建议使用 `type="digit"`。

7. **键盘类型**：`confirmType` 属性仅在 `type="text"` 时生效，用于控制键盘右下角按钮的文字。

8. **表单校验**：使用 `prop` 和 `rules` 属性进行表单校验时，需要将组件放在 `wd-form` 和 `wd-form-item` 中。

9. **自定义样式**：使用 `customStyle` 属性时，样式值应为字符串形式的内联样式，如 `"margin: 10px; color: red;"`。

10. **合成事件处理**：`ignoreCompositionEvent` 默认为 `true`，即忽略 composition 事件。如果需要在中文输入法输入过程中实时获取输入内容，可设置为 `false`。
