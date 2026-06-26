# SQL Server -> 达梦数据库转换器设计要点

## 架构

```
convert() 流程:
 Step1: _tokenize() - 字符串/注释 -> 占位符
 Step2: 按对象类型转换 (procedure/function/view/trigger/table/index/constraint)
 Step3: _tokenize() 重新tokenize + 合并token_map
 Step4: 通用转换 (data_types/functions/global_vars/statements/try_catch/transaction)
 Step5: _detokenize() 用合并后的map还原所有占位符
 Step6: _tokenize_strings_only() + _convert_variable_syntax() + detokenize
 Step7: _convert_goto_label()
 Step8: _add_terminator() (仅procedure/function/trigger)
```

## 已修复的坑（v2.4.0及之前）

### 1. token_map 合并
Step2的_convert_procedure等返回token化文本(含__TOKEN_0__)，Step3重新_tokenize产生新map。
如果不合并，Step4 _detokenize用新map找不到__TOKEN_0__的映射。

修复:
```python
original_token_map = dict(token_map) # Step2前保存
tokens, token_map = self._tokenize(result) # Step3
merged_map = dict(original_token_map)
merged_map.update(token_map) # 合并
# Step4用merged_map
result = self._detokenize(result, merged_map)
```

### 2. content = new_content 不可省略
_convert_variable_syntax中全局@替换后忘记`content = new_content`，
导致return content返回的是替换前的文本。

### 3. 嵌套括号匹配
`VARCHAR(100)`中的`)`会截断`[^)]*`，导致参数列表匹配失败。

错误: `r'\(([^)]*)\)'` -> 在`VARCHAR(100)`的`)`处截断
正确: `r'(\([^)]*(?:\([^)]*\)[^)]*)*\))'` -> 匹配嵌套括号

### 4. DECLARE上下文的数据类型
数据类型转换正则的前缀只匹配`,\(\s*|\n\s*`时，
`DECLARE @v_date DATETIME`中的DATETIME不会被匹配。

修复: 前缀加上`DECLARE\s+`

### 5. INSERT INTO误匹配
`\n INSERT INT` 被匹配为: 前缀`\n` + 列名`INSERT` + 类型`INT`
导致INSERT变成INTEGERO

修复方向: 数据类型替换前检查列名是否为SQL关键字(SELECT/INSERT/UPDATE/DELETE等)

### 6. 变量@转换时机
在token保护下做@替换时，__TOKEN_0__等占位符名不含@，安全。
但更安全的做法: 先还原所有token，再用_tokenize_strings_only只保护字符串，
然后做@替换。

### 7. 终止符 /
GO在Step2已被转成/，_add_terminator需要先去掉已有的/再添加新的。
```python
if content.endswith('/'):
    content = content[:-1].rstrip()
```

## 代码审查发现的未修BUG（2026-05-27审查）

用户反馈"达梦转换不好用"，代码审查发现以下严重问题：

### BUG-1: 函数映射转换结果语法错误（严重）

**CONVERT函数** (line 118):
```python
(r'\bCONVERT\s*\(\s*(\w+)\s*,', r'CAST(', True)
```
- 只替换了`CONVERT(type,`为`CAST(`，丢掉了type参数
- SQL Server: `CONVERT(VARCHAR(50), @val)` → 达梦: `CAST(@val AS VARCHAR(50))`
- 参数顺序和格式都不对，需要回调函数重排参数

**DATEADD函数** (line 127-128):
```python
(r'\bDATEADD\s*\(\s*day\s*,', 'CURRENT_TIMESTAMP + ', True)
(r'\bDATEADD\s*\(\s*month\s*,', 'ADD_MONTHS(CURRENT_TIMESTAMP,', True)
```
- 丢了date参数，直接硬编码CURRENT_TIMESTAMP
- SQL Server: `DATEADD(day, 7, @order_date)` → 达梦: `@order_date + 7`
- SQL Server: `DATEADD(month, 3, @start_date)` → 达梦: `ADD_MONTHS(@start_date, 3)`
- 需要回调函数提取3个参数并重排

