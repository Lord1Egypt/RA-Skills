# Circle 圆形进度


## 组件概况

`wd-circle` 是一个基于 Canvas 绘制的圆形进度组件，支持动画过渡、渐变色填充、自定义文字展示等丰富功能。组件内部通过 `canvas` 元素绘制环形轨道与进度弧线，适用于需要直观展示百分比进度的业务场景。

## 核心功能描述

- **Canvas 绘制**：基于 Canvas 2D API 绘制圆形轨道和进度弧线，在微信小程序中使用 `canvas2d` 新接口，在其他平台使用旧版 `createCanvasContext` 接口
- **动画过渡**：内置定时器动画，通过 `speed` 属性控制进度变化速率，实现平滑过渡效果
- **渐变色支持**：`color` 属性支持传入对象格式的渐变色配置
- **进度端点形状**：通过 `strokeLinecap` 属性可设置进度条端点的形状（`butt`、`round`、`square`）
- **顺时针/逆时针**：支持通过 `clockwise` 属性切换进度增长方向
- **零值处理**：当进度值为 0 时，自动在顶部渲染一个小圆点而非完整的弧线
- **v-model 双向绑定**：通过 `modelValue` 属性实现数据双向绑定

## 适用业务场景

- 数据仪表盘中的指标完成率展示
- 任务进度、下载进度的环形展示
- 会员等级/经验值进度展示
- 数据统计可视化中的占比展示

## 使用示例

### 示例一：基本用法

最基础的圆形进度组件，通过 `v-model` 绑定当前进度值，使用 `text` 属性显示提示文字。

```vue
<template>
  <wd-circle v-model="current" :text="current + '%'" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const current = ref<number>(20)
</script>
```

### 示例二：样式定制

通过 `stroke-width`、`layer-color`、`color`、`size`、`clockwise` 等属性实现丰富的样式定制效果。

```vue
<template>
  <!-- 进度条宽度定制 -->
  <wd-circle v-model="current" :stroke-width="6" text="宽度定制" />

  <!-- 轨道和进度条颜色定制 -->
  <wd-circle v-model="current" layer-color="#eee" color="#ee0a24" text="颜色定制" />

  <!-- 渐变色进度条 -->
  <wd-circle v-model="current" :color="gradientColor" text="渐变色" />

  <!-- 逆时针方向 -->
  <wd-circle v-model="current" color="#07c160" :clockwise="false" text="逆时针" />

  <!-- 大小定制 -->
  <wd-circle v-model="current" :size="120" text="大小定制" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const current = ref<number>(20)

// 进度条渐变色配置，key 为百分比位置，value 为对应颜色
const gradientColor: Record<string, string> = {
  '0': 'red',
  '100': 'white'
}
</script>
```

### 示例三：使用插槽自定义内容

当不设置 `text` 属性时，组件会渲染默认插槽，允许在圆环中心插入任意自定义内容。

```vue
<template>
  <wd-circle v-model="current" :stroke-width="6">
    <view style="color: red">{{ current }}%</view>
  </wd-circle>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const current = ref<number>(20)
</script>
```

### 示例四：动态增减进度

通过按钮控制进度值的增加和减少，组件内置的动画会自动过渡到新值。

```vue
<template>
  <wd-circle v-model="current" :text="current + '%'" />
  <wd-button type="primary" size="small" @click="doAdd">增加</wd-button>
  <wd-button type="error" size="small" @click="doDecre">减少</wd-button>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const current = ref<number>(20)

function doAdd() {
  if (current.value < 100) {
    current.value += 10
  }
}

function doDecre() {
  if (current.value > 0) {
    current.value -= 10
  }
}
</script>
```

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| v-model / modelValue | 当前进度值，范围 0-100 | number | - | 0 | - |
| size | 圆环直径，单位为 px | number | - | 100 | - |
| color | 进度条颜色，传入对象格式可以定义渐变色 | string \| Record<string, string> | - | '#4d80f0' | - |
| layer-color | 轨道颜色 | string | - | '#EBEEF5' | - |
| fill | 填充颜色 | string | - | - | - |
| speed | 动画速度，单位为 rate/s | number | - | 50 | - |
| text | 圆环中心显示的文字 | string | - | - | - |
| stroke-width | 进度条宽度，单位为 px | number | - | 10 | - |
| stroke-linecap | 进度条端点的形状 | StrokeLinecapType | 'butt' \| 'round' \| 'square' | 'round' | - |
| clockwise | 是否顺时针增加 | boolean | - | true | - |
| custom-style | 根节点自定义样式 | string | - | - | - |
| custom-class | 根节点自定义类名 | string | - | - | - |

### Slots

| 名称 | 说明 |
|------|------|
| default | 当不设置 `text` 属性时生效，自定义圆环中心显示的内容 |

### Methods

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| drawCircle | 重新绘制圆形进度 | currentValue: number | void |
| reRender | 重新渲染组件，带动画过渡效果 | - | void |

## 注意事项

1. **Canvas 渲染差异**：组件在微信小程序中使用 `canvas2d` 新接口（通过 `canvasHelper` 适配器），在其他平台（如支付宝小程序、H5）使用旧版 `createCanvasContext` 接口。两种实现可能存在渲染差异，建议在目标平台上充分测试。

2. **尺寸适配**：在支付宝小程序中，组件内部会自动将 `size` 和 `strokeWidth` 乘以设备像素比进行适配。在其他平台直接使用原始值。

3. **进度值范围**：组件内部通过 `format` 函数将进度值限制在 0-100 范围内，超出范围的值会被自动截断。

4. **动画性能**：`speed` 属性控制动画速度，值越大动画越快。当 `speed` 小于等于 0 或大于 1000 时，不启用动画，直接跳转到目标值。动画通过 `setTimeout` 实现，步长为 1，每步间隔为 `1000 / speed` 毫秒。

5. **零值圆点**：当进度值为 0 时，不会绘制进度弧线，而是在圆环顶部（角度 0 位置）绘制一个小圆点，圆点直径等于进度条宽度。

6. **渐变色的使用**：`color` 属性传入对象时，key 为 0-100 之间的数值表示渐变位置，value 为对应颜色。组件会按 key 值排序后创建线性渐变，渐变方向为从右到左（`createLinearGradient(canvasSize, 0, 0, 0)`）。

7. **size 变化重绘**：当 `size` 属性发生变化时，组件会通过定时器（50ms 延迟）重新绘制圆形进度，以确保尺寸计算完成。

8. **组件卸载清理**：组件卸载时会自动清除动画定时器，避免内存泄漏。
