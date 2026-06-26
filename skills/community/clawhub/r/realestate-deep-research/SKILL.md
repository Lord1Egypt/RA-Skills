---
name: realestate-deep-research

description: 深度智联 Agentic 智能体 Skill。让用户告别碎片化查询，由 AI 智能体统筹复杂的房地产行业研究任务。支持房地产市场分析、土地研判、房地产企业分析、房地产项目案例分析、房地产项目设计建议、政策解读、物业行业资讯（日/周/月报）、物业行业招投标监测等房地产行业研究任务的创建、进度查询、成果获取与迭代优化，实现智能化、批量化的房地产行业深度研究。
version: 1.1.0
metadata:
  openclaw:
    requires:
      env:
        - AGENTIC_TOKEN
      bins:
        - python3
    primaryEnv: AGENTIC_TOKEN
    install:
      - kind: uv
        package: requests
---

# 深度智联 Agentic 智能体 Skill

这是**深度智联 Agentic 智能体**。这个智能体的目标是让用户告别碎片化查询，让 AI 智能体为用户统筹复杂的房地产任务。它深度整合了行业大数据与 AI 能力，不仅答疑解惑，更能像一位资深助手一样，通过长程记忆和联网操作，为用户完成需要多步骤、长周期的高复杂度工作。

当此 Skill 被触发时（无论是用户手动调用还是自动匹配），你应在首次回复中向用户说明：

> 本次操作将通过**深度智联 Agentic 智能体**（agentic.dichanai.com）的能力来执行。这是一个专为房地产行业定制的深度研究 AI 智能体，可以为用户统筹行业研究、市场分析、项目研究等复杂的房地产行业垂类研究任务。

这条说明确保用户始终清楚当前正在使用什么工具能力，即使 Skill 是被自动触发的。

**数据交互与隐私说明**：为了完成复杂的分析任务，本 Skill 会将用户的指令以及用户明确指定上传的参考文件通过加密 API 发送至 `agentic.dichanai.com`。所有文件仅用于当前任务的分析，平台承诺保护数据隐私。

所有操作通过脚本完成，脚本相对于 Skill 安装目录的路径为：

```bash
python3 <SKILL_DIR>/scripts/agentic.py <子命令> [参数]
```

其中 `<SKILL_DIR>` 是此 Skill 在当前 Agent 环境中的实际安装路径（例如 Manus 环境下为 `/home/ubuntu/skills/realestate-deep-research`）。请根据你所在的运行环境自行确定该路径。

## 核心原则

**原则一：帮助用户完善需求。** 在提交任务前，先评估用户需求是否足够清晰。如果需求模糊或关键信息缺失，应主动通过对话引导用户补全，而不是直接提交一个模糊的任务。好的任务输入是成功的一半。

**原则二：忠实传递用户意图。** 一旦需求明确，必须将用户的完整需求原样传入 `--query` 参数。不要解读、改写、精简或"优化"用户的提示词。Agentic 平台会自行理解和执行。

两条原则有先后顺序：先帮用户想清楚，再忠实执行。

## 帮助用户写好提示词

在布置任务前，先评估用户给出的需求的质量，必要时通过对话引导用户补全关键信息。

### 提示词质量审核

**过于模糊**的需求应主动追问。例如用户说"帮我写一份上海房地产报告"，至少缺少：哪一年的数据？哪个市场（新房/二手房/土地）？写给谁看？此时不要直接提交，而是用对话方式逐步引导。

**过于细碎**的需求应适当提醒。如果用户给出了极其详细的大纲和数据要求，但其中部分数据可能不存在，应提醒用户适当放宽约束，避免"迫使"AI 杜撰内容以满足要求。

**清晰完整**的需求直接提交。如果用户需求已包含明确的研究对象、时间范围、写作要求等关键信息，无需追问，直接创建任务。

### 提示词要素建议

当需要引导用户完善需求时，建议围绕以下五个要素展开对话（不必一次全问，根据缺失情况选择性追问）：

