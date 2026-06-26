# 动态数据更新

[返回目录](../index.md)

## 功能说明

Table 组件支持动态更新数据源，包括添加数据、删除数据、清空并重新加载等操作。在 React 中，使用 `useState` 管理数据，通过创建新数组触发组件重渲染。

## 示例代码（React）

### 添加数据

```jsx
import React, { useState, useCallback } from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const columns = [
  { title: '姓名', dataIndex: 'name', width: 150 },
  { title: '年龄', dataIndex: 'age', width: 100 },
  { title: '部门', dataIndex: 'department' }
];

let counter = 3;

export default () => {
  const [dataSource, setDataSource] = useState([
    { id: '1', name: '张三', age: 28, department: '研发部' },
    { id: '2', name: '李四', age: 32, department: '产品部' }
  ]);

  const handleAdd = useCallback(() => {
    const newItem = {
      id: String(counter),
      name: `新员工${counter}`,
      age: 20 + Math.floor(Math.random() * 20),
      department: ['研发部', '产品部', '设计部'][Math.floor(Math.random() * 3)]
    };
    setDataSource(prev => [...prev, newItem]);
    counter++;
  }, []);

  return (
    <div>
      <button onClick={handleAdd}>添加一行</button>
      <span>共 {dataSource.length} 条数据</span>
      <SlTable rowKey="id" columns={columns} dataSource={dataSource} />
    </div>
  );
};
```

---

### 删除数据

```jsx
import React, { useState, useCallback, useMemo } from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';
import { generateCustomSlot } from "@kdcloudjs/shoelace/dist/components/table/utils.js";

const columns = [
  { title: '姓名', dataIndex: 'name', width: 150 },
  { title: '邮箱', dataIndex: 'email', width: 250 },
  { title: '操作', dataIndex: 'action', width: 100, slot: true }
];

export default () => {
  const [dataSource, setDataSource] = useState([
    { id: '1', name: '张三', email: 'zhangsan@example.com' },
    { id: '2', name: '李四', email: 'lisi@example.com' }
  ]);

  const handleDelete = useCallback((id) => {
    setDataSource(prev => prev.filter(item => item.id !== id));
  }, []);

  const cellSlots = useMemo(() => {
    return generateCustomSlot(
      'id',
      dataSource,
      [
        {
          type: 'customCell',
          columnId: 'action',
          callback: (props) => (
            <div key={props.slotName} slot={props.slotName}>
              <button onClick={() => handleDelete(props.rowInfo.id)}>删除</button>
            </div>
          )
        }
      ]
    );
  }, [dataSource, handleDelete]);

  return (
    <SlTable rowKey="id" columns={columns} dataSource={dataSource}>
      {cellSlots}
    </SlTable>
  );
};
```

---

## 注意事项

1. **不可变更新**：React 中更新数据需用展开运算符创建新数组（`[...prev, newItem]`），触发重渲染
2. **rowKey 唯一性**：添加新数据时确保 `rowKey` 字段值唯一

