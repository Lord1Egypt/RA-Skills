# 树形数据展示

[返回目录](../index.md)

## 功能说明

表格支持树形数据的展示，当数据中有 children 字段时会自动展示为树形表格，如果需要使用其他字段可以用 tree.childrenRecordName 进行配置。另外可以通过设置 tree.expandColumnKey 以控制树形表的展开列。

## 示例代码（React）

```jsx
import React, { useState } from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

export default () => {
  const [dataSource, setDataSource] = useState([
    { key: '1', seq: '1', age: 25, email: 'zhangsan@example.com', children: [
      {
        key: '4', seq: '1-1', age: 25, email: 'zhangsan@example.com',
        children:[
          {
            key: '5', seq: '1-1-1', age: 25, email: 'zhangsan@example.com' 
          }
        ]
      },
      {key: '6', seq: '1-2', age: 25, email: 'zhangsan@example.com',}
    ]},
    { key: '2', seq: '2', age: 30, email: 'lisi@example.com',  },
    { key: '3', seq: '3', age: 28, email: 'wangwu@example.com', children:[
      {
        key: '7', seq: '3-1', age: 25, email: 'zhangsan@example.com',
      }
    ]},
  ]);

  const columns = [
    { dataIndex: 'seq'},
    { dataIndex: 'age'},
    { dataIndex: 'email'}
  ];

  const tree = {
    childrenRecordName: 'children',
    expandColumnKey: 'seq'
  }

  return (
    <SlTable
      rowKey="key"
      columns={columns}
      dataSource={dataSource}
      tree={tree}
    />
  );
};
```

---

## 注意事项

1. **rowKey 必须唯一**：`rowKey` 指定的字段在数据中必须唯一，否则会导致树形表格功能异常