# MessageBox 消息提示框


## 组件概况

MessageBox 消息提示框组件是一个模态对话框组件，用于向用户展示重要信息并等待用户响应。该组件基于 `wd-popup` 弹出层实现，通过 zoom-in 缩放动画展示对话框，支持三种弹框类型：alert（仅确认按钮）、confirm（确认和取消按钮）、prompt（带输入框的确认框）。组件内部使用 `useMessage` 组合式 API 实现命令式调用，同时也支持通过组件标签方式在模板中声明使用。

组件内置了标题、消息内容、确认/取消按钮的完整布局，prompt 类型还内置了输入框及输入校验能力。支持通过 `selector` 属性区分多个 MessageBox 实例，通过 slot 可以插入自定义内容（如评分组件等）。

## 核心功能描述

- **三种弹框类型**：支持 `alert`（单确认按钮）、`confirm`（确认+取消按钮）、`prompt`（带输入框的确认框）三种模式
- **命令式调用**：采用 `useMessage` 组合式 API 进行调用，通过 `alert()`、`confirm()`、`prompt()` 方法快速弹出对应类型的对话框
- **输入框支持**：prompt 类型内置输入框，支持 `text`、`number` 等输入类型，支持 placeholder、初始值、正则校验、自定义校验函数
- **标题与内容**：支持设置标题和消息内容，消息内容过长时弹框高度不再增加，而是将内容区域设置为滚动展示
- **按钮自定义**：通过 `confirmButtonProps` 和 `cancelButtonProps` 属性可自定义确认/取消按钮的样式和行为
- **确认前钩子**：提供 `beforeConfirm` 钩子函数，在确认按钮点击后、对话框关闭前执行，支持异步操作（如显示 loading 等待异步完成后再关闭）
- **多实例支持**：通过 `selector` 参数创建独立的 MessageBox 实例，不同实例之间互不干扰
- **自定义内容插槽**：支持通过默认插槽在消息内容区域插入自定义内容（如评分组件、富文本等）
- **点击蒙层关闭**：支持配置 `closeOnClickModal` 控制是否允许点击蒙层关闭对话框
- **懒渲染优化**：默认开启懒渲染（lazyRender），弹层内容在触发展示时才渲染，提升性能
- **国际化支持**：内置多语言翻译支持，按钮文案跟随项目语言配置

## 适用业务场景

- **删除确认**：在执行删除、清空等不可逆操作前弹出确认对话框，避免用户误操作
- **信息提示**：操作成功、失败或需要提示用户注意时使用 alert 类型展示信息
- **数据输入**：需要用户快速输入少量信息时使用 prompt 类型，如输入邮箱、备注、数量等
- **评分评价**：通过插槽插入评分组件，让用户在对话框中进行评分操作
- **二次确认**：在执行重要业务操作（如提交订单、支付确认）时进行二次确认
- **异步操作反馈**：通过 beforeConfirm 钩子在确认按钮点击后展示 loading，异步操作完成后再关闭对话框

## API

### Props

以下为通过组件标签方式使用时的 Props。若使用 `useMessage` API 调用，可通过 `MessageOptions` 对象传入同名配置项。

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| selector | string | '' | 否 | 指定唯一标识，用于区分多个 MessageBox 实例 |
| rootPortal | boolean | false | 否 | 是否从页面中脱离出来，用于解决各种 fixed 失效问题（H5: teleport, APP: renderjs, 小程序: root-portal） |
| customStyle | string | '' | 否 | 自定义组件根元素样式 |
| customClass | string | '' | 否 | 自定义组件根元素类名 |

### useMessage API

`useMessage` 是 MessageBox 组件的核心调用方式，通过组合式 API 返回一个包含多个方法的对象。

```ts
import { useMessage } from '@/uni_modules/wot-ui-plus'

const message = useMessage()
```

也可传入 `selector` 参数创建指定实例：

```ts
const message = useMessage('wd-message-box-slot')
```