**DATEDIFF函数** (line 129):
```python
(r'\bDATEDIFF\s*\(\s*day\s*,', '(', True)
```
- 直接替换成`(`，语法彻底崩了
- SQL Server: `DATEDIFF(day, @start, @end)` → 达梦: `@end - @start`（日期差）
- 需要回调函数提取参数

**STRING_AGG函数** (line 115):
```python
(r'\bSTRING_AGG\s*\(', 'LISTAGG(', True)
```
- 达梦LISTAGG需要`WITHIN GROUP (ORDER BY ...)`语法，光改名不够
- SQL Server: `STRING_AGG(name, ',')` → 达梦: `LISTAGG(name, ',') WITHIN GROUP (ORDER BY name)`

**STUFF函数** (line 112):
```python
(r'\bSTUFF\s*\(', 'OVERLAY(', True)
```
- 达梦不支持OVERLAY函数，参数语义也不同
- STUFF(str, start, len, replace) vs OVERLAY不同签名

**REPLICATE函数** (line 113):
```python
(r'\bREPLICATE\s*\(', 'RPAD(', True)
```
- RPAD是右侧填充，REPLICATE是重复字符串，语义不同
- `REPLICATE('0', 5)` = '00000' vs `RPAD('0', 5)` = '0    '

### BUG-2: 变量@转换过于粗暴（严重）

line 671:
```python
new_content = re.sub(r'@([\w]+)', r'\1', content)
```
- 全局替换所有`@word`为`word`，会误改email地址（如`user@example.com`→`userexample.com`）
- 需要增加上下文判断：只替换SQL变量上下文中的@，不替换字符串内的@

**多变量SELECT赋值** (line 659-663):
```python
new_content = re.sub(r'\bSELECT\s+@([\w]+)\s*=', r'\1 :=', content, flags=re.IGNORECASE)
```
- `SELECT @a=1, @b=2` 只处理了@a，@b被遗留
- 需要处理逗号分隔的多变量赋值

**DECLARE变量类型残留** (line 637-642):
```python
new_content = re.sub(r'\bDECLARE\s+@([\w]+)', r'\1', content, flags=re.IGNORECASE)
```
- 只删了DECLARE和@前缀，但达梦过程体内变量声明格式完全不同
- SQL Server: `DECLARE @v_count INT` → 达梦: `v_count INTEGER;`（不需要DECLARE，但需要保留类型+分号）
- 当前输出: `v_count INT`，缺少分号且类型未映射

### BUG-3: TRY-CATCH正则匹配不可靠（中等）

line 590-597:
```python
pattern = (
    r'BEGIN\s+TRY\s*(.*?)\s*END\s+TRY\s*'
    r'BEGIN\s+CATCH\s*(.*?)\s*END\s+CATCH'
)
```
- `.*?`非贪婪匹配在过程体内有多个BEGIN...END时会匹配到错误位置
- 如果TRY块内有`BEGIN...END`嵌套，`END TRY`可能匹配到错误的END
- 需要用括号深度匹配替代纯正则

### BUG-4: GOTO/LABEL误判时间格式（中等）

line 682-687:
```python
new_content = re.sub(r'^(\s*)([\w]+)\s*:\s*$', r'\1<<\2>>', content, flags=re.MULTILINE)
```
- `12:30:00`中的`30:`或`00:`在独立行上会被误判为标签
- 需要排除数字开头的"标签"和已知非标签模式（时间、CASE WHEN等）

### BUG-5: 缺失关键转换（严重）

以下SQL Server常用语法完全没有转换支持：

