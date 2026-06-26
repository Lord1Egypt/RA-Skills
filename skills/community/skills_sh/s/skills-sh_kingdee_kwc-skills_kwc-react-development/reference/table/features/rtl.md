# RTL 方向

[返回目录](../index.md)

## 功能说明

通过 `direction="rtl"` 开启从右到左布局。

## 示例代码（React）

根据语言设置动态切换表格方向。

```jsx
import React, { useState, useMemo } from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const ltrColumns = [
  { title: 'Name', dataIndex: 'name', width: 150 },
  { title: 'Age', dataIndex: 'age', width: 100 },
  { title: 'City', dataIndex: 'city' }
];

const rtlColumns = [
  { title: 'الاسم', dataIndex: 'name', width: 150 },
  { title: 'العمر', dataIndex: 'age', width: 100 },
  { title: 'المدينة', dataIndex: 'city' }
];

const ltrData = [
  { id: '1', name: 'John', age: 28, city: 'New York' },
  { id: '2', name: 'Jane', age: 35, city: 'Los Angeles' },
  { id: '3', name: 'Bob', age: 30, city: 'Chicago' }
];

const rtlData = [
  { id: '1', name: 'أحمد', age: 28, city: 'القاهرة' },
  { id: '2', name: 'محمد', age: 35, city: 'الإسكندرية' },
  { id: '3', name: 'فاطمة', age: 30, city: 'الجيزة' }
];

export default () => {
  const [direction, setDirection] = useState('ltr');

  const columns = useMemo(() => direction === 'rtl' ? rtlColumns : ltrColumns, [direction]);
  const dataSource = useMemo(() => direction === 'rtl' ? rtlData : ltrData, [direction]);

  return (
    <div>
      <button onClick={() => setDirection('ltr')}>LTR (English)</button>
      <button onClick={() => setDirection('rtl')}>RTL (العربية)</button>
      <SlTable rowKey="id" direction={direction} bordered columns={columns} dataSource={dataSource} />
    </div>
  );
};
```

