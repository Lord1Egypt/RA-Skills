# PickerView 选择器视图


## 组件概况

### 组件概述
选择器视图组件是一种在页面中直接展示的选择器，用于在页面内进行选项选择，通常用于表单、设置页、数据筛选等场景。wd-picker-view 组件提供了灵活的配置选项，支持单列/多列选择、自定义数据源、加载状态、选项高度等功能。

### 详细功能描述
- 支持单列和多列选择
- 支持自定义数据源
- 支持加载状态
- 支持自定义选项高度
- 支持自定义滚筒高度
- 支持禁用选项
- 支持立即触发change事件
- 支持双向绑定
- 支持丰富的方法调用
- 支持自定义样式和类名

### 适用业务场景
- 页面内的选择器组件
- 表单中的选择字段
- 数据筛选和排序
- 设置页面的选项选择
- 日期和时间选择
- 地址选择

## 完整API参考

### Props属性

| 名称 | 类型 | 默认值 | 必填 | 描述 |
|------|------|--------|------|------|
| loading | boolean | false | 否 | 加载状态 |
| loadingColor | string | '#4D80F0' | 否 | 加载的颜色，只能使用十六进制的色值写法，且不能使用缩写 |
| columnsHeight | number | 217 | 否 | picker内部滚筒高 |
| itemHeight | number | 35 | 否 | picker item的高度 |
| valueKey | string | 'value' | 否 | 选项对象中，value对应的 key |
| labelKey | string | 'label' | 否 | 选项对象中，展示的文本对应的 key |
| immediateChange | boolean | false | 否 | 是否在手指松开时立即触发picker-view的 change 事件。若不开启则会在滚动动画结束后触发 change 事件，1.2.25版本起提供，仅微信小程序和支付宝小程序支持 |
| modelValue | string / number / boolean / array | '' | 是 | 选中项，如果为多列选择器，则其类型应为数组 |
| columns | array | [] | 否 | 选择器数据，可以为字符串数组，也可以为对象数组，如果为二维数组，则为多列选择器 |
| columnChange | function | - | 否 | 接收 pickerView 实例、选中项、当前修改列的下标、resolve 作为入参，根据选中项和列下标进行判断，通过 pickerView 实例暴露出来的 setColumnData 方法修改其他列的数据源 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### Events事件

| 事件名 | 触发条件 | 参数说明 |
|--------|----------|----------|
| change | 选择器选中项变化时 | { picker: any, value: any, index: number } - pickerView实例、选中值、变化的列下标 |
| pickstart | 选择器开始滚动时 | - |
| pickend | 选择器结束滚动时 | - |
| update:modelValue | 选中值改变时 | value: any - 选中值 |

### Methods方法

| 方法名 | 参数 | 返回值 | 功能说明 |
|--------|------|--------|----------|
| getSelects | - | Record<string, any> / Record<string, any>[] | 获取选中项 |
| getValues | - | string / string[] | 获取选中值 |
| setColumnData | columnIndex: number, data: array, rowIndex: number = 0 | - | 设置列数据 |
| getColumnsData | - | Record<string, string>[][] | 获取所有列数据 |
| getColumnData | columnIndex: number | Record<string, string>[] | 获取某一列数据 |
| getColumnIndex | columnIndex: number | number | 获取某一列的选中项下标 |
| getLabels | - | string[] | 获取所有列选中项的label |
| getSelectedIndex | - | number[] | 获取选中的索引 |
| resetColumns | columns: array | - | 重置列数据 |

### Slots插槽

该组件没有定义插槽。

## 多场景使用示例代码

### 1. 基础用法

```vue
<template>
  <view class="picker-view-demo">
    <view class="demo-title">基础用法</view>
    <wd-picker-view 
      v-model="selectedValue" 
      :columns="columns"
      @change="onChange"
    />
    <view class="picker-view-info">选中值：{{ selectedValue }}</view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const selectedValue = ref('')
const columns = ['男', '女', '保密']

const onChange = (params: { picker: any, value: any, index: number }) => {
  console.log('选择结果', params)
}
</script>

<style scoped>
.picker-view-demo {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.demo-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.picker-view-info {
  font-size: 16px;
  color: #666;
}
</style>
```

### 2. 对象数组数据源

