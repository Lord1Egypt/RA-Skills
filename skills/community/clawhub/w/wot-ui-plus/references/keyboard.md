# Keyboard 虚拟键盘


## 组件概况

Keyboard 虚拟键盘组件是一个底部弹出的数字键盘控件，支持多种键盘模式（默认数字键盘、带自定义侧栏的键盘、车牌号键盘），并提供随机按键顺序、额外按键（如小数点、X）、双向绑定、点击外部收起、蒙层遮罩等丰富功能。适用于需要安全输入或自定义输入法的场景，如支付密码、车牌号录入、金额输入等。

## 核心功能描述

- **三种键盘模式**：支持 `default`（默认数字键盘）、`custom`（带右侧删除/确认栏的键盘）、`car`（车牌号键盘，支持中/英文切换）
- **额外按键**：通过 `extra-key` 属性支持单个或多个额外按键，如小数点 `.`、身份证号后缀 `X`、`00` 等
- **随机按键顺序**：通过 `random-key-order` 属性将 1-9 数字按键随机排列，适用于安全输入场景
- **双向绑定**：支持 `v-model` 绑定输入值，同时支持 `v-model:visible` 控制键盘显隐
- **标题与自定义**：支持 `title` 属性展示标题，支持 `#title` 插槽自定义标题内容
- **确认/关闭按钮**：支持 `close-text` 设置确认按钮文本，支持 `close-button-loading` 展示加载状态
- **车牌键盘**：`mode="car"` 时提供省份简称键盘（中文模式）和数字/字母键盘（英文模式），支持 `auto-switch-lang` 自动切换
- **外部交互控制**：支持 `modal` 展示半透明蒙层，支持 `hide-on-click-outside` 控制点击外部是否收起
- **安全区域适配**：支持 `safe-area-inset-bottom` 适配 iPhone 等设备的底部安全区域

## 适用业务场景

- **支付密码输入**：搭配 PasswordInput 组件使用，`mode="default"` 或 `mode="custom"` 提供安全数字输入
- **金额输入**：`mode="custom"` + `extra-key="."` 提供带小数点的数字键盘
- **身份证号输入**：`extra-key="X"` 提供身份证号后缀 X 按键
- **车牌号录入**：`mode="car"` 提供省份简称 + 字母数字的车牌专用键盘
- **安全验证码输入**：`random-key-order` 打乱数字键顺序，防止截屏泄露
- **底部弹窗式输入**：从底部弹出，不遮挡输入区域，适配移动端操作习惯

## API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| visible | boolean | false | 否 | 是否可见，支持 v-model:visible 双向绑定 |
| modelValue | string | '' | 否 | 绑定的值，支持 v-model 双向绑定 |
| mode | `'default' \| 'custom' \| 'car'` | `'default'` | 否 | 键盘模式 |
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
| carLang | `'zh' \| 'en'` | - | 否 | 车牌键盘语言模式，`mode="car"` 时生效 |
| autoSwitchLang | boolean | false | 否 | 是否自动切换车牌键盘语言，`mode="car"` 且 carLang 非受控时生效 |
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

    <!-- 带右侧栏的自定义键盘（含删除和确认按钮） -->
    <wd-cell title="带右侧栏的键盘" is-link @click="visible2 = true" />

    <!-- 键盘组件 -->
    <wd-keyboard v-model:visible="visible1" @input="onInput" @delete="onDelete" />

    <wd-keyboard
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

`mode="default"` 时为默认模式，底部展示 0、extraKey、删除键三键；`mode="custom"` 时在右侧额外展示删除和确认按钮栏。

### 示例 2：带标题和额外按键

展示带标题的键盘、自定义额外按键（如身份证号的 X）以及多个额外按键的场景。

```vue
<template>
  <view>
    <!-- 带标题的键盘 -->
    <wd-cell title="带标题的键盘" is-link @click="visible1 = true" />

    <!-- 身份证键盘（额外按键为 X） -->
    <wd-cell title="身份证键盘" is-link @click="visible2 = true" />

    <!-- 多个额外按键（00 和 .） -->
    <wd-cell title="多个额外按键" is-link @click="visible3 = true" />

    <!-- 带标题、额外按键为小数点的键盘 -->
    <wd-keyboard
      v-model:visible="visible1"
      title="输入密码"
      extra-key="."
      close-text="完成"
      @input="onInput"
      @delete="onDelete"
    />

    <!-- 身份证键盘，额外按键为 X -->
    <wd-keyboard
      v-model:visible="visible2"
      extra-key="X"
      close-text="完成"
      @input="onInput"
      @delete="onDelete"
    />

    <!-- 多个额外按键，mode="custom" 时支持数组 -->
    <wd-keyboard
      v-model:visible="visible3"
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

  const visible1 = ref<boolean>(false)
  const visible2 = ref<boolean>(false)
  const visible3 = ref<boolean>(false)

  const onInput = (value: string) => showToast(`${value}`)
  const onDelete = () => showToast('删除')
</script>
```

当 `extraKey` 为字符串时，默认模式下替换删除键上方的按键文本。在 `mode="custom"` 模式下，如果 `extraKey` 为数组：长度为 1 时，0 键变宽并搭配一个额外键；长度为 2 时，底部显示两个额外键夹着 0 键。

### 示例 3：随机数字键盘

打乱 1-9 数字键的排列顺序，适用于安全输入场景。

