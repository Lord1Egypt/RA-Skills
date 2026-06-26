# Excel Operation Schema

这个文件定义 `voice-excel-editor` 的结构化操作协议。Agent 规划时必须遵守这里的字段、动作名和坐标表达。

## 1. 顶层 JSON 结构

```json
{
  "sheet_selector": {
    "mode": "active",
    "sheet_name": ""
  },
  "operations": [],
  "ambiguities": []
}
```

约束：

- `sheet_selector.mode` 仅允许 `active` 或 `by_name`
- 当 `mode=by_name` 时，必须提供 `sheet_name`
- `operations` 必须按用户语句顺序排列
- `ambiguities` 为数组；无歧义时返回空数组

## 2. 坐标表达

优先使用标准 Excel A1 坐标：

- 单元格：`A4`
- 区域：`A1:E5`
- 整列：`A:A`
- 整行：`1:1`
- 已使用区域：`used_range`

不要输出自然语言位置给执行器，比如：

- 不要写 `第一行前五个单元格`
- 要写 `A1:E1`

## 3. 动作定义

### 格式类

#### `merge_cells`

```json
{"action": "merge_cells", "range": "A1:E1"}
```

#### `align_center`

```json
{"action": "align_center", "range": "A1:E1", "vertical": true}
```

`vertical` 可选，默认为 `true`。

#### `bold_font`

```json
{"action": "bold_font", "range": "A1:E10", "enabled": true}
```

#### `fill_color`

```json
{"action": "fill_color", "range": "A1:E1", "color": "FFF2CC"}
```

颜色使用 RGB 十六进制，不带 `#`。

#### `set_border`

```json
{"action": "set_border", "range": "used_range", "style": "bold"}
```

支持样式：

- `thin`
- `medium`
- `thick`
- `bold`

其中 `bold` 会被执行器映射到 `thick`。

#### `set_column_width`

```json
{"action": "set_column_width", "range": "A:C", "width": 18}
```

#### `set_row_height`

```json
{"action": "set_row_height", "range": "1:3", "height": 24}
```

#### `wrap_text`

```json
{"action": "wrap_text", "range": "A1:E10", "enabled": true}
```

### 数据类

#### `write_value`

```json
{"action": "write_value", "target_cell": "B2", "value": "项目名称"}
```

#### `clear_cells`

```json
{"action": "clear_cells", "range": "C2:C9"}
```

#### `copy_range`

```json
{"action": "copy_range", "source_range": "A1:C3", "target_cell": "E1"}
```

### 计算类

#### `write_formula`

```json
{"action": "write_formula", "target_cell": "A4", "formula": "=AVERAGE(A1:A3)"}
```

#### `calculate_average`

```json
{"action": "calculate_average", "source_range": "A1:A3", "target_cell": "A4"}
```

执行器会写入公式 `=AVERAGE(A1:A3)`。

同理支持：

- `calculate_sum`
- `calculate_max`
- `calculate_min`
- `calculate_count`

### 结构类

#### `insert_rows`

```json
{"action": "insert_rows", "row": 5, "amount": 2}
```

#### `delete_rows`

```json
{"action": "delete_rows", "row": 5, "amount": 2}
```

#### `insert_columns`

```json
{"action": "insert_columns", "column": 3, "amount": 1}
```

#### `delete_columns`

```json
{"action": "delete_columns", "column": 3, "amount": 1}
```

#### `create_sheet`

```json
{"action": "create_sheet", "title": "汇总"}
```

#### `rename_sheet`

```json
{"action": "rename_sheet", "new_title": "三月汇总"}
```

仅对当前选中的 sheet 生效。

## 4. 位置解析规则

这些规则优先于自由推理：

- “第 N 行” -> 行号 `N`
- “第 N 列” -> 列号 `N`，再映射成 Excel 列字母
- “前 N 个单元格” + 第 1 行 -> `A1:<col>N1`
- “前 N 个数” + 第 1 列 -> `A1:A<N>`
- “第 X 列第 Y 行” -> `<col>X<Y>`
- “整体边框” -> `used_range`

## 5. 歧义数组格式

当必须停下时返回：

```json
{
  "ambiguities": [
    {
      "expression": "整体加粗",
      "reason": "无法判断是字体加粗还是边框加粗",
      "needed_clarification": "请明确是字体、边框还是两者都加粗"
    }
  ]
}
```

若 `ambiguities` 非空，不应继续生成可执行动作。

## 6. 规划要求

- 一个用户短句可以拆成多个动作
- 相邻动作不要合并成模糊的“大动作”
- 公式优先用 `write_formula`
- 如果表达是“计算平均值后写入”，可用 `calculate_average`
- 如果需要更精确控制公式文本，改用 `write_formula`

## 7. 示例

输入：

```text
把第一行前五个单元格合并后居中，边框整体加粗，然后第一列前三个数计算平均值，结果放到第一列第四行。
```

输出：

```json
{
  "sheet_selector": {"mode": "active"},
  "operations": [
    {"action": "merge_cells", "range": "A1:E1"},
    {"action": "align_center", "range": "A1:E1", "vertical": true},
    {"action": "set_border", "range": "used_range", "style": "bold"},
    {"action": "calculate_average", "source_range": "A1:A3", "target_cell": "A4"}
  ],
  "ambiguities": []
}
```
