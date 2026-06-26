# Table 表格


## 组件概况

Table 表格组件用于以结构化的方式展示大量数据，由 `wd-table`（表格容器）和 `wd-table-col`（列定义）两个关联组件组成。表格支持边框、斑马纹、固定表头、固定列、列排序、索引列、自定义列模板等丰富功能，适用于各类数据展示场景。

## 核心功能描述

- **数据绑定**：通过 `data` 属性传入数组数据，配合 `wd-table-col` 的 `prop` 字段自动映射列数据
- **边框与斑马纹**：默认带有边框和斑马纹效果，可通过 `border` 和 `stripe` 属性控制
- **固定表头**：默认启用 `fixedHeader`，表头通过独立的 `scroll-view` 实现与表体同步滚动
- **固定列**：通过列的 `fixed` 属性实现左侧固定列，支持多列固定，自动计算 `left` 偏移量并添加阴影分隔效果
- **列排序**：通过列的 `sortable` 属性开启排序，点击列头触发 `sort-method` 事件，返回包含 `sortDirection`（0: 未排序, 1: 升序, -1: 降序）的列信息
- **索引列**：通过 `index` 属性开启行号列，默认显示从 1 开始的序号，支持通过对象形式自定义对齐方式、宽度、排序和固定等属性
- **超出省略**：默认开启 `ellipsis`，超出 2 行的内容自动截断并显示省略号
- **自定义列模板**：通过 `wd-table-col` 的 `value` 插槽可自定义单元格内容，作用域参数包含 `row`（当前行数据）和 `index`（行索引）
- **空数据展示**：当 `data` 为空时显示 `emptyText` 提示信息，支持通过 `empty` 插槽自定义空数据内容
- **行点击事件**：点击任意单元格触发 `row-click` 事件，返回 `{ rowIndex }` 参数

## 适用业务场景

- **数据列表展示**：各类管理后台、移动端列表中的结构化数据展示
- **数据排序交互**：需要用户通过点击列头进行排序的数据表格
- **固定关键列**：表格列数较多时，固定关键列（如名称、操作列）便于横向滚动时保持参照
- **行号索引**：需要显示数据行序号的表格场景
- **自定义单元格内容**：需要在单元格内展示按钮、标签、进度条等复杂内容的场景

## API

### wd-table Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| data | 表格数据源，为数组类型，每项为包含各列字段的对象 | array | - | -（必填） | - |
| border | 是否带有边框 | boolean | - | true | - |
| stripe | 是否为斑马纹 table | boolean | - | true | - |
| height | 表格整体高度 | number / string | - | - | - |
| rowHeight | 行高，单位为 px | number / string | - | 40 | - |
| showHeader | 是否显示表头 | boolean | - | true | - |
| ellipsis | 是否超出 2 行隐藏（省略显示） | boolean | - | true | - |
| index | 是否显示索引列，设置为 true 或传入对象自定义配置 | boolean / object | - | false | - |
| fixedHeader | 是否固定表头 | boolean | - | true | - |
| emptyText | 空数据时显示的文本 | string | - | '暂无数据' | - |
| emptyHeight | 空数据区域高度，单位为 px | number / string | - | 100 | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

**index 属性对象配置说明**

当 `index` 传入对象时，支持以下字段（对应 `TableColumnProps` 类型）：

| 字段名 | 说明 | 类型 | 默认值 |
|--------|------|------|--------|
| align | 对齐方式 | 'left' / 'center' / 'right' | 'left' |
| width | 列宽度，单位 px | number / string | '100rpx' |
| sortable | 是否开启排序 | boolean | false |
| fixed | 是否固定本列 | boolean | false |

### wd-table-col Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| prop | 列对应字段名，用于从 data 数据中取值 | string | - | -（必填） | - |
| label | 列对应字段标题，显示在表头 | string | - | -（必填） | - |
| width | 列宽度，单位 px | number / string | - | 100 | - |
| sortable | 是否开启列排序 | boolean | - | false | - |
| fixed | 是否固定本列，固定后列将吸附在左侧 | boolean | - | false | - |
| align | 列内容对齐方式 | string | left / center / right | left | - |

