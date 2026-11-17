# 拆分+转换完整工作流 + 用户反馈理解教训

## 日期: 2026-06-27

## 问题背景

昌叔要求"用sql拆分的skill功能完全拆分出存储过程"，我犯了两个错误：

### 错误1: 只拆分不转换

第一次只用`split_sql_v21.py`拆分后保留了`proc_*.sql`，但这些文件**仍然是原始SQL Server语法**，没有做达梦转换。昌叔说"拆分的不对"，我以为是dbo规则问题，实际上是因为**根本没有做转换这一步**。

**正确流程（SKILL.md v2.4.5章节）：**
1. **拆分**: `unlimited_split.py` 或 `split_sql_v21.py` → 原始SQL Server语法文件
2. **转换**: `batch_convert.py` → 达梦语法文件
3. **过滤**: 从`*_split_dm/`目录只拷贝`proc_*.sql`到最终目录

**教训**: 拆分和转换是两个独立步骤，缺一不可。拆分产出原始语法，转换产出达梦语法。

### 错误2: 误读用户反馈

昌叔说`[dbo].[xxx]`→`"HRBI_Stage"."xxx"`，`dbo.Users`→`HRBI_Stage.Users`，意思是dbo应该**替换为schema_prefix**。但我理解为"dbo统一删除"，把两段式也改成删除了。

**正确理解方式：**
- 昌叔给的格式是明确的输入→输出对照
- 三段式（已有schema名如`HRBI_Stage.[dbo].[xxx]`）: dbo是冗余默认schema→删除
- 两段式（只有dbo如`[dbo].[xxx]`或`dbo.xxx`）: dbo是唯一schema标识→替换为prefix
- 区分方法：正则先匹配三段式（含其他schema名），再匹配两段式（仅dbo）

**教训:**
1. 用户给出具体格式对照时，严格按照格式执行，不要自作主张"统一规则"
2. 三段式和两段式语义完全不同，不能用同一个规则处理
3. 改完dbo规则后必须跑全量测试（312个存储过程），不能只看几个例子

## 正确操作步骤

```bash
# 1. UTF-16转UTF-8（如果文件是UTF-16编码）
python3 -c "open('out.sql','w',encoding='utf-8').write(open('in.sql',encoding='utf-16').read())"

# 2. 拆分（绕过社区版限制）
python3 ~/.hermes/skills/sql-splitter/scripts/unlimited_split.py input_utf8.sql output_split --dialect sqlserver

# 3. 批量转换到达梦语法
python3 ~/.hermes/skills/sql-splitter/scripts/batch_convert.py output_split output_split_dm schema_prefix

# 4. 只提取存储过程
mkdir -p output_split_dm_procs
cp output_split_dm/proc_*.sql output_split_dm_procs/
```

## 质量验证（312个存储过程）

| 检查项 | 结果 |
|--------|------|
| 残留dbo. | 0 |
| 残留@@变量 | 0 |
| 残留GO | 0 |
| 残留GETDATE() | 0（注释中的除外） |
| CREATE OR REPLACE | 312/312 |
| 双重schema | 0 |
| VARCHAR加CHAR | 2057处 |
| SELECT INTO CTAS | 174处 |
| DDL缺分号 | 0 |
