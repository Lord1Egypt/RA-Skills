# NumberKeyboard 数字键盘


## 组件概况

NumberKeyboard 数字键盘组件是一个底部弹出的纯数字键盘控件，提供默认和自定义两种布局模式。与 Keyboard 组件相比，NumberKeyboard 专注于纯数字输入场景，不包含车牌号模式。支持随机按键顺序、额外按键（如小数点、00）、双向绑定、标题栏、确认按钮加载状态等功能，适用于密码输入、金额输入、验证码输入等需要安全数字键盘的场景。

## 核心功能描述

- **两种键盘模式**：支持 `default`（默认数字键盘）和 `custom`（带右侧删除/确认栏的键盘）
- **额外按键**：通过 `extra-key` 属性支持单个或多个额外按键，如小数点 `.`、`00` 等
- **随机按键顺序**：通过 `random-key-order` 属性将 1-9 数字按键随机排列，适用于安全输入场景
- **双向绑定**：支持 `v-model` 绑定输入值，同时支持 `v-model:visible` 控制键盘显隐
- **标题与自定义**：支持 `title` 属性展示标题，支持 `#title` 插槽自定义标题内容
- **确认按钮加载状态**：支持 `close-button-loading` 在确认按钮上展示加载动画
- **外部交互控制**：支持 `modal` 展示半透明蒙层，支持 `hide-on-click-outside` 控制点击外部是否收起
- **安全区域适配**：支持 `safe-area-inset-bottom` 适配 iPhone 等设备的底部安全区域

## 适用业务场景

- **支付密码输入**：搭配 PasswordInput 组件使用，提供安全数字输入键盘
- **金额输入**：`mode="custom"` + `extra-key="."` 提供带小数点的数字键盘
- **验证码输入**：搭配验证码输入框使用，提供快捷数字输入方式
- **安全输入**：`random-key-order` 打乱数字键顺序，防止截屏泄露
- **底部弹窗式输入**：从底部弹出，不遮挡输入区域，适配移动端操作习惯
- **金额快速输入**：`extra-key="00"` 提供快捷双零输入，适用于收银、支付等场景

## API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| visible | boolean | false | 否 | 是否可见，支持 v-model:visible 双向绑定 |
| modelValue | string | '' | 否 | 绑定的值，支持 v-model 双向绑定 |
| mode | `'default' \| 'custom'` | `'default'` | 否 | 键盘模式 |
| title | string | - | 否 | 键盘标题 |
| maxlength | number | Infinity | 否 | 最大输入长度 |
| zIndex | number | 100 | 否 | 层级 |
| showDeleteKey | boolean | true | 否 | 是否显示删除键（default 模式下底部删除键） |
| randomKeyOrder | boolean | false | 否 | 是否随机 1-9 数字按键顺序 |
| closeText | string | - | 否 | 确认/关闭按钮文本 |
| deleteText | string | - | 否 | 删除按钮文本 |
| closeButtonLoading | boolean | false | 否 | 关闭按钮是否显示加载状态 |
| modal | boolean | false | 否 | 是否显示半透明蒙层 |
| hideOnClickOutside | boolean | true | 否 | 是否在点击外部时收起键盘 |
| lockScroll | boolean | true | 否 | 是否锁定页面滚动 |
| safeAreaInsetBottom | boolean | true | 否 | 是否在底部安全区域内 |
| extraKey | `string \| Array<string>` | - | 否 | 额外按键，支持单个字符或字符数组 |
| rootPortal | boolean | false | 否 | 是否从页面中脱离出来，用于解决 fixed 失效问题 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点类名 |

### Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| input | (text: string) | 按下按键时触发，返回按下的字符文本 |
| delete | - | 按下删除键时触发 |
| close | - | 关闭键盘时触发（点击关闭按钮或点击蒙层） |

### Methods

组件不对外暴露任何方法。

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| title | - | 自定义键盘标题内容 |

## 使用示例

### 示例 1：基本用法

展示默认数字键盘和带右侧栏的自定义键盘。

```vue
<template>
  <view>
    <!-- 默认数字键盘 -->
    <wd-cell title="默认键盘" is-link @click="visible1 = true" />

    <!-- 带右侧栏的自定义键盘 -->
    <wd-cell title="带右侧栏的键盘" is-link @click="visible2 = true" />

    <wd-number-keyboard
      v-model:visible="visible1"
      @input="onInput"
      @delete="onDelete"
    />

    <wd-number-keyboard
      v-model:visible="visible2"
      mode="custom"
      extra-key="."
      close-text="完成"
      @input="onInput"
      @delete="onDelete"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import { useToast } from '@/uni_modules/wot-ui-plus'

  const { show: showToast } = useToast()

  const visible1 = ref<boolean>(false)
  const visible2 = ref<boolean>(false)

  const onInput = (value: string) => showToast(`${value}`)
  const onDelete = () => showToast('删除')
</script>
```