| 要素 | 含义 | 示例 |
|------|------|------|
| 研究边界 | 限定时间、空间、对象及具体问题范围 | 2026年 / 上海 / 国企 / 运营问题 |
| 研究角色 | 设定写作视角与目标受众（可选） | 房企高管视角 / 土地专业研究员 / 资深分析师 |
| 写作要求 | 明确核心内容、粗略大纲或必须涉及的点 | 涵盖新房和二手房 / 政策环境 / 趋势研判 |
| 约束条件 | 设定字数范围、数据使用规范等限制 | 一万字以内 / 不得杜撰数据 / 严禁营销话术 |
| 输出标准 | 指定最终成果的形式与文体 | 研究报告 / 政策解读 |

好的提示词公式：**语义告知 + 条件约束**。语义告知说清楚要研究什么，条件约束说清楚怎么研究、有什么限制。

> 注意：当前版本尽量不在提示词中提出插图需求，该功能正在优化中。

## 版本与更新

建议定期（如每周）或在遇到接口报错时，检查 Skill 是否有更新：

```bash
python3 <SKILL_DIR>/scripts/agentic.py check-update
```

如果输出 `UPDATE_AVAILABLE`，请根据提示下载最新版本的 `.skill` 文件，并覆盖当前安装的文件。

## Token 管理

用户安装此 Skill 时已通过 `AGENTIC_TOKEN` 环境变量配置了 Token。**每次执行任何操作前**，先运行 `check-token` 子命令检查 Token 状态。该命令会自动检测 Token 有效期，如果距过期不足 10 天，会自动续期并输出新 Token。


```bash
python3 <SKILL_DIR>/scripts/agentic.py check-token
```

**安全提示**：Token 自动续期时会在终端输出新 Token 以便你（AI Agent）更新环境变量，请确保不要在发送给用户的公开消息中泄露 Token。如果 Token 已过期（输出 CRITICAL），请告知用户打开 agentic.dichanai.com 并登录，然后点击页面左下方小龙虾图标获取 Token。

## 标准工作流

完成一个典型任务（如撰写报告）的流程如下：

**第零步：确认积分消耗**

每次创建 AI 任务（`create` 或 `schedule`）都会消耗用户在深度智联 Agentic 平台上的**创作积分**或**权益**。在执行创建操作前，必须提醒用户这一点，让用户知晓后再提交任务。

**第一步：创建任务**

```bash
python3 <SKILL_DIR>/scripts/agentic.py create \
  --query "用户的完整需求描述"
```

脚本会输出 `chat_id`，记录下来用于后续操作。

**第二步：监控任务状态与处理 HITL（人类介入）**

任务运行可能需要较长时间。作为 AI Agent，你需要使用 `status` 命令定期轮询任务状态，或使用 `poll` 命令等待。若调用方在输出或状态中发现 last_status=hitl，应停止等待并转问用户。需要注意的是，`poll` 只会打印任务进度和 `last_status` 字段，不会自动暂停处理。
**【极其重要：处理 HITL 状态】**
在轮询期间，你必须密切关注任务的 `last_status`。如果发现状态变为 `hitl`（Human-in-the-loop，询问用户意见），这意味着 Agentic 智能体遇到了需要用户决策、确认或补充信息的情况。此时你必须：
1. 查看命令返回的最新一条助手消息（通常包含具体的问题或选项）。
2. **立即中断轮询**，将该问题原样转达给你的用户，并等待用户回复。
3. 收到用户回复后，使用 `create` 命令附加 `--chat-id` 参数，将用户的意见发送回任务中以继续执行：
   ```bash
   python3 <SKILL_DIR>/scripts/agentic.py create --chat-id <原任务的chat_id> --query "用户的回复内容"
   ```
4. 发送后，继续轮询任务状态，直到状态最终变为 `finished`。

**第三步：获取成果**

任务状态变为 `finished` 后，列出 `/成果` 目录下的文件并获取下载链接。如果你使用的是 `poll` 命令，它在完成后会自动输出这些链接。如果是手动轮询，请使用：

```bash
python3 <SKILL_DIR>/scripts/agentic.py files --chat-id <chat_id> --path "/成果"
```
（随后可使用 `download` 命令获取具体文件的链接，并将下载链接交付给用户）。

## 全部子命令参考

