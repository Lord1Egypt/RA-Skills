# 嵌套子表格

[返回目录](../index.md)

## 功能说明

在展开行中再放置一个 `SlTable`，用于展示子数据。

## 示例代码（React）

```jsx
import React from 'react';
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';
import { generateCustomSlot } from '@kdcloudjs/shoelace/dist/components/table/utils';
const dataSource = [
    {
        id: 1,
        Name: 'Bob Johnson',
        Gender: 'Male',
        Age: 34,
        Position: 'Product Manager',
        Email: 'bob.johnson@example.com'
    },
    {
        id: 2,
        Name: 'Carol White',
        Gender: 'Female',
        Age: 31,
        Position: 'UX Designer',
        Email: 'carol.white@example.com'
    },
    {
        id: 3,
        Name: 'David Brown',
        Gender: 'Male',
        Age: 26,
        Position: 'Data Analyst',
        Email: 'david.brown@example.com'
    },
    {
        id: 4,
        Name: 'Eva Green',
        Gender: 'Female',
        Age: 38,
        Position: 'Marketing Lead',
        Email: 'eva.green@example.com'
    }
];
const columns = [
    { title: 'Name', dataIndex: 'Name', width: 140 },
    { title: 'Gender', dataIndex: 'Gender', width: 120 },
    { title: 'Age', dataIndex: 'Age', width: 120 },
    { title: 'Position', dataIndex: 'Position', width: 180 },
    { title: 'Email', dataIndex: 'Email', width: 280 }
];

const CustomTable = (props) => {
    return (
        <div
            slot={props.slot}
            style={{ margin: '8px', border: '1px solid #e5e5e5' }}
        >
            <SlTable
                rowKey="id"
                columns={columns}
                dataSource={dataSource}
                showHeader={false}
            ></SlTable>
        </div>
    );
};

export default () => {
    const [expandProps, setExpandProps] = React.useState({
        defaultExpandedRowKeys: [1],
        expendableRowKeys: [1],
        rowExpandable: true
    });

    const handleGenrateExpandRowSlot = () =>
        generateCustomSlot('id', dataSource, [
            {
                type: 'customRow',
                callback: ({ slotName, rowInfo }) => (
                    <CustomTable key={slotName} slot={slotName} row={rowInfo} />
                )
            }
        ]);

    return (
        <SlTable
            rowKey="id"
            expandProps={expandProps}
            columns={columns}
            dataSource={dataSource}
        >
            {handleGenrateExpandRowSlot()}
        </SlTable>
    );
};
```

---

## 注意事项

1. **rowKey 必须唯一**：`rowKey` 指定的字段在数据中必须唯一，否则会导致行展开功能异常