`mode="default"` 时为默认模式，底部第三行为 extraKey、0、删除键；`mode="custom"` 时右侧栏固定显示删除和确认按钮。

### 示例 2：带标题和额外按键

展示带标题的键盘、额外按键（如小数点）以及身份证号的 X 按键。

```vue
<template>
  <view>
    <!-- 身份证键盘（额外按键为 X） -->
    <wd-cell title="身份证键盘" is-link @click="visible1 = true" />

    <!-- 带标题的键盘 -->
    <wd-cell title="带标题的键盘" is-link @click="visible2 = true" />

    <!-- 额外按键为 X 的键盘 -->
    <wd-number-keyboard
      v-model:visible="visible1"
      extra-key="X"
      close-text="完成"
      @input="onInput"
      @delete="onDelete"
    />

    <!-- 带标题、额外按键为小数点的键盘 -->
    <wd-number-keyboard
      v-model:visible="visible2"
      title="输入密码"
      extra-key="."
      close-text="完成"
      @input="onInput"
      @delete="onDelete"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import { useToast } from '@/uni_modules/wot-ui-plus'

  const { show: showToast } = useToast()

  const visible1 = ref<boolean>(false)
  const visible2 = ref<boolean>(false)

  const onInput = (value: string) => showToast(`${value}`)
  const onDelete = () => showToast('删除')
</script>
```

当 `extraKey` 为字符串时，在默认模式下替换底部第三列的按键文本。在自定义模式下，`extraKey` 与 0 键组合排列在底部区域。

### 示例 3：多个额外按键

在 `mode="custom"` 下使用数组形式的 `extra-key`，实现多个额外按键。

```vue
<template>
  <view>
    <wd-cell title="多个额外按键" is-link @click="visible = true" />

    <wd-number-keyboard
      v-model:visible="visible"
      mode="custom"
      :extra-key="['00', '.']"
      close-text="完成"
      @input="onInput"
      @delete="onDelete"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import { useToast } from '@/uni_modules/wot-ui-plus'

  const { show: showToast } = useToast()

  const visible = ref<boolean>(false)

  const onInput = (value: string) => showToast(`${value}`)
  const onDelete = () => showToast('删除')
</script>
```

当 `extraKey` 为数组时：长度为 1 时，0 键加宽并搭配一个额外键；长度为 2 时，底部排列两个额外键夹着 0 键（如 `['00', '.']` 适用于收银场景的快速输入）。

### 示例 4：随机数字键盘

打乱 1-9 数字键的排列顺序，适用于安全输入场景。

```vue
<template>
  <view>
    <wd-cell title="随机数字键盘" is-link @click="visible = true" />

    <wd-number-keyboard
      v-model:visible="visible"
      random-key-order
      @input="onInput"
      @delete="onDelete"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import { useToast } from '@/uni_modules/wot-ui-plus'

  const { show: showToast } = useToast()

  const visible = ref<boolean>(false)

  const onInput = (value: string) => showToast(`${value}`)
  const onDelete = () => showToast('删除')
</script>
```

设置 `random-key-order` 后，每次打开键盘时 1-9 数字键的顺序会随机打乱，降低截屏泄露密码的风险。0 键和额外按键的顺序不会改变。

### 示例 5：双向绑定与长度限制

通过 `v-model` 绑定输入值，并使用 `maxlength` 限制最大输入长度。

```vue
<template>
  <view>
    <wd-cell title="双向绑定" clickable :value="value" @click="visible = true" />

    <wd-number-keyboard
      v-model="value"
      v-model:visible="visible"
      :maxlength="6"
      title="键盘标题"
      extra-key="."
      close-text="完成"
      @input="onInput"
      @delete="onDelete"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import { useToast } from '@/uni_modules/wot-ui-plus'

  const { show: showToast } = useToast()

  const visible = ref<boolean>(false)
  const value = ref<string>('')

  const onInput = (text: string) => showToast(`输入了 ${text}`)
  const onDelete = () => showToast('删除')
</script>
```

`v-model` 绑定键盘输入值，每次按键自动追加字符，删除键自动移除末尾字符。`maxlength` 限制最大输入长度，达到限制后继续按键不会追加内容。Cell 组件通过 `:value` 显示当前输入值。

