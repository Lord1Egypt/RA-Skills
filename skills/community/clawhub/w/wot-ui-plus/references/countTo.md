# CountTo 数字滚动


## 组件概况

CountTo 数字滚动组件用于实现数字从起始值到结束值的动态递增或递减动画效果。该组件基于 `requestAnimationFrame` 实现高性能的数字变化动画，支持缓动函数、小数精度、数字分隔符、前缀后缀等丰富的配置选项。适用于数据大屏、统计面板、仪表盘、业绩展示等需要数字动态变化效果的场景，能够有效吸引用户注意力并提升界面的视觉表现力。

## 核心功能描述

- **数字递增/递减动画**：支持从 `startVal` 到 `endVal` 的平滑过渡动画，可递增也可递减
- **缓动动画**：内置 `easingFn` 缓动函数，数字变化速度由快到慢，动画效果自然流畅
- **小数精度控制**：通过 `decimals` 属性控制保留的小数位数，支持自定义小数点符号
- **千位分隔符**：通过 `separator` 属性开启千位分隔效果（如 `1,234,567`）
- **前缀/后缀**：支持通过 `prefix` 和 `suffix` 属性添加单位符号（如货币符号、百分比等）
- **主题配色**：内置 `default`、`primary`、`success`、`warning`、`error` 五种预设主题色
- **手动控制**：暴露 `start`、`pause`、`reset` 方法，支持开始、暂停、重置动画
- **自定义样式**：支持自定义字体大小、颜色、根节点样式和样式类
- **插槽扩展**：提供前缀插槽（`prefix`）、默认插槽和后缀插槽（`suffix`），支持完全自定义内容

## 适用业务场景

- **数据大屏**：展示实时数据统计，数字动态变化吸引用户注意力
- **业绩看板**：展示销售额、用户量、订单数等关键指标的动态变化
- **钱包/余额**：展示账户余额的变化过程，提升用户体验
- **排行榜**：展示排名分数，增加视觉表现力
- **倒计时/计时器**：配合倒计时展示时间数值的变化效果
- **统计面板**：各类数据统计、分析报告中需要数字动画展示的场景

## API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| fontSize | number | 16 | 否 | 字体大小（单位：px） |
| color | string | `''` | 否 | 文本颜色，为空时跟随 `type` 主题色 |
| type | string | `'default'` | 否 | 主题类型，可选值为 `default`、`primary`、`success`、`warning`、`error` |
| startVal | number | 0 | 否 | 起始值 |
| endVal | number | 2024 | 否 | 最终值 |
| duration | number | 3000 | 否 | 从起始值到结束值的动画时长，单位毫秒 |
| autoStart | boolean | true | 否 | 是否自动开始动画 |
| decimals | number | 0 | 否 | 保留的小数位数，需大于等于 0 |
| decimal | string | `'.'` | 否 | 小数点符号 |
| separator | string | `','` | 否 | 千位分隔符，传入非数字字符串时启用分隔效果 |
| prefix | string | `''` | 否 | 数字前缀文本（如货币符号） |
| suffix | string | `''` | 否 | 数字后缀文本（如单位） |
| useEasing | boolean | true | 否 | 是否启用缓动动画效果 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点样式类名 |

#### type 可选值

| 值 | 说明 |
|---|------|
| default | 默认主题色 |
| primary | 主要主题色 |
| success | 成功主题色（绿色） |
| warning | 警告主题色（橙色） |
| error | 错误主题色（红色） |

### Events

| 事件名称 | 参数 | 说明 |
|---------|------|------|
| mounted | - | 组件挂载完成时触发 |
| finish | - | 数字动画结束时触发 |

### Methods

通过 ref 获取组件实例后可调用以下方法：

| 方法名称 | 参数 | 说明 |
|---------|------|------|
| start | - | 开始数字滚动动画 |
| pause | - | 暂停数字滚动动画 |
| reset | - | 重置动画，若 `autoStart` 为 `true`，重设后会自动开始动画 |

### Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|-----------|
| default | 默认文本插槽，用于完全自定义数字文本的展示 | 任意内容 |
| prefix | 前缀插槽，替换 `prefix` 属性显示的内容 | 任意内容 |
| suffix | 后缀插槽，替换 `suffix` 属性显示的内容 | 任意内容 |

> **注意**：三个插槽均使用 `wd-text` 组件作为默认渲染，自定义插槽内容时样式由开发者自行控制。

## 使用示例

### 示例 1：基本用法

最基础的数字滚动动画，设置 `endVal` 即可，起始值默认为 0，动画时长默认为 3000ms。

