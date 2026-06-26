---
name: skill-test-generate
description: 为任意 Agent Skill 自动生成 SFT 级别的功能测试用例，JSON 格式结构化输出。适用于生成测试用例、测试Skill、SFT测试、功能验证、技能测试、测试生成等场景。
---

# Skill 测试用例生成器

基于 **Agent 语义理解**，为任意遵循 [Agent Skills 标准](https://agentskills.io/specification) 的 Skill 自动生成 **SFT（功能测试）** 级别的测试用例，以 JSON 格式结构化输出。

## 设计理念

- **使用者视角**：测试粒度是 Skill 使用者（LLM Agent）能够理解和操作的功能层面，不拆到字段级或行级的单元测试
- **通用兼容**：不绑定特定平台，兼容有 handler（可执行型）和纯 prompt（指令型）两种 Skill 形态
- **语义驱动**：由 Agent 读取 Skill 文件并理解其语义，据此生成测试用例，不依赖正则匹配
- **精简输出**：测试用例只提供核心字段（case_id、title、scenario、user_input、source_refs），期望行为、严重度、标签等由测试 Agent 自行判断

## 输入：指定目标 Skill

用户必须指定要生成测试的目标 Skill，支持以下形式：

| 用户说 | 目标参数 |
|-------|---------|
| "为已安装的 `pdf` skill 生成测试" | `installed:pdf` |
| "为 `/path/to/my-skill` 目录生成测试" | `/path/to/my-skill` |
| "为这个 zip 生成测试：`/tmp/my-skill.zip`" | `/tmp/my-skill.zip` |

## 输出：结构化 JSON

输出 JSON 的完整 Schema 定义见 `references/test-schema.md`。核心结构概要：

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO 8601 UTC 时间戳>",
  "skill": {
    "name": "...",
    "description": "...",
    "source_path": "...",
    "capabilities": ["能力1", "能力2"]
  },
  "test_suites": [
    {
      "suite_id": "TS-01",
      "name": "技能激活与路由",
      "description": "...",
      "cases": [
        {
          "case_id": "TC-01-001",
          "title": "...",
          "scenario": "...",
          "user_input": "...",
          "source_refs": [
            { "file": "SKILL.md", "lines": [1, 10] }
          ]
        }
      ]
    }
  ],
  "summary": { ... }
}
```

> **注意**：`summary` 字段**不要手动添加**——由 `validate` 子命令根据 `test_suites` 自动统计生成。

## 5 大测试维度

从 Skill 使用者视角出发，按以下 5 大维度生成测试用例。每个维度对应一个或多个 test_suite：

### 1. 技能激活与路由（suite_id 前缀: TS-01）

验证 Agent 能否根据用户意图正确识别何时该/不该激活此 Skill。

**典型用例**：
- ✅ 用户意图匹配 Skill 核心能力 → 应激活
- ✅ 用户意图与 Skill 无关 → 不应激活
- ✅ 用户意图模糊，处于边界 → 应能合理处理

### 2. 核心功能（suite_id 前缀: TS-02 起，每项能力一个 suite）

对 Skill 声称的**每项能力**分别生成测试。从 SKILL.md 的 description、body、handler 的 input_schema 或正文描述中提取能力列表，每项能力对应一个 test_suite。

**典型用例**：
- ✅ 正常输入 → 功能按预期工作
- ✅ 空输入或缺少必要参数 → 优雅处理
- ✅ 特殊/边界输入 → 不崩溃，合理响应

### 3. 多步工作流（suite_id 前缀: 倒数第二个 suite）

验证 Skill 是否支持连续/组合调用完成组合任务。

**典型用例**：
- ✅ 先调用能力 A，再调用能力 B → 两步均成功
- ✅ 同一 Skill 被连续调用 → 不出现状态残留或冲突

### 4. 指令可理解性（suite_id: 倒数第二个+1）

验证 SKILL.md 正文中的指令对 Agent 是否清晰可执行。

**典型用例**：
- ✅ 正文引用的脚本/参考文档是否存在
- ✅ 指令步骤是否完整，是否有歧义或矛盾
- ✅ 缺少必要信息时 Agent 是否能判断

### 5. 异常与安全（最后一个 suite）

验证面对异常/恶意输入时是否安全处理。

**典型用例**：
- ✅ 超长输入 → 不崩溃
- ✅ 特殊字符/注入尝试 → 安全处理
- ✅ 无效参数组合 → 不崩溃，返回有意义的错误

## Agent 工作流

### 步骤 1 — 收集目标与输出路径

向用户询问（或从上下文推断）：
1. **目标 Skill**：已安装名称、目录路径或 zip 文件路径
2. **输出路径**：JSON 结果写入位置（如 `./my-skill-tests.json`）

如果都未指定，提示用户。

### 步骤 2 — 准备 Skill 文件

使用辅助脚本解析 Skill 路径并列出所有文件：

```bash
python scripts/generate.py prepare --skill <target>
```

其中 `scripts/generate.py` 位于：
`~/.workbuddy/skills/skill-test-generate/scripts/generate.py`

此命令会：
- 解析 `installed:<name>`、目录或 zip 路径
- 输出 JSON：`skill_name`、`skill_path`、`files`（`{path, size, line_count}` 列表）、`file_index`（path → {size, line_count} 映射）、`frontmatter`（name, description 等元数据）
- `line_count` 可帮助你为 `source_refs` 填写准确的行号范围

如果目标是 zip，会解压到临时目录（路径包含在输出中）。

### 步骤 3 — 阅读全部 Skill 文件

**⛔ 必须阅读目标 Skill 中的所有文件**，不要只看 SKILL.md。脚本、参考文档中可能包含 SKILL.md 未提到的能力或约束。

**首先阅读 SKILL.md**，获取：
- Skill 的用途和声称的能力
- 使用方式和触发条件
- 工作流步骤和脚本调用约定

**然后逐一阅读** `scripts/` 和 `references/` 下的所有文件，理解：
- 脚本的实际行为和参数
- 参考文档中的额外约束或能力
- 代码中的边界处理和错误处理逻辑

### 步骤 4 — 提取能力列表并规划测试

基于对 Skill 的完整理解，提取能力列表。能力来源优先级：
1. SKILL.md 正文明确描述的能力
2. handler 的 input_schema 中定义的 action/功能
3. 脚本的子命令或主要功能

然后按 5 大维度规划 test_suite 结构：
- **TS-01**：技能激活与路由（1 个 suite，2-4 个 cases）
- **TS-02 ~ TS-N**：核心功能（每项能力 1 个 suite，每个 suite 2-5 个 cases）
- **TS-N+1**：多步工作流（1 个 suite，1-3 个 cases；若 Skill 仅有一项能力可省略）
- **TS-N+2**：指令可理解性（1 个 suite，2-4 个 cases）
- **TS-N+3**：异常与安全（1 个 suite，2-4 个 cases）

### 步骤 5 — 生成测试用例 JSON

按 `references/test-schema.md` 中定义的格式组装完整 JSON。

**用例编写原则**：
- 每个 case 的 `user_input` 必须是**用户视角的自然语言**，不是 API 调用
- `scenario` 要说明这个测试场景在验证什么
- `source_refs` 要指向目标 Skill 中与该用例直接相关的源代码位置

**⚠️ 不要手动添加 `summary` 字段**——由 validate 脚本自动生成。

#### 🎯 边界用例覆盖指引

生成测试用例时，**不仅要覆盖 happy_path，还要系统性地挖掘边界和异常场景**。以下清单帮助确保覆盖面足够广：

**输入边界**：
- 空输入 / 缺少必要参数
- 超长输入（文本、列表、嵌套结构）
- 特殊字符输入（Unicode、表情符号、控制字符、HTML/JS 代码）
- 负数、零、极大值等数值边界
- 格式错误的输入（如期望 JSON 但给了纯文本）

**功能边界**：
- 同一能力的不同参数组合（最小参数集 vs 全参数集）
- 能力的可选参数省略时的行为
- 参数间的依赖关系和互斥关系
- 幂等性：同一请求多次执行是否结果一致

**路由边界**：
- 与 Skill 能力**部分相关**的模糊意图
- 多个 Skill 都可能匹配的意图（歧义场景）
- 用户使用了 Skill 能力的**同义词/俗称**

**状态与上下文边界**：
- Skill 连续调用后是否有状态残留
- 前一次调用失败后再次调用的恢复行为
- 并发请求（如果 Skill 设计支持）

**指令完整性**：
- SKILL.md 中引用的脚本/文件是否实际存在
- 工作流步骤是否有缺失或顺序矛盾
- 参考文档中的约束是否在正文中也有说明

#### 📍 source_refs 填写要求

每个测试用例**必须**填写 `source_refs`，指向目标 Skill 中与该用例直接相关的源代码位置：

- **纯描述型功能**：`file` 为 `"SKILL.md"`，`lines` 指向描述该功能的段落
- **脚本实现型功能**：`file` 为脚本相对路径（如 `"scripts/analyze.py"`），`lines` 指向实现该功能的函数/代码块
- **跨文件功能**：可引用多个文件，如同时引用 SKILL.md 的描述段落和脚本中的实现代码
- **行号范围**：使用 `[start, end]` 格式，尽量精确定位到相关代码段落，不要过大也不要过小
- **路径格式**：使用 POSIX 风格（正斜杠 `/`），与 `prepare` 命令输出一致

**填写策略**：在步骤 3 阅读 Skill 文件时，同时记录每个功能对应的文件和行号范围，这样在步骤 5 生成用例时可以直接引用。

### 步骤 6 — ⛔ 强制验证输出（必须执行）

**在写入 JSON 文件后、向用户展示结果前，必须调用验证脚本校验输出格式：**

```bash
python scripts/generate.py validate --file <输出 JSON 文件路径> --skill <目标 Skill 路径>
```

> `--skill` 参数可选。如果提供，validate 会校验 `source_refs` 中引用的文件是否存在、行号是否超出实际行数。强烈建议提供此参数以确保溯源信息准确。如果省略，则从 JSON 的 `skill.source_path` 推断。

验证脚本会检查：
- 顶层结构完整性（`schema_version`、`generated_at`、`skill`、`test_suites`）
- 每个 suite 的必填字段和字段类型
- 每个 case 的必填字段（`case_id`、`title`、`scenario`、`user_input`、`source_refs`）
- `case_id` 全局唯一性
- `source_refs` 格式正确性（`file` 非空字符串、`lines` 为 2 个正整数且 start ≤ end）
- `source_refs` 文件存在性（如果提供了 `--skill` 参数）
- `source_refs` 行号不超出文件实际行数（如果提供了 `--skill` 参数）

**验证不通过时**：脚本会输出详细的错误列表。你必须根据错误修正 JSON 文件，然后重新运行验证，直到通过。

**验证通过时**：脚本会自动从 `test_suites` 生成 `summary`（各项计数），并在 JSON 文件中添加 `"verified": true` 字段。

**⛔ 跳过此步骤的输出结果视为无效，不可作为最终交付。**

### 步骤 7 — 展示结果

读取 JSON 输出，以人类可读的摘要呈现：
- Skill 概览（名称、能力列表）
- 各测试套件的用例数和覆盖范围
- 总用例数统计

## 辅助脚本命令

`scripts/generate.py` 辅助脚本提供以下子命令：

| 命令 | 用途 |
|------|------|
| `prepare --skill <target>` | 解析路径、列出文件（含行数）、提取 SKILL.md 元数据 |
| `validate --file <json路径> [--skill <skill路径>]` | ⛔ 验证输出 JSON 格式，校验 source_refs，自动生成 `summary`，通过后添加 `verified: true` |

## 纯 prompt 型 Skill 的处理

对于没有 handler、没有 scripts，仅通过 SKILL.md 正文向 Agent 提供指令的 Skill：
- **核心功能**测试关注 Agent 能否根据正文指令正确执行
- **多步工作流**关注 Agent 是否按正文步骤顺序执行
- 不生成涉及脚本/参数的测试用例，改为生成指令理解类用例

## 注意事项

- 辅助脚本仅使用 Python 标准库，无需安装第三方依赖
- 在 **Windows** 上注意路径分隔符和临时目录差异
- 始终阅读**所有**文件，而非仅 SKILL.md，以捕获隐藏的能力和约束
- 测试用例粒度保持**功能级**：一个 case 验证一个用户可感知的功能场景，不要拆成字段级的单元测试
- Agent 的语义理解是主要的测试生成方法——不使用正则模式提取
