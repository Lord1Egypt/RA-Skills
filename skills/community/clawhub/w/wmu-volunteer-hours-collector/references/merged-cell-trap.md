# insert_rows 与合并单元格的交互问题

## 问题描述

模板的注意事项区域（表尾最后10行）每行有整行合并单元格（A:N 列合并）。
当 `adjust_rows` 在表尾前调用 `ws.insert_rows(footer_start)` 时，openpyxl
不会正确将合并单元格整体下移，而是在旧位置留下不可写入的 `MergedCell` artifact。

后续 `fill_row` 写入这些 cell 时，`MergedCell` 对象的 `value` 属性为只读，导致
部分记录的 B-N 列数据丢失，而 A 列为普通 Cell 不受影响。

## 触发条件

- 模板的表尾区域有合并单元格
- `adjust_rows` 在表尾前**插入**新行
- `fill_row` 尝试写入残留了 MergedCell artifact 的行

## 症状

- 数据区末尾部分行只有 A 列有数据
- 或者 `fill_row` 直接抛出 `AttributeError: 'MergedCell' object attribute 'value' is read-only`

## 修复（已在 helpers.py 中实现）

在 `adjust_rows` 中，插入行之前：
1. **保存**所有表尾合并单元格的范围（起止行/列）
2. **unmerge** 它们（避免 insert_rows 产生 artifact）
3. 调用 `ws.insert_rows()`
4. 在移位后的位置**重建合并单元格**

```python
footer_merges = []
for mc in list(ws.merged_cells.ranges):
    if mc.min_row >= footer_start:
        footer_merges.append((mc.min_row, mc.max_row, mc.min_col, mc.max_col))
        ws.unmerge_cells(str(mc))

for _ in range(rows_to_add):
    ws.insert_rows(footer_start)

for min_r, max_r, min_c, max_c in footer_merges:
    ws.merge_cells(
        start_row=min_r + rows_to_add,
        start_column=min_c,
        end_row=max_r + rows_to_add,
        end_column=max_c,
    )
```

注意：`list()` 确保遍历合并单元格的快照，避免 unmerge 过程中修改集合导致迭代错误。

## 为什么不在 fill_data 中 unmerge

在 `fill_data` 中 unmerge 数据区的合并单元格虽然能让数据写入成功，
但会**永久破坏表尾的合并格式**（因为表尾合并单元格 stuck 在旧位置
被 unmerge 后，不会再重建到新位置）。
