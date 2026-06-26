# Code 验证码


## 组件概况

验证码模块由 `Code` 组件组成，负责验证码发送的倒计时逻辑控制，支持倒计时持久化（页面刷新/返回后继续倒计时）、可自定义的按钮文案、以及 `start()` 和 `reset()` 方法控制。

## 核心功能描述

- **倒计时逻辑**：内置完整的倒计时功能，通过 `seconds` 属性配置倒计时时长（默认 60 秒）
- **自定义文案**：支持 `start-text`、`change-text`（X 为剩余秒数占位符）、`end-text` 自定义各阶段按钮文字
- **倒计时持久化**：通过 `keep-running` 和 `unique-key` 实现页面刷新/返回后倒计时继续，利用 uni.setStorage 持久化时间戳
- **方法控制**：通过 `ref` 暴露 `start()` 开始倒计时、`reset()` 重置倒计时、`canGetCode` 状态标识
- **事件通知**：通过 `change` 事件实时返回当前提示文案，`start` 和 `end` 事件标记倒计时生命周期

## 适用业务场景

- **手机号验证码登录**：发送短信验证码，倒计时防止频繁发送
- **密码找回验证**：通过手机/邮箱验证码验证身份
- **支付验证**：二次验证场景，确认支付操作
- **安全验证**：需要防刷的验证场景，倒计时限制请求频率

## Code API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| seconds | `string \| number` | 60 | 否 | 倒计时时长，单位秒 |
| startText | string | '获取验证码' | 否 | 开始时按钮文字 |
| changeText | string | 'X秒重新获取' | 否 | 倒计时进行中按钮文字，X 为剩余秒数占位符 |
| endText | string | '重新获取' | 否 | 结束时按钮文字 |
| keepRunning | boolean | false | 否 | 是否保持倒计时不中断（如页面切换） |
| uniqueKey | string | '' | 否 | 唯一标识 key，用于区分多个验证码组件 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点类名 |

### Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| change | (text: string) | 文案变化时触发，返回当前提示文本（开始/倒计时中/结束） |
| start | - | 倒计时开始时触发 |
| end | - | 倒计时结束时触发 |

### Methods

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| start | - | void | 开始倒计时，内部会先防止重复调用 |
| reset | - | void | 重置倒计时，清除定时器并恢复初始状态 |

### 暴露属性

| 属性名称 | 类型 | 说明 |
|---------|------|------|
| canGetCode | Ref\<boolean\> | 是否可以执行验证码操作（倒计时期间为 false） |

## 使用示例

### 示例 1：基本用法 - 发送验证码

展示基础的验证码发送按钮和倒计时效果。

```vue
<template>
  <view>
    <wd-code
      ref="codeRef"
      @change="codeChange"
      seconds="20"
      change-text="XS获取"
      @start="disabled = true"
      @end="disabled = false"
    />
    <wd-button @click="getCode" type="success" :disabled="disabled">
      {{ tips }}
    </wd-button>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  interface CodeInstance {
    canGetCode: boolean
    start: () => void
  }

  const tips = ref<string>('')
  const disabled = ref<boolean>(false)
  const codeRef = ref<CodeInstance | null>(null)

  const codeChange = (text: string): void => {
    tips.value = text
  }

  const getCode = (): void => {
    if (codeRef.value?.canGetCode) {
      // 模拟向后端请求验证码
      uni.showLoading({
        title: '正在获取验证码'
      })
      setTimeout(() => {
        uni.hideLoading()
        uni.showToast({
          title: '验证码已发送'
        })
        // 通知 Code 组件内部开始倒计时
        codeRef.value?.start()
      }, 2000)
    } else {
      uni.showToast({
        title: '倒计时结束后再发送'
      })
    }
  }
</script>
```

通过 `ref` 获取 Code 组件实例，调用 `start()` 方法开始倒计时。`change` 事件实时返回当前提示文案（如 "19秒重新获取"、"重新获取"）。`canGetCode` 属性用于判断是否可以发送验证码，防止倒计时期间重复请求。`seconds` 设置为 20 秒，`change-text` 中的 `X` 会被替换为剩余秒数。