返回的 `message` 对象包含以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- |
| alert | `options: MessageOptions \| string` | `Promise<MessageResult>` | 打开 alert 弹框，仅包含确认按钮 |
| confirm | `options: MessageOptions \| string` | `Promise<MessageResult>` | 打开 confirm 弹框，包含确认和取消按钮 |
| prompt | `options: MessageOptions \| string` | `Promise<MessageResult>` | 打开 prompt 弹框，包含输入框和确认/取消按钮 |
| close | - | void | 关闭当前 MessageBox 弹框 |

### MessageOptions

通过 `useMessage` API 调用时，可传入的 `MessageOptions` 对象结构如下：

| 选项名称 | 数据类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| title | string | '' | 弹框标题 |
| msg | string | '' | 消息内容 |
| type | 'alert' \| 'confirm' \| 'prompt' | 'alert' | 弹框类型 |
| showCancelButton | boolean | false（alert/prompt）、true（confirm） | 是否展示取消按钮 |
| closeOnClickModal | boolean | true | 是否支持点击蒙层关闭，点击蒙层回调传入的 action 为 'modal' |
| confirmButtonText | string | '确认'（跟随国际化） | 确定按钮文案 |
| cancelButtonText | string | '取消'（跟随国际化） | 取消按钮文案 |
| inputType | InputType | 'text' | 当 type 为 prompt 时，输入框类型 |
| inputSize | InputSize | - | 当 type 为 prompt 时，输入框大小，可选值：large |
| inputValue | string \| number | '' | 当 type 为 prompt 时，输入框初始值 |
| inputPlaceholder | string | '' | 当 type 为 prompt 时，输入框 placeholder |
| inputPattern | RegExp | - | 当 type 为 prompt 时，输入框正则校验，点击确定按钮时进行校验 |
| inputValidate | `(value: string \| number) => boolean` | - | 当 type 为 prompt 时，输入框校验函数，点击确定按钮时进行校验 |
| inputError | string | '' | 当 type 为 prompt 时，输入框检验不通过时的错误提示文案 |
| beforeConfirm | `(options: { resolve: (isPass: boolean) => void }) => void` | - | 确认前钩子，点击确认按钮后、关闭弹框前执行 |
| cancelButtonProps | Partial\<ButtonProps\> | - | 取消按钮属性，可自定义按钮样式 |
| confirmButtonProps | Partial\<ButtonProps\> | - | 确认按钮属性，可自定义按钮样式 |
| zIndex | number | 99 | 弹窗层级 |
| lazyRender | boolean | true | 弹层内容懒渲染，触发展示时才渲染内容 |
| success | `(res: MessageResult) => void` | - | 确认回调函数 |
| fail | `(res: MessageResult) => void` | - | 取消/关闭回调函数 |

### MessageResult

弹框确认或取消时返回的结果对象：

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| action | 'confirm' \| 'cancel' \| 'modal' | 操作类型：confirm 为确认、cancel 为取消、modal 为点击蒙层关闭 |
| value | string \| number | 当 type 为 prompt 时，返回输入框的值 |

### Events

以下为通过组件标签方式使用时的事件。`useMessage` API 方式通过 `MessageOptions` 中的 `success` 和 `fail` 回调实现。

当前组件通过 `useMessage` API 调用为主，不直接通过组件事件交互。

### Methods

当前组件未通过 `defineExpose` 暴露实例方法。所有操作均通过 `useMessage` API 完成。

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 自定义消息内容区域，替代默认的 msg 文案，可插入评分组件、富文本等自定义内容 |

## 使用示例

### 示例 1：基础 alert 提示

效果说明：最基础的 alert 弹框调用，仅展示消息内容和确认按钮，点击确认后弹框关闭。也支持传入纯字符串文案快速调用。

