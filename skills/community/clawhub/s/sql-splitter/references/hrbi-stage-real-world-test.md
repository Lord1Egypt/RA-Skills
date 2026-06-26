# HRBI_Stage.sql 真实项目测试记录 (2026-06-13)

## 测试文件
- 路径: /Users/a1234/Downloads/hrbi_sql/HRBI_Stage.sql
- 大小: 7万行, 229万字符
- 编码: UTF-16 (带BOM) — SQL Server 导出文件的常见编码
- 方言: SQL Server (自动检测)

## 测试流程

### 1. 编码转换
原始文件为 UTF-16, 拆分脚本默认读 UTF-8, 需先转换:
```python
with open('HRBI_Stage.sql', 'r', encoding='utf-16') as f:
    content = f.read()
with open('HRBI_Stage_utf8.sql', 'w', encoding='utf-8') as f:
    f.write(content)
```

### 2. 拆分结果
- 方言: SQLSERVER (自动检测)
- 对象数: 462
  - table: 373
  - view: 35
  - procedure: 54
- 全部成功, 无失败
- 合并脚本已生成: merge_all.sql

### 3. 达梦转换结果
- 462/462 全部成功 (0失败)
- 批量转换用 Python 脚本循环调用 `dm_converter.convert_sqlserver_to_dm()`
- obj_type 从文件名前缀映射: proc_→procedure, table_→table, view_→view

### 4. 发现的问题

#### DATE → DATEDATE 类型映射bug
- **症状**: 存储过程参数 `@TX_DATE DATE` 转换后变成 `TX_DATE DATEDATE`
- **根因**: dm_converter 的类型映射正则边界不够精确, `DATE` 匹配后贪婪吃进了换行或空白后的内容
- **影响**: 存储过程级, 有 `DATE` 类型参数的 procedure 均受影响
- **待修**: 需在 dm_converter.py 中修正 DATE 类型的正则后缀锚点

#### dbo前缀替换效果
- 两段式 `[dbo].[Stage_DH_View...]` → `"HRBI_Stage"."Stage_DH_View..."` ✅
- schema_prefix 从源文件名自动提取: `HRBI_Stage.sql` → `HRBI_Stage` ✅

#### VARCHAR CHAR语义
- `[nvarchar](20)` → `VARCHAR(20 CHAR)` ✅
- `[datetime]` → `TIMESTAMP` ✅
- `[bit]` → `BOOLEAN` ✅

#### 存储过程转换不完整
- 存储过程体内的 `@变量` 未全部去除@前缀
- `delete FROM [dbo].Stage_...` 中的 `[dbo].` 未被替换(表名在过程体内)
- 这些是已知限制, 需手动调整

## 批量转换脚本模板

见本次会话中 /tmp/dm_batch_convert.py — 可复用的批量转换脚本模板, 核心逻辑:
1. 遍历 _split/ 目录所有 .sql 文件
2. 从文件名前缀推断 obj_type
3. 调用 convert_sqlserver_to_dm(content, obj_type, schema_prefix=...)
4. 写入 _split_dm/ 目录
5. 生成 merging_all.sql