### 示例 2：保持倒计时（页面刷新/返回后继续）

页面刷新或返回后，倒计时继续而不中断。

```vue
<template>
  <view>
    <wd-code
      ref="codeRef1"
      @change="codeChange1"
      keep-running
      change-text="倒计时XS"
      @start="disabled = true"
      @end="disabled = false"
    />
    <wd-button type="primary" @click="getCode1" :disabled="disabled">
      {{ tips1 }}
    </wd-button>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  interface CodeInstance {
    canGetCode: boolean
    start: () => void
  }

  const tips1 = ref<string>('')
  const disabled = ref<boolean>(false)
  const codeRef1 = ref<CodeInstance | null>(null)

  const codeChange1 = (text: string): void => {
    tips1.value = text
  }

  const getCode1 = (): void => {
    if (codeRef1.value?.canGetCode) {
      uni.showLoading({ title: '正在获取验证码' })
      setTimeout(() => {
        uni.hideLoading()
        uni.showToast({ title: '验证码已发送' })
        codeRef1.value?.start()
      }, 2000)
    } else {
      uni.showToast({ title: '倒计时结束后再发送' })
    }
  }
</script>
```

`keep-running` 属性开启倒计时持久化。内部通过 `uni.setStorage` 保存时间戳，页面刷新或返回后组件 `onMounted` 时会检查是否需要继续上一次的倒计时。同一页面有多个 Code 组件时，需通过 `unique-key` 区分。

### 示例 3：自定义按钮文案样式

自定义验证码按钮的文字内容和样式。

```vue
<template>
  <view>
    <wd-code
      ref="codeRef2"
      @change="codeChange2"
      keep-running
      start-text="点我获取验证码"
    />
    <text @click="getCode2" :class="'u-page__code-text'">
      {{ tips2 }}
    </text>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  interface CodeInstance {
    canGetCode: boolean
    start: () => void
  }

  const tips2 = ref<string>('')
  const codeRef2 = ref<CodeInstance | null>(null)

  const codeChange2 = (text: string): void => {
    tips2.value = text
  }

  const getCode2 = (): void => {
    if (codeRef2.value?.canGetCode) {
      uni.showLoading({ title: '正在获取验证码' })
      setTimeout(() => {
        uni.hideLoading()
        uni.showToast({ title: '验证码已发送' })
        codeRef2.value?.start()
      }, 2000)
    } else {
      uni.showToast({ title: '倒计时结束后再发送' })
    }
  }
</script>
<style lang="scss" scoped>
  .u-page__code-text {
    color: #007aff;
    font-size: 15px;
  }
</style>
```

Code 组件本身不渲染任何可视内容，仅负责倒计时逻辑。按钮的实际样式由外部元素（如 `wd-button`、`text`）控制。通过 `change` 事件更新按钮文案，实现完整的倒计时按钮效果。

## 注意事项

1. **Code 组件不渲染任何可视内容**：Code 组件内部 template 为空（`<!-- 此组件功能由js完成，无需写html逻辑 -->`），实际的按钮/文字由外部元素控制，通过 `change` 事件传递当前阶段的提示文案
2. **changeText 中的 X 占位符**：`change-text` 中的 `X` 或 `x`（大小写均可）会被替换为剩余秒数，如设置为 `"XS获取"` 时显示 "59S获取"、"58S获取" 等
3. **start() 方法需手动调用**：获取验证码的请求成功后，必须手动调用 `codeRef.value?.start()` 才会开始倒计时，组件不会自动开始
4. **canGetCode 防重复点击**：通过 `ref.value?.canGetCode` 判断是否可以发送验证码，倒计时期间为 `false`，防止用户频繁请求
5. **keepRunning 依赖 uniqueKey**：开启 `keep-running` 后，如果页面有多个 Code 组件，务必设置 `unique-key` 区分，否则时间戳会互相覆盖
