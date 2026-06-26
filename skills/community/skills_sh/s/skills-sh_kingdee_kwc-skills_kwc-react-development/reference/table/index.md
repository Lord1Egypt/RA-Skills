# Table 数据表格组件 Skill

## 组件概述

`SlTable` 是一个功能丰富的数据表格组件，用于数据收集展示、分析整理和操作处理。基于 `@tanstack/lit-table` 构建，支持在 KWC React 框架中使用。组件提供排序、筛选、分页、行选择、列固定、行展开、虚拟滚动、列宽调整等完整的表格功能。

## 功能列表

| 功能 | 说明 | 详细文档 |
|------|------|----------|
| 基础用法 | columns、dataSource、rowKey、边框、隐藏表头 | [basic-usage.md](./features/basic-usage.md) |
| 加载状态与空数据 | loading 加载中、空数据展示、自定义空状态 | [loading-empty.md](./features/loading-empty.md) |
| 行选择 | checkbox 多选、radio 单选、默认选中、禁用、回调等 | [row-selection.md](./features/row-selection.md) |
| 列排序 | sorter 排序函数、默认排序方向、排序状态监听 | [sorting.md](./features/sorting.md) |
| 列筛选 | filters 筛选项、多选/单选筛选、默认筛选值 | [filtering.md](./features/filtering.md) |
| 受控排序筛选 | 受控排序/筛选、服务端数据联动 | [controlled-sort-filter.md](./features/controlled-sort-filter.md) |
| 固定列 | 左侧固定、右侧固定、两侧同时固定 | [fixed-column.md](./features/fixed-column.md) |
| 列宽调整 | 拖拽调整列宽、禁止某列调整、调整回调 | [column-resizing.md](./features/column-resizing.md) |
| 自定义单元格 | slot 自定义渲染、generateCustomSlot | [custom-cell.md](./features/custom-cell.md) |
| 可编辑单元格 | 点击单元格进入编辑态，失焦后保存 | [editable-cell.md](./features/editable-cell.md) |
| 文本省略与对齐 | ellipsis 省略、align 对齐、列样式类名 | [ellipsis-align.md](./features/ellipsis-align.md) |
| 行展开 | 展开行、点击行展开、指定可展开行、默认展开 | [row-expand.md](./features/row-expand.md) |
| 嵌套子表格 | 在展开行内渲染子表格 | [nested-table.md](./features/nested-table.md) |
| 行拖拽 | 拖拽排序并监听 slRowReorder | [row-drag.md](./features/row-drag.md) |
| 虚拟滚动 | 大数据量虚拟滚动、自定义行高 | [virtualized.md](./features/virtualized.md) |
| 分页 | 分页配置、分页位置、每页条数、分页回调 | [pagination.md](./features/pagination.md) |
| 事件监听 | change 事件、changeType 区分、事件联动，包含排序、筛选、分页 | [events.md](./features/events.md) |
| 动态数据更新 | 添加数据、删除数据、清空重载 | [dynamic-data.md](./features/dynamic-data.md) |
| RTL 方向 | 从右到左布局、RTL + 固定列 | [rtl.md](./features/rtl.md) |
| 行/单元格属性 | slRow、slHeaderRow、slCell、slHeaderCell | [row-cell-props.md](./features/row-cell-props.md) |
| 树形数据展示 | 展示树形数据 childrenRecordName indentSize| [tree-table.md](./features/tree-table.md) |
| 表头分组 | columns children 多级表头、嵌套分组 | [header-group.md](./features/header-group.md) |
| 总结栏 | summary 页尾汇总行、自定义表尾内容 | [summary.md](./features/summary.md) |

## 核心约束

### 必须遵守的规则

1. **rowKey 必须设置**
   - 每行数据必须有唯一标识字段，通过 `rowKey` 属性指定
   - 默认值为 `'key'`，实际使用时建议显式指定如 `'id'`

2. **columns 配置规范**
   - `dataIndex` 为列的唯一标识，必须与数据源中的字段名对应
   - `title` 为表头显示文字
   - 建议为每列设置 `width`，未设置宽度的列会自动分配剩余空间

