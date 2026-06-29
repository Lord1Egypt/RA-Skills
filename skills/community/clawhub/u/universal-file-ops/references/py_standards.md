# Python 编码规范（universal-file-ops 用）

本文档是 `py_tools.py` 的规范化/审查依据。
LLM 在处理 py 文件时，应参照本文档判断代码是否符合规范。

---

## 1. 文件编码

| 规则 | 说明 | 严重程度 |
|------|------|----------|
| 必须无 BOM | UTF-8 BOM（`\xef\xbb\xbf`）会导致 Python 2 兼容问题和部分工具解析异常 | warning |
| 建议添加编码声明 | 第一行（或 shebang 下一行）添加 `# -*- coding: utf-8 -*-` 或 `# coding: utf-8` | info |
| 禁止 GBK/GB2312 | 源文件必须 UTF-8 编码 | error |

**编码声明位置规则：**
- 有 shebang（`#!/usr/bin/env python3`）→ 编码声明在第二行
- 无 shebang → 编码声明在第一行

---

## 2. 缩进与空白

| 规则 | 说明 | 严重程度 |
|------|------|----------|
| 禁止 Tab 缩进 | 必须使用 4 空格缩进，Tab 和空格混用会导致 `IndentationError` | error |
| 禁止行尾空白 | 每行末尾不允许有多余空格或 Tab | warning |
| 文件末尾必须有换行符 | 最后一行应以 `\n` 结尾（POSIX 标准） | warning |
| 换行符必须为 LF（`\n`） | 禁止 Windows 换行符（CRLF，`\r\n`） | warning |

**例外：** 多行字符串（triple-quoted string）内部的换行符保留原样，不触发 CRLF 警告。

---

## 3. 中英文符号规范

> **适用范围：** 仅限「代码区」（不在字符串字面量、注释、docstring 内部）。

| 中文符号 | 应改为 | 说明 |
|----------|--------|------|
| `（` `）` `｜ 中文全角括号 → 英文半角括号 | 代码中的括号必须是英文半角 |
| `【` `】` | `[` `]` | 列表/索引必须用半角 |
| `，` `。` `；` `：` `！` `？` | `,` `.` `;` `:` `!` `?` | 代码区标点必须半角 |
| `"` `"` | `"` `"` | 代码中的引号必须半角（字符串内容除外） |

**不检查区域：**
- 注释（`#` 之后）
- docstring（triple-quoted string）
- 普通字符串字面量

---

## 4. 行长度

| 规则 | 说明 | 严重程度 |
|------|------|----------|
| 行长度 ≤ 120 字符 | 超过 120 字符应换行（优先在括号/方括号/花括号内换行） | info |
| 例外：URL、长字符串 | 无法换行的内容允许超长，但应加 `# noqa` 注释 | info |

---

## 5. import 规范

| 规则 | 说明 |
|------|------|
| 必须按标准库 → 第三方 → 本地模块分组 | 每组之间空一行 |
| 禁止通配符 import | `from module import *` 禁止 |
| 禁止重复 import | 同一模块不重复导入 |
| 禁止循环 import | 模块间不形成循环依赖 |

**正确示例：**
```python
import os
import sys

import requests
import yaml

from myproject import utils
from myproject.model import User
```

---

## 6. 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 函数名 | `snake_case`，动词开头 | `def get_user():` |
| 变量名 | `snake_case` | `user_count = 0` |
| 类名 | `PascalCase` | `class UserManager:` |
| 常量 | `UPPER_SNAKE` | `MAX_RETRY = 3` |
| 私有成员 | 前导单下划线 | `def _internal():` |
| 特殊方法 | 双下划线包裹 | `def __str__(self):` |

---

## 7. 文件规模规范

> **重要：区分「临时脚本」和「正式工具」**（见第 7.5 节）

| 规则 | 说明 | 触发动作 |
|------|------|----------|
| **正式工具**单文件 > 600 行 | 持久化工具必须 OO 化或拆分 | `py_tools.py oo-ify` 输出建议 |
| **临时脚本**单文件 > 600 行 | 豁免 OO 化限制（见 7.5 节） | info（仅提示） |
| 单函数 ≤ 50 行 | 超过 50 行建议拆分 | review 时 warning |
| 单类 ≤ 300 行 | 超过 300 行建议拆分 | review 时 info |

