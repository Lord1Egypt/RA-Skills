---
name: task-harness
description: 将需求拆解为结构化任务清单，生成长时运行 Agent 的任务管理系统（基于 Anthropic Effective harnesses 方法论）。当用户需要管理多会话开发任务、跟踪功能完成进度、或要求"拆解任务""任务管理""项目规划"时自动触发
argument-hint: "[项目名称] [需求描述]"
disable-model-invocation: false
user-invocable: true
---

# Task Harness — 结构化任务管理系统

将任意需求拆解为结构化任务清单，为长时运行的 Agent 建立可靠的任务追踪系统。

基于 [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) 方法论。

## 何时使用

- 大型需求需要拆解为多个子任务
- 项目需要跨多个 Agent 会话持续开发
- 需要跟踪功能完成进度（已完成 / 未完成）
- 用户说"拆解任务"、"任务管理"、"项目规划"、"创建任务清单"

## 核心流程

### Step 1: 分析代码库

探索项目结构，理解：
- 技术栈（语言、框架、构建工具）
- 目录结构和架构模式
- 现有配置（package.json、go.mod 等）
- 关键入口文件

### Step 2: 设计任务列表

根据用户需求，将工作拆解为具体的功能点（features）。每个功能点需要：
- 唯一的 `id`（如 `feat-01`、`v2-05`）
- `category` 分类（foundation、layout、components 等）
- `priority` 优先级（数字越小越优先）
- `description` 一句话描述
- `file` 主要涉及的文件路径（可为 null）
- `steps` 具体操作步骤数组（每步一个字符串）
- `passes` 布尔值（初始为 false）
- `verification` 验证条件

### Step 3: 生成 4 个 Harness 文件

在项目根目录生成以下文件：

#### `feature_list.json` — 任务清单（唯一真相来源）

```json
{
  "project": "项目名称",
  "description": "项目描述",
  "features": [
    {
      "id": "feat-01",
      "category": "foundation",
      "priority": 1,
      "description": "一句话描述要做什么",
      "file": "path/to/main/file.js",
      "steps": [
        "具体步骤 1",
        "具体步骤 2"
      ],
      "passes": false,
      "verification": "如何验证这个功能已完成"
    }
  ]
}
```

完整模板见 [references/templates/feature_list.json](references/templates/feature_list.json)

**为什么用 JSON 而不是 Markdown？** 模型倾向于自由改写 Markdown 文件（改写措辞、重组结构、删除内容）。JSON 文件被模型更谨慎对待——更可能只修改特定字段。这对维护任务完整性至关重要。

#### `progress.txt` — 叙事性进度日志

记录每个会话的详细工作内容，供后续会话理解上下文。

完整模板见 [references/templates/progress.txt](references/templates/progress.txt)

#### `init.sh` — 环境初始化脚本

每个新会话开始时运行，5 秒内恢复全部上下文。

完整模板见 [references/templates/init.sh](references/templates/init.sh)

#### `task.json` — 项目总览

记录里程碑、规则、文件清单等项目级信息。

完整模板见 [references/templates/task.json](references/templates/task.json)

### Step 4: 配置 AGENTS.md 规则

在项目的 `AGENTS.md` 文件中添加 Task Management System 章节，确保所有 Agent 会话遵循工作流。参考当前项目的 `AGENTS.md` 中的对应章节。

### Step 5: 首次验证

运行 `bash init.sh`，确认：
- 脚本可正常执行
- feature_list.json 解析正确
- 进度统计准确显示

### Step 6: 输出下一步指引

告诉用户：
- 已创建的文件列表
- 如何开始第一个任务
- 如何在新会话中恢复工作

## Agent 工作流（每个会话）

```
1. bash init.sh                    ← 5 秒上下文恢复
2. Read progress.txt               ← 理解之前做了什么、为什么
3. Read feature_list.json          ← 找到优先级最高的未完成功能
4. Pick 1~2 features               ← 不要贪多，增量推进是关键
5. Execute the feature's steps     ← 严格按步骤执行
6. Verify                          ← 必须实际验证，不要假设
7. Update feature_list.json        ← 只改 passes: false → true
8. git commit                      ← 一个功能一个 commit
9. git push                        ← 同步到远程
10. Append progress.txt            ← 记录本次会话的工作
```

## 严格规则

- **只修改 `passes` 字段**：在 feature_list.json 中，只将 `passes` 从 `false` 改为 `true`。永远不要删除功能、编辑描述、修改优先级或重组 JSON。
- **一次一个功能**：除非功能非常小（例如改一个常量），否则每个会话只做一个功能。
- **必须 commit + push**：每个功能完成后必须 git commit 和 push，确保进度永不丢失且可独立回滚。
- **必须验证后再标记完成**：阅读代码、运行 dev server 或检查输出。不要信任假设。
- **必须更新 progress.txt**：会话结束时更新进度日志，让下一个会话有完整上下文。
- **遇到阻塞时停止**：在 progress.txt 中记录阻塞原因并停止。不要默默绕过问题。

## 文件间关系

```
init.sh ──读取──→ feature_list.json (任务状态)
    │
    └──提示──→ progress.txt (历史上下文)

task.json ────→ 项目总览（里程碑、规则、文件清单）

AGENTS.md ────→ Agent 行为规范（引用 harness 规则）
```

## 引用

- [方法论详解](references/methodology.md) — 为什么用 harness、常见问题、最佳实践
- [模板文件](references/templates/) — 所有 harness 文件的空白模板