3. **React 框架规范**
   - 导入必须从 `@kdcloudjs/shoelace/dist/react/table/index.js` 默认导入
   - 自定义单元格渲染使用 `generateCustomSlot` 工具函数，从 `@kdcloudjs/shoelace/dist/components/table/utils.js` 导入

4. **组件标签名**
   - 标签名为 `SlTable`（React 包装组件）

5. **自定义 Slot 命名规范**
   - 自定义单元格 slot 名称格式：`custom-cell-{dataIndex}-{rowKeyValue}`
   - 展开行 slot 名称格式：`custom-row-{rowKeyValue}`

## 快速开始

### 组件导入

```jsx
// 默认导入 React 包装组件
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

// 自定义单元格渲染工具
import { generateCustomSlot } from "@kdcloudjs/shoelace/dist/components/table/utils.js";
```

### 最简示例

```jsx
import React from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const columns = [
  { title: '姓名', dataIndex: 'name', width: 150 },
  { title: '年龄', dataIndex: 'age', width: 100 },
  { title: '地址', dataIndex: 'address' }
];

const dataSource = [
  { id: '1', name: '张三', age: 32, address: '北京市朝阳区' },
  { id: '2', name: '李四', age: 28, address: '上海市浦东新区' },
  { id: '3', name: '王五', age: 35, address: '广州市天河区' }
];

export default () => (
  <SlTable rowKey="id" columns={columns} dataSource={dataSource} />
);
```

## API 概览

### Table 属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `rowKey` | 必填，行唯一标识字段名（区分大小写） | `string` | `'key'` |
| `columns` | 列配置数组，至少包含 `dataIndex` 与 `title` | `ColumnProps[]` | `[]` |
| `dataSource` | 表格数据源 | `TData[]` | `[]` |
| `loading` | 是否显示加载状态 | `boolean` | `false` |
| `showHeader` | 是否显示表头 | `boolean` | `true` |
| `bordered` | 是否显示边框 | `boolean` | `false` |
| `size` | 表格尺寸 | `'small' \| 'middle' \| 'default'` | `'default'` |
| `direction` | 表格方向 | `'ltr' \| 'rtl'` | `'ltr'` |
| `rowSelection` | 行选择配置 | `RowSelection` | - |
| `tableScroll` | 滚动配置 | `TableScroll` | - |
| `expandProps` | 展开行配置 | `ExpandProps` | - |
| `pagination` | 分页配置 | `Pagination` | - |
| `tree` | 树形表格配置 | `TreeConfig` | - |
| `onChange` | 分页/排序/筛选变更回调 | `(e: CustomEvent) => void` | - |
| `slRow` | 设置行属性（注入到 `tr`） | `(record: TData, index: number) => object` | - |
| `slHeaderRow` | 设置表头行属性（注入到 `tr`） | `(columns: ColumnProps[], index: number) => object` | - |
| `virtualized` | 虚拟滚动配置 | `boolean \| Virtualized` | `false` |
| `enableColumnResizing` | 是否开启列宽拖拽 | `boolean` | `false` |
| `slColumnResize` | 列宽调整回调 | `(size: Record<string, number>) => void` | - |
| `rowDrag` | 是否开启行拖拽 | `boolean` | `false` |
| `slRowReorder` | 行拖拽排序回调 | `(e: CustomEvent) => void` | - |
| `summary` | 总结栏配置，用于在表格底部展示汇总行 | `SummaryObject[]` | - |