| SQL Server语法 | 达梦语法 | 当前处理 |
|---------------|---------|---------|
| `#temp_table` / `##global_temp` | 全局临时表GTT或普通表 | 无 |
| `EXEC sp_executesql @sql` | `EXECUTE IMMEDIATE sql_str` | 无 |
| `EXEC(@sql)` | `EXECUTE IMMEDIATE sql_str` | 无 |
| `PRINT 'msg'` | `DBMS_OUTPUT.PUT_LINE('msg')` | 无 |
| `RAISERROR('msg', 16, 1)` | `RAISE_APPLICATION_ERROR(-20001, 'msg')` | 无 |
| `TOP n` | `ROWNUM <= n` 或 `FETCH FIRST n ROWS ONLY` | 无 |
| `[column_name]` | `"column_name"` | 仅token化保护，未转换引号 |
| `MERGE INTO ...` | 语法差异大 | 无 |
| `CURSOR` 游标语法 | 参数/打开/关闭语法差异 | 无 |
| `WITH (NOLOCK)` | 去掉或改写 | 无 |
| `ROW_NUMBER() OVER(...)` | 达梦支持，但分区函数有差异 | 部分支持 |
| `OBJECT_ID('name')` | 达梦用USER_OBJECTS视图 | 无 |
| `IF EXISTS(SELECT ...)` | `SELECT COUNT(*) INTO v_cnt ... IF v_cnt > 0` | 无 |
| `WHILE @i <= 10` | `WHILE i <= 10 LOOP ... END LOOP;` | 无 |

## 改进路线图

### 紧急（语法错误导致转换结果不可用）
1. CONVERT/DATEADD/DATEDIFF — 用回调函数做上下文感知替换，正确重排参数
2. 变量@转换 — 增加上下文判断，避免误改非变量@
3. 补全EXEC动态SQL、临时表、PRINT、RAISERROR、TOP转换

### 重要（转换结果可用但需手动调整）
4. TRY-CATCH — 改用括号深度匹配
5. GOTO/LABEL — 增加排除规则
6. 多变量SELECT赋值
7. DECLARE变量声明格式适配达梦

### 增强（减少手动调整量）
8. STRING_AGG → LISTAGG + WITHIN GROUP
9. STUFF/REPLICATE → 达梦等效写法
10. MERGE语句转换
11. 游标语法转换
12. WITH(NOLOCK)处理

## 映射表

### 数据类型 (40+种)
| SQL Server | 达梦 |
|-----------|------|
| INT | INTEGER |
| BIT | TINYINT |
| DATETIME/DATETIME2 | TIMESTAMP |
| MONEY | DECIMAL(19,4) |
| NVARCHAR(n) | VARCHAR(n) |
| NTEXT | TEXT |
| IMAGE | BLOB |
| UNIQUEIDENTIFIER | VARCHAR(36) |
| XML | TEXT |

### 函数 (30+种)
| SQL Server | 达梦 | 当前状态 |
|-----------|------|---------|
| GETDATE() | CURRENT_TIMESTAMP | OK |
| ISNULL(a,b) | NVL(a,b) | OK |
| LEN(s) | LENGTH(s) | OK |
| SUBSTRING(s,n,l) | SUBSTR(s,n,l) | OK |
| CHARINDEX(s,t) | INSTR(s,t) | OK |
| CONVERT(type,val) | CAST(val AS type) | BUG:参数未重排 |
| DATEADD(day,n,date) | date + n | BUG:丢参数 |
| DATEDIFF(day,s,e) | e - s | BUG:替换成( |
| YEAR(d) | EXTRACT(YEAR FROM d) | OK |
| NEWID() | SYS_GUID() | OK |
| STRING_AGG(col,sep) | LISTAGG(col,sep) WITHIN GROUP(...) | 缺WITHIN GROUP |
| STUFF(str,s,l,r) | 需自定义函数 | BUG:OVERLAY不对 |
| REPLICATE(s,n) | 需自定义或LPAD | BUG:RPAD语义不同 |

### 语句级
| SQL Server | 达梦 | 当前状态 |
|-----------|------|---------|
| SET NOCOUNT ON | -- 注释掉 | OK |
| COMMIT TRANSACTION | COMMIT | OK |
| ROLLBACK TRANSACTION | ROLLBACK | OK |
| BEGIN TRY...CATCH | EXCEPTION WHEN OTHERS | 有嵌套匹配风险 |
| EXEC @sql | EXECUTE IMMEDIATE | 缺失 |
| PRINT 'msg' | DBMS_OUTPUT.PUT_LINE | 缺失 |
| RAISERROR(...) | RAISE_APPLICATION_ERROR(...) | 缺失 |
| TOP n | ROWNUM/FETCH FIRST | 缺失 |
