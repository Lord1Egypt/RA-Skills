# Progress 进度条


## 组件概况

Progress 进度条组件用于展示操作的当前进度，为用户提供直观的视觉反馈。该组件支持百分比数值展示、自定义颜色（支持单色、颜色数组、渐变对象）、多种状态（成功、危险、警告），以及平滑的过渡动画效果。适用于文件上传、数据加载、任务处理等需要展示进度信息的业务场景。

## 核心功能描述

- **百分比进度**：通过 `percentage` 属性设置进度值，范围为 0-100
- **进度文字显示**：默认显示百分比文字，通过 `hideText` 属性隐藏
- **单色模式**：通过 `color` 属性设置进度条颜色，支持 CSS 颜色值（如 `#00c740`、`red`）
- **颜色数组模式**：传入字符串数组，颜色按百分比等分自动分配（如 4 个颜色分别在 25%、50%、75%、100% 处分界）
- **渐变对象模式**：传入 `ProgressColor[]` 数组，精确控制每个颜色节点的百分比位置
- **状态图标**：设置 `status` 属性后，隐藏文字并显示对应状态图标
- **平滑动画**：进度变化时带有过渡动画，通过 `duration` 属性控制动画速度（默认每 1% 耗时 30ms）
- **暗色模式支持**：内置 dark 主题样式，自动跟随系统主题切换

## 适用业务场景

- **文件上传**：展示文件上传的实时进度，让用户了解上传进展
- **数据加载**：页面初始化或数据拉取时展示加载进度，缓解用户等待焦虑
- **任务处理**：批量操作（如批量删除、批量导入）时展示整体完成进度
- **表单提交**：多步骤表单的完成进度指示
- **状态反馈**：操作成功、失败、警告等状态的场景化图标展示
- **下载进度**：资源下载、缓存进度展示

## API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| percentage | number | 0 | 否 | 进度百分比值，范围 0-100 |
| hideText | boolean | false | 否 | 是否隐藏进度条上的百分比文字 |
| color | string \| string[] \| ProgressColor[] | - | 否 | 进度条颜色，支持单色、颜色数组、渐变对象 |
| duration | number | 30 | 否 | 进度增加 1% 所需的时间（毫秒） |
| status | `'success' \| 'danger' \| 'warning'` | - | 否 | 进度条状态，设置后显示对应图标 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点类名 |

#### status 可选值

| 值 | 图标名称 | 说明 | 适用场景 |
|---|---------|------|---------|
| success | check-circle | 成功图标 | 任务完成、上传成功 |
| danger | close-circle | 失败图标 | 任务失败、网络错误 |
| warning | attention | 警告图标 | 任务异常、超时警告 |

#### ProgressColor 类型定义

```typescript
type ProgressColor = {
  color: string       // 颜色值
  percentage: number  // 百分比阈值
}
```

### Events

组件不对外暴露任何事件。

### Methods

组件不对外暴露任何方法。

### Slots

组件不对外暴露任何插槽。

## 使用示例

### 示例 1：基本用法

最基础的进度条展示，默认显示百分比文字，进度条高度为 3px，背景色为 `rgba(229, 229, 229, 1)`，进度条颜色为主题色 `#4D80F0`。

```vue
<template>
  <view>
    <!-- 默认进度条（0%） -->
    <wd-progress :percentage="0" />

    <!-- 30% 进度 -->
    <wd-progress :percentage="30" />

    <!-- 60% 进度 -->
    <wd-progress :percentage="60" />

    <!-- 100% 完成 -->
    <wd-progress :percentage="100" />
  </view>
</template>
<script lang="ts" setup>
</script>
```

进度条由外层容器（占满宽度，内边距为 `9px 0 8px`）、外层轨道（圆角背景）、内层进度条（动态宽度）和右侧百分比文字（字号 14px，颜色 `#333`，宽度 30px，左边距 5px）组成。进度变化时带有线性过渡动画。

### 示例 2：隐藏进度文字与状态展示

当不需要显示进度文字时，可以通过 `hideText` 属性隐藏。结合 `status` 属性，可以在进度条完成或异常时显示对应的状态图标。

