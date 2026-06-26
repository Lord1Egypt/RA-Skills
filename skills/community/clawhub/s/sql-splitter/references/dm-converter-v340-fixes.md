# dm-converter v3.4.0 修改记录

## 日期: 2026-06-20

## 变更1: TRUNCATE TABLE → DELETE FROM

### 背景
达梦数据库不支持在存储过程内使用 TRUNCATE TABLE 语句，需要转换为 DELETE FROM。

### 实现
- 新增 `_convert_truncate(self, tokens: str) -> str` 方法
- 在 `convert()` 的 Step4 中，`_convert_statements` 之后调用
- 正则: `r'\bTRUNCATE\s+TABLE\s+'` → `'DELETE FROM '` (大小写不敏感)

### 文件变更
- `dm_converter.py`: 新增方法 + convert()中调用
- `test_dm_converter.py`: 新增 TestTruncateConversion (4个测试)

## 变更2: TABLE/VIEW结尾加分号

### 背景
拆分后的表、视图等DDL对象结尾缺少分号，达梦执行时会报错。

### 实现
- 新增 `_add_ending_semicolon(self, content: str) -> str` 方法
- 逻辑: 去掉末尾GO/多余分号 → 统一加一个`;`+换行
- 在 `convert()` 的 Step9 中，对 TABLE/VIEW/INDEX/CONSTRAINT/SEQUENCE 调用
- PROCEDURE/FUNCTION/TRIGGER 仍用 `_add_terminator`（加`/`终止符）

### split_sql_v21.py 变更
- 去掉了 Oracle/DM 方言不加分号的特殊逻辑
- 现在所有方言拆分后均加分号

### 文件变更
- `dm_converter.py`: 新增方法 + convert()中调用
- `split_sql_v21.py`: 去掉 `if dialect not in (SQLDialect.ORACLE, SQLDialect.DM)` 判断
- `test_dm_converter.py`: 新增 TestEndingSemicolon (5个测试)

## 测试结果
- 全部53个测试通过 (原44个 + 新增9个)
- 0个失败