**OO 化判定标准（满足其一即建议 OO 化，仅对正式工具）：**
1. 同一前缀的函数 ≥ 3 个（如 `parse_header` / `parse_body` / `parse_footer`）
2. 函数间共享 ≥ 3 个全局变量
3. 函数参数列表中有 ≥ 3 个相同参数（可提取为实例属性）

---

### 7.5 脚本类型区分

| 类型 | 定义 | 600 行 OO 化限制 | 判断标准 |
|------|------|---------------------|------------|
| **临时脚本** | 一次性任务、临时数据处理、一次性分析、临时测试 | **豁免** | 见下方"如何判断" |
| **正式工具** | skill 脚本、长期维护的工具类脚本、系统级脚本 | **必须 OO 化** | 见下方"如何判断" |

**如何判断脚本类型：**

| 判断标准 | 类型 | 说明 |
|------------|------|------|
| 文件路径在 `skills/` 下 | 正式工具 | skill 脚本是持久化工具 |
| 文件有 shebang 且放在 `/usr/local/bin` 或 `~/bin` | 正式工具 | 系统级工具脚本 |
| 文件是临时生成的（`/tmp`、`/temp`、用户临时目录） | 临时脚本 | 操作系统临时目录 |
| 文件头部有 `# 临时脚本` 或 `# temporary script` 注释 | 临时脚本 | 显式声明 |
| 文件名包含 `temp`、`tmp`、`test_` 前缀且无 shebang | 临时脚本 | 命名暗示一次性使用 |
| 文件在 `scripts/` 下且有 shebang | 正式工具 | 项目级工具脚本 |

**LLM 判断流程：**
1. 检查文件路径 → 在 `skills/` 下？→ 正式工具
2. 检查文件头部 → 有 `# 临时脚本` 注释？→ 临时脚本
3. 检查 shebang → 有且放在系统路径？→ 正式工具
4. 检查目录 → 在临时目录？→ 临时脚本
5. 默认 → 正式工具（保守判断）

---

## 8. docstring 规范

| 规则 | 说明 |
|------|------|
| 公共函数/类必须有 docstring | 使用 triple-quoted string，第一行是简短摘要 |
| 私有函数（`_name`）可不写 | 但建议写注释 |
| 模块级 docstring | 文件第一行，描述模块用途 |

**示例：**
```python
def compute hash(data: str, salt: str = "") -> str:
    """计算数据的哈希值。

    Args:
        data: 原始数据字符串
        salt: 可选盐值

    Returns:
        十六进制哈希字符串
    """
```

---

## 9. normalize 可修复项一览

以下项目 `py_tools.py normalize --fix` 可以自动修复：

| # | 项目 | 修复方式 |
|---|------|----------|
| 1 | UTF-8 BOM | 移除 BOM 字节 |
| 2 | 缺少编码声明 | 在文件头部插入 `# -*- coding: utf-8 -*-` |
| 3 | 编码声明非 utf-8 | 替换为 `coding: utf-8` |
| 4 | Tab 缩进 | 替换为 4 个空格 |
| 5 | 行尾空白 | 去除行尾空格/Tab |
| 6 | 文件末尾无换行 | 追加 `\n` |
| 7 | CRLF 换行符 | 替换为 `\n` |
| 8 | 代码区中文括号 `（）` | 替换为 `()` |
| 9 | 代码区中文引号 `"` `"` | 替换为 `""` |
| 10 | 代码区中文标点 `，；：！？【】` | 替换为英文半角 |

**不可自动修复（需人工确认）：**
- 行长度超过 120（自动换行会在单词中间截断，改变语义）
- 缺少 docstring
- 未使用的 import
- OO 化重构

---

## 10. review 检查项一览

`py_tools.py review` 执行以下检查：

| # | 检查项 | 级别 | 脚本类型判断 |
|---|--------|------|------------|
| 1 | 语法错误（`ast.parse` 失败） | error | 无差别 |
| 2 | 缺少 docstring（公共函数/类） | warning | 无差别 |
| 3 | 文件超过 600 行 | 见下方说明 | **区分类型**（见 7.5 节） |
| 4 | 函数超过 50 行 | info | 无差别 |
| 5 | 未使用的 import（简化启发式） | info | 无差别 |
| 6 | 命名不符合规范 | warning | 无差别 |

