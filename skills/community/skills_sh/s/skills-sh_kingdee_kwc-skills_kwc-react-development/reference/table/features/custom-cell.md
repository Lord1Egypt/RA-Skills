# 自定义单元格

[返回目录](../index.md)

## 功能说明

在列上设置 `slot: true`，并通过 `custom-cell-{dataIndex}-{rowKey}` slot 名称渲染自定义内容。

## 示例代码（React）

```jsx
import React from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';
import { generateCustomSlot } from "@kdcloudjs/shoelace/dist/components/table/utils.js";

const columns = [
  { dataIndex: 'name', title: '姓名', width: 160 },
  { dataIndex: 'email', title: '邮箱', width: 260 },
  {
    dataIndex: 'action',
    title: '操作',
    width: 120,
    align: 'center',
    slot: true
  }
];

const dataSource = [
  { id: '1', name: 'Alice Smith', email: 'alice@example.com' },
  { id: '2', name: 'Bob Johnson', email: 'bob@example.com' }
];

const handleDelete = (id) => {
  console.log('删除', id);
};

export default () => {
  const customSlots = generateCustomSlot(
    'id',
    dataSource,
    [
      {
        type: 'customCell',
        columnId: 'action',
        callback: (props) => (
          <div style={{ width: '100%' }} key={props.slotName} slot={props.slotName} className="op-cell">
            <SlButton
              size="small"
              variant="text"
              onClick={() => handleDelete(props.rowInfo.id)}
            >
              删除
            </SlButton>
          </div>
        )
      }
    ]
  );

  return (
    <SlTable rowKey="id" columns={columns} dataSource={dataSource}>
      {customSlots}
    </SlTable>
  );
};
```

---

## 注意事项

1. **slot 属性**：列定义中必须设置 `slot: true` 才能启用自定义渲染
2. **slotName**：`generateCustomSlot` 自动生成符合 `custom-cell-{dataIndex}-{rowKeyValue}` 格式的 slot 名称
3. **key 属性**：每个自定义渲染的元素必须设置 `key` 属性以确保 React 正确 diff
4. **useMemo**：建议使用 `useMemo` 缓存 `generateCustomSlot` 的结果，避免不必要的重渲染

[返回目录](../index.md)
