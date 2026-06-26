# Signature 签名

## 组件概况

Signature 签名组件是一个基于 Canvas 绘制的电子签名板组件，支持普通笔迹和笔锋（压感）两种绘制模式。组件内置撤销、恢复、清空等操作功能，支持将签名结果导出为 PNG/JPG 图片。签名板可以通过 `v-model` 或组件实例方法进行控制，支持自定义画笔颜色、宽度、画板背景、画板尺寸等配置。该组件广泛应用于电子合同签署、快递签收、工单确认等需要手写签名的业务场景。

## 核心功能描述

- **Canvas 绘制签名**：基于 UniApp Canvas API 实现流畅的手写签名绘制
- **笔锋（压感）模式**：通过 `pressure` 属性开启笔锋效果，根据书写速度动态调整笔画粗细，快速书写产生细线条，慢速书写产生粗线条
- **贝塞尔曲线平滑绘制**：笔锋模式下使用二次贝塞尔曲线（quadraticCurveTo）实现平滑笔画
- **撤销与恢复**：开启 `enable-history` 后支持多步撤销和恢复操作，通过 `step` 属性控制步长
- **清空签名**：一键清空画板内容
- **导出图片**：将签名结果导出为指定格式（PNG/JPG）的临时文件，支持自定义导出质量（`quality`）和缩放比例（`export-scale`）
- **自定义画笔**：通过 `pen-color` 和 `line-width` 自定义画笔颜色和宽度
- **自定义画板**：支持设置画板的宽度（`width`）、高度（`height`）和背景色（`background-color`）
- **按钮自定义**：通过 `#footer` 插槽完全自定义底部操作按钮区域
- **禁用签名**：通过 `disabled` 属性禁止用户在画板上绘制
- **压感参数调节**：支持自定义笔锋模式下的最小宽度（`min-width`）、最大宽度（`max-width`）和最小速度阈值（`min-speed`）
- **平台兼容**：适配微信小程序（2D Canvas）和其他平台（非 2D Canvas）

## 适用业务场景

- **电子合同签署**：在电子签约场景中采集用户手写签名
- **快递签收**：物流配送场景中收件人签名确认
- **工单确认**：服务工单完成后客户签名确认
- **审批流程**：移动审批流程中主管手写签字
- **表单签署**：各类业务表单需要手写签名确认的场景
- **弹窗签名**：在弹窗中展示签名板，签名完成后自动关闭弹窗
- **横屏签名**：在横屏模式下进行签名，适配平板等大屏设备

## API

### Signature Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| penColor | string | '#000' | 否 | 签名笔颜色 |
| lineWidth | number | 3 | 否 | 签名笔宽度（非笔锋模式下生效） |
| clearText | string | '' | 否 | 清空按钮的文本，未设置时跟随国际化配置 |
| revokeText | string | '' | 否 | 撤回按钮的文本，未设置时跟随国际化配置 |
| restoreText | string | '' | 否 | 恢复按钮的文本，未设置时跟随国际化配置 |
| undoText | string | '' | 否 | 撤回按钮的文本，未设置时跟随国际化配置 |
| redoText | string | '' | 否 | 恢复按钮的文本，未设置时跟随国际化配置 |
| confirmText | string | '' | 否 | 确认按钮的文本，未设置时跟随国际化配置 |
| fileType | string | 'png' | 否 | 目标文件的类型，支持 png / jpg |
| quality | number | 1 | 否 | 目标文件的质量，取值范围 0~1 |
| exportScale | number | 1 | 否 | 导出图片的缩放比例，值越大图片越清晰 |
| disabled | boolean | false | 否 | 是否禁用签名板 |
| height | number / string | - | 否 | 画布的高度 |
| width | number / string | - | 否 | 画布的宽度 |
| backgroundColor | string | - | 否 | 画板的背景色 |
| disableScroll | boolean | true | 否 | 是否禁用画布滚动 |
| enableHistory | boolean | false | 否 | 是否开启历史记录（撤销/恢复） |
| step | number | 1 | 否 | 撤回和恢复的步长 |
| pressure | boolean | false | 否 | 是否启用压感模式（笔锋） |
| minWidth | number | 2 | 否 | 压感模式下笔画最小宽度 |
| maxWidth | number | 6 | 否 | 压感模式下笔画最大宽度 |
| minSpeed | number | 1.5 | 否 | 最小速度阈值，影响压感模式下的笔画宽度变化 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### Signature Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| start | 开始绘制签名时触发 | `(event: TouchEvent)` | 原生触摸事件对象 |
| end | 结束绘制签名时触发 | `(event: TouchEvent)` | 原生触摸事件对象 |
| signing | 签名绘制过程中持续触发 | `(event: TouchEvent)` | 原生触摸事件对象 |
| confirm | 确认签名后生成图片时触发 | `(result: SignatureResult)` | 包含图片临时路径、宽度、高度和成功状态 |
| clear | 清空签名时触发 | 无 | - |

### Signature Methods

通过 ref 可以获取 `wd-signature` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| init | `(forceUpdate?: boolean)` | void | 初始化签名板，`forceUpdate` 表示是否强制更新 |
| clear | 无 | void | 清除签名 |
| confirm | 无 | void | 确认签名并生成图片 |
| restore | 无 | void | 恢复上一步操作（重做） |
| revoke | 无 | void | 撤销上一步操作 |

### Signature Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| footer | `{ clear, confirm, currentStep, restore, revoke, canUndo, canRedo, historyList }` | 自定义底部操作按钮区域，包含清除、确认、撤销、恢复等操作 |

