# CountDown 倒计时


## 组件概况

CountDown 倒计时组件用于展示从指定时间开始倒数的剩余时间，支持秒级和毫秒级两种精度模式。该组件采用高性能的 `requestAnimationFrame` 实现精确计时，提供完整的生命周期管理和事件回调机制。适用于秒杀活动、限时抢购、考试倒计时、验证码有效期等需要倒计时展示的业务场景。

## 核心功能描述

- **高精度计时**：基于 `requestAnimationFrame` 实现，支持秒级和毫秒级两种精度模式
- **灵活格式化**：通过 `format` 属性自定义时间显示格式，支持天、时、分、秒、毫秒的任意组合
- **自动倒计时**：默认组件挂载后自动开始倒计时，也可手动控制
- **完整方法控制**：暴露 `start`、`pause`、`reset` 方法，支持开始、暂停、重置操作
- **事件回调**：提供 `change` 事件（每次时间变化触发）和 `finish` 事件（倒计时结束触发）
- **作用域插槽**：支持通过默认插槽获取当前时间数据，实现完全自定义的倒计时展示
- **高性能优化**：秒级模式下仅在秒数变化时更新，避免不必要的重渲染
- **暗色模式支持**：内置 dark 主题样式，自动跟随系统主题切换

## 适用业务场景

- **限时抢购/秒杀**：电商活动中展示活动剩余时间，营造紧迫感
- **验证码倒计时**：展示验证码有效期，超时后允许重新获取
- **考试/答题倒计时**：在线考试系统中展示剩余答题时间
- **订单超时**：展示订单支付剩余时间，超时自动取消
- **活动预告**：展示距离活动开始的倒计时
- **游戏计时**：游戏中的倒计时关卡、限时挑战等场景

## API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| time | number | - | 是 | 倒计时时长，单位毫秒 |
| millisecond | boolean | false | 否 | 是否开启毫秒级渲染 |
| format | string | `'HH:mm:ss'` | 否 | 格式化时间格式 |
| autoStart | boolean | true | 否 | 是否自动开始倒计时 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点样式类名 |

#### format 格式说明

| 占位符 | 说明 | 示例 |
|--------|------|------|
| DD | 天数（两位数） | `01`、`15` |
| HH | 小时数（两位数） | `00`、`23` |
| mm | 分钟数（两位数） | `00`、`59` |
| ss | 秒数（两位数） | `00`、`59` |
| S | 毫秒（1 位） | `0` - `9` |
| SS | 毫秒（2 位） | `00` - `99` |
| SSS | 毫秒（3 位） | `000` - `999` |

> **注意**：格式中若未使用 `DD`，天数会自动累加到小时；未使用 `HH`，小时累加到分钟；未使用 `mm`，分钟累加到秒；未使用 `ss`，秒累加到毫秒。

### Events

| 事件名称 | 参数 | 说明 |
|---------|------|------|
| change | `current: TimeData` | 倒计时每次变化时触发 |
| finish | - | 倒计时结束时触发 |

#### TimeData 类型定义

```typescript
type TimeData = {
  days: number           // 天数
  hours: number          // 小时数（0-23）
  minutes: number        // 分钟数（0-59）
  seconds: number        // 秒数（0-59）
  milliseconds: number   // 毫秒数（0-999）
}
```

### Methods

通过 ref 获取组件实例后可调用以下方法：

| 方法名称 | 参数 | 说明 |
|---------|------|------|
| start | - | 开始倒计时 |
| pause | - | 暂停倒计时 |
| reset | - | 重置倒计时，若 auto-start 为 true，重设后会自动开始倒计时 |

### Slots

| 插槽名 | 说明 | 子节点内容 | 作用域参数 |
|--------|------|-----------|-----------|
| default | 默认插槽，用于完全自定义倒计时内容的展示 | 任意内容 | `current: TimeData`（当前倒计时时间数据） |

## 使用示例

### 示例 1：基本用法

最基础的倒计时展示，使用默认格式 `HH:mm:ss`，组件挂载后自动开始倒计时。

```vue
<template>
  <view>
    <!-- 30 小时倒计时 -->
    <wd-count-down :time="time" />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  // 30 小时 = 30 * 60 * 60 * 1000 毫秒
  const time = ref(30 * 60 * 60 * 1000)
</script>
```

