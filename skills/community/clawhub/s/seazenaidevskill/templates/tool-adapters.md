# 工具适配器

> 本文件定义研发统筹智能体所需的"通用能力"，以及各 AI 编程工具的对应调用方式。
> Agent 运行时先读此文件，根据当前工具选择正确的调用方式。
> 新增工具时，在对应能力表格下加一行即可。

---

## 能力一：飞书项目管理 (Meegle)

> 用于在飞书项目中创建/更新需求、子任务、缺陷，以及流转状态。

| 工具 | 调用方式 |
|------|---------|
| Claude Code | 使用 `Skill("meegle")` 工具，传入 meegle CLI 命令（如 `workitem create`、`workflow transition` 等） |
| Codex | 在终端执行 meegle CLI 命令（需预先安装 Meegle CLI） |
| Trae | 通过 MCP 工具调用飞书项目 OpenAPI |
| WorkBuddy | 在终端执行 meegle CLI 命令（需预先安装 Meegle CLI） |

### Meegle 命令速查

| 操作 | meegle CLI 命令 |
|------|----------------|
| 搜索空间 | `project search [--project-key <key>]` |
| 获取工作项类型 | `workitem meta-types --project-key <key>` |
| 获取字段定义 | `workitem meta-fields --work-item-type <type> --project-key <key>` |
| 获取角色定义 | `workitem meta-roles --work-item-type <type> --project-key <key>` |
| 创建工作项 | `workitem create --work-item-type <type> --project-key <key> --fields [...]` |
| 更新工作项 | `workitem update --work-item-id <id> --project-key <key> --fields [...]` |
| 查询工作项 | `workitem query --project-key <key> --mql "<MQL>"` |
| 创建子任务 | `subtask update ...` |
| 节点流转 | `workflow transition --work-item-id <id> --action confirm` |
| 状态流转 | `workflow transition-state --work-item-id <id> --transition-id <id>` |
| 搜索用户 | `user search --user-keys <name/email>` |
| 获取状态流转 | `workflow list-state-transitions --work-item-id <id>` |

## 能力二：向用户提问

> 用于多轮对话中收集信息、确认决策。

| 工具 | 调用方式 |
|------|---------|
| Claude Code | 直接输出问题文本，或使用 `AskUserQuestion` 工具提供选项 |
| Codex | 直接输出问题文本 |
| Trae | 直接输出问题文本 |
| WorkBuddy | 直接输出问题文本 |

## 能力三：文件操作

> 用于读取/写入项目文件。所有主流工具均支持，无需额外适配。

| 操作 | 说明 |
|------|------|
| 读取文件 | 读取项目中的 `.seazenai/`、`docs/`、源代码等文件 |
| 写入文件 | 写入需求文档、任务拆解、测试用例等到 `.seazenai/` 目录 |

## 适用场景

当 AGENT.md 流程中提到如下指令时，按本适配器执行：

- "调用飞书项目管理工具创建需求" → 查「能力一」中当前工具的调用方式，使用 `workitem create`
- "调用飞书项目管理工具更新状态" → 查「能力一」，使用 `workflow transition` 或 `workflow transition-state`
- "向用户提问" → 查「能力二」
