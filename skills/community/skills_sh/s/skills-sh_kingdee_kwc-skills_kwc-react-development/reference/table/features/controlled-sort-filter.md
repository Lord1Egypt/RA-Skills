# 受控排序筛选

[返回目录](../index.md)

## 功能说明

通过 `sortOrder`、`filteredValue` + `onChange` 实现受控排序/筛选，适用于服务端联动。

## 示例代码（React）

```jsx
import React, { useState, useMemo } from 'react';
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';

interface DataRecord {
    id: string;
    no: number;
    name: string;
    [key: string]: string | number;
}

type SortOrder = 'asc' | 'desc' | '';
type SortingState = Record<string, SortOrder>;
type FiltersState = Record<string, string[]>;

export default () => {
    const [sorting, setSorting] = useState<SortingState>({});
    const [filters, setFilters] = useState<FiltersState>({ name: [] });

    const dataSource: DataRecord[] = [
        { id: '1', no: 1, name: 'Alice' },
        { id: '2', no: 2, name: 'Bob' }
    ];

    const columns = useMemo(() => {
        return [
            {
                dataIndex: 'no',
                title: '#',
                width: 60,
                sorter: (a: DataRecord, b: DataRecord) => a.no - b.no,
                sortOrder: sorting.no || ''
            },
            {
                dataIndex: 'name',
                title: '姓名',
                sorter: (a: DataRecord, b: DataRecord) => a.name.localeCompare(b.name),
                sortOrder: sorting.name || '',
                filters: [
                    { text: 'Alice', value: 'Alice' },
                    { text: 'Bob', value: 'Bob' }
                ],
                filteredValue: filters.name || [],
                onFilter: (value: string, record: DataRecord) => record.name.includes(value)
            }
        ];
    }, [sorting, filters]);

    // 根据 sorting 和 filters 状态派生展示数据
    const displayData = useMemo(() => {
        let result = [...dataSource];

        // 应用筛选
        Object.entries(filters).forEach(([key, values]) => {
            if (values && values.length > 0) {
                result = result.filter((record) =>
                    values.some((v: string) => String(record[key]).includes(v))
                );
            }
        });

        // 应用排序
        const sortKey = Object.keys(sorting).find((k) => sorting[k]);
        if (sortKey) {
            const col = columns.find((c) => c.dataIndex === sortKey);
            if (col?.sorter) {
                const direction = sorting[sortKey] === 'desc' ? -1 : 1;
                result.sort((a, b) => col.sorter(a, b) * direction);
            }
        }

        return result;
    }, [dataSource, sorting, filters, columns]);

    const handleChange = (e: CustomEvent) => {
        const { changeType, sorting: newSorting, columnFilters } = e.detail || {};
        if (changeType === 'sorter') {
            const next: SortingState = {};
            (newSorting || []).forEach((s: { id: string; desc: boolean }) => {
                next[s.id] = s.desc ? 'desc' : 'asc';
            });
            setSorting(next);
        }
        if (changeType === 'filters') {
            const next: FiltersState = {};
            (columnFilters || []).forEach((f) => {
                next[f.id] = f.value;
            });
            setFilters(next);
        }
    };

    return (
        <SlTable
            rowKey="id"
            columns={columns}
            dataSource={displayData}
            onChange={handleChange}
        />
    );
};
```

---

## 注意事项

1. **受控模式切换**：一旦设置了 `sortOrder` 或 `filteredValue`，该列就进入受控模式，组件不会自动排序/筛选
2. **必须配合回调使用**：受控模式下需要使用 `onChange` 事件并手动更新状态
3. **清空受控值**：将 `sortOrder` 设为 `null`、`filteredValue` 设为空数组可清除对应状态