默认情况下，倒计时以 `HH:mm:ss` 格式显示。当 `time` 属性值发生变化时，组件会自动重置倒计时并重新开始（因为默认 `auto-start` 为 `true`）。

### 示例 2：自定义格式

通过 `format` 属性自定义时间显示格式，支持天、时、分、秒的任意组合，并可添加自定义分隔文字。

```vue
<template>
  <view>
    <!-- 带天数的完整格式 -->
    <wd-count-down
      :time="time"
      format="DD 天 HH 时 mm 分 ss 秒"
    />

    <!-- 仅显示小时和分钟 -->
    <wd-count-down
      :time="time"
      format="HH 小时 mm 分"
    />

    <!-- 紧凑格式 -->
    <wd-count-down
      :time="time"
      format="DD天HH:mm:ss"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const time = ref(30 * 60 * 60 * 1000)
</script>
```

**格式占位符工作原理**：
- `DD` 显示天数，如果格式中不包含 `DD`，则天数会自动转换为小时并累加到 `HH` 上
- `HH` 显示小时数，如果格式中不包含 `HH`，则小时会累加到分钟上
- `mm` 显示分钟数，如果格式中不包含 `mm`，则分钟会累加到秒上
- `ss` 显示秒数，如果格式中不包含 `ss`，则秒会累加到毫秒上
- `S`、`SS`、`SSS` 分别显示 1 位、2 位、3 位毫秒数

### 示例 3：毫秒级渲染

通过设置 `millisecond` 属性开启毫秒级渲染，适用于需要高精度倒计时的场景。

```vue
<template>
  <view>
    <!-- 毫秒级倒计时显示 -->
    <wd-count-down
      :time="time"
      millisecond
      format="HH:mm:ss:SSS"
    />

    <!-- 仅显示秒和毫秒 -->
    <wd-count-down
      :time="5000"
      millisecond
      format="ss:SSS"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const time = ref(30 * 60 * 60 * 1000)
</script>
```

**性能说明**：
- 毫秒级模式基于 `requestAnimationFrame` 实现，每帧都会更新，性能消耗高于秒级模式
- 秒级模式下仅在秒数变化时才更新，避免不必要的重渲染
- 请根据实际业务需求选择是否需要毫秒级精度

### 示例 4：自定义样式（作用域插槽）

通过默认作用域插槽获取当前时间数据，实现完全自定义的倒计时样式。

```vue
<template>
  <view>
    <wd-count-down :time="time">
      <template #default="{ current }">
        <span class="custom-count-down">{{ current.hours }}</span>
        <span class="custom-count-down-colon">:</span>
        <span class="custom-count-down">{{ current.minutes }}</span>
        <span class="custom-count-down-colon">:</span>
        <span class="custom-count-down">{{ current.seconds }}</span>
      </template>
    </wd-count-down>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const time = ref(30 * 60 * 60 * 1000)
</script>
<style lang="scss" scoped>
  .custom-count-down {
    display: inline-block;
    width: 22px;
    color: #fff;
    font-size: 12px;
    text-align: center;
    background-color: #f0883a;
    border-radius: 2px;
  }

  .custom-count-down-colon {
    display: inline-block;
    margin: 0 4px;
    color: #f0883a;
  }
</style>
```

使用作用域插槽时：
- 插槽参数 `current` 包含 `days`、`hours`、`minutes`、`seconds`、`milliseconds` 属性
- 使用插槽后，`format` 属性将不再生效
- 可以完全自由地设计倒计时的视觉呈现

### 示例 5：手动控制

通过 `ref` 获取组件实例，手动控制倒计时的开始、暂停和重置。

```vue
<template>
  <view>
    <wd-count-down
      ref="countDown"
      :time="3000"
      millisecond
      :auto-start="false"
      format="ss:SSS"
      @finish="onFinish"
    />
    <wd-grid clickable border>
      <wd-grid-item text="开始" icon="play-circle-stroke" @itemclick="start" />
      <wd-grid-item text="暂停" icon="pause-circle" @itemclick="pause" />
      <wd-grid-item text="重置" icon="refresh" @itemclick="reset" />
    </wd-grid>
    <wd-toast />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import { useToast } from '@/uni_modules/wot-ui-plus'
  import type { CountDownInstance } from '@/uni_modules/wot-ui-plus/components/wd-count-down/types'

  const { show: showToast } = useToast()
  const countDown = ref<CountDownInstance>()

  const start = () => {
    countDown.value!.start()
  }

  const pause = () => {
    countDown.value!.pause()
  }

  const reset = () => {
    countDown.value!.reset()
  }

  const onFinish = () => showToast('倒计时结束')
</script>
```

