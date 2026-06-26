# Textarea 文本域


文本域组件用于多行文本输入场景，支持高度自适应、字数限制、清空按钮等功能，适用于需要输入较长文本内容的业务场景。

## 组件概况

Textarea 组件是一个专为多行文本输入设计的组件，在基础输入能力之上增加了高度自适应、行数变化监听等特性。组件同样支持清空按钮、字数限制、表单校验等实用功能，可与 `wd-form` 组件无缝配合使用。

### 核心功能描述

- **高度自适应**：支持输入框高度随内容自动调整，提供更流畅的输入体验
- **清空控制**：支持清空按钮的显示时机控制，可配置清空后是否自动聚焦
- **字数限制与统计**：支持最大长度限制及实时字数统计，使用 `Array.from` 正确处理多码元字符长度
- **前置图标**：支持前置图标和图标插槽，增强视觉引导
- **标签对齐**：支持左侧标题、标签宽度自定义、必填标记位置控制
- **表单集成**：原生支持 wd-form 表单校验，显示错误提示信息
- **样式定制**：支持尺寸切换、边框控制、自定义样式类
- **键盘控制**：支持键盘右下角按钮自定义、光标位置控制、键盘距离控制等
- **行数变化监听**：提供 `linechange` 事件，可监听文本行数变化
- **固定区域支持**：支持在 fixed 定位区域使用

### 适用业务场景

- 用户评价、评论内容输入
- 意见反馈、投诉建议表单
- 备注、说明等多行文本录入
- 聊天记录、消息发送框
- 文章摘要、描述信息编辑

---

## API

### Props

| 参数 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|------|------|------|--------|--------|----------|
| modelValue / v-model | 绑定值 | string \| number | - | '' | - |
| placeholder | 占位文本 | string | - | 请输入... | - |
| placeholderStyle | 指定 placeholder 的样式 | string | - | - | - |
| placeholderClass | 指定 placeholder 的样式类 | string | - | '' | - |
| disabled | 是否禁用 | boolean | - | false | - |
| readonly | 是否只读 | boolean | - | false | - |
| clearable | 是否显示清空按钮 | boolean | - | false | - |
| clearTrigger | 清空按钮显示时机 | string | always / focus | always | - |
| focusWhenClear | 点击清空按钮时是否自动聚焦 | boolean | - | true | - |
| showWordLimit | 是否显示字数限制 | boolean | - | false | - |
| maxlength | 最大输入长度，-1 表示不限制 | number | - | -1 | - |
| label | 左侧标题 | string | - | - | - |
| labelWidth | 左侧标题宽度 | string | - | '' | - |
| size | 输入框大小 | string | large | - | - |
| error | 是否显示错误状态 | boolean | - | false | - |
| center | 标题和输入框是否垂直居中 | boolean | - | false | - |
| autoHeight | 是否自动增高输入框高度 | boolean | - | false | - |
| autoFocus | 是否自动聚焦并拉起键盘 | boolean | - | false | - |
| focus | 是否获取焦点 | boolean | - | false | - |
| fixed | 是否在 fixed 定位区域使用 | boolean | - | false | - |
| prefixIcon | 前置图标名称 | string | - | - | - |
| required | 是否必填 | boolean | - | false | - |
| markerSide | 必填标记位置 | string | before / after | before | - |
| noBorder | 非 cell 类型下是否隐藏下划线 | boolean | - | false | - |
| prop | 表单域 model 字段名，用于表单校验 | string | - | '' | - |
| rules | 表单验证规则 | FormItemRule[] | - | [] | - |
| cursorSpacing | 光标与键盘的距离 | number | - | 0 | - |
| cursor | focus 时的光标位置 | number | - | -1 | - |
| selectionStart | 光标起始位置 | number | - | -1 | - |
| selectionEnd | 光标结束位置 | number | - | -1 | - |
| adjustPosition | 键盘弹起时是否自动上推页面 | boolean | - | true | - |
| holdKeyboard | focus 时点击页面不收起键盘 | boolean | - | false | - |
| confirmType | 键盘右下角按钮文字 | string | send / search / next / go / done | done | - |
| confirmHold | 点击键盘右下角按钮时是否保持键盘不收起 | boolean | - | false | - |
| showConfirmBar | 是否显示键盘上方完成按钮 | boolean | - | true | - |
| disableDefaultPadding | 是否去掉 iOS 下的默认内边距 | boolean | - | false | - |
| ignoreCompositionEvent | 是否忽略文本合成系统事件 | boolean | - | true | - |
| inputmode | 编辑元素时可能输入的数据类型提示 | string | none / text / tel / url / email / numeric / decimal / search / password | text | - |
| enableNative | 支付宝小程序：避免键盘弹出后内容上移 | boolean | - | true | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点类名 | string | - | '' | - |
| customTextareaContainerClass | 自定义文本域容器类名 | string | - | '' | - |
| customTextareaClass | 自定义文本域类名 | string | - | '' | - |
| customLabelClass | 自定义标签类名 | string | - | '' | - |

