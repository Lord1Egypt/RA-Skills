# dm_converter v3.3.0 修复记录

## 修复的问题

### 1. PROCEDURE双重引号bug
- **症状**: `_convert_procedure`输出 `CREATE OR REPLACE PROCEDURE ""sp_test" (p1 INT)" AS`
- **根因**: 三个`re.sub`顺序执行 — 第一个`_format_bracket_params`替换后输出`"sp_test"`，第三个`_fmt_no_param_proc`的正则`PROC\s+(.+?)\s+AS`又匹配到，把`"sp_test" (...)`当name再包引号
- **修复**: 合并为单一正则`_PROC_PATTERN` + 分支回调`_format_proc`，按group(2)/group(3)区分括号参数/无括号参数/无参数
- **调试技巧**: 写独立.py文件跑debug（heredoc+python3 -c容易超时），用`re.findall`+`repr()`逐步追踪每个正则的匹配结果
- **通用教训**: 多个正则顺序替换同类语法时，后面的正则会匹配前面替换的结果

### 2. IDENTITY位置修正
- **症状**: `IDENTITY("id", 1, 1)`插在了`)`前面（表定义内部），不是`)`后面
- **根因**: 正则`\)(\s*$|\s*;|...)`中`)\s*$`匹配到了`VARCHAR(100 CHAR)`行末的`)`（行尾），而非表定义结束的独占一行的`)`
- **修复**: 先删`ON [PRIMARY]`，再优先匹配独占一行的`^(\s*)\)(\s*$)`，fallback到`\)(\s*(?:;|\n|$))`
- **通用教训**: 表定义中列类型的括号`)`和表结束的`)`在正则中难以区分——要求结束括号独占一行

### 3. #临时表正则截断
- **症状**: `CREATE TABLE #TempUsers`的列定义body截断到`NVARCHAR(100`，丢失`)\n)`
- **根因**: `[^)]*`遇`NVARCHAR(100)`的`)`当成表结束括号
- **修复**: 改用`(.+)`贪婪+re.DOTALL匹配到最后一个`)`
- **附加**: `##`→`#tmp_`bug，先替换`##`→`gtmp_`再替换`#`→`tmp_`

### 4. token_map碰撞
- **症状**: 视图转换后字符串`'N/A'`变成了标识符`"v_users"`
- **根因**: Step1 tokenize `'N/A'`→`__TOKEN_0__`，Step3重新tokenize`"v_users"`也分配`__TOKEN_0__`覆盖原值
- **修复**: `_tokenize`新增`start_counter`参数，Step3从`max(original_keys)+1`开始编号

### 5. _quote_name方括号处理
- **症状**: `[dbo].[PROC_xxx]`转换后变成`"dbo]".\"[PROC_xxx"` — 方括号残留在引号内
- **根因**: `_quote_name`先检查整体以`[`开头`]`结尾就剥首尾括号，`[dbo].[PROC_xxx]`整体被剥成`dbo].[PROC_xxx`
- **修复**: 先按`.`拆分，再逐段去方括号/引号

## 质量验证
- 44个单元测试全部通过
- 462个真实SQL对象(HRBI_Stage.sql, 7万行)端到端测试: 0失败, 2秒
- 10项残留检查: 方括号/dbo/@@变量/SET NOCOUNT/GO/GETDATE/ISNULL/双重映射/双点号 均为0