### 示例 6：展示蒙层与自定义标题

添加半透明遮罩蒙层，使用插槽自定义标题内容。

```vue
<template>
  <view>
    <!-- 展示蒙层 -->
    <wd-cell title="展示蒙层" is-link @click="visible1 = true" />

    <!-- slot自定义标题 -->
    <wd-cell title="slot自定义标题" is-link @click="visible2 = true" />

    <wd-number-keyboard
      :modal="true"
      v-model:visible="visible1"
      @input="onInput"
      @delete="onDelete"
    />

    <wd-number-keyboard
      v-model:visible="visible2"
      extra-key="."
      close-text="完成"
      @input="onInput"
      @delete="onDelete"
    >
      <template #title>
        <text style="color: #fa4350">自定义标题</text>
      </template>
    </wd-number-keyboard>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import { useToast } from '@/uni_modules/wot-ui-plus'

  const { show: showToast } = useToast()

  const visible1 = ref<boolean>(false)
  const visible2 = ref<boolean>(false)

  const onInput = (value: string) => showToast(`${value}`)
  const onDelete = () => showToast('删除')
</script>
```

`:modal="true"` 控制显示半透明蒙层，点击蒙层区域关闭键盘。通过 `#title` 插槽可以完全自定义标题的内容和样式。

### 示例 7：搭配 PasswordInput 使用

与 PasswordInput 密码输入框组合使用，实现完整的密码输入交互。

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
      close-text="完成"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const visible = ref<boolean>(false)
  const value = ref<string>('')
</script>
```

PasswordInput 负责展示密码输入框的外观（掩码、光标、格子），NumberKeyboard 负责数字输入。通过 `focused` 属性联动键盘显隐，`v-model` 实现双向数据绑定。

### 示例 8：确认按钮加载状态

在提交密码时，为确认按钮添加加载状态防止重复提交。

```vue
<template>
  <view>
    <wd-cell title="提交确认" is-link @click="visible = true" />

    <wd-number-keyboard
      v-model:visible="visible"
      v-model="value"
      mode="custom"
      extra-key="."
      close-text="提交"
      :close-button-loading="loading"
      @close="onClose"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const visible = ref<boolean>(false)
  const value = ref<string>('')
  const loading = ref<boolean>(false)

  function onClose() {
    // 提交逻辑
    loading.value = true
    setTimeout(() => {
      loading.value = false
      visible.value = false
    }, 1500)
  }
</script>
```

在 `mode="custom"` 模式下，右侧栏的确认按钮支持 `close-button-loading` 属性。提交期间设置 `loading=true` 显示加载动画，防止用户重复点击。

## 注意事项

1. **与 Keyboard 的区别**：NumberKeyboard 是 Keyboard 的精简版本，不包含 `mode="car"` 车牌模式、`carLang`、`autoSwitchLang` 等车牌相关属性，专注于纯数字输入场景
2. **extraKey 在不同模式下的行为差异**：在 `default` 模式下，`extraKey` 替换底部第三列的按键文本；在 `custom` 模式下，`extraKey` 为字符串时与 0 键一起组成底部行，为数组时根据长度（1 或 2）排列不同布局
3. **randomKeyOrder 仅打乱 1-9**：`random-key-order` 仅对 1-9 数字按键生效，0 键、extraKey 键、删除键的顺序不会改变
4. **maxlength 限制输入上限**：达到 `maxlength` 限制后继续按数字键不会触发 `input` 事件和追加字符，但删除键仍然正常工作
5. **closeText 决定确认按钮显隐**：在 `default` 模式下，设置 `close-text` 后顶部右侧才会显示关闭按钮；在 `custom` 模式下，关闭按钮始终显示在右侧栏
6. **closeButtonLoading 状态**：`close-button-loading` 仅影响右侧栏的确认按钮（`custom` 模式），按钮显示 loading 动画，用于异步提交场景
7. **deleteText 默认值**：`deleteText` 没有默认值，不设置时删除键默认显示删除图标（delete-box icon）
8. **rootPortal 解决 fixed 定位问题**：当键盘嵌套在复杂布局中可能出现 fixed 定位失效时，设置 `root-portal` 将键盘从页面中脱离出来
9. **hideOnClickOutside 与 modal 的关系**：`hide-on-click-outside` 控制 Popup 的 `modal` 属性决定是否响应外部点击关闭；`modal` 属性控制蒙层的视觉显示，两者互相独立
