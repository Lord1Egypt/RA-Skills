# dm_converter v2.5.1 修复记录

## 修复的问题（2026-06-13，基于 HRBI_Stage.sql 7万行实战测试）

### 1. 存储过程参数不加括号 + AS不换IS

**症状**: 拆分后的文件已有 `CREATE OR REPLACE PROCEDURE`，但转换后参数仍是 `TX_DATE DATE`（无括号），AS也没变成IS。

**根因**: `_convert_procedure` 正则只匹配 `CREATE\s+PROC`，不匹配 `CREATE OR REPLACE PROC`（拆分阶段 v2.4.1 已自动加 OR REPLACE）。

**修复**: 所有3个procedure正则加 `(?:OR\s+REPLACE\s+)?`；name捕获组从 `[\w.\[\"]]+` 改为 `.+?`（因为方括号在字符类内转义损坏）。

**教训**: 上下游模块的输出可能改变输入格式，下游正则必须兼容。

### 2. 方括号标识符未替换（procedure/function）

**症状**: 54个procedure文件里 `[dbo]`、`[xxx]` 原样保留。

**根因**: `_post_convert_table_types` 只对 TABLE/VIEW 生效（代码 `if ctype in (TABLE, VIEW)`），非表类型只做 `_replace_dbo_prefix`，不做方括号替换和类型映射。

**修复**: 新增 `_post_convert_generic_types` 方法，所有非表/视图类型也做: 方括号类型映射 → `[xxx]→"xxx"` → dbo替换。

### 3. `_convert_data_types` 捕获组偏移 → 类型双重映射

**症状**: `p1 INT` → `p1 INTEGERINT`，`p2 VARCHAR(100)` → `p2 VARCHARVARCHAR`。

**根因**: 正则 `(\[?(INT|VARCHAR|...)\]?)` 中类型名用了捕获组 `(...)`，导致 group(4) 是类型名而非长度后缀。`_replace_type` 用 `m.group(4)` 取 suffix，实际拿到了类型名。

**修复**: 类型名改非捕获组 `(?:INT|VARCHAR|...)`，保证 group(4) 始终是长度后缀。

**教训**: 正则中每个 `(...)` 都会偏移后续组号，非提取用途的组必须用 `(?:...)`。

### 4. 长度后缀贪婪匹配

**症状**: `VARCHAR(100), flag BIT` 整段被吃进 suffix。

**根因**: suffix 正则 `[^]]*` 匹配"非`]`的字符"，文件中无 `]` 所以匹配到文件末尾。应为 `[^)]*`（匹配"非`)`的字符"）。

**修复**: `[^]]` → `[^)]`。注意 `[^]]` 在正则引擎中的语义：`[^]` 是字符类匹配"非 `]`"，后面 `]` 关闭字符类——不是"非右方括号"的意图写法。

### 5. 双点号 `..` 未替换

**症状**: `hrbi_stage..Stage_xxx` 保留原样（SQL Server省略dbo的写法）。

**修复**: `_replace_dbo_prefix` 新增双点号处理，必须在三段式之前做：
- `"xxx".."yyy"` → `"xxx"."yyy"`
- `xxx..yyy` → `xxx.yyy`

### 6. GO; 未清理

**症状**: 文件末尾 `GO;` 和 `/` 共存。

**根因**: 正则 `^\s*GO\s*$` 不匹配 `GO;`。

**修复**: 改为 `^\s*GO\s*;?\s*$`。

### 7. VARCHAR(max)/VARCHAR2(max) 映射

**需求**: `VARCHAR(max)` → `VARCHAR(4096 CHAR)`，`VARCHAR2(max)` → `VARCHAR2(4096 CHAR)`。

**修复**:
- TYPE_MAPPINGS 新增 `varchar2 → VARCHAR2`
- 两处 `(max)` 判断加 `'varchar2'`
- `VARCHAR2(max)` 保持 `VARCHAR2` 前缀不降级为 `VARCHAR`

## 调试经验

1. **正则捕获组验证**: 改正则后，用 `re.finditer` 打印每个 match 的 `m.groups()` 确认组号对应，比看代码猜更可靠。
2. **大文件测试**: 单元测试用简单输入无法发现 suffix 贪婪和组偏移问题，需要真实大文件（7万行）才能暴露。
3. **上下游格式变化**: 拆分阶段加了 `OR REPLACE`，转换器正则必须兼容，否则整个方法体跳过。
4. **字符类内方括号**: `[\w.\[\"]]` 中的 `\[` 和 `\"]` 和 `]` 交互导致字符类提前关闭，改用 `.+?` 更安全。
5. **Python缓存**: 修改 .py 后必须清理 `__pycache__/*.pyc`，否则 pytest 运行旧代码。
