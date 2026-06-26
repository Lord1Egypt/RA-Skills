# Python缩进调试技巧 — dm_converter.py 排坑记录

## 问题场景

Hermes的patch工具修改Python文件中的多行代码时，无法可靠保持原始缩进层级。特别是在if/else块内插入新代码时，新代码可能被放到错误的分支内。

## 典型症状

- `python3 -m py_compile file.py` 报 `IndentationError: expected an indented block`
- 或编译通过但逻辑不生效（代码放在了错误的if/else分支里）
- pytest测试通过但输出值与预期不符

## 诊断方法

### 1. 检查精确缩进（空格数）

```python
with open('file.py') as f:
    lines = f.readlines()
for i in range(START-1, END):
    line = lines[i].rstrip('\n')
    sp = len(line) - len(line.lstrip()) if line.strip() else 0
    print(f"L{i+1:4d} [{sp:2d}] {line[:80]}")
```

### 2. 对比期望缩进层级

`_replace_type` 是嵌套在 `_convert_data_types` 内的闭包函数，缩进层级：
- def _replace_type: 12sp (3级)
- if base_type in self.type_mappings: 12sp
- new_type = ...: 16sp (4级)
- if suffix: / else: 16sp
- if子块内容: 20sp (5级)
- if子块的if: 20sp
- if子块的if子块: 24sp (6级)

### 3. 用xxd确认实际缩进字符

```bash
sed -n '521p' file.py | xxd | head -3
```

空格=0x20，tab=0x09。关键看前几个字节是否和预期缩进层级一致。

## 修复方法

### 方案A：用write_file创建修复脚本

```python
# fix_indent.py
with open('file.py') as f:
    lines = f.readlines()

# 精确修改指定行
lines[517] = "                    new_result = f\"...\"\n"  # 20sp
lines[520] = "                if base_type in ...\n"          # 16sp

with open('file.py', 'w') as f:
    f.writelines(lines)
```

然后 `python3 fix_indent.py && python3 -m py_compile file.py`

### 方案B：用debug脚本对比逻辑

创建一个独立脚本，复制目标函数的相同逻辑但加print调试。如果独立脚本能输出正确结果但原函数不行，说明缩进把代码放到了错误的分支。

## 关键教训

1. **每次patch Python多行代码后，必须 `py_compile` 验证**
2. **py_compile通过不代表逻辑正确** — 代码可能被放到错误的if/else分支（语法合法但语义错误）
3. **read_file的输出格式带行号前缀**（` 521|content`），看不到原始缩进，必须用terminal的python脚本检查
4. **patch工具对缩进不可靠** — 对于Python文件的if/else块内插入，优先用terminal python脚本操作
