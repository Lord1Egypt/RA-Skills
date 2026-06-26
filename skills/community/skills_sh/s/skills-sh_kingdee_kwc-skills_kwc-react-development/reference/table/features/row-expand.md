# 行展开

[返回目录](../index.md)

## 功能说明

通过 `expandProps` 开启行展开，并使用 `custom-row-{rowKey}` slot 自定义展开内容。

## 示例代码（React）

```jsx
import React from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const columns = [
  { dataIndex: 'name', title: '姓名', width: 160 },
  { dataIndex: 'department', title: '部门', width: 140 },
  { dataIndex: 'email', title: '邮箱' }
];

const dataSource = [
  {
    id: '1',
    name: 'Alice Smith',
    department: '研发',
    email: 'alice@example.com'
  },
  {
    id: '2',
    name: 'Bob Johnson',
    department: '产品',
    email: 'bob@example.com'
  }
];

const expandProps = {
  rowExpandable: true,
  expandableRowKeys: ['1', '2'],
  defaultExpandedRowKeys: ['1']
};

export default () => {
  return (
    <SlTable
      rowKey="id"
      columns={columns}
      dataSource={dataSource}
      expandProps={expandProps}
    >
      <div slot="custom-row-1">
        <p>姓名：Alice Smith</p>
        <p>部门：研发</p>
      </div>
      <div slot="custom-row-2">
        <p>姓名：Bob Johnson</p>
        <p>部门：产品</p>
      </div>
    </SlTable>
  );
};
```

---

## 注意事项

1. **rowKey 必须唯一**：`rowKey` 指定的字段在数据中必须唯一，否则会导致行展开功能异常

