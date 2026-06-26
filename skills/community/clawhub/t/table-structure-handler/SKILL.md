---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: f809f4a433a4316a9a48ac900905d349
    PropagateID: f809f4a433a4316a9a48ac900905d349
    ReservedCode1: 3045022024e19edae09bac4dbd105fec5a101a0628567b887ab085496759e6faf118ea2d0221008f944f2ab6c30f5d269810f00de9feb4bd42bcb83aad419a4b5609fef073cdda
    ReservedCode2: 30450221009f4c61687f9a6737d00212b093d699034f5db4a393e271b0b51a418533505e0f02207d0ac36e1d600931319ff0a9d9046febabdb1532870e235f2eeea80a1e9f11c4
description: 表结构Excel处理技能。当用户说"表结构处理"时触发。
name: table-structure-handler
---

# table-structure-handler 表结构处理技能

## 触发词

- "表结构处理"
- "处理表结构"

## 功能说明

对上传到 `user_input_files/` 的 Excel 表结构文件进行处理：

1. **删除第一行**（原表标题行）
2. **在新的第一行 F 列起插入9列标准表头**：

   | 列 | 标题 |
   |----|------|
   | F | 表英文名称 |
   | G | 表中文名称 |
   | H | 数据类型 |
   | I | 数据长度 |
   | J | 数据精度 |
   | K | 唯一性约束 |
   | L | 创建索引 |
   | M | 数据说明（不作为注释） |
   | N | 数据质量规则（不作为注释） |

3. **设置行高为 30**
4. **添加默认边框**
5. **自动调整 F~N 列列宽**
6. **A~E 列原有数据完整保留**
7. **应用表格样式（根据 data/cellStyle.txt）**

## 输入输出

| 类型 | 路径 |
|------|------|
| 输入目录 | `/workspace/user_input_files/` |
| 输入文件 | 目录下最新的 `.xlsx` 文件，或用户指定文件名 |
| 输出文件 | `/workspace/skills_output/` + `文件名_processed.xlsx` |

## 使用方式

上传文件到 `user_input_files/`，然后说：

> **"表结构处理"**

指定文件名时：

> **"表结构处理 XXX.xlsx"**

## 注意事项

- 不覆盖原文件，输出带 `_processed` 后缀
- 支持模糊文件名（如 `表C.2.2` 即可匹配完整文件名）
- A~E 列数据原样保留
