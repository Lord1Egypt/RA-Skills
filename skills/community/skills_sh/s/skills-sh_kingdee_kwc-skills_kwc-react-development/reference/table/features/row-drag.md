# 行拖拽

[返回目录](../index.md)

## 功能说明

通过 `rowDrag` 开启拖拽排序，监听 `slRowReorder` 更新数据顺序。

## 示例代码（React）

```jsx
import React, { useState } from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

export default () => {
  const [dataSource, setDataSource] = useState([
    { id: '1', name: 'Alice Smith', position: 'SE' },
    { id: '2', name: 'Bob Johnson', position: 'PM' },
    { id: '3', name: 'Carol White', position: 'UX' }
  ]);

  const columns = [
    { dataIndex: 'name', title: '姓名', width: 160 },
    { dataIndex: 'position', title: '岗位' }
  ];

  const handleRowReorder = (detail) => {
    console.log(detail)
  };

  return (
    <SlTable
      rowKey="id"
      rowDrag={true}
      columns={columns}
      dataSource={dataSource}
      slRowReorder={handleRowReorder}
    />
  );
};
```

---

## 注意事项

1. **rowDrag 属性**：必须设置为 `true` 才能开启行拖拽功能
2. **slRowReorder 回调**：拖拽完成后触发，参数包含 fromIndex、toIndex、newRows、rows
3. **数据更新**：需要在回调中手动更新 dataSource 以反映新的顺序
