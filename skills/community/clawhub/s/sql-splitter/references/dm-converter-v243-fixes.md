# dm_converter v2.4.3 修复记录

## 修复的9个失败测试

从9个失败 → 40/40全部通过。

### 修复1: BIT→BOOLEAN, TINYINT→SMALLINT
- **问题**: type_mappings中 `'bit': 'TINYINT'`, `'tinyint': 'TINYINT'`，但达梦没有TINYINT
- **修复**: `'bit': 'BOOLEAN'`, `'tinyint': 'SMALLINT'`
- **测试**: test_data_types

### 修复2: NVARCHAR(n) → VARCHAR(n CHAR)
- **问题**: NVARCHAR(100)只转成VARCHAR(100)，缺少达梦字符语义CHAR标记
- **根因**: NVARCHAR处理的代码被patch工具放到了`else:`分支内部（即只在suffix为空时执行），导致有suffix时永远无法命中
- **修复**: 将NVARCHAR检查代码从`else:`块内移到`if suffix:` / `else:` 块**之后**（与if/else同级）
- **关键坑**: patch工具插入代码时，缩进层级容易搞错。**必须用`python3 -c`检查实际缩进**：
  ```python
  with open('dm_converter.py') as f:
      for i, line in enumerate(f, 1):
          if i >= 511 and i <= 525:
              spaces = len(line) - len(line.lstrip())
              print(f"{i}: indent={spaces} |{line.rstrip()[:70]}|")
  ```
- **测试**: test_data_types

### 修复3: SET NOCOUNT ON注释格式
- **问题**: 注释`'-- SET NOCOUNT ON (达梦不需要)'`中包含原文`SET NOCOUNT ON`，测试用assertNotIn检测到
- **修复**: 改为`'-- NOCOUNT (达梦不需要)'`，去掉注释中的原文关键字
- **测试**: test_complex_procedure, test_set_nocount_on

### 修复4: DATEADD专用转换
- **问题**: function_mappings中旧的DATEADD条目只做简单前缀替换（如`DATEADD(day,` → `CURRENT_TIMESTAMP +`），不能正确处理3个参数的重排
- **修复**: 
  - 从function_mappings删除旧的DATEADD条目
  - 添加`_parse_function_args()`方法解析嵌套括号的参数列表
  - 添加`_convert_dateadd()`方法，按unit类型重排参数：
    - `DATEADD(day, n, date)` → `date + INTERVAL 'n' DAY`
    - `DATEADD(month, n, date)` → `ADD_MONTHS(date, n)`
    - 其他单位类似
  - 在`_convert_functions()`末尾调用
- **测试**: test_dateadd_conversion

### 修复5: SELECT赋值区分有无FROM
- **问题**: 所有`SELECT @var = expr`都转成`var := expr`，但有FROM子句时达梦需要`SELECT expr INTO var FROM table`
- **修复**: 
  - 添加`_convert_select_assign()`方法
  - 解析赋值列表和FROM子句位置
  - 有FROM: `SELECT @var=expr FROM t` → `SELECT expr INTO var FROM t`
  - 无FROM: `SELECT @var=expr` → `var := expr`
  - 支持多变量赋值: `SELECT @a=col1, @b=col2 FROM t` → `SELECT col1, col2 INTO a, b FROM t`
- **测试**: test_select_into_with_from, test_select_multi_assign, test_select_assign_no_from

### 修复6: IF→THEN/END IF 控制流
- **问题**: `IF @x > 0 BEGIN ... END`没有转换为达梦语法
- **修复**: 添加`_convert_if_else()`方法
  - `IF condition` → `IF condition THEN`
  - BEGIN/END配对：IF后的BEGIN跳过，对应的END改为`END IF;`
  - ELSE保留
- **测试**: test_if_else, test_if_with_try_catch, test_nested_if

### 修复7: WHILE→LOOP/END LOOP
- **问题**: `WHILE @x > 0 BEGIN ... END`没有转换
- **修复**: 添加`_convert_while_loop()`方法
  - `WHILE condition` → `WHILE condition LOOP`
  - WHILE后的BEGIN跳过，对应的END改为`END LOOP;`
- **测试**: test_while_loop

### 修复8: PRINT→DBMS_OUTPUT.PUT_LINE
- **问题**: `PRINT 'text'`没有转换为达梦语法
- **修复**: 添加`_convert_print()`和`_print_replacer()`方法
  - `PRINT expr` → `DBMS_OUTPUT.PUT_LINE(expr);`
  - SQL Server的`+`字符串连接改为达梦的`||`
  - `CAST(...AS VARCHAR)` → `CAST(...AS VARCHAR(4000))`（达梦VARCHAR需要长度）
- **测试**: test_complex_procedure

### 修复9: 流程步骤位置
- 在convert()方法中，Step 5.5后添加控制流和PRINT调用：
  ```python
  # Step 5.5: 控制流转换 (IF/WHILE)
  result = self._convert_if_else(result)
  result = self._convert_while_loop(result)
  
  # Step 5.6: PRINT → DBMS_OUTPUT.PUT_LINE
  result = self._convert_print(result)
  ```
  位于Step 5（变量语法转换）之后、Step 6（GOTO/LABEL）之前

## 开发过程中的关键教训

### ⚠️ write_file工具会添加行号前缀
**问题**: 使用Hermes的`write_file`工具写入Python文件时，内容会被加上` NNN|`格式的行号前缀，导致Python文件损坏（语法错误）。
**修复方法**: 用`terminal`的python脚本或`patch`工具来修改Python文件，**不要用write_file写入代码文件**。如果已经损坏，用以下脚本修复：
```python
import re
with open('file.py', 'r') as f:
    raw = f.read()
lines = raw.split('\n')
cleaned = []
for line in lines:
    m = re.match(r'^\s*\d+\|(.*)$', line)
    if m:
        cleaned.append(m.group(1))
    else:
        cleaned.append(line)
with open('file.py', 'w') as f:
    f.write('\n'.join(cleaned))
```

### ⚠️ patch工具缩进陷阱
patch工具的缩进处理不可靠，尤其是：
1. 多行docstring后的代码体缩进容易错位
2. `else:`块内的代码容易与块外代码混淆
3. **每次patch后必须验证缩进**：用lint检查或`python3 -c "import module"`测试导入
4. 如果lint报`IndentationError`，用`python3 -c`检查精确缩进层级

### ⚠️ git恢复策略
当write_file损坏文件时：
1. `git diff HEAD -- file.py | wc -l` 查看差异量
2. `wc -l file.py && git show HEAD:file.py | wc -l` 对比行数
3. 如果差异巨大且行数骤降，说明文件被截断：`git checkout HEAD -- file.py` 恢复
4. 恢复后重新逐步应用修改