### SignatureResult 类型

```ts
interface SignatureResult {
  tempFilePath: string   // 生成图片的临时路径
  success: boolean       // 是否成功生成图片
  width: number          // 生成图片的宽度
  height: number         // 生成图片的高度
}
```

## 使用示例

### 示例一：基础签名

最常用的签名用法，包含基础的签名绘制、清空和确认功能。

```vue
<template>
  <wd-signature
    @confirm="confirm"
    @clear="clear"
    :export-scale="2"
    background-color="#ffffff"
  />
</template>

<script lang="ts" setup>
import type { SignatureResult } from '@/uni_modules/wot-ui-plus/components/wd-signature/types'

function confirm(result: SignatureResult) {
  if (result.success) {
    uni.previewImage({
      urls: [result.tempFilePath]
    })
  }
}

function clear() {
  console.log('签名已清空')
}
</script>
```

### 示例二：笔锋模式与历史记录

开启笔锋（压感）模式，实现类似真实手写笔的效果，并结合历史记录支持撤销和恢复操作。

```vue
<template>
  <!-- 基础笔锋模式 -->
  <wd-signature pressure :height="300" />

  <!-- 自定义笔锋参数 -->
  <wd-signature
    pressure
    :height="300"
    :min-width="1"
    :max-width="6"
    :min-speed="1.5"
    background-color="#f5f5f5"
  />

  <!-- 笔锋模式 + 历史记录 -->
  <wd-signature
    pressure
    enable-history
    :height="300"
    :min-width="1"
    :max-width="6"
    background-color="#f5f5f5"
  />
</template>
```

### 示例三：自定义底部按钮

通过 `#footer` 插槽完全自定义底部按钮区域，实现更灵活的操作控制。

```vue
<template>
  <wd-signature :disabled="disabled" enable-history :step="3">
    <template #footer="{ clear, confirm, currentStep, restore, revoke, historyList }">
      <wd-button block @click="changeDisabled" v-if="disabled">开始签名</wd-button>
      <block v-if="!disabled">
        <wd-button size="small" plain @click="revoke" :disabled="currentStep <= 0">撤回</wd-button>
        <wd-button size="small" plain @click="restore" :disabled="currentStep >= historyList.length">恢复</wd-button>
        <wd-button size="small" plain @click="clear">清除</wd-button>
        <wd-button size="small" @click="confirm">确定</wd-button>
      </block>
    </template>
  </wd-signature>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const disabled = ref(true)

function changeDisabled() {
  disabled.value = false
}
</script>
```

### 示例四：弹窗中使用签名板

在弹窗中展示签名板，打开弹窗时通过 `init` 方法重新初始化画板，签名完成后自动关闭弹窗并预览签名图片。

```vue
<template>
  <wd-button type="primary" @click="showPopup = true">打开签名板</wd-button>

  <wd-popup
    v-model="showPopup"
    closable
    safe-area-inset-bottom
    position="bottom"
    custom-style="padding: 48px 20px 20px 20px; border-radius: 16px 16px 0 0;"
    @after-enter="signatureRef?.init()"
  >
    <wd-signature
      ref="signatureRef"
      :height="300"
      enable-history
      pressure
      background-color="#f5f5f5"
      @confirm="handlePopupConfirm"
    />
  </wd-popup>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { SignatureInstance, SignatureResult } from '@/uni_modules/wot-ui-plus/components/wd-signature/types'

const showPopup = ref(false)
const signatureRef = ref<SignatureInstance>()

function handlePopupConfirm(result: SignatureResult) {
  showPopup.value = false
  if (result.success) {
    uni.previewImage({
      urls: [result.tempFilePath]
    })
  }
}
</script>
```

### 示例五：自定义画笔样式

自定义画笔颜色和宽度，适配不同视觉风格需求。

```vue
<template>
  <wd-signature pen-color="#0083ff" :line-width="4" />
</template>
```

## 注意事项

- **Canvas 平台差异**：微信小程序使用 2D Canvas（`type="2d"`），其他平台使用传统 Canvas，组件内部已做兼容处理
- **导出图片清晰度**：`export-scale` 值越大，导出图片越清晰，但文件体积也会相应增大。建议根据实际业务需求设置，移动端通常设为 2 即可获得较好的清晰度
- **笔锋模式原理**：笔锋模式通过检测书写速度来动态调整笔画宽度，快速书写产生细线条，慢速书写产生粗线条。笔画宽度变化率被限制在最大 20%，以确保笔画过渡平滑
- **撤销步长**：`step` 属性控制每次撤销/恢复的线条数量，默认为 1（每次撤销一条笔迹）
- **弹窗中初始化**：在弹窗中使用签名板时，需在弹窗动画完成后的 `@after-enter` 事件中调用 `init()` 方法重新初始化画板，否则可能因尺寸计算不准确导致画板显示异常
- **背景透明色判断**：组件内部会自动判断背景色是否为透明色，透明背景不会进行填充绘制
- **禁用状态**：设置 `disabled` 为 `true` 后，画板上的触摸事件将被忽略，无法进行签名绘制
- **文件质量**：`quality` 属性仅在 `fileType` 为 `jpg` 时生效，取值范围为 0~1
- **历史记录内存**：开启 `enable-history` 后，所有笔迹记录会保存在内存中，大量笔迹可能会占用较多内存
- **钉钉小程序兼容性**：钉钉小程序中 `canvasToTempFilePath` 返回的文件路径字段为 `filePath` 而非 `tempFilePath`，组件内部已做兼容处理
