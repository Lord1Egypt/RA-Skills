# 列筛选

[返回目录](../index.md)

## 功能说明

通过列配置 `filters`、`onFilter`、`filterMultiple` 开启筛选能力。

## 示例代码（React）

```jsx
import React from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const columns = [
  {
    dataIndex: 'name',
    title: '姓名',
    width: 160,
    filters: [
      { text: 'Alice', value: 'Alice' },
      { text: 'Bob', value: 'Bob' }
    ],
    onFilter: (value, record) => record.name.includes(value),
    filterMultiple: true
  },
  { dataIndex: 'email', title: '邮箱' }
];

const dataSource = [
  { id: '1', name: 'Alice Smith', email: 'alice@example.com' },
  { id: '2', name: 'Bob Johnson', email: 'bob@example.com' }
];

export default () => (
  <SlTable rowKey="id" columns={columns} dataSource={dataSource} />
);
```

---

## 注意事项

1. **filters 和 onFilter 配合使用**：必须同时配置 `filters` 和 `onFilter` 才能使筛选功能生效
2. **onFilter 返回布尔值**：`onFilter` 函数返回 `true` 表示该行数据符合筛选条件
3. **多选筛选逻辑**：多选模式下，只要满足任一筛选条件即显示该行（OR 逻辑）