```vue
<template>
  <view>
    <!-- 隐藏进度文字 -->
    <wd-progress :percentage="60" hide-text />

    <!-- 成功状态 -->
    <wd-progress :percentage="100" hide-text status="success" />

    <!-- 危险/失败状态 -->
    <wd-progress :percentage="80" hide-text status="danger" />

    <!-- 警告状态 -->
    <wd-progress :percentage="90" hide-text status="warning" />
  </view>
</template>
<script lang="ts" setup>
</script>
```

设置 `status` 属性后，组件会隐藏百分比文字并显示对应图标（图标字号 18px）：
- `success` 显示 `check-circle` 图标，颜色为绿色（`#34d19d`）
- `danger` 显示 `close-circle` 图标，颜色为红色（`#fa4350`）
- `warning` 显示 `attention` 图标，颜色为橙色（`#f0883a`）

### 示例 3：自定义颜色

通过 `color` 属性自定义进度条的颜色。支持传入单个颜色值，进度条将始终使用该颜色渲染。

```vue
<template>
  <view>
    <!-- 绿色进度条 -->
    <wd-progress :percentage="80" color="#00c740" />

    <!-- 使用 CSS 颜色名称 -->
    <wd-progress :percentage="50" color="green" />

    <!-- 使用 RGB/RGBA -->
    <wd-progress :percentage="70" color="rgb(77, 128, 240)" />
  </view>
</template>
<script lang="ts" setup>
</script>
```

### 示例 4：颜色数组（等分渐变）

传入字符串数组时，颜色会按数组长度等分百分比区间。例如 4 个颜色会分别在 25%、50%、75%、100% 处分界，进度条在不同进度区间显示不同颜色。

```vue
<template>
  <view>
    <!-- 4 色等分渐变：25%、50%、75%、100% -->
    <wd-progress
      :percentage="100"
      :color="['#00c740', '#ffb300', '#e2231a', '#0083ff']"
    />

    <!-- 3 色等分渐变：33.3%、66.7%、100% -->
    <wd-progress
      :percentage="80"
      :color="['#34d19d', '#f0883a', '#fa4350']"
    />
  </view>
</template>
<script lang="ts" setup>
</script>
```

颜色数组的分界点计算公式：`分界点 = (index + 1) * (100 / 数组长度)`。当进度跨越分界点时，进度条颜色会自动切换到对应区间的颜色，切换过程带有平滑过渡动画。

### 示例 5：渐变对象（精确控制）

传入 `ProgressColor[]` 数组，可以精确控制每个颜色节点的百分比阈值。这种方式适合需要自定义颜色分界点的场景。

```vue
<template>
  <view>
    <wd-progress :percentage="100" :color="colorStops" />
  </view>
</template>
<script lang="ts" setup>
  import type { ProgressColor } from 'wot-design-uni/components/wd-progress/types'
  import { ref } from 'vue'

  const colorStops = ref<ProgressColor[]>([
    {
      color: 'yellow',
      percentage: 30
    },
    {
      color: 'red',
      percentage: 60
    },
    {
      color: 'blue',
      percentage: 80
    },
    {
      color: 'black',
      percentage: 90
    }
  ])
</script>
```

使用 `ProgressColor` 对象数组时：
- 每个对象包含 `color`（颜色值）和 `percentage`（百分比阈值）两个属性
- 数组会按 `percentage` 从小到大自动排序
- 进度在某个阈值区间时，显示对应的颜色
- 例如上述示例中，进度 0-30% 显示黄色，30-60% 显示红色，60-80% 显示蓝色，80-90% 显示黑色，90-100% 也显示黑色（最后一个颜色覆盖剩余区间）

### 示例 6：动态进度

通过响应式变量控制进度值，配合加减按钮实现动态进度展示。进度变化时带有平滑过渡动画。

