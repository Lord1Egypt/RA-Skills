# dm_converter v3.2.3 修复记录 — PROCEDURE用AS而非IS

## 问题描述

用户指出：**达梦存储过程应该用AS而非IS**。

`_convert_procedure`方法错误地将所有PROCEDURE声明生成`IS`结尾：
```
CREATE OR REPLACE PROCEDURE "HRBI_Stage"."PROC_xxx" (TX_DATE DATE) IS   ← 错误
```

正确应该是：
```
CREATE OR REPLACE PROCEDURE "HRBI_Stage"."PROC_xxx" (TX_DATE DATE) AS   ← 正确
```

## 根因

达梦的PROCEDURE声明语法要求`AS`，FUNCTION才用`IS`。这是Oracle和达梦的语法差异：
- **Oracle**: PROCEDURE 可以用 IS 或 AS
- **达梦**: PROCEDURE 必须用 AS，FUNCTION 用 IS

代码中`_convert_procedure`硬编码了`IS`（套用了Oracle惯例），没有区分PROCEDURE和FUNCTION。

## 修复

在`_convert_procedure`方法中，将4处`IS`改为`AS`：

1. **有括号参数列表**（第398行）: `... {params} IS` → `... {params} AS`
2. **无括号参数(单参数)**（第417行）: `... ({params_clean.strip()}) IS` → `... AS`
3. **无括号参数(多参数)**（第419行）: `... {formatted} IS` → `... {formatted} AS`
4. **无参数存储过程**（第431行）: `'CREATE OR REPLACE PROCEDURE \\1 IS'` → `... \\1 AS`

**未修改**: `_convert_function`方法保持`IS`不变。

## 测试

- 旧断言 `assertIn('IS', result.converted)` → `assertIn('AS', result.converted)`
- 旧断言 `assertIn('sp_simple IS', ...)` → `assertIn('sp_simple AS', ...)`
- 44个单元测试全部通过
- 462个真实SQL对象端到端验证：47个proc文件全部从IS改为AS，0个残留

## 关键区分备忘

| 对象类型 | 达梦声明结尾 |
|---------|------------|
| PROCEDURE | **AS** |
| FUNCTION | **IS** |
