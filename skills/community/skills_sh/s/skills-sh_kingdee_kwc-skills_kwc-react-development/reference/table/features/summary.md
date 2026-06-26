# 总结栏（Summary）

通过 `summary` 属性可以在表格底部添加汇总行。页尾内容通过插槽自定义，页尾会跟随表体横向滚动保持对齐。

## 类型定义

```ts
interface SummaryObject {
  /** 总结行的索引，标识该行在表尾中的位置 */
  rowIndex: number;
  /** 传递给每个单元格的属性（如 style、onclick 等），key 为列的 dataIndex */
  cells?: Record<string, unknown>[];
}
```

## 基础用法

页尾单元格内容通过 `slot="custom-tfoot-cell-{rowIndex}-{dataIndex}"` 插槽自定义，`cells` 用于向对应单元格传递属性（如 style、事件等）。
```jsx
import React from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const columns = [
    { title: '商品', dataIndex: 'product', width: 150 },
    { title: '单价', dataIndex: 'price', width: 100, align: 'right' },
    { title: '数量', dataIndex: 'quantity', width: 100, align: 'right' },
    { title: '小计', dataIndex: 'subtotal', width: 120, align: 'right' }
];

const dataSource = [
    { key: '1', product: '键盘', price: 299, quantity: 2, subtotal: 598 },
    { key: '2', product: '鼠标', price: 129, quantity: 3, subtotal: 387 },
    { key: '3', product: '显示器', price: 1999, quantity: 1, subtotal: 1999 }
];

const summary = [
    {
        rowIndex: 0,
        cells: [
            {
                product: {
                    style: { color: 'red' },
                    onclick: () => alert('点击了合计')
                }
            }
        ]
    }
];

export default () => (
    <SlTable
        rowKey="key"
        columns={columns}
        dataSource={dataSource}
        summary={summary}
        bordered
    >
        <div slot="custom-tfoot-cell-0-product">合计</div>
        <div slot="custom-tfoot-cell-0-price" style={{ textAlign: 'right' }}>9999</div>
        <div slot="custom-tfoot-cell-0-quantity" style={{ textAlign: 'right' }}>6</div>
        <div slot="custom-tfoot-cell-0-subtotal" style={{ textAlign: 'right' }}>9999</div>
    </SlTable>
);
```

## 自定义页尾插槽

当 `summary` 传入空数组 `[]` 时，表格页尾会渲染 `custom-tfoot` 插槽，可完全自定义页尾内容。

```jsx
import React from "react";
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

const columns = [
    { title: '商品', dataIndex: 'product', width: 150 },
    { title: '单价', dataIndex: 'price', width: 100, align: 'right' },
    { title: '数量', dataIndex: 'quantity', width: 100, align: 'right' },
    { title: '小计', dataIndex: 'subtotal', width: 120, align: 'right' }
];

const dataSource = [
    { key: '1', product: '键盘', price: 299, quantity: 2, subtotal: 598 },
    { key: '2', product: '鼠标', price: 129, quantity: 3, subtotal: 387 },
    { key: '3', product: '显示器', price: 1999, quantity: 1, subtotal: 1999 }
];

export default () => (
    <SlTable
        rowKey="key"
        columns={columns}
        dataSource={dataSource}
        summary={[]}
    >
        <div slot="custom-tfoot" style={{ padding: '8px', textAlign: 'center', color: '#666' }}>
            这是通过 custom-tfoot 插槽自定义的页尾内容
        </div>
    </SlTable>
);
```

## 注意事项

- 页尾单元格内容通过插槽 `custom-tfoot-cell-{rowIndex}-{dataIndex}` 自定义
- `cells` 用于向单元格传递属性（如 `style`、`onclick` 等），key 为列的 `dataIndex`
- `summary` 传空数组 `[]` 时，渲染 `custom-tfoot` 插槽，可完全自定义页尾
- 页尾渲染在 `<tfoot>` 区域，跟随表体横向滚动保持对齐
- 可通过 CSS Part `table-foot`、`table-foot-row`、`table-foot-cell` 自定义样式