```vue
<template>
  <view class="picker-view-demo">
    <view class="demo-title">对象数组数据源</view>
    <wd-picker-view 
      v-model="selectedValue" 
      :columns="columns"
    />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const selectedValue = ref('')
const columns = [
  { label: '北京', value: 'beijing' },
  { label: '上海', value: 'shanghai' },
  { label: '广州', value: 'guangzhou' },
  { label: '深圳', value: 'shenzhen' }
]
</script>
```

### 3. 多列选择

```vue
<template>
  <view class="picker-view-demo">
    <view class="demo-title">多列选择</view>
    <wd-picker-view 
      v-model="selectedValue" 
      :columns="columns"
    />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const selectedValue = ref(['red', 's'])
const columns = [
  [{ label: '红色', value: 'red' }, { label: '蓝色', value: 'blue' }],
  [{ label: 'S', value: 's' }, { label: 'M', value: 'm' }, { label: 'L', value: 'l' }]
]
</script>
```

### 4. 自定义样式

```vue
<template>
  <view class="picker-view-demo">
    <view class="demo-title">自定义样式</view>
    <wd-picker-view 
      v-model="selectedValue" 
      :columns="columns"
      :columns-height="300"
      :item-height="45"
      custom-style="background-color: #f5f7fa; border-radius: 8px;"
    />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const selectedValue = ref('')
const columns = ['选项1', '选项2', '选项3', '选项4', '选项5']
</script>
```

### 5. 带加载状态

```vue
<template>
  <view class="picker-view-demo">
    <view class="demo-title">带加载状态</view>
    <wd-button @click="loading = !loading">切换加载状态</wd-button>
    <wd-picker-view 
      v-model="selectedValue" 
      :columns="columns"
      :loading="loading"
      loading-color="#ff4d4f"
    />
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const selectedValue = ref('')
const loading = ref(false)
const columns = ['选项1', '选项2', '选项3', '选项4', '选项5']
</script>
```

## 样式定制指南

### customStyle 用法
使用 customStyle 属性可以自定义选择器视图的内联样式，例如修改背景色、边框半径、阴影等。

```vue
<wd-picker-view 
  v-model="selectedValue" 
  :columns="columns"
  custom-style="background-color: #f0f9ff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);"
/>
```

### customClass 用法
使用 customClass 属性可以为选择器视图添加自定义样式类，便于在外部 CSS 中进行样式定制。

```vue
<wd-picker-view 
  v-model="selectedValue" 
  :columns="columns"
  custom-class="my-picker-view"
/>

<style scoped>
:deep(.my-picker-view) {
  --wd-picker-view-mask-color: rgba(255, 255, 255, 0.8);
  --wd-picker-view-roller-background: #4D80F0;
  --wd-picker-view-item-active-color: #4D80F0;
  --wd-picker-view-item-disabled-color: #c0c4cc;
}
</style>
```

## 注意事项

1. **数据源格式**：columns 属性支持字符串数组、对象数组和二维数组，分别对应不同的选择器类型。

2. **双向绑定**：组件支持使用 v-model 双向绑定选中值，也可以使用 :model-value 和 @update:model-value 手动绑定。

3. **loadingColor 属性**：loadingColor 只能使用十六进制的色值写法，且不能使用缩写，例如 #4D80F0 是有效的，而 #000 或 red 是无效的。

4. **immediateChange 属性**：该属性仅在微信小程序和支付宝小程序上支持，用于控制是否在手指松开时立即触发 change 事件。

5. **columnChange 事件**：用于处理多列联动逻辑，接收 pickerView 实例、选中值、当前修改列的下标和 resolve 函数作为参数。

6. **禁用选项**：可以在数据源中添加 disabled: true 属性来禁用某些选项。

7. **方法调用**：可以通过 ref 获取 pickerView 实例，然后调用其暴露的方法，如 getSelects、setColumnData 等。

8. **性能优化**：对于大数据量的场景，建议使用虚拟滚动或分页加载，避免一次性渲染过多选项。

9. **兼容性**：组件在不同平台上的表现可能略有差异，特别是在 immediateChange 属性和滚动动画方面。

10. **样式定制**：可以通过 CSS 变量修改选择器视图的样式，包括遮罩颜色、滚轮背景、选中项颜色等。