```vue
<template>
  <view>
    <wd-cell title="随机数字键盘" is-link @click="visible = true" />

    <wd-keyboard
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

设置 `random-key-order` 后，每次打开键盘时 1-9 数字键的顺序会随机打乱，降低截屏泄露密码的风险。

### 示例 4：双向绑定与长度限制

通过 `v-model` 绑定输入值，并使用 `maxlength` 限制最大输入长度。

```vue
<template>
  <view>
    <wd-cell title="双向绑定" clickable :value="value" @click="visible = true" />

    <wd-keyboard
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

`v-model` 绑定键盘输入值，每次按键自动追加字符，删除键自动移除末尾字符。`maxlength` 限制最大输入长度，达到限制后继续按键不会追加内容。Cell 组件通过 `:value` 显示当前输入值，提供直观的输入反馈。

### 示例 5：展示蒙层

添加半透明遮罩蒙层，增强视觉聚焦效果。

```vue
<template>
  <view>
    <wd-cell title="展示蒙层" is-link @click="visible = true" />

    <wd-keyboard
      :modal="true"
      v-model:visible="visible"
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

`modal` 属性控制是否显示半透明蒙层。蒙层默认不可见，设置 `:modal="true"` 后键盘弹出时背景会叠加一层遮罩，增强用户聚焦感。`hide-on-click-outside` 默认为 `true`，点击蒙层区域会关闭键盘并触发 `close` 事件。

### 示例 6：自定义标题插槽

使用 `#title` 插槽自定义标题样式和内容。

```vue
<template>
  <view>
    <wd-cell title="slot自定义标题" is-link @click="visible = true" />

    <wd-keyboard
      v-model:visible="visible"
      extra-key="."
      close-text="完成"
      @input="onInput"
      @delete="onDelete"
    >
      <template #title>
        <text style="color: #fa4350">自定义标题</text>
      </template>
    </wd-keyboard>
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

通过 `#title` 插槽可以完全自定义标题的内容和样式，如设置文字颜色、添加图标等。当设置了 `title` 属性或提供了 `#title` 插槽内容时，键盘头部区域会自动显示。

### 示例 7：车牌号键盘（非受控模式）

使用 `mode="car"` 提供车牌号专用键盘，支持省份简称和字母数字输入。

```vue
<template>
  <view>
    <wd-cell title="车牌号键盘(非受控)" :value="value" is-link @click="visible = true" />

    <wd-keyboard
      v-model="value"
      v-model:visible="visible"
      mode="car"
      auto-switch-lang
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

`mode="car"` 时进入车牌号键盘模式，默认为中文模式展示省份简称（京、沪、粤 等 36 个字符）。输入第一位后，`auto-switch-lang` 会自动将键盘切换为英文模式（数字 0-9 和字母 A-Z，不含 I 和 O）。当输入内容全部删除后，会自动恢复为中文省份模式。

### 示例 8：车牌号键盘（受控模式）

通过 `v-model:car-lang` 手动控制车牌键盘的语言模式。

```vue
<template>
  <view>
    <wd-cell title="车牌号键盘(受控)" :value="value" is-link @click="visible = true" />

    <wd-keyboard
      v-model="value"
      v-model:visible="visible"
      v-model:car-lang="carLang"
      mode="car"
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
  const carLang = ref<'zh' | 'en'>('zh')

  const onInput = (text: string) => showToast(`输入了 ${text}`)
  const onDelete = () => showToast('删除')
</script>
```

通过 `v-model:car-lang` 受控绑定车牌键盘语言，初始为 `'zh'` 中文模式（省份简称）。用户点击 "省份/ABC" 切换按钮时，会触发 `update:carLang` 事件更新绑定值。中文模式包含 36 个省份简称，英文模式包含 10 个数字和 24 个字母（不含 I 和 O）。

## 注意事项

1. **extraKey 在不同模式下的行为差异**：在 `default` 模式下，`extraKey` 替换底部第三列的按键文本（默认删除键位置上方）；在 `custom` 模式下，`extraKey` 为字符串时与 0 键一起组成底部行，为数组时根据长度（1 或 2）排列不同布局
2. **randomKeyOrder 仅打乱 1-9**：`random-key-order` 仅对 1-9 数字按键生效，0 键、extraKey 键、删除键的顺序不会改变
3. **maxlength 限制输入上限**：达到 `maxlength` 限制后继续按数字键不会触发 `input` 事件和追加字符，但删除键仍然正常工作
4. **closeText 决定确认按钮显隐**：在 `default` 和 `car` 模式下，设置 `close-text` 后顶部右侧才会显示关闭按钮；在 `custom` 模式下，关闭按钮始终显示在右侧栏
5. **车牌键盘自动切换语言**：`auto-switch-lang` 在非受控模式下生效，输入省份简称后自动切换到字母/数字模式，全部删除后自动恢复为省份简称模式
6. **closeButtonLoading 状态**：`close-button-loading` 仅影响右侧栏的确认按钮（`custom` 模式），按钮显示 loading 动画，用于异步提交场景
7. **deleteText 和 closeText 默认值**：这两个属性没有默认值，不设置时删除键默认显示删除图标（delete-box icon），extra 键默认显示键盘图标
8. **rootPortal 解决 fixed 定位问题**：当键盘嵌套在复杂布局中可能出现 fixed 定位失效时，设置 `root-portal` 将键盘从页面中脱离出来，在不同平台实现方式不同（H5: teleport, APP: renderjs, 小程序: root-portal）
9. **hideOnClickOutside 与 modal 的关系**：`hide-on-click-outside` 控制 Popup 的 `modal` 属性，决定是否响应外部点击关闭；`modal` 属性控制蒙层的视觉显示（有遮罩 vs 无遮罩透明），两者互相独立