### Column 列配置

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `title` | 列标题（必填） | `string` | - |
| `dataIndex` | 列字段名（必填且唯一） | `string` | - |
| `children` | 表头合并时用于子列的设置 | `Column[]` | - |
| `align` | 对齐方式 | `'left' \| 'right' \| 'center'` | `'left'` |
| `className` | 列样式类名 | `string` | - |
| `width` | 列宽 | `number` | - |
| `fixed` | 固定列位置 | `false \| 'left' \| 'right'` | `false` |
| `ellipsis` | 是否省略超长文本 | `boolean` | `false` |
| `slot` | 是否启用 slot 自定义渲染 | `boolean` | `false` |
| `headExtraSlot` | 是否启用表头插槽 | `boolean` | `false` |
| `colSpan` | 表头列合并属性 | `number` | - |
| `defaultSortOrder` | 默认排序状态 | `'asc' \| 'desc'` | - |
| `sorter` | 排序函数（服务端可设为 `() => null`） | `(a, b) => number` | - |
| `sortOrder` | 受控排序状态 | `'asc' \| 'desc'` | - |
| `onFilter` | 本地筛选函数 | `(value, row) => boolean` | - |
| `filters` | 筛选项 | `{ text: string; value: any }[]` | - |
| `defaultFilters` | 默认筛选值 | `any[]` | - |
| `filteredValue` | 受控筛选值 | `any[]` | - |
| `filterMultiple` | 是否多选筛选 | `boolean` | `true` |
| `filterDropdownProps` | 筛选下拉配置 | `object` | - |
| `onFilterDropdownVisibleChange` | 筛选下拉显隐回调 | `(visible: boolean) => void` | - |
| `enableResizing` | 是否允许调整该列宽度 | `boolean` | 继承全局 |
| `slCell` | 设置单元格属性（注入到 `td`） | `(record: TData, rowIndex: number) => object` | - |
| `slHeaderCell` | 设置表头单元格属性（注入到 `th`） | `(columns: ColumnProps[], columnIndex: number) => object` | - |

### RowSelection 行选择配置

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `type` | 选择类型 | `'checkbox' \| 'radio'` | `'checkbox'` |
| `hidden` | 是否隐藏选择列 | `boolean` | `false` |
| `width` | 选择列宽度 | `number` | - |
| `className` | 选择列样式类名 | `string` | - |
| `disabled` | 是否禁用表头选择框 | `boolean` | `false` |
| `defaultSelectedRowKeys` | 默认选中的行 key 数组 | `any[]` | - |
| `onChange` | 选择变化回调 | `(selectedRowKeys, selectedRows) => void` | - |
| `onSelect` | 点击行选择框回调 | `(record, selected, selectedRows, event) => void` | - |
| `onSelectAll` | 点击全选框回调 | `(selected, selectedRows) => void` | - |
| `getCheckboxProps` | 自定义选择框属性 | `(record) => Record<string, unknown>` | - |

### ExpandProps 展开行配置

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `rowExpandable` | 是否开启行展开（优先级高于 `expandableRowKeys`） | `boolean` | `false` |
| `expandableRowKeys` | 指定可展开的行 key | `any[]` | - |
| `expandRowByClick` | 是否支持点击行展开 | `boolean` | `false` |
| `defaultExpandedRowKeys` | 默认展开行 key 数组 | `any[]` | - |

### TableScroll 滚动配置

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `x` | 横向滚动宽度（像素值或百分比） | `number \| string` | - |
| `y` | 纵向滚动高度（像素值） | `number \| string` | - |
| `scrollToFirstRowOnChange` | 分页/排序/筛选变化后是否滚动到顶部 | `boolean` | `false` |

### Virtualized 虚拟滚动配置

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `itemHeight` | 行高 | `number` | `32` |
| `onScroll` | 滚动回调 | `(e: CustomEvent) => void` | - |

### 主要事件

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| `change` | 分页、排序、筛选变化时触发 | `{ sorting, columnFilters, changeType, pagination? }` |
| `row-reorder` | 行拖拽排序后触发 | `{ fromIndex, toIndex, newRows, rows }` |
| `column-resize` | 列宽变化后触发 | `Record<string, number>` |

### Pagination 分页配置

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `position` | 分页位置 | `'topStart' \| 'topCenter' \| 'topEnd' \| 'bottomStart' \| 'bottomCenter' \| 'bottomEnd'` | `'bottomStart'` |
| `total` | 数据总条数 | `number` | - |
| `pageSize` | 每页条数 | `number` | `20` |
| `currentPage` | 当前页码（受控） | `number` | - |
| `defaultCurrentPage` | 默认当前页码 | `number` | `1` |
| `pageSizeOpts` | 每页条数选项 | `number[]` | `[10, 20, 50, 100]` |
| `simpleMode` | 是否简洁模式 | `boolean` | `false` |
| `disabled` | 是否禁用 | `boolean` | `false` |
| `className` | 分页样式类名 | `string` | - |
| `sl-page-change` | 分页变化回调（事件） | `(event: CustomEvent) => void` | - |

