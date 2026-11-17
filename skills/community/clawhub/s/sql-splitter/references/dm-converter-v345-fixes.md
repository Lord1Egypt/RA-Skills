# dm_converter v3.4.5 修复记录

## 日期: 2026-06-26

## 修复概览

312个HRBI存储过程批量转换，7条用户规则全部验证通过。

| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| 转换失败数 | 0 (但规则不完整) | 0 |
| VARCHAR CHAR语义 | 2057处 | 2057处 OK |
| SELECT INTO CTAS | 0 (不支持) | 174处 OK |
| DDL缺分号 | 447处 | 0 OK |

---

## 修复1: dbo两段式无prefix时保留不替换(BUG)

**问题**: `_replace_dbo_prefix()`在两段式`dbo.xxx`且无schema_prefix时保留`dbo.`不替换，用户要求去掉dbo变成`xxx`。

**修复位置**: `_replace_dbo_prefix()` 两段式分支

**逻辑**:
- 有schema_prefix: `dbo.xxx` -> `{prefix}.xxx`
- 无schema_prefix: `dbo.xxx` -> `xxx` (去掉dbo.前缀)

---

## 修复2: DATETIME2->TIMESTAMP2而非TIMESTAMP(BUG)

**问题**: TYPE_MAPPINGS的key构建正则alternation时无排序，`DATETIME`排在`DATETIME2`前面抢先匹配，`DATETIME2`被拆成`DATETIME`+`2`变成`TIMESTAMP2`。

**根因**: Python正则`|` alternation从左到右匹配，公共前缀的类型名短者先匹配。

**修复**: 全局`_TYPE_NAMES_PATTERN`、`_FULL_TYPE_NAMES_PATTERN`、`_post_convert_table_types`和`_post_convert_generic_types`中的`_bare_type_pattern`均用`sorted(keys, key=len, reverse=True)`按长度降序排列。

**受影响位置(4处)**:
1. `convert()`方法构建`type_name_pattern`
2. `_post_convert_table_types()`构建`_bare_type_pattern`
3. `_post_convert_generic_types()`构建`_bare_type_pattern`
4. 任何新增的TYPE_MAPPINGS consumer

---

## 修复3: 方括号替换在token还原后执行导致注释内容被误改(架构BUG)

**问题**: `_post_convert_table_types`/`_post_convert_generic_types`中的`\[([^\]]+)\]`在Step 6.7(token还原后)执行，注释已还原为原始文本，注释中含方括号会被误匹配截断。

**修复**: 把方括号替换从Step 6.7移到Step 4 `_convert_bracket_identifiers()`中执行。

**关键设计**: 此时注释和字符串已被tokenize保护(`__TOKEN_N__`占位符)，方括号只出现在真实SQL代码中。

**正则改进**: `[^\]\n]+`非贪婪模式，避免同行多标识符贪婪匹配跨行截断。

**保持不变的行为**:
- 动态SQL字符串内的方括号不修改(字符串被tokenize保护)
- 注释中的`[`不修改(注释被tokenize保护)

---

## 修复4: SELECT INTO #临时表->CTAS创建GTT(新规则)

**问题**: 达梦不支持`SELECT ... INTO #新表 FROM ...`建表语法。

**转换规则**:
```sql
-- SQL Server
SELECT * INTO #tmp_xxx FROM source_table WHERE ...

-- 达梦 (CTAS)
CREATE GLOBAL TEMPORARY TABLE "tmp_xxx" AS SELECT * FROM source_table WHERE ...;
```

