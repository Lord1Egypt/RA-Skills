---
name: pyspark-to-excel
description: "将 PySpark .show() 输出转为可直接粘贴到 Excel 的 Tab 分隔格式。触发词：pyspark、数据转excel、表格整理、venus数据、show输出、复制到excel、数据格式化。"
---

# PySpark to Excel

将用户粘贴的 PySpark `.show()` 输出转为 Tab 分隔文本，可直接复制粘贴到 Excel 自动分列分行。

## 规则

1. **不分析、不加工数据**，只做格式转换
2. **不添加任何注释或说明文字**，只输出转换结果
3. 输出用代码块包裹，方便用户一键复制

## 处理流程

收到数据后立即执行：

1. 识别 PySpark `.show()` 格式：以 `+` 开头的分隔行和 `|` 分隔的数据行
2. 去掉所有 `+---...---+` 分隔行
3. 去掉每行首尾的 `|`
4. 按 `|` 拆分各列，去除每个单元格的首尾空格
5. 用 Tab (`\t`) 连接各列
6. 第一个数据行作为表头，后续行作为数据
7. 如有末尾的 `only showing top N rows` 提示行，去掉
8. 将结果放在代码块中输出

## 示例

**用户输入：**

```
+--------+------+-------+
|    name|   age|   city|
+--------+------+-------+
|   Alice|    30|Beijing|
|     Bob|    25|Shanghai|
+--------+------+-------+
```

**输出：**

```
name	age	city
Alice	30	Beijing
Bob	25	Shanghai
```

用户复制代码块内容，粘贴到 Excel 即可自动分列。