```vue
<template>
  <view>
    <wd-message-box></wd-message-box>
    <wd-button @click="showAlert">操作成功</wd-button>
    <wd-button @click="showAlertWithTitle">显示标题</wd-button>
  </view>
</template>

<script setup lang="ts">
import { useMessage } from '@/uni_modules/wot-ui-plus'

const message = useMessage()

// 纯文案提示
function showAlert() {
  message.alert('操作成功')
}

// 带标题的提示
function showAlertWithTitle() {
  message.alert({
    msg: '提示文案',
    title: '标题'
  })
}
</script>
```

### 示例 2：confirm 确认弹框

效果说明：展示 confirm 类型的弹框，包含确认和取消两个按钮。返回值是一个 Promise，可通过 `.then()` 处理确认操作，通过 `.catch()` 处理取消操作。

```vue
<template>
  <view>
    <wd-message-box></wd-message-box>
    <wd-button @click="showConfirm">删除确认</wd-button>
  </view>
</template>

<script setup lang="ts">
import { useMessage } from '@/uni_modules/wot-ui-plus'

const message = useMessage()

function showConfirm() {
  message
    .confirm({
      msg: '是否删除？',
      title: '提示'
    })
    .then(() => {
      // 用户点击确认
      console.log('用户确认删除')
    })
    .catch((error) => {
      // 用户点击取消
      console.log('用户取消删除', error)
    })
}
</script>
```

### 示例 3：prompt 输入框弹框

效果说明：展示 prompt 类型的弹框，内置输入框供用户输入。支持设置输入框初始值、placeholder 和正则表达式校验。输入校验不通过时无法确认，并显示错误提示。

```vue
<template>
  <view>
    <wd-message-box></wd-message-box>
    <wd-button @click="showPrompt">输入邮箱</wd-button>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useMessage } from '@/uni_modules/wot-ui-plus'

const message = useMessage()
const emailValue = ref<string>('')

function showPrompt() {
  message
    .prompt({
      title: '请输入邮箱',
      inputValue: emailValue.value,
      inputPattern: /.+@.+\..+/i
    })
    .then((resp) => {
      // 用户输入校验通过并确认
      console.log('输入值：', resp.value)
      emailValue.value = resp.value as string
    })
    .catch((error) => {
      // 用户取消或校验失败
      console.log(error)
    })
}
</script>
```

### 示例 4：beforeConfirm 钩子

效果说明：使用 `beforeConfirm` 钩子函数，在用户点击确认按钮后、弹框关闭前执行异步操作。示例中展示删除中的 loading 提示，3 秒后关闭 loading 并关闭弹框，最后展示成功提示。

```vue
<template>
  <view>
    <wd-message-box></wd-message-box>
    <wd-toast></wd-toast>
    <wd-button @click="showBeforeConfirm">异步确认</wd-button>
  </view>
</template>

<script setup lang="ts">
import { useMessage, useToast } from '@/uni_modules/wot-ui-plus'

const message = useMessage()
const toast = useToast()

function showBeforeConfirm() {
  message
    .confirm({
      msg: '是否删除？',
      title: '提示',
      beforeConfirm: ({ resolve }) => {
        toast.loading('删除中...')
        setTimeout(() => {
          toast.close()
          resolve(true)
          toast.success('删除成功')
        }, 3000)
      }
    })
    .then(() => {
      // 确认回调
    })
    .catch((error) => {
      console.log(error)
    })
}
</script>
```

### 示例 5：自定义按钮样式

效果说明：通过 `confirmButtonProps` 和 `cancelButtonProps` 属性自定义按钮的样式，包括按钮类型、圆角、阴影等。

