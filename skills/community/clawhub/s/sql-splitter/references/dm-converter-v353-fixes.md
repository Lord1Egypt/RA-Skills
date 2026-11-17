# dm_converter v3.5.3 修复记录

## 方括号替换规则变更

### 变更内容
`_convert_bracket_identifiers()` 方法从v3.5.3起区分类型名和普通标识符：

| 方括号内容 | v3.5.2及以前 | v3.5.3起 |
|-----------|-------------|---------|
| `[aa]` (列名等) | `aa` (裸名) | `"aa"` (加双引号) |
| `[hrbi].[xxx]` | `"hrbi"."xxx"` | `"hrbi"."xxx"` (不变) |
| `[int]` (类型名) | `int` (裸名) | `int` (裸名，不变) |
| `[nvarchar]` (类型名) | `nvarchar` (裸名) | `nvarchar` (裸名，不变) |

### 代码改动
位置：dm_converter.py 第1630行 `_convert_bracket_identifiers()`

旧逻辑（一行正则替换）：
```python
tokens = re.sub(r'\[([^\]\n]+)\]', r'\1', tokens)
```

新逻辑（回调函数区分类型名）：
```python
type_names_lower = {k.lower() for k in TYPE_MAPPINGS.keys()}

def _replace_bracket(m):
    inner = m.group(1)
    first_token = inner.split()[0].lower() if inner.split() else inner.lower()
    if first_token in type_names_lower:
        return inner  # 类型名：去[]不加双引号
    return f'"{inner}"'  # 非类型名：去[]加双引号

tokens = re.sub(r'\[([^\]\n]+)\]', _replace_bracket, tokens)
```

### 判断逻辑说明
- 取方括号内首段token（空格分隔的第一段），与TYPE_MAPPINGS键集合(小写)匹配
- `[int identity]` → 首段`int`是类型名，内容保留为裸名`int identity`
- 这是正确行为：含后缀的方括号内容只出现在列定义中，后续类型映射会处理

### 用户规则更新
规则1从"[和]去掉不加双引号"改为：
- 非类型名`[aa]`→`"aa"`(去[]加双引号)
- schema/表名`[hrbi].[xxx]`→`"hrbi"."xxx"`(加双引号)
- 类型名`[int]`→`int`/`[nvarchar]`→`nvarchar`(去[]不加双引号，后续做类型映射)

### 测试结果
- 59个单元测试全部通过
- 7条转换规则实际转换验证全部正确
