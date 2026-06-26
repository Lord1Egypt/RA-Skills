# dm_converter v2.4.5 设计记录 — 方括号→双引号 + dbo前缀 + 精确拆分

## 规则1: 方括号[] → 双引号""

### 设计决策

`_detokenize` 方法中，方括号占位符还原时做转换：

- 普通标识符 `[Users]` → `"Users"`
- SQL类型名 `[nvarchar]` → `nvarchar`（去掉方括号 + 自动做类型映射）
- SQL类型名不能转双引号，否则 `"nvarchar"(100)` 变成标识符而非类型，后续类型映射不生效

### 关键坑：类型名在detokenize时必须同时做映射

**问题链**：
1. `_tokenize` 把 `[nvarchar]` 替换为 `__TOKEN_N__`
2. Step4 `_convert_data_types` 匹配的是裸名 `NVARCHAR`，但此时是占位符，匹配不上
3. `_detokenize` 还原时如果只去掉方括号变成 `nvarchar(100)`，已经过了Step4，不会再被类型映射

**解决**：在 `_detokenize` 中，对类型名直接做映射：
```python
if inner.upper() in _TYPE_NAMES:
    mapped = self.type_mappings.get(inner.lower(), inner)
    replacement = mapped
```

### 关键坑：VARCHAR CHAR语义后处理

detokenize中类型名映射绕过了Step4中 `VARCHAR(n) → VARCHAR(n CHAR)` 的逻辑（因为Step4在token保护下，`[nvarchar]`是占位符匹配不上）。

**解决**：在Step5.4加后处理：
```python
result = re.sub(r'\bVARCHAR\((\d+)\)(?!\s+CHAR\b)', r'VARCHAR(\1 CHAR)', result, flags=re.IGNORECASE)
```

放在Step5 detokenize之后、Step5.5控制流转换之前。

## 规则2: dbo前缀智能处理

### 三段式 vs 两段式判断

| 模式 | 判断依据 | 处理方式 | 示例 |
|------|---------|---------|------|
| `[HRBI].[dbo].[Users]` | dbo前有schema前缀 | 删除dbo. | → `"HRBI"."Users"` |
| `[dbo].[Users]` | dbo前无schema前缀 | 用schema_prefix替换dbo | → `hrbi_stage."Users"` |

### 实现位置

`_convert_dbo_prefix` 方法在 **Step4.5** 执行（detokenize之后），因为：
- detokenize之前：方括号是占位符，正则无法匹配 `__TOKEN_0__.__TOKEN_1__.__TOKEN_2__` 的模式
- detokenize之后：方括号已转为双引号 `"HRBI"."dbo"."Users"`，正则可以匹配

### 正则设计

**三段式**（必须先处理！）：
```python
r'((?:"[^"]*"|\w+)\.)(?:"dbo"|dbo)\.((?:"[^"]*"|\w+))'
# 匹配: "HRBI"."dbo"."Users" 或 HRBI.dbo.Users 或混合
```

**两段式**：
```python
r'"dbo"\.|\bdbo\.'
# 匹配: "dbo"."Users" 或 dbo.Users（两种格式都支持）
```

**重要**：三段式正则中 `"dbo"` 必须同时支持双引号包裹和裸名，因为detokenize后所有方括号标识符都变成了双引号格式。

### schema_prefix来源

从源文件名自动提取：
```python
basename = os.path.splitext(os.path.basename(input_file))[0]
schema_prefix = basename  # 如 hrbi_stage.sql → hrbi_stage
```

在 `_convert_split_output` 中传递，通过 `input_file` 参数。

## 规则3: 精确拆分增强

### `_find_next_create` 兜底函数

当找不到 `;` 或 `GO` 终止符时，用下一个 `CREATE` 关键字作为对象边界上界：

```python
def _find_next_create(sql: str, start: int) -> int:
    # 跳过字符串、注释内的CREATE
    # 匹配独立的CREATE关键字（前后非字母数字下划线）
    # 返回位置或-1
```

### 在 `find_object_end` 中的调用

所有对象类型的终止符查找都有兜底：
```python
end = find_semicolon_end(...)  # 或 find_paren_end / find_block_end
if end >= n:  # 没找到终止符，到达文件末尾
    next_create = _find_next_create(sql, start + 10)
    if next_create > start:
        boundary = next_create
        while boundary > start and sql[boundary - 1] in ' \t\r\n':
            boundary -= 1
        return boundary
```

## 开发过程关键教训

### patch工具Python缩进问题 — 终极解决方案

**问题**：patch工具修改Python文件时，方法体内的缩进经常被破坏（8空格变4空格、1空格等）。

**终极方案：用Python脚本替换整个方法**，而非用patch做局部替换：

```python
#!/usr/bin/env python3
with open('dm_converter.py') as f:
    content = f.read()

old_start = '    def _detokenize(self, content: str, token_map: Dict[str, str]) -> str:'
new_method = '''    def _detokenize(self, content: str, token_map: Dict[str, str]) -> str:
        """docstring"""
        # 方法体（8空格缩进）
        ...
        return content'''

start = content.find(old_start)
end = content.find('        return content', start)
end += len('        return content')
content = content[:start] + new_method + '\n' + content[end:]

with open('dm_converter.py', 'w') as f:
    f.write(content)
```

**原则**：
- 涉及Python方法体修改时，**不要用patch**，用Python脚本替换整个方法
- 每次修改后 `python3 -m py_compile file.py` 验证
- 用 `sed -n 'Np,Mp' file | xxd` 确认精确缩进（xxd显示每个字符的十六进制）
