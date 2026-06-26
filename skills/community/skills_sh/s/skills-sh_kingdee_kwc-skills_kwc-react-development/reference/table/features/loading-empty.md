# 加载状态与空数据

[返回目录](../index.md)

## 功能说明

`loading` 控制加载态，`table-empty` slot 支持空态自定义。

## 示例代码（React）

```jsx
import React from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const columns = [{ dataIndex: 'name', title: '姓名' }];
const dataSource = [];

export default () => (
  <SlTable rowKey="id" columns={columns} dataSource={dataSource} loading={true}>
    <div slot="table-empty" className="empty-wrap">
      <p>暂无数据</p>
    </div>
  </SlTable>
);
```


