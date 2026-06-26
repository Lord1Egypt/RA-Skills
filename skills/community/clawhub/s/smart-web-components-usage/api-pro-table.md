# HtProTable 完整 API 参考

## HtProTableProps（继承 antd TableProps）

### 数据请求

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `request` | 分页数据请求方法 | `(params) => Promise<{ records: TData[], total: number }>` | - |
| `params` | 额外查询参数，变更自动触发重新请求 | `object` | - |
| `beforeSearch` | 查询前参数处理，返回 `undefined` 可拦截请求 | `(params) => params \| undefined` | - |
| `postData` | 响应数据后处理 | `(data: TData[]) => TData[]` | - |
| `onDataSourceChange` | 数据源变更回调 | `(data: TData[]) => void` | - |
| `dateFormatter` | 日期格式化方式 | `'string' \| 'number' \| false` | `'string'` |

### 搜索表单

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `columns` | 列配置（含搜索表单配置） | `HtProColumns[]` | `[]` |
| `searchConfig` | 搜索表单配置，`false` 隐藏搜索栏 | `SearchConfig \| false` | `{ span: 6, columnCount: 4, mode: 'static' }` |
| `formProps` | 表单属性透传 | `FormProps` | - |
| `formRef` | 表单实例引用 | `MutableRefObject<FormInstance>` | - |
| `onSubmit` | 查询提交回调 | `(params) => void` | - |
| `onReset` | 重置回调 | `() => void` | - |

### 行选择

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `rowSelection` | 行选择配置，`true` 开启默认多选 | `TableRowSelection \| true` | - |
| `defaultSelectedRows` | 默认选中行数据 | `TData[]` | - |
| `memoizedSelected` | 分页记忆选中（翻页后保留之前选中项） | `boolean` | `false` |
| `selectMaxCount` | 最大选择数量 | `number` | `2000` |
| `renderSelected` | 选中项展示，`true` 使用默认渲染 | `boolean \| ((rows) => ReactNode)` | `false` |
| `renderSelectedField` | 默认选中项展示字段 | `React.Key` | - |

### 布局与样式

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `containerHeight` | 容器高度，设置后自动固定表头 | `string \| number` | `'auto'` |
| `ghost` | 幽灵模式（透明背景） | `boolean` | `false` |
| `layout` | `'split'` 搜索和表格分开，`'compact'` 合并 | `'split' \| 'compact'` | `'split'` |
| `sequenceNumber` | 序号列，`false` 不显示，`true` 默认，对象自定义 | `boolean \| SequenceNumberColumnConfig` | `true` |
| `renderEmptyContent` | 空值统一默认显示 | `string` | `'-'` |

### 工具栏

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `options` | 工具栏配置 | `{ setting?: boolean \| { cacheKey }, size?: boolean }` | `{ setting: true, size: false }` |
| `renderToolbarLeft` | 左侧工具栏 | `(selectedRowKeys, selectedRows) => ReactNode` | - |
| `renderToolbarRight` | 右侧工具栏 | `(selectedRowKeys, selectedRows) => ReactNode` | - |

### 控制引用

| 参数 | 说明 | 类型 |
|------|------|------|
| `actionRef` | 操作方法引用 | `MutableRefObject<ActionType>` |
| `tableRef` | 表格实例引用 | `MutableRefObject<TableInstance>` |

```ts
// ActionType 方法
actionRef.current.reload(resetPageIndex?)   // 刷新，可重置到第一页
actionRef.current.reset()                   // 重置搜索表单并刷新
actionRef.current.getLastParams()           // 获取最后一次请求参数

// TableInstance 方法
tableRef.current.getSelectedRows()          // 获取选中行数据
tableRef.current.getSelectedRowKeys()       // 获取选中行 keys
tableRef.current.setSelectedRowKeys(keys)   // 设置选中行
tableRef.current.deleteRowKeys(keys)        // 删除指定选中项
tableRef.current.cleanSelected()            // 清空所有选中
```

### 高级功能

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `renderTable` | 自定义渲染整个表格 | `(props, getRowKey, defaultDom) => ReactNode` | - |
| `resizableColumns` | 开启拖动调整列宽（实验性） | `boolean` | `false` |

## HtProColumns（继承 antd ColumnType）

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `valueType` | 搜索表单项类型 | 见下方 valueType 列表 | `'input'` |
| `search` | 是否为搜索项 | `boolean \| { transform: fn }` | `false` |
| `searchOrder` | 搜索项排序（数值越小越靠前） | `number` | - |
| `fieldProps` | 表单项属性透传 | 对应 valueType 组件的 Props | - |
| `colProps` | 搜索表单 Col 配置 | `ColProps` | - |
| `formItemProps` | 搜索表单 Form.Item 配置 | `FormItemProps` | - |
| `renderFormItem` | 自定义渲染搜索项 | `(form, fieldProps) => ReactNode` | - |
| `dictType` | 字典类型（valueType='selectDict' 时） | `string` | - |
| `dictCode` | 字典编码（valueType='selectDict' 时） | `string` | - |
| `ellipsis` | 超出省略行数 | `boolean \| 1 \| 2 \| 3` | `false` |
| `hidden` | 是否隐藏该列 | `boolean` | `false` |
| `renderEmptyContent` | 空值显示，覆盖表格级配置 | `string` | `'-'` |

## valueType 完整列表

| valueType | 说明 | valueType | 说明 |
|-----------|------|-----------|------|
| `input` | 输入框 | `select` | 下拉选择 |
| `baseInput` | 基础输入框 | `selectDict` | 字典选择 |
| `textarea` | 文本域 | `digit` | 数字输入 |
| `date` | 日期选择 | `digitRange` | 数字范围 |
| `dateWeek` | 周选择 | `switch` | 开关 |
| `dateMonth` | 月选择 | `cascader` | 级联选择 |
| `dateQuarter` | 季度选择 | `time` | 时间选择 |
| `dateYear` | 年选择 | `timeRange` | 时间范围 |
| `dateRange` | 日期范围 | `dateTimeRange` | 日期时间范围 |
| `dateTime` | 日期时间 | | |

## HtDragSortTable（拖拽排序扩展）

继承 HtProTableProps，额外属性：

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `dragSortKey` | 拖拽列 key，该列显示拖拽把手 | `string` | - |
| `dragIcon` | 自定义拖拽图标 | `ReactElement` | `<HolderOutlined />` |
| `onDragSortEnd` | 拖动完成回调 | `(newData: T[]) => Promise<void> \| void` | - |
