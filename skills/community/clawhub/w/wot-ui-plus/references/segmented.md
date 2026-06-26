# Segmented 分段器


## 组件概况

分段器组件，用作一组选项的切换展示，常用于标签页导航、分类筛选等场景，支持按钮模式和分段模式。

## 何时使用

- 需要在少量选项中切换展示不同内容时
- 用作页面顶部的分类导航标签时
- 需要可自定义主题色、形状的分段控制时

## 基本用法

通过 `options` 传入选项数组，`v-model` 绑定当前选中项的索引值，`mode` 控制显示模式。

```vue
<template>
  <wd-segmented :options="['全部', '待付款', '已完成']" v-model="current" @change="handleChange" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const current = ref(0)

const handleChange = (index: number, item: any) => {
  console.log('当前选中索引:', index, '选项内容:', item)
}
</script>
```

## 进阶示例

### 示例一：基础 box 模式

通过 `mode="box"` 设置分段模式，激活项以背景色块高亮显示。

```vue
<template>
  <wd-segmented :options="list" mode="box" v-model="current" @change="handleChange" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const list = ['未付款', '待评价', '已付款']
const current = ref(0)

const handleChange = (index: number, item: any) => {
  current.value = index
  console.log('选中了:', item)
}
</script>
```

### 示例二：button 按钮模式

通过 `mode="button"` 设置按钮模式，激活滑块以 `barColor` 设置颜色，容器背景色通过 `bgColor` 设置。

```vue
<template>
  <wd-segmented
    :options="list"
    mode="button"
    barColor="#fff"
    activeColor="#3c9cff"
    v-model="current"
    @change="handleChange"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const list = ['未付款', '待评价', '已付款']
const current = ref(0)

const handleChange = (index: number) => {
  current.value = index
  console.log('当前索引:', index)
}
</script>
```

### 示例三：圆角模式

通过 `shape="round"` 设置选项为圆角形状，适用于 box 和 button 两种模式。

```vue
<template>
  <!-- 圆角 box 模式 -->
  <wd-segmented :options="list" mode="box" shape="round" v-model="current" @change="handleChange" />

  <!-- 圆角 button 模式 -->
  <wd-segmented
    :options="list"
    mode="button"
    shape="round"
    barColor="#3c9cff"
    activeColor="#fff"
    v-model="current"
    @change="handleChange"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const list = ['未付款', '待评价', '已付款']
const current = ref(0)

const handleChange = (index: number) => {
  current.value = index
}
</script>
```

### 示例四：自定义主题色

通过 `activeColor` 和 `barColor` 自定义激活状态颜色，实现主题切换效果。

```vue
<template>
  <!-- box 模式自定义激活色 -->
  <wd-segmented :options="list" mode="box" v-model="current" activeColor="#f56c6c" @change="handleChange" />

  <!-- button 模式自定义激活色 -->
  <wd-segmented
    :options="list"
    mode="button"
    v-model="current"
    activeColor="#fff"
    barColor="#f56c6c"
    @change="handleChange"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const list = ['未付款', '待评价', '已付款']
const current = ref(0)

const handleChange = (index: number) => {
  current.value = index
}
</script>
```

### 示例五：禁用选项

通过 options 传入对象数组，对需要禁用的选项设置 `disabled: true`，也可通过 `disabled` 属性禁用整个组件。

```vue
<template>
  <wd-segmented :options="list" mode="button" v-model="current" @change="handleChange" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 对象数组，可单独设置某项禁用状态
const list = [
  { name: '未付款', disabled: true },
  { name: '待评价' },
  { name: '已付款' }
]
const current = ref(1)

const handleChange = (index: number) => {
  current.value = index
}
</script>
```

### 示例六：自定义标签内容

通过 `label` 插槽自定义每个选项的渲染内容，可以展示头像、图标等自定义元素。

```vue
<template>
  <wd-segmented :options="userList" v-model="current" height="80px" @change="handleChange">
    <template #label="{ option }">
      <view class="custom-label">
        <image
          style="border-radius: 50%; width: 32px; height: 32px"
          :src="option.avatar"
        />
        <view class="name">{{ option.value }}</view>
      </view>
    </template>
  </wd-segmented>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const userList = [
  { value: '张三', disabled: false, avatar: '/static/img/a1.png' },
  { value: '李四', disabled: false, avatar: '/static/img/a2.png' },
  { value: '王五', disabled: true, avatar: '/static/img/a3.png' },
  { value: '赵六', disabled: false, avatar: '/static/img/a4.png' }
]
const current = ref(0)

const handleChange = (index: number) => {
  console.log('segmented change:', index)
}
</script>

<style scoped>
.custom-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4px;
}
.name {
  margin-top: 4px;
  font-size: 12px;
}
</style>
```

