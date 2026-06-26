# 基础用法

[返回目录](../index.md)

## 功能说明

用于演示 `SlTable` 的最小可用配置：`rowKey`、`columns`、`dataSource`。

## 示例代码（React）

```jsx
import React from 'react';
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const columns = [
    { dataIndex: 'name', title: '姓名', width: 160 },
    { dataIndex: 'dept', title: '部门', width: 140 },
    { dataIndex: 'email', title: '邮箱' }
];

const dataSource = [
    { id: '1', name: 'Alice Smith', dept: '研发', email: 'alice@example.com' },
    { id: '2', name: 'Bob Johnson', dept: '产品', email: 'bob@example.com' }
];

export default () => (
    <SlTable rowKey="id" columns={columns} dataSource={dataSource} />
);
```

---

## 注意事项

1. **rowKey 必须唯一**：`rowKey` 指定的字段在数据中必须唯一，否则会导致行选择、行展开等功能异常
2. **columns 必须包含 dataIndex**：每列配置必须指定 `dataIndex`，且需与数据源中的字段名对应
3. **建议设置列宽**：为每列设置 `width` 可避免列宽分配不合理的问题，未设置宽度的列会自动分配剩余空间