```vue
<template>
  <view>
    <!-- 基础数字滚动，默认 0 到 2024 -->
    <wd-count-to :endVal="endVal" suffix="年" color="#16baaa"></wd-count-to>

    <!-- 带前缀、小数位、后缀的用法 -->
    <wd-count-to
      prefix="￥"
      :decimals="2"
      :endVal="186.321"
      :fontSize="32"
      suffix="%"
      color="#1e9fff"
    ></wd-count-to>

    <!-- 大数字展示，自动千位分隔 -->
    <wd-count-to
      prefix="￥"
      :decimals="2"
      :endVal="21286.321"
      :fontSize="32"
      suffix="%"
      color="#ff5722"
    ></wd-count-to>

    <!-- 自定义动画时长 -->
    <wd-count-to
      prefix="￥"
      :decimals="2"
      :endVal="21286.321"
      :fontSize="32"
      suffix="%"
      color="#ffb800"
      :duration="2000"
    ></wd-count-to>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const endVal = ref<number>(2024)
</script>
```

**说明**：
- `endVal` 属性控制动画最终到达的数值
- `prefix` 和 `suffix` 分别显示在数字前后，字号为数字字号的 0.7 倍
- `decimals` 属性控制小数位数，默认不保留小数
- `separator` 默认为 `,`，会对整数部分自动进行千位分隔

### 示例 2：设置主题

通过 `type` 属性设置数字的主题色，支持 `primary`、`error`、`success`、`warning`、`default` 五种类型。

```vue
<template>
  <view>
    <!-- 主要主题色 -->
    <wd-count-to
      type="primary"
      prefix="￥"
      :startVal="0"
      :endVal="888888"
      suffix="%"
    ></wd-count-to>

    <!-- 错误主题色 -->
    <wd-count-to
      type="error"
      prefix="￥"
      :startVal="0"
      :endVal="888888"
      suffix="%"
    ></wd-count-to>

    <!-- 成功主题色 -->
    <wd-count-to
      type="success"
      prefix="￥"
      :startVal="0"
      :endVal="888888"
      suffix="%"
    ></wd-count-to>

    <!-- 警告主题色 -->
    <wd-count-to
      type="warning"
      prefix="￥"
      :startVal="0"
      :endVal="888888"
      suffix="%"
    ></wd-count-to>

    <!-- 默认主题色 -->
    <wd-count-to
      prefix="￥"
      :startVal="0"
      :endVal="888888"
      suffix="%"
    ></wd-count-to>
  </view>
</template>
<script lang="ts" setup>
</script>
```

**说明**：
- 当 `type` 有值且 `color` 为空时，数字颜色跟随主题色
- 当 `color` 显式设置了颜色值时，`color` 优先级高于 `type`
- `startVal` 可设置动画起始值，默认为 0

### 示例 3：手动控制

通过 `ref` 获取组件实例，手动控制动画的开始、暂停和重置。

```vue
<template>
  <view>
    <wd-count-to
      ref="countTo"
      :auto-start="false"
      prefix="￥"
      :startVal="1000"
      :decimals="3"
      :endVal="9999.32"
      :fontSize="32"
      suffix="%"
      color="#1e9fff"
    ></wd-count-to>

    <wd-grid clickable border>
      <wd-grid-item text="开始" icon="play-circle-stroke" @itemclick="start" />
      <wd-grid-item text="暂停" icon="pause-circle" @itemclick="pause" />
      <wd-grid-item text="重置" icon="refresh" @itemclick="reset" />
    </wd-grid>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import type { CountToInstance } from '@/uni_modules/wot-ui-plus/components/wd-count-to/types'

  const countTo = ref<CountToInstance>()

  const start = () => {
    countTo.value!.start()
  }

  const pause = () => {
    countTo.value!.pause()
  }

  const reset = () => {
    countTo.value!.reset()
  }
</script>
```

**说明**：
- 设置 `auto-start="false"` 可禁止组件挂载后自动播放动画
- `start()`：开始数字滚动动画
- `pause()`：暂停动画，当前数字保持不变
- `reset()`：重置为初始状态，若 `auto-start` 为 `true` 则自动开始动画

### 示例 4：数字递减动画

当 `startVal` 大于 `endVal` 时，数字从大到小递减滚动。

```vue
<template>
  <view>
    <!-- 库存数量递减 -->
    <wd-count-to
      :startVal="1000"
      :endVal="0"
      :duration="5000"
      suffix=" 件"
      :fontSize="28"
      color="#fa4350"
    ></wd-count-to>

    <!-- 倒计时金额 -->
    <wd-count-to
      prefix="￥"
      :startVal="5000.00"
      :endVal="1280.50"
      :decimals="2"
      :duration="3000"
      :fontSize="36"
      color="#ff5722"
    ></wd-count-to>
  </view>
</template>
<script lang="ts" setup>
</script>
```

**说明**：
- 组件内部会自动判断 `startVal > endVal`，使用递减的计算逻辑
- 递减时同样支持缓动动画和千位分隔符
- 递减结束后数字稳定在 `endVal` 值

### 示例 5：自定义前缀后缀（插槽）

通过 `prefix` 和 `suffix` 插槽替换默认的前缀/后缀文字，支持插入图标等自定义内容。