## API

### Props

| 属性名 | 说明 | 类型 | 默认值 |
|--------|------|------|--------|
| options | 选项数据数组，支持字符串数组或对象数组 | `string[] \| object[]` | `[]` |
| v-model | 当前选中项的索引值 | `number \| string` | `0` |
| mode | 显示模式，`button` 为按钮模式，`box` 为分段模式 | `'button' \| 'box'` | `'button'` |
| shape | 选项形状，`square` 为方形，`round` 为圆角 | `'square' \| 'round'` | `'square'` |
| activeColor | 激活状态的颜色（button 模式下为滑块内文字颜色，box 模式下为滑块背景色） | `string` | `'#3c9cff'` |
| inactiveColor | 未激活状态的文字颜色 | `string` | `'#303133'` |
| bgColor | 组件背景颜色，仅在 `mode="button"` 时有效 | `string` | `'#eeeeef'` |
| barColor | 滑块背景颜色，仅在 `mode="button"` 时有效 | `string` | `''` |
| fontSize | 文字大小 | `string \| number` | `12` |
| bold | 激活选项的字体是否加粗 | `boolean` | `true` |
| height | 组件高度 | `string \| number` | `35` |
| keyName | 从 options 对象数组中读取的键名（用于显示文本） | `string` | `'name'` |
| disabled | 是否禁用整个组件 | `boolean` | `false` |
| disabledBgColor | 禁用状态的背景颜色 | `string` | `'#c0c4cc'` |
| disabledColor | 禁用状态的文字颜色 | `string` | `'#c0c4cc'` |
| vibrate-short | 切换选项时是否触发短振动 | `boolean` | `false` |
| custom-style | 自定义根节点样式 | `string` | `-` |
| custom-class | 自定义根节点 class | `string` | `-` |

### Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| change | 选项切换时触发 | `(index: number, item: any): void` |

> `change` 事件回调参数说明：
> - `index`: 当前选中项的索引
> - `item`: 当前选中项的原始数据（字符串或对象）

### Slots

| 插槽名 | 说明 | 作用域参数 |
|--------|------|------------|
| label | 自定义选项标签内容 | `{ option: object }` - 当前选项的对象数据 |

> 当 options 为字符串数组时，作用域参数中的 `option` 会被包装为 `{ value: string }` 格式。

## 数据格式说明

### options 数据结构

组件支持两种数据格式：

**字符串数组：**

```ts
const options = ['选项1', '选项2', '选项3']
```

**对象数组：**

```ts
const options = [
  { name: '选项1', disabled: false },
  { name: '选项2', disabled: true },
  { name: '选项3', disabled: false }
]
```

对象数组中每个选项可配置以下属性：

| 属性 | 说明 | 类型 |
|------|------|------|
| name | 选项显示文本（可通过 `keyName` 修改读取字段） | `string` |
| disabled | 是否禁用该选项 | `boolean` |
| activeColor | 该选项激活时的颜色（覆盖全局设置） | `string` |
| inactiveColor | 该选项未激活时的颜色（覆盖全局设置） | `string` |
| disabledColor | 该选项禁用时的颜色（覆盖全局设置） | `string` |

## 注意事项

1. `v-model` 绑定的是选项的**索引值**（从 0 开始），而非选项的值本身。
2. 在 box 模式下，激活状态的文字颜色固定为白色 `#fff`，未激活状态使用 `inactiveColor`。
3. 在 button 模式下，激活状态的文字颜色使用 `activeColor`。
4. 对象数组中可以为单个选项设置独立的 `activeColor`、`inactiveColor`、`disabledColor`，会覆盖全局对应属性。
5. 组件支持窗口大小变化时的自动适配，确保滑块位置始终正确。
6. `vibrate-short` 仅在支持振动 API 的设备上生效。
7. 组件内部使用 `translateX` 实现滑块动画，box 模式下会自动计算滑块圆角以确保视觉一致性。
