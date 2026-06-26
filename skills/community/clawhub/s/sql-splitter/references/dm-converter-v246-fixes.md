# dm_converter v2.4.6 修复记录

## Bug 1: 存储过程方括号和dbo未替换

**症状**: 转换后54个procedure文件残留`[dbo]`和`[xxx]`方括号标识符

**根因**: `convert()`方法Step 6.7只有TABLE/VIEW走`_post_convert_table_types`做方括号→双引号+dbo替换，非表对象只做`_replace_dbo_prefix`（但此时方括号还在，dbo替换正则匹配不到`[dbo]`格式）

**修复**: 新增`_post_convert_generic_types()`方法，对所有非TABLE/VIEW对象类型做:
1. 方括号类型名映射 `[int]` → `INTEGER`
2. 方括号→双引号 `[xxx]` → `"xxx"`
3. dbo前缀替换（含`..`双点号）
4. GO → /

**位置**: dm_converter.py Step 6.7 分支逻辑

## Bug 2: 数据类型双重映射 (INTEGERINT, VARCHARVARCHAR)

**症状**: `@p1 INT` → `p1 INTEGERINT`, `@p2 VARCHAR(100)` → `p2 VARCHARVARCHAR`

**根因**: `_convert_data_types`的正则中类型名用了捕获组:
```python
# 旧: (\\[?(INT|VARCHAR|...)\\]?)  — 3个捕获组: prefix, col, type(含内部子组), suffix
r'([,\\(]\\s*|DECLARE\\s+|\\n\\s*)([\\w@]+)\\s+(\\[?(' + _FULL_TYPE_NAMES_PATTERN + r')\\]?)(\\(...\\))?'
```
`_FULL_TYPE_NAMES_PATTERN`拼接后变成`(INT|VARCHAR|...)`,是捕获组group(4)。
代码里`suffix = m.group(4) or ''`实际拿到的是类型名内部组`INT`而非长度后缀`(100)`。
替换后`f"{prefix}{col_name} {new_type}{suffix}"`变成`p1 INTEGER` + `INT` = `p1 INTEGERINT`

**修复**: 类型名内部组改为非捕获组`(?:...)`:
```python
# 新: (\\[?(?:INT|VARCHAR|...)\\]?)  — 4个捕获组: prefix, col, type, suffix(正确)
r'([,\\(]\\s*|DECLARE\\s+|\\n\\s*)([\\w@]+)\\s+(\\[?(?:' + _FULL_TYPE_NAMES_PATTERN + r')\\]?)(\\(...\\))?'
```
现在group(4)才是suffix，group(3)是完整类型名（含可选方括号）

**教訓**: Python正则中拼接变量构建捕获组时，务必确认组号偏移。用`(?:...)`非捕获组避免意外偏移

## Bug 3: 类型长度后缀贪婪匹配

**症状**: `name VARCHAR(100), flag BIT` 中`VARCHAR`的suffix吃掉了后面所有内容

**根因**: suffix正则`\\([^]]*(?:\\([^]]*\\)[^]]*)*\\)`中`[^]]*`匹配"非]的字符"而非"非)的字符"。`[^]]`是字符类`[^]`加上字面量`]`，实际等于匹配几乎任何字符（因为`]`很少出现）。应为`[^)]*`匹配"非)的字符"。

**修复**: 
```python
# 旧: \\([^]]*(?:\\([^]]*\\)[^]]*)*\\)
# 新: \\([^)]*(?:\\([^)]*\\)[^)]*)*\\)
```

## Bug 4: SQL Server双点号`..`语法

**症状**: 转换后存储过程中残留`hrbi_stage..Stage_xxx`，达梦不支持

**根因**: SQL Server的`database..object`语法省略了dbo schema，相当于`database.dbo.object`。`_replace_dbo_prefix`中三段式正则`xxx.dbo.yyy`匹配不到两段式`xxx..yyy`

**修复**: 在`_replace_dbo_prefix`开头优先处理双点号:
```python
# "xxx".."yyy" → "xxx"."yyy"
content = re.sub(r'"([^"]+)"\.\.', r'"\1".', content)
# xxx..yyy → xxx.yyy
content = re.sub(r'\b(\w+)\.\.', r'\1.', content)
```

## UTF-16编码处理

SQL Server Management Studio导出的.sql文件常用UTF-16编码（带BOM），需先转UTF-8:
```python
with open('input.sql', 'r', encoding='utf-16') as f:
    content = f.read()
with open('input_utf8.sql', 'w', encoding='utf-8') as f:
    f.write(content)
```

## 测试验证

```bash
cd scripts && python3 -m pytest test_dm_converter.py -v
# 40/40 passed
```