### wd-table Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|------------|
| default | 默认插槽，用于放置 `wd-table-col` 列定义组件 | `wd-table-col` 组件 |
| empty | 空数据状态时的自定义内容，替换默认的 `emptyText` | 任意内容 |

### wd-table-col Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|------------|
| value | 自定义单元格内容插槽，作用域参数 `{ row, index }` 分别表示当前行数据和行索引 | 任意内容 |

### wd-table Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| sort-method | 列排序事件，点击可排序列的表头时触发 | `{ prop, label, width, sortable, align, sortDirection, fixed }` - 列配置对象 |
| row-click | 行点击事件，点击表格任意单元格时触发 | `{ rowIndex }` - 被点击行的索引 |

### wd-table-col Events

无对外抛出的事件。

## 使用示例

### 基本用法

通过 `data` 属性传入表格数据，配合 `wd-table-col` 定义列的 `prop`（字段名）和 `label`（表头标题）。

```vue
<template>
  <wd-table :data="dataList" :height="400">
    <wd-table-col prop="name" label="姓名" align="center" width="50%"></wd-table-col>
    <wd-table-col prop="grade" label="分数" align="center" width="50%"></wd-table-col>
  </wd-table>
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  const dataList = ref([
    { name: '张三', grade: 88 },
    { name: '李四', grade: 92 },
    { name: '王五', grade: 76 }
  ])
</script>
```

### 固定列

当表格列数较多需要横向滚动时，可通过列的 `fixed` 属性固定关键列。固定列会吸附在表格左侧，滚动时保持可见。多个列同时设置 `fixed` 时，按从左到右的顺序依次固定。

```vue
<template>
  <wd-table :data="dataList" :height="400">
    <wd-table-col prop="name" label="姓名" fixed sortable align="center"></wd-table-col>
    <wd-table-col prop="grade" label="分数" fixed sortable align="center"></wd-table-col>
    <wd-table-col prop="hobby" label="一言以蔽之" sortable :width="160"></wd-table-col>
    <wd-table-col prop="school" label="求学之所" :width="180"></wd-table-col>
    <wd-table-col prop="major" label="专业"></wd-table-col>
    <wd-table-col prop="gender" label="性别"></wd-table-col>
  </wd-table>
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  const dataList = ref([
    {
      name: '关羽',
      grade: 66,
      hobby: '颜良文丑一取首级',
      school: '武汉市卧龙凤雏学院',
      major: '计算机科学与技术专业',
      gender: '男'
    },
    {
      name: '刘备',
      grade: 68,
      hobby: '我的孔明如鱼得水也',
      school: '武汉市卧龙编制学院',
      major: '计算机科学与技术专业',
      gender: '男'
    },
    {
      name: '赵云',
      grade: 91,
      hobby: '子龙子龙世无双',
      school: '武汉市卧龙妇幼保健学院',
      major: '计算机科学与技术专业',
      gender: '男'
    }
  ])
</script>
```

### 显示索引列

通过 `index` 属性开启索引列，默认显示从 1 开始的行号。可通过传入对象形式自定义对齐方式。

```vue
<template>
  <wd-table :data="dataList" :height="400" :index="{ align: 'center' }">
    <wd-table-col prop="name" label="姓名" sortable align="center"></wd-table-col>
    <wd-table-col prop="grade" label="分数" sortable align="center"></wd-table-col>
    <wd-table-col prop="hobby" label="一言以蔽之" sortable :width="160"></wd-table-col>
    <wd-table-col prop="school" label="求学之所" :width="180"></wd-table-col>
    <wd-table-col prop="major" label="专业"></wd-table-col>
    <wd-table-col prop="gender" label="性别"></wd-table-col>
  </wd-table>
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  const dataList = ref([
    {
      name: '关羽',
      grade: 66,
      hobby: '颜良文丑一取首级',
      school: '武汉市卧龙凤雏学院',
      major: '计算机科学与技术专业',
      gender: '男'
    },
    {
      name: '刘备',
      grade: 68,
      hobby: '我的孔明如鱼得水也',
      school: '武汉市卧龙编制学院',
      major: '计算机科学与技术专业',
      gender: '男'
    }
  ])
</script>
```

