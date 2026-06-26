# Skill 测试用例 JSON Schema

本文档定义 `skill-test-generate` 输出的 JSON 格式完整规范。

---

## 顶层结构

```json
{
  "schema_version": "1.0",
  "generated_at": "<string, ISO 8601 UTC>",
  "skill": { ... },
  "test_suites": [ ... ],
  "summary": { ... },
  "verified": true
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `schema_version` | string | ✅ | 固定为 `"1.0"` |
| `generated_at` | string | ✅ | ISO 8601 UTC 时间戳，如 `"2026-04-18T22:00:00Z"` |
| `skill` | object | ✅ | 目标 Skill 概览信息 |
| `test_suites` | array | ✅ | 测试套件数组，至少包含 1 个 suite |
| `summary` | object | ⚠️ | 统计摘要，**由 validate 脚本自动生成，不要手动添加** |
| `verified` | boolean | ⚠️ | **由 validate 脚本自动添加，不要手动添加** |

---

## `skill` 对象

```json
{
  "name": "example",
  "description": "示例技能，可回显输入或返回当前时间。",
  "source_path": "/path/to/example",
  "capabilities": ["回显输入", "获取当前时间"]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | Skill 名称，来自 SKILL.md frontmatter |
| `description` | string | ✅ | Skill 描述，来自 SKILL.md frontmatter |
| `source_path` | string | ✅ | Skill 源目录的绝对路径 |
| `capabilities` | string[] | ✅ | Skill 提供的能力列表，每项为一个简短中文描述；至少 1 项 |

---

## `test_suites` 数组

每个元素为一个测试套件（test_suite），代表一个测试维度或一项能力的测试集合。

### test_suite 对象

```json
{
  "suite_id": "TS-01",
  "name": "技能激活与路由",
  "description": "验证 Agent 能否根据用户意图正确识别并激活该技能",
  "capability": "回显输入",
  "cases": [ ... ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `suite_id` | string | ✅ | 套件唯一标识，格式 `TS-XX`（XX 为两位数字，从 01 起） |
| `name` | string | ✅ | 套件名称，简明描述本套件测试的内容 |
| `description` | string | ✅ | 套件详细说明 |
| `capability` | string | ❌ | 仅核心功能 suite 需要，对应 `skill.capabilities` 中的一项 |
| `cases` | array | ✅ | 测试用例数组，至少 1 个 case |

---

## `cases` 数组

每个元素为一个测试用例（test_case），代表一个用户可感知的功能测试场景。

> **设计原则**：测试用例只提供核心信息（case_id、title、scenario、user_input、source_refs）。
> 期望行为、严重度、标签等由测试 Agent 自行判断，不在生成阶段预设。

### test_case 对象

```json
{
  "case_id": "TC-01-001",
  "title": "匹配核心能力时正确激活",
  "scenario": "用户的请求与技能描述中的核心能力匹配",
  "user_input": "帮我回显一段文字 hello",
  "source_refs": [
    { "file": "SKILL.md", "lines": [1, 4] }
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `case_id` | string | ✅ | 用例唯一标识，格式 `TC-XX-YYY`（XX 为 suite 编号，YYY 为 case 序号）；全局唯一 |
| `title` | string | ✅ | 用例标题，简明描述测试什么 |
| `scenario` | string | ✅ | 场景描述，说明本测试的上下文和验证目的 |
| `user_input` | string | ✅ | 模拟用户输入的自然语言文本，必须是用户视角的表述 |
| `source_refs` | array | ✅ | 溯源引用数组，指向目标 Skill 中与该用例相关的源代码位置；至少 1 个引用。详见下方"source_refs 字段" |

---

## `source_refs` 字段

每个测试用例**必须**包含 `source_refs`，用于追溯该用例测试的功能对应到目标 Skill 的哪个源文件的哪些行。这是确保测试用例可追溯（traceability）的关键字段。

### source_ref 对象

```json
{
  "file": "scripts/echo.py",
  "lines": [10, 25]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | string | ✅ | 目标 Skill 中的文件相对路径（相对于 Skill 根目录），如 `"SKILL.md"`、`"scripts/handler.py"` |
| `lines` | integer[] | ✅ | 行号范围 `[start, end]`（含两端），如 `[10, 25]` 表示第 10 到 25 行；start ≤ end；行号从 1 开始 |

**规则**：
- `file` 路径使用 POSIX 风格（正斜杠 `/`），与 `prepare` 命令输出的 `files[].path` 格式一致
- `lines` 必须恰好包含 2 个正整数，且 `lines[0] ≤ lines[1]`
- 一个 case 可以引用多个文件的不同位置（如同时引用 SKILL.md 中的描述和脚本中的实现）
- 对于纯 SKILL.md 描述的功能，`file` 为 `"SKILL.md"`，`lines` 指向描述该功能的段落
- 对于脚本实现的功能，`file` 为脚本路径，`lines` 指向实现该功能的函数/代码块

---

## `summary` 对象

**由 validate 脚本自动生成，不要手动添加。**

```json
{
  "total_suites": 5,
  "total_cases": 15
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `total_suites` | integer | ✅ | 测试套件总数 |
| `total_cases` | integer | ✅ | 测试用例总数 |

---

## 完整示例

以下是一个完整输出示例（以 example skill 为目标）：

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-04-18T22:00:00Z",
  "skill": {
    "name": "example",
    "description": "示例技能，用于测试 Agent Skills 发现与调用。可回显输入或返回当前时间。",
    "source_path": "/path/to/example",
    "capabilities": ["回显输入", "获取当前时间"]
  },
  "test_suites": [
    {
      "suite_id": "TS-01",
      "name": "技能激活与路由",
      "description": "验证 Agent 能否根据用户意图正确识别并激活该技能",
      "cases": [
        {
          "case_id": "TC-01-001",
          "title": "匹配回显能力时正确激活",
          "scenario": "用户请求回显文字，与技能的回显输入能力匹配",
          "user_input": "帮我回显一段文字 hello",
          "source_refs": [
            { "file": "SKILL.md", "lines": [1, 4] }
          ]
        },
        {
          "case_id": "TC-01-002",
          "title": "请求与技能无关时不应激活",
          "scenario": "用户请求翻译，不在该技能能力范围内",
          "user_input": "帮我翻译一段英文",
          "source_refs": [
            { "file": "SKILL.md", "lines": [1, 4] }
          ]
        }
      ]
    },
    {
      "suite_id": "TS-02",
      "name": "回显输入功能",
      "description": "测试技能的文本回显完整功能",
      "capability": "回显输入",
      "cases": [
        {
          "case_id": "TC-02-001",
          "title": "正常回显文本",
          "scenario": "用户提供文本内容请求回显",
          "user_input": "用 example 技能回显 hello world",
          "source_refs": [
            { "file": "SKILL.md", "lines": [6, 10] },
            { "file": "scripts/handler.py", "lines": [15, 30] }
          ]
        },
        {
          "case_id": "TC-02-002",
          "title": "未提供回显内容时的处理",
          "scenario": "用户请求回显但未指定文本",
          "user_input": "用 example 技能回显一下",
          "source_refs": [
            { "file": "scripts/handler.py", "lines": [32, 40] }
          ]
        }
      ]
    },
    {
      "suite_id": "TS-03",
      "name": "获取时间功能",
      "description": "测试技能的获取当前时间完整功能",
      "capability": "获取当前时间",
      "cases": [
        {
          "case_id": "TC-03-001",
          "title": "请求获取当前时间",
          "scenario": "用户请求查看当前时间",
          "user_input": "现在几点了？",
          "source_refs": [
            { "file": "SKILL.md", "lines": [12, 15] },
            { "file": "scripts/handler.py", "lines": [42, 55] }
          ]
        }
      ]
    },
    {
      "suite_id": "TS-04",
      "name": "多步工作流",
      "description": "验证 Skill 是否能被连续调用完成组合任务",
      "cases": [
        {
          "case_id": "TC-04-001",
          "title": "连续调用回显和获取时间",
          "scenario": "用户先后请求回显和获取时间",
          "user_input": "先回显 test，再告诉我现在几点",
          "source_refs": [
            { "file": "scripts/handler.py", "lines": [15, 55] }
          ]
        }
      ]
    },
    {
      "suite_id": "TS-05",
      "name": "指令可理解性",
      "description": "验证 SKILL.md 正文中的指令对 Agent 是否清晰可执行",
      "cases": [
        {
          "case_id": "TC-05-001",
          "title": "步骤引用的资源是否存在",
          "scenario": "检查 SKILL.md 中引用的脚本和参考文档是否在对应目录中存在",
          "user_input": "（静态检查，无用户输入）",
          "source_refs": [
            { "file": "SKILL.md", "lines": [20, 45] }
          ]
        },
        {
          "case_id": "TC-05-002",
          "title": "指令是否有歧义或矛盾",
          "scenario": "检查 SKILL.md 正文中是否存在模糊或矛盾的指令描述",
          "user_input": "（静态检查，无用户输入）",
          "source_refs": [
            { "file": "SKILL.md", "lines": [20, 45] }
          ]
        }
      ]
    },
    {
      "suite_id": "TS-06",
      "name": "异常与安全",
      "description": "验证面对异常输入时是否安全处理",
      "cases": [
        {
          "case_id": "TC-06-001",
          "title": "handler 收到未知 action 的容错",
          "scenario": "handler 收到未定义的 action 参数",
          "user_input": "用 example 技能执行 dance 动作",
          "source_refs": [
            { "file": "scripts/handler.py", "lines": [10, 14] }
          ]
        },
        {
          "case_id": "TC-06-002",
          "title": "回显特殊字符内容的安全性",
          "scenario": "用户请求回显含特殊字符的内容",
          "user_input": "用 example 技能回显 <script>alert(1)</script>",
          "source_refs": [
            { "file": "scripts/handler.py", "lines": [15, 30] }
          ]
        }
      ]
    }
  ]
}
```
