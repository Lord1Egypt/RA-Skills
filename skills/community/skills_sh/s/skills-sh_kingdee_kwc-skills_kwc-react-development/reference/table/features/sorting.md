# 列排序

[返回目录](../index.md)

## 功能说明

通过列配置 `sorter` 和 `defaultSortOrder` 开启本地排序。

## 示例代码（React）

```jsx
import React from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const columns = [
  {
    dataIndex: 'name',
    title: '姓名',
    sorter: (a, b) => a.name.localeCompare(b.name),
    defaultSortOrder: 'asc'
  },
  { dataIndex: 'age', title: '年龄', sorter: (a, b) => a.age - b.age }
];

const dataSource = [
  { id: '1', name: 'Bob', age: 32 },
  { id: '2', name: 'Alice', age: 28 }
];

export default () => (
  <SlTable rowKey="id" columns={columns} dataSource={dataSource} />
);
```

---

## 注意事项

1. **sorter 函数返回值**：返回负数表示 a 在 b 前面，返回正数表示 a 在 b 后面，返回 0 表示相等
2. **单列排序**：当前实现同一时间只支持单列排序，点击其他列会取消之前的排序
3. **日期排序**：日期类型需要转换为 Date 对象或时间戳进行比较