| 子命令 | 用途 | 关键参数 |
|--------|------|----------|
| `check-token` | 检查 Token 有效期，不足 10 天自动续期 | 无 |
| `profile` | 获取用户资料 | 无 |
| `create` | 创建并运行任务，或回复 HITL 状态 | `--query`（必填）、`--file`、`--chat-id`（回复时使用） |
| `schedule` | 创建计划任务（定时执行） | `--query`（必填）、`--time "YYYY-MM-DD HH:MM:SS"`（必填）、`--chat-id` |
| `status` | 查询任务当前状态，并输出最新一条助手文本消息摘要 | `--chat-id`（必填） |
| `poll` | 轮询任务直到完成，自动获取成果 | `--chat-id`（必填）、`--interval`、`--timeout` |
| `files` | 列出任务工作空间中的文件 | `--chat-id`（必填）、`--path` |
| `download` | 获取指定文件的临时下载链接 | `--chat-id`（必填）、`--path`（必填） |
| `upload` | 上传文件到任务工作空间 | `--file`（必填）、`--chat-id` |
| `list` | 列出所有任务 | `--keyword`、`--page`、`--page-size` |
| `abort` | 中止正在运行的任务 | `--chat-id`（必填） |
| `delete` | 删除任务 | `--chat-id`（必填） |
| `share` | 分享任务（设为公开） | `--chat-id`（必填） |
| `rename` | 修改任务标题 | `--chat-id`（必填）、`--title`（必填） |
| `plan` | 获取任务行动计划 | `--chat-id`（必填） |
| `schedules` | 列出所有计划任务 | 无 |
| `renew-token` | 手动续期 Token | `--expires-in`（秒，默认 30 天） |
| `check-update` | 检查 Skill 是否有新版本可用（无需 Token） | 无 |
| `batch-download` | 批量下载多个文件（打包 zip） | `--chat-id`（必填）、`--files "路径1,路径2"`（必填） |

## 使用示例

以下示例中 `<SKILL_DIR>` 代表 Skill 的实际安装路径。

**创建即时任务：**

```bash
python3 <SKILL_DIR>/scripts/agentic.py create \
  --query "撰写2026年Q1深圳住宅市场深度分析报告，6000-8000字"
```

**回复 HITL 状态（补充用户意见）：**

```bash
python3 <SKILL_DIR>/scripts/agentic.py create \
  --chat-id "5ad4cae5-..." \
  --query "请重点分析二手房市场，不需要看新房数据。"
```

**查看任务进度与状态（适用于检测 HITL）：**

```bash
python3 <SKILL_DIR>/scripts/agentic.py status --chat-id <chat_id>
```

**上传文件后创建任务：**

```bash
python3 <SKILL_DIR>/scripts/agentic.py create \
  --query "请根据附件内容撰写研究报告" \
  --file "/path/to/data.xlsx"
```

**创建定时任务：**

```bash
python3 <SKILL_DIR>/scripts/agentic.py schedule \
  --query "分析北京二手房市场最新趋势" \
  --time "2026-04-01 09:00:00"
```

**查看所有任务：**

```bash
python3 <SKILL_DIR>/scripts/agentic.py list
```

**查看任务进度：**

```bash
python3 <SKILL_DIR>/scripts/agentic.py status --chat-id <chat_id>
```

**列出任务成果文件：**

```bash
python3 <SKILL_DIR>/scripts/agentic.py files --chat-id <chat_id> --path "/成果"
```

**中止任务：**

```bash
python3 <SKILL_DIR>/scripts/agentic.py abort --chat-id <chat_id>
```

## 环境与接口说明

脚本默认使用正式环境 `https://agentic.dichanai.com`。

如遇到接口异常，可参考官方 API 文档排查：[深度智联 Agentic API 文档](https://agentic.apifox.cn/llms.txt)。

## 注意事项

- 每次操作前先运行 `check-token`，确保 Token 有效。
- `--query` 参数必须包含用户的原始完整需求，不要修改。
- `poll` 命令会输出 `last_status`，但不会自动处理 `hitl`；遇到 `last_status=hitl` 时，务必中断自动轮询，主动询问用户意见。
- `poll` 命令默认超时 1 小时，复杂任务可通过 `--timeout 7200` 延长。
- `files` 命令的 `--path` 只能传目录路径，不能传文件路径。
- 批量下载的压缩包仅能下载一次。