**#3 详细说明（脚本类型判断）：**
- **正式工具**（skill 脚本、系统工具）→ 超过 600 行 → `suggest_oo: true`，触发 OO 化建议
- **临时脚本**（一次性任务、临时分析）→ 超过 600 行 → `suggest_oo: false`，仅提示文件行数，豁免 OO 化
- 判断逻辑：见第 7.5 节"如何判断脚本类型"

---

## 11. 错误输出格式规范

> **重要**：本技能是给普通大模型/智能体用户用的，不是给开发者用的。
> 所有错误提示必须**通俗易懂**，带错误码（UFO-XXXX）。

### 11.1 错误响应格式

所有子命令的错误响应必须遵循以下 JSON 格式：

```json
{
  "status": "error",
  "error_code": "UFO-XXXX",
  "script": "脚本名称.py",
  "line": 123,
  "message": "通俗易懂的问题描述",
  "suggestion": "具体可操作的解决建议",
  "detail": "详细错误信息（可选，方便调试）",
  "code": 1
}
```

### 11.2 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | 固定为 `"error"` |
| `error_code` | string | 错误码（UFO-XXXX），详见 `references/error_codes.md` |
| `script` | string | 发生错误的脚本名称（如 `py_tools.py`） |
| `line` | int | 发生错误的大致行号（方便智能体自查） |
| `message` | string | 问题描述（**必须通俗易懂**，不要出现英文技术术语） |
| `suggestion` | string | 解决建议（**必须具体可操作**） |
| `detail` | string | 详细信息（可选，方便调试） |
| `code` | int | 固定为 `1`（表示失败） |

### 11.3 通俗易懂原则

**禁止**出现的表达方式：
- ❌ `"SyntaxError: expected ':'"`
- ❌ `"IndentationError: unexpected indent"`
- ❌ `"ModuleNotFoundError: No module named 'xxx'"`

**推荐**出现的表达方式：
- ✅ `"Python 语法错误：第 365 行缺少冒号 `:"``
- ✅ `"缩进错误：第 205 行缩进不匹配（检测到 Tab 和空格混合）"``
- ✅ `"模块未找到：你没有安装 `xxx` 包（请运行：`pip install xxx`）"``

### 11.4 错误码规范

- 格式：`UFO-XXXX`（Universal File Ops 的缩写）
- 分类：
  - `UFO-1XXX`：文件/路径错误
  - `UFO-2XXX`：语法/编码错误
  - `UFO-3XXX`：环境错误
  - `UFO-4XXX`：网络/包管理错误
  - `UFO-9XXX`：未知错误
- 每个错误码必须在 `references/error_codes.md` 中有详细说明。

### 11.5 成功响应格式

```json
{
  "status": "success",
  "command": "normalize",
  "file": "/path/to/script.py",
  "result": { ... },
  "error": null,
  "code": 0
}
```

---

## 12. 与 PEP 8 的关系

本文档是 PEP 8 的**子集 + 中文开发者特化规则**。
- 与 PEP 8 不冲突，额外增加了「中英文符号规范」和「600 行 OO 化阈值」
- `normalize` 只修复「确定安全」的项目，不自动格式化整个文件（不做 black/yapf 的事）
- 如需完整 PEP 8 格式化，建议额外运行 `black` 或 `autopep8`

---

## 13. 参考资料

- PEP 8 — Style Guide for Python Code
- PEP 263 — Defining Python Source Code Encodings
- Google Python Style Guide
 的关系

本文档是 PEP 8 的**子集 + 中文开发者特化规则**。
- 与 PEP 8 不冲突，额外增加了「中英文符号规范」和「600 行 OO 化阈值」
- `normalize` 只修复「确定安全」的项目，不自动格式化整个文件（不做 black/yapf 的事）
- 如需完整 PEP 8 格式化，建议额外运行 `black` 或 `autopep8`

---

## 12. 参考资料

- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 263 — Defining Python Source Code Encodings](https://peps.python.org/pep-0263/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
