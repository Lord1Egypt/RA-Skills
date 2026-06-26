# dm_converter v3.2.2 修复记录

## 日期: 2026-06-14

## 修复内容

### 1. 存储过程VARCHAR(n)加CHAR语义

**问题**: `_post_convert_generic_types` 注释写"不做 VARCHAR(n) -> VARCHAR(n CHAR) (过程体内变量声明不需要)"，导致存储过程中所有VARCHAR(n)缺少CHAR语义。

**用户反馈**: "存储过程中也需要按照之前的类型映射进行修改"

**修复前**:
```sql
--DECLARE变量
v_Sql VARCHAR(4000);
--参数
CREATE OR REPLACE PROCEDURE sp_test (p1 INTEGER, p2 VARCHAR(100)) IS
--CAST
CAST(TX_DATE AS nvarchar(50))  -- nvarchar也未映射
```

**修复后**:
```sql
v_Sql VARCHAR(4000 CHAR);
CREATE OR REPLACE PROCEDURE sp_test (p1 INTEGER, p2 VARCHAR(100 CHAR)) IS
CAST(TX_DATE AS VARCHAR(50 CHAR))
```

### 2. CAST中nvarchar未映射

**问题**: `_post_convert_generic_types` 只有 `_bracket_type_pattern` 匹配方括号包裹的类型名（如`[nvarchar]`），但SQL Server过程体中 `cast(x as nvarchar(50))` 的 `nvarchar` 是裸名无方括号，不匹配。

**修复**: 新增 `_bare_type_pattern`，用 `(?<=\s)` lookbehind 匹配前有空白字符的裸类型名。

```python
_bare_type_pattern = re.compile(
    r'(?<=\s)(' + '|'.join(re.escape(t) for t in _type_map.keys()) + r')(?=\s*\(|\s+NULL|\s+NOT|\s+IDENTITY|\s+DEFAULT|\s+,|\s*\)|\s*$)',
    re.IGNORECASE
)
```

**设计注意**: `(?<=\s)` 确保只匹配前面有空白字符的类型名（如 `AS nvarchar(50)` 或 `as VARCHAR(4000)`），避免错误匹配列名（列名通常在逗号或括号后，前面不是空格）。

### 3. _post_convert_generic_types 新增 VARCHAR(n) → VARCHAR(n CHAR)

```python
content = re.sub(
    r'\bVARCHAR\s*\(\s*(\d+)\s*\)',
    r'VARCHAR(\1 CHAR)',
    content,
    flags=re.IGNORECASE
)
```

与 `_post_convert_table_types` 使用相同的正则模式。

## 验证结果

- 44个单元测试全部通过（含4个新增 TestProcedureTypeMapping）
- 462个真实SQL对象端到端测试全部通过（HRBI_Stage.sql, 7万行）
- 存储过程中nvarchar残留数: 0（全部映射为VARCHAR(n CHAR)）
- DECLARE变量: `v_Sql VARCHAR(4000 CHAR)` ✓
- CAST: `CAST(TX_DATE AS VARCHAR(50 CHAR))` ✓

## 测试用例

新增 `TestProcedureTypeMapping` 类，含4个测试:
- `test_procedure_varchar_char_semantic`: DECLARE变量VARCHAR加CHAR
- `test_procedure_cast_nvarchar`: CAST中nvarchar→VARCHAR(n CHAR)
- `test_procedure_parameter_varchar_char`: 参数VARCHAR加CHAR
- `test_function_returns_varchar_char`: RETURNS VARCHAR加CHAR

## 已有测试断言更新

- `test_procedure_with_params`: `p2 VARCHAR(100)` → `p2 VARCHAR(100 CHAR)`
- `test_scalar_function`: `RETURN VARCHAR` → `RETURN VARCHAR(50 CHAR)`
