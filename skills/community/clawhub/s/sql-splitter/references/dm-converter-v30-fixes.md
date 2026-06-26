# dm_converter v3.0 修复记录 (2026-06-13)

v3.0 合并了 v2.4.6 的修复并新增了真实项目验证。

## 修复内容

详见 [v2.4.6修复记录](dm-converter-v246-fixes.md)，包含：
1. 存储过程/函数方括号未替换
2. 捕获组偏移导致双重映射
3. suffix贪婪匹配
4. 双点号`..`语法

## 真实项目验证

### 测试文件: HRBI_Stage.sql
- 源文件: 70,396行, UTF-16编码, 229万字符
- 拆分结果: 462个对象 (373 table + 35 view + 54 procedure)
- 达梦转换: 462/462全部成功, 0失败
- 单元测试: 40/40通过

### 验证要点

1. **方括号替换**: 转换后0个文件残留`[dbo]`（修复前54个procedure全部残留）
2. **双点号替换**: `hrbi_stage..Stage_xxx` → `hrbi_stage.Stage_xxx`，0个文件残留`..`
3. **类型映射**: `[nvarchar](20)` → `VARCHAR(20 CHAR)`, `[bit]` → `BOOLEAN`, `[datetime]` → `TIMESTAMP`
4. **dbo前缀**: `[dbo].[xxx]` → `"HRBI_Stage"."xxx"`

### UTF-16编码处理

SSMS导出的.sql文件常用UTF-16编码，拆分前须转UTF-8:
```python
with open('HRBI_Stage.sql', 'r', encoding='utf-16') as f:
    content = f.read()
with open('HRBI_Stage_utf8.sql', 'w', encoding='utf-8') as f:
    f.write(content)
```

### v22 CLI ImportError 临时方案

`split_sql_v22.py` 导入 `SQLSplitterGUI`（依赖 tkinter），无GUI环境会报错。
临时方案：用 `split_sql_v21.py` 代替（核心拆分逻辑完全相同）:
```bash
python3 split_sql_v21.py input.sql output_dir --dialect sqlserver
```
