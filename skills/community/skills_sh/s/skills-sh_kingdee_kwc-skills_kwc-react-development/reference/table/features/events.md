# 事件监听

[返回目录](../index.md)

## 功能说明

通过 `onChange` 事件统一监听分页、排序、筛选变化。

## 示例代码（React）

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

const pagination = {
  pageSize: 10,
  total: 100
};

export default () => {
  const handleChange = (event) => {
    const { sorting, columnFilters, changeType, pagination } = event.detail || {};
    console.log({ sorting, columnFilters, changeType, pagination });
  };

  return (
    <SlTable
      rowKey="id"
      columns={columns}
      dataSource={dataSource}
      pagination={pagination}
      onChange={handleChange}
    />
  );
};
```

---

## 注意事项

1. **何时使用**：当用户希望使用受控模式下的分页、过滤、筛选时使用
2. **onChange 已映射**：Table 的 React wrapper 已映射 `change` 事件为 `onChange`，可直接在 JSX 使用

[返回目录](../index.md)
