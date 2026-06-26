# 文本省略与对齐

[返回目录](../index.md)

## 功能说明

通过列属性 `ellipsis`、`align`、`className` 控制文本溢出和对齐方式。

## 示例代码（React）

```jsx
import React from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const columns = [
  { dataIndex: 'name', title: '姓名', width: 120, align: 'left' },
  {
    dataIndex: 'desc',
    title: '描述',
    width: 120,
    ellipsis: true,
    align: 'center'
  },
  { dataIndex: 'amount', title: '金额', width: 120, align: 'right' }
];

const dataSource = [
  {
    id: '1',
    name: '张三',
    desc: '很长的描述很长的描述很长的描述很长的描述很长的描述',
    amount: 1.00
  }
];

export default () => (
  <SlTable rowKey="id" columns={columns} dataSource={dataSource} />
);
```