**识别标识**:
- `INTO #xxx` -> 临时表(#前缀)
- `INTO tmp_xxx` -> 临时表(tmp_前缀)
- `INTO gtmp_xxx` -> 全局临时表(gtmp_前缀)

**限制**: 非临时表的SELECT INTO暂不自动转换——与达梦变量赋值语法`SELECT expr INTO var FROM ...`形式相同，无法程序化区分。

**验证**: 312个存储过程中174处SELECT INTO临时表成功转为CTAS。

---

## 修复5: 过程体内DDL语句结尾加分号(新规则)

**问题**: 达梦存储过程体内每条DDL必须以`;`结尾，SQL Server不要求。

**实现**: `_ensure_ddl_semicolons()`方法(Step 8.5)，用状态机扫描过程体。

**状态机逻辑**:
1. 单行DDL: `DROP TABLE xxx` -> `DROP TABLE xxx;`
2. 跨行建表: 用括号深度跟踪，在`)`行补`;`
3. CTAS跨行: 遇到下条语句开头时给上一行补`;`
4. ON PRIMARY文件组: 去掉后补`;`

**仅对PROCEDURE/FUNCTION/TRIGGER类型执行**。

**验证**: DDL块缺分号数从447降为0。

---

## 修复6: schema_prefix参数贯穿调用链

**问题**: `_convert_split_output()`签名有schema_prefix参数但调用处没传，dbo替换永远不生效。

**修复**: `split_sql_file()`签名增加schema_prefix参数，CLI新增`--schema-prefix`参数默认从输入文件名提取。

**教训**: 新增参数到函数签名时，必须grep所有调用点确保传参。

---

## 批量转换命令

```bash
python3 batch_convert.py <src_dir> <dm_dir> <schema_prefix>
```

HRBI三大库: Stage=54, DW=157, DM=101个, 全部0失败。

---

## 待修复边缘case

1. 少量`CREATE TABLE #xxx`形式的#未被替换(约4-5处)
2. 非临时表SELECT INTO需设计更精确判别逻辑

---

## dbo替换规则演进史（重要教训）

dbo替换逻辑经历了三次重大反复，务必记录以避免未来重蹈覆辙：

### v3.4.5: 两段式无prefix时去掉dbo
- `[dbo].[Users]` → `"Users"` (无prefix时dbo直接删除)
- `dbo.Users` → `Users` (无prefix时dbo直接删除)
- 前提：当时schema_prefix总是从文件名提取，不可能为空

### v3.5.3 (2026-06-27): 错误地"统一删除"dbo
- 昌叔反馈 `[HRBI_Stage].[dbo].[xxx]` 出现双重schema `HRBI_Stage."HRBI_Stage"."xxx"`
- 修复方案：dbo在任何位置都删除
- 结果：`[dbo].[Users]` → `"Users"`（正确），但 `dbo.Users` → `Users`（❌ 昌叔要 `hrbi_stage.Users`）
- 问题根源：混淆了"三段式中dbo是冗余默认schema（该删）"和"两段式中dbo是唯schema标识（该替换）"

### v3.5.4/v3.5.6 (2026-06-27): 正确规则 — 三段式删，两段式替换
- **三段式**（已有其他schema名）: dbo是SQL Server默认schema，直接删除
  - `[HRBI_Stage].[dbo].[Users]` → `"HRBI_Stage"."Users"`
  - `HRBI_Stage.[dbo].[Users]` → `HRBI_Stage."Users"`
- **两段式**（只有dbo）: dbo替换为schema_prefix
  - `[dbo].[Users]` → `"hrbi_stage"."Users"`
  - `dbo.Users` → `hrbi_stage.Users`
- **区分方法**: 正则先匹配三段式（含其他schema名），再匹配两段式（仅dbo）

### ⚠️ dbo替换正则顺序（不可颠倒）
1. 双点号 `xxx..yyy` → `xxx.yyy`（最先，避免被后续规则误匹配）
2. 三段式全引号 `"xxx"."dbo"."yyy"` → `"xxx"."yyy"`
3. 三段式全裸名 `xxx.dbo.yyy` → `xxx.yyy`
4. 三段式混合 `xxx."dbo"."yyy"` → `xxx."yyy"`
5. 两段式有引号 `"dbo"."yyy"` → `"{prefix}""yyy"`
6. 两段式裸名 `dbo.yyy` → `{prefix}.yyy`

### ⚠️ 核心教训
- 不要试图用一个统一的规则处理所有dbo场景
- 三段式和两段式的语义完全不同：一个是冗余中间层，一个是唯一schema标识
- 用户反馈"不对"时，仔细听他说的具体格式和期望输出，不要盲目改代码
- 改完dbo规则后必须跑全量测试（312个存储过程），不能只看几个例子