**手动控制说明**：
- 设置 `auto-start="false"` 可禁止组件挂载后自动开始倒计时
- `start()`：开始或恢复倒计时
- `pause()`：暂停倒计时，剩余时间保持不变
- `reset()`：重置为初始时间，若 `auto-start` 为 `true` 则自动开始倒计时
- `finish` 事件在倒计时归零时触发

### 示例 6：动态修改时间

监听 `time` 属性变化，动态调整倒计时时长。

```vue
<template>
  <view>
    <wd-count-down :time="dynamicTime" @finish="onFinish" />
    <wd-button @click="addTime" type="primary" size="small">
      增加 5 分钟
    </wd-button>
    <wd-button @click="reduceTime" type="warning" size="small">
      减少 5 分钟
    </wd-button>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const dynamicTime = ref(10 * 60 * 1000) // 初始 10 分钟

  const addTime = () => {
    dynamicTime.value += 5 * 60 * 1000
  }

  const reduceTime = () => {
    dynamicTime.value = Math.max(0, dynamicTime.value - 5 * 60 * 1000)
  }

  const onFinish = () => {
    console.log('倒计时结束')
  }
</script>
```

**动态修改说明**：
- 修改 `time` 属性值时，组件会自动重置倒计时
- 由于默认 `auto-start` 为 `true`，重置后会自动开始新的倒计时
- `change` 事件会在每次时间变化时触发，参数为当前 `TimeData` 对象

### 示例 7：事件监听

监听 `change` 和 `finish` 事件，在倒计时过程中执行自定义逻辑。

```vue
<template>
  <view>
    <wd-count-down
      :time="time"
      @change="onChange"
      @finish="onFinish"
    />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const time = ref(60 * 1000) // 1 分钟

  const onChange = (current: {
    days: number
    hours: number
    minutes: number
    seconds: number
    milliseconds: number
  }) => {
    console.log('剩余时间:', current)
  }

  const onFinish = () => {
    console.log('倒计时结束')
  }
</script>
```

**事件触发时机**：
- `change` 事件：倒计时每次更新时触发，参数为当前剩余时间的 `TimeData` 对象
- `finish` 事件：倒计时归零时触发一次，之后不会再次触发

## 注意事项

1. **time 属性必填**：`time` 是必填属性，必须传入以毫秒为单位的倒计时时长。传入无效值（如 `NaN`、负数）时可能导致倒计时异常

2. **时间格式占位符累加规则**：如果格式字符串中不包含某个时间单位的占位符，该单位的值会自动累加到下一个单位。例如不包含 `DD` 时，天数会累加到小时上，`HH` 可能显示超过 24 的值

3. **毫秒级模式性能**：开启 `millisecond` 后，组件每帧都会更新倒计时，性能消耗较大。仅在需要展示毫秒数的场景下使用

4. **组件卸载处理**：组件在卸载时会自动暂停倒计时，无需手动清理资源，不会造成内存泄漏

5. **动态修改 time 值**：修改 `time` 属性值时，组件会调用 `reset` 方法重置倒计时。如果 `auto-start` 为 `true`，重置后会自动开始倒计时

6. **方法调用时机**：通过 `ref` 获取组件实例后，请确保在组件挂载完成后再调用 `start`、`pause`、`reset` 方法

7. **自定义插槽与 format 互斥**：使用默认作用域插槽自定义内容时，`format` 属性将不再生效，因为插槽内容完全由开发者控制

8. **计时精度**：倒计时基于 `requestAnimationFrame` 实现，在页面不可见时（如切换到后台标签页），浏览器可能会暂停或降低 `requestAnimationFrame` 的调用频率，导致倒计时变慢

9. **暗色模式适配**：组件已内置暗色主题样式，倒计时文字颜色在暗色模式下会自动调整

10. **倒计时结束后的状态**：倒计时结束后，`current` 值归零（所有字段为 0），`finish` 事件触发。如需重新开始，需调用 `reset()` 和 `start()` 方法