### Tree 树形表格配置

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `childrenRecordName` | 树形表格 `dataSource` 中每行元素中表示子级数据的字段 | `string` | `children` |
| `indentSize` | 	树形结构 `TableCell` 的缩进大小 | `number` | `16` |

### SummaryObject 总结栏配置

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `rowIndex` | 总结行的索引，用于标识该行在表尾中的位置 | `number` | - |
| `cells` | 传递给每个单元格的属性（如 style、onclick 等），key 为列的 `dataIndex` | `Record<string, unknown>[]` | - |

### Slots（插槽）

| Slot | 说明 |
|------|------|
| `table-empty` | 空数据时显示的内容 |
| `custom-cell-{dataIndex}-{rowKey}` | 自定义单元格内容 |
| `custom-row-{rowKey}` | 展开行内容 |
| `custom-tfoot-cell-{rowIndex}-{dataIndex}` | 总结栏单元格内容 |
| `custom-tfoot` | 自定义页尾内容（summary 传空数组时渲染） |
| `custon-head-extra-{columnID}` | 表头插槽 |

### CSS Parts

| Part 名称 | 说明 |
|-----------|------|
| `table-wrapper` | 表格外层容器 |
| `table-container` | 表格内层容器 |
| `table-head` | 表头区域 |
| `table-head-row` | 表头行容器 |
| `table-head-cell` | 表头单元格容器 |
| `table-body` | 表体区域 |
| `table-body-row` | 表体行容器 |
| `table-body-cell` | 表体单元格容器 |
| `table-foot` | 表尾区域 |
| `table-foot-row` | 表尾行容器 |
| `table-foot-cell` | 表尾单元格容器 |

### CSS 设计变量

| Token 名称 | 说明 |
|-----------|------|
| `--sl-table-cell-border` | 单元格边框颜色 |
| `--sl-table-cell-border-width` | 单元格边框宽度 |
| `--sl-table-cell-color` | 单元格文字颜色 |
| `--sl-table-cell-background` | 单元格背景色 |
| `--sl-table-cell-line-height` | 单元格行高 |
| `--sl-table-cell-padding` | 单元格内边距 |
| `--sl-table-header-background` | 表头背景色 |
| `--sl-table-header-line-height` | 表头行高 |
| `--sl-table-column-header-padding` | 表头单元格内边距 |
| `--sl-table-font-size` | 表格字体大小 |
| `--sl-table-row-background-hover` | 行悬停背景色 |
| `--sl-table-row-background-active` | 选中行背景色 |
| `--sl-table-icon-color-default` | 排序图标默认颜色 |
| `--sl-table-icon-color-active` | 排序图标激活颜色 |
| `--sl-table-default-text-color` | 空数据文字颜色 |
| `--sl-table-default-text-margin-vertical` | 空数据区域内边距 |
| `--sl-table-mask` | 加载遮罩背景色 |
| `--sl-c-table-direction` | 表格方向（ltr/rtl） |
| `--sl-table-expand-row-background` | 展开行背景色 |
| `--sl-table-cell-border-focus` | 单元格聚焦边框色 |
| `--sl-table-drag-handle-width` | 列宽拖拽热区宽度 |

## 使用建议

1. **rowKey 设置**：务必为 `rowKey` 指定一个在数据中唯一的字段名（如 `'id'`），这是行选择、展开、排序等功能正常工作的基础
2. **列宽设置**：建议为每列设置 `width`，可避免列宽分配不合理的问题
3. **大数据量**：数据量超过 100 条时，建议开启 `virtualized` 虚拟滚动或配合 `pagination` 分页使用
4. **自定义单元格**：通过 `slot: true` 配合 `generateCustomSlot` 工具函数实现自定义渲染
5. **服务端数据**：通过监听 `onChange` 事件，结合 `sortOrder`、`filteredValue` 受控属性实现服务端排序/筛选