### 自定义列模板

通过 `wd-table-col` 的 `value` 插槽可以自定义单元格内容，获取当前行数据和行索引进行灵活渲染。

```vue
<template>
  <wd-table :data="dataList" :height="400">
    <wd-table-col prop="name" label="姓名" fixed sortable align="center"></wd-table-col>
    <wd-table-col prop="grade" label="分数" fixed sortable align="center">
      <template #value="{ row }">
        <view class="custom-class">
          <text>{{ row.grade }}</text>
          <text>{{ '同比' }}{{ row.compare }}</text>
        </view>
      </template>
    </wd-table-col>
    <wd-table-col prop="hobby" label="一言以蔽之" sortable :width="160"></wd-table-col>
    <wd-table-col prop="school" label="求学之所" :width="180"></wd-table-col>
    <wd-table-col prop="major" label="专业"></wd-table-col>
    <wd-table-col prop="gender" label="性别"></wd-table-col>
    <wd-table-col prop="graduation" label="学成时间"></wd-table-col>
  </wd-table>
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  const dataList = ref([
    {
      name: '关羽',
      grade: 66,
      compare: '48%',
      hobby: '颜良文丑一取首级',
      school: '武汉市卧龙凤雏学院',
      major: '计算机科学与技术专业',
      gender: '男',
      graduation: '2025年10月01日'
    },
    {
      name: '刘备',
      grade: 68,
      compare: '21%',
      hobby: '我的孔明如鱼得水也',
      school: '武汉市卧龙编制学院',
      major: '计算机科学与技术专业',
      gender: '男',
      graduation: '2025年10月01日'
    }
  ])
</script>

<style lang="scss" scoped>
  .custom-class {
    height: 80rpx;
    width: 220rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
</style>
```

### 无边框 / 无斑马纹 / 不展示表头

通过 `border`、`stripe`、`showHeader` 属性分别控制边框、斑马纹和表头的显示。

```vue
<template>
  <!-- 无边框 -->
  <wd-table :data="dataList" :height="400" :border="false">
    <wd-table-col prop="name" label="姓名" align="center" width="50%"></wd-table-col>
    <wd-table-col prop="grade" label="分数" align="center" width="50%"></wd-table-col>
  </wd-table>

  <!-- 无斑马纹 -->
  <wd-table :data="dataList" :height="400" :stripe="false">
    <wd-table-col prop="name" label="姓名" align="center" width="50%"></wd-table-col>
    <wd-table-col prop="grade" label="分数" align="center" width="50%"></wd-table-col>
  </wd-table>

  <!-- 不展示表头 -->
  <wd-table :data="dataList" :height="400" :show-header="false">
    <wd-table-col prop="name" label="姓名" align="center" width="50%"></wd-table-col>
    <wd-table-col prop="grade" label="分数" align="center" width="50%"></wd-table-col>
  </wd-table>
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  const dataList = ref([
    { name: '张三', grade: 88 },
    { name: '李四', grade: 92 },
    { name: '王五', grade: 76 }
  ])
</script>
```

### 排序与行点击事件

通过 `sortable` 属性开启列排序，点击列头触发 `sort-method` 事件。点击表格任意单元格触发 `row-click` 事件。

```vue
<template>
  <wd-table :data="dataList" :height="400" @sort-method="handleSort" @row-click="handleRowClick">
    <wd-table-col prop="name" label="姓名" align="center" width="50%"></wd-table-col>
    <wd-table-col prop="grade" label="分数" sortable align="center" width="50%"></wd-table-col>
  </wd-table>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import type { TableColumn } from '@/uni_modules/wot-ui-plus/components/wd-table-col/types'

  const dataList = ref([
    { name: '张三', grade: 88 },
    { name: '李四', grade: 92 },
    { name: '王五', grade: 76 }
  ])

  function handleSort(column: TableColumn) {
    console.log('排序列：', column.prop, '排序方向：', column.sortDirection)
    // sortDirection: 0 为未排序, 1 为升序, -1 为降序
    dataList.value = dataList.value.reverse()
  }

  function handleRowClick({ rowIndex }: any) {
    console.log('点击行索引：', rowIndex)
  }
</script>
```