```vue
<template>
  <view>
    <!-- 自定义前缀插槽 -->
    <wd-count-to :endVal="100000" :decimals="2">
      <template #prefix>
        <wd-icon name="wallet" size="16px" color="#1e9fff"></wd-icon>
        <text> 余额 </text>
      </template>
    </wd-count-to>

    <!-- 自定义后缀插槽 -->
    <wd-count-to :endVal="8888" suffix=" 人">
      <template #suffix>
        <wd-icon name="user" size="16px" color="#34d19d"></wd-icon>
        <text> 人</text>
      </template>
    </wd-count-to>
  </view>
</template>
<script lang="ts" setup>
</script>
```

**说明**：
- `prefix` 插槽会替换 `prefix` 属性的默认渲染
- `suffix` 插槽会替换 `suffix` 属性的默认渲染
- 使用插槽后，前缀/后缀的样式由开发者自行控制

### 示例 6：关闭缓动效果

通过 `useEasing` 属性关闭缓动函数，使用线性匀速变化。

```vue
<template>
  <view>
    <!-- 开启缓动（默认），数字变化由快到慢 -->
    <wd-count-to
      :endVal="10000"
      :duration="3000"
      :useEasing="true"
      :fontSize="24"
      color="#1e9fff"
    ></wd-count-to>

    <!-- 关闭缓动，数字匀速变化 -->
    <wd-count-to
      :endVal="10000"
      :duration="3000"
      :useEasing="false"
      :fontSize="24"
      color="#f0883a"
    ></wd-count-to>
  </view>
</template>
<script lang="ts" setup>
</script>
```

**说明**：
- `useEasing` 默认为 `true`，使用指数缓动函数，数字变化由快到慢，视觉效果更自然
- 关闭缓动后，数字在 `duration` 时间内匀速从 `startVal` 变化到 `endVal`
- 缓动公式为 `c * (-Math.pow(2, (-10 * t) / d) + 1) * 1024 / 1023 + b`

### 示例 7：动态修改目标值

通过修改 `endVal` 或 `startVal` 属性，动态改变动画目标值。

```vue
<template>
  <view>
    <wd-count-to
      ref="countTo"
      :endVal="targetVal"
      :decimals="0"
      :duration="2000"
      :fontSize="40"
      color="#4D80F0"
      suffix=" %"
    ></wd-count-to>

    <wd-button @click="increaseTarget" type="primary" size="small">
      增加目标值
    </wd-button>
    <wd-button @click="decreaseTarget" type="warning" size="small">
      减小目标值
    </wd-button>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const targetVal = ref<number>(5000)

  const increaseTarget = () => {
    targetVal.value += 1000
  }

  const decreaseTarget = () => {
    targetVal.value = Math.max(0, targetVal.value - 1000)
  }
</script>
```

**说明**：
- 修改 `startVal`、`endVal`、`duration` 属性时，组件会自动重置动画
- 若 `auto-start` 为 `true`（默认值），重置后会自动重新播放动画
- 建议在修改值前通过 `pause()` 暂停当前动画，避免动画冲突

## 注意事项

1. **自动播放机制**：默认 `autoStart` 为 `true`，组件挂载后会自动开始数字滚动动画。如需手动控制，需显式设置 `auto-start="false"`

2. **动态属性重置**：当 `startVal`、`endVal`、`duration` 三个属性中的任何一个发生变化时，组件会自动调用 `reset` 方法重置动画，并根据 `autoStart` 决定是否自动开始

3. **缓动动画效果**：默认开启 `useEasing`，使用指数缓动函数。动画效果为数字变化由快到慢，视觉感受更自然。关闭后数字匀速变化

4. **千位分隔符启用条件**：`separator` 属性传入非数字字符串时才会启用千位分隔效果。如果传入纯数字字符串，则不会进行分隔

5. **小数位校验**：`decimals` 属性需要大于等于 0，否则不通过校验。小数位控制数字显示精度，如 `decimals=2` 时 `123.456` 显示为 `123.46`

6. **递减动画支持**：当 `startVal > endVal` 时，组件自动执行递减动画。内部通过 `isPositive` 标识判断递增还是递减，使用不同的计算逻辑

7. **默认插槽行为**：组件提供三个插槽（`prefix`、`default`、`suffix`），均通过 `wd-text` 组件进行默认渲染。使用默认插槽后，内部数字文本将由插槽内容替代

8. **前缀/后缀字号**：未使用自定义插槽时，前缀和后缀的字号为数字字号（`fontSize`）的 0.7 倍，保持视觉层次分明

9. **主题色优先级**：当同时设置了 `type` 和 `color` 时，`color` 优先级更高。`type` 仅在 `color` 为空时生效

10. **mounted 事件**：组件在 `onMounted` 钩子中触发 `mounted` 事件，可用于判断数字滚动组件是否已就绪

11. **finish 事件**：数字动画完成时触发 `finish` 事件，可用于动画结束后的后续逻辑处理

12. **性能考虑**：动画基于 `requestAnimationFrame` 实现，在页面不可见时浏览器可能降低调用频率，导致动画变慢