### Events

| 事件名 | 说明 | 回调参数 | 最低版本 |
|--------|------|----------|----------|
| update:modelValue | 绑定值变化时触发 | 输入框当前值 | - |
| input | 输入时触发 | 原生 input 事件 detail | - |
| focus | 聚焦时触发 | 原生 focus 事件 detail | - |
| blur | 失焦时触发 | { value: 当前值, cursor: 光标位置 } | - |
| confirm | 点击键盘完成按钮时触发 | 原生 confirm 事件 detail | - |
| linechange | 行数变化时触发 | 原生 linechange 事件 detail | - |
| keyboardheightchange | 键盘高度变化时触发 | 原生 keyboardheightchange 事件 detail | - |
| clear | 点击清空按钮时触发 | - | - |
| click | 点击组件时触发 | Event | - |
| clickprefixicon | 点击前置图标时触发 | - | - |

### Slots

| 插槽名 | 说明 | 最低版本 |
|--------|------|----------|
| prefix | 前置图标插槽，覆盖 prefixIcon 属性 | - |
| label | 标题插槽，覆盖 label 属性 | - |

---

## 使用示例

### 示例一：基本用法

最基础的文本域，支持双向绑定。

```vue
<template>
  <view>
    <wd-textarea v-model="content" placeholder="请填写评价内容" />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const content = ref<string>('')
</script>
```

### 示例二：带清空按钮和字数限制

适用于需要限制输入长度并可一键清空的场景，如评论、反馈等。

```vue
<template>
  <view>
    <!-- 带清空按钮和字数限制的文本域 -->
    <wd-textarea
      v-model="feedback"
      placeholder="请输入您的反馈意见"
      :maxlength="240"
      clearable
      show-word-limit
    />

    <!-- 聚焦时才显示清空按钮 -->
    <wd-textarea
      v-model="comment"
      placeholder="请输入评论内容"
      :maxlength="500"
      clearable
      clear-trigger="focus"
      show-word-limit
    />

    <!-- 清空后不自动聚焦 -->
    <wd-textarea
      v-model="description"
      placeholder="请输入描述信息"
      :maxlength="200"
      clearable
      show-word-limit
      :focus-when-clear="false"
    />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const feedback = ref<string>('')
const comment = ref<string>('')
const description = ref<string>('')
</script>
```

### 示例三：高度自适应

文本域高度随内容自动增长，提供更舒适的输入体验。

```vue
<template>
  <view>
    <wd-textarea
      v-model="article"
      placeholder="请输入文章内容，高度将自动适应"
      auto-height
      clearable
    />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const article = ref<string>('')
</script>
```

### 示例四：Cell 组合用法

与 `wd-cell-group` 配合使用，适用于表单页面布局。

