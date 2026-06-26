# 分页

[返回目录](../index.md)

## 功能说明

通过 `pagination` 配置分页，支持受控与非受控模式。

## 示例代码（React）

### 非受控

```jsx
import React from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const columns = [
  { dataIndex: 'name', title: '姓名', width: 160 },
  { dataIndex: 'email', title: '邮箱' }
];

const dataSource = Array.from({ length: 100 }).map((_, i) => ({
  id: String(i + 1),
  name: `User-${i + 1}`,
  email: `user${i + 1}@example.com`
}));

const pagination = { pageSize: 10, pageSizeOpts: [10, 20, 50, 100] };

const handleChange = (e) => { console.log(e.detail) };

export default () => (
  <SlTable
    rowKey="id"
    columns={columns}
    dataSource={dataSource}
    pagination={pagination}
    onChange={handleChange}
  />
);
```

### 受控

```jsx
import React, { useState, useMemo } from 'react';
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const columns = [
    { dataIndex: 'name', title: '姓名', width: 160 },
    { dataIndex: 'email', title: '邮箱' }
];

const allData = Array.from({ length: 100 }).map((_, i) => ({
    id: String(i + 1),
    name: `User-${i + 1}`,
    email: `user${i + 1}@example.com`
}));

export default () => {
    const [tablePagination, setTablePagination] = useState({
        pageSize: 10,
        pageSizeOpts: [10, 20, 50, 100],
        currentPage: 1,
        total: allData.length
    });

    // 根据分页状态切片数据
    const displayData = useMemo(() => {
        const { currentPage, pageSize } = tablePagination;
        const start = (currentPage - 1) * pageSize;
        return allData.slice(start, start + pageSize);
    }, [tablePagination]);

    const handleChange = (e: CustomEvent) => {
        const { changeType, pagination } = e.detail || {};
        console.log(changeType);
        if (changeType === 'pagination') {
            const { pageNumber, pageSize } = pagination;
            setTablePagination((prev) => ({
                ...prev,
                currentPage: pageNumber ?? prev.currentPage,
                pageSize: pageSize ?? prev.pageSize
            }));
        }
    };

    return (
        <SlTable
            rowKey="id"
            columns={columns}
            dataSource={displayData}
            pagination={tablePagination}
            onChange={handleChange}
        />
    );
};
```

