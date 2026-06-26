# 固定列

[返回目录](../index.md)

## 功能说明

通过列配置 `fixed: 'left' | 'right'` 并配合 `tableScroll.x` 实现固定列。

## 示例代码（React）

```jsx
import React from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const tableScroll = { x: 900 };

const columns = [
  { dataIndex: 'id', title: '#', width: 48, fixed: 'left' },
  { dataIndex: 'name', title: '姓名', width: 160, fixed: 'left' },
  { dataIndex: 'gender', title: '性别', width: 140 },
  { dataIndex: 'age', title: '年龄', width: 120 },
  { dataIndex: 'email', title: '邮箱', width: 280 },
  { dataIndex: 'position', title: '岗位', width: 180, fixed: 'right' }
];

const dataSource = [
  {
    id: '1',
    name: 'Alice',
    gender: 'Female',
    age: 28,
    email: 'alice@example.com',
    position: 'SE'
  }
];

export default () => (
  <SlTable
    rowKey="id"
    columns={columns}
    dataSource={dataSource}
    tableScroll={tableScroll}
  />
);
```