```vue
<template>
  <view>
    <wd-cell-group border>
      <!-- 带前置图标的文本域 -->
      <wd-textarea
        v-model="form.location"
        label="位置信息"
        placeholder="请输入详细位置"
        auto-height
        clearable
        prefix-icon="location"
      />

      <!-- 必填的文本域 -->
      <wd-textarea
        v-model="form.remark"
        label="备注"
        placeholder="请输入备注信息"
        clearable
        required
      />

      <!-- 带字数限制的必填文本域 -->
      <wd-textarea
        v-model="form.feedback"
        label="反馈意见"
        placeholder="请输入您的反馈"
        :maxlength="500"
        clearable
        show-word-limit
        required
      />

      <!-- 只读状态 -->
      <wd-textarea
        v-model="form.readonlyText"
        label="只读内容"
        placeholder="只读文本域"
        readonly
        clearable
      />

      <!-- 禁用状态 -->
      <wd-textarea
        v-model="form.disabledText"
        label="禁用内容"
        placeholder="禁用文本域"
        disabled
        clearable
      />
    </wd-cell-group>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const form = ref({
  location: '',
  remark: '',
  feedback: '',
  readonlyText: '这是一段只读文本',
  disabledText: '这是一段禁用文本'
})
</script>
```

### 示例五：大尺寸和高级配置

适用于需要更大输入区域和键盘配置的场景。

```vue
<template>
  <view>
    <wd-cell-group border>
      <!-- 大尺寸 + 高度自适应 -->
      <wd-textarea
        v-model="largeContent"
        label="大尺寸文本域"
        placeholder="请输入内容"
        size="large"
        auto-height
        clearable
        required
      />

      <!-- 大尺寸 + 字数限制 -->
      <wd-textarea
        v-model="largeLimit"
        label="字数限制"
        placeholder="最多240个字符"
        size="large"
        :maxlength="240"
        clearable
        show-word-limit
        required
      />
    </wd-cell-group>

    <!-- 固定区域使用 -->
    <wd-textarea
      v-model="fixedContent"
      placeholder="在 fixed 区域使用"
      :fixed="true"
    />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const largeContent = ref<string>('')
const largeLimit = ref<string>('')
const fixedContent = ref<string>('')
</script>
```

---

## 注意事项

1. **高度自适应限制**：当设置 `auto-height` 为 `true` 时，通过 `style.height` 设置的高度将不生效，文本域会根据内容自动调整高度。

2. **字数统计准确性**：组件使用 `Array.from` 处理多码元字符（如 emoji 表情），以获取正确的文本长度。当字符数超过 `maxlength` 时，字数统计会以错误样式（红色）显示。

3. **清空按钮触发时机**：`clearTrigger` 属性默认为 `always`，即输入框有值时始终显示清空按钮。设置为 `focus` 时，只有在输入框聚焦且有值时才会显示清空按钮。

4. **清空后聚焦行为**：默认情况下，点击清空按钮后会自动重新聚焦输入框。如果不需要此行为，可设置 `focus-when-clear` 为 `false`。

5. **只读与禁用区别**：
   - `disabled` 状态下文本域完全不可交互，不显示清空按钮和字数统计
   - `readonly` 状态下单仅不可编辑，但仍可选择和复制内容

6. **固定定位支持**：如果文本域处于 `position: fixed` 区域，需要设置 `fixed` 属性为 `true`，以确保键盘弹出时表现正常。

7. **表单校验**：使用 `prop` 和 `rules` 属性进行表单校验时，需要将组件放在 `wd-form` 和 `wd-form-item` 中。错误信息会显示在文本域底部。

8. **多码元字符处理**：组件内部对 `maxlength` 截断使用 `substring` 方法，字数统计使用 `Array.from` 计算长度，两者在处理多码元字符时可能有细微差异。

9. **支付宝小程序兼容**：在支付宝小程序中，建议设置 `enableNative` 为 `false`，以避免键盘弹出后内容上移的问题。

10. **合成事件处理**：`ignoreCompositionEvent` 默认为 `true`，即忽略 composition 事件。如果需要在中文输入法输入过程中实时获取输入内容，可设置为 `false`。