### 不固定表头结合分页器

通过设置 `fixed-header="false"` 切换为非固定表头模式，此时表头和表体共用一个 `scroll-view`，适合配合分页器使用。

```vue
<template>
  <wd-table :data="paginationData" :fixed-header="false">
    <wd-table-col prop="name" label="姓名" fixed align="center"></wd-table-col>
    <wd-table-col prop="grade" label="分数" fixed align="center"></wd-table-col>
    <wd-table-col prop="hobby" label="一言以蔽之" :width="160"></wd-table-col>
    <wd-table-col prop="school" label="求学之所" :width="180"></wd-table-col>
    <wd-table-col prop="major" label="专业"></wd-table-col>
    <wd-table-col prop="gender" label="性别"></wd-table-col>
  </wd-table>
  <wd-pagination custom-style="border: 1px solid #ececec;border-top:none" v-model="page" :total="total"></wd-pagination>
</template>

<script setup lang="ts">
  import { ref, computed } from 'vue'

  const page = ref(1)
  const pageSize = ref(10)

  const fullDataList = ref([
    { name: '关羽', grade: 66, hobby: '颜良文丑一取首级', school: '武汉市卧龙凤雏学院', major: '计算机科学与技术专业', gender: '男' },
    { name: '刘备', grade: 68, hobby: '我的孔明如鱼得水也', school: '武汉市卧龙编制学院', major: '计算机科学与技术专业', gender: '男' },
    { name: '赵云', grade: 91, hobby: '子龙子龙世无双', school: '武汉市卧龙妇幼保健学院', major: '计算机科学与技术专业', gender: '男' },
    { name: '孔明', grade: 99, hobby: '兴汉讨贼克复中原', school: '武汉市卧龙卧龙学院', major: '计算机科学与技术专业', gender: '男' }
  ])

  const total = ref(fullDataList.value.length)

  const paginationData = computed(() => {
    return fullDataList.value.slice((page.value - 1) * pageSize.value, page.value * pageSize.value)
  })
</script>
```

## 注意事项

1. **数据必填**：`wd-table` 的 `data` 属性为必填项，传入数组类型数据，数组每项为包含各列字段名的对象。

2. **列定义必须使用 wd-table-col**：列定义必须使用 `wd-table-col` 组件作为 `wd-table` 的子组件，每个 `wd-table-col` 需要设置 `prop`（对应数据字段名）和 `label`（表头标题）。

3. **固定列样式**：固定列通过 `position: sticky` 实现，多列固定时自动计算每列的 `left` 偏移值。最后一个固定列在滚动时会显示阴影分隔效果。

4. **排序状态互斥**：当多列设置 `sortable` 时，每次只能有一个列处于排序状态。切换排序列时，其他列的排序状态会重置为 0（未排序）。

5. **表头固定模式**：`fixedHeader` 为 `true` 时（默认），表头和表体分别使用独立的 `scroll-view` 并通过同步 `scrollLeft` 实现联动滚动。为 `false` 时表头和表体共用一个 `scroll-view`。

6. **宽度支持**：列的 `width` 属性支持纯数字（单位 px）、带单位的字符串（如 `'50%'`、`'160px'`）和 `rpx` 单位值。

7. **超出省略规则**：`ellipsis` 为 `true` 时（默认），单元格内容超出 2 行会自动截断并显示省略号（使用 CSS 多行省略）。

8. **空数据展示**：当 `data` 数组为空时，表格会显示 `emptyText` 文本或 `empty` 插槽内容。空数据区域高度可通过 `emptyHeight` 属性控制，默认为 100px。

9. **行高自定义**：默认行高为 40px，可通过 `rowHeight` 属性自定义。自定义内容插槽时需注意调整内容高度与行高保持一致。

10. **索引列配置**：`index` 属性设为 `true` 时使用默认配置（左对齐、100rpx 宽度）。如需自定义，传入包含 `align`、`width`、`sortable`、`fixed` 属性的对象。
