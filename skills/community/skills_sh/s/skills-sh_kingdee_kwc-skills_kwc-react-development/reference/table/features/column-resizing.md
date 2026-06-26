# 列宽调整

[返回目录](../index.md)

## 功能说明

通过 `enableColumnResizing` 开启拖拽调整列宽，使用 `slColumnResize` 获取调整结果。

## 示例代码（React）

```jsx
import React from 'react';
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const columns = [
    { dataIndex: 'name', title: '姓名', width: 160 },
    { dataIndex: 'email', title: '邮箱', width: 280 }
];

const dataSource = [{ id: '1', name: 'Alice Smith', email: 'alice@example.com' }];

const handleColumnResize = (e) => {
    console.log('sizes', e.detail);
};

export default () => (
    <SlTable
        rowKey="id"
        columns={columns}
        dataSource={dataSource}
        enableColumnResizing={true}
        slColumnResize={handleColumnResize}
    />
);
```