```vue
<template>
  <view>
    <wd-progress :percentage="percentageDynamic" />
    <wd-button
      custom-style="margin-right: 10px;"
      @click="add"
      type="success"
      size="small"
    >
      +10
    </wd-button>
    <wd-button @click="reduce" type="error" size="small">
      -10
    </wd-button>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const percentageDynamic = ref<number>(50)

  // 增加 10% 进度
  const add = () => {
    percentageDynamic.value = Math.min(percentageDynamic.value + 10, 100)
  }

  // 减少 10% 进度
  const reduce = () => {
    percentageDynamic.value = Math.max(percentageDynamic.value - 10, 0)
  }
</script>
```

动态修改进度时需要注意：
- `percentage` 值必须在 0-100 范围内，超出范围会在控制台输出警告信息
- 进度变化时，过渡动画时长 = `|目标进度 - 当前进度| * duration`（单位：秒）
- 动画使用 CSS `transition` 实现，过渡属性为 `width`，缓动函数为 `linear`

### 示例 7：控制动画速度

通过 `duration` 属性控制进度变化的动画速度，默认每 1% 耗时 30ms。

```vue
<template>
  <view>
    <!-- 默认速度（30ms/%） -->
    <wd-progress :percentage="50" />

    <!-- 慢速动画（100ms/%） -->
    <wd-progress :percentage="50" :duration="100" />

    <!-- 快速动画（10ms/%） -->
    <wd-progress :percentage="50" :duration="10" />

    <!-- 无动画（0ms/%） -->
    <wd-progress :percentage="50" :duration="0" />
  </view>
</template>
<script lang="ts" setup>
</script>
```

### 示例 8：常用组合

展示文件上传场景中常见的进度条组合用法，包括进度展示、成功状态、失败状态和警告状态。

```vue
<template>
  <view>
    <!-- 上传中 -->
    <view class="upload-item">
      <text>文件上传中...</text>
      <wd-progress :percentage="uploadProgress" />
    </view>

    <!-- 上传完成 -->
    <view class="upload-item">
      <text>文件上传完成</text>
      <wd-progress :percentage="100" hide-text status="success" />
    </view>

    <!-- 上传失败 -->
    <view class="upload-item">
      <text>文件上传失败</text>
      <wd-progress :percentage="45" hide-text status="danger" />
    </view>

    <!-- 上传超时警告 -->
    <view class="upload-item">
      <text>文件上传超时</text>
      <wd-progress :percentage="70" hide-text status="warning" />
    </view>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const uploadProgress = ref<number>(65)
</script>
<style lang="scss" scoped>
  .upload-item {
    margin-bottom: 16px;
  }
</style>
```

## 注意事项

1. **percentage 值范围**：`percentage` 值必须在 0-100 之间，传入无效值（如负数、大于 100、NaN）时会在浏览器控制台输出错误提示 `The value of percentage must be between 0 and 100`，但组件仍会渲染
2. **颜色数组格式校验**：当 `color` 为数组时，如果数组元素不是纯字符串数组或 `ProgressColor` 对象数组，会抛出错误 `Color must be String or Object with color and percentage`
3. **渐变对象 percentage 必须为数字**：使用 `ProgressColor[]` 时，如果 `percentage` 无法转换为数字，会抛出错误 `All the percentage must can be formatted to Number`
4. **颜色切换动画机制**：进度变化时，组件会根据新旧进度值的大小关系，从前向后或从后向前遍历颜色分界点，逐段执行颜色切换动画，每段动画之间有 50ms 的延迟
5. **status 优先级**：当 `status` 属性有值且 `hideText` 为 `true` 时，组件显示状态图标而非百分比文字；如果 `hideText` 为 `false`，则仍然显示百分比文字，不显示图标
6. **color 属性对 status 图标的影响**：当 `status` 生效时，如果 `color` 属性为字符串类型，图标颜色会使用 `color` 的值，否则使用状态对应的默认颜色
7. **动画时长计算**：过渡动画的 `transition-duration` 计算公式为 `|目标进度 - 当前进度| * duration / 1000` 秒，当进度变化较大时动画时间会相应变长
8. **customStyle 与 customClass 的使用**：通过 `customStyle` 和 `customClass` 可以进行自定义样式扩展，例如修改进度条容器的宽度、添加额外的间距等
9. **暗色模式自动适配**：组件已内置暗色主题样式，进度文字颜色在暗色模式下会自动调整，无需额外配置
