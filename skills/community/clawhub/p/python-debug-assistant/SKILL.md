---
name: python-debug-assistant
description: Python代码调试助手。帮助诊断和修复Python代码错误，覆盖SyntaxError、TypeError、NameError等10+常见错误类型，提供错误解读、代码定位、修复方案和调试技巧。
version: "2.0"
---

# Python Debug 助手

当用户提交 Python 报错信息或代码问题时，按以下流程诊断并给出修复方案。

## 执行流程

### 步骤 1：解析输入

判断用户输入包含哪些信息：

| 输入组合 | 执行分支 |
|----------|----------|
| 错误信息 + 代码片段 | → 步骤 2（完整诊断） |
| 只有错误信息（无代码） | → 步骤 2A（解释错误 + 常见原因） |
| 只有代码（无报错） | → 步骤 2B（静态检查潜在问题） |
| 截图/图片 | → 先提取文字，再判断属于以上哪种 |

### 步骤 2：完整诊断

当用户提供了错误信息和代码时：

1. **解析 traceback**：提取错误类型、错误消息、出错文件及行号
2. **对照错误类型表**：确定错误类别（见下方速查表）
3. **定位问题代码**：指出具体哪一行/哪段代码导致问题
4. **分析根因**：解释为什么会发生这个错误

### 步骤 2A：仅错误信息

给出：
- 错误类型的通俗解释
- 该错误最常见的 2-3 种原因
- 提示用户贴出相关代码以便进一步诊断

### 步骤 2B：仅代码（静态检查）

逐项检查：
1. 语法问题：括号匹配、冒号、缩进一致性
2. 变量使用：是否先定义后使用、拼写是否正确
3. 类型匹配：运算/函数调用的参数类型是否合理
4. 导入语句：模块名是否正确、是否已安装
5. 边界条件：索引范围、字典键存在性、除零等

### 步骤 3：生成修复方案

1. 给出具体修改步骤
2. 提供修改后的正确代码（标注改了哪里）
3. 如果存在多种修复方式，给出最简洁的一种

### 步骤 4：附加调试建议

根据错误类型推荐对应的调试方法：
- 简单错误（语法/命名）→ 推荐 IDE 提示 + 仔细检查
- 逻辑错误 → 推荐 print 调试或 pdb 断点
- 偶发错误 → 推荐 logging 日志
- 类型相关 → 推荐 type() / isinstance() 检查

## 错误类型速查表

| 错误类型 | 关键词识别 | 常见原因 | 检查方向 |
|----------|-----------|----------|----------|
| SyntaxError | "invalid syntax" | 拼写、括号、冒号 | 语法规则 |
| IndentationError | "unexpected indent" | 缩进不一致 | 空格/Tab 混用 |
| NameError | "name 'x' is not defined" | 变量未定义 | 变量拼写、作用域 |
| TypeError | "unsupported operand type" | 类型不匹配 | 操作数类型 |
| IndexError | "list index out of range" | 索引越界 | 列表长度 |
| KeyError | "KeyError: 'x'" | 键不存在 | 字典键名 |
| ValueError | "invalid literal" | 值不合法 | 类型转换 |
| AttributeError | "has no attribute" | 属性/方法不存在 | 对象类型 |
| ImportError | "No module named" | 模块未安装 | 包名拼写 |
| FileNotFoundError | "No such file" | 文件路径错误 | 路径检查 |

## 输出模板

严格按以下结构输出诊断结果：

```
## 🔍 问题分析
- **错误类型**：[错误类型名称]
- **错误信息**：[原始错误信息解读]
- **根因分析**：[为什么会出错，用通俗语言解释]

## 📍 问题定位
[指出具体出错的代码行，引用原始代码]

## ✅ 修复方案
[修改步骤说明]

[修改后的完整代码，关键改动处加注释标注]

## 💡 调试建议
[1-2 条针对性的调试技巧]
```

## 触发场景

以下表述应触发此 skill：
- "帮我 debug / 调试一下"
- "这个 Python 代码报错了"
- "为什么运行不了 / 报这个错"
- "这段代码有什么问题"
- "帮我看看这个错误"
- "Python 报错怎么解决"

## 使用示例

### 用户输入

```
Traceback (most recent call last):
  File "test.py", line 3, in <module>
    print(x + y)
NameError: name 'y' is not defined

代码：
x = 1
print(x + y)
```

### 预期输出

```
## 🔍 问题分析
- **错误类型**：NameError
- **错误信息**：变量 'y' 未被定义就尝试使用
- **根因分析**：代码中只定义了 x = 1，但 print 语句中引用了未定义的变量 y。
  Python 在执行时找不到 y，因此抛出 NameError。

## 📍 问题定位
第 3 行 `print(x + y)` — 变量 y 在此处首次出现但从未被赋值。

## ✅ 修复方案
在使用 y 之前先定义它：

x = 1
y = 2  # ← 新增：定义变量 y
print(x + y)  # 输出 3

## 💡 调试建议
- 使用 IDE 的自动补全功能可以减少变量名拼写错误
- 遇到 NameError 时，用 `print(dir())` 查看当前作用域中已定义的变量名
```

## 参考资料

- Python 内置异常文档：https://docs.python.org/3/library/exceptions.html
- 错误速查表（含详细示例）：[references/common-errors.md](references/common-errors.md)
- 调试工具使用指南：[references/debugging-tools.md](references/debugging-tools.md)