```vue
<template>
  <view class="page-message-box">
    <wd-message-box></wd-message-box>
    <wd-button @click="showWithButtonProps">自定义按钮</wd-button>
  </view>
</template>

<script setup lang="ts">
import { useMessage } from '@/uni_modules/wot-ui-plus'

const message = useMessage()

function showWithButtonProps() {
  message
    .confirm({
      msg: '自定义按钮样式',
      title: '提示',
      cancelButtonProps: {
        round: false,
        type: 'error',
        customClass: 'custom-shadow'
      },
      confirmButtonProps: {
        round: false,
        type: 'success',
        customClass: 'custom-shadow'
      }
    })
    .then(() => {})
    .catch((error) => {
      console.log(error)
    })
}
</script>

<style scoped lang="scss">
.page-message-box {
  :deep() {
    .custom-shadow {
      box-shadow:
        0 3px 1px -2px rgb(0 0 0 / 20%),
        0 2px 2px 0 rgb(0 0 0 / 14%),
        0 1px 5px 0 rgb(0 0 0 / 12%);
    }
  }
}
</style>
```

### 示例 6：通过插槽插入自定义内容

效果说明：通过组件标签方式使用 MessageBox，在默认插槽中插入评分组件。需要为自定义 MessageBox 设置独立的 `selector`，通过 `useMessage(selector)` 创建对应实例。

```vue
<template>
  <view>
    <!-- 自定义 MessageBox，插入评分组件 -->
    <wd-message-box selector="wd-message-box-slot">
      <wd-rate v-model="rate" />
    </wd-message-box>
    <wd-message-box></wd-message-box>
    <wd-button @click="showRate">评分</wd-button>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useMessage } from '@/uni_modules/wot-ui-plus'

const rate = ref<number>(1)

const message = useMessage()
const message1 = useMessage('wd-message-box-slot')

function showRate() {
  message1
    .confirm({
      title: '评分'
    })
    .then(() => {
      message.alert(`你的评分为 ${rate.value} 分`)
    })
    .catch((error) => {
      console.log(error)
    })
}
</script>
```

## 注意事项

1. **组件标签必须声明**：使用 `useMessage` API 调用时，需要在模板中声明 `<wd-message-box>` 组件标签，否则弹框无法渲染。如果使用 `selector` 区分实例，需要声明对应 selector 的组件标签。

2. **字符串与对象参数**：`alert()`、`confirm()`、`prompt()` 方法均支持传入纯字符串或 `MessageOptions` 对象。传入字符串时自动设置为 `msg` 字段。

3. **Promise 返回值**：`confirm()` 和 `prompt()` 方法返回 Promise，确认时 resolve，取消或点击蒙层关闭时 reject。`alert()` 方法也返回 Promise，确认时 resolve。

4. **输入校验**：prompt 类型的输入框在点击确认按钮时进行校验。校验优先级：先校验 `inputPattern`（正则表达式），再校验 `inputValidate`（自定义函数）。校验不通过时显示错误提示，且弹框不会关闭。

5. **beforeConfirm 钩子**：`beforeConfirm` 钩子接收一个包含 `resolve` 方法的对象。调用 `resolve(true)` 继续确认并关闭弹框，调用 `resolve(false)` 则不关闭弹框。适用于需要异步确认的场景。

6. **多实例隔离**：通过 `useMessage(selector)` 传入不同的 `selector` 值可创建相互独立的 MessageBox 实例。每个实例拥有独立的状态和配置，互不影响。若不传入 `selector`，则使用全局默认实例。

7. **长文案处理**：当消息内容过长时，弹框高度不再增加，而是将内容区域设置为滚动展示。这确保了弹框不会超出屏幕范围。

8. **按钮属性合并**：`confirmButtonProps` 和 `cancelButtonProps` 会与默认按钮属性合并。确认按钮默认 `block: true`，取消按钮默认 `block: true` 且 `type: 'info'`。

9. **点击蒙层行为**：设置 `closeOnClickModal` 为 false 时，点击蒙层不会关闭弹框。点击蒙层关闭时，返回的 action 值为 `'modal'`。

10. **自定义样式**：推荐使用外部样式类（`wd-message-box__title`、`wd-message-box__content`、`wd-message-box__actions-btn` 等）进行精细化样式调整。
